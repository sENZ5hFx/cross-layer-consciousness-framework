"""Subsystem 2: Holographic Memory Matrix.

Implements Holographic Reduced Representations (HRRs) for distributed,
associative, gracefully-degrading memory storage and retrieval.

Based on:
- Plate, T.A. (1995). Holographic Reduced Representations.
- Kanerva, P. (2009). Hyperdimensional Computing.
"""

import numpy as np
from typing import Dict, Any, List, Optional
from loguru import logger
from config import HolographicConfig


class HolographicMemory:
    def __init__(self, config: HolographicConfig):
        self.config = config
        self.D = config.vector_dimensions
        self._memory_traces: List[np.ndarray] = []   # Stored superposed vectors
        self._memory_labels: List[str] = []           # Human-readable labels
        self._cleanup_memory: Dict[str, np.ndarray] = {}  # For retrieval cleanup
        logger.info(f"HolographicMemory initialized: D={self.D}, capacity={config.memory_capacity}")

    def _random_vector(self) -> np.ndarray:
        """Generate a random bipolar unit vector in D-dimensional space."""
        return np.random.choice([-1, 1], size=self.D).astype(np.float32)

    def _bind(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Bind two vectors using circular convolution (HRR binding operation)."""
        if self.config.binding_method == "circular_conv":
            return np.real(np.fft.ifft(np.fft.fft(a) * np.fft.fft(b))).astype(np.float32)
        else:  # element_multiply
            return (a * b).astype(np.float32)

    def _superpose(self, vectors: List[np.ndarray]) -> np.ndarray:
        """Superpose (add) multiple vectors to create a composite memory trace."""
        return np.sum(vectors, axis=0).astype(np.float32)

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Measure resonance between two vectors."""
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def encode(self, experience: Dict[str, Any]) -> np.ndarray:
        """
        Encode an experience as a distributed vector trace and add to memory.
        The experience is NOT stored in a single slot — it is spread
        across the entire memory substrate as an interference pattern.
        """
        # Convert experience to a vector representation
        # In production: use sentence-transformers to embed text fields
        # Here: generate a reproducible random vector as a placeholder
        label = str(experience.get("input", ""))[:50]
        key_vector = self._random_vector()
        value_vector = self._random_vector()
        trace = self._bind(key_vector, value_vector)

        # Register in cleanup memory for future retrieval
        self._cleanup_memory[label] = key_vector

        # Superpose into the global memory substrate
        if len(self._memory_traces) >= self.config.memory_capacity:
            self._memory_traces.pop(0)
            self._memory_labels.pop(0)
            logger.debug("Memory capacity reached: oldest trace evicted")

        self._memory_traces.append(trace)
        self._memory_labels.append(label)
        logger.debug(f"Encoded experience: '{label[:30]}...' | Total traces: {len(self._memory_traces)}")
        return trace

    def retrieve(self, cue: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Retrieve memories by resonance with a cue.
        Gracefully degrades — partial or noisy cues still return best match.
        """
        if not self._memory_traces:
            return {"resonance": 0.0, "matches": [], "degraded": False}

        # Encode the cue as a vector
        # In production: use sentence-transformers embedding
        cue_vector = self._random_vector()  # Placeholder

        # Compute resonance with all stored traces
        scores = [
            self._cosine_similarity(cue_vector, trace)
            for trace in self._memory_traces
        ]

        # Sort by resonance
        ranked = sorted(zip(scores, self._memory_labels), reverse=True)
        top_matches = ranked[:top_k]
        best_score = top_matches[0][0] if top_matches else 0.0
        degraded = best_score < self.config.retrieval_threshold

        if degraded and not self.config.graceful_degradation:
            return {"resonance": 0.0, "matches": [], "degraded": True}

        logger.debug(f"Retrieved {len(top_matches)} matches | Best resonance: {best_score:.3f} | Degraded: {degraded}")
        return {
            "resonance": best_score,
            "matches": [{"label": label, "score": score} for score, label in top_matches],
            "degraded": degraded
        }
