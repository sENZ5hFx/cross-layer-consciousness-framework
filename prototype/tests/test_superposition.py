# Copyright (c) 2026 Haley Ann Bird. All rights reserved.
# CLCE — Cross-Layer Consciousness Engine
# Tests for Subsystem 1: Superposition Layer.

import numpy as np
import pytest

from subsystem1.superposition_layer import SuperpositionLayer, Interpretation, CollapseResult


class TestSuperpositionLayer:

    def setup_method(self):
        self.s1 = SuperpositionLayer(min_branches=3)

    # ─── load ────────────────────────────────────────────────────────────────────

    def test_load_normalises_weights(self):
        self.s1.load([("A", 1.0), ("B", 3.0), ("C", 6.0)])
        total = sum(b.weight for b in self.s1._active_branches)
        assert abs(total - 1.0) < 1e-6

    def test_load_zero_weight_raises(self):
        with pytest.raises(ValueError):
            self.s1.load([("A", 0.0), ("B", 0.0)])

    def test_observe_before_load_raises(self):
        with pytest.raises(RuntimeError):
            self.s1.observe()

    # ─── observe / collapse ──────────────────────────────────────────────────────

    def test_collapse_selects_highest_weight(self):
        self.s1.load([("Paris", 0.6), ("London", 0.3), ("Berlin", 0.1)])
        result = self.s1.observe()
        assert result.selected.text == "Paris"

    def test_alternatives_contain_remaining(self):
        self.s1.load([("X", 0.5), ("Y", 0.3), ("Z", 0.2)])
        result = self.s1.observe()
        alt_texts = {a.text for a in result.alternatives}
        assert "Y" in alt_texts
        assert "Z" in alt_texts

    def test_confidence_is_bounded(self):
        self.s1.load([("A", 0.8), ("B", 0.2)])
        result = self.s1.observe()
        assert 0.0 <= result.confidence <= 1.0

    def test_collapse_reason_without_context(self):
        self.s1.load([("A", 0.7), ("B", 0.3)])
        result = self.s1.observe()
        assert result.collapse_reason == "deadline"

    def test_collapse_reason_with_context(self):
        self.s1.load([("quantum", 0.4), ("classical", 0.4), ("random", 0.2)])
        ctx = np.zeros(64)
        ctx[0] = 1.0
        result = self.s1.observe(context_vector=ctx)
        assert result.collapse_reason == "context_signal"

    def test_active_branches_cleared_after_collapse(self):
        self.s1.load([("A", 0.6), ("B", 0.4)])
        self.s1.observe()
        assert self.s1._active_branches == []

    def test_collapse_log_grows(self):
        for _ in range(3):
            self.s1.load([("A", 0.6), ("B", 0.4)])
            self.s1.observe()
        assert len(self.s1.get_collapse_log()) == 3

    # ─── state ────────────────────────────────────────────────────────────────────

    def test_get_state_keys(self):
        state = self.s1.get_state()
        assert "active_branches" in state
        assert "total_collapses" in state

    def test_interpretation_is_dataclass(self):
        interp = Interpretation(text="test", weight=0.5)
        assert interp.text == "test"
        assert interp.weight == 0.5
