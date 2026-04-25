import os
from typing import Generator
from dotenv import load_dotenv
from sql_alchemy import create_engine,Engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set.")

engine: Engine = create_engine(DATABASE_URL, connect_args={"sslmode":"require"})

SessionLocal:sessionmaker = sessionmaker(
    autocomplete=False,autoflush=False,bind=engine
    )

Base = declarative_base()

def get_db() -> Generator(Session,None,None):
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()