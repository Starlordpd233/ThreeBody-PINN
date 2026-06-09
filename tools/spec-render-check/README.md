# spec-render-check — Phase 22 framework-spec render detector

A committed Node ESM detector that renders the three framework specs with the **same KaTeX
engine the Cursor / VS Code Markdown Preview uses** (`markdown-it` + `@vscode/markdown-it-katex`
+ `katex`) and exits non-zero on any rendering finding. It is the Wave-0 source-of-truth oracle
for Phase 22 (D-08 / G1 / G2). See `.planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-01-PLAN.md`.

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
| `node tools/spec-render-check/detect.mjs --all` | Run all three framework specs (the G2 full-suite gate) and auto-load committed Phase 22 adjudication allowlists. |
| `node tools/spec-render-check/detect.mjs --census [--root <dir>] [file ...]` | All-forms author-comment census (path-based input only; never stdin). |
| `node tools/spec-render-check/detect.mjs --regression` | Reproduce the author-flag fixtures and assert both negative controls clean. |
| `node tools/spec-render-check/detect.mjs --selftest` | Sanity gate + regression fixtures + real `sampling_method.md` control (the G1 gate). |
| `node tools/spec-render-check/detect.mjs --footnote-policy auto\|supported\|unsupported` | Branch the D4 footnote class (default `auto` reads `22-STAGE0-FOOTNOTE-PROBE.md`). |
| `node tools/spec-render-check/detect.mjs --adjudications <path>` | Load a REVIEW adjudication allowlist (JSON array of `{file, line, token, verdict, rationale}`). Matched REVIEWs are reported as ADJUDICATED (cleared); exit 0 when 0 DEFINITE + all REVIEWs adjudicated or absent. |
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

With `--all`, the detector auto-loads every committed JSON allowlist in
`tools/spec-render-check/adjudications/` before computing the full-suite exit code. With
`--adjudications <path>`, a single explicit allowlist is loaded for targeted per-file runs. In both
cases, exit `0` means 0 DEFINITE + every REVIEW is either adjudicated (matched in the allowlist) or
absent. Non-zero only when unadjudicated REVIEWs or any DEFINITE remain. The allowlists do NOT
change D1–D7 core logic.

## Adjudication allowlist

The `--adjudications` flag loads a JSON array of REVIEW findings that have been human-adjudicated
and cleared. Each entry:

```json
{
  "file": "pinn_architecture.md",
  "line": 170,
  "token": "first_omega_0",
  "verdict": "code-identifier-kept",
  "rationale": "SIREN initialization parameter name (PyTorch code identifier, not math)"
}
```

Matching: a REVIEW finding is adjudicated when all three match — file basename equals `file`,
1-based line number equals `line`, and `token` appears as a substring of the finding's message.
Adjudicated findings are printed as `[ADJUDICATED/<layer>]` with verdict and rationale, and are
excluded from the exit-code calculation. The allowlist does not affect DEFINITE findings (which
always cause exit 1) or SUPPRESSED items (which are never findings).

Typical use: when D5/D6 flag code identifiers (PyTorch parameter names, filenames) that the plan's
D-02/D-07 code-identifier exclusion says to keep as code, the allowlist records the adjudication
so the detector can honestly exit 0. The same pattern is expected to apply across plans (e.g.,
22-02 and 22-03 both encounter `first_omega_0`, `elementwise_affine`, etc.).

## Footnote policy (Stage-0 gate)

`@vscode/markdown-it-katex` + markdown-it core do **not** render `[^n]` footnotes; the detector
engine leaves them as literal text. Whether that is a *defect* depends on the real Cursor / VS Code
preview, recorded in `.planning/milestones/v1.4-phases/22-framework-spec-cleanup/22-STAGE0-FOOTNOTE-PROBE.md`:

- `--footnote-policy supported` (or probe `FOOTNOTE_POLICY: supported`) → D4 suppresses footnote
  survivors so `--all` can reach zero.
- `--footnote-policy unsupported` (or probe `unsupported`) → D4 flags the 37 refs / 17 defs in
  `pinn_architecture.md` as DEFINITE survivors for repair.
- `--footnote-policy auto` with no confirmed probe and a target containing `[^n]` → **exit 3** until
  the Stage-0 probe is confirmed.
