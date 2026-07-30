# Phase 47: Frame Completion & S_H Pipeline - Pattern Map

**Mapped:** 2026-07-29
**Files analyzed:** 11 touched files + 1 new test directory + 1 new persisted artifact
**Analogs found:** 13 / 13 (every touched file has a same-file, same-class, or sibling-file analog — this phase is a conformance repair inside an already-built codebase, not new-feature construction)

**All line numbers below were re-verified against live source in this session** (`grep -n` + targeted `Read`), not copied from `47-CONTEXT.md` or the 2026-07-28 audit report. One citation drift was confirmed and is called out explicitly in Pattern Assignment 6.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `pinn/data/adapter.py` (residency swap, CONF-09: `positions=`/`velocities=`/two `.shape[0]` sites) | data/admission service | batch, in-place edit | itself — `_scan_and_admit` candidate construction (`:861-876`) | exact (3-line self-edit) |
| `pinn/data/adapter.py` (K0/Uabs0 capture, CONF-02 pass 1) | data/admission service | batch, two-pass collect | itself — `raw_ic13_population`/`trajectory_energies` capture (`:801`, `:873-874`) | exact (same method, same shape) |
| `pinn/data/types.py` (`AdmittedRecord` gains `k0`/`uabs0` float64 fields) | model / dataclass | CRUD (record fields) | itself — `E`/`l_ratio`/`Q`/`min_separation` fields (`:230-233`) | exact (same dataclass) |
| `pinn/data/splits.py` (`StageIndex.k0(key)` / `.uabs0(key)` accessors, D-12) | model / repository accessor | request-response | itself — `snapshot_positions`/`snapshot_velocities` via `_source_value` (`:209-233`) | exact (same class, established delegation) |
| `pinn/loss_catalog.py` (component-returning extraction, D-11) | service (physics/loss) | transform | itself — `_matched_plummer_hamiltonian` (`:140-157`) | exact (self-refactor: factor out already-separate locals) |
| `pinn/training/validation_gate.py` (re-ratify `RATIFIED_VALIDATION_FRAME`, D-05) | config/constant + validation gate | request-response (admission check) | itself — `FrameConvention`/`COHERENT_FRAME_PAIRS`/`_validate_frame` (`:74-124`, `:453-476`) | exact |
| `pinn/training/controllers.py` (`eps_h` source + `_AnchorContext` field, D-19/20/21) | controller | event-driven (per-batch training step) | itself — `_build_anchor_context` (`:447-500`) | exact |
| `pinn/train.py` (S_H pipeline call + `training_metadata.json` write + `RunController` wiring) | orchestration / run-setup | batch (run setup, once, before step 1) | itself — `_build_admitted_sources`/`_build_sources` (`:381-424`) + `config.yaml` freeze (`:746-752`) | role-match (new artifact, existing write idiom) |
| `run_dir/training_metadata.json` (new artifact, D-16) | config / persisted-data artifact | file I/O, atomic write + validate-on-read | `pinn/training/config_yaml.py::freeze_resolved_config` (`:276-295`) + `pinn/data/splits.py::write_split_manifest`/`SplitManifest.from_path` (`:773-789`, `:555-559`) | role-match |
| `tests/phase46/test_pairing_repair.py` (corrected in place, D-06) | test | request-response (unit assertions) | itself | exact (in-place correction, not superseded) |
| `tests/phase47/*.py` (new, assembly-boundary + regression tests) | test | request-response | `tests/phase46/test_pairing_repair.py` fixture/oracle pattern (`_adapter` `:155-163`, `_resident_fixture` `:166-195`) | role-match |
| `pinn/data/preprocessing.py` (comment-only: stale `r_com_ordered` docstring note) | data/transform service | transform | itself — `preprocess_trajectory` (`:174-221`) | exact (docstring only, no logic change) |
| `pinn/training/config.py` (verify-only, no edit) | config | n/a | `stage.energy_floor_factor` field (`:161`, `:409`) already correct | verification target, not an edit |

---

## Pattern Assignments

### 1. Two-pass dataset-wide statistic — `pinn/data/adapter.py` (analog for CONF-02 `S_H` per-record capture)

**Analog:** the existing `raw_ic13_population` → `compute_normalization_stats` two-pass, same file.

**Pass 1 setup** (`pinn/data/adapter.py:799-802`):
```python
def _scan_and_admit(self):
    candidates = []
    raw_ic13_population = []
    trajectory_energies = []
```

**Pass 1 per-record capture + candidate construction — the exact site `K0`/`Uabs0` join** (`pinn/data/adapter.py:843-876`):
```python
try:
    pre = preprocess_trajectory(
        parsed_brutus.times, parsed_brutus.positions,
        parsed_brutus.velocities, parsed_brutus.masses)
    inv = compute_invariants(pre.masses_ordered, pre.r0_gauge, pre.v0_gauge)
    raw_ic13 = build_raw_ic13(
        pre.masses_ordered, pre.r0_gauge, pre.v0_gauge, inv.E)
except (GaugeDegenerateError, PreprocessAssertionError, MassInvarianceError):
    counts["quarantined"] += 1
    continue
...
# CONF-08 repair: resident arrays carry COM/boost + canonical
# body order, deliberately without rotation gauge or D/V scaling.
candidates.append(SimpleNamespace(
    record_key=record_key, variant=variant, fidelity=fidelity,
    times=parsed_brutus.times, positions=pre.r_com_ordered,
    velocities=pre.v_com_ordered,
    masses_ordered=pre.masses_ordered, raw_ic13=raw_ic13,
    inv=inv, measured=measured,
    dt_reference=reference.get("dt_out"),
    dt_provenance=provenance.get("dt_out"),
    n_snapshots=int(pre.r_com_ordered.shape[0]),
    stage_label=label))
raw_ic13_population.append(raw_ic13)
trajectory_energies.append(inv.E)
self._total_admitted_snapshots += int(pre.r_com_ordered.shape[0])
```
CONF-09 (D-01) touches exactly `positions=`, `velocities=`, and the two `.shape[0]` sites (`:865-866`, `:871`) — swap `pre.r_com_ordered`/`pre.v_com_ordered` → `pre.r_gauge`/`pre.v_gauge`. The stale comment at `:861-862` ("deliberately without rotation gauge or D/V scaling") must be corrected in the same change. `K0`/`Uabs0` (D-12) are captured here too, from `pre.r_gauge[0]`/`pre.v_gauge[0]` (float64, before the fp32 cast in `_materialize`), stored on the `SimpleNamespace` candidate alongside `inv`/`raw_ic13`.

**Pass 1 close-out + pass 2 reduction** (`pinn/data/adapter.py:914-922`):
```python
self._raw_ic13_population = raw_ic13_population
self._trajectory_energies = trajectory_energies
return candidates

# -- pass 2: admitted-only normalization + fp32 residency ----------------
def _materialize(self, candidates):
    stats = compute_normalization_stats(
        np.asarray(self._raw_ic13_population, dtype=np.float64),
        np.asarray(self._trajectory_energies, dtype=np.float64))
```

**The one difference that matters:** `_materialize` reduces over *all admitted* candidates — it has no split knowledge, because it runs before any `SplitManifest` exists. `S_H` must reduce over the **train split only** (D-13), so `S_H`'s reduction cannot live in `_materialize`. Copy the *per-record capture shape* from Pass 1 verbatim (store `k0`/`uabs0` as new `AdmittedRecord` fields, same style as `E`/`Q`); do **not** copy the Pass 2 reduction site — that reduction happens downstream where the train split is resolved (Pattern 2).

---

### 2. Split-scoped reduction + per-record accessor — `pinn/data/splits.py` (analog for CONF-02 `S_H` median + `StageIndex` accessor)

**Where the train split becomes available** (`pinn/data/splits.py:169-186`):
```python
@classmethod
def from_split(cls, source, manifest, split_name="train"):
    """Build one split-restricted index directly from the admitted adapter."""
    if split_name not in _SPLIT_NAMES:
        raise ValueError(f"split_name must be one of {_SPLIT_NAMES}; got {split_name!r}")
    records = _materialize_records(source)
    source_physical = {_record_key(record).physical_key for record in records}
    manifest_physical = {
        group.physical_key for group in manifest.groups
    }
    if source_physical != manifest_physical:
        raise ValueError(
            "manifest physical-key population does not match the admitted source"
        )
    allowed = manifest.physical_keys(split_name)
    selected = [record for record in records if _record_key(record).physical_key in allowed]
    blacklist = getattr(source, "blacklisted_physical_keys", frozenset())
    return cls._with_blacklist(selected, blacklist, source)
```
Already called at `pinn/train.py:414-415` (`train_index = StageIndex.from_split(adapter, manifest, "train")`), itself invoked from `_build_sources` at `pinn/train.py:801`. `S_H`'s median must be computed **after** this call returns `train_source` and **before** `RunController(...)` at `pinn/train.py:964`.

**The `_source_value` delegation new per-record data must follow** (`pinn/data/splits.py:209-224`):
```python
def _source_value(self, accessor: str, key: RecordKey):
    if key not in self._records:
        raise KeyError(key)
    if self._source is None:
        record = self._records[key]
        if hasattr(record, accessor):
            value = getattr(record, accessor)
            return value() if callable(value) else value
        raise TypeError(
            f"StageIndex(records) has no {accessor} snapshot surface; "
            "use StageIndex.from_split(adapter, manifest, split_name)"
        )
    value = getattr(self._source, accessor, None)
    if not callable(value):
        raise TypeError(f"admitted source does not expose {accessor}(key)")
    return value(key)
```

**The existing accessor pair to mirror** (`pinn/data/splits.py:229-233`):
```python
def snapshot_positions(self, key: RecordKey):
    return self._source_value("snapshot_positions", key)

def snapshot_velocities(self, key: RecordKey):
    return self._source_value("snapshot_velocities", key)
```
A new `k0(self, key)` / `uabs0(self, key)` pair, each a one-line `return self._source_value("k0", key)` / `"uabs0"`, is the D-12-mandated surface — new per-record data is exposed by adding an accessor here, never by reaching into the adapter directly. Also relevant: `records_at`/`records_at_or_below` (`pinn/data/splits.py:251-261`) for intersecting the train split with the Stage-0 admitted set (D-13).

---

### 3. Component-returning extraction — `pinn/loss_catalog.py` (analog for CONF-02 D-11 seam)

**Current body, unmodified — the extraction target** (`pinn/loss_catalog.py:140-157`):
```python
def _matched_plummer_hamiltonian(positions, velocities, masses, *, dtype, device,
                                 eps_soft=EPS_SOFT) -> torch.Tensor:
    """Matched-Plummer H_eps = T' + V_eps per snapshot; returns (N_t,)."""
    p = _as_positions(positions, dtype=dtype, device=device)
    v = _as_positions(velocities, dtype=dtype, device=device)
    m = torch.as_tensor(masses, dtype=dtype, device=device)
    # Kinetic: T' = (1/2) sum_i m_i ||v'_i||^2
    speed_sq = (v * v).sum(dim=-1)  # (N_t, 3)
    kinetic = torch.as_tensor(0.5, dtype=dtype, device=device) * (m * speed_sq).sum(dim=-1)
    # Potential: V_eps = -sum_{i<j} m_i m_j / r_safe
    eps = torch.as_tensor(eps_soft, dtype=dtype, device=device)
    potential = torch.zeros(p.shape[0], dtype=dtype, device=device)
    for i in range(_N_BODIES):
        for j in range(i + 1, _N_BODIES):
            delta = p[:, j] - p[:, i]
            r_safe = torch.sqrt((delta * delta).sum(dim=-1) + eps * eps)
            potential = potential - (m[i] * m[j] / r_safe)
    return kinetic + potential
```
`kinetic` (line 148) and `potential` (accumulated 151-156) are already separate locals before the final `return kinetic + potential`. D-11's seam: factor them into a helper (e.g. `_matched_plummer_components(...) -> (kinetic, potential)`) that this function calls and sums — `return kinetic + potential` becomes `k, v = _matched_plummer_components(...); return k + v`. Signature and return value of `_matched_plummer_hamiltonian` stay exactly as they are; nothing outside this function needs to change.

**Critical semantic note (D-10):** `S_H` needs `K0 + Uabs0` where `Uabs0 = |potential|` (potential is always negative), **not** `kinetic + potential` (the signed `H_0`). The extraction seam returns the signed `potential`; the `S_H` capture site must explicitly `abs()` it. Do not reuse `h0` (the signed per-anchor quantity already computed at `controllers.py:468-473`) for this.

**The single legal `eps_h` consumption site — unchanged by this phase** (`pinn/loss_catalog.py:269-286`):
```python
def soft_energy_loss(pred_positions, pred_velocities, h0, eps_h, *,
                     masses, dtype, device, eps_soft=EPS_SOFT):
    """§3.4 soft-energy Huber on relative Hamiltonian drift.
    ...
    """
    h = _matched_plummer_hamiltonian(
        pred_positions, pred_velocities, masses,
        dtype=dtype, device=device, eps_soft=eps_soft,
    )
    h0_t = torch.as_tensor(h0, dtype=dtype, device=device)
    eps_h_t = torch.as_tensor(eps_h, dtype=dtype, device=device)
    denom = h0_t.abs() + eps_h_t
    delta_h = (h - h0_t) / denom
    return _huber(delta_h, HUBER_DELTA_ENERGY, dtype=dtype, device=device).mean()
```
D-20: `denom = h0_t.abs() + eps_h_t` does not change. Only the *scale* fed into `eps_h` at the call site (`controllers.py`) changes.

---

### 4. Fail-closed validate-on-load — `pinn/training/validation_gate.py::validate_sidecar_payload` (analog for D-18)

`validate_sidecar_payload` (`pinn/training/validation_gate.py:541-570`, signature + docstring):
```python
def validate_sidecar_payload(
    payload,
    *,
    expected_run_dir_name=None,
    expected_global_step=None,
    expected_sidecar_path=None,
) -> dict:
    """Fail-closed structural AND semantic validation of a parsed sidecar payload.

    Raises ``ValueError`` with a reason on any violation; returns the payload
    (unmodified) on success. A schema- or semantics-invalid payload is NOT a
    durable validation-gate record (D-20) — this checker is what the D-19
    summary projection and the EVAL-01 precondition (iii) eligibility
    semantics stand on (D-17/D-18/D-19/D-20).

    Every v1 key set (top-level, ``frame``, each row, each ``record_key``) is
    exact — unknown keys fail closed the same as missing ones. ``split``,
    ``gate_status``, and the frame keys/pair/mass-convention are exact
    strings; ``global_step``/``stage``/counts/ids are strict non-negative
    JSON integers with ``bool`` excluded (WR-01); every per-row and aggregate
    metric is independently RECOMPUTED through ``gate_metrics`` and compared
    exactly to the persisted value (D-13) — a payload can never advertise a
    metric, count, or verdict that disagrees with its own rows.
    ...
    """
    _require_exact_keys(payload, _REQUIRED_TOP_KEYS, what="payload")

    if payload["schema_version"] != GATE_SIDECAR_SCHEMA_VERSION:
        raise ValueError(
            f"schema_version mismatch: {payload['schema_version']!r} "
            f"(expected {GATE_SIDECAR_SCHEMA_VERSION!r})"
        )
    if payload["split"] != "validation":
        raise ValueError(f"split must be 'validation'; got {payload['split']!r}")
```
The model to copy: (1) `_require_exact_keys` — unknown keys fail closed the same as missing ones; (2) every semantically-load-bearing field re-derived/compared, never trusted because it is present (`_validate_canonical_threshold`, `_metrics_equal` recomputation elsewhere in the same function); (3) raises `ValueError` with a specific reason rather than substituting a default. A `training_metadata.json` reader (D-18) should apply the same shape: exact-key check, then re-check `S_H`/`ε_H`/`N_train` against the fail-closed predicate (non-finite or `≤ 0` is a hard failure, D-17) — a truncated or hand-edited file must not silently re-enter the loss.

**Sibling analog for the same discipline** — `SplitManifest.from_dict` (loaded via `SplitManifest.from_path`, `pinn/data/splits.py:555-559`) also re-derives rather than trusts on load (e.g. `if tuple(dict(item) for item in summary.deviations) != expected_deviations: raise ValueError(...)` at `:551`, immediately above `from_path`). Two independent existing readers in this codebase already do "recompute and compare," not "read and trust."

---

### 5. Run-artifact layout — what exists under `run_dir/` today (analog for D-16 `training_metadata.json`)

Three existing artifacts, all written once at setup:

**`config.yaml`** — `freeze_resolved_config` (`pinn/training/config_yaml.py:276-295`):
```python
def freeze_resolved_config(config: TrainingConfig, run_dir: PathLike) -> Path:
    """Write the fully-resolved config to ``<run_dir>/config.yaml`` atomically.

    Returns the path of the frozen artifact. Re-parsing via ``load_config``
    yields a ``TrainingConfig`` EQUAL to ``config`` (CTRL-01 / CTX-51).
    ...
    """
    destination_dir = Path(run_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / "config.yaml"
    plain = resolved_config_to_dict(config)
    # sort_keys for stable identity digests (41-05); allow_unicode for run names.
    text = yaml.safe_dump(plain, sort_keys=True, allow_unicode=True)
    atomic_write_text(destination, text)
    return destination
```
Called from `pinn/train.py:746-752` — fresh launch always freezes; resume reuses the existing freeze unless missing. This is the config/derived-data boundary D-16 relies on: `config.yaml` is frozen *input*, `S_H` is *derived data* computed from that input — do not smuggle `S_H` into this file or into `config.stage.energy_floor_factor`.

**`splits.json`** — `write_split_manifest` (`pinn/data/splits.py:773-789`):
```python
def write_split_manifest(
    source, run_dir, seed, ratios=SplitRatios()
) -> SplitManifest:
    """Partition an admitted adapter internally and atomically write splits.json."""
    records = _materialize_records(source)
    manifest = _partition_by_signature(records, seed=seed, ratios=ratios)
    resolved_run_dir = _resolve_run_dir(source, run_dir)
    resolved_run_dir.mkdir(parents=True, exist_ok=True)
    destination = (resolved_run_dir / "splits.json").resolve()
    if destination.parent != resolved_run_dir:
        raise ValueError("split manifest destination escaped run_dir")
    payload = json.dumps(manifest.to_dict(), sort_keys=True, indent=2) + "\n"
    _atomic_write(destination, payload)
    ...
```
Read back via `SplitManifest.from_path` (`pinn/data/splits.py:555-559`):
```python
@classmethod
def from_path(cls, path):
    manifest_path = Path(path)
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    return cls.from_dict(payload, path=manifest_path)
```
This is the closest **structural** analog for `training_metadata.json`: a plain-dict JSON payload, `json.dumps(..., sort_keys=True, indent=2)`, written atomically, read back through a classmethod that re-validates (`from_dict` performs semantic checks, not just key presence).

**`status.json`** — `HeartbeatThread` (`pinn/train.py:668-676`), run *status* (heartbeat/liveness), not a fit for a derived scalar written once — cited only to rule it out, per D-16's own rationale.

**Atomic primitive both of the above use** — `pinn.training.atomic_io.atomic_write_text` (`pinn/training/atomic_io.py:41-64`):
```python
def atomic_write_text(path: PathLike, content: str) -> Path:
    """Atomically write UTF-8 text to ``path``.

    Verified idiom (stage_scan ``_atomic_write``): write to
    ``path.tmp.{pid}``, flush + ``os.fsync`` the file, ``os.replace`` onto the
    canonical name, then ``os.fsync`` the parent directory. A ``finally``
    unlinks any leftover temp so a failed replace cannot leave a partial
    artifact under the canonical name.
    """
    destination = _as_path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + f".tmp.{os.getpid()}")
    try:
        with open(temporary, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        _atomic_replace(temporary, destination)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    return destination
```
`training_metadata.json` should be `json.dumps({...}, sort_keys=True, indent=2)` written through this exact primitive — not a raw `open(...).write(...)` or `json.dump` — matching every other run artifact in this file and satisfying D-17's "never a partially-completed run" requirement.

---

### 6. Frame-convention constants and the admission check — `pinn/training/validation_gate.py` (verified live line numbers — CONTEXT.md D-05's `:526-528` citation is stale)

**Constants** (`pinn/training/validation_gate.py:74-86`):
```python
POSITION_FRAME_SCALED = "r_prime"
POSITION_FRAME_RAW = "r_raw"
TIME_COORD_NORMALIZED = "u_t_over_T"
TIME_COORD_RAW = "t_native"
MASS_CONVENTION_ORDERED_RAW = "ordered_raw"

# The only position/time pairs a coherent conservation measurement can use. The
# scaled pair (r_prime, u=t/T) is the locked contract; the raw pair exists ONLY
# to express an owner-ratified D-09 branch outcome, never as a default.
COHERENT_FRAME_PAIRS = frozenset({
    (POSITION_FRAME_SCALED, TIME_COORD_NORMALIZED),
    (POSITION_FRAME_RAW, TIME_COORD_RAW),
})
```

**First admission check — `FrameConvention.__post_init__`** (`pinn/training/validation_gate.py:106-124`):
```python
@dataclass(frozen=True)
class FrameConvention:
    """Explicit, recorded position/time/mass convention for one gate pass.
    ...
    """

    position_frame: str
    time_coord: str
    mass_convention: str
    conf01_evidence_ref: str

    def __post_init__(self):
        if (self.position_frame, self.time_coord) not in COHERENT_FRAME_PAIRS:
            raise IncoherentFrameError(
                f"incoherent frame pair: position_frame={self.position_frame!r} "
                f"time_coord={self.time_coord!r}; accepted pairs={sorted(COHERENT_FRAME_PAIRS)}"
            )
```

**Second admission check — `_validate_frame`** (`pinn/training/validation_gate.py:453-476`, pair check at `:464-468`):
```python
def _validate_frame(frame_obj) -> None:
    """Exact frame keys, string values, a coherent pair, ordered_raw mass, and a
    non-empty evidence ref (D-07/D-12/D-18). Never mutates
    ``RATIFIED_VALIDATION_FRAME`` or infers a frame from measurement."""
    _require_exact_keys(frame_obj, _FRAME_REQUIRED_KEYS, what="frame")
    for key in _FRAME_REQUIRED_KEYS:
        value = frame_obj[key]
        if not isinstance(value, str):
            raise ValueError(f"frame.{key} must be a JSON string; got {type(value).__name__}")
    position_frame = frame_obj["position_frame"]
    time_coord = frame_obj["time_coord"]
    if (position_frame, time_coord) not in COHERENT_FRAME_PAIRS:
        raise ValueError(
            f"incoherent frame pair: position_frame={position_frame!r} "
            f"time_coord={time_coord!r}; accepted pairs={sorted(COHERENT_FRAME_PAIRS)}"
        )
    if frame_obj["mass_convention"] != MASS_CONVENTION_ORDERED_RAW:
        raise ValueError(
            f"mass_convention must be {MASS_CONVENTION_ORDERED_RAW!r}; "
            f"got {frame_obj['mass_convention']!r}"
        )
```

**The re-ratification site itself** (`pinn/training/validation_gate.py:785-796`, comment included — the codebase already names this exact task):
```python
#
# Re-ratification is REQUIRED if Phase 47/48 moves residency to the locked
# canonical scaled contract (r' with u = t/T); this constant then goes stale.
RATIFIED_VALIDATION_FRAME = FrameConvention(
    position_frame=POSITION_FRAME_RAW,
    time_coord=TIME_COORD_RAW,
    mass_convention=MASS_CONVENTION_ORDERED_RAW,
    conf01_evidence_ref=(
        ".planning/phases/46-frame-resolution-gate-aligned-validation/"
        "evidence/target-frame/20260728T014532Z/raw.json"
    ),
)
```

**Confirmed line-number drift:** `47-CONTEXT.md` D-05 and the 2026-07-28 audit report cite `:526-528` for this constant. That range is currently inside `_metrics_equal` (`pinn/training/validation_gate.py:523-530`):
```python
def _metrics_equal(a: float, b: float) -> bool:
    """Exact equality for decoded metrics; NaN classes compare equal to NaN
    classes only (never to each other's finite/inf counterpart)."""
    if math.isnan(a) and math.isnan(b):
        return True
    if math.isnan(a) or math.isnan(b):
        return False
    return a == b
```
`_metrics_equal` has nothing to do with the frame contract — it is a metric-comparison helper used by `validate_sidecar_payload`. Live locations, re-verified this session: `COHERENT_FRAME_PAIRS` at `:83-86` (checked at `:120` in `FrameConvention.__post_init__` and at `:464` in `_validate_frame`), `RATIFIED_VALIDATION_FRAME` at `:788-796`. The plan should grep the symbol name rather than trust either citation, since the file has already drifted once since the audit (Phase 46 plans 46-08 through 46-10 added code above the constant).

---

### 7. Test conventions — `tests/phase46/test_pairing_repair.py` (analog for `tests/phase47/`, and the file D-06 corrects in place)

**Fixture construction to extend** (`tests/phase46/test_pairing_repair.py:155-195`):
```python
def _adapter(corpus):
    return AdmittedSetAdapter(
        root=corpus.data_root,
        blacklist_path=corpus.blacklist_path,
        precision="float32",
        device="cpu",
        run_dir=corpus.run_dir,
        version_metadata_path=corpus.version_metadata_path,
    )


def _resident_fixture(corpus):
    adapter = _adapter(corpus)
    key = RecordKey("hierarchical", "base", 0)
    path = corpus._brutus_path(
        "brutus_hierarchical", "hierarchical", 0
    )
    parsed = parse_brutus_file(path, root=corpus.data_root)
    masses = np.asarray(parsed.masses, dtype=np.float64)
    total_mass = float(np.sum(masses))
    initial_com = (
        np.sum(masses[:, None] * parsed.positions[0], axis=0) / total_mass
    )
    com_velocity = (
        np.sum(masses[:, None] * parsed.velocities[0], axis=0) / total_mass
    )
    positions_com = (
        parsed.positions
        - initial_com[None, None, :]
        - com_velocity[None, None, :] * parsed.times[:, None, None]
    )
    velocities_com = parsed.velocities - com_velocity[None, None, :]
    permutation = np.array([0, 2, 1], dtype=np.int64)
    return (
        adapter,
        key,
        parsed,
        positions_com[:, permutation, :],
        velocities_com[:, permutation, :],
        masses[permutation],
    )
```
Uses `TinyCorpus` (`tests/phase39/_fixtures.py`) for a dataset-free, on-disk-but-tiny corpus — this is the "dataset-free fixture" convention referenced in `47-CONTEXT.md`'s Established Patterns. Tests are `unittest.TestCase` classes run under pytest (`pytest tests/phase47/ -q -rs`).

**The one method D-06 names explicitly — assertions that must flip from `assertFalse` to the completed-frame contract** (`tests/phase46/test_pairing_repair.py:272-301`):
```python
def test_resident_trajectory_is_not_rotation_gauged_or_globally_scaled(self):
    with TinyCorpus() as corpus:
        adapter, key, parsed, *_expected = _resident_fixture(corpus)
        preprocessed = preprocess_trajectory(
            parsed.times,
            parsed.positions,
            parsed.velocities,
            parsed.masses,
        )
        resident_positions = adapter.snapshot_positions(key).cpu().numpy()
        resident_velocities = adapter.snapshot_velocities(key).cpu().numpy()

        self.assertFalse(
            np.allclose(resident_positions, preprocessed.r_gauge)
        )
        self.assertFalse(
            np.allclose(
                resident_positions,
                preprocessed.r_gauge * preprocessed.D,
            )
        )
        self.assertFalse(
            np.allclose(resident_velocities, preprocessed.v_gauge)
        )
        self.assertFalse(
            np.allclose(
                resident_velocities,
                preprocessed.v_gauge * preprocessed.V,
            )
        )
```
Post-swap, `resident_positions IS preprocessed.r_gauge` — these four `assertFalse(np.allclose(...))` calls must become equality assertions (e.g. `np.testing.assert_array_equal`), and the method name/docstring must stop claiming "not rotation gauged."

**A sibling method in the same class not named by D-06's prose but affected by construction** (`tests/phase46/test_pairing_repair.py:199-221`) builds an *independent* COM-only oracle (no rotation, no D/V scaling) via `_resident_fixture` and compares it byte-for-byte to `adapter.snapshot_positions`/`snapshot_velocities`. This comparison also breaks post-swap unless `_resident_fixture`'s independent derivation is extended to apply the same rotation gauge + D/V scaling `preprocess_trajectory` applies. Treat "which methods must change" as empirically re-verifiable at implementation time (run the suite against the post-swap adapter), not an exhaustive list transcribed from D-06 alone.

**Untouched by CONF-09 — for contrast, do not edit:** `test_resident_trajectory_preserves_com_and_zero_momentum_gauge` (`:223-270`, checks the COM/momentum postcondition, which `preprocess_trajectory` guarantees for `r_gauge`/`v_gauge` too) and all of `PreprocessingPairingSeamTests` (`:80-152`, tests `preprocess_trajectory` directly, not the adapter's residency choice).

---

### 8. CONF-03 wiring gap — `pinn/training/controllers.py` (analog for the new `eps_h`-carrying plumbing)

**`_AnchorContext` — keeps its `eps_h` field (D-21)** (`pinn/training/controllers.py:272-283`):
```python
@dataclass(frozen=True)
class _AnchorContext:
    """Everything needed to evaluate L_IC / L_phys / L_E / L_L for one batch."""

    traj: Any  # Callable[[torch.Tensor], torch.Tensor] -- scalar u -> (3,3) positions
    masses: torch.Tensor
    true_r0: torch.Tensor
    true_v0: torch.Tensor
    h0: float
    l0: torch.Tensor
    eps_h: float
    collocation_times: np.ndarray  # ascending-sorted, shape (N,)
```

**`RunController.__init__` — no run-computed scalar parameter exists yet** (`pinn/training/controllers.py:295-313`):
```python
def __init__(
    self,
    model,
    train_source,
    validation_source,
    config,
    scheduled_weights,
    grad_clipper,
    collocation_sampler,
    stage_exit_machine,
    checkpoint_store,
    runtime,
    *,
    rng: Optional[np.random.Generator] = None,
    checkpoint_hook: Optional[Callable[..., Any]] = None,
    guard_hook: Optional[Callable[..., Any]] = None,
    should_stop: Optional[Callable[[], bool]] = None,
    replay_count: Optional[int] = None,
) -> None:
```
This is 13 positional + 5 keyword parameters, none named `s_h` or `eps_h`. CONF-03 is building this channel for the first time, not fixing a bug in existing plumbing — a new keyword-only, required parameter (no default, so a missing validated value cannot be silently masked) is the pattern to follow, mirroring the existing keyword-only optional params already present.

**The defect to repair** (`pinn/training/controllers.py:478-482`):
```python
# WR-02: eps_h scale is the config-overridable StageConfig.energy_floor_factor
# (CTX-38 provisional default 1e-4 = ctl_instruction.md CURR-03 ε_H=1e-4·S_H).
# The +1e-12 additive floor is a numeric-safety zero-denominator guard, not
# the configurable scale.
eps_h = abs(h0) * float(self._config.stage.energy_floor_factor) + 1e-12
```
`stage.energy_floor_factor` (`pinn/training/config.py:161,409`, value `1e-4`) stays — it remains the named home of the `1e-4` factor. Only line 482 changes: `eps_h = 1e-4 * self._s_h` (or a precomputed `self._eps_h` read directly), and the `+ 1e-12` term is deleted outright, along with the comment that rationalizes it as a "numeric-safety guard."

---

## Shared Patterns

### Fail-closed, re-validate-on-load
**Source:** `pinn/training/validation_gate.py::validate_sidecar_payload` (`:541-570`+), sibling: `pinn/data/splits.py::SplitManifest.from_dict`/`from_path` (`:555-559`, semantic check example at `:551`)
**Apply to:** the `training_metadata.json` reader (D-18) and the `S_H` fail-closed predicate at write time (D-17)
Never trust a persisted number because it is present; recompute or re-check the invariant on load; raise with a specific reason rather than substitute a default/floor.

### Atomic artifact write
**Source:** `pinn/training/atomic_io.py::atomic_write_text` (`:41-64`), used by both `pinn/training/config_yaml.py::freeze_resolved_config` (`:294`) and `pinn/data/splits.py::write_split_manifest` (via `_atomic_write`, `:785`)
**Apply to:** `training_metadata.json` write — `json.dumps(payload, sort_keys=True, indent=2)` through `atomic_write_text`, not a raw `open().write()`.

### Two-pass admission statistic (per-record collect, later reduce)
**Source:** `pinn/data/adapter.py:801,873-874` (pass 1) / `:919-922` (pass 2, admitted-population scope)
**Apply to:** `K0`/`Uabs0` per-record capture (pass 1 shape, same file); the reduction itself moves to `pinn/train.py` after `StageIndex.from_split` returns `train_source` (train-split scope, not admitted-population scope — the one deliberate divergence from the adapter's own precedent).

### `StageIndex` accessor delegation
**Source:** `pinn/data/splits.py::_source_value` (`:209-224`), `snapshot_positions`/`snapshot_velocities` (`:229-233`)
**Apply to:** new `StageIndex.k0(key)` / `.uabs0(key)` accessors — one-line `_source_value` delegations, never a direct adapter reach-through.

### Frame coherence enforcement
**Source:** `pinn/training/validation_gate.py::COHERENT_FRAME_PAIRS` (`:83-86`), checked in `FrameConvention.__post_init__` (`:120`) and `_validate_frame` (`:464`)
**Apply to:** `RATIFIED_VALIDATION_FRAME` re-ratification (`:788-796`) — must land in the same change as the residency swap; a tree where residency has moved but this constant has not is a tree whose own coherence check is lying.

---

## No Analog Found

None. Every file this phase touches is either a same-file self-edit (the residency swap, the frame re-ratification, the component extraction, the `eps_h` wiring) or has a directly analogous sibling construct already in the same module/class (the two-pass statistic, the `StageIndex` accessor, the fail-closed loader, the atomic-write artifact, the phase-46 test fixture). This phase is source-grounded conformance repair inside an already-built, already-tested codebase — there is no library integration, new external dependency, or unprecedented architectural shape to flag as unmatched.

## Metadata

**Analog search scope:** `pinn/data/` (`adapter.py`, `types.py`, `splits.py`, `preprocessing.py`), `pinn/training/` (`validation_gate.py`, `controllers.py`, `config.py`, `config_yaml.py`, `atomic_io.py`), `pinn/loss_catalog.py`, `pinn/train.py`, `pinn/constants.py`, `pinn/verification/gate_metrics.py`, `tests/phase46/test_pairing_repair.py`.
**Files scanned:** 13 read directly (targeted ranges, non-overlapping) + 6 grepped for symbol/line verification.
**Pattern extraction date:** 2026-07-29.
**Excluded source (per phase scope):** `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/` — not consulted.
