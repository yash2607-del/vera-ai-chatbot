from typing import Dict, Any, Optional
from pydantic import BaseModel
from app.core.constants import ConversationState

class ConversationRecord(BaseModel):
    conversation_id: str
    merchant_id: str
    state: ConversationState
    last_signal_type: Optional[str] = None
    last_evidence: Optional[Dict[str, Any]] = None
    last_message: Optional[str] = None
    last_cta: Optional[str] = None
    updated_at: str
