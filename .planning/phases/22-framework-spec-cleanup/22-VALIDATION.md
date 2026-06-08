---
phase: 22
slug: framework-spec-cleanup
status: active
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
- **VER-05 re-verification:** after each batch of edits, re-run the detector on every previously-clean spec the batch could have regressed (same file, shared formula/section); any new finding reverts that region to `IN_PROGRESS` in the per-plan summary. **WS-A plans (22-02, 22-03) record per-plan summaries, not direct ledger writes, during Wave 1 parallel execution.** Plan 22-05 (Wave 3) reconciles the shared `16-ISSUE-LEDGER.md` once after Wave 1 and Wave 2 artifacts are stable, using the **existing Phase 16 ledger columns and per-finding transition-log format** (PENDING→IN_PROGRESS→FIX_APPLIED→VERIFIED lifecycle). Do not define new VER-05 fields unless a STOP-surfaced process-schema decision resolves them.

**Commit cadence (WS-A plans 22-02, 22-03):** Commit after each structural construct conversion or tightly scoped math batch that leaves the detector in a known state. Use `scripts/agent-commit` (not raw `git commit`). Before each task-boundary commit: run `git diff --check`, re-run the detector on the changed file, and inspect the changed-file diff. Prefer small commits and region-level restoration over full-file destructive rollback.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 22-01-* | 01 | 0 | VER-05 | T-22-01 (npm supply-chain) | pinned deps + committed lockfile; plugin double-wrap sanity gate aborts on load failure (inline + block math) | infra | `node tools/spec-render-check/detect.mjs --selftest` (sanity gate + regression fixtures pass, negative controls clean) | ❌ W0 | ⬜ pending |
| 22-01-Task4 (pre-WS-A baseline + census) | 01 | 0 | VER-05 | — | N/A | census | `test -f 22-COMMENT-CENSUS-PRE.md && git ls-files --error-unmatch 22-COMMENT-CENSUS-PRE.md` | ❌ W0 | ⬜ pending |
| 22-0?-* (Stage-0 footnote probe) | 01 | 0/1 | VER-05 | — | N/A | manual+auto | probe `[^n]` rendering in the Cursor target; record supported/unsupported | ❌ W0 | ⬜ pending |
| 22-02-* (WS-A repair, pinn_architecture) | 02 | 1 | VER-05 | — | N/A | render | `node tools/spec-render-check/detect.mjs pinn_architecture.md` → 0 residual findings (G2) | ❌ W0 | ⬜ pending |
| 22-03-* (WS-A repair, ctl_instruction) | 03 | 1 | VER-05 | — | N/A | render | `node tools/spec-render-check/detect.mjs ctl_instruction.md` → 0 residual findings (G2) | ❌ W0 | ⬜ pending |
| 22-??-* (math normalization) | 02/03 | 1 | VER-05 | — | N/A | equivalence | content-preservation audit (G3): each changed hunk classified into allowed categories with per-hunk evidence | ❌ W0 | ⬜ pending |
| 22-04-* (WS-B census + preservation) | 04 | 2 | VER-05 | — | N/A | census | PRE/POST `--census` diff (using committed `22-COMMENT-CENSUS-PRE.md` and `22-COMMENT-CENSUS-POST.md`): 0 author comments lost, 0 semantically changed; `22-COMMENT-HANDOFF.md` enumerates all | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky. Task IDs are placeholders until the planner finalizes plan/wave numbering; re-derive against live state, no hardcoded line numbers.*

**STOP-halt semantics:** A STOP-halted detector finding (e.g., an ambiguous transcription surfaced under the STOP protocol) is **not** a passing zero-finding run. The detector exits non-zero, and the owning plan is blocked until the user resolves or explicitly defers the halted item. Do not treat non-zero findings tied to unresolved STOP items as "green with exceptions."

---

## Wave 0 Requirements

- [ ] `tools/spec-render-check/detect.mjs` — the 6-layer detector (D1 throwOnError, D2 strict, D3 LaTeX lint, D4 survivor scan, D5 backtick-math, D6 prose-math) with the `@vscode/markdown-it-katex` double-wrap sanity gate (verifies both inline and block math).
- [ ] `tools/spec-render-check/package.json` + lockfile — pinned `markdown-it`, `@vscode/markdown-it-katex`, `katex`.
- [ ] Regression fixtures — the live author-flagged regions as ground truth the detector must reproduce.
- [ ] Negative controls — the SI-PINN-002 meta-doc comment (must stay unflagged) and `sampling_method.md` (must stay 0-findings).
- [ ] Stage-0 footnote probe result recorded (decides whether `[^n]` in `pinn_architecture.md` is a survivor defect).
- [ ] Pre-WS-A baseline ref recorded (tag `v1.4-pre-phase-22` or named commit in `22-01-SUMMARY.md`).
- [ ] `22-COMMENT-CENSUS-PRE.md` committed — pre-WS-A author-comment census (all forms) with per-comment `text_hash` and `COMMENT_HASH` lines.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Full rendered document is visually correct in the actual Cursor/VS Code preview (G4) | VER-05 / ROADMAP SC 3 | Detector approximates the renderer; final fidelity (no clipped math, broken layout, accidental code formatting, missing content) requires a human eyeball in the real target | Open each of the 3 specs in Cursor preview; inspect every edited equation + surroundings and the full document; confirm no raw LaTeX, no Pandoc artifacts, comments intact and legible |
| `[^n]` footnote rendering in the Cursor target (Stage-0 probe) | VER-05 | markdown-it has no built-in footnote support; the real Cursor target may or may not enable a plugin | Render a `[^n]` sample in Cursor preview before classifying the 37 refs / 17 defs in `pinn_architecture.md` |

---

## Validation Sign-Off

- [ ] 22-01 (Wave 0): detector + regression fixtures + negative controls + pre-WS-A baseline ref + `22-COMMENT-CENSUS-PRE.md` before any repair task runs
- [ ] 22-02, 22-03 (Wave 1, parallel): every WS-A repair task has an automated detector check (quick command) per the commit cadence
- [ ] 22-04 (Wave 2): PRE/POST census diff and `22-COMMENT-HANDOFF.md`
- [ ] 22-05 (Wave 3): full suite green + G3 audit + G4 manual review + VER-05 ledger reconciliation
- [ ] Sampling continuity: no 3 consecutive tasks without an automated detector/census check
- [ ] No watch-mode flags (detector runs once, exits with status)
- [ ] Feedback latency < 15s
- [ ] Manual Cursor render review (G4) scheduled before `/gsd-verify-work`
- [ ] `nyquist_compliant: true` set in frontmatter after the planner/checker confirms the map

**Approval:** pending
