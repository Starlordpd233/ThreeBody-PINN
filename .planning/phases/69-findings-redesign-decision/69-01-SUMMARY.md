---
phase: 69-findings-redesign-decision
plan: "01"
subsystem: verification
tags: [evidence, provenance, accounting, traceability, unittest]
status: complete
requires:
  - phase: 60-single-system-learnability
    provides: frozen historical failed-fit records
  - phase: 65-probe-on-the-record-fit-harness
    provides: recorded probe reproduction and smoke
  - phase: 66-small-network-control
    provides: three successful smaller-network controls and owner ruling
  - phase: 67-design-settings-ladders
    provides: keyed ladder reviews, attempts and successful locked controls
  - phase: 68-yardstick
    provides: known-answer audit and owner C-7 ruling
provides:
  - read-only sources, cost, traceability and all commands
  - pinned experiment, recipe, disposition and unique-activity inventory
  - 31 focused source, identity, accounting and mapping tests
affects: [69-02, 69-03, v2.6-handoff]
tech-stack:
  added: []
  patterns: [committed-byte source reads, keyed case joins, Decimal timing, live mapping rereads]
key-files:
  created:
    - .planning/phases/69-findings-redesign-decision/evidence/verify_phase69.py
    - .planning/phases/69-findings-redesign-decision/evidence/69-evidence.json
    - tests/phase69/__init__.py
    - tests/phase69/test_verifier_phase69.py
  modified: []
key-decisions:
  - "Original publication registrations establish historical capture; later re-pins remain separate."
  - "Include the committed yardstick capture timing separately from the 129-attempt subtotal."
  - "Mapping checks derive active IDs and phases anew and do not establish requirement satisfaction."
requirements-completed: []
requirements-supported: [VERD-01, VER-23]
actuals:
  tasks: 3
  commits: 1
artifact-token-estimate: 248190
artifact-token-estimate-basis: "ceil(chars/4) over four new implementation-file diffs; a size proxy, not measured model token usage"
commit-status: enclosing-atomic-plan-commit
duration: 18min
completed: 2026-11-08
---

# Phase 69 Plan 01: Checked evidence and active mapping summary

Committed-source verification now connects both historical failures to the corresponding successful locked-network controls, preserves all experiment readings and rederives measured costs without counting contrast references as attempts.

## Execution and ownership

All three implementation tasks are complete. The parent explicitly owns staging, commits, STATE, ROADMAP, REQUIREMENTS and VALIDATION in this shared worktree. No commits or shared-state writes were performed by this executor. The parent reviewed the implementation and reran the focused suite and combined verifier before including this summary in one atomic plan commit. The repository's task-end policy supersedes generic per-task and RED/GREEN commits. Resolve that enclosing commit with `git log -1 --format=%H -- .planning/phases/69-findings-redesign-decision/69-01-SUMMARY.md`; the file cannot contain its own literal commit hash.

The source baseline is `0f91709000a442507e0eb2b9616f474a81525333`. Independent, disjoint documentation commits `f02715c7` and `fc173a4f` advanced shared HEAD during execution. They were inspected read-only and preserved. Existing Phase 68, configuration and state changes were preserved. The first written test artifact was created at `2026-11-09T02:46:40.824311+00:00`; the duration above measures the approximate implementation interval from that artifact, excluding preceding context reads.

## Task results

| Task | Result | Commit |
|---|---|---|
| 1. Real 1632/42 tracer | Exact old Adam, polish and official E/tier connect to the original registration and settled control; corrupt sources, case/seed and current-registration substitution reject. | Enclosing atomic 69-01 commit |
| 2. Complete inventory and costs | DIAG-09, EXP-01 through EXP-05 and YARD-01/02/03, both matched systems, additional seed, recipe aspects, dispositions and unique activities are recorded. | Enclosing atomic 69-01 commit |
| 3. Dynamic mapping and rejection tests | Live active definitions, table mappings and roadmap detail mappings agree; empty, missing, duplicate, extra, conflicting and nonexistent-phase fixtures reject. | Enclosing atomic 69-01 commit |

`69-evidence.json` contains `sources.experiments`, `sources.matched_comparisons`, `sources.additional_control`, `sources.recipe`, `sources.dispositions`, `sources.resource_rulings` and `cost`. Source rows identify path, full committed revision and SHA-256. Scientific interpretation and owner choices remain downstream work.

## Recorded provenance and results

Historical execution uses `a686d26e00f7c1e8ba54bb2d3e1cd730a3404a69`. The three original control-publication anchors are:

| Case | Publication revision | Control E | Recorded endpoint |
|---|---|---:|---|
| 1632/42 | `df40671e2e07a95b65efc102cabc59e22ca8dc59` | 0.040691019043637484 | Tier 1, settled |
| 851/42 | `23df087ccb13dfb3123809024dcd554e24c5b954` | 0.09549573839491703 | Tier 1, settled |
| 1632/41 | `623f8df6641eebdbbfdda811e4f13c3002b1c14f` | 0.03491785615016659 | Tier 1, settled |

Historical 1632/42 Adam E is `1.1606404574102112`; polish/official E is `1.157387378319295`, Tier 0. Historical 851/42 Adam/official E is `1.2375295559620059`; polish E is `1.2383540710834968`, Tier 0. Original registration digests pass at publication; later re-pinned registration bytes are explicitly different and cannot replace them.

Keyed reviews preserve the correct EXP-03 repeat effects: `39.16428044173176` belongs to 1632/41 and `15.376889578229147` to 851/42. The inventory records the historical narrative's swapped columns without editing that page. EXP-02/04/05 confirmation arrays remain empty; EXP-03 retains confirmed-worsening, unsettled and ambiguous labels and its original improvement hypothesis.

The recipe table retains the matching 33-module map, statistics digest and actual training/scoring window hashes. It distinguishes same-seed construction from unproved archived tensor identity and leaves historical runtime/kernel/determinism equivalence unresolved. Schedule, clipping, executed diagnostic polish, update budget and selected scored state remain visible differences. This comparison establishes no isolated historical cause, physics accuracy or new-IC generalization.

## Measured accounting

| Activity | Published attempts | Recorded UTC seconds | Separate fit-wall seconds |
|---|---:|---:|---:|
| Phase 65 smoke | 1 | 3 | 2.7193587080000725 |
| Phase 66 science | 3 | 5725 | 5723.8721086669830 |
| Phase 66 timing | 1 | 25 | 24.33177595899906 |
| Phase 67 science | 60 | 100882 | 100860.19654708064667 |
| Phase 67 timing | 60 | 987 | 970.9867257890291525 |
| Phase 67 metadata | 4 | 4 | Not recorded |
| Attempt subtotal | 129 | 107626 | 125 records, 107582.1065162036579550 |

UTC attempt timestamps have one-second resolution. A zero interval is below that resolution. Fit-wall, optimizer/logging/scoring segments and attempt UTC intervals are not additive views. The probe's incomplete claim is linked once to its published outcome, with duration unknown. Pre-claim refusals and unrecorded development/operator work retain unknown costs. Historical v2.4 cost is excluded from v2.5 totals.

## Deviations from Plan

### Recorded yardstick timing, approved by the parent

The saved research and plan incorrectly stated that the yardstick JSON had no duration. The committed source at baseline, `.planning/phases/68-yardstick/evidence/yardstick-audit.json:187,195-196`, records `provenance.elapsed_seconds = 0.5945865410612896`, `utc_started = 2026-11-08T20:00:43.300573+00:00` and `utc_finished = 2026-11-08T20:00:43.895279+00:00`. Their UTC interval is exactly `0.594706` seconds.

This conflict was surfaced before final accounting. The parent independently verified it and directed inclusion under D-09. The original attempt subtotal remains unchanged. One additional named yardstick activity gives 130 timed activities and a combined named UTC subtotal of `107626.594706` seconds. Its elapsed and UTC values describe the same capture and are never summed together. Neither value covers all operator, development or test work. The parent owns correction of the research/plan prose.

## TDD evidence

The plan is `type: execute`; phase-wide TDD mode was not enabled. Task behavior-first tests were still used. No RED/GREEN commits were made under the explicit repository/parent atomic-commit adaptation.

| Task | Intentional RED | GREEN |
|---|---|---|
| 1 | `test_real_cli_connects_historical_failure_and_original_control` failed its return-code assertion, `1 != 0`, after a valid CLI reported `sources is not implemented`. The earlier missing-file bootstrap failure was not used as the behavioral RED evidence. | Six tracer tests passed before expansion; final suite includes seven tracer tests. |
| 2 | Complete-inventory assertion failed `0 != 9`; cost CLI assertion failed `1 != 0` with the unimplemented command. | Twelve identity/cost tests passed; final suite includes thirteen. |
| 3 | Real traceability CLI return-code assertion failed `1 != 0` with the unimplemented command. | Eleven traceability tests passed. |

Focused corruption tests cover altered SHA-256, missing committed objects, historical registration substitution, path escape, changed case/seed/role, swapped repeat scores, duplicate identities, repeat control references, conflicting attempts, missing/negative/nonfinite durations, unknown partial attempts, separate timing views, Boolean substitution for a numeric tier, changed cost totals, and mapping anomalies. No scientific or owner-authority judgment is replaced by these tests.

## Validation

Every Python command below used `<home>/miniforge3/envs/pinn-train/bin/python -B` from the trainex root. Checker abbreviates `.planning/phases/69-findings-redesign-decision/evidence/verify_phase69.py`.

| Exact command arguments | Observed result |
|---|---|
| `-m unittest tests.phase69.test_verifier_phase69.SourceTracerTests` | Six tests passed in 0.190 s before expansion. |
| `Checker sources` | Exit 0, `PHASE69-SOURCES-OK`; repeated through final `all`. |
| `-m unittest tests.phase69.test_verifier_phase69.IdentityAndCostTests` | Twelve tests passed in 7.679 s before the final extra corruption test. |
| `Checker cost` | Exit 0, `PHASE69-COST-OK`; exact accounting reproduced. |
| `-m unittest tests.phase69.test_verifier_phase69.TraceabilityTests` | Eleven tests passed in 0.059 s. |
| `-m unittest discover -s tests/phase69 -t .` | Final run: 31 tests passed in 18.404 s, zero skips. |
| Parent rerun of `-m unittest discover -s tests/phase69 -t .` | 31 tests passed in 16.206 s. |
| `Checker all` | Exit 0; sources, cost, traceability and `PHASE69-ALL-OK` markers all present. |
| Parent rerun of `Checker all` | Exit 0; all four success markers present, including current 13/13/13 mapping with no anomalies. |
| `-m pinn.verification.diagnostic_phase67 audit-phase --json` | Exit 0, status `PHASE67-AUDIT-OK`, `problems: []`. |
| `-m pinn.verification.diagnostic_phase67 check-review --experiment exp03` | Exit 0, `PHASE67-REVIEW-OK`. |
| `-m unittest tests.phase67.test_historical.CurrentLockedRawParityTests` | Two tests passed in 0.023 s. |
| `git diff --check` | Exit 2 for the pre-existing `tests/phase68/__init__.py:2` blank line only. Outside ownership; unchanged. |
| `git diff --no-index --check /dev/null <file>` for each of the four owned implementation additions | No whitespace diagnostics. Exit 1 identifies each new-file difference. |
| `git diff --name-only -- .planning/phases/60-single-system-learnability .planning/phases/65-probe-on-the-record-fit-harness .planning/phases/66-small-network-control .planning/phases/67-design-settings-ladders pinn` | Empty; historical evidence and shared implementation unchanged. |

The final live check read 13 definitions, 13 traceability rows and 13 roadmap mappings across Phases 65-69, with no orphan, extra, duplicate, conflict or missing phase. It recorded requirements SHA-256 `4b6ae627be4bbed3bc70700cbb2e3415d774f10d858bfd5df56d2974f13b950a` and roadmap SHA-256 `67d6a5ef64c5800dab6890b3048dd2466aac486cc797074333a078520d716ebb`. The check must run again after approved changes and at final close. Thirteen is an observed count, not a checker constant.

## Known stubs and remaining limits

None. Source-unresolved initialization/runtime equivalence, unknown activity costs, unconfirmed contrasts and open owner choices are intentional evidence limitations, not substituted results. No training, scoring rerun, raw-corpus access, evaluation spend, dependency install, physics repair, framework edit or trainex-r5 assembly occurred.

The one-page findings, scientific judgment review, actual owner closing reply and final VER-23 closing capture remain for Plans 69-02 and 69-03. `requirements-completed` is therefore empty; this implementation supports VERD-01 and VER-23 without declaring either closing obligation discharged.

## Self-check: PASSED

All four implementation files exist, their focused tests and combined command pass, and the historical/shared implementation diff is empty. All three tasks share the enclosing atomic plan commit, resolvable through the Git command above. No fabricated literal hash is recorded. The owner closing decision and final phase verification remain pending.
