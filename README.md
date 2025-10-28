# Football Injury Impact Dashboard

A professional Streamlit dashboard analyzing football injuries and their impact on players and team performance, built for the IBCP Mathematics for AI‑II coursework by Jwal Patel.

Live App: https://iadai-102-2013409-jwal-patel.streamlit.app/

---

## Contents
- [Project Overview](#project-overview)
- [Learning Outcomes](#learning-outcomes)
- [Research Questions Covered](#research-questions-covered)
- [Key Features](#key-features)
- [Dataset Information](#dataset-information)
- [Technical Stack](#technical-stack)
- [Repository Structure](#repository-structure)
- [Installation and Offline Run](#installation-and-offline-run)
- [Usage Guide](#usage-guide)
- [Deployment (Streamlit Cloud)](#deployment-streamlit-cloud)
- [Rubric Alignment (What’s Assessed)](#rubric-alignment-whats-assessed)
- [Troubleshooting](#troubleshooting)
- [References / Bibliography](#references--bibliography)
- [Author](#author)

---

## Project Overview
This dashboard enables interactive analysis of player injuries, focusing on how injuries affect individual player performance and team outcomes. It combines data preprocessing, feature engineering, and rich visualizations to answer analytical questions like top injury impact types, team win/loss change during an injured player's absence, player comeback performance, and seasonal or injury clusters.

---

## Learning Outcomes
- Perform data cleaning and feature engineering on real-world sports datasets.
- Build a user-centered interactive dashboard with filters and multi-tab views.
- Interpret injury impact on performance using statistical and visual methods.
- Deploy a Python dashboard and package it for reproducible use.

---

## Research Questions Covered
- Q1: Which injuries cause the biggest performance drop (team goal difference)?
- Q2: How do win/loss records change during a player’s absence?
- Q3: How do players perform after recovery (comeback performance)?
- Q4: Do injuries cluster by month or season (temporal patterns)?
- Q5: Which clubs are most affected by injuries?

Each question has its own visual(s) and summary in the “Overview & Insights” tab, and is further supported across other tabs.

---

## Key Features
- Multi-tab analysis: Overview & Insights, Injury Analysis, Player Performance, Team Analytics, Temporal Patterns, Advanced Statistics, Data Export.
- Rich filtering: Team, Season, Injury Severity, Position, Age Group.
- KPI indicators: Recovery duration, performance drop, win-rate changes.
- Visualizations: Bar charts, lines, pies, scatter plots, and heatmaps.
- Exports: Download filtered data as CSV, Excel (openpyxl), or JSON.
- Clean minimalist UI with high-contrast, accessible content boxes.

---

## Dataset Information
- File: `player_injuries_impact.csv`

Key fields (common examples, adjust to exact schema):
- Name, Team Name, Position, Age, FIFA rating
- Injury, Date of Injury, Date of return
- Match1/2/3_before_injury_[Player_rating|GD|Result]
- Match1/2/3_missed_match_[GD|Result]
- Match1/2/3_after_injury_[Player_rating|GD|Result]

Engineered fields:
- Injury_Duration_Days
- Avg_Rating_Before_Injury, Avg_Rating_After_Injury
- Performance_Drop_Index (before − after)
- Team_Performance_Drop (before GD − during absence GD)
- Injury_Severity (Minor/Moderate/Severe)
- Age_Group, Performance_Category
- Team_Impact_Severity

---

## Technical Stack
- Python 3.12+
- Streamlit
- Pandas, NumPy
- Plotly (graph_objects, express)
- openpyxl (Excel export)
- Caching via Streamlit cache

---

## Repository Structure
/repo-root
│
├── app.py
├── requirements.txt
├── player_injuries_impact.csv
├── README.md
└── Year-2_SA_Maths-for-AI-II_Summative_Assessment.docx (assignment file, optional)

---

## Installation and Offline Run

Clone and enter repository:
git clone <https://github.com/Jwal-Patel/IADAI-102-2013409-Jwal-Patel>
cd repo-folder


Create a virtual environment (recommended):

python -m venv .venv

Windows:
.venv\Scripts\activate

macOS/Linux:
source .venv/bin/activate


Install dependencies:

pip install --upgrade pip
pip install -r requirements.txt


Ensure dataset file is present:
- `player_injuries_impact.csv` in project root

Run the app:

streamlit run app.py


If the browser doesn't open automatically, visit:
- http://localhost:8501

---

## Usage Guide
- Use the left sidebar to filter by Team, Season, Severity, Position, Age Group.

Overview & Insights:
- Contains Q1–Q5 cards and summaries.

Injury Analysis:
- Top injury types by team performance drop; severity distribution; recovery-time vs drop scatter plot.

Player Performance:
- Most injured players; top comebacks; player deep dive with metrics and injury history.

Team Analytics:
- Injury frequency by club; performance drop; month × team heatmap.

Temporal Patterns:
- Seasonal trend lines; monthly distribution; average recovery by season.

Advanced Statistics:
- Correlation matrix; summary statistics table.

Data Export:
- Download filtered data (CSV/Excel/JSON).

---

## Deployment (Streamlit Cloud)

Prerequisites:
- `requirements.txt` includes `streamlit`, `pandas`, `numpy`, `plotly`, `openpyxl`

Steps:
1. Push code to a public GitHub repository
2. Go to share.streamlit.io
3. Connect repo and choose `app.py`
4. Deploy

The live app is here:  
https://iadai-102-2013409-jwal-patel.streamlit.app/

---

## Rubric Alignment (What’s Assessed)
- Understanding Problem: Q1–Q5 are clearly addressed within the dashboard with relevant metrics and visuals.
- Data Preprocessing: Data cleaning, feature engineering, and severity or age categories implemented.
- EDA & Insights: Statistical summaries, correlation heatmaps, and visual analyses connect injuries to outcomes.
- Dashboard Design: Tabs, filters, KPI cards, clean UI, readable content boxes, consistent color theme.
- GitHub & Deployment: Public repo with README, `requirements.txt`, dataset, and deployed Streamlit app link.

---

## Troubleshooting
“ModuleNotFoundError: openpyxl” on Streamlit Cloud:
- Ensure `openpyxl` is listed in `requirements.txt` and re-deploy.

App loads without data:
- Confirm `player_injuries_impact.csv` is in project root and readable.

Charts or text appear faint:
- Use the included CSS classes `.answer-box` and `.stat-highlight` which provide high contrast content.

Slow load:
- Confirm you are running Python 3.10+ and using Streamlit’s cache, and avoid unnecessary recomputation.

---

## References / Bibliography
- Streamlit Documentation: https://docs.streamlit.io/
- McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference.
- Plotly Python Graphing Library: https://plotly.com/python/
- Fitzpatrick, B. (2023). Interactive Dashboards and Visualizations in Python. Towards Data Science.
- Player Injuries & Team Performance Dataset: Internal project dataset.
- International Baccalaureate – IBCP Mathematics for AI‑II Coursework Guidelines.

---

## Author
- Name: Jwal Patel
- Course: IBCP Mathematics for AI‑II
- Institution: Udgam School For Children
- Email: jwalpatel.1981@gmail.com
- GitHub: [Github Profile](https://github.com/Jwal-Patel)

