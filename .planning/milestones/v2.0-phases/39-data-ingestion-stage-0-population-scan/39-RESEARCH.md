# Phase 39: Data Ingestion & Stage-0 Population Scan - Research

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

### Adapter ownership and runtime discipline

- **D-01:** Resolve the corpus from `GSD_DATA_ROOT`, falling back to the
  main-repository `simulation_data/Data/` location. Treat the corpus as
  read-only and fail closed when the blacklist is missing, unreadable, or
  schema-invalid.
- **D-02:** Implement the admitted-set reader as new Phase 39 code; do not
  import v1 `pinn/data-handling/`. By the owner's 2026-07-13 delegation of
  judgment, DATA-01's single-reader rule governs the **production ingestion
  surface**. `pinn/verification/fixture_loader.py` remains the one retained,
  probe-local Phase 38 exception. The Phase 39 audit must allow that exact
  legacy verification module, route every new production reader through the
  adapter, and fail on any additional on-disk parser.
- **D-03:** Preload only admitted trajectories as fp32 with `num_workers=0`,
  emit `mem: <bytes> (<fraction>) watermark=0.7`, and keep model-facing tensor
  construction explicit about dtype/device. Do not mutate global Torch defaults
  or infer a runtime profile.

### Admission, provenance, and partitioning

- **D-04:** Run all seven Step-1A clauses during adapter initialization. Decide
  completeness from the final parsed timestamp, recompute `eps_H` from raw
  arrays in float64 with the gate's `eps = 1e-10`, never introduce a denominator
  floor, and log admitted/rejected/quarantined/dropped counts. An empty admitted
  set is a hard initialization failure.
- **D-05:** A supplied `data_version_hash` mismatch is a hard refusal. An
  absent field emits the typed `DataVersionHashDeferred` signal and remains
  observable; Phase 39 must not invent a producer or silently treat absence as
  a match. By the owner's 2026-07-13 delegation of judgment, retain this typed
  deferral until an upstream canonical producer is ratified.
- **D-06:** Partition by `physical_key = (variant, id)` before expanding to
  `record_key`s. Persist the seed and byte-stable manifest; train may shuffle
  under that seed while validation and test iteration remain fixed.

### Batch and Stage-0 evidence boundary

- **D-07:** Keep data-fidelity and collocation points independent. Select 240
  replay trajectories plus 16 lookahead trajectories only when `has_stage(k+1)`;
  pad an undersized next-stage pool with replacement, but do not synthesize a
  lookahead pool when it does not exist. Apply the 50/50 uniform plus
  acceleration-weighted sampler to data-fidelity points only.
- **D-08:** Preserve the Phase 38 model interface: each sampled point supplies
  a 14-dimensional `[tau, IC13]` input plus explicit raw `(3,)` masses. The
  Stage-0 scan reports populations, byte counts, and the `s_min` distribution;
  it raises the fatal-class signal below 240 Stage-0 trajectories and never
  changes `s0` itself.

### the agent's Discretion

- Internal module names, admitted-set data structures, report/manifest
  serialization, and test-fixture mechanics are implementation choices, as long
  as they preserve the locked interfaces and acceptance criteria.
- The Phase 39 tests may reuse the established Phase 37/38 test style, but must
  not broaden into Phase 40 adaptive sampling or training-loop work.

### Deferred Ideas (OUT OF SCOPE)

- Phase 40: adaptive collocation sampler interface, epoch iteration, loss
  wiring, optimizer feeding, and stage-training loop.
- FUT-02: full multi-stage curriculum EDA and Stage 1–6 threshold
  recalibration.
- Owner decision: ratify `s0` from the emitted `s_min` distribution.
- Deferred by owner-ratified agent judgment: designate a canonical
  `data_version_hash` producer and metadata source. Phase 39 retains the typed
  absent-field deferral until that upstream contract exists.
- Retained Phase 38 boundary: `pinn/verification/fixture_loader.py` stays a
  probe-local exception; it does not become the admitted-set adapter.
</user_constraints>

**Researched:** 2026-07-13
**Domain:** deterministic scientific-data ingestion, admission, partitioning, and fixed-shape batch construction
**Confidence:** HIGH — all DATA-01..06 requirements are executable with no open planning blockers; GAP-39-03 and authoritative CTL fidelity ownership govern DATA-06, while GAP-39-04..08 record the resolved implementation seams without promoting autonomy choices into framework-source authority

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DATA-01 | A single production adapter preloads the admitted set in fp32, exposes snapshot metadata, and reports memory usage. | Parser schemas, root/blacklist resolution, single-reader audit, resident types, and the deduplicated owned-fp32 `resident_tensor_bytes` contract are mapped below. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-SPEC.md:28-31`; autonomy ruling `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md` GAP-39-07] |
| DATA-02 | Run all seven Step-1A clauses at load, including independent float64 conservation recomputation. | The gate pipeline, scale-aware near-zero predicate, fail-closed non-finite disposition, and exact synthetic boundary tests are specified below. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:539-638`; autonomy rulings `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md` GAP-39-04..05] |
| DATA-03 | Compare and refuse a supplied `data_version_hash`; expose typed deferral when absent. | A narrow verifier interface and all three outcomes are identified without inventing a producer. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:63-69`] |
| DATA-04 | Write a deterministic, stage-stratified 80/10/10 manifest grouped by `physical_key`. | A complete group signature carrying base `0`/collapsed `1`/`UNASSIGNED` and gold `UNASSIGNED`/missing, per-signature seeded Hamilton apportionment, stable ordering, and leakage tests are prescribed below. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-SPEC.md:43-46`; autonomy ruling GAP-39-06; resolved fidelity seam GAP-39-08] |
| DATA-05 | Construct replay/lookahead batches with independent data and collocation point sets. | Exact pool sizes, guards, replacement behavior, point budgets, sampling rules, and the base-Set-1a-only Stage-0 replay/Stage-1 lookahead boundary are mapped below. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198,1813-1853`; resolved seam GAP-39-08] |
| DATA-06 | Scan Stage-0 population, bytes, and `s_min`; flag fewer than 240 records as fatal. | The classifier and report use the authoritative Stage-0 conjunction only for original/base hierarchical Set 1a; equality and every gold record are excluded from Stage 0. Stage 1a/1b are collapsed to label `1` only for the same base source. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md` GAP-39-03 and GAP-39-08; `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`; `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/CLEARANCE.md:23`] |
</phase_requirements>

## Project Constraints (from AGENTS.md)

- Treat `simulation_data/` as authoritative, read-only input; Phase 39 must not create, move, mutate, or delete corpus files. [VERIFIED: `AGENTS.md`; `.claude/rules/dataset-reference.md`]
- Do not use v1 `pinn/` live code as a grounding source for science decisions; implement the ratified framework-spec contracts and use the old code only as a negative migration inventory. [VERIFIED: `AGENTS.md`; `pinn/constants.py:9-11`]
- Preserve the exact `pinn/verification/fixture_loader.py` probe-local reader exception; no second exception is authorized. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:42-50`]
- Stop rather than inventing semantic or process-schema decisions where authoritative material is silent or contradictory. [VERIFIED: `AGENTS.md`]
- Use explicit runtime dtype/device flow, focused `unittest` validation, and atomic, scoped changes. No dependency addition is required by this phase. [VERIFIED: `pinn/runtime.py`; `tests/phase37/test_runtime.py`; `tests/phase38/`]
- Phase 39 must remain independent of Phase 40's adaptive sampler and training-loop ownership. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:29-36`]

## Summary

Phase 39 should be planned as a one-way data pipeline: one format-aware disk boundary parses and gates records, after which typed in-memory objects are the only data source for partitioning, stage queries, batches, and reports. The existing Phase 38 fixture loader remains an exact allow-listed verification exception, not reusable ingestion code. All new computation outside the adapter should be pure over arrays/tensors so parser ownership is mechanically auditable. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:39-59`; `pinn/verification/fixture_loader.py:1-16`]

The corpus format has four trajectory folders, paired base/gold identities, fixed three-row IC files, variable-length Brutus snapshot blocks, and heterogeneous/missing footers. Completeness therefore comes from the last parsed timestamp, and identity comes from filenames plus folder context. The verified corpus contains approximately 8.23 million snapshots; the corrected resident payload estimate is about 0.72 GB in fp32, while the checked-out text corpus is 6.3 GB on disk. [VERIFIED: `simulation_data/Documentation/README.md:145-223,226-300,580-649`; `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/CLEARANCE.md:31`; direct `du -sh <home>/Desktop/3_body_problem/simulation_data/Data`]

GAP-39-03 resolves the DATA-06 source conflict for planning. Under SCOPE-18, the read-only CTL and owner-ratified integrity clearance outrank the derived phase SPEC: Stage 0 is the full CTL conjunction and includes strict `s_min > s0`; a trajectory with `s_min == s0` is not Stage 0. The contradictory `39-SPEC.md` target/acceptance wording remains visible as a routed build-discovered spec defect and must not drive implementation or tests. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md:99-148`; `.planning/REQUIREMENTS.md:126`; `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:138-150`; `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/CLEARANCE.md:23`]

GAP-39-04..07 close the four implementation semantics that authoritative sources left open. They authorize a scale-aware `64 * float64_eps * (|K0|+|V0|)` near-zero predicate, whole-trajectory quarantine after any non-finite snapshot block, complete group-signature Hamilton splitting, and deduplicated owned-fp32 `resident_tensor_bytes`. These are concrete, reversible autonomy rulings recorded with user authorization; they are not new CTL or framework-spec authority. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md` GAP-39-04..07]

GAP-39-08 closes the stage-label production seam without expanding Phase 39 into Stage 2–6 assignment. The authoritative CTL maps original/base hierarchical Set 1a to Stage 0 and Stage 1a/1b, and high-resolution hierarchical gold Set 2a to Stage 2 refinement. Therefore the pure Phase 39 classifier may emit `0` or collapsed `1` only for admitted base Set 1a records; hierarchical gold Set 2a and every other record must remain `UNASSIGNED`. Split signatures retain the gold field as `UNASSIGNED` or missing, while `StageQuery`, batch pools, and reports consume the same persisted label. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`; `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md` GAP-39-08]

**Primary recommendation:** plan DATA-01..06 through an adapter → admitted invariants → one GAP-39-08 stage classifier → signature-stratified split/query → batch/report pipeline. Every applicable task and acceptance test should cite GAP-39-03..08, distinguish autonomy seams from source authority, and prove that no gold record receives label `0` or `1`.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Corpus discovery and parsing | Database / Storage boundary | API / Backend | Only the adapter understands `.txt`, folder identity, footer variability, and the fail-closed blacklist. [VERIFIED: `simulation_data/Documentation/README.md:193-300,580-628`] |
| Step-1A admission | API / Backend | Database / Storage boundary | Pure numerical policy evaluates raw parsed arrays before resident fp32 conversion. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:539-607`] |
| Stage-0/1 record classification | API / Backend | — | One pure classifier applies CTL Stage 0 then Stage 1a/1b only to original/base hierarchical Set 1a and persists `0`, collapsed `1`, or `UNASSIGNED`; all gold remains unassigned. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`; GAP-39-08] |
| In-memory admitted set and queries | API / Backend | — | It owns stable record metadata and returns already-admitted tensors; it does not re-read disk. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:39-59`] |
| Grouped split manifest | API / Backend | Database / Storage boundary | Split logic groups identities in memory and persists one deterministic run artifact. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:71-75`] |
| Replay/lookahead batch construction | API / Backend | — | It queries admitted records and emits model-ready point sets without owning training iteration. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1813-1853`] |
| Thrust-A population report | API / Backend | Database / Storage boundary | The scan derives evidence from admitted metadata and writes a report, but cannot ratify `s0`. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:78-87`] |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.11 (project environment) | Parser, policy, manifests, and tests | The committed environment pins Python 3.11 and current `pinn/` is Python. [VERIFIED: `environment.yml`] |
| PyTorch | 2.12.1 | Resident fp32 tensors and explicit device transfer | Already locked by the environment and consumed by the Phase 38 model interface. [VERIFIED: `conda-lock.yml`; `pinn/network.py:210-228`] |
| NumPy | 2.4.6 | Float64 raw-array gate and preprocessing math | Already locked; it cleanly separates admission precision from fp32 residency. [VERIFIED: `conda-lock.yml`; `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:52-59`] |
| Python standard library | 3.11 | `pathlib`, `re`, `json`, `hashlib`, `logging`, `dataclasses`, seeded RNG, `unittest` | These cover the remaining requirements without a new dependency. [VERIFIED: repository test and serialization patterns in `tests/phase37/`, `tests/phase38/`, and `pinn/verification/`]

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `unittest` | Python 3.11 stdlib | Synthetic unit/integration and mechanical prohibition checks | Use for every task commit and dataset-free phase suite. [VERIFIED: `tests/phase37/`; `tests/phase38/`] |
| `logging` | Python 3.11 stdlib | `mem:`, admission counts, warnings, and typed deferral observability | Use at initialization/report boundaries; typed outcomes must also remain inspectable in code. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:52-69`] |

### Alternatives Considered

No alternatives are recommended. HDF5 conversion, multiprocessing, v1 `pinn/data-handling/` reuse, and a third-party stratification package all contradict locked scope or add needless state/dependencies. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:39-59`; `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:427-535`]

**Installation:** none. Use the existing `pinn-train` environment. [VERIFIED: `environment.yml`; environment probe on 2026-07-13]

## Exact Implementation Surfaces

| Proposed path | Responsibility | Allowed disk access |
|---------------|----------------|---------------------|
| `pinn/data/types.py` | Frozen `PhysicalKey`, `RecordKey`, parsed/admitted records, disposition records, split entries, and visibly distinct batch point-set types. | None. [ASSUMED] |
| `pinn/data/preprocessing.py` | Pure mass checks, COM recentering, zero-momentum boost, canonical order, rotation gauge, global scale, invariants, IC13, and statistics. | None. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:789-1069,1114-1235,1464-1594`] |
| `pinn/data/admission.py` | Pure seven-clause Step-1A evaluation, the resolved near-zero predicate, and typed admit/reject/quarantine/warn reason codes over parsed float64 arrays. | None. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:539-607`; autonomy rulings GAP-39-04..05] |
| `pinn/data/stages.py` | Pure GAP-39-08 classifier over admitted invariants and fidelity provenance: Stage 0 first, Stage 1a/1b collapsed to `1` second, otherwise `UNASSIGNED`; only base hierarchical Set 1a is eligible. | None. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`; GAP-39-08] |
| `pinn/data/adapter.py` | `GSD_DATA_ROOT`/main-repo resolution, blacklist load, filename scan, `.txt` parsing, hash verification, gate orchestration, classifier invocation, fp32 preload, accessors, counts, deduplicated storage accounting, and `resident_tensor_bytes` log. This is the sole new production reader and persists one `stage_label` per admitted record. | Yes; exact format owner. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:39-59`; autonomy ruling GAP-39-07; resolved fidelity seam GAP-39-08] |
| `pinn/data/splits.py` | Group-first signature construction using the persisted base/gold label fields, seeded per-signature Hamilton apportionment, leakage assertion, stable iteration, and byte-stable manifest writer. | Manifest write only. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:71-75`; autonomy ruling GAP-39-06; resolved fidelity seam GAP-39-08] |
| `pinn/data/batches.py` | Stage query protocol, base-Set-1a-only replay/lookahead selection, data-point sampler, uniform continuous collocation, and model-facing fixed batch. | None. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198,1813-1853`; GAP-39-08] |
| `pinn/data/stage_scan.py` | Read-only population/byte/distribution derivation plus report CLI over persisted stage labels; instantiate the adapter but never parse raw files or reclassify records itself. | Report write only. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:78-87`; GAP-39-08] |
| `pinn/data/__init__.py` | Minimal public exports only after contracts stabilize. | None. [ASSUMED] |

This separation is prescriptive; the planner may combine `types.py` with one adjacent pure module only if the single-reader audit remains trivial and no module besides `adapter.py` reads corpus text. [ASSUMED]

### Required Interfaces

Plan the production seam around these minimal contracts; exact class names are discretionary, but the responsibilities and absence of raw paths downstream are not. [ASSUMED]

```python
class AdmittedSetAdapter:
    def __init__(
        self,
        *,
        data_root: Path | None = None,
        blacklist_path: Path | None = None,
        expected_data_version_hash: str | None = None,
        supplied_data_version_hash: str | None = None,
        memory_capacity_bytes: int,
        memory_watermark: float = 0.7,
    ) -> None: ...

    def record_keys(self) -> tuple[RecordKey, ...]: ...
    def get(self, key: RecordKey) -> AdmittedTrajectory: ...
    def n_snapshots(self, key: RecordKey) -> int: ...
    def dt_out(self, key: RecordKey) -> float: ...
    def resident_tensor_bytes(self) -> int: ...
    def stage_label(self, key: RecordKey) -> StageLabel: ...
    def has_stage(self, stage: int) -> bool: ...
    def records_at_or_below(self, stage: int) -> tuple[RecordKey, ...]: ...
    def records_at(self, stage: int) -> tuple[RecordKey, ...]: ...


def write_split_manifest(
    records: Sequence[AdmittedTrajectory],
    *,
    run_dir: Path,
    seed: int,
    ratios: SplitRatios = SplitRatios(0.8, 0.1, 0.1),
) -> SplitManifest: ...


def build_stage_batch(
    source: StageQuery,
    *,
    stage: int,
    rng: numpy.random.Generator,
    dtype: torch.dtype,
    device: torch.device,
) -> FixedBatch: ...


def build_population_report(
    source: StageQuery,
    *,
    interim_s0: float,
) -> StagePopulationReport: ...
```

`AdmittedTrajectory` should retain immutable identity, folder/fidelity provenance, parsed `dt_out` plus its provenance, snapshot count, admission/gate metadata, preprocessing metadata, invariant values, IC13, raw masses, owned fp32 trajectory storage, and the single persisted `stage_label ∈ {0,1,UNASSIGNED}`. Gold records must persist `UNASSIGNED` even when their base sibling is label 0 or 1. It must not retain a callable that reopens the source file. The adapter's primary memory metric counts each admitted tensor's underlying owned storage once; views cannot inflate `resident_tensor_bytes`, and RSS/MPS allocator metrics may only appear under separate names. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198,427-535,1048-1069`; `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:39-59`; autonomy ruling GAP-39-07; resolved fidelity seam GAP-39-08]

`StageQuery` should be an in-memory protocol implemented by the adapter rather than a disk-aware repository. `has_stage`, `records_at`, and `records_at_or_below` operate only on persisted numeric labels and exclude `UNASSIGNED`; consequently real Phase 39 Stage-0 replay and Stage-1 lookahead contain original/base hierarchical Set 1a records only. Random selection belongs in `batches.py` so the adapter remains a deterministic data source. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,1091-1100,138-198,1813-1840`; GAP-39-08]

## Architecture Patterns

### System Architecture Diagram

```text
GSD_DATA_ROOT or main-repo fallback
              |
              v
  exact filename scanner + fail-closed blacklist ---- supplied hash? -- mismatch --> hard refusal
              |                                            |
              |                                            `-- absent --> typed deferred signal
              v
       float64 raw parse
              |
              v
       Step-1A clauses 1..7
     (GAP-39-04/05 boundaries)
        |          |          |
      admit      reject    quarantine / warn
        |
        v
spec preprocessing + invariants + IC13
        |
        v
GAP-39-08 stage classifier
  base Set 1a -> 0 / collapsed 1 / UNASSIGNED
  every gold + all others -> UNASSIGNED
        |
        v
fp32 resident admitted set ----> grouped split manifest
  + resident_tensor_bytes         (physical_key first;
        |                          signature + Hamilton)
        |
        +----> stage-query protocol ----> replay/lookahead selector
        |                                  |             |
        |                                  v             v
        |                         data snapshots   continuous collocation
        |                                  `------ fixed batch ------> Phase 38 model
        |
        `----> Thrust-A scan ----> report + fatal-risk signal
              (base Set 1a Stage 0 only; zero gold 0/1)
```

### Recommended Project Structure

```text
pinn/data/
├── __init__.py
├── types.py
├── preprocessing.py
├── admission.py
├── stages.py
├── adapter.py
├── splits.py
├── batches.py
└── stage_scan.py
tests/phase39/
├── __init__.py
├── _fixtures.py
├── test_adapter.py
├── test_admission.py
├── test_stages.py
├── test_splits.py
├── test_batches.py
├── test_stage_scan.py
└── test_prohibitions.py
```

### Pattern 1: Parse Once, Decide in Pure Functions

**What:** `adapter.py` converts files into one float64 parsed representation; admission and preprocessing consume that representation without paths or file handles; only admitted results are converted to resident fp32 tensors. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:39-59`]

**When to use:** every load and every synthetic test. This makes direct parser ownership auditable and lets boundary tests bypass the 6.3 GB corpus. [VERIFIED: direct corpus audit; `tests/phase38/` fixture style]

**Required processing order:** parse → finite-sample accounting → quarantine any trajectory with a dropped non-finite block → structural recheck for diagnostic reason accumulation → completeness → conservation/invariants → preprocessing/IC13 → one GAP-39-08 stage-label pass → fp32 residency. Preprocessing itself is mass check → COM recenter → zero-momentum boost → canonical order → rotation gauge → global scale → post-assertions/metadata. The quarantine disposition is GAP-39-05's reversible autonomy ruling; the base/gold fidelity boundary comes from the CTL and is carried into production by GAP-39-08. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198,789-1069`; GAP-39-05 and GAP-39-08]

### Pattern 2: Typed Outcomes, Not Log-Only State

**What:** return or retain typed `AdmissionOutcome`, `GridWarning`, `DataVersionHashDeferred`, and fatal population-risk values; logs mirror these outcomes for operators. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:61-69,78-87`]

**When to use:** any branch where downstream behavior differs. A string log alone cannot support assertions or prevent accidental proceed. [ASSUMED]

### Pattern 3: Stable Identity Before Randomness

**What:** scan exact filename regexes, reject duplicate `record_key=(variant,fidelity,id)`, sort record keys, and group by `physical_key=(variant,id)`. Build each indivisible group's signature `(regime, base_stage, gold_stage_or_missing)` from the persisted GAP-39-08 labels: base may be `0`, collapsed `1`, or `UNASSIGNED`, while gold is always `UNASSIGNED` when present. Canonically sort groups within the signature, apply a local seeded permutation, then apportion group counts by Hamilton largest remainder at 0.8/0.1/0.1 with fixed `train → validation → test` tie order. Expand to records only afterward; validation/test preserve manifest order. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198,487-535`; `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:71-75`; autonomy ruling GAP-39-06; resolved fidelity seam GAP-39-08]

**When to use:** split generation and every query that promises reproducibility. Do not assume dense IDs because the standard-gold subset is incomplete. [VERIFIED: `simulation_data/Documentation/README.md:172-184,739-760`]

### Pattern 4: Two Distinct Point-Set Fields

**What:** the batch type carries `data_points` and `collocation_points` as different fields/types. The 50/50 uniform + acceleration-weighted sampler touches only data snapshots; collocation is continuous uniform in Phase 39, and energy reuses physics collocation. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1813-1853`; `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:78-83`]

**When to use:** DATA-05 and its tests. Avoid one generic `points` field that allows Phase 40 behavior to leak backward. [ASSUMED]

### Anti-Patterns to Avoid

- **Reusing `pinn/data-handling/`:** it contains stale thresholds and format behavior and is explicitly barred from the rebuild. Port the locked formulas into new pure modules. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-SPEC.md:20-24,110-111`]
- **Letting report or batch modules reopen `.txt`:** this creates a second production parser. Pass admitted records/query interfaces instead. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:39-50`]
- **Reading completeness or conservation from a footer/metric JSON:** footer presence is heterogeneous, and Step-1A explicitly uses parsed final time and raw-array recomputation. [VERIFIED: `simulation_data/Documentation/README.md:580-649`; `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:562-581`]
- **Writing timestamps or absolute paths into deterministic manifests:** either defeats byte-for-byte reproducibility across runs/machines. Keep provenance in a separate non-canonical log/report if needed. [ASSUMED]
- **Using generic tuple keys as JSON object keys:** encode keys as explicit objects/lists in a sorted list so schema and ordering are portable. [ASSUMED]
- **Conflating disk size, tensor payload, and process RSS:** GAP-39-07 defines the primary DATA-01 numerator as deduplicated owned fp32 `resident_tensor_bytes`, divided by explicitly configured capacity. RSS/MPS metrics may be additional fields but cannot replace or rename the payload assertion. [VERIFIED: autonomy ruling `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md` GAP-39-07]
- **Reclassifying gold from shared IC invariants:** a hierarchical gold trajectory shares its IC with base, but CTL assigns Set 2a to Stage 2 refinement. Persist gold as `UNASSIGNED`; the splitter, query, batch, and report must consume the one classifier field rather than rerun Stage-0/1 predicates. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`; GAP-39-08]

## Parsing and Data Facts the Plan Must Encode

| Fact | Planning consequence |
|------|----------------------|
| IC files are exactly three rows of seven floats. [VERIFIED: `simulation_data/Documentation/README.md:226-251`] | Reject malformed IC shape before scientific gates. |
| Brutus files repeat a time header plus three body rows; footer schemas vary and may be absent. [VERIFIED: `simulation_data/Documentation/README.md:252-300,580-628`] | Use block-aware parsing and treat footer metadata as optional/provenance-only. |
| Missing footer defaults are folder-specific: hierarchical base `0.08`, standard base `0.17`, standard gold `0.01`; hierarchical gold supplies full metadata. [VERIFIED: `simulation_data/Documentation/README.md:580-628`] | `dt_out` must record both value and provenance; do not use one global default. |
| Folder plus filename defines variant/fidelity/id; base/gold share a physical identity. [VERIFIED: `simulation_data/Documentation/README.md:193-223,700-717`] | Identity scanning precedes admission and grouping. |
| `brutus_hierarchical` base is original Set 1a; `brutus_hierarchical_gold_standard` is high-resolution Set 2a, despite sharing the same physical ICs. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`; `simulation_data/Documentation/README.md:174-183,209-221`] | Only the base record may receive Phase 39 label 0 or 1; the gold sibling is `UNASSIGNED`. |
| Standard gold is a 2,565-record subset rather than a dense mirror of 2,749 base records. [VERIFIED: `simulation_data/Documentation/README.md:145-184,739-760`] | Never synthesize or dense-range missing record keys. |
| Hierarchical IC files have documented COM/momentum offsets. [VERIFIED: `simulation_data/Documentation/README.md:719-725`] | Clause 6 disposition and preprocessing must be tested; do not mistake known offsets for parser failure. |
| Completeness is final parsed timestamp `>=9.5`, and snapshot counts are not hard-coded. [VERIFIED: `simulation_data/Documentation/README.md:630-649`] | Test truncated final-time files separately from short-but-valid cadence. |
| The blacklist is a sibling under `simulation_data/Documentation/`, not under `Data/`, and currently has 65 IDs (2 hierarchical, 63 standard). [VERIFIED: direct JSON inspection; `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:609-638`] | Root resolution should accept/derive an explicit `blacklist_path`, validate its exact schema, and fail closed. |

Root discovery should resolve in this order: explicit constructor path, `GSD_DATA_ROOT`, then the main repository derived from Git's common directory; if neither Git nor the env override can establish the path, fail with an actionable error. Tests should always inject a temporary root and blacklist path. This fallback design is an implementation recommendation, not an additional science contract. [ASSUMED]

## Step-1A Gate Contract

| Order | Clause | Required behavior |
|-------|--------|-------------------|
| 1 | Identity and blacklist | Validate key/folder identity, load the exact blacklist schema, and fail initialization if the blacklist cannot be trusted. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:539-546,609-638`] |
| 2 | Remediation quarantine | Preserve a typed quarantine channel even though the verified baseline set is empty. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:547-550`] |
| 3 | Structure | Require at least two snapshots, exactly three body rows, finite retained values, and strictly increasing timestamps. Count/drop each non-finite snapshot block but quarantine its whole trajectory as `non_finite_snapshot`; retained blocks support diagnostics only, never salvage admission. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:551-557`; autonomy ruling GAP-39-05] |
| 4 | Completeness | Require final parsed time `>=9.5`; never infer it from line count/footer. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:558-561`] |
| 5 | Conservation | Recompute Plummer-softened total energy from float64 raw arrays with `eps=1e-10`; let `scale=|K0|+|V0|` and quarantine when `H0 == 0.0` or (`scale > 0` and `|H0| <= 64*finfo(float64).eps*scale`); otherwise compute `eps_H=max_t |(H(t)-H0)/H0|` with no floor. Reject only `SCS>-5`, admit equality as Marginal, and classify zero drift Excellent. The factor `64` is a reversible autonomy safety factor rather than source authority. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:562-581`; autonomy ruling GAP-39-04] |
| 6 | Physical invariants | Check mass invariance `<1e-15`, IC-vs-first-snapshot masses, and COM/momentum policy; then apply the locked preprocessing order. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:582-593,789-1069`] |
| 7 | Grid consistency | Warn if max gap exceeds `1.5*dt_out` or count is below `0.9*(final_t/dt_out+1)`; warning is observable but not rejection. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:594-607`] |

The authoritative CTL does not supply the numerical tolerance or the post-drop disposition. GAP-39-04 and GAP-39-05 resolve those silences under the user's full-autonomy instruction: use the exact scale-aware predicate above, and count/drop a corrupt block while quarantining the whole trajectory. These rulings make DATA-02 executable but must remain labeled as reversible autonomy decisions, not CTL-derived semantics. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md` GAP-39-04..05]

Acceptance must cover exact zero; the scale-aware boundary; `nextafter` immediately above it; a small but resolved `H0`; a prohibition on `max`, additive epsilon, clamp, or any denominator floor; and the real-corpus near-zero count. For non-finite handling, a trajectory with an interior corrupt block must increment `dropped_samples`, retain separate trajectory accounting, and end quarantined even when at least two finite monotone blocks remain; an all-finite control remains eligible for admission. [VERIFIED: autonomy rulings GAP-39-04..05]

## Preprocessing, Invariants, and Model Interface

Implement the CTL order exactly: mass validation; mass-weighted COM recentering; zero-total-momentum boost; deterministic body order (mass descending, then position norm, velocity norm, original index); rotation gauge with specified degeneracy fallbacks; global scale `D≈4.6416`; and postcondition metadata/assertions. Decimal is a failure classifier only, not the normal numerical path. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:789-1069`]

Compute energy `E`, angular momentum magnitude `Q`, and unsoftened minimum separation `s_min` in scaled preprocessed coordinates. The invariant potential uses `eps_inv=1e-10`, while `s_min` is unsoftened. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1114-1162`]

Form IC13 as `[m1,m2,m3,rho_x,lambda_x,lambda_y,rhodot_x,rhodot_y,rhodot_z,lambdadot_x,lambdadot_y,lambdadot_z,E]`, normalize with the locked robust-statistics formulas, and retain raw `(3,)` masses as a separate model input. Do not collapse the raw-mass side channel into IC13. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1464-1594`; `pinn/network.py:210-228`]

The final `tau_L` estimator and full adaptive stage-assignment statistics remain owner-pending. GAP-39-08 authorizes only the production Stage-0/1 seam already defined by the CTL: classify original/base hierarchical Set 1a as Stage 0 or collapsed Stage 1a/1b, and leave all other records `UNASSIGNED`. Phase 39 must not assign Stage 2–6 or recalibrate their criteria. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198,1333-1367,1654-1665`; `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:29-36`; GAP-39-08]

### Production Stage-0/1 Classifier

Run one pure classifier over each admitted record's provenance and preprocessed invariants before fp32 residency. If the record is not original/base hierarchical Set 1a, return `UNASSIGNED` immediately; this includes every hierarchical gold Set 2a record, both standard Set 1b/2b fidelities, and any future unrecognized fidelity. For eligible Set 1a records, evaluate in this order: [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`; GAP-39-08]

1. Label `0` when `E < -0.5`, `L/L_max > 0.5`, `0.7 <= Q <= 1.3`, and strict `s_min > s0`.
2. Otherwise label collapsed `1` when either Stage 1a (`-0.5 <= E < -0.1`, `L/L_max > 0.5`, the same Q band, strict `s_min > s0`) or Stage 1b (`E < -0.5`, `0.1 <= L/L_max < 0.5`, the same Q band, strict `s_min > s0`) holds.
3. Otherwise return `UNASSIGNED`.

These predicates and the Set 1a/Set 2a ownership are authoritative CTL content; persisting them as the single `stage_label` consumed by every Phase 39 downstream surface is the resolved GAP-39-08 production seam. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:138-198`; GAP-39-08]

Acceptance must prove the fidelity guard before numerical predicate evaluation: identical base/gold hierarchical records that both satisfy Stage 0 yield labels `0` and `UNASSIGNED`, respectively; likewise a base Stage-1a or Stage-1b record yields `1` while its gold sibling remains `UNASSIGNED`. Boundary tests preserve Stage-0-first priority, collapse both Stage-1 branches to integer label `1`, exclude `s_min == s0`, and reject any emitted label outside `{0,1,UNASSIGNED}`. [VERIFIED: GAP-39-08]

## Split Manifest Schema

The serialization recommendation is a canonical JSON object with `schema_version`, `seed`, ratios, algorithm identifier, tie order, ordered signature summaries, and an ordered `groups` array. Each group contains an explicit `{variant,id}` physical key, signature, split name, and sorted record entries; serialize with `json.dumps(..., sort_keys=True, indent=2) + "\n"`, use atomic sibling-temp replacement, and omit timestamps and absolute roots. [ASSUMED]

Regardless of discretionary schema shape, every artifact must preserve the resolved `(regime,base_stage,gold_stage_or_missing)` signature, Hamilton 0.8/0.1/0.1 ratios, local seeded order, and fixed tie order from GAP-39-06. GAP-39-08 constrains the signature values: `base_stage ∈ {0,1,UNASSIGNED}` and `gold_stage_or_missing ∈ {UNASSIGNED,missing}`; gold may never carry `0` or `1`. [VERIFIED: autonomy ruling GAP-39-06; resolved fidelity seam GAP-39-08]

```json
{
  "algorithm": "group-signature-hamilton-v1",
  "ratios": {"test": 0.1, "train": 0.8, "validation": 0.1},
  "schema_version": 1,
  "seed": 1234,
  "tie_order": ["train", "validation", "test"],
  "groups": [
    {
      "physical_key": {"id": 7, "variant": "hierarchical"},
      "signature": {"base_stage": 0, "gold_stage": "UNASSIGNED", "regime": "hierarchical"},
      "records": [
        {"fidelity": "base", "id": 7, "stage": 0, "variant": "hierarchical"},
        {"fidelity": "gold", "id": 7, "stage": "UNASSIGNED", "variant": "hierarchical"}
      ],
      "split": "train"
    }
  ]
}
```

Because grouping precedes expansion, a hierarchical physical group may legitimately have `base_stage=0` or `1` and `gold_stage=UNASSIGNED`. GAP-39-06 preserves that full signature rather than collapsing it: canonically sort keys within each signature, use a local seeded permutation, floor each `N_signature * ratio`, assign remaining groups by descending fractional remainder with fixed `train → validation → test` ties, then expand records. GAP-39-08 prohibits the splitter from copying the base label to gold or recomputing the stage predicate. Report unavoidable rare-signature deviations and never infer or recalibrate stages in the splitter. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-SPEC.md:43-46`; `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198,1654-1665`; autonomy ruling GAP-39-06; resolved fidelity seam GAP-39-08]

## Replay, Lookahead, and Two-Point-Set Contract

- Replay selects 240 trajectories from cumulative `D_<=k`; lookahead selects 16 only from `D_{k+1}` when `has_stage(k+1)` is true. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1813-1828`]
- In Phase 39's production Stage-0 path, `D_<=0` contains only label-0 original/base hierarchical Set 1a records, while `D_1` contains only collapsed Stage-1a/1b records from that same base source. `UNASSIGNED` records are absent from both pools, so no gold trajectory may enter Stage-0 replay or Stage-1 lookahead. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`; GAP-39-08]
- An undersized next-stage pool samples with replacement to 16; a missing next stage yields replay-only, never synthetic lookahead. Replay sampling remains without replacement across the epoch, which Phase 40 will orchestrate. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1827-1840`]
- `has_stage(1)` is true exactly when at least one admitted base Set 1a record carries label `1`; then the real Stage-0 batch exercises 240 replay plus 16 Stage-1 lookahead records. Because Phase 39 emits no Stage-2 label, `has_stage(2)` is false at this seam even though hierarchical gold is authoritative Stage-2 refinement; later Stage-2 production remains deferred. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:189-198,1813-1840`; GAP-39-08]
- Per selected trajectory, use `n_pts=min(32,n_snapshots)` without replacement for data fidelity. The nominal 8,192 data points assumes 256 trajectories; replay-only cardinality is lower unless an explicit padding contract is later supplied. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1819-1836`]
- Data times use a 50/50 mixture: `floor(n/2)` acceleration-weighted samples without replacement, then uniform samples from the remainder; the locked method uses seeded Gumbel-top-k. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1830-1853`]
- Collocation points are independent continuous draws over `[0,T]`, nominally 4,096, and energy reuses that physics set. Adaptive/mixed collocation belongs to Phase 40. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1831-1840`; `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:78-83`]
- Every emitted point carries 14D `[tau,IC13]` plus raw `(3,)` masses with explicit dtype/device transfer at the model boundary. [VERIFIED: `pinn/network.py:210-228`; `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:84-87`]

## Thrust-A Report Schema

The report should be deterministic JSON with: `schema_version`; adapter/hash status; total and per-folder admission dispositions; ordered label-0 and label-1 entries containing record count, physical-key count, and resident tensor bytes; `UNASSIGNED` counts broken down by variant/fidelity; an explicit count of gold records labeled 0/1 that must equal zero; an exact sorted Stage-0 `s_min` vector or auditable sidecar plus count/min/quantiles/max; interim `s0`; and typed fatal-risk entries including threshold 240 and observed base-Set-1a Stage-0 count. It must not mutate a threshold, claim owner ratification, or report gold Set 2a as Stage 0/1. [ASSUMED]

Keep load-time admission counts and Thrust-A stage evidence separate: the former proves parser/gate accounting, while the latter evaluates only admitted metadata. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md` Specific Ideas]

Implement Stage 0 from the complete CTL conjunction only after proving `variant=hierarchical` and `fidelity=base` (original Set 1a): `E < -0.5`, `L/L_max > 0.5`, `0.7 <= Q <= 1.3`, and strict `s_min > s0`. Test `s_min == s0` as excluded, exercise both the `>=240` proceed and `<240` fatal paths using base records only, and assert zero gold labels 0/1. Cite GAP-39-03 for predicate direction and GAP-39-08 for fidelity ownership so neither the reversed phase-SPEC wording nor shared-IC gold leakage can be reintroduced. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md` GAP-39-03 and GAP-39-08; `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Tensor residency/device policy | Global default dtype/device state | Existing explicit `RuntimeSpec` plus caller-supplied dtype/device | Global mutation conflicts with Phase 37 and makes tests/order dependent. [VERIFIED: `pinn/runtime.py`; `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:52-59`] |
| Corpus identity scan | Dense ID loops or permissive glob interpretation | Locked regex scan, folder-derived variant/fidelity, duplicate detection, sorted keys | Standard gold is sparse and filenames are authoritative. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:487-535`; `simulation_data/Documentation/README.md:172-223`] |
| Scientific parser reuse | Wrapper around v1 `pinn/data-handling/` | New adapter parser implementing current README/CTL contract | v1 thresholds and semantics are explicitly stale. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-SPEC.md:20-24`] |
| Conservation score | Footer/metrics lookup, Plummer-softening reuse, or denominator floor | Direct NumPy float64 Hamiltonian recomputation plus GAP-39-04's scale-aware near-zero quarantine | The footer is non-authoritative, `eps=1e-10` is a length softening, and the denominator floor is prohibited. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:562-581`; autonomy ruling GAP-39-04] |
| Hash production | Local file-order/content hash | Compare only to supplied canonical metadata; typed deferral when absent | Producer, scope, normalization, and location are intentionally unratified. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md:3-43`] |
| Stage labels | Independent splitter/query/report classifiers or base-label copying to gold | One pure pre-residency GAP-39-08 classifier whose persisted field is consumed everywhere | Shared ICs do not imply shared curriculum fidelity; CTL reserves gold Set 2a for Stage 2. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`; GAP-39-08] |
| Split stratifier dependency | Third-party package or record-first random split | Small deterministic group-signature allocator using seeded Hamilton apportionment | The resolved domain signature and tie-order contract are clearer than a generic splitter and prevent sibling leakage. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:71-75`; autonomy ruling GAP-39-06] |
| Atomic JSON writes | Partial in-place overwrite | Existing sibling temporary file + `os.replace` pattern | Prevents truncated run artifacts and matches repository scripts. [VERIFIED: Phase 37/38 script serialization patterns] |

**Key insight:** this phase's complexity is contract fidelity, not library selection. GAP-39-03..08 resolve every planning-blocking semantic while preserving which rules are source-authoritative versus autonomy-authorized; no new dependency is needed. [VERIFIED: repository and framework-spec audit; `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md`]

## Common Pitfalls

### Pitfall 1: A Second Parser Appears Indirectly

**What goes wrong:** tests pass, but a scan/report helper reads `.txt` independently and diverges on footer or completeness behavior.
**Why it happens:** convenient utility functions hide disk access.
**How to avoid:** audit production `pinn/` AST/calls for `open`, `read_text`, `.txt` globs, and parser imports; allow only `pinn/data/adapter.py` and exact legacy `pinn/verification/fixture_loader.py`.
**Warning signs:** paths or filename regexes appear in `admission.py`, `batches.py`, or `stage_scan.py`. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:39-50`]

### Pitfall 2: Footer-Driven Completeness or Energy

**What goes wrong:** missing/heterogeneous footers cause false admission, or footer `dE/E` substitutes for Step-1A `eps_H`.
**Why it happens:** the footer looks like a compact summary.
**How to avoid:** final parsed timestamp decides completeness; raw float64 snapshots decide conservation.
**Warning signs:** gate code references `result`, `dE/E`, metrics JSON, line count, or filename metadata. [VERIFIED: `simulation_data/Documentation/README.md:580-649,700-717`; `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:562-581`]

### Pitfall 3: Precision Is Converted Too Early

**What goes wrong:** fp32 gate calculations change marginal classifications or mass-invariance checks.
**Why it happens:** preload dtype is mistaken for gate dtype.
**How to avoid:** parse/evaluate in float64, then convert only admitted resident arrays to fp32.
**Warning signs:** `torch.float32` appears before admission completes. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:52-63`]

### Pitfall 4: Base/Gold Leakage

**What goes wrong:** two fidelities of one physical IC enter different splits.
**Why it happens:** shuffling `record_key`s before grouping.
**How to avoid:** assign physical groups first and hard-assert one split per group.
**Warning signs:** split functions accept only record lists, fidelity appears in the physical grouping key, or base `0`/`1` and gold `UNASSIGNED` are collapsed into one group-level stage. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:71-75`; GAP-39-06 and GAP-39-08]

### Pitfall 5: Determinism Is Seed-Only

**What goes wrong:** identical seeds produce different bytes because filesystem iteration, dict insertion, timestamps, temp paths, or float formatting differ.
**Why it happens:** RNG determinism is confused with artifact determinism.
**How to avoid:** sort before RNG, derive local seeded permutations per complete group signature, use Hamilton apportionment with the fixed tie order, omit unstable metadata, and compare bytes in tests.
**Warning signs:** raw `glob()` order, sets, current timestamps, traversal-order greedy balancing, or unstated remainder ties enter the manifest. [ASSUMED]

### Pitfall 6: Point Sets Become Interchangeable

**What goes wrong:** acceleration weighting is applied to continuous collocation or adaptive behavior leaks into Phase 39.
**Why it happens:** one generic sampler/points field serves both roles.
**How to avoid:** separate types/functions and assert source domains in tests.
**Warning signs:** the collocation function receives snapshot accelerations or last residuals. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1813-1853`]

### Pitfall 7: The Routed SPEC Defect Is Reintroduced

**What goes wrong:** Stage-0 population is inverted relative to the authoritative CTL, changing the fatal training decision.
**Why it happens:** the derived Phase 39 SPEC still contains the reversed predicate even though GAP-39-03 resolved source precedence.
**How to avoid:** cite GAP-39-03 plus CTL lines 138–150 in every DATA-06 plan, test strict `s_min > s0` as part of the full Stage-0 conjunction, and apply it only after the GAP-39-08 base-Set-1a fidelity guard.
**Warning signs:** equality is admitted to Stage 0, `s_min > s0` is labeled as a Stage-1 discriminator by itself, or any gold record enters the Stage-0 population. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md` GAP-39-03 and GAP-39-08; `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`]

### Pitfall 8: Autonomy Rulings Drift Into Different Semantics

**What goes wrong:** implementation substitutes `1e-10` for the near-zero energy tolerance, salvages a trajectory after deleting corrupt evidence, uses a global greedy split, reports RSS as the DATA-01 byte payload, or copies base Stage-0/1 membership to gold.
**Why it happens:** GAP-39-04..08 are treated as loose recommendations or, conversely, every seam is cited as though it amended the CTL; GAP-39-08 instead carries an already-authoritative fidelity boundary into production.
**How to avoid:** cite the exact gap resolution beside each implementation and acceptance test, implement its numerical/ordering/accounting rule literally, and retain provenance distinguishing autonomy defaults from the CTL-grounded Set 1a/Set 2a boundary.
**Warning signs:** no `64*finfo(float64).eps` boundary test; an admitted outcome with `dropped_samples>0`; absent signature/tie-order metadata; `resident_tensor_bytes` changes after unrelated process allocation; or any gold `stage_label` equals 0 or 1. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md` GAP-39-04..08; `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`]

### Pitfall 9: Physical Siblings Are Mistaken for Curriculum Peers

**What goes wrong:** a base/gold hierarchical pair shares invariants, so both are classified Stage 0 or 1; gold Set 2a then contaminates replay, lookahead, the fatal population count, and split strata.
**Why it happens:** grouping by `physical_key` is incorrectly interpreted as assigning one stage per group rather than one split per group and one stage label per record.
**How to avoid:** classify records before grouping, hard-return `UNASSIGNED` for every non-base record, retain `(base_stage,gold_stage_or_missing)` in the signature, and assert that all gold labels are unassigned at adapter, manifest, query, batch, and report boundaries.
**Warning signs:** a present gold signature value is anything other than `UNASSIGNED`; a numeric stage query contains fidelity `gold`; or the Stage-0 report count increases when gold files are added. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`; GAP-39-08]

## Code Examples

Verified patterns from repository contracts; names are proposed, not existing APIs.

### Typed Hash Outcomes

```python
# Source: 39-CONTEXT.md D-05 and 39-GAPS.md GAP-39-01
@dataclass(frozen=True)
class DataVersionHashDeferred:
    reason: str = "canonical data_version_hash metadata absent"


def verify_data_version(
    *, expected: str | None, supplied: str | None
) -> DataVersionHashVerified | DataVersionHashDeferred:
    if supplied is None:
        return DataVersionHashDeferred()
    if expected is not None and supplied != expected:
        raise DataVersionMismatch(expected=expected, supplied=supplied)
    return DataVersionHashVerified(value=supplied)
```

The adapter logs the deferred result prominently and proceeds; absence must remain observable and must not be represented as `True`. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:64-69`]

### Fidelity-Gated Stage Classifier

```python
# Source: ctl_instruction.md:23-28,138-198 and GAP-39-08
def classify_stage(record: AdmittedTrajectory, *, s0: float) -> StageLabel:
    if record.variant != Variant.HIERARCHICAL or record.fidelity != Fidelity.BASE:
        return StageLabel.UNASSIGNED

    if record.E < -0.5 and record.l_ratio > 0.5 and 0.7 <= record.Q <= 1.3 and record.s_min > s0:
        return StageLabel.STAGE_0

    stage_1a = -0.5 <= record.E < -0.1 and record.l_ratio > 0.5
    stage_1b = record.E < -0.5 and 0.1 <= record.l_ratio < 0.5
    if (stage_1a or stage_1b) and 0.7 <= record.Q <= 1.3 and record.s_min > s0:
        return StageLabel.STAGE_1

    return StageLabel.UNASSIGNED
```

The fidelity guard must precede the invariant predicates. Moving it afterward or classifying once per `physical_key` would assign shared-IC gold Set 2a records to Stage 0/1 incorrectly. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`; GAP-39-08]

### Group-First Leakage Assertion

```python
# Source: 39-CONTEXT.md D-06 / CLEARANCE.md PB-4
seen: dict[PhysicalKey, SplitName] = {}
for group in manifest.groups:
    previous = seen.setdefault(group.physical_key, group.split)
    if previous != group.split:
        raise AssertionError(f"physical_key spans splits: {group.physical_key}")
```

### Independent Point Sets

```python
# Source: ctl_instruction.md:1813-1853
@dataclass(frozen=True)
class FixedBatch:
    trajectory_keys: tuple[RecordKey, ...]
    data_points: DataFidelityPoints
    collocation_points: PhysicsCollocationPoints
    tau_ic13: torch.Tensor
    raw_masses: torch.Tensor
```

### Deterministic Artifact Write

```python
# Source: existing Phase 37/38 JSON artifact writers
payload = json.dumps(manifest.to_json(), sort_keys=True, indent=2) + "\n"
temporary = destination.with_suffix(destination.suffix + ".tmp")
temporary.write_text(payload, encoding="utf-8")
os.replace(temporary, destination)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| v1 `pinn/data-handling/` imports and stale stage thresholds | Clean Phase 39 modules implementing ratified specs | Trainex rebuild / CTX-17 | No legacy import; formulas must be ported deliberately. [VERIFIED: `pinn/constants.py:9-11`; `.planning/phases/39-data-ingestion-stage-0-population-scan/39-SPEC.md:20-24`] |
| HDF5 conversion and disk-backed flow | D3-C admitted-set fp32 preload with `num_workers=0` | trainex-r1a ratification | Format stays hidden behind one in-memory adapter. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/trainex-r1a-resolution-doc.md:23-49,64-65`] |
| Record-level random split | Physical-key grouping before record expansion | integrity-r2 PB-4 | Base/gold leakage becomes mechanically impossible. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/CLEARANCE.md:23-27`] |
| Source-silent stage balancing | Complete group signature plus seeded per-signature Hamilton apportionment | GAP-39-06 autonomy ruling | DATA-04 now has deterministic counts, ties, and rare-signature evidence without claiming framework authority. [VERIFIED: autonomy ruling GAP-39-06] |
| Group-level or invariant-only stage labels | Record-level fidelity guard plus persisted `0`/collapsed `1`/`UNASSIGNED` | CTL Set 1a/2a boundary + GAP-39-08 | Base Set 1a supplies Stage 0/1; gold Set 2a stays unassigned until later Stage-2 work. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`; GAP-39-08] |
| Ambiguous process-memory log | Deduplicated owned-fp32 `resident_tensor_bytes` | GAP-39-07 autonomy ruling | DATA-01 has a deterministic payload assertion; RSS/MPS remain separately named optional telemetry. [VERIFIED: autonomy ruling GAP-39-07] |
| One sampled point set | Independent data-fidelity and continuous collocation sets | integrity-r2 PB-3 | Sampling policy cannot cross-contaminate physics points. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/CLEARANCE.md:23-27`] |
| Implicit/absent version checking | Compare-and-refuse plus typed absent-field deferral | Phase 39 D-05 | Missing canonical producer remains visible rather than fabricated. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md:3-43`] |

**Deprecated/outdated:**

- v1 Stage-0 threshold logic (`s_min>2`) is stale and must not be copied. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-SPEC.md:20-24`]
- The README statement that all Brutus files have a footer is superseded by its later verified missing-footer inventory. [VERIFIED: `simulation_data/Documentation/README.md:283,580-628`]
- `pinn/verification/fixture_loader.py` is not deprecated, but its parser is probe-only and cannot become the Phase 39 adapter. [VERIFIED: `pinn/verification/fixture_loader.py:1-16`; `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:42-50`]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The proposed module/file decomposition is the simplest audit-friendly layout. | Exact Implementation Surfaces | Low; files can be combined without changing behavior if parser ownership stays explicit. |
| A3 | Main-repo fallback may use Git common-directory discovery when `GSD_DATA_ROOT` is absent. | Parsing and Data Facts | Medium; runtime environments without Git would need the env override. |
| A4 | Canonical JSON should omit timestamp and absolute-path provenance. | Split Manifest Schema | Low; those fields can live in a separate non-canonical report. |
| A5 | The report schema proposed here is sufficient for Thrust-A auditability. | Thrust-A Report Schema | Medium; no authoritative process-artifact schema exists. |
| A6 | Typed outcome objects and distinct data/collocation fields are the safest internal API shape. | Architecture Patterns / Required Interfaces | Low; equivalent explicit types could preserve the same behavior. |
| A7 | The proposed synthetic fixture matrix, real-scan CLI shape, and validation cadence are appropriate. | Validation Architecture | Low; command names may change while coverage remains mandatory. |
| A8 | The proposed Waves 0–5 are the minimal dependency order. | Dependency and Wave Order | Low; tasks may be combined if dependency gates remain intact. |
| A9 | Root containment, exact filename scanning, and atomic run-artifact writes are sufficient local hardening. | Security Domain | Low; stricter deployment-specific controls may be added later. |

These assumptions are implementation recommendations within the agent's discretion, not science rulings. They do not alter the resolved GAP-39-03..08 contracts below. [ASSUMED]

## Resolved Rulings (No Planning Blockers)

The authoritative sources remain unchanged. GAP-39-04..07 record concrete defaults authorized under the user's full-autonomy instruction so the planner can execute DATA-01, DATA-02, and DATA-04 without inventing semantics. GAP-39-08 carries the authoritative CTL Set 1a/Set 2a fidelity boundary into one production label seam; collapsing Stage 1a/1b to query label `1` is the authorized implementation choice, not a new Stage-2 assignment. GAP-39-03 separately resolves DATA-06 predicate precedence. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md` GAP-39-03..08; `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`]

### GAP-39-04 — Scale-aware near-zero `H(0)`

Use `scale = |K0| + |V0|` from the separately computed float64 kinetic and potential terms. Quarantine when `H0 == 0.0` or when `scale > 0` and `|H0| <= 64 * finfo(float64).eps * scale`. Only otherwise divide by `H0`; never add, clamp, or maximize against a denominator floor. The `64` factor is a reversible safety factor selected by autonomy, not a source-authored constant. [VERIFIED: autonomy ruling GAP-39-04]

**Acceptance:** exact zero and the boundary quarantine; `nextafter` immediately above the boundary and a small well-resolved value do not; an AST/mechanical prohibition catches denominator floors; the full-corpus gate records the resulting near-zero quarantine count. [VERIFIED: autonomy ruling GAP-39-04]

### GAP-39-05 — Non-finite block means whole-trajectory quarantine

Count and drop every non-finite snapshot block in sample accounting, retain finite blocks only for subsequent diagnostic checks, and quarantine the entire trajectory with `non_finite_snapshot`. Never admit a partially salvaged trajectory even if at least two finite monotone snapshots remain. [VERIFIED: autonomy ruling GAP-39-05]

**Acceptance:** an interior-corruption fixture increments `dropped_samples` once and yields quarantine while an all-finite control remains eligible; a fixture leaving fewer than two retained blocks records both non-finite and structural reasons; partial body-row salvage is prohibited; trajectory and sample accounting identities remain separate and exact. [VERIFIED: autonomy ruling GAP-39-05]

### GAP-39-06 — Complete-signature Hamilton split

Treat each `physical_key` as one indivisible unit with signature `(regime, base_stage, gold_stage_or_missing)`. Canonically sort keys, apply a deterministic local seeded permutation per signature, and apportion each signature's group count using Hamilton largest remainder at 0.8/0.1/0.1. Break equal remainders in fixed `train → validation → test` order, expand to records afterward, and report unavoidable rare-signature deviations. Consume GAP-39-08 labels without inference: gold is always `UNASSIGNED` when present. [VERIFIED: autonomy ruling GAP-39-06; resolved fidelity seam GAP-39-08]

**Acceptance:** input order does not change manifest bytes; no physical key spans splits; every signature matches exact Hamilton counts and tie order; changing the seed changes eligible identities but not counts; base labels 0/1 remain paired with gold `UNASSIGNED` siblings in one split; no signature contains gold 0/1; rare signatures emit deterministic deviation evidence. [VERIFIED: autonomy ruling GAP-39-06; resolved fidelity seam GAP-39-08]

### GAP-39-07 — Deterministic resident tensor payload

Define DATA-01's primary `mem: <bytes>` numerator as deduplicated bytes of owned, admitted fp32 tensor storage, named `resident_tensor_bytes`, divided by explicitly configured capacity. Count each underlying storage once so views do not inflate the metric. Temporary parser arrays, model tensors, RSS, and MPS allocator state are excluded; separately named RSS/MPS metrics may be supplemental but cannot replace the assertion. [VERIFIED: autonomy ruling GAP-39-07]

**Acceptance:** a 40-byte tensor, a shared-storage view, and an independent 20-byte tensor report 60 bytes rather than 80; with test capacity 100 the exact log is `mem: 60 (0.600000) watermark=0.7`; unrelated process allocation leaves the payload unchanged; the real adapter value equals the sum of unique admitted storage byte sizes. [VERIFIED: autonomy ruling GAP-39-07]

### GAP-39-08 — Base-Set-1a-only Stage-0/1 seam

Persist exactly one record-level `stage_label ∈ {0,1,UNASSIGNED}` before residency. Evaluate authoritative Stage 0 first and Stage 1a/1b second only for original/base hierarchical Set 1a, collapsing either Stage-1 branch to label `1`. Hierarchical gold Set 2a and all standard or otherwise ineligible records remain `UNASSIGNED`; Phase 39 assigns no Stage 2–6 label. The adapter, signature builder, `StageQuery`, batch constructor, and report all consume this same field. [VERIFIED: `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`; GAP-39-08]

**Acceptance:** paired records with identical Stage-0-satisfying IC invariants yield base `0` and gold `UNASSIGNED`; paired Stage-1a and Stage-1b fixtures each yield base `1` and gold `UNASSIGNED`; `records_at(0)`, `records_at(1)`, `records_at_or_below(1)`, Stage-0 replay, and Stage-1 lookahead contain no gold keys; `has_stage(1)` reflects only base Set 1a; `has_stage(2)` remains false; the report and full-corpus evidence show zero gold records labeled 0 or 1. [VERIFIED: GAP-39-08]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| `pinn-train` Python | all code/tests | ✓ | Python 3.11 environment | None needed. [VERIFIED: `$HOME/miniforge3/envs/pinn-train/bin/python`] |
| PyTorch | resident tensors/model interface | ✓ | 2.12.1 | None needed. [VERIFIED: environment import and `conda-lock.yml`] |
| NumPy | float64 admission/preprocessing | ✓ | 2.4.6 | None needed. [VERIFIED: environment import and `conda-lock.yml`] |
| `unittest` | phase tests | ✓ | Python stdlib | None needed. [VERIFIED: environment probe] |
| `pytest` | not required | ✗ | not installed in `pinn-train` | Use repository-standard `unittest`. [VERIFIED: environment import probe] |
| `psutil` | not required by GAP-39-07 | ✗ | not installed in `pinn-train` | Count unique owned Torch storage directly; RSS is not the DATA-01 numerator. [VERIFIED: environment import probe; autonomy ruling GAP-39-07] |
| Real corpus | dataset-backed acceptance/scan | ✓ outside worktree | 6.3 GB text corpus | `GSD_DATA_ROOT=<home>/Desktop/3_body_problem/simulation_data/Data`; synthetic fixtures for quick tests. [VERIFIED: direct filesystem probe] |
| Blacklist JSON | Step-1A clause 1 | ✓ outside worktree | 65 IDs | No fallback; fail closed. [VERIFIED: direct JSON inspection; `ctl_instruction.md:609-638`] |

**Missing dependencies with no fallback:** none for the locked implementation. [VERIFIED: environment audit]

**Missing dependencies with fallback:** `pytest` is absent but unnecessary because the established suite uses `unittest`; `psutil` is absent and intentionally unnecessary because GAP-39-07 uses deterministic tensor-storage payload rather than process RSS. [VERIFIED: `tests/phase37/`; `tests/phase38/`; autonomy ruling GAP-39-07]

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Python `unittest` under `pinn-train` [VERIFIED: `tests/phase37/`; `tests/phase38/`] |
| Config file | none; discovery-based [VERIFIED: repository test layout] |
| Quick run command | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests/phase39 -p 'test_*.py' -v` |
| Full suite command | `$HOME/miniforge3/envs/pinn-train/bin/python -m unittest discover -s tests -p 'test_*.py' -v` |

### Synthetic / Dataset-Free Suite

`tests/phase39/_fixtures.py` should write tiny IC/Brutus/blacklist trees under `TemporaryDirectory`, including present/full footer, each folder-specific missing-footer default, duplicate IDs, truncated time, nonmonotone time, non-finite blocks, near-zero `H0`, controlled SCS boundaries, and paired base/gold hierarchical records satisfying Stage 0, Stage 1a, and Stage 1b. The paired records should share IC invariants so only fidelity can explain base `0`/`1` versus gold `UNASSIGNED`. No synthetic test may write inside `simulation_data/`. [ASSUMED]

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DATA-01 | parser shapes, folder identity, defaults/provenance, accessors, fp32 residency, unique-storage `resident_tensor_bytes`, exact memory log, empty failure | unit/integration | `...python -m unittest tests.phase39.test_adapter -v` | ❌ Wave 0 |
| DATA-02 | all clause outcomes; float64 recompute; GAP-39-04 exact/boundary/`nextafter` predicate and no-floor prohibition; GAP-39-05 dropped-block quarantine/accounting; SCS boundaries | unit | `...python -m unittest tests.phase39.test_admission -v` | ❌ Wave 0 |
| DATA-03 | match, mismatch hard refusal, absent typed deferral | unit | `...python -m unittest tests.phase39.test_adapter.DataVersionTests -v` | ❌ Wave 0 |
| DATA-04/05/06 | GAP-39-08 base-only Stage 0, collapsed base Stage 1a/1b, all gold `UNASSIGNED`, one persisted label consumed by all downstream surfaces | unit | `...python -m unittest tests.phase39.test_stages -v` | ❌ Wave 0 |
| DATA-04 | complete signatures with base `0`/`1`/`UNASSIGNED` and gold `UNASSIGNED`/missing, per-signature Hamilton counts/ties, no leakage, input-order independence, seeded stable bytes, rare-signature evidence | unit | `...python -m unittest tests.phase39.test_splits -v` | ❌ Wave 0 |
| DATA-05 | 240 base-Set-1a replay plus 16 base-Set-1a Stage-1 lookahead when present; zero gold; missing/undersized next pool; separate points; sampling and shapes | unit | `...python -m unittest tests.phase39.test_batches -v` | ❌ Wave 0 |
| DATA-06 | base-Set-1a-only CTL Stage-0 conjunction; strict `s_min > s0`; equality and all gold excluded; collapsed Stage-1 counts; report zero-gold invariant; `>=240`/`<240` mechanics | unit | `...python -m unittest tests.phase39.test_stage_scan -v` | ❌ Wave 0 |
| DATA-01/02 | only adapter plus exact fixture-loader exception reads corpus; no v1 imports/writes/global defaults | AST/mechanical | `...python -m unittest tests.phase39.test_prohibitions -v` | ❌ Wave 0 |

### Real Dataset-Backed Gate

Synthetic tests cannot prove the real folder/default distribution, direct-parse accessor match, admitted population, near-zero/non-finite disposition counts, deduplicated memory fraction, signature distribution, Stage-0/1 base pools, or Thrust-A counts. Run one full-corpus initialization/scan using the external data root and a temporary run directory, capture logs/report/manifest, and compare at least one accessor result to the retained direct probe parse. Recompute unique admitted-storage bytes, verify per-signature Hamilton allocations and no leakage, record GAP-39-04/05 counts, and confirm that Stage 0 plus collapsed Stage 1a/1b are computed only from original/base hierarchical Set 1a. The evidence must show any real Stage-0 replay and Stage-1 lookahead keys are base, `has_stage(1)` reflects only base Set 1a, hierarchical gold Set 2a remains `UNASSIGNED`, and the count of gold records labeled 0/1 is exactly zero. This is a phase gate, not a per-commit command, because the source is 6.3 GB of text. [VERIFIED: direct corpus probe; `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md` GAP-39-03..08; `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:23-28,138-198`]

```bash
GSD_DATA_ROOT=<home>/Desktop/3_body_problem/simulation_data/Data \
  $HOME/miniforge3/envs/pinn-train/bin/python -m pinn.data.stage_scan \
  --run-dir /tmp/phase39-real-scan
```

The command shape is proposed and should be adjusted to the final CLI, but the real-corpus gate itself is mandatory. [ASSUMED]

### Sampling Rate

- **Per task commit:** targeted dataset-free module test plus `tests.phase39.test_prohibitions`.
- **Per wave merge:** complete `tests/phase39` suite.
- **Phase gate:** full repository suite, full real-corpus adapter/scan, artifact inspection, reader audit, and `git diff --check` all green.

### Wave 0 Gaps

- [ ] `tests/phase39/__init__.py` and `_fixtures.py` — deterministic tiny corpus builder.
- [ ] `tests/phase39/test_adapter.py` — DATA-01/03 contracts, including GAP-39-07 unique-storage accounting and stable memory logging.
- [ ] `tests/phase39/test_admission.py` — DATA-02 numerical boundaries and exact GAP-39-04/05 disposition/accounting contracts.
- [ ] `tests/phase39/test_stages.py` — GAP-39-08 Stage-0/1 predicates, collapsed label, base/gold fidelity guard, and all-gold-`UNASSIGNED` invariant.
- [ ] `tests/phase39/test_splits.py` — DATA-04 GAP-39-06/08 signatures, Hamilton counts/ties, grouping, determinism, and zero gold 0/1 labels.
- [ ] `tests/phase39/test_batches.py` — DATA-05 fixed shapes/two point sets, Set-1a-only Stage-0 replay/Stage-1 lookahead, and no gold keys.
- [ ] `tests/phase39/test_stage_scan.py` — DATA-06 base-only CTL Stage-0/1 classifier consumption, strict boundary, zero-gold report invariant, and fatal mechanics; cite GAP-39-03/08.
- [ ] `tests/phase39/test_prohibitions.py` — exact-reader allowlist, v1 import ban, read-only corpus, global-default ban.

## Dependency and Wave Order

| Wave | Deliverable | Requirements | Depends on | Parallelism |
|------|-------------|--------------|------------|-------------|
| 0 | Test package, synthetic format builder, frozen key/outcome/batch types | all | none | Types and fixture builder can proceed together. [ASSUMED] |
| 1 | Pure parser contract, preprocessing/invariants, GAP-39-04/05 admission gates, GAP-39-08 Stage-0/1 classifier, hash outcome types | DATA-01..03/06 | Wave 0 | Stage classifier follows invariant computation and is independently boundary-testable before adapter integration. [ASSUMED] |
| 2 | Production adapter initialization, persisted stage labels, blacklist/root resolver, fp32 resident set, accessors, GAP-39-07 storage accounting/log | DATA-01..03/06 | Wave 1 | Serial integration point; audit shared-storage accounting and assert every gold label is `UNASSIGNED`. [ASSUMED] |
| 3 | GAP-39-06/08 signature-Hamilton manifest and admitted-set stage query protocol | DATA-04 | Wave 2 persisted record labels | Split/query consume the same label; neither reclassifies or copies base stage to gold. [ASSUMED] |
| 4A | Set-1a-only replay/lookahead batch constructor and two point sets | DATA-05 | Waves 2-3 query API | Can proceed independently of report serialization; assert zero gold batch keys. [ASSUMED] |
| 4B | Thrust-A Stage-0/1 report and fatal-risk mechanics over persisted labels | DATA-06 | Wave 2 | Can proceed in parallel with batching; cite GAP-39-03/08 and assert zero gold labels 0/1. [ASSUMED] |
| 5 | Full real-corpus scan, evidence, reader audit, and full regression | all | Waves 3–4 | Final serial gate. [ASSUMED] |

The planner should not place full-corpus parsing on every task's verification path. Keep the expensive dataset-backed run in the final wave and rely on byte-small synthetic fixtures earlier. GAP-39-03..08 remove planning checkpoints; dependencies are now implementation/data-flow dependencies only. [VERIFIED: direct corpus size, repository test conventions, and resolved gap register]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no | Local scientific-data pipeline; no identity boundary. [VERIFIED: Phase 39 scope] |
| V3 Session Management | no | No sessions or network service. [VERIFIED: Phase 39 scope] |
| V4 Access Control | no | No multi-user authorization surface; corpus is read-only by contract. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:39-44`] |
| V5 Input Validation | yes | Exact regex/folder schema, blacklist schema, numeric/shape/finite/monotonic/completeness gates, duplicate rejection, and root containment. [VERIFIED: `simulation_data/Documentation/README.md:193-300`; `ctl_instruction.md:487-607`] |
| V6 Cryptography | limited | Use stdlib exact string/digest comparison for supplied version metadata; no custom hash producer or cryptographic claim. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md:3-43`] |

### Known Threat Patterns for Local Scientific Ingestion

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Path traversal/symlink escape from configured root | Tampering / Information disclosure | Resolve roots and scanned paths, require membership under the configured corpus root, and scan only exact expected filenames. [ASSUMED] |
| Malformed or oversized numeric text | Denial of service | Validate block shape incrementally, fail closed on malformed records, keep `num_workers=0`, and log disposition counts. [VERIFIED: locked parsing/admission constraints] |
| Corrupt/missing blacklist | Tampering | Schema validation and hard initialization failure; no empty fallback. [VERIFIED: `ctl_instruction.md:609-638`] |
| Split manifest overwrite/partial write | Tampering | Write only under caller-supplied run folder using atomic replacement and canonical serialization. [ASSUMED] |
| Hash mismatch ignored | Tampering | Hard refusal on mismatch; typed observable deferral only when canonical metadata is absent. [VERIFIED: `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md:64-69`] |
| Corpus mutation by test/scan | Tampering | Production adapter opens corpus read-only; tests use temp roots; prohibition test spies on writes beneath `simulation_data/`. [VERIFIED: `tests/phase38/test_prohibitions.py`; project constraints] |

## Sources

### Primary (HIGH confidence)

- `.planning/phases/39-data-ingestion-stage-0-population-scan/39-SPEC.md` — locked DATA-01..06 scope and acceptance.
- `.planning/phases/39-data-ingestion-stage-0-population-scan/39-CONTEXT.md` — owner decisions D-01..08 and exact Phase 38 exception.
- `.planning/phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md` — hash deferral, reader exception, Stage-0 precedence, reversible autonomy rulings GAP-39-04..07, and the GAP-39-08 production Stage-0/1 fidelity seam.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — parser, Step-1A, preprocessing, invariants, IC13, stage, and batch contracts.
- `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/CLEARANCE.md` — PB-1/PB-3/PB-4 and corrected resident-size estimate.
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/trainex-r1a-resolution-doc.md` and `RATIFICATION.md` — D3-C and U-12.
- `simulation_data/Documentation/README.md` plus direct read-only corpus inspection — format, population, footer, identity, and completeness facts.
- `pinn/network.py`, `pinn/runtime.py`, `pinn/constants.py`, and `pinn/verification/fixture_loader.py` — live interface and exact exception boundaries.
- `tests/phase37/` and `tests/phase38/` — current validation and prohibition patterns.

### Secondary (MEDIUM confidence)

- None. External documentation was unnecessary because Phase 39 installs no packages and is governed by repository-specific contracts. [VERIFIED: research scope audit]

### Tertiary (LOW confidence)

- The implementation-layout, canonical-JSON serialization details, report schema, and wave-placement recommendations marked `[ASSUMED]`; all are listed in the Assumptions Log. The four GAP-39-04..07 defaults are resolved autonomy rulings, while GAP-39-08 carries an authoritative CTL fidelity boundary into the production seam; neither is a tertiary research claim.

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH — versions and environment availability were checked locally; no package installation is proposed.
- Architecture: HIGH — ownership follows locked single-reader, precision, grouping, point-set, and one-classifier contracts; suggested filenames are LOW-risk assumptions.
- Parsing/admission: HIGH — dataset/CTL constraints are verified and GAP-39-04/05 supply exact, user-authorized reversible implementation boundaries with complete acceptance tests.
- Splitting: HIGH — GAP-39-06 resolves the Hamilton objective and GAP-39-08 constrains signatures to base `0`/`1`/`UNASSIGNED` plus gold `UNASSIGNED`/missing without altering physical-key grouping.
- Batching: HIGH — pool sizes and point-set contracts are explicit, and GAP-39-08 makes Stage-0 replay/Stage-1 lookahead base-Set-1a-only with no gold membership.
- Stage scan: HIGH — GAP-39-03 resolves predicate precedence and GAP-39-08 enforces original/base Set 1a ownership, collapsed Stage 1, and zero gold labels 0/1.
- Memory accounting: HIGH — GAP-39-07 resolves the deterministic owned-storage numerator and excludes RSS/MPS substitution; implementation tests can verify exact byte identity.
- Pitfalls: HIGH — derived from direct repository contradictions, format inventory, locked prohibitions, and resolved GAP-39-03..08 drift risks.

**Research date:** 2026-07-13
**Valid until:** 2026-08-12 for stable repository facts; revisit if the authoritative CTL changes or the user supersedes any GAP-39-03..08 ruling.
