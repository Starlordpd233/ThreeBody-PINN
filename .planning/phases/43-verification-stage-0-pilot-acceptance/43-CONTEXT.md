# Phase 43: Verification, Stage-0 Pilot & Acceptance - Context

**Gathered:** 2026-07-20
**Status:** Ready for planning

<domain>
## Phase Boundary

The **milestone-closing** phase of v2.0. It assembles the already-built Stage-0
components (Phases 37–42) into four operator-facing surfaces — a `verify` pre-flight
ladder, a ~5-minute smoke test, an `evaluate` gate script, and an enriched
`summary.md` — then runs a 2–3-seed Stage-0 **pilot** to calibrate the owner-owned
thresholds, and closes v2.0 with a **go / adjust / rethink** verdict plus an updated
FUT-01/FUT-04 handoff. This is assembly + execution + calibration + verdict, not a
greenfield build.

</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

**6 requirements are locked.** See `43-SPEC.md` for full requirements, boundaries, and
acceptance criteria. Downstream agents MUST read `43-SPEC.md` before planning or
implementing. Requirements are not duplicated here.

**In scope (from SPEC.md):**
- `verify` ladder orchestrator (device sanity + the four existing probes, aggregated + gated)
- Smoke-test harness (~5 min) + measured s/step + per-run duration forecast
- `evaluate` script: test set once → `metrics.json` + `metrics.md` + binary gate render
- `summary.md` enrichment (validation summary, test-set preview, comparison hint, honesty layer)
- Stage-0 pilot execution (2–3 seeds) + seed-band record + threshold-calibration note
- go/adjust/rethink verdict artifact + FUT-01/FUT-04 handoff update
- Owner-ratification pause points (B-5, D4-a ceiling, R-1/R-2, ACC-06 verdict)

**Out of scope (from SPEC.md):**
- Full multi-stage curriculum (Stages 1–6), sL-BFGS stages 3–6, RAD collocation, Tier-3
  remediation, streaming residency, auto-revert — deferred (PLAT-01..07) pending the verdict
- trainex-r2 tuning round; hyperparameter sweeps / A-B testing / cross-run stats (design §6.6)
- Building new probes or changing model/loss/data/loop (that was Phases 38–41)
- Autonomously ratifying the ⚖ thresholds, D4-a ceiling, B-5 field list, or the verdict

</spec_lock>

<decisions>
## Implementation Decisions

### verify pre-flight ladder (ACC-01)
- **CTX-70:** New module CLI `python -m pinn.verify`, mirroring the established
  `python -m pinn.train` composition-root convention (Phase 41 CTX-52). It orchestrates,
  in order: (1) a **device-sanity** rung (MPS available + the D1-p-resolved dtype) → (2)
  the componentwise-AD probe → (3) fp64-CPU gradcheck → (4) residual-on-ground-truth +
  remaining §10 probes → (5) single-trajectory overfit. It calls the existing probe
  entry points (`pinn/verification/{componentwise_ad,gradcheck_probe,residual_probe,overfit_probe}.py`)
  as **library calls**, prints per-rung PASS/FAIL + an overall verdict, and exits non-zero
  naming the **first failing rung** — a missing/broken probe counts as that rung's FAIL,
  never a silent skip.
- **CTX-71:** The **> 30-min gate** is enforced in the `pinn.train` launch preflight: a
  run whose smoke-forecast is strictly > 30 min is refused unless a fresh green `verify`
  marker exists. `verify` writes a verdict marker (verdict + timestamp + env fingerprint);
  the exact marker path + freshness window is a research/plan detail. Boundary: forecast
  == 30 min is allowed.

### smoke test + s/step forecast (ACC-02)
- **CTX-72:** The smoke test is a **config preset / `--smoke`-style invocation of the
  ordinary `pinn.train` path** (≈32 Stage-0 trajectories, ~300 steps,
  `checkpoint_every=100`) — NOT a bespoke harness — so it exercises the real mechanical
  surface (signals/status/summary/sinks/resume). Ctrl-C/resume is exercised via the
  existing SIGTERM≡one-Ctrl-C + `--resume latest` flow (B-10 / Phase 41–42).
- **CTX-73:** The forecast **reuses `RunController.s_per_step`** (already an EMA in
  `controllers.py`): forecast = measured s/step × full-Stage-0 step estimate, emitted as a
  forecast line and surfaced for the D4-a ceiling ratification. On early divergence/NaN the
  smoke reports an honest failure with the partial s/step and **never** a fabricated forecast.

### evaluate script + binary gate (ACC-03)
- **CTX-74:** New module CLI `python -m pinn.evaluate --checkpoint <ckpt> --output <dir>`.
  Output layout per design §6.3: `metrics.json` (mandatory, machine-parseable) + `metrics.md`
  (mandatory, `## Gate Check` + plain-English descriptions); `per-trajectory/` + `plots/`
  best-effort. Single **no-grad** forward over the held-out test set, run **once**.
- **CTX-75:** Gate direction is the **authoritative** one (`ctl_instruction.md` / ACC-03),
  NOT the design-doc §6.3 render example (which inverts ε_H): REJECT if `ε_H > 1e-5`
  (smaller passes); PASS if `SCS > -5`; OVERALL FAIL iff `ε_H > 1e-5` OR `SCS ≤ -5`;
  boundary `ε_H == 1e-5` → PASS, `SCS == -5` → FAIL. A gate boundary unit test locks this
  (SPEC Prohibition #1).
- **CTX-76:** ε_H (energy error) and SCS are computed by **reusing the existing invariants /
  physics machinery** (`pinn/data-handling/processing/invariants.py`,
  `pinn/physics_residual.py`), not reinvented. The PRECISE ε_H/SCS formulas from model
  predictions follow `ctl_instruction.md` / `data_quality_assessment.md` — the
  researcher/planner pins the exact definitions (research item; **not invented here**).
- **CTX-77:** matplotlib-optional: plots are guarded (skip cleanly when matplotlib is
  absent — Phase 42 no-matplotlib rule); `metrics.json`/`metrics.md` never depend on plotting.

### summary.md enrichment (ACC-04)
- **CTX-78:** Enrich `pinn/training/summary.py` **in place**, preserving its
  stub-then-finalize + **render-don't-recompute** pattern and must-NOT #1 (no fabricated
  metrics on non-success). Add: validation summary (from the run's val records), test-set
  preview (a small subset from the `evaluate` output), run-to-run comparison **hint** (read
  a named prior run's `summary.json` numbers — a hint, not a full analysis, §6.6), and the
  three §6.4 honesty rules stated.

### Stage-0 pilot + threshold calibration (ACC-05)
- **CTX-79:** The pilot runs the short training **2–3× across distinct seeds on the REAL
  admitted Stage-0 data**. Dataset logistics: the gitignored corpus lives only in the
  master-root checkout — copy the needed Stage-0 admitted trajectories into the trainex
  worktree (gitignored, zero commit noise) for the pilot, or run the pilot from master-root.
  Seeds: a fixed small set from the Phase-41 seed/RNG schema (D6).
- **CTX-80:** The calibration artifact records per-seed final losses/val + the **seed-band
  spread** + derived **R-1 guard / R-2 RECOVER+HALT threshold candidates** + the **D4-a
  ceiling** candidate. A diverged seed is **included** (variance signal), not dropped;
  < 2 completed seeds flags the calibration low-confidence. Presented for owner ratification.

### go/adjust/rethink verdict + handoff (ACC-06)
- **CTX-81:** The verdict is a markdown artifact in the phase dir (proposed
  `43-VERDICT.md`, or folded into the milestone summary / VERIFICATION) stating go|adjust|
  rethink + cited evidence (gate result, seed-band, measured s/step, open seams) — **never
  an unqualified "go" on a FAILing gate**. The FUT-01/FUT-04 handoff update (shipped /
  placeholder-seam / deferred PLAT-01..07, reflecting GAP-38-01's disposition) goes into the
  forward hand-off doc (the eventual `pinn/STATUS.md` per CLAUDE.md, or a handoff doc).
  Owner-rendered: the agent prepares evidence + a recommendation; the owner decides.

### Owner-ratification pause protocol (owner-ratified 2026-07-20)
- **CTX-82:** Execution model = **agent-runs-pauses-for-you**. The agent runs the smoke +
  pilot autonomously but PAUSES for owner sign-off at four points and self-ratifies none of
  them: (1) **B-5** resume-field list before run #1; (2) **D4-a** wall-clock ceiling value
  post-smoke (measured s/step, in r1b's 15–30 min range); (3) **R-1/R-2** thresholds
  post-pilot (from observed variance); (4) the **ACC-06** go/adjust/rethink verdict.

### Test + build conventions (carried forward)
- **CTX-83:** `tests/phase43/` stdlib **unittest** with deferred-import skip guards, conda
  env `pinn-train`; dataset-free tiny-synthetic runs where possible, real-data probes copy
  the gitignored Stage-0 payload into the worktree. The gate-direction, metric-fabrication,
  and 30-min-gate prohibitions each get a negative test (SPEC Prohibitions, test-tier).

### Claude's Discretion
All technical/implementation decisions above were made by the agent under owner delegation
(2026-07-20; "decide scientific/technical/mathematical by best judgment"). Flexibility
retained on exact module internals, the verify-marker path + freshness window, plot
contents, and the calibration-note/verdict-artifact format — to be pinned during research/plan.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Locked requirements (read first)
- `.planning/phases/43-verification-stage-0-pilot-acceptance/43-SPEC.md` — the 6 locked requirements, boundaries, acceptance criteria, edge coverage, and 7 prohibitions
- `.planning/REQUIREMENTS.md` — ACC-01..06 (Phase 43 requirement block)
- `.planning/ROADMAP.md` — Phase 43 entry + v2.0 build discipline / verification protocol

### Authoritative science (gate + metrics)
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — the post-v1.3 binary gate (REJECT if ε_H > 1e-5; PASS if SCS > -5) and softening `eps_soft = 1e-5`; the authoritative gate direction
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` §10 / §10.3 — the AD-probe / verification-probe contract the ladder rungs implement
- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` — ε_H / SCS metric definitions (read-only characterization; pin the precise formulas here)

### Ratified build decisions
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/trainex-r1a-resolution-doc.md` — D-5 (smoke-as-instrument), D6 (seed band from 2–3 pilots), R-1/R-2 (⚖ guard/RECOVER thresholds), D4-a ceiling range (15–30 min), B-5 (resume-field list)
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/RATIFICATION.md` — the owner-ratified decision set standing

### Design surface (verification & assessment)
- `docs/work/designs/cross_cutting/training-execution/2026-06-10-training-execution-design.md` — §5 (pre-flight ladder + runbook), §6.2 (`summary.md` 6-item order), §6.3 (`evaluate` output layout + gate render — ⚠ **the ε_H render example is BACKWARDS; follow `ctl_instruction.md`**), §6.4 (honesty layer), §6.5 (outcome-level failure modes). NON-authoritative baseline.

### Code to assemble / extend
- `pinn/train.py` — composition root: run-dir resolve + traversal guard, freeze, RNG record, hook closures, `curriculum.run()`; the launch preflight (>30-min gate) wires in HERE
- `pinn/verification/{componentwise_ad,gradcheck_probe,residual_probe,overfit_probe}.py` — the four ladder rungs to orchestrate
- `pinn/training/summary.py` — the OPS-05 stub-then-finalize writer to enrich (preserve must-NOT #1)
- `pinn/training/controllers.py` — `RunController.s_per_step` EMA (forecast source); `stage_exit.py` (RECOVER/HALT machine the R-1/R-2 thresholds tune)
- `pinn/data-handling/processing/invariants.py`, `pinn/physics_residual.py` — ε_H/SCS metric machinery

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **The four verification probes** already have CLI `main()`s — the `verify` ladder wraps them, adding only a device-sanity rung + aggregation + gating.
- **`RunController.s_per_step`** EMA is already computed — the smoke forecast reads it directly; no new timing instrumentation.
- **`summary.py`** already renders Run header + Final losses + Curriculum progression (from `curriculum.jsonl`, render-don't-recompute) with must-NOT #1 honesty — ACC-04 extends this file, it does not replace it.
- **`runs/<name>/` contract** (logs/, tb/, summary.{md,json}, status.json, checkpoints/{rolling-3,best,latest,anchor}, config.yaml, curriculum.jsonl, failure/) + atomic-io + `--resume latest` — the smoke and pilot reuse this wholesale.

### Established Patterns
- **CLI convention:** `python -m pinn.<cmd>` (train; add verify, evaluate) with a `runs/`-rooted, path-traversal-guarded run dir.
- **Test convention:** `tests/phase43/` stdlib unittest, deferred-import skip guards, conda env `pinn-train`, dataset-free synthetic where possible.
- **Honesty pattern:** stub-then-finalize; render-don't-recompute; null metrics (never placeholder numbers) on non-success.

### Integration Points
- `pinn.train` launch preflight ← the > 30-min verify gate (CTX-71).
- `pinn.evaluate` output → `summary.py` test-set preview + gate result feed the ACC-06 verdict.
- The Phase-41 seed/RNG schema → the pilot's 2–3 seeds and seed-band calibration.

</code_context>

<specifics>
## Specific Ideas

- **The design-doc §6.3 gate render is a known bug** (fails `ε_H = 8.2e-6` against
  "required: > 1e-5", contradicting its own "smaller is better" text). Downstream agents
  MUST build the gate from `ctl_instruction.md` / ACC-03, not from the design-doc example.
- **Watchdog chain `phase-43-work`** (owner, 2026-07-20): position A = spec+discuss (this
  session); position B = plan (`gsd-plan-phase 43`); the chain grows by **append** as
  planning reveals the execute/verify positions.

</specifics>

<deferred>
## Deferred Ideas

- **PLAT-01..07** (full multi-stage curriculum, sL-BFGS stages 3–6, RAD, Tier-3, streaming,
  auto-revert) and the **trainex-r2** tuning round — deferred pending the ACC-06 verdict (in SPEC out-of-scope).

### Reviewed Todos (not folded)
- **D-06 static-epsilon sensitivity check** (`confirm dual-context is safe on the admitted
  set`) — reviewed; it is a data/physics **validation** concern (softening `eps_soft`
  sensitivity on the admitted set), not part of the ACC-01..06 assembly/verify/evaluate/
  pilot/verdict scope. Defer to a validation milestone.
- **trainex-r1 research handoff** — out of scope (r1 research package handoff, not Phase 43).

</deferred>

---

*Phase: 43-verification-stage-0-pilot-acceptance*
*Context gathered: 2026-07-20*
