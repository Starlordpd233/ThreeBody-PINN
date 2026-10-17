---
phase: 59-read-only-baseline-scorecard
plan: 07
subsystem: verification
tags: [diag07, jx-10, jx-1, gate-g1, generation-7, adam-preconditioned-share, gap-59-11]

requires:
  - phase: 59-read-only-baseline-scorecard
    provides: Frozen scorecard, allowlisted corpus doorway, and the evidence writer and independent verifier with the 6 GiB launch preflight
provides:
  - A unit-tested DIAG-07 driver (blob-checked generation-7 snapshot, retention-pinned checkpoint loads, refusing store, per-term gradients, Adam-preconditioned shares) with the JX-10 and JX-1 entry point
  - Committed JX-10 evidence: the frozen monitor reproduces the Phase 58 packet in 54 of 54 frozen checks, and the smoke front is 0 at steps 100, 200 and 300
  - Committed JX-1 evidence and the Gate G1 record: the physics share is 7.19e-07 at step 900 and 2.60e-08 at step 951, so Gate G1 did not fire (outcome proceed)
affects: [59-09, 59-10, 61]

actuals:
  tokens: 49465
  tasks: 3
  commits: 19
plan_head_before: 1b31079c188380528161a6ff41ddc4e05a815a72

tech-stack:
  added: []
  patterns:
    - "DIAG-07 loads generation 7 from a blob-checked git archive and the five Phase 59 overlays from the repository"
    - "A rounded 4-decimal packet field is compared in exact decimal units: abs(Decimal(repr(a)) - Decimal(repr(b))) <= Decimal(repr(1e-4))"
    - "Per-term gradients come from torch.autograd.grad, accumulated in float64 on the CPU, and are cross-checked against the trainer's own microbatched step before any share is computed"
    - "A tensor is moved to the CPU before it is widened to float64, because the MPS framework has no float64"

key-files:
  created:
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/diag07_common.py
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx01_jx10.py
    - tests/phase59/test_diag07.py
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx10.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx01.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/g1.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/files_opened_jx01_jx10.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/provenance_jx01_jx10.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx01_jx10.done.json
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/summary.md
    - .planning/phases/59-read-only-baseline-scorecard/evidence/diag07/MANIFEST.json
  modified: []

key-decisions:
  - "GAP-59-11 (owner option A) is applied exactly: phase58_packet_rounded_abs stays 1e-4 and a rounded field passes at one fourth-decimal step and fails at two. The raw_rbar_bin0 relative check, the exact front-index check and the cpu-versus-mps checks are unchanged."
  - "Gate G1 is recorded from the MPS primary physics shares, recomputed with the frozen g1_fires rule, and the CPU float64 outcome must be identical. A non-finite share would make it not determinable and stops the run as owner-routed."
  - "The driver's per-term vectors must match the trainer's own microbatched step within the frozen 1e-5 before a share is used. The worst relative difference was 1.58e-07 on MPS and 3.2e-14 on CPU float64."
  - "Adam betas and eps come from the run config and are checked equal to the checkpoint's param_group values, so the bias corrections cannot silently use different constants."
  - "In an all run a JX-10 failure stops the run before JX-1 starts. A failed run keeps its result files, writes no completion marker, records the failure and releases the launch lock."

patterns-established:
  - "DIAG07-TOLERANCE-FAIL exits 3, records the launch failure, releases the lock, writes no completion marker, and keeps the unaccepted result files untracked"
  - "A long run is launched only when vm_stat shows the 6 GiB bar plus a margin at that moment; the bar itself is never lowered"

requirements-completed: [DIAG-07]

coverage:
  - id: D1
    description: "Snapshot identity, retention-pinned checkpoint loads, refusing store, monitor-field formulas, launch lock, runtime pairs, and module provenance"
    requirement: DIAG-07
    verification:
      - kind: unit
        ref: "tests/phase59/test_diag07.py#SnapshotIdentityTests,RegistryTests,RunBookkeepingTests,RefusingStoreTests,MonitorFieldsTests,RuntimePairTests,ModuleProvenanceTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "The GAP-59-11 exact-decimal packet comparison, pinned on 2.0539 against 2.0538 (pass), 2.0540 against 2.0538 (fail), a pair with a binary gap of 9.999999999998899e-05 (pass), and a sweep over every packet value"
    requirement: DIAG-07
    verification:
      - kind: unit
        ref: "tests/phase59/test_diag07.py#PacketDecimalBoundaryTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "JX-1 library and flow: per-term gradients against the trainer, microbatch independence, IC split, Adam-preconditioned shares, optimizer-state flattening, cosine, MPS-safe flattening, and the driver flow on a tiny controller"
    requirement: DIAG-07
    verification:
      - kind: unit
        ref: "tests/phase59/test_diag07.py#ShareFormulaTests,FlattenTests,DecompositionTests,MicrobatchEquivalenceTests,IcSplitTests,CosineTests,Jx1FlowTests,Float64FlattenTests"
        status: pass
    human_judgment: false
  - id: D4
    description: "Committed JX-10 result: the frozen monitor reproduces the Phase 58 packet and the smoke front is 0 at steps 100, 200 and 300"
    requirement: DIAG-07
    verification:
      - kind: integration
        ref: "python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py diag07 --require jx01,jx10,g1 --require-committed"
        status: pass
    human_judgment: true
    rationale: "The reading is the pre-registered rule's output and the independent verifier checks hashes, identity and non-interference. Whether it answers the scientific question is the owner's reading in plan 59-10."
  - id: D5
    description: "Committed JX-1 result and the Gate G1 record (physics share 7.19e-07 at step 900 and 2.60e-08 at step 951, outcome proceed)"
    requirement: DIAG-07
    verification:
      - kind: integration
        ref: "python -B .planning/phases/59-read-only-baseline-scorecard/evidence/verify_phase59_evidence.py diag07 --require jx01,jx10,g1 --require-committed"
        status: pass
    human_judgment: true
    rationale: "The verifier recomputes g1_fires from the recorded shares. What the shares mean for the Phase 61 premise is the owner's reading in plan 59-10."

duration: 87min
completed: 2026-10-16
status: complete
---

# Phase 59 Plan 07: Read-Only Checkpoint Experiments Summary

**Gate G1 did not fire (outcome: proceed): generation 7's physics term supplied 7.19e-07 of the Adam-preconditioned update at step 900 and 2.60e-08 at step 951, and the JX-10 re-score reproduced the Phase 58 packet in 54 of 54 frozen checks, all on retained checkpoints with no training step and no test-split file opened**

## In plain language

Generation 7's saved checkpoints were re-examined without training them. First, re-running the run's own "is the front advancing" monitor on the saved checkpoints reproduced the numbers recorded in Phase 58, on the GPU (MPS) and on a CPU cross-check, and the smoke run's front stayed at 0 at steps 100, 200 and 300. Second, at steps 0, 900 and 951 we measured how hard each part of the loss pushed the network, and what share of the update Adam actually took came from the physics term. At steps 900 and 951 that share was about 7 parts in ten million and 3 parts in a hundred million, far below the 1% bar, so the reading "physics was a passenger" stands and Gate G1 did not fire. The plan for Phase 61 is not re-examined on this evidence, and Phase 59 itself was unaffected either way. The IC anchor term supplied almost all of the update. The earlier rounding-boundary halt is settled: the owner ruled that a one-step difference in the fourth decimal passes, and the rerun passed every check.

## Performance

- **Duration:** 87 min (42 min in the earlier sessions, 45 min in this resume)
- **Started:** 2026-10-14T04:10:27Z; resumed 2026-10-16T23:25:15Z
- **Completed:** 2026-10-17T00:12:00Z
- **Tasks:** 3 of 3
- **Files modified:** 11 (3 code and test files, 8 evidence files)
- **Long runs (all detached, one at a time, bar unchanged at 6442450944 bytes):**

| Run | Launched (UTC) | Exit | Elapsed | `ru_maxrss` | Note |
|---|---|---|---|---|---|
| JX-10 acceptance after GAP-59-11 | 2026-10-16T23:35:16Z | 0 | 110.6 s | 3.31 GiB | Task 1 gate; 54 of 54 checks |
| JX-1 development, attempt 1 | 2026-10-16T23:47:36Z | 1 | about 20 s | n/a | MPS float64 TypeError, fixed test-first |
| JX-1 development, attempt 2 | 2026-10-16T23:49:50Z | 0 | 285.5 s | 3.58 GiB | 56 of 56 checks |
| JX-10 development (GAP-59-12) | 2026-10-16T23:55:05Z | 0 | about 100 s | not retained | refreshes the producer hash |
| Committed run, `--experiment all` | 2026-10-17T00:00:12Z | 0 | 365.7 s | 3.58 GiB | the run whose files are committed |

- **Broad test run (retained, not repeated):** `unittest discover -s tests/phase59 -p 'test_*.py'` at the final code state, 204 tests OK in 147.4 s. An earlier 202-test run (199.5 s) predates the MPS fix and is superseded.

## Accomplishments

- The GAP-59-11 ruling is implemented test-first. Under the old float comparison 15 of the 90 one-step cases (5 checkpoints, 9 packet fields, 2 directions) would have failed, not only the one seen; under exact decimal units all 90 pass and every two-step case fails.
- Task 1 acceptance passed: JX-10 on MPS float32 and CPU float64, seed-42 fronts 0, 1, 2, 2, 2 and smoke fronts 0, 0, 0, CPU equal to MPS, 54 of 54 frozen checks. The largest unrounded gap to the packet is 6.66e-05 (bound 1e-4) and the largest `raw_rbar_bin0` relative gap is 1.22e-05 (bound 1e-4).
- JX-1 records, at steps 0, 900 and 951 on both runtimes, the five per-term gradient norms, the three cosines, the IC position and velocity split, and (900, 951) the primary and secondary Adam-preconditioned shares with the primary shares summing to 1 within 1e-6.
  - **Physics:** primary share 7.19e-07 (step 900) and 2.60e-08 (step 951); CPU float64 6.94e-07 and 2.59e-08. Both steps read "supports: physics was a passenger (PC-2)".
  - **IC anchor:** primary share 0.999996 and 0.999994. The data term supplied 3.27e-06 and 5.93e-06. Energy and angular momentum supplied 0, because Stage 0 sets their weights to 0.
  - **Gradient sizes at step 900 (raw norms):** IC 5.13e+07, physics 1.09e+02, data 1.51e+00.
- Gate G1: threshold 1e-2, fires False, outcome `proceed`, identical on CPU float64. The verifier recomputes it.
- The driver's vectors match the trainer's own `_run_adam_step_microbatched` norms at a worst relative difference of 1.58e-07 on MPS and 3.2e-14 on CPU float64, against the frozen 1e-5.
- Non-interference: no optimizer constructed, 0 checkpoint writes, parameters bitwise unchanged, every `.grad` None after each measurement, run-file hashes unchanged, test split 0 opened (4,142 train and 486 validation files opened through the allowlist). The normalizer was recovered from the checkpoint (residual 1.19e-07, no fallback).

## Task Commits

1. **Task 1: JX-10 tracer** - `16f5f0db` (test), `12c5420d` (feat), `a0fc5edf` (fix, CPU pair), `bf3b858b` (test, GAP-59-11), `a892fe9e` (fix, GAP-59-11). Acceptance run EXIT=0. Earlier halt records: `384c2112` (memory preflight), `579c8e0c` (packet boundary).
2. **Task 2: JX-1 and Gate G1** - `71650f83` (test, RED), `de4e12ba` (feat, GREEN), `af566bdf` (test, MPS regression), `936f7f56` (fix, MPS regression).
3. **Task 3: committed combined run** - `41dee29a` (evidence).

**Plan metadata:** the docs commit that carries this summary. In every cycle the failing-test commit precedes the commit that makes it pass. `commits: 19` in the frontmatter is the 18 measured with `git rev-list --count 1b31079c..HEAD` at write time plus the commit carrying this summary. Twelve of the 18 are this plan's; six are `2ff434d4` (the owner rulings record) and five 59-05 commits that landed in the range while this plan was halted.

## Files Created/Modified

- `.planning/phases/59-read-only-baseline-scorecard/evidence/diag07/diag07_common.py` - Snapshot bootstrap, registry load, refusing store, monitor fields, launch bookkeeping, and now per-term gradients, optimizer-state flattening, preconditioned shares, cosine, and MPS-safe flattening
- `.planning/phases/59-read-only-baseline-scorecard/evidence/diag07/jx01_jx10.py` - JX-10 and JX-1 entry point, the exact-decimal packet comparison, the trainer cross-check, the cpu-versus-mps checks, and the Gate G1 record
- `tests/phase59/test_diag07.py` - 42 tests for the driver, library, and flow
- `.planning/phases/59-read-only-baseline-scorecard/evidence/diag07/{jx10.json, jx01.json, g1.json, files_opened_jx01_jx10.json, provenance_jx01_jx10.json, jx01_jx10.done.json, summary.md, MANIFEST.json}` - the committed evidence from the one `--experiment all` run

## Decisions Made

See `key-decisions` above. Two more choices worth stating:

- `optimizer_constructed` in `non_interference` is true when no optimizer object exists, because the verifier treats that flag as a passed check. A reader should take `true` there to mean "the no-optimizer check passed".
- The diag07 `MANIFEST.json` committed here is the Plan-07 version (SHA-256 `a2e8d488296af0aecb3c01bd3ca9e8569ae07e717f1ea597b6190d70381311bb`). Plan 59-09 rewrites it when JX-2 to JX-5 land and records this hash as superseded.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] The CPU float64 cross-check built its controller with a pair that generation 7 refuses** (earlier session)
- **Found during:** Task 1 (acceptance run, first launch after the memory halt)
- **Issue:** `_run_jx10` built the CPU controller as `("float32", "cpu")`. Generation 7's `resolve_runtime` permits only `("float32", "mps")` and `("float64", "cpu")`.
- **Fix:** Build it as `("float64", "cpu")`; the existing demote, restore, promote step keeps the monitor hash on the raw float32 bytes.
- **Files modified:** `jx01_jx10.py`, `tests/phase59/test_diag07.py`
- **Verification:** The regression test failed first on the pair list, then passed.
- **Commit:** `a0fc5edf`

**2. [Rule 1 - Bug] The MPS framework cannot widen a tensor to float64 in one `.to` call**
- **Found during:** Task 2 (first JX-1 development run, EXIT=1 after about 20 s; failure recorded as run `8abdb838a16b4a83bbb811172ab319e8`, lock released)
- **Issue:** `_flat_float64` called `.to(device="cpu", dtype=torch.float64)` on an MPS gradient and raised `TypeError`. The CPU-only unit tests could not see it.
- **Fix:** Move to the CPU first, then widen. A `populated_gradient` helper replaces the inline flattening in the trainer cross-check so one safe path serves both. A scratch smoke of the JX-1 measurement on a tiny MPS float32 controller passed before the relaunch.
- **Files modified:** `diag07_common.py`, `jx01_jx10.py`, `tests/phase59/test_diag07.py`
- **Verification:** The new MPS regression test failed first with the exact TypeError message, then passed; 42 diag07 and static-guard tests pass; the relaunch ran to EXIT=0.
- **Commit:** `af566bdf` (test), `936f7f56` (fix)

**3. [Rule 2 - Missing critical] Driver-flow tests for the JX-1 measurement**
- **Found during:** Task 2
- **Issue:** The plan's behavior block tests the library functions, but the driver's JX-1 flow only runs inside a multi-minute detached run, where a defect costs a launch, a lock cycle, and memory headroom.
- **Fix:** Three tests run `_measure_jx1` on the tiny CPU controller with a synthetic payload (shares present, no moments, and the frozen cpu-versus-mps rules), and a cosine test covers the helper.
- **Files modified:** `tests/phase59/test_diag07.py`
- **Commit:** `de4e12ba` (added with the implementation, so these four tests did not have a separate failing commit)

### Owner ruling applied

**GAP-59-11 (option A)** changes how a frozen tolerance is read, so it is owner-routed and not a deviation. It was implemented as the ruling prescribes: failing tests first (`bf3b858b`), then `_compare_packet` changed at both rounded comparisons (`a892fe9e`). The verifier only reads `jx10.json` and does not recompute a packet comparison, so it was not changed. **GAP-59-12** was followed as ruled: the JX-1 development run, then the JX-10 development run, then the Task 2 verify.

### Differences from the plan text (not deviations)

- `files_opened_jx01_jx10.json` is written by `main` after the experiments, not inside `_run_jx10`, so one attestation covers whichever experiments run.
- The development runs used a snapshot in the session scratchpad; the committed run used a `mktemp -d` snapshot, so the recorded command carries an anonymous path.

---

**Total deviations:** 3 auto-fixed (2 Rule 1 bugs, 1 Rule 2 coverage addition), plus 1 owner ruling applied.
**Impact on plan:** No frozen value, tolerance, or scorecard byte changed. The bugs were in this plan's own driver and surfaced only on the first real runs.

## Issues Encountered

- **Memory headroom was marginal.** At the start of this resume `vm_stat` showed 4.2 to 6.4 GB available against the 6.44 GB bar for about nine minutes. The run was launched only when it read 7.99 GB (about five minutes after the watcher started). There was no preflight refusal, and the bar was not lowered. Later long steps (the survey and JX-2 to JX-5) may meet the same headroom.
- **`git_head` is null in `provenance_jx01_jx10.json`.** The overlay's `pinn.verify.git_head` runs inside the generation-7 snapshot directory, which is not a repository. The code identity is carried by `code_identity` (commit and snapshot digest), `producer_sha256`, and the evidence commit's ancestry, which `--require-committed` checks. The record also shows `worktree_dirty: true` from the owner's uncommitted files. The overlay module was not edited.
- **The ROADMAP helper reformatted unrelated lines.** `roadmap update-plan-progress` inserted blank lines across the file and wrote a malformed table cell, so ROADMAP.md was restored and the three needed lines (plan count, checkbox, progress row) were edited by hand.
- **Informational, not interpreted here.** The secondary IC share is negative (-0.09 and -0.18): the stored momentum direction opposes the IC gradient at both checkpoints. The IC anchor's gradient is five orders of magnitude larger than the physics gradient. Plan 59-10 reads these.

## Authentication Gates

None.

## Known Stubs

None.

## Threat Flags

None. No new network endpoint, auth path, or file-access pattern. Every checkpoint load is SHA-256-checked against `generation-7-retention.json` and uses `weights_only=True`.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Wave 4 (59-06, 59-08, 59-09) is unblocked. The launch lock is free and no development marker remains in `evidence/diag07/`.
- Plan 59-09 owns the next diag07 manifest. It must record `a2e8d488296af0aecb3c01bd3ca9e8569ae07e717f1ea597b6190d70381311bb` as the superseded Plan-07 manifest and re-run the producer-hash check, because it reuses `diag07_common.py`.
- DIAG-07 stays pending in `REQUIREMENTS.md`: Plans 59-01, 59-03, 59-04, 59-06, 59-09, and 59-10 also declare it (`requirements.ready-ids` reports 0 of 1 ready).
- Gate G1 outcome `proceed` is the value plan 59-10 carries into the findings. Nothing here changes Phase 61's premise.

## Self-Check: PASSED

Every file and commit named in this summary exists: the three code and test files, the eight evidence files, and commits `16f5f0db`, `12c5420d`, `384c2112`, `a0fc5edf`, `579c8e0c`, `bf3b858b`, `a892fe9e`, `71650f83`, `de4e12ba`, `af566bdf`, `936f7f56`, and `41dee29a`. After the evidence commit, `verify_phase59_evidence.py diag07 --require jx01,jx10,g1 --require-committed` printed DIAG07-OK, `guardrails` printed GUARDRAILS-OK, and `scorecard-frozen` printed SCORECARD-FROZEN-OK. The task acceptance criteria all hold.

---
*Phase: 59-read-only-baseline-scorecard*
*Completed: 2026-10-16*
