from dotenv import load_dotenv
import os
load_dotenv()
your_database_url = os.getenv("DATABASE_URL")
import datetime
from narwhals import Datetime
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
    rerouted=Column(Integer)
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

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    vessel_id = Column(Integer, ForeignKey("vessels.vessel_id"))

    date = Column(DateTime)
    transit_status = Column(String)
    destination = Column(String)
    rerouted = Column(Integer)
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