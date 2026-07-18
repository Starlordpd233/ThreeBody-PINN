# Phase 41: Config, Checkpointing, Resume & Determinism - Context

**Gathered:** 2026-07-17
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 41 builds the **control layer** that wraps the Phase-40 training loop: a
single keyed-YAML config (`run/stage/opt/loss`) with a frozen resolved copy, a
production checkpoint store (dual-trigger cadence, rolling/best/latest/anchor
retention, atomic `weights_only`-clean writes, fallback scan, `curriculum.jsonl`),
`--resume`/`--hold-stage` semantics with a fail-safe field-classified config-diff,
Tier-1+2 auto-guards + RECOVER/HALT + an always-on `failure/` bundle, and full
seed/RNG recording with statistical-equivalence (+ exact-continuation)
reproducibility. It also delivers a **minimal but runnable** `python -m pinn.train`
driver (Option A) — enough to exercise CTRL-01/02/05/08 end-to-end. Operator
ergonomics, the canonical JSONL/TensorBoard surface, monitoring, and the runbook
are Phase 42; the `verify` ladder, pilot, and threshold **calibration** are Phase 43.

</domain>

<spec_lock>
## Requirements (locked via SPEC.md)

**8 requirements are locked (CTRL-01..08).** See `41-SPEC.md` for full
requirements, boundaries, acceptance criteria, edge coverage, and prohibitions.

Downstream agents MUST read `41-SPEC.md` before planning or implementing.
Requirements are not duplicated here.

**In scope (from SPEC.md):**
- Keyed YAML config (`run/stage/opt/loss` + precision/device) → `TrainingConfig`, with a frozen resolved `config.yaml`
- A **minimal but runnable** `python -m pinn.train` driver (`--config`, `--resume`, `--hold-stage`) — the falsifiability floor for CTRL-01/02/05/08
- A minimal functional step log (step, five loss terms, total, lr) — only enough to observe resume-continuity and guard trips
- Production `CheckpointStore`: dual-trigger cadence, `rolling-3`/`best`/`latest`/anchor retention, atomic (tmp+fsync+rename) `weights_only`-clean writes, fallback scan, `curriculum.jsonl`
- Idempotent ordered stage promotion + dual anchors; complete Adam reset across boundaries
- Resume/rollback + field-classified fail-safe resume config-diff (with a **surfaced** identity/operational field-list proposal)
- Tier-1+2 auto-guards + RECOVER/HALT wiring + always-on `failure/` bundle
- Full seed/RNG recording+restore; statistical-equivalence + exact-continuation repro; strict-CPU determinism switch
- Owner-carved **seams with ⚖ provisional defaults**: D4-a ceiling, R-1 guard/RECOVER thresholds, B-5 resume-field classification

**Out of scope (from SPEC.md):**
- Operator ergonomics of the five entry points — Phase 42 (OPS-01/02)
- The canonical widened JSONL schema + TensorBoard secondary view — Phase 42 (OPS-03)
- `status.json` heartbeat, `mem:` line, per-time-bin residual panel — Phase 42 (OPS-04)
- Full `runs/<name>/` contract polish (`summary.md`/`summary.json`, handover) — Phase 42 (OPS-05)
- `verify` ladder, `evaluate` gate, Stage-0 pilot, and ⚖-seam **calibration/ratification** — Phase 43 (ACC-01..06)
- **Choosing** any owner-carved value (ceiling, thresholds, resume-field list) — surfaced seams; ratified at the designed moment
- Editing framework specs (`ctl_instruction.md`/`pinn_architecture.md`) — read-only in v2.0
- Stochastic-L-BFGS stages 3–6 — refused upstream (Phase 40, TRAIN-07)

</spec_lock>

<decisions>
## Implementation Decisions

Labels continue the CTX namespace from Phase 40 (which ended at CTX-49). Phase 41
**fills the CTX-42..45 seams** Phase 40 deliberately left; those four decisions
are load-bearing and are not re-opened.

### Config System (fills CTX-42)
- **CTX-50:** YAML parsing = `yaml.safe_load` (PyYAML). The keyed `run/stage/opt/loss`
  (+ precision/device) sections map onto the CTX-42 nested frozen dataclasses
  **field-for-field**; each sub-config validates its own invariants at construction
  (the `ArchitectureSpec`/`RuntimeSpec` pattern). A missing required section or an
  unknown/misspelled key raises a **typed error naming the offending path**
  (fail-closed — never silently defaulted). The CTX-39 config-required fields
  (`MAX_EPOCHS`, stagnation window, percentile-10 relaxation) and the CTX-38
  provisional thresholds live in these dataclasses. **Planner/researcher confirms
  PyYAML is in the `pinn-train` env; add it if absent** (no bespoke parser).
- **CTX-51:** Frozen resolved copy — after resolution (defaults merged, all seams
  filled) the **fully-resolved** config is written verbatim to
  `runs/<name>/config.yaml` via the same atomic path as checkpoints (CTX-55), at run
  start. Re-parsing it yields a `TrainingConfig` equal to the one that ran (CTRL-01 AC).

### Entry Point — `pinn.train` (Option A, resolved 2026-07-17)
- **CTX-52:** `python -m pinn.train --config <c> [--resume <ckpt>] [--hold-stage]`
  (argparse). Wires: resolve config → `resolve_runtime` (CTX-20, the sole
  precision/device source) → `build_network` → the Phase-40
  `CurriculumController`/`RunController` → `CheckpointStore` → run. Emits the
  **minimal step log** (step, five loss terms, total, lr) through the CTX-45 logger
  tree. This is the falsifiability floor for the inherently-end-to-end requirements
  (CTRL-01/02/05/08); the canonical JSONL schema + operator ergonomics are Phase 42.

### Checkpoint Store (fills CTX-43; CTX-44 composition)
- **CTX-53:** Payload schema = a `weights_only`-clean nested dict keyed by component
  (CTX-44): `model` (network `state_dict`), `optimizer` (active optimizer
  `state_dict` — Adam; any L-BFGS state is within-stage transient and never crosses a
  boundary), `scheduled_weights`, `grad_clip`, `curriculum` (stage index, phase 2a/2b,
  per-stage epoch/step, disposition-log pointer), `rng` (four streams — torch,
  torch.mps, numpy, python `random`), `counters` (global step/epoch, wall-clock
  baseline), `config_identity` (sha256 digest of the canonicalized identity fields +
  the resolved config as a plain dict), `schema_version` (int). All values are plain
  tensors/containers/scalars/strings — no custom pickled classes (CTRL-03).
- **CTX-54:** Retention layout under `runs/<name>/checkpoints/`: rolling
  `step-{step:06d}.pt` (keep **newest 3 by step**; evict the oldest step index),
  `best.pt` (updated on validation improvement), `latest.pt` (an atomic-rename
  **copy**, not a symlink — survives directory handover and `weights_only` load), and
  anchors `stage-{k}-final.pt` + `stage-{k+1}-init.pt` (**excluded from rolling
  deletion**). Dual trigger: every `N` steps OR a wall-clock ceiling, whichever fires
  first; coincident triggers on one step → **exactly one write** (guarded by
  last-written-step). `best`/`latest`/anchors are never rolling-evicted.
- **CTX-55:** Atomicity + fallback — every write goes to `*.tmp` in the same dir →
  `fsync` (file + dir) → `os.replace` (atomic rename); loads use `weights_only=True`.
  On a missing/corrupt `latest.pt`, a **fallback scan** loads the newest
  structurally-valid `step-*.pt`/anchor, or raises a typed "no valid checkpoint"
  error naming the directory.
- **CTX-56:** `curriculum.jsonl` at `runs/<name>/curriculum.jsonl` — append one JSON
  line per promotion/RECOVER/HALT disposition, chronological. **Idempotent** keyed by
  `(from_stage, to_stage, disposition, step)` so a replayed promotion after a resume
  does not duplicate a row or re-write an anchor. Promotion is **ordered** (k→k+1, no
  skip/regress; refuse otherwise).

### Resume, Rollback & Config-Diff — B-5 (user-decided 2026-07-17)
- **CTX-57:** Resume config-diff classification is the **B-5 seam** — a PROPOSAL the
  owner **formally ratifies before run #1**; the fail-safe rule is locked. Owner chose
  the **Conservative** identity line:
  - **Identity (must-match → refuse on change):** architecture spec
    (layers/width/omega0/skip/LayerNorm), IC-vector definition + dataset version/hash,
    loss-catalog structure + physics constants (`D`, `eps_soft`), seed,
    **precision + device**, curriculum/stage definitions, split policy,
    **`MAX_EPOCHS` (per-stage budget)**, **guard/RECOVER thresholds (R-1)**.
  - **Operational (may differ → allow):** checkpoint cadence (`N`-steps trigger) +
    wall-clock ceiling (D4-a); plus pure-runtime knobs that cannot change results
    (log frequency, validation cadence, num workers).
  - **Unclassified → refuse (fail-safe, locked).**
  - The diff compares the incoming config's identity-field digest (CTX-53) against the
    checkpoint's.
  - **Owner-noted implication (recorded, not re-litigated):** because `MAX_EPOCHS`
    and guard thresholds are identity, *extending epochs* or *hot-tuning thresholds*
    on a resume refuses — that needs a **new run**. This is the safe reading of
    CTRL-05 "continues exactly"; the owner may loosen specific fields at run-#1
    ratification.
- **CTX-58:** `--hold-stage` rollback — `--resume <…/stage-{k}-final.pt> --hold-stage`
  re-enters stage `k` (re-runs it) instead of advancing; the same anchor without
  `--hold-stage` proceeds to advance. A missing `--resume` path → typed error naming
  the path.
- **CTX-59:** Exact continuation — resume restores model + optimizer + schedule +
  grad-clip + RNG + counters so the continued trajectory matches an uninterrupted run
  to the same step (floating tolerance). The Adam boundary reset (D7-b, CTX-37 sibling)
  is preserved: restoring from `stage-{k+1}-init.pt` starts with reset Adam state and
  empty L-BFGS history.

### Guards & `failure/` Bundle
- **CTX-60:** Guard layer = a **per-step guard callback** invoked inside the
  RunController step. Tier-1 (NaN/Inf grad/loss → RECOVER), Tier-2 (loss-explosion vs
  a ⚖ ceiling, disk-floor, memory-watermark → RECOVER/HALT per family). Thresholds are
  ⚖ **config seams** (calibrated at the Phase-43 pilot, owner-ratified — CTX-38/39
  pattern). RECOVER/HALT route through the **existing stage-exit machine** (CTX-41:
  `retries:0` → rollback + record + HALT/REVIEW). Step-0 trips are handled (no
  ordering assumption); simultaneous trips produce one coherent bundle.
- **CTX-61:** `failure/` bundle (Claude's decision) — **always-on**, written to
  `runs/<name>/failure/` on ANY guard trip, **tiered for disk-floor safety**:
  - **Tier-A (always, tiny):** `README.txt` (one line: guard, step, stage, reason) +
    `trip.json` (guard name, tier, step, stage, phase 2a/2b, timestamp, tripped metric
    + value + ⚖ threshold, disposition, last loss terms + grad-norm as scalars).
  - **Tier-B (best-effort, if space):** `tail.log` (last ~200 minimal-log lines) + a
    reference (path + digest) to the last-good checkpoint + a reference to the frozen
    `config.yaml`.
  - **No raw tensor/grad dumps by default** — the bundle must stay writable even when
    the **disk-floor** guard is the one that tripped (a large dump is exactly what we
    cannot afford then). Scalar summaries go in `trip.json`.

### Determinism & Reproducibility
- **CTX-62:** Seed/RNG recording — the **four RNG streams** (torch, torch.mps, numpy,
  python `random`) are captured into the frozen config AND every checkpoint (CTX-44
  `rng` key) and restored on resume (exact continuation). Production fp32-MPS at a
  fixed seed → statistical equivalence across fresh runs; resume → exact continuation.
- **CTX-63:** `strict_cpu_determinism` switch (Claude's decision) — a config/CLI
  **DEBUG** switch, **default OFF**. When ON: force `device=cpu` (MPS lacks
  deterministic-algorithm coverage), `torch.use_deterministic_algorithms(True)`,
  `torch.set_num_threads(1)` (pin reduction order), and re-seed all four streams from
  the recorded seed. Even strict-CPU is not guaranteed bitwise across machines/torch
  versions — it tightens **within-machine** reproducibility for debugging. Off by
  default so production keeps the fp32-MPS speed + statistical-equivalence scope.
- **CTX-64:** Reproducibility honesty — the run's own reporting states the scope as
  **statistical-equivalence + exact-checkpoint-continuation, never bitwise** (ties the
  SPEC prohibition and the design-doc §6.4 honesty layer).

### Claude's Discretion
- Exact module filenames within `pinn/training/` (e.g. a config-YAML mapper, a
  checkpoint-store impl, a guards module, a determinism helper) — must EXTEND the
  existing `config.py`/`checkpoint.py` seams and not collide with v1.3-era files.
- The identity-digest canonicalization (JSON canonical sort-keys → sha256).
- `argparse` structure of `pinn.train`; the exact `N` for the failure `tail.log`.
- Whether `latest.pt` is a copy vs hardlink is fixed to **copy** (CTX-54); only the
  internal write ordering is discretion.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Locked Phase 41 scope
- `.planning/phases/41-config-checkpointing-resume-determinism/41-SPEC.md` — Locked requirements (CTRL-01..08), boundaries, acceptance criteria, edge coverage, prohibitions. **MUST read before planning.**
- `.planning/REQUIREMENTS.md` — CTRL-01..08 requirement text (with decision codes B-9, D4-a..d, D6, D7-a..d, B-5, B-11, R-1); the owner-carved seam table.

### The seams this phase fills (Phase-40 hand-off)
- `.planning/phases/40-stage-0-curriculum-training-loop-fut-04/40-CONTEXT.md` — **CTX-42** (TrainingConfig nested dataclasses → YAML mapping), **CTX-43** (CheckpointStore protocol), **CTX-44** (state_dict composition; RNG-as-a-key; weights_only-clean), **CTX-45** (logger tree), CTX-38/39/41 (provisional thresholds, config-required fields, RECOVER semantics). MUST read.
- `.planning/phases/40-stage-0-curriculum-training-loop-fut-04/40-SPEC.md` — the loop contract this layer wraps (TRAIN-01..07).
- `pinn/training/config.py` — the frozen `TrainingConfig` seam (docstring: "Phase 41 maps YAML sections"); the field-for-field mapping target.
- `pinn/training/checkpoint.py` — the `CheckpointStore` seam + naive impl (docstring: "Phase 41" replaces it) that CTX-53..56 implement behind.
- `pinn/training/controllers.py` / `grad_clip.py` / `scheduled_weights.py` — the `state_dict`/`load_state_dict` contracts the checkpoint payload composes.
- `pinn/network.py` / `pinn/training/collocation_sampler.py` — the caller-owned **local** RNG discipline CTX-62 records/restores.
- `pinn/runtime.py` — `resolve_runtime(precision, device)`, the sole precision/device source (CTX-20) the config feeds.

### Ratified build-engineering decisions (grounding for the seams)
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/trainex-r1a-resolution-doc.md` — B-9 (frozen keyed config), D4-a (dual-trigger + ceiling), D4-b (atomic + fallback), D4-c/d (guards + failure bundle), D7-a..d (anchors, promotion, rollback, Adam reset), B-5 (resume-field list — owner-ratified), B-11 / D6 (seed/RNG + reproducibility scope), R-1 (guard/RECOVER thresholds).
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/RATIFICATION.md` — owner ratification record (2026-07-05).

### The runbook/output contracts (41↔42 boundary)
- `docs/work/designs/cross_cutting/training-execution/2026-06-10-training-execution-design.md` — §5.4 Launch (`python -m pinn.train --config …`), §5.6 Resume (`--resume`), §5.7 `runs/<name>/` output structure, §3.3/§3.4 committed-vs-placeholder surface, §6.4 honesty layer. Fixes the Option-A boundary and the run-folder contract.

### The science (read-only; constrains identity fields)
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — Stage-0 curriculum/stage definitions, CURR-03 thresholds (identity-classified in the config-diff).
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — architecture (14→256×12→9, SIREN omega0), PHYS-05 schedule, PHYS-03 `eps_soft=1e-5` (identity constants).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `pinn/training/config.py` — nested frozen `TrainingConfig` (run.seed validated);
  CTX-50 adds the YAML mapper + resolved-copy freeze around it.
- `pinn/training/checkpoint.py` — `CheckpointStore` protocol + naive
  `TorchSaveCheckpointStore`; CTX-53..56 implement the production store behind the
  same interface (no controller changes — CTX-43 seam).
- `pinn/training/controllers.py` / `grad_clip.py` / `scheduled_weights.py` — expose
  `state_dict`/`load_state_dict`; RunController already composes a nested dict keyed by
  component (CTX-44) — the checkpoint payload builds directly on this.
- `pinn/network.py` — local seeded `torch.Generator`; `spec + seed` →
  bitwise-identical params (the determinism substrate CTX-62/63 extend to run level).
- `pinn/runtime.py` — `resolve_runtime` (sole precision/device flow).

### Established Patterns
- Frozen typed dataclass validated at construction (`ArchitectureSpec`,
  `RuntimeSpec`, `TrainingConfig`) — the YAML sub-configs follow it (CTX-50).
- `tests/phaseNN` stdlib-unittest with deferred-import skip guards; conda env
  `pinn-train` via `<home>/miniforge3/bin/conda run -n pinn-train`
  (conda is off-PATH; repo/system pythons lack torch). The end-to-end resume/guard
  checks (CTRL-01/02/05/08) use a **tiny synthetic Stage-0 loop**, no real dataset.
- Structured log lines with machine-readable payloads via `logging` `extra` (CTX-45);
  Phase 41's minimal log uses this tree, Phase 42 attaches the JSONL handler.
- v1.3-era files (`basic_architecture.py`, `data-processing-pipeline-full.py`,
  `data-handling/`) are reference-only and MUST NOT be imported (CTX-17).

### Integration Points
- Phase 41 attaches at exactly the two CTX-42/CTX-43 seams (config dataclasses ←
  YAML; CheckpointStore ← atomic/retention/promotion impl) plus the new
  `pinn.train` entry module and a guards module — all under `pinn/training/`, tested
  under `tests/phase41`.
- The run-folder contract (`runs/<name>/config.yaml`, `checkpoints/`,
  `curriculum.jsonl`, `failure/`) is the Phase-42 hand-off surface (OPS-05 polishes it).
- Phase 43's `verify` ladder + pilot consume the CTX-38 provisional-threshold log and
  calibrate the ⚖ seams (D4-a ceiling, R-1 thresholds) this phase ships as placeholders.

</code_context>

<specifics>
## Specific Ideas

- **Falsifiability drove the Option-A boundary:** CTRL-01 (config drives run), CTRL-02
  (dual-trigger fires), CTRL-05 (`--resume` continues exactly / `--hold-stage`), and
  CTRL-08 (exact checkpoint continuation) are inherently end-to-end — a library-only
  phase could not verify them. Hence the minimal runnable `pinn.train`, with the
  canonical logging schema deliberately left to Phase 42 (OPS-03) to avoid a later
  widen/refactor.
- **Owner-carved seams stay provisional:** D4-a ceiling, R-1 guard/RECOVER thresholds,
  and the B-5 resume-field list ship as clearly-marked ⚖ placeholders/proposals — the
  build never presents them as ratified (SPEC prohibition + governance).
- **`failure/` bundle is disk-floor-safe by design:** the tiered Tier-A/Tier-B split
  (CTX-61) exists specifically so a disk-floor trip can still write its own diagnostic
  bundle — a large tensor dump would defeat the guard that fired.
- **The two "continues exactly" invariants must not be conflated:** *resume* is exact
  checkpoint continuation (bit-faithful next-step draws); *fresh run at the same seed*
  is only statistically equivalent. CTX-64 requires the run to report this scope
  honestly.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope. (Scope creep candidates like the
canonical JSONL/TensorBoard surface and threshold calibration are already assigned to
Phases 42/43 by the roadmap, not deferred here.)

### Reviewed Todos (not folded)
- `d-06-static-epsilon-sensitivity-check.md` (D-06 static-epsilon sensitivity check) —
  matched on generic keywords only; it is an admitted-set physics/data probe
  (Phase 38/43 territory), with no config/checkpoint/resume surface. Not folded.
- `trainex-r1-research-handoff.md` (r1a+r1b sub-package handoff review) — a
  research-process task with no code surface in the control layer. Not folded.

</deferred>

---

*Phase: 41-config-checkpointing-resume-determinism*
*Context gathered: 2026-07-17*
