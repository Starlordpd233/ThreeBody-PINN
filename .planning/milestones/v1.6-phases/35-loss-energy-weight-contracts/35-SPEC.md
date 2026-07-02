# Phase 35: Loss & Energy-Weight Contracts - Specification

**Created:** 2026-06-26
**Ambiguity score:** 0.11 (gate: <= 0.20)
**Requirements:** 4 locked

## Goal

`ctl_instruction.md` and `pinn_architecture.md` carry the adjudicated Phase 35 loss-component, energy-weight, energy-Huber, and causal-training-mode contracts, with every contract transcribed by verdict status rather than by stale issue-doc or roadmap proposal.

## Background

Phase 35 runs in the v1.6 `milestone/v1.6` worktree and is spec-side only. It does not implement training code. Phase 32 seeded the issue ledger and deliberately deferred D-04 to Phase 35; M15, NS-12, NS-13, and NS-18 also remain Phase-35-owned ledger rows requiring packet-before-edit discipline. Phase 34 completed the training-loop and batch-construction contracts that Phase 35 consumes: data-fidelity points and collocation points remain logically independent, energy reuses the physics collocation set, dense-residual ALM is not part of the default loss, and optional scalar-conservation ALM remains deferred P2 only.

The active source treatment is the v1.6 adjudication protocol: the issue doc is non-authoritative, the resolution doc is the candidate verdict source, and framework-spec edits must transcribe the adjudicated verdict plus status. For Phase 35 this means the roadmap success criteria are not copied literally where the resolution doc supersedes them. In particular, the capped-hybrid `lambda_E` cap table is rejected as a replacement, the Huber-delta quantile calibration is deferred, and D-04 is now resolved by owner instruction to retain the current per-time causal weighting baseline.

## Requirements

1. **LOSS-01 / NS-18 loss scaling and units**: The framework specs transcribe the resolution-doc `modified` verdict for loss scaling and units across the canonical homes for methodology and math.
   - Current: `pinn_architecture.md` already contains the data, physics, and energy loss math, while `ctl_instruction.md` contains the training-methodology assembly skeleton and Phase 34 handoffs. The current text is not yet tagged as the Phase 35 `LOSS-01` verdict, and the stale issue-doc/roadmap wording can be misread as authorizing L1/MAE data loss or unconditional `tau` chain factors.
   - Target: `ctl_instruction.md` owns the training-methodology/assembly contract and `pinn_architecture.md` owns the component math where it already lives. Together they state the `modified` NS-18 verdict: projected scaled positions for data, Huber data loss, componentwise normalized-time derivatives for physics, matched `epsilon_train = 1e-5` in physics and energy, raw masses, shared physics/energy collocation set, IC anchor, angular-momentum regularizer, no linear-momentum loss, and chain factors `2` and `4` only when differentiating with respect to `tau` rather than when `u` is already the autograd leaf. Sources: resolution doc §1.14 / NS18-01..04, Phase 32 ledger rows NS-12 and NS-18, Phase 34 LOOP-02/03 collocation contract.
   - Acceptance: A verifier can find `AC-LOSS-01`, `LOSS-01`, `NS-18`, `modified`, and the no-linear-momentum-loss statement in the edited framework specs; can verify the `tau`/`u` derivative-factor distinction is explicit; and can verify no new normative copy contradicts the Phase 34 data-vs-collocation contract.

2. **LOSS-02 / M15 energy-weight schedule**: The framework specs transcribe the resolution-doc `rejected as an issue-doc replacement` verdict for M15 and retain the current PHYS-05 warmup schedule.
   - Current: The Phase 35 roadmap still names the issue-doc capped-hybrid schedule `lambda_E(k) = min(10^(k-3), cap[k])` with caps up to `500`, and the issue premise includes stale `lambda_E = 1000` language. The current PHYS-05 schedule in `pinn_architecture.md` has maximum scheduled conservation weights at or below `1`.
   - Target: The specs reject the issue-doc cap table and stale `lambda_E = 1000` premise as replacements; retain the current PHYS-05 warmup schedule with maximum `lambda_E <= 1`; require logging of weighted losses, scheduled weights, and gradient statistics; and keep automatic dominance reweighting deferred until measured weighted-loss/gradient evidence exists. Sources: resolution doc §1.9 / M15-01..04 / DGR-09..10, Phase 32 ledger row M15.
   - Acceptance: A verifier can find `AC-LOSS-02`, `LOSS-02`, `M15`, `rejected`, and the retained PHYS-05 maximum `<= 1` statement; can verify the cap table up to `500` is not transcribed as a locked schedule; and can verify automatic dominance reweighting is marked deferred rather than implemented as a normative rule.

3. **LOSS-03 / NS-13 energy Huber delta**: The framework specs transcribe the resolution-doc `defer` verdict for normalized-energy Huber-delta calibration.
   - Current: `delta_E = 1.0` is the configurable current baseline in the framework specs, while the issue-doc/roadmap wording suggests immediate `0.01-0.1` per-stage quantile calibration without the missing empirical distribution and branch-occupancy evidence.
   - Target: `pinn_architecture.md` keeps `delta_E = 1.0` as the configurable baseline and both framework specs state that per-stage `|Delta H|` quantile calibration is deferred pending measurement of normalized `|Delta H|` quantiles, linear-branch occupancy, validation energy drift, and weighted gradients. No per-stage Huber-delta table is invented. Sources: resolution doc §1.13 / NS13-01..03 / DGR-14, Phase 32 ledger row NS-13.
   - Acceptance: A verifier can find `AC-LOSS-03`, `LOSS-03`, `NS-13`, `defer`, and `delta_E = 1.0` baseline text; can verify the `0.01-0.1` range is described only as deferred calibration evidence, not as a locked table; and can verify the measurement prerequisites are named.

4. **LOSS-04 / D-04 causal-training mode**: The framework specs transcribe the owner-ratified Option A verdict for D-04 and resolve GAP-32-01.
   - Current: Phase 32 recorded D-04 as `DEFERRED`, with the resolution doc routing the final causal-mode choice to the framework owner. The current specs already contain per-time causal weighting with `stopgrad`, reject dense-residual pseudo-ALM, and keep optional scalar-conservation ALM as P2 only, but the owner choice was not yet ratified.
   - Target: Phase 35 records D-04 as `RESOLVED-WITH-INSTRUCTION`: retain the current per-time causal weighting baseline with `w_1 = 1`, `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, and `eta_c = 1`; preserve the dense-residual pseudo-ALM rejection as locked; keep optional scalar-conservation ALM as deferred P2 only; and defer the numeric causal-exponent clip bound to FUT. The stale issue-doc label "Option B = global + dense-ALM" is superseded and is not reused as the current verdict. Sources: resolution doc §1.1 / CAU-01..05 / GAP-01..02, Phase 32 GAP-32-01, Phase 32 ledger row D-04, Phase 34 LOOP-01 compatibility note.
   - Acceptance: A verifier can find `AC-LOSS-04`, `LOSS-04`, `D-04`, `RESOLVED-WITH-INSTRUCTION`, and `locked` causal weighting text in the edited framework specs; can verify `GAP-32-01` is marked resolved in both gap registers; can verify no dense-residual ALM is reintroduced into the default loss; and can verify the causal-exponent clip bound remains deferred rather than assigned a number.

## Boundaries

**In scope:**
- Create Phase 35 evidence packets before spec edits for M15, NS-12, NS-13, and NS-18, and consume the existing D-04 packet and gap resolution.
- Edit `ctl_instruction.md` and `pinn_architecture.md` only, with `ctl_instruction.md` canonical for training-methodology/assembly contracts and `pinn_architecture.md` canonical for component math where it already lives.
- Use stable section-heading plus AC-ID cross-references between the two specs, with one canonical home per half and no duplicated normative body text.
- Update the Phase 32 issue ledger and v1.6 tracking only as needed to reflect Phase 35-owned rows moving through `IN_PROGRESS -> FIX_APPLIED -> VERIFIED`.
- Preserve verdict status in the edited specs: `locked`, `modified`, `rejected`, `deferred`, or `owner-pending` as applicable.

**Out of scope:**
- Implementing training-loop or DataLoader code - v1.6 is specwork only; implementation remains FUT-01/FUT-04.
- Running the admitted-set EDA, Stage-0 pilot, energy-delta quantile calibration, or causal-mode A/B/C ablation - these are FUT/calibration work.
- Inventing a causal-exponent clipping bound - resolution doc GAP-01 defers it.
- Commissioning or specifying Option C time-windowed causal design - owner ratified Option A for Phase 35.
- Adopting the issue-doc `lambda_E` cap table, `lambda_E = 1000` premise, automatic dominance-reweighting law, or per-stage Huber-delta table - these are rejected or deferred by the resolution doc.
- Editing `sampling_method.md`, `data_quality_assessment.md`, `review-of-framework.md`, `stage-strat-revision.md`, or `pinn/` live code - v1.6 SCOPE-13/SCOPE-14 keep them out of Phase 35 spec edits.

## Constraints

- STOP protocol remains active for all source-silent semantic decisions. The agent must stop and surface any attempt to invent numeric schedules, thresholds, per-stage tables, or causal-mode mechanics not grounded in the approved sources.
- `pinn/` live code is not a grounding source. It may appear only in forward-looking divergence or handoff artifacts.
- Every framework-spec edit must cite the relevant resolution-doc section and ledger row by stable section/ID, not by fragile line number.
- Phase 34 transcription discipline applies: transcribe adjudicated verdict plus status, not raw proposals; use bidirectional stable-anchor cross-references; avoid duplicated normative text.
- Existing user-owned worktree changes, including instruction-file changes, must remain separate from Phase 35 artifacts and commits.

## Acceptance Criteria

- [ ] `35-SPEC.md` locks four requirements: `LOSS-01`, `LOSS-02`, `LOSS-03`, and `LOSS-04`.
- [ ] `GAP-32-01` is recorded as `RESOLVED-WITH-INSTRUCTION` in both `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md` and `.planning/milestones/v1.6-GAPS.md`.
- [ ] Phase 35 execution plans require packet-before-edit evidence for M15, NS-12, NS-13, and NS-18, and consume the existing D-04 packet plus owner instruction.
- [ ] `ctl_instruction.md` and `pinn_architecture.md` are both treated as explicit Phase 35 edit targets, with canonical-home boundaries preserved.
- [ ] The edited specs transcribe the NS-18 `modified` verdict and include the `tau`/`u` derivative-factor distinction.
- [ ] The edited specs reject the M15 cap table and stale `lambda_E = 1000` premise as replacements while retaining the PHYS-05 `lambda_E <= 1` warmup schedule.
- [ ] The edited specs keep `delta_E = 1.0` as the configurable NS-13 baseline and defer per-stage quantile calibration pending measured evidence.
- [ ] The edited specs lock D-04 Option A: per-time causal weighting retained, dense-residual pseudo-ALM rejected, optional scalar ALM deferred P2 only, causal-exponent clip bound deferred.
- [ ] No framework-spec edit introduces the issue-doc cap table, a fabricated Huber-delta table, Option-C window mechanics, a numeric causal-exponent clip bound, or default dense-residual ALM.
- [ ] Verification uses stable anchors and AC IDs (`AC-LOSS-01` through `AC-LOSS-04`) rather than line-number-only references.

## Edge Coverage

**Coverage:** 20/20 applicable edges resolved - 0 unresolved

| Category | Requirement | Status | Resolution / Reason |
|----------|-------------|--------|---------------------|
| boundary | R1 | ✅ covered | AC-LOSS-01 requires exact handling of `epsilon_train = 1e-5`, chain factors `2`/`4`, and the `tau` versus `u` differentiation boundary. |
| empty | R1 | ⛔ dismissed | Phase 35 transcribes fixed framework-spec contracts, not collection or optional-input behavior; no empty runtime input is introduced. |
| encoding | R1 | ⛔ dismissed | The requirement has no free-form user text or text-length/equality semantics; stable anchors and AC IDs handle citation representation. |
| precision | R1 | ✅ covered | AC-LOSS-01 requires the dimensionless coordinate system, raw-mass convention, and derivative-scaling distinction to prevent unit/precision mis-scaling. |
| boundary | R2 | ✅ covered | AC-LOSS-02 requires the `lambda_E <= 1` schedule boundary and rejects the cap table up to `500` plus `lambda_E = 1000`. |
| empty | R2 | ⛔ dismissed | There is no empty collection/runtime input; the contract is a schedule/status transcription over fixed source sections. |
| encoding | R2 | ⛔ dismissed | There is no text encoding behavior; formulas are represented by stable math names and AC IDs. |
| precision | R2 | ✅ covered | AC-LOSS-02 covers numeric schedule precision by retaining PHYS-05 max `<= 1` and deferring automatic reweighting until measured weighted-loss/gradient evidence exists. |
| idempotency | R2 | ⛔ dismissed | Re-running a documentation transcription is governed by git/workflow review, not by the loss-weight runtime contract. |
| concurrency | R2 | ⛔ dismissed | Concurrent editing is governed by the repo's worktree/agent-ownership policy, not by the Phase 35 loss-weight semantics. |
| boundary | R3 | ✅ covered | AC-LOSS-03 requires `delta_E = 1.0` to remain the baseline and treats `0.01-0.1` only as deferred calibration evidence. |
| empty | R3 | ⛔ dismissed | There is no empty collection/runtime input introduced by the Huber-delta transcription requirement. |
| encoding | R3 | ⛔ dismissed | There is no text encoding behavior; the requirement concerns numeric calibration status. |
| precision | R3 | ✅ covered | AC-LOSS-03 requires quantile/occupancy/drift/gradient measurement before changing `delta_E`, preventing fabricated precision claims. |
| boundary | R4 | ✅ covered | AC-LOSS-04 fixes the D-04 mode boundary: Option A retained, Option C not commissioned, no clip bound invented. |
| empty | R4 | ⛔ dismissed | The causal-mode decision does not introduce empty collection/runtime input behavior. |
| encoding | R4 | ⛔ dismissed | The requirement has no text encoding semantics; formula names and AC IDs are the representation contract. |
| precision | R4 | ✅ covered | AC-LOSS-04 keeps `eta_c = 1` and defers the numeric causal-exponent clip bound rather than inventing a precision threshold. |
| idempotency | R4 | ⛔ dismissed | Re-applying the owner decision is a documentation/governance matter; the causal-mode runtime idempotency question is out of scope for the SPEC. |
| concurrency | R4 | ⛔ dismissed | Parallel workflow safety is governed by worktree and agent-ownership rules; Phase 35 does not define concurrent runtime updates. |

## Prohibitions (must-NOT)

**Coverage:** 4/4 applicable prohibitions resolved - 0 unresolved

| Prohibition (must-NOT statement) | Requirement | Status | Verification / Reason |
|----------------------------------|-------------|--------|------------------------|
| MUST NOT transcribe stale roadmap or issue-doc proposals as final Phase 35 verdicts when the resolution doc marks them `modified`, `rejected`, or `defer`. | R1-R4 | resolved | verification: judgment; reviewers compare each edit against resolution doc §§1.1, 1.9, 1.13, and 1.14 plus the Phase 32 ledger. |
| MUST NOT fabricate deferred numeric values: no causal-exponent clip bound, no per-stage Huber-delta table, no automatic dominance-reweighting law, and no `lambda_E` cap table. | R2-R4 | resolved | verification: test; grep/assertion checks confirm forbidden numeric constructs are absent or explicitly marked deferred/rejected. |
| MUST NOT reintroduce dense-residual pseudo-ALM or describe issue-doc "Option B = global + dense-ALM" as the current/default verdict. | R4 | resolved | verification: test; grep/assertion checks confirm default loss text rejects dense-residual ALM and keeps scalar-conservation ALM deferred P2 only. |
| MUST NOT duplicate normative loss math in both framework specs or create a second canonical home conflict; one file owns methodology/assembly and the other owns component math. | R1-R4 | resolved | verification: judgment; review checks stable-anchor cross-references and confirms no contradictory duplicate normative bodies. |

## Ambiguity Report

| Dimension          | Score | Min  | Status | Notes |
|--------------------|-------|------|--------|-------|
| Goal Clarity       | 0.90  | 0.75 | ✓ | Four LOSS requirements are named and tied to source dispositions. |
| Boundary Clarity   | 0.88  | 0.70 | ✓ | User selected both framework specs as edit targets and locked canonical-home discipline. |
| Constraint Clarity | 0.86  | 0.65 | ✓ | STOP protocol, verdict-status transcription, SCOPE-13 targets, and FUT/deferred limits are explicit. |
| Acceptance Criteria| 0.82  | 0.70 | ✓ | Requirements have pass/fail checks and negative checks for stale proposals. |
| **Ambiguity**      | 0.11  | <=0.20 | ✓ | Gate passed after owner decisions. |

Status: ✓ = met minimum, ⚠ = below minimum (planner treats as assumption)

## Interview Log

| Round | Perspective | Question summary | Decision locked |
|-------|-------------|------------------|-----------------|
| 1 | Researcher | Should Phase 35 edit only `ctl_instruction.md` or both framework specs? | Both `ctl_instruction.md` and `pinn_architecture.md` are explicit targets; `ctl` owns methodology/assembly, `pinn_architecture` owns component math, with stable cross-references and no duplicated normative body text. |
| 1 | Researcher | Should D-04 be resolved now or during execution? | Resolve D-04 at the SPEC gate; Phase 35 is the terminal owner after the Phase 32 deferral. |
| 1 | Researcher | Which D-04 mode should Phase 35 lock? | Owner ratified Option A: retain per-time causal weighting; preserve dense-residual pseudo-ALM rejection; keep optional scalar-conservation ALM deferred P2 only; defer causal-exponent clip bound to FUT. |
| 1 | Researcher | Should Phase 35 copy the roadmap success criteria literally? | No; transcribe adjudicated verdict plus status. Roadmap cap-table and Huber-calibration language is stale where superseded by resolution doc §§1.9 and 1.13. |

---

*Phase: 35-loss-energy-weight-contracts*
*Spec created: 2026-06-26*
*Next step: $gsd-discuss-phase 35 - implementation decisions (how to build what's specified above)*
