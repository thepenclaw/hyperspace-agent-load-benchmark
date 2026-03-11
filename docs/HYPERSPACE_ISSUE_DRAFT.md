# Draft Issue: Hyperspace Benchmark Collaboration

## Title
Benchmark: endpoint load profile on Apple Silicon (TPS/latency/error curve)

## Body
### Objective
We built a reproducible BYOC benchmark harness to evaluate endpoint throughput, latency, and reliability under synthetic agent traffic.

### What we implemented
- Cycle-based load harness (`run.py`) with persisted artifacts:
  - `results/cycle_XX.json`
  - `results.tsv` or `results_live.tsv`
- Metrics:
  - `observed_tps`
  - `latency_ms_avg/p95/p99`
  - `success_rate`
  - host CPU/memory snapshot
- Env-based secure config:
  - `HYPERSPACE_API_BASE`
  - `HYPERSPACE_BEARER_TOKEN` / `HYPERSPACE_API_KEY`
  - endpoint/method/concurrency/request controls

### Repository
https://github.com/thepenclaw/hyperspace-agent-load-benchmark

### Current status
- Harness and protocol runner (`live_protocol.sh`) are implemented.
- Initial real cycles on M4 completed.
- Next run is prepared for authenticated endpoint validation.

### Ask from maintainers
1. Which endpoint(s) should be canonical for baseline load characterization?
2. Preferred interpretation for endpoint-level latency as finality proxy?
3. Would maintainers review a docs/instrumentation PR with our cycle artifacts?

### Why this may help
- External reproducible load signal
- BYOC workflow other contributors can run cheaply
- Structured evidence for throughput/latency/reliability tradeoffs
