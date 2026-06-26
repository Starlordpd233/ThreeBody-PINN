---
status: complete
phase: 34-training-loop-batch-construction-contracts
source: [34-01-SUMMARY.md, 34-02-SUMMARY.md, 34-03-SUMMARY.md, 34-04-SUMMARY.md, 34-05-SUMMARY.md]
started: 2026-06-25T08:19:40Z
updated: 2026-06-25T08:25:00Z
---

## Current Test

[testing complete]

## Tests

### 1. LOOP-01 replay/lookahead batch construction
expected: ctl_instruction.md "Mini-Batch Construction with Lookahead Sampling" carries the Phase 34 LOOP-01 contract — B_replay=240 (stages <= k), B_lookahead=16 (stage k+1, gated by has_stage(k+1)), n_pts(traj)=min(n_pts_cap, n_snapshots(traj)) without replacement, n_pts_cap=32 — all tagged provisional; this ctl section is the canonical batch home (SI-PINN-003); causal mode NOT locked (deferred to Phase 35); source-silent edge cases routed to GAP-34-01, not invented.
result: pass
evidence: |
  ctl_instruction.md "### Mini-Batch Construction with Lookahead Sampling" header at
  L1785. Phase 34 contract callout L1787 (LOOP-01; provisional; AC-LOOP-01; grounded by
  resolution doc §1.4 + evidence/b-07-replay-lookahead-batching.md) declaring this ctl
  section canonical (SI-PINN-003) with pinn pointing here. B_replay=240 (stages <= k) at
  L1791; B_lookahead=16 (stage k+1, gated by has_stage(k+1)) at L1792;
  n_pts(traj)=min(n_pts_cap, n_snapshots(traj)) without replacement, n_pts_cap=32 at
  L1793; all values tagged provisional (B-07 "modified") at L1795. Windowed-causal-mode
  compatibility note at L1797 — contract does NOT select or lock a causal mode; deferred
  to Phase 35 (D-04 / GAP-02). Edge cases recorded owner-pending → GAP-34-01 at L1799,
  not filled with a default.

### 2. LOOP-02 / LOOP-03 two independent point sets + mixed time sampling
expected: ctl carries LOOP-02 (data-fidelity snapshots vs collocation points as two independent sets; a single concatenated forward pass is allowed but does NOT merge loss roles; 8192/4096 provisional/example budgets) and LOOP-03 (data-fidelity 50/50 retained; collocation 50/50 deferred, not mandated). The issue-doc "applied to both sets" wording is superseded by the adjudicated B-08 deferral.
result: pass
evidence: |
  LOOP-02 callout at L1801 (provisional; AC-LOOP-02; resolution doc §1.5 +
  evidence/b-08-data-vs-collocation-points.md). Two logically independent point sets:
  data-fidelity points (L1805) and collocation points (L1806). Single concatenated
  forward pass permitted but "does not merge the loss roles" at L1808; 8192 data / 4096
  collocation tagged "provisional/example budgets (B-08 modified)" at L1808. LOOP-03
  callout at L1810: data-fidelity 50/50 (Gumbel-top-k) "retained" at L1812; collocation
  50/50 mixed sampler "deferred (B-08 / GAP-06); Phase 34 does not mandate it" at L1813.
  The ROADMAP "applied to both sets" preview wording is superseded by this deferral
  (documented in 34-VERIFICATION.md ROADMAP Staleness Note).

### 3. LOOP-04 merged gradient clipping (single canonical home, cross-file)
expected: The clipping MECHANISM clip_value = C_stage * median(recent global grad norms) is canonical in pinn_architecture.md §4.4 ONLY; the per-stage C-schedule 7-10 / 5 / 3 is canonical in ctl_instruction.md ONLY; bidirectional AC-LOOP-04 anchors resolve in both files; 8.5 is absent from both (NOT canonized); no normative clipping text is duplicated across the two files; the merged rule is recoverable as one coherent rule.
result: pass
evidence: |
  pinn_architecture.md §4.4 callout L714; mechanism "locked" L722-728 — clip is
  C_stage · median of recent global gradient norms (Adam only); pinn "owns the mechanism,
  not the schedule" and points to ctl for C_stage. Formula clip_value = C_stage *
  torch.median(...) at L747, inside Listing 6 labeled "normative spec contract — not
  executable; FUT-01/FUT-04 implements" (L736). ctl "### Adaptive Median-Based Gradient
  Clipping" callout L1825; C_stage schedule table (locked) 0-1→7-10, 2-3→5, 4-6→3 at
  L1837-1841; ctl "owns only the per-stage multiplier" and points to pinn §4.4 for the
  mechanism (L1828-1833). Cross-file: AC-LOOP-04 present in both (ctl 7×, pinn 2×); 8.5
  absent from BOTH files; clip_value=C_stage occurs only in pinn (absent in ctl — no
  duplication); Consolidated Hyperparameter Schedule Clip column points to AC-LOOP-04
  rather than restating values (L1971-1977). Merged rule recoverable as one coherent
  contract from the two cross-referenced halves with zero duplicated normative text.

### 4. LOOP-05 optional / deferred ALM contract
expected: pinn_architecture.md §4.2 carries the LOOP-05 contract — dense-residual ALM is rejected from the default loss; ALM is OFF by default; the mu_p clamp [1e-4, 100] and RMSprop-style update are carried as deferred/conditional (optional scalar-conservation ablation only). Forbidden strings "ALM is enabled by default" and dense-residual-ALM-in-default-loss are absent.
result: pass
evidence: |
  pinn_architecture.md §4.2 "Optional ALM Ablation (P2)" with LOOP-05 callout at L674
  (deferred; AC-LOOP-05; resolution doc §1.18 + evidence/alm-mu-p-clamp.md). "Default:
  ALM is OFF ... it has no mu_p and no dense-residual ALM update. Dense-residual ALM is
  rejected from the default loss." at L676. ALM "remains an optional scalar-conservation
  add-on only" at L678. mu_p clamp to [1e-4, 100] at L681; "deferred and conditional ...
  not adopted into the default training loop and may not be used until the ablation
  specification closes GAP-19" at L683. "Never apply ALM to the dense ODE residual" at
  L688. Negative checks: "ALM is enabled by default" ABSENT; no dense-residual-ALM in an
  enabling/default-loss context.

### 5. LOOP-06 dt_out scaling + LOOP-07/08 metric roles + total-loss ordering skeleton (deferred/provisional carry-forwards)
expected: LOOP-06 dt_out-aware collocation scaling is realized-as-deferred — only the dt_base/dt_out candidate direction is recorded, the inverse is explicitly NOT adopted, and there is NO probe-able n_col formula. LOOP-07/08 carry provisional training-side roles: IPR (1e-3 ALM-convergence/noise-floor), PSC (replay-buffer governance), SASD (collocation-weighting role, no formula) — each citing VAL-02/03/04 with recalibration marked FUT. The per-step total-loss ordering skeleton (forward -> L_total -> backward -> Adam-only median clip -> optimizer.step() -> optional scalar-ALM) is present with a Phase-35 forward-reference, loss internals kept opaque.
result: pass
evidence: |
  LOOP-06 callout at ctl L1819 (deferred; AC-LOOP-06; resolution doc §1.10 +
  evidence/m16-dt-out-collocation-scaling.md): "dt_out-aware collocation scaling is
  deferred to FUT"; audit direction n_col ∝ dt_base/dt_out "recorded only as a deferred
  candidate direction — not as a locked or probe-able contract"; inverse n_col ∝
  dt_out/dt_base "explicitly not adopted"; SCOPE-11/PIPE-08 "realized-as-deferred" (L1821).
  No n_col = ... formula assignment in ctl. LOOP-07 callout at ctl L770: IPR_train as
  ALM-convergence/noise-floor (provisional 1e-3), PSC for replay-buffer governance, both
  citing VAL-03/VAL-04, recalibration FUT (SCOPE-15). LOOP-08 callout at ctl L684: SASD
  provisional collocation-weighting role, "No weighting formula is invented here",
  VAL-02, FUT. Total-loss ordering skeleton at ctl L1751-1758: forward → assemble L_total
  → L_total.backward() → Adam-only median clip (refs pinn §4.4 / AC-LOOP-04) →
  optimizer.step() → optional scalar-ALM (refs pinn §4.2 / LOOP-05); loss components,
  weight schedules (λ_E, λ_L), and Huber-δ "owned by Phase 35"; L_total kept opaque.

### 6. SI-PINN-003 batch-construction reconciliation
expected: pinn_architecture.md §3.1 no longer asserts the batch-construction inconsistency (the "is not consistent with the CTL instruction plan" author comment is removed); pinn now points to ctl_instruction.md Mini-Batch Construction as canonical (PIPE-04 pointer); the SI-PINN-003 log is marked RESOLVED and SI-PINN-002 item 3 is reconciled; no duplicated ctl batch text appears in pinn (B_replay/B_lookahead absent from pinn).
result: pass
evidence: |
  pinn_architecture.md §3.1 SI-PINN-003 reconciliation callout at L351 (ctl canonical;
  AC-LOOP-02; resolution doc §1.5 claim matrix B07-04). PIPE-04 pointer at L353: the
  operative sampling rule n_pts(traj)=min(n_pts_cap, n_snapshots(traj)) is "defined
  canonically in ctl_instruction.md Mini-Batch Construction"; "A verifier confirms
  pinn_architecture.md agrees with the canonical ctl contract and carries no contradictory
  copy here." SI-PINN-002 item 3 reconciled at L1039 ("resolved under SI-PINN-003 by
  Phase 34"). SI-PINN-003 log marked "Status: RESOLVED — reconciled by Phase 34;
  ctl_instruction.md ... canonical ... pinn §3.1 now points to it via the PIPE-04 pointer
  and no longer asserts an inconsistency" at L1042-1046. Negative checks: "is not
  consistent with the CTL instruction plan" ABSENT from pinn; B_replay / B_lookahead
  ABSENT from pinn (no duplicated batch text).

### 7. Evidence packets + Phase-32 ledger closure
expected: Four Phase 34 evidence packets exist (b-07, b-08, m16, alm) mirroring the Phase 32 schema; the five LOOP-related Phase-32 ledger rows (B-07/B-08/M16/ALM/M14) are closed VERIFIED with preserved verdicts (accept-resolution / defer-with-blocker); no new status enum or AC-ID scheme is minted; D-04 and the Phase-33/35-owned rows are untouched.
result: pass
evidence: |
  evidence/ contains b-07-replay-lookahead-batching.md, b-08-data-vs-collocation-points.md,
  m16-dt-out-collocation-scaling.md, alm-mu-p-clamp.md (plus README.md + _TEMPLATE.md
  mirroring the Phase 32 schema). LOOP-04's M14 packet is correctly reused from the
  Phase 32 evidence dir (no new M14 packet, per plan). 32-ISSUE-LEDGER.md rows: B-07
  VERIFIED / accept-resolution (L18), B-08 VERIFIED / accept-resolution (L19), M14
  VERIFIED / accept-resolution (L22), M16 VERIFIED / defer-with-blocker (L24), ALM mu_p
  clamp VERIFIED / defer-with-blocker (L32) — all five with preserved verdicts and full
  Transition-Log entries citing the consuming plan + 34-VERIFICATION.md AC PASS. Status
  enum unchanged (PENDING/IN_PROGRESS/FIX_APPLIED/VERIFIED/DEFERRED); reserved AC-LOOP IDs
  only. D-04 still DEFERRED (L15, untouched); Phase-33 rows (M6/M7/D5/L_max/adaptive)
  remain VERIFIED and unchanged; Phase-35-owned rows not closed.

### 8. GAP-34-01 + scope / owner-pending discipline (governance closure gate)
expected: The source-silent LOOP-01 batch edge cases (final-stage has_stage=false, undersized lookahead pool <16, replacement/reservoir policy) are recorded as GAP-34-01 OPEN with all required STOP fields and indexed in v1.6-GAPS.md — NOT filled with an invented default. Among framework specs only ctl_instruction.md and pinn_architecture.md were edited (sampling_method.md frozen; read-only reports and live pinn/ untouched); no locked-convention regression (D~=4.6416 preserved; 8.5 and active-scale 6.694 not adopted); Phase-34 completion is NOT advanced in STATE.md. Phase-34 closure is GATED on the user resolving or deferring GAP-34-01.
result: pass
evidence: |
  GAP-34-01 in 34-GAPS.md carries all required STOP fields (Decision point / Where in
  artifact / Task context / Classification: semantic / Source silence / Mathematical-
  engineering grounding / Agent was tempted to / What the user needs to decide [A/B/C] /
  Confidence: HIGH / Status: OPEN); the three source-silent edge cases are recorded, NOT
  filled with the "tempted-to" defaults. Indexed in v1.6-GAPS.md Phase 34 section (L36),
  GAP-34-01 OPEN (L42), open_gaps: 1 / total_gaps: 7.
  Scope: the five Phase-34 spec commits (a11cd7f6, fa7d2ca6, 1009bd15, b4325ff9, 2bc15103)
  touch ONLY ctl_instruction.md and pinn_architecture.md among framework files;
  sampling_method.md last touched pre-Phase-34 (916d3f84); pinn/ last commit pre-Phase-34
  (0445db4b). Locked conventions: D~=4.6416 canonical in ctl (L1007); all ctl "6.694"
  occurrences are rejected-provenance/future-only-rewrite (L999, L1007, L1346-1347), not
  an active scale; 8.5 absent from BOTH specs; 6.694 absent from pinn.
  STATE.md: routine per-wave progress-tracking writes occurred during execution (e.g.
  9c751f86 updated current_plan/status/metrics) and STATE.md is currently CLEAN in the
  working tree; it has NOT been advanced to "Phase 34 complete" (still status: executing,
  current_plan: 2), and the 34-05 verification plan did not touch it. That completion
  advancement is correctly withheld — see Closure Gate below.

## Summary

total: 8
passed: 8
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

[none — all 8 UAT contract checks passed with concrete spec evidence; no fixes required]

## Closure Gate (gap resolved — transcription pending)

All 8 UAT contract checks pass. The Phase-34 closure gate was the OPEN owner-pending STOP
gap **GAP-34-01** (source-silent LOOP-01 batch edge cases: final-stage `has_stage(k+1)`=false,
undersized next-stage lookahead pool < 16, and the replay/lookahead replacement / reservoir
policy).

**Gate cleared 2026-06-25:** the owner ratified **Option A** via AskUserQuestion during this
UAT → GAP-34-01 marked `RESOLVED-WITH-INSTRUCTION` in `34-GAPS.md` and `v1.6-GAPS.md`
(`open_gaps: 0`). Policy A: final stage trains replay-only; undersized look-ahead (<16) is
padded by sampling **with** replacement (batch size fixed at 240+16); replay is sampled
**without** replacement across the epoch. Values inherit the LOOP-01 `provisional` tag.

**Remaining before Phase 34 can be declared complete:**
1. **Transcribe Policy A** into the `ctl_instruction.md` Mini-Batch Construction LOOP-01
   contract (replace the L1799 "owner-pending (GAP-34-01)" callout with the ratified policy)
   — routed to a follow-up Phase 34 spec-edit plan (**34-06**) under the normal packet/verify
   discipline. NOT free-handed inside this UAT flow.
2. After transcription verifies, the **user advances** Phase 34 to complete in STATE.md /
   ROADMAP.md per the project's user-advances-STATE convention (D-34-18). This UAT did NOT
   auto-transition the phase and did NOT touch STATE.md/ROADMAP.md.

Note: `34-VERIFICATION.md` §8 still records the `passed-with-closure-gate` verdict from the
2026-06-25T07:30 verification run; it should be refreshed to `passed` when plan 34-06 lands
the transcription (Phase-36 re-run will also re-confirm).

## Notes (informational, not UAT failures)

- The ROADMAP Phase 34 Success Criteria carry pre-adjudication preview wording (SC2
  "applied to both sets"; SC3 "stages 0-1: 8.5"; SC4 verbatim `n_col ∝ dt_base/dt_out`).
  These are superseded by the B-08 / M14 / M16 verdicts and are reconciled at Phase 36,
  not Phase 34 (SCOPE-13 excludes editing ROADMAP.md). Documented in 34-VERIFICATION.md
  "ROADMAP Staleness Note".
- These UAT checks are independent semantic reads of the transcribed contracts; they
  corroborate (do not merely re-run) the structural/source-token suite already recorded in
  34-VERIFICATION.md.
