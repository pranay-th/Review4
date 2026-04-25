from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from app.database import Base


class TradeRecord(Base):
    __tablename__ = "trade_records"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    vessel_name = Column(String, nullable=False)
    mmsi = Column(String, nullable=True)
    flag = Column(String, nullable=True)
    trade_tier = Column(String, nullable=True)
    transit_status = Column(String, nullable=True)
    toll_usd = Column(Float, nullable=True)
    rerouted = Column(Boolean, nullable=True)
    commodity = Column(String, nullable=True)
    destination = Column(String, nullable=True)
    payment_rail = Column(String, nullable=True)
    ship_hull_value_usd = Column(Float, nullable=True)
    insurance_premium_delta_pct = Column(Float, nullable=True)
    insurance_cost_usd = Column(Float, nullable=True)
    days_delayed = Column(Integer, nullable=True)
    extra_fuel_tonnes = Column(Float, nullable=True)
    reroute_penalty_usd = Column(Float, nullable=True)
    total_transit_cost_usd = Column(Float, nullable=True)
    naval_escort_status = Column(String, nullable=True)
    estimated_cargo_value_usd = Column(Float, nullable=True)
    total_asset_value_at_risk_usd = Column(Float, nullable=True)
    continent = Column(String, nullable=True)
    inflation_premium_per_unit = Column(Float, nullable=True)
