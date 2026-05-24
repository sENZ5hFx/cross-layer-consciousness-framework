# Contributing to CLCE

Thank you for your interest in contributing.

**Important:** This repository contains pre-patent intellectual property
owned by Haley Ann Bird. By contributing, you agree to the terms below.

---

## Contributor License Agreement (CLA)

By submitting a pull request, issue, or any other contribution to this
repository, you agree to the following:

1. **Copyright assignment:** You assign to Haley Ann Bird all copyright
   in your contribution. You retain credit via git commit history.

2. **Patent license:** You grant Haley Ann Bird a perpetual, irrevocable,
   royalty-free license to any patent rights you hold that are necessarily
   infringed by your contribution.

3. **Original work:** You certify that your contribution is your original
   work and does not infringe any third-party rights.

4. **No expectation of compensation:** Contributions are voluntary.
   No compensation is implied or guaranteed.

5. **Developer Certificate of Origin (DCO):** All commits must include
   a sign-off: `git commit -s` (adds `Signed-off-by: Name <email>`).

If you cannot agree to these terms, please do not submit contributions.
You may still use the repository under its CC BY-NC-ND 4.0 license.

---

## What We Welcome

- Bug fixes in prototype code (with tests)
- Additional unit tests or benchmark scenarios
- Documentation improvements and corrections
- Performance improvements to existing algorithms
- Corrections to prior art registry

## What We Do NOT Accept

- New architectural claims without prior discussion
- Dependencies that are not MIT/Apache/BSD licensed
- Any code derived from proprietary or unlicensed sources
- Contributions that alter the IP_DECLARATION.md without owner approval

---

## Process

1. Open an Issue describing the change
2. Wait for approval before coding
3. Fork, branch (`fix/description` or `feat/description`), implement
4. Ensure all 39 tests pass: `pytest prototype/tests/ -v`
5. Run benchmarks: `python benchmarks/run_benchmarks.py`
6. Sign off your commits: `git commit -s`
7. Submit pull request with description of change and test results
