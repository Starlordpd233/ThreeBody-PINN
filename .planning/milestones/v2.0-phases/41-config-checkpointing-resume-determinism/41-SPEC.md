# Phase 41: Config, Checkpointing, Resume & Determinism — Specification

**Created:** 2026-07-17
**Ambiguity score:** 0.18 (gate: ≤ 0.20)
**Requirements:** 8 locked (CTRL-01..08)

## Goal

Wrap the Phase-40 training loop with a control layer so that every run is driven by one frozen keyed YAML config, survives interruption and checkpoint corruption, resumes exactly and rolls back on demand, records enough seed/RNG state to reproduce to statistical equivalence, and stops-and-preserves on trouble — implementing the ratified trainex-r1a build decisions (B-9, D4-a..d, D6, D7-a..d, B-5, B-11, R-1) **without inventing the owner-carved values**.

## Background

The v2.0 viability slice builds the CTL-PINN training stack from the authoritative framework specs and the ratified trainex-r1a decision set (2026-07-05). Phase 40 landed the training driver and, by design, left the control seams this phase fills:

- **`pinn/training/config.py`** — a nested frozen `TrainingConfig` dataclass exists, but its module docstring states *"No precision/device fields and no YAML parsing — Phase 41 maps YAML sections."* `run.seed` exists (int, validated). There is **no** YAML parser, no keyed `run/stage/opt/loss` surface, no resolved-copy freeze, and no precision/device field.
- **`pinn/training/checkpoint.py`** — a `CheckpointStore` seam plus a *"deliberately minimal"* naive `TorchSaveCheckpointStore` exists; its docstring states *"Phase 41"* replaces it. There is **no** dual-trigger cadence, no rolling/best/latest/anchor retention, no atomic (tmp+fsync+rename) write, no `weights_only`-clean discipline, no fallback scan, and no `curriculum.jsonl`.
- **`pinn/training/controllers.py`** (`RunController` / `CurriculumController`), **`pinn/training/grad_clip.py`** (`GradClipper`), and **`pinn/training/scheduled_weights.py`** already expose `state_dict` / `load_state_dict` for checkpoint composition; `CurriculumController` already emits `StageDisposition` (ADVANCE / RECOVER / HALT).
- **`pinn/training/stage_exit.py`** implements the ADVANCE/RECOVER/HALT decision *form* with provisional thresholds; **`pinn/network.py`** and **`pinn/training/collocation_sampler.py`** already enforce caller-owned **local** RNG discipline (global RNG never touched; `spec + seed` → bitwise-identical parameters).

What does **not** exist today: any keyed-YAML config system with a frozen resolved copy, a production checkpoint store (dual-trigger cadence, retention classes, atomicity, fallback scan, `curriculum.jsonl`), a `pinn.train` entry point, `--resume` / `--hold-stage` semantics, a resume config-diff, an auto-guard/`failure/`-bundle layer, or full seed/RNG recording+restore. Phase 41 builds exactly that control layer on top of the Phase-40 loop.

The slice is Stage-0-first, single M5 Pro, in-memory, manual rollback, **fp32-MPS** (D1-p ruling), reproducibility scoped to statistical-equivalence + exact checkpoint continuation (not bitwise). Spec inputs are read-only in v2.0; a build-discovered spec defect is surfaced as a gap, not edited here.

## Requirements

1. **Keyed YAML config + frozen resolved copy (CTRL-01)** `[B-9]`
   - Current: `pinn/training/config.py` is a frozen dataclass with no YAML parsing and no keyed `run/stage/opt/loss` surface; nothing freezes a resolved copy into a run folder.
   - Target: A single YAML config keyed `run / stage / opt / loss` (plus precision/device) resolves into the `TrainingConfig` and drives every run; the **fully-resolved** config (defaults merged, all seams filled) is written verbatim to `runs/<name>/config.yaml` at run start.
   - Acceptance: A test loads a keyed YAML, asserts the resolved `TrainingConfig` fields match; asserts a missing/empty config or an unknown/misspelled key raises a typed error naming the offending path (fail-closed, never silently defaulted); asserts the frozen `config.yaml` re-parses to a `TrainingConfig` equal to the one that ran.

2. **Dual-trigger checkpoint cadence + retention (CTRL-02)** `[D4-a]`
   - Current: The naive store writes on no schedule and keeps everything; no rolling/best/latest/anchor classes exist. The wall-clock ceiling value is an **owner pick** (r1b 15–30 min range, informed by the smoke test) — not yet chosen.
   - Target: Checkpoints write on a **dual trigger** — every `N` steps OR a wall-clock ceiling, whichever fires first — with retention classes `rolling-3` + `best.pt` + `latest.pt` + stage anchors. The ceiling ships as a **clearly-marked ⚖ provisional placeholder** read from config and **owner-ratified before run #1**; the mechanism, not the value, is delivered.
   - Acceptance: A test drives a stub clock+step counter and asserts a checkpoint is written when the step-trigger fires, when the wall-clock ceiling fires first, and **exactly once** when both coincide on the same step; asserts rolling retention keeps the newest 3 rolling checkpoints (deletes the oldest by step) while `best.pt`, `latest.pt`, and stage anchors are never deleted; asserts with < 3 rolling checkpoints present nothing is deleted and no error is raised.

3. **Atomic, `weights_only`-clean checkpoint writes + fallback scan (CTRL-03)** `[D4-b]`
   - Current: The naive store uses a plain `torch.save`; no atomicity, no corruption handling.
   - Target: Every checkpoint write is atomic (write to `*.tmp` → `fsync` → `rename`), payloads are `weights_only`-loadable (no arbitrary pickled objects), and a fallback scan recovers the newest valid checkpoint when `latest.pt` is missing or corrupt.
   - Acceptance: A test simulates a crash between tmp-write and rename and asserts no partial/half-written checkpoint is ever visible under the canonical name; asserts a written checkpoint loads under `torch.load(..., weights_only=True)`; asserts that with a corrupt `latest.pt`, the fallback scan returns the newest structurally-valid checkpoint (or a typed "no valid checkpoint" error naming the directory when none exist).

4. **Stage anchors + idempotent ordered promotion + `curriculum.jsonl` (CTRL-04)** `[D7-a, D7-d]`
   - Current: No stage-boundary anchors, no promotion ledger, no idempotency.
   - Target: At each stage boundary, dual anchors `stage-{k}-final.pt` + `stage-{k+1}-init.pt` are written and **excluded from rolling deletion**; promotion is **idempotent** and **ordered** (k → k+1, never skips, never regresses); a `curriculum.jsonl` appends one record for **every** promotion / RECOVER / HALT disposition, in chronological order.
   - Acceptance: A test drives a stub curriculum and asserts both anchors are written at a boundary and survive a rolling-eviction pass; asserts replaying the same promotion (e.g. after a resume) does **not** duplicate the anchor or append a second `curriculum.jsonl` row (idempotent); asserts a skip/regress promotion request is refused; asserts each ADVANCE/RECOVER/HALT appends exactly one ordered `curriculum.jsonl` line and a fresh run yields a well-formed (possibly empty) ledger.

5. **`--resume` exact continuation, `--hold-stage` rollback, fail-safe config-diff (CTRL-05)** `[D7-c, B-5]`
   - Current: No `pinn.train` entry point, no `--resume`/`--hold-stage`, no resume config-diff.
   - Target: `python -m pinn.train --config <c> --resume <ckpt>` continues exactly from the checkpoint; `--resume <…/stage-{k}-final.pt> --hold-stage` performs a manual rollback that re-enters stage `k` instead of advancing; a **field-classified** resume config-diff **refuses** (fail-safe) on any change to an *identity* field or any **unclassified** field, and permits only explicitly-*operational* fields to differ. The identity/operational field list is a **surfaced proposal, owner-ratified before run #1 — not invented**.
   - Acceptance: A test runs a tiny end-to-end Stage-0 loop, checkpoints at step `s`, resumes, and asserts the resumed trajectory matches an uninterrupted run to the same step (exact continuation) to floating tolerance; asserts `--hold-stage` from a `stage-{k}-final.pt` re-enters stage `k` (no advance); asserts resume refuses when an identity-classified field changed AND when an unclassified field changed (fail-safe), and proceeds when only a whitelisted operational field changed; asserts a missing `--resume` path raises a typed error naming the path.

6. **Complete Adam reset at every stage boundary (CTRL-06)** `[D7-b]`
   - Current: Optimizer-state reset at boundaries lives in the Phase-40 controllers but is not composed with checkpoint save/restore across a boundary.
   - Target: The Adam optimizer state is **completely reset** at every stage boundary, and L-BFGS history **never** crosses a boundary — preserved through checkpoint save/restore (resuming from `stage-{k+1}-init.pt` starts with reset Adam state).
   - Acceptance: A test asserts the Adam state after a boundary is a fresh-initialized state (all moment buffers cleared), distinct from the pre-boundary state; asserts a checkpoint taken at `stage-{k+1}-init.pt` restores with reset Adam state; asserts L-BFGS history is empty immediately after a boundary.

7. **Auto-guards Tier 1+2, RECOVER/HALT, `failure/` bundle (CTRL-07)** `[D4-c, D4-d, R-1]`
   - Current: The stage-exit machine has RECOVER/HALT *form*; there is no always-on guard layer for NaN/Inf, loss-explosion, disk-floor, or memory-watermark, and no `failure/` bundle.
   - Target: Tier-1+2 auto-guards (NaN/Inf, loss-explosion, disk-floor, memory-watermark) run every step, wired to the RECOVER seam and HALT/REVIEW family; guard thresholds are **clearly-marked ⚖ placeholders calibrated against the Phase-43 Stage-0 pilot (owner-ratified, not invented)**; on **any** guard trip an always-on `failure/` diagnostic bundle (state snapshot + last log lines + a one-line README naming the trip) is written.
   - Acceptance: A test injects a NaN gradient and asserts the guard trips → RECOVER path → a `failure/` bundle with a non-empty one-line README is written; asserts a loss-explosion, a disk-floor, and a memory-watermark trip each fire their guard and write a bundle; asserts a first-step (step 0) trip is handled (no ordering assumption); asserts guard thresholds are read from config and are tagged provisional/⚖ (no hard-coded ratified value); asserts simultaneous trips still produce exactly one coherent `failure/` bundle.

8. **Full seed/RNG recording + statistical-equivalence reproducibility + strict-CPU switch (CTRL-08)** `[D6, B-11]`
   - Current: RNG discipline exists per-component (local generators) but there is no run-level recording of the full seed/RNG state into config + checkpoints and no strict-CPU determinism switch.
   - Target: The full seed/RNG state (torch + MPS + numpy + python `random`) is recorded in the frozen config and in **every** checkpoint and restored on resume; reproducibility is scoped to **statistical equivalence** (fresh run, same seed) **+ exact checkpoint continuation** (resume), explicitly **not** bitwise re-creation; a strict-CPU determinism **debug switch** exists for tighter reproducibility during debugging.
   - Acceptance: A test asserts the frozen config and a checkpoint both contain all four RNG stream states; asserts resuming from a checkpoint reproduces the exact next-step RNG draws (exact continuation); asserts two fresh runs at the same seed are statistically equivalent (matching a documented tolerance seam, calibrated at the Phase-43 pilot — not a hard-coded pass number here); asserts the strict-CPU switch forces CPU + deterministic algorithms and is off by default.

## Boundaries

**In scope:**
- Keyed YAML config system (`run/stage/opt/loss` + precision/device) resolving into `TrainingConfig`, with a frozen resolved `config.yaml`
- A **minimal but runnable** `python -m pinn.train` driver wiring config → the Phase-40 loop → checkpoint/resume, with `--config`, `--resume`, `--hold-stage` flags (the falsifiability floor for CTRL-01/02/05/08)
- A **minimal functional step log** (step, five loss terms, total, lr) — only enough to observe resume-continuity and guard trips
- Production `CheckpointStore`: dual-trigger cadence, `rolling-3`/`best`/`latest`/stage-anchor retention, atomic (tmp+fsync+rename) `weights_only`-clean writes, fallback scan, `curriculum.jsonl`
- Idempotent ordered stage promotion with dual anchors; complete Adam reset composition across boundaries
- Resume/rollback semantics + field-classified fail-safe resume config-diff (with a **surfaced** identity/operational field-list proposal)
- Tier-1+2 auto-guards + RECOVER/HALT wiring + always-on `failure/` bundle
- Full seed/RNG recording+restore; statistical-equivalence + exact-continuation reproducibility; strict-CPU determinism switch
- Owner-carved **seams with clearly-marked provisional (⚖) defaults**: D4-a wall-clock ceiling, R-1 guard/RECOVER thresholds, B-5 resume-field classification

**Out of scope:**
- Operator ergonomics of the five entry points (Setup/Configure/Launch/Monitor/Resume as polished single commands) — Phase 42 (OPS-01/02); Phase 41 delivers the underlying `pinn.train` mechanism only
- The **canonical widened JSONL schema** (5 loss terms + total + λ vector + grad-norm + `w_n` stats + lr + s/step + ETA) and the **TensorBoard** secondary view — Phase 42 (OPS-03); Phase 41 logs only the minimal functional fields, deliberately not the full observability schema (avoids a later widen/refactor and keeps OPS-03 cleanly owned by Phase 42)
- `status.json` heartbeat, `mem:` monitoring line, per-time-bin residual panel — Phase 42 (OPS-04)
- The full `runs/<name>/` contract polish (`summary.md`/`summary.json`, handover semantics) — Phase 42 (OPS-05); Phase 41 writes `config.yaml`, `checkpoints/`, `curriculum.jsonl`, and `failure/` only
- `verify` pre-flight ladder, `evaluate` gate rendering, the Stage-0 pilot, and threshold **calibration/ratification** of the ⚖ seams — Phase 43 (ACC-01..06)
- **Choosing** any owner-carved value (ceiling, guard thresholds, resume-field list) — surfaced as seams; the owner ratifies at the designed moment (smoke test / Stage-0 pilot / before run #1)
- Editing framework specs or `pinn_architecture.md`/`ctl_instruction.md` — read-only in v2.0
- Stochastic-L-BFGS stages 3–6 — refused upstream (Phase 40, TRAIN-07), not exercised here

## Constraints

- **Platform / precision:** single M5 Pro, fp32-MPS default (D1-p LOCKED), with fp64-CPU as the in-framework escape hatch; MPS lacks full deterministic-algorithm coverage, so bitwise reproducibility is explicitly not promised — the strict-CPU switch is the tight-reproducibility path.
- **Framework:** PyTorch `torch.save`/`torch.load`; checkpoint payloads MUST be `weights_only`-loadable (no arbitrary pickled objects).
- **Reproducibility scope:** statistical equivalence (fresh run, same seed) + exact checkpoint continuation (resume) — NOT bitwise re-creation.
- **Governance:** owner-carved values are seams with provisional (⚖) defaults, ratified by the owner at their designed moments; the agent surfaces evidence, it does not pick these values.
- **Composition:** must reuse the existing `state_dict`/`load_state_dict` contracts on `RunController`/`CurriculumController`/`GradClipper`/scheduled-weights rather than re-implementing state capture.
- **Test pattern:** dataset-free `tests/phase41` unittests with deferred-import skip guards (Phase 37–40 pattern); the minimal end-to-end resume/guard checks use a tiny synthetic Stage-0 loop, no real dataset.

## Acceptance Criteria

- [ ] A keyed `run/stage/opt/loss` YAML resolves into `TrainingConfig`; unknown/missing keys fail loud with the offending path; the frozen `runs/<name>/config.yaml` re-parses equal to what ran.
- [ ] Checkpoints fire on the dual trigger (N steps OR wall-clock ceiling, whichever first) and write exactly once when both coincide; the ceiling is a config-read ⚖ placeholder marked owner-ratify-before-run-#1.
- [ ] Retention keeps `rolling-3` + `best.pt` + `latest.pt` + stage anchors; oldest rolling is evicted by step; best/latest/anchors are never evicted; < 3 rolling present → no deletion, no error.
- [ ] Checkpoint writes are atomic (no partial file ever visible under the canonical name) and load under `weights_only=True`; a corrupt `latest.pt` triggers a fallback scan to the newest valid checkpoint (or a typed error naming the dir).
- [ ] Dual stage anchors are written and survive rolling eviction; promotion is idempotent (replay does not duplicate anchor/ledger row) and ordered (no skip/regress).
- [ ] `curriculum.jsonl` appends exactly one ordered record per promotion/RECOVER/HALT; a fresh run yields a well-formed (possibly empty) ledger.
- [ ] `--resume` continues exactly (resumed trajectory == uninterrupted trajectory to floating tolerance); `--hold-stage` from a `stage-{k}-final.pt` re-enters stage `k`; a missing `--resume` path errors with the path.
- [ ] The resume config-diff refuses (fail-safe) on any identity-field or unclassified-field change and permits only whitelisted operational fields; the field-list is a surfaced proposal marked owner-ratify.
- [ ] Adam state is completely reset at every boundary (moment buffers cleared, pre≠post); restore from `stage-{k+1}-init.pt` has reset Adam state; L-BFGS history never crosses a boundary.
- [ ] Each Tier-1+2 guard (NaN/Inf, loss-explosion, disk-floor, memory-watermark) trips its path and writes an always-on `failure/` bundle with a non-empty one-line README; a step-0 trip and simultaneous trips are handled; thresholds are config-read ⚖ placeholders.
- [ ] Full seed/RNG state (torch+MPS+numpy+python) is recorded in config and every checkpoint and restored on resume (exact continuation); the strict-CPU determinism switch forces deterministic CPU and is off by default; the run truthfully reports statistical-equivalence + exact-continuation scope (never claims bitwise).
- [ ] All checks run dataset-free under `tests/phase41` with deferred-import skip guards; the end-to-end resume/guard checks use a tiny synthetic Stage-0 loop.

## Edge Coverage

**Coverage:** 17/22 applicable edges resolved (covered) · 5 dismissed (with reason) · 0 unresolved

| Category | Requirement | Status | Resolution / Reason |
|----------|-------------|--------|---------------------|
| adjacency | R1 | ✅ covered | Unknown/duplicate key or default==override → fail-loud on unknown key (AC: config parse) |
| empty | R1 | ✅ covered | Missing/empty config file → typed error naming the path (AC: config parse) |
| ordering | R1 | ⛔ dismissed | Config is a keyed mapping with no order-dependent output; the resolved freeze serializes deterministically — no equal-element ordering contract applies |
| adjacency | R2 | ✅ covered | Step-trigger and wall-clock ceiling coincide on the same step → exactly one checkpoint (AC: dual trigger) |
| empty | R2 | ✅ covered | < 3 rolling checkpoints present → no deletion, no error (AC: retention) |
| ordering | R2 | ✅ covered | Rolling eviction removes the oldest by step index; best/latest/anchors never evicted (AC: retention) |
| unclassified | R3 | ✅ covered | Crash between tmp-write and rename → no partial file visible; corrupt `latest.pt` → fallback scan to newest valid (AC: atomic + fallback) |
| boundary | R4 | ✅ covered | Promotion beyond the slice's terminal stage is refused (ties to the sL-BFGS preflight); no skip/regress (AC: ordered promotion) |
| adjacency | R4 | ✅ covered | Replayed promotion after resume is idempotent — no duplicate anchor or ledger row (AC: idempotent promotion) |
| empty | R4 | ✅ covered | Fresh run → well-formed (possibly empty) `curriculum.jsonl` (AC: ledger) |
| ordering | R4 | ✅ covered | Ledger rows appended in chronological disposition order; promotion strictly ordered (AC: ledger) |
| precision | R4 | ⛔ dismissed | Stage promotion is over integer stage indices; no floating-point rounding/tie-break contract applies |
| unclassified | R5 | ✅ covered | Resume with identity-field change → refuse; unclassified-field change → refuse (fail-safe); `--hold-stage` from a non-final checkpoint and missing path → typed error (AC: resume/rollback/diff) |
| boundary | R6 | ✅ covered | Reset happens exactly at the k→k+1 boundary; restore from `stage-{k+1}-init.pt` has reset Adam state (AC: Adam reset) |
| adjacency | R6 | ✅ covered | Resuming exactly at a boundary applies the reset correctly (AC: Adam reset + restore) |
| empty | R6 | ⛔ dismissed | Optimizer reset has no empty-input dimension; a stage always has a defined optimizer state |
| ordering | R6 | ⛔ dismissed | Optimizer reset is a state-clear with no ordered output |
| precision | R6 | ⛔ dismissed | Adam reset is a state-clear, not a precision-sensitive numeric computation |
| unclassified | R7 | ✅ covered | Step-0 trip; simultaneous multi-guard trips → one coherent bundle; disk-floor trip during a write → best-effort bundle (backstop) (AC: guards) |
| adjacency | R8 | ✅ covered | Exact checkpoint continuation vs statistical equivalence distinguished: resume reproduces exact next-step draws; fresh same-seed run only statistically equivalent (AC: reproducibility) |
| empty | R8 | ✅ covered | v2.0 is greenfield; every checkpoint carries full RNG state — no legacy checkpoint-without-RNG path (AC: RNG record) |
| ordering | R8 | ✅ covered | All four RNG streams (torch/MPS/numpy/python) recorded and restored in a defined order (AC: RNG record/restore) |

## Prohibitions (must-NOT)

**Coverage:** 3/3 applicable prohibitions resolved · 0 unresolved · 1 canon breadcrumb

| Prohibition (must-NOT statement) | Requirement | Status | Verification / Reason |
|----------------------------------|-------------|--------|------------------------|
| MUST NOT present any owner-carved seam value (D4-a wall-clock ceiling, R-1 guard/RECOVER thresholds, B-5 resume-field list) as owner-ratified; provisional values MUST be visibly tagged ⚖ and surfaced for ratification | R2, R7, R5 | resolved | judgment — governance-critical (agent surfaces evidence, does not pick values); reviewer confirms every seam default is marked provisional |
| MUST NOT resume when an identity-classified OR unclassified config field changed (fail-safe refuse; never fail-open) | R5 | resolved | test — negative acceptance: identity-field change and unclassified-field change each force a refusal |
| MUST NOT overclaim reproducibility — the run's own reporting MUST state statistical-equivalence + exact-continuation scope, never bitwise reproducibility | R8 | resolved | judgment — honesty layer; the reproducibility claim in output/reporting is scoped truthfully |
| (canon breadcrumb) pickle-RCE via `torch.load(weights_only=False)` on untrusted checkpoints | R3 | — | canon security — owned by `/gsd-secure-phase` + the `weights_only`-clean positive acceptance (CTRL-03); not minted as a bespoke prohibition here |

## Ambiguity Report

| Dimension          | Score | Min  | Status | Notes                                                        |
|--------------------|-------|------|--------|--------------------------------------------------------------|
| Goal Clarity       | 0.88  | 0.75 | ✓      | 8 requirements, each grounded in a decision code + a Phase-40 code seam |
| Boundary Clarity   | 0.82  | 0.70 | ✓      | 41↔42/43 split grounded in the design doc §3.3/§5; owner-value seams explicit |
| Constraint Clarity | 0.78  | 0.65 | ✓      | fp32-MPS, torch.save/weights_only, atomic, statistical-equivalence-not-bitwise |
| Acceptance Criteria| 0.75  | 0.70 | ✓      | mechanism-level checks concrete; numeric thresholds correctly deferred to owner |
| **Ambiguity**      | 0.18  | ≤0.20| ✓      | Gate passed; driver-scope boundary resolved to Option A (runnable driver + library) |

Status: ✓ = met minimum, ⚠ = below minimum (planner treats as assumption)

## Interview Log

| Round | Perspective    | Question summary                                             | Decision locked                                                                 |
|-------|----------------|-------------------------------------------------------------|---------------------------------------------------------------------------------|
| 0     | Researcher     | What exists today vs. what Phase 41 must build?             | Phase 40 left explicit seams in `config.py`/`checkpoint.py`; Phase 41 fills them |
| 0     | Boundary Keeper| Where is the 41↔42 line for the `pinn.train` driver?       | **Option A** — runnable driver + library (falsifiability of CTRL-01/02/05/08 requires end-to-end); OPS-03 canonical logging stays Phase 42 |
| 0     | Boundary Keeper| Owner-carved values — invent or surface?                   | Surface as ⚖ seams with provisional defaults (D4-a ceiling, R-1 thresholds, B-5 field list); ratified at designed moments |
| 5.5   | Failure Analyst| Edge completeness (22 candidates)                          | 17 covered → acceptance criteria; 5 dismissed with reason; 0 unresolved         |
| 5.6   | Failure Analyst| Prohibitions (must-NOT)                                     | 3 kept (seam-honesty, resume fail-safe, repro honesty); pickle-RCE → secure-phase canon |

---

*Phase: 41-config-checkpointing-resume-determinism*
*Spec created: 2026-07-17*
*Next step: /gsd-discuss-phase 41 — implementation decisions (how to build what's specified above)*
