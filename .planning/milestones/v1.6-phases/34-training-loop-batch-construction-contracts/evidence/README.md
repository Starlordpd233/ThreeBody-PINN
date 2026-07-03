# Issue-03 Evidence Packet Protocol — Phase 34

This directory holds the Phase 34 evidence packets for the four
Phase-34-owned PENDING rows in the Phase 32 issue ledger before any
Phase 34 framework-spec edit. It reuses the Phase 32 evidence packet
schema and verdict/status lifecycle verbatim; it does not introduce a
new process schema or ID scheme.

## Artifact Roles

| Artifact | Role |
|---|---|
| `../32-ISSUE-LEDGER.md` | Stable status index for every selected issue-03 finding consumed by Phases 32-36. Phase 34 closes the B-07, B-08, M16, and ALM `mu_p` clamp rows and leaves M14 untouched. |
| `_TEMPLATE.md` | Copy source for starting any Phase 34 evidence packet. Packet authors must fill every required section before recording a verdict or allowing a spec edit. |
| `evidence/{finding-id}.md` | One evidence packet per Phase-34-owned finding. Packets hold source citations, current-spec evidence, locked-convention or dataset evidence, engineering checks, verdict reasoning, before/after or intentional non-change notes, named acceptance checks, STOP handling, and status logs. |
| `../34-VERIFICATION.md` | Durable structural verification record for baseline capture, protocol/template checks, ledger coverage, forbidden-path status, and later packet checks. |

`../32-ISSUE-LEDGER.md` is the status index. `_TEMPLATE.md` is the schema.
`evidence/{finding-id}.md` is the finding-specific evidence record.

## Source Hierarchy

Every packet must cite line ranges from the sources relevant to that finding before assigning a verdict.

1. Locked v1.4 and v1.5 conventions from `.planning/REQUIREMENTS.md` SCOPE-12 and the current framework specs.
2. Current framework specs as revisable baseline evidence:
   - `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
   - `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
3. v1.5 locked-convention evidence where relevant, especially `.planning/milestones/v1.5-phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md` for the raw-mass `D ~= 4.6416` convention.
4. Candidate verdict source: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md`.
5. Non-authoritative issue source: `pinn_instruction/issues/03-curriculum-and-training-loop.md`.
6. Navigation and freshness aids:
   - `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md`
   - `.planning/phases/34-training-loop-batch-construction-contracts/34-BASELINE-CAPTURED`
7. Governance source: `AGENTS.md`, especially the v1.6 STOP protocol and no-live-code grounding rule.

The final resolution doc is a **candidate verdict source**, not authority. The issue doc is also non-authoritative. A packet may accept either source only after line-range citation and independent grounding against locked conventions, current specs, dataset evidence where applicable, or short first-principles / engineering checks.

## Citation Rules

- Cite line ranges, not whole files: `path:START-END`.
- For the resolution doc, include both section anchors and revision-scoped line ranges from `31-RESOLUTION-MAP.md`, then re-check freshness against `34-BASELINE-CAPTURED` before relying on those ranges.
- For current specs, cite the exact section or line range defining the convention being changed, preserved, or left unresolved.
- For locked conventions, cite the relevant prior packet, requirement, or roadmap line range. For the `D = 6.694` conflict, cite the v1.5 `compute-globals-D.md` packet and SCOPE-12.
- Do not use report-attribution columns as votes. The Phase 31 map records that the resolution doc used claim collapsing, not report weighting.

## No Live `pinn/` Grounding

Live `pinn/` code is NOT grounding evidence for v1.6 adjudication. References to `pinn/basic_architecture.py` or `pinn/data-processing-pipeline-full.py` may appear only as FUT-01/FUT-04 hand-off notes, and the same paragraph must state that the reference is NOT grounding.

## Verdict Enum

Use exactly one of these values once a packet is adjudicated:

| Verdict | Meaning |
|---|---|
| `accept-resolution` | Accept the candidate resolution document's position after independent verification. |
| `accept-issue-doc` | Accept the issue document's position after independent verification. |
| `accept-third-position` | Reject both source positions in favor of an independently justified convention. |
| `reject-both-as-unsupported` | Reject both source positions because neither survives evidence review. |
| `defer-with-blocker` | Defer because evidence is unavailable, explicit user instruction is required, or a blocker prevents adjudication. |

Pending ledger rows use `-` until the packet records one of the five verdicts.

## Status Lifecycle

Use exactly these status values:

| Status | Meaning |
|---|---|
| `PENDING` | Finding is seeded but not actively adjudicated, or adjudicated-but-unfixed because the fix belongs to a downstream phase. |
| `IN_PROGRESS` | A phase is gathering evidence, applying an edit, or re-fixing a regression. |
| `FIX_APPLIED` | The evidence-backed edit has landed, but closure has not been verified. |
| `VERIFIED` | The named acceptance check passed and the ledger was updated with evidence. |
| `DEFERRED` | The finding has a written blocker and `defer-with-blocker` verdict. |

`FIX_APPLIED` is never terminal. Closure requires `VERIFIED` or `DEFERRED` with a written blocker.

Each status transition must be recorded in the packet `Status Transition Log` and mirrored in `../32-ISSUE-LEDGER.md` with the relevant commit short SHA and plan reference. Ledger status, packet links, verdicts, and transition-log edits travel in the same commit as the packet, spec edit, or verification result that changes them.

## STOP Protocol

If a semantic, process-schema, or cross-phase decision is not explicitly grounded, stop the affected work. Before recording a STOP gap, confirm all three AGENTS.md step-2 understanding checks:

1. The agent can articulate the mathematics, physics, or engineering principles at stake.
2. The agent can explain why each candidate resolution would have different downstream consequences.
3. The agent can identify the consulted source materials and why they did not answer the question.

If any answer is no, surface an understanding question instead of writing a gap. If all answers are yes, record the gap in `../34-GAPS.md` and mirror it to `.planning/milestones/v1.6-GAPS.md` with all AGENTS.md-required fields. These gap files are created only when a real STOP gap is encountered, not during ordinary protocol setup.

## Owner-Routed Decisions

M14 and the M14-deferred clipping constants are owner-routed to Phase 34/FUT but are **not** source-silent; they are carried as body-deferred in the LOOP-04 contract, not logged as a new STOP gap. The source-silent batch edge cases flagged by B-07 (`has_stage(k+1)`=false, undersized next-stage pool <16, replacement policy) are the anticipated `../34-GAPS.md` STOP gap (D-34-16a).

## Downstream Packet-Before-Edit Mandate

Phase 34 must author each owned non-headline row's evidence packet and update `../32-ISSUE-LEDGER.md` before editing any spec section for that row. Phase 36 must reject any spec edit whose ledger row lacks packet/verdict linkage.

## ID-to-Filename Map

Phase 34 packets use these stable filenames:

| Ledger ID | Packet Filename | Acceptance Check | Consumed Verdict |
|---|---|---|---|
| `B-07` | `evidence/b-07-replay-lookahead-batching.md` | `AC-LOOP-01` | `accept-resolution` (resolution doc §1.4 `modified`) |
| `B-08` | `evidence/b-08-data-vs-collocation-points.md` | `AC-LOOP-02` | `accept-resolution` (resolution doc §1.5 `modified`) |
| `M16` | `evidence/m16-dt-out-collocation-scaling.md` | `AC-LOOP-06` | `defer` (resolution doc §1.10 `defer`) |
| `ALM mu_p clamp` | `evidence/alm-mu-p-clamp.md` | `AC-LOOP-05` | `defer` (resolution doc §1.18 `defer`) |

`M14` is **not** re-authored by Phase 34; LOOP-04 consumes the existing Phase 32 packet `../32-evidence-framework-issue-ledger-conflict-adjudication/evidence/m14-gradient-clipping.md` (no new M14 packet). `LOOP-07` (IPR/PSC) and `LOOP-08` (SASD) are v1.5 carry-forwards with no ledger row and no packet.

Non-headline packets created by later phases must use filesystem-safe, self-describing filenames and update this README or the ledger if a stable map is needed. Sanitization rule: lower-case, replace any character not in `[A-Za-z0-9_-]` with `-`, trim repeated `-`, and keep filenames unique within `evidence/`.

## Packet Start Procedure

1. Copy `_TEMPLATE.md` to `evidence/{finding-id}.md` using the ID-to-filename map.
2. Fill the header with finding ID, title, status, verdict, phase, AC-ID, spec targets, code paths, owner phase, and consumer phase.
3. Add side-by-side line-range citations from the issue doc and the candidate verdict source.
4. Add current-spec evidence and locked-convention or dataset evidence where relevant.
5. Add the FUT hand-off note only for forward-pointing implementation divergence; live `pinn/` code remains NOT grounding.
6. Complete first-principles or engineering checks before assigning any root-cause verdict.
7. Fill `Verdict:` with exactly one verdict token, or `defer-with-blocker` when explicit user instruction is required.
8. Record root-cause ambiguity, locked convention or owner route, which source was correct or wrong, before/after or intentional non-change note, named acceptance check, STOP handling, and status transition log.
9. Update `../32-ISSUE-LEDGER.md` in the same commit as the packet or status change.

## Phase 34 Boundaries

- Phase 34 Plan 34-01 creates the baseline sentinel, protocol/template, four evidence packets, and the Phase 32 ledger linkage only.
- Framework-spec edits are forbidden in Plan 34-01. Contract transcription belongs to Plans 34-02 through 34-04.
- `.planning/STATE.md` is not edited or committed by Phase 34 (D-34-18).
- `../34-GAPS.md` and `.planning/milestones/v1.6-GAPS.md` are created only if a real STOP gap is encountered (the batch edge-case gap is anticipated in Plan 34-03).

## Explicit Non-Goals

This protocol does not create a linter, graph visualization, runnable acceptance suite, framework-spec edit, production code edit, dataset EDA, Stage-0 pilot, or training-loop implementation. Those are downstream or FUT work.
