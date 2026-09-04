# Phase 55: Architecture Characterization Probe - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-04
**Phase:** 55-Architecture Characterization Probe
**Areas discussed:** Todo fold, Regression protection, Sweep generality, New-structure scope boundary

---

## Todo fold

| Option | Description | Selected |
|--------|-------------|----------|
| d-06-static-epsilon-sensitivity-check | Spec-side epsilon sensitivity question (score 0.6, generic keyword match) | |
| trainex-r1-research-handoff | r1b tuning-round handoff (score 0.6, generic keyword match) | |
| Fold neither (recommended) | Both matches look like keyword overlap, not genuine scope overlap | ✓ |

**User's choice:** Fold neither.
**Notes:** User asked whether these two stale todos should be cleaned up from the repo if no longer relevant, but explicitly deferred that to *after* Phase 55's real work — recorded under Deferred Ideas in CONTEXT.md, not acted on now.

---

## Regression protection (SC4: reproduction/regression tolerance regime)

| Option | Description | Selected |
|--------|-------------|----------|
| Exact golden-value match | Frozen fixture, byte/float match — catches everything including harmless float-rounding drift from refactors | |
| Invariant-style bounds only | Order-of-magnitude R̄, front_idx==0, weight-floor pinned — robust but looser | |
| Claude's judgment (two-tier) | Invariant bounds as the primary hard gate + a secondary exact-value JSON fixture at tight relative tolerance for defense-in-depth | ✓ |

**User's choice:** "Choose all areas worth discussion following your best judgement... no need for user manual decisions unless there's something I need to look at" — user opted out of manual selection for all three substantive areas.
**Notes:** Decided two-tier (D-01 in CONTEXT.md): primary invariant-bound assertions (robust to legitimate refactors) plus a secondary exact-value fixture (the computation is fully deterministic, so bit-level reproducibility is achievable and matches how `gate_metrics.py`'s tests already pin exact values). Rationale recorded in CONTEXT.md D-01.

---

## Sweep generality (SC1: how configurable must "a configurable seed/IC sweep" be)

| Option | Description | Selected |
|--------|-------------|----------|
| Fixed six-case fixture only | Hard-code exactly the six audited cases | |
| General config-driven tool | Arbitrary (seed, masses, IC13-mode) list via CLI/config; six audited cases as default | ✓ |

**User's choice:** Deferred to Claude's judgment (see above).
**Notes:** Decided general (D-02 in CONTEXT.md), directly grounded in the ROADMAP's own Phase 55 goal text — "committed, tested tooling that anyone can re-run against any candidate recipe" — which requires genuine configurability, not six literals. Also unblocks Phase 56 reusing the same tool for the new 4096/16-bin structure without new code.

---

## New-structure (4096-total/16-bin) scope boundary

| Option | Description | Selected |
|--------|-------------|----------|
| Run and evidence the new-structure six-case probe now | Early look at R_ref precursor numbers as part of Phase 55 | |
| Build capability only; don't exercise it as a milestone artifact | Unit-test the new binning/stratification mechanism generically; leave the real six-case run under governance to Phase 56 | ✓ |

**User's choice:** Deferred to Claude's judgment (see above).
**Notes:** Decided to hold the line on requirement ownership (D-03 in CONTEXT.md): INST-04 (Phase 55) vs GATE-04 (Phase 56) are separate requirements, and `54-RULING.md` ties `R_ref` to a measurement that must be persisted with full provenance and re-measured on structural change — governance that belongs to Phase 56. Producing an uncommitted, ungoverned R_ref-like number inside Phase 55 risks it being quoted informally before Phase 56's process runs. Phase 55 still builds and unit-tests the new-structure mechanism (so the capability genuinely exists), just doesn't run it "for real" against the six audited cases as a Phase 55 deliverable.

---

## Claude's Discretion

- Module name/location under `pinn/verification/`, result dataclass shape, CLI flag names.
- Deterministic RNG scheme for the "random tanh IC13" variable-mass case (audit row 6) — must be documented and reproducible.
- Evidence directory placement (`.planning/phases/55-*/evidence/`) and test file location (`tests/phase55/`), both following established repo conventions.

## Deferred Ideas

- Cleanup/disposition of `d-06-static-epsilon-sensitivity-check.md` and `trainex-r1-research-handoff.md` (pending todos) — after Phase 55's real work, not during it.
