from typing import Optional
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


# --- Analytics aggregations (to be filled after data engineer confirms logic) ---

def get_top_countries(db: Session, limit: int = 10) -> list[dict]:
    # TODO: confirm grouping column and ranking metric with data engineer
    raise NotImplementedError


def get_monthly_trends(db: Session) -> list[dict]:
    # TODO: confirm date truncation and aggregation fields with data engineer
    raise NotImplementedError


def get_cost_by_continent(db: Session) -> list[dict]:
    # TODO: confirm summary fields with data engineer
    raise NotImplementedError
