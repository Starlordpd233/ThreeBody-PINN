# Phase 42: Operator Runbook Surface & Monitoring - Context

**Gathered:** 2026-07-18
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 42 builds the **operator surface and monitoring layer** on top of the
runnable Phase-40/41 loop: signal handling in `pinn.train` (graceful-checkpoint
Ctrl-C semantics), the committed `caffeinate -is` unattended-run wrapper, the
canonical JSONL step log + human `train.log` mirror carrying the widened B-2
field set, a derived TensorBoard secondary view including the per-time-bin
residual panel + `w_n` causal-weight scalars, the `status.json` timestamped
heartbeat + periodic `mem:` line, completion of the `runs/<name>/` directory
contract with an always-present `summary.md`/`summary.json` one-pager, an
example config under `configs/`, and a written operator runbook under
`docs/runbooks/`. The training machinery itself (network, loop, config,
checkpoint, resume, guards, determinism) is consumed, not rebuilt. The `verify`
ladder, `evaluate` gate, smoke test, pilot, and all threshold **calibration**
are Phase 43.

</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

**7 requirements are locked (OPS-01..06, with OPS-04 split a/b).** See
`42-SPEC.md` for full requirements, boundaries, acceptance criteria, edge
coverage (E1–E4 backstops), and prohibitions (3 must-NOT negative tests).

Downstream agents MUST read `42-SPEC.md` before planning or implementing.
Requirements are not duplicated here.

**In scope (from SPEC.md):**
- Signal handling in `pinn.train` (SIGINT once → checkpoint; SIGINT twice → immediate exit; SIGTERM → graceful checkpoint).
- A committed `caffeinate -is` unattended-run wrapper (the only new executable).
- Canonical JSONL step logger (`train.log.jsonl`) + human `train.log` mirror carrying the widened field set.
- TensorBoard writer (`runs/<name>/tb/`) as a derived secondary view, including the per-time-bin residual panel + `w_n`-vs-step scalars.
- `status.json` timestamped heartbeat (with `state` incl. `initializing`) + periodic `mem:` line.
- Completion of the `runs/<name>/` directory contract (`logs/`, `tb/`, `summary.md`, `summary.json`, `status.json`; `checkpoints/`, `config.yaml`, `failure/` already exist).
- Per-run end-of-run `summary.md`/`summary.json` one-pager (header, final 5 losses + total, curriculum progression, wall-clock, device), always present incl. a failed-run template.
- An example config template under `configs/`.
- A written operator runbook under `docs/runbooks/`.

**Out of scope (from SPEC.md):**
- Held-out test-set preview, ε_H/SCS acceptance-gate rendering, cross-run comparison, go/adjust/rethink verdict — Phase 43 (ACC-02..06).
- The `verify` pre-flight ladder + ~5-minute smoke test — Phase 43 (ACC-01).
- Hyperparameter selection/tuning; distributed training / cloud fallback.
- Training-loop / network / physics internals (Phases 38/40) and config/checkpoint/resume/guards/determinism machinery (Phases 40/41) — consumed, not rebuilt.
- Experiment trackers beyond TensorBoard (W&B/MLflow, PH-10).
- Final ratification of the B-2 log field set and calibration of R-1/R-2/D4-a thresholds — owner-carved seams at their designed moments.
- Editing framework specs — read-only in v2.0.

</spec_lock>

<decisions>
## Implementation Decisions

Labels continue the CTX namespace (Phase 41 ended at CTX-64). Grounding for
every decision below: `42-SPEC.md`, the ratified trainex-r1a verdicts (B-2, B-6,
B-9, B-10, B-11, D2, D4), the training-execution design §5/§6.1/§6.4, and the
CTX-45/CTX-52..64 seams Phases 40/41 deliberately left for this phase.

### Step Log — emission path & sinks (OPS-03, fills the CTX-45 seam)
- **CTX-65:** The widened field set is produced at the **existing single
  emission point** — `RunController._log_step` in `pinn/training/controllers.py`
  — by widening its `extra` payload (add: `stage`, λ weight vector, `grad_norm`,
  `w_n` stats, per-bin residuals, `s_per_step`, `eta_seconds`, epoch). Sinks
  (JSONL handler, human formatter, TensorBoard consumer) are **attached at the
  composition root** (`pinn/train.py main()`), never inside controllers. This is
  the CTX-45 designed architecture ("Phase 42 attaches a JSONL handler/formatter
  to the same logger tree; the widened field set is a formatter concern") — no
  new hook closure, no second emission path. **Emission ordering:** the step
  record is emitted after loss computation **regardless of guard outcome** — a
  step that trips a guard still logs (the diverged step is the most valuable
  record; E1 + OPS-04b both require it). `grad_norm` is threaded into
  `_log_step` from the existing computation (already produced for the guard
  hook); the λ vector comes from `ScheduledWeights` current values; lr from the
  active optimizer.
- **CTX-66:** Sink formats. `runs/<name>/logs/train.log.jsonl` — one JSON object
  per logged step via `json.dumps(..., allow_nan=False)` on a sanitized record;
  append-mode text stream, flushed per logged step, **no per-line fsync**
  (non-degradation; `status.json` is the atomic surface, the JSONL is
  append-only). `runs/<name>/logs/train.log` — a human line per logged step
  mirroring the design §5.4 shape
  (`step N | stage k phase 2a | total=… data=… ic=… phys=… energy=… angmom=… | lr=… | 1.2 s/step | ETA 01:23:45`)
  plus non-step events (run start, provisional-threshold set, stage
  dispositions, `mem:` lines, guard trips) via the same logger tree. Cadence =
  existing `run.log_every` (this IS the SPEC's `log_freq` concept; **do not
  rename the field** — Phase-41 schema churn for zero semantic gain; the example
  config sets it to 100 per design §5.4).
- **CTX-67:** **E1 non-finite policy (mechanism resolved):** a NaN/Inf value in
  any field serializes as JSON **`null`**, and the record gains `"finite": false`
  plus `"nonfinite_keys": [...]` naming the affected fields. Strict
  `allow_nan=False` guarantees every emitted line parses under any JSON parser.
  String sentinels are prohibited in the canonical log (SPEC E1 rejects them;
  they break typed parsers). Note: `guards._json_safe_scalar`'s string-sentinel
  behavior is a **trip.json-local** convention — planner must NOT reuse it for
  the JSONL formatter.
- **CTX-68:** **B-2 field set is a ⚖ seam, not a Phase-42 pick.** The canonical
  key names ship as a `STEP_LOG_FIELDS` registry constant (module owning the
  step-record assembly), tagged provisional and surfaced through the existing
  `provisional_fields()`-style owner-attention listing at run start. The
  registry carries the SPEC-enumerated groups — step, stage, phase, epoch, the
  five loss terms (`data/ic/phys/energy/angmom`), `total`, λ weight vector,
  `grad_norm`, `w_n` stats, `lr`, `s_per_step`, `eta_seconds` — and the **owner
  ratifies the final list before run #1** (same pattern as the B-5 resume-field
  registry). Additive keys are non-breaking by design (JSONL readers ignore
  unknown keys).

### TensorBoard & the Per-Time-Bin Residual Panel (OPS-03/04b)
- **CTX-69:** TB mechanism = `torch.utils.tensorboard.SummaryWriter` (tensorboard
  2.21.0 verified present in `pinn-train`), constructed at the composition root
  with `log_dir=runs/<name>/tb/`, fed from the **same widened step record** as
  the JSONL sink. `add_scalar` is an enqueue; the SummaryWriter's **own
  background event-writer thread** is the "written asynchronously" mechanism —
  no matplotlib, no synchronous plotting in the step loop (SPEC constraint).
  JSONL remains the canonical source of truth (D2); TB is derived and
  **always-on** (the SPEC's successful-run contract requires `tb/` — no toggle).
  Any TB sink failure logs one warning and never aborts training (monitoring
  must not kill the run it monitors).
- **CTX-70:** Panel content, grounded in the causal-weighting math
  (`w_n = exp(-η_c · Σ_{m<n} stopgrad(R̄_m))`, η_c = 1, w_1 = 1 — §3.2, D-04
  Option A): collapse means persistent early-bin residuals drive later `w_n`
  toward 0 (training sees only early τ); propagation failure means the causal
  front stops advancing. The panel therefore emits, per logged step:
  (a) per-bin residual scalars `residuals/bin_{n:02d}` for each of the
  N_t collocation time-bins (N_t = 16 at Stage 0, from the collocation sampler);
  (b) causal-weight scalars `causal/w_min`, `causal/w_mean`, `causal/w_max`, and
  `causal/front_idx` = max{n : w_n > 0.5} (the propagation front);
  (c) optionally a `w_n` histogram at a sparser cadence (discretion).
  **Exposure mechanism:** `loss_catalog.causal_physics_loss` gains an
  **additive** details path (e.g. `return_details=` keyword or sibling helper)
  returning **detached** per-bin `R̄_n` and `w_n` tensors — the default return
  type is unchanged so Phase 38/40 tests are untouched, and detaching prevents
  autograd-graph retention across steps. Emission is **unconditional** —
  under collapse (w_n → 0 are valid floats) and under NaN (TB event files store
  NaN; the panel emitting under failure is its purpose, per the SPEC).

### Signals & Unattended Wrapper (OPS-01/02, E2)
- **CTX-71:** Signal design — handlers installed **only** in `pinn.train
  main()` (composition root; the library stays signal-free and importable).
  First SIGINT sets a stop-request flag checked at step boundaries (Adam: per
  step; L-BFGS: between closure evaluations, aborting the in-progress optimizer
  step and checkpointing the last coherent state) → graceful path: write
  checkpoint, flip `status.json` to `interrupted`, finalize `summary.md`, exit
  code 130. SIGTERM ≡ first SIGINT (graceful; exit 143). **Second SIGINT
  escalates to immediate exit** — best-effort atomic `status.json` flip to
  `interrupted`, then `os._exit(130)`, no further checkpoint. **E2 debounce
  (mechanism resolved as direction):** SIGINTs arriving within a short window
  (~1 s; exact value plan-phase discretion) of the first count as the same
  press — a panic-mash during a multi-second graceful checkpoint coalesces into
  one graceful request, while a deliberate later second Ctrl-C still escalates.
  E2's atomicity invariant is already carried by the checkpoint store's
  tmp+fsync+rename path — an abandoned `.tmp` from an escalated exit never
  becomes visible.
- **CTX-72:** The graceful checkpoint reuses the **existing store path**
  (`build_checkpoint_payload` + rolling save at the current step, updating
  `latest.pt`) — no new checkpoint flavor; resume-after-interrupt is the
  ordinary `--resume latest` flow.
- **CTX-73:** Wrapper = a committed shell script (suggested
  `scripts/train-unattended.sh`; exact name discretion):
  `exec caffeinate -is python -m pinn.train "$@"` — `caffeinate` exits with the
  utility's status and `exec` removes the shell layer, so the inner exit status
  propagates verbatim (the must-NOT test: wrapper exit == inner exit). The
  script contains **no machine-specific absolute paths**; the runbook documents
  activating `pinn-train` first (Setup entry point). Lid-open + AC rule and the
  "recovery is checkpoint-resume, not wake-and-hope" doctrine (B-10) are runbook
  content, not code.

### status.json Heartbeat & mem: Line (OPS-04a, E3)
- **CTX-74:** Heartbeat mechanism = a **daemon thread** rewriting
  `runs/<name>/status.json` every K seconds (default 30; `run.monitor` knob)
  from a mutex-guarded snapshot the step loop updates, **plus** synchronous
  rewrites at every state transition and every logged step. Every rewrite goes
  through the existing `atomic_io.atomic_write_text` (temp + fsync + rename) —
  a reader never sees truncated JSON (E3). The thread-based timestamp makes
  freshness ≡ **process liveness**, exactly the SPEC's L-BFGS-trap robustness
  reading: a multi-minute line search with a frozen step count still heartbeats;
  a dead/hung process goes stale. **Startup window (E3):** `state:
  "initializing"` is written immediately after run-dir creation, **before**
  model/data build, with `step: null` and **no fabricated losses** (loss fields
  null until the first real step). Terminal transitions: `finished` (normal),
  `failed` (guard HALT / unhandled exception), `interrupted` (signal path).
- **CTX-75:** `status.json` schema (self-describing staleness): `schema_version`,
  `run_name`, `pid`, `state` ∈ {initializing, running, finished, failed,
  interrupted}, `timestamp_utc` (ISO-8601) + `timestamp_epoch` (float, trivial
  age math), `heartbeat_interval_secs`, `staleness_threshold_secs` (default
  3×K — the file carries its own threshold so a reader needs no external
  constant: `now − timestamp_epoch > staleness_threshold_secs ⇒ stalled`),
  `step`, `stage`, `phase`, `epoch`, latest losses (5 terms + total, CTX-67
  null policy), `lr`, `s_per_step_ema`, `eta_seconds`, memory fields (below).
  `pid` doubles as the operator's kill target for unattended stops (runbook).
- **CTX-76:** `mem:` line — reuse the **existing guard memory signal**
  (`torch.mps.driver_allocated_memory` + total, the Phase-41 wiring; Phase-39
  adapter `mem:` format precedent) emitted to `train.log` through the logger
  tree at a periodic cadence (from the heartbeat thread each tick, or every
  logged step — discretion), and mirrored into `status.json` memory fields. No
  new dependency (no psutil).

### runs/ Contract & Summary One-Pager (OPS-05, E4)
- **CTX-77:** **Summary lifecycle — honest stub at launch, atomic terminal
  rewrite.** `summary.md` + `summary.json` are written at run start as an honest
  "run in progress / did not complete" template and **atomically replaced** at
  the terminal transition with the final one-pager (finished / failed /
  interrupted variants). Presence is thereby guaranteed under **every** death
  mode including SIGKILL — a write-at-exit-only design cannot satisfy E4's
  presence invariant. Content: run header (name, start/end UTC, wall-clock,
  device+precision, seed, config-identity digest), final five loss terms +
  total (CTX-67 null policy; never fabricated), curriculum progression
  (rendered from the existing `runs/<name>/curriculum.jsonl`), terminal
  disposition. **B-6/D-12 reconciliation:** the ratified environment-fingerprint
  fields (`sw_vers`, `python -V`, torch version/build) live in the
  `summary.json` run header — the run folder carries the fingerprint without
  inventing a file outside the SPEC's member list. `summary.md` for a
  failed/interrupted run is the **honest failed-run template** — state named,
  no placeholder metrics (must-NOT #1). Generation lives in `pinn.train`
  (composition root), not in controllers.
- **CTX-78:** Directory contract completion — `logs/`, `tb/`, and an **empty
  `failure/`** are created at launch (the SPEC's successful-run AC lists
  `failure/` among the required members; an empty directory on success is the
  honest signal that no guard fired). A contract test asserts the full member
  list on a synthetic run.
- **CTX-79:** **Redaction policy (must-NOT #2):** all handoff artifacts
  (`train.log`, `train.log.jsonl`, `status.json`, `summary.*`, `failure/`)
  record paths **relative to the run directory** only — no `/Users/…` absolute
  paths, no hostnames, no secrets (Phase-39 `/Users/` leak precedent). A
  redaction-style negative test greps the artifacts of a synthetic run.

### Config, Runbook & Entry-Point Surface (OPS-01/06)
- **CTX-80:** New monitoring knobs live in a nested `run.monitor` sub-config
  (pattern: `run.guards`/`run.checkpoint`): `heartbeat_secs` (default 30),
  `staleness_factor` (default 3), plus discretionary cadence knobs (e.g. TB
  histogram thinning). All are **operational** under the locked B-5
  classification (log frequency / validation cadence are already operational
  there) — changing them on resume is allowed. `run.log_every` stays the log
  cadence. Additive schema only; the fail-closed unknown-key loader behavior is
  untouched.
- **CTX-81:** Operator surface — runbook at
  `docs/runbooks/training/<YYYY-MM-DD>-stage0-training-operator-runbook.md`
  (new `training/` category; date-prefixed name; follow `docs/README.md`
  conventions — planner reads it in full before creating the file). Four
  mandated sections: mental model; the five entry points; the categorized error
  surface (symptom → meaning → action, covering guard trips, NaN/divergence,
  memory watermark, disk floor, stalled heartbeat, MPS unavailable, config
  refused, resume refused); M5-Pro notes (24 GB unified memory, thermal,
  sleep/`caffeinate` lid-open+AC rule, single-MPS-device). Entry-point mapping
  (doc-only, no new CLI): **Setup** = the Phase-37 one-command env setup;
  **Configure** = copy `configs/stage0-example.yaml` → edit; **Launch** =
  `python -m pinn.train --config …` (or the wrapper for unattended);
  **Monitor** = `tail -f runs/<name>/logs/train.log` + `tensorboard --logdir
  runs/<name>/tb` + `status.json`; **Resume** = `--resume latest`. Example
  config `configs/stage0-example.yaml` (new top-level `configs/`) must load
  through `load_config` without error (validated by test) and shows the
  documented defaults (`log_every: 100`, monitor knobs) with advanced knobs
  commented.

### Claude's Discretion
- Module/file layout for the new code (e.g. `pinn/training/monitor.py` /
  `step_log.py` / `signals.py` under `pinn/training/`) — must extend existing
  seams, never fork them.
- Exact debounce window (~1 s), EMA constant for `s_per_step`, TB histogram
  cadence, heartbeat default within 15–60 s, `mem:` cadence, wrapper filename.
- ETA definition detail: **current-stage** remaining estimate (v2.0 is
  single-stage Stage-0); `eta_seconds` is null before the s/step EMA warms up.
- Human `train.log` line micro-format (must carry the design-§5.4 fields).
- TB tag taxonomy beyond the CTX-70 mandated tags.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Locked Phase 42 scope
- `.planning/phases/42-operator-runbook-surface-monitoring/42-SPEC.md` — Locked requirements (OPS-01..06), boundaries, acceptance criteria, E1–E4 edge backstops, 3 must-NOT prohibitions. **MUST read before planning.**
- `.planning/REQUIREMENTS.md` — OPS-01..06 requirement text with decision codes (design §5/§6.1, B-2, B-6, B-10, D2).

### Ratified build-engineering grounding
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/trainex-r1a-resolution-doc.md` — B-2 (widened field set + panel "early"), B-6 (run-folder member list + D-12 env fingerprint), B-9 (frozen keyed config), B-10 (`caffeinate -is`, lid-open+AC, SIGTERM ≡ one Ctrl-C), B-11 (reproducibility wording), D2 (JSONL canonical; TB secondary in `runs/<name>/tb/`), D4-c/d (guards + failure bundle).
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/RATIFICATION.md` — owner ratification record (2026-07-05).

### The operator-surface design (primary OPS grounding)
- `docs/work/designs/cross_cutting/training-execution/2026-06-10-training-execution-design.md` — §5.1–5.10 (mental model, five entry points, log-line shape + `log_freq` default 100, stop rules, monitor surfaces, `runs/<name>/` structure, error surface, M5-Pro notes), §6.1 (health question + operator action table), §6.4 (honesty layer), §6.5 (outcome-level failure modes).

### The seams this phase fills (Phase-40/41 hand-off)
- `.planning/phases/40-stage-0-curriculum-training-loop-fut-04/40-CONTEXT.md` — **CTX-45** (logger tree; "Phase 42 attaches the JSONL handler"), CTX-38/39 (provisional thresholds + run-start provisional log), CTX-52 (minimal step log fields). MUST read.
- `.planning/phases/41-config-checkpointing-resume-determinism/41-CONTEXT.md` — CTX-50..64 (config loader fail-closed behavior, frozen copy, checkpoint store atomicity CTX-55, `curriculum.jsonl` CTX-56, B-5 identity/operational line CTX-57, failure bundle CTX-61, reproducibility honesty CTX-64).
- `pinn/train.py` — the composition root: run-dir resolve + traversal guard, freeze, RNG record, hook closures, `curriculum.run()`; signals/status/summary/sinks wire in HERE.
- `pinn/training/controllers.py` — `RunController._log_step` (the single emission point to widen), guard-hook threading of `grad_norm`, `_LOGGER = logging.getLogger("pinn.training.controllers")`.
- `pinn/training/config.py` + `pinn/training/config_yaml.py` — `RunConfig` (`log_every`, nested `guards`/`checkpoint` pattern for `monitor`), `provisional_fields()` (the ⚖ owner-attention listing CTX-68 joins), fail-closed loader + `freeze_resolved_config`.
- `pinn/training/atomic_io.py` — `atomic_write_text` (the status.json/summary atomic path).
- `pinn/training/guards.py` — memory signal (`torch.mps.driver_allocated_memory`), `write_failure_bundle`, `_json_safe_scalar` (trip.json-local; NOT for JSONL — CTX-67).
- `pinn/loss_catalog.py` — `causal_physics_loss` (§3.2 `w_n` math; CTX-70's additive details path lands here).
- `pinn/training/checkpoint.py` — the store whose rolling save the graceful path reuses (CTX-72).

### The science (read-only; constrains the panel semantics)
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` §3.2 — causal weighting `w_n = exp(-η_c Σ_{m<n} R̄_m)`, η_c = 1 (D-04 Option A); the collapse/propagation phenomenology the panel must surface.

### Repo governance for the runbook deliverable
- `docs/README.md` — authoritative docs/ placement + naming rules; **read in full before creating the runbook file** (per repo CLAUDE.md).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `RunController._log_step` (controllers.py:570) — already emits `extra={event,
  step, phase, total, lr, loss_*}` at `run.log_every` cadence from both Adam
  and L-BFGS paths; Phase 42 widens this payload and attaches handlers.
- `atomic_io.atomic_write_text` — temp+fsync+rename; status.json/summary reuse
  it unchanged.
- `StepGuards` memory signal + `write_failure_bundle` — the `mem:` source and
  the failure/ population; `guard_hook` in train.py shows the closure pattern.
- `TorchSaveCheckpointStore` + `build_checkpoint_payload` — the graceful-stop
  checkpoint path (no new flavor).
- `provisional_fields()` on `TrainingConfig` — the run-start ⚖ owner-attention
  log the B-2 `STEP_LOG_FIELDS` registry joins.
- `curriculum.jsonl` (CTX-56) — the summary's curriculum-progression source.
- tensorboard 2.21.0 verified importable in the `pinn-train` conda env (ENV-01
  installed it; no new dependency).

### Established Patterns
- Frozen typed dataclass validated at construction; nested sub-configs
  (`run.guards`, `run.checkpoint`) — `run.monitor` follows.
- Stdlib-`logging` tree `pinn.training.*` with machine payloads via `extra`
  (CTX-45); unittest `assertLogs`-testable.
- `tests/phase42` stdlib-unittest with deferred-import skip guards; conda env
  via `<home>/miniforge3/bin/conda run -n pinn-train`; synthetic
  Stage-0 sources (`_synthetic_split_sources`, population floor 240) — signal /
  heartbeat / contract tests run dataset-free against tiny synthetic runs.
- Composition-root-only side effects: train.py owns process-level concerns
  (signals, threads, sinks); `pinn/training/` modules stay pure/importable.

### Integration Points
- `pinn/train.py main()` — install signal handlers; create `logs/`, `tb/`,
  empty `failure/`; write `initializing` status + summary stub; attach
  JSONL/human/TB sinks; start heartbeat thread; finalize status/summary in the
  terminal path (normal / exception / signal).
- `controllers._log_step` — widened payload (λ vector, grad_norm, w_n stats,
  per-bin residuals, s/step, ETA, stage, epoch).
- `loss_catalog.causal_physics_loss` — additive detached details path (CTX-70).
- `config.py` — `MonitorConfig` under `run.monitor`; `STEP_LOG_FIELDS` ⚖ seam
  surfaced in the run-start provisional log.
- New top-level `configs/` (example YAML) and `docs/runbooks/training/`
  (runbook); wrapper under `scripts/`.

</code_context>

<specifics>
## Specific Ideas

- **The panel is the physics deliverable:** causal-weight collapse
  (`w_n → 0` beyond a stalled front) and propagation failure are the two
  highest-value silent failures (B-2 rationale). Per-bin residual scalars +
  `causal/front_idx` make "is the causal front advancing in τ?" readable at a
  glance; the panel emitting **under** collapse/NaN is its purpose, so emission
  is ordered before any guard early-return.
- **Freshness ≡ process liveness, by design:** the daemon-thread heartbeat is
  deliberately robust to the L-BFGS line-search trap (frozen step count, live
  process ⇒ fresh timestamp ⇒ "alive"); progress questions are answered by
  `step`/losses, not the timestamp. `status.json` carries its own staleness
  threshold so any reader can classify alive-vs-stalled with no external
  constant.
- **Honesty layer everywhere (design §6.4):** stub-then-finalize summaries,
  null-not-fabricated metrics, `interrupted`/`failed` states that never read
  `finished`, and the wrapper's verbatim exit-status propagation are all the
  same principle: the surface never reports success it did not observe.
- **Two seams stay owner-owned:** the B-2 field-list ratification (before
  run #1) and all R-1/R-2/D4-a threshold values (Phase-43 pilot) — Phase 42
  builds surfaces against provisional registries and never presents them as
  ratified.

</specifics>

<deferred>
## Deferred Ideas

None new — discussion stayed within phase scope. (Test-set preview, ε_H/SCS
gate rendering, run comparison, verify ladder, and threshold calibration are
already Phase 43 by the roadmap.)

### Reviewed Todos (not folded)
- `d-06-static-epsilon-sensitivity-check.md` — matcher score 0.6 on generic
  keywords only ("safe, set, over, one, open"); it is a data/physics
  sensitivity probe about the admitted set's dual-context epsilon, with no
  operator-surface or monitoring content. Not folded.
- `trainex-r1-research-handoff.md` — score 0.2 (below threshold); research
  process task, no Phase-42 surface. Not folded.

</deferred>

---

*Phase: 42-operator-runbook-surface-monitoring*
*Context gathered: 2026-07-18*
