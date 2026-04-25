from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


# --- Vessel (main table) schemas ---

class VesselCreate(BaseModel):
    vessel_name: str
    date: Optional[datetime] = None
    flag: Optional[str] = None
    trade_tier: Optional[str] = None
    transit_status: Optional[str] = None
    toll_usd: Optional[int] = None
    rerouted: Optional[bool] = None
    commodity: Optional[str] = None
    destination: Optional[str] = None
    payment_rail: Optional[str] = None
    ship_hull_value_usd: Optional[int] = None
    insurance_premium_delta_pct: Optional[float] = None
    insurance_cost_usd: Optional[int] = None
    days_delayed: Optional[int] = None
    extra_fuel_tonnes: Optional[int] = None
    reroute_penalty_usd: Optional[int] = None
    total_transit_cost_usd: Optional[int] = None
    estimated_cargo_value_usd: Optional[int] = None
    total_asset_value_at_risk_usd: Optional[int] = None
    continent: Optional[str] = None
    inflation_premium_per_unit: Optional[float] = None


class VesselOut(VesselCreate):
    vessel_id: int

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

class TransitPredictionInput(BaseModel):
    mmsi: Optional[float] = None
    flag: Optional[str] = None
    trade_tier: Optional[str] = None
    commodity: Optional[str] = None
    destination: Optional[str] = None
    payment_rail: Optional[str] = None
    continent: Optional[str] = None


class TransitPredictionOutput(BaseModel):
    predicted_transit_status: str
    probabilities: dict


class GrowthPredictionInput(BaseModel):
    toll_usd: Optional[float] = 0
    rerouted: Optional[int] = 0
    ship_hull_value_usd: Optional[float] = 0
    insurance_premium_delta_pct: Optional[float] = 0
    insurance_cost_usd: Optional[float] = 0
    days_delayed: Optional[int] = 0
    extra_fuel_tonnes: Optional[float] = 0
    reroute_penalty_usd: Optional[float] = 0
    total_transit_cost_usd: Optional[float] = 0
    estimated_cargo_value_usd: Optional[float] = 0
    total_asset_value_at_risk_usd: Optional[float] = 0
    inflation_premium_per_unit: Optional[float] = 0
    month: Optional[int] = 1
    year: Optional[int] = 2026
    flag: Optional[str] = None
    trade_tier: Optional[str] = None
    transit_status: Optional[str] = None
    commodity: Optional[str] = None
    destination: Optional[str] = None
    payment_rail: Optional[str] = None
    continent: Optional[str] = None


class GrowthPredictionOutput(BaseModel):
    predicted_total_asset_value_at_risk_usd: float
