from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.csv_loader import load_csv_to_db, load_country_summary

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


@router.post("/load-country-summary")
def load_country_summary_route(db: Session = Depends(get_db)):
    """Loads the CountrySummary CSV into the country_summary table."""
    try:
        return load_country_summary(db)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
