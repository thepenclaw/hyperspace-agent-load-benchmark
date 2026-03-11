# Architecture

## Overview

This repository runs repeatable endpoint-level load tests for Hyperspace workflows.

Core idea:
- Configure target endpoint(s)
- Execute count or duration load cycles
- Persist per-cycle JSON + TSV rollups
- Compare runs over time

## Components

| Component | Role |
|-----------|------|
| `run.py` | Benchmark engine (requests, concurrency, metrics, export) |
| `live_protocol.sh` | Standardized trial + sweep + soak sequence |
| `auto_run.sh` | Repeated cycle automation |
| `results/cycle_*.json` | Raw cycle artifacts |
| `results.tsv` / `results_node_local.tsv` | Condensed metrics table |

## Benchmark Flow

1. Preflight request checks endpoint reachability.
2. Warmup executes a small request sample.
3. Load runner executes either:
   - `count` mode (`total_requests`)
   - `duration` mode (`duration_seconds`, optional `max_requests`)
4. Metrics are computed:
   - `observed_tps`
   - `latency_ms_avg`, `p50`, `p95`, `p99`
   - `success_rate`
   - host CPU/memory snapshot
5. Artifacts are written for each cycle and appended to TSV.

## Config Surface

Primary env controls:
- `HYPERSPACE_API_BASE`
- `HYPERSPACE_ENDPOINT` or `HYPERSPACE_ENDPOINTS`
- `HYPERSPACE_METHOD`
- `HYPERSPACE_CONCURRENCY`
- `HYPERSPACE_TOTAL_REQUESTS`
- `HYPERSPACE_MODE` (`count` / `duration`)
- `HYPERSPACE_DURATION_SECONDS`
- `HYPERSPACE_MAX_REQUESTS`
- `HYPERSPACE_BEARER_TOKEN` or `HYPERSPACE_API_KEY`

## Operating Modes

- Public endpoint profiling (hosted service latency envelope)
- Node-local profiling (`127.0.0.1:18080`) to isolate local runtime behavior
- Authenticated endpoint profiling when canonical protected routes are available
