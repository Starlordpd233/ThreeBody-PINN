---
phase: 54
checkpoint: 2
status: CHECKPOINT-2-DISCHARGED
created: 2026-08-20
---

# 54-RULING — Checkpoint ① / ② Ruling Record

## Standing

This file is the provenance record of the owner's branch selection at checkpoint ① and of any direct recalibration ruling. Phase 56 reads it as its authorizing source and may not open without it (SCOPE-34).

It is deliberately not the gap register — a ruling is not a gap (D-09) — and deliberately not the delivery note, which carries ERW routing. The gap anchor `GAP-54-01` in `.planning/phases/54-recalibration-decision-grounding/54-GAPS.md` and `.planning/milestones/v2.3-GAPS.md` stays `OPEN` until checkpoint ② is discharged.

## Checkpoint ① — the branch

- **Date:** 2026-08-21
- **Owner instruction (verbatim):** *"let's do the r3 and assemble the research pacakge to be handed off to the external research agent. make sure that the information inlcuded in that package is accurate and faithful"*
- **Branch:** **commission `trainex-r3`** — the Route-B (open-book) build-design round. Checkpoint ① is discharged; checkpoint ② remains PENDING until the round delivers and the owner ratifies.

The owner requested and received a written agent recommendation before selecting (2026-08-21, in session). That recommendation argued for commissioning the round; the selection is the owner's and is recorded here as instructed. Under SCOPE-34 the agent still marks no default, ranks no option, and picks nothing on the five decision surfaces — checkpoint ② is untouched by this entry.

The branch obligations are recorded below as they stood at the gate; the **Commission `trainex-r3`** list is the one now in force, and ERW-02 discharges it.

**Rule directly:**

- `.planning/phases/54-recalibration-decision-grounding/54-RULING.md` is filled with the branch, the date, the verbatim owner instruction, the per-surface disposition, and the SCOPE-38 re-ratification lines.
- Phase 56 then reads that file as its authorizing source.

**Commission trainex-r3:**

- ERW-02 authors `research_package/RESEARCH-AGENT-PROMPT.md` (ERW Rule 7 output contract, Rule 17 premise-challenge mandate, Rule 18 read-only bars).
- The `specs/` snapshot bundle as a single `framework-specs-bundle.md` (Rule 15).
- The Rule-20 live-tree pin in this note.
- `research_results/<agent>-resolution.md` at delivery.
- The Rule-19 per-claim in-repo verification report under `docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/`.
- The consolidated `trainex-r3-resolution-doc.md` (Rule 12).

## Checkpoint ② — the recalibration ruling

The five surfaces appear in the same transcription order the packet's §4.3 uses, and that order carries no precedence, no priority, and no sequencing implication.

- **Date:** 2026-09-04
- **Owner instruction (verbatim):** *"You're going to act as the decision-maker here and proceed with the checkpoint to rule on these items. use your best mathematical and scientific reasoning. tackle this with care."*
- **Authority:** The owner expressly delegated this checkpoint's adjudication to the Codex primary agent. That direct instruction supersedes SCOPE-34's earlier no-agent-pick constraint for this checkpoint only; it does not relax SCOPE-34 for later tuning or any other owner gate.

| Surface | Where it is specified today | Marker | Disposition |
|---|---|---|---|
| `η_c`, the causal-weight exponent coefficient | `pinn_architecture.md:435` (the `w_n` formula) | Phase 35 contract block at `pinn_architecture.md:445` (LOSS-04; D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A; AC-LOSS-04): "This file keeps the per-time causal weighting component as the default: `w_1 = 1`, `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, and `eta_c = 1`." | **RATIFIED — `A1`.** Retain the fixed value `η_c = 1`; do not add coefficient continuation. Amend what the exponent consumes from raw per-point `R̄` to the frozen-reference, 16-bin residual `R̃_b = R̄_b / R_ref`. Block 1 is re-ratified in kind, not in numeric value. |
| The `R̄` normalization and its reference scale | no normalization is specified anywhere in the spec; `pinn_architecture.md:435` consumes `R̄` unnormalized | none | **RATIFIED — `B2`, residual-wide.** Define one finite positive `R_ref` as the median of the 96 raw bin means produced at initialization by the fixed six-case GATE-04 seed/IC probe (`6` cases × `M=16` bins). Each case uses the recorded probe seed and exactly 4096 stratified times, 256 per fixed bin; all 96 bin means and the sampling/config provenance are retained. Detach and freeze `R_ref` for all of Stage 0. Use `R̃_b` both in the causal exponent and in the outer training physics loss; never update the reference online. Persist its value, cases, statistic, tree/config identity, and invalidation inputs. Log raw and normalized residual/loss views; every pre-existing absolute acceptance or safety threshold keeps its raw-unit meaning and is either evaluated on the raw view or transformed explicitly by `1/R_ref`. |
| `ω₀` / `first_omega_0`, the SIREN initialization scale | `pinn_architecture.md:181` (§2.2: "`first_omega_0` is fixed at `30` and is not scheduled during training.") | the fixed-at-30 sentence at `pinn_architecture.md:181` | **RATIFIED — `C1` / `D3-A`; NOT AMENDED.** Retain `first_omega_0 = 30`, with no in-run scheduler and the existing fresh-initialization rule for any future ablation. The unresolved stack-level scaling law is non-blocking for this ruling because this surface does not change and `R_ref` is measured on the actual initialized recipe. |
| `N_t` / `n_col`, the collocation-point count | `pinn_architecture.md:454` (`n_col=4096`), `pinn_architecture.md:461` (range 2048–4096); current run `pinn/train.py:1033` (`collocation_count=16`) | GAP-39-12 RESOLVED-WITH-INSTRUCTION / owner-delegated Option C fixes 4096 total per training batch with near-even selected-slot quotas; SPEC-06 binds the causal prefix length jointly to `η_c` | **RATIFIED — `D3`, jointly with `A1`, preserving GAP-39-12's total-budget unit.** `n_col = 4096` is the **total per training batch**, not a per-trajectory count. For a 256-slot replay-plus-lookahead batch, every selected trajectory slot contributes one independently drawn point within each of `M = 16` fixed equal bins in normalized time `u`, giving exactly 256 rows per bin and 4096 total. The batch-global causal prefix has 16 terms and is taken over the 16 per-bin mean residuals, never over all 4096 rows and never across a flattened point order. Replacement-padded occurrences remain distinct selected slots. The replay-only 240-slot allocation follows the deterministic remainder rule in the checkpoint-② discharge section. Microbatching may not reset or truncate the 16-bin aggregate/prefix. Any change to the total, slot semantics, `M`, or bin/allocation rule triggers re-measurement of `R_ref` and a fresh GATE-04 pass. |
| The causal-exponent clip's declared semantics | `pinn_architecture.md:668-671` | the underflow-only purpose at `pinn_architecture.md:668-671`, plus the Phase 35 guard block at `pinn_architecture.md:692` deferring the numeric bound | **RATIFIED — `E1` / `D5-A`; NOT AMENDED.** Retain the underflow-only purpose and the active dtype/device normal-floor guard `B = -log(finfo(dtype).tiny)`; choose no tighter semantic cap and do not use wider precision as a calibration remedy. Reject non-finite residuals/prefixes before clipping. Log the normalized unclipped exponent and a per-step binding count; any binding at initialization fails GATE-04. |

This section is filled either directly by the owner at checkpoint ① or after `trainex-r3` delivers. In the latter case the round's consolidated decision sheet is a candidate presented for ratification — not the ratification itself.

## Checkpoint ② preparation — pointers for the owner, no candidates (agent-prepared)

CHECKPOINT-2-PREPARED
Written 2026-09-03 by plan 54-13. Placed beside the existing record under an
append-only authority: no existing line of this file was deleted, reordered or
rewritten to admit it.

### ON-THE-TABLE — the artifacts the owner reads at this checkpoint

Each entry names the artifact by full repository path and states what it is for,
not what it concludes.

- `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/trainex-r3-resolution-doc.md` — the round's consolidated candidate document: the thing being ruled on, carrying the agents' menus with their authors' attributions.
- `docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/2026-09-02-trainex-r3-rule19-claim-verification.md` — the ERW Rule-19 verification report: the per-claim verdicts and the independence ledger that govern how much weight an agreement between the two reports carries.
- `.planning/phases/54-recalibration-decision-grounding/54-PREMISE-ADJUDICATION.md` — the premise adjudication record: the premise findings and the re-frame determination that travel with the round's answers.
- `.planning/phases/54-recalibration-decision-grounding/54-INTAKE.md` — the intake record: the certification of the two returned reports and the access-mode divergence finding with its consequences.
- `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/DELIVERY-NOTE.md` — the round's routing record: the join points the consolidation followed and the live-tree pin the verification was checked against.

The consolidated candidate sheet carries, besides its five enumerated-surface
rows, a separately-headed group (`CANDIDATE-SHEET`, `### Rows that are NOT
enumerated packet surfaces`): one `MERGED` row for the packet's framed `§5.6`
couplings question, one `ADDITIONAL` row for a scope question its author marks
not a menu and not put forward, and one `ADDITIONAL` row for a
next-research-expenditure question. They are named here so the owner sees the
whole sheet; their content lives in the consolidated document and is not
repeated.

### SURFACE-COMPANION — where each surface's entries live and what trust the round recorded

The rows below follow the checkpoint ② table's row order exactly, and that order
carries no precedence, no priority and no sequencing implication. Every cell
carries a pointer or a transcribed classification; a column with nothing to
record would say so, and none here is empty.

| Surface | Where its candidate entries are | Trust status the round recorded | Premise findings that reach it | Routed gaps that bear on it |
|---|---|---|---|---|
| `η_c`, the causal-weight exponent coefficient | `JOIN-4-MENUS`, `### \`S1\` — the causal-weight exponent coefficient`; `CANDIDATE-SHEET` row `S1`; composed-recipe elements in `JOIN-5-COHERENCE` | transcribed literal `SCALING-AGREED` on this surface's own law; the same cell records the menu as downstream of the round's one scaling dispute (`X-12`, `GAP-54-04` `OPEN`) and therefore not presented as trusted. Plain-language reading: the law is agreed but the menu is not trusted while the dispute behind it stands | `PREM-09` `CONTRADICTED`; `PREM-05`, `PREM-07`, `PREM-08`, `PREM-10`, `PREM-13` `QUALIFIED`; every answer on this surface `USABLE-QUALIFIED` | `GAP-54-03`, `GAP-54-05`, `GAP-54-09` |
| The `R̄` normalization and its reference scale | `JOIN-4-MENUS`, `### \`S2\` — the residual normalization and its reference scale`, including the `S2b` scope sub-decision joined in the same section; `CANDIDATE-SHEET` row `S2` | transcribed literal `SCALING-AGREED` on this surface's own law; downstream of the `X-12` dispute (`GAP-54-04` `OPEN`), so the menu is not presented as trusted; the scope difference is `X-18`, `OPEN-DISPUTE`, entitlement `NOT-CORROBORATED`, recorded as a mechanism-location difference rather than a scaling law; the joined reference options carry `NOT-CORROBORATED` (ledger row `X-16`). Plain-language reading: the law is agreed but neither the menu nor the reference choice is trusted while the dispute stands | `PREM-09` `CONTRADICTED`; `PREM-02` `UNSETTLED`; `PREM-11`, `PREM-13`, `PREM-14` `QUALIFIED`; every answer on this surface `USABLE-QUALIFIED` | `GAP-54-03`, `GAP-54-07` |
| `ω₀` / `first_omega_0`, the SIREN initialization scale | `JOIN-4-MENUS`, `### \`S3\` — the SIREN initialization scale`; `CANDIDATE-SHEET` row `S3` | transcribed literal `SCALING-DISPUTED` — the surface the round's one scaling-law disagreement sits on; `X-12`, `OPEN-DISPUTE`, entitlement `NOT-CORROBORATED`; the menus on this surface are not trusted until `GAP-54-04` is settled, with both underlying verdicts (`R-04`, `CB-07`) routed `NOT-VERIFIABLE-HERE`. The row further records one element outside the authorized amendment set, its scope question routed as `GAP-54-02`. Plain-language reading: this is the disputed surface, and nothing on it is trusted before the dispute is settled | `PREM-01`, `PREM-12` `CONTRADICTED`; `PREM-02` `UNSETTLED`; `PREM-03`, `PREM-04`, `PREM-13` `QUALIFIED`; every answer on this surface `USABLE-QUALIFIED` | `GAP-54-02`, `GAP-54-04`, `GAP-54-08` |
| `N_t` / `n_col`, the collocation-point count | `JOIN-4-MENUS`, `### \`S4\` — the collocation-point count`; `CANDIDATE-SHEET` row `S4` | transcribed literal `SCALING-AGREED` on this surface's own law; not named downstream of the `X-12` dispute; entitlement `NOT-CORROBORATED` (ledger row `X-08`), disposition `RECONCILABLE` on a qualifier the ledger names. Plain-language reading: the law is agreed and the remaining difference is recorded as reconcilable rather than resolved. The pre-declared completeness rule binds this row | `PREM-07`, `PREM-08` `QUALIFIED`; `PREM-18`, `PREM-19` `INTACT`; every answer on this surface `USABLE-QUALIFIED` | `GAP-54-05` — the count's unit is fixed by no consulted source |
| The causal-exponent clip's declared semantics | `JOIN-4-MENUS`, `### \`S5\` — the causal-exponent clip's declared semantics`; `CANDIDATE-SHEET` row `S5` | transcribed literal `SCALING-AGREED` on this surface's own law; not named downstream of the `X-12` dispute; entitlement `CORROBORATED` (ledger row `X-07`), the class being machine constants neither agent took from the package; `CC-4` `CONFIRMED-NARROWER` travels with the row. Plain-language reading: the law is agreed and the machine-constant element is corroborated | `PREM-05`, `PREM-16` `QUALIFIED`; `PREM-17`, `PREM-19` `INTACT`; every answer on this surface `USABLE-QUALIFIED` | `GAP-54-06`, carrying the conditional second-optimizer-phase risk both reports raise |

### COMPLETE-RULING-REQUIRES — the three things a complete ruling must record

Stated as requirements on the ruling, never as statements about its content.

1. **A disposition for every surface in the table above.** The completeness rule in the `## Completeness rule (pre-declared)` section of this file remains in force and is cited here rather than re-derived: a ruling that does not dispose of the surface it names is incomplete, is routed back to the owner as a gap, and is never completed by an agent choice.
2. **A re-ratification for every locked contract the ruling amends.** The standing amendment discipline (`.planning/REQUIREMENTS.md` SCOPE-38) is what makes a changed value without a re-ratified contract an illegal edit, and each framing below is drawn from it. A ratification amending a contract records the provenance of the new decision, names the superseded ruling — which each block below already names — and carries a re-issued acceptance criterion. Nothing is named here about what any amendment would say. Per-block framings: Block 1, the `η_c` Phase 35 contract (`pinn_architecture.md:445`) — a ratification touching it records a new provenance, names the Phase 35 ruling already named in the block, and re-issues the acceptance criterion. Block 2, the `first_omega_0` fixed-at-30 sentence (`pinn_architecture.md:181`) — a ratification touching it records a new provenance, names the Phase 20 ruling already named in the block, and re-issues the acceptance criterion. Block 3, the clip's underflow-only purpose (`pinn_architecture.md:668-671`) — a ratification touching it records a new provenance, names the Phase 35 guard already named in the block, and re-issues the acceptance criterion. A block whose contract the ruling does not touch is marked as not amended rather than deleted, which is what this file already states above, and is cited here rather than restated.
3. **A disposition or an explicit deferral for every gap this pass routed**, listed by identifier and classification: `GAP-54-01`, semantic (the anchor); `GAP-54-02`, cross-phase reframing; `GAP-54-03`, semantic; `GAP-54-04`, semantic; `GAP-54-05`, semantic; `GAP-54-06`, semantic; `GAP-54-07`, semantic; `GAP-54-08`, semantic; `GAP-54-09`, semantic; `GAP-54-10`, process-artifact schema; `GAP-54-11`, process-artifact schema. A deferral is a recorded instruction and not a silence.

### THIS-BLOCK-IS-NOT — what this block does not do

This block selects nothing, marks nothing, ranks nothing and disposes of nothing. The candidates are the round's, attributed to their authors in the consolidated document; the disposition cells and the re-ratification fields above remain unfilled and only the owner fills them; and this block's existence changes neither the phase's status nor the anchor gap's.

END-CHECKPOINT-2-PREPARED

## Checkpoint ② discharge — scientific basis and downstream reading

The prepared block above is a timestamped record of what was presented before
the ruling. Its statements that fields were `PENDING` were true at presentation;
the filled table and re-ratification blocks in this file are now authoritative.

The ruling adopts the open-book report's coherent `J1` family, with the count
unit and optimizer-phase semantics made explicit by this owner-authorized
adjudication. The decisive mechanics are:

1. With `R̃_b ≈ 1`, `η_c = 1`, and a 16-term exclusive prefix, a flat profile has
   endpoint exponent about `15`, endpoint weight `exp(-15) ≈ 3.06e-7`, and a
   float32 normal-floor margin `87.33654 / 15 ≈ 5.82`. The fixed reference leaves
   the weights sensitive to genuine residual descent; an online reference could
   divide that descent back out. This flat-profile calculation is illustrative,
   not a guarantee; GATE-04 evaluates every actual 16-term probe vector and its
   maximum unclipped prefix.
2. Applying the same frozen normalization to the training physics loss addresses
   the established severe physics/data conditioning mismatch. The stronger claim
   that every data-gradient component disappeared is not relied on. Raw diagnostics
   remain mandatory so normalization cannot make physical acceptance look better.
3. Both reports retain `first_omega_0 = 30`. Their incompatible stack-level
   scaling arguments do not justify a frequency change: even the optimistic
   fourth-power estimate says the enumerated reductions are insufficient alone,
   while the frozen measured reference removes raw initialization magnitude from
   the causal calibration.
4. Separating 4096 total batch samples from a 16-term causal prefix prevents
   sample count from multiplying causal strength and makes `front_idx` denote a
   fixed time bin. A front from a resampled training batch remains a stochastic
   diagnostic, not persistent advancement evidence. This retains GAP-39-12's
   owner-ratified total-budget and
   balanced-identity semantics; stratified exact allocation supersedes only its
   independent full-domain time-draw clause and supplies the bin-edge and
   empty-bin policy the candidate record left for ratification.
5. The clip remains a numerical guard, never a way to manufacture front progress.

**Optimizer-phase boundary — explicitly deferred.** This checkpoint does not
amend the optimizer contract: SCOPE-33 authorizes the five recalibration surfaces
and coupled count disposition, not new L-BFGS semantics. The conditional risk
about recomputing detached causal weights inside a line search remains real, but
`GAP-54-06` defers its disposition to owner checkpoint ③ in Phase 57, before any
RUN-04 execution. Phase 56 may implement and gate the five ratified surfaces; it
may not silently choose either second-optimizer-phase behavior.

**Front-monitoring boundary.** Adam's training-batch `front_idx` is diagnostic
only: selected slots and within-bin times can change, so a high-water mark over
those samples is upward-biased and cannot prove learning. Owner checkpoint ③
must define invariant-B advancement on a fixed, pre-registered monitoring
context (fixed IC slots and fixed within-bin times, reevaluated as model
parameters change), or ratify another estimator that separates parameter
improvement from resampling. The exact monitoring aggregation remains checkpoint
③'s decision and is not invented here.

**Batch allocation and bin policy.** The fixed bins are
`[b/16,(b+1)/16)` for `b=0…14` and `[15/16,1]` for the last. In a 256-slot
batch, draw one point per selected slot inside every bin. In a replay-only
240-slot batch, first draw one point per slot in every bin (`3840` rows), then
use one canonical seeded permutation of the 240 slots: bins 0–14 each give a
second draw to the next disjoint 16-slot slice of that permutation, and bin 15
gives a second draw to its first 16 slots. Each bin therefore has exactly 256
rows; 224 slots have 17 rows and 16 slots have 18, matching GAP-39-12's
near-even quota. A bin residual is the mean over its 256 rows. Empty bins are
impossible, and the causal prefix is one batch-global 16-bin prefix. This
re-ratifies the time allocation only; energy continues to reuse the physics set.

**Reference invalidation.** Re-measure `R_ref` and re-run GATE-04 after any change
to `first_omega_0`, depth, width, power-skip exponent, LayerNorm placement or
stabilizer, initialization bounds, `D`, `T`, `epsilon_soft`, IC13 normalization,
`n_col`, `M`, count unit, selected-slot semantics, or bin/allocation semantics.
A resource failure at the ratified total batch count is a fail-closed result,
not permission to reduce the count silently.

**Scope and sequencing.** The authorized surface set is not widened. The
power-skip stack remains a future ablation, and this ruling does not claim the
recipe will train or achieve trajectory accuracy. Phase 54 closes after its own
verification; Phase 56 remains closed until independent Phase 55 also completes.

## Completeness rule (pre-declared)

A ruling that does not dispose of `N_t` / `n_col` is **incomplete**: it leaves SPEC-06's joint-ratification requirement unmet, is routed back to the owner as a gap, and is never completed by an agent choice.

The mechanical reason: `w_n` is an exclusive prefix sum over collocation points, so the exponent moves by roughly 256× between `pinn/train.py:1033`'s `collocation_count = 16` and `pinn_architecture.md:454`'s `n_col = 4096` — and an `η_c` disposition is therefore under-determined without an `N_t` disposition.

## SCOPE-38 re-ratification lines

A changed number without a re-ratified contract is not a legal v2.3 edit. Each block below corresponds to one locked contract the ruling could amend; a block whose contract the ruling does not touch is marked `not amended` rather than deleted.

**Block 1 — the `η_c` Phase 35 contract**

- **Contract marker:** "This file keeps the per-time causal weighting component as the default: `w_1 = 1`, `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, and `eta_c = 1`."
- **Location:** `pinn_architecture.md:445`
- **Superseded ruling:** Phase 35 D-04 RESOLVED-WITH-INSTRUCTION / owner-ratified Option A (LOSS-04; AC-LOSS-04)
- **New decision provenance:** Owner instruction on 2026-09-04 expressly delegated checkpoint-② adjudication to the Codex primary agent using its best mathematical and scientific reasoning. After reading the trainex-r3 candidate document, Rule-19 verification report, premise adjudication, intake record, and routed gaps, that adjudication ratified `A1 + B2 (residual-wide) + C1 + D3 + E1`. This supersedes the Phase 35 ruling only as to the exponent's raw-residual argument and one-point-per-prefix-term structure; `η_c = 1` remains fixed.
- **Re-issued acceptance criterion:** AC-LOSS-04 is re-issued without a new identifier: the default Stage-0 causal loss uses exactly `η_c = 1`, `n_col = 4096` total per training batch, `M = 16` fixed equal-`u` bins with exactly 256 rows per bin, `R̃_b = R̄_b/R_ref`, one batch-global exclusive 16-bin prefix, and residual-wide normalization. Each of the fixed six initialization-probe cases uses exactly 4096 recorded-seed stratified times (256 per bin); `R_ref` is the finite positive median of the resulting 96 raw bin means, is detached and frozen, all 96 constituents and provenance are retained, and every trigger named in the checkpoint-② discharge section invalidates it. Raw and normalized diagnostics are both recorded; raw-unit thresholds are never silently applied to normalized values. GATE-04 must evaluate the actual full vectors and fail closed on any non-finite input, any floor-bound initialization weight, a degenerate weight vector, or a front that cannot respond to controlled residual reduction. A resampled training-batch front is diagnostic only; invariant-B evidence follows the fixed-monitor boundary above. GAP-54-06's L-BFGS question is not part of this criterion and must be settled at checkpoint ③ before RUN-04.

**Block 2 — the `first_omega_0` fixed-at-30 sentence**

- **Contract marker:** "`first_omega_0` is fixed at `30` and is not scheduled during training."
- **Location:** `pinn_architecture.md:181`
- **Superseded ruling:** Phase 20 ARCH-01 (locked SIREN initialization; no omega0 scheduler)
- **New decision provenance:** **NOT AMENDED** — checkpoint ② ratifies `C1` / `D3-A`, retaining `first_omega_0 = 30` and the existing no-scheduler/fresh-reinitialization contract.
- **Re-issued acceptance criterion:** **NOT AMENDED** — Phase 20 ARCH-01 remains the acceptance criterion; any future frequency change remains a separately ratified fresh-initialization ablation and invalidates `R_ref`.

**Block 3 — the causal-exponent clip's underflow-only purpose**

- **Contract marker:** "Clip the causal exponent to avoid underflow, but do not choose a numeric clipping bound in Phase 19; surface a gap if one is needed. The causal exponent clip is required only to avoid underflow."
- **Location:** `pinn_architecture.md:668-671`
- **Superseded ruling:** the Phase 35 guard block (numeric bound deferred to FUT)
- **New decision provenance:** **NOT AMENDED** — checkpoint ② ratifies `E1` / `D5-A`, retaining the clip's underflow-only purpose and dtype/device-derived normal-floor guard. Added logging and GATE-04 refusal behavior are observability, not a repurposing of the clip.
- **Re-issued acceptance criterion:** **NOT AMENDED** — the Phase 35 underflow-only criterion remains; implementations additionally reject non-finite values before clipping, log the unclipped exponent and binding count, and fail GATE-04 if the guard binds at initialization.

**Block 4 — the DATA-05 collocation allocation and time-draw contract**

- **Contract marker:** GAP-39-12 Option C fixes a provisional total `C = 4096` per training batch, near-even quotas over the canonically ordered selected-slot multiset, and independent continuous time draws over the full domain for each allocated row.
- **Location:** `.planning/milestones/v2.0-phases/39-data-ingestion-stage-0-population-scan/39-GAPS.md:524-608`
- **Superseded ruling:** GAP-39-12 RESOLVED-WITH-INSTRUCTION, owner-delegated Option C (2026-07-14), **only as to its independent full-domain time-draw clause**. Its total-budget, selected-slot multiplicity, exact-cardinality, near-even identity weighting, seeded determinism, and shared physics/energy-set requirements remain in force.
- **New decision provenance:** Owner instruction on 2026-09-04 delegated checkpoint-② adjudication to the Codex primary agent. The subsequent repository-wide unit trace found GAP-39-12, which the Phase-54 packet's narrower consulted-source search had missed. The ruling retains that grounded unit and re-ratifies D3's fixed-bin stratification as the minimum amendment needed to separate estimator count from causal-prefix length.
- **Re-issued acceptance criterion:** A full 256-slot batch emits exactly 4096 physics rows as one independently sampled time in each of 16 fixed bins for every selected slot. A 240-slot replay-only batch uses the seeded 3840-plus-256 remainder construction stated above, yielding exactly 256 rows per bin and per-slot totals 17 or 18. Replacement multiplicity is preserved; every bin is non-empty by construction; each bin residual is the mean of exactly 256 rows; one batch-global exclusive prefix is formed over the 16 bin means; energy reuses the same set; and microbatching preserves complete bin aggregates and never resets the prefix.

Note: §2.4's hyperparameter-table row for `first_omega_0` (`pinn_architecture.md:274`, header `:267`) is already routed to Phase 56 by Phase 53's unswept inventory and is outside this file's four blocks.

## Anchor-drift warning (for Phase 56)

`.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` quote the following four anchors, and all four were verified to point at unrelated content in the live tree after Phase 53's `spec(53)` commits shifted the file:

- `pinn_architecture.md:424`
- `pinn_architecture.md:167`
- `pinn_architecture.md:433`
- `pinn_architecture.md:440`

The verified replacements are `pinn_architecture.md:445`, `pinn_architecture.md:181`, `pinn_architecture.md:454`, and `pinn_architecture.md:461`, respectively.

This file does not correct those documents — that edit belongs to the owner or to the Phase 56 plan (54-CONTEXT.md Open Item 5). Any Phase 56 edit must re-derive its anchor by content match rather than trusting a line number.
