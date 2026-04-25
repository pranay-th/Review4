from datetime import date
from typing import Optional
from pydantic import BaseModel


class TradeRecordBase(BaseModel):
    date: date
    vessel_name: str
    mmsi: Optional[str] = None
    flag: Optional[str] = None
    trade_tier: Optional[str] = None
    transit_status: Optional[str] = None
    toll_usd: Optional[float] = None
    rerouted: Optional[bool] = None
    commodity: Optional[str] = None
    destination: Optional[str] = None
    payment_rail: Optional[str] = None
    ship_hull_value_usd: Optional[float] = None
    insurance_premium_delta_pct: Optional[float] = None
    insurance_cost_usd: Optional[float] = None
    days_delayed: Optional[int] = None
    extra_fuel_tonnes: Optional[float] = None
    reroute_penalty_usd: Optional[float] = None
    total_transit_cost_usd: Optional[float] = None
    naval_escort_status: Optional[str] = None
    estimated_cargo_value_usd: Optional[float] = None
    total_asset_value_at_risk_usd: Optional[float] = None
    continent: Optional[str] = None
    inflation_premium_per_unit: Optional[float] = None


class TradeRecordCreate(TradeRecordBase):
    pass


class TradeRecordOut(TradeRecordBase):
    id: int

    class Config:
        from_attributes = True


# --- Analytics response schemas ---

class ContinentSummary(BaseModel):
    continent: str
    total_cost: float
    avg_cost: float
    record_count: int


class CommoditySummary(BaseModel):
    commodity: str
    total_cost: float
    avg_days_delayed: float


class RerouteSummary(BaseModel):
    rerouted: bool
    count: int
    avg_penalty_usd: float


# --- Prediction schemas ---

class PredictionInput(BaseModel):
    ship_hull_value_usd: float
    insurance_premium_delta_pct: float
    days_delayed: int
    extra_fuel_tonnes: float
    reroute_penalty_usd: float
    estimated_cargo_value_usd: float


class PredictionOutput(BaseModel):
    predicted_total_transit_cost_usd: float
