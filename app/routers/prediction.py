from fastapi import APIRouter, HTTPException
from app.schemas import (
    TransitPredictionInput, TransitPredictionOutput,
    GrowthPredictionInput, GrowthPredictionOutput,
)
from app.services import ml_service

router = APIRouter(tags=["Prediction"])


@router.post("/predict-transit", response_model=TransitPredictionOutput)
def predict_transit(payload: TransitPredictionInput):
    """Random Forest: predict whether a vessel will Pass, Reroute, or be Blocked."""
    try:
        return ml_service.predict_transit_status(payload.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict-growth", response_model=GrowthPredictionOutput)
def predict_growth(payload: GrowthPredictionInput):
    """Linear Regression: predict total asset value at risk for a trade record."""
    try:
        return ml_service.predict_growth(payload.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
