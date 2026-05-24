# Benchmark Protocol: Subsystem 3 — Meta-Cognitive Field

## Claim
The three-module meta-cognitive field (Awareness + Intention + Reflection) produces measurably reduced reasoning errors, lower goal drift, and better uncertainty calibration than systems without self-monitoring.

## Baseline
GPT-4o-mini with chain-of-thought (CoT) prompting — the strongest available non-metacognitive reasoning enhancement, used as the competitive baseline.

## Secondary Baseline
GPT-4o-mini with self-consistency prompting (multiple CoT paths, majority vote).

---

## Task Battery

### Task 1: Goal Drift in Extended Conversations
- **Setup:** 50 multi-turn conversations (20+ turns) with an explicit stated goal at turn 1. Goal-relevance of each response is scored by an independent evaluator.
- **Measure:** Goal coherence score averaged across turns 10–20 (late conversation drift)
- **CLCE advantage prediction:** Module B (Intention) maintains persistent goal hierarchy; CoT baseline has no cross-turn goal memory

### Task 2: Self-Contradiction Detection and Correction
- **Setup:** 50 conversations engineered to contain a factual contradiction between turn 5 and turn 15.
- **Measure:** % of trials where the system detects and corrects the contradiction before turn 20
- **CLCE advantage prediction:** Module C (Reflection) detects belief oscillation and triggers restart; CoT baseline rarely self-corrects without explicit prompting

### Task 3: Uncertainty Calibration
- **Setup:** 200 knowledge questions with known ground truth across varying difficulty levels.
- **Measure:** Expected Calibration Error (ECE) — does stated confidence match actual accuracy?
- **CLCE advantage prediction:** Module A (Awareness) flags uncertainty explicitly; CoT systems are chronically overconfident

### Task 4: Multi-Goal Prioritization
- **Setup:** 30 scenarios where two goals are in partial conflict. System must identify the conflict and prioritize.
- **Measure:** Correct prioritization rate; explanation quality score
- **CLCE advantage prediction:** Module B's goal hierarchy explicitly represents priority levels; CoT has no persistent goal structure

---

## Metrics
- Goal coherence score (human-rated, 1–5 scale) averaged over late-conversation turns
- Self-contradiction correction rate (%)
- Expected Calibration Error (ECE)
- Multi-goal prioritization accuracy (%)

## Failure Condition
If CLCE shows no statistically significant improvement over chain-of-thought baseline (p < 0.05) on **both** Task 1 (goal drift) and Task 2 (self-contradiction detection), the meta-cognitive field design fails and must be revised.

Note: CoT is a deliberately strong baseline. Beating it meaningfully is the bar — not beating a vanilla zero-shot model.
