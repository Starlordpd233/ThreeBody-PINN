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
