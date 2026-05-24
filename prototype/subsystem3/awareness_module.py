"""
Subsystem 3, Module A: Awareness
QTTC excitation type: Awareness

Maintains a live internal state map:
  - Active beliefs (interpretations from S1)
  - Active memories (patterns from S2)
  - Unknown regions (flagged uncertainty)
  - Belief revision log (what was just changed)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class BeliefEntry:
    content: str
    confidence: float
    source: str  # 'subsystem1' | 'subsystem2' | 'external'
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class BeliefRevision:
    old_belief: str
    new_belief: str
    reason: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class AwarenessModule:
    """
    Module A — the live internal witness.
    Tracks what the system believes, remembers, doesn't know,
    and recently changed its mind about.
    """

    def __init__(self):
        self.active_beliefs: List[BeliefEntry] = []
        self.active_memories: List[str] = []
        self.uncertainty_flags: List[str] = []
        self.revision_log: List[BeliefRevision] = []

    def update_belief(self, content: str, confidence: float, source: str = "subsystem1") -> None:
        existing = next((b for b in self.active_beliefs if b.content == content), None)
        if existing:
            if abs(existing.confidence - confidence) > 0.05:
                self.revision_log.append(BeliefRevision(
                    old_belief=f"{content} @ {existing.confidence:.2f}",
                    new_belief=f"{content} @ {confidence:.2f}",
                    reason="confidence_update"
                ))
            existing.confidence = confidence
        else:
            self.active_beliefs.append(BeliefEntry(content=content, confidence=confidence, source=source))

    def flag_unknown(self, topic: str) -> None:
        if topic not in self.uncertainty_flags:
            self.uncertainty_flags.append(topic)

    def resolve_unknown(self, topic: str) -> None:
        self.uncertainty_flags = [t for t in self.uncertainty_flags if t != topic]

    def update_memory(self, memory_key: str) -> None:
        if memory_key not in self.active_memories:
            self.active_memories.append(memory_key)

    def record_revision(self, old_belief: str, new_belief: str, reason: str) -> None:
        self.revision_log.append(BeliefRevision(
            old_belief=old_belief, new_belief=new_belief, reason=reason
        ))

    def get_state_report(self) -> Dict[str, Any]:
        return {
            "active_beliefs": [{"content": b.content, "confidence": b.confidence} for b in self.active_beliefs],
            "active_memories": list(self.active_memories),
            "uncertainty_flags": list(self.uncertainty_flags),
            "recent_revisions": [
                {"old": r.old_belief, "new": r.new_belief, "reason": r.reason}
                for r in self.revision_log[-5:]
            ],
            "uncertainty_count": len(self.uncertainty_flags),
            "belief_count": len(self.active_beliefs)
        }

    def clear_session(self) -> None:
        """Reset transient state. Revision log is preserved."""
        self.active_beliefs = []
        self.active_memories = []
        self.uncertainty_flags = []
