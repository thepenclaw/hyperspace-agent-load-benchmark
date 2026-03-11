# Hyperspace Contribution Playbook (Visibility + Collaboration)

## Goal

Contribute measurable benchmarking value publicly so maintainers can validate, reproduce, and discuss optimization opportunities.

## 1) Preparation

- Keep results reproducible (`run.py`, `results.tsv`, cycle JSON files).
- Keep secrets out of repo (env vars only).
- Pin exact commit SHA and environment details in your report.

## 2) Contribution Assets

Prepare these artifacts before opening anything publicly:
- Research report from `RESEARCH_REPORT_TEMPLATE.md`
- CSV/TSV summary and cycle JSONs
- A short chart set (TPS vs concurrency, P95 vs concurrency, success rate vs concurrency)
- Proposed code changes or instrumentation patches

## 3) Public Entry Path

Use this order:
1. Open a GitHub Discussion/Issue in Hyperspace org with your findings.
2. Link your public benchmark repo and reproducible commands.
3. Ask for maintainer feedback on endpoint choice and expected bottlenecks.
4. Open a PR once alignment is confirmed.

## 4) Issue Template (Suggested)

Title:
- "Benchmark: endpoint load profile on Apple Silicon (TPS/latency/error curve)"

Body:
- Objective
- Test protocol
- Key results table
- Bottlenecks observed
- Proposed optimizations
- Repro steps
- Requested feedback

## 5) PR Scope Guidelines

Keep PRs narrow:
- One instrumentation feature per PR, or
- One benchmark automation improvement per PR, or
- One docs/reporting improvement per PR

## 6) Collaboration Angle

Position the work as:
- "External reproducible load signal"
- "Low-cost BYOC benchmarking harness"
- "Actionable optimization proposals with measured deltas"

## 7) Credibility Checklist

Before posting publicly:
- At least 5 cycles with stable trend
- Error categories captured
- Throughput and latency both reported
- Hardware/environment explicitly documented
- No unverifiable claims
