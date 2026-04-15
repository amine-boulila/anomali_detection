"""Response schema for prediction results."""

from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    """Shape of the JSON returned to the React frontend."""

    model: str = Field(..., examples=["ml"])
    predicted_class: str = Field(..., examples=["Tomato___Late_blight"])
    confidence: float = Field(..., ge=0.0, le=1.0, examples=[0.91])
