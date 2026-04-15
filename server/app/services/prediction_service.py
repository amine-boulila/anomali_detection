"""Service layer that orchestrates preprocessing and inference."""

from app.models_loader.registry import model_registry
from app.utils.image_processing import (
    DEFAULT_ML_IMAGE_SIZE,
    decode_image_bytes,
    extract_ml_feature_vector,
    preprocess_image_for_ml,
)


class PredictionService:
    """Coordinates image preprocessing and ML inference."""

    def predict(self, image_bytes: bytes, model_type: str) -> dict:
        image_bgr = decode_image_bytes(image_bytes)

        if model_type == "ml":
            return self._predict_with_ml(image_bgr)

        # Deep learning prediction is intentionally disabled for now.
        raise ValueError(
            "Only the ML model is enabled right now. "
            "The DL endpoint path is temporarily disabled."
        )

    def _predict_with_ml(self, image_bgr) -> dict:
        """
        ML path split into:
        1. image preprocessing
        2. feature extraction
        3. prediction
        """
        ml_loader = model_registry.ml

        preprocessed_image = preprocess_image_for_ml(
            image_bgr=image_bgr,
            target_size=DEFAULT_ML_IMAGE_SIZE,
        )
        feature_vector = extract_ml_feature_vector(preprocessed_image)

        expected_length = ml_loader.expected_feature_length
        if expected_length is not None and len(feature_vector) != expected_length:
            raise RuntimeError(
                "The extracted ML feature vector does not match the saved model. "
                f"Expected {expected_length} values, got {len(feature_vector)}. "
                "TODO: check the preprocessing or feature extraction steps."
            )

        return ml_loader.predict(feature_vector)

prediction_service = PredictionService()
