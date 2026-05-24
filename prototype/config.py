# CLCE System Configuration

from pydantic import BaseModel
from typing import Optional


class SuperpositionConfig(BaseModel):
    """Configuration for Subsystem 1: Superposition Layer."""
    max_branches: int = 5                  # Max parallel interpretations to maintain
    min_branches: int = 2                  # Min branches before forced collapse
    collapse_confidence_threshold: float = 0.85  # Collapse when top branch exceeds this
    temporal_deadline_steps: int = 10      # Force collapse after N steps
    log_alternatives: bool = True          # Record what branches were held open


class HolographicConfig(BaseModel):
    """Configuration for Subsystem 2: Holographic Memory Matrix."""
    vector_dimensions: int = 10000         # HRR vector size (higher = less interference)
    memory_capacity: int = 1000            # Max stored memory traces
    retrieval_threshold: float = 0.3       # Minimum resonance score to return a memory
    graceful_degradation: bool = True      # Return partial match if no clean retrieval
    binding_method: str = "circular_conv"  # Options: circular_conv, element_multiply


class MetaCognitiveConfig(BaseModel):
    """Configuration for Subsystem 3: Meta-Cognitive Field."""
    # Module A: Awareness
    belief_update_log_size: int = 50       # How many recent belief updates to track
    uncertainty_flag_threshold: float = 0.4  # Flag as uncertain if confidence below this

    # Module B: Intention
    goal_hierarchy_depth: int = 3          # Top / mid / immediate goal levels
    goal_drift_threshold: float = 0.25     # Trigger re-alignment if drift exceeds this
    goal_persistence: bool = True          # Goals persist across conversation turns

    # Module C: Self-Reflection
    interrupt_enabled: bool = True         # Allow mid-processing interrupts
    reflection_log_size: int = 100         # Reflection event log depth
    restart_on_contradiction: bool = True  # Auto-restart if self-contradiction detected


class CLCEConfig(BaseModel):
    """Master CLCE system configuration."""
    superposition: SuperpositionConfig = SuperpositionConfig()
    holographic: HolographicConfig = HolographicConfig()
    metacognitive: MetaCognitiveConfig = MetaCognitiveConfig()
    verbose_logging: bool = True
    audit_trail: bool = True               # Full decision audit log
    openai_model: str = "gpt-4o-mini"      # Baseline LLM for superposition branches


# Default config
DEFAULT_CONFIG = CLCEConfig()
