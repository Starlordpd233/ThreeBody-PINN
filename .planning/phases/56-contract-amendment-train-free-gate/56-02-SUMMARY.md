---
phase: 56-contract-amendment-train-free-gate
plan: 02
subsystem: verification
tags: [gate-04, causal-weights, gap-56-01, front-capability, operator-cli, evidence-record, tdd]

requires:
  - phase: 56-01
    provides: "the frozen public contract (Gate04Verdict / Gate04CaseResult / VERDICT_PASS / VERDICT_BLOCK / gate04_verdict / run_gate / compute_r_ref / evaluate_case / write_r_ref_artifact), the probe's ratified_causal_weights and _front_idx, and the present-but-None condition_ii/iii diagnostic slots this plan fills"
provides:
  - "condition_ii_verdict(weights) — always raises NotImplementedError naming GAP-56-01; nothing else in the module calls it"
  - "condition_ii_diagnostics(weights, floor) — descriptive statistics only (CV of the tail, monotonicity, dynamic-range decades, non-floor count), status UNRATIFIED, no comparison"
  - "condition_iii_diagnostics(raw_bin_means, r_ref, ...) + CONDITION_III_DIAGNOSTIC_FACTORS — the front-response record (uniform and late-bin-only reduction sweeps) via ratified_causal_weights and the probe's _front_idx, no pass threshold"
  - "evaluate_case now populates both diagnostic fields on every Gate04CaseResult"
  - "pinn/verification/gate04_train_free.py main(argv=None) — the operator CLI (--precision/--device/--cases-config/--evidence-root/--r-ref-path), EVIDENCE_SCHEMA_VERSION, EVIDENCE_TOP_LEVEL_KEYS"
  - "pinn/verification/artifacts/r_ref_stage0.json refreshed from a real six-case CLI run — now carries condition_ii/iii diagnostics per case (r_ref value bit-identical to the 56-01 run)"
  - "tests/phase56/test_gate04_train_free.py extended to 33 tests / 24 subtests, 0 skips"
affects: [phase-56-03, phase-56-05, phase-56-06, phase-57-run-04]

actuals:
  tokens: 13058
  tasks: 2
  commits: 4
  plan_head_before: 87e64a7ebd0b282f6345fd78b019a98339d8efee

tech-stack:
  added: []
  patterns:
    - "Diagnostic-not-verdict functions: condition_ii_diagnostics/condition_iii_diagnostics return plain descriptive-statistics mappings with a status: UNRATIFIED sentinel and no key named or implying threshold/passed/satisfied/ok — a structurally-enforced convention checked by a negative-substring test on every returned mapping"
    - "Never-satisfiable slot: condition_ii_verdict raises NotImplementedError unconditionally so an open owner gap (GAP-56-01) cannot be silently resolved in either direction by a future edit"
    - "Argparse main(argv=None) + non-verdict exit code, mirroring architecture_characterization_probe.py exactly: exit code reports whether the tool completed, the printed line reports the verdict, and a non-empty unratified_conditions always appends INCOMPLETE + the gap reference"
    - "Governed-artifact refresh gated on case-set identity: main() only calls write_r_ref_artifact for the default six-case run (args.cases_config is None), since a custom case list cannot pass the artifact's own DEFAULT_CASES identity check"

key-files:
  created: []
  modified:
    - pinn/verification/gate04_train_free.py
    - pinn/verification/artifacts/r_ref_stage0.json
    - tests/phase56/test_gate04_train_free.py

key-decisions:
  - "condition_ii_diagnostics's distinct_non_floor_count is literally 'the count of entries strictly above the clamp floor' per the plan's own <action> text, not a de-duplicated distinct-value count — the field name echoes GAP-56-01's discarded 'tempted-to' wording but the plan's prose definition governs"
  - "condition_iii_diagnostics scales raw_bin_means directly (r_ref held fixed) rather than scaling r_tilde and re-deriving raw_bin_means, since r_tilde = raw_bin_means / r_ref is linear in raw_bin_means — mathematically identical to 'scaling the normalized bin residuals uniformly', avoiding a redundant division/multiplication round-trip"
  - "main() calls write_r_ref_artifact only when args.cases_config is None: the artifact's own fail-closed identity check (56-01) raises for any case not in DEFAULT_CASES, so attempting the refresh on every custom --cases-config invocation would turn a legitimate D-07 config-driven run into a false failure"
  - "EVIDENCE_TOP_LEVEL_KEYS is a fresh 6-key set (schema_version, provenance, configuration, verdict, cases, failure) distinct from the governed R_REF artifact's 10-key FROZEN_TOP_LEVEL_KEYS — the plan's <action> text enumerates exactly these six things for the CLI's own evidence record"
  - "verdict is a nested provenance sub-object (verdict/blocking_reasons/unratified_conditions/r_ref/causal_clip_min_weight/precision/device) inside the evidence record rather than a bare string, so 'per-condition reasons' and the unratified-conditions list travel with the written record, not only with the printed line"

patterns-established:
  - "Two-tier evidence: a per-run, non-overwriting CLI evidence directory (audit trail of every invocation, any case list) versus the single governed R_ref artifact (refreshed only for the canonical six-case run) — the same distinction Phase 43's duration-gate JSON precedent established for a different gate"

requirements-completed: []

coverage:
  - id: D1
    description: "condition_ii_verdict(weights) raises NotImplementedError naming GAP-56-01 unconditionally, for every input; condition_ii_diagnostics returns the exact five-key descriptive-statistics mapping (no verdict-shaped field) with status UNRATIFIED"
    requirement: GATE-04
    verification:
      - kind: unit
        ref: "tests/phase56/test_gate04_train_free.py::ConditionIIUnratifiedSlotTests (5 tests, 8 subtests)"
        status: pass
    human_judgment: false
  - id: D2
    description: "condition_iii_diagnostics records the front index's response to a uniform residual-reduction sweep and a late-bin-only variant via ratified_causal_weights/_front_idx, with no pass threshold; docstring states both 56-RESEARCH.md structural findings"
    requirement: GATE-04
    verification:
      - kind: unit
        ref: "tests/phase56/test_gate04_train_free.py::ConditionIIIDiagnosticsStructureTests (5 tests, 3 subtests)"
        status: pass
    human_judgment: false
  - id: D3
    description: "On the six real audited cases (via run_gate): unratified_conditions narrows to (\"ii\",), both diagnostic fields are populated UNRATIFIED records, unperturbed front index is 0 for every case, late-bin-only response is constant at that value, and the uniform-factor response is non-decreasing as the factor shrinks"
    requirement: GATE-04
    verification:
      - kind: integration
        ref: "tests/phase56/test_gate04_train_free.py::RunGateEndToEndTests::test_run_gate_six_default_cases_pass"
        status: pass
    human_judgment: false
  - id: D4
    description: "The operator CLI (main) run with no case arguments exits 0, writes one evidence directory with the six default labels in order, the frozen six-key top-level schema, a complete provenance block, and a printed verdict line carrying INCOMPLETE + GAP-56-01"
    requirement: GATE-04
    verification:
      - kind: integration
        ref: "tests/phase56/test_gate04_train_free.py::Gate04CLIDefaultRunTests (5 tests, real CLI subprocess)"
        status: pass
      - kind: other
        ref: ".venv/bin/python -m pinn.verification.gate04_train_free --evidence-root .planning/tmp/gate04-smoke -> EVIDENCE_OK via 56-02-evidence-check.py"
        status: pass
    human_judgment: false
  - id: D5
    description: "Two CLI runs against the same evidence root allocate two distinct, non-overwriting directories; a malformed cases-config (bad JSON or unknown IC13 mode) fails closed with a non-zero exit and a recorded failure entry, never a PASS; an evidence root inside simulation_data is rejected before any write"
    requirement: GATE-04
    verification:
      - kind: unit
        ref: "tests/phase56/test_gate04_train_free.py::Gate04CLIEvidenceDirectoryTests, ::Gate04CLIFailureModeTests (4 tests)"
        status: pass
      - kind: other
        ref: "ls .planning/tmp/gate04-smoke | wc -l before/after two real CLI runs: 1 -> 2"
        status: pass
    human_judgment: false
  - id: D6
    description: "No fixed front-index comparison and no condition-(ii) threshold exist in the module; the CLI adds no force/skip_gate/allow_block/ignore_verdict bypass; the module is registered in no CI or verify ladder; the sibling phase55 suite is unaffected"
    requirement: GATE-04
    verification:
      - kind: other
        ref: "grep -vE '^\\s*#' gate04_train_free.py | grep -cE 'front_idx\\s*[><=!]+\\s*[0-9]' -> 0; grep -cE 'force|skip_gate|allow_block|ignore_verdict' -> 0; grep -rn gate04_train_free --include='*.yml' --include='*.yaml' --include='*.toml' --include='*.cfg' . -> 0 matches"
        status: pass
      - kind: unit
        ref: ".venv/bin/python -m pytest tests/phase55/ -q -> 46 passed"
        status: pass

duration: 52 min
completed: 2026-09-06
status: complete
---

# Phase 56 Plan 02: GATE-04 Condition (ii)/(iii) Slots and Operator CLI Summary

**Condition (iii) is wired as a front-CAPABILITY record (never a fixed front-index check), condition (ii) is a structurally-present slot that always raises naming GAP-56-01, and an operator can now run GATE-04 from the command line and get a verdict, both diagnostic records, and a provenance-complete, non-overwriting evidence directory.**

## Performance

- **Duration:** 52 min (estimated; a precise start timestamp was not captured before context-gathering began)
- **Started:** ~2026-09-06T16:05:00Z (estimated)
- **Completed:** 2026-09-06T16:56:57Z
- **Tasks:** 2/2
- **Files modified:** 3 (`pinn/verification/gate04_train_free.py`, `pinn/verification/artifacts/r_ref_stage0.json`, `tests/phase56/test_gate04_train_free.py`)

## Accomplishments

- Condition (ii) is now structurally present and impossible to satisfy or fail without an owner ruling: `condition_ii_verdict` always raises `NotImplementedError` naming GAP-56-01 and the four candidate options; `condition_ii_diagnostics` reports coefficient of variation, monotonicity, dynamic-range decades, and non-floor count with `status: "UNRATIFIED"` and no verdict-shaped field.
- Condition (iii) is wired as the front-capability structure `54-RULING.md` specifies: `condition_iii_diagnostics` records a uniform residual-reduction sweep and a late-bin-only variant, reusing `ratified_causal_weights` and the probe's `_front_idx` — never a second implementation, never a fixed comparison. On all six real audited cases the unperturbed front index is 0 (the healthy, expected result), the late-bin-only response is constant, and the uniform response is non-decreasing as the reduction factor shrinks — reproducing 56-RESEARCH.md Part (b)'s findings to close numeric agreement.
- `gate04_verdict`'s `unratified_conditions` narrows from `("ii", "iii")` to `("ii",)`; its docstring now states condition (iii)'s only wired rule is the pre-existing finiteness BLOCK.
- The operator CLI (`python -m pinn.verification.gate04_train_free`) exists: it resolves cases via the probe's `load_cases_config` or the default six, rejects a dataset-inside evidence root before anything is written, writes a schema-versioned, provenance-complete evidence record to a non-overwriting timestamped directory, and prints a verdict line that appends `INCOMPLETE` and the `GAP-56-01` reference whenever `unratified_conditions` is non-empty.
- The committed `r_ref_stage0.json` artifact was refreshed by running the CLI against its default path: the `r_ref` value is bit-identical to 56-01's run; each case entry now also carries its `condition_ii_diagnostics` / `condition_iii_diagnostics` records.

## Task Commits

1. **Task 1 RED: failing tests for condition (ii)/(iii) slots** — `e8d957bb` (`test(56-02)`) — 18 failed / 4 passed on the fast (synthetic-data) scoped run; RED evidence verified by `gsd-tools check tdd-red-evidence` → **RED_EVIDENCE_OK** (`target_test_failed`, target `ConditionIIUnratifiedSlotTests::test_condition_ii_verdict_raises_not_implemented`).
2. **Task 1 GREEN: implementation** — `73811ec2` (`feat(56-02)`) — the three functions, the factors constant, `evaluate_case` wiring, and the `gate04_verdict`/`_UNRATIFIED_CONDITIONS` update.
3. **Task 2 RED: failing tests for the CLI and evidence record** — `5009fff6` (`test(56-02)`) — 8 failed / 2 passed on the CLI test classes (fast pre-implementation, since `main` did not exist); RED evidence verified → **RED_EVIDENCE_OK** (target `Gate04CLIFailureModeTests::test_dataset_evidence_root_rejected_before_any_write`).
4. **Task 2 GREEN: CLI implementation + artifact refresh** — `6e485311` (`feat(56-02)`) — `main`, `_parse_args`, the provenance/configuration/case/verdict record builders, the `write_r_ref_artifact` case-entry enrichment, and the refreshed `r_ref_stage0.json`.

**Plan metadata:** committed with this SUMMARY (`docs(56-02)`).

No REFACTOR commits — both implementations landed clean; no cleanup changes were needed.

## TDD Gate Compliance

- **Task 1** — RED gate: `test(56-02)` commit `e8d957bb` precedes GREEN; target test failed via a real `AttributeError` naming the not-yet-existent `condition_ii_verdict`, classified `RED_EVIDENCE_OK` (`target_test_failed`). GREEN gate: `feat(56-02)` commit `73811ec2`; full `tests/phase56/` suite (including the pre-existing, updated `RunGateEndToEndTests`) passed 23/23 (24 subtests) after implementation. REFACTOR: not applicable.
- **Task 2** — RED gate: `test(56-02)` commit `5009fff6` precedes GREEN; target test failed via a real `AttributeError` naming the not-yet-existent `main`, classified `RED_EVIDENCE_OK`. GREEN gate: `feat(56-02)` commit `6e485311`; full suite passed 33/33 (24 subtests, 0 skipped) after implementation. REFACTOR: not applicable.
- Tracer feedback gate: not applicable — neither task carries `type="tracer"` (both are `type="auto" tdd="true"`).
- **RED evidence tooling note:** `gsd-tools check tdd-red-evidence` parses Node's TAP reporter format (`# tests N` / `# pass N` / `# fail N` / `not ok N - <name>`), not pytest's native output. A small uncommitted translation script (`.planning/tmp/build-red-record.py`) parses pytest's own real `FAILED <nodeid>` lines and pass/fail counts and re-expresses them in that shape — the underlying facts (which test failed, exit code, counts) are the real pytest run's own, never fabricated; only the wire format is translated. This mirrors 56-01's own precedent of using this same checker in this Python project.

## Files Created/Modified

- `pinn/verification/gate04_train_free.py` (modified) — added `condition_ii_verdict`, `condition_ii_diagnostics`, `condition_iii_diagnostics`, `CONDITION_III_DIAGNOSTIC_FACTORS`; wired both into `evaluate_case`; narrowed `_UNRATIFIED_CONDITIONS` to `("ii",)`; added `main`, `_parse_args`, `_cli_provenance`, `_cli_configuration`, `_case_record`, `_verdict_record`, `_command_string`, `EVIDENCE_SCHEMA_VERSION`, `EVIDENCE_TOP_LEVEL_KEYS`, `_GATE04_PROG`, `_DEFAULT_EVIDENCE_ROOT`; extended `write_r_ref_artifact`'s case entries with both diagnostic records; extended `__all__`; added the `if __name__ == "__main__":` guard.
- `pinn/verification/artifacts/r_ref_stage0.json` (modified) — refreshed from a real CLI run against the default six cases; `r_ref` unchanged (bit-identical); each case entry now carries `condition_ii_diagnostics` / `condition_iii_diagnostics`.
- `tests/phase56/test_gate04_train_free.py` (modified) — `_synthetic_case` gained an optional `front_idx` parameter; `Gate04VerdictTests` gained a non-finite-front-index BLOCK test; `RunGateEndToEndTests` updated for the new one-element `unratified_conditions` and populated diagnostics; added `ConditionIIUnratifiedSlotTests`, `ConditionIIIDiagnosticsStructureTests`, `Gate04CLIDefaultRunTests`, `Gate04CLIEvidenceDirectoryTests`, `Gate04CLIFailureModeTests`, `Gate04CLINoBypassTests`; extended `PublicContractTests.test_gate_public_surface`.

## Verification Evidence

| Check | Result |
|---|---|
| `pytest tests/phase56/test_gate04_train_free.py -x -q` (full suite, post both tasks) | **33 passed, 24 subtests, 0 skipped** (443.16s) |
| `pytest tests/phase55/ -q` | **46 passed** (8.03s; committed baseline held) |
| `.venv/bin/python .planning/tmp/56-02-cond-slots-check.py` | **COND_SLOTS_OK** |
| CLI smoke (`--evidence-root .planning/tmp/gate04-smoke`) x2 real runs | exit 0 both times; `verdict=PASS INCOMPLETE (unratified: ii; GAP-56-01 OPEN, see 56-GAPS.md)`; `ls .planning/tmp/gate04-smoke \| wc -l` 1 -> 2 |
| `.venv/bin/python .planning/tmp/56-02-evidence-check.py .planning/tmp/gate04-smoke` | **EVIDENCE_OK** |
| `grep -vE '^\s*#' gate04_train_free.py \| grep -cE 'front_idx\s*[><=!]+\s*[0-9]'` | **0** |
| `grep -cE 'force\|skip_gate\|allow_block\|ignore_verdict' gate04_train_free.py` | **0** |
| `grep -rn gate04_train_free --include='*.yml' --include='*.yaml' --include='*.toml' --include='*.cfg' .` | **0 matches** |
| `git diff` on the refreshed `r_ref_stage0.json`'s `"r_ref"` line | **empty** (value bit-identical to 56-01's run) |

The refreshed artifact's `condition_ii_diagnostics` for case "41" (CV=1.9879, dynamic range 5.8816 decades) reproduces 56-RESEARCH.md Part b.3's session-computed table (CV=1.988, 5.88 decades) to displayed precision — independent confirmation the diagnostics compute what the research grounding describes.

## Decisions Made

Recorded in frontmatter `key-decisions`; the load-bearing ones: `distinct_non_floor_count` follows the plan's literal prose definition (count of entries above the floor) rather than the field name's "distinct" connotation; `condition_iii_diagnostics` scales `raw_bin_means` directly rather than re-deriving from a scaled `r_tilde` (mathematically identical, avoids a redundant round-trip); `main()` refreshes the governed R_ref artifact only for the default six-case run, never for a custom `--cases-config`, since the artifact's own identity check would otherwise turn a legitimate config-driven run into a false failure.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 — Blocking] Commit subject shortened to fit the repo's 80-character limit**
- **Found during:** Task 1 GREEN commit
- **Issue:** the plan's literal suggested commit subject ("wire GATE-04 condition (iii) capability structure and the unratified condition (ii) slot") is 88 characters; `scripts/git_policy/validate_commit_msg.py`'s commit-msg hook rejects any subject over 80.
- **Fix:** shortened to "wire GATE-04 condition (iii) structure and the unratified condition (ii) slot" (77 chars), dropping only the word "capability" (elaborated in the commit body and in the code's own docstrings).
- **Files modified:** none (commit-message only).
- **Verification:** `scripts/agent-commit` succeeded on retry.
- **Committed in:** `73811ec2`

**2. [Rule 1 — Bug] Own docstring text tripped the plan's negative front_idx grep**
- **Found during:** Task 1 acceptance-criteria loop
- **Issue:** `condition_iii_diagnostics`'s docstring originally read "a fixed \`\`front_idx > 0\`\` check" — literal prose describing what NOT to do — which matched the plan's own acceptance-criteria regex (`front_idx[[:space:]]*[><=!]+[[:space:]]*[0-9]`, intended to catch real code comparisons, not documentation).
- **Fix:** reworded to "a fixed positive-front check (the front index compared against zero)", preserving the meaning while breaking the literal token adjacency the grep matches.
- **Files modified:** `pinn/verification/gate04_train_free.py`
- **Verification:** the negative grep returns 0; the docstring-content test (`test_docstring_states_both_structural_findings`) still finds both required phrases.
- **Committed in:** `73811ec2`

**Total deviations:** 2 auto-fixed (1 Rule 3, 1 Rule 1). **Impact on plan:** none to scope, contract, or code behavior — the first is a commit-message-only edit; the second is a docstring wording change with no semantic difference.

## Known Stubs

None new. Condition (ii)'s never-satisfiable slot (`condition_ii_verdict` always raising) is the plan's own intended design, not a stub — GAP-56-01 remains OPEN and untouched by this plan, exactly as specified.

## Issues Encountered

- `gsd-tools check tdd-red-evidence` parses Node TAP output, not pytest's native format — resolved by writing a small, uncommitted translation script (`.planning/tmp/build-red-record.py`) that re-expresses a real pytest run's own facts (never fabricated) in the TAP shape the checker parses. See "TDD Gate Compliance" above.
- Running a scratch verification script directly (`.venv/bin/python .planning/tmp/*.py`, not `-m`) does not put the repo root on `sys.path`, so `import pinn` fails unless the script inserts the repo root itself. Both `.planning/tmp/56-02-cond-slots-check.py` and `.planning/tmp/56-02-evidence-check.py` do this explicitly at the top.
- `.planning/tmp/build-red-record.py`, `.planning/tmp/56-02-cond-slots-check.py`, and `.planning/tmp/56-02-evidence-check.py` are scratch verification helpers per this task's own instructions ("Write `.planning/tmp/...` as part of this task") and are deliberately NOT staged or committed — `.githooks/pre-commit` (`scripts/git_policy/validate_staged_paths.py`) blocks any `*/tmp/*` path from being committed in this repo, consistent with `.planning/tmp/`'s existing untracked precedent (56-04's own scratch files).

## User Setup Required

None — no external service configuration required.

**REQUIREMENTS.md GATE-04 checkbox deliberately NOT flipped by the executor** — same phase-close/verification-act precedent 56-01 and prior Phase 47/47-01/47-02 plans followed (GATE-04 is a single requirement spanning the whole phase; three plans — 56-05, 56-03, 56-06 — remain).

## Next Phase Readiness

- GATE-04's condition (i) and (iii) are wired with grounded fail-closed rules; condition (ii) is structurally present and honestly labelled `UNRATIFIED`; the operator CLI and evidence record exist and are tested.
- **Ready for 56-03** (SC5 demonstration: the pre-amendment recipe as a committed fixture, proving `gate04_verdict` BLOCKs on all six audited cases under the old recipe) — `gate04_verdict` and `_blocking_reasons` are unchanged by this plan's edits, so 56-03 builds directly on the same verdict function 56-01 proved.
- **Ready for 56-05** (spec amendment completion) and **56-06** (phase close-out + the authoritative GATE-04 run) — the CLI this plan built is exactly the tool 56-06's "authoritative GATE-04 run and its evidence" deliverable will invoke.
- GAP-56-01 and GAP-56-02 remain OPEN and untouched, as designed. The condition-(ii) diagnostics now committed in `r_ref_stage0.json` give the eventual owner ruling real post-amendment data to rule against, per the plan's own intent.
- Note for 56-06 / Phase 57: `main()`'s default six-case run costs ~185-200s (the same per-case AD cost 56-01 recorded); a custom `--cases-config` run costs roughly `30s x len(cases)`.

---
*Phase: 56-contract-amendment-train-free-gate*
*Completed: 2026-09-06*

## Self-Check: PASSED

All four claimed files exist on disk (`pinn/verification/gate04_train_free.py`, `pinn/verification/artifacts/r_ref_stage0.json`, `tests/phase56/test_gate04_train_free.py`, this SUMMARY); all four commits exist in `git log --all` (`e8d957bb`, `73811ec2`, `5009fff6`, `6e485311`); the module exposes all seven Task-1/Task-2 public symbols (`condition_ii_verdict`, `condition_ii_diagnostics`, `condition_iii_diagnostics`, `CONDITION_III_DIAGNOSTIC_FACTORS`, `main`, `EVIDENCE_SCHEMA_VERSION`, `EVIDENCE_TOP_LEVEL_KEYS`).
