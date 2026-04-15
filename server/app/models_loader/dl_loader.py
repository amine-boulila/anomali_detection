"""Loader for the saved deep learning model."""

import json

import numpy as np

from app.config import get_settings


class DlModelLoader:
    """Loads the saved TensorFlow model lazily and performs DL inference."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self._model = None
        self._metadata = None
        self._tf = None

    def _ensure_files_exist(self) -> None:
        missing_files = []
        for path in [self.settings.dl_model_path, self.settings.dl_metadata_path]:
            if not path.exists():
                missing_files.append(str(path))

        if missing_files:
            joined = ", ".join(missing_files)
            raise FileNotFoundError(
                f"Missing required DL artifact(s): {joined}. "
                "TODO: confirm the saved DL model file names in /models."
            )

    def load(self) -> None:
        """Load TensorFlow and the saved .keras model only when needed."""
        if self._model is not None:
            return

        self._ensure_files_exist()

        try:
            import tensorflow as tf
        except ImportError as exc:
            raise RuntimeError(
                "TensorFlow is not installed. "
                "Install backend requirements before using the DL model."
            ) from exc

        self._tf = tf
        self._model = tf.keras.models.load_model(self.settings.dl_model_path)

        with self.settings.dl_metadata_path.open("r", encoding="utf-8") as file:
            self._metadata = json.load(file)

    @property
    def metadata(self) -> dict:
        self.load()
        return self._metadata

    @property
    def image_size(self) -> tuple[int, int] | None:
        value = self.metadata.get("image_size")
        if isinstance(value, list) and len(value) == 2:
            return int(value[0]), int(value[1])
        return None

    def prepare_tensor(self, preprocessed_rgb_image: np.ndarray) -> np.ndarray:
        """
        Tensor preparation step for the deep learning model.

        TODO: if your training used a different preprocessing function than
        MobileNetV2's preprocess_input, replace it here.
        """
        self.load()

        batched = np.expand_dims(preprocessed_rgb_image.astype(np.float32), axis=0)
        return self._tf.keras.applications.mobilenet_v2.preprocess_input(batched)

    def predict_tensor(self, input_tensor: np.ndarray) -> dict:
        """Run prediction on a prepared DL tensor."""
        self.load()

        probabilities = self._model.predict(input_tensor, verbose=0)[0]
        predicted_index = int(np.argmax(probabilities))
        confidence = float(np.max(probabilities))
        class_names = self.metadata.get("class_names", [])

        if predicted_index >= len(class_names):
            raise RuntimeError(
                "The DL prediction index is outside the class_names list. "
                "TODO: confirm the class order used during training."
            )

        return {
            "model": "dl",
            "predicted_class": str(class_names[predicted_index]),
            "confidence": round(confidence, 4),
        }

    def health_info(self) -> dict:
        return {
            "model_file": self.settings.dl_model_path.exists(),
            "metadata_file": self.settings.dl_metadata_path.exists(),
        }
