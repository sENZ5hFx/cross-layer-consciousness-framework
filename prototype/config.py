# Copyright (c) 2026 Haley Ann Bird. All rights reserved.
# CLCE — Cross-Layer Consciousness Engine
"""
config.py — Global configuration constants for the CLCE prototype.
"""
from __future__ import annotations

# ── Embedding ────────────────────────────────────────────────────────────────
EMBEDDING_DIM: int = 128          # dimension for pseudo-embeddings
USE_SENTENCE_TRANSFORMERS: bool = False  # flip to True once torch is available
SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"

# ── Holographic Memory ───────────────────────────────────────────────────────
MEMORY_DIM: int = 512
MEMORY_TOP_K: int = 3

# ── Superposition / Collapse ─────────────────────────────────────────────────
MIN_BRANCHES: int = 3
MAX_BRANCHES: int = 8

# ── Orchestrator ─────────────────────────────────────────────────────────────
MAX_ITERATIONS: int = 3

# ── Logging ──────────────────────────────────────────────────────────────────
LOG_LEVEL: str = "INFO"
