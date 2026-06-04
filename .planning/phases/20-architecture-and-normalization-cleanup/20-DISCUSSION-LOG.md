# Phase 20: Architecture and Normalization Cleanup - Discussion Log

> Audit trail only. Do not use as input to planning, research, or execution agents.
> Decisions are captured in `20-CONTEXT.md`; this log preserves alternatives considered.

**Date:** 2026-06-03
**Phase:** 20 - Architecture and Normalization Cleanup
**Areas discussed:** SIREN / omega0, LayerNorm, Inertia descriptors, Support ranges, Evidence / gap handling

---

## SIREN / omega0

| Option | Description | Selected |
|--------|-------------|----------|
| Evidence-first removal | Use Phase 16 ledger/protocol, create/consult B-01 and B-10, cite both primary sources, then clean only supported text. | yes |
| Direct cleanup | Use `ARCH-01`/roadmap directly with source citations in the task. | |
| Preserve with warning | Keep scheduler as non-runtime/stale historical context. | |

**User's choice:** Evidence-first removal.
**Notes:** Active wording should lock `first_omega_0=30`, `hidden_omega_0=1`, standard SIREN initialization, hidden-layer bounds divided by `hidden_omega_0`, no epochwise/optimizer-step scheduler, and stage-boundary ablation only with fresh initialization. Cleanup covers all active/normative SIREN/init/frequency surfaces in `pinn_architecture.md`. `AC-ARCH-01` closure requires B-01/B-10 packets plus post-edit surface and negative scheduler audits.

---

## LayerNorm

| Option | Description | Selected |
|--------|-------------|----------|
| Ledger/evidence-gated | Use M8, cite both primary sources, record verdict before edits, update AC-ARCH-02 proof. | yes |
| Direct cleanup from ARCH-02 | Use roadmap/requirement with source citations in the task. | |
| Minimal wording only | Avoid deciding affine/non-affine default. | |

**User's choice:** Ledger/evidence-gated.
**Notes:** Target wording, if M8 confirms it, is project-specific/author skip-path stabilizer, not original SQR-SkipResNet content, default `elementwise_affine=False`, and affine/removal only as optional future ablations. Cleanup covers all active LayerNorm surfaces. `AC-ARCH-02` closure requires M8 plus source/surface audit and negative contradictory-text audit.

---

## Inertia descriptors

| Option | Description | Selected |
|--------|-------------|----------|
| STOP-protocol adjudication task | Treat M5 / `I_3` as contested and gated by EVID-05. | yes |
| Use resolution as default | Adopt resolution unless issue doc disproves it. | |
| Surface now as blocker | Stop all planning before artifacts. | |

**User's choice:** STOP-protocol adjudication task.
**Notes:** M5 must use the full Phase 16 verdict enum. Downstream `I_3` edits are gated by the selected verdict. Raw-vs-tanh `I_norm` naming is `ARCH-04`, separate from M5 / `ARCH-03`. If no evidence/proof vehicle exists for `ARCH-04`, record a process gap instead of inventing one or attaching it to M5. Split proof trails: M5 / `AC-ARCH-03` only closes `I_3`; `ARCH-04` needs its own vehicle.

---

## Support ranges

| Option | Description | Selected |
|--------|-------------|----------|
| Evidence/proof-gated | Use M9/M10, cite primary sources, current spec, and dataset docs, then edit supported wording. | yes |
| Direct cleanup from ARCH-05 | Use the requirement directly. | |
| Defer to Phase 21 | Leave proof to final acceptance/handoff. | |

**User's choice:** Evidence/proof-gated.
**Notes:** Target framing is realized dataset support, not universal physics bounds and not a normalizer defect. Cleanup covers every active support-range surface. M9 and M10 remain separate evidence/verdict records, while a combined support-range audit may prove shared `AC-ARCH-05` closure after both verdicts.

---

## Evidence / gap handling

| Option | Description | Selected |
|--------|-------------|----------|
| Separate actual Phase 20 artifacts | Use `.planning/phases/20-architecture-and-normalization-cleanup/`; leave Phase 20.5 untouched. | yes |
| Reuse `20-5` directory | Put actual Phase 20 artifacts in Phase 20.5 directory. | |
| Stop as tooling blocker | Wait for GSD tooling fix before context/research. | |

**User's choice:** Separate actual Phase 20 artifacts.
**Notes:** Treat the GSD `20 -> 20-5` mis-resolution as an operational tooling hazard, not a Phase 20 blocker. Use explicit paths. Missing proof vehicles are process-artifact schema gaps, not opportunities to invent packet names. EDL is only for source-silent empirical questions after a STOP gap.

---

## Deep Review Decisions (2026-06-03)

Three decisions made during plan review to correct anchoring bias, source-grounding gaps, and vocabulary scope.

### D-09: "Realized Support" Is Planning Shorthand, Not Spec Vocabulary

| Option | Description | Selected |
|--------|-------------|----------|
| Use issue-doc language in spec prose | Spec says "E_norm occupies [-1, 0) for bound systems; positive range unused; acceptable for SIREN" and "hierarchical m_norm asymmetry carries mass hierarchy information" | yes |
| Keep "realized support" as spec term | Introduce the statistical-learning vocabulary formally into framework specs | |

**User's choice:** Use issue-doc language as canonical spec wording; "realized support" remains planning/acceptance shorthand only (labels the ARCH-05 objective in D-06, Phase 16 ledger, roadmap success criterion, but is NOT a new technical term in the framework spec).

### D-10: I₃ Derivation Moved to Research to Protect Adjudication Neutrality

| Option | Description | Selected |
|--------|-------------|----------|
| Move derivation to 20-RESEARCH.md | Store as conditional lemma; executor consults only after Step 4 source-definition comparison | yes |
| Keep in plan with guardrail | Keep in Step 5 but add explicit instruction about ratio-form-only applicability | |
| Keep as-is | Rely on existing safeguards (Step 4, STOP conditions, autonomous:false) | |

**User's choice:** Move to research. The executor must compare source definitions before seeing any derivation, to avoid anchoring bias toward accept-resolution.

### D-11: 20-04 Remains autonomous:true

| Option | Description | Selected |
|--------|-------------|----------|
| Keep autonomous:true | M9/M10 are not EVID-05 contested; D-06 is a locked decision; STOP conditions have deterministic safe defaults | yes |
| Set to autonomous:false | The framing choice is potentially semantic | |

**User's choice:** Keep autonomous:true. Unlike M5, M9/M10 are not flagged Sources-Disagree/EVID-05, and the only judgment ("can this be grounded?") has a deterministic safe default (record a 20-GAPS entry, halt Task 2, surface to user).

---

## the agent's Discretion

- Research artifact organization may use tables and route maps as long as it stays implementation-ready and avoids redesign/ablation exploration.

## Deferred Ideas

- Any empirical ablation or performance-choice research for `omega0`, LayerNorm, `I_norm`, or new support ranges is deferred unless a logged STOP/EDL gap requires support.
