# 🏥 UAC Healthcare Capacity, Care Load & Flow Analysis

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Statsmodels](https://img.shields.io/badge/Statsmodels-Forecasting-4051B5)](https://www.statsmodels.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **A data-driven operational analytics framework for monitoring workload, care-system flow, intake pressure, discharge activity, reporting quality, and emerging operational stress within the U.S. Unaccompanied Alien Children (UAC) care system.**

---

## 📌 Project Snapshot

| Category | Details |
|---|---|
| **Domain** | Healthcare & Government Operations Analytics |
| **Focus** | UAC care-system workload and operational pressure |
| **Data** | Daily operational reporting |
| **Observation Period** | Jan 12, 2023 – Dec 21, 2025 |
| **Raw Records** | 1,170 |
| **Populated Observations** | 720 |
| **Primary Tools** | Python, Pandas, NumPy |
| **Visualization** | Plotly, Matplotlib, Seaborn |
| **Dashboard** | Streamlit |
| **Forecasting** | Holt-Winters Exponential Smoothing |
| **Analytical Output** | KPI framework, pressure indicators, forecasting, dashboard |

---

# 🎯 Executive Summary

The **UAC Healthcare Capacity, Care Load & Flow Analysis** project converts daily operational reporting into a structured analytics framework for understanding workload and flow across the UAC care pipeline.

Rather than looking at individual daily counts in isolation, the project combines **population stocks, operational flows, rolling pressure indicators, workload volatility, reporting quality, and forecasting** to provide a broader view of system behavior.

The analysis is designed to answer five core operational questions:

1. **How much workload is currently in the observed system?**
2. **Is workload increasing or decreasing?**
3. **Are transfers into HHS care exceeding discharges?**
4. **Is operational pressure temporary or sustained?**
5. **Is the available reporting sufficient to support the conclusion?**

The resulting Streamlit dashboard provides an interactive decision-support environment for exploring workload trends, pressure conditions, flow dynamics, and data-quality issues.

> **Core principle:**  
> **Observed workload is not the same as verified facility capacity.**

The project therefore measures **care-system workload and pressure**, while identifying the additional data required for true capacity-utilization analysis.

---

# 📖 Project Overview

The U.S. Unaccompanied Alien Children care system can be viewed as a dynamic operational pipeline:

```text
Apprehension
     │
     ▼
CBP Custody
     │
     │ Transfer
     ▼
HHS Care
     │
     ├── Medical Services
     ├── Welfare Services
     ├── Case Management
     │
     ▼
Discharge
     │
     ▼
Sponsor / Appropriate Placement
```

Each stage represents a different operational state or flow.

This project analyzes these measurements over time to understand:

- Active workload
- Intake pressure
- HHS transfer activity
- Discharge activity
- Workload accumulation
- Workload relief
- Short-term pressure
- Sustained pressure
- Historical workload variation
- Data-reporting reliability

---

# ❗ Problem Statement

Daily operational reporting provides valuable information, but individual counts do not necessarily reveal the condition of the overall system.

For example:

- A single high-transfer day may not indicate sustained pressure.
- A negative monthly average may conceal several consecutive high-pressure periods.
- A high care population does not automatically imply facility overcapacity.
- A missing reporting day cannot safely be interpreted as zero activity.
- Transfers and custody populations represent different types of measurements.

Without structured analysis, operational planning can become reactive rather than evidence-driven.

### This project addresses that gap by combining:

```text
Raw Operational Data
        ↓
Data Validation
        ↓
Data Cleaning
        ↓
Exploratory Analysis
        ↓
Flow Metrics
        ↓
Workload Metrics
        ↓
Pressure Indicators
        ↓
Forecasting
        ↓
Interactive Dashboard
        ↓
Decision Support
```

---

# 🎯 Objectives

## Primary Objectives

- Quantify total observed care-system workload.
- Compare CBP custody and HHS care populations.
- Measure transfers into HHS care.
- Measure HHS discharge activity.
- Quantify daily net intake pressure.
- Identify sustained pressure periods.
- Measure workload volatility.
- Analyze historical workload patterns.
- Monitor reporting completeness.
- Develop short-term workload forecasts.

## Secondary Objectives

- Support operational situational awareness.
- Provide a reusable government KPI framework.
- Improve workload monitoring.
- Establish an early-warning methodology.
- Identify additional data requirements for future capacity modeling.
- Provide an interactive decision-support dashboard.

---

# 📊 Dataset

## Source

```text
HHS_Unaccompanied_Alien_Children_Program.csv
```

### Dataset Profile

| Metric | Value |
|---|---:|
| Raw rows | **1,170** |
| Populated observations | **720** |
| Reporting period | **Jan 12, 2023 – Dec 21, 2025** |
| Reporting structure | Daily operational observations |

The raw dataset contains completely blank records. Data validation removes unusable records while preserving meaningful operational observations.

---

# 🧾 Data Dictionary

| Field | Description | Type |
|---|---|---|
| `Date` | Reporting date | Date |
| `Children apprehended and placed in CBP custody*` | Daily apprehension/intake volume | Flow |
| `Children in CBP custody` | Active CBP custody population | Stock |
| `Children transferred out of CBP custody` | Transfers toward HHS care | Flow |
| `Children in HHS Care` | Active HHS care population | Stock |
| `Children discharged from HHS Care` | HHS discharge activity | Flow |

---

# 🔍 Stock vs Flow Framework

A critical part of the methodology is distinguishing **stocks** from **flows**.

### Stock Measures

Stocks describe the population present at a particular point in time.

```text
CBP Custody
HHS Care
Total System Load
```

### Flow Measures

Flows describe movement during a reporting period.

```text
Apprehensions
Transfers
Discharges
```

This distinction prevents inappropriate comparisons such as treating a daily transfer count as equivalent to the number of children in custody.

---

# 🧮 Analytical KPI Framework

## 1. Total System Load

Represents the combined observed population in CBP custody and HHS care.

```text
Total System Load
=
CBP Custody
+
HHS Care
```

### Purpose

Provides a high-level indicator of active workload across the observed care pipeline.

---

## 2. Net Intake Pressure

Measures the daily balance between HHS transfers and HHS discharges.

```text
Net Intake Pressure
=
HHS Transfers
-
HHS Discharges
```

| Value | Interpretation |
|---:|---|
| **> 0** | More transfers than discharges |
| **= 0** | Approximate flow balance |
| **< 0** | More discharges than transfers |

A positive value indicates **potential short-term workload accumulation**.

---

## 3. Care Load Growth Rate

Measures the percentage change in total system load.

```text
Growth Rate
=
(Current Load - Previous Load)
/
Previous Load
× 100
```

Useful for identifying rapid workload expansion or contraction.

---

## 4. Rolling Pressure

The project uses:

- **7-day rolling pressure**
- **14-day rolling pressure**

Rolling measures help distinguish isolated daily fluctuations from persistent operational pressure.

```text
Daily Pressure
      ↓
7-Day Pressure
      ↓
14-Day Pressure
      ↓
Sustained Pressure
```

---

## 5. Cumulative Pressure

Cumulative positive net intake is used as an analytical pressure indicator.

```text
Cumulative Pressure
=
Cumulative Positive Net Intake
```

### Important

This metric **does not represent a literal placement backlog**.

It represents the accumulated analytical effect of periods in which transfers exceeded discharges.

---

## 6. Discharge Offset Ratio

Measures the extent to which discharges offset transfers.

```text
Discharge Offset Ratio
=
HHS Discharges
/
HHS Transfers
```

| Ratio | Interpretation |
|---:|---|
| **> 1** | Discharges exceed transfers |
| **≈ 1** | Approximately balanced |
| **< 1** | Transfers exceed discharges |

---

## 7. Load Volatility

Measures variation in daily workload changes.

```text
Load Volatility
=
Std. Dev.(
    Daily System Load Change
)
```

Higher volatility indicates greater instability in day-to-day workload movement.

---

## 8. Reporting Coverage

Measures the availability of expected reporting observations.

This KPI is important because operational conclusions are only as reliable as the underlying reporting coverage.

```text
Reporting Coverage
=
Observed Reporting Days
/
Expected Reporting Days
× 100
```

---

# 📈 Exploratory Data Analysis

The EDA is organized around five analytical dimensions.

### Workload

- Total system load
- CBP workload
- HHS workload
- Minimum and maximum workload
- Long-term trends

### Flow

- Transfers
- Discharges
- Net intake pressure
- Discharge offset ratio

### Time

- Daily trends
- Weekly patterns
- Monthly trends
- Year-over-year comparisons

### Pressure

- 7-day pressure
- 14-day pressure
- Sustained positive-pressure periods
- Cumulative pressure

### Data Quality

- Missing dates
- Duplicate dates
- Missing values
- Transfer anomalies
- Discharge anomalies
- Reporting coverage

---

# 📌 Key Findings

## 1. HHS Is the Dominant Workload Component

The analysis indicates that the HHS care population substantially exceeds the average CBP custody population.

### Operational implication

HHS workload should be a central component of operational monitoring, particularly when considering staffing, shelter resources, case management, and discharge operations.

---

## 2. Total System Workload Shows Significant Variation

Observed total system load ranges approximately from:

| Metric | Observed Value |
|---|---:|
| Minimum | **2,002** |
| Maximum | **11,762** |

The maximum observed workload occurs in **December 2023**.

### Operational implication

A static workload assumption may not adequately represent a system with substantial temporal variation.

---

## 3. Discharges Generally Offset Transfers

Across the observed reporting period, discharge activity generally offsets or exceeds transfer activity.

However, aggregate flow balance does not eliminate short-term operational pressure.

Positive net-intake periods still occur throughout the reporting period.

### Operational implication

Monitoring should consider both:

```text
Long-Term Flow Balance
+
Short-Term Pressure
```

---

## 4. Long-Term Averages Can Hide Short-Term Pressure

A negative average net-intake measure can coexist with periods of sustained positive pressure.

Therefore, operational monitoring should move through multiple time horizons:

```text
Daily
  ↓
7-Day
  ↓
14-Day
  ↓
Sustained Period
  ↓
Historical Comparison
  ↓
Capacity Comparison
```

---

# 🚦 Early-Warning Framework

The project introduces a **conceptual pressure-monitoring framework**.

| Level | Analytical Condition | Suggested Response |
|---|---|---|
| 🟢 **Green** | Stable or declining workload | Normal monitoring |
| 🟡 **Yellow** | Emerging positive pressure | Increase monitoring |
| 🟠 **Orange** | Sustained positive pressure | Prepare surge resources |
| 🔴 **Red** | High workload + sustained pressure | Consider contingency planning |

> ⚠️ **These categories are analytical constructs created for this project and are not official HHS operational thresholds.**

Thresholds should ultimately be calibrated using verified capacity, staffing, utilization, geographic, and operational data.

---

# 🔮 Forecasting

The project includes a short-term forecasting component based on historical system-load trends.

## Current Model

**Holt-Winters Exponential Smoothing**

The forecast is intended to support:

- Short-term workload planning
- Trend monitoring
- Potential surge identification
- Scenario planning

### Future Models

Potential extensions include:

- SARIMA
- Prophet
- XGBoost
- Random Forest
- LSTM
- Probabilistic forecasting

Forecasts should be interpreted together with reporting completeness and real operational capacity data.

---

# 🖥️ Streamlit Dashboard

The project includes an interactive Streamlit dashboard designed for operational monitoring.

## Dashboard Components

```text
┌─────────────────────────────────────────────────────┐
│             UAC OPERATIONS DASHBOARD                │
├─────────────────────────────────────────────────────┤
│ Total Load │ HHS │ CBP │ Pressure │ 7-Day │ 14-Day │
├─────────────────────────────────────────────────────┤
│                                                     │
│              SYSTEM LOAD OVERVIEW                   │
│                                                     │
├──────────────────────────┬──────────────────────────┤
│ NET INTAKE PRESSURE      │ ROLLING PRESSURE         │
├──────────────────────────┴──────────────────────────┤
│                                                     │
│             CUMULATIVE PRESSURE                     │
│                                                     │
├─────────────────────────────────────────────────────┤
│              CARE PIPELINE FLOW                     │
├─────────────────────────────────────────────────────┤
│              MONTHLY PERFORMANCE                    │
├─────────────────────────────────────────────────────┤
│             DATA QUALITY MONITOR                    │
├─────────────────────────────────────────────────────┤
│                LOAD FORECAST                        │
└─────────────────────────────────────────────────────┘
```

## Interactive Controls

Users can filter and explore:

- Date range
- Daily / weekly / monthly granularity
- Workload metrics
- Flow metrics
- Pressure indicators
- Forecasts
- Data-quality anomalies

---

# 📊 Analytical Outputs

The project generates visual outputs such as:

```text
outputs/
└── charts/
    ├── 01_total_system_load.png
    ├── 02_cbp_vs_hhs.png
    ├── 03_net_intake.png
    ├── 04_rolling_pressure.png
    ├── 05_backlog.png
    └── 06_load_forecast.png
```

---

# 🏛️ Government Decision-Support Framework

The project is designed around operational questions rather than charts alone.

### Workload

**How much active workload is currently present?**

### Direction

**Is workload increasing or decreasing?**

### Flow

**Are transfers exceeding discharges?**

### Persistence

**Is pressure temporary or sustained?**

### Concentration

**Is workload concentrated within a particular component of the system?**

### Reliability

**Is reporting sufficiently complete to support the conclusion?**

### Planning

**What additional capacity information is required to move from workload monitoring to true capacity assessment?**

---

# 🧠 From Reporting to Operational Intelligence

The analytical framework can be summarized as:

```text
Operational Reporting
        ↓
Data Validation
        ↓
Descriptive Analytics
        ↓
Workload Measurement
        ↓
Flow Analysis
        ↓
Pressure Detection
        ↓
Trend Analysis
        ↓
Forecasting
        ↓
Early-Warning Indicators
        ↓
Decision Support
```

The goal is not simply to report what happened.

The goal is to identify:

> **What is happening, whether it is persistent, and what additional information is required to support an operational response.**

---

# ⚠️ Data Quality Considerations

## Missing Reporting Dates

Missing observations are not converted into zero.

```text
Missing Observation
        ≠
Zero Activity
```

Instead, missing reporting periods are explicitly identified and incorporated into data-quality monitoring.

---

## Transfer Anomalies

Some observations may contain:

```text
Transfers > Same-Day CBP Custody
```

These observations are flagged rather than automatically removed.

Because transfers are **flows** and custody is a **stock**, this relationship can be affected by reporting-period timing.

---

## Capacity Limitation

The current dataset does not contain:

- Facility capacity
- Available beds
- Staffing levels
- Facility utilization
- Geographic capacity
- Average length of stay

Therefore, the project should be interpreted as a **workload and pressure analysis**, not a direct measurement of facility overcapacity.

---

# 🗂️ Project Architecture

```text
HHS_UAC_Healthcare_Analytics/
│
├── data/
│   ├── HHS_Unaccompanied_Alien_Children_Program.csv
│   └── uac_cleaned.csv
│
├── notebook/
│   ├── 01_Data_Validation.py
│   ├── 02_EDA.py
│   ├── 03_Capacity_Analysis.py
│   └── 04_Forecasting.py
│
├── app/
│   └── app.py
│
├── outputs/
│   └── charts/
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# ⚙️ Installation

## Clone the Repository

```bash
git clone https://github.com/yourusername/HHS_UAC_Healthcare_Analytics.git
cd HHS_UAC_Healthcare_Analytics
```

## Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Analysis

### 1. Data Validation

```bash
python notebook/01_Data_Validation.py
```

### 2. Exploratory Data Analysis

```bash
python notebook/02_EDA.py
```

### 3. Capacity & Pressure Analysis

```bash
python notebook/03_Capacity_Analysis.py
```

### 4. Forecasting

```bash
python notebook/04_Forecasting.py
```

---

# 🖥️ Run the Dashboard

```bash
streamlit run app/app.py
```

The Streamlit application will open in your browser.

---

# 📦 Requirements

```text
pandas
numpy
matplotlib
seaborn
plotly
streamlit
statsmodels
scikit-learn
openpyxl
```

---

# 🚀 Future Enhancements

## Data Expansion

- Facility-level capacity
- Available beds
- Staffing levels
- Facility utilization
- Geographic information
- Average length of stay
- Sponsor-placement duration
- Healthcare service utilization

## Advanced Analytics

- SARIMA
- Prophet
- XGBoost
- Machine-learning early-warning models
- Scenario simulation
- Facility-level capacity optimization
- Geographic pressure mapping
- Probabilistic forecasting

## Dashboard Enhancements

- Automated alerts
- Facility capacity utilization
- Geographic maps
- Forecast confidence intervals
- Scenario modeling
- Executive KPI cards
- Downloadable government reports
- Automated data-quality notifications

---

# 🔬 Research Outputs

This project can be extended into several professional deliverables:

- 📊 Exploratory Data Analysis
- 📈 Workload & capacity-pressure analysis
- 🔄 Flow and pressure analysis
- 🔮 Time-series forecasting
- 🖥️ Interactive Streamlit dashboard
- 🏛️ Government stakeholder executive summary
- 📄 Research paper
- 📌 KPI framework
- ⚠️ Data-quality assessment
- 🚦 Early-warning framework

---

# 📄 Research Paper Structure

A corresponding research paper can follow:

1. **Abstract**
2. **Introduction**
3. **Literature Review**
4. **Dataset Description**
5. **Data Validation & Methodology**
6. **Exploratory Data Analysis**
7. **Workload Analysis**
8. **Flow Analysis**
9. **Pressure Analysis**
10. **Forecasting**
11. **Discussion**
12. **Operational & Government Implications**
13. **Limitations**
14. **Future Work**
15. **Conclusion**

---

# ⚠️ Important Analytical Disclaimer

This repository is an **analytical and decision-support project**.

It does not independently establish:

- Facility overcapacity
- Healthcare quality
- Individual child outcomes
- Causal relationships
- Official government thresholds
- Policy effectiveness

Actual capacity assessment requires verified operational information such as:

- Facility capacity
- Available beds
- Staffing
- Utilization
- Geographic distribution
- Operational constraints

Similarly, the early-warning levels presented in this repository are **analytical categories**, not official government standards.

---

# 📚 References

- U.S. Department of Health & Human Services
- Administration for Children and Families
- Office of Refugee Resettlement
- Unaccompanied Children Program
- U.S. Department of Homeland Security
- U.S. Customs and Border Protection
- UAC operational dataset used in this project

---

# 👤 Author

## Kaushik Prasad

**Data Analytics | Python | Power BI | Streamlit | Healthcare Analytics**

---

# ⭐ Project Objective

> **Build a transparent, data-driven early-warning framework that transforms UAC operational reporting into actionable intelligence for workload monitoring, pressure detection, forecasting, and proactive care-system planning.**

---

## 🔑 Final Takeaway

The central analytical distinction of this project is:

```text
                    WORKLOAD
                       │
          ┌────────────┴────────────┐
          │                         │
       Measured                 Not directly
       from data                measured
          │                         │
          ▼                         ▼
   Population Stocks          Actual Capacity
   Operational Flows          Available Beds
   Pressure Indicators        Staffing
   Trends                     Utilization
   Volatility                 Facility Constraints
          │                         │
          └────────────┬────────────┘
                       ▼
              OPERATIONAL INTELLIGENCE
```

The current project establishes the **workload, flow, pressure, reporting-quality, and forecasting layers**.

The next analytical stage is to integrate verified facility and workforce capacity data to transform workload pressure into **true capacity-utilization and resource-planning analytics**.