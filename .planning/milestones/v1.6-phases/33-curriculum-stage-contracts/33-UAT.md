---
status: complete
phase: 33-curriculum-stage-contracts
source: [33-01-SUMMARY.md, 33-02-SUMMARY.md, 33-03-SUMMARY.md, 33-04-SUMMARY.md]
started: 2026-06-23T09:59:49Z
updated: 2026-06-23T13:45:00Z
---

## Current Test

number: 7
name: Scope and owner-pending discipline (governance)
expected: |
  Among framework specs, only ctl_instruction.md was edited — sampling_method.md
  (frozen), the read-only reports (data_quality_assessment.md, review-of-framework.md,
  stage_strat_revision.md), and live pinn/ code are untouched. Every deferred value
  carries explicit owner-pending / provisional-pending-Stage-0 / Phase-34-35-handoff
  language rather than an invented number; no ">10%" floor, no D=6.694 active scale,
  no locked np.clip gate, and no fabricated transition thresholds were introduced.
awaiting: none (resolved)

## Tests

### 1. Adaptive stage-assignment contract (CURR-01)
expected: ctl_instruction.md "Multi-Stage Data Stratification" + "Step 5" carry the Phase 33 adaptive-assignment contract — offline admitted-set EDA -> robust transforms -> PCA -> clustering -> quantile threshold augmenting the static anchors; stable integer stage labels keyed by record_key; Stage-2 hierarchical-gold and Stage-5 quasi-random-gold roles preserved; population safeguard value explicitly owner-pending the FUT EDA, with ">10%" marked superseded rather than locked.
result: pass
evidence: |
  "Multi-Stage Data Stratification by Difficulty" header at L107, "Step 5: Curriculum
  Stage Assignment" header at L1576. Methodology chain (admitted-set EDA -> robust
  transforms -> PCA -> clustering -> quantile threshold) at L318-319 and L1632.
  Stable integer stage labels keyed by record_key at L320 / L1635. Stage-2
  hierarchical-gold + Stage-5 quasi-random-gold refinement roles preserved at L323
  / L1640. Population safeguard value owner-pending at L327 / L1638; ">10%"
  phrasing marked superseded at L330 / L1639.

### 2. L_max characteristic-scale + tau_L baseline + raw-mass D (CURR-02-LMAX)
expected: Step 3 (items 2 and 5) states L_max is the characteristic angular-momentum scale, NOT a proven global maximum; the active global scale is raw-mass D ~= 4.6416 with D = 6.694 explicitly rejected; the Rosenstein-style tau_L estimator is retained as a revisable baseline with its final estimator / time-unit / fit-window / thresholds owner-pending. The shadow-trajectory method and the PCA+Rosenstein shortcut are NOT normatively adopted.
result: pass
evidence: |
  "characteristic angular-momentum scale, not a proven global maximum" at L1167.
  Raw-mass D ~= 4.6416 active convention at L984 / L990 / L1003 / L1342. D = 6.694
  explicitly rejected as provenance, not active scale, at L1342-1343. tau_L
  Rosenstein-style revisable baseline at L1309 / L1322-1323. Estimator / time-unit
  / fit-window / thresholds marked owner-pending at L1324-1325. Shadow-trajectory
  method NOT adopted at L1329. PCA+Rosenstein shortcut NOT adopted at L1333.

### 3. tau_L exclusion from IC13 (CURR-02-M7)
expected: A canonical sentence states tau_L is staging / evaluation metadata that lives OUTSIDE the 13-component IC vector (IC13) by design — trajectory-derived, not an IC invariant, used only for stage assignment and predictability-horizon evaluation, never a network input.
result: pass
evidence: |
  Canonical sentence at L1313: "tau_L is staging / evaluation metadata outside
  IC13 (D-33-06; M7" — note spec uses `IC13` notation as the 13-component
  Jacobi-state IC vector (semantically equivalent to literal "13-component IC
  vector"). Trajectory-derived qualifier at L1315. "Not an IC invariant" at
  L1317. "Predictability-horizon analysis" use at L1321. "tau_L is staging
  metadata, not a network input; it lives outside IC13" at L1339-1340.

### 4. Stage-transition state machine (CURR-03)
expected: The "Stage Transition Criteria" section reads as one coherent dual-path ADVANCE / RECOVER / HALT-REVIEW machine. ADVANCE fires only on the four-criterion success gate; RECOVER rolls back on NaN/Inf with bounded retry; HALT/REVIEW handles max-epoch / stagnation and requires an explicit owner decision for any degraded advancement. The stale pre-decision Author-note ("...test train stage 0 and see how it goes") is gone. All numeric thresholds / epoch tables are marked provisional pending the FUT Stage-0 pilot.
result: pass
evidence: |
  "Stage Transition Criteria" header at L1830. Three dispositions (ADVANCE /
  RECOVER / HALT/REVIEW) enumerated at L1836. ADVANCE permitted only on
  four-criterion success gate at L1846-1848 with criteria enumerated 1-4 at
  L1856 / L1866 / L1871 / L1879. RECOVER semantics + bounded retry at L1886-1889.
  HALT/REVIEW + owner authorization required at L1893-1902. Stale author-note
  "test train stage 0 and see how it goes" is GONE (0 matches in current spec).
  Provisional-pending-Stage-0-pilot language at L1842 / L1864 / L1877 / L1891 /
  L1905 (5 distinct locations).

### 5. Raw L_norm storage + degenerate-L_max guard (CURR-04)
expected: Step 3 item 2 stores raw, un-clipped L_norm as staging / diagnostic metadata with a mandatory nonfinite / near-degenerate L_max diagnostic-flag guard. No global clamp is authorized; the np.clip(L_norm, 0, 1) stage-gate is explicitly NOT locked and is owner-pending admitted-set evidence. The Stage 0-6 inventory is present as the complete per-stage definition+criteria set with the cumulative-replay rule and the Stage-6 catch-all.
result: pass
evidence: |
  "Phase 33 (CURR-04): raw un-clipped storage; no global clamp authorized" at
  L1206. Mandatory nonfinite / near-degenerate L_max guard at L1178-1179 with
  diagnostic-flag semantics at L1207-1208. "No global clamp is authorized" at
  L1187. np.clip(L_norm, 0, 1) stage-gate NOT locked + owner-pending at
  L1189-1191 / L1209-1210. Stage 0-6 inventory present at L264 / L266.
  Cumulative replay rule at L265 / L269. Stage-6 catch-all at L265 / L271 / L281.

### 6. Unsoftened s_min gate + dual-context epsilon (CURR-05)
expected: The Stage-6 curriculum collision gate uses unsoftened geometric s_min from the true pairwise separations; no Plummer / additive / epsilon softening is applied and the issue-doc max(s_min, epsilon) phrasing is rejected per PHYS-03. Loss-side matched-Plummer softening (epsilon_train = 1e-5) is routed to Phase 35, not the gate. The dual-context epsilon stays distinct: epsilon_inv = 1e-10 (offline invariants) vs epsilon_train = 1e-5 (training).
result: pass
evidence: |
  Stage-6 curriculum collision gate header at L286. Unsoftened geometric s_min
  at L287. "Curriculum gate does not apply any Plummer, additive, or epsilon
  softening" at L290. Issue-doc max(s_min, epsilon) phrasing rejected per
  PHYS-03 at L293-294. Loss-side matched-Plummer softening routed to Phase 35
  at L296-298 (epsilon_train = 1e-5 contract owned by Phase 35). Dual-context
  epsilon distinct: epsilon_inv = 1e-10 (offline invariants) vs epsilon_train =
  1e-5 (training) at L302-303 / L705-706.

### 7. Scope and owner-pending discipline (governance)
expected: Among framework specs, only ctl_instruction.md was edited — sampling_method.md (frozen), the read-only reports (data_quality_assessment.md, review-of-framework.md, stage_strat_revision.md), and live pinn/ code are untouched. Every deferred value carries explicit owner-pending / provisional-pending-Stage-0 / Phase-34-35-handoff language rather than an invented number; no ">10%" floor, no D=6.694 active scale, no locked np.clip gate, and no fabricated transition thresholds were introduced.
result: pass
evidence: |
  Each of the four Phase 33 plan commits (50ce5e74, 9abd0bbd, 856be399, f1f243af)
  modified ONLY ctl_instruction.md (confirmed via git show --stat --name-only).
  Protected-path integrity: git log -1 on sampling_method.md shows last touched
  916d3f84 (2026-06-07, pre-Phase-33); data_quality_assessment.md last touched
  d3fcff99 (2026-05-20, pre-Phase-33); pinn/ last commits are Phase 4 hardcoded
  path rewrite / pre-existing baseline (pre-Phase-33). `git diff` against
  sampling_method.md / data_quality_assessment.md / review-of-framework.md /
  stage-strat-revision.md / pinn/ across the phase-33 boundary returns EMPTY.
  Untracked-file check under pinn/ and framework-specs / framework-revisions
  trees returns no content files (only git-ignored macOS .DS_Store metadata,
  which is not content and does not violate SCOPE-13/14/15).
  
  Anti-pattern scan — invented-number suppression: ">10%" appears 3 times, all
  in explicit "superseded" or "NOT locked" context (L326 / L330 / L1639); D=6.694
  appears 4 times, all in "rejected provenance, not active scale" or "mass-fraction
  alternative (not adopted)" context (L995 / L1003 / L1342-1343); np.clip(L_norm,
  0, 1) appears 2 times, both in "NOT locked, owner-pending" context (L1189 /
  L1209). Owner-pending / provisional language: 7 owner-pending matches +
  12 provisional matches across the spec.

## Summary

total: 7
passed: 7
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

[none — all 7 UAT tests passed with concrete spec evidence; no fixes required]

## Notes (informational, not UAT failures)

The cross-AI plan review (33-REVIEWS.md) flagged two HIGH automation-brittleness
concerns — "Fragile Hardcoded Dirty-Doc Guard" and "Protected-path checks miss
untracked files" — and one HIGH process concern — "STOP-gap completeness not
enforced by final automated checks." These are review findings about the
*automation* used during Phase 33 execution, not about the transcribed contracts
themselves. The substantive protected-path invariant is satisfied (no untracked
content under any protected path; only git-ignored .DS_Store metadata). The
Wave 1-3 STATE.md tracking-write divergence on the combined dirty-doc hash is
documented in 33-04-SUMMARY.md §"Known Stubs" and in 33-VERIFICATION.md §8; the
genuinely user-owned protected dirty doc (cross-cutting review-resilience plan)
IS preserved unchanged (per-path hash match `034a6636ac94...`).

These automation/process findings are out of scope for the UAT contract checks
above and should be considered for Phase 36 acceptance or for the next milestone's
verification tooling — not as Phase 33 contract gaps.