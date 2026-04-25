from typing import Generator
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from app.config import DATABASE_URL

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")

engine: Engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
