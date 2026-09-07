from pathlib import Path
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "house_price_model.joblib"


def predict_house_price(values: dict) -> float:
    bundle = joblib.load(MODEL_PATH)
    row = pd.DataFrame(
        [[values[feature] for feature in bundle["features"]]],
        columns=bundle["features"],
    )
    return float(bundle["model"].predict(row)[0])


if __name__ == "__main__":
    example = {
        "MedInc": 8.0,
        "HouseAge": 30.0,
        "AveRooms": 6.0,
        "AveBedrms": 1.0,
        "Population": 800.0,
        "AveOccup": 3.0,
        "Latitude": 34.0,
        "Longitude": -118.0,
    }

    if not MODEL_PATH.exists():
        print("Model not found. Run: python src/train.py")
    else:
        prediction = predict_house_price(example)
        print(f"Predicted median house value: ${prediction * 100000:,.2f}")
