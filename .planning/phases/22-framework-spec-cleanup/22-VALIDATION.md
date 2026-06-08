---
phase: 22
slug: framework-spec-cleanup
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-06-08
---

# Phase 22 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Phase 22 is presentation-preserving: validation is a committed **render detector** + a **census/preservation check** + **manual Cursor render review**, not a behavioral unit-test suite. Grounded in `22-RESEARCH.md` § Validation Architecture (gates G1–G4) and the design doc §5.4/§9. No new `AC-*` names are introduced — verification maps to ROADMAP Phase 22 Success Criteria 1–7.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Node detector (`markdown-it` + `@vscode/markdown-it-katex` + `katex`) + manual Cursor/VS Code KaTeX preview |
| **Config file** | `tools/spec-render-check/package.json` + lockfile (committed in Wave 0; pinned deps) |
| **Quick run command** | `node tools/spec-render-check/detect.mjs <file>` (single spec, all layers D1–D6) |
| **Full suite command** | `node tools/spec-render-check/detect.mjs --all` (3 specs) + `--census` (all-forms author-comment census + preservation diff) + `--regression` (reproduce author-flag set, negative controls clean) |
| **Estimated runtime** | ~5–15 seconds (3 small markdown files; no network) |

---

## Sampling Rate

- **After every task commit:** Run the quick command on the file(s) that task touched — must show **zero residual findings** for closed regions.
- **After every plan wave:** Run the full suite (`--all` + `--census` + `--regression`).
- **Before `/gsd-verify-work`:** Full suite green across all 3 specs AND manual Cursor render review complete (G4).
- **Max feedback latency:** ~15 seconds (detector is local + fast).
- **VER-05 re-verification:** after each batch of edits, re-run the detector on every previously-clean spec the batch could have regressed (same file, shared formula/section); any new finding reverts that region to `IN_PROGRESS` in the `16-ISSUE-LEDGER.md`.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 22-00-* | 00 | 0 | VER-05 | T-22-01 (npm supply-chain) | pinned deps + committed lockfile; plugin double-wrap sanity gate aborts on load failure | infra | `node tools/spec-render-check/detect.mjs --selftest` (sanity gate + regression fixtures pass, negative controls clean) | ❌ W0 | ⬜ pending |
| 22-0?-* (Stage-0 footnote probe) | — | 0/1 | VER-05 | — | N/A | manual+auto | probe `[^n]` rendering in the Cursor target; record supported/unsupported | ❌ W0 | ⬜ pending |
| 22-??-* (WS-A repair, per spec) | — | — | VER-05 | — | N/A | render | `node tools/spec-render-check/detect.mjs <file>` → 0 residual findings (G2) | ❌ W0 | ⬜ pending |
| 22-??-* (math normalization) | — | — | VER-05 | — | N/A | equivalence | content-preservation audit: each changed line differs only in delimiters/structure/whitespace/representation (G3) | ❌ W0 | ⬜ pending |
| 22-??-* (WS-B census + preservation) | — | — | VER-05 | — | N/A | census | `--census` before/after diff: 0 author comments lost, 0 semantically changed; `22-COMMENT-HANDOFF.md` enumerates all | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky. Task IDs are placeholders until the planner finalizes plan/wave numbering; re-derive against live state, no hardcoded line numbers.*

---

## Wave 0 Requirements

- [ ] `tools/spec-render-check/detect.mjs` — the 6-layer detector (D1 throwOnError, D2 strict, D3 LaTeX lint, D4 survivor scan, D5 backtick-math, D6 prose-math) with the `@vscode/markdown-it-katex` double-wrap sanity gate.
- [ ] `tools/spec-render-check/package.json` + lockfile — pinned `markdown-it`, `@vscode/markdown-it-katex`, `katex`.
- [ ] Regression fixtures — the live author-flagged regions as ground truth the detector must reproduce.
- [ ] Negative controls — the SI-PINN-002 meta-doc comment (must stay unflagged) and `sampling_method.md` (must stay 0-findings).
- [ ] Stage-0 footnote probe result recorded (decides whether `[^n]` in `pinn_architecture.md` is a survivor defect).

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Full rendered document is visually correct in the actual Cursor/VS Code preview (G4) | VER-05 / ROADMAP SC 3 | Detector approximates the renderer; final fidelity (no clipped math, broken layout, accidental code formatting, missing content) requires a human eyeball in the real target | Open each of the 3 specs in Cursor preview; inspect every edited equation + surroundings and the full document; confirm no raw LaTeX, no Pandoc artifacts, comments intact and legible |
| `[^n]` footnote rendering in the Cursor target (Stage-0 probe) | VER-05 | markdown-it has no built-in footnote support; the real Cursor target may or may not enable a plugin | Render a `[^n]` sample in Cursor preview before classifying the 37 refs / 17 defs in `pinn_architecture.md` |

---

## Validation Sign-Off

- [ ] Every WS-A repair task has an automated detector check (quick command) or a Wave 0 dependency
- [ ] Sampling continuity: no 3 consecutive tasks without an automated detector/census check
- [ ] Wave 0 builds the detector + regression fixtures + negative controls before any repair task runs
- [ ] No watch-mode flags (detector runs once, exits with status)
- [ ] Feedback latency < 15s
- [ ] Manual Cursor render review (G4) scheduled before `/gsd-verify-work`
- [ ] `nyquist_compliant: true` set in frontmatter after the planner/checker confirms the map

**Approval:** pending
