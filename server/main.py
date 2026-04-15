"""FastAPI entrypoint for the plant disease classification backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routes.health import router as health_router
from app.routes.prediction import router as prediction_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="API for classifying plant disease images with ML or DL models.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False if settings.cors_origins == ["*"] else True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(prediction_router)


@app.get("/", tags=["root"])
def read_root() -> dict:
    """Simple welcome route for quick browser checks."""
    return {
        "message": "Plant Disease Classifier API is running.",
        "health_endpoint": "/health",
        "prediction_endpoint": "/predict",
    }
