# Title
Benchmark contribution proposal: reproducible BYOC endpoint load harness + March 11 results

# Body
Hi Hyperspace team — we built and ran a reproducible endpoint-level benchmark harness on Apple Silicon BYOC, and want to contribute it in the most useful way for your stack.

## Repo
https://github.com/thepenclaw/hyperspace-agent-load-benchmark

## What we implemented
- Cycle-based load runner with repeatable artifacts:
  - `experiments/2026-03-11-hyperspace-agent-load-benchmark/run.py`
  - `experiments/2026-03-11-hyperspace-agent-load-benchmark/live_protocol.sh`
  - Per-cycle JSON: `results/cycle_XX.json`
  - TSV rollups: `results.tsv`, `results_node_local.tsv`
- Metrics captured per cycle:
  - `observed_tps`, `latency_ms_avg/p95/p99`, `success_rate`
  - host CPU/memory snapshot
- Config supports:
  - multi-endpoint sweeps (`HYPERSPACE_ENDPOINTS`)
  - auth via env (`HYPERSPACE_BEARER_TOKEN` / `HYPERSPACE_API_KEY`)
  - duration mode + soak mode

## March 11, 2026 results (Mac mini M4, 16GB)
- Public endpoint baseline (`https://agents.hyper.space/`, cycles 3-13):
  - 100% success
  - best observed TPS: 410.96 at concurrency 24
  - p95 reached 401.41ms at concurrency 64
- Node-local API (`http://127.0.0.1:18080`, cycles 16-39, `/health` + `/api/v1/state`):
  - 100% success (2,120,510 / 2,120,510 requests)
  - mean TPS across sweeps: 2,314.61
  - TPS range: 2,123.10..2,350.14 (conc 2..64)
  - max latency envelope in sweeps: avg 18.80ms, p95 32.68ms, p99 41.31ms
  - throughput plateaus around ~2.33k TPS on this runner/profile

## Why we think this is useful
- Separates node/runtime behavior from public endpoint variability.
- Gives maintainers and contributors a repeatable protocol with raw data artifacts.
- Can be extended to authenticated/real agent workflows for higher-fidelity capacity testing.

## Request for maintainer guidance
1. Which authenticated endpoint(s) should be canonical for load characterization?
2. Preferred contribution target: `hyperspace-node` repo path / benchmark folder / docs location?
3. Any acceptance criteria for a benchmark PR (metrics, run duration, hardware matrix)?

If useful, we can open a PR immediately with:
- benchmark scripts + docs
- protocol defaults
- the raw March 11 artifacts and report
