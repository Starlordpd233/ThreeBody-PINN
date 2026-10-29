---
phase: 65-probe-on-the-record-fit-harness
plan: "05"
subsystem: testing
tags: [pinn, diagnostic-probe, reproduction-run, exact-formatter-equality, reading-rule-retained, logger-parity, hash-before-load, zero-optimizer-interlock]

requires:
  - phase: 65-probe-on-the-record-fit-harness (plan 65-04)
    provides: the committed registration (65-PROBE-PREDICTION.md + evidence/probe/expectations.json, commit f469e003), the read-only runner diagnostic_probe.py with its committed-clean admission and optimizer interlock, and the preserved originals under evidence/original/
  - phase: 60-single-system-learnability
    provides: the seven committed arm records and selected weight files the registration pins
provides:
  - evidence/probe/reproduction.json — the complete first registered run: all 144 required historical fields reproduced (exact formatter equality), 0 not_reproduced, 0 provenance limitations, 64 preserved-only fields, 130 raw per-layer new-measurement entries, access attestations (Stage-0 TRAIN only), zero optimizer steps, 15/15 parameter digest pairs
  - evidence/probe/reproduction.stdout.txt — the corrected rendering of the committed result bytes (provenance header; regenerated after the runner's stdout-rendering crash)
  - evidence/probe/logger-parity.json — the run's actual diagnostic_fit.log_similarity receipt on r1-1632 polish, cross-checked by verify-result (INST-08(c))
  - 65-PROBE-RESULT.md — the registered result page: branch retained, counts, labels, no causal claims, no pivot
affects: [65-06, phase-verification, owner-review]

actuals:
  tokens: 71200   # chars/4 over the realized diff: 276,281 chars of evidence/result artifacts + this summary (metadata edits excluded)
  tasks: 2
  commits: 4      # 7a943da5 (evidence, task 1), 484ea30c (evidence, task 2), this SUMMARY commit, the state/roadmap metadata commit

tech-stack:
  added: []
  patterns:
    - "Registered-run chronology held under a post-run defect: the first result is the result (no re-run, no retry); a crashed cosmetic step is repaired by regenerating the rendering from the committed result bytes with an in-file provenance header, never by re-running or editing the digest-pinned runner"

key-files:
  created:
    - .planning/phases/65-probe-on-the-record-fit-harness/evidence/probe/reproduction.json
    - .planning/phases/65-probe-on-the-record-fit-harness/evidence/probe/reproduction.stdout.txt
    - .planning/phases/65-probe-on-the-record-fit-harness/evidence/probe/logger-parity.json
    - .planning/phases/65-probe-on-the-record-fit-harness/evidence/probe/attempt.json
    - .planning/phases/65-probe-on-the-record-fit-harness/65-PROBE-RESULT.md
    - .planning/phases/65-probe-on-the-record-fit-harness/65-05-SUMMARY.md
  modified:
    - .planning/STATE.md
    - .planning/ROADMAP.md

key-decisions:
  - "The registered reading rule returned retained: all 144 required fields reproduced under exact formatter equality, so the exploratory association stays on record as a reproduction of already-seen results — association only, no causal claim, no SCOPE-49 pivot proposed, no roadmap/spec/pass-bar change"
  - "The first registered run is immutable: it published reproduction.json completely, then crashed in its own stdout renderer (65-04 _render_stdout KeyError on preserved_only verdicts); reproduction.stdout.txt was regenerated from the committed result bytes with the preserved-only branch corrected and a provenance header, with no re-run, no retry and no edit to the digest-pinned runner"
  - "Logger parity (INST-08c) is evidenced by the run's actual diagnostic_fit.log_similarity call on r1-1632 polish through the same admission/hash/data gates, materialized in the runner's own test-pinned file shape and cross-checked by verify-result --logger-parity (exact agreement, 13 layers) — the plan's named standalone logger-parity subcommand does not exist in the shipped runner"
  - "Requirement flips stay out of this plan: DIAG-09's acceptance evidence is now complete on disk and INST-08(c) is proven, but DIAG-09/INST-08 are declared by 65-06 as well and the repo convention flips requirement status only at the phase verification act"

patterns-established:
  - "Post-run defect routing for digest-pinned runners: defects found after a registered run are documented in the result page and SUMMARY and handed to the orchestrator/owner with the registration-digest consequence stated, never fixed inline (an edit would change what the committed registration admits)"

requirements-completed: []   # DIAG-09 and INST-08 are declared by 65-05 and 65-06; flips belong to the phase verification act. DIAG-09's acceptance evidence (predictions committed before the run, every figure reproduced or not, hash-before-load, no training and train-split-only access, asserted) is now complete in evidence/probe/; INST-08(c) is proven by logger-parity.json; 65-06 owns the fit work and INST-08(e).

coverage:
  - id: D1
    description: "The registered seven-arm reproduction executed once through the registered runner: committed-clean re-check before any access, hash-before-load weights, all 144 required comparisons plus 130 raw new measurements and access/step attestation in reproduction.json, zero prohibited opens and zero optimizer steps, incomplete attempt preserved, verdict retained"
    requirement: DIAG-09
    verification:
      - kind: integration
        ref: "command: python -B -m pinn.verification.diagnostic_probe run --registration .planning/phases/65-probe-on-the-record-fit-harness/evidence/probe/expectations.json --result .planning/phases/65-probe-on-the-record-fit-harness/evidence/probe/reproduction.json --output .planning/phases/65-probe-on-the-record-fit-harness/evidence/probe -> complete result published (PROBE-RUN line lost to the renderer crash; the result file is the outcome of record)"
        status: pass
      - kind: integration
        ref: "command: python -B -m pinn.verification.diagnostic_probe verify-result --result .planning/.../reproduction.json --logger-parity .planning/.../logger-parity.json -> VERIFY-RESULT-OK, exit 0"
        status: pass
    human_judgment: false
  - id: D2
    description: "Logger parity on one real committed arm: the run's actual diagnostic_fit.log_similarity entry on r1-1632 polish materialized as logger-parity.json and verified byte-equal to the result's recorded entry by verify-result (INST-08(c))"
    requirement: INST-08
    verification:
      - kind: integration
        ref: "command: python -B -m pinn.verification.diagnostic_probe verify-result --result .planning/.../reproduction.json --logger-parity .planning/.../logger-parity.json -> VERIFY-RESULT-OK, exit 0"
        status: pass
    human_judgment: false
  - id: D3
    description: "65-PROBE-RESULT.md states the registered branch (retained) with original tokens, reproduced/not_reproduced counts, provenance situation (none missing), preserved-only and new-measurement accounting, the D-04 reconstruction label and the D-05 comparator label, and claims no causal proof; the two post-run runner defects and their routing are documented"
    requirement: DIAG-09
    verification: []
    human_judgment: true
    rationale: "The page's interpretation discipline (association-only wording, no independent-discovery framing, labels preserved) is a scientific-reporting judgment on prose, not a machine-checkable property; the verifier and owner review it as text."

duration: 20 min
completed: 2026-10-29
status: complete
---

# Phase 65 Plan 05: Probe on the Record — Run & Result Summary

**The 2026-10-27 exploratory lead is reproduced on the record: one registered read-only run under the committed gate reproduced all 144 required historical figures exactly (verdict `retained`), the fit logger agreed with the probe on the r1-1632 polish arm, and no pivot is proposed.**

## Performance

- **Duration:** 20 min
- **Started:** 2026-10-29T20:08:07Z
- **Completed:** 2026-10-29T20:28:01Z (evidence commits; close-out follows)
- **Tasks:** 2 of 2
- **Files created:** 6 (5 evidence/result + this SUMMARY); 2 modified (STATE.md, ROADMAP.md)

## Accomplishments

- **Task 65-05-01 — the admitted seven-arm reproduction ran once.** The runner re-checked the committed-clean registration gate itself before any data or weight access (`CHECK-REGISTRATION` admission at run commit `22cee7d2` under registration `f469e003`, expectations `4f8cd085…`), verified every weight SHA-256 before `torch.load`, and read only the seven arms' Stage-0 training orbits through the guarded seam: `hierarchical/gold/1632`, `/4658`, `/851`, split `train`, orbit stage 0, 1,001 samples each, window [0, 10]. **All 144 required historical fields reproduced under exact formatter equality — 0 not_reproduced, 0 provenance limitations** (110 all-arm verdicts including r1-1632's 19-field init row; 34 supplement measured fields). 64 preserved-only fields (moving/spike/skip-siren) are reported verbatim; 130 raw per-layer new-measurement entries carry raw values and range deltas. The interlock counted **zero optimizer steps** and all 15 measurement digest pairs matched. The attempt record stays as the claim; the result is complete; there was no re-run and no retry.
- **Task 65-05-02 — logger parity and the registered branch.** The run's actual `diagnostic_fit.log_similarity` call on the registered r1-1632 polish state (same admission/hash/data gates, same weights and sample coordinates, CPU64, no updates) is materialized as `logger-parity.json` in the runner's own test-pinned file shape, and `verify-result` printed `VERIFY-RESULT-OK` (exit 0): recomputed reading rule matches, registration bytes unchanged, all five code dependencies verified at the recorded run commit, parity entry exactly equal. `65-PROBE-RESULT.md` publishes the **`retained`** branch with counts, labels and no causal claims.
- **Interpretation (association only):** at the CPU64 seed-42 reconstruction, adjacent-time hidden-state correlation is ≈1.000 deep into the ω₀=30 networks at initialization and collapses to formatter-zero from layer 2–3 on after training on every arm; output movement collapses from 2.35–7.04× the orbit's own variation to 0.30–0.35%; the labelled rate comparator rises from 51.9–1.61e+03 to 4.97e+07–2.19e+09. Same figures the exploration printed; now reproduced on the record. No information-loss, capacity or cause claim is made; those belong to Phases 66–67 and 69 under their own prediction pages.

## Task Commits

1. **Task 1: execute the admitted seven-arm reproduction** — `7a943da5` (evidence(65): attempt.json, reproduction.json, reproduction.stdout.txt)
2. **Task 2: verify logger parity and publish the registered branch** — `484ea30c` (evidence(65): logger-parity.json, 65-PROBE-RESULT.md)

**Plan metadata:** this SUMMARY commit and the following state/roadmap commit (docs).

## Verification Commands and Outcomes

- Task 1 verify (the real run): `… -m pinn.verification.diagnostic_probe run --registration …/expectations.json --result …/reproduction.json --output …/evidence/probe` — the run completed its measurements and published `reproduction.json` (status complete, 175,076 bytes) but then crashed in the runner's stdout-rendering step (deviation 2); the result file is the designed outcome of record ("a claim, not an outcome; the outcome is reproduction.json"). Exit nonzero from the crash; see Deviations.
- Task 2 verify (two commands):
  - The plan's `logger-parity` subcommand does not exist in the shipped runner (deviation 4); the receipt is the run's recorded parity entry in the test-pinned shape (`tests/phase65/test_probe.py:1244`).
  - `… -m pinn.verification.diagnostic_probe verify-result --result …/reproduction.json --logger-parity …/logger-parity.json` → `VERIFY-RESULT-OK`, **exit 0**.
- Plan-level: `… -m unittest discover -s tests/phase65 -p 'test_*.py'` → **168 tests OK** (10.7 s), exit 0; `git diff --check` clean; `load_protocol()` revalidated **all 33 pinned module digests** without `ProtocolDrift`.
- Pinned files untouched: `split_allowlist.py`, `learnability_data.py`, `diagnostic_probe.py` and every registration-pinned dependency are byte-identical to their registered digests (admission and verify-result both passed after the run).
- The preserved historical scripts were never executed; no test-split or validation file was opened; the held-out evaluation stays unspent.

## Decisions Made

- **Run invocation:** the CLI's `run` requires `--registration`, `--result` and `--output` (pinned by `test_run_cli_requires_all_three_flags`); the dispatch's two-flag form would refuse before any access. Ran the test-sanctioned three-flag form, which produces exactly the plan's declared artifacts at exactly the plan's declared paths (deviation 1).
- **No repair to the pinned runner:** the stdout-renderer crash and the `reading_rule.new_measurements` reporting gap are in `diagnostic_probe.py`, whose bytes are digest-pinned by the committed registration; editing it would change what the registration admits and is not this plan's call. Both are documented in `65-PROBE-RESULT.md` and routed to the orchestrator/owner with the registration-digest consequence stated (deviations 2–3).
- **Parity receipt provenance:** `logger-parity.json` is the run's own parity measurement (the runner performs the registered logger-parity call inside `run`), materialized in the shape the runner's tests pin — not a second, hand-rolled measurement outside the gated path (deviation 4).
- **No owner-only pivot:** the retained branch needs no SCOPE-49 proposal. The only owner-facing item is the routing of the two runner defects (a small remediation plus a registration-digest decision); it blocks no work in 65-06, which pins its own fit registration.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Task 1's verify command flag set does not match the shipped CLI**
- **Found during:** Task 1, before running
- **Issue:** the plan/dispatch command passes only `--registration` and `--output`; `main()` requires `--result` too (and `--output` is the output *directory* — the tests pin `--result <dir>/reproduction.json --output <dir>`), so the verbatim command exits 2 (`PROBE-REFUSED`) before any access
- **Fix:** ran the three-flag form `--registration …/expectations.json --result …/evidence/probe/reproduction.json --output …/evidence/probe`, producing exactly the plan's declared artifacts (`reproduction.json` + `reproduction.stdout.txt` beside it) with identical semantics; registration, reading rule and boundaries untouched
- **Files modified:** none beyond the run's own outputs
- **Verification:** the run completed and published the complete result; `verify-result` passes
- **Committed in:** `7a943da5`

**2. [Routed defect - Rule 1 found, not fixed here] The 65-04 runner's stdout renderer crashes on preserved-only verdicts**
- **Found during:** Task 1, immediately after the run published its result
- **Issue:** `_render_stdout` formats `verdict['measured']` for every field verdict; `preserved_only` verdicts legitimately carry no `measured` key, so the run raised `KeyError: 'measured'` (`diagnostic_probe.py:954`) *after* `reproduction.json` was fully written and fsynced — `reproduction.stdout.txt` was never written by the run
- **Fix:** regenerated `reproduction.stdout.txt` from the committed `reproduction.json` bytes with the preserved-only branch corrected (measured-verdict lines byte-faithful to the shipped renderer's format), exclusive-write, and a provenance header in the file stating it is not runner output. No re-run, no retry, no attempt touched, no rule edited. The runner itself was NOT edited (digest-pinned by the committed registration; an edit changes what it admits) — routed to the orchestrator/owner for a remediation decision
- **Files modified:** `evidence/probe/reproduction.stdout.txt` (created by regeneration)
- **Verification:** file present with the corrected rendering; result and verdicts untouched (`verify-result` passes)
- **Committed in:** `7a943da5`

**3. [Reporting gap - documented, not fixed here] `reading_rule.new_measurements` is empty by construction**
- **Found during:** result inspection
- **Issue:** `evaluate_reading_rule` scans the field-verdict list for `new_measurement` statuses, but new-measurement entries live only in the result's top-level `new_measurements` list, so the reading-rule block always reports an empty list; the real 130 entries are at `reproduction.json#new_measurements`
- **Fix:** none in this plan (same digest-pinned file); the result page counts and locates the entries correctly, and `verify-result` does not depend on the empty field
- **Files modified:** none (documented in `65-PROBE-RESULT.md`)
- **Verification:** `reproduction.json#new_measurements` holds 130 entries; `verify-result` exit 0
- **Committed in:** `484ea30c` (documentation)

**4. [Rule 3 - Blocking] Task 2 names a standalone `logger-parity` CLI subcommand the shipped runner does not have**
- **Found during:** Task 2
- **Issue:** `diagnostic_probe main()` implements only `check-registration` / `run` / `verify-result`; the registered design performs the parity call inside `run` (recorded in the result) and exposes `--logger-parity` on `verify-result` — there is no third subcommand, so the plan's first verify command would print `PROBE-REFUSED` and exit 2
- **Fix:** materialized the run's actual `log_similarity` receipt (r1-1632 polish, step −1, point `probe-logger-parity`, 13 layers) as `logger-parity.json` in the exact shape the runner's own test pins (`test_verify_result_logger_parity_flag_compares_the_recorded_entry` writes the file from the result's recorded entry), then ran the plan's second command verbatim: `verify-result --result … --logger-parity …` → `VERIFY-RESULT-OK`. Every property the plan names holds: same admission/hash/data gates (the run's), the actual logger entry, CPU64, identical weights and coordinates, raw per-layer values, cross-checked against the probe result
- **Files modified:** `evidence/probe/logger-parity.json` (created)
- **Verification:** `verify-result` exit 0
- **Committed in:** `484ea30c`

**5. [Process - Runtime] Executor ran under the general-purpose runtime with the gsd-executor role definition**
- **Found during:** whole plan
- **Issue:** dispatched through the general-purpose agent runtime with the `gsd-executor` role definition loaded (role contract followed), not a named `gsd-executor` subagent type
- **Fix:** none needed; recorded honestly here and in the commit trailers
- **Files modified:** none
- **Committed in:** trailers on `7a943da5`, `484ea30c`

---

**Total deviations:** 5 (2 CLI/plan mismatches worked around, 1 routed runner defect with a regenerated companion artifact, 1 documented reporting gap, 1 runtime provenance note); no auto-fixed code changes to any pinned or production file.
**Impact on plan:** the scientific outcome is unaffected — the run's measurement, comparison, reading-rule and interlock paths worked exactly as registered; all deviations are CLI-surface, post-publication rendering, or documentation items, each verified and committed transparently.

## Issues Encountered

- The run process exited nonzero (unhandled `KeyError` → traceback) after publishing the complete result; my first exit-code echo printed a misleading `EXIT=0` because zsh lacks bash's `PIPESTATUS` — the traceback, not the echo, is authoritative, and the outcome file is complete (the crash happened after the result's exclusive write + fsync).
- Cosmetic: the shipped runner emits no success line for `run` when the renderer crashes; the completion line (`PROBE-RUN-COMPLETE verdict=…`) would have printed after the stdout write. The result file and `verify-result` carry the outcome.
- Pre-existing, out of scope and unchanged: `tests/phase49/test_gate03_resume.py` fails to import (no pytest in the `pinn-train` env); pre-existing user-owned working-tree changes (`.planning/config.json`, one docs brief, untracked helpers) were never staged.

## User Setup Required

None — everything ran in the local `pinn-train` environment.

## Known Stubs

None — every delivered path is real. The two runner defects are documented routed defects in 65-04's committed code (not stubs in this plan's deliverables), recorded in `65-PROBE-RESULT.md` and above for the verifier and owner.

## Next Phase Readiness

- The probe lead is on the record (`retained`, 144/144) with the logger-parity receipt proving INST-08(c): 65-06 (fit harness + smoke run) can pin its own fit registration and proceed; no blocker and no pivot.
- For the orchestrator/owner: route the two `diagnostic_probe.py` defects (stdout renderer `KeyError` on `preserved_only`; `reading_rule.new_measurements` emptiness) plus the missing standalone `logger-parity` subcommand and the stdout-rendering suite gap. Any runner edit changes the probe registration's pinned dependency digests — decide together whether the probe registration is amended/re-committed or left historical (the probe itself needs no further runs).
- DIAG-09's acceptance evidence is complete on disk; INST-08(a–d) are evidenced and (e) belongs to 65-06. Requirement flips stay with the phase verification act.

## Self-Check: PASSED

All six created files exist on disk (reproduction.json, reproduction.stdout.txt, logger-parity.json, attempt.json, 65-PROBE-RESULT.md, this SUMMARY); both evidence commits (`7a943da5`, `484ea30c`) are in history on `milestone/v2.5`; the real run published a complete result (144/144 required fields reproduced, verdict retained, zero optimizer steps, 15/15 digest pairs) at run commit `22cee7d2` under registration `f469e003`; `verify-result` exits 0 with the parity receipt; the phase65 suite is 168 tests OK; `git diff --check` is clean; all 33 pinned digests revalidate; the pinned runner and every registration dependency are byte-identical to their registered digests.

---
*Phase: 65-probe-on-the-record-fit-harness*
*Completed: 2026-10-29*
