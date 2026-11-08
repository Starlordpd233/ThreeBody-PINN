# Phase 67 closeout — verified scope, validation and handoff

Written 2026-11-08 by plan 67-16 from committed evidence only. It records
what the phase verified, what stays scientifically unresolved, and what it
hands to Phase 68 and Phase 69. It makes no pass-bar ruling, no redesign
decision, and no scope or owner answer beyond the factual dispositions
recorded below. The independent verifier/orchestrator owns final phase
acceptance and roadmap/state bookkeeping.

## EXP-02..05 acceptance coverage

Each requirement ran through the same prospective chain, every step
committed before the next: committed design and prediction pages
(SCOPE-47) -> metadata registration -> gated read-only metadata capture ->
timing matrix and per-row registrations -> measured timing rows ->
cost-only budget and science matrix with per-row registrations -> science
rows launched exactly once -> machine review and result page -> conditional
owner checkpoint only when the registered branch required it.

| Requirement | Registered design | Rows run | Review verdict | Disposition |
|---|---|---|---|---|
| EXP-02 depth ladder (2/4/6/8/12 at locked everything else) | 67-08 (`evidence/exp02/design.json`) | 15/15 at common N=152900 | all four contrasts unsettled, `confirmed` empty | unsettled-continue, no scope proposal |
| EXP-03 rate ladder (1e-3..1e-5 incl. locked 1e-4 control) | 67-10 (`evidence/exp03/design.json`) | 15/15 at common N=155100 | lr1e-3 confirmed-worsening; nothing confirmed-improving | refuted lead -> owner ruling authorize-recorded-proposal |
| EXP-04 time-input design (encoded f1/f12 vs raw on both backbones) | 67-12 (`evidence/exp04/design.json`) | 18/18 at common N=112700 | all four contrasts unsettled, `confirmed` empty | unsettled-continue, no scope proposal |
| EXP-05 window ladder (signed 1/2/5/10-lap prefixes) | 67-14 (`evidence/exp05/design.json`) | 12/12 at common N=148700 | all three contrasts unsettled, `confirmed` empty | unsettled-continue, no scope proposal |

Review verdicts are transcribed from the committed reviews
(`evidence/exp0{2,3,4,5}/review.json`) and their byte-embedded result pages;
`67-FINDINGS.md` carries the cell-level numbers with digests. Repeat
coverage: every contrast read on main-1632-s42, repeat-851-s42 and
repeat-1632-s41; nothing was confirmed from the main run alone.

## Exact final evidence counts

- 4 committed designs with prediction pages; 4 timing-prediction pages;
  4 budget pages.
- 4 metadata registrations, 4 metadata captures (each `metadata/record.json`
  + `attempt.json` + `power-gate.json`, all attempts `published`).
- 4 timing matrices and 60 timing rows; 4 science matrices and 60 science
  rows (15/15/18/12 per experiment). Every row directory carries exactly
  five committed artifacts: registration.json, record.json, attempt.json,
  power-gate.json, diagnostic.weights (120 of each across the 60 timing and
  60 science rows). All 124 attempt records in the phase (120 rows + 4
  metadata) are `published` with complete records; no failed or partial
  attempt exists and no successful row counts anything but a published
  complete attempt.
- 4 reviews (schema `phase67-review/v1`) with byte-embedded result pages:
  `evidence/exp02/review.json` 853a41b7…, `evidence/exp03/review.json`
  ccd236ef…, `evidence/exp04/review.json` 4a2a9883…,
  `evidence/exp05/review.json` 2e3e5e4a…; result pages 67-EXP02-RESULT.md
  eb15b210…, 67-EXP03-RESULT.md 63d9148b…, 67-EXP04-RESULT.md 5bd076ec…,
  67-EXP05-RESULT.md dacb0127… (full digests in `67-FINDINGS.md`).
- 1 conditional ruling that actually exists: `67-EXP03-RULING.md`
  (2b6e8bd8…), digest-bound to the exp03 review and result page
  (`changed_by_ruling = false` for both). No other experiment produced a
  ruling file; their conditional checkpoints were skipped by their own
  registered conditions.
- Harness freeze manifest `evidence/harness-freeze.json` (a84c93ba…):
  41 frozen paths at source commit 84754309; the audit verifies it
  (`freeze_verified` true for all four experiments).
- `67-EVIDENCE-INDEX.json` is the read-only `audit-phase --json` object's
  exact data with status PHASE67-AUDIT-OK (the plan's equality check
  printed PHASE67-INDEX-OK); it is provenance, not a new evidence schema.

## Common-budget fairness

Each experiment's science budget was derived only from its own 18/15/15/12
measured timing rows (no borrowed historical rate), choosing the largest
common optimizer step count in 100-step quanta whose worst-row projection
fits under the 3540 s cap: exp02 N=152900, exp03 N=155100, exp04 N=112700,
exp05 N=148700 (200 warmup steps each; per-experiment `budget.json` files,
digests in `67-FINDINGS.md`). Every science row ran exactly once at its
experiment's common N with the registered similarity/score cadences, inside
its cap; no arm was lengthened, retried or re-sized after its score was
read (the no-continuation policy). Actual measured walls ran below the
projections in all four experiments (19,750.2 / 32,185 / 19,695 / 29,246 s
against 25,466.9 / 39,055.1 / 25,880.3 / 30,305.5 s), every row inside its
cap and launch-window allowance.

## Case/control comparisons and prospective chronology

- Controls are per-contrast and matched: d12 for EXP-02, lr1e-4 for
  EXP-03, each backbone's own raw input for EXP-04, lap10 for EXP-05. Each
  science row registered against a freshly registered control row of the
  same case.
- The reading rule (5% final-quarter settle line, 20% effect line,
  three-case direction agreement, all-six-endpoints-settled confirmation)
  was committed in designs and executable tests before any science run and
  was never re-set after a result (SCOPE-47).
- Chronology is re-derivable from git: designs/registrations precede
  captures and rows in plan order 67-08..67-15, one commit per row before
  the next launch, reviews committed at 67-09/67-11/67-13 and 3b19801c, the
  exp03 ruling at eab52f7d, and the persisted index re-derives
  registration-to-attempt relations through the audit's committed-state
  checks. The audit reads exp03 `proposal-ruled` and the other three
  `none`, with no problems.

## Scoped compatibility results (observed 2026-11-08)

- `tests/phase65` discovery: 204 tests, OK, 31.1 s — no weakened historical
  checks and no historical-byte changes.
- `tests/phase66` discovery: 101 tests, OK, 15.1 s — no raw shape drift and
  no historical digest mismatch.
- `tests/phase67` discovery: 260 tests, OK, 159.9 s, zero skipped required
  cases; per-module decomposition in `67-VALIDATION.md`.
- Protocol load: PROTOCOL-OK. Final audit: PHASE67-AUDIT-OK (exit 0) after
  the closure artifacts.
- The 65-CLOSEOUT.md affected-use conditions were applied before affected
  new use (reader hardening scoped to the paths Phase 67 uses, committed in
  plans 67-01..07; `test_historical` 9 tests OK).

## Immutable scientific boundary (unchanged by this phase)

- Stage 0 TRAIN only: every record attests TRAIN-only access with zero
  validation/test opens; no graded run, no held-out evaluation and no
  test-split file was opened; the single preserved evaluation stays
  unspent (SCOPE-45; `tests/phase67/test_isolation` 18 tests OK).
- Diagnostic artifacts are rejected by the production/evaluator entry
  points (`artifact_kind = diagnostic`, `counted = false` in every record;
  isolation tests assert the refusal paths).
- No framework-spec edit and no locked value moved (SCOPE-46); the harness
  freeze pins 41 paths at commit 84754309 and the audit verifies those
  bytes; experiments varied settings only inside the INST-08 diagnostic
  harness with fresh named variants and committed registrations.
- Compute stayed on this Mac under the AC/weekend gate with measured
  per-row seconds-per-step budgets (SCOPE-48); no run exceeded the 3540 s
  cap, so the governed pause/resume tooling was never required.
- SCOPE-49 factual dispositions: exp02 `none`, exp03 `proposal-pending`
  resolved by the owner's 2026-11-05 instruction ("proceed with option 1",
  option `authorize-recorded-proposal`, authorizing only EXP-04's dependent
  launch under its existing registration — no plan, scope, pass-bar or
  registration change), exp04 `none`, exp05 `none`. No unresolved reserved
  proposal exists; a pending proposal is never read as permission.

## Still-valid scientific uncertainty (not mechanical failure)

- Unsettled endpoints remain across EXP-02 (main-case and repeat-system
  d12 controls among others), EXP-04 (widespread, including both
  main-case encoded pairs) and EXP-05 (all main-case endpoints and the
  repeat-system lap10 control). Under the registered rule these outcomes
  are unsettled, not failures; the no-continuation policy extends nothing
  and no owner answer is invented for them.
- EXP-05's short-prefix fits are observed fits on exact signed
  first-crossing windows (0.95/1.89/4.76/9.51 on 1632; 0.54/1.08/2.68/5.37
  on 851), never full-window successes; the census mean period stays a
  labelled rough planning estimate.
- The recorded confounds stand: depth co-varies with parameter count
  (137,737..795,657), EXP-04's encoded arms change fan-in (1/16, 1/18) and
  input design rather than `first_omega_0`, and the Phase 66 positive
  control remains a multi-setting result that identifies no single
  enabling setting.
- Adjacent-time hidden-state similarity is associated evidence only; a
  failed finite-budget fit is not representational impossibility; no fit
  here generalizes to new initial conditions; GAP-59-08 keeps the energy
  question owner-routed and unadjudicated.

## Handoff

- **To Phase 68 (energy/yardstick):** the energy/yardstick issue is
  unchanged and unadjudicated. E throughout this phase is the frozen
  scorecard's position-error score; GAP-59-08 (the production energy check
  fails even a perfect answer on the coarse grid) remains owner-routed.
  Phase 68 owns any pass bar; nothing here proposes one.
- **To Phase 69 (final cause findings and redesign):** the evidence-backed
  finite-budget findings are the four experiment verdicts above with their
  cell-level records in `67-FINDINGS.md`, plus the actual machine cost:
  the four science campaigns measured 19,750.2 + 32,185 + 19,695 + 29,246 =
  100,876.2 s (about 28.0 hours) of launch wall against 120,707.8 s of
  committed projections, plus four small timing campaigns and four
  read-only metadata captures. Phase 69 owns its redesign decision; this
  closeout neither makes it nor edits its scope.
- **To the independent verifier/orchestrator:** final phase acceptance,
  the phase-tail workflow steps and roadmap/state bookkeeping are theirs;
  every claim here is checkable against the committed artifacts and the
  re-derivable `67-EVIDENCE-INDEX.json`.
