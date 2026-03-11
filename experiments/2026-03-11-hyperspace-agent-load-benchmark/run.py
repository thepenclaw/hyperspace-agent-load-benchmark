#!/usr/bin/env python3
"""
Hyperspace Agent Load Benchmark (BYOC)

Cycle-based load testing harness for AgenticOS-compatible HTTP endpoints.
The LLM/agent should only edit CONFIG and LOAD_PROFILE.
"""

import json
import os
import statistics
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, as_completed, wait
from datetime import datetime

import requests

# =============================================================================
# CONFIG - AGENT MODIFIES THIS SECTION
# =============================================================================

CONFIG = {
    "api_base": "https://agents.hyper.space",
    "health_endpoint": "/",
    "request_timeout_seconds": 10,
    "warmup_requests": 5,
    "include_cpu_memory": True,
    "target_finality_ms": 400,
    "target_tps": 54000,
    "headers": {
        "User-Agent": "BYOC-Hyperspace-Benchmark/1.0",
    },
}

# Single-change-per-cycle discipline: adjust one item at a time.
LOAD_PROFILE = {
    "mode": "count",  # count | duration
    "total_requests": 120,
    "duration_seconds": 120,
    "max_requests": 50000,
    "concurrency": 8,
    "method": "GET",
    "endpoint": "/",
    "payload": None,
}

# =============================================================================
# CORE BENCHMARK
# =============================================================================


def now_iso():
    return datetime.utcnow().isoformat() + "Z"


def build_url(base, endpoint):
    return base.rstrip("/") + "/" + endpoint.lstrip("/")


def _env_int(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _env_bool(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_json(name):
    value = os.getenv(name)
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def resolved_config():
    # Env vars allow per-org credentials and hosts without editing source.
    cfg = json.loads(json.dumps(CONFIG))
    profile = json.loads(json.dumps(LOAD_PROFILE))

    cfg["api_base"] = os.getenv("HYPERSPACE_API_BASE", cfg["api_base"])
    cfg["request_timeout_seconds"] = _env_int(
        "HYPERSPACE_TIMEOUT_SECONDS", cfg["request_timeout_seconds"]
    )
    cfg["warmup_requests"] = _env_int("HYPERSPACE_WARMUP_REQUESTS", cfg["warmup_requests"])
    cfg["include_cpu_memory"] = _env_bool(
        "HYPERSPACE_INCLUDE_CPU_MEMORY", cfg["include_cpu_memory"]
    )
    cfg["target_finality_ms"] = _env_int("HYPERSPACE_TARGET_FINALITY_MS", cfg["target_finality_ms"])
    cfg["target_tps"] = _env_int("HYPERSPACE_TARGET_TPS", cfg["target_tps"])

    profile["total_requests"] = _env_int("HYPERSPACE_TOTAL_REQUESTS", profile["total_requests"])
    profile["duration_seconds"] = _env_int(
        "HYPERSPACE_DURATION_SECONDS", profile["duration_seconds"]
    )
    profile["max_requests"] = _env_int("HYPERSPACE_MAX_REQUESTS", profile["max_requests"])
    profile["concurrency"] = _env_int("HYPERSPACE_CONCURRENCY", profile["concurrency"])
    profile["method"] = os.getenv("HYPERSPACE_METHOD", profile["method"]).upper()
    profile["endpoint"] = os.getenv("HYPERSPACE_ENDPOINT", profile["endpoint"])
    profile["mode"] = os.getenv("HYPERSPACE_MODE", profile["mode"]).lower()

    payload = _env_json("HYPERSPACE_PAYLOAD_JSON")
    if payload is not None:
        profile["payload"] = payload

    headers = dict(cfg.get("headers", {}))
    extra_headers = _env_json("HYPERSPACE_EXTRA_HEADERS_JSON")
    if isinstance(extra_headers, dict):
        headers.update(extra_headers)

    token = os.getenv("HYPERSPACE_BEARER_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    api_key = os.getenv("HYPERSPACE_API_KEY")
    if api_key:
        headers["x-api-key"] = api_key

    cfg["headers"] = headers

    endpoint_list = os.getenv("HYPERSPACE_ENDPOINTS")
    if endpoint_list:
        targets = [item.strip() for item in endpoint_list.split(",") if item.strip()]
    else:
        targets = [profile["endpoint"]]

    return cfg, profile, targets


def one_request(session, url, method, headers, payload, timeout):
    start = time.perf_counter()
    try:
        if method == "POST":
            response = session.post(url, json=payload, headers=headers, timeout=timeout)
        else:
            response = session.get(url, headers=headers, timeout=timeout)
        elapsed = (time.perf_counter() - start) * 1000
        return {
            "ok": response.ok,
            "status_code": response.status_code,
            "latency_ms": elapsed,
            "error": None,
        }
    except Exception as exc:
        elapsed = (time.perf_counter() - start) * 1000
        return {
            "ok": False,
            "status_code": None,
            "latency_ms": elapsed,
            "error": str(exc),
        }


def percentile(values, p):
    if not values:
        return None
    sorted_values = sorted(values)
    idx = int(round((p / 100.0) * (len(sorted_values) - 1)))
    return sorted_values[idx]


def collect_host_stats(enabled):
    if not enabled:
        return None
    try:
        import psutil

        vm = psutil.virtual_memory()
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.3),
            "mem_percent": vm.percent,
            "mem_used_mb": round(vm.used / (1024 * 1024), 2),
        }
    except Exception:
        return {
            "cpu_percent": None,
            "mem_percent": None,
            "mem_used_mb": None,
            "note": "psutil not installed",
        }


def preflight(session, url, method, headers, payload, timeout):
    return one_request(session, url, method, headers, payload, timeout)


def run_load(session, url, method, headers, payload, timeout, profile):
    mode = profile["mode"]
    target_count = profile["total_requests"]
    duration_seconds = profile["duration_seconds"]
    max_requests = profile["max_requests"]
    max_workers = max(profile["concurrency"], 1)

    submitted = 0
    results = []
    end_time = time.perf_counter() + max(duration_seconds, 1)

    def should_submit_more():
        if mode == "duration":
            return submitted < max_requests and time.perf_counter() < end_time
        return submitted < target_count

    wall_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        in_flight = set()

        while len(in_flight) < max_workers and should_submit_more():
            in_flight.add(executor.submit(one_request, session, url, method, headers, payload, timeout))
            submitted += 1

        while in_flight:
            done, pending = wait(in_flight, return_when=FIRST_COMPLETED, timeout=0.5)
            in_flight = set(pending)
            for completed in done:
                results.append(completed.result())
                if should_submit_more():
                    in_flight.add(
                        executor.submit(one_request, session, url, method, headers, payload, timeout)
                    )
                    submitted += 1

    wall_elapsed_s = max(time.perf_counter() - wall_start, 0.001)
    return results, wall_elapsed_s


def run_single_target(cfg, profile, endpoint):
    url = build_url(cfg["api_base"], endpoint)
    method = profile["method"].upper()
    timeout = cfg["request_timeout_seconds"]

    print("=" * 72)
    print(f"Hyperspace Load Cycle @ {now_iso()}")
    print("=" * 72)
    print(f"Target URL: {url}")
    print(f"Method: {method}")
    print(f"Mode: {profile['mode']}")
    if profile["mode"] == "duration":
        print(
            f"Duration: {profile['duration_seconds']}s | Max requests: {profile['max_requests']}"
        )
    else:
        print(f"Total requests: {profile['total_requests']}")
    print(f"Concurrency: {profile['concurrency']}")

    with requests.Session() as session:
        preflight_result = preflight(
            session=session,
            url=url,
            method=method,
            headers=cfg["headers"],
            payload=profile["payload"],
            timeout=timeout,
        )

        for _ in range(max(cfg["warmup_requests"] - 1, 0)):
            _ = one_request(
                session=session,
                url=url,
                method=method,
                headers=cfg["headers"],
                payload=profile["payload"],
                timeout=timeout,
            )

        results, wall_elapsed_s = run_load(
            session=session,
            url=url,
            method=method,
            headers=cfg["headers"],
            payload=profile["payload"],
            timeout=timeout,
            profile=profile,
        )

    success = [r for r in results if r["ok"]]
    failures = [r for r in results if not r["ok"]]
    latencies = [r["latency_ms"] for r in success]

    observed_tps = len(success) / wall_elapsed_s
    observed_finality_ms = statistics.mean(latencies) if latencies else None

    summary = {
        "timestamp": now_iso(),
        "config": cfg,
        "load_profile": profile,
        "endpoint": endpoint,
        "requests_total": len(results),
        "requests_success": len(success),
        "requests_failed": len(failures),
        "success_rate": round(len(success) / max(len(results), 1), 4),
        "wall_time_seconds": round(wall_elapsed_s, 3),
        "observed_tps": round(observed_tps, 2),
        "latency_ms_avg": round(statistics.mean(latencies), 2) if latencies else None,
        "latency_ms_p50": round(percentile(latencies, 50), 2) if latencies else None,
        "latency_ms_p95": round(percentile(latencies, 95), 2) if latencies else None,
        "latency_ms_p99": round(percentile(latencies, 99), 2) if latencies else None,
        "finality_target_ms": cfg["target_finality_ms"],
        "target_tps": cfg["target_tps"],
        "target_finality_met": observed_finality_ms is not None
        and observed_finality_ms <= cfg["target_finality_ms"],
        "target_tps_met": observed_tps >= cfg["target_tps"],
        "host_stats": collect_host_stats(cfg["include_cpu_memory"]),
        "failure_examples": failures[:5],
        "preflight": {
            "ok": preflight_result["ok"],
            "status_code": preflight_result["status_code"],
            "latency_ms": round(preflight_result["latency_ms"], 2),
            "error": preflight_result["error"],
        },
    }

    print("\nSUMMARY")
    print("-" * 72)
    print(f"Success: {summary['requests_success']}/{summary['requests_total']}")
    print(f"Observed TPS: {summary['observed_tps']}")
    print(f"Avg latency (ms): {summary['latency_ms_avg']}")
    print(f"P95 latency (ms): {summary['latency_ms_p95']}")
    print(f"Target 400ms met: {summary['target_finality_met']}")
    print(f"Target 54k TPS met: {summary['target_tps_met']}")

    return summary, latencies


def run_cycle():
    cfg, profile, targets = resolved_config()
    target_summaries = []
    all_latencies = []
    for endpoint in targets:
        summary, latencies = run_single_target(cfg, profile, endpoint)
        target_summaries.append(summary)
        all_latencies.extend(latencies)

    total_requests = sum(item["requests_total"] for item in target_summaries)
    total_success = sum(item["requests_success"] for item in target_summaries)
    total_failed = sum(item["requests_failed"] for item in target_summaries)
    all_wall_time = 0.0
    for item in target_summaries:
        all_wall_time += item["wall_time_seconds"]

    rollup = {
        "timestamp": now_iso(),
        "config": cfg,
        "load_profile": profile,
        "targets": targets,
        "requests_total": total_requests,
        "requests_success": total_success,
        "requests_failed": total_failed,
        "success_rate": round(total_success / max(total_requests, 1), 4),
        "wall_time_seconds": round(all_wall_time, 3),
        "observed_tps": round(total_success / max(all_wall_time, 0.001), 2),
        "latency_ms_avg": round(statistics.mean(all_latencies), 2) if all_latencies else None,
        "latency_ms_p50": round(percentile(all_latencies, 50), 2) if all_latencies else None,
        "latency_ms_p95": round(percentile(all_latencies, 95), 2) if all_latencies else None,
        "latency_ms_p99": round(percentile(all_latencies, 99), 2) if all_latencies else None,
        "finality_target_ms": cfg["target_finality_ms"],
        "target_tps": cfg["target_tps"],
        "target_finality_met": False,
        "target_tps_met": False,
        "host_stats": collect_host_stats(cfg["include_cpu_memory"]),
        "target_results": target_summaries,
    }
    rollup["target_finality_met"] = (
        rollup["latency_ms_avg"] is not None and rollup["latency_ms_avg"] <= cfg["target_finality_ms"]
    )
    rollup["target_tps_met"] = rollup["observed_tps"] >= cfg["target_tps"]
    return rollup


def persist(summary):
    os.makedirs("results", exist_ok=True)
    existing = [f for f in os.listdir("results") if f.startswith("cycle_") and f.endswith(".json")]
    cycle_num = len(existing) + 1

    path = f"results/cycle_{cycle_num:02d}.json"
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    tsv_path = os.getenv("HYPERSPACE_RESULTS_FILE", "results.tsv")
    tsv_exists = os.path.exists(tsv_path)
    with open(tsv_path, "a", encoding="utf-8") as handle:
        if not tsv_exists:
            handle.write(
                "cycle\ttimestamp\tmode\tconcurrency\ttotal_requests\tsuccess_rate\tobserved_tps\tlatency_ms_avg\tlatency_ms_p95\tlatency_ms_p99\ttarget_finality_met\ttarget_tps_met\n"
            )
        handle.write(
            f"{cycle_num}\t{summary['timestamp']}\t{summary['load_profile']['mode']}\t"
            f"{summary['load_profile']['concurrency']}\t"
            f"{summary['requests_total']}\t{summary['success_rate']}\t{summary['observed_tps']}\t"
            f"{summary['latency_ms_avg']}\t{summary['latency_ms_p95']}\t"
            f"{summary['latency_ms_p99']}\t"
            f"{summary['target_finality_met']}\t{summary['target_tps_met']}\n"
        )

    print(f"\nSaved: {path}")
    print(f"Appended: {tsv_path}")


if __name__ == "__main__":
    cycle_summary = run_cycle()
    persist(cycle_summary)
