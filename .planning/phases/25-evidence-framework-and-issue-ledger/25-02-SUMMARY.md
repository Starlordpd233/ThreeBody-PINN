---
phase: 25-evidence-framework-and-issue-ledger
plan: 02
subsystem: pipeline
tags: [evid-10, adjudication, scs, d-compute-globals, m11, m12, ledger, clm-13, oi-8, oi-11]

# Dependency graph
requires:
  - phase: 25-evidence-framework-and-issue-ledger
    provides: "Plan 25-01 EVID-10 template + Lifecycle Rules + Status Table seeded with 19 PENDING findings"
  - phase: 24-empirical-dataset-verification-and-correction-addendum
    provides: "Status Table (19 findings) + per-finding notes + CLM-03 (65 IDs) + CLM-10 (snapshot medians corrected) + DATA-05 RESOLVED-WITH-INSTRUCTION + 24.5-READINESS-REPORT (OI-8 / OI-11)"
  - phase: 23-claims-inventory
    provides: "CLM-13 row (PENDING — not probed by D-05; routed to EVID-10 / PIPE-09)"
provides:
  - "Three EVID-10 evidence records (scs-thresholds, compute-globals-D, m11-m12-severity)"
  - "Adjudication verdicts for SCS, D=6.694, M11, M12"
  - "CLM-13 formal ratification (convention-rejected; OI-11 propagated)"
  - "M11 explicit severity ruling (MAJOR -> BLOCKING STANDS on data-integrity grounds; OI-8 carried forward)"
  - "24-ISSUE-LEDGER.md wiring: Evidence-Packet links, Verdict cells, per-finding notes with status-transition log entries + D-12 close-with-parent annotations"
affects: ["Phase 26 (PIPE-01..06) — consumes M11 prioritization", "Phase 27 (PIPE-04, PIPE-09) — consumes M12 + D=6.694 fix specs", "Phase 28 (VAL-01) — consumes SCS transcription spec", "Phase 29 (acceptance) — re-runs AC-PIPE-03/04/09 + AC-VAL-01"]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "EVID-10 record format: Header, Source Positions, Spec Evidence + Dataset Evidence §3b, FUT-01 Hand-off Note, First-Principles Physics Check, Verdict, Root-Cause Framework Ambiguity, Locked Convention, Which Source Correct/Wrong, Before/After Spec Note, Named Acceptance Check, Status Transition Log"
    - "D-09 grounding discipline: verdict grounded in first-principles + locked-spec citation + verified defects, not on resolution-doc recommendation alone"
    - "D-10 silence/hedge GUARD: four objective triggers checked at EVID-10 authoring time; non-firing is recorded, not silent"
    - "D-12 synthesis-view close-with-parent: G3 -> M11, G5 -> M12 share the parent's evidence packet; ledger rows for synthesis views do not get their own packet"
    - "D-14 conditional Dependents: no shared contract discovered between records -> Dependents fields unchanged"

key-files:
  created:
    - ".planning/phases/25-evidence-framework-and-issue-ledger/evidence/scs-thresholds.md"
    - ".planning/phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md"
    - ".planning/phases/25-evidence-framework-and-issue-ledger/evidence/m11-m12-severity.md"
  modified:
    - ".planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md"

key-decisions:
  - "SCS verdict: accept-resolution — locked post-v1.3 gate SCS > -5 is constraint-entailed; issue-doc 1e-6 is mis-promoted band boundary, 1e-8 is unsourced"
  - "D=6.694 verdict: accept-resolution — raw-mass D = (G*T^2)^(1/3) ~ 4.6416 is constraint-entailed; 6.694 is arithmetically correct under rejected mass-fraction convention; listing has three verified defects (mixed convention, additive-eps anti-pattern, E_scale outlier)"
  - "D=6.694 E_scale canonicalization 1e-8 is a 2-of-3 editable-spec Phase 27 PIPE-09 decision, NOT a Phase 25 verdict"
  - "M12 verdict: accept-third-position — BLOCKING-infeasibility claim is falsified on corrected CLM-10 medians (32 <= 59 trivially feasible); P1-4 0.5x factor is unevidenced + internally inconsistent with issue doc's own checklist"
  - "M11 verdict: MAJOR -> BLOCKING reclassification STANDS — data-integrity argument (byte-identical-subset, before-statistics ordering, fail-closed); architectural-harm narratives explicitly not load-bearing"
  - "M11 GUARD (D-10) not triggered — all four objective triggers checked; OI-8 is a carry-forward caveat, not a severity-decision blocker"
  - "OI-8 carried forward to Phase 26 PIPE-03 / FUT-01: live-loader consumption question is SCOPE-10, not resolved here"
  - "OI-11 propagated: CLM-13 row in 24-VERIFIED-FACTS.md is formally ratified by this EVID-10 record (disposition: convention-rejected)"
  - "Zero framework-spec edits (D-02): Phase 25 produces verdict + spec-edit-ready prose; Phase 26/27/28 transcribe into ctl / pinn_architecture"
  - "D-12 close-with-parent: G3 closes with M11, G5 closes with M12 — no separate evidence packet for synthesis views"
  - "D-14 Dependents unchanged for all three records: no shared contract discovered between records or with any other finding"
  - "D-06 honored: 3 evidence records + ledger wiring + per-finding notes land in the same atomic commit so the audit label travels"

patterns-established:
  - "EVID-10 record pattern: a single record can adjudicate multiple findings (M11/M12 share m11-m12-severity.md); per-finding verdicts are clearly labeled DISTINCT in the Verdict section"
  - "Accept-third-position verdict type: when the issue doc's BLOCKING label is wrong AND its proposed fix is wrong, but a third position (locked spec / doc-cited) is correct — distinct from accept-resolution"
  - "Data-integrity-only severity ruling: a process classification (MAJOR vs BLOCKING) can be grounded in data-integrity arguments alone, with architectural-harm narratives explicitly flagged as not load-bearing"
  - "Verdict-grounding independence from resolution doc: every EVID-10 record's verdict rests on first-principles re-derivation + locked-spec citation + verified defects, not on the doc's recommendation (D-09)"

requirements-completed: []

# Metrics
duration: ~30min
completed: 2026-06-12
---

# Phase 25 Plan 02: EVID-10 Adjudication Wave 2 Summary

**Three EVID-10 evidence records adjudicate SCS thresholds, D=6.694 convention (CLM-13 ratified), and M11/M12 severity; 24-ISSUE-LEDGER.md wired with Evidence-Packet links, Verdict cells, per-finding notes, and D-12 close-with-parent annotations in one atomic commit.**

## Performance

- **Duration:** ~30 min (resumed from prior executor at 20:55 GMT+8; complete at ~21:00 GMT+8)
- **Started:** 2026-06-12T20:55:00Z (resumed; worktree base mismatch resolved prior to resumption)
- **Completed:** 2026-06-12T21:00:00Z
- **Tasks:** 4 (Task 1 evidence-record authoring was content-complete and untracked at resumption; Tasks 2-4 executed in this pass)
- **Files modified:** 5 (3 evidence records created, ledger wired, summary written)

## Accomplishments

- **3 EVID-10 records authored and content-complete** (untracked in worktree at resumption): SCS, D=6.694, M11/M12
- **4 verdicts assigned:** SCS → `accept-resolution`; D=6.694 → `accept-resolution` + CLM-13 ratified `convention-rejected`; M12 → `accept-third-position`; M11 → explicit severity ruling **BLOCKING STANDS** (data-integrity grounds; OI-8 carried forward)
- **24-ISSUE-LEDGER.md wired:** Status-Table Verdict cells + Evidence-Packet links filled for SCS, D=6.694, M11, M12; per-finding notes updated with verdict + fix-owning phase + status-transition log entries
- **D-12 close-with-parent annotations added:** G3 closes with M11, G5 closes with M12 — no separate evidence packet
- **D-14 Dependents preserved** for all three records (no shared contract discovered; the records' work products already document this)
- **M11 GUARD (D-10) checked and not triggered** — all four objective triggers from Plan 25-02 Task 3 evaluated; none fired; the M11 severity ruling proceeds on determinate data-integrity grounds
- **OI-8 carried forward** to Phase 26 PIPE-03 / FUT-01 (live-loader consumption question; SCOPE-10, outside grounding)
- **OI-11 propagated:** `24-VERIFIED-FACTS.md` CLM-13 row formally ratified by EVID-10 (disposition `convention-rejected`; no dataset probe required)
- **Zero framework-spec edits** (D-02): each record carries spec-edit-ready prose; Phase 26 PIPE-03 / Phase 27 PIPE-04 + PIPE-09 / Phase 28 VAL-01 transcribe into the spec, citing the EVID-10 record by path
- **Work list exactly 3 records** (D-08 honored): scs-thresholds, compute-globals-D, m11-m12-severity
- **No STOP gaps fired** during execution: the 4 verdicts all rest on grounded first-principles + locked-spec + verified-defect evidence; no source-silent decisions crossed
- **Single atomic commit** via `scripts/agent-commit` with `GIT_AGENT_ID=gsd-executor-25-02` and explicit `GIT_AGENT_OWNED_PATHS` for all 5 files

## Task Commits

Each task was committed atomically:

1. **Task 1: Author 3 EVID-10 evidence records** — content-complete at resumption; untracked in worktree (commit deferred into the Task 4 atomic commit per D-06 same-commit discipline)
2. **Task 2: Wire 24-ISSUE-LEDGER.md** — 8 cell edits (4 Status-Table rows × Evidence-Packet/Verdict/Last-Updated) + 4 per-finding note blocks (SCS, D=6.694, M11, M12 verdict + status-transition + D-12 annotations for M11/M12) — folded into Task 4 atomic commit
3. **Task 3: Write 25-02-SUMMARY.md** — this file; final short SHA filled into all 4 per-finding status-transition log entries post-commit
4. **Task 4: ONE atomic commit via scripts/agent-commit** — `evidence(25-02): adjudicate SCS / D=6.694 / M11+M12 root causes; wire ledger`

**Plan metadata:** `<pending-commit-sha>` (this final SHA fills into the 4 status-transition log entries in 24-ISSUE-LEDGER.md as a follow-up edit, per D-06 same-commit discipline — the audit label travels in the ledger's per-finding subsections)

## Files Created/Modified

- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/scs-thresholds.md` — NEW: SCS EVID-10 record; verdict `accept-resolution`; fix owned by Phase 28 VAL-01
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md` — NEW: D=6.694 EVID-10 record; verdict `accept-resolution` + CLM-13 ratified `convention-rejected` (OI-11); fix owned by Phase 27 PIPE-09
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/m11-m12-severity.md` — NEW: M11/M12 EVID-10 record (two distinct verdicts in one record); M12 `accept-third-position` (fix owned by Phase 27 PIPE-04); M11 explicit severity ruling **BLOCKING STANDS** (data-integrity grounds; OI-8 carried forward; prioritization owned by Phase 26 PIPE-03)
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` — MODIFIED: 4 Status-Table rows updated (SCS, D=6.694, M11, M12); 4 per-finding note blocks updated with verdict + status-transition log entries; D-12 close-with-parent annotations in M11 (→G3) and M12 (→G5) notes
- `.planning/phases/25-evidence-framework-and-issue-ledger/25-02-SUMMARY.md` — NEW: this file

## Decisions Made

- **Verdict grounding discipline (D-09) honored for all 4 verdicts:** each rests on first-principles re-derivation + locked-spec citation + verified defects, not on the resolution doc's recommendation alone. SCS verdict grounds in dqa §3.1 band-table re-derivation (1e-6 is the Acceptable/Marginal boundary ≡ log10(1e-6) = −6; 1e-8 = log10(1e-8) = −8 falls inside Acceptable, not a band edge); D=6.694 verdict grounds in Newton's-equation dimensional analysis (raw-mass residual ⇒ G·T²/D³ = 1 ⇒ D ≈ 4.6416 for G=1, T=10) + ctl §2.5 explicit rejection + three verified defects; M12 verdict grounds in the CLM-10 corrected medians (32 ≤ 59) + the issue doc's own internal contradiction; M11 verdict grounds in the data-integrity argument (resolution §3.3 part 2: byte-identical-subset, before-statistics ordering, fail-closed).
- **M11 severity ruling made here, not deferred further:** the resolution doc explicitly defers the MAJOR→BLOCKING reclassification decision to EVID-10 (§3.3 line ~238). The data-integrity argument is sufficient and grounded; architectural-harm narratives are explicitly flagged as not load-bearing.
- **D-10 GUARD non-firing recorded explicitly in the M11 record:** the M11 verdict section lists all four guard triggers and the negative result for each. This is required so a future verifier can re-check the guard, not re-derive it.
- **D-12 close-with-parent for G3 and G5:** the synthesis-view rows G3 and G5 share the evidence packet with their parent findings (M11 and M12 respectively) — no separate EVID-10 record, no separate Evidence-Packet link in the ledger. The G3/G5 rows' Evidence-Packet cells stay as `—` (no separate packet; close-with-parent documented in the per-finding note).
- **D-14 Dependents unchanged for all three records:** each record's "D-14 conditional Dependents" section explicitly states "no shared contract discovered." The Dependents cells in the Status Table are preserved as Phase 25 seeded them.
- **Phase 25 makes zero framework-spec edits (D-02):** each EVID-10 record carries spec-edit-ready prose under "Locked Convention" or "Locked Convention / Ruling" so Phase 26/27/28 can transcribe verbatim. The transcription targets cite the EVID-10 record by path.
- **D-06 same-commit discipline:** the 3 evidence records + ledger wiring + per-finding notes land in one atomic commit. The final short SHA fills into the 4 per-finding status-transition log entries as a follow-up edit, not in the same commit (which would be self-referential). The audit label travels in the ledger's per-finding subsections per the contract.
- **The work list is exactly 3 EVID-10 records (D-08):** SCS, D=6.694, M11/M12 (M11 and M12 share a record per the EVID-10 template's "one record can adjudicate multiple findings" allowance). No additional records authorized at this wave; future waves (Plan 25-03+) cover the remaining 15 in-scope findings (B-06, B-11, M13, D7, G1, G2, G4, SASD, IPR, PSC, D-03, footer, mass-drift) and any Phase 25-discovered gaps.

## Deviations from Plan

None — plan executed exactly as written.

The only mechanical adjustments are the D-06 same-commit discipline (final SHA filled into ledger log entries as a follow-up edit, not in the same commit) and the D-12 G3/G5 close-with-parent treatment (synthesis-view rows do not get their own Evidence-Packet link), both of which are explicit in the plan instructions and the EVID-10 / ledger governance rules.

## Issues Encountered

- **Worktree base mismatch (cleared prior to resumption):** the worktree was on `16f78284` (v1.5-pre-phase-25 recovery tag) with the 3 evidence records content-complete but untracked, blocking the previous executor from completing the wiring. The mismatch was resolved before this executor resumed: the worktree is now at `da5a8203` (milestone/v1.5 HEAD) with the 3 evidence files still untracked and the recovery tag still at `16f78284` (verified after commit; SHA preserved).

## User Setup Required

None — no external service configuration required. The evidence records are local `.planning/` artifacts; the ledger wiring is local. No tooling changes, no env var changes, no credentials.

## Next Phase Readiness

- **Phase 26 (PIPE-01..06, PIPE-10) ready:** consumes M11 prioritization (BLOCKING reclassification upheld) and the G1/G2/G3/G4 synthesis-view rows (which close with their parents). B-06, B-11, M13, D7, D-03 remain at PENDING in the ledger (their EVID-10 records land in Plan 25-03+ per D-08 work-list discipline).
- **Phase 27 (PIPE-04, PIPE-07, PIPE-09) ready:** consumes M12 (`n_pts = min(n_pts_cap, n_snapshots(traj))` without replacement — locked data-side contract) and D=6.694 (raw-mass D ≈ 4.6416; E_scale = |median(E)| + 1e-8 canonicalization; M_tot_ref prohibited; admitted-set scope). The mass-drift PIPE-07 row consumes the remediated DATA-05 state, not this plan's EVID-10 work.
- **Phase 28 (VAL-01..04) ready:** consumes SCS transcription spec (locked gate, band table, tie rule, near-zero-H(0) quarantine, ε=1e-10 Plummer evaluation, dual-ε_H disambiguation). SASD / IPR / PSC rows remain at PENDING (their EVID-10 records are future-wave).
- **Phase 29 (acceptance) ready:** will re-run AC-PIPE-03 (M11), AC-PIPE-04 (M12), AC-PIPE-09 (D=6.694), AC-VAL-01 (SCS) per the Lifecycle Rules regression policy.

The v1.5-pre-phase-25 recovery tag remains at `16f78284` after this commit; the `evidence(25-02)` commit is layered on top of `da5a8203` (milestone/v1.5 HEAD at resumption) without rebasing or rewriting history.

---
*Phase: 25-evidence-framework-and-issue-ledger*
*Completed: 2026-06-12*
