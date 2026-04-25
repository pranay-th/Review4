from sqlalchemy.orm import Session
from app import crud


def get_top_countries(db: Session, limit: int = 10) -> list[dict]:
    return crud.get_top_countries(db, limit=limit)


def get_region_summary(db: Session) -> list[dict]:
    return crud.get_cost_by_continent(db)


def get_trade_trends(db: Session) -> list[dict]:
    return crud.get_monthly_trends(db)
