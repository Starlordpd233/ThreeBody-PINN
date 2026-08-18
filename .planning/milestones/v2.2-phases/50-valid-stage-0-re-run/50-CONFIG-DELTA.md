# Phase 50 Config-Delta Record

**Dated:** 2026-08-12

This record enumerates **every** deliberate difference between the Phase-50
graded configs (`configs/stage0-rerun-seed{41,42,43}.yaml`) and the frozen
v2.0 pilot config at `runs/stage0-pilot-seed42/config.yaml` — the actual,
resolved config the seed-42 pilot run executed under, read directly from disk
rather than assumed (`50-CONTEXT.md` D-03). Every row below was derived by
loading both configs through `pinn.training.config_yaml.load_config` (which
fills every dataclass default) and structurally comparing the two resolved
objects field-by-field, so a field one side sets and the other leaves at its
code default is caught the same as an explicit value change. Register entry
`STAGE0-BUDGET-DELTA` (`pinn/conformance/divergence_register.json`) carries
the durable caveat this table documents; that entry is a `kind: qualification`
record, `status: open`, and travels into every Phase-50 run's conformance
block automatically.

## Field-level differences

| Key | v2.0 pilot (frozen, seed 42) | Phase-50 graded (resolved) | Authority |
|---|---|---|---|
| `stage.max_epochs` | `300` | `1000` | `50-CONTEXT.md` D-01 — the shipped `configs/stage0-example.yaml` production budget, not the ACC-02 smoke budget the pilot actually ran. |
| `stage.n_adam` | `300` | `1000` | `50-CONTEXT.md` D-01/D-03 — see "the budget delta is a confound, not a duration extension" below. |
| `run.smoke` | `true` | absent (resolves `false`) | `50-CONTEXT.md` D-01 ground 2 — the v2.0 "pilot" config carries `run.smoke: true`; it is the ACC-02 ~5-minute mechanical smoke budget, not a Stage-0 production run, despite being called "the pilot." |
| `run.run_name` | `stage0-pilot-seed42` | `stage0-rerun-seed42` | Phase-50 run naming, deliberately distinct from every resident v2.0/v2.1 `runs/stage0-pilot-seed4X` / `runs/stage0-smoke*` artifact so those are preserved intact (`50-CONTEXT.md` "Claude's Discretion"). |
| `loss.lambda_e_max` | `1.0` | `0.0` | CONF-06 (Phase 48) — the Stage-0 energy-supervision cap was repaired to the locked PHYS-05 zero row; the pilot predates that repair. |
| `run.invariants.front_advance_window_n` | unset (`null`; invariant B record-only) | `500` | Owner ruling 2026-08-05 (`50-CONTEXT.md` GATE-03/D-20); the pilot predates invariant B entirely (Phase 49). |
| `stage.replay_count` | `32` (explicit, inherited from the smoke config the pilot actually ran) | unset at the config level (`null`); `RunController._stage_batch` then delegates to `build_stage_batch`'s own DATA-05 default, `select_stage_records(replay_count=240)` (`pinn/data/batches.py:71`) | `50-CONTEXT.md` D-01/D-06 — the graded copy source `configs/stage0-example.yaml` never sets `stage.replay_count`, so it resolves to the DATA-05 default. This is a **7.5x training-batch identity/workload change** (32 -> 240 replay identities per batch), not a cosmetic omission. |
| `run.checkpoint.rolling_keep` | `4` | `3` (class default; `configs/stage0-example.yaml` does not override it) | `50-CONTEXT.md` D-06 — the pilot's `rolling_keep: 4` was a 43-06 ACC-02 smoke-specific interrupt/resume acceptance tuning (`configs/smoke.yaml`'s own comment: "bumped from the class default (3) to 4... a mid-run SIGTERM interrupt writes an extra off-cadence step-*.pt rolling save"), never carried into `configs/stage0-example.yaml`. D-06 requires the graded configs carry the shipped example verbatim, so this smoke-only operational tuning is correctly absent, not a Phase-50 omission. |

**Fields checked and confirmed IDENTICAL (not listed above):** `run.recover_retries` (`0` both), `run.checkpoint.wall_clock_ceiling_s` (`120.0` both), `run.checkpoint.every_n_steps` (`100` both, class default), `run.guards.{loss_explosion_ceiling,disk_floor_fraction,memory_watermark_fraction}` (`1e11`/`0.05`/`0.7` both), `opt.validation_every` (`100` both), and every `opt.adam_*`/`opt.lbfgs_*`/`stage.{beta,patience,eps_plateau,eps_phys,eps_energy}` field (all resolve to the same class defaults on both sides — the `configs/stage0-example.yaml` owner-ratification comments for these fields document values that already match the class default, so leaving them commented-out changes nothing).

## Execution-protocol delta (non-YAML)

| Delta | v2.0 pilot | Phase 50 | Authority |
|---|---|---|---|
| Launch guard | ordinary fresh `python -m pinn.train --config <yaml>` (no Stage-0 ceiling) | requires `--stage-0-only` | SCOPE-27 / `50-CONTEXT.md` D-01. The flag has **no optimizer or data-path effect while inside Stage 0** — it changes behavior only after a Stage-0 `ADVANCE`, where it enforces SCOPE-27 by stopping before any Stage-1 side effect (no stage increment, no `stage_factory`/Stage-1 conformance call, no `stage-1-init` write, no 0->1 promotion, no Stage-1 rewarm). This is not hidden inside the YAML diff above because it is not a config value; it is a required CLI argument, and its absence on any Phase-50 launch is itself a conformance defect. |

## The budget delta is an optimization-path and workload confound, not a pure duration extension

`stage.n_adam` moving 300 -> 1000 does not merely lengthen the run by 3.33x.
It also moves three other quantities that are all functions of `n_adam`:

- The PHYS-05 integer warmup `I_warm = floor(0.1 * n_adam)` moves **30 -> 100**,
  so the first step at which `lambda_phys` reaches its full weight moves from
  step **31** to step **101**.
- The `CosineAnnealingLR` schedule horizon `T_max` moves **300 -> 1000**.
- The number of validation opportunities at `validation_every: 100` moves
  **3 -> 10**.

Separately, `stage.replay_count` moves **32 -> 240** (the row above) — a
7.5x training-batch identity/workload change that has nothing to do with step
count. Phase 44 (`44-DIAGNOSIS.md` §6) ranked "undertrained budget" as a live
hypothesis for the v2.0 physics-gate failure, so these intertwined,
simultaneous changes matter directly to Phase 52's DIAG-05 re-derivation and
**prohibit clean causal attribution** of any v2.2-vs-v2.0 outcome difference
to any single one of: the conformance repair, the budget extension, the
warmup-onset shift, the cosine-horizon change, or the batch-workload change.
This full confound — not merely "the runs are 3.33x longer" — is what
register entry `STAGE0-BUDGET-DELTA` exists to keep durable and travel
forward automatically into every Phase-50 run record and Phase 52's DIAG-05.

**Phase 50 does NOT add a 300-step budget-matched arm** to isolate this
confound from the conformance repair. That measurement is beyond RUN-01/RUN-02
and is recorded as a deferred idea (`50-CONTEXT.md` §Deferred Ideas); it
belongs to Phase 52's DIAG-05 if the re-derivation needs it, or to the owner
if a tighter A/B comparison is wanted.

## `run.log_every`: protocol parity, currently inert (not a pilot-vs-Phase-50 difference)

## Generation 3 (2026-08-15) — config delta verified identical to generation 2

The generation 3 config delta is verified identical to generation 2. Generation 3 does **not** change any committed config byte. The four Phase-50
configs (`configs/stage0-rerun-smoke.yaml` and
`configs/stage0-rerun-seed{41,42,43}.yaml`) were re-hashed from
`git show 312f3080ab50e35be18ba87c9f0618866265b227:<path>` (the Task-3
GAP-50-02 repair commit, C-09, the generation-3 source identity) and matched
the generation-2 `committed_config_sha256_by_path` values exactly:

| Path | sha256 (unchanged) |
|---|---|
| `configs/stage0-rerun-seed41.yaml` | `90ccd7418211ca42ebe14e06ea0bf1f62249d87e19b71c9f670c9a9b8374f073` |
| `configs/stage0-rerun-seed42.yaml` | `72db4aa458a8ae4eb8b2645a27fe0c01392ecd08050fb689e2cf939a982fa097` |
| `configs/stage0-rerun-seed43.yaml` | `1c2336d8342198a417a129d3e70e7ce53609b1d28aff3fd021a92f8bd20360e6` |
| `configs/stage0-rerun-smoke.yaml` | `a4ec6fe1e34201204fa5f958efd63bb4a4ab4b38c358afc1905f50a846620f9a` |

`committed_config_set_sha256` remains
`e6e1fd53f93ec0b3059ff2da8eb9d27b92546b3d74fd7bffdbd0a11373a4e078`.
The source changed (full-pool validation selector); the configs did not.
This is a verified identical delta, not an unrecorded silence.

`run.log_every` is **not** in the differences table above because it does
**not** differ from the pilot: both the v2.0 pilot config and the Phase-50
graded configs carry `log_every: 50`. It is documented here anyway because it
is easy to misread: `configs/stage0-example.yaml`'s own un-modified default is
`log_every: 100`, and the Phase-50 graded configs deliberately override that
to `50` — matching the v2.0 pilot's literal, not the shipped example's — for
v2.0 protocol/config parity (`50-CONTEXT.md` D-02/D-05). Two facts must be
held simultaneously and neither may be dropped: (1) the value `50` is set for
protocol parity, and (2) the current training loop does not consume
`run.log_every` at all — `train.log.jsonl` step records are emitted every
step regardless of this field's value. The literal is therefore
**scientifically inert in this code state** and must never be described as
changing diagnostic resolution, logging density, or any other observable
training behavior. It enters no loss term, no optimizer state, no data-
selection path, and no gate threshold.
