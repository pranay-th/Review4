from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import VesselCreate, VesselOut
from app import crud

router = APIRouter(prefix="/vessels", tags=["Vessels"])


@router.post("/", response_model=VesselOut, status_code=201)
def insert_vessel(payload: VesselCreate, db: Session = Depends(get_db)):
    """Insert a new vessel record into the main table."""
    return crud.create_vessel(db, payload)


@router.get("/", response_model=list[VesselOut])
def list_vessels(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    continent: Optional[str] = None,
    commodity: Optional[str] = None,
    flag: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_all_records(db, skip=skip, limit=limit, continent=continent, commodity=commodity, flag=flag)


@router.get("/{vessel_id}", response_model=VesselOut)
def get_vessel(vessel_id: int, db: Session = Depends(get_db)):
    record = crud.get_record_by_id(db, vessel_id)
    if not record:
        raise HTTPException(status_code=404, detail="Vessel not found")
    return record


@router.delete("/{vessel_id}", status_code=204)
def delete_vessel(vessel_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_record(db, vessel_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vessel not found")
