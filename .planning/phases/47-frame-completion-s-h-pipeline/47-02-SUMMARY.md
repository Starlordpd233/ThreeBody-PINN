---
phase: 47-frame-completion-s-h-pipeline
plan: "02"
subsystem: training-metadata-and-energy-scale
tags: [conf-02, s-h-pipeline, training-metadata, fail-closed, admission-capture]
status: complete
requires:
  - "47-01 frame completion: canonical scaled residency + re-ratified RATIFIED_VALIDATION_FRAME"
  - "Phase 46 atomic_write_text primitive and validate_sidecar_payload re-validate-on-load model"
provides:
  - "pinn.loss_catalog._matched_plummer_components — the single home of the softened pairwise sum (D-11)"
  - "AdmittedRecord.k0/uabs0 float64 admission capture + adapter and StageIndex accessors (D-09/D-10/D-12)"
  - "pinn/training/run_metadata.py: compute_s_h, validate_s_h, write_training_metadata, load_training_metadata (D-13..D-18)"
  - "pinn/train.py setup-path S_H wiring; both branches bind the s_h local 47-03 threads into RunController"
  - "tests/phase47/test_conf02_s_h_pipeline.py — 7 dataset-free CONF-02 tests"
affects:
  - "plan 47-03 (eps_H = energy_floor_factor * s_h wiring consumes the bound local and the artifact)"
  - "Phase 50 (first authorized Stage-0 setup/run produces the first real-corpus training_metadata.json)"
tech-stack:
  added: []
  patterns:
    - "component seam: one implementation of the softened pairwise sum feeds both the loss and the admission capture"
    - "explicit expected-binding loader parameters: a loader that cannot know the live config value takes it as a keyword-only argument"
    - "resume gate returns the validated value, so the binding is structural rather than conventional"
key-files:
  created:
    - pinn/training/run_metadata.py
    - tests/phase47/test_conf02_s_h_pipeline.py
  modified:
    - pinn/loss_catalog.py
    - pinn/data/adapter.py
    - pinn/data/types.py
    - pinn/data/splits.py
    - pinn/train.py
decisions:
  - "D-11: _matched_plummer_hamiltonian delegates to _matched_plummer_components; signature and return value unchanged (tests/phase40 + tests/phase41 green, zero edits)"
  - "D-12: the float64 boundary is crossed exactly once, at admission, on the float64 side; the median is never reduced from fp32 resident tensors"
  - "load_training_metadata takes expected_energy_floor_factor (no default) and expected_eps_train=EPS_SOFT as keyword-only bindings — the cycle-3 codex MEDIUM resolution"
  - "_assert_s_h_matches_artifact RETURNS the validated s_h so the resume branch binds it structurally — the cycle-3 claude-max MEDIUM resolution"
  - "REQUIREMENTS.md CONF-02 checkbox deliberately NOT flipped by the executor — a phase-close/verification act, mirroring the 47-01 CONF-09 precedent"
metrics:
  duration: ~30min
  completed: 2026-07-31
  tasks: 2
  commits: 2
  files_changed: 7
---

# Phase 47 Plan 02: S_H Pipeline (CONF-02) Summary

`S_H = median_train(K0 + Uabs0)` is now a validated, atomically persisted,
re-derivable run fact — computed once in float64 over the train split in the
completed CONF-09 frame, fail-closed before step 1, and re-proven on every
load and every resume.

## What shipped

Two commits.

| commit | type | what |
|---|---|---|
| `2b985eee` | feat | component seam + float64 admission capture + adapter/StageIndex accessors + first CONF-02 tests |
| `2ecc53d3` | feat | run_metadata module + setup-path wiring (both branches bind `s_h`) + remaining four CONF-02 tests |

### Task 1 — the seam and the capture (`2b985eee`, five paths)

`pinn/loss_catalog.py` gains `_matched_plummer_components`, the ONE home of
the softened pairwise sum (D-11); `_matched_plummer_hamiltonian` now delegates
and returns `kinetic + potential` with its signature and return value
byte-compatible — `tests/phase40` + `tests/phase41` stay green (356 passed,
106 subtests) with zero edits.

`pinn/data/adapter.py` computes `k0`/`uabs0` in float64 (torch, cpu) at the
capture site beside the existing `inv` construction, from
`pre.r_gauge[0]`/`pre.v_gauge[0]`/`pre.masses_ordered` — the completed frame
tuple `{position: r_prime, time: u, velocity: dr_prime_du, masses:
ordered_raw}` — at `EPS_SOFT = 1e-5`, BEFORE the fp32 residency cast
(D-09/D-12). `uabs0 = float(abs(potential0[0]))`: the ABSOLUTE VALUE of the
softened potential, never the signed Hamiltonian (D-10). The existing
`compute_invariants(pre.masses_ordered, pre.r0_gauge, pre.v0_gauge)` line is
untouched. `AdmittedRecord` gains the two float64 scalars beside the other
invariant scalars; the adapter and `StageIndex` expose them through the
`_source_value` delegation pattern. The four touched production files carry
zero references to the invariants-side verification module or its epsilon
constant (criterion 3 grep: 0).

### Task 2 — the median, the artifact, and the wiring (`2ecc53d3`, three paths)

New module `pinn/training/run_metadata.py`:

- `compute_s_h(train_source)` — pool = `sorted(records_at_or_below(0))`,
  per-key `k0 + uabs0` into a float64 numpy array, `numpy.median`; returns
  `(s_h, n_train)`; an empty pool refuses BEFORE numpy can reach a NaN-median
  path (D-13/D-14/D-17).
- `validate_s_h` — the D-17 predicate, finite AND strictly positive; exactly
  `0.0` refuses the same as negative or non-finite.
- `write_training_metadata` — validates first (refusal precedes artifact),
  computes `eps_h = energy_floor_factor * s_h`, serializes
  `json.dumps(payload, sort_keys=True, indent=2) + "\n"` through
  `atomic_write_text` (D-15; never a raw write).
- `load_training_metadata(run_dir, *, expected_energy_floor_factor,
  expected_eps_train=EPS_SOFT)` — exact key set (unknown keys fail closed the
  same as missing), schema version, the D-17 predicate re-run, the exact
  `eps_h == factor * s_h` product recheck, `n_train` a positive int (bool
  excluded), the frame block against the live `RATIFIED_VALIDATION_FRAME`,
  and the persisted-vs-live `eps_train`/`energy_floor_factor` cross-checks
  (D-18 + cycle-2/cycle-3 review resolutions). No substitute value of any
  kind exists in the module (criterion 2 grep: 0).

`pinn/train.py` wires the block into `main()` after `_build_sources` (:851)
and before `RunController(` (:1050): the fresh branch computes, validates,
persists, and re-reads through the gate; the resume branch loads, recomputes
from the live source, compares exactly, and NEVER overwrites on mismatch. The
resume helper `_assert_s_h_matches_artifact(run_dir, train_source, *,
energy_floor_factor)` RETURNS the validated `s_h`, so BOTH branches bind the
same local that plan 47-03 threads into `RunController` — a compare-without-
bind defect is structurally impossible. Any `ValueError` routes through the
same fail-closed refusal path as a bad corpus (`finish_run("failed", 1)`
before any step). `_synthetic_split_sources` records gain deterministic
positive `k0`/`uabs0` fixtures so the synthetic dev path exercises the same
pipeline.

## Deterministic artifact evidence (fixtures, NOT real-corpus values)

`test_metadata_roundtrip_revalidates` proves the persisted
`training_metadata.json` exposes all seven keys — `schema_version`, `s_h`,
`eps_h`, `n_train`, `eps_train`, `energy_floor_factor`, `frame
{position_frame, time_coord, mass_convention}` — that the float64 `s_h`/`eps_h`
round-trip bit-identically, and that the persisted relationship
`eps_h == energy_floor_factor * s_h` is enforced exactly on every load.
`test_median_train_split_only` proves `n_train` equals the Stage-0 train-pool
size and the median is `numpy.median` in float64 (even-population central
average; permutation-invariant; single-element yields that element), with the
`records_at(0) == records_at_or_below(0)` Stage-0 coincidence asserted (Q3).
`test_s_h_fails_closed` proves NaN/+inf/-inf/negative/exactly-0.0 and the
empty pool each refuse BEFORE any artifact exists. `test_resume_recompute_refuses_mismatch`
drives the production `_assert_s_h_matches_artifact` path: a mutated live
source raises and the on-disk artifact stays byte-identical; a matched source
returns the validated `s_h`; population drift with an unchanged median is
caught by the `n_train` cross-check.

Every number above comes from synthetic duck-typed fixtures and the phase-39
tiny corpus — none of it is a real-corpus result. **The first authoritative
real-corpus `S_H`, `eps_H`, and `N_train` values are deliberately deferred to
Phase 50's first authorized Stage-0 setup/run** (owner ruling 2026-07-30,
Option B); their absence here is routing, not missing Phase 47 evidence. No
zero-step/setup-only emitter was added and no training was launched.

## Deviations from Plan

### `[Rule 3 — blocking]` Closed-form test oracle uses a derived float64 bound

- **Found during:** Task 1, first GREEN run.
- **Issue:** my auxiliary closed-form numpy oracle for the synthetic-snapshot
  components differed from the torch seam by 2.8e-17 (1 ulp) on one element —
  a reduction-order difference between numpy and torch summation, so
  `assert_array_equal` (bit-exact) failed on a correct implementation.
- **Fix:** the closed-form comparison asserts against a bound DERIVED from
  the float64 dtype contract (`8 * finfo(float64).eps * max(1, |expected|)`),
  matching the phase's derived-not-declared discipline. The plan-pinned claim
  is untouched: `torch.equal(kinetic + potential, hamiltonian)` remains
  bit-exact (same-module tensors), and the admission-capture assertions
  (`record.k0 == float(k_expected_t[0])`, `record.uabs0 == abs/predicate`,
  mis-softened-oracle difference) are all exact.
- **Files:** `tests/phase47/test_conf02_s_h_pipeline.py`. **Commit:** `2b985eee`.

### `[Rule 3 — blocking]` Loader call folded to one line for the criterion-10 grep

- **Found during:** Task 2 acceptance-grep pass.
- **Issue:** criterion 10's per-line grep (`grep 'load_training_metadata('
  pinn/ ... | grep -vc 'expected_energy_floor_factor'` must return 0) counts
  per LINE; the helper's call passed `expected_energy_floor_factor=` on the
  continuation line of a two-line call, so the grep returned 1 on a correct
  call.
- **Fix:** the call in `_assert_s_h_matches_artifact` is a single source
  line; the grep returns 0. No behavior change.
- **Files:** `pinn/train.py`. **Commit:** `2ecc53d3`.

Test-construction iteration within TDD RED→GREEN (the direct-records fixture
needing an explicit `physical_key` field for `_validated_records`) is
ordinary GREEN-phase work, not a plan deviation.

## Out-of-scope observation (not fixed)

The interleaved orchestrator commit `cb63d91a` (GAP-47-01 Option-A
application + residual shortfall record) landed between this plan's two
commits; it touches only gap registers and does not interact with the CONF-02
code path. GAP-47-01 remains out of 47-02 scope per the plan's own note.

## Verification

| check | result |
|---|---|
| `pytest tests/phase47/test_conf02_s_h_pipeline.py -q -rs` | **PASS** — 7 passed |
| four named node IDs (`test_median_train_split_only`, `test_s_h_fails_closed`, `test_metadata_roundtrip_revalidates`, `test_resume_recompute_refuses_mismatch`) | **PASS** — 4 passed |
| `pytest tests/phase46/ tests/phase47/ -q -rs` (wave gate) | **PASS** — 162 passed, 68 subtests |
| `pytest tests/phase39/ tests/phase40/ tests/phase41/ -q` | **PASS** — 620 passed, 149 subtests |
| `pytest tests/phase43/test_real_data_smoke_config.py -q` (criterion 8) | **PASS** — 29 passed, 0 failures (no new failures vs the documented phase43 baseline) |
| import check (`pinn.data.adapter`, `pinn.data.splits`, `pinn.loss_catalog`) | **PASS** — no cycle |
| criterion 2: `atomic_write_text` present / banned constructs absent in run_metadata.py | **PASS** — 4 / 0 |
| criterion 3: zero non-comment `gate_metrics`/epsilon-constant refs in the four production files | **PASS** — 0 |
| criterion 4: `compute_invariants(pre.masses_ordered, pre.r0_gauge, pre.v0_gauge)` untouched | **PASS** — 1 |
| criterion 6: no `h0_train`/`s_h_signed` naming | **PASS** — 0 |
| criterion 6 (task 2): `compute_s_h` in setup path between `_build_sources` (:851) and `RunController(` (:1050) | **PASS** — call at :872 |
| criterion 7: empty diff on `pinn/training/config.py` / `config_yaml.py` | **PASS** — empty |
| criterion 10: loader signature keyword-only + all call sites pass the live binding | **PASS** — 1 / 0 |
| criterion 11: helper def exact + returns validated `s_h`; both branches bind | **PASS** |
| no diff to `pinn/verification/`, framework specs, or frozen-config modules (SCOPE-30) | **PASS** |

Task 1 criteria 1-7 and Task 2 criteria 1-11 all pass. Python used:
`<home>/Desktop/3_body_problem/.venv/bin/python` (the plan-pinned
`$(dirname $(git rev-parse --git-common-dir))/.venv/bin/python` resolution;
the worktree carries no `.venv`). No conda substitution was needed.

## Self-Check: PASSED

Files verified present on disk: `pinn/training/run_metadata.py`,
`tests/phase47/test_conf02_s_h_pipeline.py`. Commits verified in `git log`:
`2b985eee`, `2ecc53d3`. No file deletions in either commit
(`git diff --diff-filter=D` empty for both).
