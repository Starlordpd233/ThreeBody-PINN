# Phase 36: Acceptance Checks, Re-verification & Handoff - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-06-30
**Phase:** 36-acceptance-checks-re-verification-handoff
**Mode:** `$gsd-discuss-phase 36 --auto --all`
**Areas discussed:** Closure Packet Topology, Probe Execution Strategy, Ledger and SI Closure, Handoff and Trainex Routing, Git and Workflow Hygiene

---

## Closure Packet Topology

| Option | Description | Selected |
|--------|-------------|----------|
| Closure packet | Use `36-ACCEPTANCE-MANIFEST.md`, `36-PROBE-RESULTS.md`, `36-VERIFICATION.md`, and `36-HANDOFF.md`; keep SI reconciliation inside handoff. | yes |
| Separate SI report | Add a dedicated `36-SI-RECONCILIATION.md` alongside the closure packet. | |
| Single handoff | Put manifest, probes, verification, SI, and FUT routing into one `36-HANDOFF.md`. | |

**User's choice:** Auto-selected recommended default.
**Notes:** Matches the SPEC interview default and keeps downstream planning centered on one closure packet without adding an extra SI artifact.

---

## Probe Execution Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Fresh closure probes | Run fresh disposable Phase 36 checks from a manifest, citing prior phase verification as provenance. | yes |
| Replay all prior checks | Re-run every historical Phase 33-35 verification command plus new checks. | |
| Artifact audit only | Check artifact presence and ledger state, adding numerical probes only for gaps. | |

**User's choice:** Auto-selected recommended default.
**Notes:** Fresh closure probes satisfy `VER-15` while avoiding uncontrolled replay scope. Prior verification remains canonical provenance.

---

## Ledger and SI Closure

| Option | Description | Selected |
|--------|-------------|----------|
| Fail-closed terminal gate | Require all in-scope ledger rows to be `VERIFIED` or explicitly `DEFERRED`; nonterminal rows block closure. | yes |
| Document pending rows | Allow pending rows if the handoff explains why they are not blockers. | |
| Phase36-dependent rows only | Apply terminal-state gate only to rows listing Phase 36 as a dependent. | |

**User's choice:** Auto-selected recommended default.
**Notes:** Current ledger scan found 18 rows: 16 `VERIFIED`, 2 `PENDING` (`D-05`, `D-06`). Phase 36 must surface those rows as closure blockers unless they become terminal.

---

## Handoff and Trainex Routing

| Option | Description | Selected |
|--------|-------------|----------|
| Reference trainex todo as handoff input | Fold `trainex-r1-research-handoff.md` only into FUT/trainex routing; do not execute it. | yes |
| Execute trainex handoff | Treat the todo as active Phase 36 work and perform the external research handoff. | |
| Ignore trainex todo | Leave the todo entirely outside Phase 36. | |

**User's choice:** Auto-selected recommended default.
**Notes:** The todo matched Phase 36 by handoff/FUT keywords. Folding it as a routing input preserves the signal without scope creep.

---

## Git and Workflow Hygiene

| Option | Description | Selected |
|--------|-------------|----------|
| Strict owned-path commits | Use `scripts/agent-commit`, explicit staging, and exclude unrelated Phase 35/`AGENTS.md` dirty files. | yes |
| Defer commits | Write artifacts but leave them uncommitted for a later cleanup. | |
| Broad phase cleanup | Include adjacent dirty planning artifacts in this commit. | |

**User's choice:** Auto-selected recommended default.
**Notes:** Project governance requires atomic commits for `.planning/` work. Existing Phase 35 and `AGENTS.md` changes are user-owned and must stay out of Phase 36 commits.

---

## the agent's Discretion

- The planner may choose the exact plan count and probe script names.
- The planner may decide whether the manifest is generated or hand-authored, provided all SPEC acceptance criteria remain mechanically verifiable.
- Auto-mode's normal plan-phase dispatch is suppressed because the user explicitly said to stop before planning starts.

## Deferred Ideas

- Execute trainex-r1 external research handoff in the trainex/FUT track, not in Phase 36.
- Implement training-loop/DataLoader/ALM logic in FUT-01/FUT-04, not in Phase 36.

---

## Refresh — 2026-06-30 (`--all --auto --analyze`, post-SPEC re-grounding)

Re-grounded CONTEXT against the post-Phase-35 codebase after the SPEC re-grounding (commit `0ded50d`). No locked SPEC requirement changed; this pass corrected stale current-state facts and captured two newly-grounded decisions. Trade-off rationale (per `--analyze`):

| Decision | Options considered | Selected | Rationale |
|----------|--------------------|----------|-----------|
| SI universe (D-36-09) | (a) keep 3 IDs; (b) correct to 4 IDs incl. `SI-DQA-003` | (b) | A fresh grep returns four IDs; VER-18 forbids assuming any SI hit irrelevant. Empirical + grounded; (a) would leave the mechanical acceptance check under-scoped. |
| `D-05`/`D-06` closure (D-36-07) | (a) only gate/report `BLOCKED`; (b) verify-and-promote-if-clean, else `BLOCKED` | (b) | Verdicts are already `RESOLVED-WITH-INSTRUCTION`; promotion is mechanical verification of downstream transcription, not re-litigation. Fail-closed on missing/divergent transcription. SPEC permits ledger update "if a plan permits." |
| ROADMAP/REQUIREMENTS reconciliation (D-36-17) | (a) audit-only; (b) reconcile stale status flags in scope | (b), flagged | `34-VERIFICATION.md:102` explicitly defers ROADMAP reconciliation to Phase 36; `LOOP-04/07/08` and the ROADMAP progress table are stale. Edits are mechanical but NOT in the SPEC in-scope list → flagged for user confirmation before owning those paths; must be done manually (state/roadmap tool mutators broken here). |
| `SI-DQA-003` disposition (D-36-18) | (a) decide preserve now; (b) defer to execution under STOP | (b) | Issue-03-relevance is a STOP-protocol judgment; pre-deciding would risk inventing a source-silent disposition. Non-binding lean recorded as preserve-with-reason. |

**Suppression:** Auto-advance to plan-phase remains intentionally suppressed per the standing user instruction (D-36-16).
