# Hyperspace Agent Load Benchmark (BYOC)

Benchmark framework for evaluating endpoint throughput, latency, and reliability under synthetic agent load.

## Why this repo exists

This project provides a reproducible, low-cost BYOC harness to test distributed agent systems and report optimization opportunities with real cycle data.

## What it measures

- Throughput (`observed_tps`)
- Latency (`avg`, `p95`, `p99`)
- Reliability (`success_rate`, failure examples)
- Host pressure (`cpu`, `memory`)

## Quick Start

```bash
git clone <org-repo-url>
cd <repo>
cd experiments/2026-03-11-hyperspace-agent-load-benchmark
pip3 install requests psutil
export HYPERSPACE_API_BASE="https://your-host"
export HYPERSPACE_BEARER_TOKEN="your-token"
python3 run.py
```

## Experiment Loop

- Modify one variable per cycle (`concurrency`, requests, timeout, endpoint)
- Run cycle
- Save JSON + TSV
- Summarize findings in report

## Outputs

- `results/cycle_XX.json`
- `results.tsv`
- `RESEARCH_REPORT.md`

## Contribution

See `docs/HYPERSPACE_CONTRIBUTION_PLAYBOOK.md`.

## License

MIT
