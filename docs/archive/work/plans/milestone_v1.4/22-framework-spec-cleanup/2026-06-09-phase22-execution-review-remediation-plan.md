---
title: "verify: remediate Phase 22 execution-review findings"
type: docs
status: archived
archived_at: 2026-06-09
date: 2026-06-09
purpose: implementation-plan
created: 2026-06-09
milestone: v1.4
phase: 22-framework-spec-cleanup
execution: knowledge-work
execution_status: first-pass-complete
executed_at: 2026-06-09T14:54:42+0800
review_status: reviewed
retirement_trigger: "Phase 22 execution-review findings are fixed or explicitly carried as human-gated blockers"
retirement_trigger_met: 2026-06-09
---

# verify: remediate Phase 22 execution-review findings

## Summary

The Phase 22 execution reports agree that the detector, content-preservation, author-comment, and VER-05 ledger work is materially green, but they identify record and closeout defects that must be fixed before Phase 22 can be closed honestly.

This plan addresses the valid, non-semantic findings and keeps the human-only G4 Cursor/VS Code visual backstop visible as the remaining blocker. It does not mark the manual visual gate passed without user evidence.

## Verified Findings

| ID | Finding | Disposition |
|---|---|---|
| E1 | `22-02-SUMMARY.md` falsely says footnotes were preserved as `[^n]` and cites nonexistent/incorrect commit `ac601e9`. | Fix the summary to state the Stage-0-driven `[^n]` to `[n]` conversion, cite `acb8aa8`, and preserve the table-transform script as committed evidence. |
| E2 | `22-03-SUMMARY.md` says Task 1 needed no edits even though the recorded work moved `\begin{aligned}` blocks / math surroundings. | Fix Task 1 wording and keep the existing `7fe572e` summary commit reference. |
| E3 | `22-03` adjudication allowlist has 11 entries while the detector clears and the summary documents 10; `dE/E` and `cpu_times` are orphan entries. | Prune the two orphan allowlist entries, then rerun the `ctl_instruction.md` detector command. |
| E4 | `22-VALIDATION.md` remains active false/unchecked despite Waves 0-3 automated evidence being complete. | Update automated sign-offs while leaving G4 manual approval pending. |
| E5 | `16-ISSUE-LEDGER.md` claims "PASS. All gates satisfied" while G4 visual review is pending. | Change the verdict to conditional automated pass pending G4. |
| E6 | `.planning/ROADMAP.md`, `.planning/STATE.md`, `.planning/PROJECT.md`, and `.planning/REQUIREMENTS.md` still describe Phase 22 as next/planned. | Update milestone tracking to say Phase 22 automated execution is complete and manual G4 approval remains before full closure. |
| E7 | `22-02-transform.mjs` is untracked but useful for table-conversion reproducibility. | Keep it as a phase artifact and reference it from the summary. |

## Scope

In scope:
- Edit Phase 22 execution and closeout records under `.planning/`.
- Edit `tools/spec-render-check/adjudications/22-03-ctl-instruction.json`.
- Add this remediation plan.
- Run detector, diff, and status verification.

Out of scope:
- Edit framework-spec semantic content.
- Claim or simulate the manual Cursor/VS Code G4 visual review.
- Delete or archive review reports.
- Revert unrelated user-owned working-tree changes.

## Implementation Steps

1. Correct Phase 22 execution summaries:
   - Update `22-02-SUMMARY.md` footnote and commit evidence.
   - Update `22-03-SUMMARY.md` Task 1 wording and allowlist wording.

2. Tighten detector evidence:
   - Remove orphan `dE/E` and `cpu_times` entries from `tools/spec-render-check/adjudications/22-03-ctl-instruction.json`.
   - Rerun `node tools/spec-render-check/detect.mjs --adjudications tools/spec-render-check/adjudications/22-03-ctl-instruction.json pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`.

3. Update validation and ledger closeout:
   - Mark completed automated validation sign-offs in `22-VALIDATION.md`.
   - Leave the manual Cursor render review and final `nyquist_compliant` sign-off unchecked/pending.
   - Change the Phase 22 ledger acceptance verdict to a conditional pass pending G4.

4. Update milestone tracking:
   - Mark plans 22-01 through 22-04 complete.
   - Mark 22-05 as automated gates complete, pending G4 visual backstop.
   - Update current-state prose in PROJECT, REQUIREMENTS, ROADMAP, and STATE without changing unrelated policy edits already present in the working tree.

5. Verify:
   - `node tools/spec-render-check/detect.mjs --selftest`
   - `node tools/spec-render-check/detect.mjs --adjudications tools/spec-render-check/adjudications/22-02-pinn-architecture.json pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
   - `node tools/spec-render-check/detect.mjs --adjudications tools/spec-render-check/adjudications/22-03-ctl-instruction.json pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`
   - `node tools/spec-render-check/detect.mjs pinn_instruction/markdown_conversion/framework-specs/sampling_method.md`
   - `git diff --check`

## Remaining Human Gate

Phase 22 is not fully closeable until the user completes the checklist in `.planning/phases/22-framework-spec-cleanup/22-RENDER-REVIEW.md` and reports approval or defects. If approved, the final closeout pass can mark G4 complete, update the Phase 22 row to complete, and set the milestone state to complete.

## Sources

- `docs/work/reviews/milestone_v1.4/22-framework-spec-cleanup/review_of_execution/`
- `.planning/phases/22-framework-spec-cleanup/22-05-PLAN.md`
- `.planning/phases/22-framework-spec-cleanup/22-RENDER-REVIEW.md`
- `.planning/phases/22-framework-spec-cleanup/22-VALIDATION.md`
- `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md`
- `docs/README.md`
