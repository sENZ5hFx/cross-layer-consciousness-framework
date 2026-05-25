# Copyright (c) 2026 Haley Ann Bird. All rights reserved.
# CLCE — Cross-Layer Consciousness Engine
"""
Integration tests for the CLCEOrchestrator.
Run with: pytest prototype/tests/test_orchestrator.py -v
"""
from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from orchestrator import CLCEOrchestrator  # noqa: E402
from subsystem3.intention_module import GoalLevel  # noqa: E402


class TestOrchestrator:

    def setup_method(self):
        self.orc = CLCEOrchestrator(
            memory_dim=256,
            embedding_dim=64,
            top_goals=["answer accurately", "stay coherent"],
        )

    # ── Core contract ──────────────────────────────────────────────────────────

    def test_basic_process_returns_result(self):
        result = self.orc.process("What is consciousness?")
        assert result.output
        assert result.selected_interpretation
        assert 0.0 <= result.confidence <= 1.0

    def test_coherence_score_bounded(self):
        result = self.orc.process("Explain holographic memory")
        assert 0.0 <= result.coherence_score <= 1.0

    def test_reflection_action_valid(self):
        result = self.orc.process("some input text")
        assert result.reflection_action in ("continue", "reframe", "restart")

    def test_elapsed_time_positive(self):
        result = self.orc.process("test")
        assert result.elapsed_s > 0

    # ── Memory ─────────────────────────────────────────────────────────────────

    def test_memory_populated_after_process(self):
        self.orc.process("memory test query")
        assert self.orc.s2.get_state()["num_traces"] > 0

    def test_process_result_has_memory_hits_list(self):
        self.orc.process("first pass to populate memory")
        result = self.orc.process("second pass")
        assert isinstance(result.memory_hits, list)

    def test_memory_hits_are_score_value_tuples(self):
        """After at least one encode, hits must be (float, Any) tuples."""
        self.orc.process("populate")
        result = self.orc.process("populate")  # second pass triggers retrieval
        if result.memory_hits:
            score, val = result.memory_hits[0]
            assert isinstance(score, float)

    # ── Multi-turn ─────────────────────────────────────────────────────────────

    def test_multi_turn_belief_accumulation(self):
        for q in ["first query", "second query", "third query"]:
            self.orc.process(q)
        assert self.orc.mod_a.get_state_report()["belief_count"] >= 1

    # ── Session summary ────────────────────────────────────────────────────────

    def test_session_summary_keys(self):
        self.orc.process("summary test")
        summary = self.orc.get_session_summary()
        for key in ("memory_state", "reflection_summary", "goal_hierarchy"):
            assert key in summary

    # ── Goals ──────────────────────────────────────────────────────────────────

    def test_goal_can_be_added(self):
        self.orc.mod_b.set_goal("new custom goal", GoalLevel.MID)
        assert "new custom goal" in self.orc.mod_b.get_goal_hierarchy()["mid"]

    # ── Meta & config ──────────────────────────────────────────────────────────

    def test_iterations_capped(self):
        result = self.orc.process("adversarial drift test: unrelated babble")
        assert result.meta.get("iterations", 1) <= CLCEOrchestrator.MAX_ITERATIONS

    def test_meta_contains_reflection_log(self):
        result = self.orc.process("meta test")
        assert "reflection_log" in result.meta

    def test_max_iterations_reads_from_config(self):
        import config
        assert CLCEOrchestrator.MAX_ITERATIONS == config.MAX_ITERATIONS

    # ── extra_context ──────────────────────────────────────────────────────────

    def test_extra_context_accepted(self):
        result = self.orc.process("test input", extra_context="additional context")
        assert result.output

    def test_extra_context_appears_in_input_field(self):
        result = self.orc.process("query", extra_context="ctx")
        assert "ctx" in result.input
