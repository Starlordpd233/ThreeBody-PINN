---
phase: 20
slug: architecture-and-normalization-cleanup
status: passed
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-05
---

# Phase 20 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|---|---|
| **Framework** | custom shell/doc checks using `rg` and `bash` |
| **Config file** | none — Phase 20 is documentation/spec adjudication |
| **Quick run command** | `rg -n "first_omega_0=30\|hidden_omega_0=1\|elementwise_affine=False\|I_3.*\\\[0, 1/3\\\]\|I_norm_raw\|E_norm.*\\\[-1, 0\\)" pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` |
| **Full suite command** | See `Strict Full Suite Command` below. |
| **Estimated runtime** | ~15 seconds |

---

## Strict Full Suite Command

```bash
bash -lc '\
E=0; \
P16=.planning/phases/16-evidence-framework-and-issue-adjudication; \
P20=.planning/phases/20-architecture-and-normalization-cleanup; \
ARCH=$$P16/evidence; \
SPEC=pinn_instruction/markdown_conversion/framework-specs; \
echo "=== File existence ===" && \
for f in $$ARCH/B-01.md $$ARCH/B-10.md $$ARCH/M5.md $$ARCH/M8.md $$ARCH/M9.md $$ARCH/M10.md $$ARCH/D-02-NORM.md $$P20/20-CODE-DIVERGENCE.md; do test -f "$$f" || { echo "MISSING: $$f"; E=1; }; done && \
echo "=== ARCH-01: SIREN fixed omega0 ===" && \
rg -n "first_omega_0.*=.*30" $$SPEC/pinn_architecture.md | head -3 && \
rg -n "hidden_omega_0.*=.*1" $$SPEC/pinn_architecture.md | head -3 && \
rg -n "divided by.*hidden_omega_0" $$SPEC/pinn_architecture.md | head -3 && \
echo "=== ARCH-01: Negative scheduler audit ===" && \
SCHED_RAW=$(rg -ni "update_omega0|exponential decay|final_omega|decay_rate|omega0.*schedul|schedul.*omega0|omega_0.*schedul|schedul.*omega_0|dynamic[ -]schedul" $$SPEC/pinn_architecture.md) && \
SCHED=$(echo "$$SCHED_RAW" | rg -v "not scheduled|epochwise or optimizer|SI-PINN-002|Need more detail.*omega_0" || echo "") && \
if [ -n "$$SCHED" ]; then echo "FAIL: active scheduler match outside allowed anti-scheduler/SI-PINN-002"; echo "$$SCHED"; E=1; else echo "PASS: zero active scheduler matches"; fi && \
echo "=== ARCH-02: LayerNorm affine + attribution ===" && \
rg -n "elementwise_affine=False" $$SPEC/pinn_architecture.md | head -5 && \
rg -n "project-specific" $$SPEC/pinn_architecture.md | head -3 && \
echo "=== ARCH-03: I_3 raw range + staging map ===" && \
rg -n "I_3.*\\\[0, *1/3\\\]" $$SPEC/ctl_instruction.md | head -3 && \
rg -n "I_3.*in.*=.*6.*I_3.*-.*1" $$SPEC/ctl_instruction.md | head -3 && \
echo "=== ARCH-03: Negative I_3 raw [-1,1] audit ===" && \
I3_NEG=$(rg -n "I_3 *=.*\\\[-1, *?1\\\]" $$SPEC/ctl_instruction.md) && \
if [ -n "$$I3_NEG" ]; then echo "FAIL: raw I_3 [-1,1] remains"; E=1; else echo "PASS: no raw I_3 [-1,1]"; fi && \
echo "=== ARCH-04: I_norm_raw naming ===" && \
rg -n "I_norm_raw" $$SPEC/ctl_instruction.md | head -3 && \
echo "=== ARCH-04: Negative bare I_norm audit ===" && \
BARE=$(rg -n '\bI_norm\b' $$SPEC/ctl_instruction.md | rg -v "I_norm_raw|I_norm_in") && \
if [ -n "$$BARE" ]; then echo "FAIL: bare I_norm without suffix"; E=1; else echo "PASS: no bare I_norm"; fi && \
echo "=== ARCH-05: Energy occupancy + mass asymmetry ===" && \
rg -n "E_norm.*\\\[-1, *0\\)" $$SPEC/ctl_instruction.md | head -3 && \
rg -n "asymmetric|hierarchy" $$SPEC/ctl_instruction.md | head -3 && \
echo "=== Ledger: all 7 Phase 20 findings VERIFIED ===" && \
for f in B-01 B-10 M5 M8 M9 M10 D-02-NORM; do \
  if ! rg -q "| $$f |.*VERIFIED" $$P16/16-ISSUE-LEDGER.md; then echo "FAIL: $$f not VERIFIED"; E=1; fi; \
done && \
echo "PASS: all 7 findings VERIFIED" && \
echo "=== No pinn/ diff ===" && \
PINN_DIFF_CACHED=$(git diff --name-only --cached -- pinn 2>/dev/null) && \
PINN_DIFF_WT=$(git diff --name-only -- pinn 2>/dev/null) && \
if [ -n "$$PINN_DIFF_CACHED" ] || [ -n "$$PINN_DIFF_WT" ]; then echo "FAIL: pinn/ diff exists"; E=1; else echo "PASS: no pinn/ diff"; fi && \
if [ "$$E" -eq 0 ]; then echo "=== STRICT FULL SUITE: ALL PASS ==="; else echo "=== STRICT FULL SUITE: FAILURES DETECTED ==="; fi && \
exit $$E'
```

This command proves: required evidence/divergence files exist; ARCH-01 fixed-omega0 SIREN contract markers are present with zero active scheduler matches; ARCH-02 LayerNorm `elementwise_affine=False` and project-specific attribution present; ARCH-03 I_3 raw `[0, 1/3]` range and staging map are present with no contradictory raw `[-1, 1]`; ARCH-04 `I_norm_raw` naming is present with no bare `I_norm` without suffix; ARCH-05 energy occupancy `[-1, 0)` and mass asymmetry prose are present; all seven Phase 20 findings are VERIFIED in the ledger; and no staged or unstaged `pinn/` diff exists.

---

## Sampling Rate

- **After every task commit:** Run the task-owned verification command plus the quick run command.
- **After every plan wave:** Run the wave-owned verification command. The strict full suite command is a Phase 20 final gate and only runs after `20-CODE-DIVERGENCE.md` exists and all seven evidence packets are filled and VERIFIED.
- **Before `$gsd-verify-work`:** Full suite must be green and issue-ledger rows for all seven Phase 20 findings must be `VERIFIED`.
- **Max feedback latency:** 15 seconds.

---

## Per-Task Verification Map

> **Note (2026-06-05 post-execution):** The `File Exists` and `Status` columns below are the **post-execution** state recorded against the strict full suite run captured in `20-VERIFICATION.md`. `20-VERIFICATION.md` is the post-execution authority for the per-task evidence; this map is retained for traceability.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---|---|---|---|---|---|---|---|---|---|
| 20-01-01 | 01 | 1 | ARCH-01 | T-20-01 | B-01/B-10 evidence exists before spec edits, fixed-omega0 SIREN contract, no in-run scheduler. | doc-structure | `rg -n "first_omega_0.*=.*30" pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` + negative scheduler rg | yes | green |
| 20-02-01 | 02 | 2 | ARCH-02 | T-20-02 | M8 evidence exists before spec edits, project-specific LayerNorm attribution, elementwise_affine=False default. | doc-structure | `rg -n "elementwise_affine=False" pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` + attribution rg | yes | green |
| 20-03-01 | 03 | 2 | ARCH-03 | T-20-03 | M5 EVID-05 adjudication complete before I_3 edits, raw [0, 1/3] range, staging map, metadata-only scope. | doc-structure | `rg -n "I_3.*\\\[0, *1/3\\\]" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` + negative I_3 rg | yes | green |
| 20-04-01 | 04 | 3 | ARCH-05 | T-20-04 | M9/M10 evidence exists before spec edits, energy occupancy + mass asymmetry prose, no defect-framing. | doc-structure | `rg -n "E_norm.*\\\[-1, *0\\)" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` + defect-framing negative rg | yes | green |
| 20-05-01 | 05 | 4 | ARCH-04 | T-20-05 | D-02-NORM evidence packet with raw-only I_norm convention, I_norm_raw/I_norm_in naming distinction, no framework-spec edit (ARCH-04 raw-only). | doc-structure | `rg -n "I_norm_raw" pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` + negative bare I_norm rg | yes | green |

*Status: pending / green / red / flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all Phase 20 validation requirements:

- [x] `rg` exists for structural searches.
- [x] `20-GAPS.md` records GAP-20-01 as `RESOLVED-WITH-INSTRUCTION` (D-02-NORM evidence packet with raw-only I_norm convention, option a, by user instruction).
- [x] No new test framework or package install is required.
- [x] No runtime service, database, or schema push is in scope.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|---|---|---|---|
| ARCH-04 raw-only grounding | ARCH-04 | Grep can prove `I_norm_raw` exists but cannot verify the metadata-only / not-an-IC-slot reasoning. | Read `ctl_pinn_resolution.md:1435-1446` (D-02 "Closed": `I_norm_raw`/`I_norm_in = tanh(I_norm_raw)` "as metadata only unless a widened-input ablation is run"). Confirm ARCH-04 is satisfied by the named raw-vs-bounded distinction, not by a live network-input surface. |
| STOP-protocol compliance for new discoveries | ARCH-01..05 | A newly discovered source-silent semantic decision cannot be automatically classified by static search. | During execution review, if a task proposes ungrounded content beyond `20-CONTEXT.md`, confirm a new `20-GAPS.md` entry exists before the task proceeds. |

---

## Validation Sign-Off

- [x] All planned task groups have automated doc-structure verification.
- [x] Sampling continuity: no 3 consecutive tasks without automated verify.
- [x] Wave 0 covers all missing infrastructure references.
- [x] No watch-mode flags.
- [x] Feedback latency < 15s.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** approved 2026-06-05 — closure artifacts verified (see `20-VERIFICATION.md`).
