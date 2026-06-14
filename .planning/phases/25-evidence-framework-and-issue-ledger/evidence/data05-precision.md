# Evidence Packet: DATA-05 / mass-drift - Precision Handling (float64 sufficiency; Decimal-as-classifier)

> **Pointer packet (GAP-27-01 Option C, 2026-06-13).** This is a thin pointer packet: the
> DATA-05 precision verdict was already adjudicated and empirically resolved in **Phase 24**
> (`GAP-24-01` RESOLVED-WITH-INSTRUCTION + the validated 70/70 rerun remediation). This packet
> satisfies the EVID-06 packet-before-edit gate for the PIPE-07 (`AC-PIPE-07`) spec edit by
> **citing** the Phase 24 artifacts as the verdict source. It does **not** re-derive or
> re-adjudicate DATA-05. EVID-10 is **not triggered** (the two primary sources do not disagree
> on the precision decision; the only nearby contested convention, `D = 6.694`, is a separate
> ledger row routed to PIPE-09 / `compute-globals-D.md`).

## Header

| Field | Value |
|---|---|
| ID | `mass-drift` / `DATA-05` (PIPE-07 precision facet) |
| Title | Precision Handling — float64 sufficiency; `decimal.Decimal` as mass-gate failure classifier |
| Severity | `MINOR` (precision-policy codification; the substantive data fix — 70 stale base-hier outputs — was remediated in Phase 24) |
| Current Status | `VERIFIED` (AC-PIPE-07 PASS; Phase 27 P02; same-commit discipline with ctl §2.1 edit + ledger transition) |
| Current Verdict | `accept-resolution` |
| Phase | `Phase 27` (verdict source: `Phase 24`) |
| Acceptance Check ID | `AC-PIPE-07` |
| Spec Sections Touched | `ctl_instruction.md` §2.1 mass-invariance gate (precision note to be appended; planned, not yet landed). `pinn_architecture.md` None (data-side per CONTEXT D-02/D-04). |
| Code Paths Touched | `Not code-applicable` (framework-spec + process artifact; live `pinn/` rewrite is FUT-01) |

## Source Positions

| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` | §4.3 Q-B3 `:92`; Q-B2 `:91`; Cluster A/B `:68,:70` | float64 is sufficient for all data-side validation metrics and invariants; `decimal.Decimal` is mandated **only** as the Q-B2 IC↔Brutus `t=0` mass-gate failure classifier (never the routine parse/metric path). The 70 base-hierarchical mismatches are a genuine, enumerated **staleness** phenomenon (not text-precision); current ICs are canonical; the 70 stale outputs are quarantined pending rerun. (Confidence High; unanimous among addressers.) |
| `pinn_instruction/issues/02-data-pipeline-and-validation.md` | `:204`, `:208-216`, `:292`, `:343` | float64 is acceptable for validation metrics (`:212`), but proposes: if the IC↔Brutus `t=0` mass comparison mismatches at `rtol=1e-15`, **"retain `decimal.Decimal` parsing for mass values"** (`:214`, `:204`, P2-2 `:292`). Treats a detected mismatch as a text-rounding/precision problem to be solved by Decimal parsing — the remedy DATA-05 empirically disproved. |

BOTH citations recorded per D-04 §2 (required even for an uncontested verdict).

## Spec Evidence

Current framework-spec convention being clarified/extended:

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` §2.1 mass-invariance gate (≈`:560-576`) — parses in float64; `max_{t,i} |m_i(t) − m_i(0)| < 1e-15` float64 **absolute**; folds in the IC↔Brutus `t=0` consistency clause. The PIPE-07 precision note (float64-sufficiency rationale + Decimal-as-classifier scope) is to be **appended after §2.1** by the Phase 27 PIPE-07 plan; this is net-new but short prose, not a convention change.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — None (precision/parsing is a data-pipeline concern with no architecture surface; CONTEXT D-02/D-04).

### Dataset Evidence (§3b)

- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` **DATA-05 row** (`:31-35`): `data05_mass_drift.py` probe — **70/4,857** base-hier mismatches (`m_IC ≠ m_Brutus(t=0)` at `np.allclose(rtol=1e-15)`); **0/4,857** gold-hier; **0/2,749** base-std; **0/2,565** gold-std; total compared **15,028**, total mismatch **70**. Differences are **0.1–1.0 mass units** (e.g. id 5: 0.9056 vs 1.2569, Δ≈0.351) — orders of magnitude too large for a float64 round-trip (`:94`), so precision does not explain them. Affected IDs `0005`–`0059`, `0061`–`0075` (55 + 15 = 70). Verdict **corrected / RESOLVED-WITH-INSTRUCTION**: current ICs canonical; the 70 stale base-hier outputs quarantined from training/metrics/PIPE-07 pending rerun. Run 2026-06-11.
- Remediation + validation (verdict-of-record): `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-DATA05-RERUN-REMEDIATION.md` and `24-DATA05-RERUN-VALIDATION.md` — the 70 affected IDs were re-simulated from the current canonical ICs; **70/70 reruns satisfy `m_IC == m_Brutus(t=0)` at float64**, all gates passed, the swap was user-approved, the post-swap DATA-05 probe returns **0/4857**, and the old artifacts were archived under `simulation_data/Data/forensic/data05_gap24-01_old_outputs/`.

## FUT-01 Hand-off Note (formerly "Code Evidence")

Not v1.5 evidence — forward-pointing only. The FUT-01 DataLoader/metrics rewrite must implement the locked precision contract: parse and compute all data-side validation metrics and invariants in CPU `float64`; reserve `decimal.Decimal` solely for the IC↔Brutus `t=0` mass-gate escalation classifier (3 scalar masses per trajectory) — never for the routine parse or metric path. No v1.3-era code path is cited as a basis for this verdict (live `pinn/` is not grounding, directive 2026-05-19).

## First-Principles Physics Check

> Optional — **EVID-10 not triggered** (Sources Disagree? = NO). No physics adjudication is performed here. The decisive numerical fact (the 70 mismatches are 0.1–1.0 mass units, ≫ the ~1e-15 relative reach of a float64 round-trip, hence not a precision artifact) is already established and re-derivable in `24-VERIFIED-FACTS.md` DATA-05 (`:94`) and was confirmed by the 70/70 post-rerun float64 mass-equality validation. Not re-derived here per the GAP-27-01 Option-C pointer-packet instruction.

## Verdict

`accept-resolution`

The resolution document's position — float64 is sufficient for all data-side metrics/invariants, and `decimal.Decimal` is reserved exclusively as the IC↔Brutus `t=0` mass-gate failure classifier — is accepted after **independent empirical verification**: Phase 24's full-population scan (15,028 pairs) found the 70 base-hier mismatches to be a **staleness** phenomenon (0.1–1.0 mass units, not a 1e-15 text-rounding effect), and the targeted rerun validated **70/70** at float64 mass equality. The issue doc's contrary remedy ("retain `Decimal` parsing for mass values" when a mismatch is detected) is rejected: the mismatch was not a precision/text-rounding problem, so Decimal parsing would not have fixed it — re-simulation from the current canonical ICs did. Reason is linked to the Source Positions (resolution-doc §4.3 Q-B3 / Q-B2), the current §2.1 spec gate, and the DATA-05 dataset evidence + 70/70 rerun validation above.

## Root-Cause Framework Ambiguity

> Optional — **EVID-10 not triggered.** N/A: the two primary sources do not disagree on the precision *convention* (both accept float64 for metrics). They differ only on the *remedy* for a detected IC↔Brutus mass mismatch, and DATA-05 settled that empirically (staleness, not precision). No framework-spec ambiguity enabled a genuine source conflict.

## Locked Convention

float64 is the data-side precision contract for all validation metrics and invariants. `decimal.Decimal` is used **only** as the failure classifier for the IC↔Brutus `t=0` mass-consistency gate (`max_i |Δm_i| < 1e-15`, float64 absolute), never as the routine parsing or metric-computation path. Current IC masses are canonical; a future IC↔Brutus mass-gate mismatch is a **fail** condition for the affected trajectory (quarantine), not a trigger to switch the metric path to Decimal. (Spec-ready prose lands in the Phase 27 `ctl_instruction.md` §2.1 precision note; transcribed here as a pointer, not re-derived. Anchor: resolution-doc §4.3 `:481-489`, Q-B3 `:92`.)

## Which Source Was Correct / Wrong

- **Resolution doc — correct** on the convention (float64 sufficient; Decimal only as the mass-gate classifier) and on the diagnosis (the 70 mismatches are stale artifacts, not precision).
- **Issue doc — partly correct, partly wrong:** correct that float64 is adequate for validation metrics (`:212`); **wrong** that a detected IC↔Brutus mass mismatch should be remedied by retaining `decimal.Decimal` mass parsing (`:214`, `:204`, P2-2 `:292`) — DATA-05 showed the mismatch was staleness, fixed by re-simulation, not by higher-precision parsing.

## Before / After Spec Note

- **Section:** `ctl_instruction.md` §2.1 (mass-invariance gate) — precision note appended.
- **Before:** §2.1 states the float64 `1e-15` absolute mass-invariance gate and IC↔Brutus consistency clause, but does not explicitly state the float64-sufficiency rationale for data-side metrics or scope `decimal.Decimal` to the mass-gate classifier only.
- **After:** §2.1 carries an explicit precision note: float64 sufficient for all data-side metrics/invariants; `decimal.Decimal` reserved as the mass-gate failure classifier only; current ICs canonical; stale-artifact (not precision) interpretation of historical mismatches; fail condition for any future mass-gate mismatch.
- This is an **additive clarification**, not a convention change; the existing §2.1 gate is preserved verbatim.

## Named Acceptance Check

`AC-PIPE-07` (seeded; no new AC ID — D-06). Runnable pass criteria are authored by the Phase 27 PIPE-07 plan and executed in Phase 27 / re-run in Phase 29. Intended assertion: the §2.1 precision note states float64 sufficiency + Decimal-only-as-classifier + current-ICs-canonical + stale-not-precision interpretation + a future-mass-gate fail condition, and cites the Phase 24 DATA-05 rerun remediation/validation; negative control — `decimal.Decimal` does NOT appear as the routine parse/metric path.

## Status Transition Log

Each entry: `date`, `commit short SHA`, `status transition`, `actor / plan reference`.

```text
2026-06-13 09e37f8 PENDING -> PENDING (Phase 27 /gsd-plan-phase; data05-precision pointer packet authored + accept-resolution verdict assigned via pointer to Phase 24 DATA-05 artifacts; GAP-27-01 Option C, user instruction)
2026-06-14 <pending-27-02-sha> PENDING -> IN_PROGRESS (Phase 27 P02; evidence packet linked from ledger mass-drift/footer rows, ctl_instruction.md §2.1 precision-note edit prepared)
2026-06-14 <pending-27-02-sha> IN_PROGRESS -> FIX_APPLIED (Phase 27 P02; ctl_instruction.md §2.1 precision note appended; AC-PIPE-07 authored and executed)
2026-06-14 <pending-27-02-sha> FIX_APPLIED -> VERIFIED (Phase 27 P02; AC-PIPE-07 PASS — float64 sufficiency + Decimal-only-as-classifier + stale-not-precision + DATA-05 citation confirmed; D7 regression AC-PIPE-06 PASS; mass-drift and footer rows VERIFIED)
```

> Forward transitions `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED` are applied by the **Phase 27 PIPE-07 plan execution**, in the same commit as the `ctl_instruction.md` §2.1 precision-note edit, the `24-ISSUE-LEDGER.md` mass-drift/footer-row Evidence-Packet link + status edit, and the passing `AC-PIPE-07` check (same-commit discipline, evidence/README.md `:101`). The `<commit-pending>` SHA above is backfilled with this packet's authoring commit short SHA.
