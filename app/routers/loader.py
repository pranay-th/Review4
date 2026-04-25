from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.csv_loader import load_csv_to_db

router = APIRouter(tags=["Loader"])


@router.post("/load-csv")
def load_csv(db: Session = Depends(get_db)):
    """Truncates all tables and reloads the CSV dataset into the database."""
    try:
        return load_csv_to_db(db)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
