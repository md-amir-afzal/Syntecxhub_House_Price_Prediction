from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "house_price_model.joblib"

st.set_page_config(page_title="House Price Predictor", page_icon="🏠")
st.title("🏠 House Price Prediction")
st.caption("Syntecxhub Machine Learning Internship — Linear Regression")

if not MODEL_PATH.exists():
    st.warning("Model is not trained yet.")
    st.code("python src/train.py")
    st.stop()

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
features = bundle["features"]

defaults = {
    "MedInc": 8.0,
    "HouseAge": 30.0,
    "AveRooms": 6.0,
    "AveBedrms": 1.0,
    "Population": 800.0,
    "AveOccup": 3.0,
    "Latitude": 34.0,
    "Longitude": -118.0,
}

values = {}
for feature in features:
    values[feature] = st.number_input(
        feature, value=float(defaults.get(feature, 0.0)), format="%.4f"
    )

if st.button("Predict House Value", type="primary"):
    row = pd.DataFrame([[values[f] for f in features]], columns=features)
    prediction = float(model.predict(row)[0])
    st.success(f"Estimated median house value: ${prediction * 100000:,.2f}")
