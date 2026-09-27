from datetime import datetime, timezone
from fastapi import APIRouter
from app.models.responses import HealthResponse

router = APIRouter()

@router.get("/healthz", response_model=HealthResponse)
def get_health():
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc).isoformat()
    )
