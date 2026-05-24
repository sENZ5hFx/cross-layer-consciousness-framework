"""
Tests for the embedding layer.
Always uses pseudo backend (no external dependencies required).
"""

import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from embeddings import embed, backend_info, _embed_pseudo


class TestEmbeddings:

    def test_pseudo_returns_unit_vector(self):
        vec = _embed_pseudo("hello world", 64)
        assert abs(np.linalg.norm(vec) - 1.0) < 1e-6

    def test_pseudo_is_deterministic(self):
        v1 = _embed_pseudo("test", 64)
        v2 = _embed_pseudo("test", 64)
        assert np.allclose(v1, v2)

    def test_pseudo_different_texts_differ(self):
        v1 = _embed_pseudo("cat", 64)
        v2 = _embed_pseudo("dog", 64)
        assert not np.allclose(v1, v2)

    def test_embed_returns_correct_shape(self):
        vec = embed("test text", dim=128)
        assert vec.shape == (128,)

    def test_embed_returns_unit_norm(self):
        vec = embed("normalize me", dim=64)
        assert abs(np.linalg.norm(vec) - 1.0) < 1e-5

    def test_backend_info_has_required_keys(self):
        info = backend_info()
        assert "active_backend" in info
        assert "upgrade_note" in info

    def test_embed_consistency_across_calls(self):
        v1 = embed("consistent", dim=32)
        v2 = embed("consistent", dim=32)
        assert np.allclose(v1, v2)
