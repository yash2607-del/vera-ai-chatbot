from fastapi import APIRouter
from app.models.responses import MetadataResponse
from app.core.config import settings

router = APIRouter()

@router.get("/metadata", response_model=MetadataResponse)
def get_metadata():
    return MetadataResponse(
        bot_name=settings.APP_NAME,
        version="1.0.0",
        supported_verticals=["dentists", "salons", "restaurants", "gyms", "pharmacies"],
        features=[
            "version_aware_context_storage",
            "deterministic_signal_scoring",
            "suppression_guardrails",
            "explicit_intent_state_machine",
            "zero_hallucination_fallback"
        ],
        llm_enabled=bool(settings.OPENAI_API_KEY and settings.USE_LLM)
    )
