# Copyright (c) 2026 Haley Ann Bird. All rights reserved.
# CLCE — Cross-Layer Consciousness Engine
"""
Tests for the embedding layer (embeddings.py).

Always exercises the pseudo backend in CI (sentence-transformers not in
requirements.txt).  All tests are deterministic and require no network access.
"""
from __future__ import annotations

import numpy as np
import pytest

from embeddings import _embed_pseudo, backend_info, embed


class TestPseudoEmbeddings:
    """Direct tests for _embed_pseudo — the deterministic fallback."""

    def test_returns_unit_vector(self):
        vec = _embed_pseudo("hello world", 64)
        assert abs(np.linalg.norm(vec) - 1.0) < 1e-6

    def test_is_deterministic(self):
        assert np.allclose(_embed_pseudo("test", 64), _embed_pseudo("test", 64))

    def test_different_texts_differ(self):
        assert not np.allclose(_embed_pseudo("cat", 64), _embed_pseudo("dog", 64))

    @pytest.mark.parametrize("dim", [32, 64, 128, 512])
    def test_correct_dim(self, dim):
        assert _embed_pseudo("x", dim).shape == (dim,)

    def test_empty_string_does_not_raise(self):
        vec = _embed_pseudo("", 64)
        assert vec.shape == (64,)
        assert abs(np.linalg.norm(vec) - 1.0) < 1e-6

    def test_float32_dtype(self):
        assert _embed_pseudo("dtype check", 32).dtype == np.float32


class TestEmbed:
    """Tests for the public embed() façade."""

    def test_returns_correct_shape(self):
        assert embed("test text", dim=128).shape == (128,)

    def test_returns_unit_norm(self):
        assert abs(np.linalg.norm(embed("normalize me", dim=64)) - 1.0) < 1e-5

    def test_consistent_across_calls(self):
        assert np.allclose(embed("consistent", dim=32), embed("consistent", dim=32))

    @pytest.mark.parametrize("dim", [16, 64, 256])
    def test_different_dims_produce_correct_shapes(self, dim):
        assert embed("dim test", dim=dim).shape == (dim,)

    def test_default_dim_matches_config(self):
        from config import EMBEDDING_DIM
        assert embed("default dim").shape == (EMBEDDING_DIM,)


class TestBackendInfo:
    """Tests for backend_info() metadata helper."""

    def test_has_required_keys(self):
        info = backend_info()
        for key in ("active_backend", "upgrade_note", "model"):
            assert key in info

    def test_active_backend_is_string(self):
        assert isinstance(backend_info()["active_backend"], str)

    def test_valid_backend_value(self):
        assert backend_info()["active_backend"] in ("pseudo", "sentence-transformers")

    def test_pseudo_has_none_model(self):
        info = backend_info()
        # In CI sentence-transformers is not installed, so model must be None.
        if info["active_backend"] == "pseudo":
            assert info["model"] is None

    def test_upgrade_note_is_nonempty_string(self):
        assert isinstance(backend_info()["upgrade_note"], str)
        assert len(backend_info()["upgrade_note"]) > 0
