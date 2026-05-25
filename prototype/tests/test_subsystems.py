# Copyright (c) 2026 Haley Ann Bird. All rights reserved.
# CLCE — Cross-Layer Consciousness Engine
"""
Unit tests for all three CLCE subsystems.
Run with: pytest prototype/tests/test_subsystems.py -v

Note: sys.path manipulation below is belt-and-suspenders alongside conftest.py.
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from subsystem1.superposition_layer import SuperpositionLayer  # noqa: E402
from subsystem2.holographic_memory import HolographicMemory, cosine_similarity  # noqa: E402
from subsystem3.awareness_module import AwarenessModule  # noqa: E402
from subsystem3.intention_module import CoherenceSignal, GoalLevel, IntentionModule  # noqa: E402
from subsystem3.reflection_module import ReflectionModule  # noqa: E402


# ── Shared fixtures ────────────────────────────────────────────────────────────

def _make_coherence_signal(
    score: float = 0.8,
    drifting: list | None = None,
) -> CoherenceSignal:
    return CoherenceSignal(
        score=score,
        drifting_goals=drifting or [],
        resolution="On track." if score >= 0.4 else "Reorient.",
    )


def _make_awareness_report(uncertainty_count: int = 0) -> dict:
    return {
        "active_beliefs": [],
        "active_memories": [],
        "uncertainty_flags": [],
        "recent_revisions": [],
        "uncertainty_count": uncertainty_count,
        "belief_count": 0,
    }


# ── Subsystem 1 ────────────────────────────────────────────────────────────────

class TestSuperpositionLayer:
    def setup_method(self):
        self.s1 = SuperpositionLayer(min_branches=3)

    def test_load_and_collapse(self):
        self.s1.load([("Paris", 0.6), ("London", 0.3), ("Berlin", 0.1)])
        result = self.s1.observe()
        assert result.selected.text == "Paris"
        assert len(result.alternatives) == 2

    def test_weights_sum_to_one(self):
        self.s1.load([("A", 1.0), ("B", 3.0), ("C", 6.0)])
        total = sum(b.weight for b in self.s1._active_branches)
        assert abs(total - 1.0) < 1e-6

    def test_alternatives_preserved(self):
        self.s1.load([("X", 0.5), ("Y", 0.3), ("Z", 0.2)])
        result = self.s1.observe()
        alt_texts = [a.text for a in result.alternatives]
        assert "Y" in alt_texts
        assert "Z" in alt_texts

    def test_confidence_between_zero_and_one(self):
        self.s1.load([("A", 0.8), ("B", 0.2)])
        result = self.s1.observe()
        assert 0.0 <= result.confidence <= 1.0

    def test_context_vector_reweights(self):
        self.s1.load([("quantum", 0.4), ("classical", 0.4), ("random", 0.2)])
        ctx = np.zeros(64)
        ctx[0] = 1.0
        result = self.s1.observe(context_vector=ctx)
        assert result.collapse_reason == "context_signal"

    def test_collapse_log_grows(self):
        for _ in range(3):
            self.s1.load([("A", 0.6), ("B", 0.4)])
            self.s1.observe()
        assert len(self.s1.get_collapse_log()) == 3

    def test_active_branches_cleared_after_collapse(self):
        self.s1.load([("A", 0.6), ("B", 0.4)])
        self.s1.observe()
        assert self.s1._active_branches == []

    def test_observe_before_load_raises(self):
        with pytest.raises(RuntimeError):
            self.s1.observe()

    def test_zero_weight_raises(self):
        with pytest.raises(ValueError):
            self.s1.load([("A", 0.0)])


# ── Subsystem 2 ────────────────────────────────────────────────────────────────

class TestHolographicMemory:
    def setup_method(self):
        self.mem = HolographicMemory(dim=256)

    def test_encode_increments_trace_count(self):
        self.mem.encode("sky", "blue")
        assert self.mem.get_state()["num_traces"] == 1

    def test_retrieve_returns_list(self):
        self.mem.encode("ocean", "deep")
        results = self.mem.retrieve("ocean")
        assert isinstance(results, list)
        assert len(results) >= 1

    def test_retrieve_top_match_value(self):
        self.mem.encode("capital", "Paris")
        results = self.mem.retrieve("capital", top_k=1)
        _, val = results[0]
        assert val == "Paris"

    def test_retrieve_empty_returns_empty(self):
        assert self.mem.retrieve("ghost") == []

    def test_retrieve_partial_returns_list(self):
        self.mem.encode("quantum", "entanglement")
        assert isinstance(self.mem.retrieve_partial("quantum"), list)

    def test_get_state_keys(self):
        state = self.mem.get_state()
        for key in ("num_traces", "memory_norm", "dim"):
            assert key in state

    def test_retrieve_returns_float_value_tuples(self):
        self.mem.encode("topic", "value")
        hits = self.mem.retrieve("topic", top_k=1)
        assert len(hits) == 1
        score, val = hits[0]
        assert isinstance(score, float)
        assert isinstance(val, str)


class TestCosineSimilarity:
    def test_identical_vectors(self):
        v = np.array([1.0, 0.0, 0.0])
        assert abs(cosine_similarity(v, v) - 1.0) < 1e-6

    def test_orthogonal_vectors(self):
        assert abs(cosine_similarity(np.array([1.0, 0.0]), np.array([0.0, 1.0]))) < 1e-6

    def test_zero_vector_safe(self):
        assert isinstance(cosine_similarity(np.zeros(4), np.ones(4)), float)


# ── Subsystem 3 ────────────────────────────────────────────────────────────────

class TestAwarenessModule:
    def setup_method(self):
        self.mod = AwarenessModule()

    def test_update_belief_adds_entry(self):
        self.mod.update_belief("sky is blue", 0.9)
        assert self.mod.get_state_report()["belief_count"] == 1

    def test_flag_and_resolve_unknown(self):
        self.mod.flag_unknown("dark matter")
        assert self.mod.get_state_report()["uncertainty_count"] == 1
        self.mod.resolve_unknown("dark matter")
        assert self.mod.get_state_report()["uncertainty_count"] == 0

    def test_clear_session_resets(self):
        self.mod.update_belief("test", 0.8)
        self.mod.flag_unknown("x")
        self.mod.clear_session()
        report = self.mod.get_state_report()
        assert report["belief_count"] == 0
        assert report["uncertainty_count"] == 0

    def test_revision_logged_on_large_delta(self):
        self.mod.update_belief("claim", 0.1)
        self.mod.update_belief("claim", 0.9)
        assert len(self.mod.get_state_report()["recent_revisions"]) >= 1


class TestIntentionModule:
    def setup_method(self):
        self.mod = IntentionModule()

    def test_set_goal_appears_in_hierarchy(self):
        self.mod.set_goal("answer accurately", GoalLevel.TOP)
        assert "answer accurately" in self.mod.get_goal_hierarchy()["top"]

    def test_deactivate_removes_goal(self):
        self.mod.set_goal("temp", GoalLevel.IMMEDIATE)
        self.mod.deactivate_goal("temp")
        assert "temp" not in self.mod.get_goal_hierarchy()["immediate"]

    def test_evaluate_coherence_returns_signal(self):
        self.mod.set_goal("explain consciousness", GoalLevel.TOP)
        signal = self.mod.evaluate_coherence("consciousness is a field")
        assert 0.0 <= signal.score <= 1.0

    def test_no_goals_returns_perfect_coherence(self):
        signal = self.mod.evaluate_coherence("anything")
        assert signal.score == 1.0


class TestReflectionModule:
    def setup_method(self):
        self.mod = ReflectionModule()

    def test_clean_state_continues(self):
        event = self.mod.evaluate("output", _make_awareness_report(), _make_coherence_signal(0.9))
        assert event.action == "continue"

    def test_low_coherence_reframes_or_restarts(self):
        event = self.mod.evaluate(
            "off-topic", _make_awareness_report(1), _make_coherence_signal(0.25, ["g"])
        )
        assert event.action in ("reframe", "restart")

    def test_very_low_triggers_restart(self):
        event = self.mod.evaluate(
            "chaos", _make_awareness_report(6), _make_coherence_signal(0.1, ["a", "b"])
        )
        assert event.action == "restart"

    def test_interrupt_log_accumulates(self):
        for _ in range(3):
            self.mod.evaluate("x", _make_awareness_report(), _make_coherence_signal())
        assert len(self.mod.interrupt_log) == 3

    def test_summary_totals_match(self):
        for score in [0.9, 0.9, 0.25]:
            self.mod.evaluate(
                "x",
                _make_awareness_report(1 if score < 0.4 else 0),
                _make_coherence_signal(score, ["g"] if score < 0.4 else []),
            )
        s = self.mod.summary()
        assert s["total_interrupts"] == 3
        assert s["continues"] == 2
