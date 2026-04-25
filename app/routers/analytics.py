from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import analytics_service

router = APIRouter(tags=["Analytics"])


@router.get("/top-countries")
def top_countries(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Top trading countries (flags) ranked by total transit cost."""
    return analytics_service.get_top_countries(db, limit=limit)


@router.get("/region-summary")
def region_summary(db: Session = Depends(get_db)):
    """Trade summary grouped by continent/region."""
    return analytics_service.get_region_summary(db)


@router.get("/trade-trends")
def trade_trends(db: Session = Depends(get_db)):
    """Monthly trade volume and cost trends."""
    return analytics_service.get_trade_trends(db)
