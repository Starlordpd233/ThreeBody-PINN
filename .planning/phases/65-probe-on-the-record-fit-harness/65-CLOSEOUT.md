---
phase: 65-probe-on-the-record-fit-harness
closed: 2026-10-31
status: complete
decision_authority: owner-delegated technical review
requirements: [DIAG-09, INST-08]
---

# Phase 65 closeout

Phase 65 is complete. All four items in `65-UAT.md` are resolved under the
owner's technical delegation. This records an agent review and decision, not
a claim that the owner personally inspected or approved the technical text.

The owner directed this closeout on 2026-10-31 and explicitly delegated the
probe framing, smoke framing, registration drift and runner-defect decisions.
That instruction reinforces `65-CONTEXT.md` D-01 and PROJECT.md's standing
delegation. `65-05-PLAN.md` Task 2 already says reporting review under D-01
is not a new owner approval gate. Two independent read-only reviews supported
the rulings below. No source-silent scientific decision or scope change was
needed, so no new gap is opened.

## Decisions

1. Approve the probe framing. `65-PROBE-RESULT.md` and `65-FINDINGS.md`
   Section 1 correctly describe a reproduction of already-seen exploratory
   results. All 144 required historical fields reproduced under the original
   exact-formatter rule. Low neighbour cosine remains an association, with
   no finding of information loss, insufficient capacity or a confirmed cause.
   CPU64 initialization reconstruction remains distinct from historical MPS32
   training. The normalized-tau autograd/gold-finite-difference label remains.
2. Approve the smoke framing. `65-SMOKE-PREDICTION.md` and `65-FINDINGS.md`
   Sections 3-4 establish mechanics and measured cost only. The 20 updates
   contain 2 warmup and 18 timed updates. The 0.014265412 seconds per measured
   step applies only to that locked-12, MPS float32, seed-42, 1,001-sample,
   [0, 10], Adam-1e-4 configuration. It is not steady-state throughput, evidence
   of learnability, cause confirmation or a cost measurement for another variant.
3. Preserve the probe registration and predictions as historical evidence.
   Do not replace the old dependency hashes with current ones. The result
   binds the registration's exact bytes and the dependencies at run commit
   `22cee7d241f10286594c3c5cc1a2a6817663d4a7`. Amending the registration
   would break that binding. Only `diagnostic_fit.py` and `diagnostic_guard.py`
   differ from its dependency list, following the planned 65-06 implementation.
   Historical `verify-result` passes; current `check-registration` correctly
   refuses. A future probe run requires a separately named, committed
   registration and its own prediction page before execution. The independent
   smoke registration still admits its current implementation.
4. Accept the documented probe reporting defects as historical, with the
   reuse conditions below. Do not rerun the probe or rewrite its result,
   parity receipt, stdout or reading rule to make the old execution look clean.
   The committed stdout remains explicitly labelled as regenerated from JSON.

The content-test correction follows decision 3. Dependency hashes are now
checked against the recorded run commit, with registration hash, exact bytes
and commit ancestry checked as well. Preserved source, frozen artifacts,
arm records and weights still have live digest checks. Synthetic tests still
require new-run admission to refuse changed dependencies. No test was skipped
and no production admission or result-verification rule was weakened.

## Defect dispositions and reuse conditions

These are recorded limitations, not claims of repair. `65-REVIEW.md` remains
the retained review record. Its warnings do not invalidate the registered
finite inputs, loader-derived time coordinates or top-level marked artifacts.

| Item | Disposition | Required action before affected future use |
|---|---|---|
| Probe stdout `KeyError` on `preserved_only` | Accepted as a historical reporting failure after JSON publication | Before any new probe execution, fix rendering and add a regression using preserved-only fields; prove publication and CLI completion together. |
| Empty `reading_rule.new_measurements` | Accepted as a historical redundant-summary defect; all 130 entries exist in top-level `new_measurements`, and the rule recomputes exactly | Before a new probe, repair the summary or remove the redundant contract explicitly, test agreement, then register the changed runner. Do not backfill the old result. |
| Missing standalone `logger-parity` command | Accepted implementation deviation; the run's actual fit-logger entry and `verify-result --logger-parity` prove INST-08(c) | Use the existing verified receipt. Do not add an unused command solely to match the old plan. Any future plan must name the implemented path or specify and test a new one before relying on it. |
| Missing stdout-rendering test | Deferred with renderer repair | Add the regression before any new probe run; a JSON-only success must not masquerade as a clean CLI completion. |
| WR-01, list/tuple-nested diagnostic markers | Live guard limitation, not a historical-only probe defect | Repair recursion and prove rejection at the production entry points before any graded run or held-out evaluation. This closeout authorizes neither. Existing diagnostic writers mark the top level; Phase 66 retains those writers and Stage-0 TRAIN-only access. |
| WR-02, non-finite formatter tokens can hang | Deferred before new probe registrations | Reject non-finite anchors with bounded refusal tests before accepting any new registration. The existing registered tokens are finite. |
| WR-03, malformed result CLI exceptions | Deferred verifier hardening | Before expanding these CLIs beyond the known committed records, test and normalize malformed/missing/unmarked-result refusals. Tracebacks remain failures, never verification success. |
| WR-04, record-supplied verification paths | Deferred verifier hardening | Validate repository-relative registration paths and local weight filenames before treating caller-supplied result files as trusted verifier input. Current committed records use the expected paths. |
| WR-05, malformed probe-section exceptions | Deferred before new probe registrations | Validate the probe-section structure and formatter-cell encoding before any new probe execution. |
| WR-06, normalized-time monotonicity unchecked | Deferred shared-logger hardening | Add a strict tau-increase refusal before introducing a sample source other than the current validated loader, or changing its time transform. Current loader-derived tau is increasing. |
| IN-01, string-valued `t_start` | Deferred input consistency | Type-check both endpoints consistently before admitting a new externally supplied settings format. Existing smoke uses numeric endpoints. |
| IN-02, duplicate reshape/dead branch | Accepted non-blocking cleanup | No closeout change required. |
| IN-03, default probe result path printed as None | Deferred with probe CLI repair | Correct the completion path before any new probe execution. |
| IN-04, redundant re-raise wrapper | Accepted non-blocking cleanup | No closeout change required; exclusive attempt evidence remains. |
| IN-05, private refusal accounting | Accepted current coupling | Revisit if parent refusal accounting changes; retain pre-open refusal assertions. |
| IN-06, optimizer-subclass snapshot | Accepted bounded implementation | Existing constructor interlock remains; re-test if optimizer loading or interlock use changes. |
| IN-07, timeout-test wall bound | Accepted current test limitation | Revisit upon a reproduced timeout flake; do not relax the actual run cap. |

Phases 66-67 use the fit harness and shared logger, not the historical probe's
execution path. They need their own committed predictions, registrations and
measured budgets. If their implementation touches a pinned dependency, it
must use a fresh registration; historical smoke evidence stays unchanged.
Runs at or above a one-hour cap remain refused until governed pause/resume
and power compatibility is proven. GAP-59-08 remains open for Phase 68.

## Fresh closeout checks, 2026-10-31

All Python commands below use
`<home>/miniforge3/envs/pinn-train/bin/python -B` from the trainex root.
Here `P` means `.planning/phases/65-probe-on-the-record-fit-harness` and is
notation for these command paths, not a required environment variable.

| Command arguments | Observed result |
|---|---|
| `-m unittest tests.phase65.test_probe.RegistrationContentTests` before correction | 8 tests, 1 failure, the known live-dependency mismatch |
| Same content-test command after correction | 9 tests passed |
| `-m unittest tests.phase65.test_probe` | 73 tests passed |
| `-m unittest discover -s tests/phase65 -t .` | 204 tests passed in 32.799 seconds, no skips; includes production parity and isolation tests |
| `-m pinn.verification.diagnostic_probe verify-result --result P/evidence/probe/reproduction.json --logger-parity P/evidence/probe/logger-parity.json` | `VERIFY-RESULT-OK`, exit 0 |
| `-m pinn.verification.diagnostic_fit verify-result --registration P/evidence/fit/smoke-registration.json --result P/evidence/fit/1632-smoke/record.json` | `VERIFY-RESULT-OK`, exit 0 |
| `-m pinn.verification.diagnostic_fit check-registration --registration P/evidence/fit/smoke-registration.json` | `CHECK-REGISTRATION-OK`, exit 0; registration commit `ac4358cbe61159c0a4663c9e719f19a43182edfb` |
| `-m pinn.verification.diagnostic_probe check-registration --registration P/evidence/probe/expectations.json` | Expected `PROBE-REFUSED`, exit 2, live fit dependency differs; historical registration is not current run permission |
| `from pinn.verification.learnability_protocol import load_protocol; load_protocol()` | `PROTOCOL-OK`; all 33 frozen source digests revalidated |
| `node <home>/.codex4/gsd-core/bin/gsd-tools.cjs query roadmap.validate` | Exit 0; `warnings: []` |
| `node <home>/.codex4/gsd-core/bin/gsd-tools.cjs query phase.uat-passed 65 --require-verification` | Exit 0; `passed: true`, 4 passing checks, no blockers, verification staleness check determinate |
| Inline preservation and metadata assertions against the hashes below and pre-closeout commit | Exit 0, `CLOSEOUT-INTEGRITY-OK`: 11 unchanged artifacts, 6/6 plans and summaries, 4/4 reviews, 2/13 requirements complete, Phase 66 next; no production/evidence diff |
| `git diff --check` | Exit 0; no whitespace errors |

The full suite emitted the existing PyTorch warning about converting a
gradient-carrying loss tensor to a scalar at `diagnostic_fit.py:653`; it had
no failures. Its optimizer calls use temporary fixtures. No new real probe,
corpus training run or held-out evaluation was launched for this closeout.

## Preserved evidence hashes

Each file below was compared byte-for-byte with the pre-closeout HEAD
`bc52030c687df2c44db186433e0150f02d4db2a1`, and is unchanged. Paths are relative
to this phase directory. These hashes make preservation re-derivable.

| File | SHA-256 |
|---|---|
| `65-PROBE-PREDICTION.md` | `688958f16927b936510a27537c2ce7c7ed259ade412be057beeba19afea78668` |
| `65-SMOKE-PREDICTION.md` | `d746e46ccf39236bb7c8b16ace15a8df1e4fce78557f2f1f15b2348e1c200bd7` |
| `evidence/probe/expectations.json` | `4f8cd0858c08a46717c49785082f9928bc804e3a2c29d18f4431eaa53949a2cb` |
| `evidence/probe/reproduction.json` | `b83528011ca045b15ffd449f38d9d1e69860cb8a21cfd726a22ef62b66f02ef8` |
| `evidence/probe/logger-parity.json` | `4f908f39b500d9976a2cd82fa549db0087b7405bc7443b2f2d33a70b731da6b5` |
| `evidence/probe/attempt.json` | `bdf0618f89ed00f89c216a40398c3febfb26f2cc7bc64d4adc6f41d652fbd2dd` |
| `evidence/probe/reproduction.stdout.txt` | `c7217d15f8e49a3fc087ea792a3e4352374baa6b1758a34d7a4ca791cf97329c` |
| `evidence/fit/smoke-registration.json` | `ba54e8124a33bb8b172256c6c7150b1f37e3dde1c52c682635bc49e169140d8e` |
| `evidence/fit/1632-smoke/record.json` | `f6faee77d5278aef139052a694e9e17b3090201aac17000eb9453fadd108d6ea` |
| `evidence/fit/1632-smoke/attempt.json` | `beff71b4205c2e01b11e154a6be3e399e3005bb86e8c135e26d90f9aaec95ffb` |
| `evidence/fit/1632-smoke/diagnostic.weights` | `12115adda4f9b11538091d40da8922c880a14728ed6e92f883affca85710320e` |

## Transition

DIAG-09 and INST-08 are Complete. Phase 66 is ready for discussion/planning;
this closeout does not start it. Budget, project purpose, scope/pivot,
redesign direction and other reserved owner choices remain owner decisions.
Technical judgment inside the approved direction remains delegated.
