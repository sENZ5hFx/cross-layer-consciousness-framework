# Copyright (c) 2026 Haley Ann Bird. All rights reserved.
# CLCE — Cross-Layer Consciousness Engine
"""
CLCE Full-Stack Orchestrator
Wires Subsystem 1, 2, and 3 into a single coherent processing loop.

All tuneable constants are read from config.py — no magic numbers here.

Usage
-----
    from prototype.orchestrator import CLCEOrchestrator
    orc = CLCEOrchestrator()
    result = orc.process("What is the nature of consciousness?")
    print(result.output)
    print(result.meta)
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, List, Optional

import numpy as np

import config
from embeddings import embed
from subsystem1.superposition_layer import SuperpositionLayer
from subsystem2.holographic_memory import HolographicMemory
from subsystem3.awareness_module import AwarenessModule
from subsystem3.intention_module import GoalLevel, IntentionModule
from subsystem3.reflection_module import ReflectionModule


@dataclass
class ProcessingResult:
    input: str
    output: str
    selected_interpretation: str
    confidence: float
    coherence_score: float
    reflection_action: str          # 'continue' | 'reframe' | 'restart'
    reframe_instruction: Optional[str]
    memory_hits: List[Any]
    elapsed_s: float
    meta: dict = field(default_factory=dict)


class CLCEOrchestrator:
    """
    End-to-end CLCE processing loop.

    Processing contract
    -------------------
    1. Generate N candidate interpretations of the input  (N = config.GENERATE_CANDIDATES_N)
    2. Embed input into context vector                     (dim = config.EMBEDDING_DIM)
    3. S1 collapses superposition → selected interpretation
    4. S2 retrieves relevant memories; encodes new output  (top_k = config.MEMORY_TOP_K)
    5. S3A updates awareness; S3B checks goal coherence
    6. S3C decides: continue / reframe / restart
    7. If reframe/restart: loop once more with reframe instruction injected
    8. Return ProcessingResult

    Loop is capped at config.MAX_ITERATIONS iterations.
    """

    MAX_ITERATIONS: int = config.MAX_ITERATIONS

    def __init__(
        self,
        memory_dim: int = config.MEMORY_DIM,
        embedding_dim: int = config.EMBEDDING_DIM,
        top_goals: Optional[List[str]] = None,
    ):
        self.s1 = SuperpositionLayer(
            min_branches=config.MIN_BRANCHES,
            max_branches=config.MAX_BRANCHES,
        )
        self.s2 = HolographicMemory(dim=memory_dim)
        self.mod_a = AwarenessModule()
        self.mod_b = IntentionModule()
        self.mod_c = ReflectionModule()
        self.embedding_dim = embedding_dim
        self._top_k = config.MEMORY_TOP_K

        for goal in (top_goals or ["answer accurately", "maintain coherence", "stay goal-aligned"]):
            self.mod_b.set_goal(goal, GoalLevel.TOP)

    # ── Public API ────────────────────────────────────────────────────────────

    def process(self, user_input: str, extra_context: Optional[str] = None) -> ProcessingResult:
        """Process a single user query through the full CLCE pipeline."""
        t0 = time.time()
        reframe_prefix = ""
        result = None

        for iteration in range(self.MAX_ITERATIONS):
            result = self._single_pass(
                user_input=user_input,
                extra_context=extra_context,
                reframe_prefix=reframe_prefix,
                iteration=iteration,
            )
            if result.reflection_action == "continue":
                break
            if result.reframe_instruction:
                reframe_prefix = result.reframe_instruction + " | "

        result.elapsed_s = round(time.time() - t0, 4)
        result.meta["iterations"] = iteration + 1
        result.meta["reflection_log"] = self.mod_c.get_audit_log()[-3:]
        result.meta["goal_hierarchy"] = self.mod_b.get_goal_hierarchy()
        return result

    def get_session_summary(self) -> dict:
        """Return a full snapshot of all subsystem states."""
        return {
            "memory_state": self.s2.get_state(),
            "collapse_log_length": len(self.s1.get_collapse_log()),
            "awareness": self.mod_a.get_state_report(),
            "reflection_summary": self.mod_c.summary(),
            "goal_hierarchy": self.mod_b.get_goal_hierarchy(),
        }

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _single_pass(
        self,
        user_input: str,
        extra_context: Optional[str],
        reframe_prefix: str,
        iteration: int,  # noqa: ARG002  kept for future per-iteration logic
    ) -> ProcessingResult:
        full_input = reframe_prefix + user_input
        if extra_context:
            full_input = f"{extra_context} | {full_input}"

        candidates = self._generate_candidates(full_input, n=config.GENERATE_CANDIDATES_N)
        ctx_vec = embed(full_input, dim=self.embedding_dim)
        self.s1.load(candidates)
        collapse = self.s1.observe(context_vector=ctx_vec)
        selected = collapse.selected.text
        confidence = collapse.confidence

        memory_hits = self.s2.retrieve(selected, top_k=self._top_k)
        self.s2.encode(selected, full_input, strength=confidence)

        self.mod_a.update_memory(selected)
        self.mod_a.update_belief(selected, confidence, source="subsystem1")
        report = self.mod_a.get_state_report()
        signal = self.mod_b.evaluate_coherence(selected)
        event = self.mod_c.evaluate(selected, report, signal)

        output = self._synthesize_output(selected, memory_hits, signal, event)
        return ProcessingResult(
            input=full_input,
            output=output,
            selected_interpretation=selected,
            confidence=confidence,
            coherence_score=signal.score,
            reflection_action=event.action,
            reframe_instruction=event.reframe_instruction,
            memory_hits=memory_hits,
            elapsed_s=0.0,
        )

    def _generate_candidates(self, text: str, n: int = config.GENERATE_CANDIDATES_N) -> list:
        """Generate *n* candidate interpretations of *text*.

        The first candidate is always the raw input at weight 1.0.  Up to
        n-1 semantically-tagged variants are appended at decreasing weights.
        If n > 5 the last slot is padded with a [synthetic] variant.
        """
        base = [(text, 1.0)]
        modifiers = [
            (f"[literal] {text}",    0.80),
            (f"[abstract] {text}",   0.70),
            (f"[causal] {text}",     0.60),
            (f"[contextual] {text}", 0.50),
        ]
        extras_needed = max(0, n - 1 - len(modifiers))
        for i in range(extras_needed):
            modifiers.append((f"[synthetic-{i}] {text}", 0.40 - i * 0.05))
        return base + modifiers[: n - 1]

    @staticmethod
    def _synthesize_output(selected, memory_hits, signal, event) -> str:
        parts = [f"Selected interpretation: {selected}"]
        if memory_hits:
            top_hit = memory_hits[0]
            parts.append(f"Relevant memory: {top_hit[1]} (sim={top_hit[0]:.3f})")
        parts.append(f"Goal coherence: {signal.score:.2f}")
        if event.reframe_instruction:
            parts.append(f"Reframe applied: {event.reframe_instruction}")
        return " | ".join(parts)
