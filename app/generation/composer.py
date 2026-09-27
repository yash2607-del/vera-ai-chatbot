from typing import Dict, Any
from app.models.signals import CandidateSignal
from app.generation.llm_client import LLMClient
from app.generation.fallback import FallbackComposer

class MessageComposer:
    def __init__(self):
        self.llm_client = LLMClient()

    def compose(self, signal: CandidateSignal) -> Dict[str, str]:
        # Build structured message brief
        brief = {
            "merchant_id": signal.merchant_id,
            "category": signal.category,
            "signal_type": signal.signal_type.value,
            "evidence": signal.evidence,
            "recommended_action": signal.recommended_action,
            "default_cta": signal.cta,
            "rationale": signal.rationale
        }
        
        # Try LLM generation first
        llm_result = self.llm_client.generate_copy(brief)
        if llm_result:
            return llm_result

        # Fallback to deterministic template composer
        return FallbackComposer.generate(signal)
