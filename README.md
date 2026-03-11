# Playwright Autoresearch MLX BYOC - ThePenclaw

**BYOC (Bring Your Own Compute) Autoresearch Platform for Apple Silicon**

Zero-cost automated research using cloud LLM agents + local M-series Macs.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: macOS](https://img.shields.io/badge/Platform-macOS-blue.svg)](https://www.apple.com/macos/)
[![Powered by: OpenClaw](https://img.shields.io/badge/Powered%20by-OpenClaw-green.svg)](https://openclaw.ai)
[![MLX](https://img.shields.io/badge/MLX-Apple%20Silicon-orange.svg)](https://github.com/ml-explore/mlx)

---

## What is BYOC Autoresearch?

**BYOC = Bring Your Own Compute**

A distributed research pattern where:
- **Cloud LLM Agent** (OpenClaw/Kimi) designs experiments
- **Local M-series Mac** (your machine) executes experiments  
- **GitHub** coordinates between them
- **Result:** Zero cloud compute costs, fully automated research

### The Loop

```
Cloud LLM (Designs) ←──────→ GitHub ←──────→ M4 Mac (Executes)
        ↑                      │                  │
        └──────────────────────┴──────────────────┘
                    (15 min cycles)
```

---

## Completed Research

| Date | Experiment | Key Finding | Status |
|------|------------|-------------|--------|
| 2026-03-10 | [Playwright M4 Optimization](experiments/2026-03-10-playwright-m4-optimization/) | 99% speedup, optimal config found | ✅ Complete |
| 2026-03-11 | [Hyperspace Agent Load Benchmark](experiments/2026-03-11-hyperspace-agent-load-benchmark/) | Cycle harness for TPS/latency/reliability testing | 🚧 In Progress |

---

## Quick Start

```bash
# Clone
git clone https://github.com/thepenclaw/playwright-autoresearch-mlx-byoc-thepenclaw.git
cd playwright-autoresearch-mlx-byoc-thepenclaw

# See a completed experiment
cd experiments/2026-03-10-playwright-m4-optimization
./auto_run.sh  # Or just read the results

# Start Hyperspace load benchmarking
cd ../2026-03-11-hyperspace-agent-load-benchmark
python3 run.py
```

---

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

**Key Principle:** Zero additional cost
- Use hardware you already own (M1/M2/M3/M4 Mac)
- Open source tools only
- No API keys needed
- No cloud compute bills

---

## Repository Structure

```
autoresearch-mlx-byoc-thepenclaw/
├── README.md                    # This file
├── LICENSE                      # MIT
├── ARCHITECTURE.md              # System design
│
├── experiments/                 # All research (date-wise)
│   ├── 2026-03-10-playwright-m4-optimization/
│   │   ├── README.md
│   │   ├── scraper.py
│   │   ├── auto_run.sh
│   │   ├── program.md
│   │   ├── RESEARCH_REPORT.md
│   │   └── results/
│   ├── 2026-03-11-hyperspace-agent-load-benchmark/
│   │   ├── README.md
│   │   ├── run.py
│   │   ├── auto_run.sh
│   │   ├── program.md
│   │   └── results/
│   └── YYYY-MM-DD-your-experiment/   # Add yours here
│
└── docs/                        # Documentation
    ├── SETUP.md
    ├── ADD_EXPERIMENT.md
    └── TROUBLESHOOTING.md
```

**Date-wise structure** makes it easy to:
- Track multiple studies
- Compare results over time
- Contribute new experiments
- Reference prior work

---

## Credits & Attribution

**Methodology:**  
[Andrej Karpathy](https://github.com/karpathy) - Autoresearch pattern from nanoGPT experiments

**MLX Framework:**  
[Apple MLX Team](https://github.com/ml-explore/mlx) - Apple Silicon machine learning framework

**Original MLX Port:**  
[trevin-creator/autoresearch-mlx](https://github.com/trevin-creator/autoresearch-mlx) - MLX port of Karpathy's autoresearch

**Platform:**  
[OpenClaw](https://openclaw.ai) - Agent ecosystem, ClawHub skills, built-in LLM

**Developer:**  
thepenclaw team

---

## License

MIT License - See [LICENSE](LICENSE)

---

*Last Updated: March 2026*  
*Status: Active research - accepting new experiments*
