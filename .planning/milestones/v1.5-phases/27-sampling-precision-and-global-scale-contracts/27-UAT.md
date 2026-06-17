---
status: complete
phase: 27-sampling-precision-and-global-scale-contracts
source: [27-01-SUMMARY.md, 27-02-SUMMARY.md, 27-03-SUMMARY.md, 27-04-SUMMARY.md]
started: 2026-06-14T12:50:12+08:00
updated: 2026-06-14T12:50:12+08:00
verification_mode: automated (docs/spec adjudication phase; checks re-run against specs, ledgers, evidence packets, gap registers, and git objects)
---

## Current Test

[testing complete]

<!--
Spec-adjudication phase: no runtime UI to click through. Each test below is an
independent, evidence-based re-verification of the Phase 27 deliverables against
the edited framework specs, Phase 24 issue ledger, Phase 25 evidence packets,
Phase 27 gap register, Phase 27 validation strategy, acceptance scripts, and git
objects. Dataset probe cross-checks for DATA-05/DATA-06 were not re-run during
this UAT because an active standard-gold Brutus rerun was detected; Phase 27
plans explicitly allow deferring corroborating dataset probes under an in-flight
rerun and relying on grep checks plus already-verified CLM/DATA facts.
-->

## Tests

### 1. PIPE-04 M12 points-per-trajectory contract and G5 closure
expected: `ctl_instruction.md` Mini-Batch Construction carries `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))` without replacement, rejects an operative `0.5 * n_snapshots` rule, cites DATA-06 medians and `m11-m12-severity.md`; `pinn_architecture.md` points the `points_per_trajectory=32` default back to the ctl contract; M12 and G5 ledger rows are VERIFIED.
result: pass
evidence: `ac-pipe-04.sh` re-run PASS (all 8 assertions plus curriculum-table preservation); `ctl_instruction.md` Mini-Batch region contains `min(n_pts_cap, n_snapshots)`, `without replacement`, DATA-06 medians 61/127/1003, `dt_out`/`n_snapshots`, and doc-03/M16 deferral; `pinn_architecture.md:352` carries the code-default note; `24-ISSUE-LEDGER.md:26` M12 and `:33` G5 are VERIFIED with AC-PIPE-04; commits `6e81d14f`, `da2149d`, `3f4f9d9`, `0a44029` exist.

### 2. PIPE-07 float64 / Decimal precision contract and DATA-05 consumption
expected: `ctl_instruction.md` says `float64` is sufficient for data-side metrics/invariants, `decimal.Decimal` is only the future mass-gate failure classifier, current IC masses are canonical, stale base-hier artifacts were remediated, and a future mass mismatch fails/quarantines the trajectory rather than switching metric paths; mass-drift and footer rows are VERIFIED.
result: pass
evidence: Corrected AC-PIPE-07 probe PASS: `ctl_instruction.md:578-588` contains the precision note, DATA-05 validation citation, current-IC canonicality, stale-artifact interpretation, fail/quarantine future mismatch, and exactly one `decimal.Decimal` token. `data05-precision.md:19` is VERIFIED, names AC-PIPE-07, and has transition log entries at `:92-93`; `24-ISSUE-LEDGER.md:40-41` footer and mass-drift rows are VERIFIED with `data05-precision.md` and AC-PIPE-07. AC-PIPE-06 regression assertions pass (`param_provenance`, `direct`, `inferred`, `absent`, `measured` present). Commits `b6fe225d`, `70dd29b`, `7d39dad` exist.

### 3. PIPE-08 stage-query interface and metadata consistency
expected: `ctl_instruction.md` exposes data-side `sample_replay(n, max_stage)` and `sample_lookahead(n, stage)` using the same `dt_out`/`n_snapshots` metadata settled by PIPE-04/G5; training-loop and collocation-density policy remain deferred to doc-03/M16; `pinn_architecture.md` has only the visibility note.
result: pass
evidence: `ac-pipe-08.sh` re-run PASS (7/7): both signatures present, `dt_out` and `n_snapshots` found, `param_provenance` preserved, doc-03/M16 reference found, and the stage-query subsection negative control has no forbidden training-loop/collocation-density policy outside the blockquote deferral note. `ctl_instruction.md:848-858` contains the stage-query signatures; `pinn_architecture.md:352` contains the visibility note; `24-ISSUE-LEDGER.md:346` records G5/PIPE-08 metadata consistency without reopening G5. Commits `c647fc3`, `8fb87fa`, `3efd840`, `eb43a41` exist.

### 4. PIPE-09 compute_globals global-scale contract
expected: `ctl_instruction.md` §2.5 carries the normative raw-mass `compute_globals` contract: `D = (G*T^2)^(1/3) ~= 4.6416` is canonical, `6.694`/mass-fraction D and `M_tot_ref` are rejected by name, no config parameter may select the mass-fraction form, `E_scale` floor is `+10^{-8}`, Plummer `eps_inv = 1e-10` is preserved, additive epsilon is prohibited, admitted-set scope is transcribed per GAP-27-02 Option A, and SCS remains untouched.
result: pass
evidence: `ac-pipe-09.sh` re-run PASS (14 assertions): raw-mass D expression and 4.6416 present, normative heading present, Plummer positive checks pass, admitted-set scope present, `compute-globals-D` citation present, `6.694` and mass-fraction D only in rejection context, `No configuration parameter` prohibition present, `E_scale` no longer has 1e-10 and does have 1e-8, additive-epsilon prohibition present, arch §5.2 already `+1e-8`, and SCS untouched. `ctl_instruction.md:781-785` contains the normative contract and `E_scale` line; `24-ISSUE-LEDGER.md:39` and `:444` put D=6.694 at VERIFIED with AC-PIPE-09; `compute-globals-D.md:134` records PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED. Commits `731c795e`, `95575fd9`, `7a2b7ad2`, `3e5e7ec7`, `81a587c0` exist.

### 5. Phase-exit governance, validation, and STOP-gap handling
expected: All Phase 27 in-scope ledger rows are terminal VERIFIED, no in-scope Phase 27 STOP gap is open, validation frontmatter is verified/nyquist-compliant, full-suite acceptance checks are green, and the ROADMAP/STATE transition is ready for user confirmation.
result: pass
evidence: `24-ISSUE-LEDGER.md` rows M12, G5, footer, mass-drift, and D=6.694 are VERIFIED; `27-GAPS.md` has GAP-27-01 and GAP-27-02 at RESOLVED-WITH-INSTRUCTION; `27-VALIDATION.md:4-8` is `status: verified`, `nyquist_compliant: true`, `wave_0_complete: true`; `27-VALIDATION.md:95` records full-suite AC green and phase-exit gate met. `audit-open --json` found no current Phase 27 open UAT/verification/context items. `ROADMAP.md` still has Phase 27 unchecked, so the transition step remains pending user confirmation per the interactive transition workflow.

## Summary

total: 5
passed: 5
issues: 0
pending: 0
skipped: 0
blocked: 0
observations: 3

## Gaps

<!-- No failed truths. The observations below are non-blocking verification/hygiene findings.
     They do not change the Phase 27 spec contracts, acceptance results, ledger terminal states,
     or STOP-gap resolutions, but they should be cleaned up before or during Phase 27 transition. -->

- observation: "OBS-1 - Evidence packet header metadata is stale in two packets: `compute-globals-D.md:10` and `m11-m12-severity.md:10` still show `Current Status | PENDING` even though their relevant transition logs and `24-ISSUE-LEDGER.md` rows reached VERIFIED."
  status: non-blocking
  severity: minor
  disposition: "Contract verification is not blocked: Phase 27 plan acceptance criteria require the ledger rows and packet Status Transition Logs to reach VERIFIED, and they do. Cleanup is recommended so packet header metadata matches the terminal state; `data05-precision.md:19` is the local positive precedent."
  artifacts:
    - path: ".planning/phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md"
      issue: "Header Current Status still PENDING while `24-ISSUE-LEDGER.md:39` and packet log `:134` are VERIFIED."
    - path: ".planning/phases/25-evidence-framework-and-issue-ledger/evidence/m11-m12-severity.md"
      issue: "Header Current Status still PENDING while M11 and M12 transition logs reach VERIFIED and ledger rows are terminal."

- observation: "OBS-2 - `m11-m12-severity.md:185-187` contains stale provenance prose from the Phase 25 backfill note, including 'The M12 transition above (`e05b4b1a`) is unchanged' even though the visible M12 Phase 27 transitions now use `6e81d14f`."
  status: non-blocking
  severity: minor
  disposition: "The machine-checkable transition log lines are correct, and M12/G5 ledger rows are VERIFIED. Cleanup is recommended to remove misleading provenance prose."
  artifacts:
    - path: ".planning/phases/25-evidence-framework-and-issue-ledger/evidence/m11-m12-severity.md"
      issue: "Stale prose after the updated M12 transition log."

- observation: "OBS-3 - The worktree was already dirty at UAT start, including modified Phase 27 plan files and the milestone-wide gap index; these were treated as pre-existing/user-owned and were not folded into this UAT verification."
  status: non-blocking
  severity: minor
  disposition: "Phase 27 contracts are verified in the current working tree, but repo hygiene is not clean. Before a final phase-transition commit or handoff, decide whether to keep, commit, or discard the pre-existing dirty plan/gap edits separately."
  artifacts:
    - path: ".planning/phases/27-sampling-precision-and-global-scale-contracts/27-01-PLAN.md"
      issue: "Pre-existing modified file at UAT start."
    - path: ".planning/phases/27-sampling-precision-and-global-scale-contracts/27-02-PLAN.md"
      issue: "Pre-existing modified file at UAT start."
    - path: ".planning/phases/27-sampling-precision-and-global-scale-contracts/27-03-PLAN.md"
      issue: "Pre-existing modified file at UAT start."
    - path: ".planning/milestones/v1.5-GAPS.md"
      issue: "Pre-existing modified file at UAT start."
