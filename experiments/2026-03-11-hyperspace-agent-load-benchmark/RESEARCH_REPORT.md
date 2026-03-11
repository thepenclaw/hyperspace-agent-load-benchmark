# Hyperspace Agent Load Benchmark - Research Report

## Metadata

- Date: 2026-03-11
- Runner: Mac mini M4, 16 GB RAM
- Repo: https://github.com/thepenclaw/hyperspace-agent-load-benchmark
- Experiment path: `experiments/2026-03-11-hyperspace-agent-load-benchmark`

## Objective

Run a real, cycle-based load benchmark against `https://agents.hyper.space/` to measure throughput, latency, and reliability on local Apple Silicon BYOC infrastructure.

## Protocol

- Endpoint: `/`
- Method: GET
- Warmup requests: 5
- Timeout: 10s
- Target thresholds:
  - Finality proxy: <= 400 ms average latency
  - Throughput claim check: >= 54,000 TPS

### Execution plan

1. One trial cycle with moderate load.
2. Ten live cycles with a concurrency sweep.

## Trial Cycle

| Cycle | Concurrency | Requests | Success | TPS | Avg Latency (ms) | P95 (ms) |
|---|---:|---:|---:|---:|---:|---:|
| 3 | 4 | 30 | 100% | 145.63 | 26.36 | 72.85 |

## Live 10-Cycle Sweep

| Cycle | Concurrency | Requests | Success | TPS | Avg Latency (ms) | P95 (ms) |
|---|---:|---:|---:|---:|---:|---:|
| 4 | 2 | 120 | 100% | 74.72 | 26.55 | 40.23 |
| 5 | 4 | 120 | 100% | 142.69 | 27.74 | 48.04 |
| 6 | 8 | 120 | 100% | 266.67 | 29.18 | 79.20 |
| 7 | 12 | 120 | 100% | 328.77 | 33.79 | 138.64 |
| 8 | 16 | 120 | 100% | 335.20 | 46.11 | 114.42 |
| 9 | 24 | 120 | 100% | 410.96 | 53.19 | 129.63 |
| 10 | 32 | 120 | 100% | 270.27 | 96.00 | 176.56 |
| 11 | 40 | 120 | 100% | 297.03 | 111.92 | 211.57 |
| 12 | 48 | 120 | 100% | 210.16 | 161.11 | 262.35 |
| 13 | 64 | 120 | 100% | 220.99 | 214.37 | 401.41 |

## Key Findings

- Reliability: 100% success on all live cycles (10/10 cycles, 1,200/1,200 requests).
- Best throughput in this run: 410.96 TPS at concurrency 24.
- Latency behavior:
  - Concurrency 2-24 stayed low and stable (<60 ms avg).
  - Beyond concurrency 24, latency rose sharply and TPS became non-linear.
- Finality proxy check:
  - Average latency remained below 400 ms in all live cycles.
  - P95 breached 400 ms at concurrency 64 (401.41 ms), indicating the upper edge of this runner+endpoint operating zone.
- Throughput claim check:
  - Observed endpoint-level TPS in this harness is far below 54k TPS.
  - This is not a chain-level TPS benchmark; it is an HTTP endpoint load profile from one BYOC runner.

## Recommended Operating Region (This Setup)

- Suggested default concurrency: 16-24
- Rationale:
  - Peak/near-peak throughput
  - Lower latency volatility
  - Better P95 stability vs. high-concurrency tails

## Next Experiments

1. Repeat the same sweep on authenticated API endpoints (not just `/`) using `HYPERSPACE_BEARER_TOKEN` or `HYPERSPACE_API_KEY`.
2. Add multi-endpoint mode (`HYPERSPACE_ENDPOINTS`) with weighted request mix.
3. Run 3 independent repetitions of the 10-cycle sweep to build confidence intervals.
4. Add per-cycle CPU/memory trend charting and correlate with throughput knees.

## Artifacts

- `results.tsv`
- `results/cycle_03.json` (trial)
- `results/cycle_04.json` to `results/cycle_13.json` (live 10 cycles)
