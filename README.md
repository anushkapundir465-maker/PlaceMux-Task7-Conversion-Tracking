# PlaceMux Phase 2 – Pay-per-Application Flow

## Project overview

PlaceMux Phase 2 delivers a polished conversion tracking dashboard for a Data Analyst Marketplace. The app uses Python, Streamlit, Pandas, and Plotly to present conversion KPIs, application workflows, funnel visuals, analytics, and tracking metrics from CSV source data.

## Features

- Conversion Dashboard with professional KPI cards
- Application Flow visualization from Visitor to Hired
- Plotly Conversion Funnel for full user journey
- Interactive analytics charts for daily trends, company and job performance
- Tracking Plan summary of business conversion metrics
- Filters by company, job, date, and search term
- Download filtered CSV data
- Automatic CSV generation for missing data files

## Folder structure

```
TASK7/
  app.py
  requirements.txt
  README.md
  data/
    companies.csv
    jobs.csv
    candidates.csv
    applications.csv
    conversions.csv
    events.csv
  pages_logic/
    analytics.py
    application_flow.py
    conversion_dashboard.py
    conversion_funnel.py
    tracking_plan.py
    __init__.py
  utils/
    data_manager.py
    __init__.py
  screenshots/
```

## Tech stack

- Python
- Streamlit
- Pandas
- Plotly

## Installation

1. Create a Python environment:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\\Scripts\\activate   # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m streamlit run app.py
```

## Screenshots

The `screenshots/` folder contains example dashboard views for:
- Conversion Dashboard
- Conversion Funnel
- Analytics insights

## Edge cases handled

- Missing CSV files are automatically generated with sample data
- Empty CSV files are detected and replaced with realistic sample data
- Duplicate application rows are removed and a warning is shown
- Invalid IDs and missing references are handled through safe merges
- Invalid dates are coerced to `NaT` and filtered safely
- Null values do not crash UI calculations
- Zero conversions and zero-division cases return clean metrics
- Filter selections with no matches display informative warnings

## Demo

Launch the app and use the sidebar to:
- switch between Conversion Dashboard, Application Flow, Conversion Funnel, Analytics, and Tracking Plan
- filter by Company, Job, Date range, and Search
- view KPI cards, charts, and event/application tables
- export filtered application records as CSV
