"""Tests for Subsystem 2: Holographic Memory Matrix."""

import pytest
from subsystem2.holographic_memory import HolographicMemory
from config import HolographicConfig


@pytest.fixture
def memory():
    return HolographicMemory(HolographicConfig(vector_dimensions=1000, memory_capacity=50))


def test_encode_returns_vector(memory):
    trace = memory.encode({"input": "The sky is blue", "result": {}})
    assert trace.shape == (1000,)


def test_retrieve_returns_dict_with_required_keys(memory):
    memory.encode({"input": "Test experience", "result": {}})
    result = memory.retrieve("Test")
    assert "resonance" in result
    assert "matches" in result
    assert "degraded" in result


def test_graceful_degradation_on_empty_memory(memory):
    result = memory.retrieve("anything")
    assert result["resonance"] == 0.0
    assert result["matches"] == []


def test_memory_capacity_eviction(memory):
    for i in range(60):  # Exceeds capacity of 50
        memory.encode({"input": f"Experience {i}", "result": {}})
    assert len(memory._memory_traces) <= 50
