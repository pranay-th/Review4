import pandas as pd
from sqlalchemy.orm import Session
from app.models import Vessel

CSV_PATH = "dataset/Cleaned.csv"


def load_csv_to_db(db: Session) -> dict:
    df = pd.read_csv(CSV_PATH)
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.drop_duplicates()
    df = df.dropna(subset=["vessel_name"])
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["rerouted"] = df["rerouted"].map({"Yes": True, "No": False}).astype(object)
    df["rerouted"] = df["rerouted"].where(pd.notna(df["rerouted"]), other=None)
    numeric_cols = [
        "toll_usd",
        "ship_hull_value_usd",
        "insurance_premium_delta_pct",
        "insurance_cost_usd",
        "days_delayed",
        "extra_fuel_tonnes",
        "reroute_penalty_usd",
        "total_transit_cost_usd",
        "estimated_cargo_value_usd",
        "total_asset_value_at_risk_usd",
        "inflation_premium_per_unit",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def build_vessel_records(df: pd.DataFrame) -> list[Vessel]:
    import math

    def clean(val):
        if val is None:
            return None
        try:
            if math.isnan(val):
                return None
        except TypeError:
            pass
        return val

    records = []
    for _, row in df.iterrows():
        v = Vessel()
        v.vessel_name = clean(row.get("vessel_name"))
        v.date = clean(row.get("date"))
        v.flag = clean(row.get("flag"))
        v.trade_tier = clean(row.get("trade_tier"))
        v.transit_status = clean(row.get("transit_status"))
        v.toll_usd = clean(row.get("toll_usd"))
        v.rerouted = clean(row.get("rerouted"))
        v.commodity = clean(row.get("commodity"))
        v.destination = clean(row.get("destination"))
        v.payment_rail = clean(row.get("payment_rail"))
        v.ship_hull_value_usd = clean(row.get("ship_hull_value_usd"))
        v.insurance_premium_delta_pct = clean(row.get("insurance_premium_delta_pct"))
        v.insurance_cost_usd = clean(row.get("insurance_cost_usd"))
        v.days_delayed = clean(row.get("days_delayed"))
        v.extra_fuel_tonnes = clean(row.get("extra_fuel_tonnes"))
        v.reroute_penalty_usd = clean(row.get("reroute_penalty_usd"))
        v.total_transit_cost_usd = clean(row.get("total_transit_cost_usd"))
        v.estimated_cargo_value_usd = clean(row.get("estimated_cargo_value_usd"))
        v.total_asset_value_at_risk_usd = clean(row.get("total_asset_value_at_risk_usd"))
        v.continent = clean(row.get("continent"))
        v.inflation_premium_per_unit = clean(row.get("inflation_premium_per_unit"))
        records.append(v)
    return records


def insert_records(db: Session, records: list[Vessel]) -> int:
    from app.models import TradeRecord, Cost, Cargo

    for v in records:
        db.add(v)
        db.flush()  # gets vessel_id without committing

        db.add(TradeRecord(
            vessel_id=v.vessel_id,
            flag=v.flag,
            destination=v.destination,
            date=v.date,
            commodity=v.commodity,
            estimated_cargo_value_usd=v.estimated_cargo_value_usd,
            transit_status=v.transit_status,
            trade_tier=v.trade_tier,
            rerouted=v.rerouted,
            days_delayed=v.days_delayed,
        ))

        db.add(Cost(
            vessel_id=v.vessel_id,
            toll_usd=v.toll_usd,
            insurance_cost_usd=v.insurance_cost_usd,
            total_transit_cost_usd=v.total_transit_cost_usd,
            reroute_penalty_usd=v.reroute_penalty_usd,
        ))

        db.add(Cargo(
            vessel_id=v.vessel_id,
            commodity=v.commodity,
            estimated_cargo_value_usd=v.estimated_cargo_value_usd,
            total_asset_value_at_risk_usd=v.total_asset_value_at_risk_usd,
        ))

    db.commit()
    return len(records)
