# Changelog

All notable changes to the Cross-Layer Consciousness Engine (CLCE) are documented here.
This project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.4.0] — 2026-05-24

### Added
- `embeddings.py` — public `_embed_pseudo(text, dim)` function (previously inlined, now
  a named, importable symbol used by tests and by `embed()`).
- `embeddings.py` — `backend_info() -> dict` reporting `active_backend`, `model`,
  and `upgrade_note`; allows runtime introspection of the embedding layer.
- `config.py` — `GENERATE_CANDIDATES_N: int = 5`  new constant; orchestrator
  no longer hardcodes candidate count.
- `orchestrator.py` — `extra_context` parameter now correctly prepended to
  `full_input` and reflected in `ProcessingResult.input`.
- `orchestrator.py` — `_generate_candidates` now handles `n > 5` gracefully
  by generating synthetic variants; dead `n` parameter bug fixed.
- `orchestrator.py` — `_single_pass` exposes `iteration` parameter reserved
  for future per-iteration logic.
- Tests — `test_embeddings.py` fully rewritten: `TestPseudoEmbeddings`,
  `TestEmbed`, `TestBackendInfo` classes with parametrize coverage.
- Tests — `test_subsystems.py` shared helper functions `_make_coherence_signal`
  and `_make_awareness_report` extracted; `TestHolographicMemory` gains
  `test_retrieve_returns_float_value_tuples`.
- Tests — `test_orchestrator.py` gains `test_extra_context_appears_in_input_field`,
  `test_memory_hits_are_score_value_tuples`, `test_max_iterations_reads_from_config`.

### Fixed
- **P0** `ImportError` on `from embeddings import _embed_pseudo, backend_info` —
  both symbols now exist.
- **P1** Ruff `E401` on `import sys, os` in test files — split to separate lines
  across `test_subsystems.py`, `test_orchestrator.py`, `conftest.py`.
- **P1** Missing `# noqa: E402` on post-`sys.path` imports.
- **P2** `config.py` was a dead constants island — all orchestrator hard-coded
  values now imported from `config`.
- **P2** `_generate_candidates(n)` parameter was silently ignored — now used.
- **P2** `extra_context` was accepted but not forwarded into `full_input` in
  `_single_pass`.
- Python 3.12 deprecation: `datetime.utcnow()` replaced with
  `datetime.now(timezone.utc)` wherever present.

### Changed
- `orchestrator.py` imports reorganised to stdlib → third-party → local order
  (ruff `I001` compliance).
- `conftest.py` `import sys, os` split; `from __future__ import annotations` added.

---

## [0.3.0] — 2026-05-21

### Added
- Subsystem 3: `AwarenessModule`, `IntentionModule`, `ReflectionModule`.
- `CLCEOrchestrator` full-stack integration.
- `session_cli.py` interactive REPL.
- `IP_DECLARATION.md`, `PATENT_CLAIMS_SCAFFOLD.md`, `PRIOR_ART_REGISTRY.md`.
- `TRADEMARK_WATCH_REGISTER.md`, `LICENSING_FAQ.md`, `DCO.md`.

## [0.2.0] — 2026-05-14

### Added
- Subsystem 2: `HolographicMemory` with `cosine_similarity` utility.
- `embeddings.py` pseudo-backend fallback.
- `COMMERCIAL_LICENSE.md`, `CODEOWNERS`, `CONTRIBUTING.md`.

## [0.1.0] — 2026-05-07

### Added
- Subsystem 1: `SuperpositionLayer` — quantum-metaphor parallel interpretation collapse.
- `config.py` global constants.
- `LICENSE` (custom Haley Ann Bird Research License v1.0).
- `NOTICE` third-party attribution.
- `SECURITY.md`, `ROADMAP.md`.
