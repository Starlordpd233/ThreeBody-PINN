---
phase: 60
phase_name: "Single-System Learnability"
project: "Three-Body Physics-Informed LLM"
generated: "2026-10-26"
counts:
  decisions: 9
  lessons: 9
  patterns: 8
  surprises: 6
missing_artifacts:
  - "60-UAT.md"
---

# Phase 60 Learnings: Single-System Learnability

Phase 60 built the INST-05 learnability harness and ran the ladder's first rung: the production network trained data-only on one Stage-0 system at a time (systems 1632, 851 and 4658), with the L-BFGS polish, under a run protocol sealed before any real arm. All three ended at Tier 0, Gate G2 fired, the four-setting `first_omega_0` sweep (60, 120, 240, 480) rescued nothing, and the phase closed on its stop path, handing RETHINK-REPRESENTATION to Phase 64 with Rung 2 and the hard-stage probes recorded as skipped ("no rescue"). Extracted from 60-01..60-23 PLAN/SUMMARY, 60-VERIFICATION.md (independent gsd-verifier pass) and the v2.4 gap index. No UAT file exists for this phase.

## Decisions

### Seal the run protocol before any real arm
The run protocol is built from the code's own constants and SHA-pinned to 33 modules and 5 cited inputs; admission starts an arm only under a drift-free protocol, a cleared record and the amendment commit. Any edit to a pinned file after the seal is drift, and an absent, untracked, dirty or malformed protocol raises the same `ProtocolDrift`.

**Rationale:** pre-registration (SCOPE-42) must be machine-checkable at launch, not a promise in a plan.
**Source:** 60-10-SUMMARY.md, 60-13-SUMMARY.md

### Fix the pinned scorer through exactly one governed successor
The scorer's MPS crash (GAP-59-13) was fixed in place (move to the CPU, then widen) and recorded as one committed successor digest. The Phase 59 verifier accepts exactly one six-key successor record, consulted only when a producer digest mismatches, and re-derives the baselines on a digest-substituted copy.

**Rationale:** the Phase 59 evidence pins the scorer's hash; a single, tightly-schematized successor keeps that evidence valid without opening a general relaxation.
**Source:** 60-02-SUMMARY.md, 60-04-SUMMARY.md

### Owner ruling GAP-60-03: clip in every arm
Gradient clipping with the trainer's `GradClipper` stays on in data-only arms (`clip_data_only_arms: true`), so data-only and physics arms share one optimizer stabilization.

**Rationale:** the ratified recipe locks the mechanism; the owner decided its scope at the protocol seal.
**Source:** 60-13-SUMMARY.md, .planning/milestones/v2.4-GAPS.md (GAP-60-03)

### Owner ruling GAP-60-09: no pre-answer for a failed confirmation
A G2 confirmation that ends below Tier 1 stops the phase and goes to the owner with concrete results (`failed_confirmation_pre_answer: null`). It did not occur.

**Rationale:** the meaning of a failed confirmation is an owner decision, not a branch the harness may take alone.
**Source:** 60-13-SUMMARY.md, 60-VERIFICATION.md (Carried forward)

### The first completed run of each arm is the result
One launch invocation per arm, seed 42, MPS float32: no restart, no second seed, and the outcome files (`g2-outcome.json`, `sweep-curve.json`) written once, each in its own commit after the records it reads.

**Rationale:** re-running until a better number appears would defeat the pre-registered rule; one seed per arm is a stated limit, not a reason to add seeds.
**Source:** 60-14-SUMMARY.md, 60-15-SUMMARY.md, 60-VERIFICATION.md (Carried forward)

### Off-path branch plans end "complete", not "halted"
Plans 60-16, 60-17 and 60-19 to 60-21 printed BRANCH-NOT-TAKEN, recorded that, launched nothing and ended `status: complete` with empty `requirements-completed`.

**Rationale:** `halted` would mark every dependent plan as blocked, and the roadmap defines an off-path branch plan as a clean ending.
**Source:** 60-16-SUMMARY.md, 60-17-SUMMARY.md, 60-19-SUMMARY.md

### Skip records before the handoff, both write-once
On the stop branch the skip records for FEAS-04 and FEAS-09 were committed alone, with the reason copied byte-for-byte from the branch query, before the handoff writer ran, so the handoff reads only committed inputs.

**Rationale:** the handoff's verdict must be derivable from committed records alone.
**Source:** 60-18-SUMMARY.md

### Repair the verifier rather than bypass it
When the evidence verifier crashed on first real use (the sweep-curve check in wave 15, the `rescore` check at closeout), the executor stopped and reported; the fix was made as an authorized Rule 1 correction with regression tests, and the curve was committed only after the fixed verifier printed `G2-OK`.

**Rationale:** the verifier is not one of the 33 pinned files, the intended check was unambiguous, and a bypassed check is no evidence.
**Source:** 60-15-SUMMARY.md, 60-22-SUMMARY.md

### The findings call nothing a verdict
`60-FINDINGS.md` presents RETHINK-REPRESENTATION as the frozen rule's output on "G2 fired and the sweep rescued nothing", recorded in `stop-handoff.json`, for Phase 64 to own and confirm.

**Rationale:** the verdict and its owner checkpoint belong to Phase 64.
**Source:** 60-22-SUMMARY.md

---

## Lessons

### Mocked tests hid every first-real-use crash of the verifier
The sweep-curve check passed tuples where the pinned function takes mappings and a keyword-only scorecard; the `rescore` check had three defects behind one error, hidden because its unit test mocked `open_real_context` as a context manager and fed torch tensors where real data are NumPy arrays.

**Context:** both crashes happened on real artifacts after the tests were green; both were fixed with tests rewritten on real objects.
**Source:** 60-15-SUMMARY.md, 60-22-SUMMARY.md, 60-VERIFICATION.md (Known issues 1)

### float32 at first_omega_0 = 30 amplifies rounding
An element-wise rtol 1e-4 / atol 1e-5 band left 17, 41 and 42 percent of position, velocity and acceleration elements outside, although the arrays agree to under 1e-4 of their largest magnitude; the test bound became 1e-3 of the largest magnitude.

**Context:** comparing the MPS float32 scorer path with CPU float64.
**Source:** 60-02-SUMMARY.md

### A reference built with the function under test lets bugs cancel
Comparing `network_trajectory` on MPS with `network_trajectory` on CPU missed two of seven injected mutations; computing the reference from the trainer's closure and `componentwise_du` caught all seven.

**Context:** mutation-checking the MPS scorer test.
**Source:** 60-02-SUMMARY.md

### torch.optim.LBFGS.step returns the objective at the start of the call
Using its return value as "the objective after this call" makes call 1 tie the Adam baseline and lags every comparison by one call; the objective must be evaluated at the iterate the call ends with.

**Context:** the GAP-60-05 polish-improvement rule.
**Source:** 60-01-SUMMARY.md

### The phase60 suite takes about 13 minutes, not 60 seconds
The full `tests/phase60` discovery runs 989 to 992 tests in about 788 s, against the plan's and `60-VALIDATION.md`'s "under about 60 s"; `test_admission` alone takes 70 to 160 s.

**Context:** the closeout gate and the validation contract.
**Source:** 60-22-SUMMARY.md, 60-10-SUMMARY.md

### NFKC turns a circled digit into a plain digit
A literal U+2463 (④) becomes "4" under NFKC normalization, silently changing a pre-registered reason; the edit tool also turned the escape into the literal. Sources keep the escape.

**Context:** the second skip reason in the G2 module.
**Source:** 60-06-SUMMARY.md

### A SUMMARY file marks a plan complete
GSD's plan index treats any `*-SUMMARY.md` as completion, so no SUMMARY draft may exist while a long arm runs; the waiting record was carried in STATE.md instead.

**Context:** Plan 60-14's multi-hour Rung-1 wait.
**Source:** 60-14-SUMMARY.md

### Small platform traps
Python block-buffers redirected stdout, so a long run's log looks empty until exit; `os.kill(0, 0)` addresses the caller's whole process group, so a PID of zero must never be probed; the production admission gate raises `IndexError`, not `NotAdmitted`, for a file with no complete snapshot block.

**Context:** the 60-04 detached `final`, the 60-07 supervisor liveness check and the 60-23 preflight.
**Source:** 60-04-SUMMARY.md, 60-07-SUMMARY.md, 60-23-SUMMARY.md

### gsd's TDD-red check does not read Python unittest
`check tdd-red-evidence` parses Node TAP output and reports zero tests for Python `unittest`; RED evidence was kept as retained logs instead.

**Context:** test-first tasks in 60-04 and 60-07.
**Source:** 60-04-SUMMARY.md, 60-07-SUMMARY.md

---

## Patterns

### Mutation-check the tests, restore byte-identically
Inject faults into the code under test, require the tests to catch each, and restore the file byte-identically (SHA-256 checked) after every mutation; 60-07 injected 81 faults and caught 80, the remaining one equivalent.

**When to use:** any guard or verifier whose tests could pass vacuously.
**Source:** 60-02-SUMMARY.md, 60-07-SUMMARY.md, 60-01-SUMMARY.md

### Authorize first, then gate, then check first-result files, then read
`run_arm` resolves and checks the setting before runtime resolution, fixture gating, the first-result check, any data read and any network build; a checkpoint is vetted before any record or corpus file is touched.

**When to use:** any entry point that can spend compute or write evidence.
**Source:** 60-08-SUMMARY.md, 60-23-SUMMARY.md, 60-12-SUMMARY.md

### Owner answers enter through one strict reader
Owner rulings reach the harness only through `learnability_ruling`: fixed paths, a strict block, an opaque verbatim quote and a SHA-256 cited downstream.

**When to use:** whenever an owner decision changes what code is allowed to do.
**Source:** 60-06-SUMMARY.md

### One exception and one exit code per outcome class
`G2Halt` exits 2, `G2Pending` exits 4, `OwnerRouted` exits 3 (handled only in `main`); every owner-routed handler below `main` ends in a bare `raise`.

**When to use:** CLIs whose exit codes drive later automation.
**Source:** 60-06-SUMMARY.md, 60-11-SUMMARY.md

### Checkpoint the state, not the decision
A resume re-enters the budget driver's own loop, so the extension decision is made once by the same frozen function; only an arm that exited through its own handler (129, 130, 143) may resume.

**When to use:** resumable long runs whose decisions are pre-registered.
**Source:** 60-12-SUMMARY.md, 60-07-SUMMARY.md

### Guard the write, not the caller
`record.json` cannot be created until `validate_record` accepts the assembled payload; a stop writes its own record before it re-raises.

**When to use:** write-once evidence files.
**Source:** 60-11-SUMMARY.md

### Data or instrument? Establish which before editing
When an independent verifier fails on a new artifact, first recompute the claim separately and run the unchanged verifier with only the suspect call patched in memory; then stop and report before editing the instrument.

**When to use:** any verifier failure on a write-once artifact.
**Source:** 60-15-SUMMARY.md

### Taken and not-taken branch records
A branch plan records the query line and exit code, the outcome re-derived from committed blobs, a statement of what was (not) launched or asked, and its deviations; sustained runs record each status reading and owner reply verbatim and never stage `runs/`.

**When to use:** conditional plans and multi-hour detached runs.
**Source:** 60-16-SUMMARY.md, 60-18-SUMMARY.md, 60-14-SUMMARY.md

---

## Surprises

### Every trained network learned only the average position
For all seven arms the output varies in time by about 0.3% of the real orbit's variation; the error equals that of predicting each body's mean position (ratio 0.9999 to 1.0001), and the frozen scorer grades the constant mean predictor Tier 0 with E within 0.004 of the trained networks.

**Impact:** E sits in a narrow band (1.14 to 1.24) whatever the orbit; the records cannot separate a representation limit from an outcome of the fixed recipe. Phase 64 states this beside the label.
**Source:** 60-VERIFICATION.md (Independent observation for Phase 64)

### No first-layer setting rescued anything
Rung 1 ended Tier 0 on all three systems (worst position error 1.14 to 1.24 against the 0.10 Tier-1 line, valid horizon 0.0), and all four sweep settings ended Tier 0 on system 1632.

**Impact:** G2 fired and the ladder stopped; Phases 61–63 were skipped, not failed.
**Source:** 60-14-SUMMARY.md, 60-15-SUMMARY.md

### The weights moved a long way and the output did not
In the `r1-1632` Adam state every input and hidden tensor ended 5.3 to 14.0 times its initial norm away from initialization, while the output stayed nearly constant in time.

**Impact:** rules out "the optimizer never moved the network" as the explanation.
**Source:** 60-VERIFICATION.md (Independent observation for Phase 64)

### Seven arms cost 22.4 machine hours
r1-1632 2.573 h, r1-851 2.842 h, r1-4658 5.693 h (it earned its one budget doubling, 980,623 to 1,961,246 steps) and the four sweep arms 2.730, 2.903, 3.046 and 2.591 h; timed seconds per step ran 0.0109 to 0.0136.

**Impact:** the measured cost basis for the verdict's cost model.
**Source:** 60-14-SUMMARY.md, STATE.md (Decisions from 60-18)

### The arms ran below the memory bar
The owner waived the 6 GiB free-memory figure; Rung 1 ran with about 4 GiB advisory free and 9.9 GB of swap in use, the sweep with about 5.3 GiB, and every arm exited 0.

**Impact:** no stop or visible slowdown, but the effect of swap on seconds per step was not measured.
**Source:** 60-14-SUMMARY.md, 60-15-SUMMARY.md

### One production-shape step costs about 29 s on the CPU
A single 4,096-row physics step on the production network in CPU float64 takes about 29 s (47 s with diagnostics), so the committed oracle uses 400 rows and the full-shape equality was checked once outside the suite.

**Impact:** bit-identity tests must be sized to the suite budget, not to production.
**Source:** 60-05-SUMMARY.md
