---
phase: 46-frame-resolution-gate-aligned-validation
plan: "08"
subsystem: data
tags: [conf-08, pairing, com-recenter, boost-removal, canonical-order, tdd, regression]

requires:
  - phase: 46-frame-resolution-gate-aligned-validation
    provides: 46-06 measured CONF-01 ambiguity and its 1651/1651 pairing/COM confound register
  - phase: 46-frame-resolution-gate-aligned-validation
    provides: GAP-46-05 owner-ratified minimum repair boundary
provides:
  - "PreprocessedTrajectory.r_com_ordered/v_com_ordered: float64 COM/boost-gauged and canonically ordered arrays before rotation or scaling"
  - "Adapter residency whose positions, velocities, and masses address the same bodies"
  - "Eight-test CONF-08 regression contract, including all twelve pre-existing preprocessing outputs"
affects: [46-09 unchanged-instrument post-repair probe, 47 frame-dependent work]

tech-stack:
  added: []
  patterns:
    - "Expose an already-computed canonical pipeline seam; do not duplicate transform math in the adapter"
    - "Separate the upstream float64 1e-12 gauge invariant from a scale-derived fp32 residency round-trip bound"

key-files:
  created:
    - tests/phase46/test_pairing_repair.py
    - .planning/phases/46-frame-resolution-gate-aligned-validation/46-08-SUMMARY.md
  modified:
    - pinn/data/preprocessing.py
    - pinn/data/adapter.py

key-decisions:
  - "The resident surface receives exactly COM recentering, zero-momentum boost removal, and canonical body ordering"
  - "The rotation gauge and D/V global scalings remain absent so 46-09 is a measurement rather than a tautology"
  - "No pre-existing test encoded the divergent pairing; therefore Task 3 required no test expectation edits"

requirements-completed: [CONF-08]

coverage:
  - id: D1
    description: "Ordered COM/boost arrays are independently re-derived from raw fixture equations and a literal nonidentity permutation"
    requirement: CONF-08
    verification:
      - kind: unit
        ref: "tests/phase46/test_pairing_repair.py#PreprocessingPairingSeamTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "Adapter resident positions, velocities, and masses share one body order while membership/accounting stays fixed"
    requirement: CONF-08
    verification:
      - kind: unit
        ref: "tests/phase46/test_pairing_repair.py#AdapterPairingRepairTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "The repair stops before rotation and global scaling and leaves all twelve old preprocessing outputs byte-identical"
    requirement: CONF-08
    verification:
      - kind: unit
        ref: "tests/phase46/test_pairing_repair.py#PreprocessingPairingSeamTests::test_exposed_arrays_are_neither_rotated_nor_globally_scaled"
        status: pass
      - kind: unit
        ref: "tests/phase46/test_pairing_repair.py#PreprocessingPairingSeamTests::test_additive_fields_leave_every_preexisting_output_bit_identical"
        status: pass
    human_judgment: false

completed: 2026-07-27
status: complete
---

# Phase 46 Plan 08: Resident Pairing and COM/Boost Repair Summary

**The resident trajectory now addresses bodies in the same canonical order as
`masses_ordered` and carries the COM-recenter/zero-momentum gauge. The repair
stops before the rotation gauge and before both global scalings.**

## Repair

`PreprocessedTrajectory` gained two additive float64 fields:

- `r_com_ordered`: positions after COM recentering, uniform COM-drift removal,
  and canonical body permutation.
- `v_com_ordered`: velocities after COM-velocity removal and the same canonical
  body permutation.

The fields expose the existing `r_bar`/`v_bar` values immediately after
`_canonical_order`; no transform was re-derived and no existing computation
line moved. All twelve pre-existing outputs (`masses_ordered`, `permutation`,
`r0_gauge`, `v0_gauge`, `r_gauge`, `v_gauge`, `R0`, `R_COM0`, `V_COM`, `D`,
`T`, `V`) retain their captured pre-repair bytes or scalar bit patterns.

At `pinn/data/adapter.py:861-875`, candidate residency now uses
`pre.r_com_ordered` and `pre.v_com_ordered`; `pre.masses_ordered` is unchanged.
`n_snapshots` and `_total_admitted_snapshots` use the repaired position array's
unchanged leading dimension. Materialization and public snapshot accessor
signatures are unchanged.

## Explicit transform boundary

- Applied: COM recentering.
- Applied: zero-momentum/COM-velocity boost removal.
- Applied: canonical body permutation.
- **Not applied:** `_rotation_gauge`.
- **Not applied:** position scaling by `D`.
- **Not applied:** velocity scaling by `V`.

The negative contract verifies that the resident seam is neither `r_gauge` nor
`r_gauge * D`, and likewise is neither `v_gauge` nor `v_gauge * V`. Therefore
the repair does not pre-answer CONF-01.

## Surviving raw parsed-array uses

| Location | Use | Why it remains correct |
|---|---|---|
| `pinn/data/adapter.py:492-493` | `to_parsed_trajectory` admission input | Admission must assess the parsed corpus before preprocessing; these arrays never become resident tensors. |
| `pinn/data/adapter.py:845-846` | Input to `preprocess_trajectory` | The canonical pipeline must begin from parsed raw arrays; this is the single implementation of every transform. |

There is no surviving `parsed_brutus.positions` or
`parsed_brutus.velocities` use in candidate construction, materialization, or
the resident snapshot surface.

## TDD evidence

The preprocessing seam first failed with three `AttributeError` cases because
`r_com_ordered`/`v_com_ordered` did not exist; the captured-old-output test was
already green. After the additive preprocessing change, the seam plus all Phase
39 adapter tests passed.

The adapter contract then failed exactly two behaviors: resident arrays still
equaled parsed file-order values, and resident snapshot-0 COM was nonzero
(`5.548494343332077`). After the candidate-source switch, all eight behaviors
passed. The upstream float64 COM/momentum values meet `1e-12`; fp32 resident
values are checked against a scale-derived round-trip bound.

## Full-suite baseline and triage

The authoritative pre-repair baseline was run from inside a clean detached
worktree at `997c731bea518594070742d7103471904768b520`, with that worktree
explicitly on `PYTHONPATH`:

`13 failed, 1245 passed, 11 skipped, 20 warnings, 311 subtests passed`

The live repaired worktree reported:

`14 failed, 1260 passed, 3 skipped, 20 warnings, 311 subtests passed`

The detached baseline lacks the ignored local `runs/stage0-smoke/summary.json`,
so `HonestyGuardTests::test_evidence_readme_documents_the_findings` skips there
but activates and fails in the live worktree. DI-46-04-01 already records this
test as pre-existing alongside the other eleven Phase 43 failures. The other
thirteen live failures are present in the detached baseline. No repair-coupled
failure appeared.

An earlier attempted baseline was discarded before interpretation because its
absolute test path was detached while its process cwd/import root remained the
live worktree. The corrected baseline above ran with both cwd and `PYTHONPATH`
pinned to the detached commit.

### Three-bucket triage

| Test id(s) | Bucket | Justification |
|---|---|---|
| none | (a) encoded the divergence | No pre-existing expectation depended on masses and positions disagreeing. |
| none | (b) fixture-shaped | No positional `PreprocessedTrajectory` constructor or fixture arity broke. |
| `PilotCalibrationEvidenceTests::{test_candidates_are_observation_linked_and_await_owner_ratification,test_manifest_has_traceable_completed_seed_band_and_required_schema}` | (c) pre-existing/unrelated | Missing archived Phase 43 pilot evidence path; recorded in DI-46-04-01 and present at `997c731b`. |
| `VerdictGroundingTests::{test_current_verdict_is_receipt_seed_timing_and_seam_grounded,test_failing_gate_rejects_unqualified_go,test_invalid_calendar_date_is_rejected,test_missing_receipt_seed_timing_or_seam_citation_is_rejected,test_owner_adjust_decision_and_dated_sign_off_are_persisted,test_quoted_yaml_gate_is_typed_and_validates,test_receipt_mismatched_go_is_rejected}` | (c) pre-existing/unrelated | Missing archived Phase 43 verdict path; recorded in DI-46-04-01 and present at `997c731b`. |
| `DurationGateLaunchTests::{test_forecast_exactly_1800_accepted_run_dir_created,test_over_limit_with_green_marker_accepted_run_dir_created}` | (c) pre-existing/unrelated | Existing calibration-path/environment failure; recorded in DI-46-04-01 and present at `997c731b`. |
| `HonestyGuardTests::test_evidence_readme_documents_the_findings` | (c) pre-existing/unrelated | Activated only by the live worktree's ignored smoke summary; recorded before this repair in DI-46-04-01. |
| `GlobalPackagingTests::{test_a5_canonical_bin_matches_repo_source,test_a6_deployed_skill_paths_rewritten}` | (c) pre-existing/unrelated | Existing global watchdog deployment drift; recorded in DI-46-05-01 and present at `997c731b`. |

No test was deleted, skipped, marked xfail, or weakened. No Task-3 test file
needed modification.

## Verification

- `pytest tests/phase46/test_pairing_repair.py -x -q -rs`:
  **8 passed, zero skipped**.
- `pytest tests/phase39/ tests/phase46/ -q -rs`:
  **366 passed, 70 subtests passed, zero skipped**.
- `pytest tests/ -q -rs`: **1260 passed**; the 14 failures are exactly
  DI-46-04-01 and DI-46-05-01 as detailed above.
- Added skip/xfail grep: no matches.
- `git diff --check`: pass.
- `git diff -- pinn/verification/target_frame_probe.py`: empty.

## Deviations

The first baseline invocation did not isolate the import root and was rejected;
it was repeated correctly in a detached worktree before any baseline claim was
used. No implementation or scope deviation occurred.

## Task commit

This plan's code, tests, and summary are carried by the atomic
`fix(46-08): pair resident trajectories with ordered masses under the com boost gauge`
commit.

## Next

Plan 46-09 must first prove probe, manifest, blacklist, code-commit, and transform
identity, then perform exactly one post-repair measurement. No frame is
ratified by this plan.

