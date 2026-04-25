import joblib
import numpy as np
import pandas as pd
from pathlib import Path

MODEL_DIR = Path("notebooks/models")

RF_MODEL_PATH = MODEL_DIR / "rf_model.pkl"
CG_MODEL_PATH = MODEL_DIR / "country_growth_model.pkl"
LE_PATH = MODEL_DIR / "label_encoder.pkl"

# RF model predicts transit_status (0=Blocked, 1=Passed, 2=Rerouted)
RF_FEATURES = [
    "mmsi", "flag_Germany", "flag_Greece", "flag_India", "flag_Iran",
    "flag_Iraq", "flag_Israel", "flag_Liberia", "flag_Marshall Islands",
    "flag_Norway", "flag_Pakistan", "flag_Panama", "flag_Russia",
    "flag_Turkey", "flag_UAE", "flag_UK", "flag_USA",
    "trade_tier_Privileged", "trade_tier_Taxed",
    "commodity_Container Ship", "commodity_Crude Oil",
    "commodity_Crude Oil Tanker", "commodity_LNG Carrier", "commodity_Various",
    "destination_Hidden", "destination_Hidden/Private", "destination_Houston",
    "destination_Mumbai", "destination_Ningbo", "destination_Rotterdam",
    "destination_Singapore", "payment_rail_Other Non-USD",
    "payment_rail_Tether (USDT) / Yuan", "payment_rail_Yuan (e-CNY/CIPS)",
    "continent_Asia", "continent_Eurasia", "continent_Europe",
    "continent_North America", "continent_Oceania",
]

CG_FEATURES = [
    "toll_usd", "rerouted", "ship_hull_value_usd", "insurance_premium_delta_pct",
    "insurance_cost_usd", "days_delayed", "extra_fuel_tonnes", "reroute_penalty_usd",
    "total_transit_cost_usd", "estimated_cargo_value_usd", "total_asset_value_at_risk_usd",
    "inflation_premium_per_unit", "month", "year",
    "flag_Germany", "flag_Greece", "flag_India", "flag_Iran", "flag_Iraq",
    "flag_Israel", "flag_Liberia", "flag_Marshall Islands", "flag_Norway",
    "flag_Pakistan", "flag_Panama", "flag_Russia", "flag_Turkey",
    "flag_UAE", "flag_UK", "flag_USA",
    "trade_tier_Privileged", "trade_tier_Taxed",
    "transit_status_Passed", "transit_status_Rerouted",
    "commodity_Container Ship", "commodity_Crude Oil",
    "commodity_Crude Oil Tanker", "commodity_LNG Carrier", "commodity_Various",
    "destination_Hidden", "destination_Hidden/Private", "destination_Houston",
    "destination_Mumbai", "destination_Ningbo", "destination_Rotterdam",
    "destination_Singapore", "payment_rail_Other Non-USD",
    "payment_rail_Tether (USDT) / Yuan", "payment_rail_Yuan (e-CNY/CIPS)",
    "continent_Asia", "continent_Eurasia", "continent_Europe",
    "continent_North America", "continent_Oceania",
]


def _one_hot(data: dict, feature_list: list) -> pd.DataFrame:
    """Build a single-row DataFrame with all required one-hot columns."""
    row = {col: 0 for col in feature_list}
    for key, val in data.items():
        ohe_key = f"{key}_{val}"
        if ohe_key in row:
            row[ohe_key] = 1
        elif key in row:
            row[key] = val
    return pd.DataFrame([row])[feature_list]


def predict_transit_status(input_data: dict) -> dict:
    """Random Forest: predict transit status (Passed / Rerouted / Blocked)."""
    rf = joblib.load(RF_MODEL_PATH)
    le = joblib.load(LE_PATH)
    X = _one_hot(input_data, RF_FEATURES)
    pred_class = int(rf.predict(X)[0])
    proba = rf.predict_proba(X)[0].tolist()
    label = le.classes_[pred_class]
    return {
        "predicted_transit_status": label,
        "probabilities": {le.classes_[i]: round(p, 4) for i, p in enumerate(proba)},
    }


def predict_growth(input_data: dict) -> dict:
    """Linear Regression: predict total asset value at risk (country growth model)."""
    bundle = joblib.load(CG_MODEL_PATH)
    model = bundle["model"]
    scaler = bundle["scaler"]
    X = _one_hot(input_data, CG_FEATURES)
    X_scaled = scaler.transform(X)
    prediction = float(model.predict(X_scaled)[0])
    return {"predicted_total_asset_value_at_risk_usd": round(prediction, 2)}
