#!/bin/bash
# Hyperspace Agent Load Benchmark - 10 Cycles

cd "$(dirname "$0")"

echo "========================================"
echo "Hyperspace Agent Load Benchmark"
echo "Started: $(date)"
echo "Directory: $(pwd)"
echo "========================================"

if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 not found"
    exit 1
fi

echo "Checking dependencies..."
pip3 install -q requests psutil 2>/dev/null || echo "Note: pip install may require user action"

for i in {1..10}; do
    echo ""
    echo "========================================"
    echo "CYCLE $i/10"
    echo "Time: $(date)"
    echo "========================================"

    echo "Pulling latest code..."
    git pull origin main

    echo "Running run.py..."
    python3 run.py

    echo "Pushing results..."
    git add results/ results.tsv run.py
    git commit -m "Hyperspace cycle-$i: $(date +%Y%m%d-%H%M%S)"
    git push origin main

    if [ $i -lt 10 ]; then
        echo "Sleeping 15 minutes..."
        sleep 900
    fi
done

echo "========================================"
echo "All cycles complete: $(date)"
echo "========================================"
