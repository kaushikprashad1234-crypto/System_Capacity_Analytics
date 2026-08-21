# ============================================================
# HHS UAC PROGRAM
# HEALTHCARE CAPACITY & PRESSURE ANALYSIS
# ============================================================

import pandas as pd
import numpy as np

INPUT_FILE = "E:\\power bi\\System_Capacity_Analytics\\outputs\\uac_cleaned.csv"

df = pd.read_csv(
    INPUT_FILE,
    parse_dates=["Date"]
)

df = df.sort_values("Date").reset_index(drop=True)


# ============================================================
# KPI 1 — TOTAL CHILDREN UNDER CARE
# ============================================================

latest = df.iloc[-1]

total_children = (
    latest["Children in CBP custody"]
    +
    latest["Children in HHS Care"]
)

print("=" * 70)
print("HEALTHCARE CAPACITY KPI REPORT")
print("=" * 70)

print(
    f"\nLatest Reporting Date: "
    f"{latest['Date'].date()}"
)

print(
    f"Total Children Under Care: "
    f"{total_children:,.0f}"
)


# ============================================================
# KPI 2 — NET INTAKE PRESSURE
# ============================================================

net_pressure = (
    latest["Children transferred out of CBP custody"]
    -
    latest["Children discharged from HHS Care"]
)

print(
    f"Net Intake Pressure: "
    f"{net_pressure:,.0f}"
)


# ============================================================
# KPI 3 — HHS SHARE OF SYSTEM
# ============================================================

hhs_share = (
    latest["Children in HHS Care"]
    /
    total_children
    *
    100
)

print(
    f"HHS Share of System Load: "
    f"{hhs_share:.2f}%"
)


# ============================================================
# KPI 4 — DISCHARGE OFFSET RATIO
# ============================================================

transfers = (
    df["Children transferred out of CBP custody"]
)

discharges = (
    df["Children discharged from HHS Care"]
)

df["Discharge Offset Ratio"] = np.where(
    transfers > 0,
    discharges / transfers,
    np.nan
)

print(
    "Average Discharge Offset Ratio:",
    round(
        df["Discharge Offset Ratio"].mean(),
        3
    )
)


# ============================================================
# KPI 5 — VOLATILITY
# ============================================================

df["Daily Load Change"] = (
    df["Total System Load"].diff()
)

volatility_index = (
    df["Daily Load Change"]
    .std()
)

print(
    f"Care Load Volatility Index: "
    f"{volatility_index:.2f}"
)


# ============================================================
# KPI 6 — BACKLOG
# ============================================================

df["Positive Pressure"] = (
    df["Net Intake Pressure"]
    .clip(lower=0)
)

df["Cumulative Backlog"] = (
    df["Positive Pressure"].cumsum()
)

print(
    f"Cumulative Positive Pressure: "
    f"{df['Cumulative Backlog'].iloc[-1]:,.0f}"
)


# ============================================================
# HIGH PRESSURE DAYS
# ============================================================

threshold = (
    df["Net Intake Pressure"]
    .quantile(0.90)
)

high_pressure = df[
    df["Net Intake Pressure"] >= threshold
]

print(
    "\n90th Percentile Pressure Threshold:",
    round(threshold, 2)
)

print(
    "High-pressure observations:",
    len(high_pressure)
)


# ============================================================
# SUSTAINED PRESSURE
# ============================================================

df["Pressure_7D"] = (
    df["Net Intake Pressure"]
    .rolling(7)
    .mean()
)

df["Sustained_Pressure"] = (
    df["Pressure_7D"] > 0
)

print(
    "\nSustained pressure observations:",
    df["Sustained_Pressure"].sum()
)


# ============================================================
# MONTHLY KPI TABLE
# ============================================================

df["Month"] = (
    df["Date"]
    .dt.to_period("M")
)

monthly_kpi = (
    df
    .groupby("Month")
    .agg(
        Average_Load=(
            "Total System Load",
            "mean"
        ),
        Maximum_Load=(
            "Total System Load",
            "max"
        ),
        Average_Pressure=(
            "Net Intake Pressure",
            "mean"
        ),
        Total_Transfers=(
            "Children transferred out of CBP custody",
            "sum"
        ),
        Total_Discharges=(
            "Children discharged from HHS Care",
            "sum"
        )
    )
    .reset_index()
)

monthly_kpi["Net_Flow"] = (
    monthly_kpi["Total_Transfers"]
    -
    monthly_kpi["Total_Discharges"]
)

print("\nMONTHLY KPI TABLE")

print(
    monthly_kpi.tail(12).to_string(
        index=False
    )
)