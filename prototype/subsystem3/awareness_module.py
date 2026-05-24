"""Subsystem 3, Module A: Awareness.

Maintains a continuously updated live internal state map:
- What the system currently believes (active branches)
- What it currently remembers (activated memory patterns)
- What it doesn't know (uncertainty flags)
- What it just changed its mind about (belief update log)

QTTC excitation type: Awareness.
"""

from typing import Dict, Any, List, Deque
from collections import deque
from loguru import logger
from config import MetaCognitiveConfig


class AwarenessModule:
    def __init__(self, config: MetaCognitiveConfig):
        self.config = config
        self._belief_state: Dict[str, Any] = {}
        self._uncertainty_flags: List[str] = []
        self._belief_update_log: Deque[Dict] = deque(maxlen=config.belief_update_log_size)
        logger.info("AwarenessModule initialized")

    def update(
        self,
        branches: List[Dict],
        memory_landscapes: List[Any],
        context: Dict[str, Any]
    ) -> None:
        """
        Update the internal state map based on current processing state.
        Called after every superposition + memory retrieval step.
        """
        # Record previous belief state for update log
        previous_state = dict(self._belief_state)

        # Update current beliefs from branches
        top_branch = max(branches, key=lambda b: b["confidence"])
        self._belief_state = {
            "top_interpretation": top_branch["interpretation"],
            "top_confidence": top_branch["confidence"],
            "n_active_branches": len(branches),
            "memory_resonance": memory_landscapes[0].get("resonance", 0.0) if memory_landscapes else 0.0,
            "context_keys": list(context.keys())
        }

        # Flag uncertainty if top confidence is below threshold
        self._uncertainty_flags = []
        if top_branch["confidence"] < self.config.uncertainty_flag_threshold:
            self._uncertainty_flags.append("low_confidence_top_branch")
        if any(m and m.get("degraded") for m in memory_landscapes):
            self._uncertainty_flags.append("degraded_memory_retrieval")

        # Log belief update if state changed
        if previous_state != self._belief_state:
            self._belief_update_log.append({
                "from": previous_state.get("top_interpretation", "[none]"),
                "to": self._belief_state["top_interpretation"],
                "confidence_delta": (
                    self._belief_state["top_confidence"] -
                    previous_state.get("top_confidence", 0.0)
                )
            })

        logger.debug(f"Awareness updated | Confidence: {top_branch['confidence']:.2f} | Flags: {self._uncertainty_flags}")

    def get_state(self) -> Dict[str, Any]:
        """Return current internal state map."""
        return {
            "belief_state": self._belief_state,
            "uncertainty_flags": self._uncertainty_flags,
            "recent_updates": list(self._belief_update_log)[-5:]
        }

    def get_uncertainty_flags(self) -> List[str]:
        return self._uncertainty_flags
