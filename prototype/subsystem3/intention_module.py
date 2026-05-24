"""
Subsystem 3, Module B: Intention
QTTC excitation type: Intention

Maintains a persistent goal hierarchy that does NOT reset between sessions.
Monitors goal coherence and issues resolution signals when drift is detected.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


class GoalLevel(Enum):
    TOP = "top"
    MID = "mid"
    IMMEDIATE = "immediate"


@dataclass
class Goal:
    description: str
    level: GoalLevel
    active: bool = True
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class CoherenceSignal:
    score: float  # 0.0 = full drift, 1.0 = fully coherent
    drifting_goals: List[str]
    resolution: str  # human-readable instruction to Subsystem 1
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class IntentionModule:
    """
    Module B — the persistent goal-keeper.
    Issues coherence signals to Subsystem 1 when processing drifts from goals.
    Persists across sessions (goals are not reset on clear_session).
    """

    def __init__(self):
        self.goals: List[Goal] = []
        self.coherence_signals: List[CoherenceSignal] = []

    def set_goal(self, description: str, level: GoalLevel) -> None:
        existing = next((g for g in self.goals if g.description == description), None)
        if not existing:
            self.goals.append(Goal(description=description, level=level))

    def deactivate_goal(self, description: str) -> None:
        for g in self.goals:
            if g.description == description:
                g.active = False

    def evaluate_coherence(self, current_output: str) -> CoherenceSignal:
        """
        Evaluate whether current_output is aligned with active goals.
        Simple keyword overlap scoring — replace with semantic similarity in Phase 4.
        """
        active_goals = [g for g in self.goals if g.active]
        if not active_goals:
            return CoherenceSignal(score=1.0, drifting_goals=[], resolution="No active goals.")

        output_lower = current_output.lower()
        drifting = []
        scores = []
        for goal in active_goals:
            keywords = set(goal.description.lower().split())
            overlap = sum(1 for kw in keywords if kw in output_lower)
            score = overlap / max(len(keywords), 1)
            scores.append(score)
            if score < 0.3:
                drifting.append(goal.description)

        coherence = float(sum(scores) / len(scores))
        resolution = "Reorient toward: " + "; ".join(drifting) if drifting else "On track."

        signal = CoherenceSignal(
            score=coherence,
            drifting_goals=drifting,
            resolution=resolution
        )
        self.coherence_signals.append(signal)
        return signal

    def get_goal_hierarchy(self) -> Dict:
        return {
            level.value: [g.description for g in self.goals if g.level == level and g.active]
            for level in GoalLevel
        }

    def get_recent_signals(self, n: int = 5) -> List[CoherenceSignal]:
        return self.coherence_signals[-n:]
