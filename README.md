# PricePulse | Pricing & Revenue Optimization

**Elasticidade, arquitetura de preços, cenários e impacto em receita e margem**

PricePulse é um case de Pricing & Revenue Analytics construído como um sistema de apoio à decisão, e não como um exercício de dashboard ou um "otimizador automático de preços".

## Business Problem

Uma empresa varejista com milhares de SKUs e múltiplas lojas precisa identificar onde alterações de preço podem ser economicamente interessantes sem destruir volume, respeitando incerteza estatística e limites de extrapolação.

O projeto procura responder:

1. Em quais produtos existe evidência suficiente para testar aumento de preço?
2. Onde uma redução pode potencialmente gerar volume incremental?
3. Quais SKUs apresentam maior sensibilidade?
4. Quanto da mudança de receita é explicada por preço, volume, mix e sortimento?
5. Quais cenários apresentam melhor relação entre impacto esperado e risco?
6. Onde não existe evidência suficiente para agir?
7. Quais hipóteses deveriam ser priorizadas para experimentação?

## Data Source

Dataset principal: **M5 Forecasting Accuracy (Walmart)**.

Arquivos esperados em `data/raw/`:

- `calendar.csv`
- `sell_prices.csv`
- `sales_train_evaluation.csv`

Os dados não são distribuídos neste repositório. Faça o download pela competição M5 no Kaggle e coloque os arquivos acima em `data/raw/`.

## Evidence Labels

Ao longo do projeto, cada número relevante deve ser interpretado como:

- **Observed**: existe diretamente no dataset.
- **Calculated**: derivado deterministicamente.
- **Estimated**: produzido por um modelo estatístico.
- **Simulated**: hipótese criada para demonstrar uma mecânica.
- **Hypothesis**: proposta para decisão/experimento.

## Methodology

Business Problem  
→ Data Quality  
→ Pricing Diagnostics  
→ Eligibility  
→ Elasticity Modeling  
→ Robustness Checks  
→ Price-Volume-Mix  
→ Scenario Simulation  
→ Recommendation Engine  
→ Experiment Design  
→ Power BI  
→ Executive Storytelling

## Core Modeling Principle

Elasticidade histórica **não é causalidade**.

O projeto usa histórico para priorizar hipóteses e estimar cenários, mas mudanças de preço deveriam ser validadas por experimentação controlada sempre que possível.

## Project Structure

```text
PricePulse/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── config/
├── data/
├── sql/
├── notebooks/
├── src/
├── tests/
├── dashboard/
├── docs/
├── outputs/
└── images/
```

## Quick Start

### 1. Create environment

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Put M5 raw files in `data/raw/`

Expected:

```text
data/raw/calendar.csv
data/raw/sell_prices.csv
data/raw/sales_train_evaluation.csv
```

### 3. Build the analytical layer

```powershell
python src/build_data.py
```

### 4. Run tests

```powershell
pytest -v
```

### 5. Build eligibility table

```powershell
python src/run_sql.py sql/03_eligibility.sql
```

### 6. Run elasticity models

```powershell
python src/run_elasticity_pipeline.py
```

### 7. Build PVM, scenarios and recommendations

```powershell
python src/run_pvm.py
python src/run_scenarios.py
python src/run_recommendations.py
```

### 8. Export Power BI layer

```powershell
python src/export_powerbi.py
```

## Expected Structural Checks

For the complete M5 evaluation dataset:

- 3,049 products
- 10 stores
- 30,490 SKU-store series
- 1,941 days
- approximately 59.18 million SKU-store-day observations

These are structural expectations. Do not invent business findings before running the project.

## Executive Findings

**Intentionally blank until the models are run.**

Do not replace this section with fabricated results.

## Limitations & Guardrails

See `docs/limitations.md`.

Key limitations:

- historical elasticity is not automatically causal;
- price may be endogenous;
- stockouts are not directly observed;
- SKU promotion is not fully observed;
- cost is simulated;
- competitor price is not used because it is not observed;
- scenarios are local estimates;
- extrapolation is constrained;
- model uncertainty must be displayed;
- recommendations are hypotheses for testing.

## Power BI

Recommended pages:

1. Executive Overview
2. Price Architecture
3. Elasticity
4. Revenue Drivers / PVM
5. Scenario Simulator
6. Recommendation Center

See `docs/power_bi_spec.md`.

## Tech Stack

- Python
- DuckDB
- Parquet
- pandas
- statsmodels
- linearmodels
- scipy
- scikit-learn
- matplotlib
- seaborn
- Plotly
- pytest
- Power BI
- Git/GitHub

The project deliberately avoids Spark, Kafka, Airflow, cloud infrastructure and deep learning because they do not add material value to this problem at this scale.
