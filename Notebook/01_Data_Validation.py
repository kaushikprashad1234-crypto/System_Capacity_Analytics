# ============================================================
# HHS UAC PROGRAM
# DATA VALIDATION & NORMALIZATION
# ============================================================

import pandas as pd
import numpy as np

INPUT_FILE = "E:\\power bi\\System_Capacity_Analytics\\Data\\HHS_Unaccompanied_Alien_Children_Program.csv"
OUTPUT_FILE = "E:\\power bi\\System_Capacity_Analytics\\outputs\\uac_cleaned.csv"

# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("DATASET INFORMATION")
print("=" * 70)

print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")
print("\nColumns:")
print(df.columns.tolist())


# ------------------------------------------------------------
# 2. REMOVE COMPLETELY EMPTY ROWS
# ------------------------------------------------------------

before = len(df)

df = df.dropna(how="all").copy()

after = len(df)

print(f"\nRemoved blank rows: {before - after}")


# ------------------------------------------------------------
# 3. CLEAN COLUMN NAMES
# ------------------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
)


# ------------------------------------------------------------
# 4. DATE CONVERSION
# ------------------------------------------------------------

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

print("\nInvalid dates:", df["Date"].isna().sum())


# ------------------------------------------------------------
# 5. NUMERIC COLUMNS
# ------------------------------------------------------------

numeric_columns = [
    "Children apprehended and placed in CBP custody*",
    "Children in CBP custody",
    "Children transferred out of CBP custody",
    "Children in HHS Care",
    "Children discharged from HHS Care"
]

for col in numeric_columns:

    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )


# ------------------------------------------------------------
# 6. SORT CHRONOLOGICALLY
# ------------------------------------------------------------

df = (
    df
    .sort_values("Date")
    .reset_index(drop=True)
)


# ------------------------------------------------------------
# 7. DUPLICATE DATE CHECK
# ------------------------------------------------------------

duplicate_dates = df["Date"].duplicated().sum()

print("Duplicate dates:", duplicate_dates)


# ------------------------------------------------------------
# 8. MISSING CALENDAR DATES
# ------------------------------------------------------------

full_date_range = pd.date_range(
    start=df["Date"].min(),
    end=df["Date"].max(),
    freq="D"
)

missing_dates = full_date_range.difference(
    df["Date"]
)

print("Expected calendar days:", len(full_date_range))
print("Observed reporting days:", df["Date"].nunique())
print("Missing calendar days:", len(missing_dates))


# ------------------------------------------------------------
# 9. LOGICAL VALIDATION
# ------------------------------------------------------------

df["Transfer_Anomaly"] = (
    df["Children transferred out of CBP custody"]
    > df["Children in CBP custody"]
)

df["Discharge_Anomaly"] = (
    df["Children discharged from HHS Care"]
    > df["Children in HHS Care"]
)

print(
    "Transfer anomalies:",
    df["Transfer_Anomaly"].sum()
)

print(
    "Discharge anomalies:",
    df["Discharge_Anomaly"].sum()
)


# ------------------------------------------------------------
# 10. DERIVED METRICS
# ------------------------------------------------------------

df["Total System Load"] = (
    df["Children in CBP custody"]
    +
    df["Children in HHS Care"]
)

df["Net Intake Pressure"] = (
    df["Children transferred out of CBP custody"]
    -
    df["Children discharged from HHS Care"]
)


# ------------------------------------------------------------
# 11. DAILY LOAD CHANGE
# ------------------------------------------------------------

df["Daily Load Change"] = (
    df["Total System Load"].diff()
)


# ------------------------------------------------------------
# 12. LOAD GROWTH %
# ------------------------------------------------------------

df["Care Load Growth Rate"] = (
    df["Total System Load"]
    .pct_change()
    * 100
)


# ------------------------------------------------------------
# 13. ROLLING PRESSURE
# ------------------------------------------------------------

df["7D Net Intake"] = (
    df["Net Intake Pressure"]
    .rolling(7, min_periods=1)
    .mean()
)

df["14D Net Intake"] = (
    df["Net Intake Pressure"]
    .rolling(14, min_periods=1)
    .mean()
)


# ------------------------------------------------------------
# 14. BACKLOG INDICATOR
# ------------------------------------------------------------

df["Backlog Accumulation"] = (
    df["Net Intake Pressure"]
    .clip(lower=0)
    .cumsum()
)


# ------------------------------------------------------------
# 15. REPORTING FLAG
# ------------------------------------------------------------

df["Reporting Available"] = True


# ------------------------------------------------------------
# 16. SAVE CLEAN DATA
# ------------------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nClean dataset saved:")
print(OUTPUT_FILE)

print("\nFinal shape:", df.shape)