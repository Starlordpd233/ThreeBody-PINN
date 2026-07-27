---
phase: 46-frame-resolution-gate-aligned-validation
plan: "04"
subsystem: verification
tags: [conf-01, frame-probe, evidence, d-05, split-manifests, deterministic-serialization, containment]

requires:
  - phase: 46-frame-resolution-gate-aligned-validation
    provides: 46-02 probe core (probe_population/decide_verdict/outcome types) this plan serializes
provides:
  - resolve_probe_population (manifest-parametric D-02 eligibility, no withheld-split view)
  - render_evidence_payload / write_frame_probe_evidence (deterministic D-05 artifact)
  - python -m pinn.verification.target_frame_probe CLI (single sanctioned entry point)
  - tests/phase46/test_frame_probe_evidence.py (12 dataset-free tests, zero skips)
affects: [46-06 real-corpus evidence run, 46-VERDICT branch routing]

tech-stack:
  added: []
  patterns:
    - "Population rule as a recorded module constant quoted into the evidence payload"
    - "Resolution-source-label provenance (never absolute paths) with a fail-closed redaction guard"
    - "Containment-guarded evidence writer: simulation_data and corpus-root refusal + non-overwriting UTC run dirs"

key-files:
  created:
    - tests/phase46/test_frame_probe_evidence.py
    - .planning/phases/46-frame-resolution-gate-aligned-validation/deferred-items.md
  modified:
    - pinn/verification/target_frame_probe.py
    - tests/phase39/test_prohibitions.py

key-decisions:
  - "Exclusion ledger is keyed on PhysicalKey read from manifest payloads, so the excluded set is exactly the supplied manifests' test partitions (never a StageIndex)"
  - "Resident reader routes per key through the FIRST supplied manifest's membership; both split views read the same residency so the choice affects routing only"
  - "Control reader streams per key with a FIFO window bounded by --chunk-size; the corpus is never cached whole"
  - "Registered the sanctioned CONF-01 control reader in the Phase 39 sole-reader audit allow-list (Rule 3 blocking fix)"

patterns-established:
  - "Evidence payload: every float through JSON-safe sentinels, json.dumps(sort_keys=True), byte-identical re-render proven by test"
  - "Summary markdown leads with verdict + population size, symmetric hypothesis columns with controls beside, tolerance derivation stated separately from the no-physics-threshold sentence"

requirements-completed: [CONF-01]

coverage:
  - id: D1
    description: "Manifest-parametric population resolution with test_under_<label> attribution and empty-eligibility fail-closed"
    requirement: CONF-01
    verification:
      - kind: unit
        ref: "tests/phase46/test_frame_probe_evidence.py#ResolveProbePopulationTest"
        status: pass
    human_judgment: false
  - id: D2
    description: "Resident/control reader builders: model-facing surface routing, adapter-seam containment, eligibility filtering"
    requirement: CONF-01
    verification:
      - kind: unit
        ref: "tests/phase46/test_frame_probe_evidence.py#ReaderBuildersTest"
        status: pass
    human_judgment: false
  - id: D3
    description: "Deterministic D-05 evidence payload: completeness, redaction, containment, non-finite sentinels, non-overwriting run dirs"
    requirement: CONF-01
    verification:
      - kind: unit
        ref: "tests/phase46/test_frame_probe_evidence.py#EvidencePayloadTest"
        status: pass
    human_judgment: false
  - id: D4
    description: "CLI surface: exactly the five sanctioned flags, --help exit 0, operational-only exit semantics"
    requirement: CONF-01
    verification:
      - kind: unit
        ref: "tests/phase46/test_frame_probe_evidence.py#test_12_cli_help_names_exactly_the_sanctioned_flags"
        status: pass
      - kind: other
        ref: "python -m pinn.verification.target_frame_probe --help (exit 0)"
        status: pass
    human_judgment: false

duration: ~45min
completed: 2026-07-26
status: complete
---

# Phase 46 Plan 04: Frame-Probe Evidence Writer and Manifest-Parametric CLI Summary

**CONF-01 probe evidence layer: manifest-parametric population resolution with attributed test exclusions, deterministic D-05 raw.json+summary.md with host-path redaction and containment guards, and the single sanctioned `target_frame_probe` CLI — all dataset-free (D-24)**

## Performance

- **Duration:** ~45 min
- **Started:** 2026-07-27T04:30:00Z
- **Completed:** 2026-07-27T05:14:00Z
- **Tasks:** 2 (TDD: RED confirmed failing, then GREEN)
- **Files modified:** 2 created, 2 modified

## Accomplishments

- `resolve_probe_population` — the D-02 rule fixed and manifest-set-parametric:
  eligible = train-or-validation under EVERY supplied manifest; excluded =
  test under ANY, counted and attributed as `test_under_<label>`; the test
  partition is read as a physical-key set from the manifest payload, never
  materialized as a StageIndex (D-16); empty eligibility raises
  `FrameProbeUnavailable`.
- `render_evidence_payload` / `write_frame_probe_evidence` — the D-05 artifact:
  every D-05 field present, JSON-safe string sentinels for non-finite measures
  (never dropped/nulled), `json.dumps(sort_keys=True)` byte-identical re-render
  proven by test, simulation_data/corpus-root containment refusal,
  non-overwriting UTC run dirs, both files via `atomic_write_text`, and a
  fail-closed redaction guard (home prefix / resolved corpus root can never
  reach committed bytes).
- `main` — the single sanctioned entry point with operational-only exit
  semantics (0 = measured+written whatever the verdict; 2 = operational
  failure), exactly five flags, no split/precision/sample flag.
- CLI-side readers reuse the adapter module's own seams
  (`BRUTUS_FOLDER_TABLE`/`BRUTUS_SUBDIR` glob, `record_key_from_brutus`,
  `parse_brutus_file` with root containment, `preprocess_trajectory`) — no
  second path-mapping convention; StageIndex views built for train/validation
  only, with `StageIndex.from_split`'s population check failing closed on drift.

## Contract surfaces Plan 46-06 quotes verbatim

**Final CLI synopsis line:**

```
usage: python -m pinn.verification.target_frame_probe [-h] --manifest PATH [--evidence-root EVIDENCE_ROOT] [--data-root DATA_ROOT] [--blacklist-path BLACKLIST_PATH] [--chunk-size CHUNK_SIZE]
```

**Evidence payload top-level key list (sorted):**

```
D_characteristic_length, T_characteristic_time, aggregates, arms,
blacklist_sha256, confound_register, data_root_source, device, dtype,
exclusion_counts, manifests, math, population, probe_invocation, rationale,
repo_commit, schema_version, tolerance_derivation, torch_version,
trajectories, verdict
```

**Exact population rule sentence (module constant `POPULATION_RULE`, embedded
in the payload at `population.rule`):**

> A Stage-0 record is eligible iff its RecordKey appears in the train-or-validation view of EVERY supplied manifest; a record whose physical key is in ANY supplied manifest's test partition is excluded, with the exclusion counted and attributed as test_under_<label>.

## Task Commits

Both tasks landed in one plan-prescribed commit (TDD performed locally: RED
suite failed on missing symbols, then GREEN):

1. **Tasks 1-2: population resolution + evidence writer + CLI** - see hash below (feat)

## Files Created/Modified

- `pinn/verification/target_frame_probe.py` — added `ProbePopulation`,
  `ManifestIdentity`, `EvidenceProvenance`, `FrameProbeRun`,
  `POPULATION_RULE`, `TOLERANCE_DERIVATION`, `resolve_probe_population`,
  `_build_resident_reader`, `_build_control_reader`, `render_evidence_payload`,
  `render_summary_markdown`, `write_frame_probe_evidence`, `main` (+`__main__`
  runner); updated module docstring and `__all__`. No 46-02 symbol changed.
- `tests/phase46/test_frame_probe_evidence.py` — 12 dataset-free tests covering
  all four Task-1 behaviors and all five Task-2 behaviors plus the CLI surface.
- `tests/phase39/test_prohibitions.py` — one-hunk allow-list registration
  (deviation 1 below).
- `.planning/phases/46-frame-resolution-gate-aligned-validation/deferred-items.md`
  — new; logs the pre-existing phase43 sweep failures (DI-46-04-01).

## Decisions Made

- Exclusion ledger keyed on `PhysicalKey` from manifest payloads (behavior 2:
  the excluded set is exactly the supplied manifests' test keys, including keys
  in no train/validation view).
- Resident-reader routing uses the first supplied manifest's membership;
  recorded via `ProbePopulation.first_manifest_label` (plan-prescribed).
- Control reader holds at most `--chunk-size` parsed controls (FIFO eviction) —
  the plan's agent-discretion memory-hygiene choice; the corpus is never cached
  whole.
- Manifest labels derive from path stems with deterministic `~2` collision
  suffixes; labels are what `test_under_<label>` attributes to.
- Aggregate payload distributions labeled `role: descriptive_diagnostic`
  (D-06/D-14 discipline).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Registered the sanctioned control reader in the Phase 39 sole-reader audit**
- **Found during:** phase-wide verification sweep (Task 2 verify).
- **Issue:** `tests/phase39/test_prohibitions.py::SoleReaderAuditTests::test_only_allowed_modules_parse_the_corpus`
  failed — GAP-39-02's `ALLOWED_CORPUS_READERS` registers every module permitted
  to parse the corpus, and the plan-mandated control reader
  (`parse_brutus_file` + corpus `*.txt` glob) is a new sanctioned reader the
  registry did not yet know. Both contracts are explicit: the plan requires the
  adapter-seam parse (Task 1 action, acceptance criterion 5), and the audit
  requires registration; exactly one coherent resolution exists.
- **Fix:** added `pinn/verification/target_frame_probe.py` to
  `ALLOWED_CORPUS_READERS` with a comment citing D-01/D-03 and plan 46-04
  (provenance/positive-control arms only, never a second training-data path).
- **Files modified:** `tests/phase39/test_prohibitions.py` (one hunk; outside
  the plan's `files_modified`, necessarily so — the audit gate lives there).
- **Verification:** `pytest tests/phase39 -q` → 264 passed, 43 subtests passed.
- **Committed in:** the Task 1-2 feat commit.

---

**Total deviations:** 1 auto-fixed (Rule 3 - blocking)
**Impact on plan:** Required for the plan's own verification block
(`tests/phase37`-`phase43` sweep) to hold; no scope creep, no behavior change
beyond registration.

## Issues Encountered

- **Pre-existing `tests/phase43` failures (12)** — two environmental classes
  (worktree-missing ACC-02 calibration artifact, already documented by 46-01;
  stale `.planning/phases/43-*` paths after the v2.0 milestone archival to
  `.planning/milestones/v2.0-phases/43-*`). Zero coupling with this plan (no
  phase43 module imports the probe; the failure set is identical before/after
  the diff). Logged as DI-46-04-01 in `deferred-items.md`; NOT fixed (scope
  boundary).
- The full `pytest tests/ -q` sweep exceeds an 8-minute shell timeout; suites
  were run per-phase instead (phase37–43 + phase46 all verified individually,
  phase43 modulo the pre-existing failures above).

## Verification

- `pytest tests/phase46/test_frame_probe_evidence.py -x -q -rs` → **12 passed,
  0 skipped** (≥9 required; zero-skip guard passed).
- `pytest tests/phase46/ -q` → **64 passed** (fixtures + probe core + gate
  composition + evidence).
- `python -m pinn.verification.target_frame_probe --help` → exit 0; usage names
  exactly `--manifest`, `--evidence-root`, `--data-root`, `--blacklist-path`,
  `--chunk-size`; no flag containing `split`, `precision`, or `sample`.
- Sibling sweeps: phase37 (55 passed), phase38 (128 passed + 88 subtests),
  phase39 (264 passed + 43 subtests), phase40 (163 passed + 106 subtests),
  phase41 (193 passed), phase42 (35 passed + 3 skipped — pre-existing skips,
  not this suite), phase43 (186 passed + the 12 pre-existing failures above).
- Acceptance greps: `physical_keys` manifest-payload read present;
  `from_split(.*["']test["']` count **0**; `resolve_within_root|parse_brutus_file`
  present; `atomic_write_text` used for both artifacts.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Plan 46-05 (isolation/artifact tests) can assert the CLI's held-out fences
  against the landed module: no withheld-split StageIndex, no `pinn.evaluate`
  import, no held-out receipt.
- Plan 46-06 owns the single real-corpus invocation; its three quoted contract
  surfaces are recorded above. The population-instantiation decision (which
  retained manifests to pass, per GAP-46-02's seed-41/42/43 intersection
  ruling) is a recorded 46-06 input — the machinery is manifest-count-invariant.

## Self-Check: PASSED

- `pinn/verification/target_frame_probe.py` — FOUND (modified)
- `tests/phase46/test_frame_probe_evidence.py` — FOUND (created)
- `tests/phase39/test_prohibitions.py` — FOUND (modified, deviation 1)
- `.planning/phases/46-frame-resolution-gate-aligned-validation/deferred-items.md` — FOUND (created)
- `.planning/phases/46-frame-resolution-gate-aligned-validation/46-04-SUMMARY.md` — FOUND (this file)
- Commit hash recorded below after commit (self-check completed post-commit; see Task Commits).

---
*Phase: 46-frame-resolution-gate-aligned-validation*
*Completed: 2026-07-26*
