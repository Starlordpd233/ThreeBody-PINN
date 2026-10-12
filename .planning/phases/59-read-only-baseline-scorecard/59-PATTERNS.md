# Phase 59: Read-Only Baseline & Scorecard - Pattern Map

**Mapped:** 2026-10-11
**Mapped against:** HEAD `805de014` on `milestone/v2.4`. Verified read-only: `git diff --quiet 629b1a6c HEAD -- pinn configs` exits 0, so every `pinn/` line number below is also the generation-7 line number.
**Files analyzed:** 26 deliverables (8 modules + 1 artifact, 12 test files, 1 test edit, 3 evidence tools, 1 document), plus 5 evidence output directories.
**Analogs found:** 24 / 26 (9 exact, 11 role-match, 4 partial). Two deliverables have no analog: `two_kepler.py`, `nn_copy.py`.

Tracked-source gate: every analog path named here was checked with `git ls-files` and is git-tracked source (no gitignored mirror). Note that `runs/stage0-v23g7-seed42/**` is also force-tracked (32 files), although `runs/` is in `.gitignore`. No corpus data file, no `splits.json` and no test-split file was opened while mapping.

## How to use this map

1. Read "Shared Patterns" first. **S1 is a hazard that 59-RESEARCH does not list**: three repository-wide scans apply to every new `pinn/**/*.py` module, not only `tests/phase39/test_prohibitions.py`.
2. Each assignment names one primary analog. Where a part has no analog it points to the 59-RESEARCH pattern (1-7) that supplies it.
3. "Do not copy" marks code in an analog that Phase 59 forbids (it opens test files, uses finite-difference velocity, or constructs an optimizer).
4. Tests are `unittest.TestCase` (D-37). Several analog tests (`tests/phase55`, `tests/phase56`) mix in pytest idioms; convert `pytest.raises` -> `assertRaises`, `tmp_path` -> `tempfile.TemporaryDirectory`, `pytest.approx` -> `assertAlmostEqual`.

## File Classification

| # | New/Modified File | Role | Data Flow | Closest Analog | Match |
|---|-------------------|------|-----------|----------------|-------|
| 1 | `pinn/verification/split_allowlist.py` | guard + reader | file-I/O (read-only) + event-driven (audit hook) | `pinn/verification/target_frame_probe.py::_build_control_reader` (1104-1150) + `pinn/data/adapter.py` seams | role-match |
| 2 | `pinn/verification/production_reference.py` | utility (loader, normalizer recovery) | transform | `pinn/data/adapter.py::_scan_and_admit` (820-891) + `pinn/data/preprocessing.py` (62-80, 290-348) | role-match |
| 3 | `pinn/verification/feasibility_scorecard.py` | config loader + pure rule functions | request-response | `pinn/training/config.py::load_frozen_r_ref_artifact` (166-275), `pinn/training/config_yaml.py::_map_section` (147-194), `pinn/verification/candidate_eligibility.py` | exact |
| 4 | `pinn/verification/feasibility_scorer.py` | service (metrics) | transform + request-response (autograd) | `pinn/verification/gate_metrics.py` (130-200), `pinn/training/validation_gate.py` (177-294), `pinn/training/controllers.py` (1091-1095, 1173-1176) | role-match |
| 5 | `pinn/verification/two_kepler.py` | utility (physics) | transform | none (module style only: `gate_metrics.py`) | none |
| 6 | `pinn/verification/nn_copy.py` | utility | transform (lookup) | none (module style only) | none |
| 7 | `pinn/verification/stage0_census.py` | batch analysis + CLI | batch | `pinn/data/stage_scan.py` + `pinn/verification/architecture_characterization_probe.py` | role-match |
| 8 | `pinn/verification/dataset_survey.py` | batch analysis + CLI | batch | `pinn/data/stage_scan.py::_sensitivity_sweep` (253-294), `pinn/data/stages.py::classify_stage_label` (58-86), spec snippet `ctl_instruction.md:1369-1435` | role-match |
| 9 | `pinn/verification/artifacts/feasibility_scorecard_v1.json` | config artifact | file-I/O | `pinn/verification/artifacts/r_ref_stage0.json` | exact |
| 10 | `tests/phase59/__init__.py` | test scaffold | - | `tests/phase46/__init__.py` | exact |
| 11 | `tests/phase59/_fixtures.py` | test fixtures | - | `tests/phase46/_fixtures.py`, `tests/phase39/_fixtures.py`, `tests/phase57/_fixtures.py` | role-match |
| 12 | `tests/phase59/test_split_allowlist.py` | test | event-driven | `tests/phase39/test_prohibitions.py` (432-470), `tests/phase39/test_splits.py` (495-511) | role-match |
| 13 | `tests/phase59/test_static_guards.py` | test (AST + subprocess) | batch | `tests/phase39/test_prohibitions.py` + `tests/phase46/test_isolation.py` + `tests/phase55/test_architecture_characterization.py` | exact (composite) |
| 14 | `tests/phase59/test_scorecard.py` | test | request-response | `tests/phase56/test_gate04_train_free.py` (32-43, 429-481) | exact |
| 15 | `tests/phase59/test_scorecard_rules.py` | test | request-response | `tests/phase56/test_gate04_train_free.py::PublicContractTests` (484-) | role-match |
| 16 | `tests/phase59/test_scorer_known_errors.py` | test | transform | `tests/phase46/test_fixtures_selfcheck.py` + `tests/phase46/_fixtures.py::make_dual_frame_trajectory` | role-match |
| 17 | `tests/phase59/test_two_kepler.py` | test | transform | closed-form only (conventions: `test_fixtures_selfcheck.py`) | partial |
| 18 | `tests/phase59/test_nn_copy.py` | test | transform | conventions only | partial |
| 19 | `tests/phase59/test_census.py` | test | batch | conventions only | partial |
| 20 | `tests/phase59/test_survey.py` | test | batch | conventions only | partial |
| 21 | `tests/phase59/test_diag07.py` | test | request-response | `tests/phase57/test_microbatch_equivalence.py` + `tests/phase46/test_isolation.py::NonInterferenceTests` | role-match |
| 22 | `tests/phase39/test_prohibitions.py` (MODIFY: `ALLOWED_CORPUS_READERS`, lines 40-50) | test config | - | same file, Plan 46-04 precedent (lines 40-45) | exact |
| 23 | `.planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py` | verifier CLI | batch | `.planning/phases/57-.../evidence/verify_phase57_evidence.py` | exact |
| 24 | `.planning/phases/59-.../evidence/manifest.json` | evidence manifest | file-I/O | `build_phase57_evidence.py::cmd_finalize` (389-401), `generation-7-retention.json` | exact |
| 25 | `.planning/phases/59-.../evidence/diag07/<driver>.py` | evidence driver | request-response (forward/backward, no optimizer) | Phase-58 replay script (`v2.3-closure-evidence-bundle.md:304-392`) + `phase57_production_conformance.py` (212-324) | role-match |
| 26 | `docs/work/designs/milestone_v2.4/59-read-only-baseline-scorecard/<date>-feasibility-scorecard.md` | design doc | - | `docs/work/designs/milestone_v2.3/58-verdict-traceability-close/2026-10-03-phase-58-diag-06-verdict-packet.md` | exact |

Evidence output directories (data, no analog needed): `evidence/census/`, `evidence/baselines/`, `evidence/survey/`, `evidence/diag07/`, `evidence/audit/`.

---

## Pattern Assignments

### 1. `pinn/verification/split_allowlist.py` (guard + reader, file-I/O + event-driven)

**Primary analog:** `pinn/verification/target_frame_probe.py::_build_control_reader` (1104-1150). It is the only existing code that reads corpus files per key behind an allowlist of physical keys, with a bounded FIFO cache.

**Per-file read, preprocess, cache** (target_frame_probe.py:1122-1150, trimmed):
```python
    eligible = frozenset(eligible_physical_keys)
    ...
    cache = collections.OrderedDict()

    def read(key):
        cached = cache.get(key)
        if cached is not None:
            return cached
        parsed = parse_brutus_file(paths[key], root=root)
        pre = preprocess_trajectory(parsed.times, parsed.positions,
                                    parsed.velocities, parsed.masses)
        controls = (parsed.times, parsed.positions, parsed.velocities,
                    parsed.masses, pre)
        cache[key] = controls
        while len(cache) > chunk_size:
            cache.popitem(last=False)
        return controls
```

**DO NOT COPY from the same function:** lines 1127-1133 build the `paths` map by `folder_dir.glob("*.txt")` over all four folders (it enumerates every file name, test files included). Phase 59 builds the path from the key after `require(key)` has passed (59-RESEARCH Pattern 1, last line). Also do not copy `_run_probe` (target_frame_probe.py:1611-1612), which does `AdmittedSetAdapter(root=..., blacklist_path=...)` and therefore opens every file (59-RESEARCH C-2).

**Imports pattern** (target_frame_probe.py:81-93). Keep the style, but drop `AdmittedSetAdapter` and `DEFAULT_BLACKLIST_NAME` unless needed; a static test bans the adapter class name (D-35):
```python
from pinn.data.adapter import (
    BRUTUS_FOLDER_TABLE,
    BRUTUS_SUBDIR,
    EvidenceRedactionError,
    parse_brutus_file,
    record_key_from_brutus,
)
from pinn.data.preprocessing import preprocess_trajectory
from pinn.data.splits import SplitManifest
```

**Folder table and filename grammar to invert** (adapter.py:81-86, 95-98). Gold status lives in the folder name only; the filename prefix is always the base prefix:
```python
BRUTUS_FOLDER_TABLE: dict[str, tuple[str, str]] = {
    "brutus_hierarchical": ("hierarchical", "base"),
    "brutus_hierarchical_gold_standard": ("hierarchical", "gold"),
    "brutus_standard_quasi_random": ("standard", "base"),
    "brutus_standard_quasi_random_gold_standard": ("standard", "gold"),
}
_BRUTUS_NAME_RE = re.compile(r"^brutus_(hierarchical|standard)_(\d{4})\.txt$")
```
Invert it by `(variant, fidelity) -> folder` and build `root / BRUTUS_SUBDIR / folder / f"brutus_{variant}_{id:04d}.txt"` (do not spell the four corpus tokens in new code; import the table).

**Containment** (adapter.py:173-187, 386-390). `parse_brutus_file(path, root=root)` already calls `resolve_within_root` and raises `CorpusPathEscape` (adapter.py:135) on escape:
```python
def resolve_within_root(root, target):
    root_resolved = Path(root).resolve()
    target_resolved = Path(target).resolve()
    try:
        target_resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise CorpusPathEscape(
            f"{target_resolved} is not contained beneath data root {root_resolved}"
        ) from exc
    return target_resolved
```

**Data-root precedence and label** (adapter.py:743-759, 761). Reuse this order exactly (explicit, then `GSD_DATA_ROOT`, then `default_data_root()`), record the label, never the path:
```python
        chosen = root if root is not None else data_root
        if chosen is not None:
            resolved = Path(chosen)
            source = "explicit"
        elif os.environ.get(DATA_ROOT_ENV):
            resolved = Path(os.environ[DATA_ROOT_ENV])
            source = "env:GSD_DATA_ROOT"
        else:
            resolved = default_data_root()
            source = "git_common_dir_default"
```
**Hazard:** `default_data_root()` (adapter.py:603-606) shells out to `git rev-parse --git-common-dir` with `check_output`. From a detached `git archive` snapshot with no `.git` it raises. The DIAG-07 driver must pass an explicit root and record `data_root_source = "explicit"`.

**Manifest identity and allowlist source** (stage_scan.py:495-504 and splits.py:390-395, 442-445):
```python
def _split_file_evidence(path: Path) -> dict[str, Any]:
    first = path.read_bytes()
    second = path.read_bytes()
    if first != second:
        raise RuntimeError("splits.json changed while recording byte identity")
    return {"sha256": hashlib.sha256(first).hexdigest(), "bytes": len(first),
            "byte_identity": True}
```
```python
    def physical_keys(self, split_name: str) -> frozenset[PhysicalKey]:
        ...
        return frozenset(
            group.physical_key for group in self.groups if group.split == split_name
        )
```
`SplitManifest.from_dict(payload, path=...)` (splits.py:442) validates the schema, duplicates, signature agreement and Hamilton allocation, so a tampered manifest is rejected before any key is used. The expected hash is committed in `generation-7-retention.json` (`runs/stage0-v23g7-seed42/splits.json`, 4,159,982 bytes).

**Admission and fp32 residency** (adapter.py:820-832, 844-850, 944-958). "The same admitted, preprocessed trajectories the trainer sees" means this chain, then the float32 CPU cast:
```python
                parsed_brutus = parse_brutus_file(path, root=self.data_root)
                record_key = record_key_from_brutus(folder, path.name)
                parsed = to_parsed_trajectory(record_key, parsed_brutus)
                outcome = evaluate_admission(
                    parsed,
                    blacklist=self.blacklisted_physical_keys,
                    remediation_quarantine=self._remediation_quarantine,
                    dt_out=reference.get("dt_out"))
                ...
                    pre = preprocess_trajectory(
                        parsed_brutus.times, parsed_brutus.positions,
                        parsed_brutus.velocities, parsed_brutus.masses)
                    inv = compute_invariants(pre.masses_ordered, pre.r0_gauge, pre.v0_gauge)
                    raw_ic13 = build_raw_ic13(
                        pre.masses_ordered, pre.r0_gauge, pre.v0_gauge, inv.E)
```
```python
            times_t = torch.tensor(
                np.asarray(cand.times, dtype=np.float64), dtype=self._dtype, device=self._device)
            ...
            normalized = normalize_ic13(cand.raw_ic13, stats)
            ic13_t = torch.tensor(normalized, dtype=self._dtype, device=self._device)
```
The blacklist is loaded by `load_blacklist_file(path)` (adapter.py:609-641); `pinn/train.py:482-495` shows how a relative `data.blacklist_path` resolves against the data root.

**Error handling:** typed exceptions as in adapter.py:131-143 (`DuplicateRecordError(ValueError)`, `CorpusPathEscape(ValueError)`, `EvidenceRedactionError(ValueError)`). Make the refusal class a `PermissionError` subclass as in 59-RESEARCH Pattern 1. Name it without a `Test` prefix (for example `SplitRefused`): the research name `TestSplitRefused` would be collected by pytest in the `.venv` convenience runner.

**Evidence redaction** (adapter.py:1005-1042 and target_frame_probe.py:1512-1524): fail closed if serialized evidence contains `str(Path.home())` or the resolved data root. See S4.

**No analog:** the `sys.addaudithook` attestation. The repository has no use of `addaudithook` (grep). Use 59-RESEARCH Pattern 1; the closest real test idiom for "spy on file access" is the `builtins.open` spy in `tests/phase39/test_prohibitions.py:432-462`.

**Global scans that apply to this file:** S1 (all three).

---

### 2. `pinn/verification/production_reference.py` (utility, transform)

**Primary analog:** `pinn/data/adapter.py::_scan_and_admit` (820-891), reused through `split_allowlist`. This module turns one admitted record into a `ReferenceTrajectory` (float64, pipeline frame `(r', u = t/T)`, inner pair located through the permutation).

**Frame fields to consume** (preprocessing.py:62-80):
```python
@dataclass
class PreprocessedTrajectory:
    masses_ordered: Any        # (3,) raw ordered masses (unscaled)
    permutation: Any           # (3,) canonical-order indices into the input
    r_com_ordered: Any         # (Nt, 3, 3) COM/boost-gauged + canonically ordered; NOT rotated, NOT scaled
    v_com_ordered: Any
    r0_gauge: Any
    v0_gauge: Any
    r_gauge: Any               # (Nt, 3, 3) full trajectory positions, scaled
    v_gauge: Any               # (Nt, 3, 3) full trajectory velocities, scaled
    R0: Any
    ...
    D: float
    T: float
    V: float
```
`permutation` comes from `_canonical_order`, which uses `np.lexsort` (preprocessing.py:112-123), and is applied at preprocessing.py:191-194 (`masses_ordered = masses[permutation]`), so ordered slot `k` holds file body `permutation[k]`. File body `j` sits in ordered slot `np.argsort(permutation)[j]`. The inner pair is file bodies 1 and 2 (indices 0 and 1, D-03).

**Known-permutation test fixture to copy for D-03** (tests/phase46/test_pairing_repair.py:46-47, 66-76): masses `(0.8, 0.6, 1.0)` give permutation `[2, 0, 1]`, a non-identity case:
```python
_MASSES = (0.8, 0.6, 1.0)
_EXPECTED_PERMUTATION = np.array([2, 0, 1], dtype=np.int64)
...
def _fixture_and_preprocessed():
    trajectory, _offset, _drift = make_com_offset_trajectory(masses=_MASSES, n_snapshots=8)
    preprocessed = preprocess_trajectory(
        trajectory.times_raw, trajectory.positions_raw,
        trajectory.velocities_raw, trajectory.masses)
    return trajectory, preprocessed
```

**IC13 and the normalizer to reproduce** (preprocessing.py:290-348; types.py:269-276). The recovery must produce this exact type:
```python
@dataclass
class NormalizationStats:
    slot_means: Any     # (12,) -- the 12 pre-energy IC13 slots
    slot_stds: Any
    e_scale: float

def normalize_ic13(raw_ic13, stats: NormalizationStats):
    """``z_in = tanh((z - mu) / (sigma + 1e-8))`` for the 12 mass/Jacobi slots
    and ``tanh(E / E_scale)`` for the final energy slot."""
    raw_ic13 = np.asarray(raw_ic13, dtype=np.float64)
    normalized_first_12 = np.tanh((raw_ic13[:12] - stats.slot_means) / (stats.slot_stds + 1e-8))
    normalized_energy = np.tanh(raw_ic13[12] / stats.e_scale)
    return np.concatenate([normalized_first_12, [normalized_energy]]).astype(np.float64)
```

**Where the already-normalized rows live in a checkpoint** (controllers.py:300-317): `ckpt["front_monitor"]["batch"]["data"]["tau_ic13"]` (shape `(8192, 14)`, column 0 is `tau`, columns 1-13 are normalized IC13), with `["data"]["record_keys"]`, `["data"]["masses"]`, `["data"]["targets"]`, `["data"]["times"]`. All are plain tensors and lists, so `torch.load(..., weights_only=True)` reads them.
```python
    return {
        "data": {
            "tau_ic13": data.tau_ic13.detach().cpu().clone(),
            "masses": data.masses.detach().cpu().clone(),
            "targets": data.targets.detach().cpu().clone(),
            "times": data.times.detach().cpu().clone(),
            "record_keys": [_record_key_payload(key) for key in data_keys],
            ...
```

**No analog:** the `atanh` least-squares recovery of `mu`, `sigma`, `e_scale` (the normalizer is only ever computed forward, preprocessing.py:327-339). Use 59-RESEARCH Pattern 6, assert the residual at most 1e-6 (D-35), commit the values with the checkpoint SHA-256.

**Global scans:** S1.

---

### 3. `pinn/verification/feasibility_scorecard.py` (config loader + rule functions)

**Primary analog (loader):** `pinn/training/config.py::load_frozen_r_ref_artifact` (166-275). Copy its shape: one read, JSON errors become `ValueError`, required-key set, exact `schema_version`, exact nested values, finite-positive checks, no recomputation, no writes.
```python
    required = {
        "schema_version", "valid", "r_ref", "raw_bin_means",
        "configuration", "provenance", "statistic", "statistic_convention",
    }
    missing = sorted(required.difference(payload))
    if missing:
        raise ValueError(f"R_ref artifact missing required keys: {missing}")
    if payload["schema_version"] != R_REF_ARTIFACT_SCHEMA_VERSION:
        raise ValueError(
            "R_ref artifact schema_version must be "
            f"{R_REF_ARTIFACT_SCHEMA_VERSION!r}; got {payload['schema_version']!r}"
        )
```
(config.py:184-201.) The schema-version constant and the relative-path constant live at config.py:32-33.

**Gap in that analog:** it rejects only *missing* keys. FEAS-01 needs unknown keys rejected too (59-RESEARCH Pattern 3). Copy the dotted-path rejection from `pinn/training/config_yaml.py::_map_section` (165-170) and its `ConfigKeyError` (58-68):
```python
    known = {f.name: f for f in dataclasses.fields(cls)}
    unknown = [k for k in raw.keys() if k not in known]
    if unknown:
        first = sorted(unknown)[0]
        dotted = f"{path_prefix}.{first}" if path_prefix else str(first)
        raise ConfigKeyError(dotted, f"unknown config key: {dotted}")
```
Apply it at every depth (tier table, budget block, L-BFGS block, G2 grid), not only the top level.

**Primary analog (rule functions):** `pinn/verification/candidate_eligibility.py` (whole file, 99 lines). A small pure module with `__all__`, module-level ordering constants, literal-`True` strictness and "always recompute, never trust a caller-supplied flag":
```python
CANDIDATE_ORDER: tuple[int, ...] = (42, 41, 43)
...
    facts = {name: record.get(name) is True for name in REQUIRED_STRUCTURAL_FACTS}
    facts["eligible"] = all(facts.values())
...
        # Always recompute the projection.  A caller-provided ``eligible``
        # field is not trusted because it could be stale or metric-derived.
```
Use the same style for `tier_of(E, eps_h)`, the counting rule (D-05), the decision rule (2 of 3, 12 of 16, branch a) and the budget rule (still-improving 25%/75%, one doubling, inconclusive).

**Boundary convention to mirror** (gate_metrics.py:253-268). Strict inequality, boundary passes, non-finite fails. D-04 tiers use `<=`; keep that explicit and test both sides of each threshold:
```python
def gate_verdict(eps_h: float) -> str:
    v = float(eps_h)
    if not math.isfinite(v):
        return "FAIL"
    if v > GATE_EPS_H_REJECT_THRESHOLD:
        return "FAIL"
    return "PASS"
```

**Hash and freeze:** `SCORECARD_SHA256 = sha256(raw file bytes)`, exported for run records. Raw-bytes hashing idiom: `verify_phase57_evidence.py:82-87` (`sha256_file`, 1 MiB chunks). Ordering proof: see S8.

**Global scans:** S1.

---

### 4. `pinn/verification/feasibility_scorer.py` (service, transform + autograd)

**Primary analogs:** `gate_metrics.py` (energy), `validation_gate.py` (network over a snapshot-time array), `controllers.py` (the trainer's own autograd velocity).

**Energy (use these two functions; they are the gate's own definition)** (gate_metrics.py:130-132, 180-200):
```python
def matched_plummer_hamiltonian_series(
    positions, velocities, masses, *, eps_inv: float = EPS_INV
) -> torch.Tensor:
...
def trajectory_eps_h(hamiltonian_series) -> float:
    """``eps_H = max_t |(H(t) - H(0)) / H(0)|`` for one trajectory.
```
`EPS_INV = 1e-10` (gate_metrics.py:59). Spec definition: `ctl_instruction.md:565-567` (no denominator floor; `H' = D*H`, so `eps_H` is invariant to the raw or scaled frame).

**DO NOT CALL** (D-30, GAP-59-02; a static test enforces it). `compute_trajectory_gate_metrics` (gate_metrics.py:211-222) is the finite-difference path:
```python
    velocity = finite_difference_velocity(positions, times)
    h_series = matched_plummer_hamiltonian_series(
        positions, velocity, masses, eps_inv=eps_inv
    )
    return TrajectoryGateMetrics(
        hamiltonian_series=h_series, eps_h=trajectory_eps_h(h_series)
    )
```
The production gate calls it at `validation_gate.py:257-259`. D-30 still wants a *labelled context column* with the finite-difference value: compose it explicitly from `finite_difference_velocity` (gate_metrics.py:84-122) + `matched_plummer_hamiltonian_series` + `trajectory_eps_h`, with `velocity_source = "finite_difference_context"`. The static test must therefore ban the names `compute_trajectory_gate_metrics` and `compute_validation_gate`, but not `finite_difference_velocity`.

**Network over a time array** (validation_gate.py:177-191, `build_gate_inputs` is public and reusable; 223-243 and 268-275 show the prior-mode bracket):
```python
def build_gate_inputs(times, ic13, *, dtype, device) -> torch.Tensor:
    t = torch.as_tensor(times, dtype=dtype, device=device).detach().reshape(-1)
    tau = (2.0 * (t / float(T_CHARACTERISTIC_TIME)) - 1.0).reshape(-1, 1)
    ic = torch.as_tensor(ic13, dtype=dtype, device=device).detach().reshape(13)
    ic_batch = ic.reshape(1, 13).expand(int(tau.shape[0]), 13)
    return torch.cat([tau, ic_batch], dim=1)
```
Keep the handler-less `try/finally` that restores the prior `model.training` mode (validation_gate.py:223-275, D-12). **Difference:** the gate runs under `torch.no_grad()`; the scorer must not, because it needs `dr'/du`.

**Autograd velocity, the trainer's own route** (controllers.py:1091-1095, 1173-1176; physics_residual.py:102-147):
```python
        def traj(u_scalar: torch.Tensor) -> torch.Tensor:
            tau = (2.0 * u_scalar - 1.0).reshape(1)
            tau_ic13 = torch.cat([tau, ic13], dim=0).unsqueeze(0)
            pos = self._model(tau_ic13, masses_t.unsqueeze(0))
            return pos.reshape(3, 3)
```
```python
        first, second = componentwise_du(anchor_ctx.traj, u_leaf)
        positions = torch.func.vmap(lambda s: anchor_ctx.traj(s).reshape(-1))(u_leaf)
        positions = positions.reshape(-1, 3, 3)
        velocities = first.reshape(-1, 3, 3)
```
`componentwise_du` computes first and second derivatives with nested `jacrev` under `vmap`; the forbidden summed-output VJP is documented at physics_residual.py:22-28. First-derivative-only `jacrev` halves the cost (59-RESEARCH Pattern 2). The network's public `forward(tau_ic13, masses)` returns COM-projected positions (network.py:210-228).

**Non-finite handling in evidence:** JSON string sentinels, not null (validation_gate.py:302-319 `json_safe_float`; target_frame_probe.py:1158-1183 `_json_safe`). See S4.

**Frame test fixture:** `tests/phase46/_fixtures.py::make_dual_frame_trajectory` (401-431) emits the same trajectory raw and scaled: `velocities_scaled = velocities_raw * T / D`, `times_scaled = times_raw / T`.

**Global scans:** S1. In particular do not probe device availability and do not give `--precision` a default (the scorer should take a `RuntimeSpec` from `resolve_runtime`).

---

### 5. `pinn/verification/two_kepler.py` and 6. `pinn/verification/nn_copy.py` (utilities, transform)

**No analog.** The repository has no Kepler propagation code and no nearest-neighbour search (grep of `pinn/`, `tests/`, `scripts/`; the only `arctan2` hits are in v1.3-era files). Use 59-RESEARCH Pattern 4 (Kepler f,g propagator, validated against RK4) for `two_kepler.py`.

Style analog for both: `pinn/verification/gate_metrics.py` (pure functions, explicit shape validation raising `ValueError`, `__all__`, no I/O). Typed "not applicable" exceptions: follow `FrameProbeUnavailable(Exception)` (target_frame_probe.py:193) and `IncompleteTrajectoryError(ValueError)` (fixture_loader.py:100).

**Construction convention to match** (`sampling_method.md:23-63`, step 6-7): bodies 1 and 2 are the inner binary about their own centre of mass, body 3 is the outer body about the system centre of mass; velocities are circular-speed values with later perturbation. The formula therefore inverts exactly that construction.

**Ties go to the lowest ID** (D-16, D-32): `RecordKey` and `PhysicalKey` are `@dataclass(frozen=True, order=True)` (types.py:113-136), so `min(candidates, key=lambda k: (distance(k), k))` and `sorted(keys)` give a deterministic lowest-ID tie-break with no custom comparator.

**Normalizer for `nn_copy.py`:** call `production_reference` (item 2), then `normalize_ic13` (preprocessing.py:342-348). Never recompute statistics from train and validation records (GAP-59-06).

**Global scans:** S1 (these two modules are numpy-only; D-37 allows stdlib, numpy, torch, yaml, `pinn.*`).

---

### 7. `pinn/verification/stage0_census.py` (batch analysis + CLI)

**Primary analogs:** `pinn/data/stage_scan.py` (population report, distributions, exit codes) and `pinn/verification/architecture_characterization_probe.py` (CLI, provenance, plain-language summary).

**Distribution report shape** (stage_scan.py:168-192):
```python
def _linear_quantile(values: tuple[float, ...], fraction: float) -> Any:
    if not values:
        return None
    position = (len(values) - 1) * fraction
    ...
def _distribution(values: Iterable[float]) -> dict[str, Any]:
    ordered = tuple(sorted(float(value) for value in values))
    return {"count": len(ordered), "min": ordered[0] if ordered else None,
            "quantiles": {...}, "max": ordered[-1] if ordered else None,
            "values": list(ordered)}
```
D-32 pins `np.percentile(..., q)` (linear), `np.array_split` into 16 bins and `np.median`; do not reuse `_linear_quantile` as the panel rule. (A one-line equality test against it is a cheap sanity check, since both are linear interpolation at index `(n-1)*q`.)

**Rule recorded verbatim in evidence** (target_frame_probe.py:922-927, `POPULATION_RULE`): make the panel rule a module constant, write it into `panels.json` together with the census hash, and have `--check` compare it.

**Module/CLI skeleton** (architecture_characterization_probe.py:40-95, 884-948): `from __future__ import annotations`, module docstring stating governance, `__all__`, `_REPO_ROOT = Path(__file__).resolve().parents[2]`, `_DEFAULT_EVIDENCE_ROOT` under `.planning/phases/59-.../evidence/`, `EVIDENCE_SCHEMA_VERSION`, `EVIDENCE_TOP_LEVEL_KEYS`, `_parse_args(argv=None)`, `main(argv=None) -> int`, `sys.exit(main())`. Provenance block to copy (lines 740-770): `argv`, `command`, `git_sha` (via `pinn.verify.git_head`, verify.py:361-384), worktree-dirty flag, torch and numpy versions, UTC timestamp.

**Deliberate difference:** `_new_run_dir` (architecture_characterization_probe.py:684-698, target_frame_probe.py:1497-1509) allocates a fresh UTC-stamped directory per run. FEAS-02 requires the census to **re-derive byte-identically**, so write fixed filenames under `evidence/census/` (atomic overwrite of identical bytes) and put no timestamp inside the compared bytes. Keep provenance (timestamp, argv) in a separate non-compared file or exclude it from the `--check` comparison.

**`--check` has no existing analog.** The nearest idioms are the no-write mode of `scripts/verify_environment.py:390-422` (`--check-only`, returns 0 without writing) and the build/verify split of `build_phase57_evidence.py` / `verify_phase57_evidence.py`. Implement `--check` as: recompute in memory, compare bytes to the committed file, print a stable `...-OK` token, return 1 on any difference.

**Alias-safe `N_in`, gold-grid agreement check, samples-per-inner-period flag:** no analog; 59-RESEARCH Pattern 5 and Q11. `measure_dt_out` (adapter.py:258-265, median of `diff(times)`) is the existing way to get the base cadence.

**Stage-0 population from the manifest:** a group is Stage 0 when `group.signature == ("hierarchical", 0, "UNASSIGNED")` (splits.py:575-587 decodes signatures; 590-614 builds them) and `group.split in ("train", "validation")`. `MISSING_GOLD` is an enum sentinel: compare with `is`, never with a string (59-RESEARCH Pitfall 5).

**Global scans:** S1.

---

### 8. `pinn/verification/dataset_survey.py` (batch analysis + CLI)

**Primary analogs:** `stage_scan.py::_sensitivity_sweep` (253-294) for a pre-declared diagnostic grid; `stages.py::classify_stage_label` (58-86) for predicate and precedence style.

**Pre-declared grid tagged as diagnostic** (stage_scan.py:290-294). Reuse the labelling convention for the `tau_L` fit-window sensitivity columns (1, 2, 3 time units):
```python
    return {
        "purpose": "diagnostic_only_reversible_grid",
        "multipliers": list(_SWEEP_MULTIPLIERS),
        "entries": entries,
    }
```

**Predicate and precedence style** (stages.py:68-86): degenerate inputs short-circuit first, strict inequalities, and an explicit evaluation order ("Stage 0 is evaluated BEFORE the collapsed Stage 1 branch", stages.py:14-15):
```python
    if record.variant != Variant.HIERARCHICAL or record.fidelity != Fidelity.BASE:
        return StageLabel.UNASSIGNED
    if _is_degenerate(record.l_ratio):
        return StageLabel.UNASSIGNED
    ...
    if record.E < _E_STAGE0_MAX and l_ratio > _L_RATIO_STAGE0_MIN and common:
        return StageLabel.STAGE_0
```
D-33 requires ascending precedence with Stage 6 as the residual, every label carrying its rule and source. Stage 0 and 1 are read from the manifest, never recomputed here. Do **not** edit or import-extend `classify_stage_label` (it is the sole Stage-0/1 classifier, GAP-39-08); the survey owns its own diagnostic predicates for Stages 2-6 and must say so in its docstring. The repository scans that guard the classifier cover only `pinn/data/` (tests/phase39/test_prohibitions.py:189-191, 244-251), so this file is outside them.

**`tau_L` oracle:** the spec snippet `ctl_instruction.md:1369-1435`. The vectorized numpy estimator is tested against a literal loop transcription of it (D-33). Key lines to transcribe literally:
```python
            dist_matrix = squareform(pdist(embedded_trajectory, 'euclidean'))   # :1398
            np.fill_diagonal(dist_matrix, np.inf)
            ...
            neighbor_indices = np.argmin(dist_matrix, axis=1)                    # :1406
            max_iter = N - (embedding_dim - 1) * delay - np.max(neighbor_indices)  # :1409
```
`scipy` is absent from `pinn-train`, so the transcription must replace `squareform(pdist(...))` by a numpy pairwise-distance loop; the snippet's `max_iter` collapses to one point on some records (`np.polyfit` raises `LinAlgError`), so the test must also cover the degenerate case returning "not computable" with a reason (GAP-59-04).

**DO NOT import** `pinn/data-handling/processing/rosenstein_lyapunov.py` (imports scipy and sklearn; v1.3-era, cross-check only). **Also do not write the strings `data-handling` or `data_handling` anywhere in executable source** (docstrings and comments are fine): `tests/phase38/test_prohibitions.py:313-` bans them in every `pinn/**/*.py`. See S1.

**Global scans:** S1.

---

### 9. `pinn/verification/artifacts/feasibility_scorecard_v1.json` (config artifact)

**Analog:** `pinn/verification/artifacts/r_ref_stage0.json`, top-level keys: `cases, configuration, invalidation_triggers, provenance, r_ref, raw_bin_means, schema_version, statistic, statistic_convention, valid`. Its writer is `gate04_train_free.py::write_r_ref_artifact` (911-941): frozen top-level key set, `json.dumps(..., sort_keys=True, indent=2)`, written via `atomic_write_text`, `valid` marker, provenance block with a source hash.

Copy: `"schema_version": "phase59-feasibility-scorecard/v1"` style string, `sort_keys=True, indent=2` plus trailing newline (so the SHA-256 is stable), a `valid`/`frozen` marker, and a `provenance` object. Content keys come from D-01..D-11, D-39 and GAP-59-02/05/07 (see 59-RESEARCH Pattern 3). Key names for the L-BFGS block should mirror production names: `lbfgs_history_size`, `lbfgs_max_iter`, `lbfgs_line_search` (config.py:668-670).

**Hand-off hazard:** `INVALIDATION_TRIGGERS` (gate04_train_free.py:103-115) lists `first_omega_0`. The G2 grid `{60, 120, 240, 480}` changes a trigger for the governed `R_ref`. Phase 59 only *freezes the grid as data*; do not touch `r_ref_stage0.json`.

---

### 10-11. `tests/phase59/__init__.py`, `tests/phase59/_fixtures.py`

**`__init__.py` analog:** `tests/phase46/__init__.py` (the single `_SKIP_PHRASE` constant, never re-spelled) and `tests/phase57/__init__.py` (docstring recording the runner command). Phase 59 can choose either skip discipline (Phase 39/46 localized `_require` skips) or deliberately-RED Wave 0 (Phase 57); both exist.
```python
_SKIP_PHRASE = "skipped Phase46 production symbol"
__all__ = ["_SKIP_PHRASE"]
```

**`_fixtures.py` building blocks to reuse (import, do not copy):**
- `tests.phase46._fixtures.make_dual_frame_trajectory` (401-431): raw and scaled encodings from one `D`/`T`; Lagrange equilateral. Use for offset, time-shift (`E = 2 sin(omega*dt/2)`) and frame-invariance tests.
- `tests.phase46._fixtures.make_pairing_confound_trajectory` (476-504) and `make_com_offset_trajectory` (507-544).
- `tests.phase39._fixtures.TinyCorpus` (a context manager building a miniature corpus under a `TemporaryDirectory`; layout and ids in its docstring, lines 174-196). **Its trajectories are rigid translations with constant velocities** (`_body_line`, lines 74-86: relative positions and all velocities are time-independent). They pass the admission chain (checked on a temporary copy: `evaluate_admission` returns `admit`, `eps_H` about 7e-16) but they are not orbits. Use it for layout, refusal-before-open, missing-root and admission-plumbing tests; never for a physics assertion (`N_in`, Kepler, energy drift).
- `tests.phase57._fixtures.build_run_controller` (182-218), `make_training_config` (140-179), `make_full_slot_source` (69-79): a real `RunController` on CPU float64 over a stub source.
- `tests.phase40._fixtures.make_stub_model` (161-176).

**New fixtures (no analog):**
- Eccentric Kepler orbit with time-varying kinetic energy (59-RESEARCH Pitfall 11): the Lagrange fixture has constant `H(t)`, so the velocity-scaling test cannot fail on it. Add a guard test that proves the Lagrange case is vacuous.
- Synthetic manifest with a test group, to prove refusal. Build it through the real writer so `SplitManifest.from_dict` accepts it (tests/phase39/test_splits.py:47-54 `_Source`, 286-312):
```python
class _Source:
    """Minimal admitted-set source consumed by the splitter."""
    def __init__(self, records):
        self._records = list(records)
    def admitted_records(self):
        return tuple(self._records)
...
            manifest = splits.write_split_manifest(
                _Source(records), run_dir=run_dir, seed=11, ratios=splits.SplitRatios())
```
(records are `SimpleNamespace(physical_key=..., record_key=..., stage_label=...)`, one base and one gold record per physical key.) Use 10 or more physical keys per signature so the Hamilton allocation at 0.8/0.1/0.1 leaves train, validation and test all non-empty (the writer test uses `range(10)`).

---

### 12. `tests/phase59/test_split_allowlist.py`

**Analogs:** refusal-before-open test text in 59-RESEARCH "Refusal-before-open test pattern"; the `builtins.open` spy at `tests/phase39/test_prohibitions.py:432-462`; manifest tamper tests at `tests/phase39/test_splits.py:495-511`:
```python
        bad_counts = json.loads(json.dumps(payload))
        bad_counts["signatures"][0]["counts"]["train"] += 1
        with self.assertRaisesRegex(ValueError, "Hamilton allocation"):
            splits.SplitManifest.from_dict(bad_counts)
```
Required cases: test-split id refused with `open` and `Path.read_text` patched to raise `AssertionError` (so passing proves nothing was opened); refusal precedes a missing-root `FileNotFoundError`; manifest hash mismatch rejected; audit hook records and blocks a withheld filename; `ALLOWED_CORPUS_READERS` grew by exactly one entry (S1).

---

### 13. `tests/phase59/test_static_guards.py`

Three detector families; copy each, and self-test each against an injected violating source (`tests/phase39/test_prohibitions.py::DetectorSelfTests`, 265-316), because a detector that cannot fail is a vacuous gate (59-RESEARCH Pitfall 11).

**(a) Executable-source extraction** (tests/phase39/test_prohibitions.py:89-108; same logic as `_executable_source` at tests/phase55/test_architecture_characterization.py:264-280). Import the functions, not the test classes, so unittest discovery does not load foreign `TestCase`s:
```python
from tests.phase39.test_prohibitions import executable_source, parses_corpus
```

**(b) AST import ban for `pinn.evaluate`, plus fresh-subprocess check** (tests/phase46/test_isolation.py:99-143 and 206-233). `_import_nodes_targeting_evaluator` covers `import pinn.evaluate`, `from pinn.evaluate import x`, `from pinn import evaluate` and relative forms. The subprocess variant:
```python
        code = (
            "import sys\n"
            "sys.path.insert(0, '.')\n"
            "import pinn.training.validation_gate\n"
            "bad = [m for m in sys.modules\n"
            "       if m == 'pinn.evaluate' or m.startswith('pinn.evaluate.')]\n"
            "print('present' if bad else 'absent')\n"
        )
        result = subprocess.run([sys.executable, "-c", code], capture_output=True,
                                text=True, cwd=str(ROOT), timeout=180)
```
Replace the imported module with each Phase-59 `pinn.verification.*` module.

**(c) Call-graph closure with a non-vacuity anchor** (tests/phase55/test_architecture_characterization.py:590-665). Use for "the scorer never reaches `compute_trajectory_gate_metrics`" and "no optimizer name appears":
```python
    assert reachable, "call-graph closure is empty — parser would green a vacuous gate"
    assert "_ic13_for_case" in reachable, (
        "known-reachable helper _ic13_for_case missing from the closure; "
        "a broken parser cannot satisfy D-03 by finding nothing"
    )
```
**Name sets to ban in every Phase-59 module** (D-26, D-27, D-30, D-35): `AdmittedSetAdapter`, `_build_admitted_sources`, `compute_trajectory_gate_metrics`, `compute_validation_gate`, `torch.optim`/`Optimizer`, `save`, `save_checkpoint`, `TorchSaveCheckpointStore`, and the import of `pinn.evaluate` and `pinn.train`. **Allowed:** `finite_difference_velocity` (only for the labelled context column). The DIAG-07 driver lives outside `pinn/`, so include its path explicitly in the scan list. It imports `RunController`, whose module contains `torch.optim.Adam` (controllers.py:2634), but the driver itself must never name it; scan the driver's own source, not the imported module's.

**(d) Import-surface ban** (D-37): Phase-59 modules import only stdlib, numpy, torch, yaml and `pinn.*`; assert no `scipy`, `pandas`, `sklearn`, `pytest`, `psutil` by walking `ast.Import`/`ast.ImportFrom`.

---

### 14. `tests/phase59/test_scorecard.py` and 15. `test_scorecard_rules.py`

**Frozen-key test** (tests/phase56/test_gate04_train_free.py:32-43, 452-481):
```python
FROZEN_TOP_LEVEL_KEYS = frozenset({
    "schema_version", "r_ref", "statistic", ...
})
...
            assert set(payload) == FROZEN_TOP_LEVEL_KEYS, sorted(payload)
            assert payload["schema_version"] == "phase56-r-ref-stage0/v1"
            ...
            assert not list(pathlib.Path(tmp).rglob("*.tmp.*")), (
                "the atomic writer must leave no temp residue"
            )
```
Add: unknown key at any depth rejected with its dotted path; SHA-256 of the committed file equals the recorded constant; thresholds equal the pre-registered golden values (0.01, 0.10, 1e-5, 1e-3, caps, 25%/75%, 10%, 5%, L-BFGS 10/strong_wolfe/50, cadence 100, G2 grid).

**Public-surface test** (tests/phase56/test_gate04_train_free.py:484-515, `PublicContractTests.test_gate_public_surface`): assert the names the Phase-60 harness imports exist (`hasattr` over a name list), because the scorer and baselines must be importable by Phase 60.

**Rule tests:** table-driven boundary tests (value exactly on, just below, just above each threshold), counting rule, decision rule and budget rule on synthetic curves.

---

### 16. `tests/phase59/test_scorer_known_errors.py` (and 17-20)

**Analog:** `tests/phase46/test_fixtures_selfcheck.py` (closed-form fixtures verified against inline formulas, no skips). Cases from D-10: reference against itself (`E = 0`, `h = 1`); constant offset (`e_sys` equals the imposed fraction exactly, `e_in = 0`); time shift on the Lagrange fixture (`E = 2 sin(omega*dt/2)`); velocity scale on the eccentric-Kepler fixture (vis-viva gives the analytic `eps_H`); inner-pair-only phase error (`e_in = 2 sin(phi/2)`, small `e_sys`); frame invariance (raw versus scaled dual-frame fixture, equal to 1e-9); pair tracking through synthetic permutations `(2,0,1)` and `(0,2,1)` (fixture in item 2).

Files 17-20 (`test_two_kepler`, `test_nn_copy`, `test_census`, `test_survey`) have no content analog; they follow the same closed-form style. `test_two_kepler`: propagator against RK4 at several eccentricities, identity at `t = 0`, unbound gives `NotApplicable`. `test_survey`: includes the literal-loop `tau_L` oracle (item 8).

---

### 21. `tests/phase59/test_diag07.py`

**Primary analog:** `tests/phase57/test_microbatch_equivalence.py` (38-116). It compares a monolithic backward with `_run_adam_step_microbatched` using `torch.allclose` on losses (`rtol=1e-6`) and per-parameter gradients (`rtol=1e-5`), across non-dividing microbatch sizes, with a `subTest` per case:
```python
                for p in parameters:
                    p.grad = None
                micro_terms, _gradient_stats = controller._run_adam_step_microbatched(
                    batch, anchor_ctx, weights, parameters,
                    microbatch_size=microbatch_size, want_diagnostics=False,
                )
```
Use the same shape for "per-term gradient vectors against a finite-difference check on `make_stub_model`" and "microbatched equals unchunked within 1e-6".

**Non-interference analog** (tests/phase46/test_isolation.py:324-340): parameters bitwise identical and `p.grad is None` after the pass:
```python
        before = [p.detach().clone() for p in model.parameters()]
        ...
            self.assertTrue(torch.equal(old, new), f"parameter {index} was mutated ...")
        for index, p in enumerate(params):
            self.assertIsNone(p.grad, f"parameter {index} holds a populated gradient")
```
Extend with: `runs/` hash manifest unchanged (reuse the retention-manifest idea, item 23) and the registry test (`best.pt` has `counters.global_step == 900`, SHA-256 equals `generation-7-retention.json`).

**Loading a driver that lives under `.planning/`** (tests/phase57/test_evidence_ledger_v2.py:21-27, 45-60): `importlib.util.spec_from_file_location` + `module_from_spec` + `exec_module`, then `mock.patch.object(module, "REPO_ROOT", tmp)` to relocate it.

---

### 22. `tests/phase39/test_prohibitions.py` (MODIFY lines 40-50)

Current text (lines 40-50):
```python
# GAP-39-02: the exact permitted corpus-reader set. ``adapter.py`` is the new
# production reader (may not exist yet); ``fixture_loader.py`` is the sole
# retained Phase 38 probe exception. ``target_frame_probe.py`` is the Phase 46
# CONF-01 probe exception (D-01/D-03, plan 46-04): it reads parsed corpus
# arrays as provenance/positive-control arms through the adapter module's own
# containment-enforcing parse seams, never as a second training-data path.
ALLOWED_CORPUS_READERS = {
    "pinn/data/adapter.py",
    "pinn/verification/fixture_loader.py",
    "pinn/verification/target_frame_probe.py",
}
```
Change: add exactly `"pinn/verification/split_allowlist.py",` and extend the comment with three or four lines in the same voice (Phase 59 D-35: the one allowlist-bound reader; per-file seams only; never instantiates the adapter). Precedent: Plan 46-04 added `target_frame_probe.py` the same way. Pair it with the `tests/phase59` assertion that the set grew by exactly this one entry and that no other Phase-59 module has a corpus token.

---

### 23-24. `evidence/verify_phase59_evidence.py` and `evidence/manifest.json`

**Analog:** `.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/verify_phase57_evidence.py` (1272 lines) and `build_phase57_evidence.py`.

**Bootstrap so a script under `.planning/` can import `pinn`** (verify_phase57_evidence.py:20-26):
```python
if __package__ in (None, ""):
    _ROOT = Path(__file__).resolve().parents[4]
    if str(_ROOT) not in sys.path:
        sys.path.insert(0, str(_ROOT))
```
**Fail-closed helpers to copy** (lines 74-102): `VerifyError`, `fail(message)`, `sha256_file(path)` (1 MiB chunks), `repo_path(raw, what=...)` (rejects escape and symlinks), `load_json`, `HEX64 = re.compile(r"^[0-9a-f]{64}$")`.

**Git helpers** (lines 596-663):
```python
def is_ancestor(ancestor: str, descendant: str) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=str(REPO_ROOT), capture_output=True, check=False,
    )
    return result.returncode == 0
```
`assert_fingerprint_inputs_clean()` (618-653) runs `git status --porcelain -- <paths>` and fails on any dirty line; it is the model for the `scorecard-frozen` check (scorecard file committed and clean, its commit an ancestor of every census, baseline and survey evidence commit; SCOPE-42).

**Retention check to reuse for the DIAG-07 registry and for "`runs/` unchanged"** (`assert_generation_seven_retained`, 506-593): per-entry `{path, role, size_bytes, sha256}` validation, `sha256_file(path) != digest` failure, on-disk file set equals manifest set (catches an extra or missing file), and `git ls-files --cached` equals the manifest paths. Retention entries look like:
```json
{"path": "runs/stage0-v23g7-seed42/checkpoints/best.pt", "role": "run-artifact",
 "size_bytes": 11251663, "sha256": "21c69f2d9f975689..."}
```
**Subcommand dispatch** (1248-1272): a single positional `command` with `choices`, a dict of `cmd_*` functions, `except Exception as exc: print(str(exc), file=sys.stderr); return 1`, and a stable `...-OK` token per command. Planned subcommands: `scorecard-frozen`, `pair-tracking`, `census`, `baselines`, `survey`, `diag07`, `guardrails`, `final`.

**Manifest** (`build_phase57_evidence.py:389-401`): `{"schema": "phase57-evidence-manifest/v1", "files": {relative_path: sha256}}` written by `atomic_json` (`json.dumps(..., sort_keys=True, indent=2, ensure_ascii=True) + "\n"`, lines 66-92). Phase 59 adds `size_bytes` per file (59-RESEARCH layout). Evidence `README.md` analog: `.planning/phases/57-.../evidence/README.md` ("required records" contract).

---

### 25. `evidence/diag07/<driver>.py` (JX-1 executed half, JX-2, JX-3, JX-4, JX-5 split, JX-10)

**Primary analog:** the Phase-58 replay script (`pinn_instruction/markdown_conversion/framework-specs/trainex-r4/research_package/v2.3-closure-evidence-bundle.md:304-392`, script SHA-256 `0e1297fa...`). Skeleton to follow, with the changes marked:
```python
REPO = Path("<home>/Desktop/3_body_problem/.worktrees/trainex")   # CHANGE: --code-root, inserted FIRST
sys.path.insert(0, str(REPO))
...
def build_controller(run_name: str, tmp: Path) -> RunController:
    run_dir = REPO / "runs" / run_name
    config = load_config(REPO / "configs" / f"{run_name}.yaml")
    shutil.copy2(run_dir / "splits.json", tmp / "splits.json")
    train_source, validation_source = _build_admitted_sources(config, tmp)   # DO NOT COPY: opens test files
    runtime = resolve_runtime(config.run.precision, config.run.device)
    model = build_network(ArchitectureSpec(seed=int(config.run.seed)), dtype=runtime.dtype, device=runtime.torch_device)
    s_h = json.loads((run_dir / "training_metadata.json").read_text())["s_h"]
    return RunController(
        model, train_source, validation_source, config,
        ScheduledWeights(int(config.stage.n_adam)), GradClipper(),
        CollocationSampler(2, np.random.default_rng(int(config.run.seed) + 1000)),
        StageExitMachine(config), TorchSaveCheckpointStore(tmp / "store"), runtime,   # CHANGE: refusing store
        s_h=float(s_h), rng=np.random.default_rng(int(config.run.seed)),
        replay_count=int(config.stage.replay_count),
        r_ref=load_frozen_r_ref_artifact(REPO / config.loss.r_ref_artifact_path),
    )
...
            payload = torch.load(path, map_location="cpu", weights_only=True)
            controller.load_state_dict(payload)
            stats = controller._evaluate_front_monitor()
```
The reference values for JX-10 are in the same bundle (lines 401-405): `best.pt` global_step 900, front 1, `prefix_through_front` 0.7277; `step-000951.pt` front 2, 1.1891; init front 0, 0.8754 (MPS float32).

**Replace the two data/checkpoint seams:**
- *Source:* `_build_admitted_sources` (pinn/train.py:498-533) builds `AdmittedSetAdapter`, which parses every corpus file. Substitute allowlisted sources built from `split_allowlist`. Two precedents for a non-adapter source:
  - hand-written accessor class: `_SyntheticStageQuery` (phase57_production_conformance.py:212-289), whose method set is the minimum `RunController` and `build_stage_batch` need (`blacklisted_physical_keys`, `gold_numeric_stage_count`, `has_stage`, `records_at`, `records_at_or_below`, `record_keys`, `get`, `n_snapshots`, `snapshot_times/positions/velocities`, `acceleration_magnitudes`, `stage_label`, `is_blacklisted`);
  - **cheaper alternative found while mapping:** `pinn.data.splits.StageIndex(records)` (splits.py:138-139, 209-224) accepts records that carry their own accessor attributes (`snapshot_times`, `snapshot_positions`, `snapshot_velocities`, `acceleration_magnitudes`, `k0`, `uabs0`, `dt_out_measured`, `n_snapshots`, `ic13`, `masses`, `stage_label`, `record_key`, `physical_key`). Usage precedent: `tests/phase47/test_conf02_s_h_pipeline.py:244-257`. `StageIndex.from_split` (splits.py:170-186) is **not usable** because it requires `source_physical == manifest_physical`, i.e. all 7,606 groups including test.
- *Checkpoint store:* define a local store whose `save`, `save_rolling`, `save_best`, `save_anchor` raise. The narrow protocol is `CheckpointStore` (checkpoint.py:141-154: `save`, `load_latest`, `rollback`); `EmptyCheckpointStore` (checkpoint.py:63-116) lists the wider surface the curriculum controller may call (`save_rolling`, `save_best`, `save_anchor`, `promote`, `record_disposition`, `load_checkpoint`, `fallback_scan`, `should_checkpoint`). The driver never calls `run_stage`, so a store whose write methods all raise is safe; make `should_checkpoint` return False. Do not import `TorchSaveCheckpointStore` (banned by the D-27 static test).

**Controller construction on a duck-typed source (CPU float64 cross-check)** (phase57_production_conformance.py:297-324): `resolve_runtime("float64", "cpu")`, `build_network(ArchitectureSpec(seed=...), dtype=runtime.dtype, device=runtime.torch_device)`, then `RunController(model, source, source, config, scheduled, clipper, sampler, exit_machine, store, runtime, s_h=1.0, rng=..., replay_count=..., r_ref=...)`. Primary runtime is MPS float32 (`resolve_runtime("float32", "mps")`); `resolve_runtime` accepts only those two pairs (runtime.py:44-57).

**JX-1 per-term gradients:** the trainer already computes them, but keeps only norms. Mirror `RunController._run_adam_step_microbatched` (controllers.py:1822-2017). Key lines:
```python
        def _accumulate_raw_grad(
            name: str, term_scalar: torch.Tensor, *, retain_graph: bool,
        ) -> None:
            grads = torch.autograd.grad(
                term_scalar, parameters, create_graph=False, retain_graph=retain_graph,
                allow_unused=True, materialize_grads=False,
            )
            acc = raw_grads[name]
            for i, g in enumerate(grads):
                if g is not None:
                    acc[i] = acc[i] + g.detach()
```
```python
            row_weight_chunk = (
                w_n[bin_idx_chunk]
                / (float(n_bins) * r_ref * bin_counts[bin_idx_chunk])
            )
            phys_chunk = (row_weight_chunk * rbar_chunk).sum()
```
(1874-1884, 1918-1922.) `raw_grads` is keyed by `_GRAD_STAT_TERMS` names `data, ic, phys, energy, angmom` (controllers.py:142-148). Keep the full vectors (flatten per term) instead of norms, apply the scheduled weights (`self._scheduled_weights.current(epoch)`, controllers.py:2058) for `g_tot = sum_k lambda_k g_k`, and cross-check the resulting norms against `_run_adam_step_microbatched(..., want_diagnostics=True)` (that call does backward but no optimizer step) and against the logged values (`grad_norm_raw_ic` 3.03e6, `grad_norm_raw_phys` 109.0, `grad_norm_raw_data` 1.46 at step 900, from `runs/.../logs/train.log.jsonl`). Position and velocity IC split: `ic_anchor_loss` is `l_r + beta_v * l_v` (loss_catalog.py:279-294), so the two halves are the two terms of that sum.

**G1 share (GAP-59-05, D-34):** no analog in the repository (no code reads `exp_avg_sq`). Read the moments straight from the loaded payload: `payload["optimizer"]["state"][i]` with keys `exp_avg`, `exp_avg_sq`, `step`, indexed in `model.parameters()` order (Adam is constructed over `self._model.parameters()`, controllers.py:2634-2639), `beta2 = cfg.opt.adam_betas[1]`, `eps = cfg.opt.adam_eps` (config.py:664-665). Assert `len(state) == number of parameters` and matching shapes. Loading the payload with `controller.load_state_dict` only stores the optimizer state as pending (controllers.py:863-864) and constructs no optimizer, which is what D-27 needs. Verify the formula on a toy two-parameter case with a known answer first.

**JX-2 time draws:** `architecture_characterization_probe.stratified_collocation_times(n_bins=16, per_bin=256, rng=...)` (412-477) and `bin_mean_residuals` (480-509) give the ratified 4,096-row stratified draw and the bin means, with an explicit `np.random.Generator`.

**JX-3 inputs:** `validation_gate.build_gate_inputs` (177-191). **JX-4 true acceleration scale:** `softened_acceleration` (physics_residual.py:193-231). **JX-5 split at the default architecture:** `architecture_characterization_probe.measure_case` (310-395) already measures `||r'||, ||v'||, ||a'||, ||F_grav||` at initialization through the trainer's own functions; it does not cover IC error, mixed derivatives or skip contributions.

**Memory (D-25):** use `_evaluate_front_monitor` (controllers.py:1027-1070) and `_collocation_chunk_raw` (1746-1770) with `opt.adam_microbatch_size` (256); never write a full-batch 4,096-row evaluation. Record `resource.getrusage(RUSAGE_SELF).ru_maxrss` (the footprint reader is unreliable on this OS, 59-RESEARCH Pitfall 12).

**Code identity (D-36):** prefer `git archive 629b1a6c pinn configs | tar -x -C <tmp>` (reads objects only, writes nothing to `.git`) over `git worktree add --detach`; either satisfies D-23. After `sys.path.insert(0, code_root)`, assert `Path(pinn.__file__).resolve()` lies under `code_root`. Pass an explicit data root (see item 1 hazard).

**Evidence per result (D-24):** the command, checkpoint SHA-256, and the reading supported or falsified. Provenance block: copy `architecture_characterization_probe._provenance` (740-770).

---

### 26. `docs/work/designs/milestone_v2.4/59-read-only-baseline-scorecard/<YYYY-MM-DD>-feasibility-scorecard.md`

**Analog:** `docs/work/designs/milestone_v2.3/58-verdict-traceability-close/2026-10-03-phase-58-diag-06-verdict-packet.md`. Frontmatter (required by `docs/README.md`, which must be read in full before creating the file):
```yaml
---
status: active
purpose: design
created: 2026-10-03
milestone: v2.3
phase: 58-verdict-traceability-close
retirement_trigger: the owner's checkpoint-⑤ verdict is recorded in Phase 58 artifacts and the v2.3 milestone closes
---
```
Opening style to copy: `**Audience:**`, `**This document is:**`, `**This document is not:**`, then numbered plain-language sections before any detail. Every Phase-59 result artifact opens with a plain-language summary (CONTEXT "Specifics"). Use `milestone: v2.4`, `phase: 59-read-only-baseline-scorecard`, a date-prefixed filename, and `status` from the allowed list only.

---

## Shared Patterns

### S1. Repository-wide scans that every new `pinn/**/*.py` module must pass (NEW; not in 59-RESEARCH)

**Apply to:** items 1-8 (all new modules under `pinn/`). Executable source means docstrings and comment lines are stripped (tests/phase39/test_prohibitions.py:89-108); every other string literal counts.

| Scan | Where | Forbidden in executable source | Consequence for Phase 59 |
|------|-------|-------------------------------|--------------------------|
| A. Sole corpus reader | `tests/phase39/test_prohibitions.py:67-68, 199-205` over `discover_pinn_modules()` (171-186) | tokens `brutus_hierarchical`, `brutus_standard`, `ic_hierarchical`, `ic_standard`; a `glob(`/`rglob(` call whose arguments contain `.txt` | Only `split_allowlist.py` may name them, and only after the one-entry edit (item 22). Import `BRUTUS_FOLDER_TABLE` instead of re-spelling folder names elsewhere. |
| B. Precision/availability | `tests/phase38/test_prohibitions.py:297-311` over `_discover_phase38_modules()` (107-) | substrings `set_default_dtype`, `is_available`, `add_argument("--precision", default=` (also with single quotes) | No MPS availability probe in `pinn/` code (the DIAG-07 driver is outside `pinn/` and exempt). A CLI `--precision` must be `required=True` or absent. |
| C. v1.3-era references | `tests/phase38/test_prohibitions.py:313-` | `basic_architecture`, `data-processing-pipeline-full`, `data_processing_pipeline_full`, `data-handling`, `data_handling` | The survey may mention the legacy estimator only in a docstring or comment, never in a string literal or path. |

Also: do not add imports to `pinn/verification/__init__.py` (its docstring says rung modules are imported on demand). Phase-40's scan covers only `pinn/training/*.py` and Phase-39's classifier scan only `pinn/data/`, so neither constrains `pinn/verification/`.

**Cheap pre-flight for every module-writing plan** (read-only, one line): run the three scans plus `tests.phase39.test_adapter tests.phase46.test_isolation` (59-RESEARCH baseline: 175 tests OK in 1.5 s).

### S2. One choke point for corpus access (D-26, D-35)

**Source:** item 1. **Apply to:** items 2, 4-8, 25. No other Phase-59 file may import `parse_brutus_file`, `BRUTUS_FOLDER_TABLE`, or open a path under the data root. Everything else consumes `ReferenceTrajectory` objects or the allowlisted source. Refusal happens before a path is built; the audit hook is the second, independent line.

### S3. Velocity-source rule for `eps_H` (D-30)

**Source:** items 3-4. One label per computed value: `"autograd"` (networks), `"analytic"` (two-Kepler formula), `"brutus"` (neighbour copy), `"finite_difference_context"` (generation-7 continuity column, never tier-defining). A sanity check that catches the finite-difference mistake: a Brutus reference scored against itself with its file velocities must give `eps_H` of order 1e-14; the finite-difference value on the same data is 4.7e-2 to 3.8e-1 (59-RESEARCH C-3, GAP-59-02).

### S4. Evidence writing

**Apply to:** items 1, 4, 7, 8, 23-25.
- **Atomic write:** `pinn.training.atomic_io.atomic_write_text(path, content)` (atomic_io.py:41-64: tmp + fsync + `os.replace` + directory fsync + finally-unlink). Do not copy the private `_atomic_write` clones in `overfit_probe.py:88-94` or `stage_scan.py:463-480`.
- **Evidence root guard:** refuse a root inside `simulation_data/` or the corpus root (`_reject_evidence_root`, target_frame_probe.py:1474-1494; `_reject_dataset_evidence_root`, overfit_probe.py:79-85).
- **Redaction:** fail closed if serialized bytes contain `str(Path.home())` or the resolved data root; record the `data_root_source` label, not the path:
```python
def _guard_serialized_bytes(raw, *, data_root=None):
    home = str(Path.home())
    if home and home in raw:
        raise EvidenceRedactionError(
            "serialized frame-probe evidence contains the host home prefix")
    if data_root is not None:
        root_str = str(Path(data_root).resolve())
        if root_str in raw:
            raise EvidenceRedactionError(
                "serialized frame-probe evidence contains the resolved data root")
```
(target_frame_probe.py:1512-1524; same idea in adapter.py:1005-1042.) Also reduce paths with `_reduce_path` (1560-1571) and record the invocation with `_reduced_invocation` (1574-1584).
- **Non-finite values:** string sentinels `"NaN"`, `"Infinity"`, `"-Infinity"`, never `null` (target_frame_probe.py:914-918, 1158-1183; validation_gate.py:302-319). A failing arm with a non-finite `eps_H` must stay visible.
- **Serialization:** `json.dumps(payload, sort_keys=True, indent=2) + "\n"` everywhere, so hashes are stable.
- **Plain-language summary first:** `_summary_markdown(raw)` (architecture_characterization_probe.py:784-856) pairs `raw.json` with `summary.md`; Phase 59 summaries must open in plain language.

### S5. CLI shape and exit codes

**Apply to:** items 7, 8 and any Phase-59 `main`. `main(argv=None) -> int`; `if __name__ == "__main__": sys.exit(main())`; argparse; validate numeric arguments in `main` (argparse `type=float` accepts NaN/Inf: stage_scan.py:613-637); a stable one-line status on stdout; non-zero return on failure with the reason on stderr. Template: stage_scan.py:573-709 and architecture_characterization_probe.py:884-948.

### S6. Test conventions and commands

**Apply to:** items 10-21.
- `unittest.TestCase` only; no pytest, scipy, pandas, sklearn or psutil in `pinn-train` (D-37).
- Quick: `<home>/miniforge3/bin/conda run -n pinn-train python -B -m unittest tests.phase59.<module> -v`
- Full: `... python -B -m unittest discover -s tests/phase59 -p 'test_*.py' -v`
- Long runs: call `<home>/miniforge3/envs/pinn-train/bin/python` directly (`conda run` buffers output).
- Do not put `tests/phase57` discovery in a Phase-59 regression command (a pre-existing footprint test fails on this OS, 59-RESEARCH Pitfall 12); name adjacent suites explicitly.
- Dataset-free tests build their data under `TemporaryDirectory`; no test writes under `simulation_data/`.

### S7. Frozen-artifact discipline (SCOPE-42)

**Apply to:** items 3, 9, 23. Strict load (items 3), exact key set (item 14), SHA-256 of raw bytes recorded in committed state (not `/tmp`), and an ancestry check proving the scorecard commit precedes every dependent evidence commit (`is_ancestor`, item 23). A threshold edit after any rung has run is owner-routed.

### S8. Percentile, bin and tie rules (D-32)

**Apply to:** items 7, 8. `np.percentile(x, q)` (linear), distance `|N_in - q|`, `np.array_split` of the `(N_in, id)`-sorted list into 16 bins (sizes 114 for the first 4, 113 for the other 12), `np.median` of each bin, ties to the lowest id through the ordered `RecordKey` (see items 5 and 6). The three single-system picks additionally require at least 3 base-grid samples per inner period; the 16-system family and the 227-system validation panel are unrestricted, with the flag reported.

---

## No Analog Found

Planner should use the cited 59-RESEARCH section instead.

| Component | Role | Data Flow | Reason | Use |
|-----------|------|-----------|--------|-----|
| `sys.addaudithook` attestation inside `split_allowlist.py` | guard | event-driven | no `addaudithook` anywhere in the repository | 59-RESEARCH Pattern 1 (empirically: `Path.read_text` and `numpy.loadtxt` both raise the `open` event) |
| Kepler f,g propagator and two-orbit assembly (`two_kepler.py`) | utility | transform | no orbital-element or Kepler code in `pinn/`, `tests/`, `scripts/` | 59-RESEARCH Pattern 4 |
| Nearest-neighbour copy (`nn_copy.py`) | utility | lookup | no nearest-neighbour search code | plain numpy over normalized IC13 |
| Alias-safe `N_in` (gold-grid unwrap) | utility | transform | no angle-unwrapping code outside v1.3-era files | 59-RESEARCH Pattern 5 |
| IC13 normalizer recovery (atanh least squares) | utility | transform | the normalizer is only computed forward (preprocessing.py:327-348) | 59-RESEARCH Pattern 6 |
| Vectorized `tau_L` | utility | transform | only the scipy-based spec snippet and the sklearn-based legacy file | spec snippet as the oracle (item 8) |
| Adam-preconditioned share (G1) | utility | transform | no code reads `exp_avg` or `exp_avg_sq` | GAP-59-05 formula; toy-case test first |
| `--check` byte-identical re-derivation | CLI mode | batch | no existing `--check`; only `--check-only` in `scripts/verify_environment.py:390-422` | item 7 description |
| Eccentric-Kepler test fixture | test fixture | transform | the only closed-form fixture is the constant-`H` Lagrange orbit | 59-RESEARCH Pitfall 11 |

---

## Hazards found while mapping (beyond 59-RESEARCH C-1..C-12)

1. **Three global scans, not one (S1).** The research lists only the Phase-39 corpus-token scan. The Phase-38 scans (`is_available`, defaulted `--precision`, `data-handling` strings) also run over every new `pinn/**/*.py` module, and would fail a survey module that spells the legacy path in a string.
2. **`StageIndex(records)` can replace a hand-written duck-typed source** (item 25), and `StageIndex.from_split` cannot be used under D-26 because it requires the full 7,606-group population.
3. **`default_data_root()` needs a `.git` directory** (adapter.py:603-606). A `git archive` snapshot has none; pass an explicit root and record the label.
4. **Two nearby analogs open test files.** `target_frame_probe._run_probe` (line 1611, `AdmittedSetAdapter`) and the Phase-58 replay script (`_build_admitted_sources`). Both are structurally good templates; copy the structure, not the data seam.
5. **`_build_control_reader` globs directory names** (target_frame_probe.py:1127-1133). Names only, no file contents, but Pitfall 1's "any glob in a Phase-59 module" warning applies and scan A flags `.txt` globs.
6. **pytest idioms in analog tests.** `tests/phase55/` and parts of `tests/phase56/` use pytest fixtures; the `pinn-train` environment has none (S6).
7. **`RunController.__init__` builds a monitor from `train_source`** before `load_state_dict` replaces it (controllers.py:819-820, 909-956, 958-1024), so the allowlisted train source must support the full batch-builder accessor set (`gold_numeric_stage_count`, `n_snapshots`, `snapshot_times`, `snapshot_positions`, `acceleration_magnitudes`, `has_stage`, `records_at`, `records_at_or_below`; batches.py:106-152, 259-287) even though the restored monitor makes the constructed one irrelevant.
8. **`runs/stage0-v23g7-seed42/**` is force-tracked** (32 files), so `git status runs/` detects a modified tracked file. It does NOT detect a newly created file, because `runs/` is gitignored; catch that with the on-disk-set-equals-manifest-set comparison in `verify_phase57_evidence.py:563-569` (or `git status --ignored`), together with the retention-manifest hash comparison.
9. **Refusal exception name.** Avoid a `Test` prefix (pytest collection in the convenience runner).
10. **G2 grid versus `INVALIDATION_TRIGGERS`** (item 9): freezing `first_omega_0` values as data is safe; applying one is Phase 60-61 and invalidates the governed `R_ref`.
11. **A baselines runner is implied but not listed.** 59-RESEARCH's real-corpus check row names `baselines --check` and a `baselines` evidence subcommand, but its recommended structure has only `two_kepler.py` and `nn_copy.py` (pure functions) and no module that scores them with the scorer over the panels and writes `evidence/baselines/`. Decide in the plan whether each of the two modules gets a `main(argv=None)` or a small `baselines.py` runner does; the CLI, `--check` and evidence pattern is item 7 either way. If a runner is added it is a ninth `pinn/verification/` module and falls under S1 and S2 (it must consume `ReferenceTrajectory` objects, never the corpus).

## Uniformity checks to grep across the plans (plan-checker aid)

- Every plan that creates a `pinn/**/*.py` module states S1 (all three scans) in its acceptance criteria.
- Every task that writes evidence names the redaction guard and the `atomic_write_text` call (S4).
- Every static detector has a paired injected-violation self-test (item 13).
- Every plan that touches `eps_H` names the velocity-source label (S3) and forbids `compute_trajectory_gate_metrics`.
- Every long command uses the `pinn-train` interpreter path (S6) and no `-I` for `pinn` imports (D-37).
- Exactly one entry is added to `ALLOWED_CORPUS_READERS`.

## Metadata

**Analog search scope:** `pinn/` (data, training, verification, top-level modules), `tests/phase38`, `phase39`, `phase40`, `phase46`, `phase47`, `phase55`, `phase56`, `phase57`, `.planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/`, `scripts/`, `configs/`, `docs/work/designs/`, and the framework specs (`ctl_instruction.md`, `sampling_method.md`, `trainex-r4-*`).
**Files read in full or in targeted ranges:** about 45; no corpus data file and no `splits.json` was opened.
**Pattern extraction date:** 2026-10-11
