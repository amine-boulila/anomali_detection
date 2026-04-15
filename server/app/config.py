"""Central configuration for the FastAPI backend."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Loads configuration from environment variables when available."""

    app_name: str = "Plant Disease Classifier API"
    frontend_origin: str = "http://localhost:5173"
    additional_cors_origins: str = (
        "http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"
    )
    allow_all_cors: bool = True

    ml_model_filename: str = "best_ml_model.joblib"
    ml_metadata_filename: str = "ml_metadata.json"
    label_encoder_filename: str = "label_encoder.joblib"

    dl_model_filename: str = "tensorflow_leaf_disease_model.keras"
    dl_metadata_filename: str = "dl_metadata.json"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def models_dir(self) -> Path:
        return self.project_root / "models"

    @property
    def ml_model_path(self) -> Path:
        return self.models_dir / self.ml_model_filename

    @property
    def ml_metadata_path(self) -> Path:
        return self.models_dir / self.ml_metadata_filename

    @property
    def label_encoder_path(self) -> Path:
        return self.models_dir / self.label_encoder_filename

    @property
    def dl_model_path(self) -> Path:
        return self.models_dir / self.dl_model_filename

    @property
    def dl_metadata_path(self) -> Path:
        return self.models_dir / self.dl_metadata_filename

    @property
    def cors_origins(self) -> list[str]:
        if self.allow_all_cors:
            return ["*"]

        raw_origins = [self.frontend_origin, self.additional_cors_origins]
        origins: list[str] = []
        for group in raw_origins:
            for item in group.split(","):
                cleaned = item.strip()
                if cleaned and cleaned not in origins:
                    origins.append(cleaned)
        return origins


@lru_cache
def get_settings() -> Settings:
    """Caches settings so every module uses the same configuration."""
    return Settings()
