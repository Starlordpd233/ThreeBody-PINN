# Phase 39: Data Ingestion & Stage-0 Population Scan - Pattern Map

**Mapped:** 2026-07-13
**Files analyzed:** 18 implementation/test files, plus generated run/evidence artifacts
**Analogs found:** 13 / 18 strong role/structural matches; 5 production science modules have no current same-role analog

## Governing Boundary

This map follows `39-CONTEXT.md`, `39-RESEARCH.md`, `39-SPEC.md`,
`39-GAPS.md`, and `39-VALIDATION.md` together. Where the derived phase SPEC
conflicts with the authoritative CTL, GAP-39-03 controls:

```python
# DATA-06 authoritative membership; ctl_instruction.md:23-28,138-150.
# GAP-39-03: strict `>` excludes equality.
# GAP-39-08: only original/base hierarchical Set 1a is eligible.
is_stage_0 = (
    record.variant == "hierarchical"
    and record.fidelity == "base"
    and record.E < -0.5
    and record.angular_momentum_ratio > 0.5
    and 0.7 <= record.Q <= 1.3
    and record.s_min > interim_s0
)
```

Do not implement the reversed `39-SPEC.md:55-56,106` wording. The report must
use the complete conjunction above, not an `s_min`-only bin, and a record with
`s_min == interim_s0` is not Stage 0. GAP-39-08 carries the authoritative CTL
fidelity boundary into production: Stage 0 and collapsed Stage 1a/1b apply only
to admitted original/base hierarchical Set 1a. Every gold record—including
hierarchical Set 2a—and every otherwise ineligible record is `UNASSIGNED` in
Phase 39; no gold record may enter a numeric Stage-0/1 pool.

GAP-39-04..07 are also resolved. They are reversible implementation defaults
authorized under the user's full-autonomy instruction, not new CTL/framework
authority: use the scale-aware 64-epsilon `H0` quarantine, quarantine an entire
trajectory after dropping any non-finite snapshot block, split complete
physical-group signatures with seeded Hamilton apportionment, and define the
DATA-01 numerator as deduplicated owned-fp32 `resident_tensor_bytes`.

The v1 `pinn/data-handling/` tree and `pinn/data-processing-pipeline-full.py`
are negative migration inventory only. They may help locate behavior that must
be rewritten from the locked specs, but no new module may import them or use
their thresholds as scientific grounding.

## File Classification

### Production files

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `pinn/data/__init__.py` | package/config | transform | `pinn/verification/__init__.py` | role-match; keep minimal |
| `pinn/data/types.py` | model | transform | `pinn/architecture_spec.py:35-140`, `pinn/runtime.py:23-38` | exact structural match |
| `pinn/data/preprocessing.py` | service | transform | `pinn/architecture_spec.py:71-140` | structural only; science comes from CTL |
| `pinn/data/admission.py` | service | transform | `pinn/architecture_spec.py:71-140` | structural only; science comes from CTL Step 1A |
| `pinn/data/stages.py` | service | transform | `pinn/architecture_spec.py:71-140` | structural only; classification comes from CTL/GAP-39-08 |
| `pinn/data/adapter.py` | service/storage boundary | file-I/O + batch preload | `pinn/verification/fixture_loader.py:68-404` | role/data-flow match with a hard reuse prohibition |
| `pinn/data/splits.py` | service | batch + file-I/O | `pinn/verification/gradcheck_probe.py:41-88` | artifact-write match |
| `pinn/data/batches.py` | service | batch + transform | `pinn/network.py:210-228`, `pinn/runtime.py:65-95` | interface match; no sampling analog |
| `pinn/data/stage_scan.py` | service/CLI | batch + file-I/O + request-response | `pinn/verification/gradcheck_probe.py:41-88,155-190` | strong CLI/report match |

### Tests

| New File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `tests/phase39/__init__.py` | test config | transform | `tests/phase38/__init__.py` | exact |
| `tests/phase39/_fixtures.py` | test utility | file-I/O | `tests/phase38/test_fixture_loader.py:65-112` | exact, expanded to a tiny corpus tree |
| `tests/phase39/test_adapter.py` | test | file-I/O + batch preload | `tests/phase38/test_fixture_loader.py:114-339` | strong role/data-flow match |
| `tests/phase39/test_admission.py` | test | transform | `tests/phase38/test_fixture_loader.py:292-334` | assertion-style match; no gate analog |
| `tests/phase39/test_stages.py` | test | transform | `tests/phase38/test_fixture_loader.py:167-187,206-229` | assertion-style match; classifier comes from CTL/GAP-39-08 |
| `tests/phase39/test_splits.py` | test | batch + file-I/O | `tests/phase38/test_fixture_loader.py:114-121,189-197` | test-style match |
| `tests/phase39/test_batches.py` | test | batch + transform | `tests/phase38/test_fixture_loader.py:206-229` | tensor shape/dtype assertion match |
| `tests/phase39/test_stage_scan.py` | test | batch + file-I/O + request-response | `tests/phase38/test_fixture_loader.py:206-246` | test-style match; report consumes persisted GAP-39-08 labels |
| `tests/phase39/test_prohibitions.py` | test | static analysis + file-I/O audit | `tests/phase38/test_prohibitions.py:80-122,157-320` | exact |

### Generated run and evidence files

These are outputs, not hand-maintained source files. Names are within the
phase's report/manifest serialization discretion; the following names make the
planner's actions concrete and keep canonical artifacts separate from logs:

| Generated File | Role | Data Flow | Pattern Source |
|---|---|---|---|
| `<run-dir>/splits.json` | config/manifest | file-I/O | canonical JSON + atomic replace from `gradcheck_probe.py:51-57,75-88` |
| `<run-dir>/stage_population.json` | report | batch + file-I/O | raw JSON evidence from `gradcheck_probe.py:75-88` |
| `.planning/phases/39-data-ingestion-stage-0-population-scan/evidence/stage-scan/<UTC>/stage_population.json` | evidence report | file-I/O | exclusive evidence directory from `gradcheck_probe.py:60-72` |
| `.planning/phases/39-data-ingestion-stage-0-population-scan/evidence/stage-scan/<UTC>/scan.log` | evidence log | streaming/file-I/O | CLI stdout/stderr capture; keep outside the deterministic report payload |

Do not put timestamps, absolute corpus paths, or process-specific temporary
names inside `splits.json`; the same seed and input must reproduce it
byte-for-byte. Keep any non-canonical provenance in the evidence directory or
operator log.

## Core Analog Excerpts

### Frozen typed state and fail-closed validation

**Sources:** `pinn/runtime.py:18-38,65-95` and
`pinn/architecture_spec.py:35-140`

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class RuntimeSpec:
    precision: str
    requested_device: str
    dtype: torch.dtype
    torch_device: torch.device
```

Copy this shape for immutable identities, records, outcomes, manifests, and the
two distinct point sets. Put validation in `__post_init__` when invalid values
must fail before parsing, tensor construction, or artifact writing. Error
messages should name the offending field and the accepted contract, as
`ArchitectureSpec.__post_init__` does at lines 71-140.

Recommended ownership in `types.py`:

- `PhysicalKey(variant, id)` and `RecordKey(variant, fidelity, id)`;
- a closed `StageLabel` with exactly `STAGE_0=0`, `STAGE_1=1`, and
  `UNASSIGNED="UNASSIGNED"` (explicit JSON serialization; no Stage 2–6 values);
- parsed/admitted trajectory records and immutable disposition/reason records;
- `DataVersionHashVerified`, `DataVersionHashDeferred`, and mismatch/fatal
  exception types;
- `SplitManifest`/entry types;
- `DataFidelityPoints`, `PhysicsCollocationPoints`, and `FixedBatch` as visibly
  distinct types;
- `StagePopulationReport` and typed fatal-risk entries.

Expose `resident_tensor_bytes` as a deterministic adapter property/metric, not
as a generic memory value. Admission accounting must distinguish trajectory
dispositions from `dropped_samples`, so a quarantined record with one corrupt
snapshot contributes once to trajectory quarantine and once to sample drops.

### Exact Phase-38 fixture-loader exception: pattern and prohibition

**Source:** `pinn/verification/fixture_loader.py:1-33,68-96,201-228,235-316,323-404`

The existing loader documents its boundary directly:

```python
# fixture_loader.py:3-6
# This is the ONE narrow data source the Phase 38 verification rungs consume.
# It is deliberately NOT the Phase 39 data adapter: it implements no Step-1A
# gate, no splits, no batching, and no data_version_hash.
```

Use it to understand folder-derived identity, exact filename validation,
optional-footer handling, final-timestamp completeness, explicit tensor
construction, and read-only modes. Do **not** import or delegate to it from
`pinn/data/adapter.py`: GAP-39-02 preserves it as the sole probe-local exception,
not as shared production parsing code.

The useful scanner/path pattern is:

```python
# fixture_loader.py:93-96,219-228
_ID_PATTERN = re.compile(r"^[0-9]{1,4}$")

variant = _validated_variant(variant)
id_str = _validated_id(id)
brutus_dir, brutus_prefix, ic_dir, ic_prefix = VARIANTS[variant]
base = Path(root) if root is not None else _default_dataset_root()
```

Phase 39 must strengthen this from a caller-computed single path to a sorted
folder scan using CTL `^brutus_(hierarchical|standard)_(\d{4})\.txt$`, duplicate
`record_key` refusal, resolved-root containment, and no dense-ID assumption.
Keep the parser physically in `adapter.py` so the production reader audit is
unambiguous; `admission.py`, `preprocessing.py`, `splits.py`, `batches.py`, and
`stage_scan.py` must accept arrays/typed records and must never accept raw corpus
paths.

The current load boundary also supplies the explicit-residency pattern:

```python
# fixture_loader.py:398-404
return TrajectoryFixture(
    times=torch.tensor(times, dtype=dtype, device=device),
    positions=torch.tensor(positions, dtype=dtype, device=device),
    velocities=torch.tensor(velocities, dtype=dtype, device=device),
    masses=torch.tensor(masses, dtype=dtype, device=device),
    provenance=provenance,
)
```

Phase 39 differs deliberately: parse and gate in NumPy float64, preprocess and
compute invariants in the locked order, then convert admitted resident storage
to fp32. Model-facing construction still receives explicit caller-supplied
`dtype` and `device`; it must not call `torch.set_default_dtype`, infer a
runtime, or probe device availability.

### Atomic canonical artifacts and CLI

**Source:** `pinn/verification/gradcheck_probe.py:41-88,155-190`

```python
def _atomic_write(path: Path, content: str) -> None:
    temporary = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
    with open(temporary, "w", encoding="utf-8") as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)

payload = json.dumps(raw, sort_keys=True, indent=2) + "\n"
```

Copy the sibling-temp, flush/fsync, and `os.replace` pattern for both the split
manifest and Stage-0 report. Ensure the destination resolves beneath the
caller-supplied run directory and reject a run/evidence directory beneath
`simulation_data/`, following `_reject_dataset_evidence_root` at lines 41-48.

For `stage_scan.py`, copy the testable CLI seam:

```python
def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="python -m pinn.data.stage_scan",
        description="Run the Phase 39 admitted-set Stage-0 population scan.",
    )
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    # resolve adapter -> build report -> atomic write -> one-line outcome
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

Keep report creation callable independently of CLI parsing so
`test_stage_scan.py` can test aggregation/serialization over persisted labels
without the real 6.3 GB corpus. Classification belongs only to `stages.py`.

### Model-facing batch interface

**Source:** `pinn/network.py:210-228`

```python
def forward(self, tau_ic13, masses):
    # tau_ic13: (14,) or (N, 14), caller-supplied wholesale
    # masses: raw ordered (3,) or (N, 3), explicitly separate
    raw = self._forward_unprojected(tau_ic13)
    return project_com(raw, masses,
                       dtype=self._build_dtype, device=self._build_device)
```

`FixedBatch` must therefore expose a 14-wide `[tau, IC13]` tensor and a separate
raw-mass tensor aligned per sampled point. Never reconstruct raw masses from
normalized IC13 slots. Keep data-fidelity and collocation tensors separately
named even if a later caller concatenates one forward pass.

### Dataset-free `unittest` fixtures and deferred imports

**Source:** `tests/phase38/test_fixture_loader.py:29-112`

```python
import importlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

def _require(symbol_name, module_name=LOADER_MODULE):
    module = _require_module(module_name)
    if not hasattr(module, symbol_name):
        raise unittest.SkipTest(f"{module_name}.{symbol_name} not implemented yet")
    return getattr(module, symbol_name)
```

Wave 0 may use the same per-symbol deferred import pattern so test files land
before production modules without discovery errors. `_fixtures.py` should
expand the line-oriented helpers at `test_fixture_loader.py:72-112` into a tiny
complete tree under `TemporaryDirectory`: IC folders, all relevant Brutus
variant folders, a valid blacklist sibling, optional hash metadata, and a run
directory. It must never write under `simulation_data/`.

Use `self.assertRaises`, `self.assertEqual`, `self.assertAlmostEqual`, and exact
shape/dtype checks as at `test_fixture_loader.py:206-246,276-334`. Tests should
assert typed outcomes as well as log text; logs are operator mirrors, not the
only program state.

### Mechanical prohibition audit

**Source:** `tests/phase38/test_prohibitions.py:80-122,157-320`

Copy three mechanics:

1. Parse executable source with `ast`, excluding comments/docstrings, before
   checking banned imports/calls (`_executable_source`, lines 80-96).
2. Discover the current production module set with sorted `Path.rglob`, and
   hard-check that a known-module set is a subset so a new file cannot evade
   the audit (`_discover_phase38_modules`, lines 99-122; superset assertion,
   lines 284-287).
3. Patch write/mkdir/replace/remove APIs and record any resolved target beneath
   `simulation_data/` (lines 157-282).

Phase 39's reader allowlist is exact:

```python
ALLOWED_CORPUS_READERS = {
    "pinn/data/adapter.py",
    "pinn/verification/fixture_loader.py",  # GAP-39-02 sole probe exception
}
```

The audit must fail if any other `pinn/**/*.py` executable source opens corpus
text, calls `read_text`/`read_bytes` on corpus paths, owns `.txt` filename
regexes/globs, or imports parser helpers. It must separately fail on imports or
references to `pinn/data-handling`, `data-processing-pipeline-full.py`, or the
v1 threshold logic. Also retain the global-default and availability-probe bans
from `test_prohibitions.py:289-320`.

## Pattern Assignments

### `pinn/data/__init__.py` (package/config, transform)

Keep this a minimal package marker. Do not turn it into a barrel that imports
`adapter.py` and triggers corpus discovery as an import side effect. Export only
stable pure types after their names settle; all loading/scanning must remain an
explicit call.

### `pinn/data/types.py` (model, transform)

Use frozen dataclasses from `pinn/runtime.py:23-38` and construction-time
validation from `pinn/architecture_spec.py:71-140`. Identity must be structural,
not a formatted path:

```python
@dataclass(frozen=True, order=True)
class PhysicalKey:
    variant: str
    id: int

@dataclass(frozen=True, order=True)
class RecordKey:
    variant: str
    fidelity: str
    id: int
```

The admitted record owns in-memory fp32 storage and metadata (`dt_out` and its
provenance, `n_snapshots`, IC13, raw masses, gate results, invariant values,
resident bytes), plus exactly one persisted `stage_label`. Gold records must
persist `UNASSIGNED` even when their base sibling has label `0` or `1`. It must
not hold a callback/path that reopens the source.

Model `DataVersionHashDeferred` as a distinct frozen value, never `True` or
`None`, and model mismatch as a hard typed exception. Model Stage-0
under-population as a typed fatal-class result/exception carrying threshold
`240` and observed count.

### `pinn/data/preprocessing.py` (service, transform)

There is no rebuild-era production analog to copy scientifically. Follow the
authoritative CTL order at `ctl_instruction.md:789-801`:

```text
parse -> mass-invariance check -> COM recenter -> zero-momentum boost ->
canonical ordering -> canonical rotation gauge -> global scaling ->
assertions and stored metadata
```

Functions must be pure over NumPy float64 arrays. Copy only the fail-closed,
field-specific error style from `ArchitectureSpec.__post_init__`; do not copy
v1 `pinn/data-handling/processing/*` logic. Import
`D_CHARACTERISTIC_LENGTH` from `pinn/constants.py:20-24`; do not add a
selectable `6.694` path. Preserve raw masses and build the CTL IC13, leaving
dtype/device conversion to the adapter/batch boundary.

### `pinn/data/admission.py` (service, transform)

No path, file handle, footer-derived energy, or metrics JSON is accepted by
this module. Its public function consumes a parsed float64 record and returns a
typed admit/reject/quarantine/warn outcome with reason codes.

Implement all seven clauses in CTL order (`ctl_instruction.md:539-607`):

1. identity/blacklist;
2. remediation quarantine;
3. at least two finite 3-body snapshots and strict time monotonicity;
4. `times[-1] >= 9.5`;
5. raw-array float64 Hamiltonian with Plummer `eps=1e-10`,
   compute `scale=abs(K0)+abs(V0)`, quarantine exact zero or
   `scale > 0 and abs(H0) <= 64*np.finfo(np.float64).eps*scale`, and only then
   compute `eps_H=max(abs((H-H0)/H0))`; reject only `SCS > -5`, admit/flag
   equality, map zero drift to `SCS=-inf`, and never add/clamp/max a denominator;
6. mass/COM/momentum gates;
7. observable grid warnings, never rejection.

The adapter logs aggregate outcomes, but every disposition/reason remains
assertable in the record. Footer `dE/E` and metrics JSON must not enter this
module.

At parse/admission handoff, count and remove each complete snapshot block
containing NaN/Inf, retain finite blocks only for diagnostic structural checks,
and unconditionally quarantine the whole trajectory as
`non_finite_snapshot`. Never admit a partially salvaged record, even when at
least two finite monotone blocks remain. A malformed partial body block is not
salvaged as a sample; retain the structural error separately.

### `pinn/data/stages.py` (service, transform)

This is the one pure stage-classification seam. It runs once per admitted
record after invariant computation and before fp32 residency. The fidelity
guard must precede every invariant predicate; never classify once per
`PhysicalKey`, because shared base/gold IC invariants do not share curriculum
fidelity.

```python
# ctl_instruction.md:23-28,138-198; GAP-39-03 and GAP-39-08
def classify_stage(record, *, s0):
    if record.variant != Variant.HIERARCHICAL or record.fidelity != Fidelity.BASE:
        return StageLabel.UNASSIGNED

    common = 0.7 <= record.Q <= 1.3 and record.s_min > s0
    if record.E < -0.5 and record.l_ratio > 0.5 and common:
        return StageLabel.STAGE_0

    stage_1a = -0.5 <= record.E < -0.1 and record.l_ratio > 0.5
    stage_1b = record.E < -0.5 and 0.1 <= record.l_ratio < 0.5
    if (stage_1a or stage_1b) and common:
        return StageLabel.STAGE_1

    return StageLabel.UNASSIGNED
```

Evaluate Stage 0 first, collapse both CTL Stage-1 branches to numeric label `1`,
and emit no Stage 2–6 labels. Standard base, all gold, and base hierarchical
records outside these predicates remain `UNASSIGNED`.

### `pinn/data/adapter.py` (service/storage boundary, file-I/O + batch preload)

This is the sole new production reader. Use the format awareness in
`fixture_loader.py:68-96,235-316`, but rewrite it inside this module to the full
README/CTL contract. Required seams:

- root order: explicit constructor argument, `GSD_DATA_ROOT`, then main-repo
  `simulation_data/Data/` fallback; resolve paths and enforce root containment;
- derive or accept the blacklist path, validate exactly top-level
  `hierarchical` and `standard` integer-like lists, and fail closed on missing,
  unreadable, or invalid schema (`ctl_instruction.md:609-635`);
- sorted exact-filename scan, folder-derived variant/fidelity, duplicate hard
  error, sparse IDs, and `physical_key` blacklist expansion;
- one float64 parse, one admission/preprocessing/invariant pass, exactly one
  `classify_stage` invocation for each admitted record, then fp32 residency;
  persist the returned label and hard-fail an empty admitted set;
- `record_keys`, `get`, `n_snapshots`, `dt_out`, `resident_tensor_bytes`,
  `stage_label`, `has_stage`, `records_at_or_below`, and `records_at` operate
  only on memory. Numeric queries consume the persisted label, exclude
  `UNASSIGNED`, assert every returned key is base hierarchical Set 1a, and never
  reclassify or copy a base label onto its gold sibling;
- `verify_data_version`: supplied mismatch aborts, absent metadata returns and
  logs `DataVersionHashDeferred`, and no hash producer is invented;
- log per-folder found/admitted/rejected/quarantined/dropped counts and
  `mem: <bytes> (<fraction>) watermark=0.7`; keep `num_workers=0` explicit;
- expose `resident_tensor_bytes`: visit only admitted fp32 resident tensors,
  deduplicate their underlying storages (for example by stable
  `(storage.data_ptr(), storage.nbytes())` identity during the measurement),
  and sum each storage's bytes once. Exclude parser arrays, model tensors, RSS,
  and MPS allocator state; separately named telemetry may supplement but never
  replace this numerator.

### `pinn/data/splits.py` (service, batch + file-I/O)

Group sorted admitted records by `PhysicalKey` before any RNG action. Give each
indivisible group the complete signature
`(regime, base_stage, gold_stage_or_missing)`, consuming persisted record labels
without inference. `base_stage` is one of `0`, `1`, or `UNASSIGNED`;
`gold_stage_or_missing` is only `UNASSIGNED` or `missing`. A present gold
signature value of `0` or `1` is a hard invariant failure. Canonically sort
signatures and keys, create a local generator per signature deterministically
from the recorded global seed plus the signature's canonical index, and permute
only within that signature.

For a signature of size `N`, compute `quota = N * (0.8, 0.1, 0.1)`, take the
floors, and assign the remaining groups by descending fractional remainder;
break equal remainders in fixed `train -> validation -> test` order. Slice the
local permutation by those counts, then expand groups to `RecordKey`s. Assert
no physical key spans splits. Persist `schema_version`,
`algorithm="group-signature-hamilton-v1"`, seed, ratios, tie order, signature
summaries/quotas/counts, rare-signature deviations, and ordered groups/records.
Never infer or recalibrate stages in this module. Train may expose a seeded
shuffle; validation/test expose fixed manifest order.

Concrete paired-record manifest shape:

```json
{
  "physical_key": {"id": 7, "variant": "hierarchical"},
  "signature": {
    "regime": "hierarchical",
    "base_stage": 0,
    "gold_stage": "UNASSIGNED"
  },
  "records": [
    {"fidelity": "base", "id": 7, "stage": 0, "variant": "hierarchical"},
    {"fidelity": "gold", "id": 7, "stage": "UNASSIGNED", "variant": "hierarchical"}
  ]
}
```

Use `json.dumps(..., sort_keys=True, indent=2) + "\n"` and the atomic writer
from `gradcheck_probe.py:51-57`. Compare the destination bytes in tests across
two independent executions with the same seed.

### `pinn/data/batches.py` (service, batch + transform)

Depend on an in-memory `StageQuery` protocol, not `AdmittedSetAdapter` disk
internals. The selection and point-set contract comes from
`ctl_instruction.md:1813-1853`:

```python
class StageQuery(Protocol):
    def stage_label(self, key: RecordKey) -> StageLabel: ...
    def has_stage(self, stage: int) -> bool: ...
    def records_at(self, stage: int) -> tuple[RecordKey, ...]: ...
    def records_at_or_below(self, stage: int) -> tuple[RecordKey, ...]: ...
```

All four methods consume the same persisted field. Numeric methods expose only
labels `0`/`1` and base hierarchical Set-1a keys; `UNASSIGNED` is observable by
`stage_label` but never returned in a numeric pool.

- Stage-0 replay: 240 from persisted numeric label `0`, all original/base
  hierarchical Set 1a;
- Stage-1 lookahead: 16 from persisted collapsed label `1` only when
  `has_stage(1)`, also all original/base hierarchical Set 1a;
- `UNASSIGNED` is absent from `records_at`, `records_at_or_below`, replay, and
  lookahead; a gold key in any numeric query/batch is a hard invariant failure;
- `has_stage(1)` reflects only admitted base Set 1a label-1 records, and
  `has_stage(2)` is false at the Phase 39 seam;
- no next stage: replay-only with no synthetic lookahead;
- undersized nonempty next pool: replacement padding to 16;
- data points per record: `min(32, n_snapshots)`, without replacement;
- data time mix: seeded Gumbel-top-k for `floor(n/2)` acceleration-weighted
  points, then uniform without replacement from the remainder;
- collocation: a separate continuous uniform `[0,T]` set (nominal 4096);
- output: aligned `(N,14)` `[tau,IC13]` and `(N,3)` raw masses, explicitly moved
  to caller-supplied dtype/device.

Do not add Phase 40 residual-aware/adaptive collocation, epoch ownership, loss
wiring, or optimizer behavior.

### `pinn/data/stage_scan.py` (service/CLI, batch + file-I/O)

Expose a pure `build_population_report(source, interim_s0)` plus CLI `main(argv)`.
It consumes persisted `stage_label` values and must not reclassify records. The
report contains at minimum:

- schema version and observable adapter/hash state;
- total and per-folder admission dispositions;
- ordered numeric-label `0` and collapsed-label `1` record/physical-key counts
  and resident tensor bytes, all restricted to base hierarchical Set 1a;
- `UNASSIGNED` counts broken down by variant/fidelity;
- an explicit `gold_numeric_stage_count` that must equal zero;
- sorted/auditable Stage-0-only `s_min` distribution plus
  count/min/quantiles/max;
- the interim `s0` value as an input seam, never a mutation/ratification;
- a typed fatal-risk entry when authoritative Stage-0 population is `<240`.

Write only to the caller's run directory using the atomic writer. The module
must instantiate/use the adapter and never parse `.txt` itself. Follow
`gradcheck_probe.main` for argument parsing, one-line outcome, and nonzero exit
on a fatal result.

## Test Assignments

### `tests/phase39/_fixtures.py`

Build deterministic valid and one-variable-invalid records beneath
`TemporaryDirectory`. Include helpers for:

- every folder/default `dt_out` case and optional/malformed footers;
- valid and invalid blacklist schemas;
- base/gold twins sharing one `PhysicalKey`;
- duplicate/sparse IDs, truncated/nonmonotone times, non-finite blocks;
- controlled conservation cases (`SCS > -5`, `SCS == -5`, zero drift,
  exact-zero `H0`, the 64-epsilon boundary, `nextafter` above it, and a small
  well-resolved `H0`);
- an interior non-finite complete snapshot block, a case leaving fewer than two
  finite blocks, and an all-finite control;
- next-stage absent and undersized pools;
- paired base/gold hierarchical records with identical invariants satisfying
  Stage 0, Stage 1a, and Stage 1b, so only fidelity explains base `0`/`1` versus
  gold `UNASSIGNED`;
- Stage-0 conjunction near-misses and exact `s_min == s0`.

Tests must alter one predicate per fixture whenever possible so failures name
the contract rather than a pile of unrelated defects.

### `tests/phase39/test_adapter.py`

Follow `test_fixture_loader.py:114-339`: temporary roots, direct shapes/dtypes,
exact provenance, path validation, optional footer behavior, and explicit
exceptions. Add DATA-01/03 assertions for fp32 admitted-only residency,
`n_snapshots`, `dt_out` value/provenance, memory log/fraction, empty-set failure,
hash match, mismatch hard refusal, and typed absent-field deferral.

Assert the adapter persists exactly one label from `classify_stage` per admitted
record. Paired identical-invariant fixtures must store base `0` or `1` and gold
`UNASSIGNED`; standard and otherwise ineligible records are also unassigned.
Assert the adapter never derives a gold label from its base sibling.

For GAP-39-07, construct one 40-byte fp32 tensor, a view sharing its storage,
and an independent 20-byte fp32 tensor. Assert `resident_tensor_bytes == 60`,
not 80; with configured capacity 100, assert the exact log
`mem: 60 (0.600000) watermark=0.7`. Allocate unrelated process memory and
confirm the metric is unchanged. The full-corpus gate independently sums
unique admitted storages and compares the adapter result.

The eventual real-corpus accessor comparison may call the retained
`fixture_loader.py` as an independent probe, but production `adapter.py` must
not import it.

### `tests/phase39/test_admission.py`

Test every Step-1A clause and disposition independently. Required scientific
boundaries include:

- footer `dE/E` disagrees with recomputed `eps_H`: raw recomputation wins;
- metrics JSON disagrees: raw recomputation wins/no JSON read occurs;
- `SCS > -5` rejects, `SCS == -5` admits as Marginal, `eps_H == 0` is Excellent;
- near-zero `H0` quarantines and no denominator floor token/path exists;
- exact zero and `abs(H0) == 64*eps*(abs(K0)+abs(V0))` quarantine;
  `np.nextafter(boundary, np.inf)` and a small scale-resolved `H0` proceed to
  ratio evaluation;
- an interior corrupt snapshot increments `dropped_samples` once and
  quarantines the whole trajectory as `non_finite_snapshot` even when two
  finite monotone blocks remain; an all-finite control stays eligible;
- fewer-than-two retained blocks record both non-finite and structural reasons,
  and partial-body-row salvage is prohibited;
- counts satisfy parsed = admitted + rejected + quarantined (with dropped
  samples separately accounted as an independent exact identity);
- grid inconsistency warns but does not reject.

### `tests/phase39/test_stages.py`

Cite GAP-39-03/08 and test the pure classifier before adapter integration:

- Stage 0 uses base hierarchical Set 1a plus the full CTL conjunction and strict
  `s_min > s0`; equality is `UNASSIGNED`;
- Stage 1a and Stage 1b each collapse to `StageLabel.STAGE_1` for base Set 1a;
- identical gold counterparts for all three cases are `UNASSIGNED`;
- standard base/gold and nonmatching base hierarchical records are unassigned;
- output is always one of `0`, `1`, or `UNASSIGNED`, with Stage 0 evaluated
  first and no Stage 2–6 value present.

### `tests/phase39/test_splits.py`

Assert base/gold twins remain in one split, every physical key appears once,
the seed/ratios are persisted, identical inputs+seed produce identical bytes,
different input enumeration order does not change bytes, train ordering is
seeded, and validation/test order is fixed. Inject the run directory; never
write a manifest into the corpus root.

Also cover GAP-39-06/08 directly: a numeric base label plus present gold
`UNASSIGNED` produces the full
`(regime, base_stage, gold_stage_or_missing)` signature; every
signature gets exact Hamilton counts and the fixed tie order; changing the seed
changes eligible identities without changing counts; a missing-gold group uses
the explicit missing sentinel; rare signatures emit deterministic deviation
evidence; and records expand only after their physical group is assigned.
Reject a manifest/signature input where any gold record carries `0` or `1`.

### `tests/phase39/test_batches.py`

Assert 240 base-label-0 replay plus 16 base-label-1 lookahead when present,
replay-only behavior when `has_stage(1)` is false, undersized lookahead
replacement padding, no replacement for per-record data snapshots, separate
point-set types/cardinalities, data-only mixed sampling, continuous uniform
collocation, and aligned `(N,14)`/`(N,3)` tensors. Assert blacklisted keys cannot
cross the defense-in-depth batch check. Assert all keys returned by
`records_at(0)`, `records_at(1)`, `records_at_or_below(1)`, replay, and
lookahead have `fidelity="base"`; inject a gold numeric key and require a hard
invariant failure. Assert `has_stage(2)` is false.

### `tests/phase39/test_stage_scan.py`

The module docstring and boundary test must cite GAP-39-03/08. The scan consumes
persisted labels rather than calling the classifier. Build a report source with
base Stage-0/1 and gold `UNASSIGNED` records, then assert:

```python
self.assertEqual(report.stages[0].record_count, base_stage_0_count)
self.assertEqual(report.gold_numeric_stage_count, 0)
self.assertEqual(report.unassigned_by_fidelity["gold"], admitted_gold_count)
```

Use generated base-only populations to assert `>=240` proceeds and `<240`
returns/raises the typed fatal-class signal. Verify report ordering/bytes and
assert the scan does not mutate the supplied `interim_s0` or any global
constant. Adding gold records must not change Stage-0/1 counts, the Stage-0
`s_min` distribution, or the fatal threshold outcome.

### `tests/phase39/test_prohibitions.py`

Copy the AST/discovery/write-spy structure from
`tests/phase38/test_prohibitions.py`. Required checks:

- exact production-reader allowlist: `adapter.py` plus the one pre-existing
  `fixture_loader.py` exception, no others;
- no v1 `pinn/data-handling` or legacy pipeline import/reference in new code;
- no corpus write/create/move/delete target;
- configured-root containment and symlink/traversal rejection;
- no `torch.set_default_dtype`, device availability probe, or runtime inference;
- no footer `dE/E`/metrics JSON gate path;
- no denominator floor in conservation (mechanically reject additive epsilon,
  `max`/`maximum`, `clamp`/`clip`, or fallback-denominator paths around `H0`);
- only `pinn/data/stages.py` may own Stage-0/1 invariant predicates;
  adapter/split/query/batch/report modules consume persisted labels, and a
  numeric gold label is always an invariant failure;
- no code path mutating/ratifying `s0`;
- discovered module set is a superset of every expected `pinn/data/*.py` file.

## Shared Patterns

### Authentication

Not applicable. Phase 39 is a local scientific-data pipeline with no network or
identity boundary.

### Error handling and observability

- Fail before partial state: invalid root/blacklist/schema/duplicate/version
  mismatch/empty admitted set/unsafe destination are hard typed exceptions.
- Scientific record failures are typed admit/reject/quarantine/warn outcomes,
  retained per record and aggregated in logs.
- Absent hash metadata is `DataVersionHashDeferred`, not success and not a
  swallowed warning.
- Stage-0 underpopulation is fatal-class and must produce report evidence before
  returning a failing CLI status.
- Error messages name the record key, clause, and offending value; avoid broad
  catch-and-proceed behavior.

### Precision and device

- Parse, admission, preprocessing, and invariant calculations: NumPy float64.
- Plummer gate/invariant softening: `1e-10`, distinct from
  `pinn.constants.EPS_SOFT == 1e-5`.
- Resident admitted trajectories: torch fp32.
- Model-facing batch tensors: explicit caller-supplied dtype/device.
- No global Torch defaults, runtime inference, MPS availability probe, or
  fallback.

### Identity, ordering, and randomness

- Folder context + exact filename determine `RecordKey`; no dense-ID arithmetic.
- Stage classification is record-level before grouping: only base hierarchical
  Set 1a may receive `0`/`1`; all gold is `UNASSIGNED`.
- Sort keys before grouping/RNG; group by `PhysicalKey` before split expansion.
- Pass a local `numpy.random.Generator` into selection/sampling functions; do
  not seed global NumPy/Torch RNG state.
- Canonical artifacts omit timestamps/absolute paths and use sorted JSON.

### File safety

- Corpus paths are resolved and contained beneath the configured data root.
- Corpus opens are read-only; all synthetic writes occur under temporary roots.
- Run artifacts resolve beneath the supplied run directory, never beneath
  `simulation_data/`.
- Manifest/report writes are sibling-temp + flush/fsync + atomic replace.

## Resolved Autonomy Patterns — No Planning Blockers

The authoritative sources remain unchanged; cite GAP-39-04..07 as reversible
user-authorized implementation defaults rather than CTL-derived semantics.
GAP-39-08 carries the already-authoritative CTL Set-1a/Set-2a fidelity boundary
into one persisted production label seam; only collapsing Stage 1a/1b to query
label `1` is an implementation choice.

### GAP-39-04 — scale-aware near-zero `H(0)`

```python
scale = abs(K0) + abs(V0)
near_zero = H0 == 0.0 or (
    scale > 0.0
    and abs(H0) <= 64 * np.finfo(np.float64).eps * scale
)
if near_zero:
    return quarantine("near_zero_initial_energy")
# Only this branch may divide by H0; no floor/add/clamp/max.
eps_H = np.max(np.abs((H - H0) / H0))
```

Acceptance hook: exact zero and the exact boundary quarantine;
`nextafter(boundary, +inf)` and a small well-resolved value reach ratio
evaluation; an AST/mechanical check detects denominator floors; the full-corpus
report records the resulting count.

### GAP-39-05 — non-finite block quarantines the trajectory

For each complete snapshot block, increment `dropped_samples` and remove the
block if any numeric field is non-finite. Retained blocks support diagnostic
shape/monotonicity checks only. If any block was dropped, disposition is
quarantine with `non_finite_snapshot`; no later clause can promote it to admit.
Keep sample-drop and trajectory-disposition counters independent.

Acceptance hook: one interior corrupt block produces one drop plus one
trajectory quarantine; an all-finite control remains eligible; fewer than two
retained blocks accumulate both reason codes; partial-row salvage is rejected.

### GAP-39-06 — complete-signature Hamilton split

The indivisible unit is `PhysicalKey`, with signature
`(regime, base_stage, gold_stage_or_missing)`. Consume GAP-39-08 labels without
inference: present gold is always `UNASSIGNED`, never `0`/`1`. Within each
canonically ordered signature, use a deterministic local seeded permutation.
Apply Hamilton largest remainder independently to 0.8/0.1/0.1 group quotas:
floor all quotas, then give remaining units to descending remainders, breaking ties in fixed
`train -> validation -> test` order. Expand records afterward and report
unavoidable rare-signature deviations.

Acceptance hook: input order cannot change bytes; exact per-signature counts
and tie order are asserted; seed changes identities but not counts; numeric
base labels remain paired with gold `UNASSIGNED`; no gold signature contains
`0`/`1`; missing gold and rare signatures are explicit.

### GAP-39-07 — deterministic resident tensor payload

`resident_tensor_bytes` is the sum of unique underlying storages owned by
admitted fp32 resident tensors. Views count zero additional bytes. Parser
arrays, transient/model tensors, process RSS, and MPS allocation are excluded.
The required fraction is `resident_tensor_bytes / configured_capacity_bytes`.

Acceptance hook: 40-byte storage + its view + independent 20-byte storage is
exactly 60 bytes; capacity 100 logs
`mem: 60 (0.600000) watermark=0.7`; unrelated allocations do not change it;
the real-corpus value equals an independent unique-storage sum.

### GAP-39-08 — base-Set-1a-only Stage-0/1 seam

Persist exactly one record-level `stage_label` in `{0, 1, UNASSIGNED}` before
residency. Apply the complete strict Stage-0 predicate first and the CTL Stage
1a/1b predicates second only when provenance is original/base hierarchical Set
1a; collapse either Stage-1 branch to `1`. Every gold record, standard record,
and unmatched base record is `UNASSIGNED`. Phase 39 emits no Stage 2–6 label.
Adapter queries, split signatures, batches, and reports consume this exact field
without reclassification.

Acceptance hook: identical-invariant base/gold Stage-0 pairs yield
`0`/`UNASSIGNED`; Stage-1a and Stage-1b pairs yield `1`/`UNASSIGNED`;
`records_at(0)`, `records_at(1)`, `records_at_or_below(1)`, replay, and
lookahead contain no gold; `has_stage(1)` reflects base Set 1a only;
`has_stage(2)` is false; report/full-corpus gold numeric-label count is zero.

## Validation Commands

Use the committed `pinn-train` interpreter and `unittest`; `pytest` is neither
installed nor required.

### Per-task slices

```bash
$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_prohibitions -v

$HOME/miniforge3/envs/pinn-train/bin/python -m unittest \
  tests.phase39.test_adapter tests.phase39.test_admission \
  tests.phase39.test_prohibitions -v

$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_stages -v

$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_splits -v

$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_batches -v

$HOME/miniforge3/envs/pinn-train/bin/python -m unittest tests.phase39.test_stage_scan -v
```

After every production task, pair its targeted module with
`tests.phase39.test_prohibitions` even when the validation table abbreviates the
slice.

### Wave suite

```bash
$HOME/miniforge3/envs/pinn-train/bin/python -m unittest discover \
  -s tests/phase39 -p 'test_*.py' -v
```

### Full regression

```bash
$HOME/miniforge3/envs/pinn-train/bin/python -m unittest discover \
  -s tests -p 'test_*.py' -v
```

### Real-corpus Phase 39 gate

```bash
GSD_DATA_ROOT=<home>/Desktop/3_body_problem/simulation_data/Data \
  $HOME/miniforge3/envs/pinn-train/bin/python -m pinn.data.stage_scan \
  --run-dir /tmp/phase39-real-scan
```

This final gate is intentionally separate from the dataset-free suite. Inspect
the report and logs for admitted/disposition accounting, GAP-39-04 near-zero
quarantine count, GAP-39-05 non-finite drop/quarantine counts,
`resident_tensor_bytes` independently recomputed from unique admitted fp32
storages, per-signature Hamilton allocations/no leakage/rare deviations,
base-Set-1a-only Stage-0/1 pools, `has_stage(1)` based only on base label `1`,
`has_stage(2) == false`, hierarchical gold Set 2a plus all other gold marked
`UNASSIGNED`, `gold_numeric_stage_count == 0`, exact Stage-0 CTL conjunction,
strict `s_min > s0`, and the fatal-risk result. Preserve the final
report/log/manifest as execution evidence without modifying the corpus or
ratifying `s0`.

### Diff hygiene

```bash
git diff --check
```

## No Analog Found

The rebuild has no existing production analog for these scientific policies:

| File | Missing Analog | Required Source Instead |
|---|---|---|
| `pinn/data/preprocessing.py` | no current deterministic CTL preprocessing module | `ctl_instruction.md:789-1069,1114-1162,1464+` |
| `pinn/data/admission.py` | no current seven-clause admission gate | `ctl_instruction.md:539-638` plus resolved autonomy rulings GAP-39-04..05 |
| `pinn/data/stages.py` | no current record-level Stage-0/1 classifier | `ctl_instruction.md:23-28,138-198` plus GAP-39-03/08 |
| `pinn/data/splits.py` | no physical-key grouped, stage-stratified splitter | CONTEXT D-06 plus resolved autonomy ruling GAP-39-06 |
| `pinn/data/batches.py` | no replay/lookahead or two-point-set constructor | `ctl_instruction.md:1813-1853` |

Do not fill these holes by copying v1 code. Copy current code only for frozen
types, explicit runtime flow, CLI/artifact mechanics, and unittest/audit style;
transcribe scientific behavior from the named authoritative contracts and
explicitly labeled autonomy rulings.

`pinn/data/stage_scan.py` has a strong CLI/report analog in
`pinn/verification/gradcheck_probe.py`; it is deliberately not a classifier.
It consumes the label produced by `pinn/data/stages.py` and enforces the
GAP-39-08 zero-gold-numeric-label invariant.

## Metadata

**Analog search scope:** `pinn/`, `pinn/verification/`, `tests/phase37/`,
`tests/phase38/`, Phase 37/38 evidence patterns, and targeted authoritative CTL
sections. v1 `pinn/data-handling/` was inventoried only to enforce the ban.

**Strong analog families:**

1. `pinn/runtime.py` / `pinn/architecture_spec.py` — immutable typed contracts;
2. `pinn/verification/fixture_loader.py` — exact retained reader exception and
   format-boundary migration inventory;
3. `pinn/network.py` — explicit `[tau,IC13]` plus raw-mass interface;
4. `pinn/verification/gradcheck_probe.py` — atomic artifacts and testable CLI;
5. `tests/phase38/test_fixture_loader.py` /
   `tests/phase38/test_prohibitions.py` — temporary fixtures, unittest, and
   mechanical containment audits.

**Pattern extraction date:** 2026-07-13
