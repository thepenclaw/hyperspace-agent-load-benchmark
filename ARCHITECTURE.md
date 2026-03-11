# BYOC Architecture

## System Design

### Overview

BYOC (Bring Your Own Compute) pairs cloud-based LLM agents with local Apple Silicon Macs for zero-cost automated research.

### Components

| Component | Role | Location | Cost |
|-----------|------|----------|------|
| **LLM Agent** | Designs experiments, analyzes results | Cloud (OpenClaw) | Free/cheap built-in |
| **GitHub** | Coordination, version control | Cloud | Free tier |
| **M-series Mac** | Execute experiments | Local (your machine) | $0 (you own it) |

### Data Flow

```
Cloud LLM (Designs) ←──────→ GitHub ←──────→ M4 Mac (Executes)
        ↑                      │                  │
        └──────────────────────┴──────────────────┘
                    (15 min cycles)
```

### Cycle Walkthrough

1. **LLM designs experiment** → Pushes config to GitHub
2. **Mac pulls config** → Runs experiment
3. **Mac pushes results** → Back to GitHub
4. **LLM analyzes** → Designs next cycle
5. **Repeat** for 10 cycles

### Communication

Git acts as message queue:
- Push = Send message
- Pull = Receive message
- No webhooks needed
- Works with intermittent connectivity

### Date-Wise Structure

```
experiments/
├── 2026-03-10-playwright-m4-optimization/
├── 2026-04-15-mlx-quantization-study/
└── YYYY-MM-DD-descriptive-name/
```

**Benefits:**
- Natural chronological ordering
- Easy to find past work
- Multiple concurrent studies
- Clear versioning

---

*See README.md for usage instructions*
