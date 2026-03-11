# Hyperspace Agent Load Benchmark

Reproducible load benchmark harness for Hyperspace-style agent endpoints.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: macOS](https://img.shields.io/badge/Platform-macOS-blue.svg)](https://www.apple.com/macos/)

## Scope

This repository is dedicated to Hyperspace load characterization:
- Endpoint throughput (`observed_tps`)
- Latency (`avg`, `p95`, `p99`)
- Reliability (`success_rate`, failures)
- Host pressure snapshots (CPU/memory)

## Quick Start

```bash
git clone https://github.com/thepenclaw/hyperspace-agent-load-benchmark.git
cd hyperspace-agent-load-benchmark/experiments/2026-03-11-hyperspace-agent-load-benchmark
pip3 install requests psutil
python3 run.py
```

Run full protocol (trial + sweeps + soak):

```bash
./live_protocol.sh
```

## Repository Structure

```
hyperspace-agent-load-benchmark/
├── README.md
├── LICENSE
├── ARCHITECTURE.md
├── docs/
└── experiments/
    └── 2026-03-11-hyperspace-agent-load-benchmark/
        ├── run.py
        ├── auto_run.sh
        ├── live_protocol.sh
        ├── RESEARCH_REPORT.md
        ├── results.tsv
        ├── results_node_local.tsv
        └── results/
```

## Current Results

See `/experiments/2026-03-11-hyperspace-agent-load-benchmark/RESEARCH_REPORT.md` for:
- Public endpoint baseline
- Node-local API sweeps
- Soak run behavior
- Recommended operating region

## Contribution

If you are a Hyperspace maintainer/contributor, open an issue with:
- Canonical endpoint list
- Target auth flow
- Required benchmark acceptance criteria

## License

MIT - see [LICENSE](LICENSE).
