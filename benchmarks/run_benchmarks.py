"""CLCE Benchmark Runner.

Usage:
    python run_benchmarks.py --subsystem all
    python run_benchmarks.py --subsystem superposition
    python run_benchmarks.py --subsystem holographic
    python run_benchmarks.py --subsystem metacognitive
"""

import argparse
import sys
import os
from loguru import logger

# Add prototype to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "prototype"))

from config import DEFAULT_CONFIG
from subsystem1.superposition_layer import SuperpositionLayer
from subsystem2.holographic_memory import HolographicMemory
from subsystem3.awareness_module import AwarenessModule
from subsystem3.intention_module import IntentionModule
from subsystem3.reflection_module import ReflectionModule


def run_superposition_benchmark():
    logger.info("=== Running Subsystem 1: Superposition Benchmark ===")
    layer = SuperpositionLayer(DEFAULT_CONFIG.superposition)

    test_cases = [
        "The bank was steep and the current was strong.",
        "I saw the man with the telescope on the hill.",
        "She told her friend that she had won the prize.",
        "Visiting relatives can be annoying.",
        "The horse raced past the barn fell."
    ]

    results = []
    for tc in test_cases:
        branches = layer.generate_branches(tc, {})
        coherence = {"score": 0.7}
        landscapes = [{"resonance": 0.5}] * len(branches)
        result = layer.collapse(branches, landscapes, coherence)
        results.append({
            "input": tc,
            "n_branches": len(branches),
            "confidence": result["confidence"],
            "alternatives": len(branches) - 1
        })
        logger.info(f"Input: '{tc[:50]}' | Branches: {len(branches)} | Confidence: {result['confidence']:.2f}")

    logger.success(f"Superposition benchmark complete. {len(results)} cases processed.")
    return results


def run_holographic_benchmark():
    logger.info("=== Running Subsystem 2: Holographic Memory Benchmark ===")
    memory = HolographicMemory(DEFAULT_CONFIG.holographic)

    # Encode test experiences
    experiences = [
        {"input": "Running the last mile of a marathon", "result": {}},
        {"input": "Finishing a difficult project under deadline", "result": {}},
        {"input": "The feeling of crossing a finish line", "result": {}},
        {"input": "Quantum superposition in physics", "result": {}},
        {"input": "Multiple possibilities existing simultaneously", "result": {}},
    ]

    for exp in experiences:
        memory.encode(exp)

    # Test retrieval with partial/cross-domain cues
    test_cues = [
        "marathon finish",
        "deadline pressure",
        "quantum states",
        "simultaneous options",  # Cross-domain: should link to superposition
        "exhausted but triumphant",  # Partial cue
    ]

    results = []
    for cue in test_cues:
        result = memory.retrieve(cue)
        results.append({
            "cue": cue,
            "resonance": result["resonance"],
            "n_matches": len(result["matches"]),
            "degraded": result["degraded"]
        })
        logger.info(f"Cue: '{cue}' | Resonance: {result['resonance']:.3f} | Degraded: {result['degraded']}")

    logger.success(f"Holographic benchmark complete. {len(results)} cues tested.")
    return results


def run_metacognitive_benchmark():
    logger.info("=== Running Subsystem 3: Meta-Cognitive Benchmark ===")
    config = DEFAULT_CONFIG.metacognitive
    awareness = AwarenessModule(config)
    intention = IntentionModule(config)
    reflection = ReflectionModule(config, awareness, intention)

    intention.set_top_goal("Understand the nature of consciousness")

    test_scenarios = [
        # (branches, should_trigger_interrupt)
        ([{"interpretation": "On-topic reasoning", "confidence": 0.85}], False),
        ([{"interpretation": "Uncertain output", "confidence": 0.2}], True),
        ([{"interpretation": "Off-topic drift", "confidence": 0.5}], True),
        ([{"interpretation": "Clear relevant response", "confidence": 0.9}], False),
    ]

    results = []
    for branches, expected_interrupt in test_scenarios:
        awareness.update(branches, [{"resonance": 0.6, "degraded": False}], {})
        coherence = intention.check_coherence(branches, awareness.get_state())
        should_restart, reason = reflection.evaluate(branches, coherence, awareness.get_state())
        correct = should_restart == expected_interrupt
        results.append({
            "input": branches[0]["interpretation"],
            "expected_interrupt": expected_interrupt,
            "actual_interrupt": should_restart,
            "correct": correct,
            "reason": reason
        })
        logger.info(f"Scenario: '{branches[0]['interpretation']}' | Expected: {expected_interrupt} | Got: {should_restart} | {'✓' if correct else '✗'}")

    accuracy = sum(r["correct"] for r in results) / len(results)
    logger.success(f"Meta-cognitive benchmark complete. Accuracy: {accuracy:.0%}")
    return results


def main():
    parser = argparse.ArgumentParser(description="CLCE Benchmark Runner")
    parser.add_argument(
        "--subsystem",
        choices=["all", "superposition", "holographic", "metacognitive"],
        default="all"
    )
    args = parser.parse_args()

    logger.info("CLCE Benchmark Suite starting...")

    if args.subsystem in ("all", "superposition"):
        run_superposition_benchmark()

    if args.subsystem in ("all", "holographic"):
        run_holographic_benchmark()

    if args.subsystem in ("all", "metacognitive"):
        run_metacognitive_benchmark()

    logger.success("All benchmarks complete.")


if __name__ == "__main__":
    main()
