# IP Declaration
## Cross-Layer Consciousness Engine (CLCE)

**Owner:** Haley Ann Bird  
**First Publication:** 2026-05-07 (GitHub commit record)  
**Last Updated:** 2026-05-24  
**Repository:** https://github.com/sENZ5hFx/cross-layer-consciousness-framework

---

## 1. Scope of Claim

This declaration covers all original source code, architecture documents,
research preprints, and design artefacts contained in this repository,
authored solely by Haley Ann Bird, and first disclosed via timestamped
GitHub commits beginning 2026-05-07.

All rights reserved. No licence to use, copy, modify, distribute, or
sublicense any part of this work is granted except as expressly stated in
the `LICENSE` file at the repository root.

---

## 2. Covered Artefacts (as of 2026-05-24)

### Prototype Source

| File | Description | Added |
|---|---|---|
| `config.py` | Global tuneable constants; single source of truth for all magic numbers across the prototype | v0.1.0 |
| `embeddings.py` | Dual-backend embedding layer; `embed()`, `_embed_pseudo()`, `backend_info()` | v0.2.0 / updated v0.4.0 |
| `orchestrator.py` | Full-stack CLCE pipeline; `CLCEOrchestrator`; config-wired constants | v0.3.0 / updated v0.4.0 |
| `main.py` | Batch entry-point | v0.3.0 |
| `session_cli.py` | Interactive REPL | v0.3.0 |
| `conftest.py` | pytest sys.path bootstrap | v0.3.0 |
| `subsystem1/superposition_layer.py` | Quantum-metaphor parallel plugin state collapse | v0.1.0 |
| `subsystem2/holographic_memory.py` | Content-addressable holographic memory store | v0.2.0 |
| `subsystem3/awareness_module.py` | Belief, memory, and uncertainty tracking | v0.3.0 |
| `subsystem3/intention_module.py` | Goal hierarchy and coherence evaluation | v0.3.0 |
| `subsystem3/reflection_module.py` | Meta-cognitive interrupt and reframe controller | v0.3.0 |

### Test Suite

| File | Coverage Target |
|---|---|
| `tests/test_embeddings.py` | `_embed_pseudo`, `embed`, `backend_info` |
| `tests/test_subsystems.py` | All three subsystems; `cosine_similarity` |
| `tests/test_orchestrator.py` | `CLCEOrchestrator` end-to-end integration |

### Documentation & Legal

`LICENSE`, `COMMERCIAL_LICENSE.md`, `NOTICE`, `CONTRIBUTING.md`,
`CHANGELOG.md`, `ROADMAP.md`, `SECURITY.md`, `DCO.md`,
`CODEOWNERS`, `LICENSING_FAQ.md`, `TRADEMARK_WATCH_REGISTER.md`,
`IP_DECLARATION.md` (this file), `PATENT_CLAIMS_SCAFFOLD.md`,
`PRIOR_ART_REGISTRY.md`, `PREPRINT_DRAFT.md`, `UOXAFW.md`

---

## 3. Novel Contributions

1. **Config-Centralised Architecture** — all tuneable parameters for a
   consciousness-engine prototype live in a single `config.py`; no subsystem
   duplicates a constant.

2. **Dual-Backend Embedding** — a single `embed()` façade that degrades
   gracefully from real semantic embeddings to a deterministic, zero-dep
   pseudo-backend without breaking any downstream caller.

3. **Quantum-Metaphor Superposition Collapse** — a software-only
   probabilistic candidate-selection mechanism modelled on wavefunction
   collapse; not a claim of physical quantum computation.

4. **Holographic Associative Memory** — content-addressable storage where
   each trace is superimposed on a shared memory vector; partial-key
   retrieval is supported.

5. **Three-Module Meta-Cognitive Layer** — Awareness (belief/uncertainty
   tracking), Intention (goal hierarchy + coherence scoring), Reflection
   (interrupt/reframe/restart arbitration) operating as a unified S3.

6. **Config-Driven Iteration Cap** — `CLCEOrchestrator.MAX_ITERATIONS` reads
   from `config.MAX_ITERATIONS`; no hard-coded loops anywhere in the pipeline.

---

## 4. Third-Party Attributions

See `NOTICE` for full third-party dependency list.
See `PRIOR_ART_REGISTRY.md` for prior art acknowledgements.

---

## 5. Legal Notices

- Copyright © 2026 Haley Ann Bird. All rights reserved.
- This declaration does not constitute a patent application.  
  See `PATENT_CLAIMS_SCAFFOLD.md` for the scaffolded claims narrative.
- Commercial use requires a separate written licence agreement.  
  See `COMMERCIAL_LICENSE.md`.
- This work is protected under applicable copyright law from the date of  
  first commit. The GitHub commit timestamps constitute prima facie evidence  
  of creation date.
