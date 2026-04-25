from fastapi import FastAPI
from app.database import Base, engine
from app.routers import trade, analytics, prediction

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hormuz Trade Analytics API",
    version="1.0.0",
    description="Trade analytics and prediction API for Hormuz strait trade data.",
)

app.include_router(trade.router)
app.include_router(analytics.router)
app.include_router(prediction.router)


@app.get("/")
def root():
    return {"message": "Hormuz Trade Analytics API is running"}
