---
status: complete
phase: 35-loss-energy-weight-contracts
source: [35-01-SUMMARY.md, 35-02-SUMMARY.md, 35-03-SUMMARY.md, 35-04-SUMMARY.md]
started: 2026-06-30T01:43:31Z
updated: 2026-06-30T01:43:31Z
---

## Current Test

[testing complete]

## Tests

<!--
Phase 35 is a v1.6 specwork (spec-transcription) phase: each "test" is a read-only
SEMANTIC check — does the transcribed contract in ctl_instruction.md / pinn_architecture.md
match its adjudicated verdict (modified / rejected / defer / owner-ratified) AND the negative
constraints (what must NOT be present)? Verified directly by the agent with file:line evidence
and a deterministic 16/16 cross-spec suite, corroborating (not merely re-running)
35-VERIFICATION.md. One presentation-only defect was found and fixed during this UAT (see
"Fixes Applied During UAT").
-->

### 1. LOSS-01 / NS-18+NS-12 loss scaling, units, componentwise AD, tau/u boundary
expected: pinn_architecture.md carries the LOSS-01 (NS-18 `modified`) component contract and the AC-LOSS-01-AD (NS-12 `accepted`) AD contract; ctl_instruction.md carries the LOSS-01 assembly contract. Together they state: dimensionless `u=t/T`, `r'=r/D`; projected scaled positions for Huber data loss; ordered raw masses where COM/force terms need them; matched `epsilon_train = 1e-5` in physics AND energy; data-fidelity snapshot points separate from physics/energy collocation points (energy reuses the physics collocation set); IC anchor; angular-momentum regularizer; NO linear-momentum loss; chain factors `2` and `4` apply ONLY to a direct `tau = 2u-1` leaf, not when `u` is the autograd leaf; componentwise derivatives required, summed-output VJP forbidden.
result: pass
evidence: |
  pinn_architecture.md:310 LOSS-01/NS-18 callout (dimensionless u=t/T & r'=r/D, projected
  scaled positions for Huber data loss, ordered raw mass metadata, matched
  epsilon_train = 1e-5, separate data-fidelity vs physics/energy collocation points, IC
  anchor, angular-momentum regularizer, "no linear-momentum / no-linear-momentum-loss
  term"). pinn_architecture.md:890 AC-LOSS-01-AD callout (NS-12 accepted + NS-18 modified):
  "canonical autograd leaf is u=t/T"; factors 2 and 4 "apply only to a direct tau = 2u-1
  leaf"; "Componentwise derivatives are required and the summed-output VJP remains
  forbidden". pinn_architecture.md:625 angular-momentum role ("does not authorize a separate
  linear-momentum loss"). ctl_instruction.md:1737 assembly home, preserves the Phase 34
  data-vs-collocation separation and "records that energy reuses the physics collocation
  set"; uses the full NS-12 packet path (WR-01 fix). Grounded by resolution doc §§1.12/1.14
  + evidence/ns-18-loss-scaling-units.md + evidence/ns-12-componentwise-ad.md.

### 2. LOSS-02 / M15 energy-weight schedule (reject issue-doc replacement, retain PHYS-05 lambda_E<=1)
expected: M15 transcribed as `rejected as an issue-doc replacement`; the PHYS-05 warmup schedule is retained with `lambda_E^max <= 1` (scheduled conservation weights at or below one); the issue-doc cap-table replacement (`cap = {0:1,...,6:500}`) and the stale `lambda_E = 1000` high-weight premise are rejected, NOT adopted as a locked schedule; training instrumentation must log weighted losses, scheduled weights, and gradient statistics; automatic dominance reweighting is deferred until measured weighted-loss/gradient evidence exists.
result: pass
evidence: |
  pinn_architecture.md:667 LOSS-02/M15 "rejected as issue-doc replacement" callout:
  "Retain the PHYS-05 warmup schedule above with lambda_E^max <= 1"; "issue-doc cap-table
  replacement and stale high-energy-weight premise are rejected, not adopted as a locked
  schedule"; "log weighted losses, scheduled weights, and gradient statistics; automatic
  dominance reweighting is deferred until measured weighted-loss/gradient evidence exists".
  ctl_instruction.md:1739 assembly mirror (retains PHYS-05 lambda_E^max <= 1, rejects the
  replacement). Negative suite: `cap = {0:1,1:5,2:20,3:50,4:100,5:200,6:500}` ABSENT and
  `lambda_E = 1000` ABSENT from both specs (no locked cap table; no dominance controller as
  default). Grounded by resolution doc §1.9 + evidence/m15-energy-weight-schedule.md.

### 3. LOSS-03 / NS-13 energy Huber delta (defer; delta_E = 1.0 baseline)
expected: NS-13 transcribed as `defer`; `delta_E = 1.0` retained as the configurable current baseline; calibration to a smaller range such as `0.01-0.1`, any stage-indexed Huber-delta table, and any median/quantile replacement are deferred until normalized `|Delta H|` quantiles, linear-branch occupancy, validation energy drift, and weighted gradients are measured; NO per-stage Huber-delta table is invented.
result: pass
evidence: |
  pinn_architecture.md:537 LOSS-03/NS-13 "defer / deferred calibration" callout:
  "delta_E = 1.0 for Phase 35 traceability and remains the configurable current baseline";
  "Calibration to a smaller range such as 0.01-0.1, any stage-indexed Huber delta table,
  and any median/quantile replacement are deferred until normalized |Delta H| quantiles,
  linear-branch occupancy, validation energy drift, and weighted gradients are measured".
  ctl_instruction.md:1741 assembly mirror (points to the pinn Soft Energy Conservation
  Regularizer math home; keeps delta_E = 1.0; defers stage/quantile calibration). Negative
  suite: `per-stage Huber-delta table` ABSENT. Grounded by resolution doc §1.13 +
  evidence/ns-13-energy-huber-delta.md.

### 4. LOSS-04 / D-04 causal-training mode (owner-ratified Option A; GAP-32-01 resolved)
expected: D-04 transcribed as `RESOLVED-WITH-INSTRUCTION` / owner-ratified Option A; per-time causal weighting is the default — `w_1 = 1`, `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, `eta_c = 1`; dense-residual ALM is rejected from the default loss; optional scalar-conservation ALM remains deferred P2 only; the numeric causal-exponent clip bound is deferred to FUT; Option C / windowed-causal mechanics are not commissioned; the stale "Option B = global + dense-ALM" label is superseded (not reused as the current verdict). GAP-32-01 is `RESOLVED-WITH-INSTRUCTION` / Option A in BOTH committed gap registers.
result: pass
evidence: |
  pinn_architecture.md:424 LOSS-04/D-04 callout carries the formula body
  (w_1 = 1, w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m)), eta_c = 1), "Dense-residual ALM
  is rejected from the default loss, optional scalar-conservation ALM remains deferred P2
  only, and the numeric causal-exponent clip bound is deferred to FUT. Option C
  time-windowed causal mechanics are not commissioned." ctl_instruction.md:1749 assembly
  callout points to the pinn Physics Residual Term as the canonical math home and keeps
  w_1 = 1 / eta_c = 1 — "the causal-weight formula body is defined there (see AC-LOSS-04)
  and is not restated in this assembly file" (the GAP-35-01 de-duplication). GAP-32-01
  active dual-register read: 32-GAPS.md and v1.6-GAPS.md both carry RESOLVED-WITH-INSTRUCTION
  + Option A. Negative suite: no `owner-pending` near D-04; no `Option B = global + dense`.
  Grounded by resolution doc §1.1 + 32-GAPS.md GAP-32-01 + evidence/d-04-causal-training-mode.md.

### 5. No-fabrication / source-precedence negatives (D-35-12 prohibitions)
expected: Across BOTH framework specs, none of the forbidden constructs appears as normative/default text: the energy cap table up to 500, `lambda_E = 1000`, a per-stage Huber-delta table, a numeric causal-exponent clip bound, an automatic dominance-control law, Option-C/windowed-causal as default, default dense-residual ALM, or issue-doc "Option B" as the current/default D-04 verdict. Any provenance mention of a forbidden construct carries a same-line `rejected`/`deferred`/`superseded`/`not commissioned` verdict marker (hardened per cross-AI review M2 — generic nearby negations no longer absolve a match).
result: pass
evidence: |
  Hardened cross-spec negative suite (same-line absolution per review M2) returns 0
  unabsolved forbidden-default matches across pinn_architecture.md + ctl_instruction.md;
  `lambda_E=1000` / cap table / `per-stage Huber-delta table` / numeric causal-clip bound /
  automatic-dominance / windowed-Option-C-as-default / dense-residual-as-default /
  `D-04 ... owner-pending` all absent or carry an inline deferral/rejection marker. Mirrors
  35-VERIFICATION.md Behavioral Spot-Checks "All 25 labels PASS".

### 6. Canonical-home / no-duplication (D-35-05; GAP-35-01) + B4 callout structure
expected: One canonical authoritative home per formula across the two specs. The energy-Huber loss body `L_{E} =` resolves to `pinn_architecture.md` ONLY; the causal-weight body `exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))` resolves to `pinn_architecture.md` ONLY (the ctl LOSS-04 callout points to it and does not restate the body — GAP-35-01 refined de-duplication). Each of AC-LOSS-01..04 sits inside a well-formed `> **Phase 35 contract: ...**` blockquote carrying its `LOSS-NN` id, an inline verdict, and a grounded-by source (so a stray token cannot satisfy a presence check).
result: pass
evidence: |
  D-35-05 single-home sentinels: `L_{E} =` -> [pinn_architecture.md] only;
  `exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))` -> [pinn_architecture.md] only.
  ctl_instruction.md:1749 explicitly states the causal-weight body "is not restated in this
  assembly file". B4 well-formed-callout check passes for AC-LOSS-01, AC-LOSS-02, AC-LOSS-03,
  AC-LOSS-04 (each `> **Phase 35 contract: ...**` with LOSS id + verdict + grounded-by).
  35-03 cross-ref component-section anchors (Data Fidelity Term, Physics Residual Term, Soft
  Energy Conservation Regularizer, Angular Momentum Conservation Loss) all present in pinn.

### 7. Evidence packets + Phase-32 ledger closure
expected: Four Phase 35 evidence packets exist (m15, ns-12, ns-13, ns-18); the five Phase-35-owned Phase-32 ledger rows (M15/NS-12/NS-13/NS-18/D-04) are `VERIFIED` with their packet path + AC ID + preserved verdict, and each finding's transition log records the `IN_PROGRESS -> FIX_APPLIED -> VERIFIED` chain (B3; FIX_APPLIED transient log-only per Phase 34 precedent). No new status enum or AC-ID scheme is minted; only the five owned rows are touched.
result: pass
evidence: |
  evidence/ holds m15-energy-weight-schedule.md, ns-12-componentwise-ad.md,
  ns-13-energy-huber-delta.md, ns-18-loss-scaling-units.md. 32-ISSUE-LEDGER.md: M15
  (VERIFIED, AC-LOSS-02), NS-12 (VERIFIED, AC-LOSS-01-AD), NS-13 (VERIFIED, AC-LOSS-03),
  NS-18 (VERIFIED, AC-LOSS-01), D-04 (VERIFIED, AC-LOSS-04, RESOLVED-WITH-INSTRUCTION) — all
  five carry the packet path + verdict; transition-log sections for all five record
  FIX_APPLIED (B3 lifecycle). Ledger anti-truncation anchors (## Transition Logs,
  ## Non-Headline Packet Mandate, B-07, M14, adaptive stage assignment) intact.

### 8. GAP discipline + scope + protected paths (governance closure gate)
expected: GAP-35-01 (whether D-35-05 reaches the pre-existing causal-weight formula in ctl) is `RESOLVED-WITH-INSTRUCTION` (owner instruction 2026-06-29) in 35-GAPS.md and indexed in v1.6-GAPS.md; no new STOP gap is open. Among framework specs only ctl_instruction.md and pinn_architecture.md were edited; sampling_method.md, data_quality_assessment.md, review-of-framework, stage-strat-revision, the final resolution doc, and live pinn/ code are untouched (`git diff HEAD` clean for protected paths). The pre-existing AGENTS.md instruction-file change stays SEPARATE from Phase 35 artifacts/commits (SPEC Constraints + 35-04 A5 guard). This UAT did NOT auto-advance STATE.md / ROADMAP.md (user advances per D-34-18).
result: pass
evidence: |
  35-GAPS.md GAP-35-01 Status: RESOLVED-WITH-INSTRUCTION (owner 2026-06-29, refined
  de-duplication realizing Option B's intent at Option A's cost; no Phase-34-locked content
  edited — only the Phase-35-authored ctl callout from commit 83f82219); indexed in
  v1.6-GAPS.md. No OPEN Phase 35 STOP gap. Protected-path guard (git diff HEAD --name-only
  over sampling_method.md / data_quality_assessment.md / review-of-framework /
  stage-strat-revision / 03-final-resolution.md / pinn) returns EMPTY. AGENTS.md (+6 lines,
  "GSD milestone worktree awareness") is the only out-of-domain working-tree change and is
  excluded from Phase 35 commits, per SPEC Constraints + the 35-04 A5 guard note. STATE.md /
  ROADMAP.md untouched by this UAT.

## Summary

total: 8
passed: 8
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

[none — all 8 UAT contract checks pass against concrete spec evidence; 16/16 deterministic
cross-spec checks PASS. No source-silent semantic decision arose, so no STOP gap was opened.]

## Fixes Applied During UAT

**Stale anti-truncation anchor in the uncommitted plan-hardening edits (presentation-only).**
- **Found during:** Test 6 / Test 1 deterministic anti-truncation guard.
- **Root cause:** Plan 35-02 (commit `8c61eb16`) renamed the spec heading from
  `The Multi-Component, Physics-Constrained Loss Function` (comma form) to
  `The Multi-Component Loss Function (Physics-Constrained)` (paren form) to satisfy an earlier
  substring check. The later cross-AI review-incorporation pass (uncommitted) then hardened
  the anti-truncation guard in `35-02-PLAN.md` (x2) and `35-04-PLAN.md` (x2) with the *comma*
  form — a heading that no longer exists in `pinn_architecture.md` — which would raise a FALSE
  truncation alarm if the plan guard were re-run.
- **Scope:** Limited to the uncommitted plan check strings. `35-VERIFICATION.md` is unaffected
  (its run used the current committed heading, per the 35-04-SUMMARY deviation note), so the
  recorded verification stands.
- **Fix:** Replaced the comma-form anchor with the actual current heading
  `The Multi-Component Loss Function (Physics-Constrained)` in `35-02-PLAN.md` and
  `35-04-PLAN.md`. The framework spec was NOT changed (heading is correct and semantically
  equivalent; reverting it would be needless spec churn). The two SUMMARY files that *describe*
  this deviation retain the comma form intentionally (accurate historical record).
- **Classification:** mechanical / presentation-only (matching a verification string to
  committed reality) — not a source-silent semantic decision; no STOP gap warranted.
- **Verification after fix:** the corrected anti-truncation guard passes; 0 comma-form anchors
  remain in the plan files; full 16/16 independent suite PASS.

## Closure Note

All 8 UAT contract checks pass; the single defect found (stale plan anchor) was fixed during
this UAT. No OPEN STOP gap gates closure (GAP-35-01 and GAP-32-01 are both
`RESOLVED-WITH-INSTRUCTION`).

- STATE.md already records Phase 35 as complete (transitioned to Phase 36 on 2026-06-29). This
  UAT did not modify STATE.md or ROADMAP.md; per the project convention (D-34-18) the user owns
  any STATE/ROADMAP advancement. No advancement is pending — Phase 35 is already marked complete;
  this UAT supplies the previously-missing user-acceptance layer for that completion.
- The pre-existing `AGENTS.md` working-tree change (worktree-awareness governance text) is
  user-owned and is intentionally kept OUT of every Phase 35 commit.

## Notes (informational, not UAT failures)

- These UAT checks are independent semantic reads of the transcribed contracts; they
  corroborate (do not merely re-run) the structural/source-token suite already recorded in
  `35-VERIFICATION.md` (status: passed, 4/4 must-haves).
- The literal ROADMAP/REQUIREMENTS preview wording for M15 (cap table), NS-13 (immediate
  calibration), and D-04 (Option-C preservation) is stale; `35-SPEC.md` explicitly supersedes
  it with the adjudicated verdict-status transcription, and Phase 36 reconciles ROADMAP text
  (SCOPE-13 excludes editing ROADMAP.md here).
