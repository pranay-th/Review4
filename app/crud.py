from typing import Optional
from sqlalchemy.orm import Session
from app.models import TradeRecord
from app.schemas import TradeRecordCreate


# --- Basic Trade CRUD ---

def get_all_records(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    continent: Optional[str] = None,
    commodity: Optional[str] = None,
    flag: Optional[str] = None,
) -> list[TradeRecord]:
    query = db.query(TradeRecord)
    if continent:
        query = query.filter(TradeRecord.continent == continent)
    if commodity:
        query = query.filter(TradeRecord.commodity == commodity)
    if flag:
        query = query.filter(TradeRecord.flag == flag)
    return query.offset(skip).limit(limit).all()


def get_record_by_id(db: Session, record_id: int) -> Optional[TradeRecord]:
    return db.query(TradeRecord).filter(TradeRecord.id == record_id).first()


def create_record(db: Session, record: TradeRecordCreate) -> TradeRecord:
    db_record = TradeRecord(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def delete_record(db: Session, record_id: int) -> bool:
    record = get_record_by_id(db, record_id)
    if not record:
        return False
    db.delete(record)
    db.commit()
    return True


# --- Analytics aggregations ---

def get_top_countries(db: Session, limit: int = 10) -> list[dict]:
    # TODO 
    raise NotImplementedError


def get_monthly_trends(db: Session) -> list[dict]:
    # TODO
    raise NotImplementedError


def get_cost_by_continent(db: Session) -> list[dict]:
    # TODO
    raise NotImplementedError
