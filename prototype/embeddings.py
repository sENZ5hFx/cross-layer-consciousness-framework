# Copyright (c) 2026 Haley Ann Bird. All rights reserved.
# CLCE — Cross-Layer Consciousness Engine
"""
embeddings.py — Embedding backend with graceful fallback.

If sentence-transformers + torch are installed the real model is used.
Otherwise a deterministic pseudo-embedding (hash-seeded numpy) is returned
so every other subsystem can run without heavyweight ML deps in CI.
"""
from __future__ import annotations

import hashlib

import numpy as np

try:
    from sentence_transformers import SentenceTransformer as _ST
    _MODEL = _ST("all-MiniLM-L6-v2")
    _HAS_ST = True
except Exception:
    _MODEL = None
    _HAS_ST = False


def embed(text: str, dim: int = 128) -> np.ndarray:
    """Return a unit-normalised embedding vector for *text*.

    Real path  : sentence-transformers model (when available).
    Fallback   : deterministic hash-seeded random unit vector — always the
                 same for the same input string, safe for tests.
    """
    if _HAS_ST and _MODEL is not None:
        vec = _MODEL.encode(text, normalize_embeddings=True)
        if len(vec) != dim:
            # Resize: truncate or pad with zeros then re-normalise
            resized = np.zeros(dim)
            copy_len = min(len(vec), dim)
            resized[:copy_len] = vec[:copy_len]
            norm = np.linalg.norm(resized)
            return resized / norm if norm > 0 else resized
        return vec.astype(np.float32)

    # ── Deterministic fallback ────────────────────────────────────────────
    seed = int(hashlib.md5(text.encode()).hexdigest(), 16) % (2**32)
    rng = np.random.default_rng(seed)
    vec = rng.standard_normal(dim).astype(np.float32)
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec
