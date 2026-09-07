import pandas as pd
from sklearn.linear_model import LinearRegression


def test_linear_regression_can_fit():
    X = pd.DataFrame({"feature": [1, 2, 3, 4, 5]})
    y = pd.Series([2, 4, 6, 8, 10])

    model = LinearRegression()
    model.fit(X, y)

    prediction = model.predict(pd.DataFrame({"feature": [6]}))[0]
    assert round(prediction, 6) == 12.0
