# Copyright (c) 2026 Haley Ann Bird. All rights reserved.
# CLCE — Cross-Layer Consciousness Engine
"""
main.py — Entry-point for the CLCE prototype.
"""
from __future__ import annotations

from orchestrator import CLCEOrchestrator


def main() -> None:
    orc = CLCEOrchestrator()
    queries = [
        "What is the nature of consciousness?",
        "How does quantum superposition apply to cognition?",
        "Describe holographic memory storage.",
    ]
    for q in queries:
        result = orc.process(q)
        print(f"\n--- Query: {q} ---")
        print(f"Output   : {result.output}")
        print(f"Confidence: {result.confidence:.3f}")
        print(f"Coherence : {result.coherence_score:.3f}")
        print(f"Reflection: {result.reflection_action}")
        print(f"Elapsed   : {result.elapsed_s}s")
        print(f"Iterations: {result.meta.get('iterations', 1)}")


if __name__ == "__main__":
    main()
