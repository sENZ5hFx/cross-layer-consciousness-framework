"""Subsystem 3, Module C: Self-Reflection.

The system's interrupt mechanism.
Can pause Subsystems 1 and 2, query Modules A and B,
and issue restart instructions with logged reasons.

QTTC excitation type: Self-reflection.
"""

from typing import Dict, Any, List, Tuple
from collections import deque
from loguru import logger
from config import MetaCognitiveConfig
from subsystem3.awareness_module import AwarenessModule
from subsystem3.intention_module import IntentionModule


class ReflectionEvent:
    def __init__(self, reason: str, action: str, awareness_snapshot: Dict, coherence_score: float):
        self.reason = reason
        self.action = action
        self.awareness_snapshot = awareness_snapshot
        self.coherence_score = coherence_score

    def __repr__(self):
        return f"ReflectionEvent(reason='{self.reason}', action='{self.action}', coherence={self.coherence_score:.2f})"


class ReflectionModule:
    def __init__(
        self,
        config: MetaCognitiveConfig,
        awareness: AwarenessModule,
        intention: IntentionModule
    ):
        self.config = config
        self.awareness = awareness
        self.intention = intention
        self._reflection_log: deque = deque(maxlen=config.reflection_log_size)
        logger.info("ReflectionModule initialized")

    def evaluate(
        self,
        branches: List[Dict],
        coherence_signal: Dict[str, Any],
        awareness_state: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """
        Evaluate whether to interrupt processing.
        Returns (should_restart: bool, reason: str).
        """
        if not self.config.interrupt_enabled:
            return False, ""

        reasons_to_interrupt = []

        # Check 1: Goal drift
        if coherence_signal.get("status") == "drifting":
            reasons_to_interrupt.append("goal_drift_detected")

        # Check 2: All branches have low confidence
        if all(b["confidence"] < 0.35 for b in branches):
            reasons_to_interrupt.append("all_branches_low_confidence")

        # Check 3: Self-contradiction in belief update log
        recent_updates = awareness_state.get("recent_updates", [])
        if self.config.restart_on_contradiction and len(recent_updates) >= 2:
            last_two = recent_updates[-2:]
            if last_two[0]["to"] == last_two[1]["from"] and last_two[1]["to"] == last_two[0]["from"]:
                reasons_to_interrupt.append("belief_oscillation_detected")

        if reasons_to_interrupt:
            reason_str = " | ".join(reasons_to_interrupt)
            event = ReflectionEvent(
                reason=reason_str,
                action="restart",
                awareness_snapshot=awareness_state,
                coherence_score=coherence_signal.get("score", 0.0)
            )
            self._reflection_log.append(event)
            logger.warning(f"Reflection interrupt triggered: {reason_str}")
            return True, reason_str

        return False, ""

    def get_recent_events(self, n: int = 5) -> List[str]:
        """Return the N most recent reflection events as strings."""
        return [repr(e) for e in list(self._reflection_log)[-n:]]
