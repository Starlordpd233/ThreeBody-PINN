---
phase: 56-contract-amendment-train-free-gate
plan: 04
subsystem: spec
tags: [scope-38, contract-amendment, causal-exponent, r-ref, frozen-reference, collocation, transcription, pinn-architecture]

requires:
  - phase: 54-recalibration-decision-grounding
    provides: 54-RULING.md checkpoint ② — the ratified A1 + B2 (residual-wide) + C1 + D3 + E1 surface set, the four SCOPE-38 re-ratification blocks (Blocks 1 and 4 carry the re-issued acceptance criteria), the "Batch allocation and bin policy" and "Reference invalidation" verbatim source paragraphs
  - phase: 56-contract-amendment-train-free-gate plan 01
    provides: the GATE-04 condition-(i) slice, the committed r_ref_stage0.json artifact (the reference's only legitimate producer), and the frozen Phase-57-facing contract
provides:
  - pinn_architecture.md §3.2 Phase 56 contract blockquote "causal-exponent argument amended" (Block 1, AMENDED additively; AC-LOSS-04 re-issued verbatim; Phase 35 block retained byte-identical above it)
  - pinn_architecture.md §3.2 Phase 56 contract blockquote "frozen residual reference" (the R_ref procedure, persistence obligation, and the verbatim fifteen-trigger invalidation list; no numeric value fixed)
  - pinn_architecture.md §3.2 Phase 56 contract blockquote "collocation allocation and time draw amended" (Block 4, AMENDED; 4096 total per batch exact, bin boundary convention, 240-slot replay-only construction verbatim, re-issued AC verbatim, SPEC-06 binding + re-check trigger)
affects: [phase-56-05, phase-56-03, phase-56-06, phase-57-run-04, fut-01-trainer-rebuild]

actuals:
  tokens: 2222
  tasks: 3
  commits: 3
  plan_head_before: 34cbe213b2a045faeffff01a38190a5478a66925

tech-stack:
  added: []
  patterns:
    - "SCOPE-38 additive amendment: the superseded contract blockquote stays byte-identical directly above its amendment; the amendment names the superseded ruling, transcribes provenance and the re-issued acceptance criterion verbatim, and closes by naming what it does NOT decide"
    - "Byte-exact transcription gate: python containment of ruling-source passages against the spec at execute time (extended by .planning/tmp/56-04-invalidation-check.py for the trigger list), not eyeballing"
    - "Anchor re-derivation by content match before every edit within the phase's own shifting file (54-RULING.md anchor-drift warning honored; no recorded line number was trusted)"

key-files:
  created: []
  modified:
    - pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md

key-decisions:
  - "Rendered the ratified relations in ASCII inline-code notation (`Rtilde_b = Rbar_b / R_ref`, `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rtilde_m))`) matching the retained Phase 35 block rather than authoring display mathematics — a presentation-only choice made by Task 1, recorded here per the plan's instruction and the STOP protocol's mechanical-choice class"
  - "Transcribed the reference-invalidation trigger list as running prose — its source form in 54-RULING.md — rather than reformatting to a bulleted list, so verbatim containment holds by construction (the plan's list-versus-prose presentation-only decision: prose, no reformatting occurred)"
  - "Placement: the three Phase 56 blockquotes sit immediately after the retained Phase 35 blockquote in §3.2 (Block 1 → frozen reference → Block 4), ahead of 'Collocation Point Sampling:'; Listing 3 and every pre-existing contract line are byte-identical (0 removed lines in the whole-plan diff)"
  - "Commit-message scope follows the orchestrator dispatch (`spec(56-04)`), not the plan's literal `spec(56)` naming; subjects shortened under the 80-char hook (see deviation 2)"

patterns-established:
  - "Re-issued acceptance criteria are embedded prefixed by 'Re-issued acceptance criterion:' and open with the ruling's own words ('AC-LOSS-04 is re-issued without a new identifier: ...' / 'A full 256-slot batch emits exactly 4096 physics rows ...') — no new identifiers are coined"
  - "Each amendment blockquote closes with an explicit not-decided sentence (GAP-54-06 L-BFGS deferral; GAP-56-01 condition-(ii) unratified), following the Phase 53 block's own model"

requirements-completed: [SPEC-01, SPEC-06]

coverage:
  - id: D1
    description: "§3.2 Phase 56 'causal-exponent argument amended' blockquote — additive Block 1 amendment naming Phase 35 D-04 / Option A / LOSS-04 / AC-LOSS-04, the 2026-09-04 provenance and A1+B2+C1+D3+E1 surface set, retention/governs sentence, verbatim re-issued AC-LOSS-04, and the not-decided close (L-BFGS deferral, GAP-56-01)"
    requirement: SPEC-01
    verification:
      - kind: other
        ref: "grep -c -F 'AC-LOSS-04 is re-issued without a new identifier' <spec> -> 1; grep -c -F 'Phase 35 contract: causal-training mode' <spec> -> 1"
        status: pass
      - kind: other
        ref: "python byte-exact containment of 54-RULING.md Block 1 provenance paragraph and re-issued AC against the spec -> True/True"
        status: pass
      - kind: other
        ref: "git diff -U0 HEAD -- <spec> removed-line contract-token gate (.planning/tmp/56-04-t1-diff.txt) -> CONTRACT_LINES_PRESERVED (0 removed lines)"
        status: pass
      - kind: other
        ref: "node tools/spec-render-check/detect.mjs --adjudications tools/spec-render-check/adjudications/22-02-pinn-architecture.json <spec> -> exit 1, 0 DEFINITE, totals identical to pre-edit baseline"
        status: pass
    human_judgment: false
  - id: D2
    description: "§3.2 Phase 56 'frozen residual reference' blockquote — the R_ref procedure (median of 96 raw bin means, two-central-order-statistics convention), detached/frozen for Stage 0 with residual-wide application, persistence obligation, the verbatim complete invalidation-trigger list, and the explicit no-numeric-value close"
    requirement: SPEC-01
    verification:
      - kind: other
        ref: ".venv/bin/python .planning/tmp/56-04-invalidation-check.py -> INVALIDATION_OK (every trigger name from the ruling paragraph present, closing fail-closed sentence present, full paragraph contained verbatim)"
        status: pass
      - kind: other
        ref: "grep -c -F 'Re-measure' <spec> -> 1; grep -cE '1\\.97[0-9]*e\\+?10|19749775821|1974977582' <spec> -> 0 (no illustrative reference figure in the spec)"
        status: pass
      - kind: other
        ref: "render oracle -> exit 1, 0 DEFINITE, totals identical to baseline"
        status: pass
    human_judgment: false
  - id: D3
    description: "§3.2 Phase 56 'collocation allocation and time draw amended' blockquote — 4096 rows total per training batch exact (not per trajectory, not a range), half-open/closed bin boundary convention, one batch-global exclusive 16-term prefix, verbatim batch-allocation/bin-policy paragraph, verbatim re-issued Block 4 AC, GAP-39-12 Option C supersession limited to the time-draw clause, SPEC-06 binding + re-check trigger; Listing 3 untouched"
    requirement: SPEC-06
    verification:
      - kind: other
        ref: "grep -c -F 'A full 256-slot batch emits exactly 4096 physics rows' <spec> -> 1; grep -c -F 'Empty bins are impossible' <spec> -> 1"
        status: pass
      - kind: other
        ref: "python byte-exact containment of the ruling's 'Batch allocation and bin policy' paragraph and Block 4 re-issued AC against the spec -> True/True"
        status: pass
      - kind: other
        ref: "git diff -U0 HEAD -- <spec> (.planning/tmp/56-04-t3-diff.txt) -> CONTRACT_LINES_PRESERVED; no hunk touches the Listing 3 collocation-sampling code block or its docstring"
        status: pass
      - kind: other
        ref: "render oracle -> exit 1, 0 DEFINITE, totals identical to baseline"
        status: pass
    human_judgment: false

duration: 15 min
completed: 2026-09-06
status: complete
---

# Phase 56 Plan 04: SCOPE-38 Amendment Core — §3.2 Contract Amendment Summary

**The ratified A1 + B2 (residual-wide) + C1 + D3 + E1 recalibration is now law in `pinn_architecture.md` §3.2 as three additive SCOPE-38 contract blockquotes — the amended causal-exponent argument (AC-LOSS-04 re-issued verbatim, Phase 35 block retained byte-identical above it), the frozen median-of-96 `R_ref` procedure with its complete verbatim invalidation-trigger list and no numeric value fixed, and the exact 4096-per-batch / 16-bin / 256-rows collocation and time-draw contract with its verbatim re-issued acceptance criterion and SPEC-06 binding — over a whole-plan diff containing zero removed lines and a clean render oracle.**

## Performance

- **Duration:** 15 min
- **Started:** 2026-09-06T13:26:30Z
- **Completed:** 2026-09-06T13:41:48Z
- **Tasks:** 3/3
- **Files modified:** 1 committed (`pinn_architecture.md`); 1 uncommitted verification script under `.planning/tmp/`

## Accomplishments

- Block 1 (the `η_c` causal-exponent contract) amended additively: the exponent now consumes the frozen-reference normalized bin residual as one batch-global exclusive sixteen-term prefix over sixteen bin means; the Phase 35 blockquote is retained byte-identical as the historical record, with the amendment stating that where the two differ the Phase 56 block governs.
- The frozen residual reference is defined as a *procedure* — finite positive median (two-central-order-statistics convention) of the 96 raw bin means from the fixed six-case GATE-04 initialization probe, detached and frozen for all of Stage 0, applied residual-wide, never updated online — with the ruling's fifteen-trigger invalidation list and fail-closed resource-failure sentence transcribed verbatim, and an explicit statement that no numeric value is fixed by the spec.
- Block 4 (collocation allocation and time draw) amended additively: `n_col = 4096` rows total per training batch (exact, not a range, not per trajectory), the sixteen fixed equal-`u` bin boundary convention, exactly 256 rows per bin, one batch-global exclusive 16-term prefix, the verbatim 240-slot replay-only construction (per-slot totals 17 or 18), microbatching never resetting the prefix, GAP-39-12 Option C superseded only as to its independent full-domain time-draw clause, and the SPEC-06 binding sentence with its re-check trigger cross-referencing the invalidation list.

## Task Commits

Each task was committed atomically:

1. **Task 1: Amend the causal-exponent contract (Block 1) additively in section 3.2** — `22489fb2` (spec)
2. **Task 2: Define the frozen residual reference and its invalidation triggers in section 3.2** — `740a390c` (spec)
3. **Task 3: Amend the collocation allocation and time-draw contract (Block 4) in section 3.2** — `e53ff47d` (spec)

**Plan metadata:** committed with this SUMMARY (`docs(56-04)`).

## Files Created/Modified

- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` (modified, +9 lines / −0) — one bridging sentence after the causal-loss equations plus the three Phase 56 contract blockquotes in §3.2; nothing else in the file changed.
- `.planning/tmp/56-04-invalidation-check.py` (created, uncommitted scratch) — Task 2's mandated acceptance script: parses the trigger list out of the ruling's "Reference invalidation" paragraph, asserts every trigger name and the closing fail-closed sentence appear in the spec's new block, asserts full verbatim containment, prints `INVALIDATION_OK`.

## Decisions Made

Recorded in frontmatter `key-decisions`. The load-bearing ones: the presentation-only inline-code notation choice (plan-mandated record); the invalidation list kept as running prose (its source form); the three-block additive placement after the retained Phase 35 blockquote; commit scope `56-04` per the orchestrator dispatch.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 — Bug] `56-04-invalidation-check.py` repository-root index off by one**
- **Found during:** Task 2 acceptance-criteria loop
- **Issue:** the script resolved the repo root as `parents[3]` of its own path; `.planning/tmp/` is two levels deep, so the ruling read failed with FileNotFoundError.
- **Fix:** corrected to `parents[2]`; re-ran.
- **Files modified:** `.planning/tmp/56-04-invalidation-check.py` (uncommitted verification artifact)
- **Verification:** `.venv/bin/python .planning/tmp/56-04-invalidation-check.py` → `INVALIDATION_OK`, exit 0
- **Committed in:** not committed (scratch verification script; the plan's `<verify>` commands reference it under `.planning/tmp/`)

**2. [Rule 3 — Blocking] Commit subjects shortened under the 80-character hook**
- **Found during:** Task 2 commit (first attempt rejected: "git policy: subject must be 80 characters or fewer")
- **Issue:** the plan's literal commit namings under scope `spec(56)` combined with the orchestrator-dispatched `56-04` task scope exceed this repo's 80-char subject limit (Task 2's would have been 96 chars).
- **Fix:** kept type and scope and shortened the subjects preserving meaning — `spec(56-04): define frozen residual reference and invalidation triggers` and `spec(56-04): amend section 3.2 collocation allocation and time-draw contract`; the full detail (superseded rulings, provenance, re-issued ACs) lives in the required `spec`-type bodies.
- **Files modified:** none (commit metadata only)
- **Verification:** both commits accepted by the hook chain on the first retry
- **Committed in:** `740a390c`, `e53ff47d`

**3. [Rule 1 — Bug] STATE.md counter regression by the gsd-tools mutating verbs (standing checkout issue), hand-repaired**
- **Found during:** close-out state updates
- **Issue:** `state.advance-plan` regressed `completed_phases` 3→2 and `percent` 50→33 and left stale position text ("Ready to execute", 56-01 references); `state.record-session` updated `stopped_at` but left the stale "Next action: execute 56-04". This is the documented standing behavior of these verbs in this checkout (54-10/54-11/56-01 all record the same class of repair; STATE.md carries its own hand-maintenance note).
- **Fix:** hand-set `completed_phases: 3`, `completed_plans: 20`, `percent: 53`, refreshed `last_activity_desc`, the Current Position block (plan 3 of 6; next 56-02/56-05 wave 2), and Session Continuity's next action. The metric row (`Phase 56 P04 | 15 min | 3 tasks | 1 files`) and the decision entry appended by the verbs were correct and retained.
- **Files modified:** `.planning/STATE.md`
- **Verification:** frontmatter and both blocks re-read after repair and confirmed forward-moving (19→20 plans, 50→53 percent, `completed_phases` restored to 3)
- **Committed in:** this plan's metadata commit

**Total deviations:** 3 auto-fixed (2 Rule 1, 1 Rule 3).
**Impact on plan:** none to scope or contract — the spec edits are exactly as planned; the deviations concern a scratch script's path bug, commit-message length compliance, and the known STATE.md tooling regression.

## Issues Encountered

None beyond the deviations above. REQUIREMENTS.md was deliberately not mutated: SPEC-01/SPEC-06 are shared with 56-05/56-06, whose SUMMARYs do not yet exist, and the ready-ids gate returned 0/2 — expected behavior, not an error (56-01 left GATE-04 untouched for the same reason).

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- §3.2 now carries the ratified recalibration law FUT-01's trainer rebuild is built from; ROADMAP Phase 56 success criteria 1 and 3 are met for the §3.2 surface this plan owns.
- **Ready for 56-05** (wave 2): the two NOT-AMENDED records (Blocks 2 and 3), the three secondary wordings (`collocation_count = 16` reconciliation prose, the Listing 3 recommended-range wording, the §4.1 `η_c` cross-reference), and render-oracle re-adjudication if 56-05's edits introduce findings (this plan introduced none — 0 DEFINITE, totals identical to the pre-edit baseline at every task boundary).
- **Ready for 56-02** (wave 2) and 56-03 (wave 3): the gate-side plans; unaffected by this plan's spec-only edits.
- GAP-56-01 and GAP-56-02 remain OPEN and untouched, as designed; the Block 1 blockquote explicitly defers the L-BFGS recomputation semantics (GAP-54-06) to the Phase 57 owner checkpoint and names GAP-56-01 as unratified.

---
*Phase: 56-contract-amendment-train-free-gate*
*Completed: 2026-09-06*

## Self-Check: PASSED

- Spec file exists and carries exactly one occurrence of each new Phase 56 blockquote lead (`causal-exponent argument amended`, `frozen residual reference`, `collocation allocation and time draw amended`) — verified by grep (1/1/1).
- `.planning/tmp/56-04-invalidation-check.py` exists and runs to `INVALIDATION_OK`.
- All three task commits exist in `git log --oneline --all`: `22489fb2`, `740a390c`, `e53ff47d`.
- Whole-plan diff (`34cbe213..HEAD`) contains zero removed lines; the render oracle reports 0 DEFINITE with totals identical to the pre-edit baseline.
