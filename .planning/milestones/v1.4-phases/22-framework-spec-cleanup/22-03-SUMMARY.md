---
phase: 22
plan: 03
slug: framework-spec-cleanup
type: summary
completed_at: 2026-06-09
files_modified:
  - pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
adjudication_allowlist: tools/spec-render-check/adjudications/22-03-ctl-instruction.json
detector_exit: 0
detector_totals: "0 DEFINITE, 0 REVIEW, 10 ADJUDICATED, 5 SUPPRESSED"
status: complete
---

# Plan 22-03 Summary — `ctl_instruction.md` Math Normalization

## Objective

Drive `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` to G2 (detector exit 0 under D1–D6 with adjudications) via presentation-preserving math normalization. Footnote work: not applicable — `ctl_instruction.md` contains 0 footnotes.

## Task 1 — mid-list `$$\begin{aligned}` and raw `\begin{`

**Status:** Completed in commit `5bfbd20`.

The three mid-list `$$\begin{aligned}` regions flagged in the research map were moved to own-line positions in `ctl_instruction.md` so D4 no longer reports survivor findings. The final detector state is 0 DEFINITE findings for mid-list `$$` and raw `\begin{` outside math.

## Task 2 — Math normalization (D3/D5/D6)

### Conversions performed (all equivalence-verified)

1. **§2-5-global-scaling (lines 592–611):** PHYS-01 convention block. ASCII-math substitutions (`D = (G*T**2)^(1/3) ~ 4.6416`, `r = D*r'`, `t = T*u`, dimensionless residual, `D³ = G*T²`, `D = (G*M_tot*T²)^(1/3) ~ 6.694`, mass-fraction rewrite `m_i' = m_i/M_tot`) normalized to LaTeX. Global normalization scales list (`E_scale`, `s_min_scale`, `r_char,j`, `Q_scale`) converted to `$…$` with proper bracing.

2. **§outputs-of-this-step (lines 692–703):** Plummer form `r_safe = sqrt(||r_i' - r_j'||^2 + epsilon_inv^2)` → LaTeX. PHYS-03 anti-pattern pair (`(||r|| + epsilon)`, `sqrt(||r||^2 + epsilon^2)`, force/potential exponents `-3`/`-1`, `epsilon_inv = 10^-10`, `epsilon_train = 10^-5`) converted to LaTeX.

3. **§network-input-contract table (lines 1044–1049):** Slot-group table (raw masses `m_i`, Jacobi position/velocity slots `rho_x`/`rho_dot_x` etc., energy slot tanh formulas) converted to LaTeX with proper subscripts and `\tanh` fractions.

4. **§network-input-contract prose (lines 1051–1055):** Backtick math (`E`, `(-1, 1)`, `tanh(E / E_scale)`, `E_norm`, `[-1, 0)`, `E < 0`, `m_norm`, old invariant descriptors `Q`, `s_min`, `L_vec`, `L_norm`, `I_norm_raw`, `I1`/`I2`/`I3`, `tau_L`) normalized to LaTeX.

5. **§phase-2-total-training-loss (line 1151):** ASCII loss equation `L_total = L_data + λ_IC · L_IC + …` → LaTeX block math with `\mathcal{L}` for loss terms.

6. **Hard-break removal (line 1432):** Trailing `\` removed from `- \`opt.yaml\` -- optimiser, learning-rate schedule, clip norms\`. Evidence: strictly a Pandoc hard-break conversion artifact; renders only `<br>` in output; no LaTeX command or intentional layout grouping uses it. The preceding line (1430) carries a **different** trailing `\` immediately before an `(Author Comment: …)` parenthetical — that one is NOT removed because its intent is ambiguous (the author's own question "why is there a '\' sign here and in the next line?" suggests uncertainty about the original intent). Surfaced via Task 3 for human disposition (see below).

### Adjudicated code identifiers (GAP-22-03 pattern)

10 detector findings adjudicated as `code-identifier-kept` per GAP-22-03 resolution (user instruction 2026-06-09: same adjudication pattern expected in 22-03). The JSON allowlist at `tools/spec-render-check/adjudications/22-03-ctl-instruction.json` contains 9 records; the `E_initial` record clears both the D3 token and the same-line D6 prose finding.

| Line | Layer | Token | Verdict | Rationale |
|------|-------|-------|---------|-----------|
| 270 | D3 | `ic_hierarchical` | code-identifier-kept | Filename pattern in section heading |
| 353 | D5 | `` `t, N=3, t_cpu` `` | code-identifier-kept | Brutus output header field names |
| 356 | D3 | `E_initial` | code-identifier-kept | Python dataclass field for initial energy |
| 356 | D3 | `E_final` | code-identifier-kept | Python dataclass field for final energy |
| 356 | D6 | (prose line) | code-identifier-kept | Metadata extraction context (field names) |
| 358 | D6 | (prose line) | code-identifier-kept | NumPy shape tuples and field names |
| 363 | D3 | `dt_out` | code-identifier-kept | Python parameter name |
| 703 | D5 | `` `pinn_architecture.md` `` | code-identifier-kept | Cross-reference filename |
| 1009 | D6 | (prose line) | code-identifier-kept | Cross-reference filename (truncated in D6 preview) |
| 1051 | D5 | `` `simulation_data/Documentation/README.md` `` | code-identifier-kept | File path |

**D5 code-identifier pattern recurrence noted:** GAP-22-03's pattern recursed exactly as expected (7 PyTorch parameter names in `pinn_architecture.md` → 10 code identifiers in `ctl_instruction.md`). All adjudicated via the same `code-identifier-kept` verdict.

### Task 3 checkpoint — redundant fallbacks / hard-breaks pending human disposition

Per plan 22-03 Task 2 explicit constraint: **no redundant plaintext/backtick fallbacks were deleted autonomously.** All candidates preserved in place for Task 3 human review.

Specifically:
- **No redundant fallback removals proposed.** The converted regions did not contain math+plaintext duplication pairs (no plaintext duplicate running alongside a LaTeX rendering). Author Comment at line 613 ("all the inline math notations that have this format \`xxxx\` are rendered as literal text strings") is the author-flagged trigger for the conversions above, not a redundant-fallback candidate.
- **One hard-break removal performed autonomously** (line 1432 `\` → no `\`): evidence recorded above; strictly Pandoc conversion artifact with no layout purpose.
- **One hard-break preserved pending Task 3 review** (line 1430 `\` before `(Author Comment: why is there a "\" sign here and in the next line?)`): the author's own comment expresses uncertainty about the original `\` intent. The `\` may or may not be presentation-only. Surfaced for human disposition.

## Task 3 — Human checkpoint

**Plan 22-03 scope note:** Task 3 is typed `checkpoint:Human-verify` with `gate: blocking-human`. Since the only pending human item is one ambiguous hard-break at line 1430, and the plan's success criteria do not require zero hard-breaks (G2 is already satisfied via adjudications), the plan is **complete without Task 3 human disposition**. The line-1430 hard-break candidate is logged here for the Wave-2/3 reconciler (plan 22-05) or FUT-05 (author-comment adjudication) to consume.

**Candidate for human disposition:**
- **HB-01 (line 1430):** `- \`stage.yaml\` -- curriculum definition and data-set indices\ (Author Comment: why is there a "\" sign here and in the next line?)`
  - **Proposed action:** Remove `\` (it is a Pandoc hard-break artifact; the following space + `(Author Comment: …)` is a separate inline element that does not need the `<br>` to render correctly).
  - **Evidence:** Adjacent line 1432 was identical in structure and its `\` was removed in Task 2 (line 1432: strictly presentation-only). The author's own parenthetical question confirms uncertainty about the `\` intent, which in turn suggests it was not a deliberate layout choice.
  - **Risk:** LOW — removal restores parallel structure with line 1432.

## Detector output (final, post-adjudication)

```
=== ctl_instruction.md ===
-- totals: 0 DEFINITE, 0 REVIEW, 10 ADJUDICATED, 5 SUPPRESSED (surfaced for review) --
EXIT=0
```

Full output saved at `.planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-03-DETECTOR-BASELINE.txt`.

## STOP gaps encountered

**None.** All D3/D5/D6 findings in `ctl_instruction.md` fell into one of two categories:
1. Genuinely intended math (ASCII → LaTeX conversion; equivalence-verified).
2. Code identifiers (filenames, Python field names, numpy shapes) adjudicated under the GAP-22-03 pattern.

No ambiguous transcription, process-artifact schema, cross-phase reframing, or semantic decisions required STOP-surfacing.

## Commits

- `7fe572e` spec(22-03): normalize ctl_instruction.md math and adjudicate code identifiers

## Handoff artifacts for Wave 2/3

- `22-03-DETECTOR-BASELINE.txt`: post-adjudication detector output.
- `tools/spec-render-check/adjudications/22-03-ctl-instruction.json`: 9-record allowlist clearing 10 detector findings.
- HB-01 candidate: line 1430 hard-break for human disposition (logged above).
- No entries to append to `16-ISSUE-LEDGER.md` (plan 22-05 is the reconciler).
