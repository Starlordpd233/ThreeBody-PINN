# Phase 41 Gap Register

Phase-local record for source-silent decision points hit during Phase 41
(config, checkpointing, resume & determinism). Milestone-wide index:
`.planning/milestones/v2.0-GAPS.md`.

---

## GAP-41-01 — frozen_config_rng_recording_format (CTRL-08 config-side RNG carriage)

- **Decision point:** CTRL-08 / ROADMAP SC #4 / SPEC AC require the full
  seed/RNG state (four streams: `torch`, `torch_mps`, `numpy`,
  `python_random`) to be recorded on the frozen-config path AND in every
  checkpoint. CTRL-01 / CTX-51 simultaneously require the frozen
  `runs/<name>/config.yaml` to re-parse to an EQUAL `TrainingConfig`. The
  checkpoint half shipped in plans 41-02/-04; the SERIALIZATION
  REPRESENTATION for the config half was owner-carved and left
  `UNDECIDED` rather than invented.
- **Where in artifact:** `pinn/training/config.py` (`provisional_fields()`
  seam entry), `pinn/training/config_yaml.py` (`freeze_resolved_config`),
  `pinn/train.py` (composition root), surfaced as the single failed
  must-have in `41-VERIFICATION.md` (score 5/6, status `gaps_found`).
- **Task context:** Phase 41 execution (plans 41-01..05) and goal-backward
  verification of CTRL-08.
- **Classification:** process-artifact schema (artifact-layout /
  serialization representation; no physics content).
- **Source silence:** `41-SPEC.md` AC (line 64) pins the constraint ("frozen
  config and a checkpoint both contain all four RNG stream states") but not
  the representation; `.planning/REQUIREMENTS.md` CTRL-08 and ROADMAP SC #4
  likewise; the trainex-r1a decisions (D6, B-11) fix scope (statistical
  equivalence + exact continuation, never bitwise) but are silent on where
  the config-side record lives. Cross-AI review (cycle-2 HIGH) confirmed the
  A/B candidate space without ruling.
- **Mathematical / engineering grounding:** the four streams include
  `torch.get_rng_state()` (a ~5 KB ByteTensor), an optional MPS ByteTensor,
  numpy `bit_generator.state` (nested dict), and `random.getstate()` (a
  nested tuple of 625 ints). `capture_rng_state`'s contract is torch-native
  ("round-trips clean under `torch.save` / `torch.load(weights_only=True)`").
  (A) sidecar `_runtime_state` envelope inside `config.yaml` forces a SECOND
  serialization format (base64/int-list YAML encodings with new round-trip
  pitfalls), carves an exemption into `load_config`'s fail-closed
  unknown-top-level-key rejection, injects mutable runtime state into the
  artifact used for stable identity digests (41-05), and couples failure
  domains (a corrupt RNG write can render the run's config unloadable).
  (B) sibling `runs/<name>/run_start_rng.pt` reuses the exact tested
  checkpoint path (`capture_rng_state` + `atomic_io.atomic_write_torch`,
  read with `weights_only=True`), keeps `config.yaml` a pure
  `TrainingConfig` (CTRL-01 untouched), and isolates failure domains. The
  "single artifact travels with the config" argument for A is void: the unit
  that travels is `runs/<name>/`, which already contains `checkpoints/`.
- **Agent was tempted to:** implement B during execution (it is the
  engineering-consistent choice) — correctly withheld pending owner pick.
- **What the user needs to decide:** (A) sidecar `_runtime_state` envelope in
  `config.yaml` ignored by `load_config`, or (B) sibling
  `runs/<name>/run_start_rng.pt` plus the four streams every checkpoint
  already carries.
- **Confidence of impact:** HIGH — sole blocker on CTRL-08 / SC #4 and on
  closing Phase 41.
- **Status:** RESOLVED-WITH-INSTRUCTION (2026-07-18)
- **Resolution note:** owner delegated the pick 2026-07-18 ("You pick A or B
  for frozen_config_rng_recording_format. follow your best judgement and
  close this"). Under that delegation: **Option B** — `config.yaml` stays a
  pure `TrainingConfig`; `pinn.train` records the four run-start streams in
  `runs/<name>/run_start_rng.pt` via `determinism.record_run_start_rng`
  (same `capture_rng_state` + `atomic_write_torch` + `weights_only=True`
  representation as every checkpoint), written once at fresh launch, AFTER
  the strict-CPU runtime resolve (so a reseed is reflected) and on the same
  generator `RunController` consumes; `--resume` never overwrites the
  original run-start record. SPEC AC reading under representation B: the
  "frozen config" side of the four-stream assertion is satisfied by the
  frozen-config-side artifact `run_start_rng.pt` (the frozen `config.yaml`
  remains pure by design). The seam left `provisional_fields()` (it is
  decided, and the run-start log labels every listed entry provisional); the
  decision is carried by `config.FROZEN_CONFIG_RNG_RECORDING_FORMAT =
  "sibling-artifact:run_start_rng.pt"`, module docstrings, this record, and
  tests (`RunStartRngRecordTests`, `RngRecordedEverywhereTests`,
  `test_frozen_config_rng_recording_format_decided_option_b`). ERW triage:
  not ERW-grade (serialization/artifact layout; no physics content).
