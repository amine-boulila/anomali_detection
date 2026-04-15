"""Prediction route for uploaded plant images."""

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas.prediction import PredictionResponse
from app.services.prediction_service import prediction_service
from app.utils.validators import normalize_model_type, validate_image_upload

router = APIRouter(tags=["prediction"])


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    file: UploadFile = File(...),
    model_type: str = Form(...),
) -> PredictionResponse:
    """
    Predict the disease class for an uploaded image.

    Expected form-data:
    - file: the uploaded image
    - model_type: "ml" or "dl"
    """
    try:
        validate_image_upload(file)
        selected_model = normalize_model_type(model_type)
        image_bytes = await file.read()

        if not image_bytes:
            raise ValueError("The uploaded image is empty.")

        prediction_result = prediction_service.predict(
            image_bytes=image_bytes,
            model_type=selected_model,
        )
        return PredictionResponse(**prediction_result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
