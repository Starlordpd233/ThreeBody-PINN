# Phase 43: Verification, Stage-0 Pilot & Acceptance — Specification

**Created:** 2026-07-20
**Ambiguity score:** 0.16 (gate: ≤ 0.20)
**Requirements:** 6 locked

## Goal

Assemble the already-built Stage-0 components into a `verify` pre-flight ladder, a
~5-minute smoke test, an `evaluate` gate script, and an enriched `summary.md`; run a
2–3-seed Stage-0 pilot to calibrate the owner-owned thresholds; and close milestone
v2.0 with a **go / adjust / rethink** verdict plus an updated FUT-01/FUT-04 handoff.

## Background

Phases 37–42 built the CTL-PINN Stage-0 slice: the model (`pinn/network.py`,
`pinn/loss_catalog.py`, `pinn/physics_residual.py`), the data adapter
(`pinn/data/`), the two-phase Adam→L-BFGS curriculum loop
(`pinn/training/controllers.py`), config/checkpoint/guards/resume
(`pinn/training/{config_yaml,checkpoint,guards,resume,determinism}.py`), and the
operator runbook + monitoring surface (OPS-01..06). Individual verification **probes**
already exist as standalone CLIs — `pinn/verification/{componentwise_ad, gradcheck_probe,
residual_probe, overfit_probe}.py`; `RunController` already computes an `s_per_step`
EMA; and `pinn/training/summary.py` already writes an honesty-preserving
`summary.md`/`summary.json` (OPS-05, must-NOT #1: no fabricated metrics on non-success)
carrying Run header + Final losses + Curriculum progression.

What does **not** exist yet is the milestone-closing verification and acceptance
surface: no orchestrator chains the probes into a gated `verify` ladder; no smoke-test
harness converts the ~30×-wide duration envelope into a measured per-run forecast; no
`evaluate` script renders the binary post-v1.3 gate to `metrics.md`; `summary.md` lacks
the validation summary / test-set preview / run-to-run comparison / stated honesty layer;
no multi-seed pilot has calibrated the ⚖ thresholds; and no go/adjust/rethink verdict
has been rendered. This is the last phase of v2.0 (ACC-01..06); it is largely
**assembly + execution + calibration + verdict**, not greenfield build.

**Owner-ratified execution model (2026-07-20):** the agent runs the pilot autonomously
but **pauses for owner sign-off** at each human-owned decision point — the B-5
resume-field list (before run #1), the D4-a wall-clock ceiling value (post-smoke, from
the measured s/step), the R-1 guard / R-2 RECOVER+HALT thresholds (post-pilot, from the
observed variance), and the ACC-06 verdict.

## Requirements

1. **verify pre-flight ladder** (ACC-01): A single command runs the ordered verification
   ladder and gates long runs.
   - Current: The four probes exist only as separate CLIs; there is no orchestrator, no
     device-sanity rung, no aggregate verdict, and no gate on run duration.
   - Target: `python -m pinn.verify` runs, in order, (1) device sanity (MPS available +
     dtype) → (2) §10.3 componentwise-AD probe → (3) fp64-CPU gradcheck → (4)
     residual-on-ground-truth + remaining §10 probes → (5) single-trajectory overfit;
     prints per-rung PASS/FAIL and an overall verdict; and blocks any run whose
     smoke-forecast exceeds 30 min unless the ladder is green.
   - Acceptance: exits 0 with all rungs PASS on a healthy env/checkpoint; exits non-zero
     naming the first failing rung when any rung (including a missing/broken probe) fails;
     the launch path refuses a run forecast strictly > 30 min when the ladder is not green.

2. **Smoke test + s/step forecast** (ACC-02): A ~5-minute run exercises the whole
   mechanical surface and measures per-step wall time.
   - Current: `RunController` computes an `s_per_step` EMA, but no smoke-test config/harness
     exercises Ctrl-C/resume and emits a per-run forecast.
   - Target: A smoke invocation (≈32 Stage-0 trajectories, ~300 steps,
     `checkpoint_every=100`) runs end-to-end in ~5 min, exercises launch→monitor→Ctrl-C
     →resume, records the measured s/step, and prints a per-run duration forecast for a
     full Stage-0 run.
   - Acceptance: completes ~300 steps; writes checkpoints at steps 100/200/300; survives a
     Ctrl-C + resume to completion; emits a numeric `s_per_step` + forecast line; on early
     divergence/NaN it reports an honest failure with the partial s/step and never a
     fabricated forecast.

3. **evaluate script + binary gate** (ACC-03): A separate script renders the authoritative
   post-v1.3 gate on the held-out test set.
   - Current: No `evaluate` module exists; the gate is defined in specs but rendered by no
     script.
   - Target: `python -m pinn.evaluate --checkpoint <ckpt> --output <dir>` runs the test set
     **once** (no-grad forward), writes `metrics.json` + `metrics.md`, and renders the
     binary gate with plain-English descriptions and an OVERALL verdict.
   - Acceptance: `metrics.md` contains a `## Gate Check` block with
     `ε_H: <v> (reject if > 1e-5) → ✅/❌`, `SCS: <v> (reject if > -5) → ✅/❌`, and an
     `OVERALL: PASS/FAIL`; OVERALL is FAIL iff `ε_H > 1e-5` (equivalently `SCS > -5`); the boundary
     `ε_H == 1e-5` → PASS and `SCS == -5` → PASS; `metrics.json` carries the same numbers;
     an empty/absent test set is refused with a clear non-zero error, and a NaN/Inf metric
     renders an honest FAIL rather than a crash.

4. **summary.md enrichment + honesty layer** (ACC-04): The end-of-run one-pager gains the
   comparison/assessment content and states the honesty rules.
   - Current: `summary.py` writes Run header + Final losses + Curriculum progression +
     honest non-success template; it lacks a validation summary, test-set preview,
     run-to-run comparison hint, and the stated honesty layer.
   - Target: `summary.md` additionally reports a validation summary (final val loss +
     trend), a test-set preview, and a run-to-run comparison hint (vs a named prior run),
     and states the three honesty-layer rules.
   - Acceptance: a completed run's `summary.md` contains Run header, Final losses,
     Validation summary, Curriculum progression, Test-set preview, and Comparison hint
     sections plus the three honesty statements (healthy val ≠ working model; comparison ≠
     progress; clean loss curve ≠ correct physics); a failed/interrupted run still names its
     disposition and leaves metrics null (must-NOT #1 preserved).

5. **Stage-0 pilot + threshold calibration** (ACC-05): Repeated seeded runs measure
   variance and produce owner-ratifiable threshold candidates.
   - Current: `recover.retries: 0` and the R-1/R-2 guard/HALT thresholds are ⚖ placeholders;
     no multi-seed pilot has run.
   - Target: The pilot runs the short training 2–3× across distinct seeds, records the
     seed-band spread in `summary.md` (or an aggregate), and derives calibrated R-1 guard /
     R-2 RECOVER+HALT threshold candidates from the observed variance, presented for owner
     ratification.
   - Acceptance: an artifact records ≥2 seeded runs and their seed-band spread (a diverged
     seed is included, not dropped; < 2 completed seeds flags the calibration
     low-confidence); a calibration note records the raw per-seed observations AND the
     derived R-1/R-2 candidates and the D4-a ceiling, and the owner is asked to ratify
     (agent does not self-ratify).

6. **go/adjust/rethink verdict + handoff** (ACC-06): The milestone closes with a grounded
   verdict and an updated forward handoff.
   - Current: No milestone-closing verdict exists; the FUT-01/FUT-04 handoff does not record
     v2.0's shipped/seam/deferred inventory.
   - Target: A milestone-closing artifact renders one of {go, adjust, rethink} on whether
     the Stage-0 slice justifies building the full multi-stage platform, grounded in the
     verify/evaluate/pilot evidence; the FUT-01/FUT-04 handoff is updated.
   - Acceptance: the verdict states go|adjust|rethink with cited evidence (gate result,
     seed-band, measured s/step, open seams) and does not render an unqualified "go" on a
     FAILing gate; the handoff lists what shipped, what stayed a placeholder seam
     (`recover.retries:0`, ⚖ thresholds, sL-BFGS stages 3–6, RAD collocation, Tier-3
     remediation, streaming residency, auto-revert), and what was deferred (PLAT-01..07);
     the verdict is owner-rendered (agent prepares evidence + recommendation, owner decides).

## Boundaries

**In scope:**
- `verify` ladder orchestrator (device sanity + the four existing probes, aggregated + gated)
- Smoke-test harness (~5 min) + measured s/step + per-run duration forecast
- `evaluate` script: test set once → `metrics.json` + `metrics.md` + binary gate render
- `summary.md` enrichment (validation summary, test-set preview, comparison hint, honesty layer)
- Stage-0 pilot execution (2–3 seeds) + seed-band record + threshold-calibration note
- go/adjust/rethink verdict artifact + FUT-01/FUT-04 handoff update
- Owner-ratification pause points (B-5, D4-a ceiling, R-1/R-2, ACC-06 verdict)

**Out of scope:**
- Full multi-stage curriculum (Stages 1–6 end-to-end) — the slice proves Stage 0; advancing
  is the full platform (PLAT-01), gated on this verdict
- Stochastic-L-BFGS stages 3–6, RAD adaptive collocation, Tier-3 auto-remediation, streaming
  residency, auto-revert — deferred (PLAT-02..07) pending the verdict
- The trainex-r2 tuning round — post-viability
- Hyperparameter sweeps, A/B architecture testing, cross-run statistical analysis
  (design §6.6) — explicitly not in the verification layer
- Building new probes, or changing the model / loss / data / training loop — that was
  Phases 38–41; Phase 43 assembles and runs, it does not re-build
- Autonomously ratifying the ⚖ thresholds, D4-a ceiling, B-5 field list, or the verdict —
  owner-owned

## Constraints

- Single M5 Pro Mac; PyTorch 2.12 + MPS; `pinn-train` conda env; tests run under **unittest**
  (project convention, not pytest). No cloud/distributed — hard constraint.
- Stage-0 only; in-memory fp32 admitted set (~0.55 GB); manual rollback.
- **Binary gate direction is the authoritative one** (`REQUIREMENTS.md` ACC-03 /
  `ctl_instruction.md`): **REJECT if `ε_H > 1e-5`** (smaller energy error passes), equivalently **REJECT if
  `SCS > -5`** (`SCS = log10(ε_H)`; PASS iff `SCS ≤ -5`). The non-authoritative design doc §6.3 render example inverts `ε_H` (it fails
  `8.2e-6`, contradicting its own "smaller is better, < 1e-5 is excellent" text) and MUST NOT
  be copied — see Prohibitions.
- The `verify` ladder gates any run **projected > 30 min**; the ~5-min smoke test is exempt.
- Human-ratification points pause for the owner (agent-runs-pauses-for-you): B-5 resume-field
  list before run #1; D4-a ceiling post-smoke; R-1/R-2 thresholds post-pilot; ACC-06 verdict.
- `summary.py` must preserve must-NOT #1 (no fabricated metrics on a non-success run).
- Milestone-close watch-item: Phase 38 holds **GAP-38-01** (real-trajectory evidence deferred);
  its disposition must be reflected in the ACC-06 handoff.

## Acceptance Criteria

- [ ] `python -m pinn.verify` runs the 5-rung ladder in order, prints per-rung PASS/FAIL + an overall verdict, and exits 0 only when all rungs PASS
- [ ] `verify` exits non-zero and names the first failing rung when any rung (including a missing/broken probe) fails
- [ ] The launch path blocks a run whose smoke-forecast is strictly > 30 min unless the ladder is green (== 30 min allowed)
- [ ] Smoke test (~32 Stage-0 traj, ~300 steps, `checkpoint_every=100`) completes in ~5 min, writes checkpoints at steps 100/200/300, survives Ctrl-C + resume, and emits a numeric `s_per_step` + per-run forecast
- [ ] On early smoke divergence/NaN, the smoke reports an honest failure with partial s/step and does NOT emit a fabricated forecast
- [ ] `python -m pinn.evaluate --checkpoint <ckpt> --output <dir>` runs the test set once and writes `metrics.json` + `metrics.md`
- [ ] `metrics.md` renders `## Gate Check` with `ε_H` (reject if > 1e-5), `SCS` (reject if > -5), and `OVERALL: PASS/FAIL`; OVERALL FAIL iff `ε_H > 1e-5` (equivalently `SCS > -5`)
- [ ] Gate boundary: `ε_H == 1e-5` → PASS and `SCS == -5` → PASS (strict-inequality reject: `ε_H > 1e-5` / `SCS > -5`)
- [ ] `metrics.md` includes plain-English descriptions of `ε_H` and `SCS`; `metrics.json` carries the same numeric values
- [ ] `evaluate` refuses an empty/absent test set with a clear non-zero error and renders an honest FAIL (no crash) on a NaN/Inf metric
- [ ] A completed run's `summary.md` contains Run header, Final losses, Validation summary, Curriculum progression, Test-set preview, and Comparison hint, plus the three honesty-layer statements
- [ ] A failed/interrupted run's `summary.md` names its disposition and leaves metrics null (must-NOT #1 preserved)
- [ ] The Stage-0 pilot records ≥2 seeded runs + their seed-band spread; a diverged seed is included, not dropped; < 2 completed seeds flags the calibration low-confidence
- [ ] A calibration note records raw per-seed observations AND derived R-1/R-2 threshold candidates + the D4-a ceiling, presented for owner ratification (agent does not self-ratify)
- [ ] The milestone-closing verdict states go|adjust|rethink with cited evidence and does not render an unqualified "go" on a FAILing gate
- [ ] The FUT-01/FUT-04 handoff lists what shipped, what stayed a placeholder seam, and what was deferred (PLAT-01..07), reflecting GAP-38-01's disposition
- [ ] Each owner-ratification pause point (B-5, D4-a ceiling, R-1/R-2, ACC-06 verdict) pauses for owner sign-off before proceeding

## Edge Coverage

**Coverage:** 8/11 applicable edges resolved · 0 unresolved · 3 dismissed

| Category | Requirement | Status | Resolution / Reason |
|----------|-------------|--------|---------------------|
| unclassified | R1 | ✅ covered | Broken/missing probe → ladder names first failing rung (AC 2); duration gate uses strict `> 30 min` (AC 3) |
| unclassified | R2 | ✅ covered | Ctrl-C mid-checkpoint → resume from last atomic checkpoint; early divergence → honest failure + partial s/step, never a fabricated forecast (AC 5) |
| adjacency | R3 | ✅ covered | Threshold boundary pinned: `ε_H == 1e-5` PASS, `SCS == -5` PASS — strict-inequality reject (AC 8) |
| empty | R3 | ✅ covered | Empty/absent test set refused with non-zero error; NaN/Inf metric → honest FAIL, no crash (AC 10) |
| ordering | R3 | ⛔ dismissed | Fixed two-metric render in a published order; no data-dependent collection to order |
| adjacency | R4 | ⛔ dismissed | `summary.md` uses a fixed section template; no touching/merge semantics |
| empty | R4 | ✅ covered | Failed/interrupted/empty run → disposition named, metrics null; "(no curriculum records)" handled (AC 12) |
| ordering | R4 | ⛔ dismissed | Curriculum progression rendered in recorded event order from `curriculum.jsonl`, not sorted/recomputed |
| boundary | R5 | ✅ covered | < 2 completed seeds → low-confidence flag; a diverged seed is included in the seed-band, not dropped (AC 13) |
| precision | R5 | ✅ covered | Calibration note records raw per-seed observations AND the derived candidate (no single opaque rounded number); owner ratifies (AC 14) |
| unclassified | R6 | ✅ covered | A FAILing gate does not yield an unqualified "go"; verdict cites the gate result and is owner-rendered (AC 15) |

## Prohibitions (must-NOT)

**Coverage:** 7/7 applicable prohibitions resolved · 0 unresolved

| Prohibition (must-NOT statement) | Requirement | Status | Verification / Reason |
|----------------------------------|-------------|--------|------------------------|
| MUST NOT render the binary gate in the design-doc §6.3 backwards direction (treating `ε_H > 1e-5` as PASS) — the authoritative gate REJECTS `ε_H > 1e-5` | R3 | resolved | verification: **test** — a gate unit test with `ε_H` just above/below 1e-5 and `SCS` just above/below -5 asserts the correct verdicts |
| MUST NOT fabricate or placeholder metrics in `summary.md`/`metrics.md` for a failed/interrupted run (preserve must-NOT #1) | R4 | resolved | verification: **test** — a failed-run summary test asserts metrics are null and disposition is named |
| MUST NOT self-ratify the ⚖ thresholds, D4-a ceiling, B-5 resume-field list, or the go/adjust/rethink verdict — each pauses for the owner | R5, R6 | resolved | verification: **judgment** — owner-ratification pause is a workflow gate, not a mechanical check |
| MUST NOT let a run projected > 30 min proceed without a green `verify` ladder | R1 | resolved | verification: **test** — launch-path test asserts a > 30-min forecast is refused when the ladder is not green |
| MUST NOT claim the model "works" / render "go" on the basis of validation loss or loss-curve health alone (the test-set gate is the only honest pass — §6.4) | R6 | resolved | verification: **judgment** — verdict review confirms the "go" is grounded in the gate result |
| MUST NOT build new probes, change the model/loss/data/loop, or advance beyond Stage 0 / implement PLAT items (scope creep) | all | resolved | verification: **judgment** — diff review confirms assembly-only scope |
| MUST NOT evaluate the held-out test set more than once, or let test data influence training or model selection (single-eval discipline) | R3 | resolved | verification: **judgment** — the `evaluate` script is the sole test-set consumer and runs once at the milestone boundary |

## Ambiguity Report

| Dimension          | Score | Min  | Status | Notes                                                        |
|--------------------|-------|------|--------|--------------------------------------------------------------|
| Goal Clarity       | 0.85  | 0.75 | ✓      | 6 named deliverables (ACC-01..06) with numeric acceptance    |
| Boundary Clarity   | 0.85  | 0.70 | ✓      | Explicit PLAT-01..07 deferral; assembly-not-rebuild boundary |
| Constraint Clarity | 0.80  | 0.65 | ✓      | M5 Pro/MPS, gate direction pinned, 30-min gate, 2–3 seeds    |
| Acceptance Criteria| 0.85  | 0.70 | ✓      | 17 pass/fail criteria incl. threshold boundaries             |
| **Ambiguity**      | 0.16  | ≤0.20| ✓      | Gate passed at initial assessment (requirements pre-locked)  |

Status: ✓ = met minimum, ⚠ = below minimum (planner treats as assumption)

## Interview Log

| Round | Perspective    | Question summary                                   | Decision locked                                                        |
|-------|----------------|----------------------------------------------------|-----------------------------------------------------------------------|
| 0     | Initial assess | Are ACC-01..06 already falsifiable?                | Yes — ambiguity 0.16 at round 0; multi-round interview skipped         |
| —     | High-level (owner) | Chain shape for `phase-43-work`?               | Minimal A→B, grow by append (owner, 2026-07-20)                        |
| —     | High-level (owner) | Who drives the pilot runs + verdict?           | Agent runs, pauses for owner at each ratification point (2026-07-20)   |
| —     | Adversarial    | Is the design-doc §6.3 gate render authoritative?  | No — design doc inverts `ε_H`; SPEC locks `ctl_instruction.md` direction |

*Technical/scientific/mathematical spec decisions were made by the agent under owner
delegation (2026-07-20); high-level pipeline decisions were surfaced to and answered by
the owner. No STOP-protocol spec-adjudication gap was hit (the gate direction is resolved
by the authoritative spec, not invented).*

---

*Phase: 43-verification-stage-0-pilot-acceptance*
*Spec created: 2026-07-20*
*Next step: /gsd-discuss-phase 43 — implementation decisions (how to build what's specified above)*
