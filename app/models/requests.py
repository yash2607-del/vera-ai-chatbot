from typing import Optional, Dict, Any, Union, List
from pydantic import BaseModel, Field

class ContextPayload(BaseModel):
    scope: str = Field(..., description="Context scope: category, merchant, customer, trigger")
    context_id: str = Field(..., description="Unique ID for context entity")
    version: Union[int, str, float] = Field(..., description="Version identifier")
    data: Optional[Dict[str, Any]] = None
    payload: Optional[Dict[str, Any]] = None
    delivered_at: Optional[str] = None

    @property
    def get_data(self) -> Dict[str, Any]:
        if self.payload is not None:
            return self.payload
        return self.data or {}

class TickRequest(BaseModel):
    merchant_id: Optional[str] = None
    trigger_id: Optional[str] = None
    customer_id: Optional[str] = None
    available_triggers: Optional[List[str]] = None
    now: Optional[str] = None
    timestamp: Optional[str] = None
    dry_run: Optional[bool] = False

class ReplyRequest(BaseModel):
    merchant_id: Optional[str] = None
    conversation_id: str = Field(..., description="Active conversation session ID")
    message: Optional[str] = None
    merchant_message: Optional[str] = None
    customer_id: Optional[str] = None
    from_role: Optional[str] = "merchant"
    received_at: Optional[str] = None
    turn_number: Optional[int] = 1

    @property
    def get_message(self) -> str:
        if self.message is not None:
            return self.message
        return self.merchant_message or ""
