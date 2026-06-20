---
status: active
purpose: verification-report
created: 2026-06-20
milestone: v1.6
phase: resolution-doc-readiness
retirement_trigger: Phase 32 evidence-packet construction begins consuming the resolution doc
---

# Phase 31 Readiness Report — Issue-03 Resolution Doc

**Subject:** `pinn_instruction/markdown_conversion/framework-revisions/research_reports/03-curriculum-and-training-loop/research_result/03-final-resolution.md` (282 lines, 48,049 bytes, commit `49fb7958`, 2026-06-20)
**Cross-reference anchors:** the ROADMAP-SC1 selected-finding set (15) + 3 contract-phase extras (CONTEXT D-09); the archived v1.5 verified-facts register `24-VERIFIED-FACTS.md` (CLM-01..12 + DATA-05; CLM-13 PENDING); the SCOPE-12 locked v1.4+v1.5 conventions (7).

## 1. Executive summary

**Verdict: READY-WITH-CAVEATS.**

All four readiness checks PASS. Every one of the 18 selected findings is `covered` (the three
`surface_to_user` human-approval decisions D-04/D-05/D-06 covered-as-routed-human-approval;
the three `defer` rows M16/NS-13/ALM `mu_p` covered-with-routing; the remaining 12 covered
outright) — **zero `partial`, zero `silent`.** The resolution doc contradicts **zero**
v1.5-verified dataset facts (it cites CLM IDs as provenance anchors without restating any
verified numeric value with a contradicting number, and the one value it does assert in its
own voice — `D ≈ 4.6416` — agrees exactly with the v1.5 Phase-25 EVID-10 ratified convention).
It commits **zero** violations of the 7 SCOPE-12 locked conventions (it actively upholds all
seven, including the §1.16 mandatory `D = (G·T²)^(1/3) ≈ 4.6416` with the `6.694` claim and
P4-1 rerun directive rejected).

The "with-caveats" qualifier reflects open items the resolution doc itself registers (§4 GAP-01
through GAP-19) that are **deferred or surfaced by design** — the three `surface_to_user`
human-approval decisions routed to **Phase 32 EVID-15**, the six `defer`-routed items owned by
Phases 33–35 or FUT, the unverified-but-non-contradicting figures flagged FUT, and the §6
non-independence note (claim-collapsing, not weighting). None of these block the start of
adjudication; each is owned downstream. Per the fixed precedence (D-05), Phase 32 proceeds with
awareness of these caveats.

**Verdict derivation (re-derivable from the four check tables in §3):**

- NOT-READY triggers? `silent` finding count = 0 (R3); verified-fact contradiction count = 0
  (R4); locked-convention violation count = 0 (R5). **No NOT-READY trigger fires.**
- Caveats present? YES — `surface_to_user` rows (3), `defer` rows (3), the §1.17 mixed-direction
  `L_max`/`tau_L`, unverified figures (7 sets), and the §6 non-independence note. →
  **READY-WITH-CAVEATS**.
- All-clean? NO. → not `READY`.

## 2. Pre-execution gate

Both gate conditions PASS with evidence; no STOP triggered.

| Gate condition | Result | Evidence |
|----------------|--------|----------|
| (a) Canonical resolution doc exists, non-empty, substantive | PASS | `…/research_result/03-final-resolution.md` present, 48,049 bytes (>> 10,000-byte floor), 282 lines; byte-identical blob at commit `49fb7958` (2026-06-20) — **matches the reference exactly, no re-delivery refresh needed** (Task 1 re-delivery routing did not fire); single coherent doc, not a stub/header-only placeholder |
| (b) Phase 30 COMPLETE in STATE.md | PASS | STATE.md line 32: `Plan: 31-01 created + verified; 0 of 1 executed (Phase 30: 5/5 complete + verified)` — the completion-specific marker (`5/5 complete + verified`), not a bare "Phase 30" string match |

## 3. Check results

| # | Check (R-task) | Result |
|---|----------------|--------|
| 1 | Pre-execution gate (R1) | **PASS** — both conditions PASS with evidence (see §2) |
| 2 | Presence / structural (R2) | **PASS** — single coherent §0–§7 doc with 18 per-finding subsections; four v1.6 topic areas identifiable |
| 3 | Finding-coverage crosswalk (R3, 18 findings) | **PASS** — 18/18 covered, 0 partial, 0 silent |
| 4 | Dataset-figure consistency (R4, vs `24-VERIFIED-FACTS.md`) | **PASS** — 0 contradictions |
| 5 | Locked-convention compliance (R5, SCOPE-12) | **PASS** — 0 violations, 0 scope observations |

### R2 — Presence / structural check: PASS

- **Exists, non-empty, single coherent document.** 282 lines; not a raw concatenation. The doc
  reads as one consistent adjudication with a strict source hierarchy declared up front (§0,
  lines 8–21): locked SCOPE-12 constraints → framework specs as revisable baseline → verified
  grounding companions → non-authoritative issue document and baseline design reports. No
  duplicate or competing top-level numbering. §6 (lines 266–273) records that apparent report
  synthesis was handled by claim-collapsing — an explicit coherence-preserving design choice,
  not a coherence-breaking non-independence.
- **Citable structure.** Numbered §-sections (§0 method; §1.1–§1.18 per-finding; §2 claim
  matrix; §3 disagreement register; §4 gap register; §5 source-coverage; §6 non-independence;
  §7 deliverable index) with line-range-citable subsections (the §1.x subsections are each a
  short ≈4-line range), satisfying EVID-11's line-range-citation requirement. The automated
  Task-2 grep confirms exactly 18 `### 1.x` headings.
- **Four v1.6 topic areas identifiable** (per the §1 section inventory in `31-RESOLUTION-MAP.md`):
  - **curriculum-stage**: §1.4 (B-07 replay/lookahead batching), §1.11 (D5 stage transitions),
    §1.15 (data-driven adaptive stage assignment);
  - **training-loop / batch-construction**: §1.5 (B-08 data vs collocation points),
    §1.10 (M16 `dt_out`-aware scaling), §1.18 (ALM `mu_p` clamp);
  - **loss / energy**: §1.6 (M6 `L_norm` clamping), §1.9 (M15 energy-loss weights),
    §1.13 (NS-13 Huber delta), §1.14 (NS-18 loss scaling and units);
  - **human-approval decisions**: §1.1 (D-04 causal-training mode), §1.2 (D-05 `s_min` frame),
    §1.3 (D-06 epsilon strategy).

### R3 — Finding-coverage crosswalk: PASS (18/18 covered)

Full table in `31-RESOLUTION-MAP.md` §2. By-identity matching (heading text reconciled to the
selected-set key per CONTEXT D-09): the doc's §1.1 "Causal-training mode" = D-04; §1.2 "`s_min`
frame" = D-05; §1.3 "Epsilon strategy" = D-06; §1.12 "componentwise automatic differentiation"
= NS-12; §1.16 "Locked `D` conflict" = the `D = 6.694` SC1 finding. The three contract-phase
extras are mapped to their literal §1.x: §1.15 → CURR-01 (adaptive stage assignment); §1.17 →
CURR-02 (`L_max`/`tau_L` formulas); §1.18 → LOOP-05 (ALM `mu_p` clamp). **Zero `silent`, zero
`partial`** — every selected finding maps to a section that states an actual position.

Coverage shapes of note (covered-with-caveat, not gaps):

- **D-04 / D-05 / D-06 (`surface_to_user`)** — each carries a recorded position AND a named
  open owner decision (the static-vs-softened frame, the static `ε_inv`, the causal-mode
  selection). These are routed to **Phase 32 EVID-15**, not silent — covered-as-routed-human-approval.
- **M16 / NS-13 / ALM `mu_p` (`defer`)** — each states a baseline retention AND names the
  missing evidence/calibration that blocks a change (no `|ΔH|` distribution, no fixed-compute
  ablation, no scalar-ALM ablation). covered-with-routing — neither is silent.
- **§1.17 (`L_max`/`tau_L`)** — mixed direction: `L_max` is `modified` (retained as
  characteristic scale, not proven maximum); the canonical `tau_L` estimator is
  `surface_to_user` (Rosenstein baseline vs shadow/Benettin). Both sub-decisions are stated;
  covered.
- **§1.16 (`D = 6.694`)** — KNOWN CONFLICT, resolved in the expected direction: `accepted` for
  `4.6416`, `rejected` for `6.694`. The external-artifact provenance under `6.694` is GAP-17
  (deferred — attachments do not establish whether any processed store or threshold was
  produced under `6.694`). Re-adjudication of the convention itself is **Phase 32 EVID-15**.

### R4 — Dataset-figure consistency check: PASS (0 contradictions)

The doc cites 13 CLM/VF IDs (CLM-01, CLM-02, CLM-08, CLM-10, CLM-11, CLM-12, CLM-14, CLM-16,
CLM-17, CLM-19, CLM-20, VF-1, VF-5) — every one as a **provenance anchor** inside a
`[Canonical: S4, …]` citation, never restating the verified numeric value with a contradicting
number. The doc explicitly treats CLM-11's cap table and CLM-20's `dt_base/dt_out` factors as
`claimed_unverified` / `rejected` — it does NOT present them as verified facts. The single
figure the doc asserts in its own voice — `D = (G·T²)^(1/3) ≈ 4.6416` (§1.16) — agrees exactly
with the v1.5 Phase-25 EVID-10 ratified convention (SCOPE-12 convention 6).

`consistent?` table (mapped figures only; within-stated-precision rule applied):

| CLM / row | Verified value (`24-VERIFIED-FACTS.md`) | Resolution doc position | Consistent? |
|-----------|------------------------------------------|-------------------------|-------------|
| CLM-01 (std ID gaps) | 1,250 gaps / 2,749 files / max_id 3,998 | cited as provenance anchor for the D conflict (§1.16: "S4, CLM-01/19 and VF-5") — value NOT restated, NOT contradicted | YES (no contradiction; provenance-only citation) |
| CLM-02..07 (adaptive staging figures) | CLM-02..07 PENDING (claimed-unverified) | §1.15: "CLM-02..07 remain unverified" — explicitly NOT cited as verified | YES (consistent — doc agrees they are unverified; never presented as facts) |
| CLM-08/09 (tol=1e-14 gold files; transition stability) | 592 standard-gold `tol=1e-14`; folder defaults | §1.11 cites CLM-08/09 as provenance for D5 transition stability — value NOT restated, NOT contradicted | YES (no contradiction; provenance-only citation) |
| CLM-10 (snapshots/traj medians 61/127/1003) | corrected medians 61/127/1003 | §1.8 cites CLM-10 as provenance for M14 gradient clipping — value NOT restated, NOT contradicted | YES (no contradiction; provenance-only citation) |
| CLM-11 (`λ_E = 1000` issue premise; cap table) | PENDING / `claimed_unverified` | §1.9: "the issue premise of `lambda_E = 1000` is stale … reject CLM-11's cap table up to `500`" — explicitly REJECTS the unverified figure; never presented as verified | YES (consistent — doc rejects the unverified claim) |
| CLM-12 (nominal IC counts ~4,000/~5,000; `n_pts_cap`) | ~4,000 std / ~5,000 hier (max_id 3,998/4,999) | §1.4/§1.5 cite CLM-12 as provenance for B-07/B-08; treats `240/16`, `n_pts_cap=32`, `8192/4096` as **provisional defaults, not verified optima** | YES (no contradiction; CLM-12 IC-count value NOT restated; provisional figures flagged unverified) |
| CLM-16 (snapshot sampling `min(cap, n_snapshots)`) | part of B-07 claim register | §1.4 cites CLM-16 alongside CLM-12 as provenance — value NOT restated, NOT contradicted | YES (no contradiction; provenance-only citation) |
| CLM-17/20 (`dt_out` / `dt_base` factors) | CLM-17 = verified `dt_out` distribution; CLM-20 PENDING | §1.10: "verified `dt_out` values do not establish a collocation-density objective … do not adopt CLM-20's `dt_base/dt_out` factors or the inverse" — explicitly DEFERS and rejects the unverified scaling | YES (consistent — doc defers; never adopts the unverified figure) |
| CLM-19 / VF-5 (D convention verification) | VF-5 = verified D anchor | §1.16: "D = (G·T²)^(1/3) ≈ 4.6416 is mandatory" — agrees exactly with the verified anchor | YES (agrees within stated precision — exact match) |
| CLM-14/15 (adaptive staging extension) | zero rows in register (D-06 prose sweep found none) | §1.15 cites CLM-14/15 as provenance alongside CLM-02..07 — no figure restated | YES (no contradiction; provenance-only citation) |
| DATA-05 (70 base-hier mass-drift) | 70/4,857 mismatches quarantined | NOT cited in the doc (out of doc-03 scope — DATA-05 was settled in v1.5) — no position taken, no contradiction | N/A (no mapped figure; out of scope) |
| CLM-13 (`D = 6.694` contested convention) | PENDING — routed Phase 25 EVID-10 (now ratified `convention-rejected`) | §1.16: upholds `≈ 4.6416`, rejects `6.694` — the EXPECTED contested-convention position | YES (expected position; not a contradiction here — re-adjudication is Phase 32 EVID-15) |

**No CLM/VF row shows a contradicted value.** The doc never restates a verified number with a
different figure; it either cites the CLM ID as a provenance anchor or explicitly flags the
figure as unverified / rejected. **0 contradictions → R4 PASS.**

**Unverified-but-non-contradicting figures flagged FUT (caveats, NOT failures):** `240/16` /
`n_pts_cap = 32` (B-07 provisional defaults, §1.4); `8192/4096` (B-08 provisional budgets,
§1.5); `7–10 / 5 / 3` and `8.5` (M14 CTL schedule retained / midpoint rejected, §1.8);
`λ_E = 1000` / cap-up-to-`500` (M15 rejected, §1.9); `δ_E = 1.0` baseline / `0.1` / `0.01–0.1`
(NS-13 deferred, §1.13); `[1e-4, 100]` ALM bounds (ALM `mu_p` deferred, §1.18). None is
presented as a verified fact; none fails the check.

### R5 — Locked-convention compliance (SCOPE-12): PASS (0 violations, 0 scope observations)

`compliant?` table over the 7 SCOPE-12 locked conventions (verbatim from REQUIREMENTS.md
SCOPE-12 + the `4.6416` convention):

| # | Convention | Resolution doc position | Compliant? |
|---|-----------|-------------------------|------------|
| 1 | 14D input `[τ, IC₁₃]` | §1.6: "`L_norm` is metadata, not an `IC13` slot"; §1.7: "`tau_L` is deliberately excluded from the locked Jacobi-state input" — both treat the 14D contract as a fixed input, never touched | YES (upheld; not altered) |
| 2 | Jacobi IC₁₃ (13 components) | §1.6/§1.7 affirm the Jacobi-state input vector — no position adds or removes an IC slot | YES (upheld) |
| 3 | Mass-weighted COM projection head | No doc position touches the projection head (out of doc-03 scope — the head was settled in v1.4 Phase 17); no breach, no recommendation | YES (not touched; no breach) |
| 4 | PHYS-03 softening `eps_soft = 1e-5` | §1.3: "`ε_train = 1e-5`, matched-Plummer, identically in physics and energy" — explicitly upholds; §1.17 carefully distinguishes the shadow-method `1e-8`/`1e-10` from "training softening" | YES (upheld; shadow-method eps correctly distinguished from training softening) |
| 5 | Post-v1.3 SCS gate (`ε_H > 10⁻⁵` / `SCS > −5`) | No doc position touches SCS (settled in v1.5 Phase 25 EVID-10; out of doc-03 scope); no breach, no recommendation | YES (not touched; no breach) |
| 6 | PHYS-01 raw-mass `D = (G·T²)^(1/3) ≈ 4.6416` (`D = 6.694` rejected) | §1.16 (read fresh, lines 84–87): "`D = (G T^2)^(1/3) ≈ 4.6416` is mandatory. Remove the issue document's `6.694` claim and reject its P4-1 rerun directive." — **explicitly upholds** `4.6416`, **explicitly rejects** `6.694`. The §1.16 `defer` of GAP-17 is about external-artifact *provenance under 6.694*, NOT a recommendation to revisit the D convention | YES (upheld; rejected `6.694`; no recommendation to change) |
| 7 | v1.5 data-side contracts (PIPE-01..10 / VAL-01..04) | §1.4: "Adopt stage-aware replay/lookahead selection **through the locked query interfaces**" (cites PIPE-04 / SI-PINN-003) — respects the v1.5 DataLoader/stage-query contracts as fixed inputs; no breach, no recommendation | YES (respects the locked data-side contracts) |

**Scope observations requiring a user decision: NONE.** The doc recommends changing **zero**
locked conventions. It explicitly declines to re-open PHYS-01/SCOPE-12 convention 6 (§1.16 makes
`4.6416` mandatory and rejects `6.694`); the §1.1 "unless that lock is explicitly reopened"
wording is a *conditional about the causal-mode lock*, not a recommendation. The §1.16 GAP-17
defer is a provenance question (whether any external artifact was produced under `6.694`), not
a recommendation to change the D convention. Re-adjudication of the D conflict itself remains
**Phase 32 EVID-15** (SCOPE-12 hard constraint).

**0 violations → R5 PASS.** Phase 31 confirms compliance only; it does **not** re-adjudicate
any locked convention (including the `D = 6.694` conflict).

## 4. Gap list

No **blocking** gaps — no silent finding (R3), no verified-fact contradiction (R4), no
locked-convention violation (R5). The NOT-READY triggers (silent / contradiction / violation)
are all absent; `grep -E "silent|contradiction|violation"` over this gap list returns only this
paragraph's enumeration of the triggers that did NOT fire, confirming the structural
anti-rubber-stamp invariant (a NOT-READY verdict would require ≥1 `Blocking? = yes` row OR a
NOT-READY-trigger keyword in the gap list — neither holds here).

The following are **non-blocking caveats** — open items the resolution doc registers (§4
GAP-01..GAP-19) and routes downstream by design. They are recorded here for Phase 32+
awareness, not as readiness failures:

| ID | Caveat | Affects (finding/convention) | Owner / route | Blocking? |
|----|--------|------------------------------|---------------|-----------|
| C-01 | D-04 causal-training mode — owner must select Option A/B/C | D-04 (§1.1); CAU-04 | Phase 32 EVID-15 → owner decision | No |
| C-02 | D-05 `s_min` frame — geometric vs softened stage gate | D-05 (§1.2); SMIN-03 | Phase 32 EVID-15 → owner decision | No |
| C-03 | D-06 epsilon strategy — static `ε_inv = 1e-10` vs collapse to `1e-5` | D-06 (§1.3); EPS-03/EPS-05 | Phase 32 EVID-15 → owner decision | No |
| C-04 | §1.17 `tau_L` estimator — Rosenstein vs shadow/Benettin; time-unit convention | CURR-02 (§1.17); TAUL-01/TAUL-03 | Phase 32 EVID-15 + Phase 33 CURR-02 → owner decision | No |
| C-05 | M16 `dt_out` scaling deferred — objective/direction undefined | M16 (§1.10); M16-02/M16-03 | Phase 34 LOOP-06 → fixed-compute ablation | No |
| C-06 | NS-13 Huber delta deferred — no `\|ΔH\|` distribution | NS-13 (§1.13); NS13-02/NS13-03 | Phase 35 LOSS-03 → pilot calibration | No |
| C-07 | ALM `mu_p` clamp deferred — no scalar-ALM ablation | ALM (§1.18); ALM-02/ALM-03 | Phase 34 LOOP-05 → ablation before bounds | No |
| C-08 | GAP-17 prior-D-artifact provenance under 6.694 unavailable | `D = 6.694` (§1.16); D-04 | Phase 32 EVID-15 → recompute only affected artifacts on provenance | No (NOT a recommendation to revisit the D convention) |
| C-09 | Unverified-but-non-contradicting figures flagged FUT | B-07 (`240/16`/`n_pts_cap=32`); B-08 (`8192/4096`); M14 (`7–10/5/3`, `8.5`); M15 (`λ_E=1000`, cap-to-500); NS-13 (`δ_E=1.0`/0.1/0.01–0.1); ALM (`[1e-4,100]`) | Phases 33–35 + FUT-01/FUT-02/FUT-04 — calibrate against admitted-set distributions | No (caveats flagged FUT; never presented as verified) |
| C-10 | §6 non-independence note — reports handled by claim-collapsing, not weighting | Provenance interpretation (R1–R7 attributions) | Phase 32 EVID-11..15 packets must treat report-attribution columns as provenance, not vote counts | No (provenance-hygiene note) |
| C-11 | Adaptive population safeguard (5% vs >10%) surfaced | CURR-01 (§1.15); ADAPT-04/ADAPT-07 | Phase 33 CURR-01 → owner policy after admitted-set EDA | No |
| C-12 | `L_norm` storage policy (raw vs clipped metadata) deferred | M6 (§1.6); M6-02/M6-03 | Owner selects storage contract; audit admitted distribution | No |

## 5. Fix instructions

No fixes are required for readiness — **no blocking gap fired.** The resolution doc is usable
as-is by Phase 32.

The §4 caveats are **routed downstream by design**, not fix packages routed back to the
consolidation agent:

- **C-01..C-04 (the surface_to_user decisions + the tau_L estimator)** are owned by
  **Phase 32 EVID-15** — they are the *headline conflicts* that phase exists to adjudicate.
  The doc is the candidate verdict source for that step, exactly as ROADMAP §"Phase 32"
  intends.
- **C-05..C-07, C-11, C-12 (the defer items)** are owned by the contract phases
  (Phases 33–35) or by FUT calibration; they are not missing from the doc — the doc
  explicitly retains the current baseline and names the missing evidence.
- **C-08 (GAP-17 prior-D-artifact provenance)** is a provenance question for Phase 32 EVID-15
  to resolve; the doc correctly declines to make a blanket claim about prior outputs.
- **C-09 (unverified figures)** are calibration-pending constants flagged FUT — they are
  neither contradictions nor failures (R4 PASS).
- **C-10 (§6 non-independence note)** is a provenance-hygiene reminder for EVID-11..15 packet
  authors; nothing to fix in the doc.

Because no blocking gap fired, **no fix package is routed to the external consolidation agent.**
Phase 32 can start evidence-packet construction immediately using `31-RESOLUTION-MAP.md`.

## 6. Re-check protocol

If the resolution doc is re-delivered after any change, re-run only the affected check(s)
(affected-only; §/finding-ID anchors are stable across re-pagination, line numbers are not):

- **Structural change** (sections renamed/renumbered, doc re-split, or a byte count ≠ the
  recorded `48,049` / commit `49fb7958`) → re-run Task 1 (re-confirm gate (a)) + Task 2
  (structural) + **refresh the line ranges in `31-RESOLUTION-MAP.md` §1 section index and §2
  mapping**. The §/finding-ID anchors survive; only the line numbers are revision-scoped. This
  is a "doc re-delivered → refresh inventory" event, not a blind retry.
- **New/changed disposition on a finding** → re-run Task 3 for that finding row only; update
  the map's §2 finding-to-section row and §4 verdict-direction row; re-derive the verdict.
- **Any dataset-figure claim added/changed** → re-run Task 4 for the affected CLM/VF row(s)
  against `24-VERIFIED-FACTS.md` (apply the within-stated-precision rule).
- **Any recommendation touching a SCOPE-12 convention** → re-run Task 5 for that convention; if
  the doc now *recommends* changing a locked convention, record it as a **scope observation**
  and surface to the user (do NOT auto-pass or auto-fail).
- **Re-derive the gate decision (§1)** from the refreshed check results using the fixed
  precedence (D-05).

A re-delivery does NOT require re-running the unaffected checks. **Phases 32–36 remain blocked
on NOT-READY until the routed fix lands and an affected-only re-check passes** — not
applicable here (verdict is READY-WITH-CAVEATS, not NOT-READY).

## 7. Gate decision

**Decision: READY-WITH-CAVEATS → Phases 32–36 are UNBLOCKED; proceed with awareness of the §4
caveats (C-01..C-12).**

Decision-rule application (D-05 / SPEC R7 fixed precedence):

- **NOT-READY branch?** The NOT-READY triggers are (a) silent findings — **none** (18/18
  covered); (b) verified-fact contradictions — **none** (0 contradictions, R4); (c)
  locked-convention violations — **none** (0 violations, R5). **No trigger fires.**
- **READY branch (all-clean)?** NO — the `surface_to_user` rows (3), `defer` rows (3), the
  §1.17 mixed direction, the unverified-but-non-contradicting figures (7 sets), and the §6
  non-independence note are all caveats. The strict "all-clean" branch does not apply.
- **READY-WITH-CAVEATS applies.** The only open items are minor, deferred/surfaced by design,
  and owned by Phase 32 (EVID-15) / Phases 33–35 / FUT / the user gate. The most consequential
  (D-04/D-05/D-06 + `D = 6.694` re-adjudication + GAP-17 provenance) is routed to EVID-15 — a
  Phase 32 work item — exactly as ROADMAP §"Phase 32" intends. Phase 32 can start
  evidence-packet construction immediately using `31-RESOLUTION-MAP.md`.

**Structural verdict-consistency (anti-rubber-stamp invariant, finding B):** the §4 gap list
carries a `Blocking?` column. Every row is `Blocking? = No`; the gap list contains no
NOT-READY-trigger keyword (`silent` / `contradiction` / `violation`) applied to an actual
finding — those words appear only in §4's enumeration of the triggers that did NOT fire. This
is consistent with a **READY-WITH-CAVEATS** verdict (which permits non-blocking caveats). A
`READY` (no caveats) verdict would require zero `Blocking? = yes` rows AND zero caveats — the
caveats are present, so READY-WITH-CAVEATS is the correct branch.

**Caveats Phases 32–36 must carry forward:** C-01..C-04 (the human-approval decisions + the
`tau_L` estimator → Phase 32 EVID-15); C-05..C-07 (the M16/NS-13/ALM defers → Phases 34/35);
C-08 (GAP-17 prior-D-artifact provenance → Phase 32 EVID-15); C-09 (unverified figures →
calibrate FUT); C-10 (§6 non-independence → provenance hygiene for EVID-11..15 packets);
C-11/C-12 (adaptive population safeguard + `L_norm` storage → Phase 33 CURR-01 / owner). See
`31-RESOLUTION-MAP.md` §6 for the full GAP-01..GAP-19 carry-forward.

**STATE.md / ROADMAP.md:** will be updated to reflect the gate outcome via the named gsd-tools
handlers (Task 8, applied by the orchestrator): `state complete-phase` for the passing gate,
plus `roadmap update-plan-progress 31` to reconcile the Phase 30 (`5/5 Complete`) and Phase 31
(`N/1`) progress rows. No direct STATE.md Write/Edit (universal anti-pattern 15); the
counter-integrity guard (Task 8 finding C.2) snapshots STATE.md before the handler call and
restores + hand-corrects under `docs(planning)` scope if any `progress` counter regresses.

## 8. Acceptance-criteria check (against `31-SPEC.md` §"Acceptance Criteria")

| # | SPEC acceptance criterion | Status | Evidence |
|---|---------------------------|--------|----------|
| 1 | Pre-exec gate records both conditions PASS (doc present/non-empty/canonical; Phase 30 COMPLETE); a stub/empty doc or missing marker STOPs | **MET** | §2 — both conditions PASS with evidence; doc is 48,049 bytes (substantive, not a stub), byte-identical to `49fb7958`; STATE.md line 32 carries `5/5 complete + verified` |
| 2 | Presence/structural check records PASS/FAIL with a section inventory; raw concatenation → FAIL | **MET** | §3 R2 — PASS; §0–§7 + §1.1–§1.18 inventory in `31-RESOLUTION-MAP.md` §1; single coherent doc (§6 claim-collapsing is coherence-preserving); 18 `### 1.x` headings confirmed |
| 3 | Crosswalk maps all 18 findings by identity with covered/partial/silent; surface_to_user/defer = covered-with-caveat; every partial/silent flagged as gap; row count = 18 | **MET** | §3 R3 + `31-RESOLUTION-MAP.md` §2 — 18/18 covered (3 surface_to_user + 3 defer + 12 outright); 0 partial; 0 silent; by-identity matching documented |
| 4 | Consistency check lists each mapped figure with `consistent? yes/no` under within-precision; passes iff 0 contradictions; unverified = caveats; zero-mapped = vacuous pass | **MET** | §3 R4 — `consistent?` table lists 12 mapped CLM/VF rows, all YES; 0 contradictions; 7 sets of unverified figures flagged FUT as caveats |
| 5 | Convention-compliance marks each of 7 SCOPE-12 conventions `compliant? yes/no`; passes iff 0 violations; scope observations surfaced, never failures; no convention re-adjudicated | **MET** | §3 R5 — `compliant?` table marks all 7 YES; 0 violations; 0 scope observations; §1.16 read fresh and recorded verbatim; no re-adjudication in any Phase 31 artifact |
| 6 | `31-RESOLUTION-MAP.md` exists with section index (line ranges), 18-finding mapping, citation guide with concrete revision-anchored example, per-finding verdict-direction preview, open-items carry-forward | **MET** | `31-RESOLUTION-MAP.md` — §1 section index (all §0–§7 + §1.1–§1.18 line ranges anchored to `49fb7958`); §2 18-finding mapping; §3 citation guide with `03-final-resolution.md:24–27` example (sed-verified to land in §1.1); §4 verdict-direction preview (18 rows); §6 GAP-01..GAP-19 carry-forward + §6 note |
| 7 | `31-READINESS-REPORT.md` exists with exec verdict, four check results, gap list, fix instructions, re-check protocol, gate decision — verdict derivable by precedence | **MET** | this report — §1 exec verdict (READY-WITH-CAVEATS, re-derived in §1 and §7); §3 four check results; §4 gap list (12 caveats, 0 blocking); §5 fix instructions (none needed); §6 re-check protocol; §7 gate decision |
| 8 | On NOT-READY, fix instructions routed and Phases 32–36 stay blocked until affected-only re-check passes | **N/A** | verdict is READY-WITH-CAVEATS (not NOT-READY); Phases 32–36 are UNBLOCKED; the re-check protocol in §6 governs any future re-delivery |
| 9 | `git diff` for the Phase 31 commit shows zero changes to `ctl_instruction.md` / `pinn_architecture.md` / `03-final-resolution.md` / `pinn/**`; no finding carries a Phase 31 verdict | **MET (asserted by design)** | Phase 31 reads documents only; the two reports carry coverage status + direction preview only — no adjudication, no verdict text. The zero-edit invariant is asserted against the captured commit SHA in Task 8 (orchestrator-applied) |

## 9. Governance note (v1.6 STOP protocol)

No STOP-protocol gap was opened during this verification. No source-silent semantic /
process-schema / cross-phase decision requiring invention arose: every check is grounded in
the resolution doc, the archived v1.5 verified-facts register, the SCOPE-12 conventions, or
the locked Phase-30-complete marker. The places the resolution doc itself declines to invent
(the three `surface_to_user` decisions, the six `defer` items, the GAP-17 prior-D-artifact
provenance) are recorded as preserved caveats (C-01..C-08), correctly carried forward rather
than filled. `silent` coverage status would have been a reportable outcome; none occurred
(18/18 covered).
