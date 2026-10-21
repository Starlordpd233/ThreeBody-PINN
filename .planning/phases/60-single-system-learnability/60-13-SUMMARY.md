---
phase: 60-single-system-learnability
plan: 13
subsystem: verification
tags: [run-protocol, preflight, verifier, fail-closed, pre-registration, gap-60-03, gap-60-09]

requires:
  - phase: 60-single-system-learnability
    provides: "60-03 amendment commit, 60-04 baselines successor digest, 60-07 CPU cross-check scope, 60-09 failed confirmation procedure, 60-12 arm runner and admission"
  - phase: 59-read-only-baseline-scorecard
    provides: "the frozen scorecard f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b"

provides:
  - "verify_phase60_evidence.py: fail-closed independent evidence verifier for protocol, preflight, records, g2, rescore and final subcommands"
  - "tests/phase60/test_verifier_phase60.py: 26 unit tests covering synthetic evidence trees, G2 token validation, and re-scoring"
  - "evidence/preflight/records.json: preflight check of all ten assigned dataset records (train split, 1001/126/59 counts, 0 blocked, 0 attestation opens)"
  - "evidence/run-protocol.json: pre-registered and sealed run protocol (SHA-256 93486d240f129bb5947cddb56d2eb18936ac0cbad7ac0bceeb0af0372b850383)"
  - "60-RUN-PROTOCOL.md: plain-language protocol for the project owner"

protocol_sha256: 93486d240f129bb5947cddb56d2eb18936ac0cbad7ac0bceeb0af0372b850383
preflight_sha256: 7f4fffe8702da3da8307582310221ccc0d4b1abab1156dd48b2c6103c89892cd
amendment_commit: dc3edac0e9ae737b42be276dd9b67e12b8ab8926

owner_reply_verbatim:
  GAP-60-03: "Keep clipping in data-only arms (delegated default: Adam limits unusually large gradient steps using GradClipper at Stage 0 multiplier 8.5)"
  GAP-60-09: "No pre-answer: ask me if it happens (stop the phase and prompt for decision if a failed confirmation occurs)"

actuals:
  tokens: 18500
  tasks: 4
  commits: 3
  plan_head_before: 8df698864d420f86b406981cfb56c4d7ec59b56f

tech-stack:
  added: []
  patterns:
    - "Fail-closed evidence verifier with zero production code dependencies except frozen scorecard and network builders"
    - "Pre-registration of all hyperparameters, schedules, seeds, digests, and owner decisions before launching any real arm (SCOPE-42)"
    - "Assigned-record preflight with strict attestation checks (0 test split opens, 0 blocked attempts) before any real arm (SPEC Requirement 8)"

key-files:
  created:
    - .planning/phases/60-single-system-learnability/evidence/verify_phase60_evidence.py
    - tests/phase60/test_verifier_phase60.py
    - .planning/phases/60-single-system-learnability/evidence/preflight/records.json
    - .planning/phases/60-single-system-learnability/evidence/run-protocol.json
    - .planning/phases/60-single-system-learnability/60-RUN-PROTOCOL.md
  modified: []

key-decisions:
  - "GAP-60-03: Gradient clipping in data-only arms is kept (clip_data_only_arms: true) per owner decision, ensuring identical optimizer stabilization across data-only and physics arms"
  - "GAP-60-09: Failed G2 confirmation has no pre-answer (failed_confirmation_pre_answer: null) per owner decision; if this condition occurs, execution stops and prompts the owner with concrete results"
  - "The verifier maintains its own independent copy of REQUIRED_REAL_FIELDS matching learnability_run.REQUIRED_REAL_FIELDS"
  - "rescore subcommand loads weights with weights_only=True and re-scores on MPS float32 and CPU float64 without retraining"

requirements-completed: [INST-05, FEAS-03, FEAS-04, FEAS-09]

duration: 25min
completed: 2026-10-20
status: complete
---

# Phase 60 Plan 13: Evidence Verifier, Assigned-Record Preflight, and Run Protocol Pre-Registration Summary

**The Phase 60 evidence verifier is built and proven, all ten assigned records are checked and verified in preflight, the owner has decided GAP-60-03 and GAP-60-09, and the run protocol is sealed and committed before any real arm has launched.**

In plain language: the experiment's ruler, rules, hardware configuration, random seed, and exact code digests are now fingerprinted and locked. Every real result must cite this sealed protocol, and all three initial Rung-1 arms are admissible.

## Performance

- **Duration:** about 25 min
- **Tasks:** 4 (Task 1 verifier tracer, Task 2 preflight record, Task 3 owner decision checkpoint, Task 4 run protocol seal)
- **Commits:** 3
  1. `a264d2e8`: `feat(60-13): add the fail-closed phase 60 evidence verifier and tests`
  2. `fb15e438`: `evidence(60-13): record the assigned-record preflight`
  3. `52d98211`: `spec(60-13): pre-register the phase 60 run protocol`
- **Files created:** 5 files (`verify_phase60_evidence.py`, `test_verifier_phase60.py`, `records.json`, `run-protocol.json`, `60-RUN-PROTOCOL.md`)

## Accomplishments

- **Independent Fail-Closed Verifier (Task 1):** Built `.planning/phases/60-single-system-learnability/evidence/verify_phase60_evidence.py` supporting `protocol`, `preflight`, `records`, `g2`, `rescore`, and `final`. Independent from the runner code. Tested across 26 unit tests in `tests/phase60/test_verifier_phase60.py` covering synthetic evidence trees, token syntax rules, missing fields, corrupted weights, and digest mismatches.
- **Assigned-Record Preflight (Task 2):** Preflight ran and confirmed all ten assigned records (hierarchical 1632, 851, 4658 gold & base; standard 2279, 3418 gold & base) under `evidence/preflight/records.json`. All counts matched verified expectations (1,001 within T on gold, 126 on hierarchical base, 59 on standard base). All attestation counters are 0. Verified by `verify_phase60_evidence.py preflight` -> `PREFLIGHT-OK`.
- **Owner Checkpoint (Task 3):** Presented the two pre-seal decisions to the project owner in plain language and recorded the responses verbatim:
  - **GAP-60-03:** Keep gradient clipping in data-only arms (delegated default: Adam limits unusually large gradient steps using GradClipper at Stage 0 multiplier 8.5).
  - **GAP-60-09:** No pre-answer: ask me if it happens (stop the phase and prompt for decision if a failed confirmation occurs).
- **Protocol Pre-Registration (Task 4):** Written via `pinn.verification.learnability_protocol write --amendment-commit dc3edac0e9ae737b42be276dd9b67e12b8ab8926`. Created plain-language companion `60-RUN-PROTOCOL.md`. Verified by `verify_phase60_evidence.py protocol` -> `PROTOCOL-OK`. Dry-run admission tested via `learnability_run r1-1632 --admit-only` -> `ADMIT-OK r1-1632` and `launch_phase60_arm.py --sequence rung1 --dry-run` -> all three Rung-1 arms admitted.

## Task Commits

1. `a264d2e8` - `feat(60-13): add the fail-closed phase 60 evidence verifier and tests`
2. `fb15e438` - `evidence(60-13): record the assigned-record preflight`
3. `52d98211` - `spec(60-13): pre-register the phase 60 run protocol`

## Verification Results

| Command | Result |
|---|---|
| `python -B -m unittest tests.phase60.test_verifier_phase60 tests.phase60.test_static_guards -v` | Ran 52 tests in 7.356s, OK, exit 0 |
| `python -B .planning/phases/60-single-system-learnability/evidence/verify_phase60_evidence.py preflight` | `PREFLIGHT-OK`, exit 0 |
| `python -B .planning/phases/60-single-system-learnability/evidence/verify_phase60_evidence.py protocol` | `PROTOCOL-OK`, exit 0 |
| `python -B -m pinn.verification.learnability_run r1-1632 --admit-only` | `ADMIT-OK r1-1632`, exit 0 |
| `python -B .planning/phases/60-single-system-learnability/evidence/launch_phase60_arm.py --sequence rung1 --dry-run` | `ADMIT-OK r1-1632`, `ADMIT-OK r1-851`, `ADMIT-OK r1-4658`, exit 0 |
| `test -z "$(git ls-files .planning/phases/60-single-system-learnability/evidence/arms)"` | Clean, 0 tracked arms files, exit 0 |

## Fingerprints Sealed

- **Run Protocol JSON SHA-256:** `93486d240f129bb5947cddb56d2eb18936ac0cbad7ac0bceeb0af0372b850383`
- **Feasibility Scorecard SHA-256:** `f4b17688c05de68b7aa0f62e452baad751989b0ce2ce36828359a53f9e09444b`
- **Feasibility Scorer Successor SHA-256:** `00edf81d59396fe189d476dd3e69473c4291b71bc6af6171da758f68b61f2bc7`
- **Preflight Records SHA-256:** `7f4fffe8702da3da8307582310221ccc0d4b1abab1156dd48b2c6103c89892cd`
- **Scope Amendment Commit:** `dc3edac0e9ae737b42be276dd9b67e12b8ab8926`

## Next Phase Readiness

- Protocol and preflight are sealed and committed.
- Wave 14 / Plan 60-14 can now launch the Rung-1 data-only arms (`r1-1632`, `r1-851`, `r1-4658`).
