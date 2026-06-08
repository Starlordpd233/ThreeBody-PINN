# Phase 22: Framework-Spec Cleanup - Research

**Researched:** 2026-06-08
**Domain:** Markdown/KaTeX rendering normalization + author-comment census (documentation tooling, Node ESM)
**Confidence:** HIGH (design doc is validated; live state re-verified this session)

## Summary

This is a CONSOLIDATION + LIVE-STATE-VERIFICATION research pass. A fully validated design doc
(`docs/work/designs/milestone_v1.4/framework-spec-cleanup/2026-06-07-framework-spec-cleanup-design.md`,
hereafter "the design") already specifies the approach: build a Node detector (`detect.mjs`) using
`markdown-it` + `@vscode/markdown-it-katex` + `katex` matching Cursor/VS Code's KaTeX engine, run a
6-layer (D1–D6) scan, repair every rendering-breaking construct so all three framework specs render
correctly, and census-and-preserve every author comment for FUT-05. The detector prototype was taken
through build→test→fix→re-validate and is plan-ready; it does not yet exist as a committed file.

Phase 22 has two workstreams. **WS-A (math/rendering):** repair all rendering breakage, normalize math
to LaTeX `$…$`/`$$…$$`, equivalence-verify each conversion, surface ambiguous transcriptions under STOP.
**WS-B (author comments) — REDUCED to preserve-and-defer:** census EVERY author comment in any form,
preserve verbatim, mechanically repair only render-breaking wrappers, and produce `22-COMMENT-HANDOFF.md`.
Per GAP-22-01 (RESOLVED → Defer) the design's §6 disposition/adjudication engine (basis classes,
git temporal grounding) is **FUT-05 work, OUT of Phase 22 scope**; Phase 22 keeps only §6.1's
detection/census step and the preservation guarantee.

Live-state re-verification (this session) **confirms the GAP-22-02 resolution**: 26 author-marker lines
(13 ctl + 13 pinn + 0 sampling), the "28 `\authcomment`" figure is retired, and the lone literal
`\authcomment{}` token appears only inside the SI-PINN-002 meta-doc (the negative control). It also
confirms the design's recurrence observations: the `L_*` bare-subscript bug recurs far more than the
hand-flags, and there are 3 Pandoc multiline tables in `pinn_architecture.md` (only 1 hand-flagged).

**Primary recommendation:** Plan WS-A and WS-B as separately-gated workstreams sharing one committed
`detect.mjs` + a scoped `package.json`/lockfile. Bake in the precision exclusions and the plugin-load
sanity gate as first-class detector requirements. Re-derive all counts/locations against live state at
execution — no hardcoded line numbers.

<phase_requirements>
## Phase Requirements

Phase-22-specific REQ IDs are TBD (per `.planning/REQUIREMENTS.md` line 139). The following
cross-cutting and future requirements are addressable and MUST be kept so:

| ID | Description | Research Support |
|----|-------------|------------------|
| VER-05 | Iterative re-verification ledger: each finding tracked PENDING→IN_PROGRESS→FIX_APPLIED→VERIFIED; re-run on regression candidates after each batch; nothing closes until all in-scope findings VERIFIED or DEFERRED | The detector (G2 zero-residual) IS the re-verification mechanism for WS-A: after each fix batch, re-run `detect.mjs` over all 3 files; any new/regressed finding reverts the affected item to IN_PROGRESS. Ledger lives at `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` (stable path); Phase 22 appends. |
| FUT-05 | Adjudicate the author comments Phase 22 preserves; consumes `22-COMMENT-HANDOFF.md`; per-comment basis classification + disposition under human adjudication per design §6 | Phase 22 produces the census + verbatim-preservation + `22-COMMENT-HANDOFF.md` handoff that FUT-05 consumes. Phase 22 performs NONE of the §6 adjudication. |
</phase_requirements>

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** Normalize all intended math into valid KaTeX math contexts where rendering is currently broken. Single-dollar `$` for inline, double-dollar `$$` for block.
- **D-02:** Preserve already-correct notation, environments, spacing, and layout. No cosmetic repository-wide restyling.
- **D-03:** Equivalence-check each conversion and surface ambiguous cases under the STOP protocol.
- **D-04:** Preserve and defer **all author-flagged comments in any form or format** — `Author Comment:` / `Author note:` / `Historical author note:` prose markers, the `\authcomment` macro, and any other author-comment form discovered — carefully enumerated at execution. (The "28 `\authcomment`" figure was a mis-census; live corpus ~26 author-marker lines across ctl + pinn, 1 literal `\authcomment` token (in the meta-doc); sampling is clean. GAP-22-02 resolved.) Keep every comment's substantive text in place; do not delete, extract, resolve, rewrite as ordinary prose, or reclassify during Phase 22.
- **D-05:** If a comment wrapper itself prevents correct Markdown rendering, convert only the wrapper mechanically into a render-safe author-comment format while preserving text, meaning, and location. Do not assess or alter the substance.
- **D-06:** Verify **every** enumerated author-flagged comment remains present and none lost or semantically changed. Produce `.planning/phases/22-framework-spec-cleanup/22-COMMENT-HANDOFF.md` (each comment: form, file, location, verbatim text, preservation-verified flag); register individual review/adjudication under **FUT-05**. (GAP-22-01 resolved → Defer.)
- **D-07:** Use both automated validation and manual visual review. Do not rely on only one method.
- **D-08:** Automated validation: create and commit a Node detector using `markdown-it`, `@vscode/markdown-it-katex`, `katex` matching the Cursor/VS Code KaTeX engine. Report parse errors (throwOnError), strict-mode warnings, unbalanced delimiters, raw LaTeX, math-like backtick fragments, broken Markdown structures. Must pass known author-flagged regression fixtures, keep a known-clean negative control free of findings, finish with zero unresolved rendering findings across all three files, and verify all enumerated author comments remain present.
- **D-09:** Manual visual review: open all three complete specs in the actual Cursor/VS Code Markdown Preview and inspect fully. Check every edited equation and its surroundings. Confirm no raw LaTeX, clipped math, broken layouts, accidental code formatting, or missing content.
- **D-10:** Record the exact detector command and output plus a per-file visual-review checklist. Render correctness established only when both automated detector and manual review pass.

### Claude's Discretion
None — all presentation and verification decisions strictly defined.

### Deferred Ideas (OUT OF SCOPE)
- **Adjudication of author comments** — individual review and resolution of all author-flagged comments (any form/format) is explicitly deferred to **FUT-05** (a dedicated post-v1.4 phase) consuming `22-COMMENT-HANDOFF.md`. Phase 22 only mechanically repairs wrappers if they break Markdown rendering.
- Design §6 disposition engine (basis classes GROUNDED-STALE/SURFACE/KEEP, git temporal grounding) describes FUT-05, NOT Phase 22.
- Resolving flagged content inconsistencies (SI-PINN-002 batch construction, IC-dimension reconciliation, outdated code-folder reference) — owned by their tracks / FUT-01.
</user_constraints>

## Project Constraints (from CLAUDE.md / AGENTS.md)

- **v1.4 STOP protocol:** do NOT invent semantic content where sources are silent. Ambiguous math
  transcriptions are surfaced as findings to the orchestrator, never resolved autonomously. The
  executor returns findings; only the parent agent writes the gap register.
- **No-live-code directive:** `pinn/` is NOT a grounding source. The three framework specs + the design
  doc + CONTEXT.md are authoritative. (Phase 22 edits the specs themselves; it does not read `pinn/`.)
- **Git commit protocol:** use `scripts/agent-commit` (not raw `git commit`); never `--no-verify`
  without approval. Commit message `<type>(<scope>): <subject>`; allowed types include `fix`, `chore`,
  `feat`, `verify`, `docs`; scope `22` or `22-NN`. Body required for multi-file commits and commits
  touching `pinn_instruction/` or `.planning/`. Agent-authored commits need an `Agent-Assisted-By:` or
  `Co-Authored-By:` trailer. Run `scripts/setup-git-hooks.sh` if hooks path isn't `.githooks`.
- **Atomic commits:** WS-A fix that resolves a syntax-flag comment's referent may bundle the (deferred)
  comment's wrapper-repair into the same atomic commit — but NO comment deletion in Phase 22.
- **Commit cadence:** commit at logical task boundaries; specs under `pinn_instruction/` → one atomic
  commit at task end.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Render-defect detection | Build/CI tool (`detect.mjs`, Node ESM) | — | Must mirror the Cursor KaTeX engine; lives as a committed script run against the 3 specs |
| Math normalization (the edits) | Documentation content (the 3 `.md` specs) | Detector (verifies) | The repair is a content edit; the detector is the oracle that gates it |
| Author-comment census | Build/CI tool (census pass, can share `detect.mjs`) | Handoff doc | Deterministic enumeration → `22-COMMENT-HANDOFF.md` |
| Preservation verification | Build/CI tool (before/after diff) | Manual review | Proves 0 lost / 0 semantically changed |
| Manual render review | Human in Cursor/VS Code preview | — | Backstop for what the detector cannot judge (visual layout, prose-math recall) |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Node.js | ≥ 24 (local: v24.16.0 [VERIFIED: `node --version`]) | ESM runtime for `detect.mjs` | Design §11 pins ≥24; present locally |
| `markdown-it` | latest 14.x [ASSUMED — pin at install] | Markdown→HTML parser; same family VS Code uses | Cursor/VS Code markdown preview is markdown-it based |
| `@vscode/markdown-it-katex` | latest [ASSUMED — pin at install] | The math plugin VS Code/Cursor actually uses | Maximal fidelity to target renderer (design §5.1) |
| `katex` | latest 0.16.x [ASSUMED — pin at install] | Math engine (throwOnError, strict) used by D1/D2 | The engine whose pass/fail defines "renders correctly" |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| (none required) | — | — | Pure stdlib (`fs`, `node:test` optional) suffices for layers, census, diff |

**Installation (scoped tools dir — recommended):**
```bash
# Recommended: a scoped tools dir with committed package.json + lockfile, NOT repo root
mkdir -p tools/spec-render-check
cd tools/spec-render-check
npm init -y
npm install --save-exact markdown-it @vscode/markdown-it-katex katex
# Commit package.json + package-lock.json (lockfile pins exact versions → CI-reproducible)
```

**Version verification:** Run `npm view <pkg> version` at install time and record the resolved version
in `package-lock.json`. Training-data versions are stale — confirm against the npm registry, then
`--save-exact` to pin. The three packages are the design-mandated, validated stack; do not substitute.

**Where the detector lives (planner decision, recommended):** `tools/spec-render-check/detect.mjs`
with its own `package.json` + lockfile + a short README. Rationale: keeps a Node/JS toolchain out of
the Python-centric repo root, makes the CI invocation self-contained, and isolates `node_modules`.
Add `tools/spec-render-check/node_modules/` to `.gitignore`. The script takes the 3 spec paths as
argv (or defaults to the `framework-specs/` glob), exits non-zero on any finding, and prints a
deterministic per-file/per-layer report (CI-runnable).

## Package Legitimacy Audit

> slopcheck/pip were not run in this session (research-only environment). All three packages are the
> design-mandated, prototype-validated stack and are widely-used VS Code ecosystem packages, but per
> the package-provenance rule they are tagged `[ASSUMED]` until verified at install.

| Package | Registry | Age | Downloads | Source Repo | slopcheck | Disposition |
|---------|----------|-----|-----------|-------------|-----------|-------------|
| `markdown-it` | npm | mature (years) | very high | github.com/markdown-it/markdown-it | not run | Approved at install after `npm view` + lockfile pin |
| `@vscode/markdown-it-katex` | npm | mature | high (VS Code ecosystem) | github.com/microsoft/vscode-markdown-it-katex | not run | Approved at install; **known double-wrapped export landmine — see Pitfall 1** |
| `katex` | npm | mature (years) | very high | github.com/KaTeX/KaTeX | not run | Approved at install after `npm view` + lockfile pin |

**Packages removed due to slopcheck [SLOP] verdict:** none
**Packages flagged [SUS]:** none

*Planner action:* gate the single `npm install` behind a `checkpoint:human-verify` task (or run
`npm view <pkg>` + slopcheck at install) since slopcheck did not run at research time. Then pin via
lockfile so the verification is one-time.

## Architecture Patterns

### System Architecture Diagram

```
                    3 spec .md files (live state)
                  ctl / pinn / sampling
                            │
                            ▼
     ┌──────────────────────────────────────────────┐
     │  detect.mjs  (Node ESM, scoped tools dir)     │
     │                                               │
     │  [SANITY GATE] load markdown-it + plugin;     │
     │   render a known-good $x^2$; assert KaTeX     │
     │   MathML/HTML produced → ELSE abort(2)        │  ◄─ Pitfall 1 guard
     │                                               │
     │   D1 KaTeX throwOnError ──► DEFINITE          │
     │   D2 KaTeX strict       ──► REVIEW            │
     │   D3 LaTeX lint (token-aware, exclusions) ──► REVIEW
     │   D4 survivor scan (render → leftover markup)──► DEFINITE (complete-by-construction)
     │   D5 backtick-math scan (oracle-guided) ──► REVIEW
     │   D6 prose-math scan   (oracle-guided) ──► REVIEW
     │                                               │
     │   + author-comment CENSUS pass (any form)     │
     └──────────────────────────────────────────────┘
                            │
              ┌─────────────┴──────────────┐
              ▼                             ▼
   per-file/per-layer findings      author-comment inventory
   (exit≠0 if any residual)                 │
              │                             ▼
              ▼                    22-COMMENT-HANDOFF.md  (→ FUT-05)
   WS-A repair edits (equivalence-verified)
              │
              ▼
   re-run detect.mjs  ─► G2 zero residual ─► manual Cursor review (D-09)
```

Recall is NOT the detector alone (design §5.2):
**Recall = detector (survivor/structural/lint) ∪ author comments as ground-truth oracle (prose/backtick math) ∪ human render-review backstop.**

### Recommended Project Structure
```
tools/spec-render-check/
├── package.json          # pins markdown-it, @vscode/markdown-it-katex, katex (--save-exact)
├── package-lock.json     # committed; CI-reproducible
├── detect.mjs            # 6 layers + sanity gate + census pass
└── README.md             # exact run command + interpretation (feeds D-10)
.planning/phases/22-framework-spec-cleanup/
└── 22-COMMENT-HANDOFF.md # census output → FUT-05
```

### Pattern 1: Sanity gate before any layer runs
**What:** On startup, render a trivially-valid expression (e.g. `$x^2$`) and assert the KaTeX plugin
actually consumed it (MathML annotation / katex HTML present). Abort (non-zero) if not.
**When to use:** Always, first thing — guards against the silent plugin-load failure (Pitfall 1).
**Source:** design §5.1 ("A sanity gate asserts valid math is consumed … the script aborts if the plugin fails to load").

### Pattern 2: D4 survivor scan = complete-by-construction
**What:** Render with the real engine, then scan the *rendered visible text* for control-markup that
must never survive: literal `$$`, `\command`, `:::`, `[^n]`, `{.attr}`, Pandoc multiline-table rows,
`: Table …` captions. Enumerates "markup that must never appear literally," not a fixed defect list —
so it catches unknown-unknowns.
**Source:** design §5.1 D4.

### Pattern 3: Line-number independence
**What:** Every layer + census re-derives positions against live file bytes at execution. Report by
section/anchor + matched snippet, never by hardcoded line number (lines drift during edits).
**Source:** design §8, §10.

### Anti-Patterns to Avoid
- **Hardcoding line numbers** in the detector or plan tasks — files are edited mid-phase; positions drift.
- **Trusting `npx --yes`** to fetch the toolchain — install explicitly + pin via lockfile (security + reproducibility).
- **Treating D5/D6 raw output as defects** — they are REVIEW-tier and noisy by design (prose has `=`, filenames have `_`); the author-comment oracle + human review drive recall, not raw D5/D6 hits.
- **Adjudicating/removing any author comment in Phase 22** — that is FUT-05.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Deciding "does this math render in Cursor?" | A regex math validator | `katex` throwOnError/strict via `@vscode/markdown-it-katex` | Only the real engine matches the target renderer; regex misses real KaTeX semantics |
| Markdown parsing / structure | A custom MD tokenizer | `markdown-it` (+ render to detect survivors) | Cursor/VS Code IS markdown-it; fidelity is the whole point |
| Detecting leftover control markup | A fixed defect list | D4 render-survivor scan | Complete-by-construction; catches unknown-unknowns |

**Key insight:** "Renders correctly in Cursor" is only verifiable by running Cursor's actual engine
(`markdown-it` + `@vscode/markdown-it-katex` + `katex`). Any hand-rolled approximation diverges from
the target and produces false confidence.

## Runtime State Inventory

> Phase 22 edits documentation files only; there is no stored data, live service config, OS-registered
> state, or secrets involved. The only "build artifact" is the new tool's `node_modules`.

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data | None — verified: phase touches 3 `.md` files + 1 handoff doc only | — |
| Live service config | None — no external service references this work | — |
| OS-registered state | None — no scheduled tasks / daemons | — |
| Secrets/env vars | None — verified: no secrets in scope | — |
| Build artifacts | `tools/spec-render-check/node_modules/` (gitignore); committed lockfile is the only persisted artifact | gitignore `node_modules`, commit lockfile |

## Live Defect Map (verified against current files, 2026-06-08)

> Re-derived this session. By section/anchor, NOT line number (lines drift). The detector re-derives
> exact positions at execution.

### `ctl_instruction.md` (1448 lines; 27 `$$` tokens)
Defect classes present (design §4 taxonomy):
- **Surviving `$$\begin{aligned}` opened mid-list-item (DEFINITE, D4):** in the IC-derivation list
  (around the "Total energy E, virial ratio Q, minimal separation s_min" item and ≥2 more list-item
  derivations), a `$$\begin{aligned}` is appended to the same line as bold list text
  (`…**$s_{\min}$.** $$\begin{aligned}`). markdown-it won't treat `$$` mid-paragraph as a block →
  block math leaks as literal text. **3 such `$$\begin{aligned}` sites** in this file.
- **Bare multi-char sub/superscript (REVIEW, D3):** `L_*` family (`L_total`, `L_data`, `L_phys`, etc.)
  recurs ~8 raw occurrences here — more than the hand-flags. Plus other bare subscripts.
- **Backtick / prose ASCII-math (REVIEW, D5/D6, oracle-guided):** several backtick fragments mixing
  math and code (e.g. the rejected-ALM formula `` `L_data + λ_p·L_phys + (μ_p/2)·L_phys² + λ_E(k)·L_energy` ``);
  these need human/oracle distinction from genuine code/filenames.
- **Redundant math+plaintext duplication (per-instance):** author-flagged "why duplicate" sites.
- **Trailing-`\` hard-break (per-instance, D8):** 1 line. Renders `<br>` → layout-noise, confirm per-instance, NOT a parse defect.
- Pandoc fenced divs `:::`: **0**. Footnotes: **0**. `\authcomment` macro: **0**.

### `pinn_architecture.md` (1034 lines; 33 `$$` tokens)
Defect classes present:
- **Pandoc multiline tables (DEFINITE, D4): 3 tables**, not the 1 hand-flagged — separator rows at
  the architectural-hyperparameters table (inside a `::: {#tab:…}` fenced div, with `: Table 1:`
  caption) and the Consolidated Implementation Blueprint table (bare multiline table + `: Table 2:`
  caption, spanning two separator-row segments). These Pandoc constructs do NOT render in
  markdown-it/Cursor → must be converted to GFM pipe tables preserving every cell byte-for-byte.
- **Pandoc fenced div `:::` (DEFINITE, D4): 2** (`::: {#tab:architectural_hyperparameters}` … `:::`).
- **Pandoc caption `: Table …` (DEFINITE, D4): 2** (`: Table 1:`, `: Table 2:`).
- **Footnotes `[^n]` (verify-target, D4): 37 references, 17 definitions.** markdown-it footnote support
  is NOT enabled by default. Stage-0 MUST verify how Cursor renders `[^n]` against the actual target
  (design §10 footnote-rendering mitigation) BEFORE classifying these as defects. If Cursor renders
  them, they are fine; if not, they are survivors.
- **Bare multi-char sub/superscript (REVIEW, D3):** `L_*` family recurs ~22 raw occurrences here —
  the dominant recurring class, far above the hand-flags.
- **Backtick / prose ASCII-math (REVIEW, D5/D6):** e.g. `` `H_ε` ``, `` `epsilon_H = 1e-4 * S_H` `` in the blueprint table cells; `c_E = RMS_n(ΔH_n)`, `c_{L,α} = RMS_n(...)` prose forms (design-flagged AMBIGUOUS — STOP candidates).
- **Trailing-`\` hard-break (per-instance, D8):** 2 lines.
- **`\authcomment` literal token: 1**, but it is INSIDE the SI-PINN-002 meta-doc (negative control), NOT a defect — see WS-B below.

### `sampling_method.md` (281 lines; 12 `$$` tokens)
- **CONFIRMED CLEAN — 0 author markers, 0 fenced divs, 0 Pandoc grid-table rows, 0 footnotes.**
- Note: it uses Pandoc **definition lists** (`` `epsilon` `` followed by `:   text`). The design declares
  this file 0-findings, so the detector's negative-control expectation is that these definition-list
  lines do NOT produce findings. The detector/plan MUST NOT flag `:   ` definition-list continuations
  as Pandoc captions. (The 3 `: ` lines here are definition-list bodies, not `: Table` captions.)
- This file is a **negative control for D4**: any finding here is a false positive to be fixed in the detector.

## WS-B — All-Forms Author-Comment Census + Preservation

### Census basis (canonical, per GAP-22-02 resolution)
Marker set = **every author-flagged comment in any form/format**: `Author Comment` / `Author note` /
`Historical author note` / `\authcomment`, **plus any other author-comment form discovered at execution**.
Case-insensitive; fence-excluded for the prose markers; the `\authcomment` macro matched literally.

### Verified live census (re-derive at execution; this is the expected baseline)
| File | Author-marker lines | Forms observed | `\authcomment` literal |
|------|--------------------|----------------|------------------------|
| `ctl_instruction.md` | **13** | `Author Comment`, `Author note`, `Historical author note` | 0 |
| `pinn_architecture.md` | **13** | `Author Comment` (incl. preserved `**[...]**` notes) | 1 (meta-doc only) |
| `sampling_method.md` | **0** | — | 0 |
| **Union** | **26 marker lines** | — | **1** (negative control) |

The single literal `\authcomment{}` token is inside the **SI-PINN-002 meta-doc** in
`pinn_architecture.md` — a section that *documents* that 3 author comments were preserved as
`**[...]**`. This meta-doc is the **negative control**: it must be enumerated/understood but must NOT
be treated as a render defect, and the 3 `**[...]**` preserved notes it references ARE author comments
to census. (The "28 `\authcomment`" figure is retired.)

### Census method (deterministic)
1. A census pass (can share `detect.mjs` or be a sibling script) scans each file, fence-excluded for
   prose markers, for the marker set; emits `{form, file, section/anchor, matched-snippet, verbatim-text}`.
2. Treat `**[...]**` bracketed bold notes as author comments **only when** they carry/derive-from an
   author marker (design §6.1 step 1) — e.g. the 3 SI-PINN-002 notes.
3. Emit `22-COMMENT-HANDOFF.md`.

### Preservation check (G3 input)
- Snapshot every enumerated comment's verbatim text **before** any WS-A edit.
- After all edits, re-census and diff: assert **0 lost, 0 semantically changed**. The only permitted
  edit to a comment is a mechanical wrapper repair (D-05) where the wrapper itself breaks Markdown
  rendering, preserving text/meaning/location. (Live state shows no comment wrapper currently breaks
  rendering — `\authcomment` appears only in the meta-doc as inline code — so wrapper repairs are
  expected to be NONE or trivial; re-confirm at execution.)
- Record a before/after census-count + per-comment text-hash comparison in committed state (not `/tmp`).

### `22-COMMENT-HANDOFF.md` schema (for FUT-05)
```
# Phase 22 Author-Comment Handoff (for FUT-05 adjudication)
Census basis: <marker set> | Re-derived at execution: <date>
Total comments: <N>  (ctl: <n1>, pinn: <n2>, sampling: 0)

| # | form | file | section/anchor | verbatim text | preservation-verified |
|---|------|------|----------------|---------------|-----------------------|
| 1 | Author Comment | ctl_instruction.md | <anchor> | "<verbatim>" | ✓ |
| … |
Negative control (NOT a comment to adjudicate, documents the others): SI-PINN-002 meta-doc — noted, excluded from defect findings.
```
**Excluded from Phase 22 (FUT-05 owns):** per-comment basis classification (GROUNDED-STALE / SURFACE /
KEEP), git temporal grounding, any deletion/revision/resurfacing, the design §6 disposition engine.

## Math Equivalence Verification + Content-Preservation Audit

- **Per-conversion equivalence (D-03/D7):** for each backtick/prose ASCII-math → LaTeX conversion,
  render both the ASCII source and the LaTeX result with the same KaTeX engine and confirm identical
  rendered meaning. Mechanical when unambiguous.
- **Content-preservation audit rule (G3):** every changed line differs only in delimiters / structure /
  whitespace / representation — **no math or prose meaning altered.** Enforce as a reviewable invariant
  over the diff.
- **GFM-table conversion:** convert Pandoc multiline tables → GFM pipe tables preserving **every cell
  byte-for-byte** (cell text, footnote refs `[^n]`, inline math `$…$` unchanged). The conversion changes
  table syntax only, never cell content.
- **Escape literal `$`:** where a `$` is a literal dollar (not math), escape `\$` so it doesn't open math.
- **Trailing-`\` (D8):** renders `<br>` → layout-noise, NOT a parse defect; remove only where it is
  conversion noise, confirm each instance.
- **STOP-protocol candidates (design-flagged ambiguous transcriptions):** e.g. *is `RMS` an operator?*
  (in `c_E = RMS_n(ΔH_n)`), *is `c_{L,α}` a subscript list?* The executor MUST surface these as findings
  to the orchestrator under the STOP protocol and MUST NOT invent the transcription. (Per governance,
  the executor returns the finding; the parent agent decides whether to log a gap.)

## Validation Architecture

> nyquist_validation: treated as enabled (not explicitly false in config). The detector IS the
> automated test harness; manual Cursor review is the human gate.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | `detect.mjs` (Node ESM, `markdown-it` + `@vscode/markdown-it-katex` + `katex`) — purpose-built detector, not a generic test runner |
| Config file | `tools/spec-render-check/package.json` + `package-lock.json` (to be created — Wave 0) |
| Quick run command | `node tools/spec-render-check/detect.mjs <file>` (single file during iteration) |
| Full suite command | `node tools/spec-render-check/detect.mjs` (all 3 specs; exit≠0 on any finding) |

### Regression set & negative controls (ground truth)
- **Regression set (must be reproduced):** the 26 author-marker lines double as a labeled regression
  set — the detector run must reproduce the author-flagged regions (recall oracle, design §5.2).
- **Negative control 1:** the **SI-PINN-002 meta-doc** comment in `pinn_architecture.md` must stay
  **unflagged** as a defect (it documents the comments; the WS-B prototype's one fixed bug was
  mislabeling exactly this comment).
- **Negative control 2:** `sampling_method.md` must stay **0-findings** under all layers (incl. not
  flagging its definition-list `:   ` lines as captions).

### Phase Requirements → Test/Gate Map
| Gate | Behavior | Automated? | Command / Method |
|------|----------|-----------|------------------|
| **G1** | Detector reproduces the author-flag regression set; both negative controls stay clean | yes | `node …/detect.mjs` over all 3 files; assert author-flagged regions reproduced, SI-PINN-002 + sampling clean |
| **G2** | Zero residual findings across all 3 files under ALL layers (D1–D6) | yes | `node …/detect.mjs` exits 0 |
| **G3** | Content-preservation audit passes (every changed line: delimiters/structure/whitespace/representation only) + comment preservation (0 lost / 0 semantically changed) | yes (diff + before/after census) | committed before/after census diff + per-comment text-hash compare |
| **G4** | Full HTML render + manual Cursor eyeball (no raw LaTeX, clipped math, broken layout, accidental code formatting, missing content) | manual (D-09) | open all 3 specs in Cursor/VS Code preview; per-file checklist recorded (D-10) |

### Sampling Rate (VER-05 loop)
- **Per fix batch (commit):** re-run `detect.mjs` over the edited file(s) → must not introduce new findings; update ledger.
- **Per file complete:** full-suite `detect.mjs` (all 3) green.
- **Phase gate:** G1–G4 all pass; ledger has all in-scope findings VERIFIED or DEFERRED; no OPEN STOP gap (unless user defers).

### Wave 0 Gaps (build before repair)
- [ ] `tools/spec-render-check/package.json` + `package-lock.json` — install + pin `markdown-it`, `@vscode/markdown-it-katex`, `katex` (gate the install behind a verify checkpoint).
- [ ] `tools/spec-render-check/detect.mjs` — sanity gate + D1–D6 + census pass + deterministic CI report + exit codes.
- [ ] Stage-0 footnote probe: confirm how Cursor renders `[^n]` (37 in pinn) before classifying.
- [ ] `.gitignore` entry for `tools/spec-render-check/node_modules/`.
- [ ] README capturing the exact detector command + interpretation (feeds D-10).

## Common Pitfalls

### Pitfall 1: Silent `@vscode/markdown-it-katex` plugin-load failure (double-wrapped export)
**What goes wrong:** The plugin's export is double-wrapped; a naive `md.use(plugin)` silently fails to
register, so KaTeX never runs and the detector flags ALL valid math (or, worse, flags nothing and
passes a broken file).
**Why it happens:** ESM/CJS interop — the imported module may need `.default` (or `.default.default`).
**How to avoid:** The **sanity gate** (Pattern 1) renders `$x^2$` and asserts KaTeX output before any
run; abort if absent. This was design test-fix #1.
**Warning signs:** Every math expression flagged, OR zero findings on a file you know is broken.

### Pitfall 2: D3 false positives on legitimate precision notation
**What goes wrong:** Bare-subscript lint flags valid escaped/structured forms.
**How to avoid (baked-in exclusions, design §5.1):** exclude escaped `\_` / `\^`; `H_\epsilon`;
`m_1r_1` (digit-led); `t_{max}` (braced label position); regex `(?<!\\)[_^](?!\{)[A-Za-z]{2,}`
(letters-only, no backslash, no brace, no digit-lead); exclude code spans/fences from D3/D4 (but D5
explicitly scans code spans).

### Pitfall 3: Trailing-`\` mistaken for a parse defect
**What goes wrong:** Treating Pandoc hard-break `\` as broken LaTeX.
**How to avoid:** It renders `<br>` — it's layout-noise (D8), removed per-instance on confirmation, not
flagged as a math/parse error.

### Pitfall 4: Mis-counting the author-comment census
**What goes wrong:** Anchoring on the retired "28 `\authcomment`" figure makes the preservation
predicate unsatisfiable (only 1 literal macro exists, and it's the negative control).
**How to avoid:** Use the all-forms basis; re-census at execution; expected baseline 26 marker lines
(13 + 13 + 0). Record the exact count in `22-COMMENT-HANDOFF.md`.

### Pitfall 5: Flagging `sampling_method.md` definition lists
**What goes wrong:** D4 mistakes Pandoc definition-list `:   text` lines for `: Table` captions →
false positives on the known-clean negative control.
**How to avoid:** Distinguish `: Table N:` captions (followed by table separator rows) from `:   `
definition-list bodies; assert sampling stays 0-findings.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Pandoc-flavored markdown (`:::` divs, multiline tables, `: Table` captions, `[^n]` footnotes) | GFM + `$…$`/`$$` KaTeX (markdown-it/Cursor target) | This phase | Pandoc constructs don't render in Cursor → must convert |
| "28 `\authcomment`" census | all-forms marker set, re-derived at execution (26 lines) | GAP-22-02, 2026-06-08 | Preservation predicate now well-formed |
| WS-B per-comment adjudication in Phase 22 | preserve-and-defer to FUT-05 | GAP-22-01, 2026-06-08 | Phase 22 = census + preservation + handoff only |

**Deprecated/outdated:**
- Design §6 disposition engine (basis classes, git temporal grounding) as Phase-22 work — now FUT-05.
- "28 `\authcomment`" figure — retired mis-census.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `markdown-it` / `@vscode/markdown-it-katex` / `katex` install cleanly at current npm versions and the plugin double-wrap workaround still applies | Standard Stack / Pitfall 1 | Detector fidelity; mitigated by sanity gate + lockfile pin at install |
| A2 | Cursor's footnote `[^n]` rendering behavior — assumed possibly-unsupported, MUST be probed in Stage-0 | Live Defect Map (pinn) | If Cursor renders footnotes, the 37 refs are not defects; if not, they are survivors. Probe resolves it |
| A3 | No author-comment wrapper currently breaks Markdown rendering (so D-05 wrapper repairs ≈ none) | WS-B Preservation | If a wrapper does break, a mechanical text-preserving repair is needed; re-confirm at execution |
| A4 | Package versions (not yet pinned) | Standard Stack | Stale-version risk; resolved by `npm view` + `--save-exact` at install |

**Note:** A2 is the one assumption that materially changes the defect count — resolve it in Wave 0/Stage-0 before classifying the 37 footnote refs.

## Open Questions (RESOLVED)

1. **Footnote rendering in Cursor (`[^n]`, 37 refs in pinn_architecture.md) — RESOLVED AS EXECUTION-TIME GATE**
   - What we know: markdown-it has no built-in footnote support; design §10 lists this as a mitigation requiring a Stage-0 probe.
   - What's unclear: whether Cursor/VS Code's preview enables a footnote plugin.
   - Resolution path: blocking Wave-0 `22-STAGE0-FOOTNOTE-PROBE.md` before any WS-A repair runs. The detector's D4 footnote handling branches at runtime via `--footnote-policy auto|supported|unsupported`; `auto` reads the recorded probe and blocks if the probe is missing while target files contain `[^n]`. No research claim is made about the actual Cursor result.

2. **Detector location convention — RESOLVED**
   - What we know: design says "formalize the detector as a committed script"; doesn't pin a path.
   - Resolution path: `tools/spec-render-check/` with committed `package.json` + lockfile (keeps Node toolchain out of repo root). This is the planner-selected detector location used by the Phase 22 plans.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Node.js | `detect.mjs` runtime | ✓ | v24.16.0 [VERIFIED] | — |
| npm | install toolchain | ✓ | 11.13.0 [VERIFIED] | — |
| `markdown-it`/`@vscode/markdown-it-katex`/`katex` | detector | ✗ (not installed) | — | install + pin (Wave 0) |
| Cursor / VS Code Markdown Preview | manual review G4 (D-09) | assumed (user's editor) | — | none — G4 is the human gate |
| Git history | WS-B temporal grounding | ✓ | — | **Not needed in Phase 22** (temporal grounding is FUT-05) |

**Missing dependencies with no fallback:** none (install resolves the toolchain).
**Missing dependencies with fallback:** the three npm packages — install + lockfile-pin in Wave 0.

## Sources

### Primary (HIGH confidence)
- `docs/work/designs/milestone_v1.4/framework-spec-cleanup/2026-06-07-framework-spec-cleanup-design.md` — full design (§2 scope, §3 D1–D8, §4 taxonomy, §5 detector+layers, §6 disposition [FUT-05], §8 validation evidence, §11 tooling). Authoritative.
- `.planning/phases/22-framework-spec-cleanup/22-CONTEXT.md` — locked D-01..D-10.
- `.planning/phases/22-framework-spec-cleanup/22-GAPS.md` — GAP-22-01 (Defer), GAP-22-02 (all-forms census). Both RESOLVED.
- `.planning/REQUIREMENTS.md` — VER-05 (line 64), FUT-05 (line 73), Phase-22 REQ TBD (line 139).
- Live file census (this session) — `grep`/`sed` over the 3 specs: 26 author-marker lines (13+13+0); 3 Pandoc tables + 2 `:::` divs + 37 footnote refs in pinn; 3 mid-list `$$\begin{aligned}` + 1 trailing-`\` in ctl; sampling clean. [VERIFIED: codebase grep]
- `node --version` → v24.16.0; `npm --version` → 11.13.0. [VERIFIED]

### Secondary (MEDIUM confidence)
- CLAUDE.md / AGENTS.md governance (STOP protocol, no-live-code, commit protocol).

### Tertiary (LOW confidence)
- npm package current versions — not verified this session; pin at install via `npm view` + lockfile.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — design-mandated + prototype-validated; only exact versions deferred to install.
- Architecture / layers: HIGH — fully specified and validated in design §5; live state confirms recurrence claims.
- Live defect map: HIGH — re-verified by grep/sed this session; matches design observations.
- Author-comment census: HIGH — re-verified (26 lines), matches GAP-22-02 resolution.
- Footnote handling: MEDIUM — depends on the Stage-0 Cursor probe (A2).

**Research date:** 2026-06-08
**Valid until:** 2026-07-08 (stable domain; re-verify counts at execution since files may be edited by Phases 20.5/21 first).
