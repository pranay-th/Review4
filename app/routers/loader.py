from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import csv_loader

router = APIRouter(tags=["Loader"])


@router.post("/load-csv")
def load_csv(db: Session = Depends(get_db)):
    """Load the CSV dataset into the database."""
    try:
        df = csv_loader.load_csv_to_db(db)
        records = csv_loader.build_vessel_records(df)
        count = csv_loader.insert_records(db, records)
        return {"status": "success", "rows_inserted": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
