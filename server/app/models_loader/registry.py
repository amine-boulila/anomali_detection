"""Single place that exposes the active model loaders."""

from app.models_loader.ml_loader import MlModelLoader

# Deep learning is intentionally disabled for now.
# Keep the file below for later reuse when you want to re-enable the DL path.
# from app.models_loader.dl_loader import DlModelLoader


class ModelRegistry:
    """Keeps one shared loader instance for the currently active model(s)."""

    def __init__(self) -> None:
        self.ml = MlModelLoader()
        # Deep learning is not used in the current backend version.
        # self.dl = DlModelLoader()

    def health_summary(self) -> dict:
        return {
            "ml": self.ml.health_info(),
            # "dl": self.dl.health_info(),
        }


model_registry = ModelRegistry()
