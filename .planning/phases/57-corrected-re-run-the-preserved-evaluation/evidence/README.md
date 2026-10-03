# Phase 57 Evidence Contract

This directory is the append-only evidence surface for RUN-04, RUN-05, and
EVAL-02.  The fresh GATE-04 raw record and the independent production
conformance record are committed before any expensive run window.  Run
outputs may be added later, but the fingerprinted source/config/test/plan
inputs must not be changed between the smoke and graded band.

## Required records

- `gate04/<UTC>/raw.json` — one fresh six-case GATE-04 invocation.  The
  governed `pinn/verification/artifacts/r_ref_stage0.json` records this exact
  path and SHA-256 digest and is valid only for a complete `PASS` with empty
  blocking and unratified arrays.
- `production-conformance.json` — independent CPU proof of the public
  `FixedBatch`/`RunController`/loss/checkpoint seams, bound to the Gate raw
  digest and final `R_ref` digest.  It is dataset-free and held-out-free.
- `run-ledger.md` — append-only smoke/band history. Each attempted run has
  one record with an `invocations[]` entry for every process; a continuation
  stays in that run record, while a new attempt gets a new record.
- `generation-2-retention.json` — all 16 preserved files from the interrupted
  historical smoke, with byte sizes and SHA-256 digests.
- `generation-5-retention.json` — the 23 completed generation-5 smoke files
  retained in place and committed byte-identical snapshots of its timing
  calibration and verify marker, with byte sizes and SHA-256 digests for all
  25 files. Verify these retained bytes before generation-7 admission.
- `generation-6-retention.json` — the 23 generation-6 smoke files, the 24
  files of the lost graded seed 42, and byte-identical snapshots of the
  generation-6 timing calibration and verify marker: 49 files with byte sizes
  and SHA-256 digests (GAP-57-12 R1). `blocked-state-g6.json` records the
  process loss. Verify both before generation-7 admission.
- `launch_phase57_run.py` — the GAP-57-12 L1 detached launcher every
  generation-7 process starts through (see the invocation contract below).
- `source-manifest.json`, `band-record.md`, and `candidate-receipt.json` —
  normal-mode artifacts built only after a complete three-seed band.
- `terminal-state.json` or `blocked-state-g7.json` — mutually exclusive
  generation-7 outcome records.  Only `gate04_block` and
  `invariant_b_halt_no_advance` may be terminal; resource, guard, and
  operational failures remain incomplete.  The historical generation-1
  `blocked-state.json` and the generation-3, generation-4, and generation-6
  blocked states are retained at their original paths and must not be
  overwritten.

## Verification commands

Run from the repository root under the `pinn-train` environment:

```text
python .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/verify_phase57_evidence.py admit-run-window
python .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/verify_phase57_evidence.py seed42-setup
python .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/verify_phase57_evidence.py run-window
python .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/verify_phase57_evidence.py candidate
python .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/verify_phase57_evidence.py pre-evaluation
python .planning/phases/57-corrected-re-run-the-preserved-evaluation/evidence/verify_phase57_evidence.py final
```

`admit-run-window` is expected to pass before the operator authorizes the
fresh generation-7 smoke and fixes the immutable run-window HEAD.
`seed42-setup` compares the actual generation-7 smoke and graded seed-42
`splits.json` bytes and exact `s_h`/`n_train` as soon as the graded setup
artifacts exist; seeds 41 and 43 cannot launch before it passes. The
evaluation candidate order remains `42`, `41`, `43`. The later commands fail
closed until their corresponding run or evaluation artifacts exist. They
never launch training or materialize a held-out split.

## Selection and frame rules

Candidate selection recomputes only the four Phase-50 structural facts:
`eval01_precondition_i`, `guard_invariant_rule`, `finished`, and
`eval01_precondition_iii`, in the fixed order `42`, `41`, `43`.  Loss, SCS,
front trajectories, and other scientific values are descriptive only and
cannot trigger fallback.

The evaluator boundary is canonical-only: predicted `r_prime`, normalized
time `u_t_over_T`, and ordered raw masses.  The pre-access assertion must run
before any test-split object is constructed.  The attempt/receipt marker is
single-use; once claimed, no retry or fallback is legal.

## Version-2 invocation contract

GAP-57-04 option B makes process provenance explicit in the version-2 run
ledger. For an admitted generation-7 run, the first invocation is `fresh`. Each
later invocation is `resume`,
uses `--stage-0-only --resume latest`, and references the prior process's
SHA-256-pinned boundary checkpoint. The independent verifier loads that
checkpoint with `weights_only=True` and requires `invariant_b_state`. Each
invocation records its own command, PID, start/end times, exit status, Git
HEAD, and source-config digest. All processes in one run share the same HEAD
and config identity. An interrupted process can be followed by a resume only
when its boundary checkpoint is present and valid.

GAP-57-12 option L1 adds one rule for generation 7. Every process starts
through `launch_phase57_run.py --run-name <run> [--resume]`. The launcher
starts a supervisor in its own session, which runs the unchanged
`/usr/bin/caffeinate -is <pinned python> -m pinn.train --config
configs/<run>.yaml --stage-0-only` command, so a closing terminal or agent
session cannot kill the trainer. The supervisor writes
`runs/.launch/<run>/invocation-<n>/` with `launch.json`, `process.json`,
`output.log` (all trainer output), `exit.json` (exit code or signal), and
`supervisor.err`. Each generation-7 invocation entry copies its PID,
start/end time, exit code, and wall time from those files. It also carries a
`launch` object with mode `detached-session`, that directory, and the SHA-256
of `launch.json`, `process.json`, `output.log`, and `exit.json`; `run-window`
rejects an invocation whose files or values disagree. A deliberate stop still
signals the trainer PID recorded in `process.json`.

Generation 1 is the preserved blocked smoke. Generation 2 is the retained,
operator-reported deliberate stop from 2026-09-13; its original command, exit
code, Git HEAD, and exact launch kind are not independently recorded and remain
null. It is
historical and incomplete, not a calibration for the next band. Generation 3
is the preserved sandbox-blocked retry attempt. Generation 4 is the preserved
operator-stop attempt without a resumable boundary checkpoint. Generation 5
is the completed host-level smoke at `stage0-v23g5-smoke`; its 23 run files
and two governed singleton snapshots remain historical under
`generation-5-retention.json`. Generation 6 is the preserved attempt whose
graded seed 42 was lost at step 513 with no boundary checkpoint and no
retained stderr; its smoke, lost run, and snapshots remain historical under
`generation-6-retention.json` and `blocked-state-g6.json`. Generation 7 uses
fresh `stage0-v23g7-{smoke,seed41,seed42,seed43}` names and is the active
band. A generation-7 operational block is written to `blocked-state-g7.json`;
the generation-1, generation-3, generation-4, and generation-6 blocked-state
paths and digests remain historical. Earlier generations remain in the append-only
ledger and their run artifacts must not be moved or overwritten.

The generation-7 launch must run with host-level Metal access; the launcher
refuses to start when the pinned interpreter cannot see the Metal device. A sandboxed
process can report `torch.backends.mps.is_available() == False` and expose zero
Metal devices even when the host-level process reports one available device.
