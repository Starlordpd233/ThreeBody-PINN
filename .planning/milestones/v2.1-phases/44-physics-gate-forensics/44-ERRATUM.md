# Phase 44 Erratum — DIAG-04 Rankings Qualified by Verified Spec Divergences

**Issued:** 2026-07-24, after the trainex-r2 research result returned and its
repository-derived claims were independently verified.

**Why this is a separate file.** `44-DIAGNOSIS.md` is pinned byte-identically
inside the delivered trainex-r2 package (`45-AUDIT.md` Check 4, sha256
`466000bc…`) and Check 5 asserts no source changed since `source_baseline`.
Editing the diagnosis in place would retroactively falsify both checks on an
already-delivered package. The diagnosis is therefore left untouched and this
erratum carries the qualification. Anyone reading `44-DIAGNOSIS.md` should read
this file alongside it.

## What is qualified

Phase 44 met its stated success criteria on the evidence available to it. Its
numbers are unchanged and remain re-derivable. What is qualified is the
**interpretive layer** — the DIAG-04 candidate-cause rankings — because the
diagnosis was assembled on an assumption that has since been falsified:

> that the executed Stage-0 pilot implemented the locked framework specs.

It did not, in at least five verified respects. Evidence:

- `docs/work/reviews/milestone_v2.1/45-trainex-r2-erw-package-assembly/2026-07-24-trainex-r2-report-factw-verification.md`
  — per-claim verification of the trainex-r2 report's repository-derived claims.
- `docs/work/reviews/cross_cutting/stage0-conformance-audit/2026-07-24-stage0-training-path-conformance-audit.md`
  — the full divergence inventory (findings C-01…C-08), the verified-clean
  inventory, and the unresolved items.

Phase 44 could not have consulted a known-divergence register because none
existed; the divergences were flagged only in inline code comments. That
structural gap is the subject of
`docs/work/designs/cross_cutting/training-verification-regime/2026-07-24-verification-enforcement-charter.md`.

## Per-row effect on the DIAG-04 table

| DIAG-04 row | Original rank | Effect |
|---|---|---|
| H-01 / H-03 — population-scale generalization shortfall | Strong; "no contradicting evidence" | **Weakened.** "The failure is population-wide" still holds (uniform 1500/1500, F-02). "Population *scale* is the distinguishing cause" is no longer supported by DIAG-01..03 alone: the Phase-38 control rung differed from the pilot in objective, LR, IC₁₃, and target frame, and the uniform failure is equally consistent with any recipe-level mechanism applying identically to every trajectory. The "no contradicting evidence" cell no longer reads cleanly. |
| H-04 — loss-term imbalance | Moderate | **Qualified both ways.** Dominance facts (F-07, F-09) hold, but the executed λ vector was not the locked Stage-0 vector (λ_E = 1.0 against a locked 0), so the pilot never instantiated the "conservation weights zero by design" configuration. Loss-value dominance also remains an ambiguous proxy absent per-term gradient evidence, which was never logged (C-06). |
| H-05 — optimization / warmup pathology | Moderate | **Sharpened.** The standing optimization-level pathology is the causal collapse: physics supervision reached one collocation point out of sixteen for 300/300 steps in all five runs (C-01/C-02). DIAG-02 recorded `front_idx = 0` at the spikes but did not surface it as a finding. |
| H-06 — normalization / data-scale mismatch | Moderate | **Gains the most.** Now has concrete, checkable loci rather than a generic scale suspicion: the ε_H stand-in (C-04), the R̄ factor (C-03), the `L_data` reduction ambiguity (C-07), and the unresolved target-frame question. |
| H-07 — insufficient budget | Weak | **Confounded further.** The Weak ranking leaned on the 176-step Phase-38 comparator, which differs from the pilot in recipe and frame. Neither supports nor refutes a budget story cleanly. Note the 300-step budget interacts with C-01: the mechanism that would advance the causal front never had the steps to do so. |
| H-02 / H-08 — pre-registered rubric, tie handling | — | **Unaffected.** No evidence found against the process claims. |

## What this does NOT change

- Every measured number in `44-DIAGNOSIS.md` stands, including the GAP-44-01
  headline `max = 237.2086056078468` and the uniform 1500/1500 failure.
- Phase 44's remedy abstinence stands and was correct.
- No causal claim is established. The divergences are not proven to have caused
  the gate failure; they establish that the experiment was not a valid test of
  the design.

## Standing of this erratum — RESOLVED 2026-07-24

**GAP-44-02 resolved: Option C — erratum now, re-derivation mandatory later.**

Phase 44 stays closed and this erratum is the operative qualification. It is
explicitly **not** a correction: the DIAG-04 rankings are recorded as
under-determined rather than re-ranked, because nothing short of a conformant
Stage-0 run can discriminate the candidate causes, and no such run exists.

The condition on which Phase 44 is permitted to stay closed: **the next milestone
carries an explicit, mapped requirement to re-derive the diagnosis from a
conformant run**, with an acceptance check — not a best-effort intention. A
reader of `44-DIAGNOSIS.md` should treat its §7 rankings as superseded-pending-
re-derivation, and should expect that re-derivation to be a tracked deliverable
rather than an open-ended follow-up.

Full record: `44-GAPS.md` GAP-44-02; index `.planning/milestones/v2.1-GAPS.md`.
