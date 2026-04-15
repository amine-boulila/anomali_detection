"""Loader for the saved classical machine learning model."""

import json

import joblib
import numpy as np
from sklearn.impute import SimpleImputer

from app.config import get_settings


class MlModelLoader:
    """Loads the saved scikit-learn model, metadata, and label encoder lazily."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self._model = None
        self._label_encoder = None
        self._metadata = None

    def _ensure_files_exist(self) -> None:
        missing_files = []
        for path in [
            self.settings.ml_model_path,
            self.settings.ml_metadata_path,
            self.settings.label_encoder_path,
        ]:
            if not path.exists():
                missing_files.append(str(path))

        if missing_files:
            joined = ", ".join(missing_files)
            raise FileNotFoundError(
                f"Missing required ML artifact(s): {joined}. "
                "TODO: confirm the saved file names in /models."
            )

    def load(self) -> None:
        """Load the model only once."""
        if self._model is not None:
            return

        self._ensure_files_exist()

        self._model = joblib.load(self.settings.ml_model_path)
        self._apply_compatibility_patches(self._model)
        self._label_encoder = joblib.load(self.settings.label_encoder_path)

        with self.settings.ml_metadata_path.open("r", encoding="utf-8") as file:
            self._metadata = json.load(file)

    def _apply_compatibility_patches(self, estimator) -> None:
        """
        Patch older scikit-learn objects after unpickling.

        The saved ML pipeline was likely trained with an older scikit-learn
        version where SimpleImputer stored `_fit_dtype`. Newer versions may
        expect `_fill_dtype` during transform/predict.
        """
        if isinstance(estimator, SimpleImputer):
            if hasattr(estimator, "_fit_dtype") and not hasattr(estimator, "_fill_dtype"):
                estimator._fill_dtype = estimator._fit_dtype
            return

        if hasattr(estimator, "steps"):
            for _, step_estimator in estimator.steps:
                self._apply_compatibility_patches(step_estimator)

        if hasattr(estimator, "transformers"):
            for _, transformer, _ in estimator.transformers:
                if transformer not in ("drop", "passthrough"):
                    self._apply_compatibility_patches(transformer)

    @property
    def metadata(self) -> dict:
        self.load()
        return self._metadata

    @property
    def expected_feature_length(self) -> int | None:
        value = self.metadata.get("feature_vector_length")
        return int(value) if value is not None else None

    def _decode_prediction(self, raw_prediction) -> str:
        """Convert the model output back to a readable class label."""
        if isinstance(raw_prediction, str):
            return raw_prediction

        prediction_index = int(raw_prediction)

        if self._label_encoder is not None:
            return str(self._label_encoder.inverse_transform([prediction_index])[0])

        class_names = self.metadata.get("class_names", [])
        if 0 <= prediction_index < len(class_names):
            return str(class_names[prediction_index])

        raise RuntimeError(
            "Could not decode the ML prediction. "
            "TODO: confirm the saved label encoder or class_names order."
        )

    def predict(self, feature_vector: np.ndarray) -> dict:
        """Run prediction on a single handcrafted feature vector."""
        self.load()

        feature_matrix = np.asarray(feature_vector, dtype=np.float32).reshape(1, -1)
        raw_prediction = self._model.predict(feature_matrix)[0]

        confidence = 0.0
        if hasattr(self._model, "predict_proba"):
            probabilities = self._model.predict_proba(feature_matrix)[0]
            confidence = float(np.max(probabilities))

        return {
            "model": "ml",
            "predicted_class": self._decode_prediction(raw_prediction),
            "confidence": round(confidence, 4),
        }

    def health_info(self) -> dict:
        return {
            "model_file": self.settings.ml_model_path.exists(),
            "metadata_file": self.settings.ml_metadata_path.exists(),
            "label_encoder_file": self.settings.label_encoder_path.exists(),
        }
