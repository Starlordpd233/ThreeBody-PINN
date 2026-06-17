# Evidence Packet: IPR - Interpolation Physics Residual

## Header

| Field | Value |
|---|---|
| ID | `IPR` |
| Title | Interpolation Physics Residual units and dual-epsilon contract |
| Severity | `MAJOR` |
| Current Status | `VERIFIED` |
| Current Verdict | `accept-resolution` (raw G=1 units; GAP-28-02 user sign-off 2026-06-16) |
| Phase | Phase 28 |
| Acceptance Check ID | `AC-VAL-03` |
| Spec Sections Touched | `ctl_instruction.md` Step-1A Data-side quality-metric contracts subsection (IPR clause, raw units); `pinn_architecture.md` §3.4 dual-epsilon visibility note |
| Code Paths Touched | Not code-applicable |

## Source Positions

| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` | `§5.3 Q-C3:L627-L673` | Proposes the data-side IPR contract: `CubicHermiteSpline(t, q, dydx=v)`, PCHIP prohibition, deterministic interior points, validation `eps = 1e-10`, stacked residual aggregation, raw `G=1` units, provisional `IPR > 1e-3` flag, and `IPR_train` re-housing for training `eps = 1e-5`. It explicitly calls units the consequential fork and preserves scaled-units dissent. |
| `pinn_instruction/issues/02-data-pipeline-and-validation.md` | `L155-L165` | Describes IPR as a physics residual for a piecewise Cubic Hermite interpolant, but assigns `eps = 1e-5` and an ALM noise-floor training role. This source is non-authoritative and does not settle data-side units. |

Do not treat either primary source as authoritative before user resolution. The resolution doc gives a candidate raw-units answer but marks the unit pin as a consequential fork with a calibration tripwire.

## Spec Evidence

- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md:L160-L174` is the read-only written home of the IPR definition: piecewise cubic Hermite over `(q_i, v_i)`, synthetic points between samples, and squared physics residual against gravity. It does not state raw vs scaled units.
- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md:L220-L252` places IPR in a Phase-1 "Load and Normalize" workflow and gives the `IPR > 10^-3` gate. The phrase "Load and Normalize" prevents the agent from treating "on load" as a clean raw-units proof.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:L930-L935` distinguishes static-invariant `eps_inv = 1e-10` from training-time `epsilon_train = 1e-5`.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md:L520-L535` carries the training Hamiltonian loss denominator and training `epsilon_train = 10^-5`; this grounds the `IPR_train` re-housing target but not the data-side IPR unit convention.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` currently has no `Data-side quality-metric contracts` subsection with an IPR clause. No IPR spec edit has been made in this packet.

### Dataset Evidence (§3b)

- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md:24` (`CLM-09`) records `dt_out` context for base and gold variants.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md:25` (`CLM-10`) records snapshot-count context for base and gold variants.

These rows ground the need for interpolation/aliasing diagnostics but do not decide whether the `1e-3` IPR flag was authored in raw or scaled units.

## FUT-01 Hand-off Note (formerly "Code Evidence")

Live `pinn/` code is not a v1.5 evidence source and was not consulted for this verdict. FUT-01 must implement the eventual user-resolved IPR unit convention and keep data-side IPR distinct from any doc-03 `IPR_train` training-noise-floor metric.

## Verdict

`accept-resolution` (raw G=1 units) — RESOLVED 2026-06-16 via GAP-28-02 user sign-off (Option A). The EDL gold-flag-rate calibration tripwire was inconclusive (both raw-1e-3 and scaled-1e-3 saturate the admitted-set proxy because IPR is dominated by close-encounter under-resolution), so the unit pin rests on grounded convention-consistency: the pipeline computes conservation in raw `G = 1` units (SCOPE-06/07). The IPR clause landed in `ctl_instruction.md` Step-1A; AC-VAL-03 PASS. The original `defer-with-blocker` rationale is retained below for provenance.

The packet could not lock the IPR unit convention without user instruction. The following facts are grounded:

- The construction should use the velocity-carrying cubic Hermite interpolant rather than shape-derived `PchipInterpolator`.
- The data-side validation metric uses the validation softening `eps = 1e-10`; the issue-doc `eps = 1e-5` belongs, if adopted, to a distinct doc-03 `IPR_train` training/noise-floor role.
- IPR is dimensionful. Under locked scaling, acceleration scales as `D/T^2`, so acceleration-squared residuals differ by `D^2/T^4`; with the locked constants this is a factor of about 464 between scaled and raw readings against the same `1e-3` flag.

Those facts do not settle the semantic unit pin. The resolution doc chooses raw units from a placement inference, but DQA's workflow says "Load and Normalize" before listing the static metrics, so the on-load inference cannot be discharged from the cited sources. Because the same `1e-3` threshold has radically different meaning under raw vs scaled units, the IPR clause is parked until GAP-28-02 is resolved or explicitly deferred by the user.

## Before / After Spec Note

Before this packet: no canonical IPR contract existed in editable framework specs. DQA §3.3 and issue-02 carried metric descriptions; the resolution doc carried a candidate raw-units completion and preserved scaled-units dissent.

After this packet: no framework-spec IPR edit has been made. The intended `ctl_instruction.md` IPR clause and `pinn_architecture.md` dual-epsilon visibility note remain parked pending GAP-28-02.

## Named Acceptance Check

`AC-VAL-03`

Phase 28 Plan 03 owns AC-VAL-03, but its runnable structural check is parked with the spec edit. Once GAP-28-02 is resolved, AC-VAL-03 must verify the IPR clause, Hermite/PCHIP construction, validation epsilon, unit-bound gate wording, dual-epsilon `IPR_train` separation, packet citation, and no accidental training-metric conflation.

## Status Transition Log

```text
2026-06-16 aea6747 PENDING -> IN_PROGRESS (Phase 28 Plan 03; IPR EVID-06 packet opened and Q-C3 units fork evaluated)
2026-06-16 aea6747 IN_PROGRESS -> DEFERRED (Phase 28 Plan 03; GAP-28-02 opened for IPR unit-convention sign-off, no spec edit landed)
2026-06-16 ea2af12 DEFERRED -> VERIFIED (Phase 28 Plan 03 resumed; GAP-28-02 RESOLVED-WITH-INSTRUCTION raw G=1 units on grounded convention-consistency; IPR clause landed in ctl Step-1A + arch §3.4 note; AC-VAL-03 PASS; 1e-3 threshold provisional; EDL support FINDINGS.md)
```
