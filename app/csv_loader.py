import pandas as pd
from pathlib import Path
from sqlalchemy.orm import Session
from app.models import (
    Vessel, TradeRecord, Cost, Cargo, TradeCategory
)

CSV_PATH = Path("dataset/Cleaned.csv")


def _val(row, col):
    v = row.get(col)
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    if isinstance(v, str) and v.strip() == '':
        return None
    return v


def _int(row, col):
    v = _val(row, col)
    if v is None:
        return None
    try:
        return int(float(v))
    except (ValueError, TypeError):
        return None


def _float(row, col):
    v = _val(row, col)
    if v is None:
        return None
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def _str(row, col):
    v = _val(row, col)
    return str(v).strip() if v is not None else None


def _bool(row, col):
    v = _val(row, col)
    if v is None:
        return None
    if isinstance(v, bool):
        return v
    if type(v).__name__ == "bool_":
        return bool(v)
    if isinstance(v, str):
        return v.strip().lower() in ("true", "yes", "1")
    return bool(v)


def load_csv_to_db(db: Session) -> dict:
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"{CSV_PATH.name} not found at {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    rows_read = len(df)
    rows_skipped = 0

    # Truncate all child tables first (FK order), then parent
    for model in [TradeRecord, Cost, Cargo, TradeCategory]:
        db.query(model).delete()
    db.query(Vessel).delete()
    db.commit()

    seen_tiers = set()

    for _, row in df.iterrows():
        try:
            vessel = Vessel(
                vessel_name=_str(row, "vessel_name"),
                date=pd.to_datetime(_val(row, "date"), errors="coerce"),
                flag=_str(row, "flag"),
                trade_tier=_str(row, "trade_tier"),
                transit_status=_str(row, "transit_status"),
                toll_usd=_int(row, "toll_usd"),
                rerouted=_bool(row, "rerouted"),
                commodity=_str(row, "commodity"),
                destination=_str(row, "destination"),
                payment_rail=_str(row, "payment_rail"),
                ship_hull_value_usd=_int(row, "ship_hull_value_usd"),
                insurance_premium_delta_pct=_float(row, "insurance_premium_delta_pct"),
                insurance_cost_usd=_int(row, "insurance_cost_usd"),
                days_delayed=_int(row, "days_delayed"),
                extra_fuel_tonnes=_int(row, "extra_fuel_tonnes"),
                reroute_penalty_usd=_int(row, "reroute_penalty_usd"),
                total_transit_cost_usd=_int(row, "total_transit_cost_usd"),
                estimated_cargo_value_usd=_int(row, "estimated_cargo_value_usd"),
                total_asset_value_at_risk_usd=_int(row, "total_asset_value_at_risk_usd"),
                continent=_str(row, "continent"),
                inflation_premium_per_unit=_float(row, "inflation_premium_per_unit"),
            )

            vessel.trade_records = [TradeRecord(
                flag=_str(row, "flag"),
                destination=_str(row, "destination"),
                date=vessel.date,
                commodity=_str(row, "commodity"),
                estimated_cargo_value_usd=_int(row, "estimated_cargo_value_usd"),
                transit_status=_str(row, "transit_status"),
                trade_tier=_str(row, "trade_tier"),
                rerouted=_bool(row, "rerouted"),
                days_delayed=_int(row, "days_delayed"),
            )]

            vessel.costs = [Cost(
                toll_usd=_int(row, "toll_usd"),
                insurance_cost_usd=_int(row, "insurance_cost_usd"),
                total_transit_cost_usd=_int(row, "total_transit_cost_usd"),
                reroute_penalty_usd=_int(row, "reroute_penalty_usd"),
            )]

            vessel.cargos = [Cargo(
                commodity=_str(row, "commodity"),
                estimated_cargo_value_usd=_int(row, "estimated_cargo_value_usd"),
                total_asset_value_at_risk_usd=_int(row, "total_asset_value_at_risk_usd"),
            )]

            db.add(vessel)

            # TradeCategory — one row per unique trade_tier
            tier = _str(row, "trade_tier")
            if tier and tier not in seen_tiers:
                seen_tiers.add(tier)
                db.add(TradeCategory(
                    trade_tier=tier,
                    transit_status=_str(row, "transit_status"),
                    commodity=_str(row, "commodity"),
                ))

        except Exception:
            rows_skipped += 1

    db.commit()
    rows_inserted = rows_read - rows_skipped
    return {
        "rows_read": rows_read,
        "rows_inserted": rows_inserted,
        "rows_skipped": rows_skipped,
    }
