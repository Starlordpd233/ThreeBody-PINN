# Evidence Packet: SCS - Symplectic Conservation Score definition + thresholds

## Header

| Field | Value |
|---|---|
| ID | `SCS` |
| Title | `Symplectic Conservation Score definition + thresholds` |
| Severity | `BLOCKING` |
| Current Status | `PENDING` |
| Current Verdict | `accept-resolution` |
| Phase | `Phase 25 (EVID-10 record) / Phase 28 (VAL-01 edit)` |
| Acceptance Check ID | `AC-VAL-01` |
| Spec Sections Touched | `None (Phase 28 VAL-01 lands the ctl edit)` |
| Code Paths Touched | `Not code-applicable` |

## Source Positions

| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` | `02-resolution-doc.md §5.1 Q-C1:543-574` | Accept the locked post-v1.3 gate verbatim, reject the issue-doc ratio thresholds as a mis-promoted band boundary (`1e-6`) plus an unsourced proposal (`1e-8`). |
| `pinn_instruction/issues/02-data-pipeline-and-validation.md` | `02-data-pipeline-and-validation.md:129-141` | Proposes ratio thresholds: `SCS > 1e-6` reject during Phase-1 screening; `SCS < 1e-8` tighten for high-resolution chaotic-orbit data. Formula given as `SCS = max_t \|H(t) - H(0)\| / \|H(0)\|`. |

The resolution doc's Q-C1 adjudicates the SCS conflict by accepting the locked HC-5 gate verbatim and treating the issue-doc's two numbers as a *diagnostic disposal* rather than a transcription. The `1e-6` is the dqa Acceptable/Marginal band boundary mis-promoted to a reject gate; `1e-8` has no source anywhere in the package.

## Spec Evidence

- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md §3.1` — the **sole written home** of the locked post-v1.3 SCS gate (SI-DQA-003). READ-ONLY (SCOPE-09): citable, NEVER editable. Definition: `ε_H = max_{t∈[0,T]} |(H(t) − H(0)) / H(0)|`, `SCS = log₁₀(ε_H)`, **reject if `SCS > −5`** (equivalently `ε_H > 1e-5`). Non-strict band structure: Excellent `SCS ≤ −10`; Acceptable `−10 < SCS ≤ −6`; Marginal `−6 < SCS ≤ −5` (admitted, flagged for review); Reject `SCS > −5`. The tie `SCS = −5` exactly is Marginal, admitted and flagged (the gate is strict `>`).
- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md §5.1` — gate-on-load placement (Phase-1 screening runs the SCS gate at DataLoader init).
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md §3.4` — the training-side `ε_H = 1e-4·S_H` (distinct glyph, distinct quantity; explicitly NOT this validation gate).
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — transcription target for Phase 28 VAL-01; the editable spec will carry the locked gate's clauses (band table, tie rule, near-zero-`H(0)` quarantine, `ε = 1e-10` Plummer evaluation, storage). Dual-ε note at ~line 703 disambiguates the two `ε_H` quantities.
- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` — **read-only by SCOPE-09**. Phase 28 VAL-01 must create a canonical SCS contract in `ctl_instruction.md` WITHOUT touching DQA. The DQA remains the historical record of the locked gate's sole written home.

### Dataset Evidence (§3b)

- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md` Addendum (DATA-07-CORRECTION-ADDENDUM): **silent on SCS by design** — no CLM row exists for the SCS gate. The conflict is a convention, not a dataset count. This is the expected state: SCS is a metric definition, not a dataset claim, and Phase 24's CLM register correctly contains no SCS row.
- No DATA-05 dependency, no CLM-13 dependency, no probe required for the verdict.

## FUT-01 Hand-off Note (formerly "Code Evidence")

Live code in `pinn/` is NOT a v1.4 or v1.5 evidence source per user directive 2026-05-19. This finding is a spec-convention adjudication; no v1.3-era code path applies. `Not FUT-01-applicable` — the SCS contract is a metric definition consumed by the validation framework, not a code-rewrite gap.

## First-Principles Physics Check

The SCS gate is a conservation-diagnostic on the Brutus integrator's Hamiltonian drift. The dimensionless residual

```
ε_H = max_{t∈[0,T]} |(H(t) − H(0)) / H(0)|
```

measures the maximum normalized Hamiltonian deviation over a trajectory. Under the locked scaling `H' = D·H` uniformly (kinetic and potential both scale as `1/D` when `G = 1, D³ = G·T²`), `ε_H` — and therefore SCS and every band decision — is identical in raw and scaled units (independently re-derived; matches dqa §3.1 placement).

**Independent arithmetic check on the issue-doc numbers (do not just cite the doc):**

- `1e-6` ≡ `SCS = log₁₀(1e-6) = −6` — exactly the Acceptable/Marginal **band boundary** in the locked scheme. Adopting it as a reject gate would purge the entire Marginal band the locked scheme deliberately retains for review. This is a band boundary mis-promoted to a gate, not a different gate.
- `1e-8` ≡ `SCS = log₁₀(1e-8) = −8` — falls inside the Acceptable band, NOT a band boundary in any dqa text. The issue doc's framing (`< 1e-8` "tightening for high-resolution data") has no source anywhere in the package — not a dqa band edge, not a constraint, not a dataset fact. It is an unsourced proposal.
- The locked reject gate `SCS > −5` ≡ `ε_H > 1e-5` is the value that the package has carried since v1.3, and is what `data_quality_assessment.md` §3.1 records. The issue doc's claim that the ratio numbers are "the same physics in different units, just stricter" is arithmetically accurate but incomplete: translated or not, adopting them overrides a locked gate and destroys the Marginal band's design content.

**Verdict grounding is independent of the resolution doc's arithmetic** (D-09): the doc's Q-C1 §1 clause 7 arrives at the same diagnostic disposal, but the grounding here is the band-table re-derivation from dqa §3.1, not a doc citation.

## Verdict

`accept-resolution`

The resolution doc's Q-C1 disposition is correct. The issue doc's `> 1e-6` is the Acceptable/Marginal band boundary wearing a gate's clothes (explains *why* the issue doc landed on that number, but does not authorize it). The `< 1e-8` is an unsourced proposal with no package basis. The locked post-v1.3 gate `SCS = log₁₀(ε_H)`, reject `SCS > −5` (≡ `ε_H > 1e-5`), is the canonical SCS contract. D-09 honored: the verdict is grounded in the band-table re-derivation, the diagnostic disposal matches the doc, but the verdict does not stand on the doc alone.

## Root-Cause Framework Ambiguity

The ambiguity is a **contract-gap in the package's own structure**: the locked SCS gate's sole written home is `data_quality_assessment.md §3.1` (a read-only research report, SCOPE-09), while the issue doc's ratio thresholds were written as if the gate lived in editable specs and was open to numerical re-derivation. The two sources disagree because the package's authorial chain for the gate is single-source (DQA only) and the issue doc author either did not consult DQA or did not recognize the band boundaries as the canonical threshold scheme. Additionally:

- The `1e-6` value is *recognizably* the dqa Acceptable/Marginal boundary, but framed as a reject gate — a misreading of band structure, not a different convention.
- The `1e-8` value has no source in the package; it is a proposed tightening that was never anchored to a dqa band, a dataset fact, or a constraint.

The reconciliation in the resolution doc §5.1 part 7 is a **diagnostic** disposal (recognize what the issue doc's numbers actually are), not a *dismissal* (the issue doc's problem report — that the SCS gate needs a canonical spec home — is real and is the driver of Phase 28 VAL-01).

## Locked Convention

The canonical SCS contract (in spec-edit-ready prose for Phase 28 VAL-01 transcription into `ctl_instruction.md`):

> **SCS definition and gate (HC-5).** `ε_H = max_{t∈[0,T]} |(H(t) − H(0)) / H(0)|`, computed in float64 with the Plummer validation softening `ε = 1e-10` in the potential only. `SCS = log₁₀(ε_H)`. **Reject if `SCS > −5`** (equivalently `ε_H > 1e-5`). Non-strict band structure: Excellent `SCS ≤ −10`; Acceptable `−10 < SCS ≤ −6`; Marginal `−6 < SCS ≤ −5` (admitted, flagged for review); Reject `SCS > −5`. The tie `SCS = −5` exactly is Marginal — admitted and flagged, not rejected (the gate is strict `>`). Edge cases: `|H(0)|` numerically near zero ⇒ SCS undefined ⇒ quarantine for manual review (never patched with a denominator floor); `ε_H = 0` exactly ⇒ `SCS = −∞` ⇒ Excellent. Persist per-trajectory `eps_H`, `SCS`, and the band label; the Stage-4→5 admission gate consumes them. The training-loss symbol `ε_H = 1e-4·S_H` (pinn §3.4) is a distinct quantity and is unaffected by this gate.

Phase 25 makes **zero framework-spec edits** (D-02); the transcription into `ctl_instruction.md` is owned by Phase 28 VAL-01, citing this EVID-10 record by path.

## Which Source Was Correct / Wrong

- **Resolution doc:** correct on the locked gate (constraint-entailed; HC-5 verbatim) and on the diagnostic disposal of the issue-doc numbers (`1e-6` = mis-promoted band boundary; `1e-8` = unsourced).
- **Issue doc:** wrong on both numbers (`1e-6` is a band boundary, not a gate; `1e-8` is unsourced). Correct that the SCS gate needs a canonical editable-spec home — this is what drives Phase 28 VAL-01.
- **DQA (`data_quality_assessment.md` §3.1):** authoritative for the locked gate's definition and band structure; read-only, NEVER editable (SCOPE-09). The transcription target is `ctl_instruction.md`, not DQA.
- **Locked convention (PHYS-05/HC-5):** correct. The `SCS > −5` reject gate is what the package has carried since v1.3 and what the dqa records.

## Before / After Spec Note

**Before:** `ctl_instruction.md` does not contain a canonical SCS contract; the locked gate lives only in the read-only `data_quality_assessment.md §3.1` (SI-DQA-003), and the issue doc's ratio thresholds are unadjudicated.

**After (Phase 28 VAL-01):** `ctl_instruction.md` carries the locked SCS contract — definition, band table, tie rule, near-zero-`H(0)` quarantine, `ε = 1e-10` Plummer evaluation, storage, and the dual-`ε_H` disambiguation note — citing this EVID-10 record. The DQA §3.1 remains the historical record (read-only).

**Accept-resolution as no-change (D-02 / EVID-08 false-positive record):** the **locked gate itself** does not change. The change is a *transcription* from a read-only research report into an editable spec, plus a clarification that the issue doc's two numbers are mis-promoted band boundary (`1e-6`) and unsourced proposal (`1e-8`). No reversal of the locked convention. No overturn of HC-5.

## Named Acceptance Check

`AC-VAL-01`

Phase 28 VAL-01 owns the runnable pass criteria for AC-VAL-01 (verification suggestion per resolution doc §5.1 part 5: bitwise-equal band decisions under raw/scaled units; unit tests for `ε_H = 1e-5` ⇒ Marginal-flagged, `1.0001e-5` ⇒ rejected, `H(0) = 1e-14` ⇒ quarantined, constant-`H` ⇒ `SCS = −∞` Excellent). Phase 25 mints no new AC-IDs (D-13); AC-VAL-01 is the seeded assignment from `24-ISSUE-LEDGER.md`.

## Status Transition Log

```text
2026-06-12 <pending-commit-sha> PENDING -> PENDING (Phase 25 P02 EVID-10 record authored + accept-resolution verdict assigned; fix owned by Phase 28 VAL-01)
```

The final short SHA replaces `<pending-commit-sha>` after the atomic 25-02 commit; the audit label travels in the ledger's per-finding subsection (D-06 same-commit discipline).

**D-14 conditional Dependents:** no shared contract discovered. The SCS gate and the `compute_globals` D convention (D=6.694) both live in ctl but operate on different quantities (Hamiltonian drift diagnostic vs global length scale); no coupling. The `SCS` row's `Dependents:` field is unchanged.
