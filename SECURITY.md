# Security Policy
## Cross-Layer Consciousness Engine (CLCE)

---

## Supported Versions

| Version | Supported |
|---------|-----------|
| Phase 4 (current `main`) | ✅ Active |
| Phase 3 and earlier | ❌ No longer patched |

---

## Reporting a Vulnerability

Do **NOT** open a public GitHub Issue for security vulnerabilities.

To report a security issue:
1. Email the repository owner directly (contact info in NOTICE)
2. Use the subject line: `[CLCE SECURITY] <brief description>`
3. Include: affected file(s), reproduction steps, potential impact
4. Expect acknowledgment within 72 hours
5. Coordinated disclosure: allow 30 days before public disclosure

---

## IP Security Considerations

This repository contains pre-patent intellectual property. The following
security posture is in effect:

### Source Code
- All code is CC BY-NC-ND 4.0. Do not fork for commercial use.
- No production API keys, credentials, or secrets are committed.
  The `embeddings.py` OpenAI backend reads from `OPENAI_API_KEY`
  environment variable only — never hardcoded.
- Secret scanning is enabled on this repository (GitHub Advanced Security).

### Dependency Security
- Dependencies are minimal and audited: numpy, scipy, pytest only (core).
- Optional dependencies (sentence-transformers, openai) are not bundled.
- Run `pip audit` before adding any new dependency.

### Branch Protection
- `main` branch: direct pushes require owner authentication.
- All CI runs are logged and artifacts retained for audit.
- Force-push is disabled to preserve commit timestamp integrity
  (critical for IP priority date chain).

### Data
- No user data is collected or stored by this repository.
- `benchmarks/results/` JSON files contain no PII.
- Session CLI (`session_cli.py`) is local-only; no network calls
  unless OpenAI backend is explicitly configured.

---

## Commit Integrity

All commits to `main` are signed with the repository owner's credentials.
Git SHA-256 hashes provide cryptographic integrity over the full history.
The commit chain constitutes a legally admissible timestamp record for
IP priority date purposes.

Do not rebase or amend commits on `main`. This would break the
timestamp chain and could compromise IP priority date claims.
