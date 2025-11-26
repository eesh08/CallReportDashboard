Tech Stack: Python, SQL, Excel 

This project delivers a fully interactive Sales Force Effectiveness (SFE) dashboard built on top of a clean data pipeline.
The data was cleaned and transformed using Python + SQL, loaded into Excel as a structured table, and consumed by multiple pivot tables feeding the final dashboard.

🚀 Project Overview

The dashboard analyzes field performance across:
Coverage & Doctor Reach
Call Productivity (Call Avg / Avg Visits)
Field Working Days
Compliance%
Digital Adoption (E-Detailing%)
RTE Quality Metrics
Usage Distribution

The purpose is to help managers quickly identify performance gaps, productivity patterns, and digital adoption issues across months and units.

🧹 Data Cleaning & Processing
Python (Pandas) – Key Steps

Imported raw Excel/CSV logs
Standardized column formats (dates, numeric types, missing values)
String normalization for BU / HQ / Rep names
Created derived metrics (Call Avg, E-Detailing %, Compliance %)
Exported clean dataset for SQL ingestion

SQL – Data Transformation

Created a clean relational table (sfe_data)

Removed duplicates
Handled null visits / outlier calls
Applied monthly aggregation queries
Prepared metrics for Excel consumption

Example SQL operations used:

GROUP BY month & rep
Window functions for averages
CASE WHEN for E-Detailing slabs
Normalization of call metrics

Final output was exported as an Excel Table (SFE_Data) for pivot consumption.

📊 Excel Dashboard Features
Structure

SFE_Data → Clean dataset from Python/SQL

Pivots_Base → All pivot tables (backend)

Dashboard_FY2025 → Final UI layer

Interactive Components

KPI Cards

Coverage Trend
Call Avg Trend
Visit Volume Trend
RTE Line Chart
E-Detailing Slabs Pie/Donut
Distribution Segments
Slicers for Month, BU, HQ, Rep
Dashboard Design Focus
Clean layout with white theme
Uniform chart formatting
Transparent chart backgrounds
Proper alignment & spacing

