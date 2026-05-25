# Copyright (c) 2026 Haley Ann Bird. All rights reserved.
# CLCE — Cross-Layer Consciousness Engine
"""
run_benchmarks.py — Lightweight benchmark suite for CI.

Runs timing benchmarks on the three core subsystems and writes results
to benchmarks/results/benchmark_results.json.
"""
from __future__ import annotations

import json
import os
import sys
import time

# Allow running from repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "prototype"))

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def bench(label: str, fn, iterations: int = 20) -> dict:
    times = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    avg = sum(times) / len(times)
    print(f"  {label:40s}  avg={avg*1000:.2f}ms  min={min(times)*1000:.2f}ms")
    return {"label": label, "avg_ms": round(avg * 1000, 4), "min_ms": round(min(times) * 1000, 4), "iterations": iterations}


def main() -> None:
    results = []
    print("\n=== CLCE Benchmark Suite ===")

    # ── Embedding benchmark ───────────────────────────────────────────────
    try:
        from embeddings import embed
        import numpy as np
        results.append(bench("embed() 128-dim", lambda: embed("What is consciousness?", dim=128)))
        results.append(bench("embed() 512-dim", lambda: embed("What is consciousness?", dim=512)))
    except Exception as e:
        print(f"  [SKIP] embeddings: {e}")

    # ── Superposition benchmark ───────────────────────────────────────────
    try:
        from subsystem1.superposition_layer import SuperpositionLayer
        from embeddings import embed
        s1 = SuperpositionLayer(min_branches=3, max_branches=8)
        candidates = [(f"candidate {i}", 1.0 / (i + 1)) for i in range(5)]
        ctx = embed("test", dim=128)
        s1.load(candidates)
        results.append(bench("S1 collapse (5 candidates)", lambda: s1.observe(ctx)))
    except Exception as e:
        print(f"  [SKIP] superposition: {e}")

    # ── Holographic memory benchmark ──────────────────────────────────────
    try:
        from subsystem2.holographic_memory import HolographicMemory
        mem = HolographicMemory(dim=512)
        mem.encode("consciousness", "source text", strength=0.9)
        results.append(bench("S2 encode()", lambda: mem.encode("test", "text", strength=0.8)))
        results.append(bench("S2 retrieve() top_k=3", lambda: mem.retrieve("test", top_k=3)))
    except Exception as e:
        print(f"  [SKIP] holographic memory: {e}")

    # ── Write results ────────────────────────────────────────────────────
    out_path = os.path.join(RESULTS_DIR, "benchmark_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults written to {out_path}")
    print(f"Total benchmarks run: {len(results)}")


if __name__ == "__main__":
    main()
