# Phase 27: Sampling, Precision, and Global-Scale Contracts - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-06-13
**Phase:** 27-sampling-precision-and-global-scale-contracts
**Areas discussed:** Spec-edit strategy and boundaries, Evidence and ledger workflow, Acceptance checks and regression surface, Planning order and batching
**Mode:** `--all --auto` - Codex auto-selected the recommended default for each gray area per user instruction, then stopped before planning.

---

## Spec-edit strategy and boundaries

| Option | Description | Selected |
|--------|-------------|----------|
| Use locked SPEC + Phase 25 packets as constraints | Transcribe locked Phase 27 contracts; stop on any source-silent semantic/process gap. | yes |
| Reopen candidate verdict choices | Re-adjudicate M12, Decimal policy, and D convention during planning. | no |
| Broaden edit targets | Include `sampling_method.md`, read-only DQA, or live `pinn/` behavior. | no |

**User's choice:** Auto-selected recommended default.
**Notes:** Requirements are locked by `27-SPEC.md`; discussion is implementation/process only.

---

## Evidence and ledger workflow

| Option | Description | Selected |
|--------|-------------|----------|
| Reuse Phase 25 lifecycle and seeded AC IDs | Use existing evidence packets/artifacts, existing ledger rows, and AC-PIPE-04/07/08/09 only. | yes |
| Create new process schema as needed | Mint new acceptance IDs, packet structures, or lifecycle states. | no |
| Skip ledger transitions until phase end | Make spec edits first, then reconcile ledger later. | no |

**User's choice:** Auto-selected recommended default.
**Notes:** If a required packet mapping or process artifact is missing, the correct behavior is a process-schema STOP gap.

---

## Acceptance checks and regression surface

| Option | Description | Selected |
|--------|-------------|----------|
| Define per-contract checks before verification | AC-PIPE-04/07/08/09 each name exact spec evidence, data evidence, and pass/fail command or check. | yes |
| Treat SPEC text as sufficient | Mark rows verified once the spec text is edited. | no |
| Run broad unrelated checks | Expand verification beyond touched/shared contracts. | no |

**User's choice:** Auto-selected recommended default.
**Notes:** Previously verified Phase 26 rows are rechecked only where Phase 27 edits touch shared sections or dependents.

---

## Planning order and batching

| Option | Description | Selected |
|--------|-------------|----------|
| M12/G5 -> precision -> stage-query -> compute_globals | Handle dependency-shaped contracts first, keep isolated global-scale cleanup last, and keep batches reviewable. | yes |
| One large monolithic plan | Edit all four contracts and all ledger rows in one broad change. | no |
| Plan downstream training policy now | Include M16/doc-03, Phase 28 metrics, or FUT-01 implementation choices. | no |

**User's choice:** Auto-selected recommended default.
**Notes:** The planner may batch adjacent contracts only if acceptance checks and ledger transitions remain auditable.

---

## Codex's Discretion

- Exact heading placement in `ctl_instruction.md` / `pinn_architecture.md`.
- Exact plan count and wave grouping.
- Whether acceptance checks are inline commands or disposable Phase 27 scripts.

## Deferred Ideas

- M16 collocation-density and training-loop sampling policy - doc-03 milestone.
- SCS/SASD/IPR/PSC validation metrics - Phase 28.
- Acceptance-suite build, SI-ledger reconciliation, and final handoff - Phase 29.
- FUT-01 live `pinn/` implementation.
