"""
Subsystem 3, Module C: Self-Reflection
QTTC excitation type: Self-reflection

The system's interrupt mechanism. Can pause processing, query state,
and issue restart-with-different-framing instructions.
Logs every interruption for post-hoc audit.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Callable, Any
from datetime import datetime


@dataclass
class InterruptEvent:
    trigger: str  # What caused the interrupt
    belief_state_snapshot: dict
    goal_coherence_score: float
    action: str  # 'continue' | 'restart' | 'reframe'
    reframe_instruction: Optional[str]
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class ReflectionModule:
    """
    Module C — the internal witness and interrupt.
    Pauses processing, queries Modules A and B, decides: continue, restart, or reframe.

    Falsifiability condition:
        Systems with Module C must show statistically fewer goal-drift
        events and self-contradictions than chain-of-thought baselines.
    """

    INTERRUPT_THRESHOLD = 0.4  # coherence below this triggers interrupt
    RESTART_THRESHOLD = 0.2    # coherence below this triggers full restart

    def __init__(self):
        self.interrupt_log: List[InterruptEvent] = []
        self._paused: bool = False

    def evaluate(
        self,
        current_output: str,
        awareness_report: dict,
        coherence_signal,
    ) -> InterruptEvent:
        """
        Core evaluation loop. Called after each processing step.
        Returns an InterruptEvent describing the action taken.
        """
        score = coherence_signal.score
        uncertainty_count = awareness_report.get("uncertainty_count", 0)

        if score >= self.INTERRUPT_THRESHOLD and uncertainty_count < 3:
            action = "continue"
            reframe = None
        elif score < self.RESTART_THRESHOLD or uncertainty_count >= 5:
            action = "restart"
            reframe = self._generate_reframe(coherence_signal, awareness_report)
        else:
            action = "reframe"
            reframe = self._generate_reframe(coherence_signal, awareness_report)

        event = InterruptEvent(
            trigger=f"coherence={score:.2f}, uncertainty={uncertainty_count}",
            belief_state_snapshot=awareness_report,
            goal_coherence_score=score,
            action=action,
            reframe_instruction=reframe
        )
        self.interrupt_log.append(event)
        return event

    def _generate_reframe(self, coherence_signal, awareness_report: dict) -> str:
        parts = []
        if coherence_signal.drifting_goals:
            parts.append(f"Realign with: {', '.join(coherence_signal.drifting_goals)}")
        unknowns = awareness_report.get("uncertainty_flags", [])
        if unknowns:
            parts.append(f"Resolve unknowns first: {', '.join(unknowns[:3])}")
        recent = awareness_report.get("recent_revisions", [])
        if recent:
            parts.append(f"Note recent belief change: {recent[-1].get('new', '')}")
        return " | ".join(parts) if parts else "Restart with broader framing."

    def get_audit_log(self) -> List[dict]:
        return [
            {
                "timestamp": e.timestamp,
                "trigger": e.trigger,
                "action": e.action,
                "coherence": e.goal_coherence_score,
                "reframe": e.reframe_instruction
            }
            for e in self.interrupt_log
        ]

    def summary(self) -> dict:
        total = len(self.interrupt_log)
        if total == 0:
            return {"total_interrupts": 0, "continues": 0, "reframes": 0, "restarts": 0}
        return {
            "total_interrupts": total,
            "continues": sum(1 for e in self.interrupt_log if e.action == "continue"),
            "reframes": sum(1 for e in self.interrupt_log if e.action == "reframe"),
            "restarts": sum(1 for e in self.interrupt_log if e.action == "restart"),
            "avg_coherence": sum(e.goal_coherence_score for e in self.interrupt_log) / total
        }
