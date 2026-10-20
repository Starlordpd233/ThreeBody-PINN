---
phase: 60-single-system-learnability
plan: 06
subsystem: testing
tags: [gate-g2, sweep-pair, rescue, failed-confirmation, skip-records, stop-handoff, branch-state, owner-rulings, strict-machine-block, tracked-and-clean]

requires:
  - phase: 60-single-system-learnability
    provides: "Plan 60-01 arm record schema, exclusive record writer and Phase 60 static guard; Plan 60-23 closed arm catalog, panel constants and exit codes; Plan 60-05 is a coupling edge only (same-tree guard suites)"
  - phase: 59-read-only-baseline-scorecard
    provides: "frozen scorecard rules g2_fires, decision_verdict and OwnerRouted; the tracked-and-clean git check pattern; the synthetic-repository test helpers"
provides:
  - "pinn/verification/learnability_g2.py: Gate G2 from three committed Rung-1 records, the pinned sweep pair, the sweep curve and its one confirmation, the rescue or failed-confirmation record, byte-exact skip records, the Phase 64 stop handoff, the GATE-04 re-measure record reader, and the six-name branch query with its command line"
  - "pinn/verification/learnability_ruling.py: strict D-11 and GAP-60-09 ruling loaders (one machine block, one opaque owner quote, tracked and clean, SHA-256 cited) and the on-grid and equals-confirmed facts"
  - "tests/phase60/test_g2.py and test_ruling.py: 203 tests on synthetic git repositories, with scenario builders later plans can import"
affects: [60-09, 60-10, 60-13, 60-14, 60-15, 60-16, 60-17, 60-18, 60-19, 60-20, 60-21, 60-22]

actuals:
  tokens: 48003
  tasks: 3
  commits: 3
plan_head_before: 48be1d2fd4880b4a892de3218989ccd8d72e6207

tech-stack:
  added: []
  patterns:
    - "Recompute and compare: every committed record a query reads is rebuilt from the records it came from and compared after a JSON round trip; a mismatch halts"
    - "Tracked and clean as the only way into a decision (git ls-files --error-unmatch plus an empty git status --porcelain); an uncommitted file is PENDING in a query and a halt in a writer"
    - "Fence-aware opaque quote: a Markdown fence scanner closes a block only at a same-character fence at least as long, so quote content cannot cut a block short or add one"
    - "Cached scenario repositories: a synthetic git scenario is built once per process and copied for each test"
    - "A spy that wraps the frozen rule, to prove what it was called with and how often"
    - "Mutation checks with a scratch harness that restores the file and compares its SHA-256 after each mutation"

key-files:
  created:
    - pinn/verification/learnability_g2.py
    - pinn/verification/learnability_ruling.py
    - tests/phase60/test_g2.py
    - tests/phase60/test_ruling.py
  modified: []

key-decisions:
  - "branch_state recomputes g2-outcome.json from the Rung-1 records, sweep-curve.json from the four sweep records and rescue.json from the confirmation record and the run protocol, and halts on any mismatch (T-60-16); so a fixture for a later plan must carry the underlying arm records"
  - "Missing deciding file: pending (exit 4). Uncommitted or edited deciding file: PENDING in a query, G2-HALT (exit 2) in a writer. Malformed or inconsistent committed file: always G2-HALT"
  - "The run protocol's pre-answer is final when it is not null; the GAP-60-09 ruling is read only when the protocol holds none; a confirmed rescue always goes to checkpoint 4"
  - "A go-to-verdict ruling that also names approved_first_omega_0 is refused (stricter than the plan's required-only-for-continue)"
  - "After a continue the ladder opens only when a committed GATE-04 re-measure passed at exactly the ruling's value under the ruling's SHA-256; a BLOCK holds it for the owner; a mismatch halts"
  - "The circled digit in the second skip reason is stored as the escape U+2463 in source, never as a literal character, because NFKC normalization turns the literal into the digit 4"

patterns-established:
  - "Owner answers enter the harness only through learnability_ruling: fixed paths, strict block, opaque quote, SHA-256 cited downstream"
  - "One module-level exception per outcome class: G2Halt (exit 2), G2Pending (exit 4), OwnerRouted and FailedConfirmationOwnerStop (exit 3, handled only in main)"

requirements-completed: [FEAS-03, FEAS-04, FEAS-09]

coverage:
  - id: D1
    description: "Gate G2 is the frozen g2_fires on the three committed Rung-1 tiers in panel order; exactly one failing system and Tier exactly 1 do not fire; g2-outcome.json records tiers, record hashes, failing systems and, when fired, the pinned sweep, confirmation and uncovered systems"
    requirement: "FEAS-03"
    verification:
      - kind: unit
        ref: "tests/phase60/test_g2.py#G2RuleTests, SweepPlanTests, OutcomeWriterTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "The sweep curve needs all four settings of the recorded sweep system; the confirmation is the highest first_omega_0 at Tier 1 or better (Tier exactly 1 counts), with the other Tier 1 settings labelled not confirmed and none meaning no confirmation"
    requirement: "FEAS-03"
    verification:
      - kind: unit
        ref: "tests/phase60/test_g2.py#ConfirmedOmegaTests, SweepCurveTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "A confirmed rescue writes rescue.json and then reaches the frozen OwnerRouted at main once (exit 3, no retry); a confirmation below Tier 1 follows the protocol pre-answer, and with none raises FailedConfirmationOwnerStop without calling decision_verdict"
    requirement: "FEAS-03"
    verification:
      - kind: unit
        ref: "tests/phase60/test_g2.py#RescueTests, ModuleContractTests"
        status: pass
    human_judgment: false
  - id: D4
    description: "Skip records accept only the two byte-exact reasons, only the one the committed records imply, never after a Rung-2, probe or continue arm has a run or evidence directory, and once; the stop handoff holds the frozen verdict computed with four None inputs (none on go-to-verdict), Level 3 as not tested (skipped at G2), Phases 61-63 as skipped not failed, and per-arm wall hours"
    requirement: "FEAS-04"
    verification:
      - kind: unit
        ref: "tests/phase60/test_g2.py#SkipWriterTests, StopHandoffTests, OwnerStopPathTests"
        status: pass
    human_judgment: false
  - id: D5
    description: "D-11, GAP-60-09 and GAP-60-11 loaders: one strict machine block, one opaque owner-quote block that a hostile quote cannot change, closed key sets, plain positive decimals (any off-grid value accepted), tracked and clean files only, SHA-256 returned, on_grid and equals_confirmed facts"
    requirement: "FEAS-09"
    verification:
      - kind: unit
        ref: "tests/phase60/test_ruling.py"
        status: pass
    human_judgment: false
  - id: D6
    description: "The six-name branch query (sweep, confirmation, owner-decision, stop, continue-gate, ladder) answers TAKEN, NOT-TAKEN or PENDING from committed records; an unanswered checkpoint holds the ladder; the ladder after a continue waits for a GATE-04 PASS at the ruling's value; a skip beside a taken ladder halts"
    requirement: "FEAS-03"
    verification:
      - kind: unit
        ref: "tests/phase60/test_g2.py#BranchTracerTests, BranchSweepTests, BranchOwnerTests, RemeasureRecordTests"
        status: pass
    human_judgment: false
  - id: D7
    description: "The Phase 60 static guard, the Phase 59 static guard and the Phase 38 and 39 prohibition suites pass with both new modules in the scan set"
    verification:
      - kind: unit
        ref: "tests/phase60/test_static_guards.py; tests/phase39/test_prohibitions.py; tests/phase59/test_static_guards.py"
        status: pass
    human_judgment: false
  - id: D8
    description: "Readings of the plan text that the sources leave open (listed under Decisions Made and in the report): go-to-verdict with a value is refused; the protocol pre-answer beats a GAP-60-09 file; skip and ladder interplay; JSON field names beyond the ones the plan names; the re-measure artifact bytes are not read by the branch query; writers' pending versus halt"
    verification: []
    human_judgment: true
    rationale: "Each choice fails closed and moves no locked value, but they fix the record and refusal shapes that Plans 60-09, 60-10, 60-13 and 60-14 to 60-22 read. The owner or verifier should confirm them, or ask for a gap entry, before the first real arm."

duration: 60min
completed: 2026-10-20
status: complete
---

# Phase 60 Plan 06: G2 rules, skip writer, owner rulings and branch state Summary

**Gate G2, the pinned sweep pair, the one confirmation, the rescue or failed-confirmation record, byte-exact skip records and the Phase 64 handoff are now small tested functions over committed files, the owner's checkpoint 4 and GAP-60-09 answers are read only through a strict ruling loader with an opaque quote, and one read-only query tells every later plan whether its branch is taken, not taken or still waiting.**

In plain language: after the first three experiments a fixed rule decides what happens next. This plan turns that rule into code that decides from committed files only, records its answer once, hands the owner's questions to the owner untouched, and refuses to guess when a file is missing, uncommitted or contradicts the files it came from.

## Performance

- **Duration:** about 1h of active work. The first 48 min ran from 2026-10-20T03:50:41Z to the last Task 3 verification; a session-limit pause of about 3h 13m followed; about 10 min of closeout came after it. Wall clock from start to the SUMMARY is about 4h 8m.
- **Started:** 2026-10-20T03:50:41Z
- **Completed:** 2026-10-20T07:58:00Z (approximate; the SUMMARY commit follows)
- **Tasks:** 3 (Task 1 tracer, Task 2, Task 3)
- **Files:** 4 created (4,244 lines: g2 module 1,259, ruling module 292, test_g2 2,099, test_ruling 594); no file modified

## Accomplishments

- **Gate G2 and the sweep pair (Task 1).** `g2_outcome` applies the frozen `g2_fires` to the three committed Rung-1 tiers in panel order and, when it fires, names the sweep, confirmation and uncovered systems with `sweep_plan` (laps 10.47, 18.61, 39.35; the four pinned cases tested, plus input order and the refusals). `outcome` writes `g2/g2-outcome.json` once with tiers, per-record SHA-256, failing systems and the pair. The tracer `branch` query read only tracked and clean files.
- **Sweep, confirmation, rescue (Task 2).** `sweep-curve` needs all four settings of the recorded sweep system and picks the highest `first_omega_0` at Tier 1 or better (labels: selected, reached Tier 1 not confirmed, below Tier 1; none means no confirmation and no rescue). `rescue` writes `rescue.json` first, then hands the frozen rule `sweep_rescued=True` with four `None` inputs so `OwnerRouted("owner checkpoint 4")` reaches `main` once; below Tier 1 it follows the protocol's `g2.failed_confirmation_pre_answer` (`no_rescue` returns, `rescue` goes to checkpoint 4, null raises `FailedConfirmationOwnerStop` without any verdict call).
- **Skip records and the handoff (Task 2).** `skip --reason` accepts only the two byte-exact reasons (the second holds U+2463), only the one the records imply, and refuses once any `r2a`, `r2b`, `p1`, `p2b` or `c-` arm has a run or evidence directory (all 23 ids tested, both kinds of directory). `stop-handoff` carries the frozen verdict computed with four `None` inputs, Level 3 as "not tested (skipped at G2)", Phases 61-63 as "skipped at G2, not failed", Phase 64 next, and per-arm wall hours (seven arms with no confirmation, eight with one).
- **Rulings (Task 3).** `learnability_ruling` accepts a ruling file only when it is tracked and clean, holds exactly one `phase60-ruling` block and exactly one `owner-quote` block, uses closed key sets and plain positive decimals, and returns the file's SHA-256. The quote is located by its fences and never read. Hostile quotes (a fake machine block, shorter fences, answer words, a path, a shell command, Python text, a 100,000-character line) change nothing, and a spy on `subprocess.run` shows only fixed `git` argument lists. The real tree holds no ruling, so the loaders fail closed with `RulingMissing`.
- **Branch table (Tasks 2 and 3).** A confirmed rescue takes `owner-decision` and leaves `stop`, `continue-gate` and `ladder` PENDING until the ruling is committed; `go-to-verdict` takes `stop` with the second skip reason; `continue` at a value (on or off the grid) takes `continue-gate` with that `first_omega_0`; the ladder then waits for a committed GATE-04 re-measure PASS at exactly that value and the ruling's SHA-256 (BLOCK gives "GATE-04 BLOCK at 120.0; owner"; another value or hash halts); G2 passed takes the ladder at 30.0 with provenance `locked`; a skip beside a taken ladder halts.
- **Real-tree smoke (read-only).** `learnability_g2 branch <name>` for all six names prints `BRANCH-PENDING` (g2-outcome.json is not recorded) and exits 4 against the real evidence tree; nothing was written.

## Task Commits

1. **Task 1: Tracer, Gate G2 from three committed records to the branch query** - `f3780d6d` (feat)
2. **Task 2: Sweep curve, rescue, skip records and stop handoff** - `ba4df889` (feat)
3. **Task 3: Rulings, owner-decision, continue gate and ladder** - `be5ed70f` (feat, subject as the plan states)

**Plan metadata:** the SUMMARY commit that follows this file (docs).

Tracer feedback gate after Task 1: not auto mode (`_auto_chain_active` false, `auto_advance` unset), `human_verify_mode` unset so `end-of-phase`, verify has only an automated command, so it was re-run on the committed tree (39 tests OK) before Task 2 started: "Tracer verified end-to-end - expanding".

## Files Created/Modified

- `pinn/verification/learnability_g2.py` - the rules, writers, handoff, re-measure reader, branch query and command line
- `pinn/verification/learnability_ruling.py` - `parse_machine_block`, `load_checkpoint4_ruling`, `load_gap6009_ruling`, `ruling_grid_facts`, `tracked_and_clean`, `RulingError` with `RulingMissing` and `RulingUncommitted`
- `tests/phase60/test_g2.py` - 145 tests in 14 classes; also the scenario builders `Tree`, `outcome_tree`, `curve_tree`, `protocol_tree`, `confirmed_tree`, `rescued_tree`, `record_payload`, `remeasure_payload`
- `tests/phase60/test_ruling.py` - 58 tests in 5 classes, with the synthetic ruling-file builders `checkpoint4` and `gap6009`

## Decisions Made

Readings of the plan text that I had to choose between (all fail closed; none moves a locked value):

- **Commit shape.** Three commits, one per task, as the orchestrator briefing requires. The plan's Task 3 action names one commit "of the plan's modules and tests"; Tasks 1 and 2 got their own descriptive subjects and Task 3 uses the plan's subject.
- **go-to-verdict plus a value.** "Required only for continue" is read as "named only for continue": a go-to-verdict ruling that also names `approved_first_omega_0` is refused.
- **Record container.** `g2_outcome` takes `Rung1Record` (system_id, arm_id, path, sha256, tier) from `load_rung1_records`, not raw dicts.
- **Field names beyond those the plan names.** The plan names `g2_fired`, `sweep_system`, `confirmation_system`, `uncovered_system`, `confirmation_arm`, outcome values and the labels. I added `panel_systems`, `tiers`, `records[]`, `failing_systems`, `rows[]` (first_omega_0, arm_id, record_sha256, tier, E, eps_h, h, label), `confirmed_first_omega_0`, `g2_outcome_sha256`, `record`, `sweep_curve_sha256`, `pre_answer`, `entries{FEAS-04, FEAS-09}`, `level3`, `basis[]`, `stop_reason`, `verdict`, `owner_answer`, `verdict_note`, `arms[]`, `total_wall_hours`. Rows copy the record's `result.h` pairs and check them against the scorecard horizons 0.01 and 0.1.
- **Command-line tokens for writers** (the plan fixes only the branch lines and the exit codes): `G2-OUTCOME-WRITTEN`, `SWEEP-CURVE-WRITTEN`, `RESCUE-WRITTEN`, `SKIP-RECORDS-WRITTEN`, `STOP-HANDOFF-WRITTEN`. Output goes to stdout. A second write of any file exits 2 (`FirstResultExists` is mapped to `G2Halt` inside the module so `main` keeps a narrow handler list).
- **Pending versus halt in writers.** A missing deciding file exits 4; an uncommitted one exits 2; a missing run protocol exits 2.
- **Branch semantics.** `sweep` is TAKEN iff G2 fired. `confirmation` is TAKEN iff the curve names a setting, and stays TAKEN after the run. `owner-decision` is TAKEN for a confirmed rescue, a failed confirmation pre-answered `rescue`, or a failed confirmation with no pre-answer, and stays TAKEN after the owner answers (so it is PENDING only when its inputs are missing). A skip file keeps the ladder NOT-TAKEN even while the other records are undecided; a skip beside a taken ladder halts; on a stop path a skip with a different reason halts (my addition); an uncommitted skip makes the ladder PENDING.
- **Pre-answer versus GAP-60-09 file.** A non-null protocol pre-answer is final and a GAP-60-09 file is then ignored; the file is read only when the protocol holds null. A confirmed rescue goes to checkpoint 4 whatever the pre-answer. `rescue.json` carries the pre-answer, so `rescue` and the branch query need the committed protocol even for a confirmed rescue.
- **Deep recompute in `branch_state`** (T-60-16 read literally), described under key-decisions.
- **Re-measure artifact.** `R_REF_APPROVED_REL` is exported for Plan 60-09 and the others, but the query validates only the shape of `r_ref_artifact` (`path` and 64-hex `sha256`) in a PASS record. It does not read the artifact's bytes, because Plan 60-09 owns that file and I cannot see how it will record the path.
- **Handoff.** `stop-handoff` also refuses once a ladder arm has started (the same guard as the skip writer). Arms are Rung 1, the four sweep settings and the confirmation if the curve names one. `wall.hours` is required; `timing.seconds_per_step` is carried when present, else null.
- **Signatures.** `repo_root` (default: the git top level above the evidence root) and `scorecard` (default: the frozen scorecard) are optional keywords everywhere; the plan shows `repo_root` required for three functions.
- **Ruling parser.** Fences follow Markdown (at most three spaces of indent; a backtick fence's info string holds no backtick; line breaks are `\r\n`, `\n` and `\r` only); key lines start at column 0 and need a space or tab after the colon; blank lines are ignored; leading zeros are accepted; any unclosed fence is an error; symbolic links and paths outside the repository are refused.

## Deviations from Plan

None - plan executed as written. Additions beyond the plan text, all inside the plan's own threat model or needed to run it: the names `G2Pending`, `UncommittedInput`, `Rung1Record`, `Remeasure`, `parse_remeasure`, `RulingMissing`, `RulingUncommitted` and the public `tracked_and_clean`; refusal of a symbolic link as a record or ruling; the hash-shape checks in `parse_remeasure`; the started-ladder guard on the handoff.

**Total deviations:** 0 auto-fixed. **Impact on plan:** none; no file outside the four owned paths changed.

### Process notes

- **RED evidence.** Task 1: `ImportError` (module missing). Task 2: `Ran 136 tests`, `FAILED (failures=5, errors=99)`, all missing commands or symbols. Task 3: the ruling tests failed on the missing module; the g2 module failed 59 checks, all in the three new classes (`BranchOwnerTests`, `OwnerStopPathTests`, `RemeasureRecordTests`). Each task's tests and code are in one commit, as the plan fixes one commit per task.
- **Mutation checks, 144 mutants in four batches** (module text changed one place at a time, tests run, file restored and its SHA-256 compared each time): Task 1 24 (23 caught, 1 equivalent: the frozen `g2_fires` also rejects bool and float tiers), Task 2 53 (49 caught; of 4 escapes 2 were equivalent because a later check also refuses, 2 exposed missing tests for the horizon check and a confirmed rescue with a `no_rescue` pre-answer), Task 3 g2 32 (29 caught, 3 test gaps), ruling 35 (29 caught, 6 test gaps). All 11 test gaps were closed and their mutants re-run and caught; 3 equivalent mutants remain. A first AST test of mine flagged `re.compile` as dynamic execution and was narrowed.
- **A time-bomb test was dropped.** A test that the real repository holds no ruling would fail the day Plan 60-17 commits the real ruling; fail-closed behavior is tested on synthetic repositories instead.
- **Co-author trailer** is `Claude Sonnet 5.5` per the orchestrator's protocol; the plan text names Opus 5.5.
- **Branch assertions.** The generic executor rule that a linked-worktree branch be named `agent-*` does not apply: the orchestrator ran this plan sequentially on `milestone/v2.4`. The cwd-drift and protected-branch assertions ran before each commit.
- **Not touched.** `STATE.md`, `ROADMAP.md` and `REQUIREMENTS.md` (FEAS-03, FEAS-04 and FEAS-09 are declared by other plans too, so the orchestrator marks them), the user-owned changes in the tree, and `.planning/WINDOWS.md` (no stub, skipped test or unrun verify was left). The Sequentialthinking MCP named in `CLAUDE.md`, ToolSearch and the context-mode tools were not available to this executor.

## Issues Encountered

- The edit tool turned the escape `④` into the literal circled digit in my first writes. A literal U+2463 becomes the digit 4 under NFKC normalization, which would silently change a pre-registered reason, so the module and the tests use the escape; both sources are ASCII-only (the ruling module's first docstring line keeps the literal digit, as the plan specifies, and is documentation only).
- The tests were slow at first (56 s for `test_g2`). Cached scenario repositories brought it to 37 to 50 s; the three-module Task 3 verify takes 61 s, just over the 60 s expensive-command mark, so it was run once and its output retained.
- A session-limit pause came between the last Task 3 verification and the Task 3 commit. On resume I confirmed that HEAD was my own Task 2 commit, that nothing else had changed, and that the SHA-256 of the four owned files equalled the hashes in the retained verify log before staging and committing exactly those four paths.

## Verification Results

| Command | Result |
|---|---|
| Task 1 verify: `python -B -m unittest tests.phase60.test_g2 -v` | Ran 39 tests in 7.1 s, OK; re-run on the committed tree as the tracer gate: Ran 39 tests, OK |
| Task 2 verify: `... tests.phase60.test_g2 tests.phase60.test_static_guards -v` | Ran 138 tests in 40.2 s, OK |
| Task 3 verify 1 and plan verification 1: `... tests.phase60.test_ruling tests.phase60.test_g2 tests.phase60.test_static_guards -v` | Ran 229 tests in 61.0 s, OK. Run once on the final tree; reused after the pause because the four files' SHA-256 (g2 `3104be6b29be`, ruling `1f7da2b2925e`, test_g2 `39c24f6a9af8`, test_ruling `88969485eaeb`) match the log header and the commit records byte-identical files |
| Task 3 verify 2 and plan verification 2: `... tests.phase39.test_prohibitions` with the four named `tests.phase38.test_prohibitions` tests `-v` | Ran 35 tests in 1.9 s, OK |
| Extra: `... tests.phase59.test_static_guards -v` | Ran 15 tests, OK |
| Earlier guard runs (Task 1 tree, Task 2 tree) | 61 tests OK and 50 tests OK |
| `fails_when` strings (FAILED, Error, Ran 0 tests) in every retained verify log | none |
| `git diff --quiet 48be1d2f HEAD --` STATE, ROADMAP, REQUIREMENTS, the frozen scorecard and its JSON, and the Plan 60-01, 60-23 and 60-05 modules | exit 0 (unchanged) |
| `git diff --quiet HEAD --` the four owned files | exit 0 (working tree equals HEAD) |
| `git diff --diff-filter=D --name-only HEAD~1 HEAD` after each commit | no deletions |

Complete logs are retained outside the repository in the session scratchpad (`.../scratchpad/exec-60-06/`; each starts with the command and HEAD). The whole `tests/phase60` package was not re-run: this plan changes no existing Phase 60 module, and the guard that scans the new modules is in the verify command.

## Known Stubs

None.

## Threat Flags

None. The modules add no endpoint, authentication path or corpus access. They read committed JSON and Markdown and run `git` with fixed argument lists. Threat register: T-60-04 mitigated (closed keys, plain decimals, one machine and one quote block, tracked and clean, SHA-256 cited; `MachineBlockTests`, `OpaqueQuoteTests`, `CommittedTests`); T-60-11 mitigated (both owner stops handled only in `main`, exit 3, `RescueTests`, `ModuleContractTests`, the static guard); T-60-15 mitigated (byte-exact reasons, implied-reason check, 23-id started-ladder refusal, single write; `SkipWriterTests`); T-60-16 mitigated (recompute and compare, `BranchSweepTests`, `BranchOwnerTests`); T-60-05 mitigated (fixed ruling paths; a subprocess spy shows no file value in any command); T-60-06 mitigated (every writer goes through `write_record_exclusive`, repo-relative paths and digests only, no home or absolute path in any written file); T-60-SC accepted (nothing installed).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Plan 60-09 (re-measure).** Constants `REMEASURE_REL`, `R_REF_APPROVED_REL`, `REMEASURE_SCHEMA`; the record the ladder reads has `verdict` PASS or BLOCK, boolean `complete_pass` (true for PASS, false for BLOCK), `first_omega_0` (compared exactly with the ruling's), `ruling_sha256` (64 lowercase hex, compared with the ruling's) and, for PASS, `r_ref_artifact {path, sha256}`. `learnability_ruling.load_checkpoint4_ruling` and `ruling_grid_facts` give the value and the on-grid and equals-confirmed facts.
- **Plan 60-10 (admission).** Use `branch_state(name, *, evidence_root, repo_root=None)`; the ladder's TAKEN state carries `first_omega_0` and `omega_provenance` (`locked` at 30.0, `owner_approved` after a continue). Because queries recompute from the underlying arm records, a fixture needs committed real-kind `arms/<id>/record.json` files with `schema`, `run_kind`, `arm_id`, `first_omega_0`, `omega_provenance`, `result {tier, E, eps_h, h}` and `wall.hours`; the builders in `tests/phase60/test_g2.py` produce a consistent tree. The run protocol must hold `g2.failed_confirmation_pre_answer` (null allowed) before any `rescue`.
- **Plan 60-13 (verifier).** Public rule functions: `sweep_plan`, `confirmed_omega`, `g2_outcome` (takes `Rung1Record`), `parse_remeasure`; file schemas `phase60-g2-outcome/v1`, `phase60-sweep-curve/v1`, `phase60-rescue/v1`, `phase60-skip-records/v1`, `phase60-stop-handoff/v1`.
- **Plans 60-14 to 60-22.** Command line: `python -B -m pinn.verification.learnability_g2 {outcome | sweep-curve | rescue | skip --reason <exact> | stop-handoff | branch <sweep|confirmation|owner-decision|stop|continue-gate|ladder>} [--evidence-root PATH]`. Branch lines are `BRANCH-TAKEN|NOT-TAKEN|PENDING: <name> (<reason>)`; exits 0 ok, 2 `G2-HALT`, 3 `OWNER-ROUTED`, 4 pending. `rescue` exits 3 on a rescue and on an unanswered failed confirmation, 0 on a failed confirmation pre-answered `no_rescue`, and a second run exits 2.
- **Plan 60-17 (writing the rulings).** The files are `60-CHECKPOINT-4-RULING.md` and `60-GAP-60-09-RULING.md` in the phase directory. One fenced block with info string `phase60-ruling` holding `ruling: checkpoint-4` and `answer: continue` plus `approved_first_omega_0: <plain decimal>` (or `answer: go-to-verdict` with no value), or `ruling: gap-60-09` and `reading: no_rescue` or `rescue`; one fenced block with info string `owner-quote` fenced longer than anything inside it; key lines at column 0 with a space after the colon; the file committed before any query reads it.
- **Open for the owner or verifier:** coverage item D8, the readings listed under Decisions Made.

## Post-execution fix (orchestrator, 2026-10-20)

The chain closeout ran the four-module verify command once and it failed with one error: `shutil.copytree` in `Tree.scenario` raised ENOENT on 18 entries under `.git/objects` of a cached template repository (nothing outside `.git/objects` failed). Every `git commit` starts a detached `git maintenance run --auto`, which can run `git repack -d` and delete loose objects mid-copy; a traced run of the module spawned 310 maintenance processes and 2 repacks. The same command passed on an immediate rerun (357 tests), so the failure is intermittent.

Commit `08ea9a2a` turns off `maintenance.auto` and `gc.auto` in the fixture's repositories and adds `FixtureRepoTests` (one test, which fails if the fixture goes back to plain `init_repo`). `test_g2` now has 146 tests and `tests/phase60` discovery 579. A traced run after the change spawned no maintenance process. Only `tests/phase60/test_g2.py` changed; no module under `pinn/` did. The mechanism is established, but the one observed failure was not reproduced on demand. Other fixtures that copy a live git repository would have the same exposure; they were not audited.

---
*Phase: 60-single-system-learnability*
*Completed: 2026-10-20*

## Self-Check: PASSED

- All four created files exist on disk; commits `f3780d6d`, `ba4df889` and `be5ed70f` exist and `git log --grep='(60-06)'` returns exactly them; both module docstrings start "Phase 60".
- Task acceptance criteria and the plan-level verification were re-established on the final tree: the 229-test run covers every acceptance class of Tasks 1 to 3 plus the static guard, and the 35-test run covers the prohibition suites; the inputs are byte-identical to the ones committed.
- STATE.md, ROADMAP.md, REQUIREMENTS.md, the frozen scorecard and the earlier Phase 60 modules are unchanged since the plan base; the working tree holds only the user-owned changes.
