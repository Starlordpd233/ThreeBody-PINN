# RATIFIED_VALIDATION_FRAME re-ratification record — Phase 47 Plan 01 (CONF-09)

**Recorded:** 2026-07-31 (UTC directory stamp `20260731T012304Z`)
**Artifact class:** bookkeeping on an existing owner ruling (47-CONTEXT.md D-07).
**Not** a new gap, **not** a new CONF-01 verdict, **not** a new decision.

---

## 1. What superseded what

`pinn/training/validation_gate.py::RATIFIED_VALIDATION_FRAME` moved, in the same
commit as the CONF-09 residency swap, from

| field | before (Phase 46 plan 46-07) | after (Phase 47 plan 47-01) |
|---|---|---|
| `position_frame` | `POSITION_FRAME_RAW` = `"r_raw"` | `POSITION_FRAME_SCALED` = `"r_prime"` |
| `time_coord` | `TIME_COORD_RAW` = `"t_native"` | `TIME_COORD_NORMALIZED` = `"u_t_over_T"` |
| `mass_convention` | `MASS_CONVENTION_ORDERED_RAW` = `"ordered_raw"` | `MASS_CONVENTION_ORDERED_RAW` = `"ordered_raw"` (unchanged — the mass encoding never moves) |
| `conf01_evidence_ref` | `.planning/phases/46-frame-resolution-gate-aligned-validation/evidence/target-frame/20260728T014532Z/raw.json` | this file |

Tuple form: `("r_raw", "t_native", "ordered_raw")` → `("r_prime", "u_t_over_T",
"ordered_raw")`. Both pairs are members of `COHERENT_FRAME_PAIRS`
(`validation_gate.py`, the `POSITION_FRAME_*` / `TIME_COORD_*` block); the
scaled pair is the locked contract, and the raw pair existed only to express the
owner-ratified D-09 branch outcome.

**Why it had to be the same commit.** The constant describes what the adapter
actually serves. The CONF-09 swap changed that: `AdmittedSetAdapter` residency
moved to `preprocess_trajectory`'s fully rotation-gauged, `D`/`V`-scaled output,
paired with the `u = t/T` normalization already applied at the sampling
boundary. A tree in which residency has moved and this constant has not is a
tree whose `COHERENT_FRAME_PAIRS` admission check is lying about the
measurement it admits (47-CONTEXT.md D-05).

## 2. On whose authority

The **GAP-46-07 owner ruling of 2026-07-28, option A**, recorded in
`.planning/milestones/v2.2-GAPS.md` (GAP-46-07) and in full in
`.planning/phases/46-frame-resolution-gate-aligned-validation/46-GAPS.md`. That
ruling re-scoped Phase 47 so the frame condition Phase 47 was waiting on is
satisfied *by* Phase 47: CONF-09 completes the residency transform first, and
`S_H` is then computed once in the canonical scaled frame.

The staleness condition was **declared in advance** by GAP-46-06's own constant.
The superseded comment block above `RATIFIED_VALIDATION_FRAME` read:

> Re-ratification is REQUIRED if Phase 47/48 moves residency to the locked
> canonical scaled contract (r' with u = t/T); this constant then goes stale.

`.planning/ROADMAP.md` (Phase 46 amendment, 2026-07-28) states the same standing
consequence: *"`RATIFIED_VALIDATION_FRAME` goes stale if Phase 47/48 moves
residency to the locked canonical scaled contract, and re-ratification is then
required under the same D-12 discipline."* This record is that re-ratification,
executed under the same discipline: the values are quoted from the locked
requirement text, never inferred from any measurement.

Grounding for the destination values: `.planning/REQUIREMENTS.md` CONF-09 and
`.planning/ROADMAP.md` Phase 47 SC-2, both naming
`(POSITION_FRAME_SCALED, TIME_COORD_NORMALIZED, MASS_CONVENTION_ORDERED_RAW)`.

## 3. What is NOT changed by this record (D-27)

CONF-01's Complete status and its mandatory EVAL-01 precondition-(ii) qualification are unchanged by this phase.
CONF-09 *applies* CONF-01's answer; it does not
re-decide it. The Phase 46 machine verdict `VERDICT_NON_FRAME_DIVERGENCE`
recorded in `46-VERDICT-POSTREPAIR.md` is not overwritten, not revisited, and
not superseded by anything in this file. This artifact is bookkeeping on an
existing ruling — it is **not** a new gap and **not** a new CONF-01 verdict.

Also unchanged in this plan: `COHERENT_FRAME_PAIRS`, `_validate_frame`, every
other function in `validation_gate.py`, `pinn/data/preprocessing.py` (the
`r_com_ordered` / `v_com_ordered` intermediate fields survive per D-03), the
`IC₁₃`/`E` construction in `pinn/data/adapter.py`, the `u = t/T` normalization
boundary in `pinn/data/batches.py`, and
`pinn/verification/target_frame_probe.py`.

## 4. Regression evidence (D-22/D-23)

*(Appended by plan 47-01 task 3. Empty at the time this record was written — the
implementation is frozen before any number below is observed, which is the
ordering defence SCOPE-29 requires.)*

<!-- gsd:47-01-task3-regression-evidence -->
