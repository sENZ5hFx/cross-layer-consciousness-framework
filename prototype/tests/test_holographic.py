# Copyright (c) 2026 Haley Ann Bird. All rights reserved.
# CLCE — Cross-Layer Consciousness Engine
# Tests for Subsystem 2: Holographic Memory Matrix.

import numpy as np
import pytest

from subsystem2.holographic_memory import HolographicMemory, cosine_similarity


class TestHolographicMemory:

    def setup_method(self):
        self.mem = HolographicMemory(dim=512)

    # ─── encode / retrieve ─────────────────────────────────────────────────────

    def test_encode_updates_memory_norm(self):
        self.mem.encode("sky", "blue")
        state = self.mem.get_state()
        assert state["memory_norm"] > 0

    def test_encode_increments_trace_count(self):
        self.mem.encode("a", "alpha")
        self.mem.encode("b", "beta")
        assert self.mem.get_state()["num_traces"] == 2

    def test_retrieve_returns_list_of_tuples(self):
        self.mem.encode("ocean", "deep")
        results = self.mem.retrieve("ocean")
        assert isinstance(results, list)
        assert len(results) >= 1
        sim, val = results[0]
        assert isinstance(sim, float)

    def test_retrieve_top_match_is_correct_value(self):
        self.mem.encode("capital", "Paris")
        results = self.mem.retrieve("capital", top_k=1)
        _, val = results[0]
        assert val == "Paris"

    def test_retrieve_scores_bounded(self):
        self.mem.encode("test", "value")
        results = self.mem.retrieve("test")
        for sim, _ in results:
            assert -1.1 <= sim <= 1.1

    def test_retrieve_empty_memory_returns_empty(self):
        results = self.mem.retrieve("anything")
        assert results == []

    def test_retrieve_partial_returns_list(self):
        self.mem.encode("quantum", "entanglement")
        results = self.mem.retrieve_partial("quantum")
        assert isinstance(results, list)

    def test_multiple_encodes_accumulate_traces(self):
        for i in range(5):
            self.mem.encode(f"key_{i}", f"value_{i}")
        assert self.mem.get_state()["num_traces"] == 5

    def test_get_state_has_required_keys(self):
        state = self.mem.get_state()
        assert "num_traces" in state
        assert "memory_norm" in state
        assert "dim" in state

    def test_strength_param_accepted(self):
        self.mem.encode("strong", "signal", strength=2.0)
        assert self.mem.get_state()["num_traces"] == 1


class TestCosimeSimilarity:

    def test_identical_vectors_score_one(self):
        v = np.array([1.0, 0.0, 0.0])
        assert abs(cosine_similarity(v, v) - 1.0) < 1e-6

    def test_orthogonal_vectors_score_zero(self):
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 1.0])
        assert abs(cosine_similarity(a, b)) < 1e-6

    def test_zero_vector_doesnt_explode(self):
        a = np.zeros(4)
        b = np.ones(4)
        result = cosine_similarity(a, b)
        assert isinstance(result, float)
