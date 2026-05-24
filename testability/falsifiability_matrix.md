# CLCE Falsifiability Matrix

This document maps every theoretical claim in the CLCE framework to
a concrete, falsifiable experimental condition with defined pass/fail criteria.

A framework that cannot be falsified is philosophy, not engineering.
Every claim here must eventually be tested and *could fail*.

---

## Subsystem 1: Superposition Claims

### Claim S1-A
**Claim:** Holding multiple interpretations in superposition before collapsing
produces better outcomes on ambiguous inputs than greedy single-pick selection.

**Test protocol:**
- Dataset: AmbigQA or equivalent benchmark with intentionally ambiguous inputs
- Baseline: greedy argmax of initial weights
- Metric: accuracy@1 on disambiguation tasks
- Pass condition: CLCE accuracy > baseline by ≥5% (p < 0.05, n ≥ 200 trials)
- Fail condition: no statistically significant improvement

**Status:** Synthetic baseline in `benchmarks/run_benchmarks.py`. Real eval pending real embeddings.

---

### Claim S1-B
**Claim:** Context-vector reweighting improves collapse accuracy vs. weight-only collapse.

**Test protocol:**
- Same dataset as S1-A
- Compare: collapse with context vector vs. collapse without
- Metric: accuracy@1
- Pass condition: context-reweighted > weight-only (p < 0.05)
- Fail condition: no significant difference

**Status:** Infrastructure implemented; awaiting real embedding backend for meaningful comparison.

---

## Subsystem 2: Holographic Memory Claims

### Claim S2-A
**Claim:** HRR-based associative retrieval outperforms exact-key lookup under
partial/degraded cue conditions.

**Test protocol:**
- Encode 100 key-value pairs to the HRR memory
- Query with 30% character-corrupted or truncated keys
- Baseline: Python dict exact-match lookup
- Metric: hit rate in top-3 results
- Pass condition: CLCE hit rate ≥ baseline + 15% (degraded keys are unresolvable by exact match)
- Fail condition: CLCE hit rate ≤ baseline

**Status:** Implemented in `benchmarks/run_benchmarks.py::benchmark_holographic`.

---

### Claim S2-B
**Claim:** HRR memory degrades gracefully as more traces are added (signal/interference tradeoff).

**Test protocol:**
- Encode N = [10, 50, 100, 200, 500] traces
- Measure mean retrieval cosine similarity vs. N
- Pass condition: similarity decreases monotonically but remains > 0.3 up to N = 0.1 × dim
- Fail condition: similarity collapses below 0.3 at N << 0.1 × dim

**Status:** Not yet automated. Can be run manually via `HolographicMemory` API.

---

## Subsystem 3: Meta-Cognitive Claims

### Claim S3-A
**Claim:** Systems with Module C (Reflection) produce statistically fewer
goal-drift events than chain-of-thought (CoT) processing without self-monitoring.

**Test protocol:**
- Benchmark task: multi-turn goal-directed dialogue (20 turns)
- With CLCE: Module B monitors; Module C corrects
- Without CLCE (baseline): raw LLM output without monitoring
- Metric: % of outputs rated as goal-aligned by human evaluators (blind)
- Pass condition: CLCE ≥ baseline + 10% alignment rate (p < 0.05, n ≥ 100 sessions)
- Fail condition: no significant improvement

**Status:** Infrastructure in `run_benchmarks.py::benchmark_metacognitive`. Human eval pending.

---

### Claim S3-B
**Claim:** Belief revision logging (Module A) reduces self-contradiction in
extended reasoning chains vs. no-memory baselines.

**Test protocol:**
- Task: 10-step reasoning chain on complex factual question
- Measure: contradiction rate (automated NLI check between step N and all prior steps)
- Baseline: standard chain-of-thought, no belief state
- Pass condition: CLCE contradiction rate ≤ 50% of baseline (p < 0.05)
- Fail condition: no significant reduction

**Status:** Requires NLI model integration. Planned for Phase 5.

---

### Claim S3-C
**Claim:** The reframe → S1 injection loop reduces the number of processing
iterations needed to reach goal coherence ≥ 0.7 vs. random restart.

**Test protocol:**
- Task: 50 synthetic goal-drift scenarios
- CLCE: reframe instruction injected as high-weight S1 candidate
- Baseline: random restart (new random weights, no reframe)
- Metric: mean iterations to coherence ≥ 0.7
- Pass condition: CLCE ≤ 70% of baseline mean iterations (p < 0.05)
- Fail condition: no significant reduction

**Status:** Infrastructure ready. Requires meaningful embeddings for semantic coherence scoring.

---

## Integration Claims

### Claim INT-A: Emergent Meta-Cognition
**Claim:** The three-subsystem integration produces behaviors not present in
any subsystem alone (superposition alone, memory alone, or reflection alone).

**Test protocol:**
- Run ablation study: S1 only, S2 only, S3 only, S1+S2, S1+S3, S2+S3, S1+S2+S3
- Metric: goal coherence score over 50-turn sessions
- Pass condition: S1+S2+S3 > all ablated variants (p < 0.05)
- Fail condition: any ablated variant matches or exceeds full system

**Status:** Framework complete. Requires real eval harness.

---

### Claim INT-B: CLCE vs. QNHF
**Claim:** CLCE's explicit, falsifiable implementation outperforms QNHF's
single-metric emergence score on interpretability and error diagnosis.

**Test protocol:**
- Run both systems on identical ambiguous input sets
- Human evaluators assess: (a) output quality, (b) explainability of result
- Pass condition: CLCE rated higher on explainability (p < 0.05)
- Fail condition: QNHF rated equivalent or higher on explainability

**Status:** Pending QNHF reference implementation for direct comparison.

---

## Non-Claims (What CLCE Does NOT Assert)

The following are *not* claims of CLCE and are out of scope for falsification:

- CLCE does **not** claim phenomenological consciousness or qualia
- CLCE does **not** claim to implement physical quantum superposition
- CLCE does **not** claim to replicate biological neural mechanisms
- CLCE does **not** claim the system is sentient or has subjective experience
- CLCE does **not** claim to solve the Hard Problem of Consciousness

CLCE claims only that these mechanisms produce measurable improvements in
specified cognitive benchmarks relative to specified baselines.
