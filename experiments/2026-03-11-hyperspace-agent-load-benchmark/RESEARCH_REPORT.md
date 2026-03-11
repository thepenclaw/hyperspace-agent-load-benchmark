# Hyperspace Agent Load Benchmark - Research Report

## Metadata

- Date: 2026-03-11
- Runner: Mac mini M4, 16 GB RAM
- Repo: https://github.com/thepenclaw/hyperspace-agent-load-benchmark
- Experiment path: `experiments/2026-03-11-hyperspace-agent-load-benchmark`
- Runtime profile:
  - Public web endpoint sweep: `https://agents.hyper.space/`
  - Node-local API sweep: `http://127.0.0.1:18080` (live Hyperspace node with provided key/peer)

## Objective

Run real, cycle-based load benchmarks to measure throughput, latency, and reliability on local Apple Silicon BYOC infrastructure, then assess what this says about practical load-testing value for Hyperspace workflows.

## Protocol

- Method: GET
- Warmup requests: 5
- Timeout: 10s
- Target thresholds:
  - Finality proxy: <= 400 ms average latency
  - Throughput claim check: >= 54,000 TPS (contextual reference target)

### Execution plan

1. One trial cycle with moderate load.
2. Ten live cycles with a concurrency sweep.

## Phase A - Public Endpoint Baseline (`https://agents.hyper.space/`)

### Trial Cycle

| Cycle | Concurrency | Requests | Success | TPS | Avg Latency (ms) | P95 (ms) |
|---|---:|---:|---:|---:|---:|---:|
| 3 | 4 | 30 | 100% | 145.63 | 26.36 | 72.85 |

### Live 10-Cycle Sweep

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

### Findings (Phase A)

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

## Phase B - Node-Local API Bench (`http://127.0.0.1:18080`)

### Trial + 10-cycle x2 sweep + soak

- Trial cycles:
  - Cycle 16 (`/health`, count mode, conc 8): 2,197.80 TPS, avg 2.95 ms, p95 4.41 ms.
  - Cycle 17 (`/api/v1/state`, count mode, conc 8): 2,033.90 TPS, avg 3.03 ms, p95 5.89 ms.
- Main protocol:
  - Trial pair (cycle 18) at concurrency 4.
  - Repeated duration sweeps (cycles 19-38): concurrency 2,4,8,12,16,24,32,40,48,64; repeated twice.
  - Soak pair (cycle 39) at concurrency 24.

### Aggregated findings (Phase B)

- Reliability: 100% success on all node-local cycles (24/24 cycles, 2,120,510/2,120,510 requests).
- Throughput stability:
  - Mean TPS across duration sweeps (cycles 19-38): 2,314.61.
  - Range: 2,123.10 to 2,350.14 TPS.
- Latency envelope across duration sweeps:
  - Avg latency max: 18.80 ms.
  - P95 max: 32.68 ms.
  - P99 max: 41.31 ms.
- Concurrency behavior:
  - Throughput plateaus around ~2.33k TPS from concurrency 8 through 64.
  - Latency scales near-linearly with concurrency while staying well below the 400 ms proxy.
- Soak caveat:
  - Soak run was configured for 180s but hit `max_requests=120000` per endpoint first (~51s each endpoint), so this is a capped high-volume run, not a full-time soak.

### Why this adds value

- Separates transport/runtime ceiling from public endpoint noise by measuring node-local APIs directly.
- Produces repeatable cycle artifacts (`results/cycle_*.json`) that can be compared run-to-run.
- Creates a practical baseline before introducing authenticated workload endpoints and real agent workflows.

## Recommended Operating Region (This Setup)

- Suggested default concurrency: 16-24
- Rationale:
  - Near-plateau throughput on node-local API.
  - Lower tail latency versus high concurrency stress edges.
  - Headroom for adding heavier authenticated endpoints.

## Next Experiments

1. Run authenticated endpoint sweeps using `hyperspace token --json` and protected API routes.
2. Raise/disable `max_requests` during soak to force true time-based long-duration tests (15-60 min).
3. Add weighted endpoint mix (light + heavy paths) to model real agent workflows.
4. Capture per-endpoint CPU/memory/disk and compute saturation points.
5. Convert this into a contribution PR with reproducible scripts + raw artifacts + interpretation notes.

## Artifacts

- `results.tsv`
- `results_node_local.tsv`
- `results/cycle_03.json` (trial)
- `results/cycle_04.json` to `results/cycle_13.json` (live 10 cycles)
- `results/cycle_16.json` to `results/cycle_39.json` (node-local protocol)
