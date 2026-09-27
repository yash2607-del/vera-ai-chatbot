from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.storage.database import init_db
from app.api.health import router as health_router
from app.api.metadata import router as metadata_router
from app.api.context import router as context_router
from app.api.tick import router as tick_router
from app.api.reply import router as reply_router

setup_logging()
init_db()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Vera AI Business Assistant Backend - Magicpin AI Challenge Submission"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# V1 API Routes
app.include_router(health_router, prefix="/v1", tags=["Health"])
app.include_router(metadata_router, prefix="/v1", tags=["Metadata"])
app.include_router(context_router, prefix="/v1", tags=["Context"])
app.include_router(tick_router, prefix="/v1", tags=["Tick"])
app.include_router(reply_router, prefix="/v1", tags=["Reply"])

# Root route
@app.get("/")
def get_root():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "docs": "/docs",
        "health": "/healthz"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
