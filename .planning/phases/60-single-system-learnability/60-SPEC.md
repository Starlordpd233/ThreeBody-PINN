# Phase 60: Single-System Learnability — Specification

**Created:** 2026-10-17
**Ambiguity score:** 0.07 (gate: ≤ 0.20)
**Requirements:** 8 locked

## Goal

Phase 60 answers whether the production network can learn one Stage-0 system to physical accuracy: first on the gold record it is scored on, then from the physics, but only if that ceiling does not end the ladder.

## Background

Phase 59 froze the scorecard, the panels, and Gate G1 (`proceed`). No learnability harness exists. The Phase 38 overfit probe trains a data term on a zero IC13 placeholder. The trainer's loss functions live in `pinn/loss_catalog.py` and `pinn/training/controllers.py`. The trainer's numeric pools accept only hierarchical base keys (`pinn/data/batches.py`).

The frozen scorecard grades every tier on the gold sibling (`tier_defining: gold_sibling`). Hierarchical base output step is 0.08; hierarchical and standard gold are 0.01; standard base is 0.17 (`ctl_instruction.md` footer defaults). Panel systems 1632, 851, and 4658 have inner-lap counts 10.47, 18.61, and 39.35. On the 0.08 grid that is 11.94, 6.72, and 3.18 base samples per inner lap. The gold grid gives system 4658 about 25 samples per lap.

`feasibility_scorer.network_trajectory` crashes on MPS when it widens with one `.to(device="cpu", dtype=float64)` call (GAP-59-13). Phase 59 left the shared scorer byte-unchanged and forwarded the fix to this phase.

`decision_verdict` refuses later-rung inputs once G2 has fired. `g2_fires` counts only tiers strictly below 1 and fires at 2 or more. `tier_of` uses inclusive cuts (`inclusive_le`): a non-finite `E` is Tier 0, and a non-finite `ε_H` fails every level that has an energy condition, so `E ≤ 0.1` with non-finite `ε_H` is Tier 1.

## Requirements

1. **Scope amendment**: One amendment, committed before any real rung, inserts the locked sentences into `REQUIREMENTS.md` and `ROADMAP.md`. The frozen scorecard file is byte-unchanged.
   - Current: SCOPE-39 names two exceptions. FEAS-04 and roadmap success criterion 3 require Rung 2 with no skip. FEAS-09 and SCOPE-44 run the probes only if G2 passes.
   - Target: SCOPE-39 names the gold data-only arms as a third exception. FEAS-04 and roadmap success criterion 3 skip Rung 2 when the ladder stops at G2. FEAS-09 and SCOPE-44 run the probes only if the ladder continues past G2. On an owner continue, the uncovered panel system gets one data-only Rung 1 at the approved setting, and every remaining Phase 60 arm uses that setting.
   - Acceptance: After collapsing whitespace, the inserted sentences match the **Amendment text** below. The scorecard SHA-256 is unchanged.

2. **Learnability harness**: `pinn/verification/` gains a tested harness that extends the Phase 38 probe. It trains the production architecture on one named training-split system under a named loss arm and writes a diagnostic run record.
   - Current: The Phase 38 probe uses a zero IC13 placeholder and a data-loss ratio gate. No harness record exists for the graded-run path to refuse.
   - Target: Real normalized IC13. The trainer's own loss and residual functions, with no re-implementation. Adam, then the frozen full-batch L-BFGS polish, both states scored. Diagnostic overrides of `first_omega_0` only on data-only sweep arms, written into the run record. Test-split paths refused. Graded-run and evaluator paths refuse a harness record, including one with an override. An override is refused on an arm with a physics term. A data-only arm's weights do not initialize another run.
   - Acceptance: Tests prove INST-05 (a)–(e). The short run in (d) uses a fixture and a test evidence root. It is not a Rung 1 result, and a second test invocation does not replace a committed real-arm record.

3. **Scorer fix**: Before any network is scored, `network_trajectory` widens an MPS float32 tensor by moving it to the CPU and then to float64. An MPS regression test passes. The new scorer SHA-256 is recorded. Phase 59 evidence that pins the old hash is not re-run.
   - Current: One `.to(device="cpu", dtype=float64)` call raises `TypeError` on an MPS tensor. JX-4 used a byte-equivalent copy in the Phase 59 driver.
   - Target: The shared scorer is safe on MPS. Official metric arithmetic stays float64 on the CPU. A CPU float64 re-score of the same weights is reported beside the official score.
   - Acceptance: The MPS regression fails on the old one-call widen and passes on CPU-then-float64. On a CPU float64 network the widened path matches `score_network` field for field. If the cross-check tier or the counts-boolean differs, the arm stops for the owner. The better of the two scores is never taken.

4. **Run protocol**: A Phase 60 run-protocol file is committed before the first real rung. Every real-arm record cites its SHA-256, together with the seed, runtime, torch and macOS versions, code commit, config hash, scorecard SHA-256, scorer SHA-256, protocol SHA-256, wall hours, seconds per step, and the SHA-256 of each scored state's weights.
   - Current: No protocol file exists. The scorecard does not name the harness seed or runtime.
   - Target: Seed 42 and MPS float32 for Adam and the polish on every real arm: Rung 1, Rung 2a, Rung 2b, the four sweep arms, the confirmation, the uncovered-system Rung 1, and both probe arms. `resolve_runtime` is not consulted. The first completed run is the result. Re-deriving a result re-scores the committed weights and does not retrain.
   - Acceptance: A record missing any required hash or version field is invalid. A second seed, or a second fresh training run, is not the result.

5. **Rung 1 and Gate G2**: Rung 1 trains on the hierarchical gold record (output step 0.01) for systems 1632, 851, and 4658, at `first_omega_0 = 30`, under the frozen budget rule and polish. Gate G2 is the frozen `g2_fires` result.
   - Current: The three IDs and the G2 grid `[60, 120, 240, 480]` are frozen. No Rung 1 result exists.
   - Target: Each system records the budget-rule trail, both optimizer states and which is better, tier, `E`, inner-pair error, valid horizon at 1% and 10%, `ε_H`, the base-grid scores beside the gold-grid scores, the formula comparison, whether it counts, the trace, and the wall hours. The official tier uses the gold grid. An inconclusive arm enters G2 at the tier of its result. G2 does not wait for more budget.
   - Acceptance: `g2_fires` on the three tiers matches the recorded outcome. Exactly one system below Tier 1 does not fire. Tier exactly 1 does not fire. `E` exactly 0.1 is Tier 1. A non-finite `E` is Tier 0. A non-finite `ε_H` caps the tier at 1 when `E ≤ 0.1`, and the tier is 0 when `E > 0.1`. Equal formula error does not count (`position < formula`).

6. **Settings sweep**: If G2 fires, all four data-only settings run, in order 60, 120, 240, 480, even after a success. "Reaches Tier 1" means the arm result, the better of Adam and polish by the frozen lexicographic rule, is Tier 1 or higher.
   - Current: The scorecard names one confirmation and the first and second failing systems. It does not say which setting is confirmed when several reach Tier 1.
   - Target: The lap counts 10.47, 18.61, and 39.35 pin the pair. All three fail, or 1632 and 851 fail: sweep 1632, confirm on 851. 1632 and 4658 fail: sweep 1632, confirm on 4658. 851 and 4658 fail: sweep 851, confirm on 4658. The confirmation is the highest `first_omega_0` that reached Tier 1, one run, same seed, runtime, gold grid, budget rule, and polish. Zero Tier ≥ 1 settings means no confirmation and no rescue. Other Tier ≥ 1 settings are listed as "reached Tier 1, not confirmed (one-confirmation budget)". The four-setting curve (tier, `E`, `ε_H`, valid horizon) is part of the checkpoint ④ record.
   - Acceptance: The recorded sweep system, confirmation system, and confirmed omega match that rule. No setting between the grid points is run. A confirmed rescue raises the frozen `OwnerRouted` checkpoint and does not continue by itself.

7. **Rung 2 and the probes**: Rung 2 and the hard-stage probes run only if the ladder continues past G2. While checkpoint ④ is unanswered, Phase 60 does not run them, does not skip them, and does not close.
   - Current: FEAS-04 has no skip clause. FEAS-09 runs only after G2 passes, so a rescue would skip the probes even if the owner continued.
   - Target: If G2 did not fire, Rung 2 and the probes run at the locked setting. If the owner continues, they run at the approved `first_omega_0`, and the panel system that neither the sweep nor the confirmation covered gets one data-only Rung 1 at that setting first. Rung 2a has no data term. Rung 2b trains on the hierarchical base record (0.08). Probe Rung-1 arms train on the standard gold record (0.01) of `standard/base/2279` and `standard/base/3418`. Probe Rung-2b trains on the standard base record (0.17) for 2279 and on the standard gold record (0.01) for 3418. If the ladder stopped, Rung 2 and FEAS-09 are skipped. Level 3 is reported as "not tested (skipped at G2)", not "not reached". Skipped results are not passed into `decision_verdict`.
   - Acceptance: A skip record uses only `no rescue` or `checkpoint ④ answered go to the verdict`. Once any Rung-2 arm has started, a skip cannot be recorded. Probe arms are not counted: the harness never calls `counts()` for them and records the formula as `not applicable: no hierarchical split`. On a counted system, a missing formula still raises `OwnerRouted`.

8. **Records, resume, and closeout**: Every assigned train or score record is checked before the first arm launches. An arm that cannot resume goes to the owner. Machine hours and measured seconds per step are recorded per arm.
   - Current: No Phase 60 preflight or resume rule exists. `polish_should_stop` compares polish wall time with a fraction of Adam wall time and does not define an interruption.
   - Target: Missing, empty, or unreadable covers the record an arm trains on and the record it is scored on, including Rung 2a's gold score record. No substitute fidelity and no substitute system. A blocked Rung-1 arm makes G2 impossible, because `g2_fires` requires exactly three tiers. An interrupted arm resumes from its checkpoint, including through the polish. Adam's running time is the sum across segments, not calendar time that includes the interruption. The step budget is not re-timed on resume. The polish cap is 25% of that summed Adam time, or five outer calls without improvement, whichever the frozen function reaches first. On no rescue, Phases 61–63 are marked skipped by G2, not failed, and Phase 64 is next. One seed per arm is a stated limit for the verdict, not a reason to add seeds.
   - Acceptance: A blocked record produces no arm and no fallback. A resume does not change the step budget. A silent restart is not a result. The three frozen `OwnerRouted` cases stop the work: a missing formula on a counted system, a rescue, and an extended arm whose improvement rate cannot be computed. The harness does not catch them and retry.

## Amendment text

Compare after collapsing whitespace.

**SCOPE-39.** Stage-0 only, with three read-only or diagnostic exceptions: FEAS-08's survey of training-split data for every stage; FEAS-09's two single-system diagnostic probes on Stage-4b and Stage-6 systems; and the data-only arms (Rung 1, the G2 sweep and its confirmation, and the probes' Rung-1 arms), which train on their own system's gold record, the record the frozen scorecard grades them on. Arms with a physics term train on the data their stage's recipe assigns. No data-only arm's weights start another run. No curriculum training beyond Stage 0, no PLAT-01..07. SCOPE-36 is carried forward.

**FEAS-04, last acceptance bullet.** Rung 2 runs only if the ladder continues past G2: G2 passed, or the owner continued at checkpoint ④. Otherwise FEAS-04 is recorded as skipped, with one of the pre-registered reasons: no rescue, or checkpoint ④ answered go to the verdict.

**Roadmap success criterion 3, added sentence.** If the ladder stopped at G2, Rung 2 is recorded as skipped.

**FEAS-09.** The probes run only if the ladder continues past G2. On a continue they use the approved setting. If the ladder stopped at G2, FEAS-09 is recorded as skipped, with one of the same two reasons.

**SCOPE-44.** The hard-stage probes run only if the ladder continues past G2.

**Checkpoint ④ continue.** The owner-approved `first_omega_0` is the setting for the uncovered system's data-only Rung 1, for Rung 2, and for both probe arms. Phase 60 does not edit `pinn_architecture.md`. The approved value is the ladder's setting for those arms, not a diagnostic override, and a physics arm still refuses an override the owner did not approve.

## Boundaries

**In scope:**
- The SCOPE-39 / FEAS-04 / FEAS-09 / SCOPE-44 / roadmap amendment above
- The learnability harness and INST-05 tests (a)–(e)
- The in-place GAP-59-13 scorer fix and its MPS regression test
- The run protocol, committed before the first real rung
- Rung 1 on 1632, 851, and 4658
- The G2 sweep, confirmation, and checkpoint ④ hold
- Rung 2a and Rung 2b when the ladder continues
- The uncovered system's data-only Rung 1 when the owner continues
- The two hard-stage probes when the ladder continues
- Skip records, machine hours, and the Phase 64 handoff on a stop

**Out of scope:**
- Editing the frozen scorecard — its hash is an acceptance check
- Editing `pinn_architecture.md` or the other framework specs — SPEC-07..10 belong to Phase 61, and this phase changes no recipe value in those files
- Conformance, per-slot physics, telemetry, and the observe-only trainer modes — Phase 61
- Rung 3, the 16-system family, and the validation-panel accuracy curve — Phase 62
- The corrected control — Phase 63
- The verdict document and the charter — Phase 64 receives this phase's records, including "not tested (skipped at G2)"
- A second seed, a second confirmation, or a silent restart — a second confirmation would change the frozen one-confirmation budget
- Graded runs, held-out evaluation, and test-split files — SCOPE-40
- Curriculum training beyond Stage 0 — a gold data-only arm is the named third exception, not a Stage 2 run

## Constraints

- Every real arm is seed 42, MPS float32, one at a time, on this Mac. The first completed run is the result.
- Data grids are fixed: data-only arms use that system's gold record; physics arms use the stage recipe's record, as the table in the interview locked (Rung 2b hierarchical base 0.08; probe 2279 standard base 0.17; probe 3418 standard gold 0.01).
- Official tiers use the gold grid. Base-grid scores are a beside column.
- Single-system arms use the frozen 3-hour cap, one doubling, and the frozen polish (`lbfgs_max_iter` 50, history 10, strong Wolfe, stop after 5 outer calls without improvement or at 25% of summed Adam running time).
- The harness reads gold through a path the production base-only pool does not have to accept. It does not weaken that pool.
- Re-scoring committed weights is the re-derive. Fresh same-seed runs are statistically similar, not bit-identical (`pinn/training/determinism.py`).
- One seed cannot separate luck from capability. The verdict states that limit. Extra seeds are not added after a result.

## Acceptance Criteria

- [ ] The amendment text matches `REQUIREMENTS.md` and `ROADMAP.md` after collapsing whitespace, and the scorecard SHA-256 is unchanged
- [ ] INST-05 tests (a)–(e) pass, including mutation of the trainer's loss, test-split refusal, graded-run and evaluator refusal, a short polish run with both states scored, and override refusal on a physics arm
- [ ] The MPS regression passes, and a CPU float64 re-score that changes the tier or the counts-boolean stops for the owner
- [ ] The protocol file is committed before the first real-arm record, and every real-arm record cites it
- [ ] Rung 1 on 1632, 851, and 4658 trains on hierarchical gold and is scored on that same gold grid
- [ ] G2 matches `g2_fires`, and the sweep pair matches the pinned lap-count cases
- [ ] All four sweep settings run before any confirmation, and the confirmation is the highest Tier ≥ 1 setting, or there is no confirmation
- [ ] Unanswered checkpoint ④ leaves Rung 2 and the probes neither run nor skipped
- [ ] A stop at G2 records Rung 2 and FEAS-09 skipped with `no rescue` or `checkpoint ④ answered go to the verdict`, and does not call `decision_verdict` with later-rung inputs
- [ ] A continue runs the uncovered system's gold Rung 1, Rung 2, and the probes at the approved setting
- [ ] Probe arms do not call `counts()`, and their formula field is `not applicable: no hierarchical split`
- [ ] Every assigned train or score record is checked before the first arm, and a missing, empty, or unreadable record does not fall back
- [ ] Resume keeps the original step budget, sums Adam running time across segments, and an unrestorable arm stops for the owner
- [ ] The harness does not catch and retry a missing formula on a counted system, a rescue, or an undeterminable improvement rate
- [ ] Phases 61–63 are marked skipped by G2, not failed, when the ladder stops

## Edge Coverage

**Coverage:** 27/27 applicable edges resolved · 0 unresolved

R1–R8 in this table are the edge-probe ids. Spec requirements 1–8 are the numbered list above: R3 is requirement 1, R1 is requirement 2, R2 is requirement 3, R4 is requirement 4, R5 is requirement 5, R6 is requirement 6, and R7–R8 are requirement 7. Requirement 8 collects the resume and preflight edges from R4 and R5.

| Category | Requirement | Status | Resolution / Reason |
|----------|-------------|--------|---------------------|
| idempotency | R1 | ✅ covered | The INST-05 short run is a fixture, not a real-arm result, and a second invocation does not replace a committed real-arm record |
| concurrency | R1 | ✅ covered | Arms run one at a time; an interrupt resumes that same arm, including the polish |
| boundary | R2 | ✅ covered | MPS widening is CPU then float64; a non-finite `E` is Tier 0 |
| precision | R2 | ✅ covered | Inclusive cuts: `E` exactly 0.1 is Tier 1. A non-finite `ε_H` caps the tier at 1 when `E ≤ 0.1`. Cross-check disagreement stops |
| empty | R3 | ✅ covered | A skip reason must be one of the two pre-registered reasons. Once any Rung-2 arm has started, a skip cannot be recorded |
| encoding | R3 | ✅ covered | Amendment equality is exact after collapsing whitespace |
| idempotency | R4 | ✅ covered | The first completed run is the result. Re-scoring committed weights does not retrain. An unrestorable arm goes to the owner; there is no silent restart |
| concurrency | R4 | ✅ covered | One arm at a time. Polish uses summed Adam running time, not calendar time that includes the interruption. The step budget is not re-timed on resume |
| boundary | R5 | ✅ covered | `g2_fires` is strict. Exactly 1 of 3 does not fire. Tier exactly 1 does not fire. An inconclusive Rung 1 enters G2 at its result tier |
| adjacency | R5 | ⛔ dismissed | Rung 1 trains and is scored on one gold record. Base-grid scores are a beside column, not merged into the tier |
| empty | R5 | ✅ covered | A missing, empty, or unreadable train or score record is checked before the first arm. No substitute. A blocked Rung-1 arm makes G2 impossible |
| ordering | R5 | ✅ covered | The three Rung 1 scores are independent. The only order that changes what runs is the G2 pair order pinned under R6 |
| precision | R5 | ✅ covered | The arm result is the frozen lexicographic rule. A non-finite `ε_H` with `E ≤ 0.1` stays eligible to count against the formula |
| boundary | R6 | ✅ covered | Tier ≥ 1 includes Tier exactly 1. Tier 0 does not reach confirmation |
| adjacency | R6 | ⛔ dismissed | The grid values are four settings, not ranges. Adjacent values are not interpolated or merged |
| empty | R6 | ✅ covered | Zero Tier ≥ 1 settings produce no confirmation and no rescue |
| ordering | R6 | ✅ covered | Pinned pairs from laps 10.47, 18.61, 39.35: sweep the fewer, confirm the next. All four settings run in grid order before confirmation |
| precision | R6 | ✅ covered | Confirmation is the maximum `first_omega_0` among Tier ≥ 1 results. The four values are distinct, so there is no tie-break |
| idempotency | R6 | ✅ covered | Each sweep setting and the confirmation follow the first-completed-run rule |
| concurrency | R6 | ✅ covered | The four settings and the confirmation run one at a time |
| idempotency | R7 | ✅ covered | A no-rescue skip is not overwritten by launching Rung 2. A started Rung-2 arm cannot later be relabeled as a skip |
| concurrency | R7 | ✅ covered | Rung 2 and the probes do not start until G2 has passed or checkpoint ④ is answered continue. An unanswered checkpoint holds the phase |
| boundary | R8 | ✅ covered | Probe arms use the same budget, polish, seed, and runtime. On a continue they use the approved setting |
| adjacency | R8 | ⛔ dismissed | Each probe arm uses one named record. 3418's base times being a subset of gold is why its recipe record is gold, not a second series to merge |
| empty | R8 | ✅ covered | Probe records are in the preflight. On a skip path the files are not required. On a run path a missing record stops for the owner |
| ordering | R8 | ⛔ dismissed | 2279 and 3418 are named and independent. Running one before the other does not change either result |
| precision | R8 | ✅ covered | Probes are not counted and never call `counts()`. The formula field is `not applicable: no hierarchical split`. A missing formula on a counted system still goes to the owner |

## Prohibitions (must-NOT)

**Coverage:** 8/8 applicable prohibitions resolved · 0 unresolved

Path traversal and injection on evidence paths are canon — owned by `/gsd-secure-phase`; not minted here.

Routine engineering dropped in the precision pass: partial-file cleanup, input mutation, and the MPS crash itself (that crash is requirement 3, not a values constraint).

| Prohibition (must-NOT statement) | Requirement | Status | Verification / Reason |
|----------------------------------|-------------|--------|------------------------|
| MUST NOT open a test-split file or spend the held-out evaluation | R2 | resolved | verification: test. INST-05 (b) and the graded-run refusal |
| MUST NOT replace a completed arm with another seed, a silent restart, or a second fresh training run | R4 | resolved | verification: test. A second seed or a restart without an owner decision is refused |
| MUST NOT take the better of the official MPS score and the CPU float64 cross-check | R3 | resolved | verification: test. A tier or count difference stops for the owner |
| MUST NOT pass later-rung inputs to `decision_verdict` when G2 has fired | R7 | resolved | verification: test. The frozen function raises if those inputs are present; the harness must not supply them on a stop |
| MUST NOT substitute another fidelity or another system for a missing, empty, or unreadable assigned record | R5 | resolved | verification: test. Preflight failure stops the arm |
| MUST NOT catch `OwnerRouted` from a missing formula on a counted system, a rescue, or an undeterminable improvement rate and retry | R6 | resolved | verification: test. The exception propagates |
| MUST NOT record a Rung 2 or FEAS-09 skip after a Rung-2 arm has started, or with a reason outside the two pre-registered reasons | R7 | resolved | verification: test. The skip writer rejects any other reason and any skip after a Rung-2 start |
| MUST NOT let a data-only arm's weights initialize another run, and MUST NOT change the frozen scorecard bytes | R1 | resolved | verification: test. A follow-on run that loads those weights is refused. The scorecard SHA-256 matches the Phase 59 freeze |

## Ambiguity Report

| Dimension          | Score | Min  | Status | Notes |
|--------------------|-------|------|--------|-------|
| Goal Clarity       | 0.94  | 0.75 | ✓      | Ceiling on gold; physics only if the ladder continues |
| Boundary Clarity   | 0.93  | 0.70 | ✓      | Third SCOPE-39 exception and the skip clause are one amendment |
| Constraint Clarity | 0.92  | 0.65 | ✓      | Seed, runtime, grids, sweep pair, resume, and owner routes are pinned |
| Acceptance Criteria| 0.91  | 0.70 | ✓      | Pass/fail checks cite the frozen functions |
| **Ambiguity**      | 0.07  | ≤0.20| ✓      | 1 − (0.35×0.94 + 0.25×0.93 + 0.20×0.92 + 0.20×0.91) = 0.0725 |

## Interview Log

| Round | Perspective | Question summary | Decision locked |
|-------|-------------|------------------|-----------------|
| 1 | Researcher | What does Phase 60 still owe if the sweep rescues nothing, and which seed and runtime are official? | Run Rung 2, recorded, not fed into the verdict. Seed 42 and MPS float32, with a CPU float64 cross-check that never replaces the official score |
| 2 | Researcher + Simplifier | Which grid does each data term train on, and which Tier ≥ 1 setting is confirmed? | Data-only arms train on gold. Physics arms use the stage recipe's data. Run all four settings, then confirm the highest Tier ≥ 1 `first_omega_0` |
| 3 | Boundary Keeper | Does the gold ceiling reverse the Rung 2 decision, and how is gold named in SCOPE-39? | Skip Rung 2 only together with a named third SCOPE-39 exception. The skip does not hold if Rung 1 stays on the 0.08 grid |
| Edge | Failure Analyst | 27 probe edges, plus the checkpoint hold and a missing record | Accepted with corrections: non-finite `ε_H` caps the tier at 1; probes are not counted; sweep pairs are pinned; resume covers the polish and an unrestorable arm goes to the owner; continue runs the rest of Phase 60 at the approved setting, including the uncovered system's Rung 1 and the probes |

---

*Phase: 60-single-system-learnability*
*Spec created: 2026-10-17*
*Next step: /gsd-discuss-phase 60 — implementation decisions (how to build what this spec locks)*
