from fastapi import APIRouter, Depends, HTTPException, status
import sqlite3
from app.models.context import ContextPayload
from app.models.responses import ContextResponse
from app.storage.database import get_db
from app.storage.context_store import ContextStore

router = APIRouter()

@router.post("/context", response_model=ContextResponse)
def post_context(payload: ContextPayload, db: sqlite3.Connection = Depends(get_db)):
    if payload.scope not in ["category", "merchant", "customer", "trigger"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid scope '{payload.scope}'. Must be one of: category, merchant, customer, trigger"
        )
    
    data_dict = payload.get_data
    store = ContextStore(db)
    
    # Adapt to store
    record_payload = ContextPayload(
        scope=payload.scope,
        context_id=payload.context_id,
        version=payload.version,
        data=data_dict
    )
    result = store.upsert_context(record_payload)
    
    return ContextResponse(
        status="success",
        accepted=True,
        scope=payload.scope,
        context_id=payload.context_id,
        version=payload.version,
        message=f"Context {result['status']} successfully."
    )
