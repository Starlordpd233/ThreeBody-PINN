# Phase 50: Valid Stage-0 Re-Run - Research

**Researched:** 2026-08-14
**Domain:** Controlled ML experiment closure, runtime conformance, and evidence provenance
**Confidence:** HIGH for the observed failures and validation repair; MEDIUM for causal-front diagnosis because the retained evidence does not ground a recipe remedy

<user_constraints>
## User Constraints (from CONTEXT.md)

The following constraints preserve the operative text of the locked decisions. The complete decision rationales and citations remain binding in `50-CONTEXT.md`; omission of explanatory prose here does not create planner discretion. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:55-482]

### Locked Decisions

- **D-01 [BUDGET — the shipped Stage-0 config, not the v2.0 smoke budget]:** The three graded runs execute at `stage.max_epochs = 1000` and `stage.n_adam = 1000` — the values committed in `configs/stage0-example.yaml`. Before the first smoke, add the narrow `--stage-0-only` conformance switch. Every Phase-50 launch uses it and verifies that all persisted stage fields equal zero and no Stage-1 checkpoint exists. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:59-98]
- **D-02 [WHAT RUN-02 COMPARABILITY ACTUALLY REQUIRES]:** "Matching the v2.0 protocol" is comparability at the **protocol** layer, not byte-identity of config. What is held identical to v2.0: seeds `41, 42, 43`; the admitted corpus and blacklist; `float32`/`mps` and the pinned environment; `validation_every: 100`; `log_every: 50`; and the run-record contract. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:100-113]
- **D-03 [THE OPTIMIZATION-PATH AND WORKLOAD DELTAS ARE RECORDED CONFOUNDS, NOT HIDDEN ONES]:** Phase 50 does **not** add a 300-step matched arm to isolate the confound: that is measurement beyond RUN-01/RUN-02 and is recorded as a deferred idea. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:115-130]
- **D-04 [PER-RUN COMMITTED CONFIGS, DIFFERING ONLY IN `seed` AND `run_name`]:** The three graded configs are **byte-identical except `run.seed` and `run.run_name`**. `run.smoke` is absent (false) in all three. The committed `configs/stage0-example.yaml` and `configs/smoke.yaml` are **not edited**. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:132-140]
- **D-05 [LOGGING LITERAL IS PROTOCOL PARITY, CURRENTLY INERT]:** `run.log_every: 50`. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:142-150]
- **D-06 [EVERYTHING ELSE IS THE SHIPPED CONFIG, UNTOUCHED]:** The R-1 guard thresholds (`1e11` / `0.05` / `0.7`), R-2 `recover_retries: 0`, D4-a `wall_clock_ceiling_s: 120`, `front_advance_window_n: 500`, `loss.lambda_e_max: 0.0`, the stage-exit thresholds, and the monitor block are carried verbatim from `configs/stage0-example.yaml`. Any change to any of them inside this phase is prohibited unless it passes the D-18 conformance-repair test. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:152-158]
- **D-07 [THE SPLIT IS SEED-DEPENDENT — this is why pre-registration is mandatory]:** Every selection rule this phase can fix is fixed in writing, in the phase's pre-registration record, **before the first graded run starts**. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:162-172]
- **D-08 [PRE-REGISTERED SUBMISSION CANDIDATE: seed 42]:** The run offered to Phase 51 for the single EVAL-01 evaluation is the **seed-42** run. No metric, from any run, may influence this choice. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:174-184]
- **D-09 [PRE-REGISTERED CHECKPOINT: `checkpoints/best.pt`]:** The rule is the v2.0 rule: `runs/<run>/checkpoints/best.pt`. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:186-194]
- **D-10 [INELIGIBILITY-ONLY FALLBACK ORDER: 42 → 41 → 43]:** The fallback fires **only** on eligibility, **never** on a metric's value. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:196-204]
- **D-11 [NO ELIGIBLE SEED IS AN OWNER CHECKPOINT, NOT A WORKAROUND]:** If none of the three runs is eligible, Phase 50 does not manufacture a candidate, relax a precondition, or waive an entry. It records the state, writes the gap, and routes to the owner; Phase 51 does not open. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:206-212]
- **D-12 [SPLIT REPRODUCTION IS VERIFIED, NOT ASSUMED]:** the pinned seed-41/42/43 `splits.json` SHA-256 values are respectively `c25568a18f3c4e31bcef5bf36f71591f0978edca4ca6cd490a28ec88ea276c86`, `5846ae5b55104e55a85d644875c3da187200c3d521f52a9298876d656c6d8903`, and `a8618b0c6d0f0f1487fe4e3f8c0409a3e3398c7e8cb8bee2b4d3d7962a576172`; a mismatch is a mandatory qualification, never a license to adjust anything. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:214-225]
- **D-13 [THE SMOKE IS ENFORCED BY THE DURATION GATE, NOT CHOSEN]:** Phase 50 opens with an ACC-02 smoke on the current code state. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:229-239]
- **D-14 [THE SMOKE IS ALSO THE GATE'S AND `S_H`'s FIRST REAL-CORPUS CONTACT]:** `training_metadata.json` (`s_h`, `eps_h`, `n_train`) is captured as the first authoritative real-corpus record. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:241-249]
- **D-15 [THE SMOKE CARRIES `front_advance_window_n: 500`]:** the value is copied, not chosen. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:251-260]
- **D-16 [`S_H` CROSS-CHECK: the smoke runs at seed 42]:** the seed-42 smoke and seed-42 graded run must have byte-identical `splits.json` and exactly equal `s_h` and `n_train`. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:262-272]
- **D-17 [NO COMMIT BETWEEN THE CALIBRATION AND THE GRADED RUNS]:** land every code/config commit the phase needs → run the smoke → run all three graded seeds → only then commit the evidence extraction. If a code/config commit becomes necessary mid-band, close the current generation terminally and archive every attempt. Before a later full rerun, revise and commit the pre-registration source-identity binding while keeping the selection policy bytes unchanged. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:274-293]
- **D-18 [EXECUTION ORDER AND THE VERIFY-LADDER CONTINGENCY]:** smoke → seed 41 → seed 42 → seed 43. If the smoke's measured `s_per_step × 1000` exceeds 1800 s, run `python -m pinn.verify`, **never** reduce the budget. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:295-305]
- **D-19 [THE ONLY LEGAL EDIT INSIDE THIS PHASE IS A CONFORMANCE REPAIR]:** *does this bring the implementation closer to a locked spec value, an owner ruling, or a Phase-46..49 contract — justified **without reference to what a run produced**?* If yes, it is a conformance repair and is allowed only after terminal closeout and a new pre-band pre-registration/source-identity commit. If the justification requires citing an observed number, it is tuning and is prohibited. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:309-319]
- **D-20 [AN INVARIANT-B HALT IS AN OWNER CHECKPOINT, NOT A NUMBER TO ADJUST]:** If it fires, preserve the HALT evidence and route it to the owner. **`N` is not raised, softened, re-marked provisional, or bypassed by any agent**. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:321-336]
- **D-21 [PREFLIGHT REFUSAL AND GUARD TRIPS]:** no waiver is minted; `recover_retries` stays `0`; no Phase-50 resume is admissible; every interruption closes terminally; any later continuation requires an amended plan and a fresh generation from step zero. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:338-349]
- **D-22 [NO RUN IS SILENTLY DISCARDED]:** Every launch that starts is listed in a committed run ledger with the prescribed invocation, identity, exit, and hash evidence. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:351-359]
- **D-23 [THE HELD-OUT SET IS NOT TOUCHED, AND THAT IS CHECKED]:** No `pinn/evaluate.py` invocation, no `runs/<run>/evaluation/` directory, no `evaluation-attempt.json`, no materialization of the `test` split. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:361-368]
- **D-24 [THE BAND RECORD — concrete contents]:** project the eight `gate_*` keys verbatim, retain all ten validation events and referenced sidecars, characterize terminal per-trajectory distributions, retain `s_h`/`eps_h`/`n_train`, front high-water trajectory, final losses, gradient statistics, preflight/eligibility facts, and open divergences; report only descriptive three-seed variation. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:370-397]
- **D-25 [CHARACTERIZATION IS DESCRIPTIVE — it grades nothing and feeds nothing]:** validation `ε_H` may not choose a seed, choose a checkpoint, or justify a parameter change; `gate_status` and `gate_verdict` remain distinct. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:399-409]
- **D-26 [THE PHASE DOES NOT PRE-EMPT THE VERDICT]:** Phase 50 describes what the runs did; it does not conclude that the design works, fails, or explains v2.0. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:411-418]
- **D-27 [EXECUTION LOCATION AND ENVIRONMENT]:** Runs execute **inline in `.worktrees/trainex` on `milestone/v2.2`**, under `<home>/miniforge3/bin/conda run -n pinn-train`; Python `3.11.15`, torch `2.12.1`, and MPS available are pinned. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:422-432]
- **D-28 [CORPUS RESOLUTION — no copy, and the partial copy is refused]:** `data.root` stays unset; `GSD_DATA_ROOT` and `GSD_ALLOW_PARTIAL_DATA_ROOT` are **not** set. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:434-454]
- **D-29 [EVIDENCE EXTRACTION IS MANDATORY — `runs/` never commits]:** copy the prescribed artifacts to `.planning/phases/50-valid-stage-0-re-run/evidence/`, record source paths and SHA-256, retain `train.log.jsonl`, omit checkpoints/TensorBoard, and rename copied `failure/tail.log` to tracked `failure/tail.log.txt`. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:456-479]
- **D-30 [GOVERNANCE — gaps, checkboxes, and the standing prohibitions]:** route source-silent adjudication to the gap register and owner; flip RUN-01/RUN-02 only during verification; commit through `scripts/agent-commit` with ownership variables and explicit paths; no protected-branch push. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:481-499]

### the agent's Discretion

The planner and executor own, without re-opening anything above: the exact run
and config file names (the only locked properties are that they are **distinct
from the v2.0 `stage0-pilot-seed4X` names** so v2.0 artifacts are preserved
intact, that the configs are committed, and that the three graded configs differ
only in `run.seed`/`run.run_name`); the wave decomposition and how D-17's
no-commit-mid-band constraint is expressed in it; the file format and layout of
the run ledger, band record, pre-registration record, and config-delta record;
which quantiles the D-24 distribution reports; whether the smoke and the band
extraction are one plan or several; attended (`python -m pinn.train`) versus
unattended (`scripts/train-unattended.sh`) launch; and the sha256 manifest format
for the evidence extraction. Those choices must preserve every decision above,
add no dependency, introduce no new threshold or selection rule, and change
nothing that enters a loss term, an optimizer, the data path, or a gate.

[VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:501-514]

### Deferred Ideas (OUT OF SCOPE)

- **A 300-step budget-matched arm** to isolate the conformance repair from the
  3.33× budget change (D-03). Legitimate measurement, but beyond RUN-01/RUN-02;
  it belongs to Phase 52's DIAG-05 if the re-derivation needs it, or to the owner
  if they want the tighter A/B.
- **Any recipe change suggested by the conformant numbers** — λ weights, learning
  rate, warmup, budget, clip bound, curriculum pacing. v2.3, with the trainex-r2
  resolution doc as a premise-qualified candidate verdict source (SCOPE-29/31).
- **Re-ruling `N` for invariant B** after observing a Phase-50 HALT — an owner
  decision the shipped config comment already anticipates ("retain this value
  verbatim unless the owner re-rules after a Phase-50 invariant-B HALT"). Routed
  as a gap (D-20), never taken here.
- **Stage-1+ advance, `stage_factory` multi-stage λ reconfiguration (PLAT-01),
  and sL-BFGS (PLAT-02)** — SCOPE-27; the gate's stage-2 refusal (Phase-49 D-06)
  is the correct behavior and stays.
- **Config-resolving `collocation_count`** (hard-coded 16 at `train.py:920`) and
  the `I_warm` integer-floor interpretation — both already open `qualification`
  entries in the register; changing either is a recipe surface (SCOPE-29).
- **Committing `logs/train.log`** — blocked by the global `*.log` ignore; would
  need an explicit negation like Phase 39's. Not needed:
  `train.log.jsonl` carries the machine-readable record (D-29).
- **The general verification-enforcement regime** — normative-statement index,
  full CI integration, waiver policy, thresholds X/M — charter workstream,
  SCOPE-32.
- **Spec-text amendments** — the four VER-20 routing items, Phase 52 (SCOPE-30).
- **Spending the single authorized evaluation** — Phase 51. Phase 50 produces the
  facts and pre-registration, then mechanically evaluates the four D-10
  structural-eligibility criteria without opening the held-out test split:
  `eval01_precondition_i`, the attempt-level guard/invariant rule, final process
  and ledger dispositions, and `eval01_precondition_iii` plus independent
  production-sidecar validation. Phase 51 rechecks those facts before it performs
  the one authorized evaluation.
- **Re-deriving the Phase 44 diagnosis** — Phase 52 (DIAG-05, the GAP-44-02
  obligation). D-24 exists so that re-derivation finds its evidence already
  captured rather than reconstructing it from logs.

[VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:711-758]
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|---|---|---|
| RUN-01 | "Stage-0 re-run under the corrected recipe, with conformance-only iteration (SCOPE-29)." | Separates the grounded validation implementation repair from the still-ungrounded causal-front remedy; specifies fresh-generation gates and full-run terminal criteria. [VERIFIED: .planning/REQUIREMENTS.md:63-64] |
| RUN-02 | "Re-establish the three-seed band, matching the v2.0 protocol so the runs are comparable." | Specifies the strict seed order, all-three-finished prerequisite, validation sidecar health, normal evidence extraction, band characterization, and candidate finalization. [VERIFIED: .planning/REQUIREMENTS.md:65-66] |
| SCOPE-29 | "**NO recipe tuning.** Iteration inside v2.2 is *conformance-only* — repairing divergences against the spec, never adjusting hyperparameters against observed results. This is what protects the single look; violating it re-creates the leakage the budget exists to prevent." | Supplies the edit classification fence and the mandatory owner checkpoint when no independently grounded causal-front remedy exists. [VERIFIED: .planning/REQUIREMENTS.md:82-82] |
</phase_requirements>

## Summary

Phase 50 is not complete. Generation 3's seed-41 attempt terminated at step 501 with `front_idx=0`; seeds 42 and 43 were not launched; therefore no finished corrected-recipe run, three-seed validation band, or candidate exists. The authoritative verification rates only 2/4 truths and keeps RUN-01/RUN-02 blocked. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md:1-20,28-33,78-89]

There are two independent technical findings. First, invariant B behaved according to its locked algorithm: the causal-front high-water remained zero through the `N=500` window, so the guard halted. The retained evidence proves the symptom and guard conformance but does not prove why the first residual bin never admitted the second causal bin, and it grounds no recipe/config change that would make it do so. Second, every scheduled validation attempt failed because production passes an MPS float32 tensor into a one-step CPU/float64 conversion; torch 2.12.1 raises the reproduced `TypeError`. The established gate contract already requires detached CPU/float64 inputs, and another in-repo implementation converts in the correct order. Moving to CPU before float64 is therefore a D-19 conformance repair, not a scientific choice. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/evidence/runs/stage0-rerun-seed41-attempt-02/failure/trip.json:5-30; pinn/training/guards.py:487-617; pinn/training/validation_gate.py:243-248; pinn/verification/gate_metrics.py:72-76; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:309-336]

**Primary recommendation:** plan a diagnosis/repair gate before any new pre-registration or launch. Repair and test the validation conversion and normal evidence tooling; audit the training-vs-validation causal-weight telemetry seam; then require an owner checkpoint. If no independently grounded causal-front conformance defect and repair is found, stop without launching. Do not treat a repeated unchanged run as RUN-01 closure merely because the validation exception is repaired. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:274-349; .planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md:182-206]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|---|---|---|---|
| Causal-front computation | Training controller | Step guard | Controller derives `w_n`/`front_idx`; guard owns high-water/window/HALT. [VERIFIED: pinn/training/controllers.py:651-702; pinn/training/guards.py:487-617] |
| Validation conservation gate | Validation adapter | Verification metric | Adapter converts full trajectories and publishes sidecars; metric consumes detached CPU/float64 tensors. [VERIFIED: pinn/training/validation_gate.py:199-292; pinn/verification/gate_metrics.py:72-76] |
| Generation orchestration | Phase execution/evidence | Training CLI | Ledger, pre-registration, immutable identities, and owner checkpoints gate the CLI launch. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:274-359] |
| Three-seed characterization | Evidence builder | Evidence verifier | Builder projects authoritative run artifacts; verifier independently validates hashes, eligibility, band membership, and terminal markers. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:79-348] |

## Project Constraints (from AGENTS.md)

- Treat source-silent semantic choices as blocking: articulate the engineering issue, cite silent sources, route the decision to the owner, and do not invent a resolution. [VERIFIED: AGENTS.md:21-102]
- Work in the milestone-owning worktree and surface branch/worktree state before GSD work. Phase 50's locked execution location is `.worktrees/trainex` on `milestone/v2.2`. [VERIFIED: AGENTS.md:148-182; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:422-432]
- Treat existing worktree changes as user-owned; do not discard them or run destructive Git operations without exact approval and a recovery checkpoint. [VERIFIED: AGENTS.md:123-147]
- Any future commit must use `scripts/agent-commit`, explicit owned paths, `GIT_AGENT_ID`, and `GIT_AGENT_OWNED_PATHS`; never broad-stage or push the protected milestone branch directly. [VERIFIED: AGENTS.md:184-221]
- Run relevant targeted verification, then broader checks in proportion to risk, and distinguish new failures from unrelated baseline failures. [VERIFIED: AGENTS.md:240-260]

## Standard Stack

### Core

| Component | Locked Version/Surface | Purpose | Why Standard Here |
|---|---|---|---|
| Python | `3.11.15` | Training, evidence tools, unittest | Pinned by the protocol/environment fingerprint. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:104-112,422-432] |
| PyTorch | `2.12.1`, MPS available, production `float32` | Model execution and validation tensors | Pinned to v2.0 parity; the TypeError is version/backend-specific and reproduced on this target. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:104-112,422-432; target-host runtime probe 2026-08-14] |
| `unittest` | Python standard library | Regression and phase tests | Existing Phase 46/50 tests use it; no dependency addition is needed. [VERIFIED: tests/phase46/test_gate_composition.py:1-20; tests/phase50/test_validation_full_pool.py:1-24] |
| SHA-256 (`shasum -a 256`) | System tool | Immutable evidence and config/corpus/head receipts | Required by the locked ledger/extraction contract. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:351-359,456-479] |

### Supporting

| Component | Version/Surface | Purpose | When to Use |
|---|---|---|---|
| Conda | `pinn-train`, invoked by absolute path | Reproduce pinned runtime | Every smoke, verify, test, and graded command. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:422-432] |
| `scripts/train-unattended.sh` | Existing repository script | Durable launch/transcript surface | Future authorized smoke and graded runs. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/evidence/run-ledger.md:500-520] |
| Phase evidence builder/verifier | `build_phase50_evidence.py`, `verify_phase50_evidence.py` | Copy, hash, characterize, finalize, independently verify | Complete the currently reserved normal mode before a later band. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/evidence/build_phase50_evidence.py:153-186; .planning/phases/50-valid-stage-0-re-run/evidence/verify_phase50_evidence.py:754-778] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|---|---|---|
| CPU-before-float64 conversion | Change gate dtype to float32 | Prohibited semantic drift: existing gate-metric contract explicitly normalizes to CPU/float64. [VERIFIED: pinn/verification/gate_metrics.py:72-76] |
| Grounded causal diagnosis | Raise `N`, alter `eta`, threshold, replay, LR, warmup, budget, or collocation | Prohibited recipe tuning/source-silent adjudication. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:309-349,711-758] |
| Fresh generation | Resume or mix attempts/code heads | Prohibited because the collocation RNG is not restored and generations are identity-bound. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:274-293,338-349] |

**Installation:** none. This continuation uses only the locked environment and repository code. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:422-432]

## Package Legitimacy Audit

Not applicable: the phase must add no dependency, and this research recommends none. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:501-514]

## Evidence-Backed Technical Diagnosis

### Seed-41 invariant-B halt

The attempt's authoritative trip record quotes `"guard": "invariant_b"`, `"step": 501`, `"threshold": 500`, `"value": 501`, and `"disposition": "HALT"`; status is `"state": "failed"`, `"step": 501`. All 502 retained log records have `front_idx=0`. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/evidence/runs/stage0-rerun-seed41-attempt-02/failure/trip.json:5-30; .planning/phases/50-valid-stage-0-re-run/evidence/runs/stage0-rerun-seed41-attempt-02/status.json:18-28; .planning/phases/50-valid-stage-0-re-run/evidence/runs/stage0-rerun-seed41-attempt-02/logs/train.log.jsonl:1-502]

The implementation computes mean squared residual per causal bin, cumulative-prefix exponential weights, and `front_idx = max(n where w_n > 0.5)`; the guard maintains a high-water mark and halts when an unsaturated front has not advanced for more than `N`. The code quotes the locked defaults `"causal_eta": 1.0` and `"causal_w1": 1.0`. [VERIFIED: pinn/training/controllers.py:651-702; pinn/loss_catalog.py:283-347; pinn/training/guards.py:487-617; pinn/constants.py:67-72]

With `eta=1`, `front_idx=0` means the next weight did not exceed 0.5, equivalently the first-bin mean squared residual was not below `ln(2)` at the evaluated step. This is a direct algebraic consequence of the implemented formula, not a diagnosis of why the residual stayed there. [VERIFIED: pinn/loss_catalog.py:303-334; .planning/phases/49-conformance-gate/49-RESEARCH.md:193-215]

The evidence therefore distinguishes four possibilities:

| Class | Finding | Planner consequence |
|---|---|---|
| Recipe/config issue | The frozen recipe may produce expected-but-unacceptable slow/no front advance, but the observed number cannot authorize a recipe change. No retained source identifies a wrong literal. [VERIFIED: configs/stage0-rerun-seed41.yaml:1-68; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:309-336] | Do not edit recipe values. If no independent contract mismatch is found, stop at owner checkpoint. |
| Implementation nonconformance | The causal-weight formula and invariant window match their locked contracts; no causal guard defect is established. [VERIFIED: pinn/training/controllers.py:651-702; pinn/training/guards.py:487-617; .planning/phases/49-conformance-gate/49-RESEARCH.md:193-215] | A repair requires new evidence independent of this run; “make it pass” is insufficient. |
| Expected dynamics | `front_idx=0` is mathematically compatible with large first-bin residual under the specified weighting. [VERIFIED: pinn/loss_catalog.py:303-334] | Treat the HALT as a valid gate outcome, not proof the gate is broken. |
| Source-silent semantics | The retained sources do not decide whether the frozen recipe should be rerun unchanged, whether dynamics should be changed, or which causal mechanism is wrong. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-GAPS.md:252-281; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:321-336] | Preserve GAP-50-03 Option A unchanged. Surface a new owner authorization/grounding checkpoint before another generation. |

One telemetry seam warrants a conformance audit before relying on D-24 front trajectories: the training guard consumes training-step causal stats before validation, but `_run_validation` also calls the loss composer and can overwrite the controller's `_last_widened_details`; `_log_step` runs afterward. The code already snapshots gradient telemetry specifically because validation overwrites composer state, but it does not visibly apply the same protection to causal-weight stats. This cannot have caused the HALT—the guard runs before validation—but it may make validation-step log rows describe validation weights rather than training weights. [VERIFIED: pinn/train.py:799-807,929-933,1058-1118,1173-1190]

### Validation-gate TypeError

All five scheduled validation rows quote `"gate_status":"failed:TypeError"`, and the run produced no validation sidecar. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/evidence/runs/stage0-rerun-seed41-attempt-02/validation.jsonl:1-5; .planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md:121-145]

The call chain is:

1. The production model emits MPS float32 predicted positions under the locked config. [VERIFIED: configs/stage0-rerun-seed41.yaml:1-68]
2. `compute_validation_gate` calls `torch.as_tensor(predicted, dtype=torch.float64, device=torch.device("cpu"))`. [VERIFIED: pinn/training/validation_gate.py:243-248]
3. On the locked torch/MPS host, that one-step call reproduces exactly: `TypeError: Cannot convert a MPS Tensor to float64 dtype as the MPS framework doesn't support float64. Please use float32 instead.` [VERIFIED: target-host runtime probe 2026-08-14]
4. The broad validation catch persists only `failed:TypeError`, erasing the message and continuing training. [VERIFIED: pinn/train.py:153-174]

The established metric adapter uses the semantically correct order: detach, move to CPU, then cast to float64. A focused repair at the production validation adapter is therefore uniquely grounded at the semantic level; exact syntax remains implementation discretion. It must not change pool membership, shape, frame, thresholds, `gate_verdict`, or any recipe value. [VERIFIED: pinn/verification/gate_metrics.py:72-76; pinn/training/validation_gate.py:199-292; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:309-319]

## Architecture Patterns

### System Architecture Diagram

```text
locked code/config/corpus identities
          |
          v
diagnose conformance seams ---- no grounded causal repair ----> OWNER STOP/CHECKPOINT
          |
          +---- grounded repairs + regression tests + normal evidence tooling
          |
          v
immutable next-generation pre-registration + open ledger + clean-head receipts
          |
          v
explicit owner launch authorization
          |
          v
fresh smoke --fail--> terminal generation / archive / no graded launch
          |
        pass
          v
owner one-way-door authorization
          |
          v
seed 41 --fail/halt--> terminal generation / no seeds 42 or 43 / no band
          |
        finish
          v
seed 42 --fail--> terminal generation / no seed 43 / no band
          |
        finish
          v
seed 43 --fail--> terminal generation / no band
          |
        finish
          v
normal extraction -> band record -> fixed eligibility fallback -> candidate receipt
          |
          v
independent verifier -> Phase-50 verification -> RUN-01/RUN-02 closure
```

This sequence derives from the locked smoke/seed order, no-commit window, fresh-generation rule, and current missing success criteria. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:274-349; .planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md:147-165]

### Recommended Project Structure

```text
.planning/phases/50-valid-stage-0-re-run/
├── 50-01..50-05-PLAN.md / SUMMARY.md  # immutable executed history
├── 50-PRE-REGISTRATION.md             # preserve selection-policy bytes; amend source identity for a new generation
├── 50-GAPS.md                         # preserve GAP-50-03 Option A and authorization boundary
├── evidence/
│   ├── build_phase50_evidence.py      # implement reserved normal mode before the run window
│   ├── verify_phase50_evidence.py     # implement reserved normal verification
│   ├── run-ledger.md                  # append-only generation/launch record
│   ├── runs/                          # faithful small-artifact copies
│   ├── source-manifest.json
│   ├── band-record.md
│   ├── candidate-receipt.json
│   └── manifest.json
└── 50-VERIFICATION.md                 # phase-goal authority; update only after evidence verification

pinn/training/validation_gate.py       # narrow MPS->CPU->float64 repair
tests/phase46/                          # contract regression for production validation adapter/wiring
tests/phase50/                          # phase-specific full-pool/evidence/telemetry regressions
```

Paths and responsibilities follow the existing plans and evidence seams; existing plan, summary, gap, and evidence files are preserved rather than rewritten. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:79-348; .planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md:147-206]

### Pattern 1: CPU before float64 on MPS

```python
# Semantics grounded by pinn/verification/gate_metrics.py:72-76.
# Exact syntax is implementation discretion.
predicted_positions = (
    torch.as_tensor(predicted)
    .detach()
    .cpu()
    .to(dtype=torch.float64)
    .reshape(-1, 3, 3)
)
```

Every discrete value in this example is already present in the source contract: `torch.float64`, CPU normalization, and the position shape `(-1, 3, 3)`. [VERIFIED: pinn/training/validation_gate.py:243-248; pinn/verification/gate_metrics.py:72-76]

### Pattern 2: Generation-gated orchestration

Each launch requires a committed, immutable source/config/corpus/environment identity, a provisional ledger entry before spawn, a closed ledger entry after exit, and terminal closure on any drift or failure. No attempt is overwritten, resumed, or silently discarded. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:274-359]

### Pattern 3: Project, do not recompute

Normal extraction copies authoritative `gate_*` values and referenced sidecars, verifies their hashes/schema, and characterizes them descriptively. It must not recompute validation epsilon from raw predictions, choose a better seed, or synthesize a partial band. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:370-418; .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:190-348]

### Anti-Patterns to Avoid

- **Repair-by-outcome:** changing any causal parameter because `front_idx=0` was observed violates SCOPE-29. [VERIFIED: .planning/REQUIREMENTS.md:82-82]
- **Validation-only optimism:** fixing the TypeError does not establish that seed 41 can satisfy invariant B. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md:121-165]
- **Run-before-tooling:** normal builder/verifier commands are currently reserved and fail; implement/test them before the zero-commit run window. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/evidence/build_phase50_evidence.py:153-186; .planning/phases/50-valid-stage-0-re-run/evidence/verify_phase50_evidence.py:754-778]
- **Partial-band finalization:** seeds 42/43 absent means `final_band_generation` must remain null and no candidate may exist. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md:28-33]
- **Mid-band commit:** any code/config commit invalidates the calibration and generation identity. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:274-293]
- **Fail-open instrumentation:** `failed:TypeError` must be a terminal smoke/graded precondition failure for the next generation, not a tolerable validation row. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:399-409]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---|---|---|---|
| Gate conversion semantics | New dtype/backend policy | Existing CPU/float64 adapter order in `gate_metrics.py` | Avoids changing metric precision or backend semantics. [VERIFIED: pinn/verification/gate_metrics.py:72-76] |
| Causal-front remedy | Ad hoc threshold/window/eta/warmup | Owner-grounded contract decision after diagnostic evidence | All such values affect experiment semantics and are source-silent here. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:309-349,711-758] |
| Band statistics | New scoring/ranking/CI | Existing D-24 descriptive projection and fixed candidate policy | Prevents leakage and false inference from `n=3`. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:370-418] |
| Artifact integrity | Informal copies/manual receipts | Existing builder/verifier plus SHA-256 manifest pattern | Makes every source/copy identity re-derivable. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:79-348] |
| Retry/resume | New recovery logic | Fresh generation from step zero under D-21 | Resume omits independent collocation RNG state. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:338-349] |

**Key insight:** this phase's hard part is epistemic integrity. The runtime bug with an existing contract gets repaired; the causal outcome without a grounded remedy gets surfaced, not “fixed.”

## Minimum Dependency Order for a Legitimate Later Run

The planner should encode these as hard dependencies, not parallel waves:

1. **Preserve history and establish the boundary.** Treat plans/summaries 50-01..50-05, generations 1–3, and GAP-50-03 Option A as immutable history. The present authorization covers research/planning only and does not authorize another launch. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-GAPS.md:252-281; .planning/phases/50-valid-stage-0-re-run/50-05-SUMMARY.md:137-154]
2. **Preflight diagnosis.** Reproduce the validation TypeError with a tensor-only MPS probe; trace invariant-B inputs and training-vs-validation telemetry; inventory any candidate divergence against already locked contracts. Do not launch training or validation. [VERIFIED: pinn/training/validation_gate.py:243-248; pinn/train.py:799-807,929-933,1058-1190]
3. **Grounded implementation repair and tests.** Fix only the CPU-before-float64 conversion. Repair the causal telemetry snapshot only if a regression proves the overwrite. A causal-front behavioral repair is admissible only if independently grounded by an existing locked source, not seed-41 output. [VERIFIED: pinn/verification/gate_metrics.py:72-76; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:309-319]
4. **Complete normal evidence tooling.** Implement the normal builder/verifier paths already specified by 50-03, with fixture tests, while retaining terminal-mode behavior. These code commits must land before smoke. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:79-348; .planning/phases/50-valid-stage-0-re-run/evidence/build_phase50_evidence.py:153-186]
5. **Causal-grounding owner checkpoint.** Present the diagnosis and exact conformance classification. If no grounded causal repair exists, stop. The owner must decide whether a later unchanged attempt is authorized or supply a grounded remedy; the planner may not infer either from GAP-50-03. This checkpoint does not revise GAP-50-03's historical ruling. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-GAPS.md:252-281; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:309-349]
6. **Immutable next-generation pre-registration.** Only after all code/config commits: append a new generation to the ledger, archive existing canonical run directories with hash-equality receipts, rebind source identity to the new ancestor, and prove the selection-policy bytes remain unchanged. Freeze configs and capture clean-head/corpus/environment/calibration identities. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:274-293,351-359]
7. **Explicit owner launch authorization.** Obtain authorization for the exact generation/head/configs before any smoke. [VERIFIED: .planning/STATE.md:246-270; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:295-305]
8. **Fresh repaired-head smoke.** Run the seed-42 smoke. Require clean preflight, finished Stage 0, valid real-corpus metadata, successful validation gate events/sidecars, no `failed:TypeError`, no Stage-1 artifact, and valid timing calibration. Any failure terminally closes the generation before graded work. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:229-293]
9. **Owner one-way-door checkpoint.** Present smoke receipts and request graded-band authorization. No seed launch is implied by smoke success. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:229-305]
10. **Full seed 41.** Launch from step zero for 1000 steps. Require finished disposition, invariant A throughout, causal-front advance by step 500, validation at all ten planned opportunities with healthy sidecars, and all identity/held-out fences. If it halts or fails, terminally close; do not launch 42/43 and do not create a band/candidate. [VERIFIED: .planning/ROADMAP.md:211-231; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:321-368]
11. **Seeds 42 then 43.** Launch each only after the predecessor satisfies the same finished-run criteria, with configs differing only in seed/name and no intervening commit. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:132-140,274-305]
12. **Three-seed extraction and characterization.** Run normal extraction, build the D-24 band record, apply only the fixed eligibility order, finalize candidate/manifest, run independent verification, then update Phase-50 verification and requirement status. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:79-376; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:370-418,481-499]

## Exact Planner Artifacts and Commands

### Code/test artifacts before the run window

| Artifact | Required content | Terminal criterion |
|---|---|---|
| `pinn/training/validation_gate.py` | CPU transfer before float64 cast; no metric/config changes | MPS float32 regression reaches the CPU/float64 gate adapter without exception. [VERIFIED: pinn/training/validation_gate.py:243-248; pinn/verification/gate_metrics.py:72-76] |
| `tests/phase46/test_gate_composition.py` | Production-path MPS regression asserting detached CPU float64 positions/times/masses | Passes on target MPS; a target-host skip is not acceptable because MPS availability is a locked precondition. [VERIFIED: tests/phase46/test_gate_composition.py:1-20; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:422-432] |
| `tests/phase46/test_validation_wiring.py` | Wiring test that `_run_validation_gate_pass` returns healthy status and publishes/revalidates a sidecar on MPS | No `failed:TypeError`; sidecar schema/relative path revalidates. [VERIFIED: tests/phase46/test_validation_wiring.py:1-30; pinn/training/validation_gate.py:199-292] |
| Phase-50 telemetry regression | Ensure guard and `train.log.jsonl` front stats both refer to the training composer result at validation steps | Either prove no defect or land a narrow snapshot repair before preregistration; never use it to alter the guard decision. [VERIFIED: pinn/train.py:929-933,1058-1190] |
| `evidence/build_phase50_evidence.py` | Implement all normal subcommands from 50-03 without weakening terminal mode | Fixture-based source manifest, run copies, band record, candidate receipt, manifest. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:79-348] |
| `evidence/verify_phase50_evidence.py` | Implement corresponding independent normal verification | Rejects missing/partial band, invalid sidecar, drift, wrong eligibility, unexpected evaluation, or hash mismatch. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:269-348] |

### Cheap pre-run test commands

```bash
<home>/miniforge3/bin/conda run -n pinn-train \
  python -m unittest \
  tests.phase46.test_gate_composition \
  tests.phase46.test_validation_wiring \
  tests.phase50.test_validation_full_pool -v
```

The current unmodified baseline completed 52 tests successfully; the repaired implementation must add MPS-specific assertions to this command rather than relying on the CPU fixtures that missed the defect. [VERIFIED: target-host test run 2026-08-14; tests/phase46/_fixtures.py:1-120]

```bash
<home>/miniforge3/bin/conda run -n pinn-train \
  python -m unittest discover -s tests -p 'test_*.py' -v
git diff --check
```

Run the full unittest suite and whitespace check after all code/config/tooling commits and before creating the new pre-registration binding. [VERIFIED: AGENTS.md:240-260; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:274-293]

### Pre-registration and identity receipts

The planner must create or update, append-only where applicable:

- `50-PRE-REGISTRATION.md`: new-generation source-identity binding; byte-identical seed-42/`best.pt`/42→41→43 selection policy. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-PRE-REGISTRATION.md:20-95,218-340]
- `evidence/run-ledger.md`: generation-open row, provisional pre-spawn row, closed post-exit row, archive and identity receipts. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/evidence/run-ledger.md:5-43,500-520]
- `evidence/generation-N-source-identity.json` and cleanliness/config/corpus/environment/calibration receipts using the existing ledger schema; exact filename is planner discretion, fields are not. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:351-359,501-514]
- Config-delta and byte-diff receipts proving no recipe change and seed/name-only graded differences. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:115-158]

### Future launch form

After both owner checkpoints, use the established unattended form, substituting only the preregistered next-generation config names:

```bash
nohup <home>/miniforge3/bin/conda run --no-capture-output \
  -n pinn-train bash scripts/train-unattended.sh \
  --config configs/<pre-registered-config>.yaml --stage-0-only
```

This is a command form, not launch authorization. Every exact invocation must be written provisionally to the ledger before spawn and closed after exit. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/evidence/run-ledger.md:500-520; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:351-359]

If the smoke's calibrated projection exceeds 1800 seconds, the only allowed contingency is:

```bash
<home>/miniforge3/bin/conda run -n pinn-train python -m pinn.verify
```

[VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:295-305]

### Normal extraction/finalization commands

The planner should reuse the exact CLI shapes already specified in 50-03 rather than inventing a second evidence interface:

```bash
<home>/miniforge3/bin/conda run -n pinn-train \
  python .planning/phases/50-valid-stage-0-re-run/evidence/build_phase50_evidence.py \
  extract --repo-root <home>/Desktop/3_body_problem/.worktrees/trainex

<home>/miniforge3/bin/conda run -n pinn-train \
  python .planning/phases/50-valid-stage-0-re-run/evidence/build_phase50_evidence.py \
  band --repo-root <home>/Desktop/3_body_problem/.worktrees/trainex

<home>/miniforge3/bin/conda run -n pinn-train \
  python .planning/phases/50-valid-stage-0-re-run/evidence/build_phase50_evidence.py \
  candidate --repo-root <home>/Desktop/3_body_problem/.worktrees/trainex

<home>/miniforge3/bin/conda run -n pinn-train \
  python .planning/phases/50-valid-stage-0-re-run/evidence/build_phase50_evidence.py \
  finalize --repo-root <home>/Desktop/3_body_problem/.worktrees/trainex

<home>/miniforge3/bin/conda run -n pinn-train \
  python .planning/phases/50-valid-stage-0-re-run/evidence/verify_phase50_evidence.py \
  all --repo-root <home>/Desktop/3_body_problem/.worktrees/trainex
```

These are the exact option names and repository-root argument specified by 50-03 and already reserved by the parser skeleton. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:156-174,195-266,297-331; .planning/phases/50-valid-stage-0-re-run/evidence/build_phase50_evidence.py:189-200; .planning/phases/50-valid-stage-0-re-run/evidence/verify_phase50_evidence.py:781-805]

### Required success artifacts

| Artifact | Required end state |
|---|---|
| Per-run committed copies | all prescribed config, summary, preflight, training metadata, splits, curriculum, validation rows, referenced sidecars, status, RNG provenance, `train.log.jsonl`, and failure copies with source/copy hashes. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:456-479] |
| `evidence/source-manifest.json` | Three finished runs in one finalized generation; exact source/copy identities and no mixed code heads. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:79-187] |
| `evidence/band-record.md` | D-24 fields for all seeds, ten healthy validation events each, descriptive three-seed epsilon/SCS characterization, no ranking/verdict. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:370-418] |
| `evidence/candidate-receipt.json` | Candidate selected only by structural eligibility using 42→41→43 and `best.pt`. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-PRE-REGISTRATION.md:20-95] |
| `evidence/manifest.json` | Hash-complete final evidence set; independent verifier passes. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:269-348] |
| `50-VERIFICATION.md` | All four roadmap truths pass; RUN-01/RUN-02 then become eligible for verification-time checkbox updates. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md:17-33; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:481-499] |

## Terminal Criteria and Conformance Fences

### A run is successful only if all are true

- It starts from step zero under the pre-registered clean head/config/corpus/environment identity and never resumes. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:274-293,338-359]
- Preflight reports zero unwaived divergences and all persisted stages remain zero with no Stage-1 checkpoint. [VERIFIED: .planning/ROADMAP.md:216-224; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:59-98]
- The graded run finishes all 1000 Stage-0 steps; invariant A holds; invariant B's high-water advances within 500; disposition is `finished`. [VERIFIED: .planning/ROADMAP.md:216-224; configs/stage0-rerun-seed41.yaml:1-68]
- Each graded run produces ten validation events at steps 100..1000; each has healthy `gate_status`, valid referenced sidecar, and the final summary projects the gate fields without recomputation. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:104-112,370-409]
- `eval01_precondition_i` and `eval01_precondition_iii` are true, and no held-out evaluation/test materialization exists. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:361-409]
- Smoke and seed 42 have byte-identical splits and exactly equal `s_h`/`n_train`; each graded split hash is compared with the pinned v2.0 hash and any mismatch is qualified. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:214-225,262-272]

### A generation closes terminally if any occur

- preflight refusal, identity/config/head/corpus drift, invalid calibration, unexpected resume, invariant/guard HALT, non-finite or unknown failure, missing/invalid validation sidecar, or any `failed:TypeError`; [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:274-359,399-409]
- seed 41 does not finish—in which case 42/43 do not launch—or seed 42 does not finish—in which case 43 does not launch; [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:295-305,321-349]
- a mid-generation code/config commit becomes necessary; archive all attempts and start only under a separately authorized, newly bound generation. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:274-293]

### Anti-tuning/conformance fences

- Freeze `N=500`, replay count/default, thresholds, optimizer/loss values, 1000-step budget, seed order, candidate seed/checkpoint/fallback, validation cadence, and held-out policy. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:59-225,251-319]
- No change may cite observed seed-41 metrics as its justification; each repair needs a pre-existing contract/source and a regression proving conformance. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:309-319]
- No partial band, metric-based seed/checkpoint choice, evaluation, test split materialization, resume, retry except the narrow positive disk/external-memory case, or mixed generation. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:174-212,274-418]
- Do not reopen or reinterpret GAP-50-03. Its Option A accurately records generation 3's terminal disposition; a future generation requires new explicit authorization. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-GAPS.md:252-281]

## Common Pitfalls

### Pitfall 1: Treating a gate HALT as a guard bug

**What goes wrong:** the planner weakens `N`, threshold, or causal weighting to obtain a finished run. **Why:** the observed halt is confused with implementation nonconformance. **Avoidance:** prove a mismatch against a locked source independently of the output or stop for owner direction. **Warning sign:** repair rationale contains “front stayed at zero,” “too strict,” or “just get past step 501.” [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:309-336]

### Pitfall 2: Fixing validation but assuming RUN-01 will close

**What goes wrong:** a new generation is launched after the dtype repair even though the causal uncertainty is unchanged. **Why:** two independent failures are collapsed into one. **Avoidance:** separate repair gate and causal-grounding checkpoint. **Warning sign:** the plan moves directly from the MPS regression to preregistration. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md:121-165]

### Pitfall 3: CPU fixtures hide MPS transfer semantics

**What goes wrong:** unit tests pass while production MPS fails. **Why:** CPU float64 fixtures never exercise an MPS float32-to-CPU-float64 transition. **Avoidance:** add a target-MPS regression and assert the adapter receives detached CPU float64 tensors. **Warning sign:** the new test can pass with `predicted` already on CPU. [VERIFIED: tests/phase46/_fixtures.py:1-120; pinn/training/validation_gate.py:243-248]

### Pitfall 4: Logging validation causal weights as training weights

**What goes wrong:** D-24 front trajectories are tainted at validation steps although guard behavior is correct. **Why:** validation reuses the loss composer between guard evaluation and logging. **Avoidance:** prove and, if necessary, snapshot training causal details exactly as gradient telemetry is snapshotted. **Warning sign:** validation-step log weights differ from the values passed to `StepGuards`. [VERIFIED: pinn/train.py:929-933,1058-1190]

### Pitfall 5: Entering the no-commit window with incomplete evidence tooling

**What goes wrong:** a successful band cannot be finalized without a code commit, invalidating its generation. **Why:** normal commands remain reserved. **Avoidance:** implement and fixture-test every normal command before preregistration/smoke. **Warning sign:** `build_phase50_evidence.py` still emits “requires a generation-complete band.” [VERIFIED: .planning/phases/50-valid-stage-0-re-run/evidence/build_phase50_evidence.py:153-186]

### Pitfall 6: Confusing current planning authority with launch authority

**What goes wrong:** a run starts because a plan exists. **Why:** the owner checkpoint is omitted. **Avoidance:** explicit authorization tasks before smoke and before graded seeds. **Warning sign:** a plan task contains `nohup` without a preceding blocking checkpoint. [VERIFIED: .planning/STATE.md:246-270; .planning/phases/50-valid-stage-0-re-run/50-GAPS.md:252-281]

## State of the Art Within This Phase

| Executed attempt | Result | Meaning for continuation |
|---|---|---|
| 50-01 | Configs, stage-0 ceiling, and preregistration established | Preserve; do not redesign recipe/selection policy. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-01-SUMMARY.md:1-120] |
| 50-02 / generation 1 | Terminal before valid full band | Preserve as provenance. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-02-SUMMARY.md:1-160] |
| 50-04 / generation 2 | Full-pool validation repair, terminal generation | Preserve; no mixing with later code state. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-04-SUMMARY.md:1-180] |
| 50-05 / generation 3 | Smoke finished; seed41 invariant-B HALT; 42/43 not launched; no band | Authoritative remaining phase-goal failure. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-05-SUMMARY.md:94-154] |
| Current research | MPS validation conversion defect grounded; causal remedy unresolved | Plan repairs/tooling and stop for owner grounding before another generation. [VERIFIED: pinn/training/validation_gate.py:243-248; .planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md:121-206] |

**Deprecated/outdated:** treating 50-03 normal evidence flow as already executable is false; only terminal evidence mode is implemented. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/evidence/build_phase50_evidence.py:153-186; .planning/phases/50-valid-stage-0-re-run/evidence/verify_phase50_evidence.py:754-778]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|---|---|---|
| — | None. Recommendations are derived from opened repository sources and target-host probes; unresolved semantic questions are explicitly left open. | — | — |

## Open Questions

1. **DISPOSITIONED — no independently grounded causal-front defect or remedy exists in the current sources.**
   - Question resolved for planning: what independently grounded causal-front conformance defect, if any, explains seed 41?
   - What we know: the formula, guard, frozen config, and HALT evidence are internally consistent; `front_idx` stayed zero. [VERIFIED: pinn/training/controllers.py:651-702; pinn/training/guards.py:487-617]
   - What's unclear: whether a locked contract is violated upstream of the front computation, or whether the behavior is the specified recipe's expected dynamics. Retained logs do not answer this. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md:182-206]
   - Disposition: automatic causal-front repair is prohibited. Plan 50-06 may report only the result of the separately bounded telemetry-overwrite regression and must record `grounded_causal_front_repair: none-in-current-sources`; it may not infer or implement a dynamics remedy. Plan 50-08 owns the owner decision when no remedy exists.
2. **DISPOSITIONED — Plan 50-06's bounded deterministic regression decides the telemetry implementation branch.**
   - Question resolved for planning: does validation overwrite the causal stats later written to the training log?
   - What we know: the composer runs for training and validation; guard precedes validation; log follows validation; gradient stats already need a snapshot. [VERIFIED: pinn/train.py:929-933,1058-1190]
   - What's unclear: whether `_last_widened_details` is the actual source of logged `w_*` at validation steps in this code path.
   - Disposition: run the regression against the current implementation before editing production. Repair only if the overwrite is proven; if the regression is already green, leave production unchanged and record `telemetry_overwrite_proven: false`. Both outcomes are explicit, and neither assumes or changes causal dynamics.
3. **DISPOSITIONED — no later-generation authorization exists in the current sources.**
   - Question reserved to the owner: will the owner authorize a new unchanged generation after grounded repairs when no causal defect is found?
   - What we know: GAP-50-03 authorized no further generation at that time and explicitly left any later generation separately authorized. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-GAPS.md:252-281]
   - What's unclear: current launch authorization; this research request grants none.
   - Disposition: Plan 50-08 owns an explicit prerequisite decision on whether unchanged-recipe preregistration may proceed. Later exact-identity smoke and graded-launch checkpoints remain separate; preregistration authority never implies process-launch authority.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|---|---|---:|---|---|
| Git | identity/cleanliness/provenance | ✓ | 2.54.0 | none [VERIFIED: target-host environment probe 2026-08-14] |
| Conda | locked `pinn-train` runtime | ✓ | 26.3.2 | none [VERIFIED: target-host environment probe 2026-08-14] |
| Python in `pinn-train` | tests/tools/runs | ✓ | 3.11.15 | none [VERIFIED: target-host environment probe 2026-08-14] |
| PyTorch in `pinn-train` | training/validation | ✓ | 2.12.1 | none [VERIFIED: target-host environment probe 2026-08-14] |
| Apple MPS | protocol parity and regression | ✓ | `torch.backends.mps.is_available() == True` | none [VERIFIED: target-host environment probe 2026-08-14] |
| `unittest` | automated validation | ✓ | standard library | none [VERIFIED: target-host test run 2026-08-14] |
| `pytest` | not required | ✗ | not installed | use locked `unittest` suite [VERIFIED: target-host environment probe 2026-08-14] |
| `shasum` | SHA-256 receipts | ✓ | 6.02 | none [VERIFIED: target-host environment probe 2026-08-14] |
| `nohup` | unattended launch | ✓ | system | attended launch allowed by D-discretion [VERIFIED: target-host environment probe 2026-08-14; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:501-514] |
| `setsid` | not required | ✗ | — | existing unattended script/nohup surface [VERIFIED: target-host environment probe 2026-08-14] |

**Missing dependencies with no fallback:** none among required tools. [VERIFIED: target-host environment probe 2026-08-14]

**Missing dependencies with fallback:** `pytest` and `setsid` are absent but not required; use `unittest` and the established launch script. [VERIFIED: target-host environment probe 2026-08-14]

## Validation Architecture

### Test Framework

| Property | Value |
|---|---|
| Framework | Python `unittest` under Python `3.11.15` [VERIFIED: tests/phase46/test_gate_composition.py:1-20; target-host environment probe 2026-08-14] |
| Config file | none; module/discovery invocation [VERIFIED: tests/phase46/test_validation_wiring.py:1-30] |
| Quick run command | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest tests.phase46.test_gate_composition tests.phase46.test_validation_wiring tests.phase50.test_validation_full_pool -v` [VERIFIED: target-host test run 2026-08-14] |
| Full suite command | `<home>/miniforge3/bin/conda run -n pinn-train python -m unittest discover -s tests -p 'test_*.py' -v` [VERIFIED: repository test layout and target-host runtime 2026-08-14] |

### Validation Layers

```text
Layer 0: source/identity checks
  config diffs + head/corpus/env/calibration hashes + prereg bytes
Layer 1: unit contracts (<30 s target per module)
  MPS conversion + sidecar schema + causal telemetry + evidence fixtures
Layer 2: repository suite
  full unittest discovery + git diff --check
Layer 3: smoke (requires owner launch authorization)
  real corpus + preflight + gate + sidecars + stage-0 ceiling + timing
Layer 4: sequential graded runs (requires second owner authorization)
  seed41 -> seed42 -> seed43, fail-closed after each
Layer 5: evidence verification
  copied hashes + D-24 band + fixed eligibility + no held-out touch
Layer 6: phase-goal verification
  four roadmap truths and RUN-01/RUN-02 status
```

This layered architecture prevents expensive execution from becoming the first place a dtype, telemetry, evidence-tool, or identity defect is discovered. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:229-359; .planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md:97-206]

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|---|---|---|---|---|
| RUN-01 | MPS validation adapter conforms to CPU/float64 gate contract | backend unit/integration | quick Phase46/50 command above | ⚠️ Wave 0: existing files, missing MPS-specific regression [VERIFIED: tests/phase46/test_gate_composition.py:1-20; pinn/training/validation_gate.py:243-248] |
| RUN-01 | training causal stats logged without validation overwrite | deterministic unit | `python -m unittest tests.phase50.test_causal_telemetry -v` | ❌ Wave 0 [VERIFIED: pinn/train.py:929-933,1058-1190] |
| RUN-01 | preflight clean, Stage-0-only, invariants A/B, finished 1000-step run | real-corpus smoke/graded integration | authorized CLI plus independent artifact verifier | ✅ runtime code; manual/expensive execution gate [VERIFIED: .planning/ROADMAP.md:216-224] |
| RUN-02 | normal run extraction/source hashes | fixture integration | `python -m unittest tests.phase50.test_evidence_builder -v` | ❌ Wave 0 normal-mode coverage [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:79-187] |
| RUN-02 | D-24 band characterization of exactly three finished seeds | fixture integration | `python -m unittest tests.phase50.test_band_record -v` | ❌ Wave 0 [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:190-266] |
| RUN-02 | fixed eligibility fallback/candidate/final manifest | fixture integration | `python -m unittest tests.phase50.test_candidate_finalization -v` | ❌ Wave 0 [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:269-348] |
| RUN-02 | independent normal verifier rejects partial/mixed/invalid band | negative fixture integration | `python -m unittest tests.phase50.test_evidence_verifier -v` | ❌ Wave 0 [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:269-348] |
| RUN-01/RUN-02 | no evaluation directory/test materialization | artifact policy integration | normal verifier `all` | ❌ normal mode reserved [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:361-368; .planning/phases/50-valid-stage-0-re-run/evidence/verify_phase50_evidence.py:754-805] |

### Required Fixture Matrix

The evidence-tool tests should cover at least:

- one valid three-seed generation with ten valid sidecars per seed;
- missing seed 42 or 43, non-finished disposition, front not advanced, unhealthy gate status, missing/malformed sidecar, mixed head/config generation, and unexpected resume;
- config differences beyond seed/name, validation count/step mismatch, split-hash match and qualified mismatch;
- candidate 42 eligible, candidate 42 structurally ineligible with fallback to 41, 41 ineligible with fallback to 43, and none eligible owner-stop;
- unexpected `evaluation/` or evaluation-attempt artifact;
- source/copy hash mismatch and manifest tampering;
- terminal mode remains byte/behavior compatible with generations 1–3 evidence. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:79-348; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:174-225,351-418]

### Sampling Rate

- **Per task commit:** run the closest module tests plus `git diff --check`. [VERIFIED: AGENTS.md:240-260]
- **Before immutable preregistration:** full unittest discovery, normal builder/verifier fixture suite, exact config diffs, and clean runtime/head checks. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:132-158,274-293]
- **After smoke:** independently validate every smoke artifact/sidecar and the calibration receipt before the graded authorization checkpoint. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:229-272]
- **After each graded seed:** close ledger, verify full-run/invariants/validation/identity/held-out absence before authorizing the next seed. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:295-368]
- **Phase gate:** normal verifier passes; all four roadmap truths pass; only then run phase verification and update RUN-01/RUN-02. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md:17-33; .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:481-499]

### Wave 0 Gaps

- [ ] Add MPS float32 conversion regression to existing Phase-46 composition/wiring tests. [VERIFIED: pinn/training/validation_gate.py:243-248]
- [ ] Add deterministic causal telemetry ownership regression; repair only if it proves overwrite. [VERIFIED: pinn/train.py:929-933,1058-1190]
- [ ] Implement and test normal `extract`, `band`, `candidate`, `finalize`, and verifier `all` paths while preserving terminal mode. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/evidence/build_phase50_evidence.py:153-200; .planning/phases/50-valid-stage-0-re-run/evidence/verify_phase50_evidence.py:754-805]
- [ ] Add positive/negative three-seed fixture matrix above; no training data or job is needed for these tests. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:79-348]

## Security Domain

This is a local scientific-computing/evidence-integrity phase. Authentication, sessions, and network access control are not in scope; input/artifact validation and provenance integrity are. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:351-479]

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---|---:|---|
| V2 Authentication | no | No user/auth boundary in the local CLI workflow. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:422-432] |
| V3 Session Management | no | No session state. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:422-432] |
| V4 Access Control | no | Owner checkpoints are governance gates, not application authorization controls. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:321-349] |
| V5 Input Validation | yes | Strict config/artifact schema validation, relative-path containment, existence/hash checks, and fail-closed normal verifier. [VERIFIED: pinn/training/validation_gate.py:199-292; .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:79-348] |
| V6 Cryptography | limited | Use system SHA-256 for provenance; do not design cryptography or treat hashes as signatures. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:351-359,456-479] |

### Known Threat Patterns

| Pattern | STRIDE | Standard Mitigation |
|---|---|---|
| Evidence path escapes the phase/run root | Tampering | Resolve canonical paths, require relative containment, reject symlinks/escapes in builder and verifier. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:79-187] |
| Existing attempt overwritten or omitted | Repudiation/Tampering | Append-only ledger, immutable archive, source/copy hashes, every launch listed. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:351-359] |
| Partial/mixed band presented as final | Tampering | One finalized generation, three finished seeds, common head/identities, independent normal verifier. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:269-348] |
| Metric-based candidate selection | Information disclosure/experiment leakage | Pre-registered structural policy bytes and eligibility-only fallback. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:162-212] |
| Held-out evaluation spent early | Information disclosure | Reject evaluation directory/attempt and test materialization; Phase 51 alone owns the look. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:361-368] |
| Instrumentation exception appears as a usable metric | Tampering | Keep `gate_status` distinct from verdict; treat non-healthy status/missing sidecar as terminal. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:399-409] |

## Sources

### Primary (HIGH confidence)

- `.planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md` — locked protocol, repair classification, ordering, evidence, and anti-tuning boundaries. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-CONTEXT.md:55-758]
- `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` — RUN-01/RUN-02/SCOPE-29 and success criteria. [VERIFIED: .planning/REQUIREMENTS.md:63-85; .planning/ROADMAP.md:199-232]
- `.planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md` — authoritative incomplete status and validation failure. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-VERIFICATION.md:1-206]
- `.planning/phases/50-valid-stage-0-re-run/50-GAPS.md` — historical GAP-50-03 Option A boundary. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-GAPS.md:252-281]
- Seed-41 trip/status/log/validation evidence — invariant and TypeError observations. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/evidence/runs/stage0-rerun-seed41-attempt-02/failure/trip.json:5-30; .planning/phases/50-valid-stage-0-re-run/evidence/runs/stage0-rerun-seed41-attempt-02/status.json:18-28; .planning/phases/50-valid-stage-0-re-run/evidence/runs/stage0-rerun-seed41-attempt-02/validation.jsonl:1-5]
- `pinn/training/{controllers,guards,validation_gate}.py`, `pinn/loss_catalog.py`, and `pinn/verification/gate_metrics.py` — runtime implementation and established conversion contract. [VERIFIED: pinn/training/controllers.py:651-702; pinn/training/guards.py:487-617; pinn/training/validation_gate.py:199-292; pinn/loss_catalog.py:283-347; pinn/verification/gate_metrics.py:72-76]
- Plans/summaries 50-01..50-05 and evidence tooling — executed history and already specified normal evidence interface. [VERIFIED: .planning/phases/50-valid-stage-0-re-run/50-03-PLAN.md:79-376; .planning/phases/50-valid-stage-0-re-run/50-05-SUMMARY.md:94-154]
- Target-host runtime/test/environment probes on 2026-08-14 — exact MPS TypeError, baseline 52-test pass, and dependency availability. [VERIFIED: target-host runtime/test/environment probes 2026-08-14]

### Secondary (MEDIUM confidence)

- None. No external source was necessary; the task is governed by repository contracts and direct target-host behavior.

### Tertiary (LOW confidence)

- None.

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH — protocol versions and target-host availability were directly verified.
- Architecture: HIGH — call chains, guard ordering, evidence interfaces, and generation governance were read from source and locked artifacts.
- Validation repair: HIGH — exact exception reproduced and the established CPU/float64 order exists in repository code.
- Causal-front root cause: MEDIUM — the invariant symptom and algorithm are proven, but the upstream causal mechanism/remedy remains intentionally unresolved.
- Pitfalls: HIGH — each is a direct failure mode of locked sequencing, existing code, or authoritative verification.

**Research date:** 2026-08-14  
**Valid until:** until any relevant code/config/source-identity commit or owner ruling; otherwise 2026-09-13.
