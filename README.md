
# E-commerce Revenue Dashboard

A simple Streamlit app that connects to a DuckDB database created by the e-commerce data pipeline. It provides an interactive dashboard with daily revenue metrics, filters, and charts.

## Features
- Connects to a local DuckDB database
- Displays daily revenue metrics in a table and line chart
- Interactive filters for date range
- Easy one-command local run

## Prerequisites
This app expects a DuckDB database with a `mart_revenue_daily` table. By default, it looks for the file at `../ecommerce_data_pipeline_v1/warehouse/ecom.duckdb`. You can change the path in `config.py` or set it with an environment variable.

## Quick Start
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open the URL printed in your terminal (usually `http://localhost:8501`).

## Configuration
- Default database path: `../ecommerce_data_pipeline_v1/warehouse/ecom.duckdb`
- Override with:
  ```bash
  export DUCKDB_PATH=/absolute/path/to/ecom.duckdb
  ```

## Notes
The code is fully commented and written for clarity.
