---
phase: 59
phase_name: "Read-Only Baseline & Scorecard"
project: "Three-Body Physics-Informed LLM"
generated: "2026-10-26"
counts:
  decisions: 8
  lessons: 7
  patterns: 7
  surprises: 6
missing_artifacts:
  - "59-UAT.md"
---

# Phase 59 Learnings: Read-Only Baseline & Scorecard

Phase 59 froze the feasibility scorecard and built everything the v2.4 ladder is read against, without training a step: the FEAS-01 scorer, one allowlisted reader, the Stage-0 census and panels, the whole-dataset survey, the two comparison points (the two-Kepler formula and a nearest-neighbour copy) and the DIAG-07 read-only experiments on generation 7's checkpoints, ending at Gate G1 (proceed). Extracted from 59-01..59-10 PLAN/SUMMARY, 59-VERIFICATION.md and the v2.4 gap index. No UAT file exists for this phase; its verification was written by the executing agent, not an independent gsd-verifier pass.

## Decisions

### Freeze the ruler before any result exists
The scorecard is a canonical JSON loaded by a strict SHA-256 loader into read-only mappings, committed as a tracer so `phase_start_head` is the commit before the first Phase 59 execution commit. The evidence verifier proves the scorecard was frozen before any result, and recomputes Gate G1 from the frozen rule.

**Rationale:** pre-registration (SCOPE-42) is only checkable if the freeze point is a commit that precedes every result.
**Source:** 59-01-SUMMARY.md, 59-04-SUMMARY.md

### An undeterminable number is owner-routed, never invented
When an arm's improvement rate has no finite reference-window reading, `budget_outcome` raises `OwnerRouted` instead of dividing by a missing reference.

**Rationale:** a guessed rate would silently decide an extension the pre-registered rule cannot decide.
**Source:** 59-01-SUMMARY.md

### The scorecard's ε_H never uses finite differences
`score_trajectory` accepts only autograd (network), analytic (formula) and Brutus (copy) velocities; the finite-difference ε_H survives only as the labelled context column `fd_context_eps_h` (GAP-59-02).

**Rationale:** the finite-difference gate cannot score even an exact answer well (GAP-59-08), so it cannot be the scorecard's energy measure.
**Source:** 59-02-SUMMARY.md, .planning/milestones/v2.4-GAPS.md (GAP-59-02)

### GAP-59-10: record the deviation, keep the frozen value
The reader's monitor IC13 residual (2⁻²³ ≈ 1.19e-07) exceeded the frozen 1e-7. The owner ruled option A: keep the frozen value, record `passed: false` beside an `owner_accepted_deviation` block, and accept exactly 2⁻²³. The ceiling lives as a constant in the verifier, so an edited record cannot raise it, and the deviation applies only while the frozen value and the checkpoint-recovered normalizer are unchanged.

**Rationale:** a frozen tolerance moves only by owner ruling, and the ruling must not widen into a general allowance.
**Source:** 59-05-SUMMARY.md

### GAP-59-13: leave the pinned scorer byte-unchanged and work around it
The scorer's `network_trajectory` crashed on MPS. Because the committed Plan-07 evidence pins the scorer's SHA-256, the scorer was left untouched; JX-4 scores through a line-for-line copy that moves to the CPU before widening, and Phase 60 was charged with fixing the scorer in place.

**Rationale:** editing a pinned producer would invalidate committed evidence; a tested copy keeps the evidence valid until a governed successor digest exists.
**Source:** 59-09-SUMMARY.md, 59-VERIFICATION.md (Carried forward)

### GAP-59-11: the JX-10 packet comparison passes exactly one 1e-4 step
The 4-decimal packet comparison uses exact decimal units: one fourth-decimal step passes and two fail. The other JX-10 checks are unchanged.

**Rationale:** owner option A fixes how the frozen tolerance is read without moving it.
**Source:** 59-07-SUMMARY.md

### Diagnostic labels and picks are reported, not acted on
Survey stage labels are diagnostic (Stages 0–1 from the splits manifest, 2–6 by ascending precedence with Stage 6 the residual); the FEAS-09 probe picks are the pre-declared rule's output. Every sensitivity window moves both picks, and this is reported, not acted on (D-20).

**Rationale:** the official stage mapping is owner-pending; a diagnostic phase must not promote its own labels into decisions.
**Source:** 59-06-SUMMARY.md

### A sign-off item that is not met stays unticked
The `59-VALIDATION.md` "Feedback latency < 10s" item stays unticked with the measured times beside it (`test_evidence_verifier` 69.7 s, `test_diag07` 13.6 s); every other item is ticked.

**Rationale:** a ticked box is a claim; the honest record is the measured shortfall.
**Source:** 59-10-SUMMARY.md, 59-VERIFICATION.md (Known issues)

---

## Lessons

### MPS cannot widen to float64 in one call
`.to(device="cpu", dtype=torch.float64)` on an MPS tensor raises `TypeError`; the tensor must move to the CPU first and then widen. CPU-only unit tests cannot see this; it first surfaced as a failed development run.

**Context:** JX-1 development run (EXIT=1 after ~20 s) and the scorer's `network_trajectory` (GAP-59-13).
**Source:** 59-07-SUMMARY.md, 59-09-SUMMARY.md

### Forward-mode autodiff fails on MPS
`jacfwd` and `jvp` promote Python scalars such as `2.0 * u` to float64 duals, which MPS refuses. Reverse-over-reverse (the gradient of the linear pullback) gives the same Jacobian.

**Context:** an MPS smoke of `branch_scales` before any run.
**Source:** 59-09-SUMMARY.md

### Generation 7 accepts only two runtime pairs
`resolve_runtime` permits only `("float32", "mps")` and `("float64", "cpu")`; a CPU cross-check built as `("float32", "cpu")` is refused.

**Context:** the JX-10 acceptance run's CPU float64 cross-check.
**Source:** 59-07-SUMMARY.md

### A known-error test can be vacuous by construction
A constant 5% scale of a rigid orbit leaves both ε_H values at roundoff, so a relative check cannot pass for a correct scorer and cannot catch a crossed frame. Applying the scale only on the later half of the times makes the check bite. Likewise, componentwise relative error at small entries is truncation-dominated; the vector-norm relative error is the right measure.

**Context:** the scorer's frame-invariance and central-difference tests.
**Source:** 59-02-SUMMARY.md

### The gsd roadmap helper corrupts this ROADMAP
`roadmap update-plan-progress` inserted blank lines across the file and wrote a malformed table cell; ROADMAP.md was restored and edited by hand.

**Context:** Plan 59-07's state updates.
**Source:** 59-07-SUMMARY.md

### Free memory on this Mac gates long runs
`vm_stat` showed 4.2 to 6.4 GB available against the 6.44 GB bar, mostly held by browser processes; runs waited up to about 70 minutes, and the bar was never lowered.

**Context:** the JX-1/JX-10 and JX-2..JX-5 development runs.
**Source:** 59-07-SUMMARY.md, 59-09-SUMMARY.md

### A first-match text replace can hit a comment
Replacing "nyquist_compliant: false" changed the comment line above the key; the sign-off-only check caught it before commit.

**Context:** the 59-VALIDATION.md sign-off edit.
**Source:** 59-10-SUMMARY.md

---

## Patterns

### Frozen-ruler loading
Canonical JSON, strict SHA-256 loader, read-only mappings with tuples for nested lists, and unknown or missing keys failing with one sorted dotted path before the hash check.

**When to use:** any pre-registered threshold set that later results are judged against.
**Source:** 59-01-SUMMARY.md

### One long step at a time behind a launch lock
Long steps run one at a time through `evidence/logs/launch.lock.log`; stale recovery refuses a live foreign PID. A long run is launched only when `vm_stat` shows the bar plus a margin at that moment.

**When to use:** detached multi-minute evidence runs on a shared laptop.
**Source:** 59-04-SUMMARY.md, 59-07-SUMMARY.md

### Commit evidence only after a detached run and a detached --check
An evidence area is committed only after its detached run and its detached `--check` both end with `EXIT=0` and its completion marker verifies; each inline step records `WALL-SECONDS` for the run and the check.

**When to use:** any evidence area whose bytes later steps pin.
**Source:** 59-06-SUMMARY.md, 59-05-SUMMARY.md, 59-08-SUMMARY.md

### Fail-closed exits with distinct codes
`CensusHalt` prints `CENSUS-HALT`, writes nothing and exits 2; `DIAG07-TOLERANCE-FAIL` exits 3, records the launch failure, releases the lock and writes no completion marker.

**When to use:** drivers whose partial outputs must never be mistaken for results.
**Source:** 59-05-SUMMARY.md, 59-07-SUMMARY.md

### Open attestation in a subprocess
File-open attestation is a process-global audit hook, exercised only in a subprocess, so the allowlisted reader can prove it never opened a held-out file.

**When to use:** proving a read-only boundary rather than asserting it.
**Source:** 59-03-SUMMARY.md

### Finish the driver before the development run
When a memory wait blocks the development runs, write and commit all the driver code first, so the development runs exercise the final code and no development result goes stale.

**When to use:** whenever a run waits on an external resource.
**Source:** 59-09-SUMMARY.md

### Keep home paths out of tracked evidence
Re-derivation commands are written as `python -B -m ...`, not the absolute interpreter path, because guardrails reject a home directory in tracked evidence; completion markers redact the data root.

**When to use:** any committed provenance or README command.
**Source:** 59-04-SUMMARY.md, 59-09-SUMMARY.md

---

## Surprises

### The comparison points are weak on Stage 0
The two-Kepler formula reaches Tier 1 on 1 of 1812 training systems and 0 of 227 validation systems (median E 0.99 and 0.94); copying the nearest training system reaches Tier 1 on 0 of 227 validation systems.

**Impact:** "beats the formula" is a low bar, so the counting rule's Tier ≥ 1 condition does the real work.
**Source:** 59-08-SUMMARY.md

### Physics was a passenger in generation 7
Gate G1 did not fire: the physics term supplied 7.19e-07 of the Adam-preconditioned update at step 900 and 2.60e-08 at step 951, while the IC anchor's gradient was five orders of magnitude larger and the secondary IC share was negative.

**Impact:** the conformance-first premise of Phases 61–63 stood; G1 recorded "proceed".
**Source:** 59-07-SUMMARY.md

### The production energy gate cannot pass even on the exact answer
With finite-difference velocities on the 0.08 grid, even Brutus's exact trajectory scores ε_H of 4.7e-2 to 3.8e-1 (GAP-59-08, OPEN, owner-routed).

**Impact:** blocks any held-out spend and the FEAS-10 pass-bar choice; carried to the charter (C-7).
**Source:** 59-VERIFICATION.md (Carried forward), .planning/milestones/v2.4-GAPS.md

### Harder stages diverge fast
Stage 4b (654 records) has a median τ_L of 2.98, about 29-fold growth by t = 10; Stage 6 (269 records) has 1.71, about 352-fold.

**Impact:** frames how hard the stages after Stage 0 are before any of them is attempted.
**Source:** 59-06-SUMMARY.md

### Several checks sat just inside their frozen limits
The monitor IC13 residual was exactly 2⁻²³, just above the frozen 1e-7; the gold-base maximum deviation was 96.8% of its 1e-6 limit and the largest inner unwrap step 97.8% of the π alias bound.

**Impact:** one owner ruling (GAP-59-10) and two near-limit values worth a line on the findings page.
**Source:** 59-05-SUMMARY.md

### The test suite was far slower than its target
`test_evidence_verifier` took 69.7 s and `test_diag07` 13.6 s against a 10 s feedback target.

**Impact:** the latency sign-off stayed open; the Nyquist file is green but its feedback item is not.
**Source:** 59-10-SUMMARY.md
