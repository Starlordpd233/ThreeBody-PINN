---
phase: 64-feasibility-verdict
plan: 04
subsystem: verdict
tags: [feasibility-verdict, plain-language, rules-mode, rendered-token-check, evidence-index, gap-64-03, feas-06]

requires:
  - phase: 64-feasibility-verdict
    provides: "the number manifest and its CPU re-derivation (64-02): 365 entries, 161 marked verdict-required, numbers_sha256 632e02b2"
  - phase: 64-feasibility-verdict
    provides: "the one verdict figure and its provenance (64-03): figure-1632.svg d9754afa and figure-1632.provenance.json 409e5e87"
  - phase: 60-single-system-learnability
    provides: "the sealed stop handoff 7ed8223c with the frozen label, the qualifier and the empty-edge reasons, plus the seven committed arm records"
  - phase: 59-read-only-baseline-scorecard
    provides: "the frozen scorecard, the formula and copy baselines, the stage survey and the census"

provides:
  - "64-VERDICT.md: the owner-facing feasibility verdict, plain language first, 15 level-2 sections, status awaiting-owner, verdict RETHINK-REPRESENTATION, with the D-01 side-by-side box, the per-arm table, the time-constant evidence, the cost section with the GAP-64-03 subsection, the eight unranked fixes and the 22-row evidence index"
  - "verify_phase64_verdict.py rules: the full heading skeleton, the front-matter schema, the required phrases, the D-03 bullets, the cost subsection, the v2.5 next milestone, the Mac-only guard, the banned wording and every evidence-index digest; prints RULES-OK"
  - "verify_phase64_verdict.py numbers: check_verdict_renders requires all 161 verdict-required entries' rendered tokens at a digit boundary; prints NUMBERS-OK"
  - "tests/phase64/test_verifier_phase64.py: 17 new VerdictContentTests (168 in all) covering the real files and every Task 2 negative control"

actuals:
  tokens: 16496  # chars/4 over the 65,985 added-line characters of git diff 096a95db..HEAD
  tasks: 2
  commits: 2
  plan_head_before: 096a95dbd783ecc8791046632ca233ab929dc5ad

tech-stack:
  added: []
  patterns:
    - "The verdict is checked, not trusted: rules recomputes every evidence-index SHA-256 and both front-matter file digests, and numbers re-derives all 365 entries before requiring the 161 verdict renders"
    - "Digit-boundary matching for numeric renders (the Phase 59 pattern): 0.01 does not match inside 0.010856, so a longer decimal cannot stand in for a required token"
    - "Text tokens (STR, BOOL, LIT, OFN) are plain substrings; numeric tokens use the (?<!\\d)...(?!\\d) boundary"
    - "The cost subsection is located by span, not by phrase presence anywhere: exactly one ### Cost to the next level inside ## Cost on this Mac, holding both GAP-64-03 phrases"
    - "D-03 is checked as structure: eight candidates must appear on bullet lines and no numbered list item may appear in the section"
    - "The temporary-repository fixture copies all 22 evidence-index files, so rules exercises the real digest path rather than a stub"

key-files:
  created:
    - .planning/phases/64-feasibility-verdict/64-VERDICT.md
  modified:
    - .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py
    - tests/phase64/test_verifier_phase64.py

key-decisions:
  - "D-01 fold drop: the manifest renders 25 and 48; 64-CONTEXT rounds the same range to 25- to 50-fold. Judged within rounding, the verdict writes both (factor of 25 to 48, about 25- to 50-fold as the decision context puts it) rather than stopping; no manifest value falls outside the CONTEXT figures beyond rounding"
  - "The prior-work denial is required as the positive sentence No novelty claim is made, so an inverted claim cannot satisfy the phrase check"
  - "A literal floor of 161 verdict-required entries and 22 evidence-index rows keeps the checks from shrinking silently if the manifest or the index loses rows"
  - "The render-map audit found all 161 verdict-required entries named by the interfaces map and no map name missing from the manifest; the 10 map-named entries with required_in [] (curve fold-drop, first-reading fraction and Tier-1 multiple, and the timed and sustained seconds-per-step bounds) are quotable but not required"
  - "The final metadata commit goes through scripts/agent-commit (AGENTS.md commit protocol) rather than a raw git commit, with the same docs(64-04) message and trailer"

requirements-completed: [FEAS-06]

coverage:
  - id: D1
    description: "ROADMAP criterion 1: each rung's tier and where along the window it broke, via the per-arm table and the along-window facts"
    requirement: "FEAS-06"
    verification:
      - kind: integration
        ref: "python -B .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py rules -> RULES-OK; numbers -> entries 365, NUMBERS-OK"
        status: pass
      - kind: unit
        ref: "tests/phase64/test_verifier_phase64.py#VerdictContentTests.test_real_verdict_passes_rules"
        status: pass
    human_judgment: false
  - id: D2
    description: "ROADMAP criterion 2: the best official eps_h 123.62 against the locked 10^-5 bar (about 1.24 x 10^7 times), with the more favourable readings footnoted"
    requirement: "FEAS-06"
    verification:
      - kind: integration
        ref: "python -B .../verify_phase64_verdict.py numbers -> NUMBERS-OK"
        status: pass
    human_judgment: false
  - id: D3
    description: "ROADMAP criterion 3: the measured Mac cost is reported, and the next-level cost is stated as not estimable from this evidence in the GAP-64-03 subsection"
    requirement: "FEAS-06"
    verification:
      - kind: unit
        ref: "tests/phase64/test_verifier_phase64.py#VerdictContentTests.test_cost_subheading_removed_fails,test_cost_subheading_moved_under_another_section_fails,test_cost_subheading_without_not_estimable_fails,test_cost_subheading_without_gap_fails"
        status: pass
    human_judgment: false
  - id: D4
    description: "ROADMAP criterion 4 and FEAS-06: the result under the pre-registered rule, the comparison points, the ladder, the unrun items with verbatim reasons, and the v2.5 next milestone"
    requirement: "FEAS-06"
    verification:
      - kind: integration
        ref: "python -B .../verify_phase64_verdict.py rules -> RULES-OK; figure -> figure times 1001, FIGURE-OK; inputs -> INPUTS-OK; frozen -> FROZEN-OK"
        status: pass
      - kind: unit
        ref: "tests/phase64/test_verifier_phase64.py#VerdictContentTests (17 tests)"
        status: pass
    human_judgment: false
  - id: D5
    description: "Every number in the verdict is a manifest token: numbers requires all 161 verdict-required renders, and rules recomputes every cited digest"
    requirement: "FEAS-06"
    verification:
      - kind: unit
        ref: "tests/phase64/test_verifier_phase64.py#VerdictContentTests.test_changed_per_arm_e_fails_numbers,test_digit_boundary_does_not_match_inside_a_longer_number,test_stale_evidence_index_digest_fails"
        status: pass
    human_judgment: false

duration: 22min
completed: 2026-10-26
status: complete
---

# Phase 64 Plan 04: The Feasibility Verdict Summary

**The owner-facing verdict is committed: 15 plain-language sections that state the frozen RETHINK-REPRESENTATION label beside the evidence that every network learned only each body's average position, and a verifier that re-derives every number, every cited digest and every required phrase.**

In plain language: this page answers "can this work?" without asking the owner to read a single training log. It says what the rule agreed in advance concluded, what the experiments actually did, how far each one got, how the result compares with a no-learning formula and two published studies, where the project stands on the 0-to-9 ladder, what it cost on this Mac, what could be tried next, and what the next milestone is. A checking program now refuses the page if any of those statements loses its required wording, if any evidence digest is stale, if a candidate fix is ranked, or if any of the 161 required numbers stops appearing.

## Performance

- **Duration:** about 22 min (this continuation; Task 1 landed earlier in the same plan run)
- **Started:** 2026-10-26T05:38:10Z (ledger base `096a95db`, the 64-03 summary commit)
- **Completed:** 2026-10-26T06:00:18Z
- **Tasks:** 2
- **Commits:** 2
- **Files modified:** 3 (the verdict created; the verifier and the test module extended)

## Accomplishments

- **Task 1 — the tracer:** the front matter (`phase64-verdict/v1`, status `awaiting-owner`, verdict `RETHINK-REPRESENTATION`, the handoff and manifest digests), the Audience line, `## In plain language` with the D-01 side-by-side box, and `## The result under the pre-registered rule` with the D-02 qualifier note. The new `rules` mode checked the front-matter schema, the heading prefix, the required phrases, the owner's wording guard and the host-home scan, and printed RULES-OK.
- **Task 2 — the rest of the verdict:** the 13 remaining sections. The per-arm table (seven arms, official MPS float32), the along-window facts (re-derived CPU float64: error at the first scored moment, the best moment, 0 of 1,001 times within Tier 1), the best official eps_h 123.62 against the locked 10⁻⁵ bar (about 1.24 × 10⁷ times) with the 30.29 and 0.9999 readings footnoted, the constant-predictor table with the gap and the two ratios, the accuracy curves that levelled off at 11 to 12 times Tier 1, the formula/copy/published comparisons with the corrected 0.02–3% and no novelty claim, the survey and the probes with their verbatim reasons, Level 1 on the ladder, 22.378 hours of Mac time with the per-arm cost table, the labelled v2.5 illustration and the for-scale figure, the `### Cost to the next level` subsection (GAP-64-03 option A), the eight unranked candidate fixes, the v2.5/trainex-r5 next milestone, the three-option decision table, the sign-off, and the 22-row evidence index with the five verifier commands.
- **The verifier grew two checks:** `rules` now requires the 15 level-2 headings exactly once in order, the cost subsection in its span with both GAP-64-03 phrases, the eight D-03 bullets with no numbered item, `v2.5` inside the next-milestone section, and every evidence-index digest current; `numbers` gained `check_verdict_renders`, which requires all 161 verdict-required entries' rendered tokens, with digit-boundary matching for numeric rules.
- **Tests:** 17 new `VerdictContentTests`, one per negative control in the plan's `<behavior>` plus the real-file smokes and a digit-boundary pin; the full suite runs 168 tests, all passing.

## Task Commits

Each task was committed atomically through `scripts/agent-commit`:

1. **Task 1: the verdict headline and its rules check** — `bd768374` (`docs`)
2. **Task 2: the full feasibility verdict** — `e2a8c407` (`docs`)

**Plan metadata:** the SUMMARY commit (docs, below).

## Files Created/Modified

- `.planning/phases/64-feasibility-verdict/64-VERDICT.md` — the verdict: 15 level-2 sections, one level-3 cost subsection, 22 evidence rows; SHA-256 `b0507c03e116c6a88241d447f549c169be16eee84e9e10487280b180b052b801`.
- `.planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py` — the `rules` mode and the `numbers` render check (`check_verdict_renders`, `_check_cost_to_next_level`, `_check_candidate_fixes`, `_check_next_milestone`, `_check_evidence_index`, `EVIDENCE_INDEX_PATHS`, the extended phrase list).
- `tests/phase64/test_verifier_phase64.py` — `VerdictContentTests` (17 tests) and the 22-file temporary-repository fixture.

## Decisions Made

- **D-01 fold drop is written both ways.** The manifest renders `25` and `48`; 64-CONTEXT rounds the same range to "25–50-fold". The two are the same range at the CONTEXT's precision, so the verdict says "factor of 25 to 48" and "(about 25- to 50-fold as the decision context puts it)". No manifest value falls outside the CONTEXT figures beyond rounding, so the plan's stop-and-report condition was not met.
- **The novelty denial is checked as a positive sentence.** `No novelty claim is made` is required verbatim, so an inverted "a novelty claim is made" cannot satisfy the check.
- **Literal floors.** `VERDICT_REQUIRED_COUNT = 161` and `EVIDENCE_INDEX_COUNT = 22` are literals, not derived from the lists they check, so a manifest or index that silently loses rows fails closed.
- **Render-map audit.** All 161 verdict-required entries are named by the plan's `<interfaces>` map, and no map name is missing from the manifest. The 10 map-named entries with `required_in: []` (fold-drop min/max, first-reading fraction min/max, Tier-1 multiple min/max, and the timed and sustained seconds-per-step min/max) are quotable but not required.
- **Final metadata commit.** The SUMMARY is committed through `scripts/agent-commit` with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`, because AGENTS.md requires that path for every agent commit; the message and trailer are the ones the plan specifies.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Test anchor matched the backticked pointer, not the heading**
- **Found during:** Task 2 (the moved-subsection negative control)
- **Issue:** `self.verdict.index("### Cost to the next level")` found the backticked mention in `## In plain language` first, so the "moved" mutation deleted a large block and failed on the heading order instead of the cost span.
- **Fix:** Anchor on `"\n### Cost to the next level\n"` and add one, so the mutation starts at the heading line.
- **Files modified:** `tests/phase64/test_verifier_phase64.py`
- **Commit:** `e2a8c407`

### Judgements (not deviations)

- The D-01 fold-drop wording above is a rounding judgement, recorded rather than escalated because both sources describe the same range.
- The phrase `No novelty claim is made` is capitalized to match the verdict and to defeat inversion; the plan's action names "no novelty claim" without fixing case.
- An extra test pins the digit boundary (`0.01` inside `0.010856` must not count), beyond the `<behavior>` list, because the plan's action requires the Phase 59 boundary and no listed control exercised it.

**No auth gates; no package installs; no architectural changes.**

## Verification Results

| Command | Result |
|---|---|
| `<home>/miniforge3/envs/pinn-train/bin/python -B -m unittest tests.phase64.test_verifier_phase64 -v` | `Ran 168 tests in 57.777s` — `OK`, exit 0 |
| `python -B .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py rules` | `RULES-OK`, exit 0 |
| `python -B .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py numbers` | `entries 365` / `NUMBERS-OK`, exit 0 |
| `python -B .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py figure` | `figure times 1001` / `FIGURE-OK`, exit 0 |
| `python -B .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py inputs` | `INPUTS-OK`, exit 0 |
| `python -B .planning/phases/64-feasibility-verdict/evidence/verify_phase64_verdict.py frozen` | `frozen paths pinned=33 sealed=8 trees=4` / `FROZEN-OK`, exit 0 |
| `grep -c '^## ' .planning/phases/64-feasibility-verdict/64-VERDICT.md` | `15` |
| `git ls-files --error-unmatch .planning/phases/64-feasibility-verdict/64-VERDICT.md` | tracked, exit 0 |

**Hand mutant:** replacing the digit-boundary render match with a plain substring made `test_digit_boundary_does_not_match_inside_a_longer_number` fail; the file was restored byte-identically and the test passed again.

## Requirements Coverage

- **FEAS-06** — met by `64-VERDICT.md` with RULES-OK and NUMBERS-OK: the rule's result, the empty-edge reasons, the comparisons, the ladder, the cost, the next-level statement and the next milestone are all present and mechanically checked.

## Known Stubs

None. The verdict is complete and ready for checkpoint ①; the only pending values are the owner's decision and signature (`owner_decision: pending`, `ruling_citation: pending`), which are the checkpoint's subject, not stubs.

## Threat Flags

None. The plan's mitigations are in place: T-64-11 (home-directory scan over the verdict, manifest, SVG and provenance), T-64-12 (every cited digest recomputed), T-64-09 (all 161 verdict-required renders), T-64-02 (the exact label and the front-matter value).

## Self-Check: PASSED

- `64-VERDICT.md` exists, is tracked, and hashes to `b0507c03…`.
- `bd768374` and `e2a8c407` exist in the log; the two task commits name only the three plan files (this SUMMARY commit adds the fourth).
- The verifier and the test module are committed clean; all six mode outputs above are the committed files' outputs.
- `.planning/STATE.md`, `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`, `pinn/`, the framework specs and the Phase 59/60 evidence are untouched by this plan's commits.

## Orchestrator correction after the plan run

`4b2bae05 fix(64-04): correct the 4658 below-formula cell` changed one table cell. The per-arm table read `no (Tier 0; numerically below)` for r1-4658, contradicting the manifest entry `rung1.below_formula_systems` = `4658` and the verdict's own sentence at `## The result under the pre-registered rule` that Rung 1's E is below the formula's only on 4658, 1 of 3. E 1.1432 is strictly below the formula's 1.9697, so the cell now reads `yes (Tier 0)`; the arm still ends at Tier 0.

The verdict's SHA-256 is therefore `dd1a078d820eaf08c56ecb55e6a285fbfeb3a4f4120faff1675a1e72918a372a`, not the `b0507c03…` recorded above. Re-verified after the correction: `RULES-OK`, `NUMBERS-OK`, `FIGURE-OK`, `INPUTS-OK`, `DERIVE-OK`, `FROZEN-OK`, and 168 tests `OK`.
