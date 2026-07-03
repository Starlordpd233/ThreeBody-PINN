# Phase 32: Evidence Framework, Issue Ledger & Conflict Adjudication - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-06-21
**Phase:** 32-evidence-framework-issue-ledger-conflict-adjudication
**Areas discussed:** Artifact topology, headline conflicts, ledger and verification, planning boundary

---

## Artifact Topology

| Option | Description | Selected |
|--------|-------------|----------|
| v1.5-style phase-local machinery | Adapt Phase 25's evidence template, protocol README, stable ledger, and verification pattern for v1.6 issue-03. | yes |
| Single combined adjudication memo | Put all source treatment and conflict notes into one long memo. | |
| Push machinery into contract phases | Let Phases 33-35 each invent their own packet/ledger pattern. | |

**User's choice:** Auto-selected recommended default.
**Notes:** The v1.5 Phase 25 precedent is the strongest local pattern and keeps Phase 32 as machinery plus headline records, not spec-edit execution.

---

## Headline Conflicts

| Option | Description | Selected |
|--------|-------------|----------|
| Five separate packets | D-04, D-05, D-06, M14, and the D conflict each get a separate record with own verdict/defer state and consumer phase. | yes |
| One umbrella packet | Combine all headline conflicts into a single source-conflict packet. | |
| Machinery only | Create template/protocol/ledger but leave all headline packets to later phases. | |

**User's choice:** Auto-selected recommended default.
**Notes:** The conflicts have different source status and downstream owners. Separate records reduce accidental cross-contamination.

---

## STOP-Safe Owner Decisions

| Option | Description | Selected |
|--------|-------------|----------|
| Surface or defer D-04/D-05/D-06 | If no explicit user instruction exists, record `defer-with-blocker` or a STOP/gap entry; do not auto-pick semantic defaults. | yes |
| Auto-pick likely defaults | Choose likely recommended values from the resolution doc in auto mode. | |
| Push all three to Phase 36 | Leave owner decisions until acceptance/handoff. | |

**User's choice:** Auto-selected recommended default.
**Notes:** This follows AGENTS.md governance and the Phase 31 `surface_to_user` routing. Auto mode is allowed for process defaults, not source-silent semantic decisions.

---

## Ledger and Verification

| Option | Description | Selected |
|--------|-------------|----------|
| Deterministic structural checks | Verify schema, lifecycle, ledger coverage, headline packet coverage, forbidden-path diff, and no `32-*-PLAN.md`. | yes |
| Manual review only | Rely on human reading of artifacts. | |
| Defer verification to Phase 36 | Let acceptance phase discover process-artifact issues. | |

**User's choice:** Auto-selected recommended default.
**Notes:** Phase 32 is machinery; structural checks are the right level of validation before downstream phases depend on its artifacts.

---

## Planning Boundary

| Option | Description | Selected |
|--------|-------------|----------|
| Stop before planning | Write context/log, commit them, and do not create or invoke `32-*-PLAN.md`. | yes |
| Follow `--auto` chain into plan-phase | Let auto-mode chain launch `gsd-plan-phase`. | |

**User's choice:** User explicitly requested stopping before planning starts.
**Notes:** The discuss workflow's default auto-chain behavior is overridden by the user's explicit boundary.

## the agent's Discretion

- Exact packet filename slugs.
- Exact ledger table formatting.
- Exact deterministic validation command shape.

## Deferred Ideas

- Phase 33-35 framework-spec edits.
- Phase 36 acceptance execution and handoff.
- FUT implementation/calibration work.
