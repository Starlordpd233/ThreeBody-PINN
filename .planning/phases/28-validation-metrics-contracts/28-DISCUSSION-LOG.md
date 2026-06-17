# Phase 28: Validation-Metrics Contracts - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-06-14
**Phase:** 28-validation-metrics-contracts
**Mode:** `--auto --all` (all gray areas auto-selected; recommended defaults chosen by Claude per explicit user instruction; auto-advance to plan-phase suppressed)
**Areas discussed:** Spec placement, SCS handling, SASD/IPR/PSC adjudication approach, Evidence/ledger/AC discipline, Plan order & batching, Doc-03 deferrals, Autonomous execution & STOP recovery

---

## Spec placement

| Option | Description | Selected |
|--------|-------------|----------|
| ctl primary + arch where FUT-01-facing | All four contracts land in `ctl_instruction.md`; `pinn_architecture.md` only where architecture-facing wording is needed; SCS transcribed into ctl, DQA cited read-only | ✓ |
| Split by metric type | Distribute metrics across both spec files by theme | |
| Edit DQA in place | Edit the metric definitions where they already live | |

**Auto-selected:** ctl primary + arch where FUT-01-facing (recommended default).
**Notes:** Grounded by the `24-ISSUE-LEDGER.md` Spec-Section column (`ctl_instruction.md; pinn_architecture.md` for SASD/IPR/PSC) and Phase 27 D-02. "Edit DQA in place" is rejected outright - DQA is read-only under SCOPE-09. Captured as CONTEXT D-02.

---

## SCS handling (re-adjudicate vs transcribe)

| Option | Description | Selected |
|--------|-------------|----------|
| Transcribe locked verdict | VAL-01 transcribes the Phase 25 `accept-resolution` verdict (locked log-drift gate; reject ratio thresholds); no re-adjudication | ✓ |
| Re-open the SCS gate | Re-adjudicate the threshold from scratch | |

**Auto-selected:** Transcribe locked verdict (recommended default).
**Notes:** SCS is already adjudicated - `evidence/scs-thresholds.md` carries `accept-resolution`. Re-opening a locked Phase 25 verdict is out of scope (mirrors Phase 27 D-03). Captured as CONTEXT D-03.

---

## SASD / IPR / PSC adjudication approach

| Option | Description | Selected |
|--------|-------------|----------|
| Evidence-backed + surface flagged forks (STOP protocol) | Author EVID-06 packets before edits; adjudicate against dataset + DQA + first principles; surface Q-C2/C3/C4 forks for user sign-off where unsettled | ✓ |
| Adopt the resolution doc's positions | Take the resolution doc's Q-C2/C3/C4 choices as the answer | |
| Defer the whole metric set to a later phase | Punt VAL-02/03/04 | |

**Auto-selected:** Evidence-backed + surface flagged forks (the only STOP-protocol-compliant option).
**Notes:** This is the one area where `--auto` does NOT pick a substantive answer. The resolution doc itself flags Q-C2 (SASD endpoints, "for sign-off"), Q-C3 (IPR units, ~464x gate impact - "the consequential one"), and Q-C4 (PSC composition, "present in neither input"). The v1.5 STOP protocol forbids adopting source-silent semantic forks on the resolution doc's authority alone, so "Adopt the resolution doc's positions" is rejected. The fork outcomes are deliberately left undecided - to be settled with evidence during execution or surfaced to the user. Captured as CONTEXT D-04 (and D-13/D-14 for STOP handling).

---

## Evidence / ledger / AC discipline

| Option | Description | Selected |
|--------|-------------|----------|
| Reuse Phase 25 machinery, seeded AC IDs | EVID-06 packets per ID->Filename map; seeded AC-VAL-01..04; lifecycle + same-commit wiring | ✓ |
| Invent a Phase 28-local schema | New packet/AC scheme for metrics | |

**Auto-selected:** Reuse Phase 25 machinery, seeded AC IDs (recommended default).
**Notes:** AC-VAL-01..04 are pre-reserved (evidence README D-13). Inventing a new schema would be a process-schema STOP violation. Captured as CONTEXT D-06/D-07/D-08/D-09.

---

## Plan order & batching

| Option | Description | Selected |
|--------|-------------|----------|
| SCS first, then SASD -> IPR -> PSC | Lowest-risk transcription first; each un-adjudicated metric gated on authoring its packet | ✓ |
| Single combined plan | All four in one plan | |
| PSC/IPR/SASD before SCS | Hardest first | |

**Auto-selected:** SCS first, then SASD -> IPR -> PSC (recommended default).
**Notes:** SCS depends only on the already-locked PIPE-09 scale and is pure transcription. Batching allowed only if reviewable and no un-surfaced fork blocks it. Captured as CONTEXT D-12.

---

## Doc-03 deferrals

| Option | Description | Selected |
|--------|-------------|----------|
| Forward-references only | Record M16/ALM/replay as factual forward-references; data-side only | ✓ |
| Define training-loop policy now | Specify collocation/noise-floor/replay usage | |

**Auto-selected:** Forward-references only (recommended default).
**Notes:** SCOPE-11 + OI-10 keep training-loop usage with doc-03. Captured as CONTEXT D-05.

---

## Autonomous execution & STOP recovery

| Option | Description | Selected |
|--------|-------------|----------|
| Carry forward Phase 27 D-15..D-18 | Park-at-gap, no destructive ledger revert, owned-paths self-audit, re-locate by content | ✓ |
| Re-derive fresh operational rules | New autonomous handling | |

**Auto-selected:** Carry forward Phase 27 D-15..D-18 (recommended default).
**Notes:** Operational-coordination defaults grounded in CLAUDE.md governance and the Phase 27 audit remediation. Captured as CONTEXT D-13/D-14/D-15/D-16.

---

## Claude's Discretion

- Exact heading names / placement within `ctl_instruction.md` / `pinn_architecture.md` (auditable via canonical refs + before/after notes).
- Acceptance checks as inline commands vs small disposable scripts (Phase 29 builds/executes regardless).
- Exact plan count and wave grouping (constrained by CONTEXT D-04/D-07/D-09/D-12).
- SASD/IPR/PSC evidence-packet filenames, per the evidence README ID->Filename map.

## Deferred Ideas

- Training-loop usage of all four metrics (SASD-weighted collocation/M16, IPR-as-ALM-noise-floor, PSC-governed replay) - doc-03 (OI-10).
- Acceptance-suite build/execution, SI-ledger reconciliation, FUT-01 handoff - Phase 29.
- DataLoader implementation in live `pinn/` code - FUT-01.
- Standard-gold missing-counterpart rerun - separate operational work.
