import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor


def forecast(df, column, days=30):
    """
    Forecast future values of a numeric column.
    Returns the saved graph image path.
    """

    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found.")

    if not np.issubdtype(df[column].dtype, np.number):
        raise ValueError(f"Column '{column}' is not numeric.")

    y = df[column].dropna().values

    X = np.arange(len(y)).reshape(-1, 1)

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    future_X = np.arange(
        len(y),
        len(y) + days
    ).reshape(-1, 1)

    prediction = model.predict(future_X)

    plt.figure(figsize=(10, 5))

    plt.plot(
        range(len(y)),
        y,
        label="Historical Data",
        color="blue"
    )

    plt.plot(
        range(len(y), len(y) + days),
        prediction,
        "--",
        label="Forecast",
        color="red"
    )

    plt.title(f"30-Day Forecast: {column}")
    plt.xlabel("Time")
    plt.ylabel(column)
    plt.legend()
    plt.grid(True)

    filename = "forecast.png"

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

    return filename