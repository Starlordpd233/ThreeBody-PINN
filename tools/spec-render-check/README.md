# spec-render-check — Phase 22 framework-spec render detector

A committed Node ESM detector that renders the three framework specs with the **same KaTeX
engine the Cursor / VS Code Markdown Preview uses** (`markdown-it` + `@vscode/markdown-it-katex`
+ `katex`) and exits non-zero on any rendering finding. It is the Wave-0 source-of-truth oracle
for Phase 22 (D-08 / G1 / G2). See `.planning/phases/22-framework-spec-cleanup/22-01-PLAN.md`.

> All commands are invoked **from the repository root**, not from this directory.

## Provenance / supply-chain (T-22-01 mitigation)

The detector toolchain is the only supply-chain surface in Phase 22. The three packages were
verified against the npm registry (canonical repos, exact names, MIT licenses) and installed
with `--save-exact`; `package-lock.json` is committed. Versions are pinned **exactly** (no
`^`/`~`): `markdown-it@14.2.0`, `@vscode/markdown-it-katex@1.1.2`, `katex@0.16.47`.

`katex@0.16.47` was chosen over the newer `0.17.0` because `@vscode/markdown-it-katex@1.1.2`
declares `katex: ^0.16.4` (`>=0.16.4 <0.17.0`); `0.16.47` keeps a **single** katex engine shared
by the plugin and the detector's direct-katex layers (D1/D2), preserving D-08 single-engine
fidelity with the Cursor target.

**Single-engine verification** — verbatim `npm ls katex` from `tools/spec-render-check/`
(run 2026-06-09; exactly one `katex@0.16.47`, the plugin copy `deduped` to the single top-level
install, no nested/duplicate katex):

```
spec-render-check@1.0.0 <home>/Desktop/3_body_problem/tools/spec-render-check
├─┬ @vscode/markdown-it-katex@1.1.2
│ └── katex@0.16.47 deduped
└── katex@0.16.47
```

`node_modules/` is git-ignored (repo-root `.gitignore` line 238); the committed
`package-lock.json` is the only persisted dependency artifact. Re-derive the dependency state any
time with `cd tools/spec-render-check && npm ci && npm ls katex`.

## Commands (run from the repository root)

| Command | Purpose |
| --- | --- |
| `node tools/spec-render-check/detect.mjs <file>` | Quick single-file run, all layers. |
| `node tools/spec-render-check/detect.mjs --all` | Run all three framework specs (the G2 full-suite gate). |
| `node tools/spec-render-check/detect.mjs --census [--root <dir>] [file ...]` | All-forms author-comment census (path-based input only; never stdin). |
| `node tools/spec-render-check/detect.mjs --regression` | Reproduce the author-flag fixtures and assert both negative controls clean. |
| `node tools/spec-render-check/detect.mjs --selftest` | Sanity gate + regression fixtures + real `sampling_method.md` control (the G1 gate). |
| `node tools/spec-render-check/detect.mjs --footnote-policy auto\|supported\|unsupported` | Branch the D4 footnote class (default `auto` reads `22-STAGE0-FOOTNOTE-PROBE.md`). |
| `node tools/spec-render-check/detect.mjs --prove-sanity-gate` | Pitfall-1 proof: force a non-callable plugin; must abort with exit 2. |

## Layers

- **D1 — KaTeX `throwOnError`** (DEFINITE): hard math parse errors.
- **D2 — KaTeX `strict`** (REVIEW): suspicious-math warnings.
- **D3 — LaTeX lint** (REVIEW, global; code/fences excluded): bare multi-char sub/superscript such
  as `L_total`. Baked-in exclusions: escaped `\_`/`\^`, braced `t_{max}`, digit-led `m_1`,
  `H_\epsilon`. Identifier-shape tokens (snake_case, base length > 2, e.g. `close_low_L`) are
  **SUPPRESSED** — surfaced for review, never silently dropped.
- **D4 — render survivor scan** (DEFINITE): control markup that must never reach visible text —
  Pandoc `:::` divs, `: Table …` captions, multiline-table separator rows, mid-line `$$`,
  surviving `\commands`, `{.attr}`/`{#id}`. Footnote `[^n]` is policy-gated (see below).
- **D5 — backtick-math** (REVIEW, oracle-guided): ASCII math inside code spans, scanned only within
  author-flagged regions.
- **D6 — prose-math** (REVIEW, oracle-guided): ASCII math in prose, scanned only within
  author-flagged regions.

D5/D6 are **oracle-guided** (design §5.2: author comments are the ground-truth oracle for
prose/backtick math). They emit only inside the ±20-line window of an author marker, which is why
the clean negative control `sampling_method.md` (zero author markers) stays at 0 findings despite
its many `snake_case = value` code spans.

## Output interpretation (feeds D-10)

Each finding prints as `[<tier>/<layer>] §<section-anchor> (line N): <message>` followed by the
matched source snippet. Positions are reported by **section/anchor + snippet** and re-derived from
live bytes (Pattern 3) — the line number is a run-time convenience, never a hardcoded constant.

- **DEFINITE** (D1, D4): a real rendering defect; must reach zero before the phase closes (G2).
- **REVIEW** (D2, D3, D5, D6): human-reviewed candidates; the author-comment oracle and manual
  Cursor review (G4) drive recall, not raw REVIEW volume.
- **SUPPRESSED**: a D3 candidate excluded by a baked-in rule, printed for transparency; not a finding.

**Exit codes:** `0` clean (or selftest/regression pass) · `1` one or more findings (DEFINITE or
REVIEW) · `2` sanity-gate failure (plugin load) · `3` missing prerequisite (Stage-0 footnote probe
unconfirmed while a target contains `[^n]`) · other non-zero = tool failure. Rendering findings are
non-zero and cannot be masked as success.

## Footnote policy (Stage-0 gate)

`@vscode/markdown-it-katex` + markdown-it core do **not** render `[^n]` footnotes; the detector
engine leaves them as literal text. Whether that is a *defect* depends on the real Cursor / VS Code
preview, recorded in `.planning/phases/22-framework-spec-cleanup/22-STAGE0-FOOTNOTE-PROBE.md`:

- `--footnote-policy supported` (or probe `FOOTNOTE_POLICY: supported`) → D4 suppresses footnote
  survivors so `--all` can reach zero.
- `--footnote-policy unsupported` (or probe `unsupported`) → D4 flags the 37 refs / 17 defs in
  `pinn_architecture.md` as DEFINITE survivors for repair.
- `--footnote-policy auto` with no confirmed probe and a target containing `[^n]` → **exit 3** until
  the Stage-0 probe is confirmed.
