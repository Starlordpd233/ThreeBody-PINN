---
status: active
purpose: other
created: 2026-06-20
milestone: v1.6
phase: resolution-doc-readiness
retirement_trigger: Phases 32–36 closed; resolution doc no longer the active candidate verdict source
---

# Phase 31 Resolution-Doc Quick-Reference Map

Navigation aid for Phases 32–36 (EVID / CURR / LOOP / LOSS / VER). Lets the adjudication
phases locate verdicts, cite the resolution doc, and preview verdict direction **without
reading the full 282-line doc first.**

## Resolution-doc identity

- **Path (verbatim):**
  `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md`
- **Length:** 282 lines (48,049 bytes).
- **Committed revision:** `49fb7958` (2026-06-20). Line numbers in this map are anchored to
  that revision; §/finding-ID anchors are stable across re-pagination, line numbers are not.
- **Standing:** Candidate verdict source for Phases 32–36 — the same standing
  `ctl_pinn_resolution.md` held in v1.4 and `02-resolution-doc.md` held in v1.5. NOT
  authoritative; verdicts are Phase 32's to assign via EVID-11..15. The doc itself records
  (§0, lines 8–21) that it "follows the source hierarchy: locked SCOPE-12 constraints, then
  the framework specs as revisable baseline, then verified grounding companions, then the
  non-authoritative issue document and baseline design reports" and that "claimed-unverified
  figures remain proposals, not facts."
- **Nature:** A single coherent consolidation with §0–§7 structure and 18 per-finding
  subsections (§1.1–§1.18), each carrying a one-word disposition tag in its heading
  (`surface_to_user` / `modified` / `accepted` / `rejected` / `defer`). No competing
  top-level numbering; §6 explicitly notes non-independent inputs handled by claim-collapsing
  rather than weighting.

## 1. Section index

Captured by `grep -nE "^#{1,4} "` against the committed doc. Ranges are start-of-heading to
line-before-next-heading; the doc is 282 lines total.

| § | Lines | Covers |
|---|-------|--------|
| Title | 1–7 | Document identity, status ("final adjudication from the attached bundles only"), date, spec-edit targets, evidence boundary |
| §0 | 8–21 | Adjudication method — source hierarchy (SCOPE-12 → framework specs → verified companions → non-authoritative issue/baseline), the 81-claim independent ledger frozen before the reports bundle was opened, disposition-word meanings (`accepted` / `rejected` / `modified` / `surface_to_user` / `defer`) |
| §1 | 22–23 | "Final Issue 03 resolutions" — section opener |
| §1.1 | 24–27 | **D-04** Causal-training mode — `surface_to_user` |
| §1.2 | 28–31 | **D-05** `s_min` frame — `surface_to_user` |
| §1.3 | 32–35 | **D-06** Epsilon strategy — `surface_to_user` |
| §1.4 | 36–39 | **B-07** replay/lookahead batching — `modified` |
| §1.5 | 40–43 | **B-08** data versus collocation points — `modified` |
| §1.6 | 44–47 | **M6** `L_norm` clamping — `modified` |
| §1.7 | 48–51 | **M7** `tau_L` exclusion from `IC13` — `accepted` |
| §1.8 | 52–55 | **M14** gradient clipping — `modified` |
| §1.9 | 56–59 | **M15** energy-loss weights — `rejected` as an issue-doc replacement |
| §1.10 | 60–63 | **M16** `dt_out`-aware collocation scaling — `defer` |
| §1.11 | 64–67 | **D5** stage transitions — `modified` |
| §1.12 | 68–71 | **NS-12** componentwise automatic differentiation — `accepted` |
| §1.13 | 72–75 | **NS-13** energy Huber delta — `defer` |
| §1.14 | 76–79 | **NS-18** loss scaling and units — `modified` |
| §1.15 | 80–83 | **adaptive stage assignment** (CURR-01) — `modified` |
| §1.16 | 84–87 | **D = 6.694 conflict** — `accepted` for `4.6416`, `rejected` for `6.694` |
| §1.17 | 88–91 | **`L_max` / `tau_L` formulas** (CURR-02) — `modified` / `surface_to_user` |
| §1.18 | 92–95 | **ALM `mu_p` clamp** (LOOP-05) — `defer` |
| §2 | 96–183 | Claim matrix — 81-row machine-readable ledger mapping claim → disposition + canonical-source basis + supporting/opposing R#-reports + uncertainty type |
| §3 | 184–212 | Disagreement register — 22 `DGR-xx` rows retaining every material conflict and minority position ("agreement was not treated as evidence") |
| §4 | 213–238 | Gap register — 19 `GAP-xx` rows, "no source-silent or ambiguous point below has been filled by invention" |
| §5 | 239–265 | Source-coverage checklist — every outer canonical section (S1–S6) and every research report (R1–R7) marked `touched`; no section silently omitted |
| §6 | 266–273 | Non-independent-input note — apparent synthesis handled by **claim collapsing, not weighting**; dissent retained even when isolated |
| §7 | 274–282 | Deliverable index — `issue03-final-resolution.md`, the 6 CSV sidecars (`claim-matrix`, `disagreement-register`, `gap-register`, `source-coverage-checklist`, `report-claim-crosswalk`, `independent-source-ledger`) |

## 2. Finding-to-section mapping

Derived from the Task 3 crosswalk (18 rows, by identity — heading text reconciled to the
selected-set key per CONTEXT D-09). All 18 selected findings are `covered`; the `surface_to_user`
rows (D-04/D-05/D-06) are covered-as-routed-human-approval and the `defer` rows (M16/NS-13/ALM
mu_p) are covered-with-routing — neither is `silent`. No finding carries a Phase-31 verdict;
the "Coverage" column records coverage status only.

| Finding ID | Title (short) | Resolution-Doc Section | Lines | Coverage |
|-----------|----------------|------------------------|-------|----------|
| D-04 | Causal-training mode | §1.1 | 24–27 | covered (as routed human-approval — `surface_to_user`) |
| D-05 | `s_min` frame | §1.2 | 28–31 | covered (as routed human-approval — `surface_to_user`) |
| D-06 | Epsilon strategy | §1.3 | 32–35 | covered (as routed human-approval — `surface_to_user`) |
| B-07 | replay/lookahead batching | §1.4 | 36–39 | covered |
| B-08 | data versus collocation points | §1.5 | 40–43 | covered |
| M6 | `L_norm` clamping | §1.6 | 44–47 | covered |
| M7 | `tau_L` exclusion from `IC13` | §1.7 | 48–51 | covered |
| M14 | gradient clipping | §1.8 | 52–55 | covered |
| M15 | energy-loss weights | §1.9 | 56–59 | covered |
| M16 | `dt_out`-aware collocation scaling | §1.10 | 60–63 | covered (with routing — `defer`) |
| D5 | stage transitions | §1.11 | 64–67 | covered |
| NS-12 | componentwise automatic differentiation | §1.12 | 68–71 | covered |
| NS-13 | energy Huber delta | §1.13 | 72–75 | covered (with routing — `defer`) |
| NS-18 | loss scaling and units | §1.14 | 76–79 | covered |
| adaptive stage assignment | data-driven adaptive stage assignment (CURR-01) | §1.15 | 80–83 | covered |
| D = 6.694 | locked `D` conflict | §1.16 | 84–87 | covered (`accepted` for `4.6416`, `rejected` for `6.694`) |
| L_max / tau_L | `L_max` and `tau_L` formulas (CURR-02) | §1.17 | 88–91 | covered (`L_max` modified; `tau_L` estimator surfaced) |
| ALM mu_p clamp | ALM `mu_p` clamp (LOOP-05) | §1.18 | 92–95 | covered (with routing — `defer`) |

## 3. Citation guide (for Phase 32 evidence packets — EVID-11)

EVID-11 requires line-range citations into the candidate verdict source. Conventions:

- **File path (verbatim):**
  `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md`
- **Section anchor:** cite by the doc's own §-number (e.g. `§1.1` for D-04, `§1.16` for the D
  conflict) or by the finding-ID the subsection resolves (e.g. `§1.1 D-04`, `§1.12 NS-12`).
  §/finding-ID anchors are **stable across re-pagination**; line numbers are not.
- **Line-range format:** `03-final-resolution.md:START–END` (1-based, inclusive). Example for
  EVID-11: `03-final-resolution.md:24–27` lands inside §1.1 (D-04 Causal-training mode —
  `surface_to_user`), confirmed by sed extraction of the committed doc:

  ```
  sed -n '24,27p' …/03-final-resolution.md   # → the §1.1 heading + the surface_to_user body
  ```

  Line numbers in this map are anchored to commit `49fb7958` (48,049 bytes, 2026-06-20).
  Re-verify line numbers if the doc is re-delivered after a fix; section/finding-ID anchors
  survive minor re-pagination.
- **Disposition word:** each §1.x heading carries a one-word tag in backticks (e.g.
  `### 1.1 Causal-training mode — \`surface_to_user\``). That word is the doc's recorded
  disposition and is the triage key; the actual reasoning is the subsection body.
- **Claim-matrix / disagreement / gap registers:** §2/§3/§4 carry the machine-readable
  CSV sidecars (`issue03-claim-matrix.csv`, `issue03-disagreement-register.csv`,
  `issue03-gap-register.csv`). EVID-11 packets may cite a specific claim_id (e.g. `CAU-04`,
  `D-04`, `ADAPT-04`) to point at the row that maps a sub-claim to its canonical source basis.
- **Authority reminder for packets:** the doc is a candidate verdict source. Phase 32
  verdicts must cite the empirical grounding (`24-VERIFIED-FACTS.md` CLM rows where applicable,
  framework-spec lines, SCOPE-12 conventions) alongside the doc's recommendation — the doc's
  agreement is not itself the verdict (EVID-15 owns root-cause adjudication).

## 4. Verdict-direction preview

One-word direction per finding (for fast triage; read the section for the actual verdict).
Transcribed from the doc's heading disposition words; this is a **direction preview, not an
adjudication** — Phase 32 (EVID-11..15) assigns the actual verdicts.

| Finding | Direction | One-line note |
|---------|-----------|---------------|
| D-04 | surface_to_user | Per-time causal weighting is the baseline; dense-residual ALM rejected; final training mode is an owner decision (Option A/B/C) |
| D-05 | surface_to_user | Unsoftened geometric `s_min` for stage gate + matched-Plummer pair distance; softened-vs-unsoftened gate is owner-selected |
| D-06 | surface_to_user | Loss-side `ε_train = 1e-5` matched-Plummer locked; only the static/invariant `ε_inv = 1e-10` vs collapse-to-1e-5 is open |
| B-07 | modified | Stage-aware replay/lookahead via the locked query interfaces; `240/16` and `n_pts_cap = 32` are provisional defaults, not optima |
| B-08 | modified | Two independent logical point sets (Huber data vs collocation); `8192/4096` are example/provisional budgets; mandatory 50/50 mix deferred |
| M6 | modified | `L_norm` is metadata, not an IC slot; no global clamp authorized; storage policy deferred to owner |
| M7 | accepted | `tau_L` deliberately excluded from the locked Jacobi-state input; staging/evaluation metadata only |
| M14 | modified | `clip_value = C_stage × median(grad_norm)`; CTL schedule `7–10 / 5 / 3` retained; midpoint `8.5` not canonized |
| M15 | rejected | Issue premise `λ_E = 1000` stale; PHYS-05 warmup (max `1`) retained; CLM-11 cap table up to `500` rejected |
| M16 | defer | Verified `dt_out` does not establish a collocation objective; CLM-20 `dt_base/dt_out` factors not adopted |
| D5 | modified | Four success criteria retained; explicit ADVANCE/RECOVER/HALT-REVIEW state machine; relaxation/thresholds remain unverified |
| NS-12 | accepted | PHYS-02 already requires coordinatewise first/second derivatives and forbids the summed-output VJP; `review_of_framework.md` all-ones-covector snippet rejected |
| NS-13 | defer | `δ_E = 1.0` remains the configurable baseline; no `|ΔH|` distribution supports an immediate change to `0.1` or `0.01–0.1` |
| NS-18 | modified | Dimensionless contract confirmed (scaled positions, normalized-time derivatives, matched `ε_train`, raw masses, IC anchor, angular-momentum reg); issue L1/MAE replaced by spec's Huber |
| adaptive stage assignment | modified | Offline EDA / PCA / clustering permitted as boundary-calibration; `stage_strat_revision.md` Table 4 not adopted wholesale; `Q_norm = Q_raw/s³` only where per-record `s` is established |
| D = 6.694 | accepted / rejected | `D = (G·T²)^(1/3) ≈ 4.6416` mandatory; `6.694` claim and P4-1 rerun directive rejected; external-artifact provenance under 6.694 is unavailable (GAP-17) |
| L_max / tau_L | modified / surface_to_user | `L_max = M_tot · r_char · √(2|E|/M_tot)` retained as **characteristic scale** (not proven maximum); canonical `tau_L` estimator unresolved (Rosenstein baseline vs shadow/Benettin) — owner decision |
| ALM mu_p clamp | defer | Default loss has no `mu_p` (dense-residual ALM rejected); clamp could apply only to an optional scalar-conservation ALM after that ablation; exact `[1e-4, 100]` bounds not adopted |

Direction legend: **accepted** (supported by the governing canonical sources) · **rejected**
(contradicted by a lock, the authoritative spec, or the attached evidence) · **modified** (core
concern survives, framing/implementation must change) · **surface_to_user** (sources reserve
the decision or materially conflict without a governing resolution) · **defer** (evidence or
specification insufficient; no value or rule invented). All five disposition words are defined
in the doc's §0 (lines 14–20).

## 5. Out-of-scope / forward-reference notes (Phase 31 does NOT adjudicate these)

Phase 31 verifies and maps; it assigns no verdict. The following are routed to their owners,
not decided here:

- **D-04 / D-05 / D-06 (the three `surface_to_user` human-approval decisions)** — adjudicated
  in **Phase 32 / EVID-15**, not here. Phase 31 confirms they are present and flags them as
  caveats (covered-as-routed-human-approval).
- **`D = 6.694` re-adjudication** — SCOPE-12 hard constraint; only Phase 32 **EVID-15** may
  revisit it, and only with new first-principles evidence surfaced as a gap. The doc §1.16
  upholds `≈ 4.6416` and rejects `6.694`; Phase 31 confirms compliance only.
- **Empirical verification / re-measurement of any dataset figure** — no Phase-24 analog in
  v1.6 (CONTEXT D-10). Figures are checked for *contradiction* of already-v1.5-verified facts
  only; re-measuring is **FUT-01/FUT-02/FUT-04** (trainex).
- **Adaptive-stage-assignment EDA run + Stage-0 pilot calibration** — SCOPE-14/15, **FUT**.
  v1.6 specifies the methodology contracts (CURR-03, CURR-04); it does not run the EDA.
- **Training-loop code (DataLoader, batch constructor, ALM update, causal-window mechanics)** —
  SCOPE-14, **FUT-01/FUT-04** (trainex). v1.6 transcribes the verbatim audit "Section 6"
  pseudocode as normative spec contracts, never implemented.
- **Editing `ctl_instruction.md` / `pinn_architecture.md`** — Phases 33–35 (CURR / LOOP /
  LOSS). Phase 31 reads documents only.
- **Editing or re-writing the resolution doc** — the doc is the user's external product. If
  `NOT-READY`, Phase 31 routes fix instructions to the consolidation agent; it does not edit.

## 6. Open-items carry-forward (from the doc's §4 gap register + §6 non-independence note)

The doc's own §4 registers 19 `GAP-xx` items (lines 213–238) — "no source-silent or ambiguous
point below has been filled by invention." The items that materially route into Phases 32–36
or the user gate, for awareness (NOT readiness blockers — see `31-READINESS-REPORT.md` §4):

| Doc GAP | Topic | Disposition | Route |
|---------|-------|-------------|-------|
| GAP-01 | Causal exponent clip (numeric bound unset) | defer | Owner/FUT if causal weighting remains (CAU-05) |
| GAP-02 | Causal mode — no A/B/C ablation or Option-C window contract | surface_to_user | Owner selects mode; **Phase 32 EVID-15** (CAU-04) |
| GAP-03 | `s_min` frame — no geometric-vs-softened sensitivity | surface_to_user | Owner selects frame; **Phase 32 EVID-15** (SMIN-03) |
| GAP-04 | Static epsilon — no per-record invariant/stage sensitivity between `ε_inv=1e-10` and `1e-5` | surface_to_user | Owner selects A/B; **Phase 32 EVID-15** (EPS-03, EPS-05) |
| GAP-05 | Replay edge cases (absent/undersized next-stage, replacement, final-stage) | defer | Specify deterministic sampling policy; **Phase 34 LOOP-01** (B07-05) |
| GAP-06 | Collocation budget/mix — no validated 4096 budget or canonical 50/50 mix | defer | Compute-budget + sampler ablation; **Phase 34 LOOP-02/LOOP-03** (B08-04, B08-05) |
| GAP-07 | `L_norm` storage — raw vs clipped metadata, degenerate `L_max` handling | surface_to_user | Owner selects storage contract; audit admitted distribution (M6-02, M6-03) |
| GAP-08 | Gradient clipping execution — early-stage C, bootstrap floor, history reset | defer | Stage-0 gradient trace; **Phase 34 LOOP-04** (M14-03, M14-04) |
| GAP-09 | Energy dominance control — no coherent automatic safeguard | defer | Log weighted losses/gradients first; **Phase 35 LOSS-02** (M15-04) |
| GAP-10 | `dt_out` scaling — objective/direction/caps/rounding undefined | defer | Fixed-compute ablation; **Phase 34 LOOP-06** (M16-02, M16-03) |
| GAP-11 | Stage advancement — degraded-checkpoint advance after max epochs/stagnation | surface_to_user | Owner decision; **Phase 33 CURR-03** (D5-04) |
| GAP-12 | Transition constants — percentile, thresholds, epoch table, stagnation, retry | defer | Stage-0 pilot; **Phase 33 CURR-03** (D5-05) |
| GAP-13 | Executable AD — batched implementation/memory strategy | defer | Implement + run PHYS-02 acceptance; **FUT-01** (NS12-03) |
| GAP-14 | Energy Huber delta — no `\|ΔH\|` distribution or branch occupancy | defer | Pilot-based calibration; **Phase 35 LOSS-03** (NS13-02, NS13-03) |
| GAP-15 | Adaptive population — 5% vs >10%, cluster-count/stage mapping | surface_to_user | Owner sets policy after admitted-set EDA; **Phase 33 CURR-01** (ADAPT-04, ADAPT-07) |
| GAP-16 | Sampling scale `s` — per-record persistence/reconstruction not established | defer | Audit metadata; exclude `Q_norm` when `s` unavailable; **Phase 33 CURR-01** (ADAPT-05) |
| GAP-17 | Prior D artifacts — provenance under 6.694 unavailable | defer | Provide provenance or recompute only affected; **Phase 32 EVID-15** (D-04) |
| GAP-18 | `tau_L` method/units — estimator, time unit, fit params, uncertainty, thresholds | surface_to_user | Owner selects method; cross-calibrate; **Phase 33 CURR-02** (TAUL-01, TAUL-03) |
| GAP-19 | Optional ALM — scalar-constraint update law, normalization, reset, clamp sensitivity | defer | Specify ablation before bounds; **Phase 34 LOOP-05** (ALM-02, ALM-03) |

**§6 non-independence note (lines 266–273), carried forward:** the consolidation was done by
**claim collapsing, not weighting** — an 81-claim independent ledger was frozen from the
canonical bundle *before* the reports bundle was opened, then each report section was mapped
to that ledger. Restatements, shared wording, and apparent synthesis produced only another
provenance entry for the same claim; they did not increase confidence or alter the disposition.
Dissent was retained even when isolated (e.g. R2/R4/R5/R6 support for `dt_base/dt_out`;
R3's characteristic-scale reading of `L_max`; R5/R6 false missing-source claims). EVID-11..15
packets must therefore treat the report-attribution columns as provenance, not vote counts.
