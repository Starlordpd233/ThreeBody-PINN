---
phase: 65-probe-on-the-record-fit-harness
plan: "04"
subsystem: testing
tags: [pinn, diagnostic-probe, reproduction-registration, formatter-rounding-cells, committed-clean-admission, hash-before-load, tdd]

requires:
  - phase: 65-probe-on-the-record-fit-harness
    provides: measure_time_signal (65-01), the guarded Stage-0 data seam and recorded normalizer (65-02), and the production-entry isolation refusals (65-03) this plan's runner composes
  - phase: 60-single-system-learnability
    provides: the seven committed arm records and selected weight files (better_state choices, SHA-256s) the registration pins
  - phase: 65-probe-on-the-record-fit-harness (plan 65-04 task 01)
    provides: the preserved original scripts and scoped historical stdout under evidence/original/
provides:
  - evidence/original/ — both 2026-10-27 exploratory probe scripts byte-exact with verified SHA-256s, the complete verbatim text of exactly the two historical numerical tool outputs, and source-manifest.json with re-derivable scoped provenance including the scratchpad recovery chain
  - evidence/probe/expectations.json — machine expectations: seven arm identities in stable committed-record path order, the 14 init/selected-state rows, every historical token with its exact formatter-defined rounding cell (float-hex endpoints, inclusion, excluded nextafter neighbours), the separate r1-1632 Adam/polish supplement, code/evidence/frozen-source digest pins and the reading rule
  - 65-PROBE-PREDICTION.md — the committed historical expectations page: historical vs runtime distinctions (D-04), measurement definitions (D-05), the immutable exact-formatter reproduction rule and its retained/withdrawn/provenance-limitation/preserved-only/new-measurement branches (D-03/D-07)
  - pinn/verification/diagnostic_probe.py — the read-only DIAG-09 runner with check-registration / run / verify-result CLI, exclusive attempts, no-retry, complete-evidence-record-even-when-figures-fail, and the optimizer interlock
  - pinn/verification/diagnostic_guard.py require_committed_registration — committed-clean admission (tracked/clean scoped to the registration's own enumerated artifacts, exact digests, ancestor-commit proof, ordered arms) shared with the fit registration, before any data resolution, weight deserialization or attempt creation
affects: [65-05, 65-06]

actuals:
  tokens: 65237   # chars/4 over the realized plan diff (260,949 chars, 5,890 insertions across 9 files)
  tasks: 3
  commits: 6      # 4 task commits (e71daf0a, b9645d36, 7255835f, f469e003) + this SUMMARY commit + the state/roadmap metadata commit

tech-stack:
  added: []
  patterns:
    - "Exact formatter equality defines reproduction: each token's acceptance region is its formatter-defined rounding cell (first/last representable doubles as float hex with inclusion and excluded nextafter neighbours), derived by exponential search plus float bisection and cross-checked against the formatter — never a visible-digit-count tolerance"
    - "Committed-clean admission scoped to the registration's own enumerated artifacts: an unrelated dirty file elsewhere in the tree is never a refusal reason, while any tampering with the page, expectations, sources, arm records, code dependencies or pinned protocol refuses with zero opens"
    - "The reading rule is immutable after observation: reproduced/not_reproduced per field, retained/withdrawn(SCOPE-49)/provenance-limitation/preserved_only/new_measurement verdict branches, fixed before any rerun and never repaired by editing it"

key-files:
  created:
    - pinn/verification/diagnostic_probe.py
    - .planning/phases/65-probe-on-the-record-fit-harness/evidence/original/probe_time_signal.py
    - .planning/phases/65-probe-on-the-record-fit-harness/evidence/original/probe_all_arms.py
    - .planning/phases/65-probe-on-the-record-fit-harness/evidence/original/stdout.json
    - .planning/phases/65-probe-on-the-record-fit-harness/evidence/original/source-manifest.json
    - .planning/phases/65-probe-on-the-record-fit-harness/evidence/probe/expectations.json
    - .planning/phases/65-probe-on-the-record-fit-harness/65-PROBE-PREDICTION.md
  modified:
    - pinn/verification/diagnostic_guard.py
    - tests/phase65/test_probe.py

key-decisions:
  - "Reproduction is exact formatter equality against preserved tokens (.2f/.3f/.4f/.3g per the original all-arm formatters, the source formats for the single-arm supplement); every token's exact rounding cell is recorded as float-hex endpoints with boundary inclusion and excluded nextafter neighbours, covering signed zero, decimal-midpoint ties (round-half-even), exponent changes and .3g's omitted trailing zeros — no tolerance is ever widened after results"
  - "require_committed_registration scopes its git tracked/clean checks to the registration's own enumerated artifacts (page, expectations, source manifest/scripts/stdout, arm records, code dependencies, frozen scorer/scorecard, the pinned run protocol revalidating all 33 frozen sources) and proves ancestor-commit membership, so tampering with any registered artifact refuses before any corpus/weight access while unrelated user-owned dirty files never block"
  - "The one shared measure_time_signal serves the probe and the fit logger; preserved-only single-arm columns (moving/spike/skip-siren) are reported verbatim without a second reduction, and other arms' individual deep-layer values are new measurements with raw values and deltas — never invented historical targets"
  - "The CPU float64 seed-42 rerun initialization is labelled a reconstruction, distinct from the historical MPS float32 training initialization (D-04); recorded trained states load only after their committed record and weight SHA-256 agree (weights_only=True, CPU map location), hash-before-load"
  - "A complete probe execution returns a complete evidence record even when figures fail; verify-result determines the registered verdict (retained/withdrawn/provenance-limitation) and verifies historical dependencies against the recorded run commit rather than requiring later source bytes to stay identical"

patterns-established:
  - "Registration-before-rerun chronology: the machine-verified committed registration gate exists in git history before the first original rerun is possible; the next plan (65-05) runs under this gate, not under an executor's assertion that a page exists"
  - "Zero-effect refusal fixtures: temporary git fixtures prove missing/untracked/staged-only/dirty/changed-dependency registrations refuse with zero open/load calls, and a matching committed fixture passes; the probe-only optimizer interlock refuses construction/steps with counted attempts and parameter digests around every measurement"

requirements-completed: []   # DIAG-09 and INST-08 stay open: this plan registers the reproduction and proves the gates synthetically; plan 65-05 performs the real seven-arm rerun under the committed gate and the logger reproduction (INST-08c) lands with the fit work

coverage:
  - id: D1
    description: "Both original exploratory probe scripts are preserved byte-exact under evidence/original/ with SHA-256s re-verified against the context hashes (16db5c8c…, a4dea7d0…), the complete verbatim text of exactly the two historical numerical tool outputs (toolu_01PUFNWxrDDsVrU8DTCH4tX3, toolu_01NHGWRv6pEQCJmqeAXxqonK) is preserved with precision/signed zero/timestamps, source-manifest.json records re-derivable scoped provenance (session, lines 332/353, message uuids, hashes, byte counts, recovery chain), the 14 all-arm state rows and the distinct r1-1632 Adam/polish supplement are validated, and the scripts are never imported or executed"
    requirement: DIAG-09
    verification:
      - kind: unit
        ref: "tests/phase65/test_probe.py#HistoricalSourceTests"
        status: pass
    human_judgment: false
  - id: D2
    description: "The exact-reproduction and registration gates are implemented and synthetic-tested: formatter-defined rounding cells with exact representable endpoints and nextafter neighbours (signed zero, ties, exponent changes, .3g omitted trailing zeros), the immutable reading rule with retained/withdrawn/provenance-limitation/preserved_only/new_measurement branches, require_committed_registration refusing missing/untracked/staged-only/dirty/changed-dependency registrations with zero opens while a matching committed registration passes and unrelated dirty files never refuse, exclusive attempts, interrupted attempts never publishing, complete records even when figures fail, the optimizer interlock, and the check-registration/run/verify-result CLI"
    requirement: DIAG-09
    verification:
      - kind: unit
        ref: "tests/phase65/test_probe.py#FormatterCellTests"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_probe.py#RegistrationAdmissionTests"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_probe.py#ProbeRunGateTests"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_probe.py#OptimizerInterlockTests"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_probe.py#ReadingRuleTests"
        status: pass
      - kind: unit
        ref: "tests/phase65/test_probe.py#RegistrationContentTests"
        status: pass
    human_judgment: false
  - id: D3
    description: "The registration (65-PROBE-PREDICTION.md + evidence/probe/expectations.json + all dependencies) is committed (evidence(65), f469e003) before any rerun, and the read-only check-registration command succeeds against the committed tree, reporting the registration commit and every artifact hash with zero corpus/weight opens and no probe result or attempt created"
    requirement: DIAG-09
    verification:
      - kind: unit
        ref: "tests/phase65/test_probe.py#CheckRegistrationTests"
        status: pass
      - kind: other
        ref: "command: python -B -m pinn.verification.diagnostic_probe check-registration --registration .planning/phases/65-probe-on-the-record-fit-harness/evidence/probe/expectations.json -> CHECK-REGISTRATION-OK registration-commit=f469e0031e7de3046881ce26a9865cc244d5a6f9, exit 0, pre/post git status identical"
        status: pass
    human_judgment: false

duration: ~1h 30m total (tasks 01-03 in the interrupted prior executor session 13:26-14:43 CDT; verification and close-out in this resume session from 14:48 CDT)
completed: 2026-10-29
status: complete
---

# Phase 65 Plan 04: Probe on the Record — Registration & Gates Summary

**The 2026-10-27 exploratory probe is now on the record before any rerun: preserved original scripts and scoped historical stdout with re-derivable provenance, a committed registration fixing every historical token's exact formatter rounding cell and the immutable reading rule, and a machine-verified committed-clean admission gate that refuses tampering with zero opens.**

## Performance

- **Duration:** ~1h 30m across two sessions (see Deviations — continuation execution)
- **Started:** 2026-10-29T13:26:25-0500 (first task commit; prior session)
- **Resumed:** 2026-10-29T14:48:00-0500 (this session: verification + close-out)
- **Tasks:** 3 of 3
- **Files modified:** 10 (7 created, 3 modified) plus this SUMMARY, STATE.md and ROADMAP.md

## Accomplishments

- Task 65-04-01 preserved the two original exploratory scripts byte-exact under `evidence/original/` (SHA-256s re-verified against the context hashes: `probe_time_signal.py` `16db5c8c…a4f` 4040 bytes, `probe_all_arms.py` `a4dea7d0…4c8` 3145 bytes; never imported or executed), extracted the complete verbatim text of exactly the two historical numerical tool outputs (3077 and 1771 bytes, with timestamps, precision and signed zero), and recorded re-derivable scoped provenance in `source-manifest.json` — including the recovery chain for the lost scratchpad originals (restored by the orchestrator from the durable file-history store, snapshots `85ac6b7d6b97691b@v2` / `4f2e7a23e12db4e1@v2`, re-hashed byte-exact). `HistoricalSourceTests` validate the hashes, both messages, the 14 all-arm state rows and the distinct r1-1632 Adam/polish supplement.
- Task 65-04-02 (TDD) implemented `pinn/verification/diagnostic_probe.py` (1128 lines) and `require_committed_registration` in `pinn/verification/diagnostic_guard.py` (+231): exact formatter equality against the preserved tokens with every token's rounding cell derived and cross-checked (float-hex endpoints, inclusion, excluded `nextafter` neighbours; signed zero, ties, exponent changes, `.3g` omitted trailing zeros), the immutable reading rule with all verdict branches, committed-clean admission scoped to the registration's own artifacts with ancestor-commit proof and exact digests, exclusive attempt claims, no automatic retry, complete evidence records even when figures fail, `reproduction.stdout.txt` beside `reproduction.json`, the probe-only optimizer interlock, logger parity via `diagnostic_fit.log_similarity`, and the `check-registration` / `run` / `verify-result` CLI. 39 planned-behavior RED tests were committed first (machine-verified `RED_EVIDENCE_OK`) and passed after GREEN.
- Task 65-04-03 committed the registration — `65-PROBE-PREDICTION.md` and `evidence/probe/expectations.json` (2975 lines) with the seven arm identities in stable committed-record path order, the 14 init/selected-state rows, every historical token's exact rounding cell, the separate single-arm supplement, code/evidence/frozen-source digest pins and the reading rule — as `evidence(65)` commit `f469e003`, then proved live admission read-only: `check-registration` prints `CHECK-REGISTRATION-OK registration-commit=f469e003…` with every artifact hash, exits 0, opens no corpus/weight file and creates no probe result or attempt. No real probe ran in this plan; the seven-arm rerun belongs to plan 65-05 under this committed gate.

## Task Commits

Each task was committed atomically through `scripts/agent-commit` (`GIT_AGENT_ID=gsd-executor-65-04`, explicit owned paths):

1. **Task 1: preserve original scripts and scoped numerical output** — `e71daf0a` (evidence(65-04))
2. **Task 2: implement exact reproduction and registration gates (TDD)** — `b9645d36` (test, RED) + `7255835f` (feat, GREEN)
3. **Task 3: commit the registration and prove live admission without running** — `f469e003` (evidence(65))

**Plan metadata:** this SUMMARY commit and the following state/roadmap commit (docs).

## Files Created/Modified

- `pinn/verification/diagnostic_probe.py` — the read-only DIAG-09 runner: registration validation, exact formatter cells, reading rule, attempts, interlock, CLI
- `pinn/verification/diagnostic_guard.py` — `require_committed_registration`, shared with the fit registration
- `tests/phase65/test_probe.py` — `HistoricalSourceTests`, `MeasurementSemanticsTests`, `MeasurementRefusalTests`, `FormatterCellTests`, `ReadingRuleTests`, `RegistrationAdmissionTests`, `CheckRegistrationTests`, `ProbeRunGateTests`, `OptimizerInterlockTests`, `ProbeCliTests`, `RegistrationContentTests`
- `.planning/phases/65-probe-on-the-record-fit-harness/evidence/original/{probe_time_signal.py,probe_all_arms.py,stdout.json,source-manifest.json}` — preserved sources and scoped output with provenance
- `.planning/phases/65-probe-on-the-record-fit-harness/evidence/probe/expectations.json` — machine expectations (tokens, cells, digests, reading rule)
- `.planning/phases/65-probe-on-the-record-fit-harness/65-PROBE-PREDICTION.md` — the committed expectations page

## Verification Commands and Outcomes

- Task 1 verify: `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase65.test_probe.HistoricalSourceTests -v` → 5 tests OK, exit 0 (re-run at final HEAD in this session)
- Task 2 verify: `… -m unittest tests.phase65.test_probe -v` → 72 tests OK, exit 0 (re-run at final HEAD in this session)
- Task 3 verify: `… -m pinn.verification.diagnostic_probe check-registration --registration .planning/phases/65-probe-on-the-record-fit-harness/evidence/probe/expectations.json` → `CHECK-REGISTRATION-OK registration-commit=f469e0031e7de3046881ce26a9865cc244d5a6f9` listing the page (688958f1…), expectations (4f8cd085…), both original scripts (16db5c8c…, a4dea7d0…), stdout/source-manifest, code dependencies, frozen scorer/scorecard and all seven arm records; exit 0; pre/post `git status` identical (zero probe result/attempt created, zero corpus/weight opens)
- Plan-level: `… -m unittest discover -s tests/phase65 -p 'test_*.py'` → 168 tests OK, 11.6 s; `git diff --check` clean; `load_protocol()` revalidates all 33 pinned module digests without `ProtocolDrift`
- Preserved originals never executed: `HistoricalSourceTests` hash bytes only; no import/exec/subprocess/runpy reference to `evidence/original/` exists in tests or code; no reproduction/attempt artifact exists anywhere; the pre-existing gitignored `runs/probe-run` / `runs/probe-mem-b` trees date from v2.0/v2.2 (July/September) and are unrelated
- Pinned files untouched: `split_allowlist.py`, `learnability_data.py` and the 33 frozen modules unmodified (digest revalidation passed)

## Decisions Made

- **Rounding cells, not tolerances:** each historical token's acceptance region is its formatter-defined rounding cell, recorded as first/last representable doubles in float hex with boundary inclusion and the excluded `nextafter` neighbours, derived by exponential search plus float bisection. This makes signed zero, round-half-even ties, exponent changes and `.3g`'s omitted trailing zeros exact, and visible-digit counting is never used to widen acceptance.
- **Admission scoping:** `require_committed_registration` checks tracked/clean against HEAD only for the registration's own enumerated artifacts, so user-owned unrelated working-tree changes elsewhere never trigger a false refusal (the dispatch's required scoping), while any change to a registered artifact refuses with zero opens.
- **Verdict branches fixed before observation:** retained / withdrawn (with a SCOPE-49 proposal to the owner) / provenance-limitation (separately reported, never a fabricated failure or success) / preserved-only (single-arm moving/spike/skip-siren columns kept verbatim, no second reduction) / new-measurement (individual deep-layer values for arms other than r1-1632, with raw values and deltas, never invented historical targets).
- **Chronology labelling:** the rerun's CPU float64 seed-42 initialization is registered as a reconstruction, never as the historical MPS float32 training initialization (D-04); the output-rate comparator is labelled as network-autograd over gold finite differences in the same tau coordinate (D-05); low mean neighbour cosine is registered as association only (D-07).

## Deviations from Plan

### Process deviations

**1. [Process - Continuation] Plan executed across two executor sessions**
- **Found during:** this resume session
- **Issue:** the prior `gsd-executor-65-04` session executed all three tasks with their commits (`e71daf0a`, `b9645d36`, `7255835f`, `f469e003`) but was interrupted before the close-out (no SUMMARY, STATE/ROADMAP not yet updated) — the illegal partial-plan state the close-out invariant reserves a resume to complete
- **Fix:** this session did NOT redo any task; it independently re-ran all three task verify commands plus the plan-level verification at the committed HEAD (working tree clean, so HEAD is the verified tree), confirmed the check-registration read-only run against the committed registration, and completed SUMMARY/STATE/ROADMAP
- **Files modified:** this SUMMARY, `.planning/STATE.md`, `.planning/ROADMAP.md`
- **Verification:** all verify outcomes listed above, at `f469e003` + close-out commits
- **Committed in:** the SUMMARY and metadata commits

**2. [Process - Runtime] Executor ran under the general-purpose runtime with the gsd-executor role definition**
- **Found during:** both sessions
- **Issue:** the orchestrator dispatched the executor through the general-purpose agent runtime with the `gsd-executor` role definition loaded (role contract followed: atomic task commits, deviation rules, checkpoint protocol), rather than a named `gsd-executor` subagent type
- **Fix:** none needed; recorded honestly here and in the task commits' `Agent-Assisted-By: gsd-executor-65-04 (GLM-5.3-Flash via general-purpose runtime)` trailers
- **Files modified:** none
- **Verification:** commit trailers on `e71daf0a`, `b9645d36`, `7255835f`, `f469e003`
- **Committed in:** n/a (process provenance note)

**3. [Precondition - Recovery] Task 1's temporary sources were lost to macOS cleanup and restored before execution**
- **Found during:** Task 1 (prior session)
- **Issue:** the precondition's temporary scratchpad scripts were deleted by macOS tmp cleanup
- **Fix:** the orchestrator restored both scripts from the durable session file-history store (snapshots `85ac6b7d6b97691b@v2`, `4f2e7a23e12db4e1@v2`) and re-verified them byte-exact against the plan's expected SHA-256s; the recovery chain is recorded in `source-manifest.json#recovery_provenance` and the two historical tool messages were confirmed present at the cited session lines 332/353
- **Files modified:** `evidence/original/source-manifest.json` (recovery_provenance block)
- **Verification:** `HistoricalSourceTests` hash checks pass at HEAD
- **Committed in:** `e71daf0a`

---

**Total deviations:** 3 process/provenance entries (1 continuation, 1 runtime provenance, 1 precondition recovery); no auto-fixed code defects.
**Impact on plan:** none on content — the plan's tasks were executed exactly as written; the deviations are execution-chronology and provenance records required for honest hand-off.

## TDD Gate Compliance

Task 65-04-02 (`tdd="true"`) committed `test(65-04)` RED `b9645d36` before `feat(65-04)` GREEN `7255835f`; the RED evidence was machine-verified `RED_EVIDENCE_OK` via `check tdd-red-evidence` at commit time (target test `FormatterCellTests.test_cell_endpoints_are_exact_representable_values`; 64 tests, 25 pass, 39 fail — all 39 failures on planned behavior via assertive helpers, never import errors). No REFACTOR commit: the GREEN implementation needed no post-GREEN cleanup. Tasks 65-04-01 and 65-04-03 are `type="auto"` evidence tasks with their own verify commands passing.

## Issues Encountered

- Cosmetic: three task-commit bodies contain the attribution line twice (once in the message text naming the runtime, once as the hook-appended `Agent-Assisted-By` trailer). Harmless and left as-is (no history rewrite); the trailer value satisfies the attribution policy.
- Pre-existing environment gap (out of scope, unchanged): `tests/phase49/test_gate03_resume.py` fails to import in the `pinn-train` environment (no pytest); unrelated to this plan and outside every verify command.

## User Setup Required

None — no external service configuration; everything runs on the local `pinn-train` environment.

## Known Stubs

None — every delivered path is real; no placeholder, TODO or unwired data source remains. The probe's real measurement path is unexercised by design: this plan proves it synthetically only, and plan 65-05 performs the registered seven-arm rerun under the committed gate.

## Next Phase Readiness

- The registration gate is live and machine-verified: plan 65-05's `run` command admits only through `require_committed_registration` against the committed `f469e003` tree, loads each arm's recorded trained state only after its committed record and weight SHA-256 agree, and writes a complete evidence record whose verdict `verify-result` computes from the immutable reading rule.
- The fit registration (65-05/65-06) shares `require_committed_registration`; the logger must reproduce DIAG-09 on the registered r1-1632 polish state before its training trace is trusted (D-10).
- No blocker. DIAG-09 and INST-08 stay open (later plans own their completion); the held-out evaluation remains unspent; no real probe or corpus access occurred in this plan.

---
*Phase: 65-probe-on-the-record-fit-harness*
*Completed: 2026-10-29*

## Self-Check: PASSED

All ten key files exist on disk (`diagnostic_probe.py`, `diagnostic_guard.py`, `test_probe.py`, the four `evidence/original/` artifacts, `evidence/probe/expectations.json`, `65-PROBE-PREDICTION.md`, this SUMMARY); all four task commits (`e71daf0a`, `b9645d36`, `7255835f`, `f469e003`) are in history with the TDD gate order present (`test(65-04)` RED before `feat(65-04)` GREEN); all three task verify commands and the plan-level verification (168-test suite, `check-registration` read-only with zero side effects, `git diff --check`, 33 pinned digests) exit 0 at the committed HEAD this SUMMARY documents.
