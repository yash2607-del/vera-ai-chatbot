from fastapi import APIRouter, Depends
import sqlite3
from app.models.requests import ReplyRequest
from app.models.responses import ReplyResponse
from app.models.conversation import ConversationRecord
from app.core.constants import ConversationState
from app.storage.database import get_db
from app.storage.message_store import MessageStore
from app.engine.intent_engine import IntentEngine

router = APIRouter()

@router.post("/reply", response_model=ReplyResponse)
def post_reply(request: ReplyRequest, db: sqlite3.Connection = Depends(get_db)):
    m_store = MessageStore(db)
    record = m_store.get_conversation(request.conversation_id)
    
    merchant_id = request.merchant_id or (record.merchant_id if record else "m_001")
    merchant_msg = request.get_message

    if not record:
        prev_state = ConversationState.NONE
        last_evidence = {"merchant_id": merchant_id, "offer_title": "deal", "discounted_price": 299}
        last_cta = "Should I activate this deal?"
    else:
        prev_state = record.state
        last_evidence = record.last_evidence or {}
        last_cta = record.last_cta or "Should I activate this offer?"

    current_state, reply_msg, action_taken, new_cta, bot_action = IntentEngine.process_reply(
        previous_state=prev_state,
        merchant_message=merchant_msg,
        last_evidence=last_evidence,
        last_cta=last_cta
    )

    # Save updated conversation state
    new_record = ConversationRecord(
        conversation_id=request.conversation_id,
        merchant_id=merchant_id,
        state=current_state,
        last_signal_type=record.last_signal_type if record else None,
        last_evidence=last_evidence,
        last_message=reply_msg,
        last_cta=new_cta or last_cta,
        updated_at=""
    )
    m_store.save_conversation(new_record)

    return ReplyResponse(
        conversation_id=request.conversation_id,
        action=bot_action,
        body=reply_msg,
        message=reply_msg,
        previous_state=prev_state,
        current_state=current_state,
        action_taken=action_taken,
        cta=new_cta
    )
