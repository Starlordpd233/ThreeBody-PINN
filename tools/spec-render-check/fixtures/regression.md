# Phase 22 detector regression fixtures

Labeled ground-truth for `detect.mjs --selftest` / `--regression` (G1). Each region is delimited
by an HTML-comment marker `<!-- REGION id=<id> expect=flag|clean -->`; the selftest derives region
line ranges from these markers at run time (no hardcoded line numbers, Pattern 3). `expect=flag`
regions must each produce >= 1 finding; `expect=clean` regions must produce 0 findings.

The flag regions are representative copies of the live author-flagged constructs (re-derived via
`detect.mjs --census` over `ctl_instruction.md` / `pinn_architecture.md`). The clean regions are the
two mandated negative controls: a `sampling_method.md`-style Pandoc definition list and an
SI-PINN-002-style meta-doc.

Region ordering note: the two `expect=clean` regions are placed first, and the two oracle-guided
(`D5`/`D6`) flag regions — the only ones carrying author markers — are placed last, so the ±20-line
oracle window of a marker can never reach a clean region.

<!-- REGION id=nc-sampling-definition-list expect=clean -->
## Negative control 1: Pandoc definition list (must NOT flag as a `: Table` caption)

This region mirrors `sampling_method.md` definition lists. It has no author marker, so D5/D6 stay
silent, and the `:   ` continuation lines must not be mistaken for table captions.

`epsilon`
:   This is a static, initial filter applied once to the configuration. Its purpose is a cheap
    rejection of initial conditions born in a near-collision state.

`min_sep`
:   This is a dynamic, short-term filter that checks for close encounters during the brief
    Leapfrog integration window.

The bounds are written `s_lo` and `s_hi` rather than `s_min` and `s_max` to avoid collision with
the minimum pairwise separation invariant.

<!-- REGION id=nc-si-pinn-002-metadoc expect=clean -->
## SI-PINN-002: Author comments preserved in converted body

These notes are metadata for future reconciliation. They are not part of the faithful converted
body and are excluded from fidelity comparison.

- **Description:** 3 author comments from the LaTeX source (`\authcomment{}`) are preserved in the
  converted body as bold bracketed text (`**[...]**`). These are editorial notes from the original
  authors, not content discrepancies:
  1. "Need more detail on this dynamic scheduling for omega_0" (Section 2)
  2. "Need confirmation on this hidden layer's detail" (Section 2)
- **Status:** Documented for future reconciliation; author resolves before training.

This meta-doc must be enumerated by `--census` but must never be flagged as a render defect: the
`\authcomment{}` token lives inside an inline code span and the bracketed notes are plain prose.

<!-- REGION id=ctl-midlist-aligned expect=flag -->
## Outputs of this step (D4: `$$` opened mid-list-item)

1.  **Total energy E, virial ratio Q, minimal separation $s_{\min}$.** $$\begin{aligned}
    E &= T + U,\\
    Q &= -T/U.
    \end{aligned}$$

This reproduces the `$$\begin{aligned}` appended to a bold list line: markdown-it will not treat
the mid-paragraph `$$` as block math, so the delimiters leak into visible text.

<!-- REGION id=pinn-fenced-div-table-caption expect=flag -->
## Finalized architectural hyperparameters (D4: `:::`, separator row, `: Table`)

::: {#tab:architectural_hyperparameters}
  **Hyperparameter**   **Recommended Value**   **Rationale**
  -------------------- ----------------------- -------------
  Depth                12 hidden layers        balance

  : Table 1: Architectural hyperparameters of the SQR-SkipResNet-SIREN backbone
:::

<!-- REGION id=pinn-footnote expect=flag -->
## Footnote reference and definition (D4, policy=unsupported branch)

The width is a strong default balancing expressivity and cost.[^1]

[^1]: Power-enhanced ResNet for Function Approximation.

<!-- REGION id=lint-bare-subscript expect=flag -->
## Bare multi-character subscripts in prose (D3 REVIEW)

The total loss decomposes as L_total = L_data + L_phys, where L_data anchors to ground truth and
L_phys is the physics residual. These render as literal text because they are not in math context.

<!-- REGION id=katex-parse-error expect=flag -->
## Hard KaTeX parse error (D1 DEFINITE)

The expression $x = \nonexistentmacro{y}$ contains an undefined control sequence that KaTeX
rejects under throwOnError.

<!-- REGION id=oracle-backtick-math expect=flag -->
## Backtick-wrapped math near an author flag (D5, oracle-guided)

Author Comment: all the inline math notations in `xxxx` format render as literal strings; fix the
syntax so it renders correctly in preview.

The energy softening uses `epsilon_H = 1e-4 * S_H` for the matched-Plummer Hamiltonian.

<!-- REGION id=oracle-prose-math expect=flag -->
## Raw-prose ASCII math near an author flag (D6, oracle-guided)

Author note: this syntax is not ideal since it involves math formulae; it should use proper
render-friendly markdown.

Constraints: c_E = RMS_n(dH_n) for energy drift across the trajectory window.
