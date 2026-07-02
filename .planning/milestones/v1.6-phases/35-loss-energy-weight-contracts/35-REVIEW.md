---
phase: 35-loss-energy-weight-contracts
reviewed: 2026-06-29T03:52:28Z
depth: standard
files_reviewed: 2
files_reviewed_list:
  - pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
  - pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
findings:
  critical: 0
  warning: 0
  info: 0
  total: 0
status: clean
---

# Phase 35: Code Review Report

**Reviewed:** 2026-06-29T03:52:28Z
**Depth:** standard
**Files Reviewed:** 2
**Status:** clean

## Summary

Reviewed the Phase 35 framework-spec edits in `ctl_instruction.md` and `pinn_architecture.md` against the Phase 35 context, evidence packets, verification artifact, and Phase 32 issue ledger. No blocker-level loss-contract regression was found: the reviewed specs do not lock the stale `lambda_E = 1000` premise, the issue-doc cap table, a stage-indexed Huber-delta table, default dense-residual ALM, Option C window mechanics, or a numeric causal-exponent clip bound.

One warning was found and resolved: the `ctl_instruction.md` LOSS-01 callout now uses the full Phase 35 NS-12 evidence packet path, restoring AC-LOSS traceability.

## Narrative Findings (AI reviewer)

## Warnings

Resolved.

### WR-01: LOSS-01 callout links NS-12 to a non-existent relative evidence path

**Severity:** WARNING
**File:** `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1737`
**Issue:** The LOSS-01 / NS-12 callout cites the NS-18 packet with the correct phase-local path, but cites the NS-12 packet as ``evidence/ns-12-componentwise-ad.md``. From the repository root and from the framework-spec directory, that path does not exist. This breaks the traceability chain for `AC-LOSS-01-AD` in the CTL-side contract even though the correct packet exists at `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-12-componentwise-ad.md` and `pinn_architecture.md` uses that full path correctly.
**Resolution:** Fixed in `ctl_instruction.md` by replacing the non-resolving relative path with `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-12-componentwise-ad.md`.
**Fix:**
```markdown
> **Phase 35 contract: loss scaling and units (LOSS-01; NS-18 modified / NS-12 accepted; AC-LOSS-01 / AC-LOSS-01-AD; grounded by the resolution doc sections 1.12/1.14 and `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-18-loss-scaling-units.md` / `.planning/phases/35-loss-energy-weight-contracts/evidence/ns-12-componentwise-ad.md`).**
```

---

_Reviewed: 2026-06-29T03:52:28Z_
_Reviewer: the agent (gsd-code-reviewer)_
_Depth: standard_
