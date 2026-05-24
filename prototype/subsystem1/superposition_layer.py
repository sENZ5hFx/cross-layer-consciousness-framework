"""
Subsystem 1: Superposition Layer (Floor 1 → 4)
Holds N competing interpretations open in parallel and delays collapse
until a contextual resolution signal forces a decision.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class Interpretation:
    text: str
    weight: float  # amplitude α_i
    metadata: dict = field(default_factory=dict)


@dataclass
class CollapseResult:
    selected: Interpretation
    alternatives: List[Interpretation]
    confidence: float
    collapse_reason: str  # 'context_signal' | 'goal_coherence' | 'deadline'


class SuperpositionLayer:
    """
    Maintains a superposition of N interpretations and collapses to the
    highest-weighted branch when a resolution trigger fires.
    
    Falsifiability condition:
        Must outperform a temperature-sampled ensemble baseline on
        controlled ambiguity tasks (p < 0.05).
    """

    def __init__(self, min_branches: int = 3, max_branches: int = 8):
        self.min_branches = min_branches
        self.max_branches = max_branches
        self._active_branches: List[Interpretation] = []
        self._collapse_log: List[CollapseResult] = []

    def load(self, candidates: List[Tuple[str, float]]) -> None:
        """
        Load N candidate interpretations with relevance weights.
        candidates: list of (text, weight) tuples, weights need not sum to 1.
        """
        total = sum(w for _, w in candidates)
        if total == 0:
            raise ValueError("At least one candidate must have non-zero weight.")
        self._active_branches = [
            Interpretation(text=t, weight=w / total)
            for t, w in candidates
        ]
        self._active_branches.sort(key=lambda x: x.weight, reverse=True)

    def observe(self, context_vector: Optional[np.ndarray] = None) -> CollapseResult:
        """
        Collapse the superposition to the winning interpretation.
        If a context_vector is provided, re-weight branches by cosine similarity
        before collapsing. Otherwise collapses on current weights.
        """
        if not self._active_branches:
            raise RuntimeError("No branches loaded. Call load() first.")

        if context_vector is not None:
            self._reweight_by_context(context_vector)

        winner = self._active_branches[0]
        alternatives = self._active_branches[1:]
        confidence = winner.weight / (winner.weight + sum(b.weight for b in alternatives) + 1e-9)
        reason = "context_signal" if context_vector is not None else "deadline"

        result = CollapseResult(
            selected=winner,
            alternatives=alternatives,
            confidence=confidence,
            collapse_reason=reason
        )
        self._collapse_log.append(result)
        self._active_branches = []
        return result

    def _reweight_by_context(self, context_vector: np.ndarray) -> None:
        """Reweight branches using cosine similarity to context vector."""
        ctx_norm = np.linalg.norm(context_vector)
        if ctx_norm == 0:
            return
        ctx_unit = context_vector / ctx_norm
        for branch in self._active_branches:
            # Embed text as a simple hash-based pseudo-vector (swap for real embeddings in Phase 4)
            branch_vec = _pseudo_embed(branch.text, len(context_vector))
            sim = float(np.dot(ctx_unit, branch_vec))
            branch.weight *= max(0.0, sim + 1.0)  # shift to [0, 2]

        total = sum(b.weight for b in self._active_branches)
        if total > 0:
            for b in self._active_branches:
                b.weight /= total
        self._active_branches.sort(key=lambda x: x.weight, reverse=True)

    def get_state(self) -> dict:
        return {
            "active_branches": len(self._active_branches),
            "branch_weights": [b.weight for b in self._active_branches],
            "total_collapses": len(self._collapse_log)
        }

    def get_collapse_log(self) -> List[CollapseResult]:
        return list(self._collapse_log)


def _pseudo_embed(text: str, dim: int) -> np.ndarray:
    """Deterministic pseudo-embedding. Replace with sentence-transformers in Phase 4."""
    rng = np.random.default_rng(abs(hash(text)) % (2**32))
    vec = rng.standard_normal(dim)
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec
