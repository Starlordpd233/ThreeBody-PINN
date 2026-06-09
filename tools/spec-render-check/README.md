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

<!-- Command reference and output interpretation (D-10) are added in Task 3. -->
