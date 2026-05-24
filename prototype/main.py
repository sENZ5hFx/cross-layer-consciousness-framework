"""CLCE Entry Point — Cross-Layer Consciousness Engine."""

import sys
from loguru import logger
from config import DEFAULT_CONFIG, CLCEConfig
from subsystem1.superposition_layer import SuperpositionLayer
from subsystem2.holographic_memory import HolographicMemory
from subsystem3.awareness_module import AwarenessModule
from subsystem3.intention_module import IntentionModule
from subsystem3.reflection_module import ReflectionModule


class CLCE:
    """
    Cross-Layer Consciousness Engine.
    Integrates all three subsystems into a unified processing pipeline.
    """

    def __init__(self, config: CLCEConfig = DEFAULT_CONFIG):
        self.config = config
        logger.info("Initializing CLCE...")

        # Subsystem 1
        self.superposition = SuperpositionLayer(config.superposition)

        # Subsystem 2
        self.memory = HolographicMemory(config.holographic)

        # Subsystem 3
        self.awareness = AwarenessModule(config.metacognitive)
        self.intention = IntentionModule(config.metacognitive)
        self.reflection = ReflectionModule(
            config.metacognitive,
            awareness=self.awareness,
            intention=self.intention
        )

        logger.success("CLCE initialized. All subsystems online.")

    def process(self, input_text: str, context: dict = None) -> dict:
        """
        Full CLCE processing pipeline for a single input.

        Pipeline:
        1. Superposition layer generates N interpretations
        2. Each interpretation queries holographic memory
        3. Awareness module updates internal state map
        4. Intention module checks goal coherence
        5. Reflection module may interrupt and restart
        6. Superposition layer collapses to best interpretation
        7. Return response with full audit trail
        """
        context = context or {}
        logger.info(f"Processing input: {input_text[:80]}...")

        # Step 1: Generate branching interpretations
        branches = self.superposition.generate_branches(input_text, context)
        logger.debug(f"Generated {len(branches)} branches")

        # Step 2: Query holographic memory for each branch
        memory_landscapes = [
            self.memory.retrieve(branch["interpretation"])
            for branch in branches
        ]

        # Step 3: Update awareness state
        self.awareness.update(
            branches=branches,
            memory_landscapes=memory_landscapes,
            context=context
        )

        # Step 4: Check goal coherence
        coherence_signal = self.intention.check_coherence(
            branches=branches,
            awareness_state=self.awareness.get_state()
        )

        # Step 5: Reflection check — may interrupt and restart
        should_restart, restart_reason = self.reflection.evaluate(
            branches=branches,
            coherence_signal=coherence_signal,
            awareness_state=self.awareness.get_state()
        )

        if should_restart:
            logger.warning(f"Reflection interrupt: {restart_reason}. Restarting...")
            return self.process(input_text, {**context, "restart_reason": restart_reason})

        # Step 6: Collapse superposition to best interpretation
        result = self.superposition.collapse(
            branches=branches,
            memory_landscapes=memory_landscapes,
            coherence_signal=coherence_signal
        )

        # Step 7: Store this interaction in holographic memory
        self.memory.encode(
            experience={
                "input": input_text,
                "result": result,
                "awareness_state": self.awareness.get_state()
            }
        )

        return {
            "response": result["response"],
            "confidence": result["confidence"],
            "alternatives_held": [b["interpretation"] for b in branches if b != result["branch"]],
            "goal_coherence": coherence_signal["score"],
            "reflection_events": self.reflection.get_recent_events(n=3),
            "uncertainty_flags": self.awareness.get_uncertainty_flags()
        }


if __name__ == "__main__":
    engine = CLCE()

    # Example: ambiguous input to demonstrate superposition
    test_input = "The bank was steep and the current was strong."
    result = engine.process(test_input)

    print("\n=== CLCE Output ===")
    print(f"Response: {result['response']}")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Alternatives held open: {result['alternatives_held']}")
    print(f"Goal coherence: {result['goal_coherence']:.2f}")
    print(f"Uncertainty flags: {result['uncertainty_flags']}")
