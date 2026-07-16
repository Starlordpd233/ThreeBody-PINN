---
phase: 39-data-ingestion-stage-0-population-scan
plan: "07"
subsystem: data
tags: [phase-close, real-corpus-scan, evidence, reader-audit, train-ready]

# Dependency graph
requires:
  - phase: 39-04
    provides: "Canonical split writer and retained splits.json manifest"
  - phase: 39-05
    provides: "Locked build_stage_batch / select_stage_records signature"
  - phase: 39-06
    provides: "Deterministic persisted-label population report + scan CLI"
provides:
  - "Phase-close dataset-free + full-repository regression evidence"
  - "Read-only 6.3 GB real-corpus Thrust-A scan evidence retained byte-for-byte"
  - "Exact-reader / sole-classifier / source-integrity / readiness audit"
  - "Honest Stage-0 readiness outcome: stage0_full_split_count=2265 (>=240) -> train-ready"
affects: [40-training-loop]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Real-corpus evidence is a final-only read-only gate, never part of normal feedback"
    - "Retained evidence logs are byte-identical copies; scan.log echoes $GSD_DATA_ROOT/$HOME placeholders only"
    - "DATA-06 readiness binds exclusively to stage0_full_split_count; the train count is diagnostic Phase-40 seam evidence"

key-files:
  created:
    - .planning/phases/39-data-ingestion-stage-0-population-scan/evidence/stage-scan/phase-close/dataset-free.log
    - .planning/phases/39-data-ingestion-stage-0-population-scan/evidence/stage-scan/phase-close/scan.log
    - .planning/phases/39-data-ingestion-stage-0-population-scan/evidence/stage-scan/phase-close/stage_population.json
    - .planning/phases/39-data-ingestion-stage-0-population-scan/evidence/stage-scan/phase-close/splits.json
    - .planning/phases/39-data-ingestion-stage-0-population-scan/evidence/stage-scan/phase-close/verification.log
  modified:
    - tests/phase39/test_adapter.py
    - .gitignore

key-decisions:
  - "Treat the Phase-39 end-to-end wiring test's stale call sites as a blocking regression and realign them to the locked 39-05/39-06 signatures so the full repository suite is green at phase close."
  - "Run the real-corpus scan as a single read-only Thrust-A pass against the master-root 6.3 GB corpus (GSD_ALLOW_PARTIAL_DATA_ROOT unset), retaining byte-identical stage_population.json + splits.json."
  - "Bind phase-close readiness solely to stage0_full_split_count (DATA-06); stage0_train_split_count is retained diagnostic Phase-40 seam evidence and never a second gate."

requirements-completed: [DATA-01, DATA-02, DATA-03, DATA-04, DATA-05, DATA-06]

coverage:
  - id: P1
    description: "Dataset-free Phase 39 suite and full repository unittest discovery both exit zero with structured command_result markers"
    requirement: DATA-01..06
    verification:
      - kind: integration
        ref: "evidence/stage-scan/phase-close/dataset-free.log (phase39_suite=PASS, repository_suite=PASS)"
        status: pass
    human_judgment: false
  - id: P2
    description: "Read-only real-corpus Thrust-A scan with train-ready exit code, zero numeric gold labels, memory fraction within watermark, and byte-identical retained evidence"
    requirement: DATA-06
    verification:
      - kind: e2e
        ref: "evidence/stage-scan/phase-close/scan.log + stage_population.json + splits.json"
        status: pass
    human_judgment: false
  - id: P3
    description: "Exact-reader, sole-classifier, source-integrity, and readiness audit; full-admitted replay/lookahead selection over base Set 1a only; framework specs and corpus byte-unchanged"
    requirement: DATA-01..06
    verification:
      - kind: integration
        ref: "evidence/stage-scan/phase-close/verification.log"
        status: pass
    human_judgment: false

# Metrics
duration: 42min
completed: 2026-07-15
status: complete
---

# Phase 39 Plan 07: Phase-Close Real-Corpus Scan and Audit Summary

**Phase 39 closes train-ready: the read-only 6.3 GB Thrust-A scan reports `stage0_full_split_count=2265` (>= 240) with `gold_numeric_stage_count=0`, retained byte-identical evidence, and an exact-reader/source audit — after a green dataset-free + full-repository regression.**

## Performance

- **Duration:** ~42 min active (two 6.3 GB read-only passes for scan + audit)
- **Completed:** 2026-07-15
- **Tasks:** 3
- **Files produced:** 5 evidence artifacts (+ 1 test realignment + 1 gitignore exception)

## Real-Corpus Scan Outcome (DATA-06)

| Metric | Value |
|---|---|
| `scan_exit_code` | 0 (allowlisted; train-ready) |
| `stage0_full_split_count` | **2265** (>= 240 fatal threshold -> train-ready) |
| `stage0_train_split_count` | 1812 (diagnostic Phase-40 seam; also >= 240 here) |
| `gold_numeric_stage_count` | 0 |
| Stage 0 / Stage 1 / UNASSIGNED | 2265 / 2592 / 10171 |
| `mem:` fraction | 0.024292 (<= 0.7 watermark); resident_tensor_bytes=625989388; mem_ballpark=624246140 |
| `allow_partial_data_root` | 0 |
| `evidence_byte_identity` | true |
| `phase39_status` | **train-ready** |
| Blacklist | 65 entries (2 hierarchical + 63 standard); all 65 absent from Brutus output (pre-simulation prescreening exclusions) |

## Accomplishments

- Ran the dataset-free Phase 39 suite (discovery + all 16 validation slices 39-01-01..39-06-02) and the full repository unittest discovery (402 tests) — both green, captured with structured `command_result=<label>:exit=0` markers in `dataset-free.log`.
- Executed a single read-only Thrust-A pass over the 6.3 GB master-root corpus via the sole `AdmittedSetAdapter` + scan CLI path (`GSD_ALLOW_PARTIAL_DATA_ROOT` unset; `num_workers=0`; fail-closed), retaining byte-identical `stage_population.json` and `splits.json` plus a privacy-sanitized `scan.log` (freshness markers, redacted `$GSD_DATA_ROOT`/`$HOME` echo, no `/Users/` leakage).
- Performed the phase-close audit: full-admitted Stage-0 replay=240 and Stage-1 lookahead=16 over a full-admitted `StageIndex` (zero gold/non-Set-1a keys); `stage0_train_split_count=1812` re-derived from retained `splits.json` via `StageIndex.from_split(..., "train")` (Phase-40 DATA-04->DATA-05 seam); independent sample parse recomputes raw/normalized IC13 to match the adapter record; resident bytes reconcile; spec hashes + corpus fingerprint recorded.
- Confirmed framework specs and `simulation_data` are byte-unchanged; only Phase-39 test/evidence/summary files were modified.

## Task Commits

Each task was committed atomically via `scripts/agent-commit` (with `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`), after its exact `<verify>` gate passed:

1. **39-07-01** `7279e943` (test) — realign end-to-end wiring test + dataset-free regression evidence.
2. **39-07-02** `acf9b207` (evidence) — read-only real-corpus Thrust-A scan evidence.
3. **39-07-03** `fdc83fa3` (evidence) — phase-close reader/readiness audit.

## Verification (exact `<verify>` gates)

- **39-07-01:** exit 0 — `phase39_suite=PASS`, `repository_suite=PASS`, all `command_result=...:exit=0`, no skipped Phase39 production symbol.
- **39-07-02:** exit 0 — freshness markers, allowlisted `scan_exit_code=0`, `evidence_byte_identity=true`, mem fraction <= 0.7, no `/Users/` in any retained artifact, JSON invariants satisfied.
- **39-07-03:** exit 0 — `phase39_stage0_fatal=false`, `phase39_train_ready=true`, `phase39_status=train-ready`; prohibition/stages + phase38 preflight pass; `git diff --check` clean; specs and `simulation_data` unchanged.

## Decisions Made

- **Honor the locked signatures at phase close.** The Phase-39 end-to-end wiring test had stale call sites from earlier waves; the closeout gate requires a green repository suite, so the test was realigned to the 39-05/39-06 contracts rather than weakening the gate.
- **One real pass, retained bytes.** The scan is a single read-only Thrust-A pass; scratch `/tmp` is never sole proof — retained copies under the fixed repository evidence path carry their SHA-256 and byte identity.
- **Readiness is one operand.** `phase39_stage0_fatal == (stage0_full_split_count < 240)`; the train-split count is diagnostic Phase-40 evidence and cannot flip readiness.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Realigned stale end-to-end wiring test to locked signatures**
- **Found during:** Task 39-07-01 full-repository regression.
- **Issue:** `EndToEndIntegrationTests.test_full_chain_wires_without_breaking_module_boundaries` called `build_stage_batch(adapter, stage=0)` (missing required `rng`/`dtype`/`device`) and `build_population_report(adapter, interim_s0=0.01)` (unsupported kwarg; report is a dict), so the full suite exited nonzero. The calls went stale when Plans 39-05/39-06 locked the signatures; the test only stayed green on TinyCorpus because all-UNASSIGNED records short-circuit before the mismatched accessor.
- **Fix:** Supplied `rng`/`dtype`/`device` to `build_stage_batch` and read `gold_numeric_stage_count` from the dict-form report (return path and attached-fatal path).
- **Files modified:** `tests/phase39/test_adapter.py`
- **Commit:** `7279e943`

**2. [Rule 3 - Blocking] Narrow `.gitignore` exception for phase-close evidence logs**
- **Found during:** Task 39-07-01 commit staging.
- **Issue:** The repo carries a universal `*.log` gitignore (line 263) and the established evidence convention is `.json`/`.md` (zero tracked `.log` files repo-wide), yet Plan 39-07 declares `.log` evidence as retained deliverables. Force-add is forbidden by policy.
- **Fix:** Added a narrow negation `!.planning/phases/39-data-ingestion-stage-0-population-scan/evidence/stage-scan/phase-close/*.log` (mirroring the existing `!**/logging_config.py` precedent) so normal `git add` retains the declared evidence; the generic `*.log` rule still applies everywhere else.
- **Files modified:** `.gitignore`
- **Commit:** `7279e943`

**3. [Rule 3 - Blocking] Resolved real blacklist location for the scan command**
- **Found during:** Task 39-07-02 setup.
- **Issue:** The scan CLI defaults to `data_root/problematic_ics_blacklist.json`, but the real corpus's blacklist lives at `simulation_data/Documentation/problematic_ics_blacklist.json`. The VALIDATION row omits `--blacklist-path`, so the command as written would fail with `BlacklistSchemaError`.
- **Fix:** Passed `--blacklist-path` resolved as `$GSD_DATA_ROOT/../Documentation/problematic_ics_blacklist.json`; the retained `scan.log` echoes the placeholder form so no personal path leaks.
- **Files modified:** none (scan invocation only)
- **Commit:** `acf9b207`

**4. [Rule 3 - Blocking] Used a full-admitted StageIndex for the audit's replay/lookahead selection**
- **Found during:** Task 39-07-03 audit.
- **Issue:** `select_stage_records` passes an `int` stage and is contracted against the `StageIndex`/StageQuery seam (whose `records_at_or_below` accepts an int via `_numeric_stage`). `AdmittedSetAdapter.records_at_or_below(stage)` instead does `stage.value` and only tolerates an int when every record is UNASSIGNED (short-circuit), so it `AttributeError`s on the real corpus. Production never hits this because `build_stage_batch` receives a `StageIndex` via `from_split`, never the raw adapter.
- **Fix:** Built a full-admitted `StageIndex` via the existing internal `_with_blacklist` constructor (blacklist + source wired) and ran `select_stage_records` over it, preserving the plan's "full admitted set" intent without touching production code.
- **Files modified:** none (audit driver only)
- **Commit:** `fdc83fa3`

---

**Total deviations:** 4 auto-fixed blocking issues. **Impact:** the phase-close gates pass as written without weakening any acceptance criterion; production behavior, framework specs, the corpus, and global defaults are unchanged.

## Issues Encountered

- **Deferred (out of scope):** `AdmittedSetAdapter.records_at_or_below(stage)` and `records_at(stage)` assume `stage` is a `StageLabel` (they dereference `.value` / compare enum equality), while `select_stage_records` and the DATA-05 contract pass an `int`. This is latent because production routes through `StageIndex` (which accepts both). It is logged here for a future plan to reconcile the adapter accessors with the int-stage contract; it is not exercised by any Phase-39 test or the production `build_stage_batch` path and does not affect this phase's train-ready outcome.

## Known Stubs

None. No TODO/FIXME, placeholder, threshold ratification, or deferred implementation remains in the files touched by this plan. The interim `s0 = 0.01` floor is intentionally retained (owner-ratification pending, FUT-02), not a stub.

## User Setup Required

None. The phase-close gates are automated; the real-corpus scan ran read-only against the existing master-root corpus.

## Next Phase Readiness

- Phase 40 can consume the retained `splits.json` manifest and the diagnostic `stage0_train_split_count=1812` via `StageIndex.from_split(adapter, manifest, "train")` without changing DATA-06's admitted/full readiness invariant (`stage0_full_split_count=2265 >= 240`).
- The Thrust-A scan confirms Stage 0 is populated enough to train (2265 >= 240); the interim `s0 = 0.01` floor remains pending owner ratification (FUT-02), recorded as input evidence only.
- The deferred `data_version_hash` producer (GAP-39-01) and the adapter int-stage accessor reconciliation are the only carried-forward items; neither blocks Phase 40.

## Self-Check: PASSED

- All five evidence artifacts exist under the fixed repository path; `dataset-free.log`, `scan.log`, `stage_population.json`, `splits.json`, and `verification.log` are present and non-empty.
- Task commits `7279e943`, `acf9b207`, `fdc83fa3` exist on `milestone/v2.0`.
- Each task's exact `<verify>` gate exited 0.
- Framework specs and `simulation_data` are byte-unchanged (`git diff --exit-code` / `git status --short -- simulation_data` clean).
- `requirements: [DATA-01..06]` were already marked Complete by Plans 39-01..06; this plan re-confirms them on the real corpus.

---
*Phase: 39-data-ingestion-stage-0-population-scan*
*Completed: 2026-07-15*
