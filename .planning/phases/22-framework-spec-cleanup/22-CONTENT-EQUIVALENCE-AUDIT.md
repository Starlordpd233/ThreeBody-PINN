---
phase: 22
slug: framework-spec-cleanup
artifact: content-equivalence-audit
type: verification
audit_mode: audit-only
created: 2026-06-09
baseline_ref: v1.4-pre-phase-22
baseline_commit: faa73d0
head_commit: e773838
status: FINDINGS — phase stays OPEN pending user remediation instruction
verdict: 1 confirmed meaning-altering corruption (HIGH) + 5 flagged content changes (LOW–MEDIUM, value/meaning preserved) + 3 intentional structural changes (no remediation)
governance: "Governed by CLAUDE.md CRITICAL GOVERNANCE: audit-only decision (fix nothing, surface all) + v1.4 STOP protocol. Findings logged to 22-GAPS.md (GAP-22-04) and .planning/milestones/v1.4-GAPS.md."
tooling: .planning/phases/22-framework-spec-cleanup/22-06-content-audit.mjs
primary_evidence: .planning/phases/22-framework-spec-cleanup/22-06-BASELINE-HEAD.diff
---

# Phase 22 Content-Preservation Audit (audit-only)

## Purpose

Phase 22 revised the **syntax/formatting** of two authoritative framework specs —
`pinn_architecture.md` (23 changed hunks) and `ctl_instruction.md` (8 changed hunks).
`sampling_method.md` was untouched. The visual render check was already approved.

This audit answers the remaining question the render check cannot: **did the syntax
cleanup accidentally alter content** — a number, an equation, a dropped/added term, a
swapped operator/index, a mangled word, or a broken table cell? Per the user's
decisions: **audit-only** (fix nothing; surface all findings) and **bar = meaning-altering**.

**Result:** the audit found **one confirmed meaning-altering corruption** (the known
anchor at `pinn_architecture.md:263`), plus five lower-risk flagged content changes whose
value/meaning is preserved under the only coherent reading, plus three intentional
structural changes with no dangling references. The completeness guarantee holds: every
changed region of both files was adjudicated and **no number value and no prose word
changed anywhere except as itemized below.**

## Completeness guarantee (why this audit is exhaustive)

The `git diff` between the baseline tag `v1.4-pre-phase-22` (commit `faa73d0`) and HEAD
(`e773838`) is the **complete universe of changes**. Git guarantees every unchanged
(context) line is byte-identical between the two versions, so nothing outside the diff can
have drifted. The audit reduces to adjudicating every changed hunk (23 + 8 = **31**), and
this was cross-checked by a **whole-file token-multiset diff** (Detector D) that is immune
to table/paragraph reflow: it tokenizes the entire normalized file and nets unchanged
regions to zero, so any added/removed meaning-bearing token *anywhere* in either file
surfaces regardless of how lines were re-flowed.

## Tooling & reproducible commands

All commands run from repo root on commit `e773838` (branch `milestone/v1.4`).

```bash
# 0. Freeze inputs: confirm specs clean; sampling_method.md byte-identical (auto-pass)
git diff v1.4-pre-phase-22 HEAD -- pinn_instruction/markdown_conversion/framework-specs/sampling_method.md | wc -c   # -> 0

# 0/1. Save canonical raw diff (primary evidence) of the two edited files; count hunks
git diff v1.4-pre-phase-22 HEAD -- \
  pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md \
  pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md \
  > .planning/phases/22-framework-spec-cleanup/22-06-BASELINE-HEAD.diff
grep -c '^@@' .planning/phases/22-framework-spec-cleanup/22-06-BASELINE-HEAD.diff   # 23 + 8 reconcile to 31

# 2–6. Run the content audit (self-tests first, then Detectors A–D over the 31 hunks + whole files)
node .planning/phases/22-framework-spec-cleanup/22-06-content-audit.mjs

# 7. Supporting render gates (NOT content evidence)
node tools/spec-render-check/detect.mjs --selftest      # exit 0
node tools/spec-render-check/detect.mjs --regression    # exit 0
node tools/spec-render-check/detect.mjs --all           # exit 0 (0 DEFINITE, 0 REVIEW)

# 5. Census reproduction (26 PRE = 26 POST) — POST on HEAD, PRE on extracted baseline
node tools/spec-render-check/detect.mjs --census <three specs>          # union 26
# (baseline: git show v1.4-pre-phase-22:<spec> to a temp tree, then --census)   # union 26
```

**Evidence files (committed):**
- `22-06-BASELINE-HEAD.diff` — canonical raw diff (primary evidence).
  `sha256 = 66e9ee587728ac59743993f991cf08206f05d63ef47f513953bf8aefdebc8ad1`
- `22-06-content-audit.mjs` — the audit detector (self-tests + Detectors A–D).
- `22-COMMENT-CENSUS-PRE.md` / `22-COMMENT-CENSUS-POST.md` / `22-COMMENT-DIFF.md` — author-comment census (reproduced; see Step 5).

## Method — bounded normalization

Each detector compares the `-` (baseline) and `+` (HEAD) sides after **bounded
normalization** that folds **only declared formatting transforms**:

- math/code delimiters `$`↔`` ` ``↔bare; markdown `**bold**`/`*italic*` unwrapped;
- footnote refs `[^n]`↔`[n]`;
- LaTeX formatting wrappers (`\mathbf`/`\mathrm`/`\text`/…) and spacing/sizing commands removed;
- ASCII↔LaTeX symbol map (`sqrt`↔`\sqrt`, `sum`/`Σ`↔`\sum`, `epsilon`/`\varepsilon`↔`ε`, `||`↔`\lVert\rVert`, `<=`↔`\leq`, `\frac{A}{B}`↔`(A)/(B)`);
- greek name spelling (`\lambda`/`λ`/`lambda` → one canonical token);
- brace style (`_total`↔`_{total}`, `^2`↔`^{2}`) and prime repositioning (`r_j'`↔`r'_j`);
- numeric representation (`1e-10`==`10^{-10}`==`10^-10`); whitespace.

**Normalization NEVER touches the signal:** digits, `+ − = < >` operators, sign, or the
*contents* of a subscript/superscript (`_i`, `_{i,j}`, `^3`). A real content change cannot
be masked. This was proven by self-tests (below).

## Per-step results

**Step 0 — Freeze inputs & auto-pass.** Working tree clean for all three specs.
`git diff v1.4-pre-phase-22 HEAD -- sampling_method.md` = **0 bytes** → byte-identical →
100% preserved, excluded from further work. Canonical diff of the two edited files saved.

**Step 1 — Enumerate change universe.** Hunk count reconciles exactly:
`pinn_architecture.md` = 23, `ctl_instruction.md` = 8, **total 31**. ✓ (completeness established)

**Step 2 — Numeric-literal audit.** Whole-file number residual: **pinn_architecture.md
removed `{1e-5, 1e-5, 1e-8}`, added none; ctl_instruction.md removed `{1,2,3,3}`, added
none.** No number value was *changed*. The pinn removals are three author-flagged duplicate
parentheticals (F2); the ctl `{1,2,3}` are `I1/I2/I3`→`I_1/I_2/I_3` digits that became
subscript tokens (F5), and the 4th `3` is the `step3` of the removed heading anchor.

**Step 3 — Math token-sequence audit.** Per-hunk and whole-file symmetric difference of
operators, functions, relations, and full subscript/superscript tuples. Real signals: F3
(indices added to the residual equation), F4/F5 (subscript restructures), F6 (broken
subscript/prime repair). All other math deltas (`\mathbf` bolding, `\lVert`, `\frac`
vs `/`, greek spelling, brace style, inline→display promotion) normalized to empty.

**Step 4 — Table cell boundary & content audit.** Three tables compared cell-by-cell after
recovering baseline cells by the authors' 2-space visual separators (the Pandoc dash-rule
columns are unreliable — the long math overflows them, which is the exact mechanism of the
line-263 corruption):
- **Table 1 (`pinn_architecture.md`, "Architectural Hyperparameters")** — 12 rows, 3 cols
  both sides. FLATTENED token diff: removed `designed`, added `designe`. **CELL DRIFT** on
  the "Weight Init. (Hidden)" row: the Value↔Rationale boundary moved (math fused with the
  rationale prefix in col1; only "to preserve…" left in col2). → **F1**.
- **Table 2 (`pinn_architecture.md`, "Implementation Blueprint")** — 13 rows, 3 cols both
  sides. FLATTENED token diff **empty** → every cell token preserved.
- **Table (`ctl_instruction.md`, input-normalization slots)** — 4 rows, 3 cols both sides.
  FLATTENED token diff **empty**.

**Step 5 — Prose, footnote, cross-reference & comment audit.**
- **Prose words:** whole-file WORD residual contains **no author-comment or body prose
  word** other than the corruption (`designed`→`designe`), the heading rename
  (`Footnotes`→`References`), and the removed-anchor tokens (`architectural`, `tab`, `sec`,
  `ctl`, `step`). No sentence lost or gained a word.
- **Footnotes:** `pinn_architecture.md` has **17 = 17** definitions; all definition texts
  **byte-identical** modulo the declared `[^n]`→`[n]` renumbering. `ctl_instruction.md` has
  none. ✓
- **Cross-references:** the `PHYS-` / `FUT-` / `AC-` / `§` label set is **unchanged** in
  both files. ✓
- **Author-comment census (independent re-run):** `--census` on HEAD and on the extracted
  baseline both yield **union 26** (ctl 13, pinn 13, sampling 0). Re-derived PRE and POST
  hash sets **match the committed `22-COMMENT-CENSUS-PRE/POST.md` exactly (0 differences)**,
  reproducing the documented **26 PRE ↔ 26 POST bijection** (0 lost, 0 gained; 23
  hash-identical + 3 documented D-05 wrapper repairs where only surrounding prose was
  normalized and the comment clause is byte-identical). ✓

**Step 6 — Normalized full-text residual (backstop).** Whole-file token-multiset residual
(reflow-immune). Content (NUM+WORD) deltas are **exactly** the itemized findings; the only
high-volume SYM deltas are the declared table-syntax conversion (Pandoc rule dashes `-` →
GFM pipes `|`) and the subscript restructures. **No residual content token is unexplained
by the findings table.**

**Step 7 — Supporting render re-verification (NOT content evidence).** `--selftest` exit 0,
`--regression` exit 0, `--all` exit 0 (0 DEFINITE, 0 REVIEW, 17 ADJUDICATED). Confirms the
final state renders clean and the committed detector evidence reproduces. Explicitly
**supporting** — a green result does not close the content question.

## FINDINGS

### Confirmed meaning-altering corruption (must be remediated)

| # | File:line (HEAD) | Hunk | Baseline (`v1.4-pre-phase-22`) | Current (HEAD) | Category | Severity |
|---|---|---|---|---|---|---|
| **F1** | `pinn_architecture.md:263` | #18, Table 1 "Weight Init. (Hidden)" row | col2 (Rationale) = `…all subsequent SIREN layers, **designed** to preserve activation variance…` ; col1 (Value) = the `$\mathrm{U}[…]$` math **only** | col1 fuses math + `…all subsequent SIREN layers, **designe**` ; col2 = `to preserve…` ; stray `\|` mid-word at `designe \| to` | **Mangled word (dropped "d") + broken table cell** (math formula fused with rationale prose; Value/Rationale boundary lost) | **HIGH** |

F1 is the known anchor. The committed G3 audit (`22-RENDER-REVIEW.md`) classified this exact
hunk as *"cell content preserved"* — asserted, never mechanically verified. A pipe-count
check passes (row still has the right number of pipes). Only a cell **boundary/content**
comparison catches it. Mechanism: the baseline table was malformed (rationale text began at
column ~181 but the declared Pandoc rationale column starts at position 236), so the
Pandoc→GFM conversion split by column position, landing mid-word and dropping the "d".

### Flagged content changes (value/meaning preserved; surfaced for user disposition)

| # | File:line (HEAD) | Hunk | Change | Assessment | Severity |
|---|---|---|---|---|---|
| **F2** | `pinn_architecture.md:534, 592, 606` | #24/#25/#26 | Three author-flagged duplicate parentheticals removed: `(`10^-5`)`, `(`10^-5`)`, `(`10^-8`)` | **No information lost** — the canonical value remains stated in the same sentence (`$\epsilon_{train}=10^{-5}$`, `$\epsilon_L=10^{-8}$`). Content deletion beyond pure formatting, but value-preserving; author comments explicitly flagged the duplicates. | LOW |
| **F3** | `ctl_instruction.md:596` | #1 | PHYS-01 nondimensionalization residual: `Σ`→`\sum_j` and `d²r'/du²`→`d²\mathbf{r}'_i/du²` (LHS body index `_i` added) | RHS indices unchanged; the additions make implicit indices explicit on a governing physics equation. Likely notation completion, not a value/operator change. Flagged because it modifies a governing equation. | MEDIUM |
| **F4** | `ctl_instruction.md:609` | #2 | `s_min_scale` → `s_{\min,\mathrm{scale}}` | Chained-underscore identifier restructured to a comma subscript. Same referent (the normalization scale for `s_min`). | LOW–MED |
| **F5** | `ctl_instruction.md:1055` | #6 | `I1,I2,I3`→`I_1,I_2,I_3` ; `I_norm_raw`→`I_{norm,raw}` | Invariant-descriptor names properly subscripted in a metadata list (not a governing equation). Same referents. | LOW |
| **F6** | `pinn_architecture.md:672` | #29 | §3.5 angular-momentum constraint: broken subscripts/primes repaired — `L'_θ,α`→`L'_{θ,α}`, `L_0,α'`→`L'_{0,α}` | Indices grouped into braces and prime repositioned; same quantities under the only physically-coherent reading. Author comment explicitly flagged the syntax as broken and requested repair. | MEDIUM |

F2–F6 are all consistent with the **authorized Phase 22 scope** (the author comments
explicitly asked to fix broken inline-code math syntax; the duplicates were flagged). They
are surfaced per the audit-only decision and the v1.4 governance's MUST-surface rule for
subscript/index and physics-equation edits — **not** because they are believed to be drift.
The user adjudicates whether each is an accepted cleanup or requires remediation.

### Intentional structural changes (documented; no remediation)

| File:line (HEAD) | Hunk | Change | Why not a finding |
|---|---|---|---|
| `ctl_instruction.md:655` | #3 | Heading anchor `{#sec:ctl:step3}` removed | **No references** anywhere in the repo (grep hits are review docs describing the removal). Documented as intentional in execution reviews (commit `5bfbd20`). |
| `pinn_architecture.md` Table 1 (#18) | #18 | Div anchor `{#tab:architectural_hyperparameters}` removed | **No references** (only the detector's own regression fixture contains a copy). Part of the Pandoc-div→GFM table conversion. |
| `pinn_architecture.md:940` | #31 | `## Footnotes` → `## References` | Accompanies the declared `[^n]`→`[n]` footnote→numbered-reference conversion; the 17 reference definitions are byte-identical. Same semantic content (the source list). |
| both files | #18, #31, #6 | Pandoc fixed-width / multiline tables → GFM pipe tables | Structural syntax conversion; cell content verified token-clean by Detector B (F1 is the sole cell defect). |

## Verification — how we know the audit itself is sound

1. **Completeness.** Step 1 hunk count reconciles to 23 + 8 = 31; Step 0 proves no change
   exists outside the diff; Detector D (whole-file token diff) is reflow-immune and surfaces
   any content token changed *anywhere*. Together: no changed region is unaudited.
2. **Self-test against planted edits.** Before trusting the detectors, the script injects
   known defects into scratch inputs and confirms each is flagged:
   `[PASS]` changed digit (`1e-5`→`1e-4`); `[PASS]` swapped subscript index (`i,j`→`j,i`);
   `[PASS]` operator flip (`+`→`-`); `[PASS]` moved table pipe (cell-boundary drift);
   `[PASS]` mangled word (`designed`→`designe`); `[PASS]` **negative control** (a pure
   declared-formatting transform yields an empty symmetric difference). All 6 pass; a run
   with any failure aborts before auditing real data.
3. **Reproduce existing evidence.** The independent `--census` run reproduces the committed
   **26 PRE = 26 POST** bijection and matches the committed PRE/POST hash files exactly;
   Step 7 render gates exit 0 — the audit environment matches committed state.
4. **Known-positive anchor.** The run asserts `pinn_architecture.md:263` surfaces; it does
   (`ANCHOR SURFACED ✓`) via both Detector B (cell drift + FLATTENED `designed`→`designe`)
   and Detector A (per-hunk WORD diff). An audit that missed it would be defective.

## Disposition (audit-only)

Per the audit-only decision and the v1.4 STOP protocol: **nothing was fixed.** Findings are
logged to `22-GAPS.md` (**GAP-22-04**) and the milestone index `v1.4-GAPS.md`.

**The phase stays OPEN** until the user reviews and instructs on remediation. Restoring the
baseline value (`designed`, and reconstructing the Value/Rationale cell boundary) at F1 is
**grounded** (the baseline states it explicitly), but is deferred to that user-directed
remediation pass. F2–F6 await the user's disposition (accept as authorized cleanup, or
remediate). The three structural changes require no action.
