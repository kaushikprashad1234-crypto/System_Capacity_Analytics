# ============================================================
# HHS UAC HEALTHCARE CAPACITY DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="System Capacity Analytics",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "outputs" / "uac_cleaned.csv"


@st.cache_data
def load_data():

    if not DATA_FILE.exists():
        st.error(
            f"Could not find {DATA_FILE.name}. "
            "Please ensure the CSV exists in the Data folder."
        )
        st.stop()

    df = pd.read_csv(
        DATA_FILE,
        parse_dates=["Date"]
    )

    return df


df = load_data()


# ============================================================
# TITLE
# ============================================================

st.title(
    "🏥 HHS Unaccompanied Alien Children Program"
)

st.subheader(
    "Healthcare Capacity, Care Load & Flow Monitoring"
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "Dashboard Filters"
)

min_date = df["Date"].min()
max_date = df["Date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

granularity = st.sidebar.selectbox(
    "Time Granularity",
    [
        "Daily",
        "Weekly",
        "Monthly"
    ]
)


# ============================================================
# FILTER
# ============================================================

if len(date_range) == 2:

    start_date = pd.Timestamp(
        date_range[0]
    )

    end_date = pd.Timestamp(
        date_range[1]
    )

    filtered = df[
        (df["Date"] >= start_date)
        &
        (df["Date"] <= end_date)
    ].copy()

else:

    filtered = df.copy()


# ============================================================
# LATEST KPI
# ============================================================

latest = filtered.iloc[-1]

total_load = (
    latest["Children in CBP custody"]
    +
    latest["Children in HHS Care"]
)

net_pressure = (
    latest["Children transferred out of CBP custody"]
    -
    latest["Children discharged from HHS Care"]
)

hhs_load = (
    latest["Children in HHS Care"]
)

cbp_load = (
    latest["Children in CBP custody"]
)

pressure_7d = (
    filtered["Net Intake Pressure"]
    .tail(7)
    .mean()
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Children Under Care",
    f"{total_load:,.0f}"
)

col2.metric(
    "HHS Care",
    f"{hhs_load:,.0f}"
)

col3.metric(
    "CBP Custody",
    f"{cbp_load:,.0f}"
)

col4.metric(
    "Net Intake Pressure",
    f"{net_pressure:,.0f}"
)

col5.metric(
    "7-Day Pressure",
    f"{pressure_7d:,.1f}"
)


# ============================================================
# SYSTEM LOAD
# ============================================================

st.header(
    "System Load Overview"
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=filtered["Date"],
        y=filtered["Children in CBP custody"],
        name="CBP Custody",
        mode="lines"
    )
)

fig.add_trace(
    go.Scatter(
        x=filtered["Date"],
        y=filtered["Children in HHS Care"],
        name="HHS Care",
        mode="lines"
    )
)

fig.add_trace(
    go.Scatter(
        x=filtered["Date"],
        y=filtered["Total System Load"],
        name="Total System Load",
        mode="lines"
    )
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Children",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# TWO COLUMN ANALYSIS
# ============================================================

left, right = st.columns(2)


# ------------------------------------------------------------
# NET INTAKE
# ------------------------------------------------------------

with left:

    st.subheader(
        "Net Intake Pressure"
    )

    fig_pressure = px.bar(
        filtered,
        x="Date",
        y="Net Intake Pressure",
        title="Transfers − Discharges"
    )

    fig_pressure.add_hline(
        y=0,
        line_dash="dash"
    )

    st.plotly_chart(
        fig_pressure,
        use_container_width=True
    )


# ------------------------------------------------------------
# ROLLING PRESSURE
# ------------------------------------------------------------

with right:

    st.subheader(
        "Rolling Pressure"
    )

    fig_rolling = go.Figure()

    fig_rolling.add_trace(
        go.Scatter(
            x=filtered["Date"],
            y=filtered["7D Net Intake"],
            name="7-Day"
        )
    )

    fig_rolling.add_trace(
        go.Scatter(
            x=filtered["Date"],
            y=filtered["14D Net Intake"],
            name="14-Day"
        )
    )

    fig_rolling.add_hline(
        y=0,
        line_dash="dash"
    )

    fig_rolling.update_layout(
        xaxis_title="Date",
        yaxis_title="Pressure"
    )

    st.plotly_chart(
        fig_rolling,
        use_container_width=True
    )


# ============================================================
# BACKLOG
# ============================================================

st.header(
    "Backlog Accumulation"
)

fig_backlog = px.area(
    filtered,
    x="Date",
    y="Backlog Accumulation",
    title="Cumulative Positive Intake Pressure"
)

st.plotly_chart(
    fig_backlog,
    use_container_width=True
)


# ============================================================
# CARE PIPELINE
# ============================================================

st.header(
    "Healthcare Pipeline"
)

pipeline_values = [
    filtered[
        "Children apprehended and placed in CBP custody*"
    ].mean(),

    filtered[
        "Children transferred out of CBP custody"
    ].mean(),

    filtered[
        "Children in HHS Care"
    ].mean(),

    filtered[
        "Children discharged from HHS Care"
    ].mean()
]

pipeline = pd.DataFrame(
    {
        "Stage": [
            "CBP Apprehensions",
            "Transfers to HHS",
            "HHS Care",
            "Discharges"
        ],
        "Average": pipeline_values
    }
)

fig_pipeline = px.bar(
    pipeline,
    x="Stage",
    y="Average",
    title="Average Pipeline Activity"
)

st.plotly_chart(
    fig_pipeline,
    use_container_width=True
)


# ============================================================
# MONTHLY SUMMARY
# ============================================================

st.header(
    "Monthly Performance"
)

monthly = (
    filtered
    .assign(
        Month=filtered["Date"].dt.to_period("M")
    )
    .groupby("Month")
    .agg(
        Average_Load=(
            "Total System Load",
            "mean"
        ),
        Average_HHS=(
            "Children in HHS Care",
            "mean"
        ),
        Average_CBP=(
            "Children in CBP custody",
            "mean"
        ),
        Transfers=(
            "Children transferred out of CBP custody",
            "sum"
        ),
        Discharges=(
            "Children discharged from HHS Care",
            "sum"
        )
    )
    .reset_index()
)

monthly["Net Pressure"] = (
    monthly["Transfers"]
    -
    monthly["Discharges"]
)

monthly["Month"] = (
    monthly["Month"]
    .astype(str)
)

st.dataframe(
    monthly,
    use_container_width=True
)


# ============================================================
# DATA QUALITY
# ============================================================

st.header(
    "Data Quality & Validation"
)

q1, q2, q3, q4 = st.columns(4)

q1.metric(
    "Reporting Days",
    f"{len(filtered):,}"
)

q2.metric(
    "Transfer Anomalies",
    f"{filtered['Transfer_Anomaly'].sum():,}"
)

q3.metric(
    "Discharge Anomalies",
    f"{filtered['Discharge_Anomaly'].sum():,}"
)

q4.metric(
    "Missing Values",
    f"{filtered.isna().sum().sum():,}"
)


# ============================================================
# ANOMALY TABLE
# ============================================================

show_anomalies = st.checkbox(
    "Show operational anomalies"
)

if show_anomalies:

    anomalies = filtered[
        (
            filtered["Transfer_Anomaly"]
        )
        |
        (
            filtered["Discharge_Anomaly"]
        )
    ]

    st.dataframe(
        anomalies[
            [
                "Date",
                "Children in CBP custody",
                "Children transferred out of CBP custody",
                "Children in HHS Care",
                "Children discharged from HHS Care",
                "Transfer_Anomaly",
                "Discharge_Anomaly"
            ]
        ],
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "UAC Healthcare Capacity Analytics | "
    "Operational monitoring and analytical decision support"
)