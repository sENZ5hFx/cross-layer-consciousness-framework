# Benchmark Protocol: Subsystem 2 — Holographic Memory Matrix

## Claim
Holographic Reduced Representation (HRR) memory produces more human-like associative retrieval than vector database lookup, particularly under degraded, partial, or cross-domain cue conditions.

## Baseline
FAISS vector database with cosine similarity retrieval (standard dense retrieval baseline).

## Secondary Baseline
BM25 sparse retrieval (keyword-based) — controls for lexical overlap effects.

---

## Task Battery

### Task 1: Degraded Cue Retrieval
- **Setup:** Encode 500 experiences into both HRR memory and FAISS. Add Gaussian noise to retrieval cues at three degradation levels: 10%, 30%, 50% noise.
- **Measure:** Retrieval accuracy (correct memory returned in top-3) at each noise level
- **HRR advantage prediction:** Graceful degradation — HRR accuracy degrades more slowly than FAISS as noise increases

### Task 2: Partial Cue Completion
- **Setup:** Encode 200 detailed experiences. Present only 30% of the key features as retrieval cue.
- **Measure:** % of correct memories returned in top-3
- **HRR advantage prediction:** HRR reconstructs from partial activation; FAISS fails without near-complete key match

### Task 3: Cross-Domain Association
- **Setup:** Encode 100 pairs of thematically related memories from different domains (e.g., "a tight deadline at work" and "running the last mile of a race").
- **Measure:** When cued with one domain, does the system retrieve the related cross-domain memory?
- **HRR advantage prediction:** Superposed encoding creates implicit cross-domain links; FAISS treats them as unrelated

### Task 4: Memory Capacity Under Interference
- **Setup:** Encode memories in batches of 100, 500, 1000, 5000. Test retrieval accuracy at each batch size.
- **Measure:** Accuracy degradation curve as memory load increases
- **HRR advantage prediction:** HRR degrades gracefully; FAISS maintains accuracy but with higher compute cost — test whether HRR's graceful curve better matches human memory forgetting curves

---

## Metrics
- Top-3 retrieval accuracy at each degradation level
- Degradation slope (rate of accuracy loss per noise increment)
- Cross-domain association rate
- Compute cost per retrieval at scale

## Failure Condition
If HRR retrieval accuracy under **30% noise** is not significantly better than FAISS (p < 0.05), and cross-domain association rate is not significantly above chance, the holographic memory design fails and must be revised.
