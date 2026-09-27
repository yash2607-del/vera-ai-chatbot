from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from app.core.constants import TickStatus, ConversationState

class ContextResponse(BaseModel):
    status: str = "success"
    accepted: bool = True
    scope: str
    context_id: str
    version: Any
    message: str

class TickResponse(BaseModel):
    status: TickStatus
    accepted: bool = True
    actions: List[Dict[str, Any]] = []
    message: Optional[str] = None
    cta: Optional[str] = None
    send_as: Optional[str] = "Vera"
    suppression_key: Optional[str] = None
    rationale: Optional[str] = None
    conversation_id: Optional[str] = None
    intent: Optional[str] = None
    evidence: Optional[Dict[str, Any]] = None

class ReplyResponse(BaseModel):
    conversation_id: str
    action: str = "send"
    body: str
    message: str
    previous_state: ConversationState
    current_state: ConversationState
    action_taken: Optional[str] = "NONE"
    cta: Optional[str] = None
    wait_seconds: Optional[int] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: str

class MetadataResponse(BaseModel):
    team_name: str = "Vera AI Team"
    bot_name: str = "Vera AI Assistant"
    model: str = "gpt-4o-mini"
    version: str = "1.0.0"
    supported_verticals: List[str] = ["dentists", "salons", "restaurants", "gyms", "pharmacies"]
    features: List[str] = [
        "version_aware_context_storage",
        "deterministic_signal_scoring",
        "suppression_guardrails",
        "explicit_intent_state_machine",
        "zero_hallucination_fallback"
    ]
    llm_enabled: bool = True
