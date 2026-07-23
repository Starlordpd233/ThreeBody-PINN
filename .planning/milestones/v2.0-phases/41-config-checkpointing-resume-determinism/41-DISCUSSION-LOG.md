# Phase 41: Config, Checkpointing, Resume & Determinism - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-07-17
**Phase:** 41-config-checkpointing-resume-determinism
**Areas discussed:** Gray-area selection, Resume config-diff split (B-5)

---

## Gray-area selection (which HOW-decisions to weigh in on)

| Option | Description | Selected |
|--------|-------------|----------|
| Checkpoint payload schema | Nested state_dict keys + retention file layout | (delegated to Claude) |
| Resume config-diff split (B-5) | Identity vs operational field classification; fail-safe | ✓ |
| failure/ bundle contents | Diagnostics captured on a guard trip | (delegated to Claude) |
| Determinism switch scope | What strict-CPU toggles; default off | (delegated to Claude) |

**User's choice:** "Resume config-diff split (B-5), you can decide on option 1, 3, and 4."
**Notes:** Requirements were locked by SPEC.md (8 CTRL) and most of the approach was
pre-fixed by the Phase-40 CTX-42..45 seams, so only B-5 carried genuine owner stake.

---

## Resume config-diff split (B-5) — Q1: where does the identity line sit?

| Option | Description | Selected |
|--------|-------------|----------|
| Conservative | Identity = model/data/science/numerics/seed; operational = only pure runtime knobs; unclassified → refuse | ✓ |
| Middle | Identity = model/data/science/seed; operational adds tuning knobs (MAX_EPOCHS extension, guard thresholds); precision/device stays identity | |
| Permissive | Widest set allowed to differ (incl. precision/device, thresholds, epoch extension) | |

**User's choice:** Conservative (Recommended).
**Notes:** Matches the fail-safe philosophy and CTRL-05 "continues exactly". Final list is
a PROPOSAL the owner ratifies before run #1; the fail-safe `unclassified → refuse` rule is locked.

## Resume config-diff split (B-5) — Q2: which swing fields are OPERATIONAL?

| Option | Description | Selected |
|--------|-------------|----------|
| Checkpoint cadence + wall-clock ceiling | Pure runtime; cannot change results | ✓ |
| MAX_EPOCHS (per-stage budget) | Extending to "train longer" on resume | (stays identity) |
| Guard / RECOVER thresholds (R-1) | Tuning ⚖ placeholders mid-run | (stays identity) |
| Precision / device (fp32-MPS ↔ fp64-CPU) | ENV-04 escape hatch; breaks exact continuation | (stays identity) |

**User's choice:** Only "Checkpoint cadence + wall-clock ceiling" operational; all other swing
fields stay identity (refuse on change).
**Notes:** Recorded implication — extending epochs or hot-tuning thresholds on a resume will
refuse; that requires a new run. This is the safe reading of "continues exactly"; the owner may
loosen specific fields at run-#1 ratification. (CTX-57.)

---

## Claude's Discretion

- **Checkpoint payload schema** (CTX-53..56) — nested `weights_only`-clean dict keyed by
  component; rolling-3/best/latest/anchor layout; atomic tmp+fsync+rename; fallback scan;
  idempotent `curriculum.jsonl`.
- **`failure/` bundle contents** (CTX-61) — tiered Tier-A (always, tiny: README + trip.json) /
  Tier-B (best-effort: tail.log + last-good-checkpoint ref + config ref); no raw tensor dumps
  (disk-floor-safe).
- **Determinism switch scope** (CTX-63) — `strict_cpu_determinism` default OFF; toggles CPU +
  `use_deterministic_algorithms(True)` + `set_num_threads(1)` + re-seed.
- **Driver-scope boundary** (spec-phase, Option A) — minimal runnable `pinn.train` driver +
  library; canonical JSONL logging stays Phase 42.
- Module filenames within `pinn/training/`; identity-digest canonicalization; argparse shape.

## Deferred Ideas

None — discussion stayed within phase scope. Reviewed-not-folded todos
(`d-06-static-epsilon-sensitivity-check`, `trainex-r1-research-handoff`) are recorded in
CONTEXT.md `<deferred>`.
