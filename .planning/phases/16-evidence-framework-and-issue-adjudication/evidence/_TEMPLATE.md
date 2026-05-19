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

Add side-by-side line-range citations from both primary Issue 01 sources before selecting a verdict.

| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md` | `path:Lx-Ly` | Summarize the resolution document claim. |
| `pinn_instruction/issues/01-architecture-and-physics-foundations.md` | `path:Lx-Ly` | Summarize the issue document claim. |

Do not add a primary-source field. Neither source is authoritative before adjudication.

## Spec Evidence

Add line-range citations from the current framework specs that define the convention being changed or kept:

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`

## FUT-01 Hand-off Note (formerly "Code Evidence")

> **Note (v1.4 update 2026-05-19):** Live code in `pinn/` is NOT a v1.4 evidence source per user directive 2026-05-19. This section is repurposed for forward-pointing FUT-01 hand-off documentation only. Do NOT cite live code as a basis for a v1.4 verdict.

If this finding's new framework-spec contract diverges from the v1.3-era code and FUT-01 will need to rewrite something, note the relevant v1.3-era code paths with line ranges so `NN-CODE-DIVERGENCE.md` (or the eventual `pinn/STATUS.md`) can index it. Forward-pointing reference only.

- `pinn/basic_architecture.py:Lx-Ly` — v1.3-era position (FUT-01 hand-off reference only, NOT v1.4 evidence)
- `pinn/data-processing-pipeline-full.py:Lx-Ly` — same
- `Not FUT-01-applicable` when this finding creates no code-rewrite gap (e.g., process-artifact decisions).

## First-Principles Physics Check

<!-- REQUIRED for EVID-05: B-02, B-04, B-09, M5, and any further source conflict. -->

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

<!-- REQUIRED for EVID-05: B-02, B-04, B-09, M5, and any further source conflict. -->

Name the specific framework-spec passage, naming collision, missing convention, or contract gap that allowed the two primary sources to disagree.

## Locked Convention

<!-- REQUIRED for EVID-05: B-02, B-04, B-09, M5, and any further source conflict. -->

State the convention now adopted in spec-edit-ready prose. This section is required before any downstream spec edit for an EVID-05 finding.

## Which Source Was Correct / Wrong

<!-- REQUIRED for EVID-05: B-02, B-04, B-09, M5, and any further source conflict. -->

Assign correctness on a per-claim basis. Acceptable outcomes include one source correct, both partly correct, both wrong, or neither source addressing the decisive convention.

## Before / After Spec Note

For accepted edits, name the affected spec section and summarize the contract before and after the edit.

For false positives and intentional non-changes, state that the current convention remains valid and record `accept-resolution as no-change` when the verified resolution position is to keep the existing convention.

## Named Acceptance Check

Reserve an `AC-` identifier for this finding. Use the `AC-{REQ-ID}[-{NN}]` naming policy from the evidence README.

Phase 16 does not define runnable commands, fixtures, or pass criteria. Later phases fill those details when acceptance checks are implemented and executed.

## Status Transition Log

Each entry must include `date`, `commit short SHA`, `status transition`, and `actor / plan reference`.

Example format:

```text
2026-MM-DD <SHA> PENDING -> IN_PROGRESS (Phase NN PXX by agent-or-user)
```
