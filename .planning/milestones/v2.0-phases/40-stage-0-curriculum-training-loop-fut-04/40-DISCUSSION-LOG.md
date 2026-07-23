# Phase 40: Stage-0 Curriculum Training Loop (FUT-04) - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-07-16
**Phase:** 40-stage-0-curriculum-training-loop-fut-04
**Areas discussed:** Module layout, Clip constants, Provisional-threshold mechanics, Phase-41 seam, Phase-42 logging seam, Optimizer & loop details (auto-resolved)
**Mode:** `--all` (all gray areas auto-selected; interactive discussion). Mid-session
(after the Phase-41/42 seam answers), the owner directed autonomous best-judgment
resolution for all remaining questions; the final area is agent-resolved with logged
rationale. `--assumptions` and `--auto` flags from the original invocation were
dropped by owner decision (recorded in-session): `--assumptions` routes to a
no-file-output workflow, and `--auto` would auto-advance into plan-phase, which this
session was explicitly forbidden to enter (watchdog-chain position B).

---

## Module layout

| Option | Description | Selected |
|--------|-------------|----------|
| `pinn/training/` subpackage | Mirrors pinn/data/ and pinn/verification/ precedent for a cohesive multi-module concern; ~6 modules; Phase 41/42 seams importable from one namespace | ✓ |
| Flat modules at `pinn/` root | Strict CTX-15 continuity; adds 6 files to a root still holding v1.3-era legacy files | |
| Single `pinn/trainer.py` | One module; works against the SPEC's per-requirement isolated tests | |

**User's choice:** `pinn/training/` subpackage (recommended option)
**Notes:** CTX-15's "flat" precedent covered 5 single-purpose science modules; the driver layer is the pinn/data/ shape.

---

## Todo triage (cross_reference_todos)

| Option | Description | Selected |
|--------|-------------|----------|
| Neither — record as reviewed, not folded | Both matched at the 0.4 threshold on generic keywords; neither is training-loop work | ✓ |
| Fold D-06 static-epsilon check | If the dual-context/epsilon question bears on the loop's residual path | |
| Fold trainex-r1 research handoff | If an unlanded r1 decision blocks Phase 40 | |

**User's choice:** Neither (recommended) — "I'm not sure if we should select anything else here. follow your own best judgement."
**Notes:** Agent concurred: D-06 is an admitted-set physics/data probe; the handoff is process work.

---

## Clip constants (the §4.4 FUT-deferred set)

### C_stage 8.5 provenance

| Option | Description | Selected |
|--------|-------------|----------|
| Provisional default 8.5, flagged — calibrate at Phase 43 | Implement per TRAIN-05 (REQUIREMENTS is a grounding source); record that the "trainex-r1a-ratified" citation does not hold; config-overridable; ACC-05 calibrates | ✓ |
| Owner-carved seam — config-required, no default | Strictest SCOPE-19 reading; every run needs an explicit pick first | |
| Owner ratifies 8.5 now | Converts the unsourced midpoint into a real owner decision | |

**User's choice:** Provisional default 8.5, flagged (recommended)
**Notes:** Scout finding: `8.5` appears nowhere in trainex-r1/, framework specs, or .planning outside TRAIN-05; r1a B-1 and §4.4 both leave the value open (range 7–10).

### Bootstrap median (window not yet populated)

| Option | Description | Selected |
|--------|-------------|----------|
| Median of the partial window | Same formula over shorter history; always defined/finite; no unclipped window; no invented constant | ✓ |
| No clipping until window fills (100 steps) | Literal reading; leaves the riskiest early-training window unclipped | |
| Warm-up floor — clip disabled + WARN per step | Same exposure, loudly visible | |

**User's choice:** Median of the partial window (recommended)

### Median lower floor

| Option | Description | Selected |
|--------|-------------|----------|
| Config seam, default 1e-6, flagged provisional | The only number §4.4 puts on the page; prevents clip→0 freeze; ACC-05 calibrates | ✓ |
| No floor — literal formula | Accepts the clip→0 silent-freeze risk | |
| Config-required, no default | Third mandatory pick per run | |

**User's choice:** Config seam, default 1e-6, flagged provisional (recommended)

### Gradient-history reset at stage boundaries

| Option | Description | Selected |
|--------|-------------|----------|
| Clear at every stage boundary | Parallels D7-b Adam reset; C_stage changes at boundaries so a stale median mis-clips | ✓ |
| Carry history across boundaries | Mixes gradient scales across a curriculum change | |
| Clear, but seed with last pre-boundary median | Invents a seeding rule the spec doesn't describe | |

**User's choice:** Clear at every stage boundary (recommended)

---

## Provisional-threshold mechanics (CURR-03 gate)

### Marking provisional values

| Option | Description | Selected |
|--------|-------------|----------|
| Provisional-tagged config defaults + run-start log | Spec values as dataclass defaults with provenance tags; loop logs the provisional set at run start | ✓ |
| `Provisional[float]` wrapper type | Strongest type-level signal; bespoke type threading cost | |
| Plain constants + documented table | No per-run record of uncalibrated values | |

**User's choice:** Provisional-tagged config defaults + run-start log (recommended)

### MAX_EPOCHS / stagnation window / percentile-10 relaxation

| Option | Description | Selected |
|--------|-------------|----------|
| Config-required — loop refuses to start without them | Mirrors D4-a; honors "claimed-unverified, not transcribed as locked"; bounds every run | ✓ |
| Optional — unset disables the max-epoch HALT check | Unbounded-run risk | |
| Required max_epochs, optional stagnation | Fewer mandatory picks | |

**User's choice:** Config-required (recommended)

### ε_phys shape

| Option | Description | Selected |
|--------|-------------|----------|
| Single scalar ε_phys, no per-stage table | Transcribes what the spec locks; refuses the claimed-unverified issue-doc table | ✓ |
| Per-stage table, all defaulting to 1e-4 | Materializes a structure CURR-03 declined to lock | |

**User's choice:** Single scalar (recommended)

### RECOVER semantics at retries: 0

| Option | Description | Selected |
|--------|-------------|----------|
| Roll back, then HALT/REVIEW — no retraining attempt | Zero retries ≠ zero rollback; preserves a numerically valid state; matches SPEC AC literally | ✓ |
| HALT immediately, preserve the NaN state | Better forensics; contradicts the AC's rollback wording | |
| Roll back and retry once, then HALT | Reads the ratified default 0 as 1 | |

**User's choice:** Roll back, then HALT/REVIEW (recommended)

---

## Phase-41 seam (config + checkpoint)

### Config shape

| Option | Description | Selected |
|--------|-------------|----------|
| Nested frozen dataclasses mirroring run/stage/opt/loss | Field-for-field CTRL-01 YAML mapping; per-cluster validation; ArchitectureSpec pattern | ✓ |
| One flat TrainingConfig | Phase 41 invents the grouping; validation piles up | |
| Per-module configs, no composition | Five-object assembly at every construction site | |

**User's choice:** Nested frozen dataclasses (recommended)

### Checkpoint seam

| Option | Description | Selected |
|--------|-------------|----------|
| CheckpointStore protocol + naive in-phase impl | Interface is the seam; Phase 41 swaps in atomic/retention/promotion behind it | ✓ |
| In-memory checkpoints only | RECOVER-across-process-death untestable | |
| Build the real atomic store now | Scope creep across the phase boundary | |

**User's choice:** CheckpointStore protocol + naive impl (recommended)

### State shape

| Option | Description | Selected |
|--------|-------------|----------|
| state_dict()/load_state_dict() on every stateful module | Torch convention; weights_only-satisfiable; RNG capture slots in later | ✓ |
| One TrainingState dataclass snapshot | Pickling fights CTRL-03 weights_only | |
| Each module persists itself | Checkpoint consistency becomes each caller's problem | |

**User's choice:** state_dict()/load_state_dict() (recommended)

### Logging seam

| Option | Description | Selected |
|--------|-------------|----------|
| Stdlib logging w/ structured extra dicts | Zero deps; assertLogs-testable; Phase 42 attaches JSONL formatter to the same tree | ✓ |
| Metrics-emitter protocol injected into controllers | Second injected dependency; front-loads Phase-42 design | |
| Minimal print/logging, no structure | Re-plumbing later; poor pilot grep-ability | |

**User's choice:** Stdlib logging w/ structured extras (recommended)

---

## Optimizer & loop details (agent-resolved under the owner's autonomy directive)

No AskUserQuestion rounds — resolved by the agent with logged rationale after the
owner's mid-session directive ("from now on, you're responsible for the answers
automatically… ground yourself in the mathematics and the science").

| Decision | Resolution | Rationale |
|----------|-----------|-----------|
| Plateau-handoff detector form | Per-epoch finite difference of log10(L_phys), 50-consecutive-epoch counter, reset on violation | Literal transcription of the spec criterion; satisfies the SPEC AC exactly; regression smoothing would be invented |
| L-BFGS max_iter | Provisional config default 20 (spec range 20–50 open) | Conservative wall-time end on single M5 Pro (D5-a's flagged uncertainty); torch's own default; flagged like C_stage |
| Cosine-annealing horizon | T_max = N_Adam,k (stage's Adam epoch budget); joins the config-required set | PHYS-05's warmup formula already treats N_Adam,k as known per-stage; owner picks with ACC-02's s/step data |
| Validation cadence | Provisional default validation_every = 10 epochs | Operational knob (U-6 set-at-implementation precedent applies); ~20 val points per 200-epoch patience window for criterion-2 min-tracking without per-epoch val cost |
| Batch/resample cadence | NOT decided — routed to researcher/planner | Answered by LOOP-01..03 + Phase-39 contracts (DATA-04/05), not a preference |

---

## Claude's Discretion

- Exact module filenames within `pinn/training/` (no v1.3-era collisions).
- Controller injection seams for the TRAIN-01 forced-signal ACs.
- Logger payload key names (mechanism and required events fixed by CTX-45).

## Deferred Ideas

None — discussion stayed within phase scope. Reviewed-but-not-folded todos are
recorded in CONTEXT.md `<deferred>`.
