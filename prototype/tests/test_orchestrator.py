"""
Integration tests for the CLCEOrchestrator.
Run with: pytest prototype/tests/test_orchestrator.py -v
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator import CLCEOrchestrator
from subsystem3.intention_module import GoalLevel


class TestOrchestrator:

    def setup_method(self):
        self.orc = CLCEOrchestrator(
            memory_dim=256,
            embedding_dim=64,
            top_goals=["answer accurately", "stay coherent"]
        )

    def test_basic_process_returns_result(self):
        result = self.orc.process("What is consciousness?")
        assert result.output
        assert result.selected_interpretation
        assert 0.0 <= result.confidence <= 1.0

    def test_coherence_score_bounded(self):
        result = self.orc.process("Explain holographic memory")
        assert 0.0 <= result.coherence_score <= 1.0

    def test_reflection_action_valid(self):
        result = self.orc.process("some input text")
        assert result.reflection_action in ("continue", "reframe", "restart")

    def test_elapsed_time_positive(self):
        result = self.orc.process("test")
        assert result.elapsed_s > 0

    def test_memory_populated_after_process(self):
        self.orc.process("memory test query")
        state = self.orc.s2.get_state()
        assert state["num_traces"] > 0

    def test_multi_turn_belief_accumulation(self):
        for q in ["first query", "second query", "third query"]:
            self.orc.process(q)
        report = self.orc.mod_a.get_state_report()
        assert report["belief_count"] >= 1

    def test_session_summary_keys(self):
        self.orc.process("summary test")
        summary = self.orc.get_session_summary()
        assert "memory_state" in summary
        assert "reflection_summary" in summary
        assert "goal_hierarchy" in summary

    def test_goal_can_be_added(self):
        self.orc.mod_b.set_goal("new custom goal", GoalLevel.MID)
        hierarchy = self.orc.mod_b.get_goal_hierarchy()
        assert "new custom goal" in hierarchy["mid"]

    def test_iterations_capped(self):
        result = self.orc.process("adversarial drift test: weather is sunny lalala")
        assert result.meta.get("iterations", 1) <= CLCEOrchestrator.MAX_ITERATIONS

    def test_meta_contains_reflection_log(self):
        result = self.orc.process("meta test")
        assert "reflection_log" in result.meta
