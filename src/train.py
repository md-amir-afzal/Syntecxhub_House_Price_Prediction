from pathlib import Path
import json

import joblib
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "models"
REPORT_DIR = ROOT / "reports"
MODEL_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "house_price_model.joblib"
RESULT_PATH = REPORT_DIR / "model_results.json"


def load_data() -> pd.DataFrame:
    housing = fetch_california_housing(as_frame=True)
    df = housing.frame.copy()
    df = df.drop_duplicates().dropna()
    return df


def train_model(df: pd.DataFrame):
    target = "MedHouseVal"
    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    coefficients = dict(zip(X.columns, model.coef_))

    joblib.dump(
        {"model": model, "features": list(X.columns), "target": target},
        MODEL_PATH,
    )

    results = {
        "model": "Linear Regression",
        "dataset_rows": int(len(df)),
        "features": list(X.columns),
        "rmse": float(rmse),
        "r2": float(r2),
        "intercept": float(model.intercept_),
        "coefficients": {k: float(v) for k, v in coefficients.items()},
        "sample_predictions": [
            {"actual": float(a), "predicted": float(p)}
            for a, p in zip(y_test.iloc[:5], predictions[:5])
        ],
    }

    RESULT_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return model, results


if __name__ == "__main__":
    data = load_data()
    print("Dataset shape:", data.shape)
    print("\nMissing values:\n", data.isna().sum())
    print("\nFeature summary:\n", data.describe().round(2))

    _, results = train_model(data)

    print("\n--- Model Evaluation ---")
    print(f"RMSE: {results['rmse']:.4f}")
    print(f"R²:   {results['r2']:.4f}")

    print("\n--- Coefficients ---")
    for feature, coefficient in results["coefficients"].items():
        print(f"{feature:>10}: {coefficient:+.6f}")

    print(f"\nModel saved to: {MODEL_PATH}")
    print(f"Results saved to: {RESULT_PATH}")
