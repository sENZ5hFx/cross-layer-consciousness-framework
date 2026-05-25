# Copyright (c) 2026 Haley Ann Bird. All rights reserved.
# CLCE — Cross-Layer Consciousness Engine
"""
session_cli.py — Interactive REPL for CLCE sessions.

Usage:
    python -m prototype.session_cli
    python prototype/session_cli.py
"""
from __future__ import annotations

import sys

from orchestrator import CLCEOrchestrator


def run_session() -> None:
    print("CLCE Session CLI — type 'exit' or Ctrl-C to quit.")
    orc = CLCEOrchestrator()
    while True:
        try:
            user_input = input("\n> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break
        if not user_input or user_input.lower() in {"exit", "quit"}:
            break
        result = orc.process(user_input)
        print(f"Output   : {result.output}")
        print(f"Confidence : {result.confidence:.3f}  |  Coherence: {result.coherence_score:.3f}")
        print(f"Reflection : {result.reflection_action}")
        if result.reframe_instruction:
            print(f"Reframe    : {result.reframe_instruction}")


if __name__ == "__main__":
    run_session()
    sys.exit(0)
