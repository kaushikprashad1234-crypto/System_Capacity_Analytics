# ============================================================
# HHS UAC PROGRAM
# EXPLORATORY DATA ANALYSIS
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

INPUT_FILE = "E:\\power bi\\System_Capacity_Analytics\\outputs\\uac_cleaned.csv"

OUTPUT_DIR = "E:\\power bi\\System_Capacity_Analytics\\outputs\\charts"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

df = pd.read_csv(
    INPUT_FILE,
    parse_dates=["Date"]
)

df = df.sort_values("Date")


# ============================================================
# DESCRIPTIVE STATISTICS
# ============================================================

print("\nDESCRIPTIVE STATISTICS")
print("=" * 60)

print(
    df[
        [
            "Children in CBP custody",
            "Children transferred out of CBP custody",
            "Children in HHS Care",
            "Children discharged from HHS Care",
            "Total System Load",
            "Net Intake Pressure"
        ]
    ].describe()
)


# ============================================================
# 1. TOTAL SYSTEM LOAD
# ============================================================

plt.figure(figsize=(15, 6))

plt.plot(
    df["Date"],
    df["Total System Load"],
    label="Total System Load"
)

plt.title(
    "Total UAC Healthcare System Load Over Time"
)

plt.xlabel("Date")
plt.ylabel("Children")

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/01_total_system_load.png",
    dpi=300
)

plt.show()


# ============================================================
# 2. CBP VS HHS
# ============================================================

plt.figure(figsize=(15, 6))

plt.plot(
    df["Date"],
    df["Children in CBP custody"],
    label="CBP Custody"
)

plt.plot(
    df["Date"],
    df["Children in HHS Care"],
    label="HHS Care"
)

plt.title(
    "CBP Custody vs HHS Care"
)

plt.xlabel("Date")
plt.ylabel("Children")

plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/02_cbp_vs_hhs.png",
    dpi=300
)

plt.show()


# ============================================================
# 3. NET INTAKE PRESSURE
# ============================================================

plt.figure(figsize=(15, 6))

plt.plot(
    df["Date"],
    df["Net Intake Pressure"],
    label="Daily Net Intake"
)

plt.axhline(
    0,
    linestyle="--"
)

plt.title(
    "Net Intake Pressure"
)

plt.xlabel("Date")
plt.ylabel("Transfers − Discharges")

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/03_net_intake.png",
    dpi=300
)

plt.show()


# ============================================================
# 4. ROLLING PRESSURE
# ============================================================

plt.figure(figsize=(15, 6))

plt.plot(
    df["Date"],
    df["7D Net Intake"],
    label="7-Day Average"
)

plt.plot(
    df["Date"],
    df["14D Net Intake"],
    label="14-Day Average"
)

plt.axhline(
    0,
    linestyle="--"
)

plt.title(
    "Rolling Net Intake Pressure"
)

plt.xlabel("Date")
plt.ylabel("Children")

plt.legend()

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/04_rolling_pressure.png",
    dpi=300
)

plt.show()


# ============================================================
# 5. BACKLOG
# ============================================================

plt.figure(figsize=(15, 6))

plt.plot(
    df["Date"],
    df["Backlog Accumulation"]
)

plt.title(
    "Cumulative Backlog Accumulation"
)

plt.xlabel("Date")
plt.ylabel("Accumulated Positive Pressure")

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_DIR}/05_backlog.png",
    dpi=300
)

plt.show()


# ============================================================
# 6. MONTHLY ANALYSIS
# ============================================================

df["Month"] = df["Date"].dt.to_period("M")

monthly = (
    df
    .groupby("Month")
    .agg(
        Average_System_Load=(
            "Total System Load",
            "mean"
        ),
        Average_HHS_Load=(
            "Children in HHS Care",
            "mean"
        ),
        Average_CBP_Load=(
            "Children in CBP custody",
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

monthly["Net_Pressure"] = (
    monthly["Total_Transfers"]
    -
    monthly["Total_Discharges"]
)

print("\nMONTHLY ANALYSIS")
print(monthly.tail(12))


# ============================================================
# 7. VOLATILITY
# ============================================================

df["Load Change"] = (
    df["Total System Load"].diff()
)

volatility = (
    df["Load Change"]
    .std()
)

print(
    "\nCare Load Volatility Index:",
    round(volatility, 2)
)


# ============================================================
# 8. ANOMALIES
# ============================================================

print("\nDATA QUALITY")
print("=" * 60)

print(
    "Transfer anomalies:",
    df["Transfer_Anomaly"].sum()
)

print(
    "Discharge anomalies:",
    df["Discharge_Anomaly"].sum()
)

print(
    "Missing values:"
)

print(
    df.isna().sum()
)