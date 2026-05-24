# CLCE Roadmap

## Phase 1 — Theoretical Foundation ✅ COMPLETE
- Drafted core consciousness model comparison
- Mapped QNHF vs CLCE theoretical differences
- Authored preprint draft (`PREPRINT_DRAFT.md`)
- Built `big_map.md` floor-by-floor conceptual architecture
- Published `consciousness_models_comparison.md` and `qnhf_critique_and_upgrade.md`

## Phase 2 — Subsystem Specification ✅ COMPLETE
- Specified Subsystem 1 (Superposition Layer)
- Specified Subsystem 2 (Holographic Memory Matrix)
- Specified Subsystem 3A/B/C (Awareness, Intention, Reflection)
- Defined inter-subsystem data contracts
- Wrote falsifiability matrix (`testability/falsifiability_matrix.md`)

## Phase 3 — Prototype Infrastructure ✅ COMPLETE
- `prototype/config.py` — global configuration
- `prototype/main.py` — entry point
- `prototype/requirements.txt` — dependencies
- Directory structure established

## Phase 4 — Full Working Prototype ✅ COMPLETE
- `prototype/subsystem1/superposition_layer.py` — full S1 implementation
- `prototype/subsystem2/holographic_memory.py` — full HRR memory
- `prototype/subsystem3/awareness_module.py` — Module A
- `prototype/subsystem3/intention_module.py` — Module B
- `prototype/subsystem3/reflection_module.py` — Module C
- `prototype/orchestrator.py` — full-stack wiring
- `prototype/embeddings.py` — sbert/openai/pseudo routing
- `prototype/session_cli.py` — interactive REPL
- `prototype/tests/test_subsystems.py` — 22 unit tests
- `benchmarks/run_benchmarks.py` — three falsifiability benchmark trials
- `.github/workflows/ci.yml` — CI: test + benchmark + lint on Python 3.10/3.11/3.12
- `architecture/CLCE_architecture.md` — full system design doc
- `testability/falsifiability_matrix.md` — per-claim test matrix

## Phase 5 — Real Evaluation 🕐 IN PROGRESS
- [ ] Replace pseudo-embeddings with `sentence-transformers` (MiniLM-L6-v2)
- [ ] Replace rule-based candidate generator with LLM paraphraser (GPT-4o / Claude)
- [ ] Run S1-A, S1-B against AmbigQA or equivalent real dataset
- [ ] Run S2-A degraded-cue benchmark with real keys
- [ ] Run S3-A human evaluation protocol (n ≥ 100 sessions)
- [ ] Run S3-B contradiction rate benchmark with NLI model
- [ ] Run ablation study (INT-A) across all subsystem combos
- [ ] Produce p-values and confidence intervals for all claims
- [ ] Publish updated preprint with empirical results section

## Phase 6 — Integration & Deployment 💤 PLANNED
- [ ] Wrap orchestrator as REST API (FastAPI)
- [ ] Add streaming output mode
- [ ] Plugin interface for external tools (web search, code execution)
- [ ] Session persistence (SQLite or Redis)
- [ ] Docker image + Compose file
- [ ] Public demo endpoint

## Phase 7 — Peer Review & Publication 💤 PLANNED
- [ ] Submit preprint to arXiv (cs.AI)
- [ ] Submit to conference (NeurIPS workshop / Consciousness & Cognition)
- [ ] Address reviewer comments
- [ ] Open-source benchmark dataset
- [ ] Community contribution guide
