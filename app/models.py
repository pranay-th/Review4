import datetime
from sqlalchemy import (
    Boolean, Column, DateTime, Float,
    ForeignKey, Integer, String
)
from sqlalchemy.orm import relationship
from app.database import Base


class Vessel(Base):
    __tablename__ = "vessels"
    vessel_id = Column(Integer, primary_key=True, autoincrement=True)
    vessel_name = Column(String)
    date = Column(DateTime)
    flag = Column(String)
    trade_tier = Column(String)
    transit_status = Column(String)
    toll_usd = Column(Integer)
    rerouted = Column(Boolean)
    commodity = Column(String)
    destination = Column(String)
    payment_rail = Column(String)
    ship_hull_value_usd = Column(Integer)
    insurance_premium_delta_pct = Column(Float)
    insurance_cost_usd = Column(Integer)
    days_delayed = Column(Integer)
    extra_fuel_tonnes = Column(Integer)
    reroute_penalty_usd = Column(Integer)
    total_transit_cost_usd = Column(Integer)
    estimated_cargo_value_usd = Column(Integer)
    total_asset_value_at_risk_usd = Column(Integer)
    continent = Column(String)
    inflation_premium_per_unit = Column(Float)

    costs = relationship("Cost", back_populates="vessel", cascade="all, delete-orphan")
    cargos = relationship("Cargo", back_populates="vessel", cascade="all, delete-orphan")
    trade_records = relationship("TradeRecord", back_populates="vessel", cascade="all, delete-orphan")


class TradeRecord(Base):
    __tablename__ = "trade_records"
    trade_id = Column(Integer, primary_key=True, autoincrement=True)
    vessel_id = Column(Integer, ForeignKey("vessels.vessel_id"))
    flag = Column(String)
    destination = Column(String)
    date = Column(DateTime)
    commodity = Column(String)
    estimated_cargo_value_usd = Column(Integer)
    transit_status = Column(String)
    trade_tier = Column(String)
    rerouted = Column(Boolean)
    days_delayed = Column(Integer)
    vessel = relationship("Vessel", back_populates="trade_records")


class Cost(Base):
    __tablename__ = "costs"
    id = Column(Integer, primary_key=True)
    vessel_id = Column(Integer, ForeignKey("vessels.vessel_id"))
    toll_usd = Column(Integer)
    insurance_cost_usd = Column(Integer)
    total_transit_cost_usd = Column(Integer)
    reroute_penalty_usd = Column(Integer)
    vessel = relationship("Vessel", back_populates="costs")


class Cargo(Base):
    __tablename__ = "cargo"
    id = Column(Integer, primary_key=True)
    vessel_id = Column(Integer, ForeignKey("vessels.vessel_id"))
    commodity = Column(String)
    estimated_cargo_value_usd = Column(Integer)
    total_asset_value_at_risk_usd = Column(Integer)
    vessel = relationship("Vessel", back_populates="cargos")


class CountrySummary(Base):
    __tablename__ = "country_summary"
    summary_id = Column(Integer, primary_key=True, autoincrement=True)
    flag = Column(String, unique=True)
    total_trade_volume_usd = Column(Integer)
    total_trades = Column(Integer)
    average_trade_value_usd = Column(Integer)
    commodities = Column(String)
    date = Column(DateTime)


class TradeCategory(Base):
    __tablename__ = "trade_categories"
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    trade_tier = Column(String, unique=True)
    transit_status = Column(String)
    commodity = Column(String)


class LogsTable(Base):
    __tablename__ = "logs_table"
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    message = Column(String)
