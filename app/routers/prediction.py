from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import PredictionInput, PredictionOutput
from app.services import ml_service

router = APIRouter(tags=["Prediction"])


@router.post("/predict/train")
def train(db: Session = Depends(get_db)):
    """Train the regression model on current DB data."""
    try:
        return ml_service.train_model(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/predict-growth", response_model=PredictionOutput)
def predict_growth(payload: PredictionInput):
    """Predict total transit cost given trade features."""
    try:
        cost = ml_service.predict_cost(payload.model_dump())
        return {"predicted_total_transit_cost_usd": cost}
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
