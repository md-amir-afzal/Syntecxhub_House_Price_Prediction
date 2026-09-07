# Syntecxhub House Price Prediction

Professional Machine Learning internship project for Syntecxhub Week 1.

## Objective
Build a Linear Regression model to predict house prices from housing features.

## Requirements covered
- Load a housing dataset
- Clean and explore features
- Select features
- Train/test split
- Linear Regression
- RMSE and R² evaluation
- Interpret model coefficients
- Save trained model
- Generate example predictions

## Dataset
Uses the California Housing dataset available through scikit-learn.

## Setup
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Train
```bash
python src/train.py
```

## Predict
```bash
python src/predict.py
```

## Web demo
```bash
streamlit run app.py
```

## Tests
```bash
pytest
```

## Suggested GitHub repository name
`Syntecxhub_House_Price_Prediction`
