---
status: complete
phase: 28-validation-metrics-contracts
source: [28-01-SUMMARY.md, 28-02-SUMMARY.md, 28-03-SUMMARY.md, 28-04-SUMMARY.md]
started: 2026-06-16T04:30:00Z
updated: 2026-06-16T04:40:00Z
verification_mode: spec-phase-claim-audit
phase_closeable: false
phase_blocked_by: [GAP-28-01, GAP-28-02, GAP-28-03]
---

## Current Test

[testing complete]

> **Verification note.** Phase 28 is a v1.5 spec-adjudication phase, not interactive
> software — there is no runnable UI to click through. UAT here is an independent
> *claim audit*: each SUMMARY assertion was re-derived against the live repository
> (re-ran AC-VAL-01, re-hashed the PIPE-09 region, inspected every park commit's file
> list, checked ledger/gap/counter consistency, and spot-checked grounding in the
> candidate resolution doc). Checks were performed by the verifier, not the user.
>
> **The phase is NOT eligible for completion-transition.** Three STOP-protocol gaps
> (GAP-28-01/02/03) are OPEN and require user sign-off. Auto-transition to "complete"
> was deliberately suppressed — see Summary.

## Tests

### 1. SCS canonical contract landed and correct (VAL-01 / AC-VAL-01)
expected: ctl_instruction.md Step-1A carries the single canonical SCS gate — `eps_H = max_t |(H(t)-H(0))/H(0)|`, `SCS = log10(eps_H)`, REJECT if `SCS > -5`; band table + tie rule; near-zero `|H(0)|` quarantine + Plummer `eps=1e-10`; issue-02 ratio thresholds `1e-6`/`1e-8` rejected by name (not canonical); scs-thresholds.md cited; raw/scaled invariance + dual-`eps_H` symbol hygiene present.
result: pass
evidence: AC-VAL-01 re-run against current ctl_instruction.md — all six assertions PASS (formula, band_table_and_tie, quarantine_and_plummer, ratio_thresholds_rejected, scs_packet_citation, invariance_and_symbol_hygiene). Issue-ledger SCS row = VERIFIED, `accept-resolution`, AC-VAL-01 PASS (2026-06-16). Commit bd31dcd8 modified ctl_instruction.md (+24 lines). Grounding = transcription of the Phase 25 locked verdict (D-03), not re-adjudication.

### 2. PIPE-09 global-scale contract non-regression
expected: The Phase 27 PIPE-09 `compute_globals` region (which feeds the SCS definition) is byte-identical after the SCS edit — SHA-256 `816589102aea99f2878991bda9cee351db08e8d2cd5c64fbe725c551a825b986`.
result: pass
evidence: Re-extracted the region from the live ctl_instruction.md; SHA-256 matches the baseline byte-for-byte. No regression to the locked PIPE-09 raw-mass D convention.

### 3. No spec clauses silently landed for the parked metrics (STOP-protocol integrity)
expected: Because SASD/IPR/PSC each parked at their fork (Task 1 STOP, Task 2 not run), NO clause text was written into ctl_instruction.md or pinn_architecture.md, and the shared `Data-side quality-metric contracts` subsection heading was never created.
result: pass
evidence: Negative proof via commit file-lists — park commits 2f7681d3 (SASD), aea67477 (IPR), f7c68e65 (PSC) each touch ZERO framework-spec files. The `### ... Data-side quality-metric contracts` heading is absent from ctl_instruction.md (only a prose forward-pointer naming the future subsection exists, added by SCS — correct). This is the strongest available evidence the STOP protocol held: nothing was invented.

### 4. SASD/IPR/PSC evidence packets authored (defer-with-blocker)
expected: One EVID-06 packet per deferred metric under 25-.../evidence/, each carrying a `defer-with-blocker` verdict and registered in the evidence README ID->filename map.
result: pass
evidence: sasd-sampling-density.md, ipr-physics-residual.md, psc-coverage-entropy.md all exist with `Current Verdict | defer-with-blocker`. evidence/README.md carries all three map rows (SASD/IPR/PSC -> filenames).

### 5. STOP gaps fully recorded (GAP-28-01/02/03)
expected: 28-GAPS.md records each fork as a semantic STOP gap with all required fields (decision point, where-in-artifact, task context, classification, source-silence citations, math/engineering grounding, agent-tempted-to, user-decision options, confidence, status OPEN, resolution note).
result: pass
evidence: 28-GAPS.md contains GAP-28-01 (SASD endpoint), GAP-28-02 (IPR raw-vs-scaled units, ~464x), GAP-28-03 (PSC population/weighting). Each carries the full STOP field set with file:line source citations and a correct dimensional-analysis grounding. All three Status = OPEN; resolution notes empty (awaiting user).

### 6. Milestone-wide gap index and counters consistent
expected: GAP-28-01/02/03 mirrored into v1.5-GAPS.md with frontmatter counters incremented in the same edit.
result: pass
evidence: v1.5-GAPS.md frontmatter — total_gaps: 9, open_gaps: 3, resolved_gaps: 6, deferred_gaps: 0, last_updated: 2026-06-16. All three Phase 28 gap rows present with option text matching 28-GAPS.md.

### 7. Issue-ledger VAL rows at terminal lifecycle states
expected: SCS = VERIFIED; SASD/IPR/PSC = DEFERRED, each with packet link, owning gap ID, and a same-commit transition-log entry.
result: pass
evidence: 24-ISSUE-LEDGER.md — SCS VERIFIED (AC-VAL-01 PASS); SASD/IPR/PSC each DEFERRED with `defer-with-blocker (GAP-28-0X ...)`, packet links, "no spec edit landed", and dated transition rows citing the correct commit SHAs (2f7681d/aea6747/f7c68e6).

### 8. Parking decisions are grounded (not work-avoidance)
expected: Each parked fork is one the candidate resolution doc itself flags for project sign-off — so STOP (not transcribe-the-candidate) is the correct, grounded action.
result: pass
evidence: Spot-checked 02-resolution-doc.md at the cited lines. Q-C2: "Endpoints — genuine fork; ... CR-A's literal reading is the preserved dissent ... the project should weigh directly since it decides the fork." Q-C3: "Units — genuine fork, the consequential one ... differ by ×≈464 ... Preserved as the dissent." Q-C4: "a consolidator synthesis ... flagged as such ... the project should sanity-check the composed weighting on the first run." Parking matches the SPEC/CONTEXT pre-execution framing (D-04) and v1.5 governance.

### 9. Phase-state honesty (STATE.md, REQUIREMENTS.md)
expected: Authoritative state files report Phase 28 as executed-but-blocked, not complete.
result: pass
evidence: STATE.md — `status: executed, blocked on user decisions`; `stopped_at: ... VAL-01/SCS VERIFIED; VAL-02/SASD, VAL-03/IPR, VAL-04/PSC DEFERRED behind GAP-28-01/02/03`; "Phase 28 is not closed until user decisions resolve or explicitly defer those gaps." REQUIREMENTS.md — VAL-01 [x] verified; VAL-02/03/04 [ ] each "Deferred pending GAP-28-0X"; status table rows match.

### 10. ROADMAP status-table accuracy
expected: The ROADMAP phase-status summary table reflects Phase 28 as executed/blocked, consistent with STATE.md and REQUIREMENTS.md.
result: issue
reported: "ROADMAP.md status-summary table (line ~309) still reads `| 28. Validation-Metrics Contracts | v1.5 | 0/TBD | Not started (gated on Phase 24.5) | - |`. This is stale: Phase 24.5 completed 2026-06-11 and Phase 28 has been executed (SCS verified; 3 metrics deferred). It contradicts STATE.md (`executed, blocked`) and REQUIREMENTS.md. The `e8c4399b docs(28): record phase execution blockers` commit updated ROADMAP.md but missed this row."
severity: minor

### 11. Commit provenance and blocker recording
expected: Claimed commit SHAs exist and touch the claimed files; agent-assisted trailers present; a phase-level commit records the non-closure.
result: pass
evidence: bd31dcd8 / 2f7681d3 / aea67477 / f7c68e65 all resolve to the claimed park/spec commits, with `verify(28-0X): backfill commit sha` follow-ups. e8c4399b `docs(28): record phase execution blockers` body: "VAL-01 is verified, while VAL-02 through VAL-04 remain deferred behind GAP-28-01/02/03. Phase 28 is explicitly not marked closed." Agent-Assisted-By trailers present.

## Summary

total: 11
passed: 10
issues: 1
pending: 0
skipped: 0
blocked: 0

**Verdict:** Phase 28 executed correctly and to a high standard of governance integrity.
The one landed contract (SCS / VAL-01) is correct, grounded, and regression-clean; the
three deferred contracts (SASD/IPR/PSC) were parked exactly as the v1.5 STOP protocol
requires — evidence packets authored, forks surfaced as fully-specified gaps, and **no
spec text invented** (proven by the park commits touching zero framework-spec files).
Bookkeeping (ledger, gap register, milestone index, counters, state files) is internally
consistent and honest.

**One minor defect:** ROADMAP.md's status-summary table row for Phase 28 is stale
("Not started"). This is a documentation-consistency issue, not a spec-deliverable or
grounding defect — root cause is known (missed row in the e8c4399b ROADMAP update), so
no diagnosis pass is required. Fix = one-line table edit.

**Completion-transition deliberately NOT performed.** Unlike a normal passing UAT, this
phase must not be auto-marked complete: GAP-28-01/02/03 are OPEN and the phase-exit gate
(CONTEXT D-13) blocks closure while any in-scope VAL gap is OPEN. The genuine next step is
USER adjudication of the three forks, not a `/gsd-execute-phase --gaps-only` fix loop.

## Gaps

<!-- The three OPEN items below are STOP-protocol forks requiring USER sign-off, not code
     defects. They are owned by 28-GAPS.md / v1.5-GAPS.md; listed here for traceability
     only. They are NOT inputs to /gsd-plan-phase --gaps. -->

- truth: "ROADMAP status-summary table reflects Phase 28's executed/blocked state"
  status: failed
  reason: "Verifier found: ROADMAP.md line ~309 still shows Phase 28 as '0/TBD | Not started (gated on Phase 24.5)', contradicting STATE.md and REQUIREMENTS.md"
  severity: minor
  test: 10
  root_cause: "e8c4399b docs(28) updated ROADMAP.md but did not refresh the phase-status summary-table row for Phase 28"
  artifacts:
    - path: ".planning/ROADMAP.md"
      issue: "stale status-table row (~line 309): plan count 0/TBD and status 'Not started (gated on Phase 24.5)'"
  missing:
    - "Update the Phase 28 status-table row to reflect executed-but-blocked (e.g. plans 1/4 landed + 3 deferred; status 'Executed — blocked on GAP-28-01/02/03'; dated 2026-06-16), consistent with Phase 27's row format and STATE.md"
  debug_session: ""

## Phase Blockers (USER decisions required — not UAT code gaps)

- GAP-28-01 — SASD endpoint convention: both-endpoint max vs DQA-literal left endpoint (or defer). Options A/B/C in 28-GAPS.md.
- GAP-28-02 — IPR raw-vs-scaled unit pin for `IPR > 1e-3` (~464x impact) (or defer). Options A/B/C in 28-GAPS.md.
- GAP-28-03 — PSC pooled population/weighting composition: adopt dedup+equal-record now, partial, or defer. Options A/B/C/D in 28-GAPS.md.

Phase 28 closes only after each is RESOLVED-WITH-INSTRUCTION or explicitly user-DEFERRED
(then resume 28-02/03/04 to land the SASD/IPR/PSC clauses + AC-VAL-02/03/04), and Phase 29
owns milestone-wide acceptance/handoff.
