---
phase: 65-probe-on-the-record-fit-harness
verified: 2026-10-29T22:26:48Z
status: human_needed
score: 7/7 must-haves verified
behavior_unverified: 0
overrides_applied: 0
runtime: general-purpose (gsd-verifier role definition loaded)
re_verification:
  previous_status: none
  note: initial verification (no previous 65-VERIFICATION.md existed)
human_verification:
  - test: "Review the 65-05 judgment-tier prohibition: 'The historical cosine association must not be presented as independent prospective discovery or causal proof' (65-05-PLAN.md must_haves.prohibitions, status unresolved) against 65-PROBE-RESULT.md and 65-FINDINGS.md Section 1."
    expected: "The prose keeps the reproduction framed as a reproduction of already-seen results, association only, with D-02/D-07 labels preserved. Non-authoritative LLM-judge text review: COMPLIANT (both pages state the association-only framing explicitly and route themselves for review in 65-FINDINGS.md Section 5). Human confirmation is the deciding verdict."
    why_human: "Prohibition carries no wired-check descriptor; it is scientific-reporting judgment on prose, untestable by any deterministic gate."
  - test: "Review the 65-06 judgment-tier prohibition: 'The short 1632 smoke must not be presented as learnability, cause confirmation or measured cost for an unmeasured variant' (65-06-PLAN.md must_haves.prohibitions, status unresolved) against 65-SMOKE-PREDICTION.md and 65-FINDINGS.md Sections 3-4."
    expected: "The prose keeps mechanics and cost separate from inference; the 0.014265 s/step basis is bounded to the exact configuration with the not-steady-state caveat. Non-authoritative LLM-judge text review: COMPLIANT. Human confirmation is the deciding verdict."
    why_human: "Same judgment-tier reporting prohibition; no deterministic check can adjudicate phrasing."
  - test: "Owner decision: amend/re-commit the 65-05 probe registration's two drifted dependency digests (pinn/verification/diagnostic_fit.py 2e2c06eb->b00e45b4, pinn/verification/diagnostic_guard.py d164bc4d->8dd577a2), or leave the probe registration historical."
    expected: "A recorded owner decision. The probe itself needs no further runs; its committed result remains verifiable (probe verify-result -> VERIFY-RESULT-OK, exit 0, historical-dependency mode). Until decided, probe check-registration refuses against the live tree (exit 2) and one content test fails (RegistrationContentTests.test_the_recorded_dependency_and_source_digests_match_disk)."
    why_human: "Amending committed 65-05 evidence is an owner registration-digest decision, pre-routed by 65-05 and recorded in 65-FINDINGS.md Section 7; the verifier does not amend committed evidence."
  - test: "Owner decision: route the two documented 65-04 runner defects (diagnostic_probe.py _render_stdout KeyError on preserved_only verdicts; empty reading_rule.new_measurements field), the missing standalone logger-parity subcommand, and the stdout-rendering suite gap."
    expected: "A recorded routing decision (remediation plan or accepted-as-historical). Any diagnostic_probe.py edit changes the probe registration's pinned dependency digests, so the decision is coupled to the digest decision above."
    why_human: "Owner-routed by 65-05/65-06 deviations and 65-FINDINGS.md Section 7; the defects are documented, none touches the recorded result's content."
---

# Phase 65: Probe on the Record & Fit Harness — Verification Report

**Phase Goal:** The probe's lead is either on the record or withdrawn, and a tested harness can train and score any named network variant on one orbit in minutes. (ROADMAP.md Phase 65)
**Verified:** 2026-10-29T22:26:48Z
**Status:** human_needed (7/7 truths verified; 2 flagged judgment-tier prohibitions + 2 owner decisions require human review)
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

Roadmap success criteria (the contract) split into seven checkable truths.

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | SC-1: The probe script and the 2026-10-27 figures are committed as predictions before it runs; every figure recorded as reproduced or not on all seven arms, at initialization and after training; every weight file checked by SHA-256 before loading | ✓ VERIFIED | Registration commit `f469e003` is a git ancestor of run commit `22cee7d2` (`git merge-base --is-ancestor` → true); `evidence/probe/expectations.json` (2975 lines) records every token's exact formatter rounding cell; `reproduction.json`: `reading_rule.verdict = retained`, `required_count = 144`, `reproduced_count = 144`, `failed_required = []`, `provenance_limitations = []`, 64 preserved-only fields, 130 new measurements; hash-before-load enforced by the runner and behaviorally proven by the passing `test_changed_weight_bytes_refuse_before_any_load` (tests/phase65/test_probe.py:820) |
| 2 | SC-2a: The locked 12-layer variant gives the production network's forward pass at the same seed and weights | ✓ VERIFIED | `ParityContractTests` re-run live: 4/4 OK including `test_mps_float32_parity_with_copied_identical_weights` (MPS available on this Mac — the case ran, not skipped) and bitwise CPU64 parameter/output equality with unequal raw masses |
| 3 | SC-2b: The harness scores with the frozen FEAS-01 scorer (not a re-implementation) | ✓ VERIFIED | `FrozenSourceContractTests` passed in the discovery; `load_protocol()` re-run by this verifier → PROTOCOL-OK (all 33 pinned module digests revalidate); frozen scorecard digest unchanged; `record.json#scores` carries the full frozen `ScoreResult` shape |
| 4 | SC-2c: The similarity logger reproduces the probe's value on one committed arm | ✓ VERIFIED | `logger-parity.json` is the run's actual `diagnostic_fit.log_similarity` entry (r1-1632 polish, step -1, 13 layers, CPU64, no updates); verifier re-ran `verify-result --logger-parity` → VERIFY-RESULT-OK (exit 0), and independently confirmed the receipt entry equals the result's recorded entry (parsed-object equality) |
| 5 | SC-2d: Test-split paths are refused, and the graded-run and evaluator paths refuse its records | ✓ VERIFIED | `Stage0AdmissionTests`, `EvaluateEntryIsolationTests`, `GradedEntryIsolationTests`, `CheckpointRouteIsolationTests`, `DiagnosticEnvelopeTests` all passed in the re-run discovery (zero-effect refusal fixtures: relocation beside valid provenance, CTX-53 key laundering, explicit-file/directory/latest resume forms, marker refusal outside corrupt-file handlers); guard placement confirmed in `pinn/evaluate.py` (`require_not_diagnostic` before the evaluation claim, evaluate.py:412-423) |
| 6 | SC-3: A short run on orbit 1632 completes and is scored; measured seconds per step is recorded and sets the budgets for Phases 66-67 | ✓ VERIFIED | `evidence/fit/1632-smoke/record.json`: `status: complete`, schema `inst08-diagnostic/v1`, `steps.completed = 20` (2 warmup + 18 measured), all within the registered 600 s whole-run cap (fit body 2.72 s; `attempt.json` records `whole_run_cap_seconds: 600.0`); `timing.seconds_per_step = 0.014265412` (18 measured synchronized steps, denominator recorded); network E 24.80 tier 0, window-mean constant E 1.1538 tier 0, two-Kepler E 0.9168 tier 0 (applicable, converged); 5 similarity entries at steps 0/5/10/15/20 (13 layers each); 65-FINDINGS.md Section 4 publishes the budget formula for Phases 66-67 with the not-steady-state caveat |
| 7 | SC-4: No training step ran in the probe, no test-split file was opened, and the tooling asserts this | ✓ VERIFIED | `reproduction.json#interlock.attempted_steps = 0` with 15/15 matching parameter digest pairs; probe access attestations: all 7 arms `split: train`, orbit stage 0, 1,001 samples; smoke `access.attestation`: `train: 1, validation: 0, test_split_opened: 0`, `stage0.actual_opens = 1` (hierarchical/gold/1632, train, stage 0); the assertions are wired (guarded seam + process open attestation + optimizer interlock) and tested |

**Score:** 7/7 truths verified (0 present, behavior-unverified)

All four production-refusal and parity claims above carry passing behavioral tests (not mere symbol presence), and the two registered runs are themselves behavioral evidence recorded by the tooling under their committed gates.

### Requirement Acceptance Detail

**DIAG-09 — SATISFIED.** (i) The 2026-10-27 figures are committed as predictions with reproduction tolerance (exact formatter rounding cells, never a widened tolerance) before the script ran — commit chronology proven by ancestry. (ii) Each figure recorded as reproduced or not — 144/144, 0 not_reproduced. (iii) Weights checked by SHA-256 before loading — hash-before-load gate, behaviorally tested. (iv) No training runs and no test-split file opened, asserted — interlock + attestations + tests.

**INST-08 — SATISFIED.** (a) locked-variant production parity — ParityContractTests 4/4 OK (live re-run). (b) frozen FEAS-01 scorer — FrozenSourceContractTests + 33-digest protocol revalidation (PROTOCOL-OK). (c) logger reproduces DIAG-09 on one committed arm — logger-parity receipt + verify-result cross-check. (d) test-split refusals + graded-run/evaluator refuse records — entry isolation suites passed. (e) short run completes and is scored — the registered smoke (INST-08(e)); variant/registry/run-record fields (depth, width, time features, lr, window; marked diagnostic; budget and measured seconds per step) all present in `record.json`.

**SCOPE-45..49 — all honored.** SCOPE-45: Stage-0 TRAIN-only reads attested in both runs; the single preserved evaluation stays unspent — the only evaluation receipt on disk is the historical v2.0 one (`runs/stage0-pilot-seed42/evaluation/evaluation-receipt.json`, 2026-07-22); no new evaluation directory or receipt was created in the phase window, and the phase's own evaluate-path tests ran in temporary layouts with zero claim calls. SCOPE-46: no framework-spec edits — `git diff be7c2af8..HEAD` touches no `pinn_instruction/` file and no REQUIREMENTS.md; only `.planning/ROADMAP.md` (wave-checkbox progress) and `.planning/STATE.md` outside the phase dir. SCOPE-47: prediction pages and registrations committed before their runs (probe: `f469e003` → run at `22cee7d2`; fit: `ac4358cb`/`b1dcacc4` → `84128fe2`, ancestry verified; reading rule immutable). SCOPE-48: compute on this Mac (MPS), measured seconds-per-step recorded, 600 s cap enforced by supervised worker, caps ≥ 3600 s refuse before data access. SCOPE-49: no pivot proposed — `scope49_proposal: false`, verdict `retained`.

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `pinn/verification/diagnostic_variants.py` | sealed variant registry + locked-12 | ✓ VERIFIED | exists, substantive; sealed registry test-pinned |
| `pinn/verification/diagnostic_similarity.py` | one shared centred-neighbour measurement | ✓ VERIFIED | used by both probe and fit logger (wired both directions) |
| `pinn/verification/diagnostic_data.py` | guarded Stage-0 seam + recorded normalizer | ✓ VERIFIED | admission precedes I/O; three-way stats digest check |
| `pinn/verification/diagnostic_fit.py` | fit_diagnostic, log_similarity, bounded CLI | ✓ VERIFIED | real-data CLI verified end to end by this verifier's re-runs |
| `pinn/verification/diagnostic_guard.py` | intrinsic markers + refusals + committed-registration admission | ✓ VERIFIED | wired into evaluate.py/train.py/checkpoint.py/resume.py |
| `pinn/verification/diagnostic_probe.py` | read-only DIAG-09 runner + CLI | ✓ VERIFIED | verify-result re-run OK; check-registration refuses on the documented drift (see Open Items) |
| `pinn/evaluate.py`, `pinn/train.py`, `pinn/training/checkpoint.py`, `pinn/training/resume.py` | production entry-point refusals | ✓ VERIFIED | wired, behaviorally tested; production semantics for unmarked payloads unchanged (regression suites in summaries) |
| `tests/phase65/` (5 modules) | 203 tests | ✓ VERIFIED | re-run: 203 tests, 1 known owner-routed failure (see Gaps/Notes) |
| `65-PROBE-PREDICTION.md` + `evidence/probe/expectations.json` | committed registration | ✓ VERIFIED | commit `f469e003`; page SHA-256 recorded inside expectations |
| `evidence/probe/{reproduction.json,logger-parity.json,attempt.json,reproduction.stdout.txt}` | run evidence | ✓ VERIFIED | complete result; stdout.txt carries provenance header (regenerated, not runner output) |
| `65-PROBE-RESULT.md`, `65-SMOKE-PREDICTION.md`, `65-FINDINGS.md` | result/findings pages | ✓ VERIFIED | interpretation discipline present; prohibitions self-flagged for review |
| `evidence/fit/smoke-registration.json`, `evidence/fit/1632-smoke/{record.json,diagnostic.weights,attempt.json}` | fit registration + run evidence | ✓ VERIFIED | record sha256 `f6faee77…` matches attempt; marked `inst08-diagnostic` payload |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| evaluate.py / train.py / checkpoint.py / resume.py | diagnostic_guard.py | require_not_diagnostic / carries_diagnostic_marker / require_resume_not_diagnostic | WIRED | content guards before claim/run-creation; verified by passing isolation suites |
| diagnostic_fit.py | learnability_losses.py / feasibility_scorer.py | data_only_loss, score_network, score_trajectory | WIRED | direct frozen-source calls; frozen-source contract tests pass |
| diagnostic_fit.py + diagnostic_probe.py | diagnostic_similarity.py | measure_time_signal (one shared implementation) | WIRED | reductions pinned against direct cosine in tests |
| reproduction.json | expectations.json | committed registration identity + exact per-field comparison | WIRED | verify-result recomputes the reading rule from the committed registration |
| logger-parity.json | diagnostic_fit.py | actual log_similarity call recorded in the run | WIRED | receipt == result's recorded entry (independently confirmed) |
| smoke record | smoke-registration.json | phase65-fit-registration/v1 admission | WIRED | check-registration OK at commit `ac4358cb`; verify-result OK |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Full phase65 suite | `python -B -m unittest discover -s tests/phase65 -t .` | Ran 203 tests; FAILED (failures=1) — the single failure is exactly `RegistrationContentTests.test_the_recorded_dependency_and_source_digests_match_disk` (documented owner-routed digest drift) | ✓ PASS (expected outcome matched) |
| Probe result verification | `python -B -m pinn.verification.diagnostic_probe verify-result --result …/reproduction.json --logger-parity …/logger-parity.json` | VERIFY-RESULT-OK, exit 0 | ✓ PASS |
| Fit result verification | `python -B -m pinn.verification.diagnostic_fit verify-result --registration …/smoke-registration.json --result …/1632-smoke/record.json` | VERIFY-RESULT-OK, exit 0 | ✓ PASS |
| Fit registration re-admission | `python -B -m pinn.verification.diagnostic_fit check-registration --registration …/smoke-registration.json` | CHECK-REGISTRATION-OK registration-commit=ac4358cb…, exit 0 | ✓ PASS |
| Probe registration re-admission (live tree) | `python -B -m pinn.verification.diagnostic_probe check-registration --registration …/expectations.json` | PROBE-REFUSED (exit 2): diagnostic_fit.py digest drift — the documented, owner-routed consequence; the committed result remains verifiable via verify-result (historical-dependency mode) | ⚠ DOCUMENTED (open item, not a regression of the recorded run) |
| 33 pinned digests | `load_protocol()` (learnability_protocol) | PROTOCOL-OK | ✓ PASS |
| MPS parity (behavioral) | `unittest tests.phase65.test_contracts.ParityContractTests` | 4/4 OK incl. the MPS float32 case (ran, not skipped) | ✓ PASS |
| Parity receipt equality | parsed-object comparison of logger-parity.json entry vs result's recorded entry | equal | ✓ PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| DIAG-09 | 65-01..65-06 (all declare it) | The 2026-10-27 probe, on the record | ✓ SATISFIED | All four acceptance items verified (see Requirement Acceptance Detail). REQUIREMENTS.md checkbox remains `[ ]` Pending — flip is recorded as this verification act's finding for the orchestrator |
| INST-08 | 65-01..65-06 (65-03 declares it alone among subsets) | Minute-scale diagnostic fit harness | ✓ SATISFIED | All five acceptance items (a)-(e) verified. Same checkbox note as DIAG-09 |
| SCOPE-45..49 | REQUIREMENTS.md | Scope boundaries | ✓ HONORED | See Goal Achievement section |

No orphaned requirements: REQUIREMENTS.md maps exactly DIAG-09 → Phase 65 and INST-08 → Phase 65, and both are claimed by the plans.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| (none) | — | No TBD/FIXME/XXX/TODO/HACK/PLACEHOLDER markers in any phase-created module or test (grep count 0) | — | — |
| (none) | — | No circular expected-value generation (capture/snapshot matches are git subprocess flags and provenance snapshot IDs, not generated expectations) | — | — |
| tests/phase65/test_contracts.py | 220 | One `skipTest` — MPS float32 parity case, environment-conditional | ℹ️ Info | Ran on this machine (MPS available); not a disabled requirement test |
| pinn/verification/diagnostic_probe.py | 954 (per docs) | stdout-renderer KeyError on `preserved_only`; empty `reading_rule.new_measurements`; missing standalone `logger-parity` subcommand | ⚠️ Warning (routed) | Documented 65-05/65-06 routed defects; digest-pinned file, owner decision pending; does not touch recorded result content |
| pinn/verification/diagnostic_guard.py | 87-94 (per 65-REVIEW WR-01) | list-nested markers evade the content predicate | ⚠️ Warning | Defense-in-depth gap reachable only by a hand-crafted artifact; all existing artifacts are caught; flagged by the phase's own code review (0 critical, 6 warnings, 7 info) |

### Test Quality Audit

| Test File | Linked Req | Active | Skipped | Circular | Assertion Level | Verdict |
|-----------|-----------|--------|---------|----------|-----------------|---------|
| tests/phase65/test_contracts.py | INST-08(a,b) | 38 | 0 (1 env-conditional that ran) | 0 | Value/behavioral (bitwise equality, digest pins) | VALID |
| tests/phase65/test_fit_short.py | INST-08(e) + harness | 69 | 0 | 0 | Behavioral (end-to-end fit, timing, cap, attempt ownership) | VALID |
| tests/phase65/test_isolation.py | INST-08(d), D-09 | — | 0 | 0 | Behavioral (zero-effect refusals beside valid provenance, ordinary controls) | VALID |
| tests/phase65/test_probe.py | DIAG-09 | 72 (1 fail, owner-routed) | 0 | 0 | Behavioral (formatter cells, registration gates, reading rule, interlock) | VALID |

Provenance: the 144 reproduced values are compared against preserved historical tool outputs (`evidence/original/stdout.json`, byte-preserved with SHA-256s) — an external oracle, not the system under test. VALID.

### Decision Coverage

`check.decision-coverage-verify` → `{ skipped: false, blocking: false, total: 11, honored: 11, not_honored: [] }` — "All trackable CONTEXT.md decisions are honored by shipped artifacts."

### Human Verification Required

See the `human_verification` frontmatter list (4 items):
1. Judgment-tier prohibition review (65-05): association must not be presented as discovery/cause. Non-authoritative text review: COMPLIANT.
2. Judgment-tier prohibition review (65-06): smoke must not be presented as learnability/cause/cost for an unmeasured variant. Non-authoritative text review: COMPLIANT.
3. Owner decision: probe registration digest amendment (two drifted dependency digests) vs. leave historical.
4. Owner decision: routing of the documented 65-04 runner defects and the missing standalone logger-parity subcommand.

### Gaps Summary

No blocker and no FAILED truth: every ROADMAP success criterion is verified against committed evidence re-derived by this verifier (git ancestry, direct JSON inspection, live CLI re-runs, live protocol revalidation, live parity tests). The phase goal is achieved: the probe's lead is on the record (`retained`, 144/144 under exact formatter equality) and a tested, registered harness trained and scored the locked variant on orbit 1632 in minutes, with its measured cost recorded.

The status is `human_needed`, not `passed`, solely because two judgment-tier scientific-reporting prohibitions (declared `unresolved` in the 65-05/65-06 plan frontmatter) require human review, and two owner-routed decisions (probe-registration digest drift; runner-defect remediation) are open. None of these blocks Phase 66: 65-FINDINGS.md Section 7 states the drift blocks no later work, the smoke registration pins the current implementation independently, and the probe needs no further runs.

The single failing test in the 203-test discovery is correct about its subject — it pins the 65-05 probe registration's dependency digests, which legitimately drifted when 65-06's plan mandated edits to `diagnostic_fit.py`/`diagnostic_guard.py`. The conflict is plan-sanctioned and owner-routed (65-05 pre-routed it; 65-FINDINGS.md Section 7 records it with the owner decision requested). It is not a hidden behavioral break: `verify-result` still verifies the recorded run against its own run commit, and the drift was independently enumerated by this verifier as exactly those two files (every other pinned artifact matches).

---
_Verified: 2026-10-29T22:26:48Z_
_Verifier: Claude (gsd-verifier, general-purpose runtime)_
