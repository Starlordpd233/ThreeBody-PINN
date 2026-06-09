---
phase: 22
slug: framework-spec-cleanup
artifact: render-review
status: PENDING-USER-REVIEW (visual backstop)
created: 2026-06-09
gates: [G1, G2, G3, G4, VER-05]
detector_version: "tools/spec-render-check/detect.mjs (commit faa73d0 baseline + 22-02/22-03 adjudication layer)"
---

# Phase 22 — Render Review (D-10 record)

**Purpose:** Record the exact detector command + full output for every gate run, and provide the
per-file Cursor/VS Code render-review checklist (D-09) for the human visual backstop. Render
correctness is established only when BOTH automated (G1/G2) AND manual (G4) pass.

**Baseline ref for diff computations:** git tag `v1.4-pre-phase-22` (commit `faa73d0`).
**Adjudication allowlists:**
- `tools/spec-render-check/adjudications/22-02-pinn-architecture.json` (7 entries)
- `tools/spec-render-check/adjudications/22-03-ctl-instruction.json` (9 records clearing 10 detector findings)

---

## G1 — Detector selftest

**Command:** `node tools/spec-render-check/detect.mjs --selftest`
**Exit:** 0

```
sanity gate: PASS (inline + block math rendered by KaTeX)

regression fixtures: 9 labeled regions
  region 'nc-sampling-definition-list' expect=clean
  region 'nc-si-pinn-002-metadoc' expect=clean
  region 'ctl-midlist-aligned' expect=flag
  region 'pinn-fenced-div-table-caption' expect=flag
  region 'pinn-footnote' expect=flag
  region 'lint-bare-subscript' expect=flag
  region 'katex-parse-error' expect=flag
  region 'oracle-backtick-math' expect=flag
  region 'oracle-prose-math' expect=flag

negative control sampling_method.md: 0 findings (1 suppressed)

SELFTEST PASS (G1): regression reproduced, negative controls clean.
```

**Verdict:** PASS. Sanity gate rendered both inline + block math; all 9 regression fixtures
reproduced (2 clean + 7 flag); negative control clean.

---

## G2 — Full detector suite across all 3 specs

**Command:** `node tools/spec-render-check/detect.mjs --all`
**Exit:** 0

`--all` auto-loads the committed Phase 22 adjudication allowlists:
- `tools/spec-render-check/adjudications/22-02-pinn-architecture.json` (7 records)
- `tools/spec-render-check/adjudications/22-03-ctl-instruction.json` (9 records; clears 10 detector findings because the `E_initial` record matches both the same-line D3 and D6 findings)

```
-- totals: 0 DEFINITE, 0 REVIEW, 17 ADJUDICATED, 20 SUPPRESSED (surfaced for review) --
```

Per-file results in the full-suite run:

| File | Result |
|------|--------|
| `pinn_architecture.md` | 0 DEFINITE, 0 REVIEW, 7 ADJUDICATED, 14 SUPPRESSED |
| `ctl_instruction.md` | 0 DEFINITE, 0 REVIEW, 10 ADJUDICATED, 5 SUPPRESSED |
| `sampling_method.md` | 0 DEFINITE, 0 REVIEW, 0 ADJUDICATED, 1 SUPPRESSED |

The single `sampling_method.md` SUPPRESSED item is the identifier-shape `close_low_L`, which D3
excludes. No REVIEW findings remain. Negative control is clean and unchanged since pre-Phase-22.

**G2 Verdict:** PASS. The full-suite `--all` gate reaches exit 0 with 0 DEFINITE + 0 REVIEW
findings after auto-loading the committed adjudication allowlists. The allowlist mechanism is the
documented tiered-detector mechanism (design §5.4; GAP-22-03 RESOLVED-WITH-INSTRUCTION).
`sampling_method.md` remains 0-findings (negative control).

---

## G3 — Content-preservation audit

**Baseline ref:** git tag `v1.4-pre-phase-22` (commit `faa73d0`)
**Changed files since baseline:**

| File | Hunks | +/- lines | Plan | Commit range |
|------|-------|-----------|------|--------------|
| `pinn_architecture.md` | 23 | 170 | 22-02 | `faa73d0..64345f9` |
| `ctl_instruction.md` | 8 | 60 | 22-03 | `faa73d0..64345f9` |
| `sampling_method.md` | 0 | 0 | (not edited) | — |

**Per-hunk classification (representative samples; full diff committed via `git show`):**

### pinn_architecture.md (23 hunks)

| Hunk | Lines | Classification | Evidence |
|------|-------|----------------|----------|
| H1 | 19–32 | Footnote form `[^n]` → `[n]` (footnote-policy `unsupported`; see `22-STAGE0-FOOTNOTE-PROBE.md`) | 22-02 Summary; Stage-0 probe |
| H2–H5 | 40, 62, 76, 117 | Same footnote form conversion | 22-02 Summary |
| H6 | 137–150 | Footnote form conversion | 22-02 Summary |
| H7 | 156, 175, 183 | Math delimiter normalization (`\omega_0` inline `$…$` forms) | 22-02 Summary Task 2; adjudication 22-02 |
| H8 | 248–271 | Pandoc multiline table → GFM table (hyperparameter table; cell content preserved); `\text{LayerNorm}` brace normalization | 22-02 Summary Task 1 + Task 2; adjudication 22-02 (elementwise_affine/first/hidden_omega_0 adjudicated) |
| H9–H11 | 277, 300, 464 | Math delimiter normalization (prose-embedded `$…$`/`$$…$$`) | 22-02 Summary Task 2 |
| H12–H14 | 483, 514, 531 | Trailing-`\` Pandoc hard-break removal + math brace normalization (D8) | 22-02 Summary Task 2 |
| H15–H17 | 589, 598, 620 | Math in code-block surroundings normalized; warmup schedule `$I_{warm}$` brace form | 22-02 Summary Task 2 |
| H18 | 648–652 | Warmup schedule `$I_W$` → `$I_{warm}$` brace normalization | 22-02 Summary Task 2 |
| H19 | 669 | Math normalization in P2-ablation section | 22-02 Summary Task 2 |
| H20 | 766 | Math normalization in soft-energy section | 22-02 Summary Task 2 |
| H21 | 917–961 | Large Pandoc multiline table → GFM table (architecture blueprint; cell content preserved) | 22-02 Summary Task 1 |
| H22–H23 | (author comments) | D-05 wrapper-only repairs (3 comments — see COMMENT-DIFF) | 22-04 Summary; 22-COMMENT-DIFF.md |

All 23 hunks fall into allowed categories:
1. **Math delimiter/brace normalization** (H6–H7, H9–H14, H17–H20) — design §5.3 "Fix classes"
2. **Pandoc multiline table → GFM conversion preserving cell content** (H8, H21) — design §5.3
3. **Footnote form `[^n]` → `[n]`** (H1–H6) — Stage-0 probe confirmed `unsupported`; footnote policy applied
4. **Trailing-`\` hard-break removal** (H12–H14) — design D8
5. **D-05 wrapper-only author-comment repair** (H22–H23) — 22-04 Summary; COMMENT-DIFF §D-05 Wrapper Repair Register

### ctl_instruction.md (8 hunks)

| Hunk | Lines | Classification | Evidence |
|------|-------|----------------|----------|
| H1 | 590–602 | ASCII-math → LaTeX `$…$` (D = (G*T**2)^(1/3), r = D*r', residual formula) — equivalence-verified | 22-03 Summary Task 2 |
| H2 | 605–614 | ASCII-math → LaTeX `$…$` + whitespace for block rendering (`\begin{aligned}` moved to own lines) | 22-03 Summary Task 1 + Task 2 |
| H3 | 652 | Section heading: Pandoc attribute `{#sec:ctl:step3}` removed | 22-03 Summary Task 2 (Pandoc attribute cleanup) |
| H4 | 676–722 | ASCII-math → LaTeX `$…$` (invariants `I_1, I_2, I_3`; `$s_{\min}$`; Q_scale; s_min,scale); `\begin{aligned}` own-line placement | 22-03 Summary Task 1 + Task 2; adjudication 22-03 (code-identifier-kept for `ic_hierarchical`, `E_initial`, `E_final`, etc.) |
| H5 | 1033–1050 | Math delimiter normalization around displayed equation | 22-03 Summary Task 2 |
| H6 | 1140–1152 | Whitespace for block rendering (data-flow diagram surroundings) | 22-03 Summary Task 2 |
| H7 | 1421–1433 | D-05 wrapper-only author-comment repair (single comment) | 22-04 Summary; 22-COMMENT-DIFF.md |
| H8 | (author comments elsewhere) | D-05 wrapper-only repair (counted above) | 22-04 Summary |

All 8 hunks fall into allowed categories:
1. **Math delimiter normalization / ASCII-math → LaTeX** (H1, H2, H4, H5) — design §5.3
2. **Whitespace for block rendering (`\begin{aligned}` own-line placement)** (H2, H4, H6) — design §5.3
3. **Pandoc attribute removal** (H3) — presentation-only
4. **D-05 wrapper-only author-comment repair** (H7, H8) — 22-04 Summary; COMMENT-DIFF §D-05 Wrapper Repair Register

### G3 comment-preservation sub-gate

**Source artifacts (committed):**
- `.planning/phases/22-framework-spec-cleanup/22-COMMENT-CENSUS-PRE.md` (PRE, 26 comments)
- `.planning/phases/22-framework-spec-cleanup/22-COMMENT-CENSUS-POST.md` (POST, 26 comments)
- `.planning/phases/22-framework-spec-cleanup/22-COMMENT-DIFF.md` (full D-05-aware diff)
- `.planning/phases/22-framework-spec-cleanup/22-COMMENT-HANDOFF.md` (FUT-05 handoff)

**Result:** 0 comments lost, 0 comments gained, 23/26 byte-identical text hashes, 3/26 D-05
wrapper-only repairs (verbatim author-comment clause byte-stable in all 3).

**G3 Verdict:** PASS. Every changed hunk is classified into an allowed category with
per-hunk evidence; 0 comments lost, 0 semantically changed.

**G3 post-audit correction (2026-06-09) — supersedes the H8 "cell content preserved"
assertion:** An independent content-equivalence audit
(`.planning/phases/22-framework-spec-cleanup/22-06-content-audit.mjs`, full report
`.planning/phases/22-framework-spec-cleanup/22-CONTENT-EQUIVALENCE-AUDIT.md`) confirmed that
the H8 hyperparameter-table row at `pinn_architecture.md:263` was **not** cell-content
preserved — `designed` was mangled to `designe` and the Value↔Rationale column boundary was
fused. This was remediated in commit `bf841f6`
(`fix(22): restore corrupted weight-init table cell in pinn_architecture spec`): the
baseline cell structure is now restored and the row reconciles to baseline content. All
other H1–H23 hunks in `pinn_architecture.md` and H1–H8 in `ctl_instruction.md` retain
their G3 classification; the comment-preservation sub-gate is unchanged. See
`22-GAPS.md` GAP-22-04 for the full resolution note and F2–F6 disposition.

---

## G4 — Manual Cursor/VS Code render review

**Status:** APPROVED 2026-06-09 (user visual backstop). The user opened all three framework
specs in Cursor/VS Code Markdown Preview, walked the user-facing checklist below, and
reported no defects. The H8 corruption noted in the G3 post-audit correction is not
visible in the rendered output (the cell boundary is correct and "designed" renders
intact) — the corruption was a structural defect in the markdown source, not a rendered
artifact. The checklist below is retained as the approved inspection guide.

### User-facing visual review checklist

Open each of the 3 specs in the **actual Cursor / VS Code Markdown Preview**:
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
- `pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`

For each spec, scroll the **entire document** and check every item below. Mark PASS/FAIL.

#### A. pinn_architecture.md — focus regions

1. **Footnote rendering (§1 intro, §2.1, §2.2, §2.3, §3.3, §3.4, §5.1, §5.2):** `[^1]`/`[^2]`/`[^5]` tokens should no longer appear as `[^n]`. They now render as plain `[1]`/`[2]`/`[5]` (Stage-0 probe confirmed Cursor does not render `[^n]` as footnotes). Confirm no `[^` survives in visible text.
2. **§2.4 Finalized Architectural Hyperparameters — GFM table:** The old Pandoc multiline table should now be a proper GFM table with `| LayerNorm | elementwise_affine=False, eps=1e-5 |` rows. Confirm it renders as a table (not a code block, not raw pipe text).
3. **§2.4 inline math `$\omega_0$`, `$\mathrm{W}_i$`, etc.:** Confirm each renders as typeset math (not raw backtick text, not raw `$$`).
4. **§2.2 SIREN equation:** `$$\phi_i(\mathrm{x}) = \sin(\mathrm{W}_i \mathrm{x} + \mathrm{b}_i)$$` — confirm displayed math renders cleanly on its own line.
5. **§3.4 Soft energy conservation regularizer:** `$\text{LayerNorm}$` inline forms + Plummer/anti-pattern math `$\lVert \mathbf{r} \rVert$` — confirm rendered; confirm the 3 D-05-repaired author comments above/below are still present and legible.
6. **§5.1/§5.2 Warmup schedule:** `$I_{\mathrm{warm}} = \min(2000, 0.1 \cdot N_{\mathrm{Adam},k})$` — confirm subscript braces render (not `I_w arm` broken).
7. **§6 Architecture blueprint — GFM table:** The old Pandoc multiline architecture table should render as a proper GFM table with all cells (SQR-SkipResNet, SIREN, skip connection, LayerNorm, output head rows) visible.
8. **Author comments (all 13 in this file):** Confirm each `Author Comment:` / `Author note:` / `\authcomment` marker is present and its text is legible. Specifically the 3 D-05 wrapper repairs — their surrounding prose should be intact and the comment itself unchanged verbatim.

#### B. ctl_instruction.md — focus regions

1. **§1 Governing Mathematical Convention block (around line 590–620):** The ASCII-math `D = (G*T**2)^(1/3) ~ 4.6416` should now render as `$D = (G T^2)^{1/3} \approx 4.6416$`; the residual formula should render as a proper displayed fraction. Confirm the `\begin{aligned}` block is on its own line and renders as a multi-line equation.
2. **§Step 2 invariants (around line 676–722):** `$s_{\min}$`, `$I_1, I_2, I_3$`, `$Q_{\mathrm{scale}}$`, `$s_{\min,\mathrm{scale}}$` — confirm subscripts render cleanly. Confirm the `\begin{aligned}` block is on its own line and renders as a multi-line equation.
3. **§Step 3 heading:** No longer has `{#sec:ctl:step3}` Pandoc attribute. Confirm the heading renders cleanly.
4. **§Step 1 data fields (around line 353–363):** Code identifiers `ic_hierarchical`, `t, N=3, t_cpu`, `E_initial`, `E_final`, `dt_out`, `(T,3,3)` — confirm they render as code (backtick-styled or equivalent) and are not misrendered as math.
5. **§4 network input contract (around line 1009, 1051):** Cross-references `pinn_architecture.md` and `simulation_data/Documentation/README.md` — confirm they render as code/filenames, not as math.
6. **§3.4 displayed equation (around line 1033–1050):** Confirm the displayed equation renders cleanly with proper KaTeX.
7. **Data-flow section (around line 1140–1152):** Confirm surrounding whitespace produces clean paragraph breaks, not cramped text.
8. **Author comments (all 13 in this file):** Confirm each `Author Comment:` / `Author note:` marker is present and legible. Specifically the D-05 wrapper repair — its surrounding prose should be intact and the comment itself unchanged verbatim.

#### C. sampling_method.md — baseline check (negative control, never edited)

1. **Full document scroll:** Confirm nothing has regressed (this file was NOT edited in Phase 22; the detector reports 0 findings + 1 SUPPRESSED `close_low_L` identifier).
2. **Existing math/tables/lists:** Confirm they still render correctly (no accidental breakage from shared-environment changes).

#### D. Cross-file checks

1. **Shared formulas:** The characteristic-length formula `D`, the residual formula, the Plummer softening form `ε_train=10⁻⁵`/`ε_inv=10⁻¹⁰` are referenced in both files. Confirm they render identically in both.
2. **Cross-references:** `pinn_architecture.md` referenced from `ctl_instruction.md` and vice versa — confirm the filenames appear as code, not as math.

**Please reply:** "approved" if every checklist item passes, OR describe any defect found
(which file, which section, what is broken) so it can be routed back to the owning WS-A plan.

---

## VER-05 — Phase-22 ledger reconciliation

**See:** `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`
**Section:** `## Phase 22 Acceptance & VER-05 Reconciliation Addendum` (appended by plan 22-05)

**Summary:** 3 render findings tracked (P22-R1 Pandoc multiline tables, P22-R2 raw/backtick
ASCII-math, P22-R3 Pandoc fenced-div/caption/attribute survivors). All 3 transitioned through
PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED via WS-A plans 22-02 and 22-03 with detector
zero-residual as the acceptance check.

**Deferred findings (design §12 — OUT of Phase 22 scope, explicit user-grounded deferral):**
- Content inconsistencies (SI-PINN-002 batch-construction issue) — deferred to owning track.
- IC-dimension reconciliation note — deferred to FUT-01.
- Outdated code-folder references — deferred to owning track.

**Author-comment disposition (FUT-05):** Per design §6, Phase 22 performs NO per-comment
adjudication. 22-04 produced the census + preservation diff + `22-COMMENT-HANDOFF.md` handoff;
the per-comment basis classification + disposition is FUT-05 work.

**Gaps:** GAP-22-01, GAP-22-02, GAP-22-03 — all `RESOLVED-WITH-INSTRUCTION` (see `22-GAPS.md`).
No OPEN STOP gaps remain.

**VER-05 Verdict:** PASS. All Phase-22 findings are VERIFIED or user-DEFERRED; no OPEN
STOP gaps block closure.

---

## Final gate status

| Gate | Status | Evidence |
|------|--------|----------|
| G1 (selftest) | PASS | This file §G1 — exit 0, regression reproduced, negative controls clean |
| G2 (all 3 specs 0-residual) | PASS | This file §G2 — `--all` exit 0, 0 DEFINITE + 0 REVIEW |
| G3 (content preservation) | PASS | This file §G3 — every hunk classified, 0 comments lost/changed |
| G3 (comments) | PASS | 22-COMMENT-DIFF.md + 22-COMMENT-HANDOFF.md |
| G4 (automated proxy) | PASS | G1 + G2 + G3 combined |
| G4 (visual backstop) | APPROVED 2026-06-09 | User-facing checklist; no defects reported |
| VER-05 (ledger) | PASS | 16-ISSUE-LEDGER.md Phase 22 addendum |
