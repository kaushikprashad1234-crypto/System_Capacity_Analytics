# ============================================================
# HHS UAC PROGRAM
# CARE LOAD FORECASTING
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from statsmodels.tsa.holtwinters import ExponentialSmoothing

INPUT_FILE = "E:\\power bi\\System_Capacity_Analytics\\outputs\\uac_cleaned.csv"

df = pd.read_csv(
    INPUT_FILE,
    parse_dates=["Date"]
)

df = (
    df
    .sort_values("Date")
    .set_index("Date")
)


# ============================================================
# MONTHLY AGGREGATION
# ============================================================

monthly = (
    df["Total System Load"]
    .resample("MS")
    .mean()
)

# Do NOT interpret missing reporting periods as zero
monthly = monthly.interpolate(
    method="time",
    limit_direction="both"
)


# ============================================================
# TRAIN / TEST
# ============================================================

test_size = 6

train = monthly.iloc[:-test_size]

test = monthly.iloc[-test_size:]


# ============================================================
# HOLT-WINTERS
# ============================================================

model = ExponentialSmoothing(
    train,
    trend="add",
    seasonal="add",
    seasonal_periods=12
)

fit = model.fit(
    optimized=True
)


# ============================================================
# FORECAST TEST PERIOD
# ============================================================

forecast = fit.forecast(
    test_size
)


# ============================================================
# ERROR METRICS
# ============================================================

mae = np.mean(
    np.abs(
        test.values
        -
        forecast.values
    )
)

rmse = np.sqrt(
    np.mean(
        (
            test.values
            -
            forecast.values
        ) ** 2
    )
)

print("=" * 60)
print("FORECAST PERFORMANCE")
print("=" * 60)

print(
    f"MAE: {mae:,.2f}"
)

print(
    f"RMSE: {rmse:,.2f}"
)


# ============================================================
# FUTURE FORECAST
# ============================================================

future_model = ExponentialSmoothing(
    monthly,
    trend="add",
    seasonal="add",
    seasonal_periods=12
)

future_fit = future_model.fit(
    optimized=True
)

future_forecast = (
    future_fit.forecast(6)
)

print("\nNEXT 6 MONTHS FORECAST")

print(
    future_forecast
)


# ============================================================
# VISUALIZATION
# ============================================================

plt.figure(figsize=(15, 6))

plt.plot(
    monthly.index,
    monthly.values,
    label="Historical Load"
)

plt.plot(
    future_forecast.index,
    future_forecast.values,
    linestyle="--",
    label="Forecast"
)

plt.title(
    "Forecast of Average UAC System Load"
)

plt.xlabel("Date")
plt.ylabel("Children")

plt.legend()

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    "E:\\power bi\\System_Capacity_Analytics\\outputs\\charts\\06_load_forecast.png",
    dpi=300
)

plt.show()