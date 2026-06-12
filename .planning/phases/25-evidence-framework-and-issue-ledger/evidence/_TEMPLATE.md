# Evidence Packet: <ID> - <Title>

## Header

| Field | Value |
|---|---|
| ID | `<ID>` |
| Title | `<Title>` |
| Severity | `BLOCKING` / `MAJOR` / `MINOR` / `INFO` |
| Current Status | `PENDING` / `IN_PROGRESS` / `FIX_APPLIED` / `VERIFIED` / `DEFERRED` |
| Current Verdict | `accept-resolution` / `accept-issue-doc` / `accept-third-position` / `reject-both-as-unsupported` / `defer-with-blocker` / `-` |
| Phase | `Phase NN` |
| Acceptance Check ID | `AC-<REQ-ID>` |
| Spec Sections Touched | List exact framework spec section names or `None` |
| Code Paths Touched | List exact code paths or `Not code-applicable` |

## Source Positions

Add side-by-side line-range citations from both primary Issue 02 sources before selecting a verdict.

| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` | `path §N Q-XX:Lx-Ly` | Summarize the resolution document claim. |
| `pinn_instruction/issues/02-data-pipeline-and-validation.md` | `path:Lx-Ly` | Summarize the issue document claim. |

Do not add a primary-source field. Neither source is authoritative before adjudication.

BOTH citations are required even for uncontested verdicts (D-04 §2).

## Spec Evidence

Add line-range citations from the current framework specs that define the convention being changed or kept:

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` (citable as the sole written home of a convention, NEVER editable — SCOPE-09)

### Dataset Evidence (§3b)

Add line-range citations from the dataset-evidence annex `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` by `CLM-` or `DATA-` row ID and line range (e.g. `CLM-03:Lx-Ly`, `CLM-10:Lx-Ly`, `CLM-13:Lx-Ly`, `DATA-05:Lx-Ly`).

This is **EVID-06's fourth source**, which v1.4 packets did not have. Every v1.5 packet must cite at least the relevant CLM/DATA row from `24-VERIFIED-FACTS.md` so the dataset probe is part of the verdict's evidence basis.

## FUT-01 Hand-off Note (formerly "Code Evidence")

> **Note (v1.4 update 2026-05-19, carries into v1.5):** Live code in `pinn/` is NOT a v1.4 or v1.5 evidence source per user directive 2026-05-19. This section is repurposed for forward-pointing FUT-01 hand-off documentation only. Do NOT cite live code as a basis for a v1.5 verdict.

If this finding's new framework-spec contract diverges from the v1.3-era code and FUT-01 will need to rewrite something, note the relevant v1.3-era code paths with line ranges so `NN-CODE-DIVERGENCE.md` (or the eventual `pinn/STATUS.md`) can index it. Forward-pointing reference only.

- `pinn/basic_architecture.py:Lx-Ly` — v1.3-era position (FUT-01 hand-off reference only, NOT v1.5 evidence)
- `pinn/data-processing-pipeline-full.py:Lx-Ly` — same
- `Not FUT-01-applicable` when this finding creates no code-rewrite gap (e.g., process-artifact decisions).

## First-Principles Physics Check

<!-- REQUIRED for EVID-10: any finding whose ledger row says Sources Disagree? = YES. Optional otherwise. -->

Name the physical law, dimensional argument, numerical comparison, or architecture invariant used to adjudicate the claim. Show enough work that the verdict can be reviewed without trusting either primary source.

## Verdict

Select exactly one verdict:

- `accept-resolution`
- `accept-issue-doc`
- `accept-third-position`
- `reject-both-as-unsupported`
- `defer-with-blocker`

Record the reason for the verdict and link it to the cited source, spec, code, and physics evidence.

## Root-Cause Framework Ambiguity

<!-- REQUIRED for EVID-10: any finding whose ledger row says Sources Disagree? = YES. Optional otherwise. -->

Name the specific framework-spec passage, naming collision, missing convention, or contract gap that allowed the two primary sources to disagree.

## Locked Convention

<!-- REQUIRED for EVID-10: any finding whose ledger row says Sources Disagree? = YES. Optional otherwise. -->

State the convention now adopted in spec-edit-ready prose. This section is required before any downstream spec edit for an EVID-10 finding.

## Which Source Was Correct / Wrong

<!-- REQUIRED for EVID-10: any finding whose ledger row says Sources Disagree? = YES. Optional otherwise. -->

Assign correctness on a per-claim basis. Acceptable outcomes include one source correct, both partly correct, both wrong, or neither source addressing the decisive convention.

## Before / After Spec Note

For accepted edits, name the affected spec section and summarize the contract before and after the edit.

For false positives and intentional non-changes, state that the current convention remains valid and record `accept-resolution as no-change` when the verified resolution position is to keep the existing convention. This block doubles as the **EVID-08 false-positive record**: name the spec section, confirm no edit, and state why the current convention stands and which source misread it.

## Named Acceptance Check

Reserve an `AC-` identifier for this finding. Use the `AC-{REQ-ID}[-{NN}]` naming policy from the evidence README.

Phase 25 reserves names only. Runnable pass criteria, commands, and fixtures remain the owning spec-edit phase (Phases 26-28) and acceptance phase (Phase 29) scope. The packet's AC-ID citation feeds Phase 29's runnable acceptance-check build.

## Status Transition Log

Each entry must include `date`, `commit short SHA`, `status transition`, and `actor / plan reference`.

Example format:

```text
2026-MM-DD <SHA> PENDING -> IN_PROGRESS (Phase NN PXX by agent-or-user)
```
