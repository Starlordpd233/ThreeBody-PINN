# Phase 42: Operator Runbook Surface & Monitoring — Specification

**Created:** 2026-07-18
**Ambiguity score:** 0.16 (gate: ≤ 0.20)
**Requirements:** 7 locked

## Goal

Build the operator-facing surface and monitoring layer on top of the existing v2.0 training loop so that a non-expert operator can run, observe, and hand off a CTL-PINN training run: five documented single-action entry points, a `caffeinate -is` unattended-run wrapper with graceful-signal checkpointing, a canonical JSONL step log + human mirror + secondary TensorBoard view (including a per-time-bin residual panel), a timestamped `status.json` heartbeat, the complete `runs/<name>/` directory contract with a per-run `summary.md`/`summary.json`, and a written runbook under `docs/runbooks/`.

## Background

The training *machinery* exists (Phases 38/40/41): `python -m pinn.train --config <keyed.yaml> [--resume <ckpt>] [--hold-stage]` is the composition root, and `pinn/training/` provides config (`config_yaml.py`), checkpointing (`checkpoint.py`), resume (`resume.py`), guards (`guards.py`, NaN/memory), determinism, controllers, and atomic I/O (`atomic_io.py`). `train.py` already resolves `runs/<name>/` (with a path-traversal guard), freezes `config.yaml`, writes `checkpoints/` + `run_start_rng.pt`, and emits a failure bundle + failure checkpoints; `grad_norm` is computed.

The **operator surface and monitoring are absent**. Scouting `train.py` and `pinn/` confirms: no signal handling (SIGINT/SIGTERM/KeyboardInterrupt all absent), no per-step metrics log loop, no `train.log`/`train.log.jsonl`, no TensorBoard anywhere, no `status.json`/heartbeat/`mem:` line, no residual panel, no `summary.md`/`summary.json`, no `caffeinate` wrapper, no example config under `configs/`, and no training runbook (`docs/runbooks/` holds only EDL/external-research/maintenance/migration). This phase closes exactly that delta. Primary grounding: the training-execution design `docs/work/designs/cross_cutting/training-execution/2026-06-10-training-execution-design.md` §5 (User Runbook Surface) and §6.1 (health), plus the ratified trainex-r1a decisions B-2 (log field set), B-6 (`runs/` contract), B-10 (`caffeinate -is`), and D2 (canonical JSONL). Requirements OPS-01..06.

## Requirements

1. **Operator entry points (OPS-01)**: The five entry points (Setup, Configure, Launch, Monitor, Resume) are each a single documented operator action with internals hidden.
   - Current: `train.py` exposes Launch/Resume as `python -m pinn.train --config … [--resume …] [--hold-stage]`; there is no Setup/Configure/Monitor surface and no operator-facing framing.
   - Target: Launch/Resume remain the existing commands; Setup = documented shell steps; Configure = edit one run YAML; Monitor = read the live log / open TensorBoard. The **only** new executable is the `caffeinate -is` unattended-run wrapper (R2) — no new CLI framework and no per-entry-point wrapper scripts.
   - Acceptance: the runbook (R7) documents all five entry points, each reducible to one operator action; a reviewer can execute Launch and Resume verbatim from the runbook against the example config; no new subcommand/CLI is introduced beyond the `caffeinate` wrapper.

2. **Unattended launch + signal semantics (OPS-02)**: Unattended runs launch under `caffeinate -is`, and interrupts checkpoint gracefully.
   - Current: no signal handling in `pinn.train`; no `caffeinate` wrapper; Ctrl-C aborts without a graceful checkpoint.
   - Target: a committed `caffeinate -is` unattended-run wrapper launches training with sleep prevented (lid-open + AC-power); `pinn.train` installs signal handling — SIGINT once → graceful checkpoint then exit; SIGINT twice → immediate exit (no further checkpoint); SIGTERM → treated as one graceful Ctrl-C (writes a checkpoint).
   - Acceptance: SIGINT-once to a running train process writes a checkpoint and exits cleanly; SIGTERM writes a checkpoint; the wrapper invokes training under `caffeinate -is`. (Signal re-entrancy / panic-mash debounce: Edge E2 backstop.)

3. **Canonical JSONL step log + widened field set + TensorBoard (OPS-03)**: Every logged step emits the widened field set to a canonical machine log, mirrored to a human log, with TensorBoard as a derived secondary view.
   - Current: no per-step metrics loop, no JSONL, no `train.log`, no TensorBoard; `grad_norm` computed but not emitted.
   - Target: every logged step (cadence `log_freq`) appends one JSON object to `runs/<name>/logs/train.log.jsonl` carrying the widened field set — the five loss terms, total, the λ weight vector, grad-norm, `w_n` causal-weight stats, learning rate, seconds-per-step, ETA, step, stage; `runs/<name>/logs/train.log` mirrors each logged step for humans; `runs/<name>/tb/` is a derived, secondary TensorBoard view (never the source of truth; written asynchronously so it does not block the step loop).
   - Acceptance: after ≥ `log_freq` steps, `train.log.jsonl` exists with ≥1 parseable JSON object containing keys for each widened field; `train.log` has a corresponding human line; `tb/` contains TensorBoard event data. (Non-finite serialization: Edge E1 backstop. The exact enumerated field set is the B-2/D2-designed set, ratified by the owner before run #1 — a seam, not invented here.)

4. **status.json heartbeat + mem line (OPS-04a)**: A timestamped heartbeat answers "is it alive / healthy?" from a single file.
   - Current: no `status.json`, no heartbeat, no `mem:` line.
   - Target: `runs/<name>/status.json` is a timestamped heartbeat carrying a wall-clock timestamp, current step, stage/phase, latest losses, and run state (one of `initializing`/`running`/`finished`/`failed`/`interrupted`), rewritten at least every `log_freq` steps AND at least every K seconds; a periodic `mem:` line (MPS/unified-memory footprint) is emitted to `train.log`. Alive-vs-stalled is decidable from `status.json` alone: `now − heartbeat_ts > staleness_threshold ⇒ stalled` (robust even when an L-BFGS line search traps the thread at high GPU with a frozen step count).
   - Acceptance: a reader classifies running vs stalled using only `status.json`'s timestamp age; the `state` field transitions correctly across a normal finish and a killed run; a `mem:` line appears periodically in `train.log`. (Startup-window presence + atomic rewrite: Edge E3 backstop.)

5. **Per-time-bin residual panel (OPS-04b)**: A monitoring panel surfaces causal-weight collapse and propagation failure.
   - Current: no residual panel, no per-time-bin diagnostics, no `w_n` visualization.
   - Target: a per-time-bin residual panel is emitted to TensorBoard showing residual magnitude across collocation time-bins and `w_n` causal-weight statistics over training steps, so an operator can see causal-weight collapse and forward-propagation failure; the diagnostic emits even under collapse/NaN (that is its purpose).
   - Acceptance: after a run with ≥1 curriculum step, TensorBoard contains a per-time-bin residual visualization and `w_n`-vs-step scalars; the panel still emits when `w_n` stats collapse toward zero.

6. **runs/<name>/ directory contract + per-run summary (OPS-05)**: A run produces a self-contained, handoff-able directory.
   - Current: `train.py` writes `runs/<name>/{config.yaml (frozen), checkpoints/, run_start_rng.pt}` + failure bundle/checkpoints; no `logs/`, `tb/`, `summary.md`, `summary.json`, or `status.json`.
   - Target: each run produces the complete contract — `config.yaml` (frozen), `checkpoints/`, `logs/{train.log, train.log.jsonl}`, `tb/`, `summary.md`, `summary.json`, `status.json`, `failure/` — such that handing over the directory reproduces the result. `summary.md`/`summary.json` is a **per-run one-pager**: run header (name, start/end, wall-clock, device), final five loss terms + total, curriculum progression. `summary.md` is **always present** (a failed/interrupted run uses an honest "failed run" template — never absent, never a false success). Excludes the held-out test-set preview, ε_H/SCS acceptance-gate rendering, and cross-run comparison — those are Phase 43 (ACC).
   - Acceptance: a successful run yields every listed file/dir; `summary.md` contains the run header, final losses, and curriculum progression; handing the directory to a fresh checkout reproduces the result from `config.yaml` + `checkpoints/`. (Partial/failed-run contract: Edge E4 backstop.)

7. **Operator runbook + config template (OPS-06)**: A written runbook + example config make the surface usable by a non-expert.
   - Current: `docs/runbooks/` has no training runbook; no example config under `configs/`.
   - Target: a written operator runbook under `docs/runbooks/` covers (1) the mental model, (2) the five entry points, (3) the categorized error surface (symptom → meaning → action), and (4) M5-Pro-specific notes (24 GB unified memory, thermal throttling, sleep/`caffeinate`, single-MPS-device); a committed example config template under `configs/` is loadable/validatable by the config loader.
   - Acceptance: the runbook exists under `docs/runbooks/` with all four sections present; the example config validates against the config loader (`config_yaml.py`) without error.

## Boundaries

**In scope:**
- Signal handling in `pinn.train` (SIGINT once → checkpoint; SIGINT twice → immediate exit; SIGTERM → graceful checkpoint).
- A committed `caffeinate -is` unattended-run wrapper (the only new executable).
- Canonical JSONL step logger (`train.log.jsonl`) + human `train.log` mirror carrying the widened field set.
- TensorBoard writer (`runs/<name>/tb/`) as a derived secondary view, including the per-time-bin residual panel + `w_n`-vs-step scalars.
- `status.json` timestamped heartbeat (with `state` incl. `initializing`) + periodic `mem:` line.
- Completion of the `runs/<name>/` directory contract (`logs/`, `tb/`, `summary.md`, `summary.json`, `status.json`; `checkpoints/`, `config.yaml`, `failure/` already exist).
- Per-run end-of-run `summary.md`/`summary.json` one-pager (header, final 5 losses + total, curriculum progression, wall-clock, device), always present incl. a failed-run template.
- An example config template under `configs/`.
- A written operator runbook under `docs/runbooks/`.

**Out of scope:**
- Held-out test-set preview, ε_H/SCS acceptance-gate rendering, cross-run comparison, the go/adjust/rethink verdict — Phase 43 (ACC-02..06).
- The `verify` pre-flight ladder + ~5-minute smoke test — Phase 43 (ACC-01).
- Hyperparameter selection/tuning — the first run uses documented defaults (design §5.9).
- Distributed training, cloud fallback — excluded by design §5.9 / Q2 decision.
- Training-loop / network / physics internals (Phases 38/40) and config/checkpoint/resume/guards/determinism machinery (Phases 40/41) — consumed, not rebuilt.
- Choice of experiment tracker beyond TensorBoard (W&B/MLflow, PH-10) — TensorBoard is the locked secondary view for v2.0.
- Final ratification of the B-2 log field set and calibration of R-1/R-2/D4-a thresholds — owner-carved seams calibrated at their designed moments (before run #1 / the Phase 43 pilot); Phase 42 builds the surface against the designed set as a seam, it does not pick the values.
- Editing framework specs — read-only in v2.0 (a build-discovered spec defect is surfaced as a gap and routed to a spec milestone).

## Constraints

- **Platform (M5 Pro):** 24 GB unified memory (single budget), macOS 14+ MPS, single MPS device (`torch.mps.device_count() == 1`), thermal throttling on long runs, sleep prevented via `caffeinate -is` (lid-open + AC-power rule). Production default `precision=float32, device=mps` (D1-p); `fp64-CPU` is the in-framework escape hatch.
- **Canonical source of truth:** the JSONL log is the machine source of truth; TensorBoard is a derived, secondary view written asynchronously — no synchronous/blocking plotting (e.g. `matplotlib`) inside the step loop.
- **Heartbeat cadence:** `status.json` rewritten at least every `log_freq` steps AND at least every K seconds; every rewrite atomic (temp + rename) so a reader never sees truncated JSON.
- **Non-degradation:** the logging/monitoring layer must not materially degrade seconds-per-step.
- **Reuse existing seams:** consume the existing `runs/<name>/` root + path-traversal guard, the config loader (`config_yaml.py`), checkpoint/resume, guards, and `atomic_io.py`; do not fork or rebuild them.

## Acceptance Criteria

- [ ] The runbook documents all five entry points (Setup, Configure, Launch, Monitor, Resume), each reducible to one operator action; no new CLI/subcommand beyond the `caffeinate` wrapper.
- [ ] A committed `caffeinate -is` wrapper launches `python -m pinn.train …` with sleep prevented.
- [ ] SIGINT-once writes a checkpoint and exits cleanly; SIGINT-twice exits immediately; SIGTERM writes one graceful checkpoint.
- [ ] After ≥ `log_freq` steps, `runs/<name>/logs/train.log.jsonl` contains ≥1 parseable JSON object with keys for all widened fields (5 loss terms, total, λ vector, grad-norm, `w_n` stats, lr, s/step, ETA, step, stage); `train.log` has the corresponding human line.
- [ ] `runs/<name>/tb/` contains TensorBoard event data, including a per-time-bin residual visualization and `w_n`-vs-step scalars (emitted even under `w_n` collapse).
- [ ] `runs/<name>/status.json` lets a reader classify running-vs-stalled from its timestamp age alone; `state` ∈ {initializing, running, finished, failed, interrupted} transitions correctly across a normal finish and a killed run; a `mem:` line appears periodically in `train.log`.
- [ ] A successful run yields the complete `runs/<name>/` contract (`config.yaml`, `checkpoints/`, `logs/{train.log,train.log.jsonl}`, `tb/`, `summary.md`, `summary.json`, `status.json`, `failure/`); `summary.md` contains the run header, final losses, and curriculum progression; `summary.md` is present (honest failed-run template) even when the run does not succeed.
- [ ] A written operator runbook exists under `docs/runbooks/` with all four sections (mental model, five entry points, categorized error surface, M5-Pro notes); the example `configs/` template validates against `config_yaml.py` without error.
- [ ] **(must-NOT, test)** `status.json`/`summary.md` never report `finished`/healthy when the run diverged (NaN/Inf) or was terminated without completing; `summary.md` contains no fabricated/placeholder metrics.
- [ ] **(must-NOT, test)** committed/handoff artifacts (`train.log`, `train.log.jsonl`, `status.json`, `summary.*`, `failure/`) embed no secrets/tokens and no operator home-directory absolute path / machine-identifying info beyond the run's declared parameters.
- [ ] **(must-NOT, test)** the `caffeinate -is` wrapper does not swallow a non-zero exit — the inner `train.py` exit status propagates through the wrapper.

## Edge Coverage

**Coverage:** 4/4 consequential edges resolved (backstop) · 0 unresolved · 14 raw candidates dismissed by the relevance filter

The compiled edge-probe engine raised 18 candidate rows over R1–R7. After the relevance filter, four consequential edges survive — each resolved as **backstop** (the invariant is locked here; the mechanism is a held-out edge test carried into plan-phase `must_haves`, deliberately leaving mechanism-choice open to avoid a bad forced design).

| Category | Requirement | Status | Resolution / Reason |
|----------|-------------|--------|---------------------|
| precision (non-finite) | R3 | 🧪 backstop (E1) | Invariant: a NaN/Inf loss/grad step stays **written and parseable** and divergence is recorded. Held-out test proves parseability under divergence. Mechanism (JSON `null` vs `is_diverged` flag vs token) → plan-phase; string tokens rejected (break typed parsers). |
| concurrency (signal race) | R2 | 🧪 backstop (E2) | Invariant: an in-progress graceful checkpoint completes **atomically** (temp+rename, never half-written); a second SIGINT escalates to immediate exit. Held-out double-signal test. Mechanism (debounce window to survive a panic-mash of a multi-second L-BFGS checkpoint) → plan-phase. |
| adjacency + empty (status.json) | R4 | 🧪 backstop (E3) | Invariant: liveness is **proven during startup** and every rewrite is atomic (reader never sees truncated JSON); staleness `now − heartbeat_ts > threshold ⇒ stalled`. Held-out test. Mechanism = a `state="initializing"` schema (no fabricated pre-step-0 losses) → plan-phase. |
| boundary (partial run) | R6 | 🧪 backstop (E4) | Invariant: an interrupted/failed run still yields an **honest, handoff-able** `runs/<name>/` — `status.json state ∈ {failed,interrupted}`, `failure/` populated when a guard fired, `summary.md` **present** as a failed-run template (satisfies file-presence for Phase 43, never a misleading success). Held-out killed-run test. Mechanism (failed-run template) → plan-phase. |
| encoding / ordering (R3,R4,R6) | R3,R4,R6 | ⛔ dismissed | Non-applicable: JSON is UTF-8 and object key order is not semantically significant for these fixed-schema artifacts; no length/equality semantics at stake. |
| unclassified (R1,R7) | R1,R7 | ⛔ dismissed | Documentation/deliverable requirements with no data-boundary edge; operational edges live in R2/R6, which are covered above. |
| unclassified (R5) | R5 | ⛔ dismissed | Folded into R5's own acceptance (panel emits under collapse/NaN — the diagnostic-under-failure case is the requirement, not a separate edge). |
| path-traversal (run_name) | R1,R6 | ⛔ dismissed (canon) | `run_name` path-escape is already guarded by `train.py:_resolve_run_dir`; generic path-traversal is canon (owned by `/gsd-secure-phase`), not minted here. |

## Prohibitions (must-NOT)

**Coverage:** 3/3 applicable prohibitions resolved (test tier) · 0 unresolved

Two-stage recall→precision prose pass over R1–R7; routine-engineering dropped, canon items (generic PII/GDPR compliance, path-traversal) referred to `/gsd-secure-phase`. Three bespoke values/safety prohibitions survive, all **test** tier. Wired-check descriptors are intentionally empty (soft capture, CHK-04): the target code does not exist yet, so plan-phase wires each negative test's `check_target`/fixtures.

| Prohibition (must-NOT statement) | Requirement | Status | Verification / Reason |
|----------------------------------|-------------|--------|------------------------|
| MUST NOT present a false-positive health/success signal: `status.json state`/`summary.md` must not read `finished`/healthy when the run diverged (NaN/Inf) or was terminated without completing, and `summary.md` must not contain fabricated/placeholder metrics. | R4,R6 | resolved | verification: test (a NaN/guard-HALT run yields `state ≠ finished` + an honestly-marked summary). Descriptor → plan-phase. Load-bearing honesty layer (design §6.4). |
| MUST NOT leak operator/machine identity or secrets into handoff artifacts: `train.log`, `train.log.jsonl`, `status.json`, `summary.*`, `failure/` must embed no secrets/tokens and no home-directory absolute path / machine-identifying info beyond the run's declared parameters. | R3,R4,R6 | resolved | verification: test (redaction-style negative check; Phase 39 `/Users/` leak precedent). Generic PII compliance = canon (`/gsd-secure-phase`). |
| MUST NOT mask a training failure in unattended mode: the `caffeinate -is` wrapper must not swallow `train.py`'s exit status — a non-zero inner exit must propagate through the wrapper. | R2 | resolved | verification: test (wrapper exit == inner exit). Prevents an overnight run silently appearing to succeed. |

## Ambiguity Report

| Dimension          | Score | Min  | Status | Notes                                                        |
|--------------------|-------|------|--------|--------------------------------------------------------------|
| Goal Clarity       | 0.86  | 0.75 | ✓      | 7 requirements enumerated; code-vs-doc scope locked          |
| Boundary Clarity   | 0.85  | 0.70 | ✓      | Phase 42/43 line locked (summary one-pager vs gate/compare)  |
| Constraint Clarity | 0.80  | 0.65 | ✓      | M5 Pro, `caffeinate -is`, JSONL-canonical, async TB, cadence |
| Acceptance Criteria| 0.82  | 0.70 | ✓      | Per-req pass/fail + 4 edge backstops + 3 negative tests      |
| **Ambiguity**      | 0.16  | ≤0.20| ✓      | Gate passed after Round 2 + edge/prohibition probes          |

Status: ✓ = met minimum, ⚠ = below minimum (planner treats as assumption). No dimension below minimum.

## Interview Log

| Round | Perspective     | Question summary                                   | Decision locked                                                                 |
|-------|-----------------|----------------------------------------------------|---------------------------------------------------------------------------------|
| 1     | Researcher/Boundary | Build scope: implement vs wire vs doc-only?    | **Implement + runbook** — Phase 42 writes the missing emission code + runbook   |
| 1     | Boundary Keeper | summary.md — Phase 42 vs Phase 43 line?            | **42 = per-run one-pager**; test-preview/ε_H·SCS gate/cross-run compare → 43     |
| 1     | Boundary Keeper | Form of the five OPS-01 entry points?             | **Docs + `caffeinate -is` wrapper** only; no CLI/wrapper-script framework        |
| 2     | Researcher      | Residual panel artifact form?                     | **TensorBoard panel** (async; no blocking matplotlib)                            |
| 2     | Failure Analyst | Definition of "alive" for `status.json`?          | **Timestamped heartbeat** — staleness proof, robust to L-BFGS line-search trap   |
| 5.5   | Failure Analyst | E1 non-finite JSONL / E2 signal race / E3 status startup+atomicity / E4 partial run | All **backstop** — invariant locked, mechanism → plan-phase (avoid forced bad design) |
| 5.6   | (must-NOT)      | False-green / PII leak / masked exit code?         | All **kept, test tier** — 3 negative acceptance criteria                          |

---

*Phase: 42-operator-runbook-surface-monitoring*
*Spec created: 2026-07-18*
*Next step: /gsd-discuss-phase 42 — implementation decisions (how to build what's specified above)*
