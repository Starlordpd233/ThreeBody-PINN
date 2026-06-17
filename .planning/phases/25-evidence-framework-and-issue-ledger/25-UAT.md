---
status: passed
phase: 25-evidence-framework-and-issue-ledger
source: 25-01-SUMMARY.md, 25-02-SUMMARY.md (tests derived from both plan summaries + ROADMAP Phase 25 success criteria 1-5 + GAP-25-01/GAP-25-02 resolutions)
started: 2026-06-12T21:26:00+08:00
updated: 2026-06-12T21:40:00+08:00
verification_mode: automated (all probes are grep/git assertions against committed artifacts, run 2026-06-12 ~21:30 +08:00; same mode as 24-UAT.md — docs-only phase, no runnable deliverable)
---

## Current Test

number: complete
name: All tests resolved — Phase 25 UAT passed
expected: |
  Two findings (one minor, one cosmetic) were remediated at UAT closure in commit
  9d2d86eb: the 25-02-SUMMARY "Plan 25-03+" wave framing was corrected to the
  GAP-25-01 Option A allocation (Phases 26-28 author remaining packets), and the
  literal <pending-commit-sha> audit labels in the three EVID-10 records were
  backfilled with e05b4b1a, mirroring the ledger backfill convention (7bcd1cdb).
result: 9/9 pass

## Tests

### 1. Evidence-packet template structure (`evidence/_TEMPLATE.md`)
expected: 12 `##` sections + `### Dataset Evidence (§3b)` sub-block; all five EVID-07 verdict enum values verbatim; issue-02 source paths; no `sampling_method.md` reference (SCOPE-08); `data_quality_assessment.md` present as citable-never-editable (SCOPE-09).
result: pass
evidence: h2count=12; §3b present; all 5 enum values present; issues/02-data-pipeline-and-validation path present; zero sampling_method hits; dqa present.

### 2. Protocol README content (`evidence/README.md`)
expected: EVID-10 trigger table carries exactly the three v1.5 conflicts (SCS, D=6.694, M11/M12); `### D-03 Downstream Enforcement` h3; GAP-25-02 status legend ("adjudicated-but-unfixed", "owns records, not fixes"); ID→filename map (scs-thresholds.md, compute-globals-D.md, m11-m12-severity.md); phase-exit scoped to Phases 26-28; no new AC-IDs minted (D-13).
result: pass
evidence: all content probes pass. AC-ID sweep found AC-ARCH-03/AC-FRAME-01/AC-PHYS-02-COMP-AD on line 111 — these are labeled "Examples:" (v1.4 precedent citations), not newly minted v1.5 IDs; D-13 satisfied.

### 3. Ledger Lifecycle Rules re-issue (D-11) in `24-ISSUE-LEDGER.md`
expected: Applicability token reads Phases 26-28 (Phase 29 acceptance); no stale "Phases 17-22"/"20.5" token; KEEP-VERBATIM strings preserved ("FIX_APPLIED is not closure", "A batch is one GSD plan", VERIFIED/DEFERRED phase-exit gate); Notes line records the D-11 re-issue.
result: pass
evidence: all 7 probes pass; stale-token greps return zero hits.

### 4. Three EVID-10 records exist and conform structurally
expected: scs-thresholds.md, compute-globals-D.md, m11-m12-severity.md each carry the 12 `##` sections + `### Dataset Evidence (§3b)`, including Status Transition Log entries with date + commit SHA + transition + actor.
result: pass
reported: "Automated finding (cosmetic): all three records retained the literal <pending-commit-sha> audit label in their Status Transition Log, plus an in-file sentence promising the final SHA 'replaces' the placeholder after the atomic commit — the 7bcd1cdb backfill covered only the ledger and summary."
resolution: "RESOLVED 2026-06-12 commit 9d2d86eb: e05b4b1a backfilled into all three record log entries; promise sentence updated to past tense recording the backfill date. Grounding: plan 25-02 governance note line 124 sanctioned the literal label, but the records' own text anticipated replacement and the ledger backfill (7bcd1cdb) established the convention."
severity: cosmetic (resolved)

### 5. Adjudication verdicts (ROADMAP criterion 4)
expected: SCS → accept-resolution; D=6.694 → accept-resolution with CLM-13 ratified convention-rejected (OI-11) and raw-mass D ≈ 4.6416; M12 → accept-third-position; M11 → explicit severity ruling BLOCKING STANDS on data-integrity grounds with OI-8 carried forward and all four D-10 GUARD triggers individually recorded as non-firing.
result: pass
evidence: all verdict strings present in the correct records; m11-m12-severity.md line 95 records GUARD triggers (a)-(d) each with its negative result; root-cause, which-source-right/wrong, and locked-convention sections present per criterion 4.

### 6. Ledger wiring (D-06 / D-12 / GAP-25-02 convention)
expected: SCS, D=6.694, M11, M12 Status-Table rows carry Evidence-Packet relative links + filled Verdict cells while Status stays PENDING (adjudicated-but-unfixed per GAP-25-02 Option A); per-finding notes carry verdict + fix-owning phase + status-transition entries with commit SHA e05b4b1a; G3 closes with M11 and G5 with M12 (close-with-parent annotations), with G3/G5 Evidence-Packet cells left as `—`.
result: pass
evidence: 4 rows wired with correct relative links and verdict cells, all at PENDING; e05b4b1a appears 4 times in ledger; G3/G5 rows confirmed `—` in Evidence-Packet column; 4 close-with-parent mentions present.

### 7. Zero framework-spec edits (D-02)
expected: No Phase 25 commit touches `pinn_instruction/` (ctl_instruction.md, pinn_architecture.md, sampling_method.md all untouched); spec-edit-ready prose lives only inside the EVID-10 records for Phases 26-28 to transcribe.
result: pass
evidence: `git diff --name-only 16f78284..HEAD` contains zero pinn_instruction/ paths (non-.planning changes are the unrelated docs-archive commit 4b75389d).

### 8. Commit hygiene + recovery tag (D-17)
expected: Wave-1 merge da5a8203 and Wave-2 commits e05b4b1a, 7bcd1cdb, 7e924836 are ancestors of milestone/v1.5 HEAD; all carry Agent-Assisted-By/Co-Authored-By trailers; recovery tag v1.5-pre-phase-25 resolves to 16f78284, never moved.
result: pass
evidence: all four ancestry checks pass; all three Wave-2 trailers present; tag resolves to 16f782847cb741aa987329665f704ae03f6dd178.

### 9. Execution-summary provenance accuracy
expected: 25-01/25-02 summaries accurately record what was delivered and where remaining work lives, consistent with GAP-25-01 Option A (Phases 26-28 author remaining packets), the plan's own governance note, and ROADMAP (Phase 25 = exactly 2 plans).
result: pass
reported: "Automated finding (minor, not user-reported): 25-02-SUMMARY.md claimed in three places that remaining findings' records land in 'future waves (Plan 25-03+)' / are 'future-wave' (lines 123, 141, 143). This contradicts GAP-25-01 Option A resolution (25-GAPS.md), 25-02-PLAN.md line 110 ('The phase has exactly TWO plans (25-01, 25-02). There is no Plan 25-03.'), and ROADMAP. Risk: a Phase 26-28 planner reading the summary could wait for a nonexistent Plan 25-03 instead of authoring packets before its spec edits (EVID-06)."
resolution: "RESOLVED 2026-06-12 commit 9d2d86eb: all three spots corrected to the grounded allocation — remaining evidence packets/verdicts are authored by the owning phase (26-28) immediately before its spec edits per GAP-25-01 Option A (split reading). No deliverable content changed; ROADMAP/STATE/ledger/README were already correct (the drift was confined to the summary)."
severity: minor (resolved)

## Summary

total: 9
passed: 9
issues: 2 (both resolved at UAT closure, commit 9d2d86eb)
pending: 0
skipped: 0
blocked: 0

## Gaps

- truth: "Execution summaries record the GAP-25-01 Option A allocation of remaining adjudication work (owning phases 26-28), not a nonexistent Plan 25-03+"
  status: resolved
  reason: "Automated probe: 25-02-SUMMARY.md lines 123/141/143 claimed 'future waves (Plan 25-03+)' cover the remaining 15 findings"
  severity: minor
  test: 9
  root_cause: "Executor-authored summary prose drifted from its own plan: 25-02-PLAN.md line 110 explicitly states there is no Plan 25-03, and GAP-25-01 Option A (resolved 2026-06-12) allocates remaining packets to Phases 26-28. The 'future waves' framing was invented at summary-writing time, not copied from any grounded source."
  artifacts:
    - path: ".planning/phases/25-evidence-framework-and-issue-ledger/25-02-SUMMARY.md"
      issue: "three stale 'Plan 25-03+/future-wave' claims (Decisions Made D-08 bullet; Phase 26 and Phase 28 readiness bullets)"
  missing: []
  debug_session: ""
  resolution: "Fixed in commit 9d2d86eb (2026-06-12); verified by re-grep — zero '25-03+/future wave' hits remain outside the plan's own governance note."

- truth: "EVID-10 record Status Transition Log entries carry the real commit short SHA per the template's entry contract"
  status: resolved
  reason: "Automated probe: literal <pending-commit-sha> retained in all three records while ledger/summary were backfilled with e05b4b1a"
  severity: cosmetic
  test: 4
  root_cause: "The 7bcd1cdb backfill scope covered 24-ISSUE-LEDGER.md and 25-02-SUMMARY.md only; the records' own logs (and their 'final SHA replaces the placeholder' sentences) were left at the placeholder. Plan 25-02 line 124 sanctioned the literal label, so this is convention-consistency, not a contract breach."
  artifacts:
    - path: ".planning/phases/25-evidence-framework-and-issue-ledger/evidence/"
      issue: "<pending-commit-sha> placeholder in scs-thresholds.md:108, compute-globals-D.md:134, m11-m12-severity.md:144"
  missing: []
  debug_session: ""
  resolution: "Fixed in commit 9d2d86eb (2026-06-12): e05b4b1a backfilled into all three log entries; promise sentences updated to past tense with backfill date."
