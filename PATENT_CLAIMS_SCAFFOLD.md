# Patent Claims Scaffold
## Cross-Layer Consciousness Engine (CLCE)

**Inventor:** Haley Ann Bird  
**First Disclosure Date:** 2026-05-07 (timestamped GitHub commit)  
**Last Updated:** 2026-05-24  
**Status:** Pre-filing scaffold — not yet filed with any patent office.

> **Legal Note:** This document is a structured pre-filing narrative to
> support a future patent application. It does not constitute a filed patent
> claim and confers no patent rights. It establishes public disclosure date
> for prior art purposes.

---

## Independent Claims

### Claim 1 — Config-Centralised Consciousness Pipeline

A computer-implemented system for processing natural language inputs through
a layered cognitive architecture, comprising:

(a) a **configuration module** (`config.py`) storing, as a single authoritative
    source, all tuneable parameters governing the behaviour of downstream
    modules, including but not limited to embedding dimensionality
    (`EMBEDDING_DIM`), memory dimensionality (`MEMORY_DIM`), candidate
    generation count (`GENERATE_CANDIDATES_N`), superposition branch bounds
    (`MIN_BRANCHES`, `MAX_BRANCHES`), memory retrieval width (`MEMORY_TOP_K`),
    and maximum processing iterations (`MAX_ITERATIONS`);

(b) a **superposition layer** (Subsystem 1) that receives a plurality of
    candidate interpretations of an input string, assigns each a normalised
    probability amplitude, and selects a single interpretation via a
    context-vector-guided collapse operation, all parameters for which are
    read from (a);

(c) a **holographic memory module** (Subsystem 2) that encodes selected
    interpretations as superimposed traces on a shared memory vector of
    dimensionality `MEMORY_DIM`, and retrieves stored values via
    cosine-similarity ranking, with retrieval width governed by `MEMORY_TOP_K`
    from (a);

(d) a **meta-cognitive layer** (Subsystem 3) comprising:
    - an awareness module tracking active beliefs, memories, and uncertainty flags;
    - an intention module maintaining a hierarchical goal register and computing
      goal-coherence scores for each selected interpretation;
    - a reflection module issuing one of {continue, reframe, restart} decisions
      based on combined awareness and coherence signals;

(e) an **orchestrator** (`CLCEOrchestrator`) that sequentially executes (b)–(d)
    for each input, reads `MAX_ITERATIONS` from (a) to cap the reframe loop,
    and returns a structured result comprising selected interpretation,
    confidence score, coherence score, reflection action, memory hits,
    elapsed time, and a meta dictionary containing iteration count,
    reflection audit log, and goal hierarchy;

wherein all numeric parameters in (b)–(e) are derived exclusively from (a),
and no module contains hard-coded constants.

---

### Claim 2 — Dual-Backend Embedding Layer

The system of Claim 1, wherein the embedding module (`embeddings.py`) provides:

(a) a primary path using a pre-trained sentence-transformer model when the
    `sentence-transformers` library is available in the runtime environment;

(b) a deterministic fallback path (`_embed_pseudo`) using an MD5-seeded
    pseudo-random number generator to produce a unit-normalised float32
    vector of configurable dimensionality, requiring no external dependencies;

(c) automatic selection between (a) and (b) at module load time;

(d) a `backend_info()` introspection function returning the active backend
    identifier, model name (if applicable), and an upgrade recommendation;

wherein any downstream module calling `embed(text, dim)` receives a
unit-normalised numpy array regardless of which backend is active.

---

### Claim 3 — Candidate Generation with Semantic Tagging

The system of Claim 1, wherein `_generate_candidates(text, n)` produces
exactly `n` candidate interpretations by:

(a) always placing the unmodified input text as the first candidate at weight
    1.0;

(b) generating up to four semantically-tagged variants with decreasing weights
    (literal 0.80, abstract 0.70, causal 0.60, contextual 0.50);

(c) if `n` exceeds the number of predefined variants, generating synthetic
    variants labelled `[synthetic-k]` at weights 0.40 − 0.05k;

(d) reading `n` from `config.GENERATE_CANDIDATES_N`, such that no call site
    hard-codes a candidate count.

---

## Dependent Claims

### Claim 4
The system of Claim 1, wherein the orchestrator accepts an optional
`extra_context` string that is prepended to the full input before candidate
generation, enabling context injection without modifying the core pipeline.

### Claim 5
The system of Claim 1, wherein the reflection module's reframe decision
causes the orchestrator to prepend a reframe instruction to the next
iteration's input, forming an explicit corrective feedback loop.

### Claim 6
The system of Claim 3, wherein the superposition layer accepts context
vectors produced by the embedding module of Claim 2, uses cosine similarity
between the context vector and pseudo-embeddings of each candidate text to
bias the collapse toward the contextually closest candidate, and records the
collapse reason as `context_signal` when context-vector reweighting governs
the outcome.

---

## Prior Art Acknowledgement

See `PRIOR_ART_REGISTRY.md` for a full registry of related prior art.
The claims above are distinguished from prior art on the basis of:
- config-centralisation as a first-class architectural constraint
- the specific three-module meta-cognitive layer design (S3A/B/C)
- the dual-backend embedding façade with introspection
- the candidate semantic-tagging + synthetic fallback scheme

---

*This scaffold was prepared by the inventor and is subject to revision
before formal filing. All rights reserved. © 2026 Haley Ann Bird.*
