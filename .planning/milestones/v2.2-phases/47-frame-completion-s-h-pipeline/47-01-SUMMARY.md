---
phase: 47-frame-completion-s-h-pipeline
plan: "01"
subsystem: data-residency-and-validation-frame
tags: [conf-09, frame-completion, residency, validation-gate, regression-evidence]
status: complete
requires:
  - "CONF-08 resident pairing repair (Phase 46 plans 46-08/46-09)"
  - "GAP-46-07 owner ruling 2026-07-28, option A"
provides:
  - "resident position/velocity series in the locked canonical scaled frame (r_prime, u = t/T, ordered_raw)"
  - "RATIFIED_VALIDATION_FRAME re-ratified to the scaled triple with a Phase 47 conf01_evidence_ref"
  - "tests/phase47 CONF-09 invariant suite incl. the derived-bound helper frame_drift_tolerance"
  - "D-07 supersession record + D-22/D-23 regression evidence"
affects:
  - "every anchor target (h0, l0, true_r0, true_v0) via the StageIndex residency pass-through"
  - "plan 47-02 (S_H is computed in this frame, once)"
  - "plan 47-03 (eps_H wiring consumes that S_H)"
tech-stack:
  added: []
  patterns:
    - "derived-not-declared numeric bounds: a tolerance is a formula over inputs, never a constant"
    - "atomic multi-file commit when a persisted constant must not lag the behaviour it describes"
key-files:
  created:
    - tests/phase47/__init__.py
    - tests/phase47/test_conf09_frame_completion.py
    - .planning/phases/47-frame-completion-s-h-pipeline/evidence/frame-re-ratification/20260731T012304Z/re-ratification.md
    - .planning/phases/47-frame-completion-s-h-pipeline/evidence/target-frame/20260731T014625Z/
    - .planning/phases/47-frame-completion-s-h-pipeline/deferred-items.md
  modified:
    - pinn/data/adapter.py
    - pinn/training/validation_gate.py
    - tests/phase46/test_pairing_repair.py
decisions:
  - "D-01/D-05/D-06/D-07 land in ONE commit (2c84d161) — no tree exists in which residency moved but the frame constant or the pairing test did not"
  - "The phase-46 independent oracle compares scale-relatively against an fp32-derived bound, not bit-exactly; the bit-exact claim lives only where one shared preprocess_trajectory call feeds both sides"
  - "The D-08 bound is implemented as the plan's four-step derivation verbatim; it was NOT widened when real-data measurement exceeded it on the finite-difference reading — that is routed to the owner"
metrics:
  duration: ~2h
  completed: 2026-07-31
  tasks: 3
  commits: 3
  files_changed: 8
---

# Phase 47 Plan 01: Frame Completion (CONF-09) Summary

Resident trajectories now carry the full canonical pipeline — COM/boost gauge,
canonical body order, rotation gauge, and `D`/`V` scaling — and
`RATIFIED_VALIDATION_FRAME` says so in the same commit.

## What shipped

Three commits.

| commit | type | what |
|---|---|---|
| `2c84d161` | fix | the atomic CONF-09 change: residency swap + frame re-ratification + pairing-test correction + D-07 record |
| `1c68368d` | test | the CONF-09 invariant suite (`tests/phase47/`) |
| `98e05193` | evidence | the one-shot D-22 re-probe and the D-23 before/after comparison |

### Task 1 — the atomic change (`2c84d161`, four paths, one commit)

`pinn/data/adapter.py` candidate construction reads `pre.r_gauge` / `pre.v_gauge`
instead of the CONF-08 intermediate, and both snapshot-count expressions
(`n_snapshots=` and the `_total_admitted_snapshots` accumulation) name that same
array — identical counts, one named residency source (D-01). `times` stays
native; `masses_ordered`, `raw_ic13`, and `inv` are untouched (D-02, D-04).

`pinn/training/validation_gate.py::RATIFIED_VALIDATION_FRAME` moved from
`("r_raw", "t_native", "ordered_raw")` to
`("r_prime", "u_t_over_T", "ordered_raw")`, with `conf01_evidence_ref` pointing
at the new D-07 record. `COHERENT_FRAME_PAIRS` and `_validate_frame` were not
touched (D-05).

`tests/phase46/test_pairing_repair.py` was corrected **in place**, never
superseded by a parallel Phase 47 oracle (D-06). Two methods changed; the
COM/momentum method, the accounting method, and every
`PreprocessingPairingSeamTests` method are byte-unmodified.

The evidence artifact records what superseded what, on whose authority
(GAP-46-07, 2026-07-28, option A, with GAP-46-06's own declared staleness
condition), and the D-27 statement that CONF-01's Complete status and its
mandatory EVAL-01 precondition-(ii) qualification are unchanged.

Atomicity is verified, not asserted: `git log -1 --name-only` for `2c84d161`
lists all four paths, and `git diff HEAD~1 -- pinn/data/preprocessing.py` is
empty.

### Task 2 — the invariant suite (`1c68368d`)

Four module-level pytest functions plus the derived-bound helper, all
dataset-free and train-free:

- `test_ic13_invariance` — `pre.r_gauge[0]` is elementwise-equal to
  `pre.r0_gauge` (one array assignment produces both sides), and the adapter's
  stored `raw_ic13`/`E` reproduce values recomputed independently through
  `build_raw_ic13`/`compute_invariants`, over **every** admitted tiny-corpus
  record.
- `test_velocity_identity` — the exact algebraic identity plus a
  finite-difference check whose per-node tolerance is computed from the
  **actual** `h_minus`/`h_plus` and the analytic scaled-frame jerk, exercised on
  a deliberately non-uniform snapshot selection as well as the full grid.
- `test_ratified_frame_is_coherent` — the constant is the scaled triple, its
  pair is admitted, `_validate_frame` accepts its dict form, and
  `conf01_evidence_ref` resolves to a Phase 47 file naming GAP-46-07.
- `test_gate_metric_near_invariance` — `eps_H` under both pairings and both
  readings, asserted against `frame_drift_tolerance`, which computes the D-08
  bound per trajectory and per reading from inputs only. No declared tolerance
  constant exists in the file.

### Task 3 — regression evidence (`98e05193`)

The unchanged probe ran **exactly once** (exit 0) over the same 1651-trajectory
population, with all three manifest SHA-256s and the blacklist SHA-256 matching
Phase 46 byte for byte. Result: `identity_scaled` true for 1651/1651,
`first_diverging_step` `null` for 1651/1651, and a **zero** maximum absolute
difference between residency and `r_gauge`/`v_gauge` across the whole
population. Both control arms reproduce their Phase 46 values to serialized
precision. Recorded strictly as a regression check, with the mandatory framing
that it is not a frame test and not a new CONF-01 verdict.

## Deviations from Plan

### `[Rule 3 — blocking]` The independent oracle's `rtol=1e-10` cannot apply to an fp32 resident

- **Found during:** Task 1(d)(i).
- **Issue:** the plan pins
  `np.allclose(resident, oracle, rtol=1e-10, atol=1e-10 * max|oracle|)` for the
  independent body-order oracle. Residency is an **fp32** contract
  (`adapter.py::_materialize`), so the resident value is the float64 pipeline
  output rounded to float32 — a relative error up to `0.5 * eps32 ≈ 6e-8`. The
  pinned literal would fail for a correct implementation, in the same way the
  plan itself says exact equality would fail for the D-08 arms.
- **Fix:** the comparison keeps the plan's form and its stated criterion but the
  bound is **derived from the residency dtype contract**:
  `32.0 * numpy.finfo(float32).eps * max|oracle|`, reusing the `32.0` fp32
  round-trip allowance this same file already uses in
  `test_resident_trajectory_preserves_com_and_zero_momentum_gauge`. This sits
  inside the plan's own stated `[1e-12, 1e-6]` plateau, and every defect the
  oracle exists to catch is O(1) relative — seven orders of magnitude away.
- **Files:** `tests/phase46/test_pairing_repair.py`. **Commit:** `2c84d161`.

### `[Rule 3 — blocking]` The oracle must implement all three §2.4 gauge branches

- **Found during:** Task 1(d)(i), first RED run.
- **Issue:** the tiny-corpus fixture is **collinear at `t = 0`**
  (`tests/phase39/_fixtures.py::_body_line` places body `i` at
  `(1+i) * (1, -0.5, 0.05)`), so `lambda_perp` vanishes to round-off and
  production takes the velocity-candidate fallback. An oracle implementing only
  the primary branch measures a different gauge and reports a spurious O(1)
  failure.
- **Fix:** all three branches written out inline in the fixture. The oracle still
  never calls `preprocess_trajectory`.
- **Files:** `tests/phase46/test_pairing_repair.py`. **Commit:** `2c84d161`.

### `[Rule 3 — blocking]` `--evidence-root` added to the probe invocation

- **Found during:** Task 3.
- **Issue:** the probe's default evidence root is the **Phase 46** tree
  (`_DEFAULT_EVIDENCE_ROOT`). Running the Phase 46 invocation verbatim would
  write into Phase 46's retained evidence and break this plan's
  one-directory cap.
- **Fix:** `--evidence-root` points at the Phase 47 tree. Output destination
  only; the instrument, population, and measurement are untouched, and
  `pinn/verification/target_frame_probe.py` has no diff across the whole plan.
- **Files:** evidence only. **Commit:** `98e05193`.

### `[presentation]` Resolved paths recorded repo-anchored, not host-absolute

The plan asks Task 3 to record the resolved absolute path of each probe input.
They are recorded as `<main-repo-root>/…` plus SHA-256, because the probe's own
evidence writer refuses to serialize a host-absolute root, username, or hostname
(T-46-04-02) — a host-absolute literal would contradict the instrument this
record is about. `<main-repo-root>` is the parent of
`git rev-parse --git-common-dir`, exactly how the probe resolves it, so the path
is re-derivable on any checkout.

## Surfaced for owner ruling — NOT resolved here

> **[SUPERSEDED 2026-07-31 — phase-close correction]** This section records the
> state as of plan 47-01's execution and is retained as the historical record.
> It is **no longer current**. GAP-47-01 was subsequently closed
> `RESOLVED-WITH-INSTRUCTION` by two owner rulings (2026-07-30), applied in
> commits `562084e8` (option A — finite-difference cancellation term) and
> `d034e215` (cover all nodes + computed-position round-off). The outcome is
> **50/50 within bound on both readings** (validation-side worst ratio 0.3887,
> median 0.0712; loss-side worst 0.6693). Only the derived bound moved — the
> measured `eps_H` values are identical to every printed digit across all three
> records. See `47-GAPS.md` GAP-47-01 §Final resolution. Verified present in
> code at phase close: the per-node span array
> (`tests/phase47/test_conf09_frame_completion.py:434-436`) and the `8u`
> numerator allowance (:451).

**The D-08 derived bound is exceeded on the validation-side reading for 9 of 50
sampled real trajectories** (max ratio 4.76; loss-side reading: 0 of 50, max
ratio 0.67).

The physics claim is confirmed: the two arms' `eps_H` agree to ~13 significant
digits on every sampled trajectory. What falls short is the **certificate**.
Step 4's operation counts (`4` for the `D` identity, `8` for the `H` assembly)
cover the frame identity and the Hamiltonian assembly, but the validation-side
reading derives velocity by a divided difference of positions
(`gate_metrics.py:84-123`). On real Brutus sampling (`dt_out ≈ 0.01 … 0.08` over
`t ∈ [0, 10]`) `pos[k+1] - pos[k-1]` is a cancelling subtraction of O(1)
operands, so the finite-difference velocity carries a relative error amplified by
roughly `|r| / |Δr| ≈ 10² … 10³` unit round-offs — a term Step 4 does not
contain. The loss-side reading consumes stored velocities, incurs no such
cancellation, and stays inside the bound, which is exactly the signature this
diagnosis predicts. The tiny-corpus unit fixture samples 12–24 snapshots over the
same horizon, so its `h ≈ 0.9` produces almost no cancellation and
`test_gate_metric_near_invariance` passes on its own fixtures.

**Nothing was changed in response.** `frame_drift_tolerance` was not widened, its
operation counts were not raised, no test was relaxed. SCOPE-29/D-26 forbid an
observed number steering the tolerance, and the plan pins the derivation
explicitly. The options are (a) extend Step 4 with a finite-difference
cancellation term, (b) narrow the D-08 claim to the loss-side reading and record
the validation-side agreement descriptively, or (c) accept the record as-is. That
is an owner decision. Full record: §4.2 of the re-ratification artifact.

## D-03 note (required by the plan's output spec)

`r_com_ordered` and `v_com_ordered` are **no longer the residency source** but
**remain on `PreprocessedTrajectory`** as the CONF-08 evidence intermediate.
`pinn/data/preprocessing.py` is byte-unchanged by this plan, and the fields are
still what the Phase 46 seam tests and the D-08 "before" arm are written against.
Deletion is deferred to a later phase that already touches that dataclass. Note
that the field comment at `preprocessing.py:68-70` still reads "CONF-08 resident
surface", which is now stale prose on a field that survives for a different
reason — a one-line correction for whichever phase performs the deletion.

## Deferred Issues

`.planning/phases/47-frame-completion-s-h-pipeline/deferred-items.md` records
D-47-01: 12 pre-existing `tests/phase43/` failures caused by evidence artifacts
removed in `89348b7c chore(planning): archive v2.0 milestone files`, an ancestor
of this branch point. None of them exercise adapter residency or the frame
constant, and the two phase-43 modules that DO reference those symbols both pass.
Out of scope, not fixed.

## Verification

| check | result |
|---|---|
| `pytest tests/phase46/ tests/phase47/ -q -rs` | **PASS** — 155 passed, 68 subtests, 0 skipped |
| `pytest tests/phase39/ -q` | **PASS** — 264 passed, 43 subtests |
| `pytest tests/phase46/test_pairing_repair.py -x -q -rs` | **PASS** — 8 passed, 0 skipped |
| the `python -c` frame check | **PASS** — `r_prime u_t_over_T`, evidence ref resolves |
| exactly one probe-evidence directory | **PASS** — 1 |
| no diff to `pinn/data/preprocessing.py` | **PASS** — empty |
| no diff to `pinn/verification/target_frame_probe.py` | **PASS** — empty across the plan |
| no diff to `pinn_instruction/` or any framework spec (SCOPE-30) | **PASS** — empty |

Task-level acceptance criteria: Task 1 criteria 1-8 all pass (grep counts 1, 1,
2, 0; the runtime frame check; the four artifact strings; both suites; the
four-path single commit; the empty preprocessing diff). Task 2 criteria 1-6 all
pass. Task 3 criteria 1-4 all pass.

## Self-Check: PASSED

Files verified present on disk: `tests/phase47/__init__.py`,
`tests/phase47/test_conf09_frame_completion.py`,
`evidence/frame-re-ratification/20260731T012304Z/re-ratification.md`,
`evidence/target-frame/20260731T014625Z/{raw.json,summary.md}`,
`deferred-items.md`. Commits verified in `git log`: `2c84d161`, `1c68368d`,
`98e05193`. No file deletions in any commit.
