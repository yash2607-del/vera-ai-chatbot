from typing import Dict, Any, Optional, Union
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

class ContextStoreRecord(BaseModel):
    scope: str
    context_id: str
    version_num: float
    version_raw: str
    data: Dict[str, Any]
    updated_at: str
