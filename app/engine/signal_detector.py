from typing import Dict, Any, List, Optional
from app.core.constants import SignalType
from app.models.signals import CandidateSignal
from app.categories.config import get_category_config
from app.engine.evidence import EvidenceExtractor
from app.engine.suppression import SuppressionEngine

class SignalDetector:
    def detect_candidates(
        self,
        merchant_context: Dict[str, Any],
        trigger_context: Optional[Dict[str, Any]] = None,
        customer_context: Optional[Dict[str, Any]] = None
    ) -> List[CandidateSignal]:
        candidates = []
        merchant_id = merchant_context.get("merchant_id") or merchant_context.get("id", "m_001")
        vertical = merchant_context.get("category_slug") or merchant_context.get("vertical", "dentists")
        cat_config = get_category_config(vertical)
        
        evidence = EvidenceExtractor.extract_evidence(
            merchant_context, trigger_context, customer_context, cat_config.model_dump()
        )
        
        owner_prefix = f"Dr. {evidence['owner_name']}" if vertical == "dentists" and evidence.get("owner_name") else (evidence.get("owner_name") or "Merchant")
        locality = evidence.get("locality", "your locality")
        offer_title = evidence.get("offer_title") or cat_config.preferred_offers[0]
        price = evidence.get("discounted_price") or 299

        # 1. Official Trigger Kind Handling
        if trigger_context:
            kind = (trigger_context.get("kind") or trigger_context.get("type", "")).lower()
            t_payload = trigger_context.get("payload", {}) if isinstance(trigger_context.get("payload"), dict) else {}
            
            if "research" in kind or "digest" in kind or kind == "search_spike":
                count = evidence.get("views") or 190
                key = SuppressionEngine.generate_suppression_key(merchant_id, "SEARCH_SPIKE", offer_title)
                candidates.append(CandidateSignal(
                    signal_type=SignalType.SEARCH_SPIKE,
                    score=95.0,
                    suppression_key=key,
                    evidence=evidence,
                    merchant_id=merchant_id,
                    category=vertical,
                    recommended_action=f"Promote {offer_title} to local searchers at ₹{price}",
                    cta=f"Should I send them a discounted {offer_title.lower()} at ₹{price}?",
                    rationale=f"High search interest and research digest opportunity in {locality}."
                ))
            elif "dip" in kind or kind == "performance_dip":
                dip_val = t_payload.get("delta_pct") or "-50%"
                key = SuppressionEngine.generate_suppression_key(merchant_id, "PERFORMANCE_DIP", "dip")
                candidates.append(CandidateSignal(
                    signal_type=SignalType.PERFORMANCE_DIP,
                    score=90.0,
                    suppression_key=key,
                    evidence=evidence,
                    merchant_id=merchant_id,
                    category=vertical,
                    recommended_action=f"Launch campaign to recover call traffic (dip: {dip_val})",
                    cta=f"Should we launch a discount for '{offer_title}' at ₹{price} to recover traffic?",
                    rationale=f"Traffic drop of {dip_val} detected in {locality}."
                ))
            elif "festival" in kind or kind == "festival_seasonal":
                fest_name = t_payload.get("festival") or "Diwali"
                key = SuppressionEngine.generate_suppression_key(merchant_id, "FESTIVAL_SEASONAL", fest_name)
                candidates.append(CandidateSignal(
                    signal_type=SignalType.FESTIVAL_SEASONAL,
                    score=85.0,
                    suppression_key=key,
                    evidence=evidence,
                    merchant_id=merchant_id,
                    category=vertical,
                    recommended_action=f"Run special package for {fest_name}",
                    cta=f"Should I activate the {fest_name} promo package at ₹{price}?",
                    rationale=f"Seasonal momentum for {fest_name} in {locality}."
                ))
            elif "recall" in kind or "lapse" in kind:
                cust_name = evidence.get("customer_name") or "VIP Customer"
                key = SuppressionEngine.generate_suppression_key(merchant_id, "CUSTOMER_LAPSE", cust_name)
                candidates.append(CandidateSignal(
                    signal_type=SignalType.CUSTOMER_LAPSE,
                    score=88.0,
                    suppression_key=key,
                    evidence=evidence,
                    merchant_id=merchant_id,
                    category=vertical,
                    recommended_action=f"Send recall invitation to {cust_name}",
                    cta=f"Should I send a private recall offer to {cust_name}?",
                    rationale=f"Recall due for {cust_name}."
                ))

        # 2. Metric / Fallback Signal
        if not candidates:
            key = SuppressionEngine.generate_suppression_key(merchant_id, "SEARCH_SPIKE", "default")
            candidates.append(CandidateSignal(
                signal_type=SignalType.SEARCH_SPIKE,
                score=75.0,
                suppression_key=key,
                evidence=evidence,
                merchant_id=merchant_id,
                category=vertical,
                recommended_action=f"Capitalize on local search demand for {offer_title}",
                cta=f"Should I activate a campaign for {offer_title} at ₹{price}?",
                rationale="Proactive search interest detected."
            ))

        return candidates
