# Evidence Packet: D=6.694 - compute_globals / D=6.694 convention conflict (CLM-13)

## Header

| Field | Value |
|---|---|
| ID | `D=6.694` |
| Title | `compute_globals / D=6.694 convention conflict (CLM-13)` |
| Severity | `BLOCKING` |
| Current Status | `PENDING` |
| Current Verdict | `accept-resolution` |
| Phase | `Phase 25 (EVID-10 record) / Phase 27 (PIPE-09 edit)` |
| Acceptance Check ID | `AC-PIPE-09` |
| Spec Sections Touched | `None (Phase 27 PIPE-09 lands the ctl edit)` |
| Code Paths Touched | `Not code-applicable` |

## Source Positions

| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` | `02-resolution-doc.md §4.4 Q-B4:493-536` | Reject `D = cbrt(G·M_tot·t_max²) = 6.694`, P1-7, and any `M_tot_ref` parameterization. Lock raw-mass `D = (G·T²)^(1/3) ≈ 4.6416` (HC-6 / PHYS-01). Identify three verified defects in the issue-doc listing (mixed convention, additive-ε anti-pattern, `E_scale` outlier). `E_scale` floor canonicalized at `1e-8` (2-of-3 editable-spec choice, flagged for spec-author sign-off). CLM-13 formal ratification routed to EVID-10/PIPE-09 (OI-11). |
| `pinn_instruction/issues/02-data-pipeline-and-validation.md` | `02-data-pipeline-and-validation.md:235-275,289,306,317` | Proposes `M_tot_ref = 3.0; D = np.cbrt(G * M_tot_ref * t_max**2) # Corrected B-02 scale: D = 6.694 for G=1, M_tot=3, T=10`. The listing scales coordinates by mass-fraction D while computing kinetic and potential energies with **raw** masses, and regularizes the potential with an **additive** `+ eps` distance. P1-7 (line 289) calls for `compute_globals` to be re-run with the corrected `D = 6.694`; P1-7 (line 306) re-appears in the verification checklist; P1-7 (line 317) is mentioned in dataset inventory. |

The issue-doc's *arithmetic* is correct under a mass-fraction convention; its *convention* is the one the locked framework rejects. The listing is internally inconsistent (mass-fraction D with raw-mass energies — dimensionless in neither convention), making the 6.694 instruction, as written, not even a coherent alternative — it is a bug.

## Spec Evidence

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md §2.5` — derives the raw-mass form `D = (G·T²)^(1/3) ≈ 4.6416` (G=1, T=10) and **explicitly rejects** the 6.694 alternative (the mass-fraction form is documented as a future-only rewrite, not a current option). This is the spec evidence that locks the convention (HC-6 / PHYS-01).
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md §2.5` line ~608 — `E_scale = |median(E)| + 1e-10` outlier (the floor value, not the definition). Re-verified by resolution-doc pass; a propagated `eps_inv` value.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` Step-4 table line ~1049 — `E_scale = |median(E)| + 1e-8` (network-facing input contract).
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md §5.2` line ~761 — `E_scale = |median(E)| + 1e-8` (network-facing input contract; matches Step-4).
- **Three-way `E_scale` conflict** (resolution doc §4.4 part 1 clause 3, re-verified): `+1e-10` at `ctl` §2.5 line ~608 (outlier) vs `+1e-8` at `ctl` Step-4 table line ~1049 and `pinn_architecture.md §5.2` line ~761 (network-facing, 2-of-3 majority). The network-facing statement governs on a 2-of-3 editable-spec basis; the `1e-10` is the outlier, plausibly propagated from the adjacent `eps_inv = 1e-10` Plummer softening.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — Plummer `ε_inv = 1e-10` rule ("only in V"); the additive-ε `r_ik = ‖Δr‖ + eps` form in the issue-doc listing is the **PHYS-03 anti-pattern** explicitly prohibited.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` additive-vs-Plummer prohibition with `ε_inv = 1e-10` scope (~line 698).

### Dataset Evidence (§3b)

- `24-VERIFIED-FACTS.md CLM-13` (lines 37, 41): **PENDING — not probed, routed to Phase 25 EVID-10 / Phase 27 PIPE-09**. CLM-13 is a *contested convention*, not a dataset count. The D-05 protocol did not probe it.
- **OI-11 readiness caveat** (from `24.5-READINESS-REPORT.md §4`, propagated per D-16): "CLM-13 formal disposition — PENDING in addendum, routed to EVID-10/PIPE-09. This is an expected routing; the doc is the candidate verdict source for that step." Phase 25 EVID-10 is that step. The disposition recorded here is **`convention-rejected`** — no dataset probe is required because the finding is a convention adjudication, not a count. The verdict rejects 6.694 as a pipeline instruction; CLM-13 is ratified by this EVID-10 record, and the `24-VERIFIED-FACTS.md` CLM-13 row's status moves from PENDING to convention-rejected (carry-forward note for the addendum maintainer; this record is the formal disposition).
- No DATA-05 dependency, no other CLM row affected.

## FUT-01 Hand-off Note (formerly "Code Evidence")

Live code in `pinn/` is NOT a v1.4 or v1.5 evidence source per user directive 2026-05-19. The D=6.694 finding is a spec-convention adjudication; no v1.3-era code path applies. `Not FUT-01-applicable` for this packet — the D convention is a framework contract, not a code-rewrite gap; Phase 27 PIPE-09 transcribes the locked convention into ctl, after which FUT-01 consumes the spec.

## First-Principles Physics Check

Start from Newton's equation:

```
d²r_i/dt² = G Σ_{j≠i} m_j (r_j − r_i) / ‖r_j − r_i‖³
```

Substitute `r = D·r'`, `t = T·u`. Then `d²r_i/dt² = (D/T²) · d²r_i'/du²`, while the force term becomes

```
G Σ_{j≠i} m_j · D(r_j' − r_i') / D³ ‖r_j' − r_i'‖³
```

After multiplying by `T²/D`, the dimensionless equation is

```
d²r_i'/du² = (G·T²/D³) · Σ_{j≠i} m_j · (r_j' − r_i') / ‖r_j' − r_i'‖³
```

The spec's target residual keeps **raw masses** `m_j` with **unit coefficient**, so `G·T²/D³ = 1` and therefore `D³ = G·T²`. This fixes `D = (G·T²)^(1/3) ≈ 4.6416` for `G = 1, T = 10`. **CONFIRMED** (mirroring v1.4 B-02.md lines 63-97; the check is a confirmation of the resolution doc's derivation, not a re-derivation — D-09 grounding discipline).

The issue-doc's `6.694` value corresponds to the **mass-fraction alternative** `D = (G·M_tot·T²)^(1/3)` with the physical total mass `M_tot = 3` used in the issue-doc example. That convention produces the residual coefficient `m_j/M_tot`, so it is a **different framework convention** requiring a framework-wide rewrite of every residual, Hamiltonian, angular-momentum, COM, and invariant formula — not a local scaling correction.

**Arithmetic for 6.694:** `D³ = 1 · 3 · 100 = 300` ⇒ `D = cbrt(300) ≈ 6.694`. CORRECT under the mass-fraction convention. But the convention is the rejected one.

**Half-adoption is concretely harmful:** under a D change, scaled kinetic energy goes as `D⁻²` and potential as `D⁻¹`, so scaled `E` shifts non-uniformly across trajectories, and scaled `E` feeds locked stage thresholds (`E < −0.5`, `|E| < 0.01`) whose meanings would silently change. The issue-doc listing is exactly such a half-adoption (mass-fraction D with raw-mass energies), confirming its listing is internally inconsistent.

## Verdict

`accept-resolution`

The locked raw-mass convention `D = (G·T²)^(1/3) ≈ 4.6416` (HC-6 / PHYS-01) is constraint-entailed by the framework's target residual. The issue doc's `D = 6.694` is arithmetically correct under a mass-fraction convention rewrite, but treating it as a local formula correction (the issue doc's framing) is wrong: it is a framework-wide convention migration. The issue-doc listing is internally inconsistent (mass-fraction D with raw-mass energies), making the 6.694 instruction, as written, not even a coherent alternative. `ctl_instruction.md §2.5` explicitly rejects the 6.694 form. D-09 honored: the verdict is grounded in the dimensional analysis + the ctl §2.5 rejection + the listing's verified defects, not on the resolution doc's recommendation alone.

**OI-11 propagation (D-15, D-16):** the CLM-13 row in `24-VERIFIED-FACTS.md` is **formally ratified by this EVID-10 record**. Disposition: `convention-rejected` (raw-mass D stands; 6.694 is not a pipeline instruction). No dataset probe is required (convention, not a count). The OI-11 readiness caveat from `24.5-READINESS-REPORT.md §4` is propagated into this ratification note.

**STOP guard (D-09):** adopting 6.694 would overturn PHYS-01/HC-6 — that is a STOP gap, not an autonomous verdict. The candidate source REJECTS 6.694, and independent grounding reaches the same conclusion. No overturn; no gap.

## Root-Cause Framework Ambiguity

The ambiguity is a **convention choice** (raw mass vs mass fraction) that was implicit in the framework before PHYS-01 locked it (Phase 20). The issue doc's framing of the 6.694 form as a "corrected B-02 scale" is a **misdiagnosis**: B-02 (and its v1.5 analogue D=6.694) is a *convention identifier*, not a *formula error*. The locked framework uses raw masses everywhere, so the locked `D` is the raw-mass form. The mass-fraction form would require:

1. Replacing every `m_j` with `m_j/M_tot` in every residual, Hamiltonian, angular-momentum, COM, and invariant formula.
2. Re-deriving stage thresholds (`E < −0.5`, `|E| < 0.01`) under the new scaling.
3. Recomputing normalizers (`E_scale`, `r_char`, `Q_scale`).
4. Regenerating processed stores.
5. Retraining the network.

The issue doc did not propose (1)–(5); it proposed the 6.694 D as a local fix. That is the root cause: a convention change treated as a formula correction.

Additionally, the issue-doc listing has **three verified defects** (resolution doc §4.4 part 1 clauses 1-3, all re-verified by the resolution pass):

1. **Mixed convention:** mass-fraction D with raw-mass energies — dimensionless in neither convention.
2. **Additive-ε anti-pattern:** `r_ik = ‖Δr‖ + eps` is the exact PHYS-03 anti-pattern; the invariant `V` must use the Plummer form `√(‖Δr‖² + ε_inv²)` with `ε_inv = 1e-10`, and ε enters `V` only.
3. **`E_scale` outlier:** the listing reads `+1e-8` (matches Step-4 and pinn_architecture), but ctl §2.5 line ~608 reads `+1e-10` — a 2-of-3 conflict. The network-facing 2-of-3 majority (`+1e-8`) governs; the `+1e-10` is propagated from the adjacent `eps_inv`.

## Locked Convention

The canonical D convention (in spec-edit-ready prose for Phase 27 PIPE-09 transcription into `ctl_instruction.md §2.5`):

> **Global-scale D (HC-6 / PHYS-01).** `D = (G·T²)^(1/3) ≈ 4.6416` for `G = 1, T = 10`. Raw masses are used throughout the framework (kinetic and potential both scale as `1/D` under the locked scaling, so `H' = D·H` is unit-invariant). The mass-fraction alternative `D = (G·M_tot·T²)^(1/3) = 6.694` (with `M_tot = 3`) is **rejected as a pipeline instruction** and remains documented as a future-only rewrite requiring a framework-wide migration (every residual, Hamiltonian, invariant, COM formula; stage thresholds re-derived; normalizers recomputed; processed stores regenerated; network retrained). No configuration parameter may select the mass-fraction form; a configuration path whose non-default branch produces a constraint-violating convention is a standing footgun. **`E_scale` floor:** `E_scale = |median(E)| + 1e-8` (canonicalizes the Step-4 table and `pinn_architecture.md §5.2` value; the `+1e-10` at ctl §2.5 line ~608 is an outlier propagated from the adjacent `eps_inv`). **Plummer form (PHYS-03):** the potential regularizes with `r_safe = sqrt(r² + ε_inv²)`, `ε_inv = 1e-10`, ε enters `V` only. **Additive `+ eps` on the distance norm is the PHYS-03 anti-pattern and is prohibited.** **`compute_globals` scope:** evaluates per-IC energies with raw masses over the **admitted set** (post-Step-1A, post-blacklist, post-DATA-05-quarantine) — a documented minor judgment flagged for spec-author sign-off; medians make it nearly equivalent to all-files computation, but the admitted-set choice is deterministic and immune to NaN poisoning from corrupt or stale records.

Phase 25 makes **zero framework-spec edits** (D-02); the transcription into `ctl_instruction.md §2.5` is owned by Phase 27 PIPE-09, citing this EVID-10 record by path. The `E_scale = 1e-8` canonicalization is a **Phase 27 edit decision** (2-of-3 editable-spec choice), NOT a Phase 25 verdict — it is recorded here in prose so Phase 27 PIPE-09 can transcribe it without re-deriving the 2-of-3 rule.

## Which Source Was Correct / Wrong

- **Resolution doc:** correct on dimensional grounds (raw-mass residual) and on the final locked convention. Correct on the three verified defects (mixed convention, additive-ε, `E_scale` outlier). Correct that CLM-13 ratification is this EVID-10 step.
- **Issue doc:** arithmetic right (6.694 is the cbrt(300) under M_tot=3), convention wrong (the mass-fraction form is the rejected one). Listing has 3 verified defects that independently falsify the listing as a pipeline instruction.
- **Locked convention (PHYS-01/HC-6):** correct. Raw-mass `D = (G·T²)^(1/3) ≈ 4.6416` is the unique choice that yields a unit-coefficient dimensionless residual with raw masses.
- **DQA / `data_quality_assessment.md`:** not applicable to this finding (DQA covers validation metrics, not global-scale D).

## Before / After Spec Note

**Before:** `ctl_instruction.md §2.5` carries the raw-mass `D ≈ 4.6416` derivation and an explicit 6.694 rejection, but the `E_scale` floor at ctl §2.5 line ~608 reads `+1e-10` (outlier vs the 2-of-3 `+1e-8` at Step-4 and `pinn_architecture.md §5.2`); the Plummer `ε_inv = 1e-10` rule and the additive-ε prohibition are stated but not consolidated into a normative `compute_globals` contract; the `M_tot_ref` parameterization is not explicitly prohibited at the configuration level.

**After (Phase 27 PIPE-09):** `ctl_instruction.md §2.5` carries the locked global-scale D convention (HC-6 / PHYS-01), the `E_scale` floor is canonicalized at `+1e-8` (2-of-3 editable-spec majority, the `+1e-10` outlier replaced), the Plummer-vs-additive-ε rule is restated as the `compute_globals` contract, the `M_tot_ref` knob is explicitly prohibited as a configuration parameter, and the admitted-set scope rule is recorded. Citing this EVID-10 record by path.

**Accept-resolution as no-change (D-02 / EVID-08 false-positive record):** the **locked D value itself** does not change. The change is consolidation of the existing spec text into a normative `compute_globals` contract, the `E_scale` floor canonicalization, and the `M_tot_ref` prohibition. No reversal of the locked convention. No overturn of HC-6.

## Named Acceptance Check

`AC-PIPE-09`

Phase 27 PIPE-09 owns the runnable pass criteria for AC-PIPE-09 (verification suggestion per resolution doc §4.4 part 5: dimensional-consistency unit test on analytic two-body circular orbit; static grep for `6.694`/`M_tot` inside any `D` computation and for additive-ε potentials; recompute `E_scale` on the admitted set under the locked convention and archive with §2.6 metadata). Phase 25 mints no new AC-IDs (D-13); AC-PIPE-09 is the seeded assignment from `24-ISSUE-LEDGER.md`.

## Status Transition Log

```text
2026-06-12 <pending-commit-sha> PENDING -> PENDING (Phase 25 P02 EVID-10 record authored + accept-resolution verdict assigned; CLM-13 ratified convention-rejected; fix owned by Phase 27 PIPE-09)
```

The final short SHA replaces `<pending-commit-sha>` after the atomic 25-02 commit; the audit label travels in the ledger's per-finding subsection (D-06 same-commit discipline). The CLM-13 ratification note (OI-11) is the formal disposition of the `24-VERIFIED-FACTS.md` CLM-13 row (carry-forward to the addendum maintainer).

**D-14 conditional Dependents:** no shared contract discovered. The D=6.694 conflict concerns the global length scale; the SCS gate concerns Hamiltonian drift diagnostics. Both live in ctl §2.5 / ctl Mini-Batch Construction, but operate on different quantities (length vs diagnostic) with no shared coupling. The `D=6.694` row's `Dependents:` field is unchanged.
