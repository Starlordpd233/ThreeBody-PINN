# Phase 60: Single-System Learnability - Pattern Map

**Mapped:** 2026-10-18
**Mapped against:** HEAD `0d0ec297` on `milestone/v2.4` (worktree `.worktrees/trainex`). Every `pinn/`, `tests/` and `.planning/` line number below was read at this HEAD, and the first and last line of the cited ranges were re-checked mechanically in two passes (ranges that ended on a blank line were tightened).
**Files analyzed:** 37 deliverable rows (9 code deliverables, 4 edits, 6 evidence-artifact classes, 18 test files)
**Analogs found:** 37 / 37 at file level (18 exact, 17 role-match, 2 partial). Ten sub-parts have no repository analog (see "No Analog Found").

Tracked-source gate (#3645): every analog path named in this file was checked with `git ls-files -- <path>` and printed non-empty, so each is tracked source. No `.gsd/capabilities` mirror path is named. Note that `runs/stage0-v23g7-seed42/**` is force-tracked although `runs/` is gitignored. No corpus file and no `splits.json` was opened while mapping; the only run metadata read was `runs/stage0-v23g7-seed42/training_metadata.json` (`s_h`, `eps_h`).

## How to use this map

1. Read "Shared Patterns" (S1-S9) first. S1 (three repository-wide scans plus a pinned allowlist), S2 (what must never be caught) and S6 (exclusive create) bind every plan.
2. Each assignment names one primary analog and says what to **copy**, what to **not copy**, and which test pattern proves it. Where a part has no analog it points to the `60-RESEARCH.md` finding or pattern that supplies it. Research code sketches are not repeated here because they are not repository code.
3. The right-hand column of the classification table names the final plan that creates each file (60-01 .. 60-23, the plan split as revised on 2026-10-18), followed by any later plan that modifies it. It no longer follows the draft numbering of `60-RESEARCH.md` "Recommended Plan and Wave Decomposition".
4. Tests are `unittest.TestCase` only. Several analog tests use pytest idioms or import pytest (see Hazard 2); convert `pytest.approx` to `assertAlmostEqual`, `pytest.raises` to `assertRaises`, `tmp_path` to `tempfile.TemporaryDirectory`.
5. Corrections to the brief that matter: the real-signal tests are in `tests/phase42/test_signals.py`, not `tests/phase41`; `tests/phase55/test_architecture_characterization.py` and `tests/phase56/test_gate04_train_free.py` cannot run under `unittest` in `pinn-train` because they `import pytest`.

## File Classification

| # | New/Modified File | Role | Data Flow | Closest Analog | Match | Plan |
|---|-------------------|------|-----------|----------------|-------|------|
| 1 | `pinn/verification/learnability_arms.py` | model + validator (closed arm catalog, omega provenance, override refusal) | transform (pure) | `pinn/verification/candidate_eligibility.py` + `pinn/verification/feasibility_scorecard.py` + `pinn/architecture_spec.py` | role-match | 60-01, 60-23 |
| 2 | `pinn/verification/learnability_data.py` | service (allowlist data seam, windowing, normalizer, preflight) | file-I/O (read-only) | `pinn/verification/baselines.py` + `pinn/verification/production_reference.py` | exact | 60-01, 60-23 |
| 3 | `pinn/verification/learnability_losses.py` | service (trainer-function composition, chunked physics step, frozen-monitor log) | transform (forward/backward, microbatched) | `pinn/training/controllers.py` microbatch step + `diag07_common.py::per_term_gradients` | exact | 60-01, 60-05 |
| 4 | `pinn/verification/learnability_run.py` | controller (budget driver, Adam, polish, scoring, cross-check, records, resume, signals) | batch + event-driven | `pinn/training/controllers.py::run_stage` family + `pinn/train.py` + `pinn/evaluate.py` claim | role-match | 60-01, 60-23, 60-08, 60-11, 60-12 |
| 5 | `pinn/verification/learnability_g2.py` | service (pure rules, skip writer, ruling loader) | transform + file-I/O | `pinn/verification/feasibility_scorecard.py` + `pinn/verification/candidate_eligibility.py` | role-match | 60-06 |
| 6 | `pinn/verification/diagnostic_architecture.py` | factory (omega override builder) | transform | `pinn/network.py::build_network` | exact | 60-23 |
| 7 | `pinn/verification/gate04_omega_remeasure.py` | CLI entry (D-07 re-measure) | batch | `pinn/verification/gate04_train_free.py::main` | role-match | 60-09 |
| 8 | `.planning/phases/60-single-system-learnability/evidence/launch_phase60_arm.py` (name is a suggestion) | launcher + supervisor | event-driven (process lifecycle) | `.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/launch_phase57_run.py` | exact | 60-07 |
| 9 | `.planning/phases/60-single-system-learnability/evidence/verify_phase60_evidence.py` | verifier CLI | batch | `.planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py` | exact | 60-13 |
| 10 | `pinn/verification/feasibility_scorer.py` (EDIT, 3 sites) | service (metrics) | transform | `.planning/phases/59-.../evidence/diag07/jx02_jx05.py::_cpu64` + `_network_trajectory` | exact | 60-02 |
| 11 | `pinn/verification/gate04_train_free.py` (EDIT, optional `first_omega_0`) | service (train-free gate) | transform | itself, plus row 6 | role-match | 60-09 |
| 12 | `verify_phase59_evidence.py` (EDIT) + `evidence/manifest.json` rewrite | verifier CLI | batch | itself, plus `evidence/scorecard-freeze.json` | exact | 60-04 |
| 13 | `.planning/REQUIREMENTS.md` (EDIT); `.planning/ROADMAP.md` (read only: criterion 3 is already verbatim, so 60-03 checks it and does not edit it) | planning documents | docs | themselves; target text is in `60-SPEC.md` "Amendment text" | exact | 60-03 |
| 14 | `evidence/scorer-successor.json` | pinned record | file-I/O | `evidence/scorecard-freeze.json` (Phase 59) | exact | 60-02 |
| 15 | `60-RUN-PROTOCOL.md` + `evidence/run-protocol.json` | pre-registration pair | file-I/O | `59-SCORECARD.md` + `evidence/scorecard-freeze.json` | exact | 60-13 |
| 16 | `evidence/preflight/records.json` | preflight manifest | file-I/O | `baselines/files_opened.json` + `audit/reader_acceptance.json` (Phase 59) | role-match | 60-13 |
| 17 | `60-CHECKPOINT-4-RULING.md` (continue path only) | owner ruling | file-I/O | `.planning/phases/57-.../57-RULING.md` | role-match | 60-17 |
| 18 | `evidence/arms/<arm-id>/{record.json, adam.weights, polish.weights}` | run record + weights | file-I/O | Phase 59 baselines payloads + `generation-7-timing-calibration.json` + `evaluate.py` claim | role-match | 60-14, 60-15, 60-16, 60-20, 60-21 |
| 19 | `evidence/g2/{g2-outcome.json, sweep-curve.json, skip-records.json}` | outcome records | file-I/O | Phase 59 baselines payload conventions | role-match | 60-14, 60-15, 60-18 |
| 20 | `tests/phase60/__init__.py` | test scaffold | - | `tests/phase59/__init__.py` | exact | 60-01 |
| 21 | `tests/phase60/test_amendment.py` | test (document contract) | file-I/O | `tests/phase56/test_spec_amendment_contract.py` + `tests/phase59/test_scorecard.py` | role-match | 60-03 |
| 22 | `tests/phase60/test_scorer_mps.py` | test (unit + static) | transform | `tests/phase59/test_diag07_panels.py::NetworkScoreTests` + `tests/phase59/test_scorer_network.py` | exact | 60-02 |
| 23 | `tests/phase60/test_arm_spec.py` | test (unit) | transform | `tests/phase59/test_scorecard_rules.py` | role-match | 60-23 |
| 24 | `tests/phase60/test_data_seam.py` | test (unit) | file-I/O | `tests/phase59/test_split_allowlist.py` + `tests/phase59/_corpus_fixtures.py` | exact | 60-23 |
| 25 | `tests/phase60/test_run_short.py` | test (integration) | batch | `tests/phase38/test_overfit_probe.py` + `tests/phase43/test_evaluate_gate.py` single-use tests | role-match | 60-01 |
| 26 | `tests/phase60/test_losses_trainer_functions.py` | test (unit) | transform | `tests/phase55/test_architecture_characterization.py:283-320` + `tests/phase57/_fixtures.py::build_run_controller` + `jx01_jx10.py::_trainer_cross_check` | exact (composite) | 60-05 |
| 27 | `tests/phase60/test_refusals.py` | test (integration) | request-response | `tests/phase43/test_evaluate_edge_cases.py` + `tests/phase41/test_checkpoint.py` | role-match | 60-23 |
| 28 | `tests/phase60/test_verifier_successor.py` | test (synthetic git repo) | batch | `tests/phase59/test_evidence_verifier.py` | exact | 60-04 |
| 29 | `tests/phase60/test_schedule.py` | test (unit) | transform | `tests/phase40/test_optimizer_phase.py:301-320, 417-451` | partial | 60-08 |
| 30 | `tests/phase60/test_gate04_remeasure.py` | test (unit) | batch | `tests/phase57/test_gate_and_evaluation.py` (runnable) + `tests/phase56/test_gate04_train_free.py` (pytest, not runnable) | partial | 60-09 |
| 31 | `tests/phase60/test_budget_driver.py` | test (unit) | request-response | `tests/phase59/test_scorecard_rules.py` | role-match | 60-08 |
| 32 | `tests/phase60/test_preflight.py` | test (unit) | file-I/O | `tests/phase59/test_split_allowlist.py::RefusalPrecedesIOTests` + `_corpus_fixtures.py` | role-match | 60-23 |
| 33 | `tests/phase60/test_resume.py` | test (integration) | event-driven | `tests/phase41/test_controllers_ext.py:262-375` + `tests/phase42/test_signals.py` | role-match | 60-12 |
| 34 | `tests/phase60/test_g2.py` | test (unit) | transform | `tests/phase59/test_scorecard_rules.py` | exact | 60-06 |
| 35 | `tests/phase60/test_protocol_records.py` | test (unit) | file-I/O | `tests/phase59/test_evidence_io.py` | role-match | 60-11 |
| 36 | `tests/phase60/test_static_guards.py` | test (AST + subprocess) | batch | `tests/phase59/test_static_guards.py` | exact | 60-01 |
| 37 | `tests/phase60/test_launcher.py` | test (process lifecycle) | event-driven | `tests/phase57/test_phase57_launcher.py` | exact | 60-07 |

Evidence-path rule for rows 14-19: every committed path stays under `.planning/phases/60-single-system-learnability/`, with no segment named `runs`, `tmp`, `outputs` or `scratch` (`scripts/git_policy/validate_staged_paths.py:11-27`). Weights use the non-ignored extension `.weights`; `*.pt`, `*.pth`, `*.ckpt`, `*.pkl`, `*.npz`, `*.npy` and `*.log` are gitignored (`.gitignore:146-158, 197, 263`). Phase 59 shows the consequence for logs: 50 tracked files against 61 on disk under its evidence tree, because `.log` files are not tracked.

---

## Pattern Assignments

### 1. `pinn/verification/learnability_arms.py` (model + validator, transform)

**Analog:** `pinn/verification/candidate_eligibility.py` for module shape and "accept only the literal value"; `pinn/verification/feasibility_scorecard.py` for the owner-routed exception style; `pinn/architecture_spec.py` and `pinn/loss_catalog.py::LossWeights` for frozen-dataclass fail-closed validation; `pinn/verification/split_allowlist.py` for "refuse before any path exists".

**Closed constants and a projection that trusts only the literal** (`candidate_eligibility.py:25-31`, `45, 53-57`, docstring trimmed):
```python
CANDIDATE_ORDER: tuple[int, ...] = (42, 41, 43)
REQUIRED_STRUCTURAL_FACTS: tuple[str, ...] = (
    "eval01_precondition_i",
    "guard_invariant_rule",
    "finished",
    "eval01_precondition_iii",
)

def structural_facts(record: Mapping[str, Any]) -> dict[str, bool]:
    if not isinstance(record, Mapping):
        raise TypeError(f"candidate record must be a mapping; got {type(record).__name__}")
    facts = {name: record.get(name) is True for name in REQUIRED_STRUCTURAL_FACTS}
    facts["eligible"] = all(facts.values())
    return facts
```
Use the same shape for the closed arm-id enumeration (rung, system, record keys, loss arm, omega provenance in {locked, g2_sweep_override, confirmation_override, owner_approved}, LR stage, clip stage). Free-form ids and paths are refused.

**Frozen dataclass that names the offending field and the source of the lock** (`pinn/loss_catalog.py:136-173`, trimmed):
```python
@dataclass(frozen=True)
class LossWeights:
    lambda_data: float = 1.0
    ...
    def __post_init__(self) -> None:
        ...
        for name, value in fields:
            try:
                finite = math.isfinite(float(value))
            except (TypeError, ValueError):
                finite = False
            if not finite or float(value) < 0.0:
                raise ValueError(
                    f"LossWeights.{name} must be finite and non-negative; "
                    f"got {value!r} ..."
                )
        if float(self.lambda_data) != 1.0:
            raise ValueError(
                f"LossWeights.lambda_data must be 1.0 (pinn_architecture.md §3.1 "
                f"unweighted data term); got {self.lambda_data!r}"
            )
```
`LossWeights` is also the reason Rung 2a cannot be expressed as `lambda_data = 0` (see row 3).

**The omega lock that makes a separate builder necessary** (`pinn/architecture_spec.py:119-124`):
```python
        if self.first_omega_0 != SIREN_FIRST_OMEGA_0:
            raise ValueError(
                f"ArchitectureSpec.first_omega_0 must be {SIREN_FIRST_OMEGA_0} "
                f"(got {self.first_omega_0!r}); sourced from pinn.constants "
                "(pinn_architecture.md §2.2/§2.4 ARCH-01)"
            )
```
INST-05(e) is enforced in `learnability_arms.py` (provenance and arm kind), never by loosening this check.

**Refuse before any path exists; arms hold a `RecordKey`, never a path** (`pinn/verification/split_allowlist.py:58-59`, `188-194`):
```python
class SplitRefused(PermissionError):
    """A key is withheld or unknown. Raised before any corpus path is built."""

    def require(self, key) -> str:
        """Return ``train`` or ``validation``. Refuse before any path exists."""
        physical = _physical_key(key)
        split = self.split_of.get(physical)
        if split not in _ALLOWED_SPLITS or physical in self.withheld:
            raise SplitRefused(f"{_REFUSAL}: {physical.variant} id {physical.id}")
        return split
```

**Do not copy:** an exception class whose name starts with `Test` (pytest collection, 59-PATTERNS hazard 9). Name the new owner-routed exceptions `OverrideRefused`, `CrossCheckDisagreement`, and so on.
**Sketch source:** `60-RESEARCH.md` "Override refusal (INST-05(e)) and sweep rule" and Pattern 2.
**Tests:** row 23.

---

### 2. `pinn/verification/learnability_data.py` (service, file-I/O read-only)

**Analog:** `pinn/verification/baselines.py` (it already opens the allowlist, installs the attestation, recovers the normalizer and windows records) and `pinn/verification/production_reference.py` (it already turns an admitted read into a reference with raw IC13). Copy the structure, not the Phase 59 constants.

**Imports** (`baselines.py:27-56`, trimmed to what the seam needs):
```python
from pinn.constants import T_CHARACTERISTIC_TIME
from pinn.data.preprocessing import normalize_ic13
from pinn.verification import evidence_io, split_allowlist
from pinn.verification.feasibility_scorecard import SCORECARD_SHA256, load_scorecard
from pinn.verification.production_reference import (
    load_reference,
    load_retained_checkpoint,
    recover_normalizer_from_checkpoint,
    stats_digest,
)
from pinn.verification.split_allowlist import (
    GENERATION7_SPLITS_REL,
    AllowlistedCorpusReader,
    SplitAllowlist,
    expected_splits_sha256,
    install_open_attestation,
    resolve_data_root,
)
```
Do not import `BRUTUS_FOLDER_TABLE`, `parse_brutus_file` or `parse_brutus_text`: the Phase 59 guard `corpus_token_violation` (`tests/phase59/test_static_guards.py:249-260`) bans them in every Phase 59 module outside `split_allowlist.py`, and the Phase 60 static guard (row 36) should apply the same ban to the Phase 60 modules; scan A (S1) separately bans the folder-name tokens. Build keys as `RecordKey("hierarchical", "gold", 1632)` (`pinn/data/types.py:126-131`).

**Open context: hash-checked allowlist, process-global attestation, reader** (`baselines.py:177-193`):
```python
def _open_context(args):
    scorecard = load_scorecard()
    allowlist = SplitAllowlist.from_manifest(
        _REPO_ROOT / GENERATION7_SPLITS_REL,
        expected_sha256=expected_splits_sha256(_REPO_ROOT),
    )
    data_root, source = resolve_data_root(args.data_root)
    attestation = install_open_attestation(
        data_root=data_root,
        data_root_source=source,
        withheld_basenames=allowlist.withheld_basenames(),
        split_by_basename=allowlist.split_by_basename(),
    )
    reader = AllowlistedCorpusReader(
        allowlist=allowlist, data_root=data_root, data_root_source=source,
    )
    return scorecard, allowlist, reader, attestation, data_root, source
```
Record the `source` label, never `data_root` (`evidence_io.guard_redaction`, S3).

**Window every record to the scored horizon** (`baselines.py:108-116`). This is the guard against the 1,002nd gold snapshot (t = 10.01):
```python
def _window(reference, t_max):
    """Times, positions and velocities with t <= t_max (+1e-9)."""
    times = np.asarray(reference.times, dtype=np.float64).reshape(-1)
    keep = times <= float(t_max) + 1e-9
    return (
        times[keep],
        np.asarray(reference.positions, dtype=np.float64)[keep],
        np.asarray(reference.velocities, dtype=np.float64)[keep],
    )
```
with `t_max` read from the scorecard (`baselines.py:119-120`: `float(scorecard.section("scoring_grid")["t_max"])`). Assert the counts 1,001 (gold), 126 (hierarchical base) and 59 (standard base) in the preflight, per `60-RESEARCH.md` Finding G.

**Real normalized IC13, fail closed on a digest difference** (`baselines.py:321-333`):
```python
def _recover_normalizer(reader, scorecard):
    payload, _provenance = load_retained_checkpoint(
        _REPO_ROOT, _RUN_NAME, _INIT_FILE, expected_step=0,
    )
    tolerance = float(scorecard.section("diag07")["tolerances"]["normalizer_recovery_max_abs"])
    recovered = recover_normalizer_from_checkpoint(reader, payload, tolerance=tolerance)
    del payload
    digest = stats_digest(recovered["stats"])
    audit = json.loads((_REPO_ROOT / _AUDIT_REL).read_text(encoding="utf-8"))
    expected = audit["normalizer"]["stats_sha256"]
    if digest != expected:
        raise BaselinesHalt(f"normalizer stats_sha256 {digest} != audit {expected}")
    return recovered["stats"], digest
```
The constants it needs are at `baselines.py:64-72` (`_RUN_NAME = "stage0-v23g7-seed42"`, `_INIT_FILE = "stage-0-init.pt"`, `_AUDIT_REL`, `_R_REF_ARTIFACT`). Raise a Phase 60 halt, not `BaselinesHalt`. The expected digest is `77526e53...79f6` (GAP-60-13).

**Which array is the data-term target.** The monitor-reproduction proof compares the trainer's `targets` with the windowed `reference.positions` row (`production_reference.py:347-350`):
```python
        snapshot = int(matches[0])
        reference_position = _cast_float32(reference.positions[snapshot]).reshape(-1)
        if not torch.equal(reference_position, targets[index].reshape(-1)):
            mismatches_targets += 1
```
So targets are the windowed `reference.positions` (float32), times `u = t / T_CHARACTERISTIC_TIME`, and the network input is `[2u - 1, normalize_ic13(raw_ic13, stats)]` (the closure shape in row 3).

**Data-points stand-in.** `accumulate_chunked_data_term` reads only `.tau_ic13`, `.masses`, `.targets`, so a `types.SimpleNamespace` is enough (used at `tests/phase40/test_optimizer_phase.py:742`); the real container is `pinn/data/types.py:284-295` (`DataFidelityPoints`).

**Preflight** (SPEC R8) per assigned key: `allowlist.require`, `reader.exists`, `reader.read` (raises `NotAdmitted` at `split_allowlist.py:287-288`), snapshot count above zero, window count as above. The nearest existing shape is `production_reference.py:374-387`:
```python
def allowlisted_file_presence(reader, allowlist):
    counts = {}
    for split in ("train", "validation"):
        for variant in ("hierarchical", "standard"):
            for fidelity in ("base", "gold"):
                keys = allowlist.records(
                    split, variant=variant, fidelity=fidelity
                )
                existing = sum(1 for key in keys if reader.exists(key))
                counts[f"{split}/{variant}/{fidelity}"] = {
                    "manifest": len(keys),
                    "existing": existing,
                }
    return counts
```
A miss blocks that arm with no substitute fidelity or system.

**Do not copy:** `AdmittedSetAdapter` or `_build_admitted_sources` (parse every file of every split, including test; Phase 59 guard `_FORBIDDEN_NAMES`, `test_static_guards.py:41-48`); `fallback_normalizer_from_allowlist` (`production_reference.py:286-307`, a recorded deviation, never silent); `target_frame_probe._build_control_reader` (globs folders); a second `install_open_attestation` for a different root (raises, `split_allowlist.py:366-371`).
**Tests:** rows 24 and 32.

---

### 3. `pinn/verification/learnability_losses.py` (service, transform; the INST-05(a) mutation target)

**Analog:** `pinn/training/controllers.py` (the loss path the harness must call, composed not copied) and `diag07_common.py::per_term_gradients` (the one place that already recomposes the same functions outside the controller, `diag07_common.py:504-600`). The controller methods read `self._model`, `self._dtype`, `self._device`, `self._r_ref`; the harness versions take them as explicit arguments so a test can feed both implementations the same tensors.

**Imports: bare names at module scope, so `mock.patch.object(harness_module, "<name>")` moves the output** (`controllers.py:89-98`):
```python
from pinn.loss_catalog import (
    LossTerms,
    angular_momentum_loss,
    causal_physics_loss,
    compose_total,
    data_huber_loss,
    ic_anchor_loss,
    soft_energy_loss,
)
from pinn.physics_residual import componentwise_du, softened_acceleration
```
plus `from pinn.training.controllers import accumulate_chunked_data_term, _RATIFIED_N_BINS, _bin_index_for_times` (the same private-helper import `diag07_common.py:518` makes) and `from pinn.data.batches import _stratified_full_slot_rows`.

**The trajectory closure** (`controllers.py:1091-1095`; identical to `feasibility_scorer.py:365-369`):
```python
        def traj(u_scalar: torch.Tensor) -> torch.Tensor:
            tau = (2.0 * u_scalar - 1.0).reshape(1)
            tau_ic13 = torch.cat([tau, ic13], dim=0).unsqueeze(0)
            pos = self._model(tau_ic13, masses_t.unsqueeze(0))
            return pos.reshape(3, 3)
```

**Data term** (`controllers.py:1148-1152`) and **IC term** (`controllers.py:1857-1865`, first lines):
```python
    def _data_term(self, data_points) -> torch.Tensor:
        pred = self._model(data_points.tau_ic13, data_points.masses)
        pred_pos = pred.reshape(-1, 3, 3)
        true_pos = data_points.targets.reshape(-1, 3, 3)
        return data_huber_loss(pred_pos, true_pos, dtype=self._dtype, device=self._device)

        zero_u = torch.zeros((), dtype=self._dtype, device=self._device)
        pred_r0 = anchor_ctx.traj(zero_u)
        first0, _second0 = componentwise_du(anchor_ctx.traj, zero_u)
        pred_v0 = first0.reshape(3, 3)
        ic_term = ic_anchor_loss(
            pred_r0, anchor_ctx.true_r0, pred_v0, anchor_ctx.true_v0,
            dtype=self._dtype, device=self._device,
        )
        data_term = self._data_term(batch.data_points)
```
Rung 2a has no data term but `LossWeights.__post_init__` rejects `lambda_data != 1.0` (`loss_catalog.py:169-173`). Do not evaluate the data term and pass `torch.zeros((), dtype=dtype, device=device)` for `terms["data"]` to `compose_total` (`loss_catalog.py:467-494` requires all five keys).

**One microbatch of physics rows** (`controllers.py:1746-1770`, docstring trimmed):
```python
    def _collocation_chunk_raw(
        self, anchor_ctx: _AnchorContext, times_chunk_np: np.ndarray,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        u_leaf = torch.as_tensor(
            times_chunk_np / T_CHARACTERISTIC_TIME, dtype=self._dtype, device=self._device,
        )
        first, second = componentwise_du(anchor_ctx.traj, u_leaf)
        positions = torch.func.vmap(lambda s: anchor_ctx.traj(s).reshape(-1))(u_leaf)
        positions = positions.reshape(-1, 3, 3)
        velocities = first.reshape(-1, 3, 3)
        accel = second.reshape(-1, 3, 3)
        force = softened_acceleration(
            positions, anchor_ctx.masses, dtype=self._dtype, device=self._device,
        )
        residual = accel - force
        rbar = (residual ** 2).sum(dim=(-2, -1)) / 3.0
        return positions, velocities, rbar
```

**Pass 1: frozen causal weights without retaining a parameter graph** (`controllers.py:1772-1820`, docstring trimmed):
```python
    def _adam_frozen_causal_weights(
        self, anchor_ctx: _AnchorContext, *, microbatch_size: int,
    ) -> tuple[dict[str, Any], torch.Tensor]:
        times_np = anchor_ctx.collocation_times
        n_total = int(times_np.shape[0])
        if microbatch_size <= 0:
            raise ValueError(f"microbatch_size must be positive; got {microbatch_size!r}")
        bin_sums = torch.zeros(_RATIFIED_N_BINS, dtype=self._dtype, device=self._device)
        bin_counts = torch.zeros(_RATIFIED_N_BINS, dtype=self._dtype, device=self._device)
        start = 0
        while start < n_total:
            end = min(start + microbatch_size, n_total)
            chunk_times_np = times_np[start:end]
            positions_chunk, velocities_chunk, rbar_chunk = self._collocation_chunk_raw(
                anchor_ctx, chunk_times_np,
            )
            rbar_chunk = rbar_chunk.detach().clone()
            times_tensor_chunk = torch.as_tensor(
                chunk_times_np, dtype=self._dtype, device=self._device,
            )
            bin_idx_chunk = _bin_index_for_times(
                times_tensor_chunk, n_bins=_RATIFIED_N_BINS, t_max=T_CHARACTERISTIC_TIME,
            )
            bin_sums = bin_sums.index_add(0, bin_idx_chunk, rbar_chunk)
            bin_counts = bin_counts.index_add(0, bin_idx_chunk, torch.ones_like(rbar_chunk))
            del positions_chunk, velocities_chunk, rbar_chunk, bin_idx_chunk, times_tensor_chunk
            self._release_chunk_memory()
            start = end
        raw_bin_means = bin_sums / bin_counts.clamp(min=1.0)
        bin_centres = (
            torch.arange(_RATIFIED_N_BINS, dtype=self._dtype, device=self._device)
            + torch.as_tensor(0.5, dtype=self._dtype, device=self._device)
        ) / _RATIFIED_N_BINS * T_CHARACTERISTIC_TIME
        _discard_loss, phys_details = causal_physics_loss(
            raw_bin_means, r_ref=self._r_ref, times=bin_centres,
            dtype=self._dtype, device=self._device, return_details=True,
        )
        return phys_details, bin_counts.detach()
```

**Pass 2: backward each chunk with a constant row weight** (`controllers.py:1895-1951`):
```python
        times_np = anchor_ctx.collocation_times
        n_total = int(times_np.shape[0])
        phys_total = torch.zeros((), dtype=self._dtype, device=self._device)
        energy_total = torch.zeros((), dtype=self._dtype, device=self._device)
        angmom_total = torch.zeros((), dtype=self._dtype, device=self._device)
        start = 0
        while start < n_total:
            end = min(start + microbatch_size, n_total)
            chunk_times_np = times_np[start:end]
            positions_chunk, velocities_chunk, rbar_chunk = self._collocation_chunk_raw(
                anchor_ctx, chunk_times_np,
            )
            times_tensor_chunk = torch.as_tensor(
                chunk_times_np, dtype=self._dtype, device=self._device,
            )
            bin_idx_chunk = _bin_index_for_times(
                times_tensor_chunk, n_bins=n_bins, t_max=T_CHARACTERISTIC_TIME,
            )
            row_weight_chunk = (
                w_n[bin_idx_chunk]
                / (float(n_bins) * r_ref * bin_counts[bin_idx_chunk])
            )
            phys_chunk = (row_weight_chunk * rbar_chunk).sum()
            chunk_frac = float(end - start) / float(n_total)
            energy_chunk = chunk_frac * soft_energy_loss(
                positions_chunk, velocities_chunk, anchor_ctx.h0, anchor_ctx.eps_h,
                masses=anchor_ctx.masses, dtype=self._dtype, device=self._device,
            )
            angmom_chunk = chunk_frac * angular_momentum_loss(
                positions_chunk, velocities_chunk, anchor_ctx.l0,
                masses=anchor_ctx.masses, dtype=self._dtype, device=self._device,
            )
            weighted_chunk = (
                weights.lambda_phys * phys_chunk
                + weights.lambda_e * energy_chunk
                + weights.lambda_l * angmom_chunk
            )
            weighted_chunk.backward()
            phys_total = phys_total + phys_chunk.detach()
            ...
            self._release_chunk_memory()
            start = end
```
Order matters for gradient equality with the oracle: Pass 1, then `(data_scaled + ic_scaled).backward()` (`controllers.py:1886-1893`), then the chunk loop. With a single system repeated 256 times, `bin_counts` is 256 in every bin. In the harness, energy and angular momentum are evaluated only when their ramped weight is above zero (k = 4 and 6 probe arms); at k = 0 the controller multiplies them by zero, so skipping them leaves the gradient equal.

**One 4096-row stratified draw** (`pinn/data/batches.py:348-366`); call it with `[key] * 256` and the seed-42 numpy stream. `sample_collocation_points` is the wrong level: it requires a hierarchical base key and a source (`batches.py:448-456`):
```python
def _stratified_full_slot_rows(
    record_keys: Sequence[RecordKey],
    *,
    rng: np.random.Generator,
    n_bins: int = RATIFIED_N_BINS,
    t_max: float = T_CHARACTERISTIC_TIME,
) -> list[tuple[RecordKey, float]]:
    rows: list[tuple[RecordKey, float]] = []
    for bin_id in range(n_bins):
        for key in record_keys:
            rows.append((key, _uniform_time_in_bin(rng, bin_id, n_bins=n_bins, t_max=t_max)))
    return rows
```
Sort the drawn times ascending before use (`controllers.py:1131-1132`).

**Frozen-monitor log at readings only (D-06)** (`controllers.py:1047-1068`): one frozen 4096-row set drawn before step 1, evaluated through the chunked Pass 1 above, never through a 4096-row `_non_data_terms`:
```python
        phys_details, _bin_counts = self._adam_frozen_causal_weights(
            anchor_ctx, microbatch_size=int(self._config.opt.adam_microbatch_size),
        )
        w_n = phys_details["w_n"]
        w_n_list = w_n.tolist()
        stats = {
            "w_n_stats": {
                "w_min": float(w_n.min()),
                "w_mean": float(w_n.mean()),
                "w_max": float(w_n.max()),
                "front_idx": max(
                    [n for n, w in enumerate(w_n_list) if w > 0.5], default=-1,
                ),
            },
            "residuals_per_bin": [float(r) for r in phys_details["rbar"].tolist()],
            "raw_residuals_per_bin": [
                float(r) for r in phys_details["raw_rbar"].tolist()
            ],
            "r_ref": float(phys_details["r_ref"]),
```

**Memory release between chunks** (`controllers.py:1739-1744`; the reason is the docstring at 1703-1738). Generation-0 only; no `is_available`:
```python
        gc.collect(0)
        if self._device.type == "mps" and hasattr(torch, "mps"):
            try:
                torch.mps.empty_cache()
            except Exception:
                pass
```

**Polish data term:** import `accumulate_chunked_data_term` and call it with `chunk_size=1024` (`OptConfig.lbfgs_chunk_size`, `config.py:672`); do not copy its body (`controllers.py:577-621`). The polish closure for physics arms must use the Pass-2 chunk loop with the frozen `w_n`, frozen rows and `scheduled_weights.freeze()` weights, never the trainer's 4096-row `_weighted_non_data_terms` (the 1.5 to 22.8 GB failure, `controllers.py:1724-1732`).

**Do not copy:** `_non_data_terms` (`controllers.py:1154-1263`, unchunked 4096 rows, writes `self._last_widened_details`); `_compose_loss_terms`; `RunController` state; `sample_collocation_points`; `PlateauDetector` or any stage-exit disposition (D-06: no self-halt).
**Tests:** row 26 (mutation, identity, oracle equivalence, chunk bound), row 29 (clip and schedule).

---

### 4. `pinn/verification/learnability_run.py` (controller, batch + event-driven)

**Analog:** `pinn/training/controllers.py::run_stage` and its Adam and L-BFGS phases for loop shape; `pinn/train.py` for signal wiring and the stop checkpoint; `pinn/evaluate.py` for the single-use claim. This module is deliberately a thinner loop and does not enter the production loop.

**(a) Pre-import capture of the MPS fallback variable** (`overfit_probe.py:16-19`; the module docstring must begin "Phase 60", not "Phase 59"):
```python
# Capture before Torch import — Phase 37 probe grammar.
import os as _os

_PRE_IMPORT_FALLBACK = _os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK") or None
```
Record the captured value in every record. The convention is that the MPS arm never inherits the variable (`scripts/run_precision_probe.py:117-127`, `env.pop("PYTORCH_ENABLE_MPS_FALLBACK", None)`).

**(b) Budget driver.** Every branch is a return value of a frozen function in `feasibility_scorecard.py`: `steps_budget` (779-799), `scoring_cadence_ok` (842-865), `budget_outcome` (814-839), `polish_should_stop` (868-888), `better_state` (894-906), `tier_of` (595-617), `counts` (684-703). The call that raises an owner stop is not to be wrapped (`feasibility_scorecard.py:833-836`):
```python
    if best_ref is None or best_final is None or best_ref == 0.0:
        raise OwnerRouted(
            "improvement rate is not determinable without a finite reference-window reading"
        )
```
Sketch source: `60-RESEARCH.md` Finding C and "Budget driver using only the frozen functions". Divergence (GAP-60-06) ends the Adam phase and skips `budget_outcome`; record `diverged_at_step`.

**(c) Adam loop: construction, resume offset, step order** (`controllers.py:2634-2663`):
```python
        optimizer = torch.optim.Adam(
            self._model.parameters(),
            lr=cfg.opt.lr_for_stage(k),
            betas=cfg.opt.adam_betas,
            eps=cfg.opt.adam_eps,
        )
        ...
        adam_start = 0
        scheduler_last_epoch = -1
        ...
        if resume_phase == "2a":
            adam_start = max(0, min(resume_epoch, n_adam_k))
            scheduler_last_epoch = adam_start - 1
        ...
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=max(n_adam_k, 1), last_epoch=scheduler_last_epoch,
        )

        self._grad_clipper.clear()
        self._scheduled_weights.rewarm()
```
Per step (`controllers.py:2060, 2092`, finite checks and update `2131-2163`, trimmed):
```python
            optimizer.zero_grad(set_to_none=True)
            ...
            clip_outcome = self._grad_clipper.clip(self._model.parameters(), stage=k)
            ...
            if not self._loss_finite(loss_terms.total):
                state["disposition"] = StageDisposition.RECOVER
                ...
                return handoff_trigger, adam_epochs_used
            if clip_outcome.non_finite:
                state["disposition"] = StageDisposition.RECOVER
                ...
                return handoff_trigger, adam_epochs_used

            optimizer.step()
            scheduler.step()
```
Harness differences: `lr = OptConfig().lr_for_stage(k)` (`config.py:705-707`), k = 0 for data-only arms (D-04), k = 4 and 6 for the probe Rung-2b arms; check the loss and the clip outcome before `optimizer.step()`; on a non-finite value skip that step and end Adam (GAP-60-06) instead of returning `RECOVER`; no `PlateauDetector` handoff (D-06). The D-03 second cosine is not in the trainer: reset `group["lr"] = group["initial_lr"]` and construct a new `CosineAnnealingLR` on the same optimizer (`60-RESEARCH.md` Finding B and its code example; verified there). `GradClipper.clip(params, stage=...)` returns `GradClipOutcome` with `non_finite`, `clip_value`, `total_norm` (`pinn/training/grad_clip.py:104-123, 208-264`); table `DEFAULT_C_STAGE_TABLE = {0: 8.5, ..., 4: 3.0, ..., 6: 3.0}` at `grad_clip.py:91`.

**(d) Polish loop: freeze, fresh L-BFGS, one outer call per `step(closure)`** (`controllers.py:2435-2448`, `2456-2484`, trimmed):
```python
        self._scheduled_weights.freeze()
        weights_frozen = self._scheduled_weights.current(0)
        fixed_batch, anchor_ctx, _frozen_causal_weights = self._start_lbfgs_segment(
            k, lbfgs_start=int(lbfgs_start),
        )

        optimizer = torch.optim.LBFGS(
            self._model.parameters(),
            history_size=cfg.opt.lbfgs_history_size,
            max_iter=cfg.opt.lbfgs_max_iter,
            line_search_fn=cfg.opt.lbfgs_line_search,
        )
        ...
        for _lbfgs_epoch in range(int(lbfgs_start), remaining_budget):
            if self._should_stop is not None and self._should_stop():
                self._scheduled_weights.rewarm()
                return StageDisposition.HALT
            ...
            try:
                optimizer.step(closure)
            except _StopRequested:
                self._scheduled_weights.rewarm()
                return StageDisposition.HALT
            epoch_count += 1
            ...
                self._lbfgs_segment_state["outer_calls"] = int(
                    self._lbfgs_segment_state.get("outer_calls", 0)
                ) + 1
```
The closure zeroes grads, accumulates the chunked data term, adds the non-data backward, returns the detached total and flags non-finite loss or gradient (`controllers.py:2361-2421`). The stop seam is an exception derived from `BaseException` raised between closure evaluations (`controllers.py:114-115`, `2368-2369`):
```python
class _StopRequested(BaseException):
    """Abort an in-progress L-BFGS step at the next closure evaluation."""

            if self._should_stop is not None and self._should_stop():
                raise _StopRequested
```
Harness differences: `lbfgs_max_iter` is 50, history 10, strong Wolfe, read from the scorecard (`feasibility_scorecard_v1.json` `lbfgs_polish`); `OptConfig.lbfgs_max_iter` defaults to 20 (`config.py:669`) and must not be used. Improvement is the closure objective strictly below the best so far, the polish state is the final iterate (GAP-60-05), and `polish_should_stop` is evaluated between outer calls with Adam wall time summed across segments.

**(e) Scoring: official gold grid plus the base grid beside it** (`baselines.py:134-174`, the pattern for both grids; for a network call `score_network`, `feasibility_scorer.py:439-482`):
```python
    times, positions, velocities = _window(gold_reference, t_max)
    ...
    result = score_trajectory(
        predicted, predicted_v, positions, masses, inner_pair, times,
        velocity_source="analytic", scorecard=scorecard, grid="gold",
    )
    ...
    if base_reference is not None:
        base_times, base_positions, _base_v = _window(base_reference, t_max)
        ...
        base_result = score_trajectory(
            base_predicted, base_predicted_v, base_positions, masses, inner_pair, base_times,
            velocity_source="analytic", scorecard=scorecard, grid="base",
        )
        row["E_base"] = base_result.to_json_dict()["E"]
        row["tier_base"] = int(base_result.tier)
```
Each scored state is also scored once on CPU float64 and compared on tier and the counts boolean (GAP-60-07); a difference raises a dedicated owner-routed exception and the better score is never taken. There is no analog for that step (see "No Analog Found").

**(f) Per-state weights digest** (`controllers.py:267-275`; apply it per parameter in sorted-name order):
```python
def _tensor_hash(value: torch.Tensor) -> str:
    """Hash tensor dtype/shape/bytes after CPU normalization."""
    tensor = value.detach().cpu().contiguous()
    descriptor = json.dumps(
        {"dtype": str(tensor.dtype), "shape": list(tensor.shape)},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(descriptor + b"\0" + tensor.numpy().tobytes()).hexdigest()
```

**(g) Signals and the stop checkpoint** (`pinn/train.py:898-911`, `1405-1414`, trimmed):
```python
    signal_state = SignalState()

    def on_escalate() -> None:
        ...

    restore_handlers = install_signal_handlers(signal_state, on_escalate=on_escalate)

    if signal_state.stop_requested:
        checkpoint_payload = build_checkpoint_payload(...)
        store.save_rolling(checkpoint_payload, int(run_controller._global_step))
        return finish_run("interrupted", signal_state.exit_code)
```
`install_signal_handlers` handles SIGINT (exit code 130, escalation after a 1.0 s debounce) and SIGTERM (143) only (`signals.py:57-75`); there is no SIGHUP handler anywhere. Add SIGHUP as a graceful stop with exit code 129 inside the harness module and do not edit `pinn/training/signals.py`. The harness writes its own `.weights`/resume payloads, never `build_checkpoint_payload`.

**(h) Resume refusals to mirror** (`controllers.py:844-851`, `2213-2218`):
```python
    def load_state_dict(self, state: dict[str, Any]) -> None:
        if self._amended_recipe and (
            "front_monitor" not in state or "lbfgs_segment_state" not in state
        ):
            raise ValueError(
                "amended resume checkpoint is missing front_monitor or "
                "lbfgs_segment_state; refusing to regenerate runtime state"
            )

        if self._lbfgs_segment_state is None:
            if int(lbfgs_start) > 0:
                raise ValueError(
                    "resume checkpoint is missing active L-BFGS segment state; "
                    "refusing to redraw samples or causal weights"
                )
```
State to persist (each has a `state_dict`/`load_state_dict` or capture helper): model, Adam, scheduler, `ScheduledWeights` (`scheduled_weights.py:246-271`), `GradClipper` (`grad_clip.py:292-344`), four RNG streams (`determinism.py:57-116`: `capture_rng_state(rng)` / `restore_rng_state(state, rng)` assign `bit_generator.state`, never reseed), budget `B`, extension flag, summed Adam wall seconds, the frozen monitor and polish segment (schema `phase57-lbfgs-segment/v1`, hash-checked on restore at `controllers.py:2341-2346`), and the module digests. Write with `atomic_write_torch` (`atomic_io.py:67-92`) under the ignored `runs/phase60/` tree; load only with the literal `torch.load(..., weights_only=True)`.

**(i) Run lifecycle and halt style** (`diag07_common.py:708-752`; `baselines.py:733-748`). The lock call defaults to the Phase 59 tree, so pass `evidence_root=` (S3):
```python
def start_run(evidence_root, planned_results, *, label, command, required_bytes) -> dict:
    evidence_io.require_frozen_scorecard()
    run_id = evidence_io.begin_long_step("diag07", label, command=command)
    try:
        preflight = evidence_io.memory_preflight(required_bytes)
    except evidence_io.MemoryPreflightError as exc:
        evidence_io.record_long_step_failure(str(exc), run_id=run_id)
        raise
    ...

def main(argv=None) -> int:
    started_wall = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    try:
        code = _run(argv, started_wall=started_wall, started=started)
    except BaselinesHalt as exc:
        print(f"BASELINES-HALT: {exc}", file=sys.stderr)
        code = 2
    except split_allowlist.SplitRefused as exc:
        print(f"SplitRefused: {exc}", file=sys.stderr)
        code = 2
```
The CLI takes an arm id from a closed enumeration, never a path. `pinn/training/timing.py:78-120` is the nearest timing-record shape (finite and positive `s_per_step`, fingerprint with device, dtype, torch and python versions, git head); the fingerprint helper `pinn/verify.py::current_fingerprint` calls `resolve_runtime`, which the SPEC says real arms do not consult, so build the fingerprint with `evidence_io.provenance_record` (`evidence_io.py:270-298`) plus `platform.mac_ver()[0]`.

**Do not copy:** the broad `except Exception` at `overfit_probe.py:487-490` and the ones in `gate04_train_free.py:885, 1231, 1252, 1304` (they would swallow an owner stop); `evidence_io.runtime_gate` at the tail of `baselines.main` (a 600 s budget, `evidence_io.py:684-699`); `resolve_runtime` and `current_fingerprint`; `build_checkpoint_payload`, `CurriculumController`, `StageDisposition`; `_make_lbfgs_closure`'s 4096-row `_weighted_non_data_terms`.
**Tests:** rows 25, 27, 29, 31, 33, 37.

---

### 5. `pinn/verification/learnability_g2.py` (service, pure rules + small file-I/O)

**Analog:** the rule functions of `feasibility_scorecard.py` (keyword-only `scorecard`, validated inputs, plain return values) and `candidate_eligibility.py` (ordered fixed candidates, never trust a caller-supplied verdict field).

**Owner-routed exception and the two rule functions the module must call, not re-implement** (`feasibility_scorecard.py:55-59`, `684-715`):
```python
class OwnerRouted(Exception):
    """A result outside a pre-registered branch.

    Callers must surface it to the owner and never handle it silently.
    """

def counts(tier, E, E_formula, *, scorecard) -> bool:
    ...
    if E_formula is None:
        raise OwnerRouted("two-Kepler formula not applicable on a counted system")
    ...
    return (
        tier_value >= int(rule["min_tier"])
        and math.isfinite(position)
        and math.isfinite(formula)
        and position < formula
    )

def g2_fires(rung1_tiers: Any, *, scorecard: Scorecard) -> bool:
    gate = _require_scorecard(scorecard).section("gate_g2")
    panel = int(gate["panel_size"])
    if not isinstance(rung1_tiers, (list, tuple)) or len(rung1_tiers) != panel:
        raise ValueError(f"rung1_tiers must have length {panel}")
    below = int(gate["trigger_below_tier"])
    needed = int(gate["trigger_min_systems"])
    count = sum(1 for tier in rung1_tiers if _require_int(tier, "tier") < below)
    return count >= needed
```
**The later-rung refusal the stop path must never trip** (`feasibility_scorecard.py:734-752`):
```python
    if g2_fired:
        if sweep_rescued:
            raise OwnerRouted("owner checkpoint 4")
        later = {
            "rung2b_counts": rung2b_counts,
            "rung3_counts": rung3_counts,
            "control_branch": control_branch,
            "rung1_beats_formula": rung1_beats_formula,
        }
        present = [name for name, value in later.items() if value is not None]
        if present:
            raise ValueError(
                "later-rung inputs must be None when G2 fired: " + ", ".join(present)
            )
```
On a stop call it with `sweep_rescued=False` and four `None` arguments; on a confirmed rescue call it with `sweep_rescued=True` and let `OwnerRouted` propagate.

**Ruling loader (D-11):** accept a file only when tracked and clean, read through the same check the Phase 59 verifier uses (`verify_phase59_evidence.py:113-118`):
```python
def is_tracked(relative: str) -> bool:
    return _git("ls-files", "--error-unmatch", "--", relative).returncode == 0


def is_clean(relative: str) -> bool:
    return _git("status", "--porcelain", "--", relative).stdout.strip() == ""
```
and parse a strict machine block (finite positive `approved_first_omega_0`, a literal answer) with the "literal value only" discipline of `structural_facts` (row 1). The owner's quote is opaque text: never executed, formatted into a path, or evaluated. Cite the ruling file's SHA-256 in every continue-path record.

**Skip writer:** the two reasons are module constants and tested byte for byte, including the circled digit U+2464 in `checkpoint ④ answered go to the verdict`; refuse once any Rung-2 arm has a state file; the Level-3 handoff text is `not tested (skipped at G2)`. The probe formula field is the literal `not applicable: no hierarchical split`, already defined at `two_kepler.py:25` and `dataset_survey.py:73`; reuse it by value, do not import a private name.

**Sweep pair and confirmation:** no repository analog (pinned lap counts 1632: 10.47, 851: 18.61, 4658: 39.35; four SPEC cases). Sketch source: `60-RESEARCH.md` Pattern 6 and its code example.

**Do not copy:** any handler around `counts`, `budget_outcome` or `decision_verdict` (S2).
**Tests:** rows 34 and 35.

---

### 6. `pinn/verification/diagnostic_architecture.py` (factory, transform)

**Analog:** `pinn/network.py` (exact; the builder is the same construction with one field overridden). `SQRSkipResNetSIREN.__init__` reads only attributes of its `spec` argument, so a duck-typed copy works (`network.py:160-196`, trimmed):
```python
    def __init__(self, spec, *, dtype, device, generator):
        super().__init__()
        self._build_dtype = dtype
        self._build_device = device
        self.power_p = int(spec.power_p)
        self.first_omega_0 = float(spec.first_omega_0)
        self.hidden_omega_0 = float(spec.hidden_omega_0)
        self.input_layer = _SIRENLayer(
            spec.input_dim, spec.hidden_width,
            omega_0=spec.first_omega_0, is_first=True,
            dtype=dtype, device=device, generator=generator)
```
**The seeding the builder must reproduce exactly** (`network.py:249-255`; the `isinstance` check at 249-252 is why `build_network` itself cannot be reused):
```python
    if not isinstance(spec, ArchitectureSpec):
        raise TypeError(
            f"build_network requires an ArchitectureSpec (got {type(spec).__name__})"
        )
    generator = torch.Generator(device=device)
    generator.manual_seed(int(spec.seed))
    return SQRSkipResNetSIREN(spec, dtype=dtype, device=device, generator=generator)
```
Fields to copy from a validated `ArchitectureSpec(seed=...)` (`architecture_spec.py:59-69`): `input_dim`, `output_dim`, `hidden_depth`, `hidden_width`, `first_omega_0`, `hidden_omega_0`, `layernorm_elementwise_affine`, `layernorm_eps`, `power_p`, `skip_cadence`, `seed`. Validate the requested omega (finite, positive) before constructing. `ArchitectureSpec` and `build_network` stay untouched (SCOPE-43). The test asserts omega 30 through the builder is bitwise equal to `build_network(ArchitectureSpec(seed=42), ...)` and that omega 60 differs only in the first layer's `omega_0` (`60-RESEARCH.md` Pattern 2, verified there).
**Do not copy:** `ArchitectureSpec.__post_init__` relaxation. Do not call the builder from a physics arm with a non-owner-approved value (row 1).
**Tests:** rows 23 and 36.

---

### 7. `pinn/verification/gate04_omega_remeasure.py` (CLI, batch)

**Analog:** `pinn/verification/gate04_train_free.py::main` (`1205-1349`) and the seam functions it drives. Copy the "complete PASS" definition and the raw-evidence write; do not copy what it does on a PASS or BLOCK.

**The complete-PASS definition** (`gate04_train_free.py:1279-1288`), with the verdict object from `run_gate(..., first_omega_0=<value>)`:
```python
    canonical_six_case_run = (
        args.cases_config is None and observed_case_ids == default_case_ids
    )
    complete_pass = bool(
        canonical_six_case_run
        and verdict_obj is not None
        and verdict_obj.verdict == VERDICT_PASS
        and not verdict_obj.blocking_reasons
        and not verdict_obj.unratified_conditions
    )
```
**What `main` does that the Phase 60 entry must not do** (`gate04_train_free.py:1296-1319`): on a complete PASS it calls `write_r_ref_artifact(verdict_obj, path=args.r_ref_path, ...)` with `args.r_ref_path` defaulting to the governed `R_REF_ARTIFACT_PATH` (`:76, 1198-1201`), and on a BLOCK it writes `terminal-state.json` through `_write_terminal_state` (`:1084-1114`). The governed `r_ref_stage0.json` is read by the trainer (`controllers.py:170-172`), the scorer (`feasibility_scorer.py:327-330`), baselines and the Phase 57 verifier; its SHA-256 must be unchanged before and after a Phase 60 re-measure.

**Seam sites** (`gate04_train_free.py`), each gets `first_omega_0=None`, default leaving behavior unchanged:
```python
def _measure_raw_bin_means(case, *, dtype, torch_device) -> np.ndarray:
    ...
    model = build_network(ArchitectureSpec(seed=case.seed), dtype=dtype, device=torch_device)   # line 716
def compute_r_ref(cases, *, precision: str, device: str) -> tuple[float, tuple[tuple[float, ...], ...]]:   # line 757
def evaluate_case(case, r_ref: float, *, precision: str, device: str) -> Gate04CaseResult:   # line 794
def run_gate(cases=DEFAULT_CASES, *, precision: str = "float64", device: str = "cpu") -> Gate04Verdict:   # line 845
```
Replace only line 716 with a branch: `None` keeps `build_network(ArchitectureSpec(...))`; a value goes through row 6's builder. `run_gate` converts every exception into a BLOCK verdict (`:885-898`), so validate the omega in the Phase 60 entry before calling it.

**Writing the re-measured artifact:** `write_r_ref_artifact(verdict, path=..., *, gate_evidence_path=None, gate_evidence_sha256=None)` accepts any `path` (`:911-917`) and enforces the six default cases in order (`:951-957`). Pass repo-relative strings for `gate_evidence_path` because it records `str(gate_evidence_path)` unredacted (`:1058`). Carry omega in the Phase 60 record that cites the artifact SHA-256: the frozen artifact key set has no omega field.
**Do not copy:** `_cli_configuration` (`:1134-1141`, absolute `str(args.evidence_root)` in committed JSON), `_write_terminal_state`, the `--r-ref-path` default, the `except Exception` blocks, `_new_run_dir` timestamp directories (use the Phase 60 evidence root). Write through `evidence_io.write_json` so the home-prefix guard applies.
**Tests:** row 30.

---

### 8. `launch_phase60_arm.py` (launcher + supervisor, event-driven)

**Analog:** `.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/launch_phase57_run.py` (exact). Copy the file and change the closed set, the command and the resume gate.

**Closed set, pinned interpreter, interrupted-exit constant** (`launch_phase57_run.py:36-47`):
```python
REPO_ROOT = Path(__file__).resolve().parents[4]
LAUNCH_ROOT_REL = Path("runs/.launch")
LAUNCH_SCHEMA = "phase57-detached-launch/v1"
LAUNCH_MODE = "detached-session"
PINNED_PYTHON = "<home>/miniforge3/envs/pinn-train/bin/python"
RUN_NAMES = (
    "stage0-v23g7-smoke",
    ...
)
INTERRUPTED_EXIT_CODE = 130
```
`parents[4]` is the repository root for any script at `.planning/phases/<phase>/evidence/`. Replace `RUN_NAMES` with the closed arm-id enumeration of row 1.

**Command form** (`launch_phase57_run.py:64-72`): `["/usr/bin/caffeinate", "-is", PINNED_PYTHON, "-m", "pinn.verification.learnability_run", <arm-id>]`, argv list only, no `shell=True`; no path argument.

**Resume gate** (`launch_phase57_run.py:75-101`). The Phase 60 form accepts the governed stop codes 129, 130 and 143, and only when a valid resume checkpoint and a stop marker exist; any other exit (including SIGKILL, returncode -9, exit code 137) means "an arm that cannot resume goes to the owner":
```python
    if not resume:
        if run_dir.exists() or launch_dir.exists():
            raise LaunchError(f"fresh launch target already exists: {run_dir} or {launch_dir}")
        return 1, launch_dir / "invocation-1"
    ...
    exit_record = json.loads(exit_path.read_text(encoding="utf-8"))
    if exit_record.get("exit_code") != INTERRUPTED_EXIT_CODE:
        raise LaunchError(
            "resume must follow a governed interrupted process (exit code "
            f"{INTERRUPTED_EXIT_CODE}); previous exit was {exit_record.get('exit_code')!r}"
        )
```
**Detached start and exclusive-create writes** (`launch_phase57_run.py:58-61`, `104-136`): `path.open("x")` for every JSON, `invocation_dir.mkdir(parents=True, exist_ok=False)`, and `subprocess.Popen(..., stdin=DEVNULL, start_new_session=True, close_fds=True)`. The supervisor records `returncode`, `exit_code` (`128 - returncode` for a signal death), `signal`, `wall_clock_secs` in `exit.json` (`:160-169`).

Keep launch files untracked under the ignored `runs/.launch/` tree (the staged-path policy blocks `runs/*`) and copy the exit code, signal, wall seconds and invocation count into the committed arm record. The script contains the home-directory interpreter path; Phase 57 already commits that, and the redaction guard applies to JSON evidence, not to scripts.
**Keep out of `pinn/`:** `_assert_host_mps` (`launch_phase57_run.py:173-180`) probes MPS by running the pinned interpreter with a `-c` string that contains `is_available`. That is acceptable in an evidence-tree script but must not be copied into any `pinn/**/*.py` module because of scan B (S1).
**Tests:** row 37.

---

### 9. `verify_phase60_evidence.py` (verifier CLI, batch)

**Analog:** `verify_phase59_evidence.py` (exact). It is independent of the producing tools: stdlib plus `pinn.verification.feasibility_scorecard`, a `fail()` that raises, `COMMANDS` dispatch, a `main` that returns 1 on any failure.

**Shape to copy** (`verify_phase59_evidence.py:24-34, 50-56, 956-988`):
```python
if __package__ in (None, ""):
    _ROOT = Path(__file__).resolve().parents[4]
    if str(_ROOT) not in sys.path:
        sys.path.insert(0, str(_ROOT))

class VerifyError(RuntimeError):
    """Fail-closed evidence verification error."""

def fail(message: str) -> None:
    raise VerifyError(f"verify_phase59_evidence FAIL-CLOSED: {message}")

COMMANDS = {
    "scorecard-frozen": cmd_scorecard_frozen,
    "manifest": cmd_manifest,
    ...
    "final": cmd_final,
}

def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    try:
        COMMANDS[args.command](args)
    except Exception as exc:  # noqa: BLE001 - verifier CLI is fail-closed
        print(str(exc), file=sys.stderr)
        return 1
    return 0
```
A broad handler is acceptable in a verifier because it fails closed; it must not run any rule that raises `OwnerRouted`.

**Helpers to reuse by copying:** `repo_path` containment and symlink refusal (`:70-81`), `load_json` (`:84-88`), `is_tracked`/`is_clean` (`:113-118`), `_file_map` skipping `logs` and `__pycache__` (`:310-323`), `_check_opened` requiring the three zero counters (`:444-452`), `_check_result`'s `producer_sha256` re-hash (`:424-441`). Subcommands per `60-VALIDATION.md`: `records`, `g2`, `rescore`, `final`. `rescore` loads committed `.weights` with `torch.load(..., weights_only=True)`, re-scores, and compares tier and `E` with the record; it is an expensive command (run once, detached, output retained).
**Do not copy:** the Phase 59 freeze assertions (`assert_scorecard_frozen`, `:238-262`) except by calling the Phase 59 verifier's `scorecard-frozen` subcommand or `evidence_io.require_frozen_scorecard`; Phase 59 area names and `phase59-` schema prefixes.
**Tests:** rows 35 and 36; the per-arm contract rows of `60-VALIDATION.md`.

---

### 10. `pinn/verification/feasibility_scorer.py` (EDIT, three widening sites)

**Edit site** (`feasibility_scorer.py:416-426`, current):
```python
            position_chunks.append(
                positions.detach().to(device="cpu", dtype=torch.float64).numpy().reshape(-1, 3, 3)
            )
            velocity_chunks.append(
                velocities.detach().to(device="cpu", dtype=torch.float64).numpy().reshape(-1, 3, 3)
            )
            if want_acceleration:
                _first, second = componentwise_du(traj, u_chunk)
                acceleration_chunks.append(
                    second.detach().to(device="cpu", dtype=torch.float64).numpy().reshape(-1, 3, 3)
                )
```
**Analog fix** (`jx02_jx05.py:56-60`, and its use at the three sites `:373-375`):
```python
def _cpu64(tensor):
    """Detach, move to the CPU, then widen to float64 (MPS has no float64)."""
    import torch

    return tensor.detach().to("cpu").to(torch.float64)

            position_chunks.append(_cpu64(positions).numpy().reshape(-1, 3, 3))
            velocity_chunks.append(_cpu64(velocities).numpy().reshape(-1, 3, 3))
            acceleration_chunks.append(_cpu64(second).numpy().reshape(-1, 3, 3))
```
The same lesson is in `diag07_common.py:468-479` (`_flat_float64`). Add one module-private helper in the scorer and use it at all three sites; `torch` is already imported at module level, so add no import. `score_network` passes `want_acceleration=True` (`feasibility_scorer.py:454-463`), so fixing two sites leaves it broken. Leave the module docstring's first line ("Phase 59 (FEAS-01) ...") unchanged: it keeps the file in the Phase 59 static-guard scan (`test_static_guards.py:58-79`), which forbids `torch.optim`, trainer or evaluator imports and checkpoint saves; a one-line helper satisfies all of them. Gold-grid arithmetic stays float64 on the CPU; CPU float64 behavior is unchanged because `.to("cpu")` and `.to(torch.float64)` are no-ops there.
**After the edit:** compute the new SHA-256 and write `evidence/scorer-successor.json` (row 14). Do not re-run Phase 59 evidence.
**Tests:** row 22, plus the green-at-HEAD suites listed in `60-VALIDATION.md` "Adjacent regression".

---

### 11. `pinn/verification/gate04_train_free.py` (EDIT, optional `first_omega_0`)

See row 7 for the four seam sites and the line-716 replacement. Constraints specific to the edit:
- Default `None` must leave every existing call and result unchanged. `tests/phase56/test_gate04_train_free.py` is the natural regression suite but imports pytest (Hazard 2), so it cannot be the gate; `tests/phase57/test_gate_and_evaluation.py` imports `condition_ii_verdict` from this module and is runnable under `unittest`. Add a default-path equality test in row 30 instead.
- Import the builder from `pinn.verification.diagnostic_architecture`; it imports only `pinn.architecture_spec` and `pinn.network`, so no cycle.
- The module is in the Phase 38 scan set (S1 scan B and C): no `is_available`, no `set_default_dtype`.
- `gate04_train_free.py` is not pinned by any committed hash (checked: no result file or verifier hashes it), unlike the Phase 59 producer modules in row 12.

---

### 12. `verify_phase59_evidence.py` (EDIT) and `evidence/manifest.json` rewrite

**Edit sites** (`verify_phase59_evidence.py`):

1. `_check_result`, lines `437-440`, current:
```python
    for relative, digest in producers.items():
        current = sha256_file(repo_path(str(relative), what=str(relative)))
        if current != digest:
            fail(f"{path.name} producer_sha256 does not match {relative}")
```
   Accept exactly one exception: when `relative` is the scorer path, `digest` equals the successor record's `predecessor_sha256` and `current` equals its `successor_sha256`. Read the record once through `repo_path(...)`, require `is_tracked` and `is_clean` (`:113-118`), refuse a record that names more than one path, and keep today's strict behavior when the record is absent. Resolve the record relative to `REPO_ROOT` at call time: the Phase 59 tests patch `REPO_ROOT` in the loaded module (`tests/phase59/test_evidence_verifier.py:384-385`).
2. `REDERIVE["baselines"]` (`:270-275`) and `_rederive` (`:499-514`): the baselines re-derivation byte-compares output that embeds the live scorer digest, so run it against a temporary copy of the committed `baselines/` directory in which the predecessor digest is replaced by the successor digest:
```python
REDERIVE = {
    ...
    "baselines": (["-m", "pinn.verification.baselines", "--check"], "BASELINES-CHECK-OK"),
}

def _rederive(area: str) -> None:
    if area not in REDERIVE:
        return
    tail, token = REDERIVE[area]
    proc = subprocess.run(
        [sys.executable, "-B", *list(tail)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=1800,
        check=False,
    )
    if proc.returncode != 0:
        fail(f"{area} re-derivation exited {proc.returncode}")
    if token not in proc.stdout:
        fail(f"{area} re-derivation did not print {token}")
```
   `baselines.py` already takes `--evidence-root` (`_parse_args`, `baselines.py:708-715`) and compares against `<root>/baselines/` (`_evidence_dir`, `:640-647`), so no producer edit is needed. If the substituted re-derivation still differs, stop and report: the fix changed CPU float64 numbers (GAP-60-02).
3. Manifest: after the verifier edit, `manifest --area all --write` (`_write_manifest`, `:338-358`) rewrites `evidence/manifest.json`; diff it and confirm only the verifier entry and `produced_at_head` changed. `_check_manifest` otherwise fails with "changed file verify_phase59_evidence.py" (`:384-392`).
4. Imports: stay inside the Phase 59 guard's allowed roots (`tests/phase59/test_static_guards.py:53-55`: stdlib, numpy, torch, yaml, pinn). `shutil` and `tempfile` are stdlib.

**Analog for the successor record:** `evidence/scorecard-freeze.json` (flat JSON: `schema`, paths, `sha256` per path, `head_at_freeze`, `note`). Name exactly one path, `predecessor_sha256` `cd5019a2ba5604f39d5c6e01763ff3f0e53547920a57bbf174ebc3bb0a73870b` and `successor_sha256`.
**Run `final` once, detached, output retained** (about 644 s); never alongside a timing run or an arm.
**Tests:** row 28.

---

### 13. `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` (EDIT, amendment text)

Target text is the "Amendment text" block of `60-SPEC.md` (single source of truth; the test parses it). Compare after `unicodedata.normalize("NFC", ...)` and whitespace collapse only (GAP-60-01). Current edit sites at this HEAD:

| Paragraph | File and lines | Today | Edit |
|---|---|---|---|
| SCOPE-39 | `REQUIREMENTS.md:319` | cell opens `**Stage-0 only, with three read-only or diagnostic exceptions:**` | delete the two `**` markers; keep the trailing `[2026-10-17 spec amendment]` |
| FEAS-04 last bullet | `REQUIREMENTS.md:135` | verbatim | none |
| Roadmap criterion 3 sentence | `ROADMAP.md:234` (criterion 3) and `:225` (end of the Gate G2 paragraph) | verbatim in both | none; check containment inside the criterion-3 item, not by whole-file count |
| FEAS-09 | `REQUIREMENTS.md:187` and `:195` | the three sentences are split across the opening line and the last acceptance bullet | make the three sentences one contiguous run in the FEAS-09 body |
| SCOPE-44 | `REQUIREMENTS.md:324` | condition is a clause inside "(four arms, about 12 hours)" | add the stand-alone sentence `The hard-stage probes run only if the ladder continues past G2.` |
| Checkpoint 4 continue | `REQUIREMENTS.md:337-340` (Owner Checkpoint 4, hard-wrapped at about 75 columns) | content spread across `:126`, `:337-340`, `:351` | insert the three sentences contiguously in Owner Checkpoint 4 (GAP-60-01) |

Hard-wrapped lines (Owner Checkpoint 4 wraps at about 75 columns with indented continuation lines) are why the comparison collapses whitespace. The scorecard SHA-256 `f4b17688...444b` (`feasibility_scorecard.py:44`) must be unchanged, and so must the other three frozen files (`scorecard-freeze.json` rels).
**Tests:** row 21.

---

### 14-15. `evidence/scorer-successor.json`, `60-RUN-PROTOCOL.md` + `evidence/run-protocol.json`

**Analog:** the Phase 59 freeze pair. `scorecard-freeze.json` is flat canonical JSON: a `schema` string, each pinned path with `*_sha256` and `*_size_bytes`, `head_at_freeze`, `decision_sources` with `git_blob`/`last_commit`/`sha256`/`verify` modes (`unchanged` or `ancestor_state`), and a one-line `note`. `59-SCORECARD.md` opens "Audience: the project owner, a non-specialist", then "In plain language", then the details; the protocol document should follow that order.

Pin in `run-protocol.json`: seed 42, runtime MPS float32 with the CPU float64 cross-check, scorecard SHA-256, scorer SHA-256 (successor), amendment commit SHA, harness module digests (`evidence_io.module_hashes`, `evidence_io.py:456-459`), the timing-run rule (GAP-60-04), clipping (GAP-60-03), polish semantics (GAP-60-05), divergence (GAP-60-06), cross-check scope (GAP-60-07), weights format (GAP-60-08), the failed-confirmation stop (GAP-60-09), and the reference-in-force rule (GAP-60-10). The pair must be committed before any real-arm record (SPEC R4). Use the Phase 59 `decision_sources` idea for the GAP and CONTEXT files if a pinned-source check is wanted; it is an optional design choice, not a requirement.

---

### 16. `evidence/preflight/records.json`

**Analog:** `baselines/files_opened.json` and `audit/reader_acceptance.json` (Phase 59). Per assigned key record: key string (`evidence_io.record_key_str`, `evidence_io.py:105-111`), split, snapshot count, within-T count, measured dt, inner pair, SHA-256 of the parsed float64 arrays (so the read is re-derivable without storing a path), and the attestation summary (`OpenAttestation.summary()`, `split_allowlist.py:325-337`, schema `phase59-files-opened/v1`). Never write the data root or home path (`evidence_io.guard_redaction`, `evidence_io.py:143-155`). Expected values: `60-RESEARCH.md` Finding G table.

---

### 17. `60-CHECKPOINT-4-RULING.md` (continue path only)

**Analog:** `.planning/phases/57-corrected-re-run-the-preserved-evaluation/57-RULING.md`: YAML front matter (`phase`, `milestone`, `created`, `pre_registered_at`, `status`, `authority`), an "Authority and boundary" section that carries the owner's words as a block quote, then numbered decisions. The D-11 file adds a strict machine block with a literal answer and a finite positive `approved_first_omega_0`; no repository file has such a parser (see "No Analog Found"). The file is written only from the owner's words, committed before any continue-path arm, and its SHA-256 is cited by every continue-path record.

---

### 18. `evidence/arms/<arm-id>/{record.json, adam.weights, polish.weights}`

**Analog for the payload conventions:** Phase 59 result payloads (`baselines.py:493-519`): `schema`, `plain_language`, `scorecard_sha256`, `producer_sha256` (a mapping of module path to digest), plus the per-row score dict `ScoreResult.to_json_dict()` (`feasibility_scorer.py:162-180`; non-finite floats become string sentinels via `json_safe_float`). Use schema `phase60-harness-run/v1`, `diagnostic: true`, and a fixture-versus-real marker (a fixture run must never read as a rung result).

**Analog for "first completed run is the result":** `pinn/evaluate.py:204-260`. A cheap pre-check plus the authoritative exclusive create, fsync of the file and of the directory, never removed:
```python
def _assert_evaluation_unclaimed(*, attempt_path: Path, receipt_path: Path) -> None:
    for path in (attempt_path, receipt_path):
        if path.exists():
            raise _single_use_refusal(path)

def _claim_evaluation_attempt(attempt_path, *, run_dir, checkpoint_path, stamp) -> None:
    attempt_path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    try:
        fd = os.open(attempt_path, flags, 0o600)
    except FileExistsError as exc:
        raise _single_use_refusal(attempt_path) from exc
    ...
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    directory_fd = os.open(attempt_path.parent, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
```
Differences: a Phase 60 arm may resume after a governed stop (SPEC R8), so the claim carries an invocation counter and a stop marker; an unclean exit is an owner stop, never a restart.

**Analog for the fingerprint fields** (`evidence/generation-7-timing-calibration.json`, written by `pinn/training/timing.py:109-118`): `fingerprint` with `device`, `dtype`, `torch_version`, `python_version`, `git_head`. Add `platform.mac_ver()[0]`, config hash, protocol SHA-256, scorer SHA-256, ruling SHA-256 when applicable, per-state weights digest (`_tensor_hash` order, row 4 f) and file SHA-256, wall hours, seconds per step (the timing run recorded separately), the budget trail, the trace, the attestation zeros, `counts` and the formula field, and the readout notes (D-04, D-05, D-08).

**Weights:** `torch.save` of a CPU float32 `OrderedDict` through `atomic_write_torch`; the extension is `.weights`. A harness payload must fail the production validators: `_is_structurally_valid` requires the keys `model, optimizer, curriculum, rng, counters, config_identity, schema_version` with `schema_version == 2` (`checkpoint.py:167-200`). The arm directory never contains `config.yaml` or `splits.json`.
**Do not copy:** `write_json` as a replace-in-place for `record.json` without an exclusive pre-check (`evidence_io.py:187-193` uses `os.replace`, so it would overwrite).

---

### 19. `evidence/g2/{g2-outcome.json, sweep-curve.json, skip-records.json}`

Same payload conventions as row 18. `g2-outcome.json` stores the three tiers and the recomputed `g2_fires`; `sweep-curve.json` the four-setting curve (tier, `E`, `eps_h`, valid horizons at 1% and 10%); `skip-records.json` one entry per skipped requirement with an exact reason string. Written by row 5; verified by row 9 (`g2` subcommand).

---

### 20-37. Tests (`tests/phase60/`)

**Scaffold:** `tests/phase60/__init__.py` is a one-line docstring like `tests/phase59/__init__.py`. The repository has no `tests/__init__.py`; a subpackage still imports as a namespace package. Quick command: `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase60.<module> -v`.

| Row | Module | Pattern to copy (file:lines) | Notes |
|---|---|---|---|
| 21 | `test_amendment.py` | `tests/phase56/test_spec_amendment_contract.py:1-80` (module-level verbatim constants, document read once); `tests/phase59/test_scorecard.py:35` (`hashlib.sha256(raw).hexdigest() == SCORECARD_SHA256`); `tests/phase59/test_evidence_verifier.py:350-355` (`scorecard-frozen` on the real worktree prints `SCORECARD-FROZEN-OK`) | Parse the six paragraphs from `60-SPEC.md` itself; assert containment inside the designated section only. The Phase 56 file is pytest-style functions: convert to `TestCase` methods. |
| 22 | `test_scorer_mps.py` | `tests/phase59/test_diag07_panels.py:280-301` (`assertEqual(actual.to_json_dict(), expected.to_json_dict())` on CPU float64); `tests/phase59/test_scorer_network.py:78-94` (`_model`, `_closure`, `_IC13`, `_MASSES`, `_TIMES`) and the AST helper `_names` at `:54-75` | MPS integration test must fail (not skip) on this Mac when MPS is missing. Static: no `.to(device="cpu", dtype=` pattern remains. The direct "old widen raises" probe is a clearly named non-gating platform test. |
| 23 | `test_arm_spec.py` | `tests/phase59/test_scorecard_rules.py:12-15, 41-45` (`_fn(self, name)` getattr helper; `assertRaises` plus message check); `tests/phase59/test_split_allowlist.py:85-109` (mock `builtins.open`, `io.open`, `pathlib.Path.open`, `pathlib.Path.read_text` to prove a refusal precedes any open) | INST-05(b) and (e). |
| 24 | `test_data_seam.py` | `tests/phase59/_corpus_fixtures.py:78-123` (`tiny_split_fixture` yields `data_root`, `manifest_path`, `manifest_sha256`, `allowed_key`, `test_key`, `test_key_with_file`, `blacklist_path`); `tests/phase59/test_split_allowlist.py:30-40` (`_reader` helper, no hook installed) | In-process tests build `AllowlistedCorpusReader` without `install_open_attestation`. Attestation counts need a subprocess (S7). `TinyCorpus` gold ids are {0, 3, 7} with 24 points on `[0, 10]` and `HIER_MASSES` (`tests/phase39/_fixtures.py:67, 89-91, 259-264`); id 3 is blacklisted in the Phase 59 fixture and the fixture copies base files only, so a gold-key helper is new work. |
| 25 | `test_run_short.py` | `tests/phase38/test_overfit_probe.py:111-139, 159-188` (tmp evidence root, `main([...])`, read the single record, assert fields); `tests/phase43/test_evaluate_gate.py:228-239` (second run refused), `:286-315` (inject a failure after the claim with `mock.patch.object(..., side_effect=RuntimeError(...))`, assert the claim file persists and a retry is refused), `:317-334` (preexisting claim refuses) | Real network, CPU float64, tiny fixture, through the polish with both states scored; the record carries the fixture marker; a second invocation never replaces it. |
| 26 | `test_losses_trainer_functions.py` | mutation: `tests/phase55/test_architecture_characterization.py:283-320`; oracle: `tests/phase57/_fixtures.py:182-218` (`build_run_controller`) with `make_full_slot_source` (`:69-79`), cross-check shape `jx01_jx10.py:445-480` (`controller._run_adam_step_microbatched(batch, anchor_ctx, weights, parameters, microbatch_size=..., want_diagnostics=True)`, read `.grad`, set back to `None`); chunk equality: `tests/phase40/test_optimizer_phase.py:734-770` | Patch bare names in the harness module: `data_huber_loss`, `ic_anchor_loss`, `causal_physics_loss`, `softened_acceleration`, `componentwise_du`, `soft_energy_loss`, `angular_momentum_loss`, `accumulate_chunked_data_term`. Add identity assertions (`harness.data_huber_loss is controllers.data_huber_loss`). The mutation file is pytest-style (`pytest.approx`): use `assertAlmostEqual(..., places=12)`. |
| 27 | `test_refusals.py` | `tests/phase43/test_evaluate_edge_cases.py:89-102` (checkpoint without a frozen run raises `CheckpointOwnershipError`); `tests/phase41/test_checkpoint.py:288-370` (`load_checkpoint` refusals raise `NoValidCheckpointError`) | See Hazard 4: use an arm directory with neither `config.yaml` nor `splits.json`, so refusal happens before the held-out claim; assert no `evaluation-attempt.json` appears, once with an override record. |
| 28 | `test_verifier_successor.py` | `tests/phase59/test_evidence_verifier.py:34-44` (`load_verifier` via `importlib`), `:47-73` (`init_repo`, `commit_all`, `run_main`), `:375-410` (`AreaFixture` with a stub producer), `:920-937` (`ProducerHashTests`) | Cases: successor accepted; same digest for another path refused; a second successor refused; any other producer mismatch refused; absent record strict; untracked or dirty record refused. The sibling suite takes about 70 s. |
| 29 | `test_schedule.py` | `tests/phase40/test_optimizer_phase.py:301-320` (spy: `mock.Mock(wraps=torch.optim.lr_scheduler.CosineAnnealingLR)`), `:417-451` (clip spy: called in Adam, zero in L-BFGS) | New assertions: `LR_k` values (k = 0, 4, 6), cosine length B, warmup `min(2000, floor(0.1 B))`, no re-ramp past B, second cosine trace over `[B, 2B)` equals `[0, B)`. |
| 30 | `test_gate04_remeasure.py` | `tests/phase57/test_gate_and_evaluation.py:32` (runnable import of the module); `tests/phase56/test_gate04_train_free.py:429-481` (artifact schema; pytest, not runnable) | Assert the governed `r_ref_stage0.json` SHA-256 is unchanged, `first_omega_0=None` reproduces today's per-case bin means, no `terminal-state.json` is written, BLOCK exits non-zero. Use a one- or two-case set to stay cheap. |
| 31 | `test_budget_driver.py` | `tests/phase59/test_scorecard_rules.py:120-228` (boundary tables for `steps_budget`, `still_improving`, `budget_outcome`, `scoring_cadence_ok`, `polish_should_stop`); divergence injection `tests/phase40/test_optimizer_phase.py:334-358` | Fakes, no training. `OwnerRouted` propagates. |
| 32 | `test_preflight.py` | `tests/phase59/test_split_allowlist.py:112-121` (missing root: test key refused, allowed file missing) | A blocked record yields no arm and no fallback. |
| 33 | `test_resume.py` | `tests/phase41/test_controllers_ext.py:262-302` (RNG restore is exact continuation, not reseed), `:305-375` (pending optimizer state applied after a fresh Adam build); `tests/phase57/test_runtime_freeze.py:242-262` (segment state present in `state_dict`); `tests/phase42/test_signals.py:122-173` (`note_signal` logic) and `:199-237` (real signal to a subprocess, exit code, no abandoned `.tmp`) | Add a SIGHUP case (exit 129). Resume keeps B, sums Adam time, refuses a missing segment state or a changed module digest. |
| 34 | `test_g2.py` | `tests/phase59/test_scorecard_rules.py:48-117` | Four sweep-pair cases, confirmation maximum, none-confirms, skip-writer reasons, `decision_verdict` never called with later inputs on a stop, rescue not caught. |
| 35 | `test_protocol_records.py` | `tests/phase59/test_evidence_io.py:82-134` (redaction, atomic write returns SHA-256), `:405-449` (`begin_long_step` lock: second launch refused) | Record validator rejects any missing hash or version field; ruling loader accepts only a tracked, clean file with a strict block. |
| 36 | `test_static_guards.py` | `tests/phase59/test_static_guards.py:71-107` (`discover_scan_set` by docstring marker plus planned list), `:149-165` (`forbidden_name_violations`), `:203-222` (evaluator import detector), `:263-282` (`torch_load_violations`: literal `weights_only=True`), `:416-474` (`DetectorSelfTests`: every detector has an injected-violation self-test), `:401-413` (training and evaluation must not import these modules); `tests/phase41/test_checkpoint.py:372-382` (source-level count: every `torch.load` in the store passes `weights_only=True`) | See S2 for the new detectors: no catch of `OwnerRouted` (or a broad handler without a re-raise) around the frozen-rule calls; no `RunController`, `CurriculumController` or `run_stage` in harness modules; no `is_available`. Drop only the Phase 59 `torch.optim` and `Optimizer` ban (harness modules build optimizers); keep the bans on `TorchSaveCheckpointStore`, `save_rolling`, `save_best` and `save_anchor`, so no production-format checkpoint is ever written. |
| 37 | `test_launcher.py` | `tests/phase57/test_phase57_launcher.py:19-25` (load the launcher by path), `:60-100` (invocation directories, resume gate), `:103-176` (detached supervisor survives `SIGHUP` plus `SIGKILL` of the caller's process group, records a signal death as `-9` and `137`) | Replace the generation-7 ledger test with a closed-arm-id test; the resume gate accepts 129, 130, 143 only. |

---

## Shared Patterns

### S1. Repository-wide scans every new `pinn/**/*.py` module must pass

**Apply to:** rows 1-7. Executable source means docstrings and comment lines are stripped (`tests/phase39/test_prohibitions.py:93-112`); every string literal counts.

| Scan | Where | Forbidden in executable source | Consequence |
|---|---|---|---|
| A. Sole corpus reader | `tests/phase39/test_prohibitions.py:183-205` over `discover_pinn_modules()` | `brutus_hierarchical`, `brutus_standard`, `ic_hierarchical`, `ic_standard`; a `glob`/`rglob` call with `.txt` | Only the four modules in `ALLOWED_CORPUS_READERS` (`:49-54`) may name them. Do not add a fifth: `tests/phase59/test_split_allowlist.py:320-330` pins the set to exactly four. Avoid identifiers such as `ic_standard_*`. |
| B. Precision and availability | `tests/phase38/test_prohibitions.py:297-311` over `_discover_phase38_modules()` (`:107-130`) | `set_default_dtype`, `is_available`, `add_argument("--precision", default=` | Hard-code `torch.device("mps")` from protocol constants; an unavailable device fails at allocation. A `--precision` argument must be absent or `required=True`. |
| C. v1.3-era references | `tests/phase38/test_prohibitions.py:313-326` | `basic_architecture`, `data-processing-pipeline-full`, `data_processing_pipeline_full`, `data-handling`, `data_handling` | Never in a string literal or path. |

Two Phase 38 tests fail at HEAD for an unrelated reason (`test_spec_byte_identity_endpoint_sha256`, `test_spec_history_no_touch_since_phase_base`); the valid gate is the other four (`60-VALIDATION.md`). `tests.phase39.test_prohibitions` passes (31 tests, about 0.9 s). Do not add imports to `pinn/verification/__init__.py` (its docstring says rung modules load on demand).

**Docstring marker:** a `pinn/verification/*.py` file whose first docstring line starts "Phase 59" joins the Phase 59 scan set (`tests/phase59/test_static_guards.py:58-79`) and inherits its bans (`torch.optim`, trainer or evaluator imports, checkpoint saves). Every Phase 60 module must start "Phase 60 ...". The scorer and the Phase 59 verifier stay in that scan set; row 10 and row 12 edits must pass it.

### S2. Owner-routed stops are never caught; fail closed with a named halt

**Apply to:** rows 4, 5, 7, 9. The frozen exception states its own contract (`feasibility_scorecard.py:55-59`). The three frozen `OwnerRouted` cases are a missing formula on a counted system (`:694`), a rescue (`:736`) and an undeterminable improvement rate (`:834`); the harness adds a fourth, the CPU float64 cross-check disagreement. Halt style: a module-level exception class and a `main` that prints `<TOOL>-HALT: <reason>` and returns 2 (`baselines.py:94-95, 739-741`). A static detector (row 36) walks `ast.Try` nodes whose body calls `counts`, `budget_outcome`, `decision_verdict`, `g2_fires` or `better_state` (directly or through the arm driver) and flags a handler that is bare or names `Exception`, `BaseException` or `OwnerRouted` unless its body re-raises. It leaves the MPS cache-release `except Exception: pass` (row 3) alone because that wraps no frozen rule. Every detector gets an injected-violation self-test, as at `tests/phase59/test_static_guards.py:416-433`.

Existing handlers not to imitate in harness code: `overfit_probe.py:487-490`, `gate04_train_free.py:885, 1231, 1252, 1304`. The verifier's broad handler (`verify_phase59_evidence.py:985`) is acceptable only because it fails closed and never evaluates an owner rule.

### S3. Evidence writing

**Apply to:** rows 4, 5, 7, 14-19.
- Canonical JSON, redaction and atomic replace come from `evidence_io.write_json` (`evidence_io.py:187-193`), which calls `reject_evidence_root`, `canonical_json_bytes` (sorted keys, ASCII, non-finite floats as string sentinels, `:131-140`) and `guard_redaction` (`:143-155`, refuses the home prefix and the resolved data root):
```python
def write_json(path: Path, payload: Any, *, data_root: Optional[Path] = None) -> str:
    """Atomically write canonical JSON and return the SHA-256 of the bytes."""
    reject_evidence_root(path, data_root=data_root)
    raw = canonical_json_bytes(payload)
    guard_redaction(raw, data_root=data_root)
    atomic_write_text(path, raw.decode("ascii"))
    return _sha256_bytes(raw)
```
- Binary state: `atomic_write_torch(path, payload)` (`pinn/training/atomic_io.py:67-92`: write to `.tmp.<pid>`, fsync, `os.replace`, fsync the directory, unlink in `finally`). Do not copy the private `_atomic_write` clone at `overfit_probe.py:88-94`.
- Pass `evidence_root=` to `begin_long_step`, `end_long_step` and `record_long_step_failure`: with no argument the lock path is the Phase 59 tree (`evidence_io.py:566-575`, `EVIDENCE_ROOT_REL` at `:32`).
- Do not reuse `runtime_gate` (600 s budget, `:684-699`).
- `module_hashes(paths)` (`:456-459`) produces the `producer_sha256` mapping; the verifier re-hashes it.
- `require_frozen_scorecard()` (`:428-453`) is wired to the Phase 59 freeze and is still the right guard to call before any corpus read, exactly as `baselines._run` does (`baselines.py:718-725`).
- Never commit under a path segment `runs`, `tmp`, `outputs`, `scratch`; logs stay untracked (see the evidence-path rule under the classification table).

### S4. Frozen rules are called, never re-implemented

**Apply to:** rows 3, 4, 5, 9. Load once with `load_scorecard()` (SHA-checked) and pass `scorecard=` to every rule. Thresholds, cadence fractions, polish limits and tiers live only in `pinn/verification/artifacts/feasibility_scorecard_v1.json`. A harness literal that duplicates a scorecard value (for example `0.05`, `0.25`, `3.0` or a polish `50`) should be read from its field instead (`budget_rule`, `lbfgs_polish`, `gate_g2`, `tiers`). Do not edit `feasibility_scorecard.py`, the scorecard JSON, `59-SCORECARD.md` or `scorecard-freeze.json`.

### S5. MPS and memory discipline

**Apply to:** rows 2-4, 10. (1) Widen on the CPU before float64 (row 10). (2) Microbatch at 256 rows (`OptConfig.adam_microbatch_size`, `config.py:673`) everywhere: Pass 1, Pass 2, the frozen-monitor evaluation, the polish closure. (3) Release chunks with generation-0 `gc.collect` plus `torch.mps.empty_cache()` (row 3). (4) `jx02_jx05.py:376-377` also deletes locals and collects after each scoring chunk; copy that in the scoring path. (5) The footprint preflight is unreliable on this macOS; the owner confirms 6 GiB free and no other heavy job, and `evidence_io.available_memory_bytes()` is logged as advisory only. (6) No other heavy job during a timing run or an arm: seconds per step sets the budget.

### S6. One result per arm: exclusive create, claim, and no silent restart

**Apply to:** rows 4, 8, 18. Primary analog `pinn/evaluate.py:204-260` (row 18); secondary `launch_phase57_run.py:58-61, 107` (`open("x")`, `mkdir(exist_ok=False)`) and `evidence_io.begin_long_step` (`:626-633`, `os.open(..., O_CREAT | O_EXCL | O_WRONLY)` for the one-launch lock). `overfit_probe._new_run_dir` (`:97-108`) allocates a fresh timestamped directory per call and so does NOT give "first completed run is the result"; do not copy it.

### S7. Test conventions

**Apply to:** rows 20-37.
- `unittest.TestCase` only; pytest, scipy and safetensors are absent. Run with `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest ...`; `conda run` buffers output.
- The open-attestation audit hook is process-global and irreversible, and a second install for a different root raises (`split_allowlist.py:366-371`). Tests that need attestation counts run a subprocess, as `tests/phase59/test_split_allowlist.py:251-288` does (`_AUDIT_SCRIPT`) and `:291-317` (`_SECOND_INSTALL_SCRIPT`).
- Dataset-free tests build their data under `TemporaryDirectory`; no test writes under `simulation_data/`.
- Reuse by import, do not copy: `tests/phase59/_corpus_fixtures.py::tiny_split_fixture`, `tests/phase59/_fixtures.py::lagrange_rotation`, `tests/phase57/_fixtures.py::build_run_controller`, `tests/phase40/_fixtures.py::make_stub_model`.
- Expensive commands (over 60 s: Phase 59 `final`, `tests.phase59.test_evidence_verifier`, `baselines --check`, the D-07 re-measure, every arm and `rescore`) run once, detached, with complete retained output.

### S8. The reference scale in force (`R_ref`) and `S_H`

**Apply to:** rows 3, 4, 7, 18. The trainer validates an explicit `r_ref` as finite and positive, or reads the governed artifact once and freezes it (`controllers.py:175-204`); the loader accepts any path (`pinn.training.config.load_frozen_r_ref_artifact`, called at `controllers.py:187`). The harness passes `r_ref` explicitly into `causal_physics_loss(raw_bin_means, r_ref=..., times=bin_centres, ...)` (Pass 1 excerpt, row 3). The scorer's context column always normalizes by the governed artifact (`feasibility_scorer.py:327-330, 475-477`), so each record states which `R_ref` normalized the physics loss and which normalized the context column (GAP-60-10). Probe energy scale: `S_H = 22.321729071058996`, `eps_h = 0.0022321729071058997` from `runs/stage0-v23g7-seed42/training_metadata.json` (tracked; GAP-60-12), applied unchanged and recorded with its source file.

### S9. Commit and agent conventions (project-wide)

Agents commit with `scripts/agent-commit` only, with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS` set, explicit paths, subject `<type>(<scope>): <lowercase imperative>` with scope `60` or `60-NN`, a body for multi-file or `.planning/` commits, and the attribution trailer last; `scripts/agent-commit` rejects `-F` (pass multiple `-m` paragraphs). No push from `milestone/*`.

---

## No Analog Found

Planner should use the cited `60-RESEARCH.md` section or the nearest partial analog.

| Part | Role | Data Flow | Reason | Use |
|------|------|-----------|--------|-----|
| D-03 second cosine (reset `initial_lr`, new `CosineAnnealingLR`, same Adam) | schedule | transform | The trainer builds one cosine per `run_stage`; no restart exists | `60-RESEARCH.md` Finding B and its code example (verified numerically there); test pattern `tests/phase40/test_optimizer_phase.py:301-320` |
| SIGHUP graceful stop (exit 129) | signal handler | event-driven | `signals.py:57-75` handles SIGINT and SIGTERM only; no SIGHUP anywhere in `pinn/` | `60-RESEARCH.md` Finding I; add in the harness module, test per `tests/phase42/test_signals.py:199-237` |
| Exact polish resume with `LBFGS.state_dict()` | optimizer state | file-I/O | The trainer builds a fresh `LBFGS` each outer loop (`controllers.py:2443-2448`) and never saves its state | `60-RESEARCH.md` Finding I (state keys verified there); validation style from `controllers.py:2307-2358` |
| CPU float64 cross-check of every scored MPS state with an owner stop on a tier or counts difference | scoring | transform | New in GAP-60-07; no code compares two precisions | Row 4 (e); `jx02_jx05.py:56-60` for the widening; `60-RESEARCH.md` Finding E |
| Strict machine-block ruling parser (D-11) | loader | file-I/O | No committed file has a machine block; closest style is `structural_facts` and the freeze-record reader | Rows 1, 5, 17; `60-RESEARCH.md` Security notes |
| G2 sweep pair and confirmation selection | pure rule | transform | Pinned lap counts and four SPEC cases are new | `60-RESEARCH.md` Pattern 6 |
| Skip-record writer (two exact reasons, refuse after a Rung-2 start) | writer | file-I/O | New | Row 5; `60-RESEARCH.md` Pattern 6 |
| Successor-digest exception and digest-substituted baselines re-derivation (D-09, GAP-60-02) | verifier logic | batch | The edit sites exist, the logic is new | Row 12; `60-RESEARCH.md` Finding F |
| Amendment-containment parser (SPEC block to paragraphs) | test helper | file-I/O | New (GAP-60-01) | Row 13; `60-RESEARCH.md` Finding A |
| Per-arm step-timing run feeding `steps_budget` | measurement | batch | `pinn/training/timing.py` is a different contract (a smoke's EMA, 24 h freshness, fingerprint match); take only its finite-and-positive refusal and fingerprint fields | Row 4 (i); GAP-60-04 |

---

## Hazards found while mapping (beyond 60-RESEARCH)

1. **Signal tests live in `tests/phase42/test_signals.py`**, not `tests/phase41` (the brief's path). `tests/phase41/test_controllers_ext.py:262-375` supplies the RNG and optimizer-restore patterns.
2. **Two analog test files import pytest**, which `pinn-train` and the base environment lack: `tests/phase55/test_architecture_characterization.py` and `tests/phase56/test_gate04_train_free.py`. They cannot run under `unittest`, so they are pattern sources only. The GATE-04 default-path regression must be a new test (row 30) plus the runnable `tests/phase57/test_gate_and_evaluation.py`.
3. **`require_frozen_scorecard`, `begin_long_step` and the lock path default to the Phase 59 evidence tree** (`evidence_io.py:32-36, 428-453, 566-575`). The freeze guard stays correct for Phase 60, but every lock call needs `evidence_root=`.
4. **`evaluate_run` claims the single held-out attempt before it loads the checkpoint's model** (claim at `evaluate.py:413`, model load at `:441-448`). A harness file placed in a real run directory would pass the ownership check (`:162-188`), consume the held-out claim and read the test split (adapter and test index at `:422-429`) before failing on the missing `"model"` key. The INST-05(c) test must use a directory with neither `config.yaml` nor `splits.json`, so the refusal is at `_resolve_owning_run`, before any claim.
5. **`run_gate` turns every exception into a BLOCK verdict** (`gate04_train_free.py:885-898`), so a bad omega passed through the new keyword would look like a scientific BLOCK. Validate it before the call.
6. **GATE-04 evidence paths are written unredacted**: `_cli_configuration` stores `str(args.evidence_root)` (`:1139`) and `write_r_ref_artifact` stores `str(gate_evidence_path)` (`:1058`). Use repo-relative strings and `evidence_io.write_json`.
7. **The Phase 59 evidence verifier is loaded by `importlib` and `REPO_ROOT` is patched in tests** (`tests/phase59/test_evidence_verifier.py:34-44, 384-385`). New verifier code must read the successor record relative to the module's `REPO_ROOT` at call time and call git through `_git`, which already does.
8. **`_file_map` skips `logs` and `__pycache__`** (`verify_phase59_evidence.py:319`) and `.log` files are gitignored; a Phase 60 manifest or verifier must follow the same rule or it will count untracked files.
9. **`SQRSkipResNetSIREN` accepts a duck-typed spec, but `build_network` refuses anything that is not an `ArchitectureSpec`** (`network.py:249-252`); the builder must replicate the local `torch.Generator(device=device)` seeding (`:253-255`) or initial weights differ from the locked network.
10. **The trainer builds one `RunController` stage with `OptConfig.lbfgs_max_iter = 20`** (`config.py:669`); the frozen polish is 50. Read the scorecard.
11. **`TinyCorpus` gold files exist only for ids {0, 3, 7} and the Phase 59 manifest fixture copies base files only** (`_corpus_fixtures.py:68-75, 107-114`). The INST-05(d) fixture needs a small new helper that places a gold file for a train-split id.
12. **`tests.phase57.test_resource_preflight` fails on this OS** for the footprint reason (`60-VALIDATION.md` Manual-Only; `59-PATTERNS.md` S6): keep `tests/phase57` discovery out of any Phase 60 regression command and name adjacent suites explicitly.

## Uniformity checks to grep across the plans (plan-checker aid)

- Every plan that creates a `pinn/verification/*.py` module states a first docstring line "Phase 60 ...", S1 scans A, B and C, the four named `tests.phase38.test_prohibitions` tests plus `tests.phase39.test_prohibitions`, and that `ALLOWED_CORPUS_READERS` is unchanged.
- Every task that writes evidence names `evidence_io.write_json` or `atomic_write_torch`, the redaction guard, and a path with no `runs`, `tmp`, `outputs` or `scratch` segment.
- Every long-arm plan: owner memory prompt, `begin_long_step(..., evidence_root=...)`, detached launcher, the 129/130/143 resume table, and "an arm that cannot resume goes to the owner".
- Every plan that calls `counts`, `budget_outcome`, `g2_fires` or `decision_verdict` forbids catching `OwnerRouted` and passes `None` for all four later-rung inputs on a stop.
- The scorer plan names all three sites (`feasibility_scorer.py:416-426`) and the successor record with exactly one path; the verifier plan names `_check_result` `:437-440`, `_rederive` `:499-514`, the manifest rewrite, and a detached `final` run.
- Every command uses the pinned interpreter `<home>/miniforge3/envs/pinn-train/bin/python -B`.
- No plan edits `pinn_architecture.md`, `ctl_instruction.md`, `feasibility_scorecard.py`, the scorecard JSON, `pinn/evaluate.py`, `pinn/train.py`, `pinn/training/signals.py`, `ArchitectureSpec`, or any Phase 59 producer module other than the scorer.

## Metadata

**Analog search scope:** `pinn/verification/`, `pinn/training/`, `pinn/data/`, `pinn/*.py`, `tests/phase38`, `phase39`, `phase40`, `phase41`, `phase42`, `phase43`, `phase55`, `phase56`, `phase57`, `phase59`, `.planning/phases/57-corrected-re-run-the-preserved-evaluation/`, `.planning/phases/59-read-only-baseline-scorecard/` (including `evidence/`), `scripts/git_policy/`, `.gitignore`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`.
**Files read in full or in targeted ranges:** about 60. No corpus file and no `splits.json` was opened. A scripted pass re-checked the first and last line of the cited ranges.
**Pattern extraction date:** 2026-10-18
