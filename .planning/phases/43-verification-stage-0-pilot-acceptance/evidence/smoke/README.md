# 43-06 Smoke Evidence — B-5 Ratification + Real ACC-02 Smoke

Phase 43 / Plan 06. This file records owner-ratified disposition of B-5 (Task 1)
and the observed evidence from the real ordinary Stage-0 smoke (Task 2). Task 3
(D4-a) is a separate owner checkpoint and is NOT recorded here by the agent —
see the plan's Task 3 gate.

## Task 1 — B-5 `RESUME_FIELD_REGISTRY` ratification

**Disposition:** `ratify-current` — the registry is ratified **as-is, unchanged**.

**Owner response (verbatim):** "Ratify current as-is"

**Date:** 2026-07-22

**Registry state:** `pinn.training.resume.RESUME_FIELD_REGISTRY` in
`pinn/training/resume.py` is **unchanged**. No source edit was made for this
task. The registry stands at 34 total fields:

- 27 `IDENTITY` fields
  - 22 `REPRESENTED` (concrete fields in `build_identity_payload`): `run.seed`,
    `run.precision`, `run.device`, `run.strict_cpu_determinism`,
    `stage.max_epochs`, `run.guards.loss_explosion_ceiling`,
    `run.guards.disk_floor_fraction`, `run.guards.memory_watermark_fraction`,
    `arch.hidden_depth`, `arch.hidden_width`, `arch.first_omega_0`,
    `arch.hidden_omega_0`, `arch.skip_cadence`,
    `arch.layernorm_elementwise_affine`, `arch.layernorm_eps`, `arch.power_p`,
    `arch.seed`, `constants.D`, `constants.eps_soft`, `constants.T`,
    `effective_runtime.precision`, `effective_runtime.device`
  - 5 `DEFERRED-NOT-REPRESENTABLE` (no v2.0 config source yet):
    `dataset.version_hash`, `dataset.ic_vector_definition`, `split.policy`,
    `loss_catalog.structure`, `curriculum.stage_definitions`
- 7 `OPERATIONAL` (whitelisted to differ across a resume):
  `run.checkpoint.every_n_steps`, `run.checkpoint.wall_clock_ceiling_s`,
  `run.checkpoint.rolling_keep`, `run.checkpoint.failure_keep`,
  `run.log_every`, `opt.validation_every`, `run.num_workers`

The fail-safe unclassified→refuse rule remains LOCKED and untouched: any field
not present in the registry above still refuses a resume.

**Verification (automated):**

```
~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase41.test_resume -v
```

Result: `Ran 30 tests in 0.390s` — `OK`. All 30 tests pass unchanged (no source
edit was made, so the pre-existing green suite is preserved verbatim).

**Note on self-ratification:** this disposition transcribes an owner decision
that was already made and communicated to the executing agent by the
orchestrator ahead of this run; the agent did not select, weigh, or infer the
disposition.

## Task 2 — Real ordinary ACC-02 smoke: HONEST FAILURE, blocked before any step

**Result: the ordinary command refused fail-closed before any training step
ran.** No steps, no checkpoints, no measured `s_per_step`, no timing forecast
were produced. Per SPEC R2 ("a failed/interrupted run names its disposition
and leaves metrics null — never fabricated") this is recorded honestly below;
nothing was substituted, patched around, or fabricated to force a pass.

### Reachability preflight — PASSED

Re-run exactly as the plan requires, immediately before launch:

```
~/miniforge3/envs/pinn-train/bin/python -c "
from pinn.training.config_yaml import load_config
from pinn.train import _admitted_data_preflight
cfg = load_config('configs/smoke.yaml')
root = _admitted_data_preflight(cfg)
print('PREFLIGHT_PASS root=', root)
"
```

Output: `PREFLIGHT_PASS root= <home>/Desktop/3_body_problem/simulation_data/Data`
— `default_data_root()` correctly resolved the corpus via the shared
git-common dir, and the directory-level CTX-79 reachability check passed.

### Ordinary command run — failed downstream of the preflight

Command run exactly as specified, no bespoke harness:

```
~/miniforge3/envs/pinn-train/bin/python -m pinn.train --config configs/smoke.yaml
```

Failure output:

```
error: failed to build data sources: blacklist file
<home>/Desktop/3_body_problem/simulation_data/Data/problematic_ics_blacklist.json
unreadable/invalid: [Errno 2] No such file or directory:
'<home>/Desktop/3_body_problem/simulation_data/Data/problematic_ics_blacklist.json'
```

**Run path:** `runs/stage0-smoke/` (created; not committed — `runs/` is
gitignored). Recorded artifacts:

- `runs/stage0-smoke/summary.json`: `"disposition": "failed"`; every
  `final_losses` value is `null`; `header.wall_clock_secs = 0.268327`
  (construction-phase only — no training loop entered).
- `runs/stage0-smoke/status.json`: `"state": "failed"`, `"step": null`,
  `"s_per_step_ema": null`, `"stage": null`, `"phase": null`.
- No `runs/.calibration/stage0-timing.json` was written — `write_calibration`
  is only ever called from a terminal-success smoke path
  (`pinn.train.main`), and that path was never reached.

**CPU-adapter/MPS-model confirmation:** not applicable — the admitted
`AdmittedSetAdapter` (CPU/fp32, DATA-01) never finished constructing, so no
adapter/model residency split was exercised this run.

**32 admitted-identity count, checkpoints 100/200/300, measured `s_per_step`,
persisted timing forecast:** none of these were produced — the run refused
before any training step, checkpoint, or optimizer construction.

**Interrupt/resume:** not attempted — there was nothing running to interrupt.

### Root cause — DI-43-06-01 (genuine, pre-existing wiring gap; NOT fixed by this task)

The admitted corpus root (`simulation_data/Data/`, resolved via
`default_data_root()`) is reachable, but `AdmittedSetAdapter._load_blacklist`
(`pinn/data/adapter.py`) defaults to `self.data_root / "problematic_ics_blacklist.json"`
when no explicit `blacklist_path` is given, and `pinn.train._build_admitted_sources`
never threads one through (`DataConfig` — 43-03 — exposes no `blacklist_path`
field either). The repo's only copy of that filename lives at
`simulation_data/Documentation/problematic_ics_blacklist.json` — confirmed via
a project-wide `find`, no copy exists anywhere under `simulation_data/Data/`.
`simulation_data/Documentation/README.md` (the canonical dataset-anomalies
source per CLAUDE.md), line 1012, documents that copy explicitly as *"Legacy
blacklist (2 hierarchical, 63 standard IDs); **not** used by current
runners."* Phase 39's own verifier passed an EXPLICIT `--blacklist-path`
CLI flag to `pinn.data.stage_scan` rather than relying on this default
(`39-VERIFICATION.md:188`) — so the ordinary `pinn.train` composition root's
silent-default blacklist resolution had, apparently, never been exercised
against the real corpus before this smoke.

**Why this was NOT fixed in this task:** 43-06's `files_modified` and this
invocation's `GIT_AGENT_OWNED_PATHS` grant
(`.../evidence/smoke/:tests/phase43/`) do not include `pinn/data/adapter.py`,
`pinn/train.py`, or `pinn/training/config.py` — a real fix touches production
code this plan does not own. More fundamentally, this plan's objective is to
prove the REAL, unmodified mechanical wiring works; patching the system under
test moments before running it would defeat the evidentiary purpose of the
smoke. CTX-79 also explicitly forbids any master-corpus mutation as a
workaround (ruling out copying a blacklist file into `Data/`), and the only
candidate file to copy is itself documented as legacy/unused — copying it in
would be inventing a data-governance decision no agent is authorized to make.

**Recommended follow-up (owner/orchestrator decision, not made here):** a
small, explicitly-scoped fix plan should (a) add a `data.blacklist_path`
field to `DataConfig` (or a documented, sane default resolution), (b) thread
it through `_build_admitted_sources` / `AdmittedSetAdapter`, and (c) resolve
— as an OWNER decision, since it governs which trajectories are excluded from
real training — whether the "legacy" Documentation copy is still authoritative
or whether a fresh, current blacklist must be generated/placed at the corpus
root. Once landed, 43-06 Task 2 must be re-run for the real
32-trajectory/300-step/checkpoint-100-200-300/interrupt+resume timing
evidence this plan's `must_haves.truths` requires.

**Consequence for D4-a (Task 3):** no measured `s_per_step` exists from this
invocation, so no honest full-run forecast or candidate wall-clock ceiling can
be derived. See the Task 3 checkpoint return to the orchestrator/owner for the
explicit statement of this gap — the agent did not invent a placeholder value.
