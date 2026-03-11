# Hyperspace Agent Load Benchmark (BYOC)

Cycle-based endpoint benchmark adapted from the Playwright autoresearch pattern.

## Purpose

Evaluate distributed-system efficiency for Hyperspace-style agent endpoints by measuring:
- Throughput (`observed_tps`)
- Latency (`avg`, `p95`, `p99`)
- Reliability (`success_rate`, failure samples)
- Host pressure (CPU/memory)

## Files

- `run.py`: load test harness and metrics export
- `auto_run.sh`: 10-cycle automation loop
- `program.md`: agent mutation constraints
- `results/`: per-cycle JSON logs
- `results.tsv`: condensed cycle metrics

## Quick Start

```bash
cd experiments/2026-03-11-hyperspace-agent-load-benchmark
pip3 install requests psutil
python3 run.py
```

For automated cycles:

```bash
./auto_run.sh
```

## Configuration

In `run.py`, update:
- `CONFIG["api_base"]` to your target host
- `LOAD_PROFILE["endpoint"]` for the specific API path
- `LOAD_PROFILE["concurrency"]` and `total_requests` for stress level

### Env-based runtime config (recommended)

Use env vars to avoid hardcoding org credentials:

```bash
export HYPERSPACE_API_BASE="https://your-api-host"
export HYPERSPACE_BEARER_TOKEN="your_token"
export HYPERSPACE_ENDPOINT="/health"
export HYPERSPACE_CONCURRENCY=16
export HYPERSPACE_TOTAL_REQUESTS=500
python3 run.py
```

Supported env vars:
- `HYPERSPACE_API_BASE`
- `HYPERSPACE_BEARER_TOKEN`
- `HYPERSPACE_API_KEY`
- `HYPERSPACE_EXTRA_HEADERS_JSON`
- `HYPERSPACE_METHOD`
- `HYPERSPACE_ENDPOINT`
- `HYPERSPACE_ENDPOINTS` (comma-separated list)
- `HYPERSPACE_PAYLOAD_JSON`
- `HYPERSPACE_CONCURRENCY`
- `HYPERSPACE_TOTAL_REQUESTS`
- `HYPERSPACE_TIMEOUT_SECONDS`
- `HYPERSPACE_TARGET_FINALITY_MS`
- `HYPERSPACE_TARGET_TPS`

## Output Schema (per cycle)

- `requests_total`, `requests_success`, `requests_failed`
- `observed_tps`
- `latency_ms_avg`, `latency_ms_p50`, `latency_ms_p95`, `latency_ms_p99`
- `target_finality_met` (<= 400ms)
- `target_tps_met` (>= 54000 TPS)
- `host_stats` (cpu/memory)

## Notes

- This harness currently uses HTTP latency as a practical finality proxy.
- For authenticated/private endpoints, inject credentials via headers or env vars in `CONFIG`.
- Add endpoint-specific payload schemas before POST benchmarks.
