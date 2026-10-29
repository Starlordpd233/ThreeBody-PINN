---
phase: "65"
slug: "probe-on-the-record-fit-harness"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-10-28"
---

# Phase 65 validation strategy

This is the execution validation contract for six plans and 15 tasks in execution
waves 1-6. No planned test or real acceptance run has been executed during planning.
Wave 0 below names test preparation inside Plan 65-01, whose execution wave is 1.

## Test infrastructure

| Property | Value |
|----------|-------|
| Framework | Python standard-library unittest in the existing pinn-train environment |
| Interpreter | <home>/miniforge3/envs/pinn-train/bin/python |
| Config | Existing repository unittest conventions; no framework installation |
| Quick run | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase65.test_probe tests.phase65.test_contracts tests.phase65.test_isolation -v` |
| Full synthetic suite | `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest discover -s tests/phase65 -p 'test_*.py' -v` |
| Runtime | Unmeasured. Keep quick synthetic feedback within 60 seconds; measure during execution. |

## Sampling rate

- After each task, run the closest unit module. After each plan wave, run the
  complete Phase 65 synthetic suite.
- Keep real-data acceptance separate from routine unit tests. The seven-arm
  reproduction and the system-1632 smoke each require their own committed
  prediction/registration page before their first run.
- Before phase verification, require the complete synthetic suite and the
  committed real acceptance evidence. A synthetic test pass is not evidence
  that the historical probe reproduced or that the network learned an orbit.

## Per-task verification map

All commands use `<home>/miniforge3/envs/pinn-train/bin/python -B`.
The module/subcommand arguments below follow that exact interpreter. New test
modules are created by 65-01 before later plans use them. Every task's PLAN
includes the complete command and an immediately following `fails_when` clause.

| Task | Wave | Requirement | Command arguments | Test type | Status |
|------|------|-------------|-------------------|-----------|--------|
| 65-01-01 | 1 | INST-08(b,e), DIAG-09 | `-m unittest tests.phase65.test_fit_short -v` | synthetic end-to-end tracer | Pending creation/run |
| 65-01-02 | 1 | INST-08(a,b) | `-m unittest tests.phase65.test_contracts -v` | parity, frozen scoring/digests | Pending creation/run |
| 65-01-03 | 1 | DIAG-09, INST-08(d) | `-m unittest tests.phase65.test_probe tests.phase65.test_isolation -v` | measurement/identity edges | Pending creation/run |
| 65-02-01 | 2 | DIAG-09, INST-08(d) | `-m unittest tests.phase65.test_isolation -v` | target/ancillary pre-open spies | Pending |
| 65-02-02 | 2 | INST-08(a,d) | `-m unittest tests.phase65.test_contracts tests.phase65.test_isolation -v` | recorded stats/window endpoints | Pending |
| 65-03-01 | 3 | INST-08(d) | `-m unittest tests.phase65.test_isolation -v` | actual relocated evaluate_run | Pending |
| 65-03-02 | 3 | INST-08(d) | `-m unittest tests.phase65.test_isolation tests.phase65.test_contracts -v` | train.main/resume and ordinary controls | Pending |
| 65-04-01 | 4 | DIAG-09 | `-m unittest tests.phase65.test_probe.HistoricalSourceTests -v` | source hash/stdout preservation | Pending class creation |
| 65-04-02 | 4 | DIAG-09, INST-08(c) | `-m unittest tests.phase65.test_probe -v` | formatter boundaries and commit gate | Pending |
| 65-04-03 | 4 | DIAG-09 | `-m pinn.verification.diagnostic_probe check-registration --registration .planning/phases/65-probe-on-the-record-fit-harness/evidence/probe/expectations.json` | live metadata-only admission | Pending CLI/commit |
| 65-05-01 | 5 | DIAG-09 | `-m pinn.verification.diagnostic_probe run --registration .planning/phases/65-probe-on-the-record-fit-harness/evidence/probe/expectations.json --output .planning/phases/65-probe-on-the-record-fit-harness/evidence/probe/reproduction.json` | registered read-only real acceptance | Pending registration |
| 65-05-02 | 5 | DIAG-09, INST-08(c) | `diagnostic_probe logger-parity` then `diagnostic_probe verify-result`, complete `-m` commands and flags in 65-05 Task 2 | registered logger parity/result check | Pending registration |
| 65-06-01 | 6 | INST-08(a,b,d,e) | `-m unittest tests.phase65.test_fit_short tests.phase65.test_isolation tests.phase65.test_contracts -v` then `diagnostic_fit check-registration`, complete command in 65-06 Task 1 | synthetic timing/commit guard | Pending CLI/commit |
| 65-06-02 | 6 | INST-08(e) | `-m pinn.verification.diagnostic_fit run --registration .planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/smoke-registration.json --output .planning/phases/65-probe-on-the-record-fit-harness/evidence/fit/1632-smoke/record.json` | registered 20-step real smoke | Pending registration |
| 65-06-03 | 6 | DIAG-09, INST-08 | `diagnostic_fit verify-result`, complete `-m` command in 65-06 Task 3, then `-m unittest discover -s tests/phase65 -p 'test_*.py' -v` | durable result/full synthetic suite | Pending |

`diagnostic_probe` is created by 65-04; `logger-parity` and `verify-result` are
implemented there before 65-05 invokes them. `diagnostic_fit` begins in 65-01;
its registered CLI/timing extensions land in 65-06 Task 1 before the real smoke.

## Wave 0 requirements

- Create the four planned test modules and their small synthetic fixtures.
- Include open spies for validation, test and later-stage refusal, including
  normalization recovery; include relocated-artifact entry-point tests that
  assert no evaluation claim or dataset open occurs.
- Test original formatter boundaries, including `.3g` trailing-zero behavior,
  before running the historical reproduction.
- Verify the recorded normalizer digest without reopening Stage 1 records.
- Verify all 33 original pinned-module digests without rewriting old evidence.
- Existing Python, torch and unittest are sufficient; add no dependency.

## Real acceptance checks

- Preserve the original scripts and numerical transcript excerpts with source
  provenance. Commit expectations, exact comparison rule and failure branches
  before the probe's first run. Hash weights before loading.
- Reproduce the seven selected arm states and CPU-float64 initialization
  reconstructions. Additional per-layer values remain new measurements.
- Run the separately registered short system-1632 fit. Record physical scores,
  matched-window comparison predictors, similarity trace, actual steps, wall
  time and measured seconds per step.
- Attest to Stage-0 training-only access. Preserve the held-out evaluation.
  A failed reproduction follows the registered withdrawal/pivot branch.
- Smoke settings are locked-12, seed 42, MPS float32, system 1632 gold TRAIN,
  physical [0,10], 20 constant-rate Adam steps at 1e-4, and similarity at
  0/5/10/15/20. A supervised 600-second whole-run cap includes setup/scoring.
  MPS synchronization brackets every timed segment. The first two updates are
  warmup; 18 measured updates define optimizer seconds per step. Setup,
  warmup, logging, scoring and total elapsed time are separately reported.
- Longer runs remain blocked until governed pause/resume and power controls
  are proven compatible. Caps at or above 3600 seconds refuse before a read.
  No rate for an unmeasured depth/device/feature design is inferred.

## Manual-only verification

No technical acceptance check is intentionally manual. An owner decision is
required only for an actual scope/pivot or other reserved checkpoint.

## Validation sign-off

- [x] Final plan/task/wave map replaces capability placeholders.
- [x] Every planned task has an automated check and observable failure direction.
- [x] No three consecutive tasks omit automated feedback.
- [x] Missing test targets have an explicit creation task before their first use.
- [x] No watch-mode command or uncontrolled real run enters the quick suite.
- [ ] Quick-suite latency is measured during execution.
- [ ] Real acceptance registrations precede their respective first runs.

Approval remains pending execution validation. `nyquist_compliant` and
`wave_0_complete` are not asserted during planning.

## Source coverage audit

| Source | Item | Plans | Status |
|--------|------|-------|--------|
| GOAL | Lead on record or withdrawn; tested named fit/scoring path and measured smoke | 65-01 through 65-06 | COVERED |
| REQ | DIAG-09 original seven-arm init/selected-state reproduction, no updates | 65-04, 65-05 | COVERED |
| REQ | INST-08(a) locked forward parity | 65-01 | COVERED |
| REQ | INST-08(b) frozen scorer/comparators | 65-01, 65-06 | COVERED |
| REQ | INST-08(c) shared logger on committed arm | 65-04, 65-05 | COVERED |
| REQ | INST-08(d) Stage-0 TRAIN access and actual relocated production refusal | 65-02, 65-03, 65-06 | COVERED |
| REQ | INST-08(e) completed scored 1632 smoke | 65-06 | COVERED |
| RESEARCH | Exact stdout/scripts, formatter cells and precommit machine gate | 65-04, 65-05 | COVERED |
| RESEARCH | Full recorded normalizer, no Stage-1 recovery/refit | 65-02 | COVERED |
| RESEARCH | 33 frozen modules, direct current production interfaces | 65-01, 65-03, 65-06 | COVERED |
| RESEARCH | Bounded synchronized cost, no inherited multi-hour budget | 65-06 | COVERED |
| CONTEXT | D-01 delegated technical judgment and recorded limits | 65-01, 65-05, 65-06 | COVERED |
| CONTEXT | D-02, D-03 registration chronology and exact original provenance | 65-04, 65-05 | COVERED |
| CONTEXT | D-04 reconstruction versus same-runtime production parity | 65-01, 65-04, 65-05 | COVERED |
| CONTEXT | D-05 shared exact measurements and coordinates | 65-01, 65-04, 65-05 | COVERED |
| CONTEXT | D-06 committed seven arms/states, pre-load hashes, no updates | 65-04, 65-05 | COVERED |
| CONTEXT | D-07 association, withdrawal and owner-only pivot | 65-04, 65-05, 65-06 | COVERED |
| CONTEXT | D-08 variant registry and sealed historical protocol | 65-01, 65-03, 65-06 | COVERED |
| CONTEXT | D-09 Stage-0 TRAIN, ancillary reads and actual refusals | 65-02, 65-03 | COVERED |
| CONTEXT | D-10 frozen physical scoring/comparators and logger parity | 65-01, 65-05, 65-06 | COVERED |
| CONTEXT | D-11 registered bounded smoke and measured cost | 65-06 | COVERED |

Deferred experiments, yardstick/redesign choices and v2.6 amendments are
excluded by the source decisions. No source item in this phase is omitted.

## Source assumptions resolved during planning

- A1: confirmed current `SQRSkipResNetSIREN`, `data_only_loss`, `score_network`,
  `score_trajectory` and `two_kepler_prediction` interfaces. Confirmed the 33
  `PINNED_MODULES` paths and that train/evaluate/checkpoint/resume are unpinned.
- A2: confirmed `evaluate_run` claims evaluation and creates the held-out
  adapter before its existing payload load. New rejection therefore precedes
  manifest/claim/data effects. Confirmed actual `train.main` and resume routes.
- A3: confirmed reader_acceptance.json's full normalizer fields and recorded
  digest, `NormalizationStats`, `stats_digest` and `EXPECTED_STATS_SHA256`.
  Confirmed monitor recovery reads row keys and is unsuitable here.
- A4: confirmed the absolute interpreter exists, Python 3.11.15 and torch
  2.12.1. This was a runtime identity check, not a test or benchmark. Smoke
  throughput and quick-suite duration remain unknown until execution.
- A5: read both original scripts without execution and confirmed their exact
  hashes, centering/reductions, tau AD/FD comparator and field formatters.

## Spec-less edge coverage

All 13 supplied applicable rows are explicit plan truths with planned tests.
No row is silently dropped or resolved by an unverified generic backstop.

| Requirement/category | Explicit rule and verification | Plan |
|----------------------|--------------------------------|------|
| DIAG-09/boundary | Exact formatter-cell endpoints and nextafter neighbours | 65-04 |
| DIAG-09/adjacency | Original sample/layer order and original cosine epsilon | 65-04 |
| DIAG-09/empty | Missing/empty/singleton/undefined cases cannot reproduce | 65-01, 65-04 |
| DIAG-09/ordering | Fixed seven-arm order; init/selected and supplemental states distinct | 65-05 |
| DIAG-09/precision | Original formatters, signed zero, ties and .3g trailing zeros | 65-04 |
| DIAG-09/concurrency | Committed-clean gate, exclusive claim, incomplete interruption | 65-04 |
| INST-08/boundary | Physical window endpoint and numeric limits | 65-02 |
| INST-08/adjacency | Strict timestamps, no duplicate endpoint and fixed-T tau | 65-02 |
| INST-08/empty | Unknown/null/empty/undefined inputs refuse before steps | 65-01 |
| INST-08/encoding | Exact unique ASCII names and numeric record round trip | 65-01 |
| INST-08/ordering | Fixed cadence/order; equal metrics never change selection | 65-01 |
| INST-08/precision | Exact same-runtime parity, finite updates, frozen scoring | 65-01 |
| INST-08/concurrency | Exclusive output, deadline/interruption status, no altered retry | 65-06 |

Prohibition recall filtered routine correctness into these edge tests and kept
the two bespoke scientific-transparency constraints in Plans 65-05 and 65-06.
They were serialized with the existing `projectProhibitions` helper as
descriptor-less unresolved items, explicitly flagged-unverified for review.
They do not invent an owner gate or a science pass threshold. Canon security
items remain in the concrete per-plan threat registers; existing SCOPE-45..49
constraints remain executable acceptance rules. No external API/ORM feature
or dependency install applies. The assumption-delta detector returned false.

## Planning verification, 2026-10-28

The independent GSD plan checker passed all six plans and 15 tasks after one
revision. The revision joined paired verification commands with `&&` so an
earlier nonzero exit cannot be hidden by a later success. No blockers or
warnings remain in that review.

The orchestrator ran these planning checks from the trainex worktree:

- `gsd_run query verify.plan-structure <plan>` for each of `65-01-PLAN.md`
  through `65-06-PLAN.md`: six valid plans, 15 tasks, no errors or warnings.
- `gsd_run query check.decision-coverage-plan <phase-dir> <context-path>`:
  11 of 11 trackable decisions covered.
- `gsd_run check gap-analysis.plan-post <phase-dir> 'DIAG-09, INST-08' --raw`:
  both requirements and all 11 decisions covered, 13 of 13 items total.
- `gsd_run check verify-failure-directions 65 --raw`: all 15 automated blocks
  have observable failure statements, with no blockers or warnings.
- `gsd_run check verify-command-paths 65 --raw`: not applicable to these Python
  module invocations. This is not a path-resolution pass. A supplementary
  check confirmed that every Python module target is an existing source or an
  explicitly declared artifact created before use.
- `gsd_run query roadmap.validate`: no warnings.
- `git diff --check`: passed.

Here `<phase-dir>` is `.planning/phases/65-probe-on-the-record-fit-harness`
and `<context-path>` is that directory's `65-CONTEXT.md`. `gsd_run` invokes
`node <home>/.codex/gsd-core/bin/gsd-tools.cjs` in this session.
These results validate the plans. Application tests, the historical probe and
the real smoke remain unrun, so the execution validation flags above stay false.
