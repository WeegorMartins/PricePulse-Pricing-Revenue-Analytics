# START HERE

## Step 1 — Download M5

Download the M5 Forecasting Accuracy files from Kaggle and place:

- `calendar.csv`
- `sell_prices.csv`
- `sales_train_evaluation.csv`

inside:

`data/raw/`

## Step 2 — Create environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Step 3 — Run the pipeline

```powershell
.un_all.ps1
```

If PowerShell blocks scripts, run each command manually in the order shown in `README.md`.

## Step 4 — Review outputs

Expected generated files:

- `data/processed/pricepulse.duckdb`
- `data/processed/elasticity_models.parquet`
- `data/processed/pvm_summary.parquet`
- `data/processed/scenario_grid.parquet`
- `data/processed/recommendations.parquet`
- Power BI export files in `data/powerbi/`

## Step 5 — Build Power BI

Use `docs/power_bi_spec.md` and `dashboard/MEASURES_DAX.md`.

## Important

Do not write Executive Findings until the pipeline is run and reviewed.

Do not treat simulated cost as observed.
