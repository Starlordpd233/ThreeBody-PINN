---
phase: 40
slug: stage-0-curriculum-training-loop-fut-04
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: 2026-07-17
---

# Phase 40 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Register authored at plan time (all nine 40-0N-PLAN.md files carry a `<threat_model>`
> block); verified retroactively via `/gsd-secure-phase 40` at ASVS L1 (grep-depth),
> confirmed by direct inspection of the landed `pinn/training/` modules.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| `pinn/training/*` source ↔ codebase invariants | New training modules could reintroduce v1.3-era code paths or mutate global torch state, breaking the D1-p precision-switch contract and the `pinn/` live-code ban. | Module source (imports, global defaults) |
| checkpoint file ↔ `torch.load` / `load_state_dict` | A checkpoint that pickles arbitrary Python objects would enable code execution on load; RECOVER now consumes the rolled-back payload, so its contents reach `model.load_state_dict`. | Serialized model/optimizer/clipper state |
| config values ↔ tensor construction | Malformed/adversarial config (negative epochs, non-finite thresholds, λ_E>1, bad `energy_floor_factor`) must be rejected before any tensor is built or reaches the `eps_h` denominator. | `TrainingConfig` / `StageConfig` fields |
| loss / gradient / validation signals ↔ ADVANCE decision | A NaN/Inf slipping past the gate as an ADVANCE would silently advance a broken model or poison the run. | Non-finite float signals |
| stage index ↔ optimizer path | An out-of-slice stage (3–6) routed to a non-existent sL-BFGS implementation would silently deviate from the locked science. | Stage integer |
| caller RNG ↔ collocation sampler | Touching global RNG state would make runs non-reproducible and cross-contaminate other seeded components. | `torch.Generator` state |
| caller-supplied `stage_factory` ↔ live curriculum | An injected callable supplies the object composing the objective and holding the model for every stage ≥ 1; a foreign model would lose all prior training. | Model identity across stages |
| stage-exit disposition ↔ stage progression | Only an ADVANCE disposition may change the stage; HALT / RECOVER / max-epoch must never advance (no fallback advancement). | `StageDisposition` enum |
| provisional constants ↔ run behavior/record | Uncalibrated C-table / median-floor / λ^max / max_iter values could silently distort clipping or weighting, or be mistaken for ratified values. | Provisional numeric constants + provenance |
| second-order autograd ↔ 24 GB unified memory | A single full-batch `create_graph` L-BFGS graph can exceed M5 Pro memory. | Autograd graph size |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-40-01 | Tampering / EoP | `TrainingConfig`/`StageConfig` malformed values reaching `eps_h` | medium | mitigate | Frozen-dataclass `__post_init__` fail-closed validation; `_finite_positive("energy_floor_factor", …)` rejects non-finite/non-positive before any tensor is built; `+1e-12` additive floor guards the zero denominator (`config.py`). | closed |
| T-40-02 | Tampering / EoP | checkpoint deserialization via `torch.load` reaching `load_state_dict` | high | mitigate | `TorchSaveCheckpointStore` loads `weights_only=True` on every `load_latest`/`rollback` (`checkpoint.py:80,90`); CTX-44 plain-tensor/scalar payloads carry no callables/custom classes; asserted by `test_checkpoint`. | closed |
| T-40-03 | Denial of Service (run) | NaN/Inf gradient/loss reaching the ADVANCE gate | medium | mitigate | Single pinned mechanism: `torch.isfinite` gate returns `GradClipOutcome.non_finite=True` (no raise); RunController/StageExitMachine branch had_nan_inf → `StageDisposition.RECOVER` before any ADVANCE; `NonFiniteContractTests` binds both halves. | closed |
| T-40-04 | Tampering | new/edited module source (v1.3 import / global-default / clip-catch / exception-type drift) | medium | mitigate | `test_prohibitions` dynamic-discovery audit blocks the banned tokens over every landed `pinn/training/` module; re-run in every task's verify command. | closed |
| T-40-05 | Tampering / Repudiation | provisional constants (C-table / median-floor / λ^max / max_iter / thresholds) presented as ratified or left unrecorded | medium | mitigate | All provisional values carry spec provenance, are config-overridable, and are surfaced for ACC-05 calibration; a run-start log dumps the provisional set once per run (assertLogs-verified). | closed |
| T-40-06 | Tampering / Repudiation | sL-BFGS stage routing — silent entry into unimplemented stages 3–6 | medium | mitigate | `check_stage_preflight(k)` typed refusal blocks stage ≥ 3 loudly, invoked BEFORE any disposition/optimizer phase (`controllers.py:905`, `slbfgs_preflight.py:38`). | closed |
| T-40-07 | Tampering / EoP | (a) collocation sampler global-RNG mutation [low]; (b) 40-09 re-label of sL-BFGS silent stage entry [high] | high | mitigate | (a) caller-owned `Generator` enforced (`TypeError` on non-Generator); global RNG untouched, seed-stable. (b) same `check_stage_preflight` runs FIRST in `step()` before any factory call. | closed |
| T-40-08 | Denial of Service (memory) | second-order full-batch L-BFGS graph on 24 GB M5 Pro | medium | mitigate | Accumulate-in-closure sub-chunking with a config knob; ACC-02 smoke test calibrates the default. | closed |
| T-40-09 | EoP / Tampering | (a) spurious stage advance via CurriculumController fallback + forced-disposition seam [high]; (b) cross-plan M1 non-finite contract drift [medium] | high | mitigate | (a) only `StageDisposition.ADVANCE` increments k; the forced-disposition param raises typed `ForcedDispositionOnLiveRun` at construction (`controllers.py:781`) — one mechanism. (b) `NonFiniteContractTests` encodes the M1 contract once and audits both producer/consumer halves. | closed |
| T-40-10 | EoP / Denial of Service | (a) RECOVER against an empty CheckpointStore at cold start [high, DoS]; (b) new zero-headroom gate poll becoming a second ADVANCE path [medium, EoP] | high | mitigate | (a) run-start `stage-0-init` anchor + `except EmptyCheckpointStore` backstop (`controllers.py:951`) → record + HALT, Δstage=0, verified against a real empty store. (b) boundary poll calls the SAME `StageExitMachine.evaluate` four-criterion conjunction, falls back to HALT; mirror test asserts no fallback ADVANCE. | closed |
| T-40-11 | Tampering | `GradClipper.load_state_dict` dtype field newly read from the payload | medium | mitigate | dtype carried as a plain string, resolved through a 2-entry CLOSED `_NAME_TO_DTYPE` dict (`grad_clip.py:287`) that raises on any other value — never `eval`/`getattr`/serialized `torch.dtype`; payload stays weights_only-clean; asserted with a corrupted-dtype payload. | closed |
| T-40-12 | Tampering | `stage_factory` returning a controller on a FOREIGN model (silent loss of all prior training) | high | mitigate | `CurriculumController` verifies `stage_factory(k+1).model is` the held model and raises typed `StageFactoryModelMismatch` (`controllers.py:922`) before any rebind; spec-grounded weight-continuity invariant (40-SPEC R2). | closed |
| T-40-13 | Tampering | `stage-{k+1}-init` anchor saved from the wrong stage's controller | medium | mitigate | The stage swap precedes the anchor save, so the anchor carries the entered stage's λ^max caps; asserted twice (anchor-provenance AC via `save_spy.call_args_list`; composed RECOVER-path AC). | closed |
| T-40-SC | Tampering | package installs (npm/pip/cargo) | low | accept | No new packages introduced by Phase 40; torch/numpy already verified in the `pinn-train` env (RESEARCH Package Legitimacy Audit: not applicable). | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above `workflow.security_block_on` (high) count toward `threats_open`*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

**ID-reuse note:** IDs `T-40-07`, `T-40-09`, and `T-40-10` were each reused across plans
for a second component. Each row above lists both meanings and the highest severity of the
pair. One further variant of `T-40-03` appears in 40-08 (a converged/degenerate clipper
window collapsing the clip threshold), dispositioned **accept** — see the Accepted Risks Log.

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-40-01 | T-40-SC | No new npm/pip/cargo packages are introduced by Phase 40; torch/numpy are already present and verified in the `pinn-train` conda env. Supply-chain surface is unchanged. | Phase 40 plan authors (40-01) | 2026-07-17 |
| AR-40-02 | T-40-03 (40-08 variant) | A converged/degenerate clipper window collapsing the clip threshold is out of scope for WR-01; the §4.4 `median_floor` (CTX-36, default 1e-6) already keeps `clip_value` finite and nonzero and is preserved across the serialization round trip (asserted). | Phase 40 plan authors (40-08) | 2026-07-17 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-07-17 | 14 | 14 | 0 | /gsd-secure-phase (Claude Opus 4.8, ASVS L1) |

L1 mitigation confirmation (direct source inspection of the landed code):
- T-40-02 → `torch.load(..., weights_only=True)` at `checkpoint.py:80,90`
- T-40-09 → `raise ForcedDispositionOnLiveRun()` at `controllers.py:781`
- T-40-10 → `except EmptyCheckpointStore` backstop at `controllers.py:951`
- T-40-12 → `raise StageFactoryModelMismatch()` at `controllers.py:922`
- T-40-06 / T-40-07(b) → `check_stage_preflight(self._stage)` runs first in `step()` at `controllers.py:905`
- T-40-11 → closed `_NAME_TO_DTYPE` map at `grad_clip.py:287`

Both implementation SUMMARYs carrying `## Threat Flags` (40-07, 40-08) report **no new
threats** beyond the plan-time register; all landed mitigations remain in place.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-07-17
