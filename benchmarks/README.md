# CLCE Benchmarks

This directory contains empirical testability protocols for all three CLCE subsystems, plus cross-system benchmarks testing the integrated engine against standard AI baselines.

---

## Structure

```
benchmarks/
├── README.md                        ← You are here
├── protocols/
│   ├── protocol_superposition.md    ← Subsystem 1 benchmark design
│   ├── protocol_holographic.md      ← Subsystem 2 benchmark design
│   └── protocol_metacognitive.md    ← Subsystem 3 benchmark design
└── cross_system/
    └── protocol_integrated.md       ← Full CLCE vs. baseline comparison
```

---

## The Falsifiability Standard

Every benchmark follows this structure:

1. **Claim** — what the subsystem theoretically produces
2. **Baseline** — the standard AI equivalent being compared against
3. **Tasks** — specific test inputs and conditions
4. **Metrics** — what is measured and how
5. **Failure condition** — the exact result that would falsify the design
6. **Statistical threshold** — minimum effect size and significance level (p < 0.05, Cohen's d > 0.5)

---

## Running Benchmarks

```bash
cd benchmarks
python run_benchmarks.py --subsystem all
python run_benchmarks.py --subsystem superposition
python run_benchmarks.py --subsystem holographic
python run_benchmarks.py --subsystem metacognitive
```
