"""Health-check route."""

from fastapi import APIRouter

from app.models_loader.registry import model_registry

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    """Returns basic health information for the ML-only API."""
    return {
        "status": "ok",
        "mode": "ml-only",
        "models": model_registry.health_summary(),
    }
