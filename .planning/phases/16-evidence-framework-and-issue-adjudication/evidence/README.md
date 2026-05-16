# Evidence Packet Protocol

This directory holds the reusable evidence workflow for v1.4 Issue 01 adjudication. Phase 16 defines the protocol only: downstream phases create one evidence packet per finding, then use the packet and `16-ISSUE-LEDGER.md` together before any framework-spec or code edit.

## Artifact Roles

| Artifact | Role |
|---|---|
| `../16-ISSUE-LEDGER.md` | Status index for every in-scope finding, including status, verdict, evidence-packet path, named acceptance check, spec section, `Dependents`, and last update. |
| `_TEMPLATE.md` | Copy source for starting a new packet. Copy it to `evidence/{finding-id}.md` and fill every required section before recording a verdict. |
| `evidence/{finding-id}.md` | One evidence packet per finding. Packets hold citations, physics checks, verdict reasoning, before/after notes, AC-ID reservations, and status transition logs. |

`16-ISSUE-LEDGER.md` is the status index. `_TEMPLATE.md` is the schema. `evidence/{finding-id}.md` is the finding-specific evidence record.

## Primary Sources

Every finding packet must cite both primary Issue 01 sources side by side before recording a verdict:

- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md`
- `pinn_instruction/issues/01-architecture-and-physics-foundations.md`

Neither source is authoritative. A verdict is allowed only after both positions are cited with line ranges and checked against the current framework specs, live code when applicable, and first-principles physics where EVID-05 applies.

`master_consolidation_report.md` is supporting evidence only. It may help explain provenance or prior consensus, but it never substitutes for either primary source and must not be used as a verdict source.

## Verdict Enum

Use exactly one of these values once a packet is adjudicated:

| Verdict | Meaning |
|---|---|
| `accept-resolution` | Accept the resolution document's position after independent verification. |
| `accept-issue-doc` | Accept the issue document's position after independent verification. |
| `accept-third-position` | Reject both source positions in favor of an independently justified convention. |
| `reject-both-as-unsupported` | Reject both source positions because neither survives evidence review. |
| `defer-with-blocker` | Defer because evidence is unavailable or a blocker prevents adjudication. |

Pending ledger rows use `-` until the packet records one of the five verdicts.

## Status Lifecycle

Use exactly these status values:

| Status | Meaning |
|---|---|
| `PENDING` | Finding is seeded but not actively adjudicated. |
| `IN_PROGRESS` | A phase is gathering evidence, applying an edit, or re-fixing a regression. |
| `FIX_APPLIED` | The evidence-backed edit has landed, but closure has not been verified. |
| `VERIFIED` | The named acceptance check passed and the ledger was updated with evidence. |
| `DEFERRED` | The finding has a written blocker and `defer-with-blocker` verdict. |

`FIX_APPLIED` is not closure; `VERIFIED` requires a passing acceptance check. In prose reviews, treat "fix applied" as an intermediate state, never as evidence that the issue is closed.

Each status transition must be recorded in the packet's `Status Transition Log` and mirrored in `16-ISSUE-LEDGER.md` with the relevant commit short SHA and plan reference.

## EVID-05 Trigger Table

These findings are pre-flagged because the two primary sources disagree or require source-conflict adjudication before any edit:

| Finding | Topic | Required Flag | Adjudication Requirement |
|---|---|---|---|
| B-02 | D formula | YES - EVID-05 required | Resolve raw-mass vs mass-fraction scaling against current specs and Newtonian nondimensionalization. |
| B-04 | Input-vector orientation slots | YES - EVID-05 required | Resolve orientation/shape slots against current IC-vector specs and live input-vector construction. |
| B-09 | Softening strategy | YES - EVID-05 required | Resolve static invariant epsilon vs training-time force/energy softening with matched physics. |
| M5 | `I_3` normalization map | YES - EVID-05 required | Resolve the `I_3` support and mapping against specs, code, and first-principles triangle bounds. |

Any further conflict discovered between `ctl_pinn_resolution.md` and `01-architecture-and-physics-foundations.md` also triggers EVID-05. A contested packet must fill `First-Principles Physics Check`, `Root-Cause Framework Ambiguity`, `Locked Convention`, and `Which Source Was Correct / Wrong` before a verdict or spec edit.

## Regression Policy

Every ledger row has a `Dependents` field. After each batch of spec or code edits in Phases 17-21, the executing agent must identify every previously `VERIFIED` finding that is a transitive dependent of the edited finding or shared contract. The agent re-runs those findings' named acceptance checks.

If a regression is found, the affected finding returns to `IN_PROGRESS`, the phase records the regression in the ledger and packet transition log, and phase-exit is blocked until the finding reaches `VERIFIED` or `DEFERRED`.

A batch is the set of edits committed by one GSD plan.

## Phase-Exit Rule

No Phase 17-21 plan may exit with an in-scope finding at `IN_PROGRESS` or `FIX_APPLIED`. Allowed phase-exit states are only `VERIFIED` and `DEFERRED`.

The ledger status and packet transition logs are part of the exit gate. Missing evidence, missing status transitions, or a "fix applied" row without a passing acceptance check blocks exit.

## Acceptance Check IDs

Reserve acceptance-check names using this pattern:

```text
AC-{REQ-ID}[-{NN}]
```

Examples: `AC-IO-01`, `AC-PHYS-02-COMP-AD`, `AC-FRAME-01`, `AC-ARCH-03`.

Phase 16 reserves names only. Runnable pass criteria, commands, and fixtures remain Phase 21 scope. Phases 17-20 cite the AC-ID their fix targets so Phase 21 can build and execute the acceptance suite.

## Packet Start Procedure

1. Copy `_TEMPLATE.md` to `evidence/{finding-id}.md`.
2. Fill the header with finding ID, status, phase, AC-ID, touched spec sections, and touched code paths.
3. Add side-by-side line-range citations from both primary sources before selecting a verdict.
4. Add current-spec evidence and live-code evidence where applicable.
5. For EVID-05 findings, complete the required conflict-adjudication sections before editing specs or code.
6. Record the verdict enum, before/after spec note, named acceptance check, and status transition log.
7. Update `16-ISSUE-LEDGER.md` in the same commit as the packet or fix that changes status.

## Explicit Non-Goals

Phase 16 does not add a linter, generated traceability table, graph visualization, executable acceptance-check suite, individual adjudication packet, framework-spec edit, or code edit. Those are deferred ideas or downstream phase work.
