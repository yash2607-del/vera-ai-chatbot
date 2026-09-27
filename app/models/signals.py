from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from app.core.constants import SignalType

class CandidateSignal(BaseModel):
    signal_type: SignalType
    score: float
    suppression_key: str
    evidence: Dict[str, Any]
    merchant_id: str
    category: str
    target_offer: Optional[Dict[str, Any]] = None
    target_customer: Optional[Dict[str, Any]] = None
    recommended_action: str
    cta: str
    rationale: str
