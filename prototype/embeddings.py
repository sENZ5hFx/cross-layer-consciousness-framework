# Copyright (c) 2026 Haley Ann Bird. All rights reserved.
# CLCE — Cross-Layer Consciousness Engine
"""
embeddings.py — Embedding backend with graceful fallback.

If sentence-transformers + torch are installed the real model is used.
Otherwise a deterministic pseudo-embedding (hash-seeded numpy) is returned
so every other subsystem can run without heavyweight ML deps in CI.

Public API
----------
embed(text, dim)          -> np.ndarray   unit-normalised embedding
_embed_pseudo(text, dim)  -> np.ndarray   deterministic fallback (also used in tests)
backend_info()            -> dict         reports active_backend, model, upgrade_note
"""
from __future__ import annotations

import hashlib

import numpy as np

from config import EMBEDDING_DIM, SENTENCE_TRANSFORMER_MODEL

try:
    from sentence_transformers import SentenceTransformer as _ST
    _MODEL = _ST(SENTENCE_TRANSFORMER_MODEL)
    _HAS_ST = True
except Exception:  # noqa: BLE001
    _MODEL = None
    _HAS_ST = False


def _embed_pseudo(text: str, dim: int) -> np.ndarray:
    """Deterministic hash-seeded unit vector.  No external deps required.

    Identical inputs always produce identical outputs — safe for tests and CI.
    The MD5 hash is used purely as a non-cryptographic seed; security is not
    a concern here.
    """
    seed = int(hashlib.md5(text.encode()).hexdigest(), 16) % (2**32)  # noqa: S324
    rng = np.random.default_rng(seed)
    vec = rng.standard_normal(dim).astype(np.float32)
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec


def embed(text: str, dim: int = EMBEDDING_DIM) -> np.ndarray:
    """Return a unit-normalised embedding vector for *text*.

    Real path  : sentence-transformers model (when USE_SENTENCE_TRANSFORMERS
                 is True and the package is importable).
    Fallback   : _embed_pseudo — deterministic, always the same for the same
                 input string, zero external dependencies.
    """
    if _HAS_ST and _MODEL is not None:
        vec = _MODEL.encode(text, normalize_embeddings=True)
        if len(vec) != dim:
            resized = np.zeros(dim, dtype=np.float32)
            copy_len = min(len(vec), dim)
            resized[:copy_len] = vec[:copy_len]
            norm = np.linalg.norm(resized)
            return resized / norm if norm > 0 else resized
        return vec.astype(np.float32)
    return _embed_pseudo(text, dim)


def backend_info() -> dict:
    """Return metadata about the active embedding backend.

    Returns
    -------
    dict with keys:
        active_backend : str   — 'sentence-transformers' or 'pseudo'
        model          : str | None
        upgrade_note   : str
    """
    if _HAS_ST:
        return {
            "active_backend": "sentence-transformers",
            "model": SENTENCE_TRANSFORMER_MODEL,
            "upgrade_note": "Real semantic embeddings active.",
        }
    return {
        "active_backend": "pseudo",
        "model": None,
        "upgrade_note": (
            "Install sentence-transformers + torch to enable real embeddings. "
            "Then set USE_SENTENCE_TRANSFORMERS = True in config.py."
        ),
    }
