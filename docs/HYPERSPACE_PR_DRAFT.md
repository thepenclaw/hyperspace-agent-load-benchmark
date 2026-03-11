# Draft PR Description: Benchmarking Workflow Contribution

## Summary
This PR contributes a reproducible BYOC benchmark workflow for endpoint-level efficiency testing (throughput, latency, reliability) under synthetic agent traffic.

## Added
- Hyperspace benchmark experiment scaffold
- Env-based secure runtime configuration for org credentials
- Duration mode + count mode with concurrency sweeps
- Soak and repeated-sweep protocol runner (`live_protocol.sh`)
- Research report template and contribution playbook

## Motivation
Provide maintainers and contributors a low-cost, reproducible method to validate and compare optimization changes against a consistent load protocol.

## Validation
- Harness executes and persists cycle artifacts.
- Supports single and multi-endpoint mode.
- Supports auth via environment variables (no secret in repo).

## Follow-up work
- Canonical endpoint profile from maintainers
- Chart generation (TPS/P95/success trends)
- CI smoke run with public endpoint profile
