"""Tests for Subsystem 1: Superposition Layer."""

import pytest
from subsystem1.superposition_layer import SuperpositionLayer
from config import SuperpositionConfig


@pytest.fixture
def layer():
    return SuperpositionLayer(SuperpositionConfig(max_branches=5))


def test_generates_correct_number_of_branches(layer):
    branches = layer.generate_branches("The bank was steep.", {})
    assert len(branches) == 5


def test_each_branch_has_required_fields(layer):
    branches = layer.generate_branches("Test input.", {})
    for branch in branches:
        assert "id" in branch
        assert "interpretation" in branch
        assert "confidence" in branch
        assert "weight" in branch


def test_collapse_returns_best_branch(layer):
    branches = layer.generate_branches("Ambiguous input.", {})
    memory_landscapes = [{"resonance": 0.5}] * len(branches)
    coherence_signal = {"score": 0.7}
    result = layer.collapse(branches, memory_landscapes, coherence_signal)
    assert "response" in result
    assert "confidence" in result
    assert 0.0 <= result["confidence"] <= 1.0


def test_temporal_deadline_forces_collapse(layer):
    layer._step_counter = layer.config.temporal_deadline_steps
    should_force, reason = layer.should_force_collapse()
    assert should_force is True
    assert reason == "temporal_deadline_reached"
