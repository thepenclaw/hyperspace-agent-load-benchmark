#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

echo "========================================"
echo "Hyperspace Live Protocol"
echo "Started: $(date)"
echo "Runner: Mac mini M4 16GB (BYOC)"
echo "========================================"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found"
  exit 1
fi

pip3 install -q requests psutil >/dev/null || true

# Shared defaults (override via environment)
export HYPERSPACE_API_BASE="${HYPERSPACE_API_BASE:-https://agents.hyper.space}"
export HYPERSPACE_ENDPOINT="${HYPERSPACE_ENDPOINT:-/}"
export HYPERSPACE_RESULTS_FILE="${HYPERSPACE_RESULTS_FILE:-results_live.tsv}"

TRIAL_REQUESTS="${TRIAL_REQUESTS:-40}"
TRIAL_CONCURRENCY="${TRIAL_CONCURRENCY:-4}"
REPEATS="${REPEATS:-3}"
SWEEP_DURATION_SECONDS="${SWEEP_DURATION_SECONDS:-60}"
SWEEP_MAX_REQUESTS="${SWEEP_MAX_REQUESTS:-120000}"
SOAK_CONCURRENCY="${SOAK_CONCURRENCY:-24}"
SOAK_DURATION_SECONDS="${SOAK_DURATION_SECONDS:-900}"
CONCURRENCY_LIST="${CONCURRENCY_LIST:-2 4 8 12 16 24 32 40 48 64}"

echo "Target base: ${HYPERSPACE_API_BASE}"
echo "Target endpoint: ${HYPERSPACE_ENDPOINT}"
echo "Results file: ${HYPERSPACE_RESULTS_FILE}"

# 1) Trial
printf "\n[1/3] Trial cycle...\n"
HYPERSPACE_MODE=count \
HYPERSPACE_TOTAL_REQUESTS="${TRIAL_REQUESTS}" \
HYPERSPACE_CONCURRENCY="${TRIAL_CONCURRENCY}" \
python3 run.py

# 2) Repeated sweeps
printf "\n[2/3] Repeated sweeps (%s repeats)...\n" "${REPEATS}"
for rep in $(seq 1 "${REPEATS}"); do
  echo "--- Repeat ${rep}/${REPEATS} ---"
  for c in ${CONCURRENCY_LIST}; do
    echo "Sweep concurrency=${c} duration=${SWEEP_DURATION_SECONDS}s"
    HYPERSPACE_MODE=duration \
    HYPERSPACE_DURATION_SECONDS="${SWEEP_DURATION_SECONDS}" \
    HYPERSPACE_MAX_REQUESTS="${SWEEP_MAX_REQUESTS}" \
    HYPERSPACE_CONCURRENCY="${c}" \
    python3 run.py
  done
done

# 3) Soak
printf "\n[3/3] Soak test...\n"
HYPERSPACE_MODE=duration \
HYPERSPACE_DURATION_SECONDS="${SOAK_DURATION_SECONDS}" \
HYPERSPACE_MAX_REQUESTS="${SWEEP_MAX_REQUESTS}" \
HYPERSPACE_CONCURRENCY="${SOAK_CONCURRENCY}" \
python3 run.py

echo "========================================"
echo "Protocol complete: $(date)"
echo "========================================"
