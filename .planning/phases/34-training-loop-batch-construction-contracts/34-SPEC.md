# Phase 34: Training-Loop & Batch-Construction Contracts — Specification

**Created:** 2026-06-24
**Ambiguity score:** 0.176 (gate: ≤ 0.20)
**Requirements:** 9 locked

## Goal

`ctl_instruction.md` and `pinn_architecture.md` carry the training-loop and batch-construction contracts (LOOP-01..08) as normative spec contracts — each transcribed at the **adjudicated verdict and its status** (locked / provisional / deferred / owner-pending) per the doc-03 resolution doc and the Phase 32 issue ledger, with source citations, reconciled with the Phase 32 verdicts and the locked v1.4/v1.5 conventions — and the `pinn_architecture.md` ↔ `ctl_instruction.md` batch-construction inconsistency (SI-PINN-003) is reconciled with `ctl_instruction.md` as canonical. No training-loop code is written (FUT-01/FUT-04).

## Background

Phase 34 is the fifth executed phase of v1.6 ("Resolving 03 Curriculum and Training Loop", phases 30–36, branch `milestone/v1.6`, **specwork-only**). Phases 30–32 stood up the external research package, verified the resolution doc (`research_reports/03-curriculum-and-training-loop/`), and adjudicated the headline conflicts into the Phase 32 issue ledger. Phase 33 locked the curriculum-stage contracts (CURR-01..05) into `ctl_instruction.md` and explicitly **deferred the training-loop / batch-construction mechanics to Phase 34**.

Current spec state (grounded in the files):
- **`ctl_instruction.md`** already carries *partial* training-loop content (the "Phase 2 — Definitive CTL-PINN Training Loop" section, ~lines 1643–1945): a two-phase Adam→L-BFGS overview, a partial "Mini-Batch Construction with Lookahead Sampling" block (`B_replay=240` / `B_lookahead=16`, `n_pts_cap=32`, a 50/50 weighted/uniform split via Gumbel-top-k), an "Adaptive Median-Based Gradient Clipping" block citing M14, and 4 ADVANCE stage-transition criteria. It does **not** yet carry: a formalized batch-construction contract reconciled to the B-07/B-08 verdicts, the two-independent-point-set contract, the ALM parameter-update contract, the `dt_out`-aware collocation-scaling contract, or the training-side use of the v1.5 metrics (IPR/PSC/SASD).
- **`pinn_architecture.md`** carries the loss components (§3) and a training-strategy section (§4) including an adaptive-gradient-clipping pseudocode block. §3 carries an author comment that its batch construction "is not consistent with the CTL instruction plan" — the **SI-PINN-003** inconsistency, conflicting with `ctl_instruction.md`'s Mini-Batch Construction.

The driving tension: the ROADMAP's LOOP-01..08 success criteria were authored mirroring the audit/issue-doc *proposals*, but the authoritative resolution doc (`03-final-resolution.md`) + Phase 32 ledger **modified / deferred / surfaced-to-owner** several of them. Phase 34 therefore transcribes the *adjudicated outcome and its status*, not the raw proposals — the pattern Phase 33 already established (CURR-04 recorded the M6 `np.clip` gate as owner-pending/not-locked; CURR-05 deferred matched-Plummer softening to Phase 35).

## Requirements

1. **LOOP-01 — Replay/lookahead batch-construction contract**: Define the replay/lookahead trajectory-batch contract in `ctl_instruction.md`.
   - Current: Partial Mini-Batch Construction block exists (`B_replay=240`, `B_lookahead=16`, `has_stage(k+1)` implied) but is not reconciled to the B-07 verdict or the D-04 causal-mode boundary; edge policies absent.
   - Target: Contract states `B_replay=240` (from `D_≤k`) + `B_lookahead=16` (from `D_{k+1}`) with the `has_stage(k+1)` guard, **tagged provisional** (B-07 `modified`: "provisional defaults, not verified optimums"), cited to the resolution doc / ledger. Batch construction is specified as **compatible with, not selecting,** a windowed causal mode — i.e. it does not preclude a windowed mode that excludes future-window trajectories should D-04 later choose one; the causal-mode decision itself is deferred to Phase 35 (owner-pending) with a forward-reference.
   - Acceptance: `ctl_instruction.md` contains the 240/16 + `has_stage` contract with an explicit `provisional` status tag, a source citation (resolution-doc/ledger line ref), and a forward-reference recording that the causal-mode selection is Phase 35 / owner-pending; no causal mode is locked in Phase 34.

2. **LOOP-02 — Two-independent-point-set contract**: Define the data-fidelity vs collocation point-set separation.
   - Current: Not formalized as a contract; `pinn_architecture.md` §3 conflates batch construction (SI-PINN-003).
   - Target: Contract states two logically independent point sets — data-fidelity points (Brutus snapshots, L1/MAE/Huber data loss) kept distinct from collocation points (`[0,T]`, physics + energy loss), even when sharing trajectory IDs; a single concatenated forward pass is permitted but does **not** merge the loss roles. The `8192/4096` figures are tagged **provisional/example budgets** (B-08 `modified`); actual data count follows the per-trajectory cap.
   - Acceptance: The two-point-set contract appears with the loss-role separation stated, the single-forward-pass allowance noted, and `8192/4096` carried with a `provisional` tag + citation.

3. **LOOP-03 — Mixed time-sampling contract**: Define the 50% uniform + 50% acceleration-weighted time sampling.
   - Current: A 50/50 weighted/uniform split exists for data points in the Mini-Batch block; collocation sampling not contract-bound.
   - Target: For **data-fidelity points**, the existing 50/50 (uniform + acceleration-weighted, without replacement) split is **retained** (B-07). For **collocation points**, a *mandatory* 50/50 mixed continuous sampler is recorded as **deferred** (B-08 `deferred`) with a forward-reference — Phase 34 does not mandate it. The ROADMAP "applied to both sets" wording is reconciled to this split status.
   - Acceptance: `ctl_instruction.md` states 50/50 retained for data-fidelity points and 50/50 **deferred (not mandated)** for collocation points, each with status tag + citation; no mandatory collocation 50/50 is locked.

4. **LOOP-04 — Merged gradient-clipping contract**: Define adaptive median-based clipping.
   - Current: An adaptive median-based clipping block exists in `ctl_instruction.md` (and a pseudocode block in `pinn_architecture.md` §4) citing M14.
   - Target: Contract states `clip_value = C_stage · median(grad_norm_history)` with the per-stage `C_table` (stages 0–1: 8.5; 2–3: 5.0; 4–6: 3.0) and a rolling window, **tagged locked** per the M14 `modified`/adopted verdict, cited. The two clipping descriptions (ctl + architecture) are made consistent (see R9 / SI-PINN-003).
   - Acceptance: The merged-clipping contract with `C_table` appears consistently in the canonical location, tagged `locked` per M14, with citation; the architecture-file description references rather than contradicts it.

5. **LOOP-05 — ALM parameter-update contract**: Define the ALM `λ_p`/`μ_p` update and `μ_p` clamp **at its adjudicated status**.
   - Current: No ALM parameter-update contract; `pinn_architecture.md` §4.2 notes an "Optional ALM Ablation".
   - Target: Per the ALM clamp verdict (`defer`) — dense-residual ALM is **rejected** from the default loss; ALM remains an **optional scalar-conservation** add-on only. The `λ_p`/`μ_p` RMSprop-style moving-average update under `torch.no_grad()` and the `μ_p` clamp `[1e-4, 100]` are transcribed as a **deferred / conditional** contract (applicable only to the optional scalar-ALM ablation once it defines constraint normalization, penalty-update law, state reset/persistence, and cadence) — **not** locked into the default training loop. The ROADMAP LOOP-05 wording is reconciled to this deferred status.
   - Acceptance: The spec records ALM as optional/non-default with the `μ_p` clamp `[1e-4,100]` carried as **deferred (not adopted in the default loss)** + citation; the default training-step contract does **not** include a dense-residual ALM update.

6. **LOOP-06 — `dt_out`-aware collocation-scaling contract**: Realize the v1.5 SCOPE-11 / PIPE-08 forward-reference.
   - Current: M16 collocation-density question marked deferred; not in the current spec.
   - Target: Contract transcribes the audit M16 line-163 **direction** `n_col ∝ dt_base / dt_out` as a **provisional / forward-referenced** contract realizing the v1.5 SCOPE-11/PIPE-08 forward-reference; the **inverse form is an explicit future methodology change and is NOT transcribed**.
   - Acceptance: `n_col ∝ dt_base/dt_out` appears tagged `provisional` with the M16 citation and an explicit note that the inverse form is not adopted; the v1.5 SCOPE-11/PIPE-08 forward-reference is marked realized.

7. **LOOP-07 — Training-side use of IPR and PSC**: Define the training-side roles of the v1.5-provisional metrics.
   - Current: VAL-03 (IPR) / VAL-04 (PSC) left provisional in v1.5 with forward-references to doc-03.
   - Target: Contract states IPR as the ALM-convergence / noise-floor signal (provisional `1e-3` carried, **confirmed-or-recalibrated only by a disposable formula-sanity probe**, never an EDA run per SCOPE-15) and PSC for replay-buffer governance (provisional grid/normalization/SCR carried). Both tagged `provisional` with v1.5 VAL-03/VAL-04 forward-references; no empirical recalibration is performed in-phase.
   - Acceptance: IPR (`1e-3`) and PSC training-side roles appear tagged `provisional` with VAL-03/VAL-04 citations; the spec states recalibration is FUT (SCOPE-15), not done here.

8. **LOOP-08 — SASD training-side collocation-weighting**: Realize the v1.5 VAL-02 deferral.
   - Current: VAL-02 explicitly deferred "training-side collocation weighting" to doc-03 with a recorded forward-reference.
   - Target: Contract records the SASD training-side collocation-weighting role as a **provisional / forward-referenced** contract per the VAL-02 deferral; no weighting formula is invented beyond what the source supports.
   - Acceptance: The SASD training-side collocation-weighting role appears tagged `provisional` with the VAL-02 citation; nothing beyond the source is fabricated.

9. **SI-PINN-003 reconciliation**: Resolve the batch-construction inconsistency between the two spec files.
   - Current: `pinn_architecture.md` §3 carries the author comment that its batch construction "is not consistent with the CTL instruction plan", conflicting with `ctl_instruction.md`'s Mini-Batch Construction.
   - Target: `ctl_instruction.md` is designated the **canonical** batch-construction contract; `pinn_architecture.md` is updated to **reference** it (and the SI-PINN-003 comment removed/resolved), removing the inconsistency.
   - Acceptance: `pinn_architecture.md` no longer asserts an inconsistency with the CTL batch-construction plan; it references the canonical `ctl_instruction.md` contract, and a verifier confirms the two files agree on batch construction.

## Boundaries

**In scope:**
- Transcribing LOOP-01..08 into `ctl_instruction.md` and `pinn_architecture.md` as normative spec contracts, each at its adjudicated verdict + status (locked / provisional / deferred / owner-pending) with source citations.
- Reconciling SI-PINN-003 with `ctl_instruction.md` canonical (R9).
- The per-step total-loss **assembly skeleton** in the training-step contract — showing *where* `L_total` enters backward → gradient-clip → optimizer.step → (optional) ALM update, treating loss terms as opaque inputs with a forward-reference to Phase 35.
- Recording the source-silent batch-construction edge cases (final stage, undersized lookahead, replacement policy) as a documented deferred/owner-pending contract gap (candidate `34-GAPS.md` entry).
- Disposable formula-sanity probes (per SCOPE-15) only, to sanity-check transcribed contracts before locking.

**Out of scope:**
- Loss-component **scaling**, the `λ_E` energy-weight schedule, Huber-δ calibration, and the causal-training-mode selection — these are Phase 35 (the training-step contract references them via forward-reference only).
- The curriculum-stage definitions / `tau_L` / `L_max` / stage-transition state machine — locked by Phase 33 (CURR-01..05); Phase 34 consumes, does not re-decide.
- Any FUT-01/FUT-04 implementation — DataLoader, batch constructor, ALM update mechanics, causal-window mechanics (SCOPE-14: contracts only, no code).
- The adaptive-stage-assignment EDA and Stage-0 pilot / threshold calibration (SCOPE-15: FUT).
- Editing `sampling_method.md` (frozen, SCOPE-08), `data_quality_assessment.md`, `review-of-framework.md`, `stage-strat-revision.md` (read-only, SCOPE-09), or any `pinn/` live code (no-live-code directive).
- Re-adjudicating D-04 / D-05 / D-06 / M14 / the D-value conflict — locked by Phase 32; the issue ledger is canonical.

## Constraints

- **Spec-edit targets (SCOPE-13):** `ctl_instruction.md` and `pinn_architecture.md` ONLY.
- **Locked v1.4/v1.5 conventions (SCOPE-12) must remain intact:** 14D input `[τ, IC₁₃]`; Jacobi IC frame with mass-weighted COM projection head; `eps_soft = 1e-5` (PHYS-03); post-v1.3 SCS gate (`ε_H > 10⁻⁵` / `SCS > −5`); raw-mass `D ≈ 4.6416` (`D = 6.694` rejected, v1.5 EVID-10); DataLoader contracts PIPE-01..10; validation metrics VAL-01..04.
- **Grounding / STOP protocol:** the doc-03 resolution doc + Phase 32 issue ledger are the candidate verdict sources; where they are silent, Phase 34 records a gap and does not invent.
- **No empirical recalibration (SCOPE-15):** provisional thresholds (IPR `1e-3`, PSC, per-stage values) are carried with forward-references; only disposable formula-sanity probes are permitted.

## Acceptance Criteria

- [ ] All 9 requirements (LOOP-01..08 + SI-PINN-003) appear in the named file(s) with (a) adjudicated content, (b) an explicit status tag (locked / provisional / deferred / owner-pending), (c) a source citation (resolution-doc / Phase-32-ledger line ref), (d) reconciliation with the relevant Phase 32 verdict.
- [ ] LOOP-01 records causal-mode as Phase-35 / owner-pending (compatibility, not selection); no causal mode is locked.
- [ ] LOOP-05 keeps dense-residual ALM out of the default training-step contract; the `μ_p` clamp `[1e-4,100]` is carried as deferred/optional, not locked.
- [ ] LOOP-06 transcribes `n_col ∝ dt_base/dt_out` (provisional) and explicitly does NOT transcribe the inverse form.
- [ ] The per-step total-loss assembly skeleton references Phase 35 for components/weights (no `λ_E` schedule or Huber-δ defined in Phase 34).
- [ ] SI-PINN-003 is reconciled: `pinn_architecture.md` references the canonical `ctl_instruction.md` batch-construction contract and no longer asserts an inconsistency.
- [ ] The source-silent batch edge cases are recorded as a deferred/owner-pending contract gap (not filled with an invented default).
- [ ] **Locked-convention regression check passes:** D≈4.6416 present and `6.694` absent; 14D `[τ,IC₁₃]`, Jacobi COM head, `eps_soft=1e-5`, post-v1.3 SCS gate, and PIPE-01..10 / VAL-01..04 references intact (unregressed).
- [ ] **Scope check passes:** only `ctl_instruction.md` and `pinn_architecture.md` are modified; no edits to frozen/read-only spec files or `pinn/` code.

## Edge Coverage

**Coverage:** 0/1 applicable edges specified · 1 recorded as deferred contract gap · 0 unresolved-and-unflagged

| Category | Requirement | Status | Resolution / Reason |
|----------|-------------|--------|---------------------|
| Boundary / undefined-input | LOOP-01 | ⚠ DEFERRED (recorded contract gap) | Final-stage (`has_stage(k+1)`=false), undersized next-stage lookahead pool (<16), and replacement policy are flagged by B-07 as "must be made deterministic" but the source is SILENT on the policy. Per STOP protocol Phase 34 records this as an owner-pending / source-silent contract gap (candidate `34-GAPS.md`) — NOT filled with an invented default. Planner must treat as deferred. |

## Prohibitions (must-NOT)

**Coverage:** 4/4 applicable prohibitions resolved · 0 unresolved

| Prohibition (must-NOT statement) | Requirement | Status | Verification / Reason |
|----------------------------------|-------------|--------|------------------------|
| MUST NOT fabricate a locked value/contract where the source defers — record the provisional/deferred status instead | all | resolved | verification: judgment (each transcribed contract must carry its adjudicated status tag + citation; a verifier reviews for invented locks) |
| MUST NOT regress `D ≈ 4.6416` or reintroduce `D = 6.694` | constraints | resolved | verification: test (grep both files: `4.6416` present, `6.694` absent) |
| MUST NOT edit frozen/read-only spec files (`sampling_method.md`, `data_quality_assessment.md`, `review-of-framework.md`, `stage-strat-revision.md`) or any `pinn/` live code | boundaries | resolved | verification: test (git diff path check — only `ctl_instruction.md` + `pinn_architecture.md` changed) |
| MUST NOT implement FUT-01/FUT-04 code (contracts only; pseudocode transcribed as normative spec text, never executed) | boundaries | resolved | verification: judgment (no runnable training-loop / DataLoader code added to spec files; transcription stays declarative) |

## Ambiguity Report

| Dimension          | Score | Min  | Status | Notes                                                        |
|--------------------|-------|------|--------|--------------------------------------------------------------|
| Goal Clarity       | 0.85  | 0.75 | ✓      | Fidelity principle (verdict+status+citation) locked          |
| Boundary Clarity   | 0.85  | 0.70 | ✓      | 34↔35 loss cut + SI-PINN-003 + D-04 boundary all resolved     |
| Constraint Clarity | 0.75  | 0.65 | ✓      | SCOPE-12/13/14/15 + STOP-protocol grounding explicit          |
| Acceptance Criteria| 0.82  | 0.70 | ✓      | Phase-33-style per-LOOP UAT + regression + scope check        |
| **Ambiguity**      | 0.176 | ≤0.20| ✓      |                                                              |

Status: ✓ = met minimum, ⚠ = below minimum (planner treats as assumption)

## Interview Log

| Round | Perspective          | Question summary                                  | Decision locked                                                              |
|-------|----------------------|---------------------------------------------------|------------------------------------------------------------------------------|
| 1     | Researcher           | How to transcribe LOOP-01..08 (proposal vs verdict)? | Verdict + status + citation, faithfully; deferrals → forward-references      |
| 1     | Boundary Keeper      | Where does total-loss assembly live (34 vs 35)?   | Skeleton in 34; loss components/weights/Huber-δ/causal mode in 35            |
| 1     | Boundary Keeper      | Is SI-PINN-003 reconciliation in scope?           | Yes — reconcile, `ctl_instruction.md` canonical                              |
| 2     | Failure Analyst      | How is Phase 34 verified "done"?                  | Phase-33-style per-LOOP UAT + locked-convention regression + scope check     |
| 2     | Boundary Keeper      | How does LOOP-01 treat the owner-pending D-04 mode? | Compatibility, not selection; mode decision deferred to Phase 35            |
| Probe | Edge / Failure       | Source-silent batch edge cases (final/undersized) | Record as deferred owner-pending contract gap; do NOT invent a default       |
| Probe | Prohibition          | Which must-NOT criteria?                           | All four (anti-fabrication, D-value, frozen-file scope, FUT-01 no-code)       |

---

*Phase: 34-training-loop-batch-construction-contracts*
*Spec created: 2026-06-24*
*Next step: /gsd-discuss-phase 34 — implementation decisions (how to transcribe the specified contracts)*
