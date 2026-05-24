# Benchmark Protocol: Subsystem 1 — Superposition Layer

## Claim
Maintaining branching representational states and delaying collapse improves reasoning performance on ambiguous inputs compared to standard single-pass inference.

## Baseline
GPT-4o-mini with standard temperature=0 inference (deterministic, single interpretation).

## Secondary Baseline
GPT-4o-mini with temperature=0.8 ensemble (5 samples, majority vote) — controls for simple sampling diversity.

---

## Task Battery

### Task 1: Lexical Ambiguity Resolution
- **Inputs:** 100 sentences with documented lexical ambiguity (e.g., "I saw the man with the telescope")
- **Measure:** Accuracy of final interpretation after full context is provided
- **CLCE advantage prediction:** CLCE holds both interpretations open until resolution context arrives; baseline commits early and fails to update

### Task 2: Referential Ambiguity Under Delayed Clarification
- **Inputs:** 50 multi-turn conversations where the referent of a pronoun is only clarified 3+ turns later
- **Measure:** Correct referent assignment at end of conversation
- **CLCE advantage prediction:** CLCE maintains competing referent hypotheses across turns

### Task 3: Goal Ambiguity in Multi-Step Reasoning
- **Inputs:** 50 problems with two equally valid solution paths; correct path revealed at step 3 of 5
- **Measure:** Solution accuracy and step-3 course-correction rate
- **CLCE advantage prediction:** CLCE pursues both paths to step 3, then collapses; baseline commits to one path at step 1

### Task 4: Overconfidence Under Adversarial Input
- **Inputs:** 50 inputs designed to trigger confident wrong answers (Winograd schemas, trick questions)
- **Measure:** Calibration score (ECE — Expected Calibration Error), frequency of "I'm not sure" responses
- **CLCE advantage prediction:** CLCE's uncertainty flags surface earlier, reducing overconfident errors

---

## Metrics
- Accuracy (% correct)
- Calibration (Expected Calibration Error)
- Course-correction rate (% of trials where CLCE successfully updates after new context)
- Overconfident error rate

## Failure Condition
If CLCE shows no statistically significant improvement (p < 0.05, Cohen's d > 0.5) over the **ensemble baseline** (not just single-pass) on Tasks 1–3, the superposition layer design fails and must be revised.

Note: Improvement over single-pass alone is insufficient — the ensemble baseline must also be beaten, because simple sampling diversity is a trivially achievable baseline.
