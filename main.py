"""Real Estate Price Predictor - Group 9.
Core data loading, feature engineering, model training and prediction.
"""
from __future__ import annotations
import csv
from pathlib import Path
from typing import Dict, List, Tuple

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "examples" / "real_estate_data.csv"
FEATURES = ["area_sqft", "bedrooms", "bathrooms", "age_years", "floor", "parking", "location"]

LOCATION_PREMIUM = {
    "Kolkata": 1.00, "Howrah": 0.78, "Salt Lake": 1.32,
    "New Town": 1.25, "Bardhaman": 0.62, "Durgapur": 0.72
}

def load_dataset(path: Path = DATA_PATH) -> List[dict]:
    """Load the included CSV dataset and convert numeric fields."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append({
                "area_sqft": float(row["area_sqft"]),
                "bedrooms": int(row["bedrooms"]),
                "bathrooms": int(row["bathrooms"]),
                "age_years": int(row["age_years"]),
                "floor": int(row["floor"]),
                "parking": int(row["parking"]),
                "location": row["location"],
                "price_lakh": float(row["price_lakh"]),
            })
    if len(rows) < 20:
        raise ValueError("Dataset must contain at least 20 records.")
    return rows

def estimate_price_lakh(property_data: Dict) -> float:
    """Transparent baseline estimator used if scikit-learn is unavailable."""
    area = float(property_data["area_sqft"])
    beds = int(property_data["bedrooms"])
    baths = int(property_data["bathrooms"])
    age = int(property_data["age_years"])
    floor = int(property_data["floor"])
    parking = int(property_data["parking"])
    location = property_data["location"]
    if area <= 0 or beds < 1 or baths < 1 or age < 0 or floor < 0:
        raise ValueError("Please enter valid positive property details.")
    premium = LOCATION_PREMIUM.get(location, 0.85)
    rate = 0.0068 * premium
    price = area * rate
    price += beds * 1.15 + baths * 0.8 + parking * 1.4 + min(floor, 20) * 0.12
    price *= max(0.62, 1 - age * 0.006)
    return max(5.0, price)

def train_model(rows=None):
    """Train a Random Forest model; return (model, metrics, method)."""
    rows = rows or load_dataset()
    try:
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder
        from sklearn.pipeline import Pipeline
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import mean_absolute_error, r2_score
        import pandas as pd

        frame = pd.DataFrame(rows)
        X = frame[FEATURES]
        y = frame["price_lakh"]
        pre = ColumnTransformer([
            ("location", OneHotEncoder(handle_unknown="ignore"), ["location"])
        ], remainder="passthrough")
        model = Pipeline([
            ("preprocessor", pre),
            ("regressor", RandomForestRegressor(n_estimators=180, random_state=42, min_samples_leaf=2))
        ])
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        metrics = {
            "mae": float(mean_absolute_error(y_test, pred)),
            "r2": float(r2_score(y_test, pred)),
            "samples": len(rows),
            "test_samples": len(y_test)
        }
        return model, metrics, "Random Forest"
    except ImportError:
        return None, {"mae": None, "r2": None, "samples": len(rows), "test_samples": 0}, "Rule-based fallback"

def predict_price(property_data: Dict, model=None) -> Tuple[float, str]:
    """Predict property price in Indian lakh rupees."""
    if model is not None:
        import pandas as pd
        row = {key: property_data[key] for key in FEATURES}
        value = float(model.predict(pd.DataFrame([row]))[0])
        return max(1.0, value), "Random Forest"
    return estimate_price_lakh(property_data), "Rule-based estimate"

def format_price(value_lakh: float) -> str:
    if value_lakh >= 100:
        return f"₹{value_lakh/100:.2f} crore"
    return f"₹{value_lakh:.2f} lakh"

if __name__ == "__main__":
    data = load_dataset()
    model, metrics, method = train_model(data)
    sample = dict(area_sqft=1200, bedrooms=3, bathrooms=2, age_years=5,
                  floor=4, parking=1, location="Kolkata")
    price, used = predict_price(sample, model)
    print("REAL ESTATE PRICE PREDICTOR")
    print(f"Model: {method} | Dataset records: {metrics['samples']}")
    if metrics["mae"] is not None:
        print(f"MAE: {metrics['mae']:.2f} lakh | R²: {metrics['r2']:.3f}")
    print(f"Sample prediction: {format_price(price)} ({used})")
