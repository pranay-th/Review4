# Hormuz Trade Analytics API

A backend-powered analytical system for maritime trade data through the Strait of Hormuz. Covers data cleaning, database design, REST APIs, and ML inference.

---

## Dataset

- Source: `hormuz_trade_uncleaned.csv` — 1890 rows, 23 columns
- Covers vessel trade records from March–May 2026 including costs, routing, cargo, and country flags

---

## Data Analysis

Performed in `notebooks/analysis.ipynb` using Pandas, NumPy, and Plotly.

- Dropped `naval_escort_status` (excessive nulls)
- Filled `inflation_premium_per_unit` missing values with mode
- Converted date columns, encoded categoricals
- Feature engineering: extracted `month`, `year`, one-hot encoded flags, tiers, commodities

**Visualizations**

![Top Countries by Trade Value](visuals/top_countries.png)
![Region-wise Trade Distribution](visuals/region_distribution.png)
![Monthly Trade Trend](visuals/trade_trend.png)

---

## Database

PostgreSQL hosted on NeonDB. Schema designed with 6 normalized tables:

| Table | Purpose |
|-------|---------|
| `vessels` | Main trade records |
| `trade_records` | Transit and routing info per vessel |
| `costs` | Cost breakdown per vessel |
| `cargo` | Cargo and value info per vessel |
| `country_summary` | Aggregated stats per country |
| `trade_categories` | Distinct trade tier lookup |

Includes PL/pgSQL functions, AFTER INSERT triggers (auto-logging to `logs_table`), aggregations, and JOIN queries. See `sql/schema.sql`.

---

## Machine Learning

Two models trained in the notebook and saved to `notebooks/models/`:

| Model | Type | Predicts |
|-------|------|---------|
| `rf_model.pkl` | Random Forest Classifier | Transit status: `Passed / Rerouted / Blocked` |
| `country_growth_model.pkl` | Linear Regression + StandardScaler | `total_asset_value_at_risk_usd` |

Random Forest accuracy: ~85–90%

---

## Backend API

Built with FastAPI + SQLAlchemy ORM, connected to NeonDB.

**Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/load-csv` | Bulk load dataset into all tables |
| POST | `/load-country-summary` | Load country summary CSV |
| POST | `/vessels/` | Insert a vessel record |
| GET | `/vessels/` | List vessels with optional filters |
| GET | `/vessels/{id}` | Get vessel by ID |
| DELETE | `/vessels/{id}` | Delete a vessel |
| GET | `/top-countries` | Top countries by transit cost |
| GET | `/region-summary` | Cost breakdown by continent |
| GET | `/trade-trends` | Monthly trade volume and cost |
| POST | `/predict-transit` | Predict transit status (RF model) |
| POST | `/predict-growth` | Predict asset value at risk (Linear Regression) |

Swagger UI: `http://127.0.0.1:8000/docs`

---

## Setup

```bash
pip install -r requirements.txt
```

`.env`:
```
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
```

```bash
uvicorn app.main:app --reload
```

---

## Project Structure

```
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── csv_loader.py
│   ├── routers/
│   │   ├── trade.py
│   │   ├── analytics.py
│   │   ├── prediction.py
│   │   └── loader.py
│   └── services/
│       ├── ml_service.py
│       └── analytics_service.py
├── notebooks/
│   ├── analysis.ipynb
│   └── models/
├── dataset/
├── sql/
├── visuals/
└── requirements.txt
```
