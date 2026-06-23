# Phase 33 Evidence Packet Protocol

This directory holds the Phase 33 evidence workflow for v1.6 Issue 03
curriculum-stage-contract adjudication. Phase 33 creates its own evidence
workspace by **mirroring** the Phase 32 protocol, packet template, status
lifecycle, verdict enum, and STOP handling; it does **not** introduce a new
verdict enum, status lifecycle, package dependency, schema push, or UI
artifact.

Phase 32 owns the protocol and template. Phase 33 owns five Phase 33
packets (`adaptive stage assignment`, `L_max / tau_L`, `M7`, `D5`, `M6`)
and links them into the Phase 32 stable ledger before any `ctl_instruction.md`
curriculum-stage edit.

## Artifact Roles

| Artifact | Role |
|---|---|
| `../32-ISSUE-LEDGER.md` (Phase 32) | Stable status index for every selected issue-03 finding consumed by Phases 32-36. Phase 33 updates only its five owned rows' Evidence Packet, Acceptance Check ID, and Transition Log fields. |
| `../32-evidence-framework-issue-ledger-conflict-adjudication/evidence/_TEMPLATE.md` (Phase 32) | Canonical packet schema; Phase 33 mirrors it via `_TEMPLATE.md` below with Phase 33 paths, no schema reinvention. |
| `_TEMPLATE.md` (Phase 33) | Phase 33 copy source for any Phase 33-owned packet. Header, source-positions, current-spec, locked-convention, FUT, first-principles, verdict, root-cause, owner-route, source-correctness, before/after, named acceptance check, STOP handling, and status-transition sections are mandatory. |
| `evidence/{finding-id}.md` (Phase 33) | One evidence packet per Phase 33-owned finding: `adaptive-stage-assignment.md`, `l-max-tau-l.md`, `m7-tau-l-ic13-exclusion.md`, `d5-stage-transitions.md`, `m6-l-norm-metadata.md`. |
| `../33-BASELINE-CAPTURED` | Sentinel recording the Phase 33 baseline (branch, dirty-doc set with dynamic SHA-256 fingerprints, resolution-doc fingerprint, `pinn/` empty snapshot). Plan 33-04 enforces the dirty-doc preservation check from this sentinel. |

## Source Hierarchy (mirrors Phase 32 README)

1. Locked v1.4 and v1.5 conventions from `.planning/REQUIREMENTS.md`
   SCOPE-12 and the current framework specs.
2. Current framework specs as revisable baseline evidence:
   - `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
   - `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
3. Phase 32 owned headline packets consumed by Phase 33:
   - `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-6-694-conflict.md`
     for the raw-mass `D ~= 4.6416` convention.
   - `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-05-s-min-frame.md`
     for the unsoftened geometric `s_min` stage-gate frame.
4. Candidate verdict source (Phase 33 packet entries):
   `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md`.
5. Non-authoritative issue source:
   `pinn_instruction/issues/03-curriculum-and-training-loop.md`.
6. Navigation and freshness aids:
   - `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md`
   - `.planning/phases/31-resolution-doc-readiness-verification/31-READINESS-REPORT.md`
7. Governance source: `AGENTS.md`, especially the v1.6 STOP protocol and
   no-live-code grounding rule.

The final resolution doc is a **candidate verdict source**, not authority.
The issue doc is also non-authoritative. A Phase 33 packet may accept either
source only after line-range citation and independent grounding against
locked conventions, current specs, dataset evidence where applicable, or
short first-principles / engineering checks.

## Citation Rules (mirror Phase 32 README)

- Cite line ranges, not whole files: `path:START-END`.
- For the resolution doc, include both section anchors and the line ranges
  mapped by `31-RESOLUTION-MAP.md`, then re-check freshness against
  `33-BASELINE-CAPTURED` before relying on those ranges.
- For current specs, cite the exact section or line range defining the
  convention being changed, preserved, or left unresolved.
- For locked conventions, cite the relevant prior packet, requirement, or
  roadmap line range.

## No Live `pinn/` Grounding

Live `pinn/` code is NOT grounding evidence for v1.6 adjudication.
References to `pinn/basic_architecture.py` or
`pinn/data-processing-pipeline-full.py` may appear only as FUT-01/FUT-04
hand-off notes, and the same paragraph must state that the reference is NOT
grounding.

## Verdict Enum (mirror Phase 32 README)

Use exactly one of these values once a packet is adjudicated:

| Verdict | Meaning |
|---|---|
| `accept-resolution` | Accept the candidate resolution document's position after independent verification. |
| `accept-issue-doc` | Accept the issue document's position after independent verification. |
| `accept-third-position` | Reject both source positions in favor of an independently justified convention. |
| `reject-both-as-unsupported` | Reject both source positions because neither survives evidence review. |
| `defer-with-blocker` | Defer because evidence is unavailable, explicit user instruction is required, or a blocker prevents adjudication. |

Pending ledger rows use `-` until the packet records one of the five
verdicts.

## Status Lifecycle (mirror Phase 32 README)

| Status | Meaning |
|---|---|
| `PENDING` | Finding is seeded but not actively adjudicated, or adjudicated-but-unfixed because the fix belongs to a downstream phase. |
| `IN_PROGRESS` | A phase is gathering evidence, applying an edit, or re-fixing a regression. |
| `FIX_APPLIED` | The evidence-backed edit has landed, but closure has not been verified. |
| `VERIFIED` | The named acceptance check passed and the ledger was updated with evidence. |
| `DEFERRED` | The finding has a written blocker and `defer-with-blocker` verdict. |

`FIX_APPLIED` is never terminal. Closure requires `VERIFIED` or `DEFERRED`
with a written blocker.

## STOP Protocol

If a semantic, process-schema, or cross-phase decision is not explicitly
grounded, stop the affected work. Before recording a STOP gap, confirm all
three AGENTS.md step-2 understanding checks:

1. The agent can articulate the mathematics, physics, or engineering
   principles at stake.
2. The agent can explain why each candidate resolution would have different
   downstream consequences.
3. The agent can identify the consulted source materials and why they did
   not answer the question.

If any answer is no, surface an understanding question instead of writing a
gap. If all answers are yes, record the gap in `../33-GAPS.md` and mirror
it to `.planning/milestones/v1.6-GAPS.md` with all AGENTS.md-required
fields. These gap files are created only when a real STOP gap is
encountered, not during ordinary protocol setup.

Phase 33 already has three owner-resolved gaps (`GAP-33-01`, `GAP-33-02`,
`GAP-33-03`, all `RESOLVED-WITH-INSTRUCTION` 2026-06-22) which carry the
grounded dispositions forward as constraints.

## Phase 33 Packet ID Map

Phase 33 owns these five findings and packet files; the Phase 32 ledger's
Acceptance Check ID column is reconciled to the convention in
`../33-01-PLAN.md`'s "Acceptance-Check ID Convention" section:

| Finding row (Phase 32 ledger) | Acceptance Check ID | Packet |
|---|---|---|
| `adaptive stage assignment` | `AC-CURR-01` | `evidence/adaptive-stage-assignment.md` |
| `L_max / tau_L` | `AC-CURR-02-LMAX` | `evidence/l-max-tau-l.md` |
| `M7` | `AC-CURR-02-M7` | `evidence/m7-tau-l-ic13-exclusion.md` |
| `D5` | `AC-CURR-03` | `evidence/d5-stage-transitions.md` |
| `M6` | `AC-CURR-04` | `evidence/m6-l-norm-metadata.md` |

(The `L_max / tau_L` row was seeded as `AC-CURR-02`; the `M6` row was seeded
as `AC-CURR-04-M6`. Phase 33 renames them to `AC-CURR-02-LMAX` and
`AC-CURR-04` respectively, per the Plan 33-01 convention section, so the
two `CURR-02` rows and the single `CURR-04` row are unambiguous.)

## Downstream Packet-Before-Edit Mandate (mirror Phase 32 README)

Phase 33 must author each owned non-headline row's evidence packet and
update `32-ISSUE-LEDGER.md` before editing any `ctl_instruction.md` section
for that row. Plan 33-01 implements that prerequisite for all five Phase 33
rows. Later Phase 33 plans (33-02, 33-03) may then transcribe contracts;
Plan 33-04 verifies the linkage, dirty-doc preservation, and protected-path
guard. Phase 36 must reject any spec edit whose ledger row lacks
packet/verdict linkage.

## Phase 33 Boundaries

- Phase 33 Plan 01 creates the baseline sentinel, evidence workspace, five
  Phase 33 packets, and links the Phase 32 ledger only. It does **not**
  edit any framework spec.
- Framework-spec edits in `ctl_instruction.md` (and any necessary
  `pinn_architecture.md` cross-links) belong to Plans 33-02 and 33-03.
- `.planning/STATE.md` is not directly edited by Phase 33 machinery for
  evidence purposes; Plan 33-04 closes the phase via the GSD workflow.
- `33-GAPS.md` is created only if a real STOP gap is encountered beyond the
  three already-resolved `GAP-33-01..03` entries.

## Explicit Non-Goals

This protocol does not create a linter, graph visualization, runnable
acceptance suite, framework-spec edit, production code edit, dataset EDA,
Stage-0 pilot, or training-loop implementation. Those are downstream or FUT
work.
