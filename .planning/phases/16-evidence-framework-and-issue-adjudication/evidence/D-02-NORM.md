# Evidence Packet: D-02-NORM - Raw-vs-bounded I_norm naming (issue-doc D-02)

## Header

| Field | Value |
|---|---|
| ID | `D-02-NORM` |
| Title | `Raw-vs-bounded I_norm naming (issue-doc D-02)` |
| Severity | `MINOR` |
| Severity Rationale | Routine documentation cleanup — naming reconciliation, not a methodology change. |
| Current Status | `IN_PROGRESS` |
| Current Verdict | `accept-resolution` |
| Phase | `Phase 20` |
| Acceptance Check ID | `AC-ARCH-04` |
| Spec Sections Touched | `ctl_instruction.md` Step 2 outputs list (invariants), Step 3 outputs tuple (I tuple), Step 3.3 compute_normalized_inertia block, Step 4 metadata-descriptor list |
| Code Paths Touched | `Not code-applicable` |

## Source Positions

| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `ctl_pinn_resolution.md` | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/01-architecture-and-physics-foundations/ctl_pinn_resolution.md:623-628` | Lines 623-628: "For inertia, distinguish the raw descriptor from the bounded metadata channel" — defines `I_norm_raw = trace(I_tensor) / (M_total * r_char**2 + eps)` and `I_norm_in = tanh(I_norm_raw)`. Also `ctl_pinn_resolution.md:1435-1443` (D-02 section, "Closed"): identical naming convention, "as metadata only unless a widened-input ablation is run." |
| `01-architecture-and-physics-foundations.md` | `pinn_instruction/issues/01-architecture-and-physics-foundations.md:42-62` | D-02 marked [ROUTINE]: "Confirm that the tanh-wrapped form is canonical for the input vector, and the raw ratio serves as the intermediate physics descriptor. This is a documentation reconciliation, not a methodology change." Status: "both forms coexist in the SOT with distinct purposes" (raw ratio for physics descriptor, tanh-wrapped for neural network input). "Methodology impact: zero." |

Neither source is authoritative before adjudication. Both sources explicitly agree on the raw-vs-bounded distinction: the raw ratio is the physics/metadata descriptor, and the tanh-wrapped form is the bounded network-facing value.

## Spec Evidence

Current `ctl_instruction.md` `I_norm` surfaces (re-located by `rg` after plans 20-03 and 20-04 shifted the file):

- `ctl_instruction.md:644` (Step 2 outputs list): Uses `I_norm_raw` in the invariants list — already aligned.
- `ctl_instruction.md:667` (Step 3 outputs tuple): Uses bare `I_{\mathrm{norm}}` in the LaTeX tuple — needs `_raw` suffix.
- `ctl_instruction.md:736-755` (Step 3.3 compute_normalized_inertia block): Uses `I_norm_raw` throughout — already aligned.
- `ctl_instruction.md:1042` (Step 4 metadata-descriptor list): Uses `I_norm_raw` among old invariant-heavy descriptors — already aligned.

**Source agreement confirmed:** Both primary sources agree on the raw-vs-bounded distinction. The resolution doc provides the explicit naming convention (`I_norm_raw` / `I_norm_in = tanh(I_norm_raw)`); the issue doc confirms the distinction is routine documentation cleanup with zero methodology impact. No source conflict exists.

## FUT-01 Hand-off Note

Not FUT-01-applicable. This finding concerns naming conventions in the framework spec only; no v1.3-era code divergence is created.

## First-Principles Physics Check

Not required — D-02-NORM is baseline non-EVID-05. No source conflict was found; sources agree on the raw/bounded distinction.

## Verdict

**`accept-resolution`**

The resolution doc (`ctl_pinn_resolution.md:623-628, 1435-1443`) provides an explicit, grounded naming convention for the raw-vs-bounded `I_norm` distinction. The issue doc (`01-architecture-and-physics-foundations.md:42-62`) confirms the same distinction as routine documentation cleanup with zero methodology impact. Both sources agree. The resolution-doc naming convention is adopted as the Locked Convention.

## Locked Convention

- `I_norm_raw` — the raw physics/metadata inertia descriptor, defined as `trace(I_tensor) / (M_total * r_char^2 + eps)`. This is a dimensionless ratio that can exceed 1 or fall below 0 (though typically positive for physical configurations).
- `I_norm_in = tanh(I_norm_raw)` — the bounded network-facing value, mapped to `(-1, 1)` via the tanh function for neural network input.
- `I_norm` (bare) — metadata only; not a final network IC slot under the Phase 17 input contract. The bare name must not be used where the raw-vs-bounded distinction matters.

## Which Source Was Correct / Wrong

Both sources are correct and consistent. The resolution doc provides the explicit naming convention; the issue doc correctly identifies the distinction as routine documentation cleanup. Neither source is wrong.

## Before / After Spec Note

| Surface | Before | After |
|---|---|---|
| Step 2 outputs list (line 644) | `I_norm_raw` | `I_norm_raw` (no change needed) |
| Step 3 outputs tuple (line 667) | `I_{\mathrm{norm}}` (bare, ambiguous) | `I_{\mathrm{norm,raw}}` (aligned with Locked Convention) |
| Step 3.3 compute_normalized_inertia (lines 736-755) | `I_norm_raw` throughout | `I_norm_raw` (no change needed) |
| Step 4 metadata-descriptor list (line 1042) | `I_norm_raw` | `I_norm_raw` (no change needed) |

## Named Acceptance Check

`AC-ARCH-04`: `I_norm` uses separate names for the raw inertia descriptor and the tanh-squashed network input.

## Status Transition Log

```text
2026-06-05 <pending-commit> PENDING -> IN_PROGRESS (Phase 20 P05 Task 1 by Phase 20 executor)
```
