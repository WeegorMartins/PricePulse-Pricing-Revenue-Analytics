#!/usr/bin/env bash

set -e

echo "======================================"
echo " PricePulse | Pricing & Revenue"
echo "======================================"

echo ""
echo "1/8 Building analytical data layer..."
python -m src.build_data

echo ""
echo "2/8 Running structural tests..."
pytest -v

echo ""
echo "3/8 Creating pricing diagnostics..."
python -m src.run_sql sql/02_pricing_diagnostics.sql

echo ""
echo "4/8 Creating elasticity eligibility..."
python -m src.run_sql sql/03_eligibility.sql

echo ""
echo "5/8 Estimating elasticity..."
python -m src.run_elasticity_pipeline

echo ""
echo "6/8 Running Price-Volume-Mix..."
python -m src.run_pvm

echo ""
echo "7/8 Creating scenarios and recommendations..."
python -m src.run_scenarios
python -m src.run_recommendations

echo ""
echo "8/8 Exporting analytical layer..."
python -m src.export_powerbi

echo ""
echo "======================================"
echo " PricePulse pipeline completed"
echo "======================================"