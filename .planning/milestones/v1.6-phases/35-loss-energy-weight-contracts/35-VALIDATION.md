---
phase: 35
slug: loss-energy-weight-contracts
status: ready-for-execution
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-27
---

# Phase 35 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Structural Markdown/source assertions via `python3` and `rg` |
| **Config file** | none — Phase 35 is a framework-spec edit phase |
| **Quick run command** | `rg -n "AC-LOSS|LOSS-|M15|NS-12|NS-13|NS-18|D-04" .planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` |
| **Full suite command** | `python3 -c "from pathlib import Path; text=Path('pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md').read_text()+Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text(); req=['AC-LOSS-01','AC-LOSS-02','AC-LOSS-03','AC-LOSS-04','NS-18','M15','NS-13','D-04']; missing=[r for r in req if r not in text]; assert not missing, missing"` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run the quick run command and the task-specific automated command below.
- **After every plan wave:** Run the full suite command plus every automated command below.
- **Before `$gsd-verify-work`:** Full suite and all task-specific commands must be green.
- **Max feedback latency:** 10 seconds.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 35-LOSS-01 | 35-02, 35-03, 35-04 | 2, 3 | LOSS-01 | — | N/A | structural/source | `python3 -c "from pathlib import Path; text=Path('pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md').read_text()+Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text(); req=['AC-LOSS-01','NS-18','modified','Huber','no linear-momentum','tau','u=t/T']; missing=[r for r in req if r not in text]; assert not missing, missing"` | yes | pending execution |
| 35-LOSS-02 | 35-02, 35-03, 35-04 | 2, 3 | LOSS-02 | — | N/A | structural/source | `python3 -c "from pathlib import Path; import re; text=Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text()+Path('pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md').read_text(); assert 'AC-LOSS-02' in text; assert 'M15' in text and 'rejected' in text; assert not re.search(r'cap\\s*=\\s*\\{0:1,\\s*1:5,\\s*2:20,\\s*3:50,\\s*4:100,\\s*5:200,\\s*6:500\\}', text), 'cap table must not be locked'; assert 'lambda_E = 1000' not in text"` | yes | pending execution |
| 35-LOSS-03 | 35-02, 35-03, 35-04 | 2, 3 | LOSS-03 | — | N/A | structural/source | `python3 -c "from pathlib import Path; text=Path('pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md').read_text()+Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text(); required=['AC-LOSS-03','NS-13','defer','delta_E = 1.0']; missing=[r for r in required if r not in text]; assert not missing, missing; assert 'per-stage Huber-delta table' not in text"` | yes | pending execution |
| 35-LOSS-04 | 35-02, 35-03, 35-04 | 2, 3 | LOSS-04 | — | N/A | structural/source | `python3 -c "from pathlib import Path; text=Path('pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md').read_text()+Path('pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md').read_text(); req=['AC-LOSS-04','D-04','RESOLVED-WITH-INSTRUCTION','w_1 = 1','eta_c = 1','dense-residual','deferred']; missing=[r for r in req if r not in text]; assert not missing, missing"` | yes | pending execution |
| 35-GAP-32-01 | 35-01, 35-04 | 1, 3 | LOSS-04 | — | N/A | structural/source | `python3 -c "from pathlib import Path; a=Path('.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-GAPS.md').read_text(); b=Path('.planning/milestones/v1.6-GAPS.md').read_text(); assert 'GAP-32-01' in a and 'RESOLVED-WITH-INSTRUCTION' in a; assert 'GAP-32-01' in b and 'RESOLVED-WITH-INSTRUCTION' in b; assert 'Option A' in a+b"` | yes | pending execution |

*Status: pending · green · red · flaky*

---

## Wave 0 Requirements

- [x] `35-RESEARCH.md` exists and contains the Phase 35 validation architecture.
- [x] `35-VALIDATION.md` exists and lists structural checks for `LOSS-01` through `LOSS-04`.
- [x] No package installation is required for Phase 35 validation.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Canonical-home split avoids duplicate normative loss math across `ctl_instruction.md` and `pinn_architecture.md`. | LOSS-01, LOSS-02, LOSS-03, LOSS-04 | Requires judgment about normative body text versus stable cross-reference text. | Review both framework specs and confirm one file owns methodology/assembly while the other owns component math, with stable `AC-LOSS-NN` cross-references and no contradictory duplicate normative bodies. |

---

## Validation Sign-Off

- [x] All tasks have automated verify commands or this Wave 0 validation dependency.
- [x] Sampling continuity: no 3 consecutive tasks without automated verify.
- [x] Wave 0 covers all MISSING references.
- [x] No watch-mode flags.
- [x] Feedback latency < 10s.
- [x] `nyquist_compliant: true` set in frontmatter for plan-phase validation coverage.

**Approval:** approved 2026-06-27 for planning coverage. Execution evidence still must pass before `$gsd-verify-work`.
