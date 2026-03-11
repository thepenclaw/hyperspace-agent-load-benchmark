# Hyperspace Agent Load Benchmark - Research Report

## Metadata

- Date:
- Researchers:
- Repo:
- Commit SHA:
- Target Environment (host, region, hardware):

## Objective

State exactly what you tested and why.

## Hypothesis

Define expected behavior under load.

## Test Protocol

- Endpoint(s):
- Method(s):
- Auth mode: Bearer/API key/custom headers
- Requests per cycle:
- Concurrency schedule by cycle:
- Timeout:
- Warmup:

## Metrics

Primary:
- observed_tps
- latency_ms_avg
- latency_ms_p95
- success_rate

Secondary:
- cpu_percent
- mem_percent
- error classes

## Results Table

| Cycle | Endpoint | Concurrency | Requests | Success Rate | TPS | Avg ms | P95 ms | 400ms met | 54k TPS met |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 |  |  |  |  |  |  |  |  |  |

## Failure Analysis

- Top failure modes:
- Error examples:
- Conditions where failure rate increased:

## Efficiency Curve

Describe the operating region where throughput scales without unacceptable latency/error growth.

## Recommendations

- Optimal default config:
- Safe max concurrency:
- Required guardrails:
- Next experiment:

## Reproducibility

```bash
cd experiments/2026-03-11-hyperspace-agent-load-benchmark
export HYPERSPACE_API_BASE="..."
export HYPERSPACE_BEARER_TOKEN="..."
python3 run.py
```

## Appendix

- `results.tsv`
- `results/cycle_*.json`
- Any notebooks/charts
