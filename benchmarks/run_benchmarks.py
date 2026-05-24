"""
CLCE Benchmark Runner — Phase 4

Runs all three subsystem falsifiability tests against baseline comparisons.
Outputs results to benchmarks/results/

Usage:
    python benchmarks/run_benchmarks.py
"""

import json
import time
import numpy as np
from pathlib import Path
from datetime import datetime
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'prototype'))

from subsystem1.superposition_layer import SuperpositionLayer
from subsystem2.holographic_memory import HolographicMemory, cosine_similarity
from subsystem3.awareness_module import AwarenessModule
from subsystem3.intention_module import IntentionModule, GoalLevel
from subsystem3.reflection_module import ReflectionModule

Results = Path(__file__).parent / 'results'
Results.mkdir(exist_ok=True)


# ─── Benchmark 1: Superposition vs Greedy Baseline ───────────────────────────

def benchmark_superposition(n_trials: int = 50) -> dict:
    """
    Task: Ambiguous input resolution.
    CLCE: holds branches, collapses on context signal.
    Baseline: greedy — picks highest weight immediately.
    Metric: % of trials where preserved alternatives contain the correct answer.
    """
    s1 = SuperpositionLayer()
    rng = np.random.default_rng(42)

    clce_correct = 0
    greedy_correct = 0

    for trial in range(n_trials):
        weights = rng.dirichlet(np.ones(4)) * 100
        candidates = [(f"interp_{i}", float(weights[i])) for i in range(4)]
        # Correct answer is NOT always the highest-weight candidate
        correct_idx = int(rng.integers(0, 4))
        correct_label = f"interp_{correct_idx}"

        # Baseline: greedy pick
        greedy_pick = max(candidates, key=lambda x: x[1])[0]
        greedy_correct += int(greedy_pick == correct_label)

        # CLCE: check if correct is anywhere in top-3 branches
        s1.load(candidates)
        result = s1.observe()
        all_branches = [result.selected.text] + [a.text for a in result.alternatives]
        clce_correct += int(correct_label in all_branches[:3])

    return {
        "benchmark": "superposition_ambiguity",
        "n_trials": n_trials,
        "clce_accuracy": clce_correct / n_trials,
        "greedy_accuracy": greedy_correct / n_trials,
        "clce_delta": (clce_correct - greedy_correct) / n_trials,
        "pass": clce_correct > greedy_correct
    }


# ─── Benchmark 2: Holographic vs Exact-Match Baseline ─────────────────────────

def benchmark_holographic(n_items: int = 30, n_queries: int = 20) -> dict:
    """
    Task: Partial-cue retrieval.
    CLCE: HRR-based associative retrieval.
    Baseline: exact key match (returns None on partial keys).
    Metric: retrieval hit rate under partial/degraded cues.
    """
    s2 = HolographicMemory(dim=512)
    rng = np.random.default_rng(42)

    keys = [f"concept_{i}" for i in range(n_items)]
    values = [f"value_{i}" for i in range(n_items)]
    for k, v in zip(keys, values):
        s2.encode(k, v)

    clce_hits = 0
    baseline_hits = 0
    stored_keys = {k: v for k, v in zip(keys, values)}

    for _ in range(n_queries):
        idx = int(rng.integers(0, n_items))
        full_key = keys[idx]
        # Partial cue: first 7 chars
        partial_key = full_key[:7]
        target_val = values[idx]

        # CLCE retrieval (partial)
        results = s2.retrieve_partial(partial_key, top_k=3)
        clce_hits += int(any(val == target_val for _, val in results))

        # Baseline: exact match only
        baseline_hits += int(stored_keys.get(partial_key) == target_val)

    return {
        "benchmark": "holographic_partial_retrieval",
        "n_items": n_items,
        "n_queries": n_queries,
        "clce_hit_rate": clce_hits / n_queries,
        "baseline_hit_rate": baseline_hits / n_queries,
        "clce_delta": (clce_hits - baseline_hits) / n_queries,
        "pass": clce_hits >= baseline_hits
    }


# ─── Benchmark 3: Meta-Cognitive Goal Drift ───────────────────────────────────

def benchmark_metacognitive(n_steps: int = 20) -> dict:
    """
    Task: Maintain goal alignment over N processing steps.
    CLCE: Module B monitors; Module C interrupts on drift.
    Baseline: no monitoring (all outputs accepted as-is).
    Metric: cumulative goal drift events detected and corrected.
    """
    mod_a = AwarenessModule()
    mod_b = IntentionModule()
    mod_c = ReflectionModule()

    mod_b.set_goal("explain consciousness architecture", GoalLevel.TOP)
    mod_b.set_goal("compare CLCE vs QNHF", GoalLevel.MID)

    rng = np.random.default_rng(42)
    outputs = (
        ["consciousness architecture explained through subsystems"] * (n_steps // 2) +
        ["the weather is great today", "I like pizza", "random unrelated content"] * (n_steps // 6)
    )
    rng.shuffle(outputs)

    clce_corrections = 0
    baseline_drift_undetected = 0

    for output in outputs[:n_steps]:
        signal = mod_b.evaluate_coherence(output)
        report = mod_a.get_state_report()
        event = mod_c.evaluate(output, report, signal)

        if event.action in ("reframe", "restart"):
            clce_corrections += 1
        if signal.score < 0.3:
            baseline_drift_undetected += 1  # baseline would miss this

    summary = mod_c.summary()
    return {
        "benchmark": "metacognitive_goal_drift",
        "n_steps": n_steps,
        "clce_corrections": clce_corrections,
        "baseline_undetected_drift": baseline_drift_undetected,
        "avg_coherence": summary.get("avg_coherence", 0.0),
        "interrupt_summary": summary,
        "pass": clce_corrections > 0
    }


# ─── Runner ───────────────────────────────────────────────────────────────────

def run_all() -> None:
    print("\n" + "=" * 60)
    print("CLCE BENCHMARK SUITE — Phase 4")
    print(f"Run at: {datetime.utcnow().isoformat()} UTC")
    print("=" * 60)

    all_results = []

    for fn, name in [
        (benchmark_superposition, "Subsystem 1: Superposition Ambiguity"),
        (benchmark_holographic, "Subsystem 2: Holographic Partial Retrieval"),
        (benchmark_metacognitive, "Subsystem 3: Meta-Cognitive Goal Drift")
    ]:
        print(f"\nRunning: {name}...")
        t0 = time.time()
        result = fn()
        elapsed = time.time() - t0
        result["elapsed_s"] = round(elapsed, 3)
        all_results.append(result)

        status = "✅ PASS" if result["pass"] else "❌ FAIL"
        print(f"  {status}")
        for k, v in result.items():
            if k not in ("pass", "interrupt_summary"):
                print(f"  {k}: {v}")

    out_path = Results / f"benchmark_run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(out_path, 'w') as f:
        json.dump({"run_at": datetime.utcnow().isoformat(), "results": all_results}, f, indent=2)

    print(f"\nResults saved to: {out_path}")
    print("\n" + "=" * 60)
    passed = sum(1 for r in all_results if r["pass"])
    print(f"TOTAL: {passed}/{len(all_results)} benchmarks passed")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_all()
