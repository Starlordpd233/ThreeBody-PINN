# Phase 39: Data Ingestion & Stage-0 Population Scan - Context

**Gathered:** 2026-07-13
**Status:** Ready for planning — owner rulings recorded 2026-07-13

## Phase Boundary

Phase 39 delivers the Phase-40-independent data substrate: an in-memory
admitted-set adapter, full Step-1A admission, a grouped split manifest,
fixed-shape Stage-0 batches, and the Thrust-A population scan. This context
records implementation decisions only. The six DATA requirements, their
boundaries, and their acceptance criteria are locked by `39-SPEC.md` at
commit `4fed73f4`; this document does not reopen their what or why.

## Requirements (locked via SPEC.md)

**6 requirements are locked.** See `39-SPEC.md` for full requirements,
boundaries, and acceptance criteria.

Downstream agents MUST read `39-SPEC.md` before planning or implementing.
Requirements are not duplicated here.

**In scope (from SPEC.md):**

- The D3-C in-memory fp32 admitted-set adapter with `n_snapshots` / `dt_out`
  accessors and the `mem:` watermark log (DATA-01).
- The full Step-1A admission gate, including float64 `eps_H` recomputation
  (DATA-02).
- Compare-and-refuse `data_version_hash` handling with the typed absent-field
  deferral (DATA-03).
- A `physical_key`-grouped, stage-stratified split manifest (DATA-04).
- A replay/lookahead two-point-set constructor for fixed-shape Stage-0 batches
  (DATA-05).
- The Thrust-A Stage-0 population scan, `s_min` report, and fatal-class flag
  (DATA-06).

**Out of scope (from SPEC.md):**

- Phase 40's adaptive collocation sampler interface and training-loop plumbing.
- The full curriculum-statistics EDA and Stage 1–6 threshold recalibration
  (FUT-02).
- Owner ratification of `s0`; Phase 39 reports evidence and keeps the interim
  `0.01` seam only.
- A `data_version_hash` producer or canonical generation algorithm.
- Reimplementation of the Phase 38 network or loss catalog.

## Implementation Decisions

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

### Claude's Discretion

- Internal module names, admitted-set data structures, report/manifest
  serialization, and test-fixture mechanics are implementation choices, as long
  as they preserve the locked interfaces and acceptance criteria.
- The Phase 39 tests may reuse the established Phase 37/38 test style, but must
  not broaden into Phase 40 adaptive sampling or training-loop work.

## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Locked Phase 39 scope

- `.planning/phases/39-data-ingestion-stage-0-population-scan/39-SPEC.md` —
  the locked DATA-01 through DATA-06 requirements, boundaries, and acceptance
  criteria from Agent A's handoff commit `4fed73f4`.
- `.planning/ROADMAP.md` §Phase 39 — Phase 39 goal and its independence from
  Phase 38.
- `.planning/REQUIREMENTS.md` §Data Ingestion & Stage-0 Population Scan —
  canonical DATA-01 through DATA-06 requirement mapping.

### Data and curriculum contracts

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
  §Step-1A, §stage queries, and §replay/lookahead batch contract — admission
  clauses, Stage-0/1 boundary, and point-set semantics.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
  §input/output contract — `[tau, IC13]` plus explicit raw masses.
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/decision-adjudication/trainex-r1a-resolution-doc.md`
  §D3-C and U-12 — in-memory fp32 / `num_workers=0` and the open hash-production
  mechanism.
- `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/CLEARANCE.md`
  §PB-1, §PB-3, §PB-4 — interim `s0`, independent point sets, and physical-key
  split invariants.
- `simulation_data/Documentation/README.md` §File Schemas, File Naming
  Conventions, and Mandatory Parsing Rules — authoritative on-disk data format
  and final-timestamp completeness rule.

### Existing code and tests

- `pinn/runtime.py` — immutable explicit runtime profiles; no device inference
  or global default-dtype mutation.
- `pinn/network.py` §`SQRSkipResNetSIREN.forward` — caller-supplied 14D inputs
  and raw masses.
- `pinn/verification/fixture_loader.py` — Phase 38 probe-local parser and
  provenance loader; it is evidence for GAP-39-02, not an approved adapter
  implementation.
- `tests/phase37/test_runtime.py` and `tests/phase38/` — current explicit
  runtime and verification-test patterns.
- `tests/phase38/test_prohibitions.py` — Phase 38 fixture-loader consumers and
  its read-only/data-write prohibition coverage.

## Existing Code Insights

### Reusable Assets

- `pinn.runtime.RuntimeSpec` / `resolve_runtime`: new data-facing tensors must
  preserve explicit dtype/device flow rather than create a new global policy.
- `pinn.network.SQRSkipResNetSIREN.forward(tau_ic13, masses)`: the batch
  boundary must retain the complete 14D input and raw-mass side channel.
- Phase 37/38 tests: use focused per-phase tests and mechanical prohibition
  checks as the closest validation pattern.

### Established Patterns

- `pinn/verification/fixture_loader.py` is intentionally a read-only,
  single-trajectory verification helper. It implements no Step-1A admission,
  split, batch, or hash policy and must not be silently repurposed.
- `pinn/data-handling/` is legacy v1 code and may not be imported by the new
  implementation (CTX-17).
- `simulation_data/` is read-only; no adapter, test, or scan may create,
  mutate, move, or delete corpus files.

### Integration Points

- The adapter and batch constructor feed the Phase 38 network contract but do
  not own epoch iteration, loss wiring, or adaptive collocation.
- The split manifest and Stage-0 report are run artifacts consumed by later
  training orchestration, not a Phase 39 training loop.

## Specific Ideas

- Make the load-time count report and the Thrust-A report separately auditable:
  the former explains admission outcomes per folder; the latter reports stage
  population, bytes, and `s_min` without ratifying a threshold.
- Keep the two point sets visibly distinct in the batch type/API so the
  data-fidelity-only mixed sampler cannot accidentally apply to collocation.
- Make the DATA-01 parser audit explicit: it protects the production ingestion
  surface and permits only the already-existing probe-local
  `pinn/verification/fixture_loader.py` exception.
- Exercise the locked boundary cases directly: `SCS = -5`, near-zero `H(0)`,
  absent hash metadata, no `k+1` stage, a next-stage pool smaller than 16, and
  `s_min = s0`.

## Deferred Ideas

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

### Reviewed Todos (not folded)

- D-06 static epsilon sensitivity check — future research/validation work, not
  an ingestion or Stage-0 population-scan requirement.
- trainex-r1 research handoff — no direct DATA-01..06 mapping; retain as a
  research carryover rather than adding it to Phase 39.

---

*Phase: 39-data-ingestion-stage-0-population-scan*
*Context gathered: 2026-07-13*
