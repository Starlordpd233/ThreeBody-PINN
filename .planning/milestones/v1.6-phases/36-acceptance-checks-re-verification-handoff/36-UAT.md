---
status: complete
phase: 36-acceptance-checks-re-verification-handoff
source: [36-01-SUMMARY.md, 36-02-SUMMARY.md, 36-03-SUMMARY.md, 36-04-SUMMARY.md, 36-05-SUMMARY.md]
started: 2026-07-02T01:23:00Z
updated: 2026-07-02T01:36:00Z
verifier: agent-b-verifier (autonomous; user away ~4h, full-autonomy directive)
verdict: PASS
---

# Phase 36 — UAT / Independent Verification Record

**Verdict: PASS.** Phase 36 execution is independently verified. The acceptance-check suite is honest and reproducible, the 15→0 fix was probe-only (no spec was edited to make probes pass), every protected path is untouched, and the v1.6 closure gate is satisfied.

This UAT was performed **autonomously by Agent B (verifier)** after the watchdog confirmed the executor (Agent A) had reached its terminal `verify(36):` commit (`05ae7698`, 2026-07-02 09:06 +0800). The user was away; per their full-autonomy directive, all checks below are deterministic/auto-verified — no human-UAT checkpoints apply to this specwork-closure phase.

## Current Test

[testing complete]

## Verification approach

The central risk for a phase that ended 15/26 FAIL → 26/26 PASS via a commit titled *"widen probe patterns"* is that the probes were **loosened to mask still-wrong specs** rather than fixed because they were over-strict. Three independent legs settle it:

1. **Independent re-run** — execute all 27 probes myself into a separate evidence dir.
2. **Legitimacy scrutiny** — read the actual widen-diff (`cfa643c0`) and confirm every semantic fix still has a real FAIL path; confirm each "rejection-context" claim against the spec text.
3. **Scope + spec-edit audit** — confirm what (if anything) Phase 36 edited, especially the protected paths.

## Tests

### 1. AC suite — independent re-run (reproducibility)
expected: All 27 probes (26 acceptance + 1 traceability) PASS when re-run by the verifier, into a separate evidence dir, matching the executor's claimed 27/27.
result: pass
source: automated
evidence: |
  Verifier re-run 2026-07-02T01:27:56Z, PYTHONHASHSEED=0, Python 3.14.5, driver exit 0.
  Evidence captured to /tmp/phase36-verifier-evidence/ (28 files; sealed evidence/ and evidence/final-rerun/ untouched).
  Result line: "summary: 27 pass / 0 fail (expect 26 acceptance + 1 traceability = 27 pass, 0 fail)".
  Every per-probe line read "PASS". The executor's verdict is reproducible, not fabricated or env-specific.

### 2. Probe-widen legitimacy — every semantic fix retains a real FAIL path
expected: The 15 FAIL→PASS fixes in commit cfa643c0 (15 files, +280/-79) are honest pattern-tolerances, not no-ops. Each fix that loosened a check must still FAIL when the wrong condition genuinely holds.
result: pass
source: automated
evidence: |
  Read the full cfa643c0 diff. Findings:
  - Rejection-context fixes (ac-curr-01 "Table 4", ac-curr-03 "automatic degraded advancement",
    ac-curr-04 np.clip, ac-loss-01 "linear-momentum", ac-evid-15-d-conflict "6.694") all keep a FAIL
    branch that fires when the token appears WITHOUT a rejection marker. They are more PRECISE, not lenient.
  - ac-evid-15-d-conflict check [3] iterates EVERY 6.694 mention and FAILs if any lacks ±12-line rejection
    context — stricter than the original absence check.
  - ac-loop-04 removed a buggy monotonic-by-stage assertion (C-schedule is intentionally 7→10 then drops
    to 5, 3); monotonicity is not a contract per the manifest. Legitimate bug fix.
  - Whitespace/Unicode/LaTeX fixes (ac-curr-05, ac-evid-15-d06, ac-loop-01, ac-loop-05, ac-loss-03 [1],
    ac-curr-04 [1]) are trivially benign.

### 3. Rejection-context claims match the actual spec language
expected: For every "X permitted only in rejection context" fix, the spec must actually mention X in rejection (not adoption).
result: pass
source: automated
evidence: |
  ctl_instruction.md:325  "Table 4 is NOT adopted wholesale; ADAPT-03 rejected; DGR-15"
  ctl_instruction.md:1971 "No automatic degraded advancement is [surfaces the stage for owner review]"
  pinn_architecture.md:310,625,654-656 "no linear-momentum / no-linear-momentum-loss term …
    linear momentum is enforced structurally … separate linear-momentum loss would be redundant"
  pinn_architecture.md:890 "Componentwise derivatives are required and the summed-output VJP remains forbidden"
  All four rejection-context families are genuine rejections in the spec. No fix masks an adoption.

### 4. Decisive — Phase 36 made ZERO framework-spec edits
expected: If the FAIL→PASS transition were achieved by weakening specs, ctl_instruction.md / pinn_architecture.md would show edits after Phase 36 began. They must show none.
result: pass
source: automated
evidence: |
  git diff --stat 9d4501b3..HEAD -- ctl_instruction.md        → EMPTY
  git diff --stat 9d4501b3..HEAD -- pinn_architecture.md      → EMPTY
  Phase 36 touched only artifacts (manifest, probes, evidence, ledger, handoff docs, REQUIREMENTS/ROADMAP).
  You cannot "pass by weakening the spec" when the spec was never touched — the fix direction was
  genuinely probe-only, exactly as 36-02-SUMMARY claims. Specs were already correct from Phases 33/34/35.

### 5. Protected-path SCOPE compliance
expected: pinn/ live code and the four frozen/read-only specs untouched since Phase 36 began.
result: pass
source: automated
evidence: |
  git diff --stat 9d4501b3..HEAD -- pinn/                     → EMPTY
  git diff --stat 9d4501b3..HEAD -- sampling_method.md,
    data_quality_assessment.md, review-of-framework.md,
    stage-strat-revision.md                                   → EMPTY
  git log 9d4501b3..HEAD -- (those paths)                     → no commits
  SCOPE-13 (editable targets) and the pinn/ live-code ban (SCOPE-05/10) both respected.

### 6. Protected-path guard is not over-narrowed
expected: ac-protected-path-guard was narrowed from "any pinn/ string" to import/Path() patterns (the old one false-positived on its own echo lines). Confirm no probe actually reads live pinn/ code via a path the narrower regex misses.
result: pass
source: automated
evidence: |
  Broad grep of probes/ for live pinn/ code paths (pinn/*.py, basic_architecture, data-processing),
  excluding the guard itself and comments → NONE.
  Every remaining "pinn" token is pinn_instruction/ (spec dir), pinn_architecture.md (spec), or a
  variable ($PINN, pinn_content). The narrowed guard is safe — there is no live-code reference for it
  to miss.

### 7. Phase 32 ledger terminal (VER-16, fail-closed)
expected: 18 finding rows, all VERIFIED, 0 PENDING/IN_PROGRESS/FIX_APPLIED.
result: pass
source: automated
evidence: |
  Independent awk tally of the ledger Status column (field 5, finding rows only):
    18 VERIFIED   (total finding rows: 18)   — 0 non-VERIFIED.
  D-05 and D-06 carry "2026-07-02 PENDING -> VERIFIED by Phase 36 Plan 36-03 Task 2" with SHA-256
  provenance (pre-write fb804f8b…, post-write 184cb56f…). Demote-on-regression check: only the two
  intended promotions changed.

### 8. REQUIREMENTS.md v1.6 traceability (VER-14)
expected: Exactly 32 v1.6 traceability rows (4 PKG + 5 EVID + 5 CURR + 8 LOOP + 4 LOSS + 6 VER), each mapped to exactly one phase.
result: pass
source: automated
evidence: |
  AC-TRACEABILITY probe (re-run by verifier, PASS) uses the precise anchored pattern
  ^\|\s*(PKG|EVID|CURR|LOOP|LOSS|VER)-\d+\s*\| and asserts len == 32. Confirmed.
  (Note: a naive grep counting "\| [A-Z]+-[0-9]" returns 33 because it also matches a scope-rule row,
  "| … | SCOPE-08 / SCOPE-09 |", which is not a traceability row. The probe's anchored family-specific
  pattern is correct; this is a loose-grep artifact, not a probe error.)

### 9. GAP-36-01 / GAP-36-02 anchor basis
expected: The 13 R6 status flips (esp. PKG-05..08 and LOOP-07/08, which lack dedicated ledger rows) must rest on user-ratified gaps, not agent invention.
result: pass
source: automated
evidence: |
  36-GAPS.md: GAP-36-01 (PKG terminal-anchor extension) — Status: RESOLVED-WITH-INSTRUCTION (2026-07-01).
  36-GAPS.md: GAP-36-02 (LOOP-07/08 anchored on 34-VERIFICATION.md truths 6-7) — RESOLVED-WITH-INSTRUCTION (2026-07-01).
  Both ratified via AskUserQuestion before execution. R6 reconciliation is grounded, not invented.

### 10. 36-PROBE-RESULTS.md — fail-closed run record
expected: OVERALL VERDICT PASS with a Final Rerun block; BLOCKED verdict clearly attributed to over-strict probes, not spec gaps.
result: pass
source: automated
evidence: |
  36-PROBE-RESULTS.md:14 "OVERALL VERDICT: PASS"; :16 "26/26 required probes passed (0 failures, 0 skips)";
  :304 "Final Rerun" block present with PASS verdict (:313); :18 attributes prior BLOCKED to over-strict
  disposable probe patterns. Per-probe blocks carry command, evidence path, SHA-256, observed metric, pass criterion.

### 11. 36-VERIFICATION.md — 7 must-have audits
expected: All 7 must-have audits (VER-13/14/15/16/17/18 + protected-path guard) satisfied.
result: pass
source: automated
evidence: |
  36-VERIFICATION.md frontmatter: status: passed, score: 7/7, gaps_remaining: [].
  Closure verdict lists all 7 audits satisfied. Independent re-checks above corroborate VER-13 (manifest),
  VER-14 (traceability), VER-15 (probes), VER-16 (ledger) directly.

## Summary

total: 11
passed: 11
issues: 0
pending: 0
skipped: 0
blocked: 0

## Observations (non-blocking, low severity — NOT gaps)

These are probe-rigor nitpicks. In every case the underlying spec is correct (confirmed above), so the
looser pattern does not mask a real defect. No fix plan is required for closure; recorded for an optional
future probe-tightening pass.

- **ac-loss-01-ad check [4]** accepts a bare "summed-output VJP" mention (any `summed-output VJP`). The spec
  forbids it (pinn_architecture.md:890), so no masking, but the pattern is weaker than the contract ("rejected").
  Severity: minor.
- **ac-loop-04 check [2]** C-schedule match accepts "5" and "3" within a 5-line window of "7-10" — could
  theoretically false-positive on unrelated digits. Schedule is correctly transcribed. Severity: minor.
- **ac-loss-02 check [4]** logging-first accepts broad patterns (`instrumentation.*log`, `observability first`).
  Spirit captured. Severity: minor.
- **ac-loss-03 check [2]** accepts generic "calibration is deferred" (loses the empirical/median-scaled
  specificity). Deferral is correctly stated. Severity: minor.

## Gaps

[none — no blocking issues; observations above are non-blocking and need no fix plan]

## Conclusion

Phase 36 execution is **verified PASS**. The acceptance-check closure gate is honest and reproducible:
the disposable-probe suite genuinely re-confirms the already-adjudicated v1.6 contracts; the BLOCKED→PASS
transition was achieved by correcting over-strict probe patterns, not by editing any spec; protected paths
were respected; the ledger is terminal; traceability holds; and the two anchor-extension gaps are
user-ratified. v1.6 milestone closure gate is satisfied.

Agent B (verifier) handoff: the phase is ready for the GSD phase-completion handler (STATE.md transition,
per repo rule D-36) — that transition is owned by the handler, not by this UAT.
