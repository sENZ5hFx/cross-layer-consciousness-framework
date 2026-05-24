"""
Unit tests for all three CLCE subsystems.
Run with: pytest prototype/tests/test_subsystems.py -v
"""

import numpy as np
import pytest

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from subsystem1.superposition_layer import SuperpositionLayer, Interpretation
from subsystem2.holographic_memory import HolographicMemory, cosine_similarity
from subsystem3.awareness_module import AwarenessModule
from subsystem3.intention_module import IntentionModule, GoalLevel
from subsystem3.reflection_module import ReflectionModule


# ─── Subsystem 1 Tests ────────────────────────────────────────────────────────

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


# ─── Subsystem 2 Tests ────────────────────────────────────────────────────────

class TestHolographicMemory:
    def setup_method(self):
        self.s2 = HolographicMemory(dim=512)

    def test_encode_and_retrieve(self):
        self.s2.encode("color", "blue")
        results = self.s2.retrieve("color")
        assert len(results) == 1
        score, val = results[0]
        assert val == "blue"
        assert score > 0.0

    def test_multiple_encodings(self):
        self.s2.encode("animal", "cat")
        self.s2.encode("vehicle", "car")
        self.s2.encode("food", "pizza")
        results = self.s2.retrieve("food")
        assert results[0][1] == "pizza"

    def test_partial_retrieval_returns_results(self):
        self.s2.encode("neuroscience", "synaptic plasticity")
        results = self.s2.retrieve_partial("neuro")
        assert len(results) > 0

    def test_memory_state(self):
        self.s2.encode("k1", "v1")
        self.s2.encode("k2", "v2")
        state = self.s2.get_state()
        assert state["num_traces"] == 2
        assert state["memory_norm"] > 0

    def test_cosine_similarity_bounds(self):
        a = np.random.randn(64)
        b = np.random.randn(64)
        sim = cosine_similarity(a, b)
        assert -1.1 <= sim <= 1.1


# ─── Subsystem 3 Tests ────────────────────────────────────────────────────────

class TestAwarenessModule:
    def setup_method(self):
        self.mod_a = AwarenessModule()

    def test_update_belief(self):
        self.mod_a.update_belief("sky is blue", 0.9)
        assert len(self.mod_a.active_beliefs) == 1

    def test_belief_revision_logged(self):
        self.mod_a.update_belief("earth is flat", 0.8)
        self.mod_a.update_belief("earth is flat", 0.1)  # confidence changed
        assert len(self.mod_a.revision_log) == 1

    def test_flag_and_resolve_unknown(self):
        self.mod_a.flag_unknown("dark matter")
        assert "dark matter" in self.mod_a.uncertainty_flags
        self.mod_a.resolve_unknown("dark matter")
        assert "dark matter" not in self.mod_a.uncertainty_flags

    def test_state_report_structure(self):
        self.mod_a.update_belief("test", 0.5)
        report = self.mod_a.get_state_report()
        assert "active_beliefs" in report
        assert "uncertainty_flags" in report
        assert "recent_revisions" in report


class TestIntentionModule:
    def setup_method(self):
        self.mod_b = IntentionModule()

    def test_set_goal(self):
        self.mod_b.set_goal("explain consciousness", GoalLevel.TOP)
        assert len(self.mod_b.goals) == 1

    def test_coherence_on_track(self):
        self.mod_b.set_goal("explain consciousness", GoalLevel.TOP)
        signal = self.mod_b.evaluate_coherence("consciousness is explained by...")
        assert signal.score > 0.3

    def test_coherence_drift_detected(self):
        self.mod_b.set_goal("explain quantum physics", GoalLevel.TOP)
        signal = self.mod_b.evaluate_coherence("the weather today is sunny")
        assert len(signal.drifting_goals) > 0

    def test_goal_hierarchy_structure(self):
        self.mod_b.set_goal("understand AI", GoalLevel.TOP)
        self.mod_b.set_goal("read CLCE paper", GoalLevel.MID)
        hierarchy = self.mod_b.get_goal_hierarchy()
        assert "top" in hierarchy
        assert "mid" in hierarchy


class TestReflectionModule:
    def setup_method(self):
        self.mod_c = ReflectionModule()

    def _make_signal(self, score, drifting=None):
        from subsystem3.intention_module import CoherenceSignal
        return CoherenceSignal(score=score, drifting_goals=drifting or [], resolution="test")

    def test_continue_on_high_coherence(self):
        signal = self._make_signal(0.9)
        report = {"uncertainty_count": 0, "uncertainty_flags": [], "recent_revisions": []}
        event = self.mod_c.evaluate("some output", report, signal)
        assert event.action == "continue"

    def test_restart_on_very_low_coherence(self):
        signal = self._make_signal(0.1, drifting=["main goal"])
        report = {"uncertainty_count": 6, "uncertainty_flags": ["x","y","z","a","b","c"], "recent_revisions": []}
        event = self.mod_c.evaluate("drift output", report, signal)
        assert event.action == "restart"

    def test_audit_log_grows(self):
        signal = self._make_signal(0.5)
        report = {"uncertainty_count": 2, "uncertainty_flags": [], "recent_revisions": []}
        for _ in range(4):
            self.mod_c.evaluate("output", report, signal)
        assert len(self.mod_c.interrupt_log) == 4

    def test_summary_keys(self):
        signal = self._make_signal(0.7)
        report = {"uncertainty_count": 1, "uncertainty_flags": [], "recent_revisions": []}
        self.mod_c.evaluate("output", report, signal)
        summary = self.mod_c.summary()
        assert "total_interrupts" in summary
        assert "avg_coherence" in summary
