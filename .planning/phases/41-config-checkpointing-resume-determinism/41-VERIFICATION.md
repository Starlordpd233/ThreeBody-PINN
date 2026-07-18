---
phase: 41-config-checkpointing-resume-determinism
verified: 2026-07-18T08:54:46Z
status: gaps_found
score: 5/6 must-haves verified
behavior_unverified: 0
overrides_applied: 0
gaps:
  - truth: "Full seed/RNG state is recorded in config + every checkpoint (CTRL-08 / ROADMAP SC #4 / SPEC AC)"
    status: failed
    reason: >
      Every checkpoint carries the four RNG streams (torch, torch_mps, numpy,
      python_random) and exact-continuation restore is tested end-to-end, but
      the frozen runs/<name>/config.yaml does NOT carry those four streams.
      freeze_resolved_config writes a pure TrainingConfig only; the
      frozen_config_rng_recording_format seam is registered as UNDECIDED with
      candidates (A) sidecar _runtime_state envelope or (B) sibling
      run_start_rng.pt — neither is implemented. SPEC AC requires a test that
      frozen config AND checkpoint both contain all four streams; that config
      half is intentionally unimplemented pending owner pick, and no later
      phase claims the work. Seed is present in config (statistical-equivalence
      path works); full RNG carriage in config is the missing half of SC #4.
    artifacts:
      - path: "pinn/training/config_yaml.py"
        issue: "freeze_resolved_config dumps pure TrainingConfig only; no RNG streams"
      - path: "pinn/training/config.py"
        issue: "provisional_fields registers frozen_config_rng_recording_format=UNDECIDED"
      - path: "pinn/train.py"
        issue: "composition root freezes config but never writes run_start_rng.pt or _runtime_state"
      - path: "tests/phase41/test_train_entrypoint.py"
        issue: "RngRecordedEverywhereTests asserts UNDECIDED and does not require config-side RNG"
    missing:
      - "Owner pick of frozen_config_rng_recording_format: (A) _runtime_state envelope in config.yaml ignored by load_config, or (B) sibling runs/<name>/run_start_rng.pt"
      - "Implement the chosen representation so freeze/startup records all four streams without breaking TrainingConfig re-parse equality"
      - "Test asserting frozen config artifact (yaml envelope or sibling .pt) contains torch/torch_mps/numpy/python_random"
deferred: []
human_verification:
  - test: "Owner pick frozen_config_rng_recording_format (A vs B) before claiming CTRL-08 complete"
    expected: "One representation is chosen and implemented; four streams land in the frozen-config path without breaking load_config equality"
    why_human: "Representation is ⚖ owner-carved; agent must not invent it (governance STOP)"
  - test: "Owner-ratify B-5 IDENTITY/OPERATIONAL field lists in RESUME_FIELD_REGISTRY before run #1"
    expected: "Lists marked owner-ratified (not only provisional/⚖); real-data deferred IDENTITY categories resolved or still explicitly deferred"
    why_human: "CTRL-05 requires owner ratification of the field list; code ships a surfaced ⚖ proposal only"
  - test: "Owner-calibrate R-1 guard thresholds at Phase-43 pilot"
    expected: "loss_explosion_ceiling / disk_floor_fraction / memory_watermark_fraction and wall_clock_ceiling_s ratified from pilot variance"
    why_human: "Values are ⚖ provisional placeholders by design; mechanism is wired, values are owner-carved"
---

# Phase 41: Config, Checkpointing, Resume & Determinism — Verification Report

**Phase Goal:** Every run is driven by one frozen keyed config, survives interruption and corruption, resumes and rolls back correctly, and records enough seed/RNG state to reproduce to statistical equivalence — with guards that stop-and-preserve on trouble.

**Verified:** 2026-07-18T08:54:46Z  
**Status:** `gaps_found`  
**Re-verification:** No — initial verification  
**Branch / HEAD:** `milestone/v2.0` @ `fe38b2d6` (post-merge fix removed banned `.is_available()` probes)

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Single keyed YAML (`run/stage/opt/loss`) drives the run; fully-resolved copy frozen into `runs/<name>/config.yaml` (CTRL-01 / B-9) | ✓ VERIFIED | `config_yaml.load_config` + recursive `ConfigKeyError`; `freeze_resolved_config` → `atomic_io.atomic_write_text`; re-parse equality tested (`FrozenCopyRoundTripTests`, `LaunchContractTests.test_fresh_launch_writes_artifacts`) |
| 2 | Dual-trigger + atomic checkpointing with rolling/best/latest/anchor retention (CTRL-02/03) | ✓ VERIFIED | `CheckpointStore.should_checkpoint` (step OR wall-clock); `atomic_write_torch`; rolling-N eviction; `save_best` / `latest.pt` / stage anchors; `weights_only=True` on all loads; `fallback_scan` on corrupt latest. Tests: DualTrigger/Atomicity/Retention/FallbackScan + e2e dual-trigger |
| 3 | Dual stage anchors + idempotent ordered promotion + `curriculum.jsonl` (CTRL-04) + complete Adam reset at boundary (CTRL-06) | ✓ VERIFIED | `CurriculumController` ADVANCE writes `stage-{k}-final` + `stage-{k+1}-init` via `build_checkpoint_payload`/`save_anchor`; `promote(k,k+1)` ordered; `record_disposition` fsync-appends ledger idempotently; init anchors carry `optimizer=None`. Tests: `LedgerAndPromotionTests`, `AdamResetCompositionTests`, `OptimizerRestoreOrderingTests` |
| 4 | `--resume` continues exactly; `--hold-stage` rolls back; field-classified resume-diff refuses identity/unclassified (CTRL-05) | ✓ VERIFIED | `pinn.train` CLI; `load_resume_target` exact-anchor routing; `validate_hold_stage_target`; `resume_config_diff` + `RESUME_FIELD_REGISTRY` (strict_cpu IDENTITY); mid-stage weight match + hold-stage e2e tests pass. Field list is ⚖ provisional (owner-ratify before run #1 — human item) |
| 5 | Tier-1+2 guards + RECOVER/HALT + always-on `failure/` bundle (CTRL-07) | ✓ VERIFIED | `StepGuards.check`: NaN/Inf→RECOVER, loss-explosion→RECOVER, disk-floor→HALT, memory-watermark→HALT; wired via `guard_hook` in Adam (pre-step) and L-BFGS (post-step); `write_failure_bundle` Tier-A README+trip.json; thresholds from `run.guards` ⚖. Tests: unit guards + controller HALT family + failure-bundle backstop |
| 6 | Full seed/RNG state recorded in **config + every checkpoint**; statistical-equivalence + exact continuation (not bitwise); strict-CPU switch (CTRL-08) | ✗ FAILED | **Checkpoint half ✓:** four streams in every CTX-53 payload; `capture_rng_state`/`restore_rng_state` exact (not reseed); honesty string; `apply_strict_cpu_determinism` returns float64/cpu RuntimeSpec used by `build_network`. **Config half ✗:** frozen `config.yaml` has seed only; four streams not recorded (UNDECIDED seam). SPEC AC unmet for config side |

**Score:** 5/6 truths verified (0 present-but-behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `pinn/training/atomic_io.py` | Shared tmp→fsync→replace→dir-fsync | ✓ VERIFIED | 92 lines; `atomic_write_text` + `atomic_write_torch` |
| `pinn/training/config.py` | precision/device/strict_cpu + ⚖ guards/cadence + provisional_fields | ✓ VERIFIED | `GuardConfig`, `CheckpointCadence`, `RunConfig` extensions; provisional registry + UNDECIDED RNG format |
| `pinn/training/config_yaml.py` | load_config + freeze_resolved_config + ConfigKeyError | ✓ VERIFIED | Recursive dotted-path unknown keys; pure TrainingConfig freeze |
| `pinn/training/checkpoint.py` | Production store dual-trigger/retention/atomic/ledger | ✓ VERIFIED | 607 lines; CTX-53 schema; promote + record_disposition |
| `pinn/training/guards.py` | StepGuards + write_failure_bundle | ✓ VERIFIED | Per-family disposition; no `.is_available()` probes |
| `pinn/training/determinism.py` | Four-stream capture/restore + strict-CPU + honesty | ✓ VERIFIED | No `.is_available()`; REPRODUCIBILITY_SCOPE honesty |
| `pinn/training/controllers.py` | Hooks, build_checkpoint_payload, resume_ctx, Adam reset | ✓ VERIFIED | checkpoint_hook/guard_hook; pending optimizer; global step |
| `pinn/training/resume.py` | Identity digest + config-diff + hold-stage validation | ✓ VERIFIED | RESUME_FIELD_REGISTRY; load_resume_target |
| `pinn/train.py` | Composition root CLI | ✓ VERIFIED | `--config`/`--resume`/`--hold-stage`; freezes config; wires hooks |
| `tests/phase41/*` | Wave-0 + plan tests | ✓ VERIFIED | 192 tests collected/passed |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `config_yaml.load_config` | `TrainingConfig` dataclasses | yaml.safe_load + `_map_section` | ✓ WIRED | Field-for-field; tuple coerce for adam_betas |
| `freeze_resolved_config` | `atomic_io.atomic_write_text` | `runs/<name>/config.yaml` | ✓ WIRED | Pure config only (no RNG) |
| `CheckpointStore` save paths | `atomic_io.atomic_write_torch` | rolling/best/anchor/latest | ✓ WIRED | All production writes |
| `build_checkpoint_payload` | store save_* | Single composer + CHECKPOINT_SCHEMA_VERSION | ✓ WIRED | Controllers + train hooks |
| `checkpoint_hook` closure | `store.should_checkpoint` + `save_rolling`/`save_best` | pinn.train | ✓ WIRED | Live curriculum_state_accessor |
| `guard_hook` | `StepGuards.check` → `write_failure_bundle` + failure anchor | pinn.train | ✓ WIRED | Disposition propagated to phase return |
| `CurriculumController` ADVANCE | promote + record_disposition + dual anchors | controllers.py | ✓ WIRED | Ledger + CTRL-06 optimizer clear |
| `load_state_dict` | `determinism.restore_rng_state` + pending optimizer | controllers.py | ✓ WIRED | Exact continuation; build-then-load fix |
| `pinn.train` strict_cpu | `apply_strict_cpu_determinism` → `build_network` | BEFORE resolve_runtime override | ✓ WIRED | HIGH 4 ordering |
| Frozen config | four RNG streams | freeze path / sibling artifact | ✗ NOT_WIRED | UNDECIDED; intentional non-implementation |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|-------------------|--------|
| Rolling checkpoint | `payload["rng"]` | `controller.state_dict()` → `capture_rng_state(self._rng)` | Live torch/numpy/python/(mps) state | ✓ FLOWING |
| Rolling checkpoint | `payload["curriculum"]` | `curriculum_state_accessor()` at fire time | Live stage/phase/epoch/step | ✓ FLOWING |
| best.pt | `payload` | `_last_val_total` strict improvement | Real validation total from `_run_validation` | ✓ FLOWING |
| failure/trip.json | trip scalars | `GuardOutcome` from live loss/grad/disk/mem | Live metrics + ⚖ thresholds | ✓ FLOWING |
| frozen config.yaml | TrainingConfig fields | resolved defaults + YAML overrides | Real resolved config | ✓ FLOWING |
| frozen config.yaml | four RNG streams | *(none)* | Not produced | ✗ DISCONNECTED |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Full phase41 suite | `pytest tests/phase41 -q` | **192 passed** in ~30s | ✓ PASS |
| phase41 + phase40 regression | `pytest tests/phase41 tests/phase40 -q` | **355 passed**, 106 subtests | ✓ PASS |
| Fresh launch artifacts | `LaunchContractTests.test_fresh_launch_writes_artifacts` | config.yaml + checkpoints + honesty stdout | ✓ PASS |
| Mid-stage exact resume | `ExactContinuationTests.test_mid_stage_resume_matches_uninterrupted_weights` | pass | ✓ PASS |
| RNG exact vs reseed | `test_resume_rng_exact_vs_fresh_statistical` | pass | ✓ PASS |
| Four streams in every ckpt | `RngRecordedEverywhereTests` | pass (also asserts config RNG UNDECIDED) | ✓ PASS (ckpt) / documents config gap |
| Hold-stage exact anchor | `HoldStageTests` | pass | ✓ PASS |
| Dual-trigger e2e rolling | `DualTriggerEndToEndTests` | pass | ✓ PASS |
| Ledger + dual anchors | `LedgerAndPromotionTests` | pass | ✓ PASS |
| Adam reset at init anchor | `AdamResetCompositionTests` | pass | ✓ PASS |
| HALT not flattened to RECOVER | `GuardHaltFamilyTests` | pass | ✓ PASS |

### Probe Execution

| Probe | Command | Result | Status |
|-------|---------|--------|--------|
| *(none declared)* | — | Phase is library + CLI, not probe-migration | SKIP |

### Requirements Coverage

| Requirement | Source Plan(s) | Description | Status | Evidence |
|-------------|----------------|-------------|--------|----------|
| CTRL-01 | 41-01, 41-05 | Keyed YAML + frozen resolved copy | ✓ SATISFIED | config_yaml + freeze + e2e freeze reparse |
| CTRL-02 | 41-02, 41-04 | Dual-trigger + rolling/best/latest/anchors | ✓ SATISFIED | CheckpointStore + hooks + e2e |
| CTRL-03 | 41-02 | Atomic + weights_only + fallback scan | ✓ SATISFIED | atomic_io; all loads weights_only; fallback_scan tests |
| CTRL-04 | 41-02, 41-04 | Dual anchors + idempotent promote + curriculum.jsonl | ✓ SATISFIED | ADVANCE path + ledger tests |
| CTRL-05 | 41-05 | --resume / --hold-stage / fail-safe config-diff | ✓ SATISFIED | resume.py + train CLI + e2e; field list ⚖ pending owner |
| CTRL-06 | 41-04 | Complete Adam reset at stage boundary | ✓ SATISFIED | optimizer=None on init anchors; restore ordering tests |
| CTRL-07 | 41-03, 41-04 | Tier-1+2 guards + RECOVER/HALT + failure/ | ✓ SATISFIED | guards.py + guard_hook + bundle tests |
| CTRL-08 | 41-03, 41-04, 41-05 | Seed/RNG in config + checkpoint; repro scope; strict-CPU | ✗ BLOCKED (partial) | Checkpoints + restore + strict-CPU + honesty ✓; **four-stream RNG in frozen config ✗** |

**Orphaned requirements:** none — all CTRL-01..08 appear in plan frontmatter.

**Note:** `.planning/REQUIREMENTS.md` marks CTRL-01..08 as Complete. Code evidence supports Complete for CTRL-01..07; CTRL-08 is **not** fully complete until config-side RNG carriage is implemented after owner pick.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| — | — | No `FIXME`/`XXX`/`TBD` debt markers in phase-modified production files | — | clean |
| — | — | No `yaml.load(` (only `safe_load`/`safe_dump`) | — | clean |
| — | — | No `.is_available()` call sites (comments only; fe38b2d6 compliance) | — | clean |
| `config_yaml.py` / `config.py` | freeze path | RNG-in-config intentionally absent (UNDECIDED) | 🛑 Blocker for SC #4 | See gap |

### Human Verification Required

### 1. Owner pick: frozen_config_rng_recording_format

**Test:** Choose (A) `_runtime_state` sidecar key in `config.yaml` ignored by `load_config`, or (B) sibling `runs/<name>/run_start_rng.pt` (+ every checkpoint already carries streams).  
**Expected:** Chosen representation implemented; four streams recorded at run start; TrainingConfig re-parse equality preserved; SPEC AC test green.  
**Why human:** ⚖ owner-carved representation; agent must not invent (governance).

### 2. Owner-ratify B-5 resume field lists

**Test:** Review `RESUME_FIELD_REGISTRY` IDENTITY/OPERATIONAL classification before production run #1.  
**Expected:** Ratified list (or explicit deferrals) replaces provisional-only status.  
**Why human:** CTRL-05 / B-5 owner ratification; code surfaces proposal only.

### 3. Owner-calibrate R-1 / D4-a provisional thresholds (Phase 43)

**Test:** After Stage-0 pilot, ratify guard ceilings and wall-clock checkpoint ceiling.  
**Expected:** Values no longer only ⚖ placeholders.  
**Why human:** Mechanism complete; values owner-carved by design (not a Phase-41 code gap).

### Gaps Summary

Phase 41 delivers a working control layer: keyed YAML config, atomic dual-trigger checkpoints with retention and anchors, curriculum ledger, resume/hold-stage with fail-safe identity diff, Tier-1+2 guards with failure bundles, four-stream RNG in checkpoints with exact continuation, strict-CPU switch, and honesty-scoped reporting. **192/192 phase41 tests and 355 combined phase40+41 tests pass.**

One roadmap success criterion remains unmet: **CTRL-08 requires full seed/RNG state in the frozen config as well as every checkpoint.** The checkpoint path is complete; the config path is deliberately left as `frozen_config_rng_recording_format=UNDECIDED` (candidates A/B enumerated, neither implemented). That is correct governance (do not invent the representation) but it is still a **failed must-have** relative to ROADMAP SC #4 and SPEC acceptance — not deferred to Phase 42/43, and not covered by an override.

**Recommended next action:** Owner picks A or B; implement config-side four-stream recording + test; re-verify. Optionally ratify B-5 field lists in the same pass. Guard-threshold ratification stays Phase 43.

---

_Verified: 2026-07-18T08:54:46Z_  
_Verifier: Claude (gsd-verifier)_
