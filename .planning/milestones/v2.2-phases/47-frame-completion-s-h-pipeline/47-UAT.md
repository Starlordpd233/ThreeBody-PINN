---
status: complete
phase: 47-frame-completion-s-h-pipeline
source: [47-01-SUMMARY.md, 47-02-SUMMARY.md, 47-03-SUMMARY.md]
started: 2026-07-31T07:25:28Z
updated: 2026-07-31T08:12:00Z
verification_mode: agent-automated
verification_note: >
  Owner delegated verification to the agent (2026-07-31): every checkpoint was
  discharged by independent re-derivation and adversarial probing against the
  live tree, not by re-reading the SUMMARY claims. Counterfactuals were run
  wherever a passing check could otherwise be vacuous.
---

## Current Test

[testing complete]

## Tests

### 1. Resident Trajectories Live in the Canonical Scaled Frame (CONF-09)
expected: Adapter residency reads `pre.r_gauge`/`pre.v_gauge`; IC13 and the position targets share one gauge; the autograd d/du velocity matches its target exactly (dr'/du = v_gauge).
result: pass
source: automated
evidence: |
  Independent grid-refinement convergence study on a curved (Lagrange +
  COM-offset + drift) trajectory, finite-differencing `pre.r_gauge` against
  u = t/T and comparing to `pre.v_gauge`:

    N      h(u)        err CURRENT   ratio | err SUPERSEDED  ratio
     128  1.597e-03      1.020e-04     -   |     8.999e+00     -
     256  7.953e-04      2.530e-05    4.03 |     9.000e+00    1.00
     512  3.968e-04      6.299e-06    4.02 |     9.000e+00    1.00
    1024  1.982e-04      1.572e-06    4.01 |     9.000e+00    1.00
    2048  9.907e-05      3.926e-07    4.00 |     9.000e+00    1.00

  The current residency's residual falls at exactly the O(h^2) rate (ratio
  4.00), i.e. it is entirely MY finite-difference truncation error — the
  identity holds exactly. The superseded CONF-08 source sits at a constant
  9.000 under refinement: a real, non-vanishing frame incoherence equal to
  (T-1) with T=10, precisely the missing time-scaling factor. The counter-
  factual proves the check is not vacuous.

  Also verified: V == D/T exactly; D = 4.641588833612778 (the locked raw-mass
  convention); `r_gauge[0]`/`v_gauge[0]` elementwise-equal `r0_gauge`/`v0_gauge`;
  IC13 built from either is bit-identical (dim 13).
  Code: adapter.py:861,884-885,890,894 read `pre.r_gauge`/`pre.v_gauge`.

### 2. Frame Constant Re-Ratified Atomically (CONF-09)
expected: `RATIFIED_VALIDATION_FRAME` is the scaled triple with a Phase 47 evidence ref; residency swap + constant + phase-46 test correction land in ONE commit; `preprocessing.py` byte-unchanged.
result: pass
source: automated
evidence: |
  Runtime read: position_frame=`r_prime`, time_coord=`u_t_over_T`,
  mass_convention=`ordered_raw`; `conf01_evidence_ref` resolves to
  `.../evidence/frame-re-ratification/20260731T012304Z/re-ratification.md`.
  `git show --name-only 2c84d161` lists exactly four paths (evidence artifact,
  adapter.py, validation_gate.py, tests/phase46/test_pairing_repair.py).
  `git diff 2c84d161^ 2c84d161 -- pinn/data/preprocessing.py` = 0 lines.

### 3. S_H Is a Persisted, Re-Derivable Run Fact (CONF-02)
expected: S_H = median_train(K0 + Uabs0) in float64, persisted atomically with exactly seven keys, re-validated on every load, exact `eps_h == factor * s_h`.
result: pass
source: automated
evidence: |
  Independent median oracle: odd population -> 2.0, even population -> 2.5
  (central average), single element -> itself; n_train correct; permutation
  invariant. Exact 7-key set confirmed. `s_h` round-trips bit-exact float64;
  `eps_h == FACTOR*s_h` exact. Frame block carries the re-ratified triple.
  Write path: 4 `atomic_write_text` refs, 0 raw `open(...,'w')`/`write_text`/
  `os.replace`.

  Adversarial tamper matrix — all 12 mutations REFUSED (ValueError):
  eps_h decoupled from s_h; s_h -> 0.0 / NaN / negative; n_train -> 0;
  n_train -> True (bool); extra unknown key; missing key; schema_version
  bumped; eps_train drifted; energy_floor_factor drifted; frame swapped to the
  superseded raw triple. A mismatched live `expected_energy_floor_factor` is
  also refused. The good artifact was byte-unchanged (SHA-256) after the whole
  tamper campaign.

### 4. S_H Validation Fails Closed (CONF-02)
expected: Non-finite, negative, and exactly 0.0 refuse before any artifact is written; an empty train pool refuses too.
result: pass
source: automated
evidence: |
  `validate_s_h` refuses NaN, +inf, -inf, -1.0 and exactly 0.0 (ValueError),
  accepts 1.5. `write_training_metadata` refuses all five AND leaves the target
  directory with **0 files** in every case — refusal provably precedes the
  artifact. `compute_s_h` on an empty pool refuses before numpy can reach a
  NaN-median path.

### 5. eps_H = 1e-4 x S_H Reaches the Loss, Additive Floor Deleted (CONF-03)
expected: Required keyword-only `s_h`; `eps_h = factor * s_h` uniform across anchors; the `+1e-12` additive fallback floor gone; per-anchor `abs(h0)` retained in the denominator.
result: pass
source: automated
evidence: |
  Swept 8 (energy_floor_factor, s_h) combinations over 300 anchors each, every
  anchor carrying a DISTINCT h0: in all 8 cases the anchor contexts yielded
  exactly ONE eps_h value, equal to `factor * s_h` exactly. eps_h is provably
  independent of h0.

  Channel: `s_h` is KEYWORD_ONLY with no default; omitting it -> TypeError;
  passing it positionally -> TypeError; NaN/+inf/-inf/0.0/-1.0 -> ValueError.
  Repudiating an unvalidated s_h is not constructible.

  Floor: `grep -c 1e-12 controllers.py` = 0; no `abs(h0)*`/`h0)*float` scale
  factor anywhere in `pinn/`. AST sweep of `pinn/**/*.py` + `tests/**/*.py`
  found 15 `RunController(` sites, 15 carrying explicit `s_h=`, 0 missing.

  D-20: `soft_energy_loss` denominator is `denom = h0_t.abs() + eps_h_t`;
  numerically loss(h0=1)=1.34259515e+00, loss(h0=10)=5.84267099e-01,
  loss(h0=100)=5.08426786e-01 at fixed eps_h — per-anchor |h0| demonstrably
  still normalises. `git diff` on `pinn/loss_catalog.py` across 47-03 = 0 lines.

### 6. Phase Regression Gate — No New Failures
expected: phase46+47 exit 0 with zero skipped; the full suite's 12 failures are all pre-existing and environmental.
result: pass
source: automated
evidence: |
  `pytest tests/phase46/ tests/phase47/ -q -rs` -> 172 passed, 68 subtests,
  0 skipped, exit 0.
  Full suite (phase41/42/43/46/47) -> **12 failed, 586 passed, 3 skipped,
  94 subtests** in 359.86s — matching 47-03-SUMMARY exactly. All 12 failures
  are in `tests/phase43/` (2 pilot_calibration + 1 smoke + 7 verdict_grounding
  + 2 verify_gate), matching the documented D-47-01 baseline shape exactly.

  CAUSATION SETTLED HISTORICALLY. A detached worktree was created at the
  Phase 47 branch point (`c0d4d9dd`, parent of the first phase-47 commit) and
  `tests/phase43/` was run there. First pass gave 11 failed / 179 passed /
  8 skipped — the 8 skips being purely an artifact of the fresh worktree
  lacking the UNTRACKED `runs/` outputs. After symlinking the same `runs/`
  directory in to make the environments identical, the pre-Phase-47 tree gave
  **12 failed, 186 passed, 0 skipped** — byte-identical to the current tree.
  The one initially-divergent test fails at the branch point too, with
  `FileNotFoundError` on `.../43-.../evidence/smoke/README.md`.

  Root cause independently confirmed: `git log --diff-filter=D` names
  `89348b7c chore(planning): archive v2.0 milestone files` (2026-07-23) as the
  commit that deleted that evidence tree, and `git merge-base --is-ancestor`
  confirms it is an ancestor of HEAD — six days before Phase 47 began
  (2026-07-30). Control: the two phase43 modules that DO exercise phase-47
  symbols pass fully (test_evaluate_gate 13 passed, test_real_data_smoke_config
  29 passed).

  Conclusion: Phase 47 introduced ZERO regressions. Temp worktree removed;
  `runs/` intact at 396M; working tree carries no stray edits.

### 7. Real-Corpus Numbers Deliberately Deferred to Phase 50
expected: No training launched, no real-corpus artifact emitted; the deferral is grounded in a recorded owner ruling, not agent invention.
result: pass
source: automated
evidence: |
  No `training_metadata.json` exists anywhere in the tree. `runs/` holds only
  pre-existing Phase-43-era directories (probe-run, stage0-pilot-seed41/42/43,
  stage0-smoke, stage0-smoke-diag), all dated 2026-07-19..22 — before the first
  Phase 47 commit (2026-07-30 18:35). No Phase 47 run exists.

  Grounding located (not invented): `.planning/STATE.md:356` records "First
  authoritative real-corpus S_H/eps_H/N_train deferred to Phase 50 (owner
  Option B)". Absence of real values is routing, not missing evidence.

## Summary

total: 7
passed: 7
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

[none — no issues found]

## Notes for phase close (not UAT failures)

These are outstanding *governance* acts, deliberately left to phase close by the
executors. None is a defect in the delivered work.

1. **`.planning/REQUIREMENTS.md` checkboxes are still unticked** for CONF-02
   (line 36), CONF-03 (line 37) and CONF-09 (line 44), and the status table
   (lines 111, 112, 118) still reads `Pending` for all three. Both 47-01 and
   47-02 state this was intentional: flipping them "is a phase-close/
   verification act, not a plan-execution act". All three are now verified
   satisfied. Flipping them mutates a locked governance doc, so it is left for
   explicit owner action.

2. **No `*-VERIFICATION.md` exists** in the phase dir, so the canonical GSD
   completion predicate cannot pass and the phase cannot auto-transition —
   `uat_blockers: ["policy: verification required but no passing
   *-VERIFICATION.md found"]`.

3. **47-01-SUMMARY.md §"Surfaced for owner ruling" is stale.** It describes the
   D-08 bound as exceeded on 9 of 50 trajectories with "nothing changed in
   response". That was true when written, but GAP-47-01 was subsequently closed
   `RESOLVED-WITH-INSTRUCTION` by two owner rulings, applied in `562084e8` and
   `d034e215`, reaching 50/50 within bound on both readings (worst ratio
   0.3887). Verified present in code: the per-node span array
   (`test_conf09_frame_completion.py:434-436`) and the `8u` numerator
   allowance (:451). The SUMMARY text, not the code, is what lags.

4. **Minor count drift in 47-03-SUMMARY.md**: it states "All 13 RunController(
   construction sites". The AST sweep finds 15 today (the plan's own new test
   file added two). The substantive claim — every site carries an explicit
   `s_h=` — holds at 15/15.

5. **D-47-01 remains OPEN/informational**: the 12 pre-existing `tests/phase43/`
   failures. Now proven pre-existing (see Test 6). Routing suggestion in
   `deferred-items.md` stands: a v2.2 test-hygiene pass.
