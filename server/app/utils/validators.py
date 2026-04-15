"""Validation helpers for API inputs."""

from pathlib import Path

from fastapi import UploadFile

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpg",
    "image/jpeg",
    "image/png",
    "image/bmp",
    "image/webp",
}


def normalize_model_type(model_type: str) -> str:
    """Normalizes the requested model type for the ML-only backend."""
    normalized = (model_type or "").strip().lower()
    if normalized != "ml":
        raise ValueError(
            "Only the 'ml' model_type is enabled right now. "
            "The deep learning path is temporarily disabled."
        )
    return normalized


def validate_image_upload(file: UploadFile) -> None:
    """Basic validation for extension and MIME type."""
    if file.filename is None:
        raise ValueError("The uploaded file must have a filename.")

    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_IMAGE_EXTENSIONS))
        raise ValueError(f"Unsupported file type. Allowed extensions: {allowed}.")

    if file.content_type and file.content_type.lower() not in ALLOWED_IMAGE_CONTENT_TYPES:
        raise ValueError(
            "Unsupported content type. Please upload a standard image file."
        )
