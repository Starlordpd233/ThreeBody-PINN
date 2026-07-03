---
phase: 30-research-package-assembly
plan: 05
subsystem: research-package-assembly (specwork / ERW delivery)
tags: [erw, doc-03, curriculum, training-loop, research-package, gate-open, repo-blind]

# Dependency graph
requires:
  - phase: 30-04
    provides: framed-research-questions.md, scope-12-hard-constraints.md, resolution-doc-skeleton.md (authored companions)
  - phase: 30-03
    provides: specs/ snapshots (6 intact + consolidated-context.md), verified-facts-reference.md, source_baseline pin
  - phase: 30-01
    provides: claims-register.md seed, 30-SNAPSHOT-HASHES.txt, reports characterization
provides:
  - RESEARCH-CONTEXT-MASTER.md (single uploaded entry point — preamble + manifest + reading order)
  - RESEARCH-AGENT-PROMPT.md (paste-ready prompt + attach-list header)
  - DELIVERY-NOTE.md (user-only routing + gate semantics, at the round root)
  - external resolution-doc gate OPEN (recorded in STATE.md via gsd-tools handlers)
affects: [phase-31, phase-32, phase-33, phase-34, phase-35, phase-36, erw-external-research]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Multi-companion ERW package: master references companions by bare filename, never folds them"
    - "Repo-blind uploads: zero repo paths in master+prompt; routing isolated to the never-uploaded delivery note"
    - "Gate-open via named gsd-tools state handlers (add-decision --phase/--summary, add-blocker --text); counters hand-restored after the known regression bug"

key-files:
  created:
    - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/RESEARCH-CONTEXT-MASTER.md
    - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_package/RESEARCH-AGENT-PROMPT.md
    - pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/DELIVERY-NOTE.md
  modified:
    - .planning/STATE.md

key-decisions:
  - "DELIVERY-NOTE.md placed at the round root (not in research_package/) — it is the only repo-path-bearing, never-uploaded file"
  - "original delivery source_baseline pinned to assembly-time HEAD 522cea7182bf3d0e3206d8faa75150e705b174f0; audit refresh superseded the current package baseline to 3781d1a68a9364717d399e536b7fc9ad56e19645 after a path-only CTL citation repair"
  - "STATE counter + status/session regressions from the gsd-tools handlers hand-restored per the documented bug remediation; only the gate-open decision + blocker + a benign last_updated timestamp remain as net changes"

patterns-established:
  - "F12 self-containment cross-check (both directions) gates delivery: every shipped file in the manifest; every manifest/attach-list bare filename resolves to a shipped file"

requirements-completed: [PKG-05, PKG-06, PKG-07]

# Metrics
duration: ~20min
completed: 2026-06-18
---

# Phase 30 Plan 05: Finalize and Deliver issue-03 Research Package Summary

**Delivered the complete repo-blind doc-03 ERW package (single-entry-point master + paste-ready prompt + round-root delivery note over the existing companions/snapshots), passed the F12 self-containment cross-check both directions, and opened the external resolution-doc gate via gsd-tools handlers with STATE progress counters verified unchanged.**

## Performance

- **Duration:** ~20 min
- **Started:** 2026-06-18T08:42Z (approx)
- **Completed:** 2026-06-18T09:01:55Z
- **Tasks:** 3
- **Files modified:** 4 (3 created + STATE.md)

## Accomplishments
- Authored `RESEARCH-CONTEXT-MASTER.md` as the single uploaded entry point — source-treatment preamble (issue-doc non-authoritative; specs source of truth; non-literal SCOPE-10 pinn override; locked-vs-revisable; figures-are-claims) + a complete bare-filename per-file manifest (all 5 companions incl. `claims-register.md` + 7 `specs/` entries + the master + prompt) + reading order; `source_baseline` pinned to assembly-time HEAD; companions referenced, never folded (multi-companion form).
- Authored `RESEARCH-AGENT-PROMPT.md` — paste-ready, ships with the master, attach-list header by bare filename (incl. `claims-register.md`), work-from-attached-only + log-silence-in-the-claims-register instruction (ERW rule 9).
- Ran the F12 end-to-end self-containment cross-check; both directions pass (no dropped file, no dangling manifest/attach row).
- Authored `DELIVERY-NOTE.md` at the round root: landing path + the "Phases 32-36 gate on the consolidated doc landing AND Phase 31 passing" sentence; DROPPED the v1.5 "Phase 24 runs in parallel" section; ADDED the no-in-milestone-verification note (D-17).
- Recorded the gate-open state in STATE.md via named gsd-tools handlers only (add-decision + add-blocker); restored the handler-induced counter + status/session regressions so net STATE change is just the gate record + a benign timestamp.

## Task Commits

This plan delivers the complete package as ONE atomic commit (the package finalization is a single delivery; tasks are not independently committable). All three tasks + the SUMMARY + the handler-produced STATE.md change ship together:

1. **Task 1: Author RESEARCH-CONTEXT-MASTER.md** — atomic delivery commit (docs)
2. **Task 2: Author RESEARCH-AGENT-PROMPT.md** — atomic delivery commit (docs)
3. **Task 3: F12 cross-check + DELIVERY-NOTE.md + gate-open + commit** — atomic delivery commit (docs)

**Commit message:** `docs(30-05): finalize and deliver issue-03 research package`

## Files Created/Modified
- `…/03-curriculum-and-training-loop/research_package/RESEARCH-CONTEXT-MASTER.md` — single uploaded entry point (preamble + manifest + reading order)
- `…/03-curriculum-and-training-loop/research_package/RESEARCH-AGENT-PROMPT.md` — paste-ready prompt + attach-list header
- `…/03-curriculum-and-training-loop/DELIVERY-NOTE.md` — user-only routing + gate semantics (round root)
- `.planning/STATE.md` — gate-open decision + downstream blocker (via handlers); counters/status/session hand-restored after the known regression

## Decisions Made
- Placed `DELIVERY-NOTE.md` at the round root, not inside `research_package/` (grounded in D-03/D-20: it is user-only, never uploaded, and the sole repo-path-bearing file).
- Kept the multi-companion form (locked 30-02): the master references the companions by bare filename and folds nothing.
- Pinned `source_baseline` to `522cea7182bf3d0e3206d8faa75150e705b174f0` (assembly-time HEAD, from `30-SNAPSHOT-HASHES.txt`, F7).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Restored gsd-tools handler regressions to STATE.md**
- **Found during:** Task 3 (gate-open recording)
- **Issue:** Running `gsd-tools state add-decision` / `add-blocker` regressed the STATE.md `progress` counters (`total_plans 5→6`, `completed_plans 2→4`) and the frontmatter `status`/`stopped_at`/`last_activity` fields to a stale earlier framing — the documented state-verb regression bug. The plan (F2) requires counters unchanged (the orchestrator owns advancement) and scopes this commit's STATE mutation to the gate-open decision + blocker only.
- **Fix:** Captured the pre-handler STATE.md to `/tmp/STATE.before-30-05.md`, diffed, and hand-corrected the regressed counter lines and the three regressed frontmatter fields back to their before-values, leaving the handler-added decision + blocker (and the benign `last_updated` timestamp refresh) intact.
- **Files modified:** `.planning/STATE.md`
- **Verification:** `diff /tmp/STATE.before-30-05.md .planning/STATE.md` shows only the `last_updated` timestamp, the gate-open decision (line 167), and the downstream blocker (line 190); the `progress` block is byte-identical to before.
- **Committed in:** the atomic delivery commit

---

**Total deviations:** 1 auto-fixed (1 bug — the documented gsd-tools state-verb regression).
**Impact on plan:** Necessary to honor the F2 "counters unchanged" invariant; no scope creep. The gate-open record itself was produced via the handlers as mandated (D-21).

## Issues Encountered
- The F12 direction-(b) check initially reported false "DANGLING" results due to shell word-splitting artifacts in the verification script (a `grep -oE` filename prefix and a non-splitting variable). Re-run with `grep -h` + a `while read` loop confirmed all 14 bare-filename references resolve to shipped files. No package defect.

## User Setup Required
None - no external service configuration required. The delivery note instructs the user on running the ERW multi-AI handoff (attach the package set, paste the prompt, collect resolutions).

## Next Phase Readiness
- The external resolution-doc gate is OPEN. The user's multi-AI ERW research can begin using the delivered package.
- Phase 31 (resolution-doc readiness verification) and Phases 32-36 remain blocked until the consolidated resolution doc lands at `…/research_reports/03-curriculum-and-training-loop/` AND Phase 31 passes — recorded as a STATE.md blocker.
- No STOP-protocol gap was encountered (the plan was mechanical assembly + delivery).

## Self-Check: PASSED

- Created files exist: RESEARCH-CONTEXT-MASTER.md, RESEARCH-AGENT-PROMPT.md, DELIVERY-NOTE.md, 30-05-SUMMARY.md — all FOUND.
- Commit `836415c4` present in history.
- Working tree clean after commit (Waves 3/4 artifacts untouched; no dangling changes).
- VC-01 leak grep returns 0 hits on both the master and the prompt.
- F12 self-containment cross-check passed both directions (14 shipped files all in the manifest; 14 bare-filename refs all resolve).
- STATE.md progress counters byte-identical to pre-handler capture (handler regression hand-restored).

_Note: the self-check ran after the atomic delivery commit; this SUMMARY annotation is committed in the plan-completion follow-up below._

---
*Phase: 30-research-package-assembly*
*Completed: 2026-06-18*
