# Copyright (c) 2026 Haley Ann Bird. All rights reserved.
# CLCE — Cross-Layer Consciousness Engine
# Tests for Subsystem 3: Meta-Cognitive Field (Awareness / Intention / Reflection).

import pytest

from subsystem3.awareness_module import AwarenessModule
from subsystem3.intention_module import IntentionModule, GoalLevel
from subsystem3.reflection_module import ReflectionModule


# ─── Fixtures ─────────────────────────────────────────────────────────────────────

@pytest.fixture
def awareness():
    return AwarenessModule()


@pytest.fixture
def intention():
    return IntentionModule()


@pytest.fixture
def reflection():
    return ReflectionModule()


# ─── AwarenessModule ────────────────────────────────────────────────────────────

class TestAwarenessModule:

    def test_update_belief_adds_entry(self, awareness):
        awareness.update_belief("sky is blue", 0.9)
        report = awareness.get_state_report()
        assert report["belief_count"] == 1

    def test_update_belief_same_content_updates_confidence(self, awareness):
        awareness.update_belief("hypothesis", 0.5)
        awareness.update_belief("hypothesis", 0.9)
        report = awareness.get_state_report()
        assert report["belief_count"] == 1
        assert report["active_beliefs"][0]["confidence"] == 0.9

    def test_update_belief_logs_revision_on_large_delta(self, awareness):
        awareness.update_belief("claim", 0.1)
        awareness.update_belief("claim", 0.9)
        report = awareness.get_state_report()
        assert len(report["recent_revisions"]) >= 1

    def test_flag_unknown_adds_to_flags(self, awareness):
        awareness.flag_unknown("dark matter")
        report = awareness.get_state_report()
        assert "dark matter" in report["uncertainty_flags"]
        assert report["uncertainty_count"] == 1

    def test_resolve_unknown_removes_flag(self, awareness):
        awareness.flag_unknown("topic")
        awareness.resolve_unknown("topic")
        assert awareness.get_state_report()["uncertainty_count"] == 0

    def test_update_memory_adds_key(self, awareness):
        awareness.update_memory("event_001")
        assert "event_001" in awareness.get_state_report()["active_memories"]

    def test_clear_session_resets_transient_state(self, awareness):
        awareness.update_belief("test", 0.8)
        awareness.flag_unknown("x")
        awareness.clear_session()
        report = awareness.get_state_report()
        assert report["belief_count"] == 0
        assert report["uncertainty_count"] == 0

    def test_get_state_report_keys(self, awareness):
        report = awareness.get_state_report()
        for key in ("active_beliefs", "active_memories", "uncertainty_flags",
                    "recent_revisions", "uncertainty_count", "belief_count"):
            assert key in report


# ─── IntentionModule ───────────────────────────────────────────────────────────

class TestIntentionModule:

    def test_set_goal_adds_to_hierarchy(self, intention):
        intention.set_goal("answer accurately", GoalLevel.TOP)
        hierarchy = intention.get_goal_hierarchy()
        assert "answer accurately" in hierarchy["top"]

    def test_duplicate_goal_not_added_twice(self, intention):
        intention.set_goal("stay coherent", GoalLevel.MID)
        intention.set_goal("stay coherent", GoalLevel.MID)
        hierarchy = intention.get_goal_hierarchy()
        assert hierarchy["mid"].count("stay coherent") == 1

    def test_deactivate_removes_from_hierarchy(self, intention):
        intention.set_goal("temporary", GoalLevel.IMMEDIATE)
        intention.deactivate_goal("temporary")
        hierarchy = intention.get_goal_hierarchy()
        assert "temporary" not in hierarchy["immediate"]

    def test_evaluate_coherence_returns_signal(self, intention):
        intention.set_goal("explain consciousness", GoalLevel.TOP)
        signal = intention.evaluate_coherence("consciousness is a field")
        assert 0.0 <= signal.score <= 1.0
        assert isinstance(signal.drifting_goals, list)
        assert isinstance(signal.resolution, str)

    def test_evaluate_coherence_detects_drift(self, intention):
        intention.set_goal("discuss quantum physics", GoalLevel.TOP)
        signal = intention.evaluate_coherence("the weather is nice today")
        assert len(signal.drifting_goals) >= 1

    def test_evaluate_coherence_no_goals_returns_perfect(self, intention):
        signal = intention.evaluate_coherence("anything at all")
        assert signal.score == 1.0

    def test_get_recent_signals(self, intention):
        intention.set_goal("g", GoalLevel.MID)
        intention.evaluate_coherence("some output")
        signals = intention.get_recent_signals(n=5)
        assert len(signals) >= 1


# ─── ReflectionModule ──────────────────────────────────────────────────────────

class TestReflectionModule:

    def _make_coherence_signal(self, score=0.8, drifting=None):
        from subsystem3.intention_module import CoherenceSignal
        return CoherenceSignal(
            score=score,
            drifting_goals=drifting or [],
            resolution="On track." if score >= 0.4 else "Reorient."
        )

    def _make_awareness_report(self, uncertainty_count=0, flags=None):
        return {
            "active_beliefs": [],
            "active_memories": [],
            "uncertainty_flags": flags or [],
            "recent_revisions": [],
            "uncertainty_count": uncertainty_count,
            "belief_count": 0,
        }

    def test_clean_state_returns_continue(self, reflection):
        signal = self._make_coherence_signal(score=0.9)
        report = self._make_awareness_report(uncertainty_count=0)
        event = reflection.evaluate("some output", report, signal)
        assert event.action == "continue"

    def test_low_coherence_triggers_reframe(self, reflection):
        signal = self._make_coherence_signal(score=0.25, drifting=["goal A"])
        report = self._make_awareness_report(uncertainty_count=1)
        event = reflection.evaluate("off-topic output", report, signal)
        assert event.action in ("reframe", "restart")

    def test_very_low_coherence_triggers_restart(self, reflection):
        signal = self._make_coherence_signal(score=0.1, drifting=["goal A", "goal B"])
        report = self._make_awareness_report(uncertainty_count=6)
        event = reflection.evaluate("chaotic output", report, signal)
        assert event.action == "restart"

    def test_evaluate_returns_interrupt_event(self, reflection):
        from subsystem3.reflection_module import InterruptEvent
        signal = self._make_coherence_signal(score=0.7)
        report = self._make_awareness_report()
        event = reflection.evaluate("output", report, signal)
        assert isinstance(event, InterruptEvent)

    def test_interrupt_log_accumulates(self, reflection):
        signal = self._make_coherence_signal()
        report = self._make_awareness_report()
        for _ in range(4):
            reflection.evaluate("output", report, signal)
        assert len(reflection.interrupt_log) == 4

    def test_get_audit_log_returns_list_of_dicts(self, reflection):
        signal = self._make_coherence_signal()
        report = self._make_awareness_report()
        reflection.evaluate("x", report, signal)
        log = reflection.get_audit_log()
        assert isinstance(log, list)
        assert "action" in log[0]
        assert "coherence" in log[0]

    def test_summary_counts_match_log(self, reflection):
        # 2 continues + 1 reframe
        for score in [0.9, 0.9, 0.25]:
            signal = self._make_coherence_signal(score=score, drifting=["g"] if score < 0.4 else [])
            report = self._make_awareness_report(uncertainty_count=1 if score < 0.4 else 0)
            reflection.evaluate("x", report, signal)
        s = reflection.summary()
        assert s["total_interrupts"] == 3
        assert s["continues"] == 2
