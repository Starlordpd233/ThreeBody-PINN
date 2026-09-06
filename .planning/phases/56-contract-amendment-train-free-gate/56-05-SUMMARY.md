---
phase: 56-contract-amendment-train-free-gate
plan: 05
subsystem: spec
tags: [scope-38, contract-amendment, not-amended, causal-exponent, collocation, render-oracle, pytest-guard, pinn-architecture]

requires:
  - phase: 56-contract-amendment-train-free-gate plan 04
    provides: the §3.2 AMENDED blocks (Block 1 causal-exponent argument, the frozen R_ref procedure, Block 4 collocation allocation/time-draw) this plan's Task 2 cross-references, and the 0-DEFINITE render-oracle baseline Tasks 1/2 build on
  - phase: 54-recalibration-decision-grounding
    provides: 54-RULING.md checkpoint ② Blocks 2 and 3 — the NOT AMENDED dispositions (first_omega_0 retain C1/D3-A; clip underflow-only purpose retain E1/D5-A with the observability addendum) this plan transcribes verbatim
provides:
  - pinn_architecture.md §2.2 "first_omega_0 fixed-at-30 sentence NOT AMENDED" blockquote, naming Phase 20 ARCH-01 as the continuing acceptance criterion and GAP-56-02 as the deliberately-untouched §2.4 table item
  - pinn_architecture.md §4.1 "causal-exponent clip underflow-only purpose NOT AMENDED" blockquote, transcribing the ruling's observability addendum (reject non-finite before clipping, log unclipped exponent + guard-binding count, fail GATE-04 on init-time binding) and stating explicitly this is observability, not a repurposing of the clip
  - Three secondary reconciliation sentences: §3.2 run-driver collocation_count=16 vs ratified 4096-total divergence (D-03, SPEC-06), Listing 3's recommended-range wording reconciled as historical (D-11, closes 53-UNSWEPT-INVENTORY item 5), §4.1 eta_c=1 default bullet cross-referencing the §3.2 re-issued AC-LOSS-04 instead of restating the formula (D-10)
  - Corrected and extended render-oracle adjudication file (tools/spec-render-check/adjudications/22-02-pinn-architecture.json, 8 entries) — six pre-existing entries re-derived by content match after a +2 line shift, one new entry for the NOT-AMENDED blockquote's first_omega_0 citations
  - tests/phase56/test_spec_amendment_contract.py (13 tests) — the committed post-phase guard protecting the whole SCOPE-38 transcription after this plan's plan-time shell gates disappear
affects: [phase-56-03, phase-56-06, phase-57-run-04, fut-01-trainer-rebuild]

actuals:
  tokens: 3406
  tasks: 3
  commits: 3
  plan_head_before: 75c63b3c83aa9a65e39b709acc09576466a57a22

tech-stack:
  added: []
  patterns:
    - "NOT-AMENDED contract blocks reuse the AMENDED blocks' header shape ('Phase 56 contract: <name> NOT AMENDED (...)') but state NOT AMENDED both in the header and the body, transcribe the ruling's disposition marker, and close with an explicit not-decided sentence naming what remains open (GAP-56-02 for the SIREN block; the clip-bound deferral for the clip block) — mirrors the AMENDED blocks' own not-decided-close convention from plan 56-04."
    - "Secondary reconciliation prose (D-03/D-10/D-11) is written as plain paragraphs (not 'Phase 56 contract:' blockquotes), since these are cross-reference/reconciliation sentences rather than ratified contract dispositions, and each cross-references the ratified block by stable identifier (AC-LOSS-04) rather than restating its formula, so it cannot drift from the source of truth."
    - "Committed pytest content-match guard, paired with plan-time shell verify gates: the shell gates (removed-line negative-diff, section-2.4-untouched, render-oracle re-run) catch a bad edit when it is made and vanish with the plan; the pytest file runs with the ordinary suite afterward, including a line/token-position check over the adjudication file itself (not just a schema check) that proves it stays synchronized with the live spec."

key-files:
  created:
    - tests/phase56/test_spec_amendment_contract.py
  modified:
    - pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
    - tools/spec-render-check/adjudications/22-02-pinn-architecture.json

key-decisions:
  - "Both NOT-AMENDED blockquotes are inserted immediately after the specific paragraph/bullet containing the locked sentence (interrupting the enclosing numbered list in §2.2 and the enclosing bullet list in §4.1), not after the whole enclosing list — a literal reading of the plan's 'immediately after the paragraph/block containing it' instruction, and an editorial placement choice 56-CONTEXT.md's 'Claude's Discretion' section explicitly authorizes. Verified render-safe beforehand: neither insertion point falls within ±20 lines of an author-comment marker in a way that changes the outcome for §4.1 (outside any window) and any new D5 finding in §2.2's window was adjudicated in Task 3, not avoided by relocating the block."
  - "Commit scope used '56-05' (task-style) for all three commits, including Tasks 1 and 2 whose plan text literally specified the phase-style scope 'spec(56)'. Both scopes pass the commit-msg hook's PHASE_SCOPE_RE/TASK_SCOPE_RE; this is a consistency choice (matching Task 3's own plan-specified '56-05' scope and plan 56-04's established phase precedent), not a hook-forced rewrite."
  - "The twelve pre-existing, unrelated Phase 34/35 REVIEW findings in §3.4/§4.2 (delta_E, ctl_instruction.md, IPR_train, mu_p, lambda_p, torch.no_grad(), [1e-4, 100]) are left unadjudicated, exactly as they were before Phase 56 touched anything. This keeps the render oracle's exit code at 1, matching the plan's own <verify> tolerance ('fails_when: exit code greater than 1') and the identical baseline every 56-04 task already inherited — adjudicating them would be undirected scope creep outside this plan's SCOPE-38 grant."
  - "STATE.md frontmatter counters (completed_phases regressed 3→2, matching the identical standing gsd-tools mutating-verb corruption 54-08/54-09/54-10/54-11/56-04 all independently hand-repaired in this checkout) were re-derived from disk truth and hand-repaired rather than replayed from the corrupted value or left stale."

requirements-completed: [SPEC-01, SPEC-06]

coverage:
  - id: D1
    description: "Two NOT-AMENDED SCOPE-38 contracts recorded separately and by name — §2.2 first_omega_0 fixed-at-30 (Phase 20 ARCH-01 named as continuing AC, GAP-56-02 named for the deliberately-untouched §2.4 table) and §4.1 clip underflow-only purpose (dtype/device normal-floor guard + Phase 35 deferred-bound guard both named unchanged, ruling's observability addendum transcribed, explicit 'not a repurposing' sentence, no numeric bound chosen)"
    requirement: SPEC-01
    verification:
      - kind: other
        ref: "git diff -U0 HEAD -- <spec> negative-diff gate (.planning/tmp/56-05-t1-diff.txt) -> CONTRACT_LINES_PRESERVED; grep -c -F 'NOT AMENDED' <spec> -> 2 (later 4 after both blocks land)"
        status: pass
      - kind: other
        ref: "git diff HEAD -- <spec> section-2.4-table gate (.planning/tmp/56-05-t1-full.txt) -> TABLE_UNTOUCHED"
        status: pass
      - kind: other
        ref: "node tools/spec-render-check/detect.mjs --adjudications <adjudications> <spec> -> exit 1, 0 DEFINITE"
        status: pass
    human_judgment: false
  - id: D2
    description: "Three secondary reconciliation wordings landed in prose only: §3.2 run-driver collocation_count=16 vs ratified 4096-total-per-batch divergence (D-03, no pinn/ file touched), Listing 3's 'recommended: 2048-4096' wording reconciled as historical (D-11, code listing byte-unchanged), §4.1 eta_c=1 default bullet cross-referencing the §3.2 re-issued AC-LOSS-04 (D-10, formula not restated, coefficient value byte-preserved)"
    requirement: SPEC-06
    verification:
      - kind: other
        ref: "git status --porcelain -- pinn/ -> empty"
        status: pass
      - kind: other
        ref: "git diff -U0 HEAD -- <spec> negative-diff gate (.planning/tmp/56-05-t2-diff.txt) -> CONTRACT_LINES_PRESERVED"
        status: pass
      - kind: other
        ref: "grep -c -F 'def sample_collocation_points' <spec> -> 1; node tools/spec-render-check/detect.mjs ... -> exit 1, 0 DEFINITE"
        status: pass
    human_judgment: false
  - id: D3
    description: "Render oracle re-adjudicated over the amended prose (6 pre-existing entries corrected for the +2 line shift, 1 new entry for the NOT-AMENDED blockquote's first_omega_0 citations) and the whole transcription protected by a committed pytest guard (tests/phase56/test_spec_amendment_contract.py, 13 tests: both re-issued acceptance criteria verbatim, both NOT AMENDED markers, both original locked sentences byte-identical, no illustrative R_ref figure literal, the collocation/causal-coefficient reconciliation sentences, adjudication schema + live line/token-position integrity)"
    requirement: SPEC-01
    verification:
      - kind: unit
        ref: ".venv/bin/python -m pytest tests/phase56/test_spec_amendment_contract.py -x -q -> 13 passed"
        status: pass
      - kind: other
        ref: "node tools/spec-render-check/detect.mjs --adjudications <adjudications> <spec> -> exit 1 (<=1), 0 DEFINITE, 12 REVIEW (pre-existing/unrelated), 10 ADJUDICATED, 14 SUPPRESSED"
        status: pass
      - kind: other
        ref: ".venv/bin/python -c \"... assert not bad ...\" -> ADJUDICATIONS_OK"
        status: pass
      - kind: integration
        ref: ".venv/bin/python -m pytest tests/phase56/ -q -> 46 passed, 24 subtests passed (0:07:16)"
        status: pass
    human_judgment: false

duration: 15 min
completed: 2026-09-06
status: complete
---

# Phase 56 Plan 05: SCOPE-38 Amendment Completion Summary

**Both SCOPE-38 NOT-AMENDED contracts (§2.2 `first_omega_0`, §4.1 clip underflow-only purpose) are now recorded separately and by name in `pinn_architecture.md`, three secondary reconciliation sentences dispose of the collocation-count and causal-coefficient wordings the recalibration forced, the render-oracle adjudication file is re-derived and extended, and a 13-test committed pytest guard (`tests/phase56/test_spec_amendment_contract.py`) protects the whole SCOPE-38 transcription after this plan closes — over a whole-plan diff with exactly one removed line (the authorized `eta_c` cross-reference edit) and a render oracle reporting 0 DEFINITE.**

## Performance

- **Duration:** 15 min
- **Started:** 2026-09-06T17:15:29Z
- **Completed:** 2026-09-06T17:30:30Z
- **Tasks:** 3/3
- **Files modified:** 2 modified (`pinn_architecture.md`, the render-oracle adjudication file); 1 created (`tests/phase56/test_spec_amendment_contract.py`)

## Accomplishments

- §2.2 now carries a "first_omega_0 fixed-at-30 sentence NOT AMENDED" blockquote immediately after the SIREN first-layer paragraph: names the retain disposition (C1/D3-A), names Phase 20 ARCH-01 as the continuing acceptance criterion, and names GAP-56-02 as the open item covering the §2.4 table's misleading "Recommended Value" heading for the same parameter — deliberately left untouched.
- §4.1 now carries a "causal-exponent clip underflow-only purpose NOT AMENDED" blockquote immediately after the clip-purpose bullet: names the retain disposition (E1/D5-A), names both guards (dtype/device normal-floor guard, Phase 35 deferred-numeric-bound guard) as unchanged, transcribes the ruling's observability addendum (reject non-finite before clipping; log the unclipped exponent and guard-binding count; fail GATE-04 if the guard binds at initialization), and states plainly that this added behaviour is observability, not a repurposing of the clip into a floor-raiser.
- Three secondary wordings land, each cross-referencing rather than restating: §3.2 names both `pinn/train.py:1033`'s `collocation_count = 16` and the ratified 4096-row-per-batch total as divergent today, states the FUT-01 trainer rebuild must honour the ratified structure, and states no production file is edited (D-03); a new paragraph after Listing 3 records the "recommended: 2048-4096" docstring wording as historical against the now-fixed 4096 total, leaving the listing byte-unchanged (D-11, closes 53-UNSWEPT-INVENTORY item 5); the §4.1 `eta_c = 1` default bullet now points at the §3.2 re-issued AC-LOSS-04 for the exponent's governing argument instead of standing beside the still-displayed raw-residual formula as though it were current (D-10).
- The render-oracle adjudication file is re-derived and extended: six of the seven pre-existing entries had drifted +2 lines out of position after the §2.2 insertion (re-verified by content match per 54-RULING.md's anchor-drift warning, not assumed) and are corrected; one new entry adjudicates the three `first_omega_0` citations the new NOT-AMENDED blockquote introduces at line 188. The twelve pre-existing, unrelated Phase 34/35 REVIEW findings are left exactly as they were.
- `tests/phase56/test_spec_amendment_contract.py` lands as the committed post-phase guard: 13 tests assert both re-issued acceptance criteria verbatim, the batch-allocation bin-policy and reference-invalidation sentences, at least two NOT AMENDED markers, both original locked sentences byte-identical, absence of the 56-RESEARCH.md b.2 illustrative `R_ref` figure literal, the three secondary reconciliation sentences, and that every adjudication entry carries its five required keys plus a non-empty rationale and points at a live spec line that actually contains its token. RED/GREEN genuinely proven for the line-position test (reverted to the pre-fix adjudication file, confirmed the test failed exactly as expected, restored the fix, confirmed green) rather than only narrated.

## Task Commits

Each task was committed atomically:

1. **Task 1: Record the two NOT AMENDED contracts separately and by name** — `75516b03` (spec)
2. **Task 2: Land the three secondary wordings the amendment forces** — `b56e3e06` (spec)
3. **Task 3: Re-adjudicate the render oracle and commit the amendment's post-phase guard** — `499ca8bf` (test)

**Plan metadata:** committed with this SUMMARY (`docs(56-05)`).

## Files Created/Modified

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (modified, +10/−1 across the plan) — two NOT-AMENDED contract blockquotes (§2.2, §4.1) and three secondary reconciliation paragraphs/edits (§3.2 run-driver, Listing 3 recommended-range, §4.1 eta_c cross-reference); the single removed line is the authorized D-10 in-place edit.
- `tools/spec-render-check/adjudications/22-02-pinn-architecture.json` (modified, 7 → 8 entries) — six pre-existing entries' line numbers corrected for the +2 shift; one new entry for the line-188 `first_omega_0` citations.
- `tests/phase56/test_spec_amendment_contract.py` (created, 201 lines, 13 tests) — the committed content-match guard.

## Decisions Made

Recorded in full in frontmatter `key-decisions`. The load-bearing ones: tight/adjacent NOT-AMENDED blockquote placement (interrupting the enclosing list, per 56-CONTEXT.md's placement discretion); D-03/D-11 written as plain reconciliation paragraphs rather than "Phase 56 contract:" blockquotes, since the plan's own artifact table calls them "sentence"/"spec prose" rather than a ratified disposition; commit scope `56-05` used uniformly (a consistency choice, not a hook rejection); the twelve pre-existing unrelated REVIEW findings left unadjudicated, matching baseline and plan 56-04's own precedent; STATE.md counter hand-repair for the standing tooling-corruption issue.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] STATE.md `completed_phases` regressed 3→2 again (standing gsd-tools mutating-verb corruption in this checkout), hand-repaired**
- **Found during:** close-out state updates
- **Issue:** `STATE.md` frontmatter showed `completed_phases: 2` / `completed_plans: 21` / `percent: 33`, even though plan 56-04's own SUMMARY (deviation 3) had already hand-set `completed_phases: 3` earlier the same day. Plan 56-02's own state-update step re-regressed it — the identical class of tooling defect independently documented and hand-repaired by 54-08, 54-09, 54-10, 54-11, and 56-04 in this exact checkout.
- **Fix:** Re-derived from disk truth rather than trusting either the corrupted value or a blind increment: counted every `*-SUMMARY.md` file across the four v2.3 phase directories (53: 1, 54: 13, 55: 4, 56: 3 pre-existing) = 21, matching the pre-repair `completed_plans` value exactly (so that field was NOT corrupted); `completed_phases` corrected to 3 (Phases 53/54/55 all carry `status: complete` / are recorded complete in PROJECT.md — Phase 56 is still executing). Added this plan's own SUMMARY to bring `completed_plans` to 22. `percent` recomputed as `completed_phases / total_phases * 100` = `3/6*100` = 50 (the field's exact original formula is not independently re-derivable from source in this session; 50 is the simplest defensible value consistent with the corrected phase count, flagged here rather than asserted as authoritative).
- **Files modified:** `.planning/STATE.md`
- **Verification:** Frontmatter re-read after repair; `completed_phases: 3`, `completed_plans: 22`, `percent: 50`; cross-checked `completed_plans` against a fresh `ls .../*-SUMMARY.md | wc -l` = 22 (post-repair, including this plan's new file).
- **Committed in:** this plan's metadata commit

**Total deviations:** 1 auto-fixed (Rule 1).
**Impact on plan:** none to scope or contract — the spec/adjudication/test edits are exactly as planned; the deviation concerns only the known STATE.md tooling regression, a pre-existing condition this plan's own edits did not cause.

## Issues Encountered

**GATE-04 test-suite side effect on a committed artifact (not a deviation — correctly scoped out, not committed).** Running the full `tests/phase56/` suite (Task 3's fourth `<verify>` command) invokes GATE-04's real computation as a side effect, which overwrote `pinn/verification/artifacts/r_ref_stage0.json`'s `provenance.git_sha` / `provenance.timestamp` fields to reflect the then-current HEAD and run time. The artifact's substantive content (`r_ref` value, all 96 `raw_bin_means`) was byte-identical before and after — confirmed by inspecting the diff before deciding how to handle it. This file is not in Task 3's declared `<files>` list and this plan does not own it (plan 56-01/56-02's territory), so the working-tree change was reverted with `git checkout -- pinn/verification/artifacts/r_ref_stage0.json` rather than committed, keeping this plan's diff exactly scoped to its three declared files.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- ROADMAP Phase 56 success criteria 2 and 3 are now met: both locked contracts the recalibration could have touched are dispositioned separately and by name (criterion 2), and the collocation-count divergence is disposed of in prose with its re-check trigger (criterion 3, closed jointly with plan 56-04).
- **Ready for 56-03** (wave 3): the SC5 demonstration (pre-amendment recipe frozen as a fixture, GATE-04 proven to return BLOCK on all six audited cases) is unaffected by this plan's spec-only edits and does not depend on anything this plan produced beyond the already-committed §3.2 amendment.
- **Ready for 56-06** (wave 4, phase close-out): `56-OPEN-ITEMS.md` can now record GAP-56-01 and GAP-56-02 as still OPEN (both deliberately untouched by this plan, per its prohibitions) alongside the two `front_idx` structural findings and the `tests/phase38` stale-guard scoping decision noted in 56-RESEARCH.md A.9. The `first_omega_0`/underflow NOT-AMENDED records give the close-out plan a citable, by-name disposition for both surfaces rather than silence.
- GAP-56-01 and GAP-56-02 remain OPEN and untouched, as designed by this plan's prohibitions.
- REQUIREMENTS.md SPEC-01/SPEC-06 checkboxes deliberately NOT flipped by this executor, following the same phase-close/verification-act precedent plans 54-*, 55-*, and 56-04 all established in this milestone (SPEC-01 is additionally shared with the not-yet-executed 56-06; SPEC-06 has no further owning plan but the convention is applied uniformly rather than selectively).

---
*Phase: 56-contract-amendment-train-free-gate*
*Completed: 2026-09-06*

## Self-Check: PASSED

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` exists and contains both new blockquote leads exactly once each (`first_omega_0` fixed-at-30 sentence NOT AMENDED`, `causal-exponent clip underflow-only purpose NOT AMENDED`) — verified by grep (1/1).
- `tests/phase56/test_spec_amendment_contract.py` exists and all 13 tests pass (`.venv/bin/python -m pytest tests/phase56/test_spec_amendment_contract.py -q` → `13 passed`).
- `tools/spec-render-check/adjudications/22-02-pinn-architecture.json` exists, parses as JSON, and every one of its 8 entries carries the five required keys and a non-empty rationale.
- All three task commits exist in `git log --oneline --all`: `75516b03`, `b56e3e06`, `499ca8bf`.
- Whole-plan diff (`75c63b3c..HEAD`) contains exactly one removed line (the authorized `eta_c` cross-reference edit); the render oracle reports 0 DEFINITE with the pre-existing unrelated REVIEW set unchanged in kind.
