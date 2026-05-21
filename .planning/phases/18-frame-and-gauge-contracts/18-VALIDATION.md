---
phase: 18
slug: frame-and-gauge-contracts
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-05-20
---

# Phase 18 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|---|---|
| **Framework** | custom shell/doc checks using `rg` and `bash` |
| **Config file** | none - Phase 18 is documentation/spec adjudication |
| **Quick run command** | `rg -n "Unified Preprocessing Pipeline|COM recenter|zero-momentum boost|canonical ordering|canonical rotation gauge|global scaling|AC-FRAME" .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-05.md .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M3.md pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` |
| **Full suite command** | See `Strict Full Suite Command` below. |
| **Estimated runtime** | ~10 seconds |

---

## Strict Full Suite Command

```bash
bash -lc 'test -f .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-05.md && test -f .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M3.md && test -f .planning/phases/18-frame-and-gauge-contracts/18-CODE-DIVERGENCE.md && rg -n "Unified Preprocessing Pipeline|mass invariance|COM recenter|zero-momentum boost|canonical ordering|canonical rotation gauge|global scaling|sum_i m_i|1e-12|stored per-trajectory metadata|AC-FRAME-01|AC-FRAME-02|AC-FRAME-03|AC-FRAME-04" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-05.md .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M3.md && rg -n "Gaussian perturbation|FRAME-01 unified preprocessing|p3 = -\\(p1 \\+ p2\\)|v1 = -v2/2|v3 = -v2/2|Center of Mass|total momentum" pinn_instruction/markdown_conversion/framework-specs/sampling_method.md && rg -n "3D Cartesian|velocities remain fully 3D|9D position|not planar|not invariant-only" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md && rg -n "^\\| B-05 \\|.*VERIFIED.*AC-FRAME-01|^\\| M3 \\|.*VERIFIED.*AC-FRAME-01" .planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md && rg -n "Phase 18|FRAME-01|FRAME-02|FRAME-03|FRAME-04|FUT-01" .planning/phases/18-frame-and-gauge-contracts/18-CODE-DIVERGENCE.md && rg -n "Phase 20.5.*section anchor|sampling_method.md" .planning/milestones/v1.4-GAPS.md && rg -n "13 constraints for an 8-dimensional reduced phase space" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md && test -z "$(git diff --name-only --cached -- pinn)" && test -z "$(git diff --name-only -- pinn)"'
```

This command proves required evidence/divergence files exist, frame/gauge contract markers are present, sampling-frame text exists, 3D Cartesian output is preserved, B-05/M3 are verified, the Phase 20.5 heads-up remains present, M4 text remains untouched for Phase 19, and no staged or unstaged `pinn/` diff exists.

---

## Sampling Rate

- **After every task commit:** Run the task-owned verification command plus the quick run command.
- **After every plan wave:** Run the strict full suite command.
- **Before `$gsd-verify-work`:** Full suite must be green and issue-ledger rows for B-05 and M3 must be `VERIFIED` or explicitly deferred with a resolved gap note.
- **Max feedback latency:** 10 seconds.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---|---|---|---|---|---|---|---|---|---|
| 18-01-01 | 01 | 1 | FRAME-01, FRAME-02, FRAME-04, VER-05 | T-18-01 / T-18-02 | B-05/M3 evidence exists before spec closure, CTL owns one unified preprocessing pipeline, model-output COM projection is referenced without re-locking Phase 17. | doc-structure | `bash -lc 'test -f .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-05.md && test -f .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M3.md && rg -n "Unified Preprocessing Pipeline|COM recenter|zero-momentum boost|canonical ordering|canonical rotation gauge|global scaling|1e-12|AC-FRAME-01|AC-FRAME-02|AC-FRAME-04|velocities remain fully 3D" .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/B-05.md .planning/phases/16-evidence-framework-and-issue-adjudication/evidence/M3.md pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md'` | pending | pending |
| 18-02-01 | 02 | 2 | FRAME-03, VER-05 | T-18-03 | Sampling prose is verified against `simulation_data/` and confined to frame behavior, leaving the Phase 20.5 Sobol coordinate target alone. | doc-structure | `bash -lc 'rg -n "Gaussian perturbation|FRAME-01 unified preprocessing|p3 = -\\(p1 \\+ p2\\)|v1 = -v2/2|v3 = -v2/2|Center of Mass|total momentum" pinn_instruction/markdown_conversion/framework-specs/sampling_method.md && rg -n "scale_range=\\(0.8, 1.2\\)|velocity_scale=0.1" simulation_data/Scripts/ic_generation/generate_ics.py simulation_data/Scripts/ic_generation/ic_generation_utils.py'` | pending | pending |
| 18-03-01 | 03 | 3 | FRAME-01, FRAME-02, FRAME-03, FRAME-04, VER-05 | T-18-01 / T-18-04 | FUT-01 divergence is recorded without `pinn/` edits, B-05/M3 are verified only after checks pass, and Phase 19/20.5 boundaries remain intact. | full-suite | Use the strict full suite command above. | pending | pending |

*Status: pending / green / red / flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all Phase 18 validation requirements:

- [x] `rg` exists for structural searches.
- [x] `18-GAPS.md` records GAP-18-01 and GAP-18-02 as `RESOLVED-WITH-INSTRUCTION`.
- [x] No new test framework or package install is required.
- [x] No runtime service, database, or schema push is in scope.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|---|---|---|---|
| Rotation-gauge prose preserves full 3D trajectory semantics | FRAME-04 | Grep can prove markers exist but cannot judge whether wording accidentally implies planar trajectory evolution. | Read `ctl_instruction.md` Step 2.4 after execution. Confirm the guard says the gauge fixes only initial orientation, velocities remain fully 3D, and the model output remains 9D Cartesian positions. |
| STOP-protocol compliance for new discoveries | VER-05 | A newly discovered source-silent semantic/process decision cannot be automatically classified by static search. | During execution review, if a task proposes ungrounded content beyond `18-CONTEXT.md`, confirm a new `18-GAPS.md` entry exists before the task proceeds. |

---

## Validation Sign-Off

- [x] All planned task groups have automated doc-structure verification.
- [x] Sampling continuity: no 3 consecutive tasks without automated verify.
- [x] Wave 0 covers all missing infrastructure references.
- [x] No watch-mode flags.
- [x] Feedback latency < 10s.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** pending execution verification.
