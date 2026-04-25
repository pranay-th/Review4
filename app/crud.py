from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Vessel
from app.schemas import VesselCreate


# --- Vessel CRUD ---

def create_vessel(db: Session, data: VesselCreate) -> Vessel:
    vessel = Vessel(**data.model_dump())
    db.add(vessel)
    db.commit()
    db.refresh(vessel)
    return vessel


def get_all_records(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    continent: Optional[str] = None,
    commodity: Optional[str] = None,
    flag: Optional[str] = None,
) -> list[Vessel]:
    query = db.query(Vessel)
    if continent:
        query = query.filter(Vessel.continent == continent)
    if commodity:
        query = query.filter(Vessel.commodity == commodity)
    if flag:
        query = query.filter(Vessel.flag == flag)
    return query.offset(skip).limit(limit).all()


def get_record_by_id(db: Session, record_id: int) -> Optional[Vessel]:
    return db.query(Vessel).filter(Vessel.vessel_id == record_id).first()


def delete_record(db: Session, record_id: int) -> bool:
    record = get_record_by_id(db, record_id)
    if not record:
        return False
    db.delete(record)
    db.commit()
    return True


# --- Analytics aggregations ---

def get_top_countries(db: Session, limit: int = 10) -> list[dict]:
    rows = (
        db.query(
            Vessel.flag,
            func.sum(Vessel.total_transit_cost_usd).label("total_cost"),
            func.count(Vessel.vessel_id).label("total_trades"),
        )
        .filter(Vessel.flag.isnot(None))
        .group_by(Vessel.flag)
        .order_by(func.sum(Vessel.total_transit_cost_usd).desc())
        .limit(limit)
        .all()
    )
    return [
        {"country": r.flag, "total_cost": r.total_cost or 0, "total_trades": r.total_trades}
        for r in rows
    ]


def get_cost_by_continent(db: Session) -> list[dict]:
    rows = (
        db.query(
            Vessel.continent,
            func.sum(Vessel.total_transit_cost_usd).label("total_cost"),
            func.avg(Vessel.total_transit_cost_usd).label("avg_cost"),
            func.count(Vessel.vessel_id).label("record_count"),
        )
        .filter(Vessel.continent.isnot(None))
        .group_by(Vessel.continent)
        .order_by(func.sum(Vessel.total_transit_cost_usd).desc())
        .all()
    )
    return [
        {
            "continent": r.continent,
            "total_cost": r.total_cost or 0,
            "avg_cost": round(float(r.avg_cost or 0), 2),
            "record_count": r.record_count,
        }
        for r in rows
    ]


def get_monthly_trends(db: Session) -> list[dict]:
    rows = (
        db.query(
            func.date_trunc("month", Vessel.date).label("month"),
            func.count(Vessel.vessel_id).label("trade_count"),
            func.sum(Vessel.total_transit_cost_usd).label("total_cost"),
        )
        .filter(Vessel.date.isnot(None))
        .group_by(func.date_trunc("month", Vessel.date))
        .order_by(func.date_trunc("month", Vessel.date))
        .all()
    )
    return [
        {
            "month": str(r.month)[:7],
            "trade_count": r.trade_count,
            "total_cost": r.total_cost or 0,
        }
        for r in rows
    ]
