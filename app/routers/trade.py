from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import TradeRecordCreate, TradeRecordOut
from app import crud

router = APIRouter(prefix="/trade", tags=["Trade"])


@router.get("/", response_model=list[TradeRecordOut])
def list_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    continent: Optional[str] = None,
    commodity: Optional[str] = None,
    flag: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_all_records(db, skip=skip, limit=limit, continent=continent, commodity=commodity, flag=flag)


@router.get("/{record_id}", response_model=TradeRecordOut)
def get_record(record_id: int, db: Session = Depends(get_db)):
    record = crud.get_record_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@router.post("/", response_model=TradeRecordOut, status_code=201)
def create_record(record: TradeRecordCreate, db: Session = Depends(get_db)):
    return crud.create_record(db, record)


@router.delete("/{record_id}", status_code=204)
def delete_record(record_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_record(db, record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Record not found")
