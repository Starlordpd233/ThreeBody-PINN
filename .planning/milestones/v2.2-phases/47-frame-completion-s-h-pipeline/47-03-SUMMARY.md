---
phase: 47-frame-completion-s-h-pipeline
plan: "03"
subsystem: loss-assembly-energy-floor
tags: [conf-03, eps-h, energy-floor, loss-wiring, fail-closed, d-19]
status: complete
requires:
  - "47-02 S_H pipeline: the validated s_h local bound on BOTH setup branches + the training_metadata.json artifact (compute_s_h/validate_s_h/write/load_training_metadata, _assert_s_h_matches_artifact)"
  - "stage.energy_floor_factor = 1e-4 (config.py provisional registry, the named home of the 1e-4 factor)"
provides:
  - "RunController.__init__ keyword-only REQUIRED s_h: float channel (no default) + self._s_h; the single structural path a run-level scalar crosses into the loss"
  - "_build_anchor_context eps_h = float(stage.energy_floor_factor) * self._s_h — the dataset-wide ε_H = 1e-4 · S_H"
  - "tests/phase47/test_conf03_eps_h_wiring.py — assembly-boundary tests incl. the uniform-across-anchors invariant and the resume hand-off test"
  - "All 13 RunController( construction sites (pinn/train.py + 12 tests) carry an explicit s_h= (AST-verified)"
affects:
  - "Phase 48 (CONF-04..07 loss-math conformance) inherits a spec-true ε_H path — the per-anchor abs(h0) is in the denominator, the dataset-wide scale supplies ε_H"
  - "Phase 50 (first authorized Stage-0 setup/run produces the first authoritative real-corpus S_H/ε_H/N_train values)"
tech-stack:
  added: []
  patterns:
    - "required keyword-only scalar across a trust boundary: no default can mask a missing validated value; the single-home fail-closed predicate is re-applied at the consumption boundary"
    - "run-level constant flows through an explicit parameter chain (config factor x validated s_h -> RunController -> _AnchorContext.eps_h -> soft_energy_loss), never a module global, never frozen config"
key-files:
  created:
    - tests/phase47/test_conf03_eps_h_wiring.py
  modified:
    - pinn/training/controllers.py
    - pinn/train.py
    - tests/phase40/test_controllers.py
    - tests/phase40/test_optimizer_phase.py
    - tests/phase41/_fixtures.py
    - tests/phase41/test_controllers_ext.py
    - tests/phase43/test_timing_calibration.py
    - tests/phase43/test_real_data_smoke_config.py
decisions:
  - "D-19: the |h0|*factor + 1e-12 additive fallback floor and its WR-02 rationalizing comment are deleted outright at the assembly site (not conditional, not configurable, not relocated); eps_h is the dataset-wide scale"
  - "D-20: per-anchor abs(h0) STAYS in the loss denominator (soft_energy_loss, pinn/loss_catalog.py byte-unchanged) — only the ε scale moved from per-anchor abs(h0)*1e-4 to dataset-wide 1e-4*S_H"
  - "D-21: _AnchorContext.eps_h field and its per-test override seam are unchanged; it now carries the identical run-level constant across all anchors"
  - "T-47-10: RunController takes a keyword-only REQUIRED s_h: float (TypeError when absent) and re-validates via validate_s_h (ValueError on non-finite/non-positive) — repudiation of an unvalidated s_h is impossible to construct"
  - "assumption-delta = promote: the per-anchor scale is DELETED, not kept alongside; companion invariant test_eps_h_uniform_across_anchors adopted"
  - "phase-40 EnergyFloorFactorWiringTests updated to the new eps_h == factor * s_h contract — its |h0|*factor+1e-12 assertions encoded the deleted behavior (mechanism intent preserved: the factor still owns the scale)"
  - "criterion 8 literal grep 's_h=s_h' in pinn/train.py counts 2 (not 1): the second is 47-02's pre-existing write_training_metadata(s_h=s_h); intent (both branches bind s_h, construction reads it) is met and proven by test_resume_binds_s_h_for_controller"
metrics:
  duration: ~45min
  completed: 2026-07-30
  tasks: 2
  commits: 2
  files_changed: 9
---

# Phase 47 Plan 03: ε_H Wiring (CONF-03) Summary

`ε_H = energy_floor_factor · S_H` (`1e-4 · S_H`) now reaches the loss through an
explicit, REQUIRED keyword-only `RunController(s_h=…)` channel threaded from the
47-02-validated `training_metadata.json` pipeline. The §3.4-prohibited additive
fallback floor is gone outright (D-19); the per-anchor `abs(h0)` stays in the
loss denominator `|H_0| + ε_H` where §3.4 puts it (D-20). This is the last Phase
47 requirement; Phase 48's loss-math conformance work inherits a spec-true `ε_H`
path.

## What changed

- **`pinn/training/controllers.py`** — `RunController.__init__` gains a
  keyword-only REQUIRED `s_h: float` (no default); `self._s_h = validate_s_h(s_h)`
  re-applies the single-home fail-closed predicate at the consumption boundary
  (T-47-10). `_build_anchor_context` now computes
  `eps_h = float(stage.energy_floor_factor) * self._s_h`. The four-line WR-02
  comment block and the `abs(h0) * factor + 1e-12` line were deleted wholesale and
  replaced with a one-line CONF-03/D-19 comment; the stale module-docstring
  `eps_h` sentence was aligned. The `validation_source is None` guard stays
  first, so the None-validation-source `ValueError` path is preserved.
- **`pinn/train.py`** — the validated `s_h` local (bound on BOTH the fresh
  `compute_s_h` branch and the resume `_assert_s_h_matches_artifact` branch in
  `main()`) is threaded into `RunController(s_h=s_h)`.
- **Construction-site sweep** — all 12 pre-existing test `RunController(` sites
  (phase40 ×7, phase41 ×3, phase43 ×2) carry an explicit `s_h=` fixture; the
  phase-40 `EnergyFloorFactorWiringTests` assertions were updated to the new
  `eps_h == factor * s_h` contract.
  > **[Count correction, phase close 2026-07-31]** The frontmatter `provides:`
  > line says "All 13 `RunController(` construction sites". The AST gate counts
  > **15** at phase close — 13 plus the two sites this plan's own new
  > `tests/phase47/test_conf03_eps_h_wiring.py` introduced. The invariant the
  > gate enforces is unchanged and still holds: **15/15 carry an explicit
  > `s_h=`, 0 missing.**
- **`tests/phase47/test_conf03_eps_h_wiring.py`** (new) — `test_eps_h_assembly_value`
  (+ the `soft_energy_loss` denominator check), `test_eps_h_uniform_across_anchors`,
  `test_resume_binds_s_h_for_controller`, the constructor fail-closed tests, and
  the `_AnchorContext.eps_h` override-seam test.

## (iii) Deterministic evidence (no real-corpus run required)

- `training_metadata.json` exposes `s_h`, `eps_h`, and `n_train`, with
  `eps_h == energy_floor_factor * s_h` as an exact float64 product (D-15), and
  every load re-validates the payload — fail-closed on any tamper (D-18;
  `test_metadata_roundtrip_revalidates`, 47-02).
- The validated `s_h` reaches `RunController` through the REQUIRED keyword-only
  parameter (omitting it raises `TypeError`; NaN/0.0/negative raise
  `ValueError`) and the loss assembly as `eps_h = factor * s_h`, independent of
  the per-anchor `abs(h0)` (`test_eps_h_assembly_value`).
- Every anchor in a stage sees the SAME `eps_h` — the companion invariant
  (`test_eps_h_uniform_across_anchors`) goes red the instant per-anchor scaling
  returns.
- The resume seam RETURNS a usable `s_h` (not merely compares): a controller
  built from `_assert_s_h_matches_artifact`'s returned value assembles
  `eps_h == factor * s_h` (`test_resume_binds_s_h_for_controller`).
- `pinn/loss_catalog.py` is byte-unchanged (D-20): `soft_energy_loss`'s
  `denom = abs(h0) + eps_h` consumes the new scale with no signature change.

## (ii) Assumption-delta outcome

`promote` — the dataset-wide scale `S_H` becomes primary and the per-anchor
scale (`abs(h0) · 1e-4`) is DELETED, not kept alongside (D-19/D-20). The retained
`_AnchorContext.eps_h` field (D-21) is NOT add-alongside: it carries an identical
value across all anchors and exists only to preserve the per-test override seam.
Companion invariant `test_eps_h_uniform_across_anchors` is adopted and green.

## (i) Phase regression gate (counts vs baseline)

Full `47-VALIDATION.md` suite (`tests/phase41/ tests/phase42/ tests/phase43/
tests/phase46/ tests/phase47/`): **12 failed, 586 passed, 3 skipped, 94 subtests
passed** (282s; pytest exit captured pre-truncation via `set -o pipefail` +
redirect-then-tail). All 12 failures are in `tests/phase43/`
(`test_pilot_calibration`, `test_smoke` HonestyGuard, `test_verdict_grounding`
×7, `test_verify_gate` DurationGate) — environmental: missing persisted Stage-0
timing calibration / owner sign-off, not `eps_h`. The count matches the
documented 12-failure phase43 baseline; **0 CONF-03 regressions** (no failing
file was edited by this plan). AC2: `tests/phase46/ tests/phase47/ -q -rs` exits
0 with **zero skipped** (172 passed, 68 subtests). The locally observed baseline
is 12, matching the documented figure.

Acceptance-criteria evidence: AST `s_h`-kwarg static gate over `pinn/**/*.py` +
`tests/**/*.py` exits 0 (`missing s_h: []`); `1e-12` count 0 (code and comments);
the assembly line `energy_floor_factor) * self._s_h` count 1; no `abs(h0)*` /
`h0)*float` scale factor in code; `git diff -- pinn/loss_catalog.py` empty; no
`s_h` field added to `pinn/training/config.py` (the `grep s_h` hits are the
pre-existing substring in `lbfgs_history_size`).

## (iv) Owner-ruling Phase 50 deferral (Option B, 2026-07-30)

Phase 47 closes on deterministic implementation tests for the complete
`S_H`/training-metadata/loss-wiring pipeline **without launching training**. The
first authoritative real-corpus `S_H`, `ε_H`, and `N_train` values are produced
and reported by **Phase 50's first authorized Stage-0 setup/run**, not here.
Accordingly this plan added no zero-step/setup-only real-data emission path,
launched no training to obtain those values, and did not STOP because no real
`run_dir/training_metadata.json` exists. Absence of real values here is
deliberate deferral, not missing evidence. Any deterministic fixture values
shown in test output remain explicitly non-authoritative. Execution history
contains neither a setup-only real-data emitter nor a Phase 47 training launch.

## (v) VER-20 routing note (D-24)

The `pinn_architecture.md §3.4:542` duplicate-softening author comment remains on
the VER-20 routing list, untouched by this plan. No framework-spec edit was made
(SCOPE-27/28/30, D-24); `git diff` confirms no change under `pinn_instruction/`,
`pinn/verification/`, or any framework spec.
