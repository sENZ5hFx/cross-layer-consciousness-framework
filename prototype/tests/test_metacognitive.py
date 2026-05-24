"""Tests for Subsystem 3: Meta-Cognitive Field."""

import pytest
from subsystem3.awareness_module import AwarenessModule
from subsystem3.intention_module import IntentionModule
from subsystem3.reflection_module import ReflectionModule
from config import MetaCognitiveConfig


@pytest.fixture
def config():
    return MetaCognitiveConfig()


@pytest.fixture
def awareness(config):
    return AwarenessModule(config)


@pytest.fixture
def intention(config):
    return IntentionModule(config)


@pytest.fixture
def reflection(config, awareness, intention):
    return ReflectionModule(config, awareness, intention)


def test_awareness_update_sets_belief_state(awareness):
    branches = [{"interpretation": "Test", "confidence": 0.8}]
    memory_landscapes = [{"resonance": 0.6, "degraded": False}]
    awareness.update(branches, memory_landscapes, {})
    state = awareness.get_state()
    assert "belief_state" in state
    assert state["belief_state"]["top_confidence"] == 0.8


def test_awareness_flags_low_confidence(awareness):
    branches = [{"interpretation": "Uncertain", "confidence": 0.2}]  # Below threshold
    awareness.update(branches, [{"resonance": 0.5, "degraded": False}], {})
    assert "low_confidence_top_branch" in awareness.get_uncertainty_flags()


def test_intention_goal_persistence(intention):
    intention.set_top_goal("Understand consciousness")
    signal = intention.check_coherence(
        branches=[{"interpretation": "Test", "confidence": 0.8}],
        awareness_state={"uncertainty_flags": []}
    )
    assert signal["score"] > 0
    assert "Understand consciousness" in signal["active_goals"]


def test_reflection_triggers_on_goal_drift(config, awareness, intention, reflection):
    coherence_signal = {"score": 0.3, "status": "drifting"}
    awareness_state = {"uncertainty_flags": [], "recent_updates": []}
    branches = [{"interpretation": "Test", "confidence": 0.8}]
    should_restart, reason = reflection.evaluate(branches, coherence_signal, awareness_state)
    assert should_restart is True
    assert "goal_drift_detected" in reason


def test_reflection_no_interrupt_on_clean_state(config, awareness, intention, reflection):
    coherence_signal = {"score": 0.85, "status": "coherent"}
    awareness_state = {"uncertainty_flags": [], "recent_updates": []}
    branches = [{"interpretation": "Test", "confidence": 0.8}]
    should_restart, reason = reflection.evaluate(branches, coherence_signal, awareness_state)
    assert should_restart is False
