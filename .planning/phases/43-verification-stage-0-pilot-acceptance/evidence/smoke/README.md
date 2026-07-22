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

### DI-43-06-01 RESOLUTION — 2026-07-22, owner Option A

**Owner decision (verbatim summary from the coordinator):** "Option A — fix
now, use the legacy blacklist. The owner has DESIGNATED the legacy 65-ID
Documentation blacklist (`simulation_data/Documentation/problematic_ics_blacklist.json`,
2 hierarchical + 63 standard, verified schema-valid via `load_blacklist_file`)
as the authoritative Stage-0 admission blacklist." The agent was authorized to
make a small, explicitly-scoped wiring fix outside 43-06's original owned
files, with `GIT_AGENT_OWNED_PATHS` expanded to also include
`pinn/training/config.py:pinn/train.py:configs/smoke.yaml`.

**Fix landed (minimal, portable, fail-closed preserved):**

1. `pinn/training/config.py`: added `blacklist_path: Optional[str] = None` to
   `DataConfig`, validated non-empty like `root` when set.
2. `pinn/train.py`: added `_resolve_admitted_data_root()` (mirrors
   `AdmittedSetAdapter._resolve_root`'s precedence — explicit `data.root` →
   `GSD_DATA_ROOT` env → `default_data_root()` — duplicated rather than
   imported, since `pinn/data/adapter.py` stays outside this plan's owned
   files) and `_resolve_blacklist_path()` (a relative `blacklist_path`
   resolves against that root, never the CWD; an absolute path is used as-is;
   `None` preserves the adapter's own default). `_build_admitted_sources` now
   threads `blacklist_path=_resolve_blacklist_path(config)` into
   `AdmittedSetAdapter`. No change to `pinn/data/adapter.py` — the existing
   fail-closed `load_blacklist_file` (missing/invalid file still raises
   `BlacklistSchemaError`, never a silent empty-blacklist substitution) is
   untouched and unbypassed.
3. `configs/smoke.yaml`: added
   `data.blacklist_path: ../Documentation/problematic_ics_blacklist.json`
   (relative to the resolved `Data/` root → resolves to the owner-designated
   legacy blacklist), with a comment recording the owner designation and date.
4. Tests: `tests/phase43/test_real_data_smoke_config.py::BlacklistPathResolutionTests`
   (8 new tests — config-seam validation, relative-vs-absolute-vs-None
   resolution against a temp data root [never the CWD], a `TinyCorpus`
   integration test proving the adapter admits via a RELATIVE sibling-directory
   blacklist path with real entries applied, and a missing-file-still-fails-closed
   regression). Full-suite verification:
   `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase43.test_real_data_smoke_config -v`
   → `Ran 29 tests in 0.300s` — `OK` (includes all 8 new tests + the 21
   pre-existing tests in that module, all still green — no regression).
   `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase41.test_config_yaml -v`
   → `Ran 35 tests in 0.016s` — `OK` (no regression from the `DataConfig`
   field addition). `~/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase41.test_resume -v`
   → `Ran 30 tests in 0.415s` — `OK` (B-5 registry unaffected).

**Result: DI-43-06-01 is CONFIRMED RESOLVED by direct evidence** — the Attempt
2 re-run below reached real per-step training losses over the real admitted
corpus (impossible before this fix), proving the blacklist wiring gap is
closed. **Status: RESOLVED.**

## Task 2, Attempt 2 — real smoke re-run: DI-43-06-01 confirmed fixed, a NEW blocking finding (DI-43-06-02) surfaced

Stale Attempt-1 `runs/stage0-smoke/` (the DI-43-06-01 failure recorded above)
was confirmed as the failed run (`summary.json` `disposition: "failed"`) and
removed (`runs/` is gitignored; not a tracked deletion) before re-launch, so
the run-folder-clobber guard would not trip on the fresh attempt.

**Reachability preflight + blacklist resolution — both PASSED**, re-verified
immediately before launch:

```
PREFLIGHT_PASS root= <home>/Desktop/3_body_problem/simulation_data/Data
blacklist_path= <home>/Desktop/3_body_problem/simulation_data/Documentation/problematic_ics_blacklist.json exists= True
```

**Ordinary command run** (same command, no bespoke harness):

```
~/miniforge3/envs/pinn-train/bin/python -m pinn.train --config configs/smoke.yaml
```

**Run path:** `runs/stage0-smoke/` (gitignored; not committed).

**CPU-adapter/MPS-model confirmation:** `runtime precision=float32 device=mps`
printed at launch (model runtime); the admitted adapter is unconditionally
constructed CPU/float32 in `_build_admitted_sources` (DATA-01, unchanged by
this fix) — this run is the first direct proof the two coexist correctly
against the real corpus: construction succeeded and produced real per-step
losses.

**Admission succeeded — DI-43-06-01 proof:** the run progressed past
`_build_admitted_sources` (impossible in Attempt 1) into real training steps
with real, non-fabricated per-step losses logged to
`runs/stage0-smoke/logs/train.log.jsonl`:

```
step 1: total=23865.10  data=0.175537  ic=23864.9    phys=3.32227e+08  energy=15891.4  angmom=61.9928  lambda_phys=0.0     lambda_e=0.0     s_per_step=null
step 2: total=9426793.0 data=0.19546   ic=13068.1    phys=2.82401e+08  energy=10555.5  angmom=37.5441  lambda_phys=0.03333 lambda_e=0.03333 s_per_step=0.15404354200109083
```

`stage.replay_count: 32` was threaded to `RunController` exactly as
`configs/smoke.yaml` declares (config-level confirmation; the existing 43-03
`ReplayCountSelectionTests` already unit-prove this threading independent of
data content — this run did not fail in any way attributable to the 32-count
seam).

**32 admitted-identity count:** confirmed via config (`stage.replay_count: 32`
threaded unconditionally, per above) — not independently re-derived from a
per-batch debug dump this run, since the run terminated at step 2.

### NEW finding — DI-43-06-02: R-1 `loss_explosion_ceiling` (owner-carved, provisional) trips at step 2 against real admitted data

**Symptom:** step 2's weighted total loss `9,426,793.0` exceeds the
`⚖ PROVISIONAL (R-1)` `run.guards.loss_explosion_ceiling` default of
`1,000,000.0` (`pinn/training/config.py` `_PROVISIONAL_LOSS_EXPLOSION_CEILING`,
never overridden in `configs/smoke.yaml`). `runs/stage0-smoke/failure/trip.json`:

```json
{
  "disposition": "RECOVER",
  "grad_norm": 227824009216.0,
  "guard": "loss_explosion",
  "loss_terms": {"angmom": 37.54, "data": 0.195, "energy": 10555.46, "ic": 13068.06, "phys": 282401184.0, "total": 9426793.0},
  "metric": "loss.total",
  "reason": "loss total 9426793.0 > ⚖ ceiling 1000000.0",
  "step": 2,
  "threshold": 1000000.0,
  "threshold_provisional": true,
  "tier": 2,
  "tripped_guards": ["loss_explosion"]
}
```

`runs/stage0-smoke/curriculum.jsonl`: `{"disposition": "RECOVER", "from_stage":
0, "step": 1, "to_stage": 0}`; `train.log` then logs a second
`stage_exit_disposition=HALT` — RECOVER has no prior ROLLING checkpoint to
roll back to this early (only `stage-0-init.pt`, the pre-training anchor;
the first rolling checkpoint would land at step 100, per
`run.checkpoint.every_n_steps: 100`), so the run terminates `disposition:
"failed"` rather than actually recovering. This is the SAME honest fail-closed
path exercised by DI-43-06-01's Attempt 1 — `summary.json` records
`"disposition": "failed"` with every `final_losses` value `null`; no
`runs/.calibration/stage0-timing.json` was written (still gated on a
terminal-success smoke, never called here).

**Root cause is a raw physics-residual SCALE mismatch, not a wiring bug:** the
RAW (unweighted) `phys` residual is ~2.8–3.3×10⁸ at random SIREN
initialization against the real admitted corpus — three orders of magnitude
larger than what the PHYS-05 warmup ramp (`I_warm = min(2000, floor(0.1 ×
N_Adam,k)) = min(2000, 30) = 30` for this smoke's `n_adam: 300`) can bring
under the 1e6 ceiling within its first couple of ramp steps (`lambda_phys` at
step 2 is only `1/30 ≈ 0.0333`, yet `282401184 × 0.0333 ≈ 9.41M` already
dominates the ceiling by itself). Whether the raw residual scale itself is
expected for real (vs. previously-only-synthetic-tested) data, or points to a
separate scale/units issue upstream, was NOT investigated further — that
diagnosis is outside this task's authorization.

**Why this was NOT fixed here:** `run.guards.loss_explosion_ceiling` is
explicitly documented in `pinn/training/config.py` and echoed in this run's
own `train.log` run-start line as `⚖ PROVISIONAL (R-1):
owner-calibrate-at-Phase-43-pilot loss-explosion guard ceiling; mechanism
ships, value is owner-carved` — R-1 is one of this milestone's five
owner-carved decisions (`.planning/STATE.md` v2.0-init entry), reserved for
the owner to calibrate using EXACTLY this kind of real-pilot evidence. Neither
this task's original scope nor the coordinator's DI-43-06-01 wiring-fix
authorization covers adjusting guard thresholds or loss weights — the agent
did not raise the ceiling, change `loss.lambda_e_max`/warmup length, or take
any other action to force a pass.

**Result:** no checkpoint reached step 100 (`runs/stage0-smoke/checkpoints/`
contains `stage-0-init.pt`, `failure-stage-0-step-1.pt`, `latest.pt`, and a
tier-2 RECOVER anchor — no `step-000100.pt`/`step-000200.pt`/`step-000300.pt`).
No stable measured `s_per_step` (a single early EMA sample,
`s_per_step=0.15404354200109083`, was logged at step 2 before the guard trip —
reported below for completeness, but it reflects two steps of a construction-
adjacent, not-yet-warm run and is NOT proposed as an authoritative D4-a basis).
No interrupt/resume was attempted — the run was already terminal before any
planned SIGTERM point. Total wall-clock for the attempt was `187.359 s`
end-to-end (construction/admission of the real ~8.23M-snapshot corpus into
memory dominates this — it is NOT a per-step training rate).

**Status:** OPEN (BLOCKING — Task 2's must_have real-timing evidence, and
therefore Task 3's D4-a candidate ceiling, still cannot be produced from a
completed real run until the owner decides how to proceed on R-1). See the
Task 3 checkpoint return to the orchestrator/owner for the explicit statement
of this new gap.

## DIAGNOSTIC run (R-1 guard temporarily lifted — NOT the acceptance run)

**Purpose:** owner-authorized (2026-07-22) diagnostic to determine whether the
~2.82e8 raw physics residual observed in the Attempt-2 acceptance run
(DI-43-06-02) is an expected random-init transient that training resolves, or
a real pathology (diverges/NaN) — and to gather a real loss trajectory +
timing so the owner can carve R-1 and D4-a informed. **This run does NOT
count as the ACC-02 acceptance smoke** and does not resolve DI-43-06-02.

**Config (throwaway, uncommitted, scratchpad-only):** a copy of
`configs/smoke.yaml` with exactly two changes — `run.run_name:
stage0-smoke-diag` (distinct run dir) and `run.guards.loss_explosion_ceiling:
1000000000000.0` (1e12, a YAML override for observation only; `configs/smoke.yaml`
and `pinn/training/config.py`'s owner-carved default were NOT touched).
`data.blacklist_path` was kept unchanged (still resolves against the data
root). The file lived only at
`/private/tmp/.../scratchpad/smoke-diag.yaml` and was never committed.

**Execution — two runs, matching the plan's interrupt+resume protocol:**

*Run A (uninterrupted control):* ran to completion in one process to observe
the full uninterrupted trajectory shape. Finished cleanly, `disposition:
"finished"`, `wall_clock_secs: 184.203173` end-to-end (construction/admission
dominates; the 300 training steps themselves took a few seconds once
underway). All 300 steps `finite: true`, zero non-finite steps.

*Run B (interrupt+resume validation):* relaunched fresh (same seed=42, same
config). Tight-polled `status.json` and sent `SIGTERM` the instant step ≥ 100
was observed (caught at step 101). Post-signal `status.json`: `"state":
"interrupted"`, `"step": 102`, exit via the established graceful SIGTERM path
(`pinn.training.signals`). **Checkpoint confirmed persisted before resume:**
`runs/stage0-smoke-diag/checkpoints/step-000100.pt` and `step-000103.pt` both
present; `summary.json` honestly recorded `disposition: "interrupted"` with
every `final_losses` value `null` (R2 — no fabrication on interrupt). Resumed
with `--resume latest`; the resumed process reconstructed the admitted corpus
again (construction is per-process, not persisted) and ran the remaining
steps to completion: `disposition: "finished"`, checkpoints
`step-000200.pt` and `step-000300.pt` landed, `train.log.jsonl` shows a single
coherent, non-duplicated, gap-free trajectory from step 1 to step 300 (300
records total). **Interrupt+resume on real admitted data: CONFIRMED WORKING.**

### Loss trajectory — does it descend?

Combined observation across Run A (full, uninterrupted) and Run B (resumed
continuation), sampled at representative steps (`total` / raw `phys` /
`lambda_phys` ramp fraction; format `value` in scientific notation):

```
step   1: total=2.3865e+04  phys=3.3223e+08  lambda_phys=0.0000
step   2: total=9.4268e+06  phys=2.8240e+08  lambda_phys=0.0333
step  10: total=7.5345e+07  phys=2.5094e+08  lambda_phys=0.3000
step  20: total=4.0334e+08  phys=6.3681e+08  lambda_phys=0.6333
step  30: total=7.9042e+08  phys=8.1761e+08  lambda_phys=0.9667
step  50: total=4.8338e+08  phys=4.8334e+08  lambda_phys=1.0000
step 100: total=3.7347e+09  phys=3.7346e+09  lambda_phys=1.0000  <- PEAK (Run A)
step 150: total=1.9788e+08  phys=1.9787e+08  lambda_phys=1.0000
step 200: total=2.4983e+08  phys=2.4980e+08  lambda_phys=1.0000
step 250: total=3.1386e+08  phys=3.1384e+08  lambda_phys=1.0000
step 300 (Run A, uninterrupted): total=6.5044e+08
step 300 (Run B, resumed):       total=4.1721e+08
```

**Per-third median/mean `total` (Run B's single coherent 1-300 trajectory) —
checking for a downward trend:**

| Steps | median | mean | min | max |
|---|---|---|---|---|
| 1-100 | 4.014e+08 | 5.989e+08 | 2.387e+04 | 3.735e+09 |
| 101-200 | 4.238e+08 | 6.364e+08 | 3.612e+07 | 4.081e+09 |
| 201-300 | 3.887e+08 | 5.569e+08 | 3.359e+07 | 4.120e+09 |

Final 10 steps (291-300) `total`: `4.24e8, 1.79e8, 8.15e8, 6.54e8, 1.90e8,
1.19e8, 1.74e8, 8.77e8, 1.06e9, 4.17e8` — still spanning two orders of
magnitude at the very end of the 300-step Adam budget.

**Non-finite check:** zero non-finite steps across all ~600 logged step
records (Run A's 300 + Run B's 300) — the loss is finite/bounded throughout,
never NaN, never Inf, and does not runaway-grow monotonically either (it
peaks once `lambda_phys` reaches ~1.0 around step ~75-100, then oscillates in
roughly the same 1e8-1e9 order of magnitude for the remainder of the budget).

**Honest characterization — this does NOT cleanly match either proposed
category:** it is not a "real pathology" in the diverge/NaN sense (confirmed
finite throughout, both runs). It is also not a clean "expected transient
that resolves" in the sense of settling to a small, controlled loss — the
per-third medians (4.01e8 → 4.24e8 → 3.89e8) show essentially NO downward
trend across the full 300-step Adam budget at this smoke's hyperparameters
(`loss.lambda_e_max: 1.0`, `I_warm=30`, `n_adam=300`, `opt.adam_lr_base` per
run-start log). The raw physics residual stays large and noisy (bounded
roughly within 1e7-1e9, briefly touching ~4e9) rather than shrinking toward
zero within this budget. Root cause (whether this residual scale is expected
for the real corpus's physical units, or points to a separate scale/tuning
issue) was NOT investigated further — outside this diagnostic's scope.

### Warm measured `s_per_step` + forecast

From Run A's `train.log.jsonl` (n=298 finite `s_per_step` samples, excluding
the first 5 post-construction warm-up samples): **median 0.09229 s/step, mean
0.09259 s/step**, range [0.08852, 0.10846]. The persisted calibration from Run
B's terminal-success finish (`run.smoke: true` → `_write_smoke_timing_calibration`
fired normally, gitignored, not committed):

```json
{
  "schema_version": "phase43-stage0-timing/v1",
  "s_per_step": 0.09410000567703417,
  "full_stage0_steps": 300,
  "forecast_seconds": 28.23000170311025,
  "fingerprint": {"device": "mps", "dtype": "torch.float32", "torch_version": "2.12.1",
                   "python_version": "3.11.15", "git_head": "464fd40dc4a7947d18f73357faa72e7a66e2d848",
                   "git_head_available": true},
  "valid": true
}
```

**300-step smoke forecast: ~28.2 s** (measured, not construction time —
construction/admission of the real corpus separately took ~150-185 s per
process launch, which is a distinct, per-launch fixed cost, not a per-step
rate). This diagnostic run's calibration write is the most recent one in the
shared, gitignored `runs/.calibration/stage0-timing.json` — expected,
harmless mechanism behavior (not committed, not a repo change).

**Note:** translating the per-step rate into a D4-a WALL-CLOCK CEILING for
the actual Stage-0 pilot/production run additionally requires the intended
real run's step count (not determined by this diagnostic, which only ran the
smoke's own 300-step budget) — see the suggested range below for how the
agent handled that gap.

### Checkpoints and resume — full accounting

`step-000100.pt` (Run B, evicted by rolling retention after later saves —
confirmed present at interrupt time before eviction), `step-000103.pt` (Run
B, final pre-interrupt save), `step-000200.pt` and `step-000300.pt` (Run B,
post-resume). Run A separately produced `step-000100.pt`, `step-000200.pt`,
`step-000300.pt` in its own uninterrupted pass (overwritten when Run B
reused the same run directory name after Run A's artifacts were copied aside
and removed). Both runs' `best.pt` / `latest.pt` / `stage-0-init.pt` anchors
present as expected.

### Explicit framing

**This diagnostic evidence is NOT a passing acceptance run.** It exists
solely to inform the owner's R-1 (`loss_explosion_ceiling`) and D4-a
(`wall_clock_ceiling_s`) carves with real trajectory and timing data. The
guard was lifted via a YAML override for observation only; `configs/smoke.yaml`
and the owner-carved default in `pinn/training/config.py` are unchanged.
DI-43-06-02 remains OPEN until the owner ratifies R-1 (or another remedy) and
a real acceptance-run smoke completes with the production guard active.

## DI-43-06-02 RESOLUTION — 2026-07-21, owner delegation ("follow your best judgement")

**Owner decision (verbatim summary from the coordinator):** the owner
DELEGATED the R-1 `loss_explosion_ceiling` value to the orchestrator's best
judgement, rather than selecting a number directly. **Ratified value:
`1.0e11`** — calibrated from the diagnostic run's observed peak total loss
(~4e9, single seed, MPS/fp32; see the loss-trajectory table above), giving
roughly 25x headroom above that peak. Provenance recorded everywhere it
matters: owner-ratified via delegation 2026-07-21; explicitly **REVISABLE at
the ACC-05 Stage-0 pilot** (this value is not assumed to generalize across
seeds, corpora, or curriculum stages beyond Stage-0).

**Fix landed (`pinn/training/config.py`, commit `9cd5e85`):**
`_PROVISIONAL_LOSS_EXPLOSION_CEILING` changed from `1.0e6` to `1.0e11`. The
constant name and its `_PROVISIONAL` registry tuple entry were deliberately
**kept as-is** (not renamed, not removed from the registry) — see the
provisional-flag ambiguity note directly below. Both `tests.phase41.test_config_yaml`
(35/35) and `tests.phase41.test_resume` (30/30) pass unchanged after this
edit; no test in the repository asserted the literal old default value
(all existing `1e6`/`1e12` references in `tests/phase41/test_guards.py`,
`tests/phase42/*`, and `tests/phase41/test_train_entrypoint.py` are explicit
test-fixture overrides, not assertions on the production default), so no test
file required a corresponding edit.

**Provisional-flag ambiguity (explicitly surfaced, not guessed):**
`run.guards.loss_explosion_ceiling`'s entry in `TrainingConfig.provisional_fields()`
still reports `provisional: True`, identical to the still-uncalibrated
`disk_floor_fraction` / `memory_watermark_fraction` R-1 siblings. This was a
deliberate choice, not an oversight: R-1 as a whole is documented (`.planning/STATE.md`
v2.0-init entry) as ONE owner-carved decision spanning all three `GuardConfig`
thresholds, reported together under one shared registry. Splitting the
*reporting mechanism* itself (i.e., making `provisional_fields()` distinguish
a ratified guard threshold from an unratified one) was judged out of scope for
this ratification — no owner instruction addressed the reporting mechanism,
only the value. The **value** change is unambiguous and is applied; the
**flag** is left untouched pending an explicit owner or design decision on
whether/how `provisional_fields()` should represent partially-ratified
seams. Each `_PROVISIONAL` registry entry's `provenance` string is
independent per field, so this is a reporting-granularity question, not a
code-structure blocker — a future plan may resolve it without re-touching the
ratified value.

**Status: RESOLVED** — DI-43-06-02 is closed. The blocking condition (no real
acceptance smoke could complete under the production guard) is lifted; see
the acceptance-run section below for the completed run this ratification
unblocked.

## Task 2 — REAL ACC-02 acceptance smoke: PASSED (R-1 = 1e11)

Two acceptance-run attempts were made under the ratified `1e11` ceiling. The
first surfaced a new, non-blocking finding (checkpoint-retention eviction);
the second, after a config-only fix, is the accepted evidence for this plan's
must_have truths.

### Attempt 1 (superseded by Attempt 2's config fix) — mechanically PASSED, but did not preserve checkpoint 100

Stale `runs/stage0-smoke/` from the DI-43-06-02 attempt (disposition
`"failed"`, guard-tripped at 1e6) was confirmed and removed before this
attempt launched.

Reachability preflight re-verified immediately before launch: `PREFLIGHT_PASS
root= <home>/Desktop/3_body_problem/simulation_data/Data`.

Ordinary command run, no bespoke harness: `python -m pinn.train --config
configs/smoke.yaml`. Interrupted once via a single `SIGTERM` after the
step-100 periodic checkpoint was confirmed on disk (caught at step 163);
`status.json` / `summary.json` honestly recorded `state`/`disposition:
"interrupted"` with every `final_losses` value `null` (R2 — no fabrication).
Resumed with `--resume latest`; ran gap-free to step 300, `disposition:
"finished"`, `final_losses` populated with finite values, `run.guards.loss_explosion_ceiling=1e11`
never tripped (`failure/` directory present but empty — proactively created,
never populated). Total run wall-clock (construction + steps, both
launches): `179.79 s` + `174.69 s`. Persisted timing calibration:
`s_per_step=0.09410` (Run A's construction), `s_per_step=0.09882` at
finish (`git_head=9cd5e853ee9536df66e780f80cb28bfb75fb5574` — confirms this
run executed against the ratified-R-1 commit).

**New finding (checkpoint-retention eviction, non-blocking, self-fixed):** at
run end, `runs/stage0-smoke/checkpoints/` held `step-000164.pt`,
`step-000200.pt`, `step-000300.pt` — **`step-000100.pt` was missing**,
evicted by `CheckpointCadence.rolling_keep`'s class default of `3`. Root
cause: `TorchSaveCheckpointStore.save_rolling()` writes ALL `step-*.pt` saves
(both the periodic cadence saves AND the interrupt-time rolling save) into
one shared eviction pool; `_evict_rolling()` keeps only the newest
`rolling_keep` entries with no distinction between "periodic" and
"interrupt" saves. The one, plan-required SIGTERM interrupt (off-cadence, at
step 163/164) added a 4th `step-*.pt` entry alongside the 3 periodic saves
(100/200/300); once step 300 landed, the pool held 4 entries against a
keep-3 limit, and the oldest (100) was evicted. This exactly reproduces what
the earlier owner-authorized DIAGNOSTIC run (Run B, above) had already shown
in passing ("`step-000100.pt` ... evicted by rolling retention after later
saves") — that observation is the same underlying mechanism, now confirmed
to actually violate this plan's must_have on a real acceptance run.

**Why this was self-fixed (Rule 3, not escalated):** `rolling_keep` is
explicitly documented in `pinn/training/config.py`'s `CheckpointCadence`
docstring as an "operational hygiene bound" — it is NOT one of the five
owner-carved v2.0 seams (D1-p precision, D4-a checkpoint ceiling, R-1/R-2
guard thresholds, B-5 resume-field list). A blocking issue in an operational,
non-scientific knob is within the executor's auto-fix authority. Fix (commit
`4ea595b`): bumped `configs/smoke.yaml`'s `run.checkpoint.rolling_keep` from
the class default (3) to **4** — the minimal value that tolerates exactly
one off-cadence interrupt alongside the 3 required periodic saves. This run's
artifacts were superseded by Attempt 2 below (re-run after the fix) rather
than patched in place, since checkpoint files cannot be un-evicted after the
fact.

### Attempt 2 (ACCEPTED — this plan's must_have evidence) — full PASS

Config: identical to Attempt 1 plus `run.checkpoint.rolling_keep: 4` (commit
`4ea595b`). `runs/stage0-smoke/` removed and the smoke re-run fresh end to
end (fresh construction, fresh interrupt, fresh resume) — no artifact reuse
across attempts.

**Reachability preflight:** re-verified before launch (unchanged from
Attempt 1's config; not re-quoted here).

**Run path:** `runs/stage0-smoke/` (gitignored, not committed).

**CPU-adapter/MPS-model confirmation:** stdout at both launch and resume:
`runtime precision=float32 device=mps` (model runtime); the admitted adapter
is unconditionally constructed CPU/float32 in `_build_admitted_sources`
(DATA-01, unchanged). `runs/stage0-smoke/config.yaml` (the frozen run config)
records `data.source: admitted`, `data.blacklist_path:
../Documentation/problematic_ics_blacklist.json`, `data.root: null` (resolves
via `default_data_root()`).

**32 admitted-identity count:** `stage.replay_count: 32` confirmed in the
frozen `runs/stage0-smoke/config.yaml` (config-level confirmation, matching
the existing `ReplayCountSelectionTests` unit proof of this threading — the
run did not fail in any way attributable to the 32-count seam).

**Checkpoints — full accounting (100/200/300 all present, plan requirement
met):**

```
best.pt                  (finished-run best-loss anchor)
ckpt-16085826544.pt      (pre-training construction anchor)
latest.pt                (final state, refreshed on every rolling save)
stage-0-init.pt          (k=0 rollback anchor)
step-000100.pt           (periodic, every_n_steps=100)
step-000158.pt           (interrupt-time rolling save — SIGTERM caught at step 157/158)
step-000200.pt           (periodic)
step-000300.pt           (periodic, final)
```

All 4 `step-*.pt` entries coexist under `rolling_keep=4` — no eviction.

**Interrupt/resume — full accounting:** single `SIGTERM` sent after the
step-100 periodic checkpoint was polled and confirmed present on disk;
signal caught at step 157 (`status.json`: `"state": "interrupted"`, `"step":
157`); `summary.json` honestly recorded `"disposition": "interrupted"` with
every `final_losses` value `null` (R2 — no fabrication on interrupt; no
timing calibration was written, per the honesty-guard contract). Internal
curriculum-machinery log lines (`[adam_lbfgs_handoff] ... trigger=budget-exhausted`,
`[stage_exit_disposition] ... disposition=HALT`) appear in `train.log` at the
interrupt step — this is EXPECTED, benign behavior: the internal Adam loop's
early exit on `should_stop()` is classified internally as budget-exhaustion
by the stage-exit machinery, but `pinn/train.py`'s composition root checks
`signal_state.stop_requested` FIRST (before consulting that internal
disposition) and correctly overrides it, reporting `"interrupted"` — the true
disposition — to `status.json`/`summary.json`. This was traced in
`pinn/train.py` (`if signal_state.stop_requested: ... return
finish_run("interrupted", ...)`) and `pinn/training/signals.py`
(`handle_sigterm` only sets `stop_requested = True`), confirming no
mislabeling occurred.

Resumed via `python -m pinn.train --config configs/smoke.yaml --resume
latest`; the resumed process reconstructed the admitted corpus again
(construction is per-process, not persisted) and ran the remaining steps to
completion: `disposition: "finished"`, checkpoints `step-000200.pt` and
`step-000300.pt` landed. `train.log.jsonl` step-record analysis (300 total
records across the combined pre-interrupt + post-resume trajectory):
**300/300 unique steps 1–300, zero missing, zero duplicated, zero non-finite**
— a single coherent, gap-free trajectory.

**Measured `s_per_step` + persisted timing forecast:**

```json
{
  "schema_version": "phase43-stage0-timing/v1",
  "s_per_step": 0.11570179534756522,
  "full_stage0_steps": 300,
  "forecast_seconds": 34.710538604269566,
  "timestamp": "2026-07-22T05:52:18.150298+00:00",
  "fingerprint": {
    "device": "mps", "dtype": "torch.float32", "torch_version": "2.12.1",
    "python_version": "3.11.15",
    "git_head": "9cd5e853ee9536df66e780f80cb28bfb75fb5574",
    "git_head_available": true
  },
  "valid": true
}
```

`git_head` confirms this run executed against the R-1-ratification commit.
Total wall-clock across both launches: `178.22 s` (pre-interrupt) + `186.42 s`
(post-resume) — construction/admission of the real ~8.23M-snapshot corpus
into memory dominates each launch; this is a distinct per-launch fixed cost,
not a per-step rate. The `s_per_step≈0.1157` this run measured is
somewhat warmer/slower than the earlier diagnostic's `0.0941–0.0982` (both
single-sample MPS/fp32 measurements on the same machine under normal
session load variance) — both are real, unfabricated measurements; D4-a
(Task 3) should treat this range, not a single point estimate, as the basis
for a wall-clock ceiling.

**R-1 guard headroom (no trip):** max observed per-step `total` loss this
run was `4.615e9` — the `1e11` ceiling held with roughly **21.7x headroom**
above that peak, consistent with the diagnostic run's ~25x estimate (this
run's specific max differs slightly from the diagnostic's ~4e9 sample by
ordinary run-to-run noise at random SIREN init + real-corpus batch content;
both are well within the ratified ceiling). `runs/stage0-smoke/failure/` is
present but **empty** — proactively created directory structure, never
populated (no guard ever tripped this run); `train.py`'s `failed` predicate
(`any((run_dir / "failure").iterdir())`) correctly evaluates `False` against
an empty directory.

**Loss trajectory — honest, non-convergence characterization (R2 / ACC-05
watch-item):** per-third `total` loss statistics over the full 300-step
combined (pre-interrupt + resumed) trajectory:

| Steps | median | mean | min | max |
|---|---|---|---|---|
| 1-100 | 4.014e+08 | 5.989e+08 | 2.387e+04 | 3.735e+09 |
| 101-200 | 4.280e+08 | 6.958e+08 | 2.038e+07 | 4.615e+09 |
| 201-300 | 4.292e+08 | 6.304e+08 | 3.864e+07 | 2.395e+09 |

Medians show essentially **no downward trend** (4.01e8 → 4.28e8 → 4.29e8)
across the full 300-step Adam budget — consistent with the earlier
diagnostic run's finding. `summary.json`'s own `validation` block records
`"trend": "worsening"` at step 300 (`final_val_loss: 1.118e9`). **This run
does NOT claim, and must not be read as claiming, convergence** — ACC-02
passing means the mechanical pipeline (launch → admit real data → train →
checkpoint → interrupt → resume → finish → measure timing) works correctly
end-to-end and the guard/timing evidence is genuine, nothing more. See the
"ACC-05 pilot watch-item" note below.

### Task 3 — real-data success-path tests: ACTIVATED, all PASS

`tests/phase43/test_smoke.py::RealSmokeArtifactTests` activated automatically
(skip-to-green convention, no source edit required — the class's `setUp`
skip guard on `checkpoints/step-000300.pt` existence resolved on its own once
Attempt 2's real run landed that file):

```
python -m unittest tests.phase43.test_smoke -v
```

Result: **9/9 pass, 0 skips** — `RealCorpusReachabilityGuardTests` (1),
`HonestyGuardTests` (4), `RealSmokeArtifactTests` (4: checkpoints-100-200-300,
measured-s_per_step-finite-positive, persisted-calibration-valid,
resume-result-finished). No `unittest.SkipTest` fired in
`RealSmokeArtifactTests` this run (confirmed via `grep -i skip` on the `-v`
output — zero matches).

```
python -m unittest tests.phase43.test_real_data_smoke_config -v
```

Result: **29/29 pass** (unchanged from the DI-43-06-01 fix — no regression;
this module's own suite doesn't touch checkpoint retention).

Full `tests/phase43/` discovery sweep (`python -m unittest discover -s
tests/phase43 -v`): **160/160 pass**.

### ACC-05 Stage-0 pilot watch-item

**The Stage-0 smoke's loss is bounded but non-descending within a 300-step
Adam budget at this smoke's hyperparameters** (`loss.lambda_e_max: 1.0`,
`I_warm=30` per PHYS-05 warmup, `n_adam=300`, real admitted 32-trajectory
replay). Both the earlier diagnostic run and this accepted acceptance run
independently observe the same pattern: per-third medians stay flat
(~4.0-4.3e8) rather than trending down, and `validation.trend` is reported
`"worsening"` at step 300. This is NOT a mechanical failure — the pipeline
trains, checkpoints, interrupts, resumes, and finishes correctly, and the
loss stays finite/bounded throughout (zero non-finite steps across both
diagnostic and acceptance runs) — but it IS an open question for the actual
ACC-05 Stage-0 pilot (a longer run, likely spanning the Adam→L-BFGS handoff
and multiple stages) to watch: does the loss actually descend given a longer
budget, a full curriculum, and/or different hyperparameters, or does this
non-descending pattern persist and indicate a tuning issue upstream (LR
schedule, warmup length, loss weighting)? Root cause was NOT investigated
further in this plan — out of 43-06's scope (owner-carved R-1 calibration,
not loss-curve tuning).

## Task 3 — D4-a `wall_clock_ceiling_s` RESOLVED — 2026-07-21, owner explicit selection

**Owner decision (explicit selection, not delegated):** `run.checkpoint.wall_clock_ceiling_s
= 120` (seconds), selected directly by the owner from the options presented
below — the owner picked the value itself rather than delegating best
judgement (contrast with R-1's DI-43-06-02 delegation above).

**Context presented to the owner before the pick:**

- **Mechanism (verified, not assumed):** `CheckpointCadence.wall_clock_ceiling_s`
  forces a checkpoint once elapsed-since-last-write reaches the ceiling,
  OR'd with the `every_n_steps` periodic cadence (`pinn/training/config.py`
  `CheckpointCadence` docstring + `__post_init__`). It is a **stall-bounding
  safety net**, not an abort trigger — it never stops or fails a run; it only
  forces an extra save if the normal cadence would otherwise leave too much
  unsaved progress during a slow/stalled stretch.
- **Normal inter-checkpoint interval, measured:** ~9-12 s in the accepted
  Task 2 acceptance smoke (Attempt 2, this file, `s_per_step≈0.1157`,
  `every_n_steps=100` → ~11.57 s between periodic saves at this smoke's
  cadence; the earlier diagnostic run's warmer `s_per_step≈0.0941-0.0982`
  gives ~9.4-9.8 s per 100-step interval).
- **Production Stage-0 forecast:** ~270-305 s per run (derived from the same
  measured `s_per_step` range scaled to a full-curriculum Stage-0 budget,
  not just this smoke's 300-step Adam-only budget).
- **Template's pre-existing example value:** `3600` s (1 hour) — the
  commented documentation example in `configs/stage0-example.yaml` before
  this plan's edit, itself inherited from `pinn/training/config.py`'s
  `_PROVISIONAL_WALL_CLOCK_CEILING_S` class default (unchanged by this
  ratification — see below).

**Owner's stated rationale (verbatim summary from the coordinator):** choose
a ceiling roughly 10x the normal ~9-12 s inter-checkpoint interval so it
never fires during a healthy run, while still bounding unsaved progress on a
stall to at most ~2 minutes. `120` s satisfies both: it is comfortably above
the ~9-12 s normal interval (never fires healthy) and comfortably below the
~270-305 s full-run forecast (bounds a stall meaningfully), landing at the
owner's explicit "~2 minutes" bound.

**Persistence — landed exactly as specified:**

`configs/stage0-example.yaml` `run.checkpoint` changed from `{}` (all
defaults) to an active mapping carrying `wall_clock_ceiling_s: 120`; the
commented `every_n_steps: 100` documentation example is retained unchanged
(still an accurate description of the class default when not overridden).
The commented `wall_clock_ceiling_s: 3600` documentation example was removed
from the commented block (it would otherwise contradict the now-active `120`
override in the same file) — the class default of `3600.0` in
`pinn/training/config.py`'s `_PROVISIONAL_WALL_CLOCK_CEILING_S` is
**unchanged**, per this task's explicit instruction to retain the config
class's provisional default. `pinn/training/checkpoint.py`,
`pinn/training/config.py`, and `pinn/training/resume.py` were **not**
touched by this task.

**Also owner-authorized in the same edit (stale-comment fix, not a new
carve):** the commented guard example `loss_explosion_ceiling: 1.0e6` in
`configs/stage0-example.yaml` was stale — it still showed the pre-DI-43-06-02
default even though R-1's `loss_explosion_ceiling` was owner-ratified to
`1.0e11` via delegation earlier in this same plan (see the DI-43-06-02
resolution section above, commit `9cd5e85`). Fixed to `1.0e11`, and the
adjacent comment now honestly states: `loss_explosion_ceiling` is
owner-ratified (2026-07-21, via delegation; explicitly revisable at the
ACC-05 Stage-0 pilot); `disk_floor_fraction` / `memory_watermark_fraction`
remain uncalibrated ⚖ provisional placeholders (R-1), unchanged by this task.

**Verification (automated):**

```
~/miniforge3/envs/pinn-train/bin/python -c "
from pinn.training.config_yaml import load_config
cfg = load_config('configs/stage0-example.yaml')
v = cfg.run.checkpoint.wall_clock_ceiling_s
assert float(v) == 120.0, v
print('D4-a persisted:', v)
"
```

Output: `D4-a persisted: 120.0` — confirms the declared production template
target loads the owner-ratified value through the ordinary `load_config`
composition root, with no other target edited.

**Commit:** `386f2ee` (`feat(43-06): persist owner-ratified d4-a wall clock
ceiling in stage0 template`).

**Status: RESOLVED.** D4-a is owner-ratified and persisted in the declared
production template before the ACC-05 Stage-0 pilot. Both of 43-06's blocking
owner checkpoints (B-5 Task 1, D4-a Task 3) are now closed; R-1 (surfaced
mid-plan as DI-43-06-02) is also closed via delegation. This plan's
`must_haves.truths` are satisfied: the real ordinary smoke evidence exists
(Task 2 Attempt 2, above) and B-5/D4-a persist at their exact owner-ratified
targets.
