---
phase: 17
slug: input-and-output-contracts
status: passed
nyquist_compliant: true
wave_0_complete: true
created: 2026-05-19
verified: 2026-05-20
---

# Phase 17 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | custom shell/doc checks using `rg` |
| **Config file** | none — Phase 17 is documentation/spec adjudication |
| **Quick run command** | `rg -n "14D|14-dimensional|\\[tau, IC_13\\]|IC_\\{13\\}|9D|9-dimensional|COM projection|mass-weighted COM|AD-derived" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` |
| **Full suite command** | See `Strict Full Suite Command` below. |
| **Estimated runtime** | ~10 seconds |

---

## Strict Full Suite Command

```bash
bash -lc 'test -f .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-03.md && test -f .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-04.md && test -f .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-06.md && test -f .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M1.md && test -f .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M2.md && test -f .planning/phases/17-input-and-output-contracts/17-CODE-DIVERGENCE.md && rg -n "14D|14-dimensional|IC_\\{13\\}|COM projection|mass-weighted COM|AD-derived" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-04.md .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-06.md && rg -n "AC-IO-04|FUT-01 priority|IC vector composition|Mass encoding|Orientation slots|Time input|COM projection head|Direct velocity output wording|Metadata-only invariants|Docstring drift" .planning/phases/17-input-and-output-contracts/17-CODE-DIVERGENCE.md && for f in pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md; do if awk '\''/^# Source Issues \\/ Notes for Future Reconciliation/ || /^## Source Issues \\/ Notes for Future Reconciliation/ {exit} {print}'\'' "$f" | rg -n "12D input vector|12-dimensional input vector|11-component IC|5 values for 3 trigonometrically encoded angles|outputs.*velocities"; then exit 1; fi; done && for id in B-03 B-04 B-06 M1 M2; do rg -n "^\\| $id \\|.*VERIFIED" .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md >/dev/null || exit 1; done && test -z "$(git diff --name-only --cached -- pinn)" && test -z "$(git diff --name-only -- pinn)"'
```

This command proves required files exist, canonical contract markers are present, AC-IO-04 divergence content exists, stale normative wording is absent before Source Issues metadata, all in-scope ledger rows are `VERIFIED`, and no staged or unstaged `pinn/` diff exists.

---

## Sampling Rate

- **After every task commit:** Run `rg -n "14D|14-dimensional|\\[tau, IC_13\\]|IC_\\{13\\}|9D|9-dimensional|COM projection|mass-weighted COM|AD-derived" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`
- **After every plan wave:** Run the full suite command from Test Infrastructure.
- **Before `$gsd-verify-work`:** Full suite must be green and issue-ledger rows for B-03, B-04, B-06, M1, and M2 must be `VERIFIED` or explicitly deferred with a resolved gap note.
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 17-01-01 | 01 | 1 | IO-01, IO-02, VER-05 | T-17-01 / T-17-02 | Both primary Issue 01 sources are cited before input-contract verdicts; live-code references are limited to FUT-01 handoff, and no source-silent decision is invented. | doc-structure | `bash -lc 'test -f .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-03.md && test -f .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-04.md && test -f .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M1.md && test -f .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M2.md && rg -n "IC_\\{13\\}|Jacobi|accept-resolution|AC-IO-01|AC-IO-02" .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-04.md .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M1.md .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M2.md pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md && test "$(awk '\''/^# Source Issues \\/ Notes for Future Reconciliation/ || /^## Source Issues \\/ Notes for Future Reconciliation/ {exit} {print}'\'' pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md | rg -c "x_\\{\\\\mathrm\\{net\\}\\} = \\[\\\\tau, IC_\\{13\\}\\]")" = "1" && test "$(awk '\''/^# Source Issues \\/ Notes for Future Reconciliation/ || /^## Source Issues \\/ Notes for Future Reconciliation/ {exit} {print}'\'' pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md | rg -c "\\[\\\\tau, IC_\\{13\\}\\]")" = "1"'` | ✅ present | ✅ green |
| 17-02-01 | 02 | 2 | IO-03, VER-05 | T-17-01 / T-17-03 | Output closure requires the B-06 evidence packet, hard COM projection text with raw mass metadata, and AD-derived velocity/acceleration wording before verification. | doc-structure | `bash -lc 'test -f .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-06.md && rg -n "9D|9-dimensional|COM projection|mass-weighted COM|ordered raw pre-tanh mass metadata|AD-derived|AC-IO-03" .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-06.md pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md'` | ✅ present | ✅ green |
| 17-03-01 | 03 | 2 | IO-04, VER-05 | T-17-02 / T-17-03 | Obsolete contract wording is removed from normative spec prose before Source Issues metadata, Source Issues metadata is deferred untouched to Phase 21, and every known D-14 spec-vs-code mismatch is recorded for FUT-01 without editing `pinn/`. | negative doc-structure | `bash -lc 'test -f .planning/phases/17-input-and-output-contracts/17-CODE-DIVERGENCE.md && rg -n "AC-IO-04|FUT-01 priority|pinn/data-processing-pipeline-full.py|pinn/basic_architecture.py|Orientation slots|Docstring drift" .planning/phases/17-input-and-output-contracts/17-CODE-DIVERGENCE.md && for f in pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md; do if awk '\''/^# Source Issues \\/ Notes for Future Reconciliation/ || /^## Source Issues \\/ Notes for Future Reconciliation/ {exit} {print}'\'' "$f" | rg -n "12D input vector|12-dimensional input vector|11-component IC|5 values for 3 trigonometrically encoded angles|outputs.*velocities"; then exit 1; fi; done && test -z "$(git diff --name-only --cached -- pinn)" && test -z "$(git diff --name-only -- pinn)"'` | ✅ present | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all Phase 17 validation requirements:

- [x] `rg` exists for structural searches.
- [x] `17-GAPS.md` records GAP-17-01 through GAP-17-11 as `RESOLVED-WITH-INSTRUCTION`.
- [x] No new test framework or package install is required.
- [x] No runtime service, database, or schema push is in scope.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| EVID-05 physics argument quality for B-04 | IO-02, VER-05 | The first-principles comparison between issue-doc options and the resolution-doc Jacobi state requires expert judgment beyond grep; live-code status quo is FUT-01 handoff context only. | Read `.planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-04.md`; confirm it explicitly compares Options A, B, C, and D, states the verdict `accept-resolution`, and explains why Jacobi-state IC_13 preserves reconstructive information better than invariant-only or trig-angle contracts. |
| STOP-protocol compliance for new discoveries | VER-05 | A newly discovered source-silent semantic/process decision cannot be automatically classified by static search. | During execution review, if any task proposes new content not grounded in the resolution doc, issue doc, prior user decision, roadmap, or requirements, confirm a new `GAP-17-NN` entry exists before the task proceeds. Live `pinn/` code is FUT-01 handoff context only, not v1.4 grounding or evidence. |

---

## Validation Sign-Off

- [x] All planned task groups have automated doc-structure verification.
- [x] Sampling continuity: no 3 consecutive tasks without automated verify.
- [x] Wave 0 covers all missing infrastructure references.
- [x] No watch-mode flags.
- [x] Feedback latency < 10s.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** approved 2026-05-19
