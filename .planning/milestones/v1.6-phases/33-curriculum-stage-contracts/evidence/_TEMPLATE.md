# Evidence Packet: <ID> - <Title>

> Phase 33 template, mirrored from the Phase 32 packet schema at `../../32-evidence-framework-issue-ledger-conflict-adjudication/evidence/_TEMPLATE.md`. No new verdict enum, status lifecycle, package dependency, schema push, or UI artifact is introduced. Section-heading changes here must be kept consistent with the Phase 32 template so a single verification harness covers both.

## Header

| Field | Value |
|---|---|
| ID | `<ID>` |
| Title | `<Title>` |
| Severity | `BLOCKING` / `MAJOR` / `MINOR` / `INFO` / `owner-decision` |
| Current Status | `PENDING` / `IN_PROGRESS` / `FIX_APPLIED` / `VERIFIED` / `DEFERRED` |
| Current Verdict | `accept-resolution` / `accept-issue-doc` / `accept-third-position` / `reject-both-as-unsupported` / `defer-with-blocker` / `-` |
| Phase | `Phase 33` |
| Owner Phase | `Phase 33` |
| Consumer Phase | `Phase 36` or other downstream phase |
| Acceptance Check ID | `AC-CURR-0X[-SUFFIX]` |
| Spec Sections Touched | Exact framework spec section names or `None` |
| Code Paths Touched | `Not code-applicable` or FUT hand-off paths only |

## Source Positions

Add side-by-side line-range citations from the two issue-03 adjudication
sources before selecting a verdict. Neither source is authoritative.

| Source | Required Line-Range Citation | Standing | Position Summary |
|---|---|---|---|
| `pinn_instruction/issues/03-curriculum-and-training-loop.md` | `path:START-END` | Non-authoritative issue source | Summarize the issue-document claim. |
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` | `path:START-END` plus section anchor | candidate verdict source, not authority | Summarize the resolution-document claim. |
| `.planning/phases/31-resolution-doc-readiness-verification/31-RESOLUTION-MAP.md` | `path:START-END` | Navigation / line-map aid | Record section mapping and freshness notes. |

Do not add an authoritative-source field. A packet verdict belongs to Phase
33 or the owning downstream phase after evidence review.

## Current Spec Evidence

Add line-range citations from the current framework specs that define the
convention being changed, preserved, or intentionally left unresolved:

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`

For read-only research reports, cite only when they explain provenance. Do
not edit or treat them as authoritative specs.

## Locked Convention / Dataset Evidence

Add line-range citations for hard constraints and empirical facts where
relevant:

- `.planning/REQUIREMENTS.md` SCOPE-12 through SCOPE-15.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-6-694-conflict.md`
  for the raw-mass `D ~= 4.6416` convention.
- `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/evidence/d-05-s-min-frame.md`
  for the unsoftened geometric `s_min` stage-gate frame.
- Phase 33 owner-resolved gaps `GAP-33-01`, `GAP-33-02`, `GAP-33-03`
  (all `RESOLVED-WITH-INSTRUCTION` 2026-06-22) — these supersede older
  owner-pending phrasing in roadmap and requirements.

If no locked-convention or dataset evidence applies, write `Not applicable`
and explain why.

## FUT Hand-off Note

Live `pinn/` code is NOT grounding evidence. References to
`pinn/basic_architecture.py` or `pinn/data-processing-pipeline-full.py` may
appear only as FUT-01/FUT-04 hand-off notes and must state in the same
paragraph that they are NOT grounding.

- FUT path / note: `<optional>`
- Not FUT-applicable: `<reason>`

## First-Principles or Engineering Check

Name the physical law, dimensional argument, numerical comparison,
architecture invariant, or engineering constraint used to adjudicate the
claim. Show enough work that the verdict can be reviewed without trusting
either source.

For owner-routed decisions, explain the engineering consequences of each
live option rather than choosing one by default.

## Verdict

Verdict: `<accept-resolution | accept-issue-doc | accept-third-position | reject-both-as-unsupported | defer-with-blocker | ->`

Explicit user instruction: `<path/line/chat reference or None>`

Reasoning:

- Cite the source, spec, locked-convention, dataset, or first-principles
  evidence that supports the verdict.
- Where a Phase 33 `GAP-33-0X` resolution is consumed, cite the resolution
  note and the AskUserQuestion disposition.

## Root-Cause Ambiguity

Name the specific framework-spec passage, naming collision, missing
convention, or contract gap that allowed the sources to disagree or forced
downstream owner routing.

Semantic, process-schema, and cross-phase gaps require STOP only when
actually encountered.

## Locked Convention or Owner Route

State one of:

- The convention now locked, in spec-edit-ready prose.
- The owner route and blocker when a decision is deferred.
- The intentional non-change rationale when current conventions stand.

Phase 33 owner-route examples (already resolved):

- `GAP-33-01`: per-stage population safeguard value is owner-pending the
  FUT admitted-set EDA; no value is locked in Phase 33.
- `GAP-33-02`: `tau_L` estimator / time-unit convention / final thresholds
  are owner-pending; Rosenstein-style baseline retained as revisable.
- `GAP-33-03`: raw `L_norm` metadata is stored unclipped; no global clamp
  is authorized; the `np.clip(L_norm, 0, 1)` clipped gate is owner-pending
  admitted-set evidence.

## Which Source Was Correct / Wrong

Assign correctness on a per-claim basis. Acceptable outcomes include one
source correct, both partly correct, both wrong, neither source addressing
the decisive convention, or owner-routed because neither source resolves
the decision.

Do not treat the resolution doc as authority and do not treat report
attribution columns as votes.

## Before / After or Intentional Non-Change Note

For accepted edits, name the affected spec section and summarize the
contract before and after the edit.

For false positives and intentional non-changes, state that the current
convention remains valid, name which source misread it, and record the
verification step.

For deferred findings, name the downstream phase, the unresolved blocker,
and the spec edit that must not happen until the blocker is resolved.

## Named Acceptance Check

Reserve an `AC-` identifier for this finding. Phase 33 uses the
reconciled convention from `../33-01-PLAN.md`: `AC-CURR-01`,
`AC-CURR-02-LMAX`, `AC-CURR-02-M7`, `AC-CURR-03`, `AC-CURR-04`.

Record the planned pass criterion and the owning phase. Runnable commands
and fixtures may be deferred to Phase 36 when this packet only routes the
evidence and acceptance-check identity.

## STOP / Gap Handling

If the packet opens a STOP gap, record:

- Gap file path: `../33-GAPS.md`
- Milestone index path: `.planning/milestones/v1.6-GAPS.md`
- Classification: `semantic` / `operational coordination` / `process-artifact schema` / `cross-phase reframing`
- Why AGENTS.md step-2 understanding checks passed.
- Which dependent work is blocked and which independent work can continue.

If no STOP gap is opened, write `No STOP gap opened` and explain why the
packet is grounded, deferred, or purely process/schema. For packets that
consume a Phase 33 owner-routed gap, the grounding reason MUST cite that
`GAP-33-0X` resolution note (e.g. "No STOP gap opened — disposition
grounded in `GAP-33-01` RESOLVED-WITH-INSTRUCTION 2026-06-22").

## Status Transition Log

Each entry must include `date`, `commit short SHA`, `status transition`,
and `actor / plan reference`.

Example format:

```text
2026-MM-DD <SHA> PENDING -> IN_PROGRESS (Phase 33 P01 by claude-code-gsd-executor-33-01)
```
