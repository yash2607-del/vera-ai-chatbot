import uuid
from typing import Dict, Any, Optional, Tuple
from app.models.signals import CandidateSignal
from app.models.responses import TickResponse
from app.core.constants import TickStatus, ConversationState
from app.storage.context_store import ContextStore
from app.storage.suppression_store import SuppressionStore
from app.storage.message_store import MessageStore
from app.models.conversation import ConversationRecord
from app.engine.signal_detector import SignalDetector
from app.engine.signal_scorer import SignalScorer
from app.engine.suppression import SuppressionEngine
from app.engine.evidence import EvidenceExtractor
from app.categories.config import get_category_config

class DecisionEngine:
    def __init__(
        self,
        context_store: ContextStore,
        suppression_store: SuppressionStore,
        message_store: MessageStore
    ):
        self.context_store = context_store
        self.suppression_engine = SuppressionEngine(suppression_store)
        self.message_store = message_store
        self.signal_detector = SignalDetector()
        self.signal_scorer = SignalScorer()

    def process_tick(
        self,
        merchant_id: str,
        trigger_id: Optional[str] = None,
        customer_id: Optional[str] = None,
        dry_run: bool = False
    ) -> Tuple[TickStatus, Optional[CandidateSignal], str]:
        """
        Processes a tick for a merchant.
        Returns: (status, selected_signal_or_none, conversation_id)
        """
        # Fetch merchant context
        merchant_context = self.context_store.get_context("merchant", merchant_id)
        if not merchant_context:
            # Fallback inline default context if not stored yet
            merchant_context = {
                "merchant_id": merchant_id,
                "name": f"Merchant_{merchant_id}",
                "vertical": "dentists",
                "locality": "locality",
                "offers": [{"title": "Special Deal", "discounted_price": 299, "active": True}],
                "metrics": {"searches_in_locality": 150, "search_growth": "+30%"}
            }

        # Fetch optional trigger context
        trigger_context = None
        if trigger_id:
            trigger_context = self.context_store.get_context("trigger", trigger_id)

        # Fetch optional customer context
        customer_context = None
        if customer_id:
            customer_context = self.context_store.get_context("customer", customer_id)

        # 1. Detect candidates
        candidates = self.signal_detector.detect_candidates(
            merchant_context, trigger_context, customer_context
        )

        # 2. Score and select top candidate
        top_candidate = self.signal_scorer.score_and_select(candidates)

        # 3. Check suppression
        if self.suppression_engine.is_suppressed(top_candidate.suppression_key):
            conv_id = f"conv_{merchant_id}"
            return TickStatus.SUPPRESSED, top_candidate, conv_id

        # Record suppression unless dry run
        if not dry_run:
            self.suppression_engine.record_suppression(
                top_candidate.suppression_key,
                merchant_id,
                top_candidate.signal_type.value,
                top_candidate.target_offer.get("offer_id") if top_candidate.target_offer else None
            )

        conv_id = f"conv_{merchant_id}"
        return TickStatus.ACTED, top_candidate, conv_id
