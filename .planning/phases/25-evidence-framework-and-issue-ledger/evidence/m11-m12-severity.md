# Evidence Packet: M11/M12 - Severity reclassifications (M11 blacklist consumption; M12 points-per-trajectory)

## Header

| Field | Value |
|---|---|
| ID | `M11/M12` |
| Title | `Severity reclassifications (M11 blacklist consumption; M12 points-per-trajectory)` |
| Severity | `BLOCKING` (M11: per ledger; M12: BLOCKING-infeasibility claim rejected on arithmetic) |
| Current Status | `PENDING` |
| Current Verdict | M12: `accept-third-position`; M11: **explicit severity ruling** recorded in §Verdict M11 sub-part below (distinct from M12; not a placeholder) |
| Phase | `Phase 25 (EVID-10 record) / Phase 26 prioritization (M11) / Phase 27 (M12)` |
| Acceptance Check ID | `AC-PIPE-03 (M11) / AC-PIPE-04 (M12)` |
| Spec Sections Touched | `None (Phase 25 makes the severity ruling; no spec edit)` |
| Code Paths Touched | `Not code-applicable` |

This record adjudicates **two distinct findings** with two distinct verdicts. M12 has a deterministic arithmetic falsification of the BLOCKING-infeasibility claim. M11 is a **process-classification ruling** that the resolution doc explicitly defers to EVID-10 — Phase 25 makes the ruling here, grounded on the data-integrity argument (not architectural-harm narratives, which the doc flags as non-load-bearing). M11 and M12 sub-parts are clearly labelled where they diverge.

## Source Positions

| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` | **M12:** `02-resolution-doc.md §4.1 Q-B1:385-422` — BLOCKING claim ("standard trajectories cannot support 32 points/trajectory") is **wrong** on verified arithmetic; P1-4 `n_pts = min(32, int(0.5·n_snapshots))` is **rejected as a normative data-side rule**; the 0.5 factor is unevidenced and internally inconsistent with the issue doc's own verification checklist (expects `gold → 128`; neither `min(32, ·) = 32` nor `int(0.5 × ~1000) = 500` produces 128). <br><br> **M11:** `02-resolution-doc.md §3.3 Q-A3:221-254` — the contract is **blocking-grade, fail-closed precondition**; the *MAJOR→BLOCKING reclassification decision* is explicitly routed to Phase 25: "Whether M11's MAJOR→BLOCKING reclassification stands is EVID-10's call" (§3.3 reasoning, line ~238). M11 ground: data-integrity argument (§3.3 part 2) — IC-level exclusion follows from the byte-identical-subset relationship; before-statistics ordering prevents contamination; fail-closed follows from the exclusion guarantee. |
| `pinn_instruction/issues/02-data-pipeline-and-validation.md` | **M11 + M12:** `02-data-pipeline-and-validation.md:59-60,70-77` — the **Severity Reclassification Ledger** reclassifies M11 and M12 audit MAJOR → BLOCKING; M11 rationale: "A DataLoader that can silently admit blacklisted ICs would corrupt training data at ingestion time." M12 rationale: "54% sampling is infeasible and blocks batch construction." P1-3 (line ~285) and P1-4 (line ~286) carry the proposed fix: blacklist load at init; adaptive `n_pts = min(32, int(0.5 * n_snapshots))`. |

The issue doc's severity reclassifications are correct in spirit (both findings identify real gaps) but the **M12 BLOCKING-infeasibility rationale is arithmetically wrong** (32 ≤ 61 is trivially feasible), and the **M11 reclassification** is a *process classification* the resolution doc explicitly defers to Phase 25.

## Spec Evidence

- **M12:** `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` Mini-Batch Construction (lines ~1197-1201) — "Sample n_pts (e.g., 32) time points per trajectory: 50% uniform …, 50% weighted by acceleration norm." The "(e.g., 32)" is parenthetical/example, not a hard contract (addendum WR-03 confirms).
- **M12:** `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md §3.1` — snapshot-sourced data points; `points_per_trajectory = 32` default (a code default, not a spec contract; re-verified).
- **M11:** `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md §5.1` — gate-before-analysis ordering rationale (the spec's stated reason for fail-closed loader preconditions).

### Dataset Evidence (§3b)

**M12 falsification (the arithmetic):**
- `24-VERIFIED-FACTS.md CLM-10` (line 25, **corrected**): per-variant medians are **brutus_standard_quasi_random median=61 (min=59, max=61)**, `brutus_standard_quasi_random_gold_standard median=1003`, `brutus_hierarchical median=127 (min=126, max=127)`, `brutus_hierarchical_gold_standard median=1003`. The standard median of 61 (vs the claim "~59") and the hierarchical median of 127 (vs the claim "~125") are corrected values per D-09; the integer-rounded MEDIAN is authoritative.
- **M12 arithmetic check:** `32 ≤ 59` (M12 feasibility) — drawing 32 distinct points from 59-61 snapshots without replacement is **trivially possible**. The verified median (61) makes a fixed 32 feasible for every admitted standard-base file. The BLOCKING-infeasibility claim is **FALSIFIED on the corrected CLM-10 medians**.
- **M12 internal contradiction:** the issue doc's own verification checklist (line ~298) expects `gold → 128` — a value neither `min(32, ·) = 32` nor `int(0.5 × ~1000) = 500` produces. The 0.5 factor is internally inconsistent with the proposing document's own checklist. (Issue doc also references `59→29` in the same checklist — the cosmetic effect at the verified median is 32→30, not "infeasibility".)

**M11 grounding:**
- `24-VERIFIED-FACTS.md CLM-03` (line 17, **confirmed**): 65 IDs (2 hierarchical + 63 standard) = `{"hierarchical": 2, "standard": 63}` total **65**, confirmed by `probes/data02_blacklist.py` against `simulation_data/Documentation/problematic_ics_blacklist.json`. The CLM-03 count is grounded; the M11 *consumption* status is `unverified — SCOPE-10` (OI-8, outside grounding).
- **OI-8 carry-forward caveat** (from `24.5-READINESS-REPORT.md §4`, propagated per D-16): "M11 live-loader consumption status — does the live loader enforce the blacklist? Routed to Phase 25 / FUT-01 (outside grounding limits, SCOPE-10)." This caveat is **carried forward** in the M11 sub-part below and is **NOT resolved here** (the data-side contract is stated regardless; live-loader consumption is a Phase 26 PIPE-03 / FUT-01 question).

## FUT-01 Hand-off Note (formerly "Code Evidence")

Live code in `pinn/` is NOT a v1.4 or v1.5 evidence source per user directive 2026-05-19.

- **M11:** the M11 live-loader consumption question is explicitly outside grounding (SCOPE-10) and is **carried forward** to Phase 26 PIPE-03 / FUT-01. The relevant v1.3-era code paths (`pinn/basic_architecture.py`, `pinn/data-processing-pipeline-full.py`) are forward-pointing references only; the live-loader's actual blacklist enforcement is a Phase 26 / FUT-01 hand-off item, NOT a Phase 25 EVID-10 verdict.
- **M12:** `pinn/basic_architecture.py` snapshot-sourced data-point contract (§3.1, re-verified by the resolution pass) is forward-pointing only; the `points_per_trajectory = 32` default is a code default, not a spec contract.

## First-Principles Physics Check

**M12 arithmetic check (the determinative check):**

```
n_pts = min(n_pts_cap, n_snapshots(traj))      # locked data-side contract (resolution §4.1)
n_pts_cap = 32                                  # spec's example value (not a hard contract)
n_snapshots(standard) = 61 (median, min 59)     # CLM-10 corrected
32 ≤ 59 ⇒ 32 distinct points from a 59-61 pool is trivially feasible
```

The issue doc's claim "54% sampling is infeasible" is arithmetically wrong: 32/61 = 52.5% (not 54%, and not "infeasible"). The 0.5 factor's proposed effect at the verified median is 32 → 30 (cosmetic, not a feasibility change). The proposed `n_pts = min(32, int(0.5 * n_snapshots))` is therefore:

- **Arithmetically wrong as a feasibility claim** (the BLOCKING rationale is falsified by CLM-10).
- **Un-evidenced as a normative rule** (the 0.5 constant has no package source — not a dqa band edge, not a constraint, not a dataset fact).
- **Internally inconsistent with the issue doc's own checklist** (which expects `gold → 128`, a value the proposed rule cannot produce).

**M12 verdict grounding is independent of the resolution doc's arithmetic** (D-09): the falsification rests on the CLM-10 corrected medians (`24-VERIFIED-FACTS.md:25`) and the simple inequality `32 ≤ 59`, not on a doc citation.

**M11 arithmetic / data-integrity check:**

The M11 reclassification is a *process classification*, not a data fact. The resolution doc explicitly hands the reclassification decision to Phase 25. The grounding is the **data-integrity argument** (resolution §3.3 part 2), not architectural-harm narratives (the doc flags those as "plausible motivation but not load-bearing"; the contract stands on data integrity alone). The data-integrity argument:

1. IC-level exclusion follows from the byte-identical-subset relationship — a blacklisted `(family, id)` excludes every realization (base and gold) of that `physical_key` (gold ICs are a byte-identical subset of base ICs; a problematic IC is problematic at every fidelity).
2. Before-statistics ordering prevents blacklisted records from contaminating normalizers (medians dampen but do not eliminate the effect; NaN-poisoned records would dominate).
3. Fail-closed follows from the exclusion property being a *guarantee*: a loader that silently proceeds without the blacklist cannot certify the property M11 exists to enforce.

CLM-03 grounding (65 IDs confirmed) is the empirical anchor; the consumption question is OI-8 (SCOPE-10, outside grounding) and is **not** part of the Phase 25 verdict's evidence basis.

## Verdict

This record records **two distinct verdicts** (one per finding), clearly labelled and DISTINCT:

### Verdict M12

`accept-third-position` (reject-issue-doc-as-posed)

The finding is **real** (standard trajectories have ~59-61 snapshots; 32 is the spec's example default, not a hard contract), but the **BLOCKING reclassification is wrong** (32 ≤ 59 is trivially feasible; the corrected CLM-10 medians falsify the infeasibility claim) and the **P1-4 `0.5×` factor is wrong** (unevidenced, internally inconsistent with the issue doc's own checklist, cosmetic effect at the verified median). The third position (resolution doc's `n_pts = min(n_pts_cap, n_snapshots(traj))` without replacement) is the locked data-side contract; the 0.5 factor and the BLOCKING label are both rejected as posed.

### Verdict M11

**Explicit severity ruling: MAJOR → BLOCKING reclassification STANDS.** The MAJOR → BLOCKING label, as set by the issue doc's Severity Reclassification Ledger, is upheld by Phase 25. Grounded on the **data-integrity argument** (resolution §3.3 part 2): IC-level exclusion (byte-identical-subset) + before-statistics ordering (no normalizer contamination) + fail-closed (exclusion is a guarantee, not a flag). The data-integrity argument alone is sufficient to uphold the BLOCKING reclassification; architectural-harm narratives (causal-firewall spikes, LayerNorm/SIREN saturation) are **not** load-bearing for this ruling and are not relied on here. CLM-03 (65 IDs, confirmed) is the empirical anchor for the count; the *consumption* question (does the live loader enforce the blacklist?) is OI-8 (SCOPE-10, outside grounding) and is **carried forward** to Phase 26 PIPE-03 / FUT-01 as a forward-pointing caveat, NOT resolved here. The M11 severity ruling is the one verdict the resolution doc explicitly defers TO Phase 25; this is that ruling, recorded explicitly and distinctly from the M12 verdict.

**M11 GUARD (D-10 silence/hedge rule applied to the M11-specific case — checked; not triggered):** the four objective guard triggers from Plan 25-02 Task 3 were checked at authoring time. None fired: (a) `24.5-RESOLUTION-MAP.md` routes M11 severity to a determinate data-integrity argument at §3.3 Q-A3:221-254, not to an Open Items / Additional Input Needed section; (b) the §3.3 part 2 line range was found and contains the data-integrity grounding (byte-identical-subset, before-statistics ordering, fail-closed); (c) `24.5-READINESS-REPORT.md` does NOT say the M11 severity ruling itself cannot be decided until OI-8 live-loader consumption is externally resolved (OI-8 is a carried-forward caveat, not a severity-decision blocker; the data-side contract is stated regardless); (d) `24-VERIFIED-FACTS.md CLM-03` (65 blacklist, confirmed) does not contradict the M11 grounding. The M11 ruling proceeds.

## Root-Cause Framework Ambiguity

**M12 root cause:** the issue doc conflated the **data-loss sample** (the discrete Brutus snapshots, ceiling for distinct without-replacement draws) with the **collocation budget** (a deferred M16 question routed to doc-03 per SCOPE-11). The 0.5 factor's "rationale" (sampling ratio) is a conflation — the data-loss sample and the collocation budget are different quantities governed by different contracts. The issue doc's own checklist contradicts P1-4 (expects `gold → 128`; the 0.5 rule cannot produce 128), which is a self-diagnosing internal inconsistency.

**M11 root cause:** severity is a **process classification**, not a data fact. The resolution doc explicitly hands the reclassification decision to EVID-10 because the data-side contract (CLM-03 count, exclusion semantics, ordering, fail-closed) is grounded in verifiable facts, but the *severity label* (MAJOR vs BLOCKING) is a process decision that turns on the question: "is silently-corrupted training data at ingestion time a fixable concern, or a blocking-grade concern?" The data-integrity argument (exclusion is a guarantee, contamination of normalizers is unrecoverable, fail-closed is the only certification path) supports the BLOCKING reclassification.

## Locked Convention / Ruling

**M12 locked convention (in spec-edit-ready prose for Phase 27 PIPE-04 transcription into `ctl_instruction.md` Mini-Batch Construction):**

> **Per-trajectory data-loss point count.** `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))`, sampled **without replacement** from the trajectory's snapshot times. `n_pts_cap` defaults to 32 (the spec's example value; not evidence-based — revisit with admitted-set snapshot distributions; exposed as a configuration knob). The 50/50 composition is realized as: `k_w = floor(n_pts/2)` acceleration-norm-weighted draws without replacement (Gumbel-top-k), then `n_pts − k_w` uniform draws without replacement from the remainder; all draws from a seeded generator. The loader exposes `n_snapshots(traj)` and `dt_out(traj)` as metadata (forward interface for the deferred M16 collocation-density question — doc-03; not used here). **No `0.5 × n_snapshots` factor is imposed** (unevidenced; see Q-B1 resolution).

**M11 severity ruling (the explicit Phase 25 ruling, owned by Phase 26 PIPE-03 prioritization):**

> **M11 severity: BLOCKING (reclassification STANDS).** Phase 25 upholds the issue doc's MAJOR → BLOCKING reclassification of M11, grounded on the data-integrity argument (resolution §3.3 part 2): IC-level exclusion (byte-identical-subset); before-statistics ordering (no normalizer contamination); fail-closed (exclusion is a guarantee). The M11 *consumption* question (does the live loader enforce the blacklist?) is OI-8 (SCOPE-10, outside grounding) and is **carried forward** to Phase 26 PIPE-03 / FUT-01 as a forward-pointing caveat — not resolved here, not blocking the severity ruling. The data-side contract is BLOCKING-grade; the live-loader consumption verification is a Phase 26 PIPE-03 / FUT-01 hand-off item.

Phase 25 makes **zero framework-spec edits** (D-02); the M12 spec transcription is owned by Phase 27 PIPE-04, citing this EVID-10 record. The M11 ruling is a process-classification decision (no spec edit), owned by Phase 25 (this record) and consumed by Phase 26 PIPE-03 prioritization.

## Which Source Was Correct / Wrong

- **M12:** underlying observation **real** (the spec's "32" default is example-parenthetical, not a hard contract; the data-loss sample is a distinct concept from the collocation budget). The **BLOCKING reclassification** is **wrong** (32 ≤ 59 is trivially feasible on the corrected CLM-10 medians). The **P1-4 `0.5×` factor** is **wrong** (unevidenced, internally inconsistent with the issue doc's own checklist, cosmetic effect at the verified median). The third position (`min(cap, n)` without replacement) is the locked data-side contract.
- **M11:** the **contract is blocking-grade** (correct: data-integrity argument, fail-closed semantics). The **MAJOR → BLOCKING label** is the **EVID-10 ruling Phase 25 makes** (correct: upheld on data-integrity grounds). The data-side contract is stated in full regardless of the live-loader consumption status (OI-8).
- **Resolution doc:** correct on M12 (BLOCKING claim falsified; `min(cap, n)` is the third position) and on M11 (contract is blocking-grade; reclassification is EVID-10's call). Correct on the §6 F-3 defect catalog (item 2: M12 BLOCKING claim + P1-4 contradiction with the doc's own checklist).
- **Issue doc:** correct that M12 identifies a real gap (the data-loss sample and the collocation budget were conflated); correct that M11 identifies a real gap (blacklist not loaded at training time). Wrong on the M12 severity rationale and on the P1-4 fix.

## Before / After Spec Note

**M12 — Before:** `ctl_instruction.md` Mini-Batch Construction carries the "(e.g., 32) … 50% uniform …, 50% weighted by acceleration norm" parenthetical as a snapshot-sourced data-point contract (lines ~1197-1201), but does not pin the data-loss sample count to `n_snapshots(traj)` or restate the 0.5× factor rejection. The `pinn_architecture.md §3.1` `points_per_trajectory = 32` is a code default.

**M12 — After (Phase 27 PIPE-04):** `ctl_instruction.md` Mini-Batch Construction carries the locked data-side contract: `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))` without replacement, seeded weighted-then-uniform split, `n_pts_cap` default 32 flagged as example-not-evidenced, `0.5×` factor explicitly rejected, `n_snapshots(traj)` and `dt_out(traj)` exposed as metadata. Citing this EVID-10 record by path.

**M11 — Before:** the M11 severity was MAJOR (audit) and the issue doc's Severity Reclassification Ledger reclassified it to BLOCKING; the M11 *consumption* question is unverified (SCOPE-10); the data-side contract is grounded in CLM-03 (65 IDs, confirmed).

**M11 — After (this EVID-10 record + Phase 26 PIPE-03 prioritization):** the BLOCKING reclassification is **upheld by Phase 25** on data-integrity grounds (this record). The M11 contract is blocking-grade, fail-closed; the live-loader consumption verification is a Phase 26 PIPE-03 / FUT-01 hand-off item, not a Phase 25 verdict. No framework-spec edit (D-02).

**D-12 (close-with-parent annotations):** the synthesis rows G3 (→M11) and G5 (→M12) close with their parent findings — no separate evidence packet. See Status Transition Log and the ledger's per-finding subsections.

## Named Acceptance Check

- **M12:** `AC-PIPE-04` (Phase 27 PIPE-04 owns the runnable pass criteria — verification suggestion per resolution doc §4.1 part 5: snapshot-count distribution per variant over the admitted set, split by footer presence extends DATA-06; unit tests `n=59 → 32` distinct indices with 16+16 weighted/uniform, `n=10 → 10` distinct indices cap-inactive, fixed seed ⇒ identical draws, all drawn times exist in the trajectory's snapshot set).
- **M11:** `AC-PIPE-03` (Phase 26 PIPE-03 owns the runnable pass criteria for the M11 contract — verification suggestion per resolution doc §3.3 part 5: probe the live loader (does a blacklisted ID appear in any emitted batch across an exhaustive stage iteration); unit tests: init fails on absent file, fails on a third top-level key, a listed ID present in both folders never appears in any manifest or batch, the batch-time assertion trips when exclusion is deliberately disabled, a listed-but-absent-on-disk ID logs and proceeds).

Phase 25 mints no new AC-IDs (D-13); AC-PIPE-03 and AC-PIPE-04 are the seeded assignments from `24-ISSUE-LEDGER.md`.

## Status Transition Log

```text
2026-06-12 <pending-commit-sha> PENDING -> PENDING (Phase 25 P02 EVID-10 record authored + M12 accept-third-position verdict + M11 explicit severity ruling BLOCKING STANDS; M12 fix owned by Phase 27 PIPE-04, M11 prioritization owned by Phase 26 PIPE-03; OI-8 carried forward; D-12 G3->M11, G5->M12 close with parent)
```

The final short SHA replaces `<pending-commit-sha>` after the atomic 25-02 commit; the audit label travels in the ledger's per-finding subsections (D-06 same-commit discipline; D-12 close-with-parent annotations in the M11 and M12 per-finding notes).

**D-14 conditional Dependents:** no shared contract discovered. M11 (blacklist consumption, IC-level exclusion) and M12 (data-loss sample count) are distinct findings on distinct code paths. The `M11` and `M12` rows' `Dependents:` fields are unchanged.

**OI-8 carry-forward:** the M11 live-loader consumption question (does the live loader enforce the blacklist?) is **NOT resolved here**. It is carried forward to Phase 26 PIPE-03 / FUT-01 as a forward-pointing caveat per OI-8 (SCOPE-10, outside grounding). The data-side contract (CLM-03 count, exclusion semantics, ordering, fail-closed) is stated in full regardless of the live-loader consumption status.
