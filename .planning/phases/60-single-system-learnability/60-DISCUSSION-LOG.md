# Phase 60: Single-System Learnability - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-10-18
**Phase:** 60-Single-System Learnability
**Areas discussed:** Learning-rate schedule, Self-halt, R_ref and GATE-04, Phase 59 verifier, Weights in git, Checkpoint ④ record

The option widget did not reach the user. They answered in prose and matched the six areas below. Neither pending todo was folded.

---

## Fold the todos

| Option | Description | Selected |
|--------|-------------|----------|
| Fold neither | D-06 and the r1 handoff stay outside Phase 60 | ✓ |
| Fold D-06 | Static-epsilon sensitivity check | |
| Fold the r1 handoff | trainex-r1 research handoff | |

**User's choice:** Fold neither.
**Notes:** D-06 is about stage labels and validation gates, which this phase does not set. The r1 handoff is finished and its todo is stale. Closing that todo is housekeeping outside this phase.

---

## Learning-rate schedule

| Option | Description | Selected |
|--------|-------------|----------|
| Stage-0 cosine for data-only arms; stage rate for probe physics; second cosine on extension | Hours become the cosine length; physics arms keep the ratified schedule | ✓ |
| Constant 1e-3 for data-only arms | The Phase 38 probe's rate | |
| Stage-0 rate on probe Rung 2b | Removes the carried-forward confound by changing the stage's rate | |

**User's choice:** The ratified schedule for physics arms. Cosine length is 3 hours divided by the timing-run seconds per step. An extension is one more cosine from the starting rate, keeping Adam's state, with no new ramp. Data-only arms use the Stage-0 cosine. Probe Rung 2b keeps the stage's rate, and the readout names the from-scratch confound.
**Notes:** The still-improving window then sits on the cosine's low-rate tail. The frozen test is not changed.

---

## Self-halt

| Option | Description | Selected |
|--------|-------------|----------|
| Never halt; log the frozen monitor on the budget-rule readings | The harness does not enter the production loop | ✓ |
| Apply invariant B | Halt when the causal front stalls for 500 steps, as generation 7 did | |

**User's choice:** Never halt. Log per-bin causal weights and the front at the scoring readings.
**Notes:** Phase 61 builds the log-only guard. A live 256-identity monitor is not added here. Generation 2's memory failure was the 4096-row batch, recorded in GAP-57-02.

---

## R_ref and GATE-04

| Option | Description | Selected |
|--------|-------------|----------|
| Re-measure and re-run GATE-04 on continue; reuse Stage-0 R_ref on the probes | Explicit call for the later-stage probes | ✓ |
| Re-measure R_ref for the probes | Treats the probes as a new stage reference | |
| Skip the continue-path re-measure | The spec's continue path did not name it | |

**User's choice:** On continue, re-measure `R_ref` and re-run GATE-04 at the approved setting before any physics arm. A fail goes to the owner. Probe physics arms reuse the Stage-0 reference.
**Notes:** Corrected during the reply: `R_ref` is ratified only for Stage 0, so the probe reuse is an explicit decision. GATE-04's pass rule was ratified in `57-RULING.md`, so the re-run is a clean pass or fail.

---

## Phase 59 verifier

| Option | Description | Selected |
|--------|-------------|----------|
| One successor hash named in a Phase 60 record | The verifier still checks every other producer | ✓ |
| Phase 59 verifies only at commit 45f65228 | Leaves the current tree's Phase 59 checks red | |

**User's choice:** One successor hash for `feasibility_scorer.py`, named in a committed Phase 60 record.
**Notes:** `verify_phase59_evidence.py` re-hashes every `producer_sha256` entry. Ten result files name the scorer.

---

## Weights in git

| Option | Description | Selected |
|--------|-------------|----------|
| Plain git for the two scored states; checkpoints and timing weights stay out | Re-score is the re-derive | ✓ |
| Git LFS | Keeps the objects out of the pack | |
| Do not commit weights | Contradicts the spec's re-derive rule | |

**User's choice:** Plain git, not LFS. Resume checkpoints stay out.
**Notes:** Corrected during the reply: about 45 MiB on the stop path and 106 MiB on the continue path, not 50–115. Each state is about 2.8 MiB.

---

## Checkpoint ④ record

| Option | Description | Selected |
|--------|-------------|----------|
| A committed ruling file quoting the owner's words and naming the value | Every continue-path arm cites it | ✓ |
| An override flag in the run config | A physics arm could not tell an approved value from a sweep override | |

**User's choice:** A committed ruling file, written only from the owner's words. Every continue-path arm record cites it. A physics arm refuses a setting that file does not name.

---

## Claude's Discretion

- Data term: every point of the assigned record, same set for the polish.
- Timing run: at least 50 steps, separate, never a result.
- Launch and resume: generation-7 safeguards, checkpoint on terminate, L-BFGS segment state required.
- Memory: ask the owner to close browsers; 6 GiB free. The footprint preflight is unreliable here.
- Module layout, INST-05 test shape, plan split, and Rung-1 order.

## Deferred Ideas

- Observe-only invariant B belongs to Phase 61.
- Close the stale trainex-r1 handoff todo outside this phase.
- D-06 softening check stays pending for later stage-label or gate work.
