---
phase: 60-single-system-learnability
plan: 21
subsystem: verification
tags: [hard-stage-probes, feas-09, ladder, branch-not-taken, stopped-at-g2, no-rescue, tracer, read-only]

requires:
  - phase: 60-single-system-learnability
    provides: "60-18 (the stop path: skip-records.json recording FEAS-04 and FEAS-09 as skipped with the reason no rescue, and stop-handoff.json with verdict RETHINK-REPRESENTATION); 60-20 (the Rung 2 branch not taken, so no Rung-2 records exist); the learnability_g2 branch query"
provides:
  - "The branch record for the hard-stage probes: learnability_g2 branch ladder printed BRANCH-NOT-TAKEN (exit 0), so no probe sequence was chosen, admitted or launched, no owner checkpoint was presented, no probe arm directory exists, and this plan wrote no skip record or evidence file"
affects: ["60-22 (depends on 60-18 and 60-21; closes Phase 60)"]

branch: not-taken
branch_query: "BRANCH-NOT-TAKEN: ladder (the ladder stopped at G2: no rescue)"
branch_query_exit_code: 0
recorded_outcome: no_rescue
g2_outcome_sha256: 3e71568fe6d243f16dc930c7b8d49d028967b625e134cf5ba52d4c48b579c529
sweep_curve_sha256: 946c0bb9a658f287f074c8768c4cd4a54333df9c7303445fd5d64a5a347706bc
skip_records_sha256: e15ad37d95e452637014f18c0eeb5d1795589717b6b82af14691bc3edd580bf8
stop_handoff_sha256: 7ed8223c066e62bd55e527dc703565367a0f9764a253e086a3bc0b4e719d02d5
sweep_system: 1632
sweep_tiers: [0, 0, 0, 0]
rung1_tiers: [0, 0, 0]
rung2_records_committed: false
sequence_chosen: null
arms_launched: []
owner_checkpoint_presented: false
handoff_verdict: RETHINK-REPRESENTATION

owner_reply_verbatim:
  go_ahead_waves_16_to_22_2026_10_23: "okay let's run this until phase 60 is closed."

actuals:
  tokens: 0   # chars/4 over the realized diff, excluding this SUMMARY: no other file changed. The plan's 55000 estimate covers the taken branch (about 15 hours of probes and their evidence commit), which did not happen
  tasks: 1    # Task 1 only; Tasks 2 to 4 are not executed on the not-taken branch
  commits: 0  # measured at write time with git rev-list --count fb36ee4b..HEAD; this SUMMARY's own commit is not counted, as in 60-15 to 60-20; a docs-only plan, so 0 is legitimate
  plan_head_before: fb36ee4bead45f4566d790b824e1d85d0b3126d5

tech-stack:
  added: []
  patterns:
    - "Conditional branch plan ending cleanly: a read-only branch query first, then a one-file 'branch not taken' SUMMARY with status complete, so the plan index counts the wave done and the dependent waves proceed"
    - "Re-run the branch query and re-read the committed records before writing a not-taken record; the orchestrator's numbers are checked against the files, not taken on trust"

key-files:
  created:
    - .planning/phases/60-single-system-learnability/60-21-SUMMARY.md
  modified: []

key-decisions:
  - "Branch not taken: the query printed BRANCH-NOT-TAKEN with exit 0, so the plan ends after Task 1; Tasks 2 to 4 are not executed, no arm launches and no skip record is written (the stop path's records come from Plan 60-18)"
  - "status is complete, not halted: the plan's branch rule is a clean ending, and Plan 60-22 depends on this plan (halted would report it as blocked)"
  - "requirements-completed is empty: FEAS-09's skip clause was recorded by Plan 60-18, and this plan adds no claim"

patterns-established:
  - "Not-taken record: the branch query line and exit code, the recorded outcome re-derived from the committed blobs, a statement that nothing was asked or launched, and the deviations"

requirements-completed: []

coverage:
  - id: D1
    description: "The branch rule applied: learnability_g2 branch ladder was re-run by this executor and printed BRANCH-NOT-TAKEN (exit 0, empty stderr), so the plan ends after Task 1"
    verification:
      - kind: other
        ref: "<home>/miniforge3/envs/pinn-train/bin/python -B -m pinn.verification.learnability_g2 branch ladder (stdout: BRANCH-NOT-TAKEN: ladder (the ladder stopped at G2: no rescue); exit 0)"
        status: pass
    human_judgment: false
  - id: D2
    description: "The recorded outcome behind the branch, read from the committed g2 files: Rung 1 at Tier 0 on all three systems, no_rescue on the sweep, the skip records (FEAS-04 and FEAS-09 skipped, reason no rescue) and the Phase 64 handoff (RETHINK-REPRESENTATION), with fingerprints equal to those recorded in the 60-18 SUMMARY"
    verification:
      - kind: other
        ref: "verify_phase60_evidence.py g2 --require outcome,skip-records,stop-handoff prints G2-OK (exit 0); an independent read of the HEAD blobs with python -I (scratch script outside the repository) matched all four fingerprints and every cited record hash, problems: none"
        status: pass
    human_judgment: false
  - id: D3
    description: "Nothing asked, launched or stray-written: no probe sequence chosen, no p1, p2b, c-p1 or c-p2b arm directory, no Rung-2 record, no probes or continue-probes launch directory, no skip record written by this plan, no Phase 60 process running, and the working tree equal to the baseline taken at the start"
    verification:
      - kind: other
        ref: "the same python -I script (git ls-files on evidence/arms, listings of evidence/arms, runs/phase60 and runs/.launch/phase60, a ps filter); git status --short --branch diffed against the baseline (identical)"
        status: pass
    human_judgment: false
  - id: D4
    description: "The owner's go-ahead for waves 16 to 22, and what skipped probes mean for the project"
    verification: []
    human_judgment: true
    rationale: "The go-ahead is an owner decision recorded verbatim, and what the skipped ladder implies belongs to the owner and the Phase 64 verdict stage; this plan reports only the pre-registered branch"

duration: 2min   # calendar time, about: started 16:05:22 CDT (ledger created), committed within about two minutes
completed: 2026-10-23
status: complete
---

# Phase 60 Plan 21: The Two Hard-Stage Probes (Branch Not Taken) Summary

**branch not taken: no_rescue, the ladder stopped at Gate G2 (the sweep recorded all four first_omega_0 settings, 60, 120, 240 and 480 on system 1632, at Tier 0), so the two hard-stage probes do not run; no sequence was chosen, the owner was not asked to free the machine, and nothing was launched or trained.**

In plain language: the probes are an early look at whether the harder curriculum stages are reachable at all, using one representative system from each: system 2279 (Stage 4b) and system 3418 (Stage 6). Each gets a data-only arm and a full-recipe arm, four experiments in all, about 15 hours of machine time. Their results would inform the final verdict and would not gate it. They only make sense once the ladder has gone past Gate G2 and Rung 2 has produced committed records. Neither is true: Rung 1 failed on all three panel orbits (Tier 0), the sweep found no setting that got within the 10% that Tier 1 allows, the ladder stopped at G2, Plan 60-20 recorded that Rung 2 did not run, and Plan 60-18 recorded the probes (FEAS-09) as skipped with the reason "no rescue". So the ladder query says the branch is not taken, and the plan's own rule is to say so, commit this record and stop. This plan writes no skip record of its own; those came from Plan 60-18.

## Performance

- **Duration:** about 2 min of calendar time.
- **Plan started:** 2026-10-23T21:05:22Z (16:05:22 CDT, when the commit ledger was created); **branch query run:** 16:05:27 CDT; **pre-write check:** 16:05:39 CDT
- **Tasks:** 1 of 4 executed (Task 1, the tracer); Tasks 2 to 4 are not executed by the plan's branch rule
- **Files committed:** 1 (this SUMMARY)

## Accomplishments

- **The branch rule was applied from a fresh query, not from the report.** `learnability_g2 branch ladder` was re-run by this executor and printed `BRANCH-NOT-TAKEN` with exit 0.
- **The recorded outcome was re-derived from the committed files.** The four g2 files were read from their HEAD blobs, matched against the fingerprints in the 60-18 SUMMARY, and accepted by the evidence verifier (`G2-OK`).
- **Nothing was asked, launched or written beyond this record.** No sequence was chosen, no owner checkpoint was presented, no probe arm or launch directory exists, and the working tree equals the baseline taken at the start.

## Branch query

Run by this executor on 2026-10-23 at 16:05:27 CDT (HEAD `fb36ee4b`), from the project root, with the stdout, stderr, exit code and time retained in the session scratchpad outside the repository:

```
<home>/miniforge3/envs/pinn-train/bin/python -B -m pinn.verification.learnability_g2 branch ladder
BRANCH-NOT-TAKEN: ladder (the ladder stopped at G2: no rescue)
```

Exit code 0, stderr empty, 1.192 s. The orchestrator reported the same line when it dispatched this plan. The task's verify fails only on a non-zero exit or on output starting with BRANCH-PENDING or G2-HALT, so it passes.

## The recorded outcome (read from the committed files)

Read from the HEAD blobs. E is the worst position error, relative (0.1 is 10%); Tier 1 needs E at most 0.1.

- `evidence/g2/g2-outcome.json`: `g2_fired` true; Rung 1 at the locked first_omega_0 30.0 is Tier 0 on systems 1632, 851 and 4658 (E 1.1574, 1.2375, 1.1432).
- `evidence/g2/sweep-curve.json`: outcome `no_rescue`, `confirmation_arm` and `confirmed_first_omega_0` null; first_omega_0 60 (E 1.1569), 120 (1.1561), 240 (1.1539) and 480 (1.1575) on system 1632, all Tier 0, every row labelled "below Tier 1".
- `evidence/g2/skip-records.json`: FEAS-04 and FEAS-09 skipped with the reason `no rescue`; Level 3 "not tested (skipped at G2)".
- `evidence/g2/stop-handoff.json`: stop reason `no rescue`; verdict RETHINK-REPRESENTATION; Phases 61-63 "skipped at G2, not failed"; next phase 64; seven arms, 22.378 machine hours.
- Absent, as expected on this path: any Rung-2 or probe arm directory (`r2a`, `r2b`, `p1`, `p2b` or `c-`, tracked, on disk or under `runs/phase60`), any `probes` or `continue-probes` launch directory (`runs/.launch/phase60` holds `rung1` and `sweep-1632` only), `evidence/continue/`, `rescue.json` and `owner-stop.json`. Plan 60-20's SUMMARY is a not-taken record, so no Rung-2 records exist. The preflight's four probe keys were not read: on a skip path the files are not required.

These are measured facts only; what skipped probes imply for the project is for Phase 64 and the owner.

## What was and was not done

| Task | Type | Outcome |
|---|---|---|
| 1. Confirm the ladder branch and the committed Rung-2 records, then admit the probes, or record that this branch is not taken | tracer | Done: the branch query printed BRANCH-NOT-TAKEN, and this record was written |
| 2. Owner: free the machine for the probes (about 15-30 hours) | checkpoint:human-action, gate blocking-human | Not executed: presented only on BRANCH-TAKEN; the owner was not asked |
| 3. Launch the probe sequence detached | auto | Not executed: no sequence was chosen and no arm was launched |
| 4. Wait for the probe sequence to end, then verify and commit the four probe records | auto | Not executed: there is no run to wait for, and its precondition is never evaluated because the plan ends before this task |

## The owner's go-ahead (verbatim)

As relayed by the orchestrator in this plan's dispatch (2026-10-23, about 11:00 CDT), the owner's go-ahead for waves 16 to 22 reads:

> okay let's run this until phase 60 is closed.

It names no wave, so it is taken as covering this one. It is not a reply to Task 2's "ready" checkpoint: that checkpoint is `gate="blocking-human"`, is presented only on BRANCH-TAKEN, and was not presented. This plan asks the owner nothing on its not-taken branch.

## Task Commits

1. **Task 1 (tracer): confirm the ladder branch and the committed Rung-2 records, then admit the probes, or record that this branch is not taken** - no code or evidence commit, by design: the task is read-only. The only commit of this plan is the one that adds this file.

**Plan metadata:** the `docs(60-21)` commit that adds this file (`docs(60-21): record that the probe branch is not taken`), made with `scripts/agent-commit` under `GIT_AGENT_ID=gsd-executor-60-21` and `GIT_AGENT_OWNED_PATHS` set to this file alone, as the plan's output section prescribes for the not-taken branch.

## Files Created/Modified

- `.planning/phases/60-single-system-learnability/60-21-SUMMARY.md` - this record. No evidence file, weights file, launch file, code file, STATE.md, ROADMAP.md or REQUIREMENTS.md was created or changed by this plan; the orchestrator updates the last three by hand.

## Decisions Made

- The plan ends after Task 1 because the branch query printed BRANCH-NOT-TAKEN; Tasks 2 to 4 are not executed, no arm launches, and no skip record is written.
- `status: complete`, not `halted`. A halted plan makes every plan that depends on it report as blocked, and Plan 60-22 (which closes the phase) depends on this plan. The branch itself is marked by the `branch: not-taken` field and by the first words of the result statement.
- `requirements-completed` is empty. FEAS-09's skip clause was recorded by Plan 60-18, and this plan adds no claim. FEAS-09 is also declared by Plan 60-22, which has no SUMMARY yet.

## Deviations from Plan

### Branch rule (by design)

**1. [Branch rule] Task 1 only; Tasks 2 to 4 not executed.**
- **Found during:** Task 1.
- **Issue:** The branch query printed BRANCH-NOT-TAKEN, so the plan's own rule ends it after the SUMMARY.
- **Action:** Wrote and committed this record; asked the owner nothing, launched nothing, wrote no skip record, because the stop path's records come from Plan 60-18.

### Owner go-ahead

**2. [Owner go-ahead] The go-ahead covered waves 16 to 22 in one sentence rather than naming this wave.** It was relayed by the orchestrator and is recorded verbatim above. No wave-specific reply was needed, because the plan asks the owner nothing on this branch.

### Process

**3. [Process] The Co-Authored-By trailer names Claude Sonnet 5.5**, the model that did this work, in place of the plan's Opus 5.5, as in earlier waves.

**4. [Process] This plan ran in the same executor session as the other two branch-not-taken plans (60-19, 60-20 and 60-21), not in its own.** One session, three records, one commit each, in wave order.

**5. [Process] The plan's execution_context names `~/.claude-max/gsd-core/...`; the active profile's `~/.claude-alt/gsd-core/...` copies were read instead,** as the orchestrator directed.

**6. [Process] The generic agent-branch allow-list was not applied.** The executor's pre-commit check that HEAD sits on an `agent-*` branch assumes a per-agent worktree. This plan ran sequentially on the milestone worktree's own branch (`milestone/v2.4`), as every earlier wave did. The checks that do apply passed before writing and are repeated in the commit step: HEAD attached, not a protected branch by the GSD query (`protected=false`), and no cwd drift from the spawn-time toplevel.

**7. [Process] CLAUDE.md's Sequentialthinking directive was not followed.** The orchestrator reserved that tool for itself and it is not among the tools this executor was given, so the steps (one query, one record, one commit) were planned by hand.

**8. [Process] The tracer feedback gate did not come into play.** Task 1 is a tracer, and its gate guards the expansion tasks. The branch rule excludes them, so none ran, and the task's verify, the branch query, ran once and passed.

**9. [Process] The commit ledger and the layout of the measured keys.** The ledger `gsd-plan-head-before-60-21` was created before the first command and holds `fb36ee4b`, the commit that added the 60-20 SUMMARY. `commits: 0` is measured at write time and does not count this SUMMARY's own commit, as in 60-15 to 60-20. The keys sit nested under `actuals`, as in 60-14 to 60-20.

**10. [Process] The executor's start-up init and state queries were not run.** `init.execute-phase` and `state.load` were skipped: the dispatch supplied the project root, branch, HEAD, plan and phase directory, and barred gsd-tools state verbs. The only gsd-tools call was the read-only `git.base-branch --is-protected` query for the pre-commit check.

---

**Total deviations:** 0 auto-fixed; 1 branch-rule ending (by design), 1 owner go-ahead wording, 8 process notes.
**Impact on plan:** None on the result. The branch was decided by the plan's own query and rule, and no recorded number was changed.

## Issues Encountered

None.

## Verification Results

Each command ran in under two seconds, so none counts as expensive. Their stdout, stderr, exit codes and timings are retained outside the repository, one set per command, in `/private/tmp/claude-501/-Users-<user>-Desktop-3-body-problem--worktrees-trainex/3ea947f8-ffa4-48cb-882d-e3390266a246/scratchpad/w19/` (files `p21-*`).

| Command (local time, 2026-10-23, CDT) | Result |
|---|---|
| `python -B -m pinn.verification.learnability_g2 branch ladder` (16:05:27) | `BRANCH-NOT-TAKEN: ladder (the ladder stopped at G2: no rescue)`, exit 0, stderr empty, 1.192 s |
| `python -B .planning/phases/60-single-system-learnability/evidence/verify_phase60_evidence.py g2 --require outcome,skip-records,stop-handoff` (16:05:29; read-only) | `G2-OK`, exit 0, 0.581 s |
| Independent read of the HEAD blobs (`python -I`, scratch script outside the repository) and its absence checks | all four SHA-256 values equal those in the 60-18 SUMMARY; every cited record hash equals its blob; verdict, hours and arm count as quoted above; no later-rung or probe arm directory, no launch directory for a later rung, no ruling file, no `evidence/continue/`, no `rescue.json` or `owner-stop.json`; no Phase 60 process running; problems: none (0.288 s) |
| `git status --short --branch` against the baseline taken at the start | identical (the owner's own entries only; nothing staged) |
| `git rev-list --count fb36ee4b..HEAD` at write time (16:05:39) | 0 |

## Threat model check

- T-60-16 (probe admission): mitigated by construction. No probe was admitted: the branch query ran first and printed BRANCH-NOT-TAKEN, and no probe arm, sequence or launch directory exists.
- T-60-01 (standard-variant reads): not reached. No record was trained or read for the probes.
- T-60-09 (memory): not reached. Nothing was launched, so no memory confirmation was needed.
- T-60-SC (package installs): none; this plan installed nothing.

## Known Stubs

None. This plan wrote one record and no code. Tasks 2 to 4 were not run because the branch rule excludes them, so their verify commands are not unrun verifies and are not entered in the broken-windows ledger.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Plan 60-22 (wave 22) is next and closes Phase 60.** It depends on 60-18 and 60-21 and declares INST-05, FEAS-03, FEAS-04 and FEAS-09: the end-to-end evidence checks, re-scoring from the committed weights, and the findings.
- **Phase 64 follows Phase 60's close** and reads `evidence/g2/stop-handoff.json`: the verdict, Level 3 "not tested (skipped at G2)", and the seven arms' hours.
- No Phase 60 tooling process was running at 16:05 CDT. STATE.md, ROADMAP.md and REQUIREMENTS.md are not touched here; the orchestrator updates them by hand.

## Fingerprints

- `g2-outcome.json`: `3e71568fe6d243f16dc930c7b8d49d028967b625e134cf5ba52d4c48b579c529`
- `sweep-curve.json`: `946c0bb9a658f287f074c8768c4cd4a54333df9c7303445fd5d64a5a347706bc`
- `skip-records.json`: `e15ad37d95e452637014f18c0eeb5d1795589717b6b82af14691bc3edd580bf8`
- `stop-handoff.json`: `7ed8223c066e62bd55e527dc703565367a0f9764a253e086a3bc0b4e719d02d5`

---
*Phase: 60-single-system-learnability*
*Completed: 2026-10-23*

## Self-Check: PASSED

Checked before this file was written:

- All four g2 files exist, are tracked and unmodified at HEAD, and match the fingerprints recorded in the 60-18 SUMMARY; the quoted numbers were derived by script from the HEAD blobs. The 60-19 and 60-20 SUMMARYs are tracked and clean.
- No probe or Rung-2 arm directory, launch directory, ruling file, `evidence/continue/`, `rescue.json` or `owner-stop.json` exists.
- `git rev-list --count fb36ee4b..HEAD` was 0 when the frontmatter was written, nothing was staged, and the working tree equalled the baseline.
- The lines added are this record only; the commit step greps it for stub patterns before staging.

Checks that can only run once this file is committed (the commit holds this file alone, and the working tree is unchanged from the baseline) are reported in the executor's return message.
