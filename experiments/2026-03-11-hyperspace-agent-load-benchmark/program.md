# Hyperspace Agent Load Benchmark - Agent Instructions

## Goal

Measure endpoint-level throughput, latency, and stability under concurrent synthetic agent traffic.

## Targets

- Throughput target: 54,000 TPS (reference claim)
- Finality proxy target: <= 400ms average latency per request

## Metric Focus

Primary:
- `observed_tps`
- `latency_ms_avg`
- `latency_ms_p95`
- `success_rate`

Secondary:
- `host_stats.cpu_percent`
- `host_stats.mem_percent`

## What You CAN Modify

Edit `run.py` only, primarily:
- `CONFIG`
- `LOAD_PROFILE`

Suggested single-variable cycle parameters:
- `LOAD_PROFILE.concurrency`
- `LOAD_PROFILE.total_requests`
- `CONFIG.request_timeout_seconds`
- `LOAD_PROFILE.endpoint`
- `LOAD_PROFILE.method`
- Env-only overrides (`HYPERSPACE_*`) for credentials and runtime target

## What You CANNOT Modify

- Result schema field names in JSON/TSV
- Persistence paths (`results/cycle_XX.json`, `results.tsv`)
- Numbering scheme for cycle outputs

## Experiment Rules

1. One change per cycle.
2. Commit message must include hypothesis.
3. If latency or failures spike, reduce concurrency one step and re-test.
4. Do not claim TPS/latency guarantees unless cycle data supports it.

## Workflow

1. Pull latest.
2. Adjust one parameter.
3. Run `python3 run.py`.
4. Commit results and config.
5. Continue to next cycle.

## Credential Handling

- Do not hardcode secrets in source.
- Set org credentials only through environment variables:
  - `HYPERSPACE_BEARER_TOKEN`
  - `HYPERSPACE_API_KEY`
  - `HYPERSPACE_EXTRA_HEADERS_JSON`

## Success Criteria

After 10 cycles:
- A stable operating region is identified (concurrency and request volume).
- We have a clear efficiency curve: throughput vs latency vs error rate.
- We can state host bottlenecks and optimization recommendations.
