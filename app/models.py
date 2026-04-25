from xmlrpc.client import DateTime

from dotenv import load_dotenv
import os
load_dotenv()
your_database_url = os.getenv("DATABASE_URL")
import datetime
from narwhals import Boolean, Datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
engine=create_engine(your_database_url)

from sqlalchemy.orm import declarative_base
Base=declarative_base()

from sqlalchemy  import Column ,String, Integer

class Vessel(Base):
    __tablename__="vessels"
    vessel_id=Column(Integer, primary_key=True,autoIncrement=True)
    vessel_name=Column(String)
    date=Column(Datetime)
    flag=Column(String)
    trade_tier=Column(String)
    transit_status=Column(String)
    toll_usd=Column(Integer)
    rerouted=Column(Boolean)
    commodity=Column(String)
    destination=Column(String)
    payment_rail=Column(String)
    ship_hull_value_usd=Column(Integer)
    insurance_premium_delta_pct=Column(float)
    insurance_cost_usd=Column(Integer)
    days_delayed=Column(Integer)
    extra_fuel_tonnes=Column(Integer)
    reroute_penalty_usd=Column(Integer)
    total_transit_cost_usd=Column(Integer)
    estimated_cargo_value_usd=Column(Integer)
    total_asset_value_at_risk_usd=Column(Integer)
    continent=Column(String)
    inflation_premium_per_unit=Column(float)

    routes = relationship("Route", back_populates="vessel", cascade="all, delete-orphan")
    costs = relationship("Cost", back_populates="vessel", cascade="all, delete-orphan")
    cargos = relationship("Cargo", back_populates="vessel", cascade="all, delete-orphan")
    trade_records = relationship("TradeRecord", back_populates="vessel", cascade="all, delete-orphan")
    country_summary = relationship("CountrySummary", back_populates="vessel", cascade="all, delete-orphan")
    trade_categories = relationship("TradeCategory", back_populates="vessel", cascade="all, delete-orphan")



class TradeRecord(Base):
    __tablename__ = "trade_records"

    id = Column(Integer, primary_key=True)
    vessel_id = Column(Integer, ForeignKey("vessels.vessel_id"))

    date = Column(DateTime)
    transit_status = Column(String)
    destination = Column(String)
    rerouted = Column(Boolean)
    days_delayed = Column(Integer)

    vessel = relationship("Vessel", back_populates="routes")

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
    
    vessel = relationship("Vessel", back_populates="trade_records")


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
    vessel = relationship("Vessel", back_populates="trade_categories")

class LogsTable(Base):
    __tablename__ = "logs_table"
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    message = Column(String)
