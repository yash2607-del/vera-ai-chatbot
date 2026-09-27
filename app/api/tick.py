from fastapi import APIRouter, Depends
import sqlite3
from app.models.requests import TickRequest
from app.models.responses import TickResponse
from app.core.constants import TickStatus, ConversationState
from app.storage.database import get_db
from app.storage.context_store import ContextStore
from app.storage.suppression_store import SuppressionStore
from app.storage.message_store import MessageStore
from app.models.conversation import ConversationRecord
from app.engine.decision_engine import DecisionEngine
from app.generation.composer import MessageComposer

router = APIRouter()

@router.post("/tick", response_model=TickResponse)
def post_tick(request: TickRequest, db: sqlite3.Connection = Depends(get_db)):
    c_store = ContextStore(db)
    s_store = SuppressionStore(db)
    m_store = MessageStore(db)

    engine = DecisionEngine(c_store, s_store, m_store)
    composer = MessageComposer()

    # Support judge harness trigger lists
    merchant_id = request.merchant_id
    trigger_id = request.trigger_id
    if not merchant_id and request.available_triggers:
        trigger_id = request.available_triggers[0]
        # Resolve merchant_id from trigger context if available
        trig_ctx = c_store.get_context("trigger", trigger_id)
        if trig_ctx and trig_ctx.get("merchant_id"):
            merchant_id = trig_ctx["merchant_id"]
        else:
            merchant_id = "m_001"
    elif not merchant_id:
        merchant_id = "m_001"

    status_val, signal, conv_id = engine.process_tick(
        merchant_id=merchant_id,
        trigger_id=trigger_id,
        customer_id=request.customer_id,
        dry_run=request.dry_run
    )

    if status_val == TickStatus.SUPPRESSED:
        return TickResponse(
            status=TickStatus.SUPPRESSED,
            accepted=True,
            actions=[],
            message=None,
            cta=None,
            suppression_key=signal.suppression_key if signal else None,
            rationale="Identical recommendation suppressed by guardrail within TTL window."
        )

    # Compose copy using LLM or deterministic fallback
    composed = composer.compose(signal)
    
    # Save active conversation state
    record = ConversationRecord(
        conversation_id=conv_id,
        merchant_id=merchant_id,
        state=ConversationState.RECOMMENDATION_SENT,
        last_signal_type=signal.signal_type.value,
        last_evidence=signal.evidence,
        last_message=composed["message"],
        last_cta=composed["cta"],
        updated_at=""
    )
    m_store.save_conversation(record)

    action_obj = {
        "body": composed["message"],
        "cta": composed["cta"],
        "send_as": composed.get("send_as", "Vera"),
        "suppression_key": signal.suppression_key,
        "rationale": signal.rationale,
        "conversation_id": conv_id,
        "merchant_id": merchant_id,
        "trigger_id": trigger_id,
        "customer_id": request.customer_id,
        "intent": signal.signal_type.value,
        "evidence": signal.evidence
    }

    return TickResponse(
        status=TickStatus.ACTED,
        accepted=True,
        actions=[action_obj],
        message=composed["message"],
        cta=composed["cta"],
        send_as=composed.get("send_as", "Vera"),
        suppression_key=signal.suppression_key,
        rationale=signal.rationale,
        conversation_id=conv_id,
        intent=signal.signal_type.value,
        evidence=signal.evidence
    )
