---
phase: 64-feasibility-verdict
plan: 02
subsystem: verification
tags: [numbers-manifest, rederived-cpu-float64, time-constant-evidence, derive, open-attestation, torch-load, feas-06, feas-10]

requires:
  - phase: 64-feasibility-verdict
    provides: "the fail-closed verifier with inputs, frozen and traceability, and ordered_sum, the left-to-right += loop (64-01)"
  - phase: 60-single-system-learnability
    provides: "the sealed stop-handoff.json with total_wall_hours 22.37828873402778 and arm order, the seven arm records with result.E and states.<state>.cross_check.E, and the committed adam/polish weights"
  - phase: 59-read-only-baseline-scorecard
    provides: "the frozen feasibility scorecard (Tier-1 E_max 0.1, tiers.comparison inclusive_le), baselines.json, survey.json, picks.json, census.json, 59-GAPS.md and runs/stage0-v23g7-seed42/status.json"

provides:
  - "evidence/numbers.json: 365 entries, schema phase64-numbers/v1, every quoted number with id, value, render, render_rule, label, source, derivation and required_in"
  - "evidence/build_phase64_evidence.py: the producer, including derive_state, constant_predictor_error, timevar_ratio, rms_ratio and the 83 arithmetic formulas; numbers --check reproduces the bytes"
  - "verify_phase64_verdict.py numbers: every committed-record entry re-read through the verifier's own id-to-key table, every arithmetic entry through its own formulas, every cited token checked and every render re-applied, with no data root"
  - "verify_phase64_verdict.py derive: 136 entries re-derived on the CPU in float64 from the committed weights, with each SHA-256 checked before torch.load(weights_only=True) and the open attestation required at zero"
  - "the D-01 time-constant evidence as committed numbers: constant-predictor E 1.1538, 1.2337 and 1.1396; official minus constant 0.0035 to 0.0038; time variation 0.0030 to 0.0034; RMS ratio 0.9999 to 1.0001; best moment 0.817 to 0.935; 0 of 1,001 inside Tier 1"
  - "tests/phase64/test_verifier_phase64.py: 106 tests, the 13 new ones covering the derive helpers, the fail-closed derive gates and the real re-derivation"

actuals:
  tokens: 93532
  tasks: 3
  commits: 3
  plan_head_before: 5e3af2b7281e2ba28b64adb9771267c07855fc24

tech-stack:
  added: []
  patterns:
    - "Number manifest with a five-value label vocabulary: official-mps-float32 and committed-record carry {path, key}, arithmetic carries {formula}, cited carries {path, commit, token}, rederived-cpu-float64 carries {record, weights, state}"
    - "Two independent implementations of the same table: the verifier carries its own id-to-key table, formula table and render rules, imports no producer code, and the producer imports no verifier code"
    - "Fail-closed before deserialization: each weights file's SHA-256 is compared with its record before torch.load(weights_only=True), and the process-wide open attestation must show five counters at zero"
    - "Shared frozen loads: one load_arm_data per system (three in all), reused across the five 1632 arms and both states through an optional arm_data= hook"
    - "Thresholds read from the scorecard at run time (Tier-1 E_max 0.1, inclusive_le), never typed as a literal in the comparison"

key-files:
  created:
    - .planning/phases/64-feasibility-verdict/evidence/numbers.json
    - .planning/phases/64-feasibility-verdict/evidence/build_phase64_evidence.py
  modified:
    - .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py
    - tests/phase64/test_verifier_phase64.py

key-decisions:
  - "The verifier never imports the producer: it keeps its own id-to-key table, its own 21 cpu formulas and its own render rules, so a swapped file or key fails numbers instead of agreeing with itself"
  - "ordered_sum stays the one summation helper for every exactly compared float sum (hours.total, hours.rung1, hours.sweep, timing.wall_seconds.total): an explicit += loop from 0.0 in handoff arm order, because math.fsum lands one ulp below 22.37828873402778"
  - "The constant predictor is per system (Rung-1 official E minus that system's constant-predictor E), giving 0.0035 to 0.0038; 64-04's 'over the seven arms' wording is loose and was not followed"
  - "CPU E equals states.<state>.cross_check.E within 1e-12 and is never compared with the official MPS E: r1-1632 reads 1.1571 (adam) and 1.1600 (polish) on the CPU against 1.1574 official"
  - "derive compares floats within 1e-12 and integers exactly, and requires the attestation counters at zero before and after the loop, so a validation or test-split open cannot pass silently"
  - "The Tier-1 count uses <= the scorecard's 0.1 on max(e_sys, e_in), and 'Rung 1 below the formula' stays strictly <: the two frozen conventions are never re-implemented"

requirements-completed: [FEAS-06, FEAS-10]

coverage:
  - id: D1
    description: "numbers.json holds every number the verdict and charter will quote, with a label, a source and a derivation, and numbers re-derives all 365 entries without a data root"
    requirement: "FEAS-06"
    verification:
      - kind: unit
        ref: "tests/phase64/test_verifier_phase64.py#NumbersTracerTests,ManifestContentTests"
        status: pass
      - kind: other
        ref: "python -B .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py numbers -> entries 365, NUMBERS-OK"
        status: pass
    human_judgment: false
  - id: D2
    description: "derive re-derives all 14 CPU states and the three constant predictors from the committed weights, checking each SHA-256 before torch.load and requiring the open attestation at zero"
    requirement: "FEAS-06"
    verification:
      - kind: unit
        ref: "tests/phase64/test_verifier_phase64.py#DeriveHelperTests,DeriveContextTests,DeriveRealTests"
        status: pass
      - kind: integration
        ref: "python -B .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py derive -> cpu entries 136, DERIVE-OK"
        status: pass
    human_judgment: false
  - id: D3
    description: "The D-01 time-constant evidence is committed and reproducible: constant E 1.1538, 1.2337, 1.1396, official-minus-constant 0.0035 to 0.0038, time variation 0.0030 to 0.0034, RMS ratio 0.9999 to 1.0001, best moment 0.817 to 0.935, 0 of 1,001 inside Tier 1"
    verification:
      - kind: integration
        ref: "derive on the real tree; numbers.json cpu.const.*, const_gap.*, cpu.range.*"
        status: pass
    human_judgment: false
  - id: D4
    description: "numbers.json is byte-reproducible in a second process"
    verification:
      - kind: other
        ref: "python -B .planning/phases/64-feasibility-verdict/evidence/build_phase64_evidence.py numbers --check -> NUMBERS-CHECK-OK"
        status: pass
    human_judgment: false

duration: 41min
completed: 2026-10-26
status: complete
---

# Phase 64 Plan 02: The Number Manifest and the CPU Re-derivation Summary

**Every number the verdict and charter will quote is now a labelled, sourced entry of `evidence/numbers.json` (365 entries), and the D-01 time-constant evidence is re-derived from the committed weights on the CPU in float64 with zero test-split and validation opens.**

In plain language: before the verdict is written, each figure it will quote has been copied into one file together with where it came from and how it was computed, and a separate program recomputes it. Numbers read from a Phase 60 record stay marked as the official MPS float32 result; numbers computed here are marked as CPU float64 re-derivations and are never confused with the official ones. The time-constant experiment — how far each trained network's output moves compared with the real orbit, and how wrong a predictor that never moves would be — is now committed evidence rather than a scratch result, re-derived in seconds from the committed weights, and the checker refuses to run if any test-split or validation file was opened.

## Performance

- **Duration:** about 41 min
- **Started:** 2026-10-25T23:15:22-05:00 (`5e3af2b7`, the 64-01 summary commit)
- **Completed:** 2026-10-26T04:56Z
- **Tasks:** 3
- **Commits:** 3
- **Files modified:** 4 (`numbers.json` and the producer created; the verifier and the test module extended)

## Accomplishments

- **Task 1 — the tracer:** the producer and `numbers.json` with one entry of each kind, and the verifier's `numbers` mode. `arm.r1-1632.E` (official MPS float32, `1.1574`), `cpu.r1-1632.polish.E` (CPU float64, `1.1600`), `hours.total` (arithmetic, `22.378`, equal to the sealed `total_wall_hours` with `==`) and `pub.kollias.energy_range` (cited, `0.02–3%`, token checked in `git show 7fda0a55:…`). 78 tests at that point.
- **Task 2 — the full manifest:** 230 entries with their labels, sources and derivations — 35 official, 94 committed-record, 83 arithmetic, 17 cited and the tracer re-derivation. Headline renders: 22.378 h total, 11.108 h Rung 1, 11.270 h sweep, 7,437,225 Adam steps, best official `eps_h` 123.62 at `g2s-1632-w240`, ratio to bar `1.24 × 10⁷`, Rung 1 below the formula 1 of 3 (4658 only), copy validation median 2.135, census one part in 1,169, for-scale 28.5 and 42.8 days.
- **Task 3 — the CPU re-derivation:** 135 entries added (114 `rederived-cpu-float64` and 21 `cpu.*`/`const_gap.*` arithmetic), for 365 in all. `derive` re-scores all 14 states from the committed weights and prints `cpu entries 136` / `DERIVE-OK`. The evidence: constant-predictor E `1.1538`, `1.2337`, `1.1396` on 1632, 851, 4658; the official E minus the constant E `0.0035` to `0.0038`; time variation `0.0030` to `0.0034` of the orbit's own; RMS ratio `0.9999` to `1.0001`; best moment `0.817` to `0.935`; `e_sys` at t=0 `0.805` to `1.009` and `e_in` `0.894` to `0.998`; `0` of `1,001` scored times inside Tier 1 at 0.1 inclusive. Each of the 14 CPU `E` values equals its record's `states.<state>.cross_check.E` within 1e-12 (r1-1632: 1.1571 adam, 1.1600 polish).

## Task Commits

Each task was committed atomically through `scripts/agent-commit`:

1. **Task 1: the number manifest tracer and its two checks** — `d2401a39` (`evidence`)
2. **Task 2: every committed and cited number** — `e3ed854a` (`evidence`)
3. **Task 3: the CPU re-derivation of the time-constant evidence** — `5f36d52a` (`evidence`)

## Verification Results

| Command | Result |
|---|---|
| `python -B -m unittest tests.phase64.test_verifier_phase64 -v` | Ran 106 tests in 59.3 s, `OK`, exit 0 |
| `verify_phase64_verdict.py numbers` | `entries 365`, `NUMBERS-OK`, exit 0 (1.4 s) |
| `verify_phase64_verdict.py derive` | `cpu entries 136`, `DERIVE-OK`, exit 0 (5.8 s) |
| `build_phase64_evidence.py numbers --check` | `NUMBERS-CHECK-OK`, exit 0 (4.5 s); `numbers.json` sha256 `632e02b2…` unchanged |
| `verify_phase64_verdict.py frozen` | `frozen paths pinned=33 sealed=8 trees=4`, `FROZEN-OK`, exit 0 (0.5 s) |
| `verify_phase64_verdict.py inputs` | `INPUTS-OK`, exit 0 (0.6 s) |
| `verify_phase60_evidence.py final` | `G2-OK`, `PHASE60-EVIDENCE-OK`, exit 0 (1.3 s) |
| `verify_phase59_evidence.py scorecard-frozen` | `SCORECARD-FROZEN-OK`, exit 0 (1.9 s) |
| `verify_phase59_evidence.py guardrails` | `GUARDRAILS-OK`, exit 0 (2.1 s) |

The open attestation read `schema phase59-files-opened/v1`, `data_root_source git_common_dir_default`, `opened.train 262`, `opened.validation 0`, `opened.other_under_root 0`, `test_split_opened 0`, `blocked_attempts 0`, `refused_before_open 0`. It is recorded in `numbers.json` as five `cpu.attestation.*` entries, each `0`.

Mutant checks (each reintroduced by hand, caught, then restored):

- Task 2: `ordered_sum` swapped for `math.fsum` — `numbers` failed on the one-ulp difference in `hours.total`.
- Task 3: the constant predictor taken at the last frame instead of the time mean — `derive` failed closed with `entry cpu.const.1632.E value 1.1538408194255343 != re-derived 2.0941699459850653 beyond 1e-12`, and `DeriveRealTests.test_real_derive_re_derives_136_entries` failed the same way. Restored file sha256 `403535d0…`, then `DERIVE-OK` again.

## Files Created/Modified

- `.planning/phases/64-feasibility-verdict/evidence/numbers.json` — 365 entries, sorted by id, canonical JSON through `evidence_io.write_json`: 115 `rederived-cpu-float64`, 104 `arithmetic`, 94 `committed-record`, 35 `official-mps-float32`, 17 `cited`.
- `.planning/phases/64-feasibility-verdict/evidence/build_phase64_evidence.py` — the producer: `render`, `ordered_sum`, `derive_state`, `constant_predictor_error`, `timevar_ratio`, `rms_ratio`, the `ARITHMETIC` table, `build_manifest`, `cmd_numbers`, `main`.
- `.planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py` — `numbers` and `derive` added: the id-to-key table, the independent formula table, `rederive_state`, `rederive_constant_error`, `cpu_value`, `_check_open_attestation`, `cmd_derive`.
- `tests/phase64/test_verifier_phase64.py` — `DeriveHelperTests`, `DeriveContextTests` and `DeriveRealTests` (13 tests), taking the module to 106.

## Decisions Made

- **Two independent implementations.** The verifier keeps its own render rules, id-to-key table and formulas and imports no producer code; the producer imports no verifier code. Agreement is therefore evidence, not tautology.
- **Label vocabulary and source shapes.** `official-mps-float32` and `committed-record` carry `{path, key}`; `arithmetic` carries `{formula}`; `cited` carries `{path, commit, token}`; `rederived-cpu-float64` carries `{record, weights, state}`. `derivation` stays prose, and `producer_sha256` entries are checked for existence and digest currency only.
- **CPU float64 is a separate fact from the official result.** The CPU `E` of each state equals `cross_check.E` within 1e-12 and is never compared with the official MPS `E` (r1-1632: 1.1571 and 1.1600 on CPU against 1.1574 official). `derive` compares floats within 1e-12 and integers exactly.
- **Frozen thresholds, read at run time.** The within-Tier-1 count uses `<=` the scorecard's Tier-1 `E_max` 0.1 (`tiers.comparison inclusive_le`); "below the formula" stays strictly `<`. Neither convention is re-implemented.
- **One frozen load per system.** The five 1632 arms share one reference, so `derive` performs three `load_arm_data` calls in all; `derive_state` and `rederive_state` accept an optional keyword-only `arm_data=` for that sharing, and four-argument calls still work for 64-03.
- **Fail closed before deserialization.** Every weights file's SHA-256 is checked against its record before `torch.load(..., weights_only=True)`, and the attestation is checked before and after the loop.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] A cited token used the MICRO SIGN instead of a superscript five (Task 2)**
- **Found during:** Task 2, while re-rendering the `10⁻⁵` citations
- **Issue:** `pub.breen.energy_projected` carried `\u00b5` (µ) where the research page has `\u2075` (⁵), so the token check would have compared a different string from the one the page shows.
- **Fix:** the token now uses `\u2075` and renders `10⁻⁵`.
- **Files modified:** `.planning/phases/64-feasibility-verdict/evidence/build_phase64_evidence.py`
- **Commit:** `e3ed854a`

### Presentation and schema choices the plan's group wording did not cover

**2. Labels chosen where the group header did not fit the data shape (Task 2)**
- **Found during:** Task 2
- **Choice:** `cost.forscale.steps_low`, `cost.forscale.steps_high` and `cost.example.steps` are `cited` (tokens `200,000`, `300,000`, `10⁵ steps`); `decision.rung2b`, `decision.rung3`, `decision.rung3_share`, `census.one_part_in_0p1` and `baseline.formula.tier1.*` are `arithmetic`; `tiers.*` stay `committed-record` with keys `tiers.levels.<index>.<field>` located by matching `tier`.
- **Why:** the plan names the entries but not the label for these shapes; each value is still sourced, rendered and re-derived, and `numbers` checks all of them.
- **Commit:** `e3ed854a`

**3. `const_gap.*` is per system, not "over the seven arms" (Task 3)**
- **Found during:** Task 3, reading 64-04's render map against the plan's stated range
- **Choice:** each gap is the Rung-1 official `E` minus that system's constant-predictor `E`, giving 0.0035 to 0.0038 on 1632, 851 and 4658.
- **Why:** only the per-system definition produces the plan's stated "about 0.0036 to 0.0038"; a seven-arm gap would mix CPU and official values across systems.
- **Commit:** `5f36d52a`

**4. `_field` accepts numeric path parts as list indices (Task 2)**
- **Found during:** Task 2, reading `trace.0.E` from the records
- **Choice:** a numeric part indexes a list in both programs.
- **Why:** the curve entries read `trace.<step>.E`; without it the curve group could not be sourced from the record.
- **Commit:** `e3ed854a`

**5. `derive_state` and `rederive_state` gained an optional keyword-only `arm_data=` (Task 3)**
- **Found during:** Task 3
- **Choice:** the caller may pass an already-loaded `ArmData`; omitted, each function loads its own.
- **Why:** the plan requires the producer to read the shared 1632 reference once per system, and the verifier's 14-state loop needs the same economy; 64-03 can keep calling the four-argument form.
- **Commit:** `5f36d52a`

## Known Stubs

None. Every entry either reads a committed file, evaluates an arithmetic formula over committed values, re-derives from committed weights, or cites a token verified in the cited commit. No placeholder, hardcoded empty value or unwired field was introduced; `required_in: []` marks entries the verdict does not render, not entries without a source.

## Threat Flags

None beyond the plan's threat model. The new surface is read-only: committed JSON and weights files, resolved through `repo_path` (containment plus symlink refusal), with `torch.load(weights_only=True)` after a digest check. No network endpoint, no write path, no new trust boundary. `numbers.json` carries `data_root_source` as a label and no host path (`test_manifest_has_no_home_directory_string`).

## Notes

- `.planning/STATE.md`, `.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md` were not modified and no state, roadmap or requirements verb was run: the orchestrator owns those files.
- `git status --porcelain -- pinn .planning/phases/60-single-system-learnability .planning/phases/59-read-only-baseline-scorecard runs` prints nothing after the plan, so no training output, sealed evidence or pinned module was touched.
- Pre-existing user-owned changes in the working tree (`.planning/config.json`, `.planning/state.json`, `.agents/`, `.gsd/`, the v2.2 stage-0 halt brief, the `docs/work` review folders, `phase-40-plan-04-grok.md`) were left alone and never staged.
- The plan-head ledger file for 64-02 was missing at SUMMARY time; it was reconstructed from the verified parent of the first task commit (`5e3af2b7`), so the measured count of 3 is exact.
- The four verification timings quoted above are from the wave-gate run after `5f36d52a`; the suite ran 106 tests and every mode printed its token on its own line.

## Next Phase Readiness

- `numbers` and `derive` are in the verifier's `COMMANDS` table; 64-03's `figure` mode can call `rederive_state` and `rederive_constant_error` directly, and 64-04/64-05 can rely on every quoted number already being in the manifest.
- The wave gate is green: 106 tests, `NUMBERS-OK`, `DERIVE-OK`, `NUMBERS-CHECK-OK`, `FROZEN-OK`, `INPUTS-OK`, `PHASE60-EVIDENCE-OK`, `SCORECARD-FROZEN-OK`, `GUARDRAILS-OK`.
- `derive` must run from the repository root, because `default_data_root()` reads the git common directory from the working directory; on this Mac `DeriveRealTests` ran rather than skipped.

## Self-Check: PASSED

- Files: `numbers.json`, `build_phase64_evidence.py`, `verify_phase64_verdict.py`, the test module and this SUMMARY all exist.
- Commits: `d2401a39`, `e3ed854a` and `5f36d52a` all present on `milestone/v2.4`.
- Ledger: 3 commits measured from `5e3af2b7`.
