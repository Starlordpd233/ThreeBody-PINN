# Framework-Spec Cleanup — Design Spec

- **Phase:** 22 — final phase of milestone v1.4
- **Date:** 2026-06-07
- **Status:** Design approved; Phase 22 added to the roadmap in commit `2436b51`; phase planning pending
- **Targets:** `pinn_instruction/markdown_conversion/framework-specs/{ctl_instruction.md, pinn_architecture.md, sampling_method.md}`
- **Target renderer (definition of "correct"):** VS Code / Cursor markdown preview (KaTeX math engine)

---

## 1. Problem & Goal

The three core framework-spec markdown files render with visibly broken syntax in the Cursor preview. The breakage is concentrated in `pinn_architecture.md` and `ctl_instruction.md`; `sampling_method.md` is structurally clean. The author has annotated many defect sites in-file with `Author Comment:` / `Author note:` markers.

Investigation showed every rendering break reduces to **one meta-defect: content that should be math is not in a working KaTeX math context** — because delimiters are missing, delimiters are malformed, the math is wrapped in backticks, or it is trapped inside a structure (a Pandoc table) that itself does not render.

**Goal:** All three files render correctly in Cursor preview, with all math normalized to a single render-correct representation, and with stale/obsolete author comments dispositioned — **without changing the mathematical or prose meaning of any content, and without the agent making semantic deletions autonomously.**

This is the finishing phase: it runs **after** Phases 20.5 and 21 so it catches any rendering breakage those phases introduce and the milestone closes on clean-rendering specs.

## 2. Scope

**In scope**
- WS-A: Repair all rendering-breaking markdown/LaTeX so the three files render correctly in Cursor; normalize all math to LaTeX `$…$`/`$$…$$`.
- WS-B: Evaluate every author comment; disposition (keep / remove / revise / resurface) under human adjudication.

**Out of scope (non-goals)**
- Any change to the **meaning** of math or prose. Conversions are equivalence-preserving only.
- Any **content** update to resolve a flagged inconsistency (e.g., the SI-PINN-002 batch-construction issue, or the "outdated code folder" reference in `ctl_instruction.md`). These are surfaced, not fixed here.
- Editing `pinn/` implementation files (forbidden in v1.4).
- Touching **normative** spec notes (FRAME-xx notes, "Loss Integration Note", "Critical Update", anti-pattern callouts).

## 3. Locked decisions

| # | Decision | Value |
|---|----------|-------|
| D1 | Target renderer | VS Code / Cursor preview (KaTeX) |
| D2 | Phase placement | New final phase **22**, after Phase 21 |
| D3 | Base scope | Rendering-breakage only — presentation-preserving |
| D4 | Comment-deletion authority | **Human-adjudicated**; grounded-stale syntax-flags batch-confirmable |
| D5 | "Historical … retained as non-normative" notes | **Case-by-case with evidence** (treat the retention marker as EXPLICIT-RETENTION) |
| D6 | Editorial vs normative | **Never touch normative**; surface ambiguous for an editorial-vs-normative ruling |
| D7 | Math representation standard | **LaTeX `$…$`/`$$`** everywhere; convert backtick/prose ASCII-math with verified equivalence; **remove redundant plaintext fallbacks per-instance on confirmation** |
| D8 | Trailing-`\` Pandoc hard-breaks | **Remove where they are conversion noise, confirm each** (renders as `<br>`, so removal is a minor layout change) |

All semantic / process decisions above were surfaced under the v1.4 STOP-protocol governance rather than chosen by the agent.

## 4. Defect taxonomy

| Class | Tier | Detected by | Example |
|-------|------|-------------|---------|
| Pandoc fenced div `::: {…}` | DEFINITE | survivor scan | `pinn` table wrapper |
| Pandoc multiline table | DEFINITE | survivor scan | hyperparameter / blueprint tables |
| Pandoc caption `: Table …` | DEFINITE | survivor scan | table captions |
| Surviving `$$` / `\command` in text | DEFINITE | survivor scan | `$$\begin{aligned}` opened mid-list-item |
| Footnotes `[^n]` (no built-in support) | verify-target | survivor scan | `[^1]…[^15]` |
| Bare multi-char sub/superscript | REVIEW | LaTeX lint | `L_total`, `L_data`, `L_phys^causal` |
| Operator missing backslash | REVIEW | LaTeX lint | `min(`, `sin(`, `epsilon_H` |
| KaTeX hard parse error | DEFINITE | KaTeX `throwOnError` | (none currently, but guards the corpus) |
| **Backtick-wrapped ASCII math** | REVIEW (oracle-guided) | backtick-math scan | `` `E_scale = |median({E_j})| + 1e-10` `` |
| **Raw-prose ASCII math** | REVIEW (oracle-guided) | prose-math scan | `c_E = RMS_n(ΔH_n)`, `c_{L,α} = RMS_n(...)` |
| `\text{}` / superscript literal (broken table / missing `$`) | partial | survivor + oracle | weight-init fields |
| Redundant math+plaintext duplication | per-instance | author comment | `$…10^{-5}$ (`10^-5`)` |
| Trailing-`\` Pandoc hard-break noise | per-instance | author comment | `stage.yaml … \` |

`sampling_method.md` currently yields **0** automated findings.

## 5. WS-A — Math / rendering normalization

### 5.1 The detector (`detect.mjs`) — validated

Engine: **`markdown-it` + `@vscode/markdown-it-katex`** (Cursor's actual math plugin) — maximal fidelity to the target renderer. A **sanity gate** asserts valid math is consumed (MathML annotation stripped) before any run; the script aborts if the plugin fails to load.

Layers:
- **D1 — KaTeX `throwOnError`**: hard math parse errors → DEFINITE.
- **D2 — KaTeX `strict` warnings**: suspicious math → REVIEW.
- **D3 — LaTeX lint** (token-tree aware; code spans/fences excluded):
  - bare multi-char sub/sup: `(?<!\\)[_^](?!\{)[A-Za-z]{2,}` (letters-only, no backslash, no digit-lead — excludes `H_\epsilon`, `m_1r_1`).
  - operator missing backslash: always-commands (`\frac`, greek, …) word-boundary, not in label position; functions (`min`/`sin`/…) only in call form `fn(` (excludes `t_{max}` labels).
  - brace balance within a span.
- **D4 — render-structure survivor scan** (complete-by-construction): render with the real engine; flag any control-markup that survives into visible text (`$$`, `\command`, `:::`, `[^n]`, `{.attr}`) and any Pandoc table/caption/div. This catches unknown-unknowns because it enumerates "markup that must never appear literally," not a fixed defect list.
- **D5 — backtick-math scan** *(new, oracle-guided, REVIEW)*: scan inline code spans for ASCII-math signatures (`_`, `^`, `=`, `\cmd`, `sqrt`, `sum`, `||…||`, `1e-±n`) to distinguish backtick-wrapped math from legitimate code/filenames. Noisy → human-reviewed.
- **D6 — prose-math scan** *(new, oracle-guided, REVIEW)*: scan prose (outside code/math) for ASCII-math signatures (subscript patterns, `{…}`, operator words, fraction slashes). Noisy → human-reviewed.

Precision rules learned during validation (all baked in): exclude escaped `\_`/`\^`; trailing-`\` renders `<br>` (not a rendering defect — handled under D8); code spans excluded from D3/D4 but explicitly scanned by D5.

### 5.2 Recall model — three independent sources

The detector is strong on survivor/structural/lint classes but **weak and noisy on prose-math and backtick-math** (prose contains `=`; filenames contain `_`). Recall is therefore not the detector alone:

> **Recall = automated detector (survivor/structural/lint) ∪ author comments as ground-truth oracle (prose/backtick math) ∪ human render-review backstop.**

"**Resolve every author-flagged region**" is a first-class success requirement. The author comments double as a labeled **regression set**: the detector run must reproduce them (and must not flag the negative-control semantic comment).

### 5.3 Fix classes & equivalence verification

- Delimiter/structure repairs (move `$$` to own line, GFM-table conversion preserving every cell byte-for-byte, escape literal `$`): mechanical, presentation-only.
- Bare sub/sup and missing-backslash repairs: grounded by the author's own canonical text forms where present.
- **Math normalization (D7)**: convert backtick/prose ASCII-math → LaTeX `$…$`. Each conversion is **equivalence-verified** (rendered meaning identical to the ASCII source). Ambiguous transcriptions (e.g., is `RMS` an operator? is `c_{L,α}` a subscript list?) → **STOP protocol**, surfaced, never invented.
- **Redundant-fallback removal (D7)**: once math renders, the plaintext/backtick duplicates the author flagged ("why duplicate") are removed **per-instance on confirmation**.
- **Hard-break cleanup (D8)**: remove trailing-`\` where it is conversion noise, **per-instance on confirmation**.

### 5.4 WS-A gates
1. Detector reproduces the author-flag regression set; negative control stays clean.
2. Zero residual findings across all three files under all detector layers.
3. **Content-preservation audit**: every changed line differs only in delimiters / structure / whitespace / representation — no math or prose meaning altered.
4. Full HTML render + human eyeball in Cursor.

## 6. WS-B — Comment & fallback disposition

### 6.1 The disposition engine — validated

Per candidate editorial comment:
1. **Detect** — author markers (`Author Comment`, `Author note`, `\authcomment`, `Historical author note`), plus `**[…]**` only when it carries an author marker. Fence-excluded.
2. **Classify intent** *(on the comment's own text, not neighbor lines — bug-fixed)*: `syntax-flag` / `inconsistency-flag` / `todo-gap` / `open-question` / `suggestion` / `retained-historical` / `meta-doc` / `normative(out-of-scope)`.
3. **Temporal grounding (git)** — when the comment was introduced; whether a v1.4 phase revised its referent afterward (factual evidence of "framework made it outdated").
4. **Referent-state check** — for syntax-flags, cross-reference the WS-A detector: does it still flag the referent? (Post-fix: no → addressed.)
5. **Basis class** → disposition:

| Basis | Disposition |
|-------|-------------|
| GROUNDED-STALE (referent provably fixed/resolved) | **REMOVE** (confirm; bundle into the fix commit) |
| RECALL-GAP (backtick/prose math the scanner misses) | verify region → convert (WS-A) → then GROUNDED-STALE → REMOVE (confirm) |
| GROUNDED-LIVE / JUDGMENT-REQUIRED | **SURFACE** — you decide |
| EXPLICIT-RETENTION ("retained as non-normative") | **SURFACE per-note** (case-by-case, D5) |
| META-DOC (SI-PINN-002 documents the comments) | **KEEP + co-update** if it describes removed comments |
| OUT-OF-SCOPE (normative spec note) | **KEEP** untouched |

### 6.2 Governance / safety
- **Default is SURFACE.** Any misclassification fails safe to human review — never a silent deletion.
- Deletions on a "no longer reasonable" basis are **never autonomous** (per v1.4 STOP protocol). The engine produces evidence + a recommendation; the user adjudicates.
- Unresolved semantic dispositions → logged as STOP-protocol gaps in the phase gap register. **The phase cannot close on an OPEN gap unless the user defers it.**
- Content-staleness comments (e.g., "the statement itself is outdated") flag stale *content*, not just a stale comment → surfaced for the user; the content itself is not edited in this phase.

## 7. Coupling between WS-A and WS-B

The workstreams are coupled but gated separately (mechanical risk must not contaminate semantic work):
- WS-A verifiably fixes what a syntax-flag comment points at → that comment becomes GROUNDED-STALE → its removal bundles into the same atomic fix commit (user-confirmed).
- WS-A's author-comment oracle (recall) depends on WS-B's census; WS-B's grounded-stale verdicts depend on WS-A's detector. The phase runs the census + detector together at execution time against **live** file state.

## 8. Validation evidence (what was actually tested)

Both engines were taken through build → test → find-real-bug → fix → re-validate against the live files:

- **WS-A detector** — 4 test-driven fixes: (1) silent plugin-load failure (`@vscode/markdown-it-katex` double-wrapped export) that had flagged all valid math; (2) false positives `H_\epsilon` / `m_1r_1` / `t_{max}`; (3) trailing-`\` proven to render `<br>` (excluded); (4) escaped `\_` false positives. Result on the author ground-truth set: **all flags reproduced, negative control clean, ~0 residual false positives.** It surfaced far more than the hand-flags (e.g., the `L_total`/`L_data` subscript bug recurs ~13×; 3 Pandoc tables vs the 1 hand-flagged; the `$$\begin{aligned}` mid-list breakage).
- **WS-B disposition engine** — 1 dangerous bug fixed: neighbor-line contamination that mislabeled the SI-PINN-002 inconsistency comment as normative→KEEP. After fix it classifies correctly and fails safe to SURFACE.
- **Recall-gap discovery** — the author's added comments exposed classes the detector misses by design (backtick-math, raw-prose math, `\text{}`-literal), which drove the D5/D6 layers and the three-source recall model.

> Line numbers drift as the files are edited; this spec encodes **algorithms and classes, never hardcoded line numbers.** Both engines re-derive against live state at execution.

## 9. Success criteria
1. Detector passes the author-flag regression set; negative control stays clean.
2. Every author-flagged region is resolved.
3. Zero residual rendering defects across all three files (detector + Cursor render-review).
4. All math normalized to LaTeX `$…$`/`$$`; every conversion equivalence-verified.
5. Content-preservation audit passes — no math or prose meaning changed without grounding + confirmation.
6. Every author comment dispositioned with a recorded basis and your adjudication; redundant fallbacks and hard-breaks confirmed per-instance.
7. No semantic change or deletion without grounding or your confirmation; unresolved items logged as STOP gaps; the phase does not close on an OPEN gap unless you defer it.

## 10. Risks & mitigations
- **Equivalence drift during math conversion** → per-conversion equivalence check + content-preservation audit; ambiguous → STOP.
- **Over-deletion of meaningful comments** → human adjudication + SURFACE default + EXPLICIT-RETENTION handling.
- **Detector precision on D5/D6** → REVIEW-tier + author-comment oracle as primary recall; human review.
- **Footnote rendering assumption** → Stage-0 verifies `[^n]` behavior against the actual Cursor target before classifying.
- **Files edited mid-phase** → engines re-run against live state; no hardcoded line numbers.

## 11. Tooling / prerequisites
- Node ≥ 24 (present), `markdown-it`, `@vscode/markdown-it-katex`, `katex` (validated in a throwaway env; the phase formalizes the detector as a committed script).
- Git history access for WS-B temporal grounding.

## 12. Out of scope / future
- Resolving flagged content inconsistencies (SI-PINN-002; IC-dimension reconciliation note; outdated code-folder references) — these remain open issues for their owning tracks / FUT-01.

---

### Appendix — engine prototypes (validated)
- WS-A detector prototype: `detect.mjs` (markdown-it + @vscode/markdown-it-katex; layers D1–D4 implemented and validated; D5/D6 specified for the phase).
- WS-B disposition prototype: intent + basis classifier with WS-A cross-reference (validated; 25 candidates across the two non-clean files).
- Author-flag ground-truth / regression set: the in-file `Author Comment:` / `Author note:` markers (re-derived at execution).
