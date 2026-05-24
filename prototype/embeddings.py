"""
Embedding layer for CLCE.

Priority order:
  1. sentence-transformers (MiniLM-L6-v2) — if installed
  2. OpenAI text-embedding-3-small — if OPENAI_API_KEY set
  3. Pseudo-embedding fallback (deterministic hash-based)

All paths return a unit-norm numpy float64 array of shape (dim,).
The dim parameter is only respected by the pseudo backend;
real backends project to a fixed native dim and then pad/truncate.
"""

from __future__ import annotations
import os
import hashlib
import numpy as np
from typing import Optional

_BACKEND: Optional[str] = None
_SBERT_MODEL = None


def _detect_backend() -> str:
    global _BACKEND, _SBERT_MODEL
    if _BACKEND:
        return _BACKEND
    try:
        from sentence_transformers import SentenceTransformer
        _SBERT_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
        _BACKEND = "sbert"
        return _BACKEND
    except ImportError:
        pass
    if os.environ.get("OPENAI_API_KEY"):
        _BACKEND = "openai"
        return _BACKEND
    _BACKEND = "pseudo"
    return _BACKEND


def embed(text: str, dim: int = 128) -> np.ndarray:
    """
    Embed text to a unit-norm numpy float64 vector.
    dim is respected only by the pseudo backend.
    """
    backend = _detect_backend()
    if backend == "sbert":
        return _embed_sbert(text, dim)
    elif backend == "openai":
        return _embed_openai(text, dim)
    else:
        return _embed_pseudo(text, dim)


def _embed_sbert(text: str, target_dim: int) -> np.ndarray:
    vec = _SBERT_MODEL.encode(text, normalize_embeddings=True)
    vec = np.array(vec, dtype=np.float64)
    return _resize(vec, target_dim)


def _embed_openai(text: str, target_dim: int) -> np.ndarray:
    import openai
    resp = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text,
        dimensions=target_dim
    )
    vec = np.array(resp.data[0].embedding, dtype=np.float64)
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec


def _embed_pseudo(text: str, dim: int) -> np.ndarray:
    """Deterministic hash-based pseudo-embedding. Stable across runs."""
    h = int(hashlib.sha256(text.encode()).hexdigest(), 16)
    rng = np.random.default_rng(h % (2**32))
    vec = rng.standard_normal(dim).astype(np.float64)
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec


def _resize(vec: np.ndarray, target_dim: int) -> np.ndarray:
    """Pad with zeros or truncate to target_dim, then renormalize."""
    current_dim = len(vec)
    if current_dim == target_dim:
        return vec
    elif current_dim > target_dim:
        vec = vec[:target_dim]
    else:
        vec = np.concatenate([vec, np.zeros(target_dim - current_dim)])
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec


def backend_info() -> dict:
    backend = _detect_backend()
    return {
        "active_backend": backend,
        "sbert_available": backend == "sbert",
        "openai_available": backend == "openai",
        "pseudo_fallback": backend == "pseudo",
        "upgrade_note": (
            "Install sentence-transformers for real semantic embeddings: "
            "pip install sentence-transformers"
        ) if backend == "pseudo" else "Real embeddings active."
    }
