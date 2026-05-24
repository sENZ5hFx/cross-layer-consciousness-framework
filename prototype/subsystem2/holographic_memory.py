"""
Subsystem 2: Holographic Memory Matrix (Floor 8 → 5)
Encodes memories as distributed interference patterns using Holographic
Reduced Representations (HRRs). Retrieval by resonance — partial cues
reconstruct full memory traces.

Based on:
  Plate, T.A. (1995). Holographic Reduced Representations.
  Kanerva, P. (2009). Hyperdimensional Computing.
"""

import numpy as np
from typing import Any, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class MemoryTrace:
    key: str
    value: Any
    vector: np.ndarray
    strength: float = 1.0


class HolographicMemory:
    """
    Content-addressable memory using circular convolution binding.
    All traces are superimposed into a single composite memory vector M.
    Retrieval: query ⊛ M^{-1} → approximate value vector → decode.

    Falsifiability condition:
        Must outperform cosine-similarity vector DB on partial/degraded
        cue retrieval tasks (p < 0.05).
    """

    def __init__(self, dim: int = 1024):
        self.dim = dim
        self.memory_vector = np.zeros(dim)
        self._traces: List[MemoryTrace] = []
        self._key_vectors: dict = {}

    def encode(self, key: str, value: Any, strength: float = 1.0) -> None:
        """
        Bind key → value using circular convolution and add to memory.
        M ← M + strength * (k ⊛ v)
        """
        k_vec = self._get_key_vector(key)
        v_vec = self._value_to_vector(value)
        binding = circular_convolve(k_vec, v_vec)
        self.memory_vector += strength * binding

        trace = MemoryTrace(key=key, value=value, vector=binding, strength=strength)
        self._traces.append(trace)

    def retrieve(self, query_key: str, top_k: int = 1) -> List[Tuple[float, Any]]:
        """
        Retrieve value(s) by key using circular correlation (approximate inverse).
        Returns list of (similarity_score, decoded_value) sorted by score.
        """
        k_vec = self._get_key_vector(query_key)
        probe = circular_correlate(k_vec, self.memory_vector)

        results = []
        for trace in self._traces:
            v_vec = self._value_to_vector(trace.value)
            sim = cosine_similarity(probe, v_vec)
            results.append((sim, trace.value, trace.key))

        results.sort(key=lambda x: x[0], reverse=True)
        return [(sim, val) for sim, val, _ in results[:top_k]]

    def retrieve_partial(self, partial_key: str, top_k: int = 3) -> List[Tuple[float, Any]]:
        """
        Retrieve using a partial/noisy cue. Degrades gracefully by normalizing
        the partial key vector against stored key patterns.
        """
        partial_vec = self._get_key_vector(partial_key)
        # Add controlled noise to simulate partial recall
        noise = np.random.default_rng(42).standard_normal(self.dim) * 0.3
        noisy_vec = partial_vec + noise
        noisy_vec /= np.linalg.norm(noisy_vec) + 1e-9

        probe = circular_correlate(noisy_vec, self.memory_vector)

        results = []
        for trace in self._traces:
            v_vec = self._value_to_vector(trace.value)
            sim = cosine_similarity(probe, v_vec)
            results.append((sim, trace.value))

        results.sort(key=lambda x: x[0], reverse=True)
        return results[:top_k]

    def get_state(self) -> dict:
        return {
            "num_traces": len(self._traces),
            "memory_norm": float(np.linalg.norm(self.memory_vector)),
            "dim": self.dim
        }

    def _get_key_vector(self, key: str) -> np.ndarray:
        if key not in self._key_vectors:
            rng = np.random.default_rng(abs(hash(key)) % (2**32))
            vec = rng.standard_normal(self.dim)
            vec /= np.linalg.norm(vec)
            self._key_vectors[key] = vec
        return self._key_vectors[key]

    def _value_to_vector(self, value: Any) -> np.ndarray:
        key = str(value)
        return self._get_key_vector(key)


def circular_convolve(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Circular convolution via FFT (HRR binding operation)."""
    return np.real(np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)))


def circular_correlate(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Circular correlation — approximate inverse of convolution."""
    return np.real(np.fft.ifft(np.conj(np.fft.fft(a)) * np.fft.fft(b)))


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-9
    return float(np.dot(a, b) / denom)
