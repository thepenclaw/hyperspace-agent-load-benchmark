# How to Add Your Own Experiment

## Quick Start

1. **Create folder with date prefix:**
   ```bash
   mkdir experiments/YYYY-MM-DD-your-experiment-name
   cd experiments/YYYY-MM-DD-your-experiment-name
   ```

2. **Create these files:**
   - `run.py` - Your experiment code (LLM edits CONFIG section)
   - `program.md` - Instructions for LLM agent
   - `auto_run.sh` - Automation script
   - `README.md` - Documentation

3. **Commit and push:**
   ```bash
   git add .
   git commit -m "New experiment: your-experiment-name"
   git push origin main
   ```

4. **Run on your Mac:**
   ```bash
   ./auto_run.sh
   ```

## File Templates

See existing experiments for examples.

---

*More docs coming soon*
