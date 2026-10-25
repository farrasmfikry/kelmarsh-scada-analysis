# Kelmarsh Scada Analysis
An end-to-end Python data analysis repository exploring SCADA telemetry from the Kelmarsh Wind Farm (6x Senvion MM92 turbines)

## 📌 Project Overview
This project demonstrates practical techniques in wind turbine performance monitoring, operational data cleaning, empirical power curve generation, and operational anomaly detection.

### Key Objectives:
* **Data Quality & Availability:** Preprocess, resample, and audit raw 10-minute SCADA logs.
* **Empirical Power Curve Analysis:** Isolate normal turbine operation from curtailment and downtime using filtering algorithms.
* **Environmental Assessment:** Map site wind resource distributions using wind roses and directional sector analysis.
* **Operational Anomalies:** Analyze SCADA telemetry during documented maintenance/fault events.

## 📊 Sample Visualizations
*(Include key high-resolution plots generated during your analysis)*

| Empirical Power Curve | Site Wind Rose | Anomaly Detection Time-Series |
| :---: | :---: | :---: |
| ![Power Curve](notebooks/plots/power_curve.png) | ![Wind Rose](notebooks/plots/wind_rose.png) | ![Time_Series](notebooks/plots/time_series.png) |

## 📜 Acknowledgments
* SCADA dataset provided open-access by Cubico Sustainable Investments. Source: https://zenodo.org/records/5841834#.YgpBQ_so-V7
* Workflows adapted from the open-source OpenWindSCADA project.

## 🚀 Getting Started
### 1. SCADA Datset cleaning
sjsjs

