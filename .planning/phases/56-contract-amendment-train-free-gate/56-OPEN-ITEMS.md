---
phase: 56
milestone: v2.3
created: 2026-09-07
---

# Phase 56 Open Items — Contract Amendment & Train-Free Gate

This document is the durable register of every decision Phase 56 deliberately
did **not** make, and of the one pre-existing test failure it deliberately
did not fix. Its purpose is narrow: so that an omitted decision is never
later mistaken for a forgotten one, and a surfaced gap is never later
mistaken for a resolved one. It resolves nothing. Where a decision belongs to
the owner, this document points at the authoritative blocking record
(`56-GAPS.md`) rather than restating, ranking, or recommending among the
options recorded there.

## Section 1 — GAP-56-01 (GATE-04 condition (ii)): still OPEN

Phase 56 did not resolve GAP-56-01. What the phase built instead of a
resolution is a structurally-present, never-satisfiable slot:

- `condition_ii_verdict(weights)` (`pinn/verification/gate04_train_free.py`)
  always raises `NotImplementedError`, unconditionally, for every input,
  naming GAP-56-01 in its message. Nothing else in the module calls it.
- `condition_ii_diagnostics(weights, causal_clip_min_weight)` computes
  descriptive statistics only — the tail dispersion metric
  `coefficient_of_variation_tail`, `monotone_non_increasing`,
  `dynamic_range_decades`, and `distinct_non_floor_count` — with a
  `status: "UNRATIFIED"` field and no key named or implying a threshold, a
  pass, or an "ok" state.
- `Gate04Verdict.unratified_conditions` carries `("ii",)` on every verdict
  this gate renders.
- The operator CLI's printed summary line appends `INCOMPLETE` plus the
  `GAP-56-01` reference whenever `unratified_conditions` is non-empty, so no
  reader of a PASS verdict can mistake it for a complete GATE-04 clearance.

No numeric threshold, comparison constant, or controlled-reduction pass
margin exists anywhere in this phase's output — not in the module, not in
its tests, not in this document. The four candidate options the owner may
choose among remain exactly as `56-GAPS.md` records them under GAP-56-01.
This document points at that file as the authoritative blocking record and
does not restate, rank, or recommend among them.

## Section 2 — Structural findings that must survive into the owner's ruling

Two structural findings about the ratified formula are recorded here so they
outlive this phase's plan artifacts, with provenance in `56-RESEARCH.md` Part
(b) and now also in the code itself
(`condition_iii_diagnostics`'s docstring, `pinn/verification/gate04_train_free.py`).

**Finding 1 — a front index of 0 at initialization is the expected healthy
result, not a failure signal.** All six audited cases produce an unperturbed
front index of 0 at initialization under the healthy, amended recipe,
because each case's second weight already falls below the half threshold
that defines `front_idx` (the trainer's own formula: the largest `n` with
`w_n` strictly greater than one half). A condition-(iii) test written as a
fixed positive-front check (the front index compared against zero) would
therefore reject every healthy case. The healthy-initialization expectation
is a graded weight vector, not an advanced front.

**Finding 2 — a residual reduction confined to the late bins cannot move the
front index at any magnitude.** The weight at bin `n` depends only on the
exclusive prefix accumulated over the bins before it (bins `0` through
`n-1`); nothing that happens at or after bin `n` can change it. Any
controlled-reduction test design that happens to perturb only late bins will
report no sensitivity regardless of magnitude or design, and that
non-response says nothing about whether the recipe is healthy — it is a
structural artifact of the ratified formula, not evidence about recipe
health.

Both findings are mechanistic facts about the ratified formula, verified by
direct computation (`56-RESEARCH.md` Part b.3 through b.5, and the code's own
sensitivity-sweep tables). They are recorded as inputs the owner's eventual
ruling will need — never as a recommendation about what that ruling should
be.

## Section 3 — GAP-56-02 (section 2.4 table scope): still OPEN

Phase 56 did not resolve GAP-56-02. Section 2.4's hyperparameter table, its
"Recommended Value" column heading, and its row for the SIREN
initial-frequency parameter (`first_omega_0`) were deliberately not touched
by any task in this phase. The three candidate mechanisms the owner may
choose among — applying locked/default markers to the row and, for
consistency, auditing the rest of the table; adding a minimal header or
footnote note pointing at the existing section 2.2 lock without touching the
convention; or leaving section 2.4 untouched and re-routing the item to a
future documentation-convention pass — remain exactly as `56-GAPS.md` records
them. This document does not restate, rank, or recommend among them.

The section 2.2 "`first_omega_0` fixed-at-30 sentence NOT AMENDED" record
(landed in `pinn_architecture.md` by plan 56-05) names this omission
explicitly, so a later reader sees the section 2.4 table's untouched state as
deliberate rather than forgotten.

One fact the research established will matter whichever mechanism the owner
eventually chooses: the render-oracle adjudication file
(`tools/spec-render-check/adjudications/22-02-pinn-architecture.json`)
already carries entries pointing at that table's heading and at the
`first_omega_0` row. Any future edit to section 2.4 Table 1 requires those
entries to be re-verified against the tree state at the time of that edit.

## Section 4 — Accepted pre-existing failure: the Phase 38 spec-freeze guard

**The facts.** The Phase 38 test package (`tests/phase38/test_prohibitions.py`)
carries a mechanical spec-freeze guard: `test_spec_byte_identity_endpoint_sha256`
asserts the two framework specification documents (`ctl_instruction.md`,
`pinn_architecture.md`) are byte-identical to a frozen pre-v2.0 baseline via
SHA-256 comparison, and `test_spec_history_no_touch_since_phase_base` asserts
neither file has been touched in git history since a fixed base reference.
Both tests enforce the same superseded SCOPE-18 prohibition; the first
asserts it in a literal message. This guard has been failing since Phase 53,
the first phase to edit `pinn_architecture.md` under a later, narrower
grant. Phase 55 recorded both failures as pre-existing and explicitly out of
its own scope, without touching the guard. This phase's own SCOPE-38
amendment (SPEC-01, SPEC-06) necessarily keeps both tests failing, because
editing `pinn_architecture.md` is the entire point of this phase's grant.

**Phase 56's decision.** The guard is NOT edited by Phase 56. Its two
failures are accepted and recorded here as pre-existing, for four reasons.

1. **Outside the grant on a plain reading.** SCOPE-33 authorizes
   framework-specification edits, narrowly enumerated (the routed VER-20
   items plus the `n_col`/`N_t` disposition). A file inside the Phase 38
   test package is neither a framework specification nor one of the
   enumerated items, so editing it is outside SCOPE-33's grant on a plain
   reading.
2. **Self-certification.** Re-baselining the guard inside the very phase
   that changes the file the guard watches would let this phase certify its
   own edit as acceptable — the same anti-pattern this repository's
   committed-fixture integrity guards exist to prevent, and which this
   phase itself applies to its own demonstration fixture (the dedicated
   SHA-256 guard over `tests/phase56/fixtures/pre_amendment_baseline.json`).
3. **Precedent.** Phase 55 set this precedent one week earlier, recording
   the same two failures as pre-existing and out of scope without touching
   the guard. This phase follows that precedent rather than diverging
   without cause.
4. **A governance decision, not a phase-scoped one.** Choosing a new base
   reference for the guard is a decision about which tree state is the
   milestone's baseline — a decision that belongs to a milestone-close or
   documentation-convention pass, not to a phase whose grant is narrow by
   design.

**Follow-up.** The guard should be re-baselined or retired by whichever
later pass carries the authority to make that governance call — not by this
phase. Until then, any full-suite run of this repository will show
**exactly two failures** in `tests/phase38/test_prohibitions.py`, both
asserting the same superseded prohibition. The distinguishing text is the
literal string "SCOPE-18 prohibits Phase-38 edits to framework specs"
(asserted verbatim by `test_spec_byte_identity_endpoint_sha256`), together
with the sibling `test_spec_history_no_touch_since_phase_base` failure over
the same two spec paths. A future reader can confirm at a glance that a red
suite showing exactly these two named failures is this known, accepted
condition rather than a new regression; any other failure count, or a
failure with a different message, is a new condition requiring
investigation.

## Section 5 — STOP protocol classification note

The two gaps recorded in Section 1 and Section 3 (GAP-56-01, GAP-56-02) are
MUST-surface decisions under the CLAUDE.md STOP protocol, left with the owner
and not invented by this phase or by this document. The scoping decision
recorded in Section 4 (the Phase 38 guard) is a mechanical scoping call, made
deliberately and recorded here rather than taken silently.

Two further presentation-only choices made during the amendment (plan 56-04)
are recorded in their own plan summary as mechanical choices, not repeated
here as decisions of this document: rendering the ratified relations
(`R̃_b`, `w_n`) in ASCII inline-code notation, matching the retained Phase 35
block, rather than authoring display mathematics; and transcribing the
reference-invalidation trigger list as running prose — its source form in
`54-RULING.md` — rather than reformatting it as a bulleted list.

---
*Phase: 56-contract-amendment-train-free-gate*
*Recorded: 2026-09-07*
