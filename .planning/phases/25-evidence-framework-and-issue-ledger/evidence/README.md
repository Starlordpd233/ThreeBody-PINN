# Evidence Packet Protocol

This directory holds the reusable evidence workflow for v1.5 Issue 02 adjudication. Phase 25 defines the protocol only: downstream phases create one evidence packet per finding, then use the packet and `24-ISSUE-LEDGER.md` together before any framework-spec or code edit.

## Artifact Roles

| Artifact | Role |
|---|---|
| `../../24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` | Status index for every in-scope finding, including status, verdict, evidence-packet path, named acceptance check, spec section, `Dependents`, and last update. |
| `_TEMPLATE.md` | Copy source for starting a new packet. Copy it to `evidence/{finding-id}.md` and fill every required section before recording a verdict. |
| `evidence/{finding-id}.md` | One evidence packet per finding. Packets hold citations, physics checks, verdict reasoning, before/after notes, AC-ID reservations, and status transition logs. |

`24-ISSUE-LEDGER.md` is the status index. `_TEMPLATE.md` is the schema. `evidence/{finding-id}.md` is the finding-specific evidence record.

## Primary Sources

Every finding packet must cite both primary Issue 02 sources side by side before recording a verdict:

- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md`
- `pinn_instruction/issues/02-data-pipeline-and-validation.md`

Neither source is authoritative. A verdict is allowed only after both positions are cited with line ranges and checked against the current framework specs, the dataset-evidence annex (`24-VERIFIED-FACTS.md` CLM/DATA rows — EVID-06's fourth source), and first-principles physics where EVID-10 applies. **Live code in `pinn/` is NOT in the examination basis** (user directive 2026-05-19) — the v1.3-era code is artifact, not authority, and will be rebuilt from v1.4 specs in FUT-01.

The four EVID-06 sources for v1.5 packets:

1. Issue doc: `pinn_instruction/issues/02-data-pipeline-and-validation.md` (line range)
2. Resolution doc: `.../02-resolution-doc.md` (`§N Q-XX:Lx-Ly`)
3. Framework specs: `ctl_instruction.md` / `pinn_architecture.md` / read-only `data_quality_assessment.md` (line ranges; the last is citable as the sole written home of a convention but NEVER editable — SCOPE-09)
4. Dataset-evidence annex: `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` (CLM- or DATA-row IDs with line ranges — the §3b source; v1.4 had only the first three)

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

Each status transition must be recorded in the packet's `Status Transition Log` and mirrored in `24-ISSUE-LEDGER.md` with the relevant commit short SHA and plan reference.

### Status Legend (GAP-25-02 resolution Option A, 2026-06-12)

A `PENDING` row with a filled `Verdict` and `Evidence Packet` field means **adjudicated-but-unfixed** — the verdict has been assigned and the evidence packet exists, but the actual spec/code fix is owned by a downstream phase (Phases 26-28). Such rows carry a `PENDING -> PENDING (Phase 25 P02 EVID-10 record authored + verdict assigned)` audit entry in the per-finding subsection, recording the date and commit-audit label, rather than a forward transition.

**Exit-gate interaction (GAP-25-02 resolution addendum, 2026-06-12):** adjudicated-but-unfixed rows are **NOT** "in-scope findings" for Phase 25's phase-exit gate. Phase 25 **owns records, not fixes**; each such row becomes in-scope for the phase that owns its fix (Phases 26-28), at which point its `PENDING` status is subject to the standard phase-exit rules.

## EVID-10 Trigger Table

These findings are pre-flagged because the two primary sources disagree or require source-conflict adjudication before any edit:

| Finding | Topic | Required Flag | Adjudication Requirement |
|---|---|---|---|
| SCS | SCS thresholds vs locked log-drift gate | YES - EVID-10 required | Resolve ratio thresholds (1e-6/1e-8) vs locked `SCS = log10(eps_H)` reject `SCS > -5` gate. |
| D=6.694 | compute_globals D convention | YES - EVID-10 required | Resolve mass-fraction 6.694 vs raw-mass PHYS-01 `D ~ 4.6416`. |
| M11/M12 | severity reclassifications | YES - EVID-10 required | Resolve MAJOR->BLOCKING reclassification against verified-facts arithmetic and process-classification grounds. |

Any further conflict discovered between `02-resolution-doc.md` and `02-data-pipeline-and-validation.md` also triggers EVID-10. A contested packet must fill `First-Principles Physics Check`, `Root-Cause Framework Ambiguity`, `Locked Convention`, and `Which Source Was Correct / Wrong` before a verdict or spec edit.

## Regression Policy

Every ledger row has a `Dependents` field. After each batch of spec or code edits in Phases 26-28, the executing agent must identify every previously `VERIFIED` finding that is a transitive dependent of the edited finding or shared contract. The agent re-runs those findings' named acceptance checks.

If a regression is found, the affected finding returns to `IN_PROGRESS`, the phase records the regression in the ledger and packet transition log, and phase-exit is blocked until the finding reaches `VERIFIED` or `DEFERRED`.

A batch is the set of edits committed by one GSD plan.

## Phase-Exit Rule

No plan in Phases 26-28 (spec-edit phases) or Phase 29 (acceptance) may exit with an in-scope finding at `IN_PROGRESS` or `FIX_APPLIED`. Allowed phase-exit states are only `VERIFIED` and `DEFERRED`.

The ledger status and packet transition logs are part of the exit gate. Missing evidence, missing status transitions, or a "fix applied" row without a passing acceptance check blocks exit.

### D-03 Downstream Enforcement

The following plan-level constraints are encoded for the downstream Phases 26-28:

- **Packet-before-edit (EVID-06):** No spec edit in Phases 26-28 is permitted without a completed evidence packet + verdict for the finding being edited. Each owning spec-edit phase authors its non-conflict packets immediately before its edits using the machinery instantiated in this phase.
- **Phase-exit gate:** Phase-exit permits only `VERIFIED` or `DEFERRED` for in-scope findings. Adjudicated-but-unfixed rows (Status `PENDING` with a filled Verdict/Evidence-Packet) are not in-scope for Phase 25's exit — they become in-scope for the phase that owns the fix (see Status Legend above).
- **Same-commit ledger edits:** Ledger status edits and Evidence-Packet links travel in the same commit as the underlying change (spec edit, code edit, or status transition). Splitting them across commits is a process defect.

## Acceptance Check IDs

Reserve acceptance-check names using this pattern:

```text
AC-{REQ-ID}[-{NN}]
```

Examples: `AC-PIPE-01`, `AC-PHYS-02-COMP-AD`, `AC-FRAME-01`, `AC-ARCH-03`.

Phase 25 mints **no new AC-IDs** (D-13): the seeded assignments stand (`AC-PIPE-01..10` for the PIPE-owned findings and `AC-VAL-01..04` for the VAL-owned findings). Phase 25 reserves names only. Runnable pass criteria, commands, and fixtures remain the owning spec-edit phase (Phases 26-28) and acceptance phase (Phase 29) scope. Phases 26-28 cite the AC-ID their fix targets so Phase 29 can build and execute the acceptance suite.

## ID→Filename Map

Evidence packet filenames under `evidence/` use the sanitization rule: filesystem-safe, self-describing, one-file-per-conflict consistent with v1.4. For findings whose ledger IDs are not simple letter-number codes, sanitize the ID to a stable filename and record the mapping here.

| Ledger ID(s) | Packet Filename |
|---|---|
| `SCS` | `evidence/scs-thresholds.md` |
| `D=6.694` | `evidence/compute-globals-D.md` |
| `M11`, `M12` | `evidence/m11-m12-severity.md` |
| `B-06` | `evidence/b-06-admission-gate.md` |
| `B-11` | `evidence/b-11-id-resolution.md` |
| `D7` | `evidence/d7-footer-heterogeneity.md` |
| `M13` | `evidence/m13-gold-counterpart.md` |
| `D-03` | `evidence/d-03-training-data-format.md` |
| `mass-drift` / `DATA-05` (PIPE-07 precision facet) | `evidence/data05-precision.md` |
| `SASD` | `evidence/sasd-sampling-density.md` |
| `IPR` | `evidence/ipr-physics-residual.md` |

Sanitization rule: replace any character not in `[A-Za-z0-9_-]` with `-` and trim repeated `-`; lower-case the result unless the ID mixes cases the ledger preserves. Each filename must be unique within `evidence/`.

## Packet Start Procedure

1. Copy `_TEMPLATE.md` to `evidence/{finding-id}.md` using the ID→Filename Map above.
2. Fill the header with finding ID, status, phase, AC-ID, touched spec sections, and touched code paths.
3. Add side-by-side line-range citations from both primary sources before selecting a verdict.
4. Add current-spec evidence AND dataset-evidence (the §3b source — `24-VERIFIED-FACTS.md` CLM/DATA rows). Live-code evidence is NOT permitted in v1.5 packets per directive 2026-05-19; the renamed "FUT-01 Hand-off Note" section captures forward-pointing live-code references only.
5. For EVID-10 findings, complete the required conflict-adjudication sections before editing specs or code.
6. Record the verdict enum, before/after spec note, named acceptance check, and status transition log.
7. Update `24-ISSUE-LEDGER.md` (stable path `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md`) in the same commit as the packet or fix that changes status.

## Explicit Non-Goals

Phase 25 does not add a linter, generated traceability table, graph visualization, executable acceptance-check suite, individual adjudication packet (other than the three EVID-10 records authored in Plan 25-02), framework-spec edit, or code edit. Those are deferred ideas or downstream phase work.
