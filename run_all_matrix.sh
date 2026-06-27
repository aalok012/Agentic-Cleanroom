#!/usr/bin/env bash
# Overnight driver — runs the FULL Python matrix, then the FULL Java matrix, back to back,
# in a single hands-off process. Each language phase is run_matrix.sh (models parallel per SRS).
#
# Outputs are fully separated per cell — nothing overwrites anything:
#   outputs/python/<srs_stem>/<model_safe>/   (24 cells)
#   outputs/java/<srs_stem>/<model_safe>/     (24 cells)
# Both phases accumulate into the SAME unified CSV (a `language` column tells them apart):
#   experiment_metrics.csv
#
# Launch and go to sleep (stays awake, survives terminal close):
#   caffeinate -i nohup ./run_all_matrix.sh > outputs/all_matrix.log 2>&1 &
#
# Watch in the morning:
#   tail -n 60 outputs/all_matrix.log
#   column -s, -t experiment_metrics.csv | less -S
set -u
cd "$(dirname "$0")"

echo "############ FULL MATRIX (python + java) START: $(date) ############"

echo "############ PHASE 1/2: PYTHON / FastAPI ############"
./run_matrix.sh python fastapi

echo "############ PHASE 2/2: JAVA / Spring Boot ############"
./run_matrix.sh java spring

echo "############ FULL MATRIX DONE: $(date) ############"
echo "Unified metrics: experiment_metrics.csv"