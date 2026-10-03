---
phase: 57-corrected-re-run-the-preserved-evaluation
plan: "05"
subsystem: training-run
tags: [stage0, run-window, invariant-b, terminal, provenance, detached-launch]

requires:
  - phase: 57-corrected-re-run-the-preserved-evaluation
    provides: "57-04's fresh GATE-04 PASS, final-R_ref production conformance, canonical evaluator boundary, and Phase-57 evidence tooling"
provides:
  - "An admitted, commit-free generation-7 run window at HEAD 629b1a6c (smoke plus graded seed 42)"
  - "The authorized invariant-B terminal closure (invariant_b_halt_no_advance) with the held-out evaluation preserved-unspent"
  - "Append-only provenance for generations 1-7, with generations 2, 5, 6 and 7 retained in Git under exact manifests"
  - "A detached launcher (GAP-57-12 L1) whose launch, process, output and exit records bind every generation-7 process"
affects: [57-06, RUN-04, RUN-05, EVAL-02]

plan_head_before: 87e50573a36c3398c459f35018c6dda6e904840f
commits: 25

key-files:
  created:
    - .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/terminal-state.json
    - .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/launch_phase57_run.py
    - .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/generation-7-retention.json
    - .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/generation-6-retention.json
    - .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/blocked-state-g6.json
    - configs/stage0-v23g7-smoke.yaml
    - configs/stage0-v23g7-seed42.yaml
    - tests/phase57/test_phase57_launcher.py
  modified:
    - .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/run-ledger.md
    - .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/verify_phase57_evidence.py
    - scripts/git_policy/validate_staged_paths.py

key-decisions:
  - "Seed 42's invariant-B trip at step 951 (front high-water 2 since step 450; 501 > N=500) is the authorized terminal branch of Task 3, not an operational block; later launches stopped."
  - "The terminal reason uses the verifier/README token invariant_b_halt_no_advance; the plan prose's 'invariant-b-no-advance' is a wording variant the verifier would reject."
  - "Six earlier band generations ended in operational blocks or historical attempts; each continuation was owner-ruled (GAP-57-02..12) rather than improvised."

requirements-completed: []

coverage:
  - id: D9
    description: "The generation-7 smoke and every attempted graded run share one commit-free admitted HEAD (629b1a6c)."
    requirement: RUN-04
    verification:
      - kind: other
        ref: "verify_phase57_evidence.py admit-run-window and run-window (terminal); ledger generation 7 records"
        status: pass
    human_judgment: false
  - id: D10
    description: "Produced smoke and graded seed-42 splits.json bytes and exact s_h/n_train matched before seeds 41 or 43 could launch."
    requirement: RUN-04
    verification:
      - kind: other
        ref: "verify_phase57_evidence.py seed42-setup (SEED42-SETUP-OK)"
        status: pass
    human_judgment: false
  - id: D16
    description: "The invariant-B no-advance trip closed the window terminally with evaluation preserved-unspent and no tuning authorized."
    requirement: RUN-05
    verification:
      - kind: other
        ref: "evidence/terminal-state.json; verify_phase57_evidence.py run-window (RUN-WINDOW-TERMINAL-OK)"
        status: pass
    human_judgment: false

duration: "generation-7 window 4 h 21 min (smoke 64 min, graded seed 42 194 min)"
completed: 2026-10-03
status: complete
---

# 57-05 Summary — Corrected Stage-0 run window

## Outcome

The run window closed on the **authorized invariant-B terminal branch**. On
generation 7 (HEAD `629b1a6c`), the calibration smoke finished. Graded seed 42
then tripped the invariant-B guard at step 951: the frozen training-only
monitor's causal-front high-water mark reached 2 at step 450 and did not
advance again within the ratified `front_advance_window_n = 500`. Under Task 3
this stops later launches. Seeds 41 and 43 were not run, the held-out
evaluation remains **preserved-unspent**, and the result authorizes no tuning.

The plan's `<done>` criterion is met through its second branch: "invariant-B
no-advance closes terminally with evaluation unspent." Requirement status
(RUN-04/RUN-05) is left to phase verification.

## Performance

| Run | Start (UTC) | End (UTC) | Wall time | Exit | Outcome |
|---|---|---|---|---|---|
| `stage0-v23g7-smoke` | 2026-10-03 03:31:45 | 04:36:04 | 3,858.6 s | 0 | finished, 300/300 steps |
| `stage0-v23g7-seed42` | 2026-10-03 04:38:08 | 07:52:30 | 11,661.9 s | 1 | invariant-B HALT at step 951 |

Throughput was 12.2–12.9 s/step at 4096 collocation rows on MPS/float32. MPS
driver memory stayed near 370 MB.

## Accomplishments

- **Generation history preserved append-only.**
  - Generation 1: blocked on a memory guard (GAP-57-02/03).
  - Generation 2: retained interrupted smoke (GAP-57-06).
  - Generation 3: sandbox-blocked (GAP-57-07/08).
  - Generation 4: non-resumable operator stop (GAP-57-09).
  - Generation 5: completed smoke, retained (GAP-57-10/11).
  - Generation 6: graded seed 42 lost silently at step 513 (GAP-57-12).
  - Generation 7: the terminal band.
- **The generation-6 loss addressed at its root.** That trainer's lifetime and
  stderr were tied to the agent session that launched it.
  `launch_phase57_run.py` now runs the unchanged trainer command under a
  supervisor in its own session, retaining output and exit status. A test
  replays the failure (SIGHUP and SIGKILL to the launching process group) and
  the trainer survives.
- **Produced-artifact D-10 check passed before any other seed.**
  `seed42-setup` found the smoke and graded seed-42 `splits.json` bytes
  identical (`5846ae5b…`) and `s_h = 22.321729071058996`, `n_train = 1812`
  exactly equal.
- **Terminal closure recorded and verified.** `terminal-state.json`
  (`phase57-terminal-state/v1`) binds the guard trip record, the failure and
  latest checkpoints, and the launcher exit record by SHA-256. The ledger marks
  generation 7 `terminal`.

## Task Commits

Commits since 57-04 (`87e50573`), oldest first:

- **Generation 1 and 2:** `9b4f6e05`, `86dcd9f2`, `db107c49`, `afc3e600`,
  `ea925010`, `82df39cc`, `93fff5c1`, `bb09bc8c`, `3ca31d3c`, `266b1f11`,
  `a3279e2c`, `63cb8616`.
- **Generations 3–6:** `6651f90e`, `bd4396a2`, `9264951c`, `ad96e6f4`,
  `a43ff611`, `f0855a20`, `d4ba8ef3`, `b151e02d`, `944f920b`, `ef4764f9`.
- **Generation 6 loss, generation 7 preparation and terminal:** `86957639`,
  `629b1a6c`, `e0ec85f6`.

## Validation Evidence

| Check | Result |
|---|---|
| `verify_phase57_evidence.py admit-run-window` at `629b1a6c` (twice, before authorization and before launch) | `ADMIT-RUN-WINDOW-OK`, MPS visible |
| `python -m pinn.verify` after the smoke (required by the >30-min duration gate) | GREEN, 5/5 rungs, marker bound to `629b1a6c` |
| `verify_phase57_evidence.py seed42-setup` | `SEED42-SETUP-OK` |
| `verify_phase57_evidence.py run-window` | `RUN-WINDOW-TERMINAL-OK`, re-deriving all 67 retained generation-7 files from Git and disk |
| `python -m unittest discover -s tests/phase57 -t .` (pre-launch, 255 s) | 104 tests OK, 1 platform skip |
| `tests.phase57.test_evidence_ledger_v2` + `test_phase57_launcher` (after retention) | 44 tests OK |
| `tests.git_policy.test_git_policy.StagedPathPolicyTests` | 12 tests OK |

## Descriptive record (no inference)

- The generation-7 smoke's invariant-B state (front 1, last advance at step 93)
  matches the generation-6 smoke's.
- The lost generation-6 graded seed 42 had reached front 2 at step 353 and was
  still at 2 when it died at step 513. The generation-7 graded seed 42 reached
  front 2 at step 450 and tripped at step 951.

## Deviations from Plan

1. **Launch path.** Task 3 originally named a direct `caffeinate` command.
   Under GAP-57-12 L1, generation-7 processes start through the detached
   launcher with the same trainer command, and the plan text was amended to say
   so before admission.
2. **Verify ladder.** Graded launches projected over 30 minutes need a fresh
   green `pinn.verify` marker for the current HEAD. The plan does not list it
   as a step. It ran once after the smoke, as generations 5 and 6 did.
3. **Terminal reason token.** The plan prose says `invariant-b-no-advance`;
   the verifier, builder, and README accept only `invariant_b_halt_no_advance`,
   which was used.
4. **Retention.** Retaining the generation-7 run bytes needed a new owner
   ruling (GAP-57-13, option A). It was not covered by the earlier
   generation-specific exceptions.

## Known Issues

- All 33 `tests/phase50` failures predate this plan. Those tests still point
  at `.planning/phases/50-valid-stage-0-re-run/evidence/`, which moved to
  `.planning/milestones/v2.2-phases/` in `12e16d7b`. 57-VALIDATION C13/C17 and
  57-06 Task 1's verify list include some of them.
- `.planning/STATE.md` was not updated by this plan; its last update is
  2026-09-08.

## Next Phase Readiness

57-06 Task 1 runs on the terminal branch: it writes `no-candidate.json` and
stops before Task 2. The held-out evaluation is never spent in Phase 57.

## Self-Check: PASSED

## Earlier attempt record (generation 3, 2026-09-27)

The text below is the summary previously committed for this plan in
`a43ff611`, retained verbatim as history. Its blocked status was superseded
by the generation-7 terminal closure above.

> # Phase 57 Plan 05: Run Window Summary
>
> The immutable run window was admitted at HEAD
> `ad96e6f46b5c7fd5ac7faa8b23c438974373dc38`. The exact seed-42 smoke command
> was launched with `--stage-0-only`, but the environment resolver failed before
> optimization with:
>
> > runtime resolve failed: The MPS backend is supported on macOS 14.0+. Current
> > OS version can be queried using `sw_vers`
>
> The attempt is recorded in `evidence/blocked-state-g3.json` and the generation
> 3 section of `evidence/run-ledger.md`. No graded seed, held-out split, or
> evaluation artifact was launched or created. The verifier returns nonzero for
> `run-window`, preserving the required incomplete disposition.
>
> ## Validation
>
> - `verify_phase57_evidence.py admit-run-window` — **ADMIT-RUN-WINDOW-OK** before launch.
> - `verify_phase57_evidence.py run-window` — **expected fail-closed** on the generation-3 operational block.
> - `python -m unittest tests.phase57.test_evidence_ledger_v2 -q` — **16/16 passed**.
> - `git diff --check` — **passed**.
>
> ## Next required action
>
> Resolve the MPS runtime/environment incompatibility or provide a supported
> execution environment. Any environment change requires a new admission check;
> the generation-3 run window cannot resume from this pre-optimization failure.
