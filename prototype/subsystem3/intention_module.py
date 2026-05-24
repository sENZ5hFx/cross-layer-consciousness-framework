"""Subsystem 3, Module B: Intention.

Maintains a persistent goal hierarchy that does not reset between contexts.
Monitors whether current processing is goal-coherent.
Issues goal-coherence resolution signals to Subsystem 1.

QTTC excitation type: Intention.
"""

from typing import Dict, Any, List, Optional
from loguru import logger
from config import MetaCognitiveConfig


class GoalNode:
    def __init__(self, label: str, level: int, parent: Optional["GoalNode"] = None):
        self.label = label
        self.level = level  # 0=top, 1=mid, 2=immediate
        self.parent = parent
        self.active = True
        self.coherence_history: List[float] = []

    def __repr__(self):
        return f"GoalNode(level={self.level}, label='{self.label}', active={self.active})"


class IntentionModule:
    def __init__(self, config: MetaCognitiveConfig):
        self.config = config
        self._goal_hierarchy: List[GoalNode] = []
        self._coherence_log: List[Dict] = []
        logger.info("IntentionModule initialized")

    def set_top_goal(self, label: str) -> GoalNode:
        """Set or update the top-level goal. Persists across all interactions."""
        node = GoalNode(label=label, level=0)
        # Replace any existing top-level goal
        self._goal_hierarchy = [g for g in self._goal_hierarchy if g.level != 0]
        self._goal_hierarchy.insert(0, node)
        logger.info(f"Top goal set: '{label}'")
        return node

    def add_subgoal(self, label: str, level: int = 1) -> GoalNode:
        """Add a mid-level or immediate subgoal."""
        parent = next((g for g in self._goal_hierarchy if g.level == level - 1), None)
        node = GoalNode(label=label, level=level, parent=parent)
        self._goal_hierarchy.append(node)
        logger.debug(f"Subgoal added at level {level}: '{label}'")
        return node

    def check_coherence(
        self,
        branches: List[Dict],
        awareness_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check whether current processing branches are coherent with active goals.
        Returns a coherence signal with score and recommendation.
        """
        if not self._goal_hierarchy:
            # No goals set — return neutral coherence
            return {"score": 0.5, "status": "no_goals_set", "recommendation": "continue"}

        active_goals = [g for g in self._goal_hierarchy if g.active]
        top_goal = next((g for g in active_goals if g.level == 0), None)

        # Simplified coherence check:
        # In production, use semantic similarity between branch interpretations and goal labels
        # Here: check if uncertainty flags suggest drift
        uncertainty_flags = awareness_state.get("uncertainty_flags", [])
        base_score = 0.75
        if "low_confidence_top_branch" in uncertainty_flags:
            base_score -= 0.2
        if "degraded_memory_retrieval" in uncertainty_flags:
            base_score -= 0.1

        status = "coherent" if base_score >= self.config.goal_drift_threshold + 0.5 else "drifting"
        recommendation = "continue" if status == "coherent" else "re_align"

        # Log coherence event
        self._coherence_log.append({"score": base_score, "status": status})
        if top_goal:
            top_goal.coherence_history.append(base_score)

        logger.debug(f"Goal coherence: {base_score:.2f} ({status})")
        return {
            "score": base_score,
            "status": status,
            "recommendation": recommendation,
            "active_goals": [g.label for g in active_goals]
        }

    def get_goal_state(self) -> List[Dict]:
        return [{"label": g.label, "level": g.level, "active": g.active} for g in self._goal_hierarchy]
