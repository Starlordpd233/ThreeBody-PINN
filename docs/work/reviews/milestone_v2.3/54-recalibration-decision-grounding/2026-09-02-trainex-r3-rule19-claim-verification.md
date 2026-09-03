---
status: active
purpose: verification-report
created: 2026-09-02
milestone: v2.3
phase: recalibration-decision-grounding
retirement_trigger: Superseded when owner checkpoint ② is discharged and a later phase re-verifies these claims against a moved tree, or when the owner rules the underlying claims disposed of.
---

# trainex-r3 — ERW Rule-19 Verification of the Returned Reports' Claims

## Why this exists

The `trainex-r3` round returned **two** reports. The round declared **one** access
mode in all three places ERW Rule 16 requires, and `54-07` check H2 certified that
declaration correctly; but one of the two engagements subsequently ran **without live
repository access**. The intake record carries that finding with each report's own
self-declaration quoted by file and line
(`.planning/phases/54-recalibration-decision-grounding/54-INTAKE.md`,
`RULE-16-DIVERGENCE`), and derives a separate verification burden per report rather
than selecting one from the runbook's access-mode table.

This half of the report discharges **ERW Rule 19** for the engagement that **did** read
the tree — the open-book report at
`pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_results/claude-resolution.md`.
Rule 19 states the reason directly: *"A Route B report's repo claims arrive as
checkable assertions, not as established facts — they carry a file:line citation
precisely so they can be re-derived independently"*, and requires the verification to
be recorded *"before any claim informs a decision, a roadmap, or a spec edit"*
(`docs/runbooks/external-research/2026-06-11-external-research-workflow.md:223`–`:227`).

The other engagement's repository anchors carry a **different** burden — a three-way
provenance triage the runbook does not anticipate, because it does not contemplate a
closed-book round whose uploads carry repository anchors. That burden is derived at
`54-INTAKE.md` under `BURDEN-CLOSED-BOOK` and is discharged by the **next pass**, which
extends **this same file** rather than opening a second one (D-12).

The divergence finding is cited here, not restated: its evidence lives at
`54-INTAKE.md` and is not reproduced.

## Scope

**What this half verifies.** Every claim the open-book report makes that this
repository can settle, re-derived independently against the tree, with a verdict from a
closed vocabulary.

**What this half does not do.** It adjudicates no premise. It merges no menu. It
disposes of no decision surface, names no candidate value for any of them, attaches no
weight to the order in which the report presents them, and selects nothing. Verifying a
claim **about** a decision surface is not the same act as disposing of that surface, and
only the first is performed here. The premise adjudication is the wave-4 plan's work;
the consolidation is the wave-5 plan's; the ruling record is the owner's at checkpoint ②.

**The sections of the source report the ledger draws from, with the count extracted from
each.**

| # | Source section in the open-book report | Extracted | Count |
|---|---|---|---|
| 1 | §7 *Claims and uncertainty register* (`claude-resolution.md:860`) | its rows, native identifiers carried through unchanged | 15 rows → 15 ledger rows |
| 2 | §1 *Premise-challenge findings* (`:42`–`:291`) | each finding split into separately checkable assertions | 9 findings → 36 ledger rows |
| 3 | §2 *departures* table (`:353`–`:360`) | each row split into its source side and its project side | 7 rows → 15 ledger rows |
| 4 | every remaining distinct repository citation in the whole report | the claim carrying each citation not already covered above | 7 loci → 7 ledger rows |

**Total ledger rows: 73.** The partition executed across the three tasks is recorded
under `PARTITION-EXECUTED` below.

## Method

Read-only inspection of the tree at the ERW Rule-20 live-tree pin
`efe8e590d6c6b2a77cc92abb0b93d625e2b92c49`, which `54-08` proved **byte-identical to the
working tree across every path either report cites** — `git diff` between the pin and
the tip empty over the set, `git status --porcelain` empty over the same set, both
printing `PIN-TREE-IDENTICAL` rather than relying on silence
(`54-INTAKE.md`, *The identity proof*). Without that proof a re-derivation performed
here would verify a different file than the one the report read, and would look
identical while doing it.

The set that proof covers is the **citable-path set**: 21 paths extracted from the two
reports and recorded as a pasteable block at `54-INTAKE.md` under `CITABLE-PATH-SET`.
Nothing is claimed about any path outside it. Three paths this pass had to read fall
outside the set — the framework-specs bundle, the round prompt, and the `trainex-r2`
report — and their identity is established **here** rather than inherited; see
*Coverage boundary* below.

No file under `pinn/` and no framework-spec file was modified. No training run was
started, no evaluation invoked, no command with side effects run. Every re-derivation is
recorded with the command that produced it, short enough to paste and specific enough to
re-run.

Claims are resolved **by content first**. A cited line number is recorded as a *separate*
finding from the content it is supposed to carry, because a claim can be true at a line
that has moved and a line number can be right while the content does not support it.

### Coverage boundary — four paths read outside the certified set

Two commands were run **once**, over all four paths together:

```
git diff --stat efe8e590d6c6b2a77cc92abb0b93d625e2b92c49 HEAD -- <the four paths>
git status --porcelain -- <the four paths>
```

Both returned empty, and the marker `OUT-OF-SET-IDENTICAL` was printed on the empty
result rather than the result being left as silence, because an empty diff and a
mistyped pathspec are indistinguishable in silence.

| Path | Why it was read | Rows that rest on it |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/specs/framework-specs-bundle.md` | `PC-8a`/`PC-8b`/`R-12` assert bundle fidelity; the bundle is the object of the claim | `PC-8a`, `PC-8b`, `R-12` |
| `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-AGENT-PROMPT.md` | `PC-2a` attributes a statement to the round prompt | `PC-2a` |
| `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_results/trainex-r2-research-report.md` | `PC-9a` quotes it; the quote is in none of the three attachments — which is itself the finding recorded at `PC-9a` | `PC-9a` |
| `pinn/train.py` | corroborating locus for the collocation count of 16, which no cited line fixes; used only as corroboration, never as the primary evidence | `PC-5b` (note only) |

Recorded rather than absorbed silently: the 21-path identity proof `54-08` recorded does
**not** cover these four, so this pass ran the same two commands over them and records
the result. A later pass that widens `CITABLE-PATH-SET` should fold them in.

**Every path the ledger's re-derivations actually resolve against is otherwise inside
the certified set.** The citation extraction below yields **18** distinct repository
paths for the open-book report, and all 18 are members of the 21-path set — the three
remaining members entered it through the closed-book report's own citations. So apart
from the four paths above, nothing in this half rests on an uncertified path.

## The closed verdict vocabulary (D-13)

Six verdicts. No ledger row carries anything else.

| Verdict | Meaning |
|---|---|
| `CONFIRMED` | Re-derived independently and the tree says what the claim says. |
| `CONFIRMED-SHARPER` | Re-derived, and the evidence supports a stronger statement than the claim made. The stronger statement is stated. |
| `CONFIRMED-NARROWER` | Re-derived, but the evidence supports the claim only under a narrower reading than its wording. The narrower reading is stated. |
| `REFUTED` | Re-derived and the tree contradicts the claim. The contradiction is stated with its evidence. |
| `UNSUPPORTED` | The cited location exists but does not carry the content the claim attributes to it. Distinct from `REFUTED`: the claim may still be true elsewhere, and the row says where. |
| `NOT-VERIFIABLE-HERE` | The claim's class admits no in-repo re-derivation within this phase's authority. Every such row names what would settle it and who may authorize that. |

The first four extend the vocabulary the Phase 45 worked example used
(`docs/work/reviews/milestone_v2.1/45-trainex-r2-erw-package-assembly/2026-07-24-trainex-r2-report-factw-verification.md`
— `CONFIRMED`, `CONFIRMED (broader than stated)`, `CONFIRMED (sharper than stated)`).
The sixth reproduces that example's own *"Not verifiable here"* section as a per-row
verdict so that unchecked claims can be **counted** rather than left in prose.

**Nothing outside these six is available.** A claim that fits none of them is a signal to
widen the vocabulary deliberately and record the widening — never to improvise a seventh
verdict in one cell.

**Split rows.** Where a claim spans a part this repository can settle and a part it
cannot, the verdict cell carries **two** verdicts separated by `·`, one for each part —
for example `CONFIRMED (repo) · NOT-VERIFIABLE-HERE (published)`. One verdict covering
both parts is not accepted. A row carrying `NOT-VERIFIABLE-HERE` in either position is
routed in the register below.

The split convention is stated for a claim spanning this repository and an **outside
source**; it is applied here to three kinds of outside, and the widening is recorded
rather than assumed: published literature, the source report's own clean-room
computation, and a state only a run would produce. All three are outside this
repository's reach in the same sense — a citation cannot be resolved against the tree —
and the alternative to splitting is to let one half's verdict stand for both, which is
precisely the false-confidence the `NOT-VERIFIABLE-HERE` verdict exists to prevent.
No seventh verdict is introduced; only the composition of the six is extended, and the
count table below carries each split combination as its own named bucket so that no
reader has to infer which half a count refers to.

## How the ledger was built

**Extraction, not summary.** Each of the four sources above was extracted as a row set
and its count derived from the source report itself. The derived counts are re-derived
independently by this plan's automated gate, which fails unless the ledger carries a row
for every register row and every premise-finding identifier, and which additionally
requires both extractions to be **non-empty** — so an extraction that silently matched
nothing cannot pass by producing zero on both sides.

**Identifiers.** The open-book report's register rows carry native identifiers `R-01` …
`R-15` and its premise findings carry `PC-1` … `PC-9`; both are carried through
**unchanged**, per `LEDGER-PREFIX-CONTRACT` at `54-INTAKE.md`. Nothing is renamed and no
parallel identifier shadows one that already exists.

**The split rule, stated once and applied uniformly.** A premise finding usually asserts
several separable things. It is split into one sub-row per **separately checkable
assertion** — an assertion with its own evidence locus (a distinct citation, a distinct
computation, or a distinct textual locus) such that it could be true while a sibling is
false. Sub-rows are lettered `a`, `b`, `c`, … **in the order the finding states them**,
so every sub-row maps back to its finding by prefix and to its position by letter. The
same rule splits each departures row into its *Source* side and its *This project* side,
which are separately checkable by construction.

**The keying rule.** The ledger is keyed on the **claim**, not on the citation. A claim
cited in several places is **one** row carrying all of its citations in the
`Cited location(s)` cell. Duplicate rows for one claim would inflate the coverage count
and hide a missing claim.

**Namespace collision, recorded.** The departures table's row labels `D-1` … `D-7` are
**the report's own** and are **not** this project's decision identifiers `D-01` … `D-18`
recorded in `54-CONTEXT.md`. The two namespaces collide by accident and a reader must not
conflate them.

**Ordering.** Ledger rows are emitted in the source report's own order within each group,
and every set comparison in this file ran under `LC_ALL=C`.

**Disagreements are recorded, not resolved.** Where the report's register row and its
body text state the same claim differently, both readings appear in the row's note. Where
the wording is ambiguous, the ambiguity is recorded rather than resolved — a resolved
ambiguity is an interpretation, and an interpretation is not a verification.

**Evidence class.** Every row records the source report's **own declared label**
(`[PKG]` package-derived · `[REPO]` repository-verified in the live tree · `[LIT]`
published literature · `[OWN]` own analysis or clean-room computation, declared at
`claude-resolution.md:35`–`:38` and counted at `54-INTAKE.md` I6) **beside** the class it
maps to in the four-class independence taxonomy `54-08` fixed (`CLASS-PACKAGE-INTERNAL`,
`CLASS-REPOSITORY-DERIVED`, `CLASS-LITERATURE`, `CLASS-ANALYTIC`). No claim is
re-labelled. Where a row carries two labels, both are recorded with the part of the claim
each covers. Class abbreviations used in the ledger: `PKG-INT`, `REPO-DER`, `LIT`, `ANA`.

**The partition declared when the ledger was built.**

| Partition | What it covers | Rows |
|---|---|---|
| `P-A` | rows left to the re-derivation task, whose class admits an in-repo re-derivation | 56 |
| `P-B` | rows left to the triage task, whose class admits none, pre-marked `NOT-VERIFIABLE-HERE` because the class decides the verdict without evidence | 15 |
| `P-C` | rows filled while the ledger was being built, because their evidence **is** the extraction and the structural read this task performs | 2 |

`56 + 15 + 2 = 73`, the ledger total. No row falls between the tasks. The executed
partition is reconciled against this declaration under `PARTITION-EXECUTED`.

## Path abbreviations used in the ledger cells

Each abbreviation binds to **exactly one** full path. The full paths appear here and in
`CITATION-COVERAGE` below, so no citation is reachable only through an abbreviation.

| Abbrev. | Full path |
|---|---|
| `AR` | `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` |
| `CT` | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` |
| `MA` | `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md` |
| `PR` | `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-AGENT-PROMPT.md` |
| `BU` | `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/specs/framework-specs-bundle.md` |
| `OB` | `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_results/claude-resolution.md` |
| `R2` | `pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_results/trainex-r2-research-report.md` |
| `LOG` | `.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/evidence/attempts/stage0-rerun-seed41-attempt-02/logs/train.log.jsonl` |
| `CFG` | `.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/evidence/attempts/stage0-rerun-seed41-attempt-02/config.yaml` |
| `PINA` | `reference-code/reference_NNs/PINA-master/pina/solver/physics_informed_solver/causal_pinn.py` |
| `REQ` | `.planning/REQUIREMENTS.md` |
| `AUD` | `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md` |

Paths under `pinn/` are written in full in the cells. Every command cell escapes a
literal pipe as `\|`, the convention `54-06-PLAN.md` set and `54-INTAKE.md` restated, so
that the empty-cell scan does not read a shell pipeline as a cell boundary.

## LEDGER — the open-book claim ledger

### Group A — the claims-and-uncertainty register (`OB` §7, `:860`)

| ID | Claim, in the source's own terms | Evidence class | Cited location(s) | Re-derivation command | Output | Verdict | Note |
|---|---|---|---|---|---|---|---|
| R-01 | The source method is Wang, Sankaran & Perdikaris, CMAME 421 (2024) 116813; §3.2's formula is its Eq. 3.2 / Expert's-Guide Eq. 2.11 term for term | `[LIT]`+`[REPO]` → LIT + REPO-DER | `PINA:55-60`; `AR:435`; published Eq. 3.2 / EG Eq. 2.11 | `sed -n '55,60p' <PINA>`; `sed -n '435p' <AR>` | `PINA:55-60` `**Original reference**: Wang, Sifan, Shyam Sankaran, and Paris Perdikaris. *Respecting causality for training physics-informed neural networks.* Computer Methods in Applied Mechanics and Engineering 421 (2024):116813.`; `AR:435` `w_n = \exp\left(-\eta_c \sum_{m=1}^{n-1} \operatorname{stopgrad}(\bar R_m)\right),` | CONFIRMED (repo) · NOT-VERIFIABLE-HERE (published) | Content and line both resolve at both anchors. Confirmed: this repository names that paper as the source of the causal weighting and carries the exponential-prefix form at `AR:435`. Not settleable here: whether the published Eq. 3.2 and Expert's-Guide Eq. 2.11 match that formula **term for term**. See the per-claim section |
| R-02 | The source's calibration procedure is annealing `ε` over `{10⁻²…10²}` with advance criterion `min_i w_i > δ = 0.99`; Expert's-Guide default `ε = 1.0`; PINA default `eps = 100` | `[LIT]`+`[REPO]` → LIT + REPO-DER | `PINA:76`; published Algorithm 1 | `sed -n '76p' <PINA>` | `        eps=100,` | CONFIRMED (repo) · NOT-VERIFIABLE-HERE (published) | Content and line both resolve: the vendored implementation's default is `100` at the cited line. Not settleable here: the annealing sequence `{10⁻²…10²}`, the `min_i w_i > δ = 0.99` advance criterion, and the Expert's-Guide default `ε = 1.0`, all of which are statements about published sources |
| R-03 | The source's prefix sum runs over `M` temporal segments with the residual averaged within each; this project's runs over individual collocation points | `[LIT]`+`[REPO]` → LIT + REPO-DER | `pinn/loss_catalog.py:330-333`; `pinn/training/controllers.py:656` | `sed -n '330,333p;342p' pinn/loss_catalog.py`; `sed -n '651,656p' pinn/training/controllers.py` | `:330` `cumsum = torch.cumsum(detached, dim=0)`, `:333` `cumsum_excl = torch.cat([zeros, cumsum[:-1]], dim=0)`, `:342` `loss = (weights * rbar).mean()`; `controllers.py:651` `residual = accel - force` with the in-code comment at `:653` "The residual has shape (N_t, 3 bodies, 3 Cartesian components)" and `:656` `rbar = (residual ** 2).sum(dim=(-2, -1)) / 3.0` | CONFIRMED (repo) · NOT-VERIFIABLE-HERE (published) | Content and line both resolve. The project side is confirmed at the construction site rather than inferred from a variable name: the leading axis of `residual` is the collocation-time index, so `rbar` carries one entry per collocation point and the prefix sum runs over those. The source side is a statement about two papers and is routed |
| R-04 | `R̄ ∝ ω₀⁴` for a pure SIREN, but under the locked SQR stack the measured law is ≈`ω₀^0.5`: 1.63 decades per 1000× | `[OWN]` → ANA | clean-room sweep, `OB:81`-`:84` | n/a — clean-room model, no in-repo locus | n/a — routed in the register below | NOT-VERIFIABLE-HERE | Class decides the verdict: the measurement was made on a re-implementation, not on this project's model |
| R-05 | The power-skip stack carries ≈8.66 decades of the initialization `R̄`, ≈1.44 decades per SQR block | `[OWN]` → ANA | clean-room depth sweep, 5 seeds, `OB:88`-`:91` | n/a — clean-room model, no in-repo locus | n/a — routed in the register below | NOT-VERIFIABLE-HERE | Same class as R-04; the report's own `G-4` records that the aggregate is undecomposed |
| R-06 | A fixed `η_c` on unnormalized `R̄` has a 3.24-decade informative window against a 14.4-decade traversal | `[OWN]` arithmetic; thresholds `[REPO]`/`[PKG]` → ANA + REPO-DER | `OB:411`-`:414`; `pinn/loss_catalog.py:97`; `CT:1963-1966`; `CFG:48`; `LOG` | `python3 -c "import math; print(math.log10(87.33654/0.05), math.log10(2.527e10/1e-4))"` | `3.2422259782038214 14.402605241919915` | CONFIRMED-NARROWER | Both numbers re-derive exactly (3.24 and 14.4). The narrower reading: the 14.4-decade traversal rests only on re-derived repository quantities — the log's median `R̄₁` (R-13) and `ε_phys = 10⁻⁴` (CC-1) — whereas the 3.24-decade window additionally requires the report's **stipulated** lower edge 0.05, which no repository fact fixes. The report's own confidence cell concedes this. See the per-claim section |
| R-07 | float64 is not a lever: 15/16 weights still floored; total clip range 0.91 decades | `[OWN]`+`[REPO]` → ANA + REPO-DER | `pinn/loss_catalog.py:97`; `LOG` | `python3 -c "import math; print(math.log(2.0**-1022), 708.396/87.33654, math.log10(708.396/87.33654))"`; `sed -n '97p' pinn/loss_catalog.py` | `-708.3964185322641 8.11110676012583 0.9090801177155879`; `:97` `    mathematical_floor = math.log(torch.finfo(dtype).tiny)` | CONFIRMED | The 0.91-decade clip range re-derives exactly. The 15/16 half is re-derived from a **repository** quantity rather than from the clean-room vector: at the retained log's median `R̄₁ = 2.527×10¹⁰` (R-13) and `η_c = 1` (D-3b), the exponent at every `n ≥ 2` is at most `−2.5×10¹⁰`, which is below the float64 floor `−708.396` by more than seven orders of magnitude, so 15 of 16 weights are floored under float64 as well |
| R-08 | Instantaneous normalization makes `front_idx` unable to advance | `[OWN]` arithmetic + `[REPO]` → ANA + REPO-DER | `pinn/training/controllers.py:692-694`; `pinn/training/guards.py:593-615` | `sed -n '692,694p' pinn/training/controllers.py`; `sed -n '588,602p' pinn/training/guards.py` | `controllers.py:692-694` `"front_idx": max(` / `[n for n, w in enumerate(w_n_list) if w > 0.5], default=-1,` / `),`; `guards.py:589-591` maintain `self.front_high_water`, `:601` `saturated = self.front_high_water >= int(n_colloc) - 1`, `:602` `if age > self._front_advance_window_n and not saturated:` | CONFIRMED-NARROWER | Content and line resolve at both anchors. The narrower reading: under a batch-statistic normalization the weight vector is exactly invariant to the residual's overall **magnitude**, so `front_idx` stops responding to the descent — that much is a closed-form identity. It does **not** follow that `front_idx` is constant: it remains a function of the per-step residual **shape**, which D-2b's per-step re-draw changes every step. See the per-claim section |
| R-09 | Residual-wide normalization moves the phys/data raw-gradient ratio from 12.80 to ≈2.57 decades | `[REPO]` log ratio; `[OWN]` rescaling arithmetic → REPO-DER + ANA | `LOG`; `OB:486` | `python3 -c "import json,math,statistics as st;rs=[json.loads(l) for l in open('<LOG>')];r=[x['grad_norm_raw_phys']/x['grad_norm_raw_data'] for x in rs];print(len(r), st.median(r), math.log10(st.median(r)), 12.800846549587316-math.log10(1/5.9e-11))"` | `502 6321884391035.326 12.800846549587316 2.5716985612294607` | CONFIRMED (repo) · NOT-VERIFIABLE-HERE (analytic) | The 12.80-decade input is a fact of the primary log, computed over all 502 records, and is confirmed. The 2.57-decade output is **not** settleable here because it divides by `R_ref`, a clean-room quantity (R-04/R-05/PC-1e). What is confirmed is the arithmetic's internal consistency with the report's own `1/R_ref ≈ 5.9×10⁻¹¹`: `12.8008 − log₁₀(1/5.9×10⁻¹¹) = 2.5717`. See the per-claim section |
| R-10 | The composed recipe satisfies GATE-04 (i)–(iii) at initialization on six seed/IC combinations | `[OWN]` clean-room → ANA | `OB:705`-`:710` | n/a — clean-room model, no in-repo locus | n/a — routed in the register below | NOT-VERIFIABLE-HERE | The report's own `G-6` requests exactly this re-derivation against the project's model |
| R-11 | `F-02`'s row text contradicts `M2`/`F-11`/`A-1` in the same document | `[PKG]` textual → PKG-INT | `MA:268`, `:121`, `:277`, `:414` | `sed -n '268p;121p;277p;414p' <MA>` | `:268` still reads "`first_omega_0 = 30` sets the second-derivative magnitude" with status `established`; `:121` `M2` states "**two compounding factors**, not one"; `:277` `F-11` names `first_omega_0` **and** the 12-layer stack; `:414` `A-1` calls the narrow wording a **correction** | CONFIRMED | Filled while the register was being extracted (partition `P-C`); all four loci are inside the extraction this task performed |
| R-12 | All 10 bundle excerpts and all cited spec anchors resolve correctly in the live tree | `[REPO]`+`[OWN]` → REPO-DER | `BU`; `AR:181`, `:429`, `:435`, `:445`, `:454`, `:461`, `:668-671`, `:692` | the block-comparison script recorded at PC-8b, plus `sed -n '181p;429p;435p;445p;454p;461p;668,671p;692p' <AR>` | `LEN-UNIFORM 10/10  VERBATIM-MATCH 10/10`; all eight master-cited spec anchors resolve by content **and** at the cited line in the live 1098-line file | CONFIRMED-SHARPER | Stronger statement the evidence supports: the report compared **three** boundary pairs line-for-line; **all ten** blocks match their live source ranges line-for-line, and in all ten the wrapper is exactly one blank line on each side. So the bundle is not merely consistent in length — it is byte-faithful across every excerpt it carries |
| R-13 | The retained log's `w_min`, `w_mean`, `front_idx`, gradient ratio and `λ_phys` ramp are as `F-04`/`F-05` state | `[REPO]` primary log, 502 rows → REPO-DER | `LOG` | `python3 -c "import json,statistics as st;rs=[json.loads(l) for l in open('<LOG>')];print(len(rs),{k:sorted(set(r[k] for r in rs)) for k in ('w_min','w_max','w_mean','front_idx')}, st.median([r['loss_phys'] for r in rs])*16)"` | `502 {'w_min': [1.1754998158862984e-38], 'w_max': [1.0], 'w_mean': [0.0625], 'front_idx': [0]} 25267107840.0` | CONFIRMED | 502 records, each of the four causal fields single-valued across all of them. The gradient ratio and the `λ_phys` ramp are the same artifact's fields and are recorded at PC-6a. `16 × median(loss_phys) = 2.5267×10¹⁰` is the median `R̄₁` every derived threshold in this report uses, re-derived here from the primary log rather than taken from the source report. The statistic's span is the whole retained record — 502 of 502 — matching the span the claim's wording implies |
| R-14 | `R̄` has a lower floor set by `‖F_grav‖²` when the position scale collapses | `[OWN]` depth-0 `ω₀` sweep → ANA | clean-room sweep, `OB:543` | n/a — clean-room model, no in-repo locus | n/a — routed in the register below | NOT-VERIFIABLE-HERE | A statement about a configuration no retained artifact instantiates |
| R-15 | Nothing in this report selects a remedy; every default is a candidate for checkpoint ② | self-attested against SCOPE-34 → PKG-INT | `OB:19`, `:795-804`, `:910` | `awk 'NR>=797 && NR<=804 {n=split($0,a,"\|"); print NR, a[n-1]}' <OB>`; `grep -c 'Suggested default' <OB>`; `grep -cniE '\bI (select\|choose\|adopt\|rule)\b' <OB>` | All 8 decision-sheet data rows carry an empty `Owner's pick` cell; 7 `Suggested default` markers; 0 first-person selection verbs; `:19` "It selects no remedy"; `:910` "No remedy selected" | CONFIRMED | Filled by the structural read this task performs over the whole source report (partition `P-C`) |

### Group B — the premise-challenge findings (`OB` §1, `:42`–`:291`), split per the rule above

| ID | Claim, in the source's own terms | Evidence class | Cited location(s) | Re-derivation command | Output | Verdict | Note |
|---|---|---|---|---|---|---|---|
| PC-1a | `F-02` reads "`first_omega_0 = 30` sets the second-derivative magnitude: `‖a′‖` column values `1.94×10⁵`–`2.79×10⁵`, `R̄` medians `1.25×10¹⁰`–`2.60×10¹⁰`" and is tiered *established* | `[PKG]` → PKG-INT | `MA:268` | `grep -nF '\| F-02' <MA>` | `MA:268` `\| F-02 \| `first_omega_0 = 30` sets the second-derivative magnitude: `‖a′‖` column values `1.94×10⁵`–`2.79×10⁵`, `R̄` medians `1.25×10¹⁰`–`2.60×10¹⁰` \| … \| established \|` | CONFIRMED | Content and line both resolve, and the row's tier is `established` as the finding states. One presentational difference, recorded rather than smoothed over: the report renders the row's opening clause in **bold**; the master's row carries no emphasis there. The wording is otherwise identical |
| PC-1b | §4.1 `M2` and `F-11` already widened the attribution to **two** factors and `A-1` records the narrow wording as a correction, but `F-02`'s row text was never updated and `S3` in §4.3 still names `ω₀` alone as the initialization-scale surface | `[PKG]` → PKG-INT | `MA:121`, `:277`, `:414`, `:268`, `:171` | `sed -n '121p;277p;414p;268p;171p' <MA>` | `:121` `**M2 — the chain, and the two factors the audit attributes it to.** … the audit attributes the magnitude of that second derivative to **two compounding factors**, not one.`; `:277` `F-11` names `first_omega_0 = 30` **and** the 12-layer SQR-SkipResNet stack; `:414` `A-1` … "The packet was narrower than its source, in a direction that overstates one decision surface."; `:268` `F-02`'s row text is unchanged; `:171` `#### S3 — `ω₀` / `first_omega_0`, the SIREN initialization scale` | CONFIRMED | All four loci resolve by content and by line. The last clause is confirmed as worded: §4.3's surface entry at `:171` names `ω₀` alone. Recorded so a later reader is not misled — §**7** does carry an `S3-adjacent` entry at `:311` naming the stack, but §7 is the gaps section, and that entry says in its own words that whether the stack is a surface "is not settled by anything in this package" |
| PC-1c | `τ = 2u − 1` enters the network only through the first layer's `sin(ω₀(W₀x + b₀))` | `[REPO]` → REPO-DER | `pinn/network.py:98`, `:171` | `sed -n '94,98p;168,172p' pinn/network.py`; `grep -rn 'first_omega_0' pinn/ --include='*.py'`; `grep -n 'torch.sin\|F.linear' pinn/network.py` | `:98` `        return torch.sin(omega * F.linear(x, self.weight, self.bias))` inside `_SIRENLayer.forward`; `:168` the comment `# The "first" SIREN layer: 14 -> 256, omega_0 = first_omega_0 = 30.` and `:171` `            omega_0=spec.first_omega_0, is_first=True,`. Scoped search over `pinn/**/*.py`: inside the live network module `first_omega_0` occurs only at `network.py:9` and `:66` (docstrings), `:165` (stored), `:168` (comment) and `:171` (the single `is_first=True` construction); `network.py` has exactly two forward primitives, `torch.sin(...)` at `:98` and a bare `F.linear` at `:149` (the linear head) | CONFIRMED | Content and line both resolve. The exclusivity is established by the scoped search, whose scope is stated: `pinn/**/*.py`, on the token `first_omega_0`. Recorded so the row is not read as more than it is — `:98` is the **shared** `_SIRENLayer.forward`, used by the input layer and by the even hidden layers alike, so it carries the *form* the claim attributes rather than being an input-layer-exclusive line; exclusivity rests on `:171` being the only `is_first=True` construction. `pinn/basic_architecture.py` also names `first_omega_0`, and it is the v1.3-era module the project records as not authoritative; the report cites neither it nor any line in it |
| PC-1d | Layer 1 of the hidden stack is an odd SQR block, so the first operation applied to `h₁` is `LayerNorm(h₁)²`; LayerNorm is positively scale-invariant | `[REPO]`+`[OWN]` → REPO-DER + ANA | `pinn/network.py:122` | `sed -n '101,104p;112,122p;174,190p' pinn/network.py`; `sed -n '61,67p' pinn/architecture_spec.py` | `:101` `class _OddSkipBlock(nn.Module):`; `:104` the docstring `forward(x_prev) = siren(x_prev) + (LayerNorm(x_prev)) ** power_p`; `:117-118` `self.layernorm = nn.LayerNorm(width, eps=layernorm_eps,` / `elementwise_affine=layernorm_elementwise_affine)`; `:122` `        return self.siren(x_prev) + self.layernorm(x_prev) ** self.power_p`; `:174-175` "12 hidden layers of width 256; odd-numbered (1,3,...,11) are SQR-SkipResNet blocks"; `:178-179` `if layer_num % 2 == 1:` → `_OddSkipBlock`; `architecture_spec.py:61` `hidden_depth: int = 12`, `:65` `layernorm_elementwise_affine: bool = False`, `:66` `layernorm_eps: float = 1e-5`, `:67` `power_p: int = 2` | CONFIRMED-NARROWER | The structural half re-derives, and more strongly than claimed: hidden layer 1 is an odd SQR block, the stack holds **exactly six** of them (odd indices 1,3,…,11 of 12), and `power_p = 2` is a locked spec field rather than an assumption. The narrowing is in the second clause: the LayerNorm actually constructed at `:117-118` carries `eps = 1e-5`, and `LN(c·h) = LN(h)` holds **exactly only in the `eps → 0` limit** — for `eps > 0` the invariance is accurate to the extent that `c²σ² ≫ eps` and is not the exact identity the wording asserts. See the per-claim section |
| PC-1e | The clean-room `ω₀` sweep table, the 1.63-decade figure per 1000×, the 8.66-decade depth result, ≈1.44 decades per SQR block, and the reproduction of the audit's six-row probe | `[OWN]` → ANA | `OB:81`-`:96` | n/a — clean-room model, no in-repo locus | n/a — routed in the register below | NOT-VERIFIABLE-HERE | The audit-side half of the comparison is separately confirmed at PC-8g and CC-7; only the clean-room half is routed |
| PC-1f | The capacity the package attributes to the SIREN initialization scale lives in `AR` §2.3's power-skip stack (`:204-261`), which is not an authorized surface under SCOPE-33 (`REQ:118`) and is recorded in master §7 only as an unsurfaced gap | `[REPO]`+`[PKG]`+`[OWN]` → REPO-DER + PKG-INT + ANA | `AR:204-261`; `REQ:118`; `MA:311` | `sed -n '204,206p;259,261p' <AR>`; `sed -n '118p' <REQ>`; `sed -n '311p' <MA>` | `AR:204` `## 2.3 The Power-Enhanced SkipResNet (SQR-SkipResNet) Formulation` with the section closing at `:260-261`; `REQ:118` `\| SCOPE-33 \| **Framework-spec edits ARE authorized**, narrowly: only the items in `52-VER-20-ROUTING-HANDOFF.md` (a)–(e), plus the `n_col`/`N_t` disposition coupled to item (e) per SPEC-06. …`; `MA:311` `**S3-adjacent — the SQR-SkipResNet contribution to the same quantity (added at ERW-02).** … Whether the stack constitutes a surface of its own is not settled by anything in this package.` | CONFIRMED-NARROWER (locus and scope) · NOT-VERIFIABLE-HERE (the capacity attribution) | Three of the four assertions re-derive exactly: §2.3 occupies `:204`–`:261`; SCOPE-33's enumeration does not reach §2.3; master §7 records the stack as an unsurfaced gap in its own words. The fourth — that the capacity **lives** in that stack — rests entirely on the clean-room depth sweep at R-05 and is routed |
| PC-2a | The round prompt states four files named `pinn_architecture.md`; master §3's table lists **five**, and amendment `A-11` records the four → five correction explicitly | `[PKG]` → PKG-INT | `PR:87-88`; `MA:424` | `grep -niE 'four\|five' <PR>`; `sed -n '87,88p' <PR>`; `sed -n '424p' <MA>` | `PR:87-88` `**Resolve repository anchors by content, not by line number.** Four files named` / `` `pinn_architecture.md` exist in the tree with different line numbering, and only ``; `MA:424` `\| A-11 \| §3 anchor-resolution rule: fifth `pinn_architecture.md` path added; "Four files" corrected to "Five files" \| **correction** \| …` | CONFIRMED | Content and line both resolve on both sides: the prompt does say four, and the master's amendment record does register the four → five correction. `PR` sits outside the certified citable-path set, so its identity against the pin was established here rather than inherited — see *Coverage boundary* |
| PC-2b | The five paths and their line counts: 1098 (live, authoritative), 1064, 1013, 1010, 1010 | `[REPO]` → REPO-DER | the five `pinn_architecture.md` copies listed at `OB:116`-`:120` | `wc -l <the five copies>`; `find . -name 'pinn_architecture.md' -not -path './.git/*' \| LC_ALL=C sort \| wc -l` | `1098` (live, authoritative), `1064` (integrity-r2), `1013` (trainex-r1), `1010` (integrity-r1), `1010` (02-data-pipeline research package); tree-wide count of files with that basename: `5` | CONFIRMED | All five line counts match the report's table exactly, path for path. The independent tree-wide count confirms the set is closed at five, so the finding's "five, not four" is complete rather than merely larger than four |
| PC-3a | `ln(smallest normal float32) = ln(1.175494×10⁻³⁸) = −87.33654` — the audit's figure is the **normal-range** boundary, not flush-to-zero; IEEE-754 flush-to-zero for float32 is at `−ln(1.401298×10⁻⁴⁵) = 103.279` | `[OWN]` → ANA | IEEE-754 binary32 constants | `python3 -c "import math; print(2.0**-126, math.log(2.0**-126), 2.0**-149, -math.log(2.0**-149))"` | `1.1754943508222875e-38 -87.3365447505531 1.401298464324817e-45 103.27892990343184` | CONFIRMED | Both figures re-derive to the digits the finding prints: `−87.33654` for the smallest **normal** binary32 and `103.279` for the smallest **subnormal**. The distinction the finding draws — that the audit's figure is the normal-range boundary and not flush-to-zero — is exactly what the two constants show |
| PC-3b | `pinn/loss_catalog.py:97` sets `mathematical_floor = math.log(torch.finfo(dtype).tiny)` and `:339` computes `weights = torch.exp(torch.clamp_min(exponent, floor))`, so the observed `w_min` is the **clamp** | `[REPO]` → REPO-DER | `pinn/loss_catalog.py:97`, `:339` | `sed -n '77,115p;339p' pinn/loss_catalog.py`; `python3 -c "import struct,math; f=lambda x: struct.unpack('f',struct.pack('f',x))[0]; n=lambda x:(lambda b: struct.unpack('f',struct.pack('I',b-1 if x<0 else b+1))[0])(struct.unpack('I',struct.pack('f',x))[0]); t=2.0**-126; r=f(math.log(t)); a=n(r) if r<math.log(t) else r; print(r,a,f(math.exp(a)))"` | `:97` `    mathematical_floor = math.log(torch.finfo(dtype).tiny)`; `:339` `    weights = torch.exp(torch.clamp_min(exponent, floor))`; and between them `:98-101` represent the floor in the active dtype, `:102-107` advance it once with `torch.nextafter` when that rounding fell below the mathematical value, `:108` `min_weight = float(torch.exp(floor_tensor)…)`. Round-trip: `-87.3365478515625 -87.33654022216797 1.175499675756452e-38` | CONFIRMED-SHARPER | Both cited lines carry exactly the attributed content. Stronger statement the evidence supports: the floor actually used is **not** `math.log(tiny)` but its dtype-rounded, `nextafter`-advanced form, and the retained log's `w_min = 1.1754998158862984e-38` equals `exp(that floor)` to within **one** float32 ULP. That pins the observed value to the clamp far more tightly than "the observed `w_min` is the clamp" |
| PC-3c | The retained log confirms it to the last digit: `w_min = 1.1754998158862984e-38` on **502/502** steps, `w_max = 1.0`, `w_mean = 0.0625` exactly | `[REPO]` → REPO-DER | `LOG` | the command recorded at R-13 | `502 {'w_min': [1.1754998158862984e-38], 'w_max': [1.0], 'w_mean': [0.0625], 'front_idx': [0]}` | CONFIRMED | Each of the three values is single-valued across all 502 records, so "on 502/502 steps" is exact rather than approximate, and `w_mean = 0.0625` is `1/16` exactly. Checked against the primary log; no summarising document stands between the claim and the record |
| PC-3d | float64's floor is `ln(2.225074×10⁻³⁰⁸) = −708.396`; the clip's entire dynamic range across the two precisions is `708.40/87.34 = 8.11×` in the exponent = **0.91 decades** in `R̄` | `[OWN]` → ANA | IEEE-754 binary64 constant | `python3 -c "import math; print(2.0**-1022, math.log(2.0**-1022), 708.396/87.33654, math.log10(708.396/87.33654))"` | `2.2250738585072014e-308 -708.3964185322641 8.11110676012583 0.9090801177155879` | CONFIRMED | All three figures re-derive to the digits the finding prints: `−708.396`, `8.11×`, `0.91` decades |
| PC-3e | The clean-room weight vector at `η_c = 1` is still 15/16 floored under the float64 floor | `[OWN]` → ANA | clean-room vector, `OB:146` | `python3 -c "import math; print(2.527e10/708.396)"` with `R̄₁` from R-13 and `η_c` from D-3b | `35672138.182598434` — the exponent at `n = 2` is `−η_c R̄₁ ≈ −2.527×10¹⁰`, below the float64 floor `−708.396` by a factor of `3.567×10⁷` | CONFIRMED-SHARPER | Stronger statement the evidence supports: the 15/16 result does not depend on the clean-room vector at all. At the project's **own** retained residual scale every one of the 15 non-leading weights sits more than seven orders of magnitude below the float64 floor, so the conclusion holds on repository evidence rather than on a re-implementation. See the per-claim section |
| PC-4a | `AR`'s `## References` (heading at `:1017`, entries `:1019-1035`) carries 17 entries and **none** cites a source for §3.2's causal weighting | `[REPO]` → REPO-DER | `AR:1017`, `:1019-1035` | `sed -n '1017p' <AR>`; `awk 'NR>=1019 && NR<=1035' <AR> \| grep -cE '^\[[0-9]+\]'`; `awk 'NR>=1017 && NR<=1035' <AR> \| grep -icE 'causal\|causality\|wang\|perdikaris\|sankaran\|116813\|2203\.07404'`; `grep -icE 'perdikaris\|sankaran\|116813\|2203\.07404\|respecting causality\|causality' <AR>` | `:1017` `## References`; numbered entries in `:1019`–`:1035`: **17**; matches inside the References block: **0** (`NEGATIVE-SEARCH-EMPTY`); matches in the **whole 1098-line file**: **0** (`NEGATIVE-SEARCH-EMPTY`) | CONFIRMED-SHARPER | The heading, the entry range and the entry count all resolve exactly. Stronger statement the evidence supports: the source is cited nowhere in the specification at all, not merely nowhere in its reference list. Scope of the negative search is stated: the whole file, on author surnames, the DOI article number and the arXiv identifier, plus the title phrase; the empty result is printed with an explicit marker rather than left as silence |
| PC-4b | `PINA:55-60` carries the block "**Original reference**: Wang, Sifan, Shyam Sankaran, and Paris Perdikaris. *Respecting causality for training physics-informed neural networks.* Computer Methods in Applied Mechanics and Engineering 421 (2024): 116813." | `[REPO]` → REPO-DER | `PINA:55-60` | `sed -n '55,60p' <PINA>` | `:55-59` `**Original reference**: Wang, Sifan, Shyam Sankaran, and Paris` / `Perdikaris.` / `*Respecting causality for training physics-informed` / `neural networks.*` / `Computer Methods in Applied Mechanics and Engineering 421 (2024):116813.`; `:60` adds `DOI: 10.1016/j.cma.2024.116813` | CONFIRMED | Content and line both resolve. The quotation is faithful; the report stops at `:59` and does not carry the DOI line, which is a truncation at a natural boundary rather than an alteration |
| PC-5a | In this project the prefix sum is taken over the per-collocation-point residual vector, with `rbar` built one entry per collocation time | `[REPO]` → REPO-DER | `pinn/loss_catalog.py:330-333`, `:342`; `pinn/training/controllers.py:656` | the commands recorded at R-03 and D-1b | `loss_catalog.py:330-333` build the exclusive prefix over `rbar`; `:342` `loss = (weights * rbar).mean()`; `controllers.py:651-656` construct `residual` with shape `(N_t, 3, 3)` and reduce it to one `rbar` entry per collocation time | CONFIRMED | Content and line both resolve. The shape is read at the construction site — `accel - force` over a `(N_t, 3, 3)` tensor, reduced on the last two axes — rather than inferred from the name `rbar` |
| PC-5b | 16 i.i.d. uniform draws are re-taken every step (`pinn/training/collocation_sampler.py:87`, `pinn/training/controllers.py:1307`) and sorted at `:607` | `[REPO]` → REPO-DER | `pinn/training/collocation_sampler.py:87`; `pinn/training/controllers.py:1307`, `:607` | the commands recorded at D-2b | `collocation_sampler.py:87` draws i.i.d. uniforms and `:82` defaults the count to `self.collocation_count`; `controllers.py:603` re-draws whenever the caller passes `None`, which the Adam loop does at `:1081`; `:607` sorts; `:1307` is the **L-BFGS** draw, taken once and held fixed for the segment | UNSUPPORTED | The same finding as D-2b, recorded here because PC-5 repeats the citation. The substance resolves by content at `:603`/`:1081`; the cited `:1307` does not carry it. The count 16 is not fixed at any cited line either — it is the sampler's configured `collocation_count`, and the retained log's `w_mean = 0.0625 = 1/16` (PC-3c) is what evidences it |
| PC-5c | In the source method the prefix sum runs over `M` temporal segments, with the residual averaged over the `N_x` points at each time level (Eq. 2.13) and restated over `M` equal sequential segments in the Expert's Guide | `[LIT]` → LIT | Wang, Sankaran & Perdikaris Eq. 2.13; Expert's Guide Eq. 2.11 | n/a — published source, not settleable in this repository | n/a — routed in the register below | NOT-VERIFIABLE-HERE | The in-repo reference implementation bearing on the same point is verified separately at PC-5d |
| PC-5d | The in-repo reference implementation does exactly that: `_split_tensor_into_chunks` (`PINA:187`), one residual per chunk, `_compute_weights` over the chunk vector (`:208-219`) | `[REPO]` → REPO-DER | `PINA:187`, `:208-219` | `sed -n '187,207p;208,219p' <PINA>`; `sed -n '127,147p' <PINA>` | `:187` `    def _split_tensor_into_chunks(self, tensor):`; `:202-205` sort by time, `time_tensor.unique(return_counts=True)`, `chunks = torch.split(tensor, tuple(idx_split))`; `:133-140` the loss loop appends **one** `loss_val` per chunk to `time_loss`; `:143` `time_loss = torch.stack(time_loss)`; `:145-146` `with torch.no_grad(): weights = self._compute_weights(time_loss)`; `:217` `cumulative_loss = self._eps * torch.cumsum(loss, dim=0)` | CONFIRMED-NARROWER | Content and line both resolve at both cited anchors, and the structural contrast the finding rests on survives intact: the vendored implementation forms **one residual per time level**, not one per collocation point. The narrowing is in "exactly that". `:204` chunks on `time_tensor.unique(...)` — the **distinct time values present in the sampled batch** — which realizes the per-time-level form of Eq. 2.13 rather than the Expert's Guide's *fixed equal sequential segments*. The two readings the finding offers are not equivalent, and only the first is implemented here. See the per-claim section |
| PC-6a | From the retained log: `median(grad_norm_raw_phys / grad_norm_raw_data) = 6.32×10¹²` — 12.80 decades; `λ_phys` ramps 0 → 1 over steps 1–100 and is 1.0 for steps 101–502; `loss_data` descends 0.0706 → 0.0209; `loss_ic` median `2.897×10⁴` | `[REPO]` → REPO-DER | `LOG` | `python3 -c "import json,math,statistics as st;rs=[json.loads(l) for l in open('<LOG>') if l.strip()];r=[x['grad_norm_raw_phys']/x['grad_norm_raw_data'] for x in rs];lam=[x['lambda_phys'] for x in rs];ld=[x['loss_data'] for x in rs];li=[x['loss_ic'] for x in rs];print(len(rs), st.median(r), math.log10(st.median(r)), lam[0], lam[99], sum(1 for v in lam if v==1.0), ld[0], ld[-1], st.median(li))"` | `502 6321884391035.326 12.800846549587316 0.0 0.99 402 0.07055064290761948 0.02091073989868164 28974.875` | CONFIRMED | Four statistics, each computed over the whole retained record — 502 of 502 — which is the span the claim's wording implies. The gradient ratio is `6.3219×10¹²` = **12.8008** decades. `λ_phys` is `0.0` at step 1, rises by `0.01` per step to `0.99` at step 100, and is `1.0` on exactly `402` records, which are steps 101–502. `loss_data` runs `0.070551` → `0.020911`. `loss_ic` median is `28974.875`, whose four-significant-figure form is `2.897×10⁴` as printed. Checked against the primary log; no summarising document stands between the claim and the record |
| PC-6b | Under round-to-nearest float32 an addend below `2⁻²⁴ = 5.96×10⁻⁸` of the running sum is lost — 7.2 decades of headroom | `[OWN]` → ANA | IEEE-754 binary32 mantissa width | `python3 -c "import math; print(2.0**-24, -math.log10(2.0**-24))"` | `5.960464477539063e-08 7.224719895935548` | CONFIRMED | Both figures re-derive to the digits the finding prints: `5.96×10⁻⁸` and `7.2` decades. This is elementary closed-form arithmetic on the binary32 significand width and is recorded as elementary, not as a repository fact: binary32 carries a 24-bit significand, so under round-to-nearest an addend below half an ulp of the running sum leaves that sum unchanged |
| PC-6c | A recipe that repairs the weight vector but leaves `L_phys` at ~10⁹ will pass GATE-04 (i)–(iii) and still train on the physics term alone; no surface among S1–S5 as the package scopes them addresses this | `[OWN]` inference + `[PKG]` → ANA + PKG-INT | `OB:216`-`:219`; `REQ:100`; `MA` §4.3, §7 | n/a — a prediction about a run this milestone does not authorize | n/a — routed in the register below | NOT-VERIFIABLE-HERE | Its arithmetic inputs are each confirmed at PC-6a and PC-6b; the prediction is not, and the scoping half is a reading of the package |
| PC-7a | Under batch-mean normalization the weight vector is **bit-identical** at `R̄ ~ 10¹⁰`, `10²` and `10⁻⁴` | `[OWN]` arithmetic → ANA | `OB:227`-`:229` | `python3` script forming `w_n = exp(-Σ_{m<n} R̄_m/mean(R̄))` on 200 random 16-point vectors and comparing the IEEE bit patterns before and after a `10⁻⁸` rescaling | `trials=200  bitwise-different=155  max \|w(R)-w(cR)\| = 2.220e-16` | CONFIRMED (exact invariance) · NOT-VERIFIABLE-HERE (bit-identity) | Two readings, and they are not the same claim. **Exact invariance** is confirmed as an elementary identity: `(cR̄_m)/mean(cR̄) = R̄_m/mean(R̄)` in real arithmetic for any `c > 0`, so the weight vector cannot respond to the residual's overall magnitude. **Bit-identity** does **not** follow from it and generically fails — on substitute vectors the rescaled weight vector differs in its last bit in 155 of 200 trials, deviating by about one ulp. The demonstration is on substitute vectors and is evidence about the two readings, **not** about the report's own vector, which this repository does not carry. See the per-claim section |
| PC-7b | `front_idx = max{n : w_n > 0.5}`, defined at `pinn/training/controllers.py:692-694` and documented at `pinn/training/tb_sink.py:15` | `[REPO]` → REPO-DER | `pinn/training/controllers.py:692-694`; `pinn/training/tb_sink.py:15` | `sed -n '688,695p' pinn/training/controllers.py`; `sed -n '13,17p' pinn/training/tb_sink.py` | `controllers.py:692-694` `"front_idx": max(` / `                    [n for n, w in enumerate(w_n_list) if w > 0.5], default=-1,` / `),` inside the `"w_n_stats"` block opened at `:688`; `tb_sink.py:14-15` `` `causal/w_min`, `causal/w_mean`, `causal/w_max`, `causal/front_idx` `` / ``(= ``max{n : w_n > 0.5}``) from the ``w_*``/``front_idx`` fields.`` | CONFIRMED | Content and line both resolve at both loci — the definition at the first, the same definition restated in documentation at the second. The `default=-1` branch is recorded because it is the value the field takes when no weight exceeds `0.5`, and the retained log's constant `front_idx = 0` (R-13) is therefore the leading weight qualifying and no other, not the empty case |
| PC-7c | Invariant B trips on the **high-water mark** of `front_idx` (`pinn/training/guards.py:593-615`, `front_advance_window_n`), which is `500` at `CFG` `run.invariants.front_advance_window_n` | `[REPO]` → REPO-DER | `pinn/training/guards.py:593-615`; `CFG:31` | `sed -n '585,617p' pinn/training/guards.py`; `grep -n 'front_advance_window_n' <CFG>` | `guards.py:586-591` maintain `self.front_high_water`, updating `self.last_advance_step` only when `front_idx > self.front_high_water`; `:593-599` open the trip condition; `:600` `age = int(step) - int(self.last_advance_step)`; `:601` `saturated = self.front_high_water >= int(n_colloc) - 1`; `:602` `if age > self._front_advance_window_n and not saturated:`; `:605` `"guard": "invariant_b"`. `CFG:31` `    front_advance_window_n: 500` | CONFIRMED | Content and line both resolve, and the high-water reading is read off the guard's own state rather than inferred: `last_advance_step` advances only on a strict increase of `front_high_water`, so `age` measures steps since the high-water mark last moved, which is exactly what the claim says the guard trips on. The `saturated` escape at `:601` is recorded because it bounds the claim: the guard does not trip once the high-water mark reaches `n_colloc − 1`, which is not a case the retained run reaches |
| PC-8a | All **10** `BEGIN VERBATIM` blocks in the framework-specs bundle have body length exactly (claimed range) + 2 wrapper blank lines — uniform across all ten | `[OWN]` over `[PKG]` → ANA + PKG-INT | `BU` | `python3` script pairing each `BEGIN VERBATIM <path>:<s>-<t>` marker with its `END VERBATIM` and comparing `end − begin − 1` against `t − s + 1`, and asserting the first and last enclosed lines are empty | `LEN-UNIFORM 10/10  WRAPPER-BLANKS 10/10` — markers at `BU:57/137`, `147/208`, `218/241`, `251/365`, `375/431`, `441/511`, `521/591`, `601/650`, `660/772`, `782/875`; claimed spans 77, 58, 20, 111, 53, 67, 67, 46, 109, 90 and enclosed spans 79, 60, 22, 113, 55, 69, 69, 48, 111, 92 | CONFIRMED | Ten blocks found, ten checked, uniform on both properties with no exception. The count `10` is derived from the file rather than taken from the claim. `BU` sits outside the certified citable-path set; its identity against the pin is established under *Coverage boundary* |
| PC-8b | Three boundary pairs (`127/203`, `383/493`, `262/281`) were compared line-for-line against the live file and match verbatim | `[REPO]` → REPO-DER | `BU`; `AR`; `CT` | the same script, extended to compare each block's stripped body list against `open(<source>).split('\n')[s-1:t]` for equality | `VERBATIM-MATCH 10/10`, with body lengths 77, 58, 20, 111, 53, 67, 67, 46, 109, 90 equal to the claimed spans in every case | CONFIRMED-SHARPER | The three named pairs match, and so do the other seven. Stronger statement the evidence supports: **all ten** blocks are line-for-line identical to their live source ranges — six against `AR` and four against `CT` — so the bundle is byte-faithful across every excerpt it carries, not merely at the three boundaries that were spot-checked. See the per-claim section |
| PC-8c | Every spec anchor the master cites resolves **by content** in the live 1098-line file: `:181`, `:429`, `:435`, `:445`, `:454`, `:461`, `:668-671`, `:692` | `[REPO]` → REPO-DER | `AR:181`, `:429`, `:435`, `:445`, `:454`, `:461`, `:668-671`, `:692` | `wc -l < <AR>`; `sed -n '181p;429p;435p;445p;454p;461p;668,671p;692p' <AR>` | `1098`; `:181` the fixed-at-30 sentence; `:429` `$$\bar R_n = \frac{1}{3}\sum_{i=1}^{3} \| f_i(u_n) \|^2.$$`; `:435` the `w_n = \exp(...)` formula; `:445` the Phase-35 LOSS-04 contract block; `:454` `def sample_collocation_points(u_min=0.0, u_max=1.0, n_col=4096, strategy='uniform',`; `:461` `n_col: Number of collocation points (recommended: 2048-4096)`; `:668-671` the underflow-only clip paragraph; `:692` the Phase-35 guard block | CONFIRMED | Eight anchors, each resolved **by content first** and then checked for line resolution; all eight resolve on both. The file is 1098 lines, as the claim states, so the "live 1098-line file" is the same object throughout |
| PC-8d | The four stale anchors the master warns about are confirmed stale in `REQ`: `:424 → :445`, `:167 → :181`, `:433 → :454`, `:440 → :461` (`REQ:90`, `:95`) | `[REPO]` → REPO-DER | `REQ:90`, `:95`; `AR:424`, `:167`, `:433`, `:440` | the two anchor sweeps recorded in the `AWKWARD-COMMANDS` block below; `sed -n '424p;167p;433p;440p' <AR>` | `REQ` carries exactly three spec anchors — one at line 90 written out as a full path with `:424`, and two at line 95 written as backticked bare anchors `:433` and `:440`. There is **no** occurrence of `:167` anywhere in `REQ`. `AR:424` is `- $\epsilon_{train} = 10^{-5}$ …` (softening-parameter prose); `AR:167` is `cause the distribution of activations to either collapse to zero or`; `AR:433` is **blank**; `AR:440` is `$$L_{phys}^{causal} = \frac{1}{N_t} \sum_{n=1}^{N_t} w_n \bar R_n.$$` | UNSUPPORTED | The cited locations exist and do not carry what the claim attributes to them. **Three** of the four anchors are present at the two cited lines and every one of the three is confirmed stale with the replacement the claim gives. The fourth, `:167`, appears **nowhere** in `.planning/REQUIREMENTS.md`; its only occurrence in the package is the master's own sweep, which does not attribute it to `REQ` either. Distinguished from `REFUTED`: the staleness of `:167 → :181` is separately true as a property of the spec file, so nothing here says the anchor is fine — only that `REQ` is not where it is cited. See the per-claim section |
| PC-8e | `F-05` verified: `front_idx = 0` on **502/502** logged steps, single-valued | `[REPO]` → REPO-DER | `LOG` | the command recorded at R-13 | `502 {…'front_idx': [0]}` — one distinct value across all 502 records | CONFIRMED | Single-valued at `0` over the whole retained record, so "502/502" is exact rather than approximate. Overlaps R-13 and is kept as its own row because `F-05` is a separately identified package fact whose verdict a later plan may need to cite on its own |
| PC-8f | `F-08` (`AR:445`), `F-09` (`AR:181`), `F-10` (`AR:668-671`, `:692`), `F-14` (`pinn/training/controllers.py:656`) and `F-15` (`pinn/loss_catalog.py:339`, floor resolver `:77`, `:97`) all verified | `[REPO]` → REPO-DER | `AR:445`, `:181`, `:668-671`, `:692`; `pinn/training/controllers.py:656`; `pinn/loss_catalog.py:339`, `:77`, `:97` | `sed -n '445p;181p;668,671p;692p' <AR>`; `sed -n '651,656p' pinn/training/controllers.py`; `sed -n '77p;97p;339p' pinn/loss_catalog.py` | The four `AR` anchors as recorded at PC-8c; `controllers.py:656` `        rbar = (residual ** 2).sum(dim=(-2, -1)) / 3.0`; `loss_catalog.py:77` `def resolve_causal_clip_facts(dtype, device) -> dict[str, object]:`, `:97` `    mathematical_floor = math.log(torch.finfo(dtype).tiny)`, `:339` `    weights = torch.exp(torch.clamp_min(exponent, floor))` | CONFIRMED | Five package facts in one finding; each checked at its own locus and each resolving by content and by line. `F-14`'s quoted code line is reproduced character for character at `controllers.py:656`, and `F-15`'s three loci are the resolver's definition, its mathematical floor and the clamp that consumes it |
| PC-8g | `M7`'s arithmetic (`R̄ ≈ ‖a′‖²/3`) re-derived: 1.374, 2.466, 1.613, 2.595, 1.254, 1.733 (×10¹⁰) against the printed 1.37, 2.46, 1.62, 2.60, 1.25, 1.74 — agrees | `[OWN]` over `[PKG]` inputs → ANA + PKG-INT | `MA:143` (`M7`); `MA:112-117`; `AUD:142`, `:144-149` | `python3 -c "a=[2.03e5,2.72e5,2.20e5,2.79e5,1.94e5,2.28e5]; print([round(x*x/3/1e10,3) for x in a])"` | `[1.374, 2.466, 1.613, 2.595, 1.255, 1.733]` | CONFIRMED | The six ‖a′‖ inputs and the six printed `R̄` medians are read from the master's table at `MA:112-117` and independently from the audit's own table at `AUD:144-149`; the two carry the same values. Five of the six re-derivations reproduce the finding's digits exactly; the fifth is `1.255` where the finding prints `1.254`, a last-place truncation rather than a rounding, and it does not move the comparison. Agreement with the printed column is within `0.5 %`, which is the precision the three-significant-figure ‖a′‖ column can support once squared |
| PC-9a | The r2 report estimates "a second-derivative residual through an ω₀ = 30 first-layer SIREN generically produces `\|a′\|` of order `(2ω₀)² ≈ 3.6e3` per unit amplitude", labelled `[PKG]` / r2 Q3 §(b) reading 1 | `[PKG]`/`[r2-QUAL]` → PKG-INT | `OB:271-273`; attributed to the package | `grep -c '3.6e3' <MA> <BU> <EV>`; `grep -n '3.6e3' <R2>`; `sed -n '631,636p' <R2>`; `grep -n 'H-01' <MA>` | Occurrences of the figure in each of the three attachments: `0`. `R2:633-635` `1. *Faithful reporting of a badly-fit model in a consistent frame.* A` / `second-derivative residual through an ω₀ = 30 first-layer SIREN generically` / `produces \|a′\| of order (2ω₀)² ≈ 3.6e3 per unit amplitude before training`, opened at `R2:631` by `compatible-with-evidence readings, none established:`. `MA:289` `\| H-01 \| The trainex-r2 round's Q3 interpretive content … \| `trainex-r2-research-report.md` Q3 (qualified in §0) \| agent analysis — not established f…` | CONFIRMED-NARROWER | The quotation is faithful: `R2:633-635` carries it word for word, it is reading 1, and `R2:631` marks all such readings "none established" — so "reading 1" is the report's own framing carried through correctly. The narrowing is the **evidence class**. Under the source report's own definitions at `claude-resolution.md:35`–`:38`, `[PKG]` means "package-derived (the three attachments)", and this sentence appears in **none** of the three; it was read in the live tree, which those definitions call `[REPO]`. What the package carries is the master's `H-01` row at `MA:289`, which *names* the r2 Q3 content and points at the file without reproducing the sentence. The claim therefore holds as "the r2 report, read in the tree, says this" and not as "the package says this". See the per-claim section |
| PC-9b | The locked first-layer bound is `U[±1/n_in]` with `n_in = 14` (`pinn/network.py:82`) and the head is `U[±1/√256]` (`:139`) | `[REPO]` → REPO-DER | `pinn/network.py:82`, `:139` | `sed -n '81,84p;135,139p' pinn/network.py`; `sed -n '59,62p' pinn/architecture_spec.py` | `network.py:81-82` `        if self.is_first:` / `            bound = 1.0 / self.in_features`, with the non-first branch at `:84` `            bound = math.sqrt(6.0 / self.in_features) / self.omega_0`; `:135` `_LinearHead.__init__` and `:139` `        bound = 1.0 / math.sqrt(self.in_features)`; `architecture_spec.py:59` `    input_dim: int = 14` and `:62` `    hidden_width: int = 256` | CONFIRMED | Content and line both resolve at both cited lines, and the two numerals the claim supplies are resolved at their own loci rather than assumed: `n_in = 14` is the spec's `input_dim` and the head's `in_features` is the spec's `hidden_width = 256`, so `U[±1/n_in]` is `U[±1/14]` and `U[±1/√256]` is `U[±1/16]`. The `is_first` branch is what makes the first-layer bound `1/n_in` rather than the SIREN default at `:84` |
| PC-9c | The clean-room depth-0 network gives `‖a′‖ ≈ 12.7`, not `3.6×10³`; the 12-layer stack then multiplies by ≈`1.6×10⁴` to reach the measured `2×10⁵` | `[OWN]` → ANA | clean-room model, `OB:280`-`:281` | n/a — clean-room model, no in-repo locus | n/a — routed in the register below | NOT-VERIFIABLE-HERE | Its internal consistency with the audit's own first row is recorded in the register entry |
| PC-9d | r2's reading 2 (frame inconsistency) and its `RG-04` (`1/9` vs `1/3`) are already retired by the 2026-08-17 audit and by `F-14`/`F-15`; both retirements confirmed | `[REPO]` → REPO-DER | `AUD:15`, `:86`; `pinn/training/controllers.py:656`; `AR:429` | `sed -n '15p;86p' <AUD>`; `grep -n 'RG-04' <R2>`; `sed -n '656p' pinn/training/controllers.py`; `sed -n '429p' <AR>`; `grep -niE 'RG-04\|1/9\|frame inconsisten' <AUD>` | `AUD:15` `**Verdict:** **NO MISMATCH.** The residual frame is conformant. The named hypothesis (a missing `u ↔ t` chain factor producing a `≈ 99·a_grav` floor) is **refuted** on four independent grounds.`; `AUD:86` `\| `R̄_n = (1/3)Σ_i‖f_i‖²` \| `controllers.py:656` \| conformant (CONF-04/D-05) \|`; `R2:1162` states `RG-04` as "implementation uses mean over 9 components ((1/9)Σ‖f‖²) where §3.2 locks (1/3)Σ‖f‖²"; `controllers.py:656` `        rbar = (residual ** 2).sum(dim=(-2, -1)) / 3.0`; `AR:429` `$$\bar R_n = \frac{1}{3}\sum_{i=1}^{3} \| f_i(u_n) \|^2.$$`; the scoped search for r2's own identifiers inside the audit returns **0** matches — `NEGATIVE-SEARCH-EMPTY` | CONFIRMED | Both retirements resolve. Reading 2 is retired at `AUD:15`, whose verdict is that the residual frame is conformant and the frame-inconsistency hypothesis refuted. `RG-04` is retired three ways that agree: `AR:429` locks the `1/3` convention, `controllers.py:656` implements it as a divide by `3.0` over the two collapsed axes, and `AUD:86` records that pairing as conformant. Recorded so the row is not read as more than it is: the audit **names** neither "reading 2" nor `RG-04` — the scoped search over `AUD` for those tokens is empty — so the retirement is established by content correspondence between the audit's findings and r2's rows, not by the audit citing r2 |

### Group C — the departures table (`OB` §2, `:353`–`:360`), split into its source side and its project side

**These labels are the report's own.** `D-1` … `D-7` here are the rows of the report's
own departures table. They are **not** this project's decision identifiers `D-01` … `D-18`
recorded in `.planning/phases/54-recalibration-decision-grounding/54-CONTEXT.md`. The two
namespaces collide by accident and a reader must not conflate them.

| ID | Claim, in the source's own terms | Evidence class | Cited location(s) | Re-derivation command | Output | Verdict | Note |
|---|---|---|---|---|---|---|---|
| D-1a | Source: the residual is averaged **within `M` temporal segments** and the prefix sum has `M` terms | `[LIT]` → LIT | Wang, Sankaran & Perdikaris Eq. 2.13; Expert's Guide Eq. 2.11 | n/a — published source, not settleable in this repository | n/a — routed in the register below | NOT-VERIFIABLE-HERE | Same class as PC-5c and routed to the same place |
| D-1b | This project: one residual per **individual collocation point**, prefix sum has `n_col` terms; each `R̄_m` is a 1-sample estimate | `[REPO]` → REPO-DER | `pinn/loss_catalog.py:330-333`; `pinn/training/controllers.py:656` | `sed -n '327,333p' pinn/loss_catalog.py`; `sed -n '651,656p' pinn/training/controllers.py` | `:327-328` the in-code comment "Prefix sum of stopgrad(Rbar) for the STRICTLY preceding points"; `:330` `cumsum = torch.cumsum(detached, dim=0)`; `:333` `cumsum_excl = torch.cat([zeros, cumsum[:-1]], dim=0)`; `controllers.py:656` `rbar = (residual ** 2).sum(dim=(-2, -1)) / 3.0` over a residual whose leading axis is the collocation-time index | CONFIRMED | Content and line both resolve. The 1-sample property is read off the construction site: `sum(dim=(-2,-1))` collapses the body and component axes and leaves one scalar per collocation time, so each `R̄_m` is formed from exactly one sampled time |
| D-2a | Source: segments are **fixed and equal**, spanning the domain | `[LIT]` → LIT | Expert's Guide Eq. 2.11 | n/a — published source, not settleable in this repository | n/a — routed in the register below | NOT-VERIFIABLE-HERE | Routed with D-1a |
| D-2b | This project: 16 i.i.d. uniform draws on `[0,T]`, **re-drawn every step**, then sorted; `front_idx` is therefore not a persistent state, yet invariant B is defined on its high-water mark | `[REPO]` → REPO-DER | `pinn/training/collocation_sampler.py:87`; `pinn/training/controllers.py:607`, `:1307`; `pinn/training/guards.py:593-615` | `sed -n '85,92p' pinn/training/collocation_sampler.py`; `sed -n '602,607p;1304,1308p' pinn/training/controllers.py`; `grep -n '_build_anchor_context' pinn/training/controllers.py` | `collocation_sampler.py:87` `points = rng.uniform(0.0, T_CHARACTERISTIC_TIME, size=n)`; `controllers.py:602-603` `if fixed_collocation_times is None:` / `colloc_times = self._collocation_sampler.uniform()`; `:607` `order = np.argsort(colloc_times)`; `:1307` `fixed_collocation_times = self._collocation_sampler.uniform()` inside the **L-BFGS** routine, passed to `:1308` and held for the whole segment; call sites `:803`, `:1081`, `:1308` | UNSUPPORTED | Content and line resolution disagree, and the row records both. The **substance** resolves: the Adam loop calls `_build_anchor_context(..., None)` at `:1081`, which re-draws at `:603` every step. The **cited line does not carry it**: `:1307` is the L-BFGS path, which draws once into `fixed_collocation_times` and holds that set fixed — the opposite of "re-drawn every step". `collocation_sampler.py:87` and `:607` both resolve as cited. See the per-claim section |
| D-3a | Source: `ε` is **annealed** over 4 decades with the `min_i w_i > 0.99` criterion | `[LIT]` → LIT | published Algorithm 1 | n/a — published source, not settleable in this repository | n/a — routed in the register below | NOT-VERIFIABLE-HERE | Routed with R-02's published half |
| D-3b | This project: `η_c = 1` fixed for the whole run; the source's self-calibration is absent, the value is adopted and the procedure is not | `[REPO]` → REPO-DER | `AR:445`; `pinn/constants.py:71` | `sed -n '445p' <AR>`; `sed -n '70,71p' pinn/constants.py`; `grep -rniE 'eta_c' pinn/ --include='*.py'`; `grep -rniE '(anneal\|schedul)' pinn/ --include='*.py' \| grep -ciE 'eta_c'` | `AR:445` "…keeps the per-time causal weighting component as the default: `w_1 = 1`, `w_n = exp(-eta_c * sum_{m<n} stopgrad(Rbar_m))`, and `eta_c = 1`."; `pinn/constants.py:71` `CAUSAL_ETA_C = 1.0`; `eta_c` occurs at **10** loci under `pinn/**/*.py`, none of them a schedule; the anneal/schedule co-occurrence count is **0** — `NEGATIVE-SEARCH-EMPTY`, printed rather than left as silence | CONFIRMED | Content and line both resolve at both cited anchors. The negative half — that the value is fixed rather than scheduled — was verified by a **scoped** search over `pinn/**/*.py`, whose scope is stated here: all 10 `eta_c` loci are the constant, its import, the loss function's keyword default, one probe call site and one conformance-census row. Recorded as ambiguity rather than resolved: `AR:445` and `AR:668` both call `η_c = 1` a *default*, where the claim says *fixed* |
| D-4a | Source: `ε = 1` presumes a **non-dimensionalized, order-one** residual | `[LIT]` → LIT | Expert's Guide non-dimensionalization precondition | n/a — published source, not settleable in this repository | n/a — routed in the register below | NOT-VERIFIABLE-HERE | Routed with R-02's published half |
| D-4b | This project: `R̄ ≈ 2.5×10¹⁰` at initialization, so the precondition is violated by 10 decades | `[PKG]`+`[REPO]` → PKG-INT + REPO-DER | `MA:112-117`; `LOG` | `sed -n '112,117p' <MA>`; the `R̄₁` re-derivation recorded at R-13 | `MA:112-117` carry `R̄` medians `1.37`, `2.46`, `1.62`, `2.60`, `1.25`, `1.74` (×10¹⁰) across the six seed/IC rows; the retained log gives median `R̄₁ = 2.5267×10¹⁰` | CONFIRMED | Content and line both resolve. Two independent supports: the package table's six initialization medians all sit in `[1.25, 2.60]×10¹⁰`, and the primary log's own median is `2.53×10¹⁰`. Against an order-one precondition that is a violation of 10.0–10.4 decades, which is what "10 decades" states |
| D-5a | Source: tanh MLP with Glorot init; the Fourier-feature scale `σ ∈ [1,10]` is an explicitly **tuned** quantity | `[LIT]` → LIT | Expert's Guide | n/a — published source, not settleable in this repository | n/a — routed in the register below | NOT-VERIFIABLE-HERE | Routed with the other published-source halves |
| D-5b | This project: SIREN `ω₀ = 30` plus a 12-layer power-skip stack, with `ω₀` **locked and unscheduled**; `hidden_omega_0 = 1` where the Sitzmann scheme carries `ω₀` in every hidden layer | `[REPO]` → REPO-DER | `AR:181`; `pinn/constants.py:48`; `pinn/network.py:84` | `sed -n '181p' <AR>`; `sed -n '45,48p' pinn/constants.py`; `sed -n '84p;174,190p' pinn/network.py` | `AR:181` "`first_omega_0` is fixed at `30` and is not scheduled during training."; `pinn/constants.py:47-48` `SIREN_FIRST_OMEGA_0 = 30.0` / `SIREN_HIDDEN_OMEGA_0 = 1.0`; `pinn/network.py:174-175` "12 hidden layers of width 256; odd-numbered (1,3,...,11) are SQR-SkipResNet blocks, even-numbered (2,4,...,12) are plain SIREN"; `:84` `bound = math.sqrt(6.0 / self.in_features) / self.omega_0` for non-first layers | CONFIRMED | Content and line both resolve at every anchor. "Locked and unscheduled" is the spec's own sentence, quoted rather than inferred. The 12-layer stack and `hidden_omega_0 = 1` are read at their own loci; the stack contains exactly **six** odd SQR blocks, which is the count the report's depth argument uses |
| D-6a | Source: `w_1 = 1`, the sum running `k = 1 … i−1` | `[LIT]` → LIT | published Eq. 3.2 | n/a — published source, not settleable in this repository | n/a — routed in the register below | NOT-VERIFIABLE-HERE | Routed with R-01's published half |
| D-6b | This project: **the same** — exclusive prefix with `w_1` pinned | `[REPO]` → REPO-DER | `pinn/loss_catalog.py:333`, `:340-341` | `sed -n '331,333p;340,341p' pinn/loss_catalog.py` | `:331-333` `# Shift right by one: exclusive prefix.` / `zeros = torch.zeros(1, dtype=dtype, device=device)` / `cumsum_excl = torch.cat([zeros, cumsum[:-1]], dim=0)`; `:340-341` `# w_1 is identically 1 by construction (cumsum_excl[0] = 0); pin via constant.` / `_ = CAUSAL_W1` | CONFIRMED | Content and line both resolve. The exclusive shift is explicit in the code and its consequence for `w_1` is stated in the code's own comment, so the fidelity claim rests on the construction rather than on a reading of it |
| D-6c | And *more* faithful than PINA, whose `_compute_weights` uses an **inclusive** `cumsum` | `[REPO]` → REPO-DER | `PINA:217` | `sed -n '208,219p' <PINA>` | `:216-217` `# compute comulative loss and multiply by epsilon` / `cumulative_loss = self._eps * torch.cumsum(loss, dim=0)`; `:219` `return torch.exp(-cumulative_loss)` — no exclusive shift anywhere in the function | CONFIRMED | Content and line both resolve: `:217` is an inclusive `cumsum` with no right-shift, so PINA's `w_1` is `exp(−ε L_1)` rather than 1. Both sides of the comparison are in this repository, so the claim is settleable here in full |
| D-7a | Source: the weights are `stop_gradient` | `[LIT]` → LIT | published Eq. 3.2 / Algorithm 1 | n/a — published source, not settleable in this repository | n/a — routed in the register below | NOT-VERIFIABLE-HERE | Routed with D-6a |
| D-7b | This project: **the same** — `detached = rbar.detach()` | `[REPO]` → REPO-DER | `pinn/loss_catalog.py:329` | `sed -n '329p' pinn/loss_catalog.py` | `    detached = rbar.detach()` | CONFIRMED | Content and line both resolve. `detached` is what `:330`'s `cumsum` consumes, so the stop-gradient applies to the whole prefix sum and not only to the first term |

### Group D — supplementary rows for cited loci the three named sources do not carry

These exist so that **every** distinct repository citation in the report lands in some
ledger row. Each row states the claim that carries the citation.

| ID | Claim, in the source's own terms | Evidence class | Cited location(s) | Re-derivation command | Output | Verdict | Note |
|---|---|---|---|---|---|---|---|
| CC-1 | ADVANCE criterion 3 requires validation `L_phys < ε_phys = 10⁻⁴` | `[PKG]`+`[REPO]` → PKG-INT + REPO-DER | `CT` §Stage Transition Criteria; `CFG:48` | `grep -nF 'Stage Transition Criteria' <CT>`; `sed -n '1963p;1966p' <CT>`; `sed -n '48p' <CFG>` | `CT:1922` `## Stage Transition Criteria`; `:1963` `### 3. Physics-Residual Threshold (ADVANCE criterion 3 of 4, stage-dependent)`; `:1966` `$$\mathcal{L}_{\text{phys}}^{\text{val}} < \epsilon_{\text{phys}} \quad (\epsilon_{\text{phys}} = 10^{-4})$$`; `CFG:48` `  eps_phys: 0.0001` | CONFIRMED | Content resolves in both files; the report cites `CT` by section rather than by line, so only content resolution applies there, and `CFG:48` resolves by line as well. Recorded beside the verdict, because it bears on what is built on this number: the same section states at `CT:1932`–`:1936` that **all** its numeric thresholds are "provisional pending FUT Stage-0 pilot calibration (SCOPE-14)" and that the spec records the *form* of the success gate, "not calibrated values" |
| CC-2 | GATE-04's three train-free conditions are (i) no weight at the clamp floor; (ii) the weight vector carries differential information; (iii) `front_idx` **able** to advance | `[REPO]` → REPO-DER | `REQ:100` | `sed -n '100p' <REQ>` | `- [ ] **GATE-04**: **Train-free acceptance gate on the recalibration.** Before RUN-04 may spend a Stage-0 run, INST-04's probe must show … (i) no causal weight pinned at the dtype clamp floor; (ii) a weight vector carrying **differen**…` — all three conditions present at the cited line, in the cited order | CONFIRMED | Content and line both resolve. The line is quoted only as far as the third condition's opening, which is where the cell's width stops; the full text at `REQ:100` carries condition (iii) as the report states it |
| CC-3 | `λ_phys^max = 1` is **[LOCKED]**, with the Phase-53 contract block immediately below it | `[REPO]` → REPO-DER | `AR:683`, `:688` | `sed -n '683p;688p' <AR>` | `:683` `  $\lambda_{phys}^{max}(k) = 1$ **[LOCKED]**`; `:688` `> **Phase 53 contract: PHYS-05 per-stage table locked and locked-vs-default convention (SPEC-02; SPEC-03; GAP-45-03 owner ruling 2026-07-24, option A; …** | CONFIRMED | Content and line both resolve at both anchors. Verified as a locus claim only: that the value is locked and that a Phase-53 contract block sits at `:688`. Nothing here is verified about the report's coherence warning, which is an argument rather than a claim about the tree |
| CC-4 | During L-BFGS the `λ` values are frozen and no clipping applies | `[REPO]` → REPO-DER | `AR:698`, `:768` | `sed -n '698p;768,769p' <AR>`; `grep -n 'clamp_min' pinn/loss_catalog.py` | `:698` `- During L-BFGS: $\lambda$ values are frozen; no dual updates inside a`; `:768` `**Adam-only scope.** No gradient clipping is applied during L-BFGS`; `:769` `refinement; the line-search trust region already bounds the step.`; `pinn/loss_catalog.py:339` `    weights = torch.exp(torch.clamp_min(exponent, floor))` | CONFIRMED-NARROWER | Content and line resolve at both cited anchors. The `λ`-freeze half is confirmed outright. "No clipping applies" is confirmed only for **gradient** clipping — `:768` scopes its own statement that way — and neither cited line reaches the **causal-exponent** clip, which is applied unconditionally wherever the causal loss is computed, including inside an L-BFGS closure |
| CC-5 | `run.guards.loss_explosion_ceiling` is `1e11` in the retained run's configuration | `[REPO]` → REPO-DER | `CFG:28` | `sed -n '28p' <CFG>` | `    loss_explosion_ceiling: 100000000000.0` | CONFIRMED | The configuration writes the value in full decimal form where the report writes `1e11`; the two are the same number and the difference is notational. The report cites the key rather than a line, so content resolution applies and the line is recorded here for the next reader |
| CC-6 | At the retained log's median `R̄₁ = 2.527×10¹⁰` and `N_t = 16`, GATE-04's conditions require `η_c < 2.30×10⁻¹⁰`, `η_c < 2.74×10⁻¹¹` (one front step) and `η_c < 1.83×10⁻¹²` (full front) | `[OWN]` over `[REPO]` inputs → ANA + REPO-DER | `OB:396`-`:398`; `LOG`; `pinn/loss_catalog.py:97`; `pinn/training/controllers.py:692-694` | `python3 -c "import math; R=2.527e10; print(87.33654/(15*R), math.log(2)/R, math.log(2)/(15*R))"` | `2.3040902255639097e-10 2.7429647034426012e-11 1.828643135628401e-12` | CONFIRMED | All three round to the report's `2.30×10⁻¹⁰`, `2.74×10⁻¹¹` and `1.83×10⁻¹²`. The input `R̄₁` is not taken from the report: it is re-derived at R-13 as `16 × median(loss_phys)` over the retained log's 502 records |
| CC-7 | The requirement `S3` is measured against is 9.64 decades (clamp, 15-term prefix), 8.46 decades on `F-03`'s single-residual statement, and 10.56 decades for front-advance | `[OWN]` over `[REPO]` inputs → ANA + REPO-DER | `OB:99`-`:101`; `LOG`; `pinn/loss_catalog.py:97` | `python3 -c "import math; R=2.527e10; print(math.log10(15*R/87.33654), math.log10(R/87.33654), math.log10(R/math.log(2)))"` | `9.637500518435756 8.461409259380074 10.561779780874776` | CONFIRMED | All three round to the report's `9.64`, `8.46` and `10.56`. Recorded because the third is easy to mis-derive: the front-advance requirement is set by the **single** leading residual against `ln 2`, not by the 15-term prefix; using the prefix gives 11.74 decades and would not reproduce the report's figure |

### AWKWARD-COMMANDS — commands recorded outside a table cell

Two commands carry backtick and pipe characters that a markdown cell cannot hold without
the escaping convention distorting them, so they are recorded here verbatim, following
the convention `54-INTAKE.md` used for the same reason. `<REQ>` is
`.planning/REQUIREMENTS.md`.

```
grep -noE 'pinn_architecture\.md:[0-9]+' <REQ> | LC_ALL=C sort -u
grep -noE '`:[0-9]+`' <REQ> | LC_ALL=C sort -u
```

Outputs, verbatim: the first prints `90:pinn_architecture.md:424` and nothing else; the
second prints two lines, both on line 95, carrying `:433` and `:440`. Together these are
the whole of `.planning/REQUIREMENTS.md`'s spec-anchor surface, and they are what `PC-8d`
is measured against.

## VERDICT-COUNTS — the verdicts this pass assigned

**Counted from the ledger, not asserted.** The table below is produced by parsing every
ledger row's identifier and verdict cell, splitting cells on unescaped pipes only, so a
row whose command cell contains an escaped pipe is not silently mis-columned.

**Rows this task was partitioned to handle (`P-A`), one row in exactly one bucket.** A
split verdict is a bucket of its own, named in full, so that no count has to be read as
standing for half a row.

| Verdict, or the split combination as the cell carries it | `P-A` rows |
|---|---|
| `CONFIRMED` | 36 |
| `CONFIRMED-NARROWER` | 6 |
| `CONFIRMED-SHARPER` | 5 |
| `UNSUPPORTED` | 3 |
| `REFUTED` | 0 |
| `NOT-VERIFIABLE-HERE` as a row's sole verdict | 0 |
| `CONFIRMED (repo) · NOT-VERIFIABLE-HERE (published)` | 3 |
| `CONFIRMED (repo) · NOT-VERIFIABLE-HERE (analytic)` | 1 |
| `CONFIRMED (exact invariance) · NOT-VERIFIABLE-HERE (bit-identity)` | 1 |
| `CONFIRMED-NARROWER (locus and scope) · NOT-VERIFIABLE-HERE (the capacity attribution)` | 1 |
| **Total** | **56** |

**56 is exactly the count `P-A` was declared to hold**, so every row this task was given
carries a verdict and none was left behind.

**Verdict occurrences across the whole 73-row ledger**, counting each half of a split row
once. This is the table a later plan should quote when it needs a per-class total; the
one above is scoped to this task's partition.

| Verdict | Occurrences |
|---|---|
| `CONFIRMED` | 43 |
| `CONFIRMED-SHARPER` | 5 |
| `CONFIRMED-NARROWER` | 7 |
| `REFUTED` | 0 |
| `UNSUPPORTED` | 3 |
| `NOT-VERIFIABLE-HERE` | 21 |
| **Total occurrences** | **79** |

73 rows, six of which carry two verdicts, gives 79 occurrences — the reconciliation is
stated rather than left for a reader to notice. **No claim was refuted.** That is
recorded as a finding, not as an absence: three rows are `UNSUPPORTED`, which is the
adjacent and distinct result, and each of the three has its own section below.

**21 rows carry `NOT-VERIFIABLE-HERE` in one position or both**, and each of the 21 is
routed in the register below: `R-01`, `R-02`, `R-03`, `R-04`, `R-05`, `R-09`, `R-10`,
`R-14`, `PC-1e`, `PC-1f`, `PC-5c`, `PC-6c`, `PC-7a`, `PC-9c`, `D-1a`, `D-2a`, `D-3a`,
`D-4a`, `D-5a`, `D-6a`, `D-7a`.

## CITATION-COVERAGE — every distinct repository citation lands in a ledger row

Extraction ran the three commands `54-INTAKE.md` records for the citable-path set,
against the open-book report alone, and the abbreviated forms were resolved to full paths
using the intake record's own resolution table. Reduction to a set ran under `LC_ALL=C`.

```
grep -oE '(\.planning|pinn|pinn_instruction|docs|reference-code|simulation_data|tests|runs)(/[A-Za-z0-9._@+-]+)+\.(md|py|yaml|yml|jsonl|json|txt)' <OB> | LC_ALL=C sort -u
grep -oE '`[^`]*`' <OB> | tr -d '`' | grep -oE '(^|[^/A-Za-z0-9._-])([A-Za-z0-9._@+-]+\.(md|py|yaml|yml|jsonl|json))' | sed -E 's/^[^A-Za-z0-9._-]//' | LC_ALL=C sort -u
grep -oE '`?\.\.\.[/A-Za-z0-9._@+-]+`?' <OB> | tr -d '`' | LC_ALL=C sort -u
```

Raw yields: 11 full-path tokens, 10 backticked bare filenames, 6 elided paths. After
resolution and set reduction: **18 distinct repository paths**.

| # | Distinct cited path | Covering ledger row(s) |
|---|---|---|
| 1 | `.planning/REQUIREMENTS.md` | PC-1f, PC-8d, CC-2 |
| 2 | `.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/evidence/attempts/stage0-rerun-seed41-attempt-02/logs/train.log.jsonl` | R-07, R-09, R-13, PC-3c, PC-6a, PC-8e, D-4b, CC-6, CC-7 |
| 3 | `.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/evidence/attempts/stage0-rerun-seed41-attempt-02/config.yaml` | PC-7c, CC-1, CC-5 |
| 4 | `pinn/constants.py` | D-3b, D-5b |
| 5 | `pinn/loss_catalog.py` | R-07, PC-3b, PC-5a, PC-8f, D-1b, D-6b, D-7b, CC-6, CC-7 |
| 6 | `pinn/network.py` | PC-1c, PC-1d, PC-9b, D-5b |
| 7 | `pinn/training/collocation_sampler.py` | PC-5b, D-2b |
| 8 | `pinn/training/controllers.py` | R-08, PC-5a, PC-5b, PC-7b, PC-8f, PC-9d, D-1b, D-2b, CC-6 |
| 9 | `pinn/training/guards.py` | R-08, PC-7c, D-2b |
| 10 | `pinn/training/tb_sink.py` | PC-7b |
| 11 | `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` | R-01, R-12, PC-1f, PC-2b, PC-4a, PC-8c, PC-8d, PC-8f, D-3b, D-5b, CC-3, CC-4 |
| 12 | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` | CC-1 |
| 13 | `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md` | R-11, PC-1a, PC-1b, PC-1f, PC-2a, PC-8g, D-4b |
| 14 | `reference-code/reference_NNs/PINA-master/pina/solver/physics_informed_solver/causal_pinn.py` | R-01, R-02, PC-4b, PC-5d, D-6c |
| 15 | `pinn_instruction/markdown_conversion/framework-specs/integrity-r1/specs/pinn_architecture.md` | PC-2b |
| 16 | `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/specs/pinn_architecture.md` | PC-2b |
| 17 | `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/specs/pinn_architecture.md` | PC-2b |
| 18 | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/specs/pinn_architecture.md` | PC-2b |

**Distinct citations: 18. Citations appearing in no ledger row: 0.**

Three further repository objects are cited by the report in **non-path form** — "the
bundle", "the round prompt", "r2 Q3 §(b) reading 1", "the audit". They are not produced
by a path extraction and therefore did not enter the citable-path set. They are named
here so the record is complete, and their identity is established under
*Coverage boundary* above:
`pinn_instruction/markdown_conversion/framework-specs/trainex-r3/specs/framework-specs-bundle.md`
(PC-8a, PC-8b),
`pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-AGENT-PROMPT.md`
(PC-2a),
`pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_results/trainex-r2-research-report.md`
(PC-9a), and
`docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md`
(PC-8g, PC-9d), the last of which **is** in the certified set, entered there through the
closed-book report's own path citation.

## PER-CLAIM SECTIONS — every row whose verdict is not a plain `CONFIRMED`

Twenty rows. Each is laid out in the worked example's two-sided form: **what the record
says**, then **what the claim says**, then **the verdict**. Rows are ordered as the
source report orders them. A plain `CONFIRMED` row stays in the ledger with its command
and output and earns no section; these twenty are the rows a later reader has to reason
about.

### R-01 — the source method's identity, split across the tree and the literature

**What the record says.** `reference-code/reference_NNs/PINA-master/pina/solver/physics_informed_solver/causal_pinn.py:55`–`:59` carries, inside a `.. seealso::` block, "**Original reference**: Wang, Sifan, Shyam Sankaran, and Paris Perdikaris. *Respecting causality for training physics-informed neural networks.* Computer Methods in Applied Mechanics and Engineering 421 (2024):116813.", with the DOI on `:60`. `pinn_architecture.md:435` carries `w_n = \exp\left(-\eta_c \sum_{m=1}^{n-1} \operatorname{stopgrad}(\bar R_m)\right),`.

**What the claim says.** That this is the source method, and that §3.2's formula is its Eq. 3.2 and the Expert's-Guide Eq. 2.11 **term for term**.

**Verdict.** `CONFIRMED (repo) · NOT-VERIFIABLE-HERE (published)`. What the repository settles is that this repository names that paper as the source of the causal weighting, and that `AR:435` carries an exponential of a negative exclusive prefix sum of stop-gradiented residuals. What it cannot settle is the term-for-term correspondence with two published equations, because neither equation is in the tree. The split is recorded rather than collapsed: a single `CONFIRMED` here would let a reader take the published half as checked when only the in-repository half was.

### R-02 — the calibration procedure, split the same way

**What the record says.** `PINA:76` is `        eps=100,` — the vendored implementation's default.

**What the claim says.** Three values from three authorities: the annealing sequence `{10⁻²…10²}` with the advance criterion `min_i w_i > δ = 0.99`; the Expert's-Guide default `ε = 1.0`; and PINA's `eps = 100`.

**Verdict.** `CONFIRMED (repo) · NOT-VERIFIABLE-HERE (published)`. Only the third of the three has an in-repository locus and it resolves exactly, by content and at the cited line. The annealing sequence, the `δ = 0.99` criterion and the Expert's-Guide default are statements about published Algorithm 1 and are routed. The row is worth reading carefully because the report's own conclusion — that the three authorities disagree by four decades — rests on all three, and this pass has checked one.

### R-03 — the prefix-sum domain, split between the paper and the code

**What the record says.** `pinn/loss_catalog.py:329`–`:333` detaches `rbar`, takes `torch.cumsum` over `dim=0` and shifts right by one to form an exclusive prefix; `:342` is `    loss = (weights * rbar).mean()`. `pinn/training/controllers.py:651` is `        residual = accel - force` over a tensor the code's own comment at `:653` describes as shape `(N_t, 3 bodies, 3 Cartesian components)`, and `:656` reduces it with `sum(dim=(-2, -1)) / 3.0` — one `R̄` entry per collocation time.

**What the claim says.** That the source's prefix sum runs over `M` temporal segments with the residual averaged within each, and that this project's runs over individual collocation points.

**Verdict.** `CONFIRMED (repo) · NOT-VERIFIABLE-HERE (published)`. The project side is confirmed at the construction site rather than inferred from the name `rbar`: the leading axis of `residual` is the collocation-time index, and the reduction collapses only the body and component axes, so the prefix sum's length is the collocation count. The source side is a statement about two papers and is routed.

### R-06 — the 3.24-decade window rests partly on a stipulated edge

**What the record says.** `python3 -c "import math; print(math.log10(87.33654/0.05), math.log10(2.527e10/1e-4))"` prints `3.2422259782038214 14.402605241919915`. The upper edge `87.33654` is `ln` of the smallest normal binary32 and is the value `pinn/loss_catalog.py:97` computes; the traversal's start `2.527×10¹⁰` is re-derived from the primary log at `R-13`; its end `10⁻⁴` is `ε_phys`, confirmed at `CC-1` in both `ctl_instruction.md` and the retained run's configuration.

**What the claim says.** That a fixed `η_c` on unnormalized `R̄` has a 3.24-decade informative window against a 14.4-decade traversal.

**Verdict.** `CONFIRMED-NARROWER`. Both numbers re-derive to the digits printed. The narrower reading: **the 14.4-decade traversal is fully repository-grounded** — both of its endpoints are re-derived here — whereas **the 3.24-decade window is not**, because its lower edge `0.05` is a threshold the report stipulates and no repository fact fixes. The report's own confidence cell concedes exactly this ("only the window's soft lower edge (0.05) is a judgement call"). Moving that edge moves the window: at `0.5` it is 2.24 decades, at `0.005` it is 4.24. The claim is therefore confirmed as arithmetic and narrower as evidence.

### R-08 — instantaneous normalization stops `front_idx` responding to magnitude, not to shape

**What the record says.** `pinn/training/controllers.py:692`–`:694` defines `front_idx` as `max([n for n, w in enumerate(w_n_list) if w > 0.5], default=-1)`. `pinn/training/guards.py:586`–`:591` advances `last_advance_step` only when `front_idx` exceeds the running `front_high_water`, and `:600`–`:602` trip invariant B when the age of that mark exceeds `front_advance_window_n` and the mark is not saturated.

**What the claim says.** That instantaneous normalization makes `front_idx` unable to advance.

**Verdict.** `CONFIRMED-NARROWER`. Under a batch statistic the weight vector is exactly invariant to the residual's overall **magnitude**, so `front_idx` stops responding to the descent — that much is a closed-form identity and it is what makes the claim consequential. It does **not** follow that `front_idx` is constant: it remains a function of the per-step residual **shape**, which the per-step re-draw recorded at `D-2b` changes every step. The narrower statement the evidence supports is that `front_idx` would cease to track progress, not that it could never take a larger value. That distinction matters downstream because invariant B trips on a **high-water mark**, and a mark can be advanced by noise in the shape while carrying no information about the descent.

### R-09 — the input decade count is a fact of the log; the output decade count is not

**What the record says.** Over all 502 records of the retained log, `median(grad_norm_raw_phys / grad_norm_raw_data) = 6321884391035.326`, i.e. `12.800846549587316` decades. `12.800846549587316 − log₁₀(1/5.9×10⁻¹¹) = 2.5716985612294607`.

**What the claim says.** That residual-wide normalization moves the phys/data raw-gradient ratio from 12.80 decades to about 2.57.

**Verdict.** `CONFIRMED (repo) · NOT-VERIFIABLE-HERE (analytic)`. The 12.80-decade input is a fact of the primary artifact, computed over the whole retained record, and is confirmed. The 2.57-decade output divides by `R_ref`, a quantity produced by the report's clean-room model and not by anything in this tree, so it is routed. What is additionally confirmed is the arithmetic's internal consistency with the report's own `1/R_ref ≈ 5.9×10⁻¹¹`: the subtraction reproduces `2.5717` exactly. Consistency of an arithmetic step is not evidence for its input, and the row says so.

### R-12 — the bundle is byte-faithful, not merely length-consistent

**What the record says.** Pairing each of the ten `BEGIN VERBATIM <path>:<s>-<t>` markers in the bundle with its `END VERBATIM`, stripping the one wrapper blank line on each side, and comparing the remaining lines against `open(<path>).split('\n')[s-1:t]` gives `VERBATIM-MATCH 10/10`. Body lengths 77, 58, 20, 111, 53, 67, 67, 46, 109 and 90 equal the claimed spans in every case. Separately, the eight spec anchors the master cites — `AR:181`, `:429`, `:435`, `:445`, `:454`, `:461`, `:668-671`, `:692` — each resolve by content and at the cited line in the live 1098-line file.

**What the claim says.** That all 10 bundle excerpts and all cited spec anchors resolve correctly in the live tree.

**Verdict.** `CONFIRMED-SHARPER`. The stronger statement the evidence supports: the excerpts are not merely *consistent* with their sources, they are **identical line for line** across all ten — six drawn from `pinn_architecture.md` and four from `ctl_instruction.md` — and the wrapper is exactly one blank line on each side in every block. The report itself compared three boundary pairs; the remaining seven were checked here and also match.

### PC-1d — LayerNorm's scale-invariance is exact only in the `eps → 0` limit

**What the record says.** `pinn/network.py:117`–`:118` constructs `nn.LayerNorm(width, eps=layernorm_eps, elementwise_affine=layernorm_elementwise_affine)`; `pinn/architecture_spec.py:65`–`:66` fix those to `False` and `1e-5`. `:122` is `        return self.siren(x_prev) + self.layernorm(x_prev) ** self.power_p`; `:177`–`:179` place an `_OddSkipBlock` at every odd `layer_num`, and `architecture_spec.py:61` fixes `hidden_depth = 12`, `:67` fixes `power_p = 2`.

**What the claim says.** That layer 1 of the hidden stack is an odd SQR block, so the first operation applied to `h₁` is `LayerNorm(h₁)²`, and that LayerNorm is positively scale-invariant.

**Verdict.** `CONFIRMED-NARROWER`. The structural half re-derives and is in fact stronger than claimed — the stack holds exactly six odd SQR blocks and `power_p = 2` is a locked field, not an assumption. The narrowing is in the second clause. LayerNorm as implemented computes `(x − μ)/√(σ² + eps)`; scaling `x` by `c > 0` gives `c(x − μ)/√(c²σ² + eps)`, which equals `LN(x)` **only when `eps = 0`**. With `eps = 1e-5` the invariance is accurate to the extent that `c²σ² ≫ eps` and fails as the pre-activation scale collapses. What this reaches: the mechanism `PC-1` uses to break the `ω₀⁴` law is real, and it is an approximate invariance rather than the exact identity the wording asserts. What it does not reach: nothing here bears on the measured `ω₀` exponent, which is a clean-room result routed at `PC-1e`.

### PC-1f — the locus and the scope resolve; the capacity attribution does not

**What the record says.** `pinn_architecture.md:204` opens `## 2.3 The Power-Enhanced SkipResNet (SQR-SkipResNet) Formulation`; its last content line is `:260` and `## 2.4` opens at `:262`, so the cited `:204-261` spans the section exactly. `.planning/REQUIREMENTS.md:118` states SCOPE-33 as authorizing "only the items in `52-VER-20-ROUTING-HANDOFF.md` (a)–(e), plus the `n_col`/`N_t` disposition coupled to item (e) per SPEC-06", an enumeration that does not reach §2.3. `RESEARCH-CONTEXT-MASTER.md:311` records the stack under §7 and says in its own words that "Whether the stack constitutes a surface of its own is not settled by anything in this package."

**What the claim says.** That the capacity the package attributes to the SIREN initialization scale **lives in** §2.3's power-skip stack, which is not an authorized surface and is recorded only as an unsurfaced gap.

**Verdict.** `CONFIRMED-NARROWER (locus and scope) · NOT-VERIFIABLE-HERE (the capacity attribution)`. Three of the four assertions re-derive exactly — the section's extent, SCOPE-33's silence about it, and the master's own characterisation of it as unsurfaced. The narrowing on the locus is small and recorded for precision: the cited range's last content line is `:260`, with `:261` blank. The fourth assertion — that the capacity *lives* there — rests entirely on the clean-room depth sweep at `R-05` and is routed. This is the split most worth keeping visible, because it is the one a downstream reader is likeliest to compress into "verified".

### PC-3b — the floor actually used is not `math.log(tiny)`

**What the record says.** `pinn/loss_catalog.py:97` is `    mathematical_floor = math.log(torch.finfo(dtype).tiny)`, and `:339` is `    weights = torch.exp(torch.clamp_min(exponent, floor))`. Between them, `:98`–`:101` represent that bound in the active dtype and device, `:102`–`:107` advance it exactly once with `torch.nextafter` toward `+inf` when the representation fell below the mathematical value, and `:108` computes `min_weight` as `exp` of the advanced floor. Re-derived: `log(2⁻¹²⁶) = −87.3365447505531`; its binary32 representation is `−87.3365478515625`, which is below it, so one `nextafter` step gives `−87.33654022216797`; `exp` of that, rounded to binary32, is `1.175499675756452e-38`. The retained log's `w_min` is `1.1754998158862984e-38`.

**What the claim says.** That `:97` sets the floor and `:339` clamps to it, so the observed `w_min` is the clamp.

**Verdict.** `CONFIRMED-SHARPER`. Both cited lines carry exactly the attributed content. The stronger statement: the floor actually applied is the **dtype-rounded, `nextafter`-advanced** value, not `math.log(tiny)` itself — and the logged `w_min` equals `exp` of that floor to within **one** binary32 ulp, the gap being the difference between evaluating `exp` in double and rounding versus evaluating it natively in single. That pins the observed value to the clamp far more tightly than the claim does, and it identifies the one place the two could differ.

### PC-3e — the 15/16 result does not need the clean-room vector

**What the record says.** `2.527e10 / 708.396 = 35672138.182598434`. The retained log gives `w_mean = 0.0625` exactly on all 502 records, which is `1/16`, and `w_max = 1.0` with `w_min = 1.1754998158862984e-38`; those three together say 15 of the 16 weights sit at the binary32 clamp. `16 × median(loss_phys) = 25267107840.0` re-derives `R̄₁ ≈ 2.527×10¹⁰` from `loss = (weights * rbar).mean()` at `loss_catalog.py:342` with `w₁ = 1` and the rest at the floor.

**What the claim says.** That the clean-room weight vector at `η_c = 1` is still 15/16 floored under the float64 floor.

**Verdict.** `CONFIRMED-SHARPER`. The stronger statement: **the conclusion holds on repository evidence and needs no re-implementation at all.** At the project's own retained residual scale the exponent at `n = 2` is already `−η_c R̄₁ ≈ −2.527×10¹⁰`, which is below the float64 floor `−708.396` by a factor of `3.567×10⁷`, and every later exponent is more negative still. So 15 of 16 weights are floored under float64 for the run this project actually retained, not merely for a model of it.

### PC-4a — the source is cited nowhere in the specification, not merely nowhere in its reference list

**What the record says.** `pinn_architecture.md:1017` is `## References`; the numbered entries occupy `:1019`–`:1035` and there are 17 of them, with `# 10. Numerical Acceptance Checks` opening at `:1037`. A case-insensitive search of the References block for `causal`, `causality`, `wang`, `perdikaris`, `sankaran`, `116813` and `2203.07404` returns **0** matches; the same search over the whole 1098-line file for the author surnames, the article number, the arXiv identifier and the title phrase also returns **0** — `NEGATIVE-SEARCH-EMPTY` in both cases.

**What the claim says.** That the reference list carries 17 entries and none cites a source for §3.2's causal weighting.

**Verdict.** `CONFIRMED-SHARPER`. The heading, the entry range and the count all resolve exactly. The stronger statement: the source is cited **nowhere in the specification**, not merely nowhere in its reference list. Both searches are scoped and both empty results are printed with an explicit marker, because an empty result and a mistyped pattern are indistinguishable in silence.

### PC-5b — the re-draw is real; the cited line is not where it happens

**What the record says.** `pinn/training/collocation_sampler.py:87` is `        points = rng.uniform(0.0, T_CHARACTERISTIC_TIME, size=n)`, with `:82` defaulting `n` to `self.collocation_count`. `pinn/training/controllers.py:602`–`:603` re-draw whenever the caller passes `None`; `:607` sorts. The three call sites are `:803` (validation, `None`), `:1081` (the Adam training loop, `None`) and `:1308` (L-BFGS). `:1307` is `        fixed_collocation_times = self._collocation_sampler.uniform()` — a single draw held for the whole L-BFGS segment.

**What the claim says.** That 16 i.i.d. uniform draws are re-taken every step, citing `collocation_sampler.py:87`, `controllers.py:1307`, and the sort at `:607`.

**Verdict.** `UNSUPPORTED`. Two of the three cited lines resolve as cited. The third does not: `controllers.py:1307` is the L-BFGS draw, taken **once** and held fixed — the opposite of "re-drawn every step". The substance is nevertheless true of the Adam loop, and lives at `:602`–`:603` reached through `:1081`. This is `UNSUPPORTED` rather than `REFUTED` because the claim is true elsewhere and the row says where. What the finding reaches: the per-step re-draw holds for Adam and **not** for L-BFGS, which is a distinction the claim as worded erases and which bears directly on `D-2b`'s consequence about `front_idx` not being a persistent state. What it does not reach: nothing in `PC-5`'s structural argument about prefix-sum length depends on it. Separately, the numeral **16** is fixed at no cited line at all; it is the sampler's configured `collocation_count`, corroborated in-repository by `.planning/REQUIREMENTS.md:95` and by `pinn/train.py:1033`, and evidenced by the retained log's `w_mean = 0.0625 = 1/16`.

### PC-5d — the vendored implementation chunks by time level, not by fixed equal segments

**What the record says.** `PINA:187` is `    def _split_tensor_into_chunks(self, tensor):`; `:202`–`:205` sort by time, take `time_tensor.unique(return_counts=True)` and split on those counts. The physics-loss path at `:127`–`:147` appends **one** `loss_val` per chunk, stacks them, and passes the stack to `_compute_weights`, whose body at `:216`–`:219` is an inclusive `cumsum` scaled by `eps` and exponentiated.

**What the claim says.** That the in-repo reference implementation does *exactly* what the source does — one residual per chunk, weights over the chunk vector.

**Verdict.** `CONFIRMED-NARROWER`. Both cited anchors resolve by content and at the line, and the contrast the finding rests on survives intact: the vendored implementation forms one residual per **time level**, never one per collocation point. The narrowing is in "exactly that". The finding offers two source descriptions — Eq. 2.13's residual averaged over the points at a time level, and the Expert's Guide's `M` **fixed equal sequential segments** — and these are not the same construction. `PINA` chunks on the distinct time values *present in the sampled batch*, which realizes the first and not the second. What this reaches: any argument that reads `PINA` as evidence for fixed equal bins is reading more than the code carries. What it does not reach: the separation of prefix-sum length from collocation budget, which holds under either description.

### PC-7a — exact invariance is confirmed; bit-identity is a different claim

**What the record says.** For any `c > 0`, `(cR̄_m)/mean(cR̄) = R̄_m/mean(R̄)` in real arithmetic, so a batch-mean-normalized weight vector cannot respond to the residual's overall magnitude. In floating point that identity does not survive: forming `w_n = exp(−Σ_{m<n} R̄_m/mean(R̄))` on 200 random 16-point vectors and comparing IEEE bit patterns before and after a `10⁻⁸` rescaling gives `bitwise-different=155`, with a maximum deviation of `2.220e-16` — about one ulp near `w = 1`.

**What the claim says.** That the weight vector under batch-mean normalization is **bit-identical** at `R̄ ~ 10¹⁰`, `10²` and `10⁻⁴`.

**Verdict.** `CONFIRMED (exact invariance) · NOT-VERIFIABLE-HERE (bit-identity)`. The load-bearing half — exact scale-invariance, and therefore the consequence for `front_idx` — is confirmed as an elementary identity. Bit-identity does **not** follow from it and generically fails, so it is a separate claim about the report's own vector and its own float sequence, neither of which this repository carries. The demonstration above is on substitute vectors and is evidence about the *relationship between the two readings*, not about the report's vector; it is recorded that way deliberately. Nothing here suggests the report's arithmetic is wrong — only that this pass did not check it and that the stronger word cannot be inherited from the weaker one.

### PC-8b — all ten blocks, not three

**What the record says.** The comparison described at `R-12` returns `VERBATIM-MATCH 10/10`. The three pairs the finding names — `127/203`, `383/493`, `262/281` — are among them and match.

**What the claim says.** That three boundary pairs were compared line-for-line and match verbatim.

**Verdict.** `CONFIRMED-SHARPER`. The three named pairs match, and so do the other seven. The bundle is byte-faithful across every excerpt it carries. This matters beyond bookkeeping: `PC-8` is the report's negative finding, and a negative finding about bundle fidelity is only as strong as its coverage. The report's own coverage was three of ten; the coverage recorded here is ten of ten.

### PC-8d — `:167` is not cited in `.planning/REQUIREMENTS.md`

**What the record says.** `.planning/REQUIREMENTS.md` carries exactly three spec anchors: one at line 90, written out as `pinn_architecture.md:424`, and two at line 95, written as backticked bare anchors `:433` and `:440`. There is **no** occurrence of `:167` anywhere in the file. All three anchors that *are* present are stale, with the replacements the claim gives: `AR:424` now carries softening-parameter prose and the LOSS-04 contract block is at `:445`; `AR:433` is blank and the `n_col=4096` signature is at `:454`; `AR:440` carries the causal-loss formula and the "recommended: 2048-4096" line is at `:461`. The only occurrence of `:167` anywhere in the package is the master's own stale-anchor sweep at `RESEARCH-CONTEXT-MASTER.md:397`, which lists the four anchors and attributes only `:424` to `REQUIREMENTS.md:90`.

**What the claim says.** That **the four** stale anchors the master warns about are confirmed stale in `.planning/REQUIREMENTS.md`, at `REQUIREMENTS.md:90` and `:95`.

**Verdict.** `UNSUPPORTED`. The cited locations exist and do not carry what the claim attributes to them: three of the four anchors are there and every one of the three is confirmed stale, but the fourth is not in that file at all. This is `UNSUPPORTED` and not `REFUTED`, and the distinction is the whole of the row's value: the staleness of `:167 → :181` is separately **true** as a property of the specification, so nothing here says that anchor is fine. What the finding reaches: any downstream document that repairs "the four anchors in `REQUIREMENTS.md`" will find only three and must look elsewhere for the fourth. What it does not reach: `PC-8`'s other sub-findings, and in particular not the `:424 / :433 / :440` staleness that a Phase-56 amendment depends on, which is confirmed here in full.

### PC-9a — the quotation is faithful; the evidence label is not

**What the record says.** The figure `3.6e3` occurs **zero** times in each of the three attachments. It occurs once in the tree at `trainex-r2-research-report.md:635`, inside reading 1 of a list opened at `:631` with "compatible-with-evidence readings, none established:". What the package carries is the master's `H-01` row at `RESEARCH-CONTEXT-MASTER.md:289`, which names "The trainex-r2 round's Q3 interpretive content", cites `trainex-r2-research-report.md` Q3, and tiers it "agent analysis — not established fact" — without reproducing the sentence.

**What the claim says.** That the r2 report estimates the quoted sentence, labelled `[PKG]` / r2 Q3 §(b) reading 1.

**Verdict.** `CONFIRMED-NARROWER`. The quotation is faithful word for word, "reading 1" is the r2 report's own numbering, and the report's decision to stop the quotation at "per unit amplitude" is a truncation at a clause boundary rather than an alteration. The narrowing is the **evidence class**. The source report defines `[PKG]` at `claude-resolution.md:35`–`:38` as "package-derived (the three attachments)" and `[REPO]` as "repository-verified by me in the live tree"; this sentence is in none of the three attachments and was read in the tree, so by the report's own definitions its label is `[REPO]`. Why this is worth a section rather than a footnote: the four-class taxonomy `54-08` fixed makes the label decide what agreement between the two returned reports would mean, and a package-internal claim and a repository-derived claim carry different entitlements. A later plan that consumes `PC-9a` should consume it as repository-derived.

### D-2b — the same citation, and the consequence it is used for

**What the record says.** As at `PC-5b`: `collocation_sampler.py:87` draws, `controllers.py:602`–`:603` re-draw on a `None` argument, `:607` sorts, `:1081` is the Adam call site that passes `None`, and `:1307` is the L-BFGS draw held fixed for the segment. `pinn/training/guards.py:586`–`:602` define invariant B on the high-water mark of `front_idx`.

**What the claim says.** That this project takes 16 i.i.d. uniform draws re-drawn every step and sorts them, so `front_idx` is not a persistent state, yet invariant B is defined on its high-water mark.

**Verdict.** `UNSUPPORTED`, for the same reason as `PC-5b` and recorded separately because the departures row uses the citation to support a different consequence. The consequence itself — that `front_idx` indexes a different time set each step while invariant B accumulates a high-water mark across steps — is confirmed by the two loci that do resolve, `:602`–`:603` via `:1081` and `guards.py:586`–`:591`. It is the **citation** that fails, and it fails in a direction that matters: during L-BFGS the collocation set is fixed, so the "different time set each step" premise does not hold there. What this reaches: the departure `D-2` is real for the Adam phase and needs re-statement for the L-BFGS phase. What it does not reach: `D-1`, `D-3` … `D-7`, each of which is confirmed at its own locus.

### CC-4 — "no clipping applies" is scoped to gradient clipping

**What the record says.** `pinn_architecture.md:698` is `- During L-BFGS: $\lambda$ values are frozen; no dual updates inside a`. `:768`–`:769` are `**Adam-only scope.** No gradient clipping is applied during L-BFGS` / `refinement; the line-search trust region already bounds the step.` `pinn/loss_catalog.py:339` applies `torch.clamp_min(exponent, floor)` unconditionally inside the causal weight construction, with no optimizer-dependent branch anywhere in the function.

**What the claim says.** That during L-BFGS the `λ` values are frozen and no clipping applies.

**Verdict.** `CONFIRMED-NARROWER`. The `λ`-freeze half is confirmed outright at `:698`. "No clipping applies" is confirmed only for **gradient** clipping, which is how `:768` scopes its own sentence; neither cited line reaches the **causal-exponent** clip, which is applied wherever the causal loss is computed, including inside an L-BFGS closure. The narrowing matters because the report's `G-7` raises the L-BFGS interaction as an open question, and the answer differs by clip: the gradient clip is genuinely absent there, the exponent clamp is not.

## NOT-RE-DERIVABLE-HERE-REGISTER — every unchecked claim, routed

> **A `NOT-VERIFIABLE-HERE` verdict says the claim was not checked, and it says
> nothing whatever about whether the claim is true. Nothing downstream may treat an
> unchecked claim as a weak confirmation.**

That sentence is the register's whole purpose. The most common way a verification pass
leaks is by letting "we could not check this" be read as "this is probably fine", and a
routed row is a row **still owing** a verification, not a row that has quietly passed one.

**Routing is not authorization.** Naming the phase or the proposal that would settle a
claim records where the settling work belongs. It does not commission that work, does not
adopt the proposal, and does not license anyone to run it. Every row routed to a probe run
or to an owner-gated proposal below carries that reading and no other.

Twenty-one rows, matching the twenty-one ledger rows that carry `NOT-VERIFIABLE-HERE` in
one position or both. Three kinds appear and each is handled differently.

### Kind 1 — grounded in the source report's own clean-room computation

The report says so itself, and the register treats that statement as the report's own
instruction rather than as this pass's inference. `claude-resolution.md:915`–`:916`: all
`[OWN]` computation "is subject to ERW Rule 19 in-repo verification before it informs any
decision, roadmap, or spec edit". `G-6` at `:832`–`:836` repeats it per figure: "The
clean-room re-implementation matches the audit's probe within its spread, which is
corroboration, not substitution."

| Ledger row | The claim, in brief | Why no in-repo re-derivation | What would settle it | Who may authorize that |
|---|---|---|---|---|
| `R-04` | the measured `ω₀` scaling law under the locked stack | measured on a re-implementation of the spec text, not on this project's model; no in-repo locus exists to read | the characterization probe this milestone lands as committed tooling in its own phase, run as an initialization-scale sweep on this project's own architecture; the report proposes exactly this as its `X-2` | the owner, at checkpoint ②; routing is not authorization |
| `R-05` | the aggregate contribution of the power-skip stack, per block | same class; the report's own `G-4` records the aggregate as undecomposed | the same probe with depth ablated — the report's `X-2` | the owner; routing is not authorization |
| `R-09` (analytic half) | the post-normalization phys/data gradient ratio | divides by a reference scale produced by the clean-room model; the input decade count **is** confirmed from the log | the same probe emitting per-term gradient norms under the recipe — the report's `X-1` | the owner; routing is not authorization |
| `R-10` | the composed recipe satisfies the train-free gate at initialization | clean-room evaluation, not this project's code; the report's `G-6` requests precisely this re-derivation | the probe run once as a calibration pass — the report's `X-1`, which the report itself says "discharges R-10 and G-6" | the owner; routing is not authorization |
| `R-14` | a lower floor on `R̄` set by the gravitational term when the position scale collapses | a statement about a configuration no retained artifact instantiates | the probe's initialization-scale sweep — the report's `X-2` | the owner; routing is not authorization |
| `PC-1e` | the clean-room sweep table and the decade figures derived from it | same class as `R-04`/`R-05`; the audit-side half of the same comparison is separately confirmed at `PC-8g` and `CC-7` | the report's `X-2` | the owner; routing is not authorization |
| `PC-1f` (capacity half) | that the capacity **lives** in the power-skip stack | rests entirely on `R-05`'s depth sweep; the locus and scope halves are confirmed | the report's `X-2`, which it says "settles whether S3 or §2.3 is the real surface" — transcribed, not endorsed | the owner; and the scope question it raises is outside the authorized surface list, so it is doubly not this pass's to take |
| `PC-7a` (bit-identity half) | the rescaled weight vector is bit-identical, not merely equal | a claim about the report's own vector and its own float sequence, neither of which this repository carries; the exact-invariance half **is** confirmed | the report's `X-3`, which evaluates the normalization options on one stored probe residual vector | the owner; routing is not authorization |
| `PC-9c` | the clean-room depth-0 amplitude and the stack's multiplier to the measured value | clean-room model | the report's `X-2` | the owner; routing is not authorization |

**The proposals named above are transcribed, attributed, and not adopted.** They are the
source report's own owner-gated experiment proposals at `claude-resolution.md:882`–`:903`,
which the report itself introduces as "a proposal for the owner to authorize, never an
action taken here". This report proposes nothing of its own. `X-1`, `X-2` and `X-3` are
train-free as the report describes them; `X-4` involves training and the report marks it
owner-gated. Nothing here authorizes any of the four.

### Kind 2 — claims about published literature

This repository cannot settle what a published paper says. Each row records what the
report says the source says, and what a reader would follow to check it. Where the
repository carries a vendored implementation bearing on the same point, **that** is
verified separately, in-repository, with its own verdict, and the two are kept apart.

| Ledger row | The claim, in brief | What a reader would follow | The separate in-repository finding, if any |
|---|---|---|---|
| `R-01` (published half) | the formula is the source's Eq. 3.2 / Expert's-Guide Eq. 2.11 term for term | Wang, Sankaran & Perdikaris, *Computer Methods in Applied Mechanics and Engineering* **421** (2024), article 116813 (arXiv:2203.07404), Eq. 3.2; and Wang, Sankaran, Wang & Perdikaris, arXiv:2308.08468 (2023), Eq. 2.11 | `PC-4b` confirms the citation block in the vendored implementation; `PC-8c` confirms the in-repo formula at its anchor |
| `R-02` (published half) | the annealing sequence, the advance criterion, and the Expert's-Guide default | Algorithm 1 of the two cited works | the vendored default is confirmed in-repository at `R-02`'s repo half |
| `R-03` (published half) | the source's prefix sum runs over temporal segments with a within-segment average | Eq. 2.13 and Expert's-Guide Eq. 2.11 | `PC-5d` verifies the vendored implementation and records, as its own finding, that it aggregates by time level rather than by fixed equal segments |
| `PC-5c` | the same statement, restated inside the premise finding | the same two equations | `PC-5d`, kept deliberately separate: a vendored implementation is in-repository evidence and the paper is not |
| `D-1a` | source: residual averaged within `M` temporal segments | Eq. 2.13 / Eq. 2.11 | `D-1b` verifies this project's side at its own loci |
| `D-2a` | source: segments fixed and equal, spanning the domain | Expert's-Guide Eq. 2.11 | `D-2b`, whose verdict is `UNSUPPORTED` for a citation reason recorded in its own section |
| `D-3a` | source: the coefficient is annealed with a stated advance criterion | Algorithm 1 | `D-3b` verifies this project's fixed value and the absence of a schedule, by a scoped search whose scope is stated |
| `D-4a` | source: the default presumes a non-dimensionalized, order-one residual | the Expert's Guide's non-dimensionalization precondition | `D-4b` verifies this project's initialization scale from two independent in-repository supports |
| `D-5a` | source: a tanh MLP with Glorot init and an explicitly tuned feature scale | the Expert's Guide | `D-5b` verifies this project's architecture at its own loci |
| `D-6a` | source: the prefix is exclusive and the leading weight is one | Eq. 3.2 | `D-6b` verifies this project's exclusive shift; `D-6c` verifies the vendored implementation's inclusive one |
| `D-7a` | source: the weights carry a stop-gradient | Eq. 3.2 / Algorithm 1 | `D-7b` verifies this project's `detach` at its own line |

The report cites the journal article and the arXiv preprint together for the primary
source, and the practitioner restatement separately. Whether two readers reached the same
**edition** is recorded per claim rather than assumed, and this pass records that it has
checked **no** edition of either.

### Kind 3 — claims about post-initialization behaviour, or about a state a run would produce

| Ledger row | The claim, in brief | Why no in-repo re-derivation | What would settle it | Who may authorize that |
|---|---|---|---|---|
| `PC-6c` | that a recipe repairing the weight vector while leaving the physics term at its present scale would pass the train-free gate and still train on that term alone | a prediction about a run; its two arithmetic inputs are separately confirmed at `PC-6a` and `PC-6b`, and its scoping half is a reading of the package rather than of the tree | a training segment under the recipe, reporting the per-term gradient norms — which is the report's `X-4`, the one proposal it marks as involving training | the owner alone; this milestone's scope rows make such a run an owner decision, and routing is not authorization |

The report's own `G-1` states the boundary this kind sits behind: "Everything derived here
is at initialization plus closed-form arithmetic on the weight definition. No source, and
no computation in this report, establishes what any recalibrated recipe does after step 0."
That statement is transcribed, not adopted.

## CANDIDATE-GAP-ROWS-PROPOSED — proposed, not filed

Six owner-routed questions this verification pass surfaced. They are **listed here rather
than written into a register** because the routing decision belongs to the wave-4 plan,
which is where the register is authorized to change. Both gap registers and the ruling
record are byte-unchanged against `HEAD` at this plan's close, and the gate asserts it.
None of the six is adjudicated here. Each carries the STOP-protocol field schema's
required fields, with `Status` and `Resolution note` left as the wave-4 plan will find
them.

**1 — The fourth stale spec anchor is not where the round's own sweep implies it is.**
*Where in artifact:* `PC-8d`, this report; the underlying sweep at
`RESEARCH-CONTEXT-MASTER.md:397`. *Task context:* re-deriving `PC-8`'s sub-findings against
`.planning/REQUIREMENTS.md`. *Classification:* operational coordination. *Source silence:*
the master's sweep names four anchors and attributes only one of them to
`REQUIREMENTS.md:90`; the returned report attributes all four to that file and to `:95`;
neither says where the fourth is cited. *Grounding:* line anchors into a file that has
moved are exactly the artefact a later amendment resolves by, and a repair pass told to fix
"the four anchors in `REQUIREMENTS.md`" will find three and either stop or guess. The
staleness of the fourth is independently true, so the risk is a missed repair, not a wrong
one. *Agent was tempted to:* record the row as `CONFIRMED` on the strength of three of
four. *What the owner decides:* (A) the fourth anchor is tracked as a separate repair item
with its own citing file located first; (B) the claim is recorded as narrowed to the three
anchors that are cited there and no further work is opened; (C) the round is asked to
correct its own sweep. *Confidence of impact:* MEDIUM — it changes what a later amendment
pass must look for, not what any spec says. *Status:* proposed, not filed. *Resolution
note:* — .

**2 — A repository-read quotation carries a package-derived evidence label.**
*Where in artifact:* `PC-9a`, this report. *Task context:* checking the evidence-class
attribution alongside the wording, because the four-class taxonomy makes the label
load-bearing. *Classification:* process-artifact schema. *Source silence:* the report
declares its label vocabulary at `claude-resolution.md:35`–`:38` and applies `[PKG]` to a
sentence that appears in none of the three attachments; nothing in the report or the intake
record says what to do when a declared label and the evidence's actual provenance disagree.
*Grounding:* the taxonomy the intake record fixed makes agreement between the two returned
reports mean different things in different classes — corroboration in one, bundle-fidelity
evidence in another. A mislabelled row is consumed under the wrong entitlement, and the
error is invisible once the label is trusted. *Agent was tempted to:* silently re-label the
row to the class the evidence supports. *What the owner decides:* (A) the ledger records
both the declared label and the provenance, and downstream consumes the provenance — which
is what this report does pending instruction; (B) the round is asked to re-label; (C) the
divergence is recorded and the row is excluded from any cross-report agreement claim.
*Confidence of impact:* MEDIUM — it affects one row's entitlement, in a taxonomy built
precisely to stop that entitlement being assumed. *Status:* proposed, not filed.
*Resolution note:* — .

**3 — The per-step collocation re-draw does not hold in both optimizer phases.**
*Where in artifact:* `PC-5b` and `D-2b`, this report. *Task context:* resolving the cited
line against its content. *Classification:* semantic. *Source silence:* the report states
the re-draw without qualification and cites a line that is the fixed-draw path; neither the
report nor the package distinguishes the two phases. *Grounding:* the departure's stated
consequence is that the causal front indexes a different time set each step while an
invariant accumulates a high-water mark across steps. Under a **fixed** collocation set that
premise does not hold, so the consequence has to be stated per phase or it is wrong in one
of them. Whether a guard ratified against one phase's semantics carries to the other is a
question about what a later phase may rely on. *Agent was tempted to:* treat the citation as
a typo and verify the claim at the line that does carry it. *What the owner decides:* (A) the
departure is re-stated per optimizer phase before any consolidation consumes it; (B) it is
scoped to the phase the retained run characterized and the other is recorded as unexamined;
(C) it is left as the round wrote it with this row attached. *Confidence of impact:* HIGH —
it bears directly on the invariant a later phase is asked to re-ratify. *Status:* proposed,
not filed. *Resolution note:* — .

**4 — The normalization mechanism's invariance is approximate, not exact, as implemented.**
*Where in artifact:* `PC-1d`, this report. *Task context:* re-deriving the mechanism the
premise finding rests on. *Classification:* semantic. *Source silence:* the finding asserts
positive scale-invariance as a property of the operation; the implemented operation carries
a stabiliser that makes it exact only in a limit, and no source in the package addresses the
difference. *Grounding:* the invariance is the mechanism by which the finding argues a
scaling law is broken. An approximate invariance still breaks the law, so the finding's
direction survives; but "exact" and "accurate while a condition holds" are different
premises, and the condition weakens exactly where the pre-activation scale collapses —
which is the regime a neighbouring row already flags. *Agent was tempted to:* record the
row as `CONFIRMED-SHARPER` on the structural half and let the invariance clause pass.
*What the owner decides:* (A) the narrowing is recorded and carried into any consolidation
that cites the mechanism; (B) the round is asked to re-state the clause; (C) the difference
is judged immaterial and recorded as such, with a reason. *Confidence of impact:* MEDIUM —
it qualifies a mechanism rather than a conclusion. *Status:* proposed, not filed.
*Resolution note:* — .

**5 — A headline derived figure depends on an edge the source stipulates.**
*Where in artifact:* `R-06`, this report. *Task context:* re-deriving the register row the
report calls its single most important derived quantity. *Classification:* semantic.
*Source silence:* the report supplies the edge as a judgement and its own confidence cell
says so; nothing in the package fixes it, and no repository fact bears on it. *Grounding:*
one of the two numbers is bounded at both ends by quantities re-derived here from the tree;
the other is bounded at one end by a stipulation. The two therefore do not carry the same
evidential status even though the report presents them as one comparison, and the derived
width moves by a decade for each decade the stipulated edge moves. *Agent was tempted to:*
record a plain `CONFIRMED` because both arithmetic results reproduce exactly. *What the
owner decides:* (A) the figure travels with its stipulation recorded, as this report
records it; (B) the stipulation is itself routed for disposition before the figure informs
anything; (C) the figure is used only in the direction the fully-grounded number supports.
*Confidence of impact:* MEDIUM — it governs how a prominent figure may be cited, not what
any surface should be. *Status:* proposed, not filed. *Resolution note:* — .

**6 — A codification item is larger than the package's own row implies.**
*Where in artifact:* `PC-4a`, this report. *Task context:* re-deriving a negative finding
about the specification's reference list. *Classification:* operational coordination.
*Source silence:* the package records the absence as a reference-list gap; neither it nor
the report states whether the source is cited anywhere else in the specification.
*Grounding:* a scoped search over the whole specification returns nothing, so the fix is a
citation added where the mechanism is defined as well as a reference-list entry. The
difference is the difference between a bibliography edit and a section edit. *Agent was
tempted to:* record the sharpening in the ledger and leave the scope of the fix implied.
*What the owner decides:* (A) the codification item is scoped to both loci; (B) it stays a
reference-list item and the section citation is a separate question; (C) it is deferred
with the sharpening recorded. *Confidence of impact:* LOW — it widens a wording fix already
routed elsewhere. *Status:* proposed, not filed. *Resolution note:* — .

## PARTITION-EXECUTED

The executed partition is derived by the same parser that produced `VERDICT-COUNTS`,
reading each ledger row's identifier and verdict cell and splitting cells on unescaped
pipes only.

| Partition | What it covers | Declared when the ledger was built | Executed | Reconciles |
|---|---|---|---|---|
| `P-A` | rows whose class admits an in-repo re-derivation | 56 | 56 | yes |
| `P-B` | rows whose class admits none, pre-marked `NOT-VERIFIABLE-HERE` | 15 | 15 | yes |
| `P-C` | rows filled while the ledger was being built | 2 | 2 | yes |
| **Total** | the whole ledger | **73** | **73** | yes |

**No row fell between the tasks.** The declared partition and the executed one agree on
every bucket, so the set of rows left unverified is exactly the set whose class admits no
in-repo re-derivation — not the set this pass ran out of room for. No row carries the
`LEDGER-PARTIAL` marker, because the ledger is complete.

## What this half establishes

Stated as facts, each with its re-derivation recorded above, and confined to what the
verdicts support.

- **The bundle the external agents read is byte-faithful to the tree.** All ten verbatim
  excerpts are line-for-line identical to their live source ranges, six against the
  architecture specification and four against the curriculum specification, each wrapped in
  exactly one blank line. The report checked three boundary pairs; ten were checked here.
- **Every spec anchor the package cites resolves, by content and at its line, in the live
  1098-line specification** — eight anchors, each checked separately.
- **The retained run's causal fields are exactly as claimed.** Across all 502 records the
  minimum weight, the maximum, the mean and the front index are each single-valued, the
  mean is exactly one sixteenth, and the median physics term re-derives the residual scale
  every threshold in the report is measured against.
- **The clamp, not IEEE underflow, is what the run observed**, and the floor actually
  applied is the dtype-rounded, once-advanced form rather than the mathematical bound — the
  logged minimum weight matches it to within one binary32 unit in the last place.
- **The double-precision floor is not a lever, on this project's own evidence** rather than
  on a model of it: at the retained residual scale the exponent at the second collocation
  point is already seven orders of magnitude below that floor.
- **The source method is named inside this repository**, in a vendored reference
  implementation, and is cited **nowhere** in the specification — not in its reference list
  and not anywhere else in the file.
- **This project's side of every departure the report tabulates is confirmed at its own
  locus**, with one exception recorded as `UNSUPPORTED` for a citation reason, and the
  vendored implementation is confirmed to differ from this project in the one respect the
  report claims it does.
- **The report selects nothing.** All eight of its decision-sheet rows carry an empty
  owner's-pick cell, it marks its defaults as suggested, and it contains no first-person
  selection verb.
- **Three claims are `UNSUPPORTED` and none is `REFUTED`.** The three are recorded in full,
  each with its own section, and none is softened or omitted.

## What this half does not establish

- **Nothing about what should be done with any decision surface.** Verifying a claim
  *about* a surface is not the same act as disposing of that surface, and only the first is
  performed here. This report marks no default, ranks no option, reproduces no menu, and
  names no candidate value of its own.
- **No causal claim is made or implied anywhere in it.** That a quantity has a value, and
  that a departure exists, are not statements that either caused the halt this milestone is
  addressing.
- **Nothing about the twenty-one routed rows.** They are unchecked. An unchecked claim is
  unchecked.
- **Nothing about the closed-book report.** Its anchors carry a different burden, derived
  separately at intake, and no verdict in this file reaches any of them.
- **Nothing about the two reports' agreement.** Where they agree, whether that agreement is
  corroboration depends on the claim's class, and that adjudication is the next pass's.
- **Nothing about what any published source says.** Eleven rows rest on published
  literature and this pass has read no edition of any of it.

**A neutrality note, recorded rather than assumed.** The ledger reproduces the report's own
derived quantities — thresholds, decade counts, locked values already in the tree — because
those quantities *are* the objects Rule 19 obliges this pass to verify. It reproduces no
options menu, no marked default, no ranking, and no joint recipe. Where a threshold this
report re-derives happens to sit numerically near a value some menu also carries, the
ledger records the threshold as the report derives it and thereby endorses, ranks or marks
nothing.

## What remains for the second half

`54-10`, in wave 3, extends **this same file** rather than opening a second one (D-12). It
carries the closed-book report's anchor triage — the three-way provenance question derived
at `54-INTAKE.md` under `BURDEN-CLOSED-BOOK`, asking of each anchor whether it was supplied
verbatim in an attachment, reconstructed by offset from one, or has no provenance in the
attachments at all — followed by content resolution of each anchor against the pinned tree.
It then carries the cross-report independence adjudication against the four-class taxonomy.
The premise adjudication is `54-11`'s, the consolidation is `54-12`'s, and the ruling record
is the owner's at checkpoint ②.

## VERIFICATION-HYGIENE — the standing bars at close

Commands carrying Bar F or Bar G cost vocabulary are recorded in fenced blocks, matching
the convention `54-07` set and `54-08` restated, so that recording a command does not trip
the check the command defines.

| Check | Command | Output | Verdict |
|---|---|---|---|
| Bar D — canonical (`54-01-PLAN.md`), index-anchored | `git diff --stat -- pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/sampling_method.md pinn/ simulation_data/ tests/` | empty | PASS |
| Bar D — the same six pathspecs anchored to `HEAD` | `git diff HEAD --stat -- <the same six pathspecs>` | empty | PASS — recorded in addition to, never instead of, the index-anchored form, because a staged-but-uncommitted edit is invisible to the latter |
| Bar E — canonical two-path form, `HEAD`-anchored | `git diff HEAD --stat -- .planning/REQUIREMENTS.md .planning/ROADMAP.md` | empty | PASS — this plan edits neither file, so no narrowing applies and none is taken |
| Bar F — cost vocabulary over the ruling record | fenced block below | `0` | PASS — equal to the number `54-08` recorded |
| Bar G1 — no candidate value across any decision surface | fenced block below, selector `S` byte-unchanged from `54-06-PLAN.md`, file list this pass's six plan files | region cardinality `G1-REGION=0`; remainder after token strip empty | `BAR-G-CLEAN-NO-SURFACE-NAMED` |
| Bar G2 — no ordering vocabulary in the plans' own voice | fenced block below | empty | PASS |
| Bar G3 — no cost framing in the plans' own voice | fenced block below | empty | PASS |
| Bar G preprocessing sanity — fence balance and retained stream size | `grep -c '^```'` over each of the six plan files; retained line count of the shared stream | fence counts 10, 8, 8, 8, 10, 10 — all even; retained stream `4233` lines | PASS — an odd fence count would make the preprocessing swallow the rest of a file and every sub-bar would then pass vacuously |
| Check R1-w — widened round-root manifest | the fenced block in `54-08-PLAN.md`'s verification section, run verbatim | `MANIFEST-OK-W` | PASS |
| Identity proof re-run against the current tip | `git diff --stat efe8e590d6c6b2a77cc92abb0b93d625e2b92c49 HEAD -- $(cat <the citable-path block>)`; `git status --porcelain -- $(cat <the same>)`; `CPN` against shell-argument count | both empty; `CPN=21 ARGS=21`; both sentinels found | `PIN-TREE-IDENTICAL` — re-run here rather than inherited, because `HEAD` advanced past the pin after `54-08` recorded the proof |
| Anchor gap still `OPEN` in both registers | `grep -n 'Status' 54-GAPS.md \| grep -i 'OPEN'`; `grep -n 'GAP-54-01' .planning/milestones/v2.3-GAPS.md \| grep -i 'OPEN'` | `54-GAPS.md:42` carries `**Status:** OPEN`; `v2.3-GAPS.md:11` and `:15` both carry `OPEN` | PASS — both non-empty |
| Ruling record and both gap registers byte-unchanged | `git diff HEAD --stat -- 54-RULING.md 54-GAPS.md .planning/milestones/v2.3-GAPS.md` | empty | PASS — anchored to `HEAD` rather than to the index, so a staged edit cannot leave the assertion empty and passing |
| The three uploaded attachments and both returned reports untouched | `git diff HEAD --stat -- <the three attachments> <the results directory>` | empty | PASS — a claim that fails is recorded as failing here, and the report that made it stays as its author wrote it |
| No consolidated document exists | `test ! -f .../trainex-r3/trainex-r3-resolution-doc.md && echo CONSOLIDATION-ABSENT` | `CONSOLIDATION-ABSENT` | PASS |
| Manual structural read of this file, end to end | read of this report in full | No sentence in this report names a candidate value for any decision surface, reproduces any options menu, reproduces any marked default, ranks anything, or marks a surface as the one to change. Where a claim under verification contains a quantity, the quantity is recorded as the object of the check and nothing is attached to it. The four groups are presented in the source report's own order, and that order is a presentation convention with no evidential weight, stated here so it is not read as one | PASS — this file names no candidate value, marks nothing, and ranks nothing |

**Bar G verdict literal, recorded exactly as the gate prints it:**
`BAR-G-CLEAN-NO-SURFACE-NAMED`, with `G1-REGION=0`. This is not a paraphrase and not a
substitute for `BAR-G-CLEAN`. The two literals mean different things: `BAR-G-CLEAN` states
that the plan files named a decision surface and named no value for it;
`BAR-G-CLEAN-NO-SURFACE-NAMED` states that this pass's six plan files named **no decision
surface at all**, so the bar's region over them is empty. The value is unchanged from what
`54-08` recorded, which is expected — no plan file in this pass was edited by this plan,
and the retained stream is the same `4233` lines.

Bar F command (fenced):

```
grep -ciE 'faster|slower|cheaper|quicker|days|weeks|hours|effort|simpler|harder|easier|more work|less work' \
  .planning/phases/54-recalibration-decision-grounding/54-RULING.md
```

Bar G shared stream and sub-bars (fenced; defined in `54-06-PLAN.md`, selector unchanged,
file list this pass's six plan files):

```
P=.planning/phases/54-recalibration-decision-grounding
V=$(cat "$P/54-08-PLAN.md" "$P/54-09-PLAN.md" "$P/54-10-PLAN.md" \
        "$P/54-11-PLAN.md" "$P/54-12-PLAN.md" "$P/54-13-PLAN.md" \
     | awk '/^```/{f=!f; next} !f' \
     | grep -v 'planner-discipline-allow' | grep -v '<automated>')
S='eta_c|η_c|η|first_omega_0|omega_0|ω₀|n_col|N_t|collocation_count|Rbar|R̄|normaliz|reference scale|clip|clamp'
printf '%s\n' "$V" | grep -icE "$S"
printf '%s\n' "$V" | grep -iE "$S" | sed -E "s/($S)//gI" | grep -E '[0-9]'
printf '%s\n' "$V" | sed 's/`[^`]*`//g' \
  | grep -inE 'recommend|suggest|prefer|best|most likely|primary candidate|default to|should use|ranked|leading option'
printf '%s\n' "$V" | sed 's/`[^`]*`//g' \
  | grep -inE 'faster|slower|cheaper|quicker|days|weeks|hours|effort|simpler|harder|easier|more work|less work'
```

## Halt state at this half's close

Phase 54 does **not** close here. `GAP-54-01` stays `OPEN` in both registers; the ruling
record's checkpoint ② stays unfilled and byte-unchanged; Phase 56 stays closed; no
consolidated document exists. No premise is adjudicated, no menu is merged, no decision
surface is disposed of, and no entry is made in the ruling record. The second verification
half follows in wave 3 and extends this file.

---

# Part II — the closed-book engagement (`54-10`, wave 3)

**Document order, stated so it is not read as a defect.** Everything above this line is
the open-book half exactly as `54-09` wrote it; not one character of it is edited here,
so a reader can diff this file against commit `22c863ee` and see the first half
unchanged. The section *Halt state at this half's close* therefore sits in the middle of
the document: it closed the first half and it still says what it said. The whole report's
closing sections are at the end of Part II and cover both halves together.

## Why this half exists, and what it is not a finding about

`54-INTAKE.md` derives this half's obligation under `BURDEN-CLOSED-BOOK`. The runbook's
access-mode table would set a Route-A receiving-end burden of "none beyond normal channel
protocol", and that line does not fit this round: ERW Rule 1 forbids repository paths in a
closed-book upload precisely so a closed-book agent cannot cite what it cannot see, and
this round's uploads were built for an open-book round and are full of repository anchors.
The engagement that ran without repository access inherited them. So the burden is stated
rather than selected, in two steps that answer different questions — **provenance triage**
of every anchor, and **content resolution** of every anchor against the pinned tree.

**The engagement declared its own evidence base, up front, in its own words.**

- `chatgpt-resolution.md:7` — "Following your revised access instruction, this report uses
  the attachments and published literature without live repository verification."
- `chatgpt-resolution.md:13` — "No claim below is labeled repository-verified. Repository
  citations retain the original `file:line` anchors supplied by the bundles."
- `chatgpt-resolution.md:596` — gaps row 12: "Additional live implementation contradictions
  are outside this report's verification claim. Repository inspection was waived."

**Stated once, and it governs every row below: nothing in this triage is a finding about
that author's conduct.** An agent that states its own evidence base plainly in its third
paragraph has done the thing the rule exists to make possible. This triage is a finding
about what the resulting **citations can and cannot support** — because a citation of the
form `file:line` looks identical whether it was resolved against a repository or relayed
from a bundle, and a reader downstream cannot tell them apart by looking.

## Method for this half

**Path abbreviations added here.** Each binds to exactly one full path; the twelve
abbreviations `54-09` declared are unchanged and still bind.

| Abbrev. | Full path |
|---|---|
| `CB` | `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_results/chatgpt-resolution.md` |
| `EB` | `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/v2.2-closure-evidence-bundle.md` |
| `D5` | `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-DIAG-05-REDERIVATION.md` |
| `V20` | `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md` |

**The two questions every verdict answers, kept apart.** Each anchor row states, in two
separate cells, (i) whether the anchor **points at the content** — does the cited line
carry the material the report is pointing to — and (ii) whether that content **supports
the proposition** the report attaches to it. A true claim at a moved line and a wrong
claim at a right line are different findings and are never collapsed. This is the
convention the open-book half fixed, applied unchanged.

**The range test is inclusive at both ends.** An anchor citing a line at the exact first
or last line of a verbatim block is **inside** that block. `pinn_architecture.md:730` is
the exact first line of the block declared `730-796` and is inside it; an exclusive test
would have reported it untraceable, which would be false.

**Substring matching is not literal matching.** The provenance test for the relayed bucket
requires the anchor token to be followed by a character that is neither a digit nor a
hyphen. Without that boundary the string `pinn_architecture.md:730` matches inside the
block declaration `pinn_architecture.md:730-796`, and a reconstruction at a block boundary
would be misreported as a relay of a citation nobody supplied. The boundary-aware form is
the one recorded below and the one whose counts are reported.

**An anchor pointing at the first line of a multi-line object is recorded as resolving.**
Where a cited line is the header of a table, the opening line of a sentence that runs over
several lines, or the first line of a blockquote whose body carries the content, the row
records `CONFIRMED` and the note states the body's span. The alternative — marking such an
anchor unresolved — would report a defect where a reader following the citation lands
exactly where the author intended.

**Candidate values are located, never reproduced.** `54-INTAKE.md` fixed the rule that
where a report's own contracted output is a marked default or a ranked menu, this pass
counts it and locates it by line and never carries it. That rule governs Part II. A
quantity that is an option value on one of the reports' menus, a component of a marked
default, or a component of a composed recipe is **located by line and its verification
verdict recorded, and the value is not printed here**. Quantities that are diagnostic
facts about the existing tree, about the retained run, or about IEEE-754 binary32 **are**
printed, because those quantities are the objects Rule 19 obliges this pass to verify, and
because they name no candidate for any surface. This is the same neutrality note the
open-book half recorded, tightened for a report whose menus carry explicit numerals.

## ANCHOR-PROVENANCE-TRIAGE

**The anchor set is derived, not listed.** Extraction command, run over the closed-book
report and reduced to a distinct set under `LC_ALL=C`:

```
grep -oE '`[A-Za-z0-9_./-]+\.(py|md|yaml|jsonl):[0-9]+(-[0-9]+)?`' \
  pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_results/chatgpt-resolution.md \
  | tr -d '`' | LC_ALL=C sort -u
```

`ANCHOR-TOTAL=72` distinct anchors, derived by that command and re-derived independently
by this plan's gate. Every anchor is a single line; the report cites no line **ranges**.
An anchor cited several times is **one** row and its occurrence count is recorded inside
the row, per the duplication rule. Anchors are triaged in sorted order under `LC_ALL=C`.

| Cited file | Distinct anchors | Where the attachments carry that file |
|---|---|---|
| `pinn_architecture.md` | 26 | six declared-range verbatim blocks in `BU` |
| `ctl_instruction.md` | 9 | four declared-range verbatim blocks in `BU` |
| `2026-08-17-residual-frame-conformance-audit.md` | 18 | reproduced in full in `EB` |
| `RESEARCH-CONTEXT-MASTER.md` | 14 | is itself one of the three uploaded attachments |
| `52-DIAG-05-REDERIVATION.md` | 4 | reproduced in full in `EB` |
| `52-VER-20-ROUTING-HANDOFF.md` | 1 | reproduced in full in `EB` |
| **Total** | **72** | thirteen verbatim reproductions across two bundles plus the master |

**Bucket precedence, stated because an anchor can satisfy two tests.** An anchor that
appears literally in an attachment **and** falls inside a declared block range is
**relayed**: the agent was handed the citation itself, which is the stronger and earlier
provenance, and the triage assigns exactly one bucket per anchor. Every relayed row below
also records the block it falls inside, so nothing is lost by the precedence.

### The thirteen verbatim reproductions, and their fidelity to the tree

All thirteen were re-extracted from the live tree and compared **byte-for-byte** against
the bundles. Ten declare a numeric range; three declare their range by reproducing the
document in full, and for those the range is `1` to the file's line count and the offset
is fixed by the reproduction itself rather than by a numeral.

| Reproduction | Declared range | Body inside the attachment | Offset | Byte comparison against the live tree |
|---|---|---|---|---|
| `AR` block 1 in `BU` | `pinn_architecture.md:127-203` | `BU:59-135` | source `k` at `BU` line `k − 68` | identical |
| `AR` block 2 in `BU` | `pinn_architecture.md:204-261` | `BU:149-206` | source `k` at `BU` line `k − 55` | identical |
| `AR` block 3 in `BU` | `pinn_architecture.md:262-281` | `BU:220-239` | source `k` at `BU` line `k − 42` | identical |
| `AR` block 4 in `BU` | `pinn_architecture.md:383-493` | `BU:253-363` | source `k` at `BU` line `k − 130` | identical |
| `AR` block 5 in `BU` | `pinn_architecture.md:654-706` | `BU:377-429` | source `k` at `BU` line `k − 277` | identical |
| `AR` block 6 in `BU` | `pinn_architecture.md:730-796` | `BU:443-509` | source `k` at `BU` line `k − 287` | identical |
| `CT` block 1 in `BU` | `ctl_instruction.md:1600-1666` | `BU:523-589` | source `k` at `BU` line `k − 1077` | identical |
| `CT` block 2 in `BU` | `ctl_instruction.md:1742-1787` | `BU:603-648` | source `k` at `BU` line `k − 1139` | identical |
| `CT` block 3 in `BU` | `ctl_instruction.md:1788-1896` | `BU:662-770` | source `k` at `BU` line `k − 1126` | identical |
| `CT` block 4 in `BU` | `ctl_instruction.md:1922-2011` | `BU:784-873` | source `k` at `BU` line `k − 1138` | identical |
| `AUD` in `EB` | in full, so `1-221` | `EB:59-279` | source `k` at `EB` line `k + 58` | identical |
| `V20` in `EB` | in full, so `1-66` | `EB:293-358` | source `k` at `EB` line `k + 292` | identical |
| `D5` in `EB` | in full, so `1-114` | `EB:372-485` | source `k` at `EB` line `k + 371` | identical |

The comparison command, recorded outside a table cell so no escaping convention distorts
it — for the ten declared-range blocks, and then for the three full reproductions:

```
awk '/^<!-- BEGIN VERBATIM /{b=NR; p=$4} /^<!-- END VERBATIM /{print b" "NR" "p}' <BU> \
| while read beg end spec; do fp="${spec%:*}"; rng="${spec##*:}"; s="${rng%-*}"; e="${rng#*-}"
    sed -n "$((beg+2)),$((end-2))p" <BU> | diff -q - <(sed -n "${s},${e}p" "$fp"); done
sed -n '59,279p' <EB> | diff -q - <AUD>
sed -n '293,358p' <EB> | diff -q - <V20>
sed -n '372,485p' <EB> | diff -q - <D5>
```

All thirteen returned no difference. **This extends the open-book half's `R-12` finding.**
`54-09` recorded `CONFIRMED-SHARPER` there for the ten specification blocks; the three
closure-evidence reproductions were outside that row's scope and are checked here, so the
bundle set the external agents read is byte-faithful to this repository across **all
thirteen** of its verbatim reproductions, not ten. That result is recorded again, on its
own terms, under `BUNDLE-FIDELITY` below.

### Bucket 1 — relayed: the attachment carries the citation itself

`ANCHOR-RELAYED=13`. In every case the supplying attachment is the master, which cites
these loci in its own claims register and its own mechanism sections. A relayed anchor is
a citation the agent was **handed**; its accuracy is the package's responsibility rather
than the agent's, and the content column below is what establishes whether the package got
it right.

| Anchor | Occ. | Attachment supplying it literally | Also inside | What the report attaches to it | Anchor → content | Content → claim | Verdict |
|---|---|---|---|---|---|---|---|
| `2026-08-17-residual-frame-conformance-audit.md:127` | 1 | `MA:131`, `MA:269` | `EB`, full | the package's `87.34` underflow figure, Finding 5 at `CB:70` | the audit row "Point where `exp(−η_c R̄)` underflows float32 \| `R̄ > 87.34`" | supports — the audit does label `87.34` an underflow point, which is the wording Finding 5 narrows | CONFIRMED |
| `2026-08-17-residual-frame-conformance-audit.md:142` | 3 | `MA:119`, `MA:267` | `EB`, full | the six-row probe's printed columns, used at `CB:42`, `:214`, `:310` | the table's header row; the six data rows are at `AUD:144-149` | supports — the columns the arithmetic uses are declared here and the values are in the same table | CONFIRMED |
| `2026-08-17-residual-frame-conformance-audit.md:165` | 1 | `MA:125`, `MA:277` | `EB`, full | the audit's scalar LayerNorm-branch Jacobian, Finding 3 at `CB:40` | the sentence carrying "`2·LN(x)/std(x)` ≈ 3 per odd layer, six of them" | supports — the expression Finding 3 calls incomplete is exactly here | CONFIRMED |
| `2026-08-17-residual-frame-conformance-audit.md:167` | 1 | `MA:141`, `MA:278` | `EB`, full | the converged-regime inference, Finding 1 at `CB:26` | the sentence "presumes `R̄ = O(1)`, which is what a *converged* network gives (Gate B …)" | supports — the inference Finding 1 says cannot supply a normalization constant is exactly here | CONFIRMED |
| `52-DIAG-05-REDERIVATION.md:58` | 3 | `MA:39`, `MA:135`, `MA:271`, `MA:371` | `EB`, full | the halted run, at `CB:94`, `:177`, register row `CB-02` | "HALTed at step 501: `front_idx=0` on all 502 logged" | supports — and `54-09`'s `R-13` re-derived `front_idx = 0` on 502 of 502 records from the primary log | CONFIRMED |
| `pinn_architecture.md:181` | 2 | `MA:174`, `MA:275`, `MA:301` | `BU` block 1 | the fixed-and-unscheduled first frequency, at `CB:413`, `:522` | "`first_omega_0` is fixed at `30` and is not scheduled during training." | supports both uses | CONFIRMED |
| `pinn_architecture.md:274` | 1 | `MA:174` | `BU` block 3 | the locked first-frequency table entry, at `CB:383` | the Table 1 row "`first_omega_0` \| 30" | supports | CONFIRMED |
| `pinn_architecture.md:429` | 5 | `MA:280` | `BU` block 4 | the residual definition and its `1/3` factor, at `CB:120`, `:175`, `:276`, `:523`, `:558` | the displayed equation for the body-averaged squared residual | supports every one of the five uses | CONFIRMED |
| `pinn_architecture.md:435` | 3 | `MA:158`, `MA:166`, `MA:299` | `BU` block 4 | the weight formula with its detached raw prefix, at `CB:32`, `:120`, register row `CB-01` | the displayed `w_n` equation with `stopgrad` over the exclusive prefix | supports; note `w₁ = 1` follows from this formula by the empty-sum convention and is stated explicitly at `AR:445` | CONFIRMED |
| `pinn_architecture.md:445` | 3 | `MA:159`, `MA:274`, `MA:297` | `BU` block 4 | the locked exponent coefficient and the LOSS-04 label, at `CB:174`, `:557`, register row `CB-01` | the Phase-35 LOSS-04 blockquote, which states the weight formula, `w_1 = 1`, the locked coefficient value, and that windowed causal mechanics are not commissioned | supports all three uses | CONFIRMED |
| `pinn_architecture.md:454` | 2 | `MA:147`, `MA:182`, `MA:273`, `MA:303` | `BU` block 4 | the sampler's default count, at `CB:46`, `:451` | the `sample_collocation_points` signature carrying `n_col=4096` | supports | CONFIRMED |
| `pinn_architecture.md:461` | 2 | `MA:182`, `MA:303` | `BU` block 4 | the recommended count range, at `CB:46`, `:451` | the docstring line "Number of collocation points (recommended: 2048-4096)" | supports | CONFIRMED |
| `pinn_architecture.md:692` | 1 | `MA:191`, `MA:276`, `MA:305` | `BU` block 5 | the exclusion of windowed mechanics, at `CB:489` | the Phase-35 source-precedence guard, which states that Option C windowed-causal mechanics are not commissioned | supports the exclusion half; the "requiring amendment" and "authorized research family" halves rest on `V20:45` and `CT:1823`, which the report cites in the same bracket | CONFIRMED |

**All thirteen relayed anchors resolve by content.** That is a finding about the master's
accuracy, and it is recorded again under `BUNDLE-FIDELITY` rather than being allowed to
stand in for a verdict on any claim.

### Bucket 2 — reconstructed: the line number was computed from a supplied reproduction

`ANCHOR-RECONSTRUCTED=59`. A reconstructed anchor is the agent computing a line number
from an offset inside a block it was given. That is legitimate work, and it is also
exactly where an off-by-one lands **silently**, because the resulting citation is
typographically indistinguishable from one that was resolved against a repository.

**The reading applied to the two reproduction forms that carry no numeral, stated
explicitly rather than assumed.** The plan's bucket definition asks whether the anchor's
line "falls inside a range that a verbatim block in an attachment declares for that file".
Ten blocks declare their range as a numeral. Three declare it by reproducing the document
**in full** — the block's marker says so in words and the reproduction is byte-identical to
source lines `1` through the file's last line, so the block declares the range `1-N` by its
content rather than by a numeral, and the offset is fixed and checkable. The master is a
fourth case: it is not wrapped in a block because it **is** one of the three uploaded
attachments, delivered whole, so line `k` of what the agent read is line `k` of the file
and the offset is zero.

**Both readings are recorded rather than one being chosen silently**, which is the
convention `54-INTAKE.md` set at its I4 note. Under the reading applied here — a
reproduction declares a range whether it does so by numeral, by reproducing in full, or by
being the file itself — the buckets are `13 / 59 / 0`. Under a strict-literal reading that
admits only a `BEGIN VERBATIM` block bearing a numeric range, the fourteen master anchors
would fall to the third bucket and the counts would be `13 / 45 / 14`. **The reading
applied here is the one the counts below report**, and the reason it is applied is that
the third bucket's stated meaning is "the anchor's line number came from somewhere the
attachments do not account for". For a master anchor the attachments account for the line
number in the most direct way available — the file *is* the attachment — so recording
fourteen such anchors as unaccounted-for would be a false finding, and it would dilute a
bucket whose entire purpose is to concentrate attention. Nothing downstream turns on the
choice: every anchor is content-resolved below whatever its bucket, and no claim verdict in
this report depends on which of the two readings a later reader prefers.

**`AR` — `pinn_architecture.md`, from the six declared-range blocks in `BU`.**

| Anchor | Occ. | Block and declared range | Arithmetic placing the line inside | What the report attaches to it | Anchor → content | Content → claim | Verdict |
|---|---|---|---|---|---|---|---|
| `pinn_architecture.md:184` | 2 | block 1, `127-203` | `127 ≤ 184 ≤ 203`; 58th line of the block | retuning only as a stage-boundary ablation, at `CB:413`, `:557` | opens the sentence "There is no epochwise or optimizer-step `omega0` scheduler. If `first_omega_0` is ever retuned …", whose body runs to `AR:186` | supports — the clause forbidding mutation inside a run is in that sentence | CONFIRMED |
| `pinn_architecture.md:221` | 1 | block 2, `204-261` | `204 ≤ 221 ≤ 261`; 18th line | the squared LayerNorm skip branch, at `CB:383` | the SQR-SkipResNet layer equation, whose power term is written with a **generic** exponent `p` | supports "a LayerNorm skip branch raised to a power"; the claim's word *squared* needs `p = 2`, which is fixed at `AR:230` and again at `AR:257` — both inside this same supplied block, and neither cited | CONFIRMED-NARROWER |
| `pinn_architecture.md:250` | 1 | block 2, `204-261` | `204 ≤ 250 ≤ 261`; 47th line | affine-free LayerNorm, at `CB:383` | "The default contract uses `elementwise_affine=False`" | supports | CONFIRMED |
| `pinn_architecture.md:270` | 2 | block 3, `262-281` | `262 ≤ 270 ≤ 281`; 9th line | the twelve-layer depth, at `CB:383`, `:522` | the Table 1 depth row, "12 hidden layers (6 SQR-SkipResNet blocks)" | supports | CONFIRMED |
| `pinn_architecture.md:273` | 1 | block 3, `262-281` | `262 ≤ 273 ≤ 281`; 12th line | affine-free LayerNorm again, at `CB:383` | the Table 1 LayerNorm row, "elementwise_affine=False, eps=1e-5" | supports; the same row also records the stabiliser the report's own §2.3 derivation carries as `ε` | CONFIRMED |
| `pinn_architecture.md:440` | 2 | block 4, `383-493` | `383 ≤ 440 ≤ 493`; 58th line | outer averaging of the weighted residual, at `CB:120`, register row `CB-01` | the displayed equation for the causal physics loss with its `1/N_t` factor | supports | CONFIRMED |
| `pinn_architecture.md:656` | 2 | block 5, `654-706` | `654 ≤ 656 ≤ 706`; 3rd line | the separate IC term, at `CB:176`, `:558` | the total-loss assembly equation carrying the IC multiplier | supports | CONFIRMED |
| `pinn_architecture.md:665` | 2 | block 5, `654-706` | `654 ≤ 665 ≤ 706`; 12th line | the locked IC multiplier, at `CB:176`, `:528` | the line fixing the IC multiplier's default | supports | CONFIRMED |
| `pinn_architecture.md:668` | 3 | block 5, `654-706` | `654 ≤ 668 ≤ 706`; 15th line | the detached weights, the locked coefficient and the clip, at `CB:90`, `:178`, `:471` | opens the sentence fixing the coefficient default, the `stopgrad` default and the clip, whose body runs to `AR:671` | supports all three uses | CONFIRMED |
| `pinn_architecture.md:671` | 1 | block 5, `654-706` | `654 ≤ 671 ≤ 706`; 18th line | the clip's declared underflow-only purpose, at `CB:471` | "The causal exponent clip is required only to avoid underflow." | supports exactly | CONFIRMED |
| `pinn_architecture.md:681` | 1 | block 5, `654-706` | `654 ≤ 681 ≤ 706`; 28th line | the warmup schedule, at `CB:178` | the displayed warmup-length expression | supports | CONFIRMED |
| `pinn_architecture.md:683` | 2 | block 5, `654-706` | `654 ≤ 683 ≤ 706`; 30th line | the locked physics multiplier ceiling, at `CB:528`, `:558` | the line marking that ceiling `[LOCKED]` | supports | CONFIRMED |
| `pinn_architecture.md:684` | 1 | block 5, `654-706` | `654 ≤ 684 ≤ 706`; 31st line | the stage-indexed conservation weights, at `CB:528` | the piecewise schedule for the energy and angular-momentum ceilings, whose stage-0 entries are zero | supports | CONFIRMED |
| `pinn_architecture.md:690` | 2 | block 5, `654-706` | `654 ≤ 690 ≤ 706`; 37th line | automatic dominance reweighting deferred pending evidence, at `CB:330`, `:560` | the Phase-35 LOSS-02 blockquote, whose closing clause defers automatic dominance reweighting until measured weighted-loss and gradient evidence exists | supports both uses, and in the specification's own words | CONFIRMED |
| `pinn_architecture.md:698` | 3 | block 5, `654-706` | `654 ≤ 698 ≤ 706`; 45th line | multipliers frozen during L-BFGS, at `CB:90`, `:532`, gap 8 at `CB:592` | "During L-BFGS: `\lambda` values are frozen; no dual updates inside a" — the sentence closing at `AR:699` | supports all three uses | CONFIRMED |
| `pinn_architecture.md:730` | 1 | block 6, `730-796` | `730 ≤ 730 ≤ 796`; the **exact first line**, inside by the inclusive test | the two-phase optimizer protocol, at `CB:178` | the section heading "4.3 Two-Phase Optimization" | supports — the anchor names the section the departure row is about | CONFIRMED |
| `pinn_architecture.md:741` | 1 | block 6, `730-796` | `730 ≤ 741 ≤ 796`; 12th line | Adam followed by L-BFGS, at `CB:90` | the numbered item opening "**Phase 2 (Fine-Tuning):** Once the Adam optimizer has converged," | supports | CONFIRMED |
| `pinn_architecture.md:768` | 1 | block 6, `730-796` | `730 ≤ 768 ≤ 796`; 39th line | the Adam-only clipping rule, at `CB:532` | "**Adam-only scope.** No gradient clipping is applied during L-BFGS" | supports; `54-09`'s `CC-4` records that this scoping is about **gradient** clipping and not about the causal-exponent clip | CONFIRMED |

**`CT` — `ctl_instruction.md`, from the four declared-range blocks in `BU`.**

| Anchor | Occ. | Block and declared range | Arithmetic placing the line inside | What the report attaches to it | Anchor → content | Content → claim | Verdict |
|---|---|---|---|---|---|---|---|
| `ctl_instruction.md:1757` | 2 | block 2, `1742-1787` | `1742 ≤ 1757 ≤ 1787`; 16th line | the residual already living in a dimensionless frame, at `CB:276`, `:523` | the Phase-35 LOSS-01 blockquote, which states that the assembly contract keeps all terms in the same dimensionless coordinate system | supports — the distinction the report draws between lacking a numerical reference and lacking nondimensionalization is grounded here | CONFIRMED |
| `ctl_instruction.md:1815` | 3 | block 3, `1788-1896` | `1788 ≤ 1815 ≤ 1896`; 28th line | the 256-trajectory batch, at `CB:46`, `:453`, gap 6 at `CB:590` | "For a 256-trajectory training batch at curriculum stage `k`:" | supports all three uses | CONFIRMED |
| `ctl_instruction.md:1823` | 1 | block 3, `1788-1896` | `1788 ≤ 1823 ≤ 1896`; 36th line | the exclusion of windowed mechanics, at `CB:489` | the D-04 compatibility note, which states that this contract does not add windowed-causal mechanics and that the design is not commissioned | supports | CONFIRMED |
| `ctl_instruction.md:1840` | 3 | block 3, `1788-1896` | `1788 ≤ 1840 ≤ 1896`; 53rd line | the provisional/example collocation budget, at `CB:46`, `:451`, gap 6 at `CB:590` | the line closes with "The budgets `8192` data points and `4096` collocation points are **provisional/example budgets**" | supports, and in the specification's own words — the report's phrase *provisional/example budget* is verbatim | CONFIRMED |
| `ctl_instruction.md:1894` | 1 | block 3, `1788-1896` | `1788 ≤ 1894 ≤ 1896`; 107th line | the existing plateau criterion, at `CB:531` | "Hand off to L-BFGS when the physics loss plateaus:" | supports; the criterion's inequality is on the next line, which the report cites alongside | CONFIRMED |
| `ctl_instruction.md:1895` | 1 | block 3, `1788-1896` | `1788 ≤ 1895 ≤ 1896`; 108th line | the plateau inequality, at `CB:531` | the displayed slope-and-window condition | supports | CONFIRMED |
| `ctl_instruction.md:1966` | 2 | block 4, `1922-2011` | `1922 ≤ 1966 ≤ 2011`; 45th line | the provisional validation threshold the report borrows a numeral from, at `CB:252`, gap 9 at `CB:593` | the displayed validation-loss criterion with its threshold | supports | CONFIRMED |
| `ctl_instruction.md:1969` | 2 | block 4, `1922-2011` | `1922 ≤ 1969 ≤ 2011`; 48th line | that threshold's provisional standing, at `CB:252`, gap 9 at `CB:593` | "the threshold value remains provisional pending Stage-0 pilot calibration." | supports exactly | CONFIRMED |
| `ctl_instruction.md:1987` | 1 | block 4, `1922-2011` | `1922 ≤ 1987 ≤ 2011`; 66th line | the preserved boundaries, at `CB:563` | opens the HALT/REVIEW paragraph, which states that no automatic degraded advancement is authorized | supports the "advancement after failed gates" half of a three-part proposition; the held-out-evaluation half rests on `MA:381`, cited in the same bracket | CONFIRMED |

**`AUD` — the 2026-08-17 audit, reproduced in full in `EB` at offset `+58`.**

| Anchor | Occ. | Reproduction and range | Arithmetic placing the line inside | What the report attaches to it | Anchor → content | Content → claim | Verdict |
|---|---|---|---|---|---|---|---|
| `2026-08-17-residual-frame-conformance-audit.md:109` | 4 | `EB`, `1-221` | `1 ≤ 109 ≤ 221`; read at `EB:167` | what Gate B actually measured, at `CB:17`, `:94`, gap 2 at `CB:586`, register row `CB-03` | "Gate B … takes a real Brutus trajectory, forms `r' = r/D`, finite-differences …" | supports — the audit's description is of a finite-differenced stored trajectory, which is the half of Finding 1's contradiction the report attributes to the audit | CONFIRMED |
| `2026-08-17-residual-frame-conformance-audit.md:125` | 5 | `EB`, `1-221` | `1 ≤ 125 ≤ 221`; read at `EB:183` | the retained run's residual spread, at `CB:146`, `:210`, `:214`, gap 4 at `CB:588`, Finding 7 at `CB:84` | the row giving the minimum, median and maximum first residual across all 502 steps | supports every use, including the maximum the report calls a deliberately severe profile | CONFIRMED |
| `2026-08-17-residual-frame-conformance-audit.md:126` | 3 | `EB`, `1-221` | `1 ≤ 126 ≤ 221`; read at `EB:184` | the front-advance bar and its decade distance, at `CB:146`, `:177`, gap 7 at `CB:591` | the row giving the advance bar and its decade distance from the median | supports; this pass re-derives that decade figure independently below | CONFIRMED |
| `2026-08-17-residual-frame-conformance-audit.md:128` | 1 | `EB`, `1-221` | `1 ≤ 128 ≤ 221`; read at `EB:186` | the fitted decline over the full-weight segment, Finding 2 at `CB:30` | the row giving the ordinary-least-squares trend over the 402 steps at full physics weight | supports, and the report's figure matches the audit's to three decimals | CONFIRMED |
| `2026-08-17-residual-frame-conformance-audit.md:132` | 3 | `EB`, `1-221` | `1 ≤ 132 ≤ 221`; read at `EB:190` | the physics-to-data gradient-norm ratio, Finding 6 at `CB:74`, at `CB:328`, register row `CB-12` | the row giving that median ratio and its decade count | supports; `54-09`'s `R-09` re-derived the decade count from the primary log over all 502 records | CONFIRMED |
| `2026-08-17-residual-frame-conformance-audit.md:134` | 3 | `EB`, `1-221` | `1 ≤ 134 ≤ 221`; read at `EB:192` | the audit's rounding argument and its conclusion, Finding 6 at `CB:74`, gap 8 at `CB:592`, register row `CB-12` | the paragraph deriving the float32 round-to-nearest headroom and concluding the data-term gradient contributes nothing once the physics weight reaches one | supports — the conclusion Finding 6 says goes beyond the evidence is stated here in the audit's own words | CONFIRMED |
| `2026-08-17-residual-frame-conformance-audit.md:136` | 1 | `EB`, `1-221` | `1 ≤ 136 ≤ 221`; read at `EB:194` | the warmup implied by the recorded Adam budget, at `CB:529` | the sentence recording the ramp and matching it to the warmup expression evaluated on a 1000-step budget | supports exactly | CONFIRMED |
| `2026-08-17-residual-frame-conformance-audit.md:140` | 2 | `EB`, `1-221` | `1 ≤ 140 ≤ 221`; read at `EB:198` | the read-only initialization characterization, Finding 2 at `CB:30`, at `CB:94` | the sentence introducing the characterization of the locked architecture alone, evaluated at 16 sorted uniform points | supports | CONFIRMED |
| `2026-08-17-residual-frame-conformance-audit.md:147` | 1 | `EB`, `1-221` | `1 ≤ 147 ≤ 221`; read at `EB:205` | one probe row, at `CB:210` | the fourth data row of the six-row probe table | supports — this row carries the largest of the six residual medians | CONFIRMED |
| `2026-08-17-residual-frame-conformance-audit.md:148` | 1 | `EB`, `1-221` | `1 ≤ 148 ≤ 221`; read at `EB:206` | one probe row, at `CB:210` | the fifth data row of the six-row probe table | supports — this row carries the smallest of the six residual medians | CONFIRMED |
| `2026-08-17-residual-frame-conformance-audit.md:151` | 2 | `EB`, `1-221` | `1 ≤ 151 ≤ 221`; read at `EB:209` | the six cases and their aggregation, Finding 2 at `CB:30`, gap 1 at `CB:585` | "(All six rows are the probe's printed output; medians over the 16 collocation points.)" | supports both uses, including the gap's point that six medians bound nothing | CONFIRMED |
| `2026-08-17-residual-frame-conformance-audit.md:159` | 1 | `EB`, `1-221` | `1 ≤ 159 ≤ 221`; read at `EB:217` | the audit calling the 502-step median "the initialization value", Finding 7 at `CB:84` | the numbered claim whose sentence names the seed-41 run's median and calls it the initialization value | supports — the conflation Finding 7 identifies is at exactly this line | CONFIRMED |
| `2026-08-17-residual-frame-conformance-audit.md:169` | 1 | `EB`, `1-221` | `1 ≤ 169 ≤ 221`; read at `EB:227` | the "exactly one point receives gradient" wording, Finding 6 at `CB:78` | the audit's blockquote, which states that the physics gradient reaches exactly one of the sixteen collocation points | supports — the wording Finding 6 re-reads is verbatim here | CONFIRMED |
| `2026-08-17-residual-frame-conformance-audit.md:175` | 1 | `EB`, `1-221` | `1 ≤ 175 ≤ 221`; read at `EB:233` | the executed collocation count recorded as an open qualification, Finding 4 at `CB:46` | the bullet recording the hard-coded executed count against the specification's default and range | supports | CONFIRMED |

**`MA` — the master, which is itself an uploaded attachment, so the offset is zero.**

| Anchor | Occ. | Reproduction and range | Arithmetic placing the line inside | What the report attaches to it | Anchor → content | Content → claim | Verdict |
|---|---|---|---|---|---|---|---|
| `RESEARCH-CONTEXT-MASTER.md:20` | 1 | the attachment itself, `1-442` | `1 ≤ 20 ≤ 442`; offset zero | the r2 round's prohibition on recommending a remedy, at `CB:417` | the second line of the two-line quoted prohibition, whose first line is `MA:19` | supports | CONFIRMED |
| `RESEARCH-CONTEXT-MASTER.md:29` | 1 | the attachment itself, `1-442` | `1 ≤ 29 ≤ 442`; offset zero | the r2 round predating the repairs, at `CB:417` | "The vintage of that round: packaged 2026-07-24 and delivered 2026-07-25, predating the v2.2 conformance repairs" | supports exactly | CONFIRMED |
| `RESEARCH-CONTEXT-MASTER.md:90` | 2 | the attachment itself, `1-442` | `1 ≤ 90 ≤ 442`; offset zero | the master's file-count rule, at `CB:13` and Finding 7 at `CB:86` | the anchor-resolution rule, which opens "Five files named `pinn_architecture.md` exist in this repository" | supports the master's-count half; the prompt's four-copy wording is at `RESEARCH-AGENT-PROMPT.md:87`, read here as corroboration and outside the certified path set | CONFIRMED |
| `RESEARCH-CONTEXT-MASTER.md:129` | 1 | the attachment itself, `1-442` | `1 ≤ 129 ≤ 442`; offset zero | the recorded correction to the attribution, Finding 3 at `CB:38` | the correction note stating that the entry previously attributed the scale narrowly and that the attribution was widened | supports | CONFIRMED |
| `RESEARCH-CONTEXT-MASTER.md:143` | 1 | the attachment itself, `1-442` | `1 ≤ 143 ≤ 442`; offset zero | the packet's own six-row consistency check, Finding 7 at `CB:82` | the `M7` entry, which prints its six computed values against the six printed medians and claims agreement to three significant figures in all six rows | supports — the claim Finding 7 narrows is stated here in the master's own words | CONFIRMED |
| `RESEARCH-CONTEXT-MASTER.md:268` | 1 | the attachment itself, `1-442` | `1 ≤ 268 ≤ 442`; offset zero | the uncorrected register row, Finding 3 at `CB:38` | the `F-02` row, whose text still attributes the second-derivative magnitude to the first-layer frequency alone | supports — and read with `MA:129` it establishes the internal inconsistency Finding 3 asserts | CONFIRMED |
| `RESEARCH-CONTEXT-MASTER.md:278` | 1 | the attachment itself, `1-442` | `1 ≤ 278 ≤ 442`; offset zero | the transcription of the converged-regime inference, Finding 1 at `CB:26` | the `F-12` row, which transcribes the audit's converged-regime comparison scale | supports | CONFIRMED |
| `RESEARCH-CONTEXT-MASTER.md:281` | 2 | the attachment itself, `1-442` | `1 ≤ 281 ≤ 442`; offset zero | the existing dtype-resolved floor guard, Finding 5 at `CB:70` and at `CB:483` | the `F-15` row, which records the implemented clamp and its per-dtype floor resolver | supports both uses; `54-09`'s `PC-3b` confirmed the resolver in the tree and sharpened which floor is actually applied | CONFIRMED |
| `RESEARCH-CONTEXT-MASTER.md:289` | 2 | the attachment itself, `1-442` | `1 ≤ 289 ≤ 442`; offset zero | H-01 as a summary rather than a source, at `CB:417` and gap 10 at `CB:594` | the `H-01` row, which describes the r2 round's interpretive content as carried in this packet | supports | CONFIRMED |
| `RESEARCH-CONTEXT-MASTER.md:301` | 1 | the attachment itself, `1-442` | `1 ≤ 301 ≤ 442`; offset zero | the absence of measured response to other initialization scales, gap 3 at `CB:587` | the `S3` entry in the master's own "what the evidence cannot answer" section | supports | CONFIRMED |
| `RESEARCH-CONTEXT-MASTER.md:309` | 2 | the attachment itself, `1-442` | `1 ≤ 309 ≤ 442`; offset zero | evidence confined to initialization, at `CB:214` and gap 4 at `CB:588` | the cross-cutting entry stating that both the audit and the eventual probe characterize the architecture at initialization | supports both uses | CONFIRMED |
| `RESEARCH-CONTEXT-MASTER.md:311` | 1 | the attachment itself, `1-442` | `1 ≤ 311 ≤ 442`; offset zero | the undecomposed stack contribution, gap 3 at `CB:587` | the `S3`-adjacent entry recording that the stack's contribution to the same quantity is unseparated | supports | CONFIRMED |
| `RESEARCH-CONTEXT-MASTER.md:321` | 1 | the attachment itself, `1-442` | `1 ≤ 321 ≤ 442`; offset zero | the package baseline pin, at `CB:13` | the provenance entry naming the forty-character package baseline commit | supports; `54-INTAKE.md` check I3 confirmed the same value at full length in all five package files | CONFIRMED |
| `RESEARCH-CONTEXT-MASTER.md:381` | 4 | the attachment itself, `1-442` | `1 ≤ 381 ≤ 442`; offset zero | the scope boundaries, at `CB:551`, `:557`, `:563`, register row `CB-13` | the boundary attestation, whose per-scope sentences cover the single unspent held-out evaluation and the conformance-only limit on later iteration | supports all four uses | CONFIRMED |

**`D5` and `V20` — reproduced in full in `EB` at offsets `+371` and `+292`.**

| Anchor | Occ. | Reproduction and range | Arithmetic placing the line inside | What the report attaches to it | Anchor → content | Content → claim | Verdict |
|---|---|---|---|---|---|---|---|
| `52-DIAG-05-REDERIVATION.md:80` | 1 | `EB`, `1-114` | `1 ≤ 80 ≤ 114`; read at `EB:451` | the universal-IC reach of the diagnosis, Finding 2 at `CB:32` | the `H-01/H-03` row, whose text says the mechanism "applies identically to every trajectory by construction" | supports — the universal claim Finding 2 calls stronger than the sampled evidence is stated here | CONFIRMED |
| `52-DIAG-05-REDERIVATION.md:83` | 2 | `EB`, `1-114` | `1 ≤ 83 ≤ 114`; read at `EB:454` | the diagnosis describing Gate B as a trained-network result, Finding 1 at `CB:17`, register row `CB-03` | the `H-06` root-cause row, whose parenthesis reads "Phase-38 Gate B shows 0.65% relative residual error on a *trained* network against ground truth" | supports — the wording Finding 1 sets against the audit's description is verbatim here | CONFIRMED |
| `52-DIAG-05-REDERIVATION.md:84` | 1 | `EB`, `1-114` | `1 ≤ 84 ≤ 114`; read at `EB:455` | the "proven budget-independent" wording, Finding 2 at `CB:30` | the `H-07` row, whose text reads "The failure is proven budget-independent" | supports — the phrase Finding 2 quotes is verbatim here | CONFIRMED |
| `52-VER-20-ROUTING-HANDOFF.md:45` | 1 | `EB`, `1-66` | `1 ≤ 45 ≤ 66`; read at `EB:337` | the routing authority's permission for curriculum redesign, at `CB:489` | opens the sentence "It is a request to recalibrate one or more of: … or to redesign the curriculum mechanism so it does not require the two to already agree at initialization", whose body runs to `V20:49` | supports — the permission the report cites is in that sentence | CONFIRMED |

### Bucket 3 — untraceable

`ANCHOR-UNTRACEABLE=0`.

**The bucket is empty, and an empty bucket is a different finding from an omitted one**, so
it is recorded with its count rather than left out. Under the reading applied above, every
one of the seventy-two anchors the closed-book report cites has its line number accounted
for by material the attachments supplied: thirteen were handed to the agent as literal
citations and fifty-nine were computed by offset inside a reproduction the agent held. **No
anchor in this report came from anywhere the attachments do not account for.**

Because the bucket has no members it has no per-member subsections. The plan's requirement
that every untraceable anchor receive its own subsection is discharged vacuously and the
vacuity is stated here rather than left to be inferred. Under the strict-literal alternative
reading recorded above, the fourteen master anchors would fall here; all fourteen are
content-resolved in the table above and all fourteen resolve, so the alternative reading
changes no verdict and would change only which heading those rows appear under.

**`13 + 59 + 0 = 72`**, equal to the independently derived total, checked arithmetically by
this plan's gate rather than asserted.

### BUNDLE-FIDELITY

**Recorded separately from every claim verdict, and it is not one.**

| Bucket | Anchors | Resolved by content | Not resolved | What the count establishes |
|---|---|---|---|---|
| Relayed | 13 | 13 | 0 | the master's own citations of this repository are accurate at every locus the closed-book report reused |
| Reconstructed | 59 | 59 | 0 | the offset arithmetic the agent performed inside the supplied reproductions is correct in every instance |
| Untraceable | 0 | 0 | 0 | the bucket is empty; nothing to establish |
| **All** | **72** | **72** | **0** | see the paragraph below |

Verdict distribution across the seventy-two anchor rows: **71 `CONFIRMED`, 1
`CONFIRMED-NARROWER`, 0 `UNSUPPORTED`, 0 `REFUTED`.** The single narrower row is
`pinn_architecture.md:221`, where the cited line carries the skip branch with a generic
exponent and the claim's word *squared* is fixed two lines further into the same supplied
block. These seventy-two verdicts are **anchor** verdicts and are counted separately from
the claim ledger's verdicts below; they are never added into the claim counts.

**What this establishes.** Over the seventy-two anchors this report actually used, the
attachments relayed this repository accurately, and the agent's reconstruction arithmetic
inside them was correct. Together with the thirteen byte-identical reproductions recorded
above, that is a real and useful result about how this package was **constructed**, and it
is worth having on the record on its own terms: a bundle assembled by excerpting a live
tree can drift from it silently, and this one did not.

**What this emphatically is not.** It is **not** a second confirmation of any claim. That an
anchor points at the content the report says it points at establishes that the citation is
sound; whether the content **supports the proposition** is the second question, answered
per row above and per claim in the ledger below. And where the closed-book report and the
open-book report agree about a repository fact, this fidelity result is precisely the
reason the agreement must be read as evidence that the bundle relayed the tree faithfully
rather than as two readings of the tree — which is what the cross-report adjudication at
the end of Part II turns on.

### Corrections stated here, attributed to this pass

**No anchor is corrected inside the closed-book report, and the report is not edited.**
Three observations belong on the record; each is stated here, attributed to this
verification pass, and left out of the source.

1. **A figure used without an anchor, and fully traceable.** Finding 1 at `CB:19` states
   the Gate B relative error to three significant figures. The audit prints that quantity
   at full precision at `2026-08-17-residual-frame-conformance-audit.md:103` — reproduced
   at `EB:161`, consistent with the `+58` offset — and rounds it to two figures at
   `2026-08-17-residual-frame-conformance-audit.md:167`. The report used the more precise
   locus and did not cite it. Its figure is a faithful rounding of the audit's; the locus
   is recorded here so a later reader does not have to rediscover it.
2. **The home locus of a figure the report corrects.** Finding 3 at `CB:42` corrects an
   effective-frequency range. The report cites the probe table for the inputs. The range it
   corrects lives at `2026-08-17-residual-frame-conformance-audit.md:165` and is transcribed
   at `RESEARCH-CONTEXT-MASTER.md:127`; the report cites the first of those elsewhere and
   neither of them in that sentence's bracket.
3. **Where the power term is fixed.** `pinn_architecture.md:221` carries the skip branch
   with a generic exponent; the exponent is fixed at `pinn_architecture.md:230` and again
   at `pinn_architecture.md:257`. Both are inside the same supplied block, so the
   information was available to the agent; neither is cited.

## CB-LEDGER — the closed-book claim ledger

**The verdict vocabulary is the one fixed for the first half and is inherited unchanged**,
including the split convention: a claim spanning a part this repository can settle and a
part it cannot carries two verdicts separated by `·`, one for each part. No seventh
verdict is introduced here.

**The split rule for premise findings is the one the open-book ledger declared**, applied
uniformly: one sub-row per **separately checkable assertion** — an assertion with its own
evidence locus such that it could be true while a sibling is false — lettered in the order
the finding states them. Applying a different split rule to the second report would make
the cross-report comparison at the end of Part II incoherent, because a point of agreement
in one report's ledger would have no counterpart row in the other's.

**Identifiers.** The register's thirteen data rows carry the positional identifiers
`LEDGER-PREFIX-CONTRACT` assigned at intake — `CB-01` at `CB:604` through `CB-13` at
`CB:616`, in the order the rows appear, header and separator excluded. Those identifiers
are a citation convenience of this pass and never a claim about the report's own
structure: the report does not label its register rows. The premise findings carry the
report's **own** identifiers `Finding 1` … `Finding 8` and are written `CB-F1a`, `CB-F1b`,
… so the finding number is carried through unchanged and the sub-row letter is the split.
Two further sets need handles the intake contract did not assign, because it assigned
identifiers for the register only: the twelve gaps rows, which the report numbers `1.`–`12.`
itself, are written `CB-G01`–`CB-G12` carrying that number unchanged; and the answer-section
assertions extracted here are written `CB-A01` onward in the order they appear. Both use the
contract's `CB-` prefix with a letter distinguishing the set, so no identifier is ambiguous
between the three.

**The `Checked against` column, and why this ledger has one.** A verdict means something
different depending on the evidence base it was reached against, and in this half that
difference is the whole point. The column's values are a closed set:

- **the package's text** — settled against the three uploaded attachments. Fully
  settleable here, and it is where this engagement's contribution is strongest, because
  the source documents were in the attachments and repository access was never needed.
- **this repository** — settled against the pinned tree. **Every row carrying this value
  records that the report's author did not read the tree**, so the verdict is this pass's
  **first** reading of the tree for that claim and is not a second confirmation of
  anything.
- **published literature** — outside this repository's reach; recorded
  `NOT-VERIFIABLE-HERE` with the citation a reader would follow, exactly as the open-book
  half did.
- **arithmetic** — re-derived independently in this pass, with the derivation recorded.

Where a row's evidence base is mixed, the cell names both.

**Anchor provenance carried into the claim verdicts.** No claim in this ledger rests on an
anchor the triage marked untraceable or unsupported, because the triage produced none of
either. The single `CONFIRMED-NARROWER` anchor row is carried into `CB-F3b`'s note, which
is the only claim that leans on it.

### Group E — the claims-and-uncertainty register (`CB` §5, `:600`), rows `CB-01`–`CB-13`

| ID | Claim, in the source's own terms | Checked against | Cited location(s) | Check performed, and its result | Verdict | Note |
|---|---|---|---|---|---|---|
| CB-01 | The pinned formula combines a raw residual prefix, a coefficient fixed at the locked value, detached weights, and outer averaging | this repository | `AR:435`, `:440`, `:445` | `sed -n '435p;440p;445p' <AR>` — the weight equation with `stopgrad` over the exclusive prefix; the causal loss with its `1/N_t` factor; the LOSS-04 blockquote fixing the coefficient and `w_1 = 1` | CONFIRMED | Four separable elements, each at its own cited line, all present. This pass read the tree; the report did not | 
| CB-02 | The reported run halted with no front advancement across 502 logged steps | this repository | `D5:58` | `sed -n '58p' <D5>` — "HALTed at step 501: `front_idx=0` on all 502 logged" | CONFIRMED | The claim resolves at the cited line, and independently: `54-09`'s `R-13` re-derived `front_idx = 0`, single-valued across 502 of 502 records, from the primary log rather than from any attachment |
| CB-03 | Gate B is not a converged-network measurement | the package's text + this repository | `AUD:109`; `D5:83` | `sed -n '109p' <AUD>`; `sed -n '83p' <D5>` — the first describes finite-differencing a stored Brutus trajectory; the second describes a trained network against ground truth | CONFIRMED | The two supplied descriptions contradict each other, exactly as the row's confidence cell says. Which of them is right about the probe is not settled here and is not what the row claims |
| CB-04 | The first-point floor and advancement thresholds differ by a factor of 126 | arithmetic | the report's own expression at `CB:607` | re-derivation block section A — the float32 smallest-normal exponent divided by the natural log of two returns exactly 126 | CONFIRMED | Exact, and exact by construction: the normal-number boundary is 126 times the natural log of two, so the ratio is an integer identity rather than a rounded quotient |
| CB-05 | Endpoint prefixes change by 273 between 16 and 4096 equal-residual samples | arithmetic | the report's own expression at `CB:608` | re-derivation block section D — `4095 / 15 = 273` exactly | CONFIRMED | Exact for the stated flat profile. See `CB-F4b` for the three-way reading against this project's own artifacts |
| CB-06 | Fixed exponent normalization and inverse coefficient scaling are equivalent | arithmetic | the report's own expression at `CB:609` | algebraic identity: with the exponent written as coefficient times prefix over reference, multiplying the reference by any positive factor divides every exponent by that factor, so only the ratio enters the weights | CONFIRMED | Exact for the weights. The row's own limit — that this is not equivalent to normalizing the outer loss — is correct and is a different mechanical statement |
| CB-07 | Residual scale changes as the fourth power of the initialization frequency | arithmetic + this repository | `CB:610`, derived at `CB:340`–`:360` | the derivation re-checked symbolically: for a first activation periodic in a frequency-scaled affine argument, the first and second derivatives carry one and two powers of that frequency, and squaring the residual carries four — exact for a bare periodic first layer at fixed weights | CONFIRMED (bare-SIREN form) · NOT-VERIFIABLE-HERE (the locked stack) | The row's own confidence cell already scopes it as a conditional heuristic not validated for this stack. Under the locked stack the law is not established here: no in-repository measurement exists, and `54-09` routed the open-book report's contradicting clean-room measurement as `NOT-VERIFIABLE-HERE`. This is the round's scaling-law dispute; see the cross-report adjudication |
| CB-08 | The published source supplies coefficient continuation and a weight-based stopping criterion | published literature | `CB:611`, `L1` §3 and Algorithm 1 | not settleable in this repository; a reader would follow the preprint the report names at `CB:620` | NOT-VERIFIABLE-HERE | Same routing target as `54-09`'s eleven literature rows: a reader following the edition and section the report names. This pass has read no edition of it |
| CB-09 | The proposed defaults avoid both forms of initial saturation in the illustrated profiles | arithmetic + the package's text | `CB:612`, computed at `CB:194`–`:260` | re-derivation block section E, run against the report's own printed figures at those lines; every quantity in the block matches the report's figure to the digits the report prints | CONFIRMED | The values are components of the report's marked default and are located rather than reproduced here. What is confirmed is that the arithmetic is right, not that the configuration is right; the row's own limit says the actual full vectors remain unmeasured, and it is correct |
| CB-10 | The proposed defaults will train an accurate three-body predictor — no supporting outcome evidence; this report makes no such claim | the package's text + this repository | `CB:613` | structural read of the whole report, plus a search of the pinned tree for any retained artifact instantiating the proposed configuration; none exists, and the report states at `CB:537` that the combination is "not yet empirically qualified" | CONFIRMED | A row asserting its own absence of support. It is confirmed as a statement of absence: no outcome evidence exists for it in this repository and the report claims none |
| CB-11 | Growing-prefix training removes the need for residual-exponential activation at initialization | arithmetic | `CB:614`, argued at `CB:502` | with the active points' exponents identically zero the active weights are one at any finite residual — a one-line identity | CONFIRMED | Confirmed exactly as the row's own confidence cell scopes it: mechanically true for active weights set to one, with convergence and accuracy unproven. Nothing beyond that is claimed and nothing beyond that is confirmed |
| CB-12 | Severe gradient imbalance is reported, but complete data-gradient loss is proven | this repository + arithmetic | `AUD:132`, `:134` | `sed -n '132p;134p' <AUD>`; and `54-09`'s `R-09`, which re-derived the median ratio over all 502 records of the primary log | CONFIRMED (the reported imbalance) · NOT-VERIFIABLE-HERE (componentwise disappearance) | **Wording ambiguity, recorded and not resolved.** The claim cell reads as asserting that complete loss *is* proven; the confidence cell beside it says the second clause is *not* established, and the body at `CB:74`–`:76` argues at length that it is not. Both readings are recorded. On the substance: the ratio is confirmed; componentwise disappearance is unsettleable here because no retained artifact records per-component gradients |
| CB-13 | The held-out evaluation must remain owner-governed and unspent by this work | the package's text + this repository | `MA:381` | `sed -n '381p' <MA>` — the boundary attestation, whose scope sentences cover the single unspent held-out evaluation and the conformance-only limit on later iteration | CONFIRMED | Confirmed both as a reading of the master and as a description of this report's own conduct: the report proposes evaluation-free diagnostics and states at `CB:533` that its recipe contains no held-out evaluation step |

### Group F — the premise-challenge findings (`CB` §1, `:15`–`:94`), split per the rule above

| ID | Claim, in the source's own terms | Checked against | Cited location(s) | Check performed, and its result | Verdict | Note |
|---|---|---|---|---|---|---|
| CB-F1a | The operative diagnosis says Gate B measured a trained network against ground truth; the audit says it finite-differenced a stored Brutus trajectory; the descriptions contradict each other | the package's text + this repository | `D5:83`; `AUD:109` | `sed -n '83p' <D5>` returns "Phase-38 Gate B shows 0.65% relative residual error on a *trained* network against ground truth"; `sed -n '109p' <AUD>` returns "takes a real Brutus trajectory … finite-differences" | CONFIRMED | Both descriptions are in the packet, both are quoted accurately, and they are incompatible. This is the class of claim the closed-book engagement could settle without repository access, and it settled it correctly |
| CB-F1b | The reported relative error does not establish a converged residual of order one; converting a relative acceleration error into the residual requires the absolute acceleration norm | arithmetic | `CB:19`–`:26` | with the residual defined as the mean squared force-balance discrepancy over three bodies, a relative error scaling the acceleration gives a residual equal to the squared relative error times the squared acceleration norm over three — the report's expression, re-derived symbolically here and identical | CONFIRMED | The dimensional point is right: a dimensionless relative error cannot fix an absolute normalization constant without the scale it is relative to. The figure the report quotes traces to `AUD:103` — see the corrections recorded above |
| CB-F1c | The audit's converged-network inference, transcribed as `F-12`, cannot supply a normalization constant | this repository | `AUD:167`; `MA:278` | `sed -n '167p' <AUD>`; `sed -n '278p' <MA>` — the inference and its transcription, both present as described | CONFIRMED | The transcription chain the row asserts is real: the inference is the audit's and the register row carries it forward as established evidence |
| CB-F2a | The record establishes six initialization cases and a 502-step halted run, and reports a fitted decline over the full-weight segment; the diagnosis nevertheless calls failure proven budget-independent | this repository | `AUD:140`, `:151`, `:128`; `D5:84` | `sed -n '140p;151p;128p' <AUD>`; `sed -n '84p' <D5>` — six-case characterization, its six-row aggregation note, the ordinary-least-squares trend of `−0.255` decades over 402 steps, and the verbatim phrase "proven budget-independent" | CONFIRMED | Every one of the four loci carries what the finding attributes to it, including the quoted phrase |
| CB-F2b | Initialization saturation proves suppression at initialization, not permanent inability; because the first weight is one, an effective physics gradient remains | arithmetic + this repository | `AR:435` | the weight formula's exclusive prefix is empty at the first point, so the first weight is the exponential of zero; `sed -n '445p' <AR>` states the same value explicitly | CONFIRMED | The logical point is right and the arithmetic supporting it is a one-line identity. Whether a larger budget would in fact descend is not claimed and not settled |
| CB-F2c | The universal-IC claim is stronger than the sampled evidence | this repository | `D5:80` | `sed -n '80p' <D5>` — the row's text states the mechanism "applies identically to every trajectory by construction" | CONFIRMED | The universal wording the finding characterizes is present at the cited line. Whether the construction argument in fact generalizes is a separate question the finding does not decide and neither does this row |
| CB-F2d | Initial suppression is not by itself contrary to the published causal-PINN method, whose illustrated weights initially vanish except at the beginning | published literature | `CB:34`, `L1` §3 | not settleable in this repository; a reader would follow the preprint section the report names | NOT-VERIFIABLE-HERE | Routed. The claim is about a figure and a passage in a published paper, and this pass has read no edition of it |
| CB-F3a | The master's `F-02` row still attributes the derivative magnitude to the first-layer frequency alone, although the same document records that attribution as corrected | the package's text | `MA:268`; `MA:129` | `sed -n '268p;129p' <MA>` — the register row still carries the narrow wording; the correction note records that the attribution was widened to include the stack | CONFIRMED | A package-internal inconsistency between one part of the packet and another, established entirely from the attachments. `54-09` reached the same reading independently as `R-11` and `PC-1` |
| CB-F3b | The audit's scalar expression for the squared-normalization branch is not the complete Jacobian of that branch, and its second derivative also depends on Hessian terms, so multiplying six approximate scalar gains is not a quantitative prediction | arithmetic + this repository | `AUD:165`; derived at `CB:362`–`:381` | the report's Jacobian for the affine-free normalization and for its elementwise square were re-derived symbolically here and are correct, including the projection and the rank-one correction; `sed -n '165p' <AUD>` carries the scalar expression and the per-layer gain the finding calls incomplete | CONFIRMED | The mathematics is right: the branch's Jacobian is a matrix with cross-coordinate structure, and a product of six scalar gains is not that. Carries the one narrower anchor row, `pinn_architecture.md:221`, whose generic exponent is fixed elsewhere in the same supplied block |
| CB-F3c | Dividing the printed acceleration medians by the printed velocity medians gives approximately 655–993, rather than 650–900 | arithmetic + this repository | `AUD:142` | re-derivation block section M, over the six data rows at `AUD:144`–`:149`: the ratios run from `654.84` to `992.88`, which round to `655` and `993` | CONFIRMED | Exact. Three readings of this quantity are recorded side by side under `THREE-WAY-READINGS` below |
| CB-F4a | The architecture listing defaults to one count and recommends a range; the curriculum document calls the collocation budget a provisional/example budget in a section describing a 256-trajectory batch; the audit records the executed count as an open qualification | this repository | `AR:454`, `:461`; `CT:1815`, `:1840`; `AUD:175` | `sed -n '454p;461p' <AR>`; `sed -n '1815p;1840p' <CT>`; `sed -n '175p' <AUD>` — every element present, and the phrase "provisional/example budgets" is verbatim at `CT:1840` | CONFIRMED | Five separable elements at five cited lines, all resolving. The counts themselves are facts already fixed in the tree and are not candidate values of this pass's making |
| CB-F4b | The count ratio is the cardinality ratio; the last exclusive prefix changes by a different and larger factor; the exponent at the second point has one preceding term regardless of total count; and the two count units multiply to the same figure | arithmetic | `CB:50`–`:56` | re-derivation block section D — `4096 / 16 = 256` exactly, `4095 / 15 = 273` exactly, `256 × 16 = 4096` | CONFIRMED | Exact, and grounded in the packet's own definition: the master describes the prefix as **exclusive** at `MA:147`, which is precisely what makes the endpoint multiplier `273` rather than `256`. The report does not cite that line for it. Three readings recorded under `THREE-WAY-READINGS` |
| CB-F4c | Per-batch and per-trajectory readings of the count are materially different configurations, and the supplied excerpts do not settle the unit | the package's text | `CB:56`–`:58` | negative search over the two specification blocks in the bundle and over the curriculum block carrying the batch construction: no passage fixes whether the collocation budget is per batch or per trajectory. `NEGATIVE-SEARCH-EMPTY`, scope stated | CONFIRMED | Confirmed as a statement about the attachments. It is also true of the specification files themselves at the pinned tree, which is a stronger statement the finding does not make and which this row does not convert into one |
| CB-F5a | For binary32, the negative log of the smallest normal is 126 times the natural log of two | arithmetic | `CB:62`–`:66` | re-derivation block section A — the identity holds to six significant figures against the machine constant read from the IEEE-754 bit pattern | CONFIRMED | Exact. This is a property of binary32, not a choice about any decision surface, which is why it is printed here |
| CB-F5b | Subnormal values extend further, with round-to-zero further still, and device flush-to-zero behavior can change the practical boundary | arithmetic | `CB:68` | re-derivation block section A — the two further boundaries are `149` and `150` times the natural log of two, matching the report's figures to six significant figures | CONFIRMED | Both figures correct, and correct for two **different** quantities: the smallest representable subnormal, and the point below which round-to-nearest returns zero. See the cross-report adjudication, where the other report names only the first |
| CB-F5c | The package's figure is appropriate for a smallest-normal floor guard, but describing it as the point where the exponential underflows to zero is too broad | this repository + arithmetic | `AUD:127`; `MA:281` | `sed -n '127p' <AUD>` — the audit's row is headed "Point where `exp(−η_c R̄)` underflows float32"; `sed -n '281p' <MA>` records the implemented per-dtype floor resolver | CONFIRMED | The label is broader than the quantity. Three readings recorded under `THREE-WAY-READINGS`. `54-09`'s `PC-3b` independently sharpened which floor the implementation actually applies |
| CB-F5d | This terminology correction does not rescue the baseline, because the observed exponents exceed either boundary enormously | arithmetic + this repository | `CB:70`; the residual scale at `AUD:125` | the retained median first residual exceeds both boundaries by more than eight orders of magnitude, from the audit's own printed row | CONFIRMED | The finding is careful to say the correction is terminological. That care is warranted and is confirmed here |
| CB-F6a | The audit reports a median physics-to-data gradient-norm ratio and concludes that the data term contributes nothing to the accumulated float32 gradient | this repository | `AUD:132`, `:134` | `sed -n '132p;134p' <AUD>` — the ratio row and the paragraph deriving the round-to-nearest headroom and drawing that conclusion | CONFIRMED | The audit's conclusion is quoted accurately, including its scope "once `λ_phys` reaches 1" |
| CB-F6b | Floating-point addition acts componentwise, so a global norm ratio does not prove that every data-gradient component rounds away; proving complete disappearance requires componentwise evidence | arithmetic | `CB:76` | the report's counterexample re-checked: two vectors with disjoint support have a norm ratio of any magnitude and lose nothing on addition. The statement is a fact about the operation, not about this run | CONFIRMED | Correct as a statement about what the cited evidence can prove. It does not assert that the data gradient survives, and this row does not either. See the cross-report adjudication, where the two reports differ on this point |
| CB-F6c | Positive floored causal weights give mathematically nonzero contributions, so "exactly one point receives gradient" should be read as one effectively weighted point | arithmetic + this repository | `AUD:169` | `sed -n '169p' <AUD>` carries the quoted wording; and a clamped exponential is strictly positive by construction, so the floored weights multiply their residuals by a small positive number rather than by zero | CONFIRMED | The reading is right and the distinction matters downstream: a strictly positive floor and a zero are different objects for any argument about what the optimizer sees |
| CB-F7a | Squaring the printed acceleration medians and dividing by three agrees with the printed residual medians to roughly a fraction of a percent, not to three significant figures in every row | arithmetic + the package's text | `MA:143` | re-derivation block section M — the six reconstructed values differ from the printed medians by at most `0.414%`, and four of the six differ from them in the **third significant figure** | CONFIRMED | Exact, and it contradicts the packet's own `M7` entry, which claims agreement to three significant figures in all six rows while printing values that disagree at that figure in four of them. Three readings under `THREE-WAY-READINGS`; the cross-report adjudication records that the other report endorsed `M7` here |
| CB-F7b | The retained run's median covers 502 steps, so calling it the initialization value conflates two different summaries | this repository | `AUD:125`, `:159` | `sed -n '125p;159p' <AUD>` — the first prints the statistic over all 502 steps; the second calls the same number the initialization value | CONFIRMED | The conflation is real and both halves of it are at the cited lines. `54-09`'s `R-13` establishes independently that the causal fields are single-valued across all 502 records, which is why the two summaries coincide numerically even though they are different statistics |
| CB-F7c | The prompt's four-copy warning is stale relative to the master's five-copy table | the package's text | `MA:90` | `sed -n '90p' <MA>` — the master's anchor-resolution rule states five; `RESEARCH-AGENT-PROMPT.md:87` states four, read here as corroboration and recorded as outside the certified path set | CONFIRMED | Settled entirely from documents the agent held. `54-09`'s `PC-2` reached the same finding independently and additionally verified the five paths in the tree, which this engagement could not do |
| CB-F8a | The specifications combine detached causal weights with Adam followed by L-BFGS, and freeze loss multipliers during L-BFGS | this repository | `AR:668`, `:698`, `:741` | `sed -n '668p;698p;741p' <AR>` — the `stopgrad` default, the frozen-multiplier rule, and the two-phase handoff | CONFIRMED | Three separable elements at three cited lines, all present |
| CB-F8b | The supplied passages do not settle whether causal weights are recomputed inside L-BFGS line searches | the package's text | `CB:90` | negative search across the two specification blocks covering the loss contract and the optimizer sections: no passage addresses weight recomputation inside a line search. `NEGATIVE-SEARCH-EMPTY`, scope stated | CONFIRMED | Confirmed as a statement about the attachments, and the other report records the same silence independently at its `G-7` |
| CB-F8c | If weights are recomputed as functions of the trial parameters while their derivatives are detached, the supplied gradient omits the weight-derivative term and is not the derivative of the scalar objective a line search compares | arithmetic | `CB:92` | differentiating the weighted mean gives two terms, one through the residuals and one through the weights; detaching the weights suppresses the second, so the vector supplied is the gradient of a different function than the scalar being compared | CONFIRMED | The mathematics is right, and it is the standard failure mode of a detached surrogate inside a line search that assumes a consistent objective and gradient pair |
| CB-F8d | This is a conditional risk, not a verified implementation defect | the package's text | `CB:92` | the report's own scoping sentence, checked against the absence established at `CB-F8b`: with the attachments silent on the behaviour, no implementation claim is available either way | CONFIRMED | The self-scoping is accurate. A closed-book agent asserting an implementation defect here would have been asserting something it could not see, and it did not |

### Group G — the gaps section (`CB` §4, `:583`–`:596`), rows `CB-G01`–`CB-G12`

| ID | Claim, in the source's own terms | Checked against | Cited location(s) | Check performed, and its result | Verdict | Note |
|---|---|---|---|---|---|---|
| CB-G01 | Full initialization profiles are missing; six medians cannot bound all residuals or cumulative prefixes at the larger count | the package's text + this repository | `AUD:151` | `sed -n '151p' <AUD>` — the six rows are medians over sixteen collocation points; no retained artifact in the pinned tree records a full residual vector at any larger count | CONFIRMED | A median over sixteen points bounds neither the maximum nor the prefix sum of a longer draw, which is the gap's own point and is correct |
| CB-G02 | No converged-PINN absolute residual reference is established; the cited gate is a reference-trajectory consistency check and cannot fix a converged-scale normalizer | the package's text + this repository | `AUD:109` | `sed -n '109p' <AUD>` — the probe operates on a stored trajectory, so it measures the consistency of that trajectory with the force law and not the residual of a converged network | CONFIRMED | Follows directly from `CB-F1a`'s reading of the audit. The other report reaches the same conclusion by a different route at its `G-2`; see the cross-report adjudication |
| CB-G03 | There is no measured response to alternative initialization scales, and the stack's Jacobian and Hessian contributions have not been separated | the package's text | `MA:301`, `:311` | `sed -n '301p;311p' <MA>` — the master's own "what the evidence cannot answer" entries state both absences | CONFIRMED-NARROWER | True of the attachments, which is what the row's citations support. It is **not** true of the round as a whole: the other report performed a clean-room sweep across seven frequency settings and a depth ablation, which `54-09` recorded as `R-04`/`R-05` and routed `NOT-VERIFIABLE-HERE`. The narrower reading is "the attachments contain no such measurement", and under that reading it holds exactly |
| CB-G04 | The baseline has post-initialization evidence; the proposed recipe does not, and the retained record must not be confused with evidence about a redesigned curriculum | the package's text + this repository | `AUD:125`; `MA:309` | `sed -n '125p' <AUD>`; `sed -n '309p' <MA>` — the retained statistics span the run; the master's cross-cutting entry confines the available characterization to initialization | CONFIRMED | Correct, and it is the same boundary `54-09` recorded from the other side |
| CB-G05 | No finite upper bound for future residuals is established; optimization can create derivative spikes or close encounters outside the sampled cases | arithmetic + this repository | `CB:589` | no retained artifact bounds the residual over a trajectory not yet run, and none of the sampled cases constrains an unsampled one; the claim is a statement of what is absent | CONFIRMED | A correct negative claim. The report labels it as its own analysis and cites nothing, which is the right handling for a statement of absence |
| CB-G06 | Count units, computational feasibility, and complete execution constants remain unresolved | the package's text | `CT:1815`, `:1840` | `sed -n '1815p;1840p' <CT>`; plus the negative search recorded at `CB-F4c` | CONFIRMED | Consistent with `CB-F4c` and settled on the same evidence. The feasibility half is a statement about what the attachments do not establish, which is correct |
| CB-G07 | Exact runtime front aggregation and tie handling were not inspected; the derivations use the audit's threshold implication | the package's text | `AUD:126` | `sed -n '126p' <AUD>` — the advance bar the derivations use | CONFIRMED-NARROWER | True as a statement about **this report's** inspection, which is what the row asserts. It is not true that the definition is unavailable: the pinned tree defines the front index at `pinn/training/controllers.py:692-694`, re-derived by `54-09` at `R-08`. The author could not have known that, and the row is narrowed rather than contradicted because it claims only non-inspection |
| CB-G08 | Gradient disappearance and optimizer consistency remain empirical questions; the attachments do not establish the L-BFGS weight-refresh behaviour | the package's text + this repository | `AUD:134`; `AR:698` | `sed -n '134p' <AUD>`; `sed -n '698p' <AR>`; plus the negative search recorded at `CB-F8b` | CONFIRMED | Both halves hold. The second half is also true of the pinned specification files, not only of the attachments |
| CB-G09 | The proposed training-control tolerance is not validated; it borrows a provisional number while changing its aggregation and role | this repository | `CT:1966`, `:1969` | `sed -n '1966p;1969p' <CT>` — the validation criterion and the sentence marking its threshold provisional pending pilot calibration | CONFIRMED | Both cited lines carry what the gap attributes to them, and the report is explicit at `CB:252` that the borrowed numeral is a candidate rather than the existing metric |
| CB-G10 | The earlier round's finding is only summarized; a full adjudication requires its actual text | the package's text | `MA:289` | `sed -n '289p' <MA>` — the `H-01` row describes the earlier round's interpretive content as carried in this packet rather than reproducing it | CONFIRMED-NARROWER | True of the round's attachments, which is the reading the citation supports. The earlier round's report does exist in this repository, at the path `54-09` abbreviates `R2`, so "requires its actual text" is satisfiable in-tree — a fact the author could not check and which the narrowing records rather than holds against the row |
| CB-G11 | Literature transfer is not project validation: the causal formula matches the published method, but the project supplies no attribution trail | this repository + published literature | `CB:595` | `sed -n '55,60p' <PINA>` returns the full published citation — author list, title, journal, volume, article number, year and DOI — inside this repository's vendored reference implementation; and `54-09`'s `PC-4a` confirmed that the specification cites that source nowhere | CONFIRMED-NARROWER (the specification reading) · NOT-VERIFIABLE-HERE (the formula's match to the published method) | **Both readings recorded, neither resolved in the other's favour.** Read as "the specification supplies no attribution trail" the clause holds exactly and is independently sharpened by `54-09`. Read as "this repository contains no attribution for the method" the tree contradicts it at the vendored implementation, re-verified in this pass. The report's wording does not distinguish the two loci, and the author could not check either. The match to the published formula is a literature claim and is routed |
| CB-G12 | Additional live implementation contradictions are outside this report's verification claim; repository inspection was waived | the package's text | `CB:596` | the report's own access declaration at `CB:7` and `:13`, and `54-INTAKE.md`'s `RULE-16-DIVERGENCE`, which quotes all three self-declarations with their line citations | CONFIRMED | Accurate self-scoping, stated three times in the report's own text. It is the sentence that makes this whole triage possible: an agent that had not said this would have left its citations indistinguishable from resolved ones with nothing on the record to warn a reader |

### Group H — assertions in the answer sections a later plan would have to rely on

Extracted under the plan's fourth extraction rule: every assertion the report itself flags
as a correction of the package's record, plus the assertions the premise adjudication in
wave 4 will consume.

| ID | Claim, in the source's own terms | Checked against | Cited location(s) | Check performed, and its result | Verdict | Note |
|---|---|---|---|---|---|---|
| CB-A01 | The findings leave the central observation intact — a correctly scaled residual frame, very large initialization derivatives, floored later weights and a halted causal front — and remove unjustified claims about convergence scales, universal impossibility and single-parameter causation | this repository | `AUD:109`, `:140`; `D5:58` | `sed -n '109p;140p' <AUD>`; `sed -n '58p' <D5>`; and each of the three removals corresponds to a confirmed finding above — `CB-F1a`, `CB-F2a` and `CB-F3a` respectively | CONFIRMED | The closing paragraph of the findings section, and the sentence the premise adjudication will read first. Each of its three removals is grounded in a finding this ledger confirms |
| CB-A02 | Copying the published source's initial coefficient would not solve this case | arithmetic | `CB:180` | re-derivation block section K — the resulting second-point exponent, re-derived from the retained median residual, matches the report's printed figure exactly and exceeds both thresholds by many orders of magnitude | CONFIRMED | The published coefficient is a value on no menu of this round and is a fact about the source method; the resulting exponent is a derived diagnostic and is confirmed |
| CB-A03 | The reference value alone, leaving the raw coefficient and the prefix unchanged, is insufficient | arithmetic | `CB:306` | re-derivation block section F — both exponents the report prints at that line re-derive exactly | CONFIRMED | A **negative** result about a component of the report's own marked default, which is why it matters to the adjudication. The value itself is located and not reproduced here |
| CB-A04 | Dividing the recorded gradient-norm ratio by the reference gives approximately 242, but that is only arithmetic holding the old gradients and weights fixed | arithmetic + this repository | `CB:328`; `AUD:132` | re-derivation block section F — the quotient is `242.308`, matching the report's figure | CONFIRMED | Confirmed including its own disclaimer, which is the load-bearing half: the quotient is not a prediction for any run, and the report says so in the same sentence |
| CB-A05 | Near convergence the acceleration and the force must cancel, so there is no general fourth-power law for the residual | arithmetic | `CB:415` | the residual is the squared difference of two quantities that approach each other, so its scaling is governed by the difference and not by either term's own scale; the fourth-power model derived at `CB:353`–`:358` explicitly assumes acceleration dominance and the report says so | CONFIRMED | An important self-limitation, and correct. It bounds the reach of `CB-07` from the report's own side |
| CB-A06 | The derivation supports the summarized second-derivative mechanism but not exclusive attribution to the initialization frequency, and the earlier round's actual text was not attached | arithmetic + the package's text | `MA:20`, `:29`, `:289` | `sed -n '20p;29p;289p' <MA>` — the earlier round's prohibition on recommending remedies, its vintage, and the summary row | CONFIRMED-NARROWER | The mechanism half and the attribution half both hold. The "cannot be adjudicated" half is narrowed for the same reason as `CB-G10`: the earlier report exists in this repository even though it was not attached to this round |
| CB-A07 | The denominator must be the fixed sequence length; dividing each prefix by its own length would produce the same weight at every later point for a flat profile | arithmetic | `CB:439` | with a flat profile the prefix is proportional to its own length, so dividing by that length cancels it and the exponent is constant in the index — re-derived symbolically here | CONFIRMED | Exact, and it is the kind of mechanical trap that is invisible until someone writes the ratio out. Confirmed as arithmetic; it recommends nothing and this row endorses nothing |
| CB-A08 | At the batch size the curriculum document describes, the larger per-sequence count implies over a million physics points per logical batch | arithmetic + this repository | `CT:1815` | re-derivation block section D — the product is `1048576`; `sed -n '1815p' <CT>` supplies the batch size | CONFIRMED | Exact arithmetic on two figures already fixed in the tree. Feasibility is unmeasured, as the report says |
| CB-A09 | The package reports an existing per-dtype floor resolver, so this is not a proposal to repair an absent clip | this repository | `MA:281` | `sed -n '281p' <MA>`; and `54-09`'s `PC-3b` confirmed the resolver in the tree at `pinn/loss_catalog.py:97` and sharpened which floor is actually applied | CONFIRMED | Correctly scoped. A closed-book agent proposing to add a guard that already exists would have been a real hazard here, and the report checked the packet before proposing |
| CB-A10 | The routing authority expressly permits curriculum redesign that avoids requiring the two scales to agree, and the current default's exclusion of windowed mechanics is a contract requiring amendment rather than a reason to omit the family | this repository | `V20:45`; `CT:1823`; `AR:692` | `sed -n '45,49p' <V20>` carries the permission verbatim; `sed -n '1823p' <CT>` and `sed -n '692p' <AR>` both state that windowed-causal mechanics are not commissioned | CONFIRMED | All three loci resolve. This is the assertion that licenses the redesign family being on the table at all, and wave 4 will consume it |
| CB-A11 | Importing a method labelled causal or adaptive does not establish independence from initialization scale, because that method's own gate motion faces the same two thresholds | arithmetic + published literature | `CB:504`–`:512`, `L5` | the two threshold conditions the report applies to the published gate are the same normal-floor and half-magnitude conditions re-derived at section A, applied to that gate's exponent | CONFIRMED (the arithmetic) · NOT-VERIFIABLE-HERE (the published gate form) | The argument's structure is right and the arithmetic is the same identity confirmed at `CB-F5a`. Whether the published gate has the form the report writes down is a literature claim and is routed |
| CB-A12 | Execution constants not reproduced in the attachments must be inherited from the authorized run manifest, not invented | the package's text | `CB:537` | the negative search at `CB-F4c` and `CB-F8b` establishes that several such constants are absent from the attachments; the statement is a boundary the report sets on its own output | CONFIRMED | A correct and unusually disciplined self-limitation for a closed-book engagement, and it is exactly the discipline whose absence this whole triage exists to detect |
| CB-A13 | Under the log-compressed alternative the flat-profile exponent stays bounded for any finite binary32 residual, and the half-magnitude threshold is crossed below a specific residual | arithmetic | `CB:264`–`:270` | re-derivation block section H — the maximum exponent over all finite binary32 residuals matches the report's figure, and the half-magnitude boundary re-derives to `33554431`, which is exactly two to the twenty-fifth power minus one | CONFIRMED | Both figures exact, and the second is exact in a way the report does not remark on: the boundary is a power of two minus one, which follows from the compression coefficient the report chose. The coefficient is an option value on its own menu and is located rather than reproduced |

### CB-AWKWARD-COMMANDS — the re-derivation block, recorded outside a table cell

Every arithmetic row above cites a section of this script. It is recorded here rather than
in cells because it carries pipes, backticks and shell metacharacters that the empty-cell
scan would read as cell boundaries. Rewording a command to fit a cell produces a different
check, so the command is moved instead.

```
python3 - <<'PY'
import math, struct
r = 2.53e10                        # retained median first residual, AUD:125
L2 = math.log(2); B32 = 126*L2     # section A
tiny32 = struct.unpack('f', struct.pack('I', 0x00800000))[0]
maxf32 = struct.unpack('f', struct.pack('I', 0x7f7fffff))[0]
print('A', B32, 149*L2, 150*L2, B32/L2, -math.log(tiny32),
      -math.log(2.2250738585072014e-308), 708.396/B32,
      math.log10(708.396/B32), math.exp(-0.5))
print('D', 4096/16, 4095/15, 256*16, 256*4096)                  # section D
print('K', 0.01*r)                                              # section K
print('H', 0.04*math.log(1+r), (1+r)**-0.04,
      0.04*math.log(1+maxf32), math.exp(L2/0.04)-1)             # section H
rows = [(310,2.03e5,1.37e10),(331,2.72e5,2.46e10),(251,2.20e5,1.62e10),
        (281,2.79e5,2.60e10),(290,1.94e5,1.25e10),(231,2.28e5,1.74e10)]
print('M ratios', [round(a/v,2) for v,a,_ in rows])             # section M
print('M devs%', [round((a*a/3-R)/R*100,3) for v,a,R in rows])
PY
```

Sections E and F re-derive quantities that are components of the reports' marked defaults
or composed recipes. Their commands are the same shape as the block above with the
reports' own printed figures substituted from `CB:194`–`:260` and `CB:286`–`:328`; the
figures are not reproduced here, per the locate-don't-reproduce rule stated at the top of
Part II. Every quantity in both sections matched the report's printed figure to the digits
the report prints.

### THREE-WAY-READINGS — where the report re-derives a quantity this project also states

Four claims in the closed-book report re-derive a quantity that a governance or evidence
artifact of this project also states. Each was re-derived a **third** time, independently,
in this pass. All three readings are recorded side by side.

**Naming a document that would need amending is not amending it.** No amendment is
performed by this pass, none is proposed by it, and the routing of these four items is
wave 4's authority, not this report's.

| Quantity | Row | This project's reading, and where | The report's reading, and where | This pass's independent reading | Where they differ | Document that would need amending if the report's reading holds |
|---|---|---|---|---|---|---|
| The effective angular-frequency range implied by the probe's own columns | `CB-F3c` | "≈ 650–900" at `AUD:165`, transcribed as "650–900" at `MA:127` | "approximately 655–993, rather than 650–900" at `CB:42` | ratios over the six rows at `AUD:144`–`:149` run `654.84` … `992.88`, rounding to `655` and `993` | the upper end: the project's `900` understates its own printed table's `993` by about ten percent | `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:165`, and its transcription at `RESEARCH-CONTEXT-MASTER.md:127` |
| The precision to which the residual reconstructs from the acceleration column | `CB-F7a` | "agreement to three significant figures in all six rows" at `MA:143` | "roughly 0.4%, not to three significant figures in every row" at `CB:82` | maximum relative deviation `0.414%`; four of six rows differ from the printed medians at the third significant figure, using `M7`'s own printed values | the claimed precision: `M7`'s own printed values disagree at the figure `M7` claims agreement to | `RESEARCH-CONTEXT-MASTER.md:143` |
| The multiplier between the executed and specified collocation counts | `CB-F4b` | "`4096 / 16 = 256` exactly, so calibrating at one count and honoring the other moves the exponent by roughly **256×**" at `MA:147`, restated as "the 256× arithmetic" at `MA:185` | `256` is the cardinality ratio; the last exclusive prefix changes by `4095 / 15 = 273`, at `CB:50`–`:54` | `4096 / 16 = 256` exactly and `4095 / 15 = 273` exactly; under the master's **own** exclusive-prefix definition at `MA:147` the endpoint exponent is proportional to the prefix length, so `273` is the endpoint multiplier and `256` is the cardinality ratio | which quantity the figure is a ratio of; the master's hedge "roughly" makes its statement defensible as an order-of-magnitude figure and not as the endpoint multiplier | `RESEARCH-CONTEXT-MASTER.md:147` and `:185` |
| The float32 exponent boundary and what it is the boundary of | `CB-F5c` | "Point where `exp(−η_c R̄)` underflows float32 \| `R̄ > 87.34`" at `AUD:127` | the figure is the smallest-normal boundary; subnormals extend further and round-to-zero further still, at `CB:60`–`:70` | the figure is `126 ln 2`, equal to the negative log of the smallest binary32 normal to six significant figures; the subnormal extent is `149 ln 2` and the round-to-nearest zero point is `150 ln 2` | the label, not the number: the value is right for a smallest-normal guard and the phrase "underflows float32" names a boundary about sixteen exponent units further down | `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:127` |

### CB-VERDICT-COUNTS — the verdicts this half assigned

**Counted from the ledger, not asserted**, by the same escaped-pipe-aware parser the first
half used. Rows this half handled: `13 + 27 + 12 + 13 = 65`.

| Verdict, or the split combination as the cell carries it | Rows |
|---|---|
| `CONFIRMED` | 55 |
| `CONFIRMED-NARROWER` | 4 |
| `CONFIRMED-SHARPER` | 0 |
| `REFUTED` | 0 |
| `UNSUPPORTED` | 0 |
| `NOT-VERIFIABLE-HERE` as a row's sole verdict | 2 |
| `CONFIRMED (bare-SIREN form) · NOT-VERIFIABLE-HERE (the locked stack)` | 1 |
| `CONFIRMED (the reported imbalance) · NOT-VERIFIABLE-HERE (componentwise disappearance)` | 1 |
| `CONFIRMED-NARROWER (the specification reading) · NOT-VERIFIABLE-HERE (the formula's match to the published method)` | 1 |
| `CONFIRMED (the arithmetic) · NOT-VERIFIABLE-HERE (the published gate form)` | 1 |
| **Total** | **65** |

**Verdict occurrences across this half's 65 rows**, counting each half of a split row once —
four rows carry two verdicts, so `65 + 4 = 69` occurrences.

| Verdict | Occurrences |
|---|---|
| `CONFIRMED` | 58 |
| `CONFIRMED-SHARPER` | 0 |
| `CONFIRMED-NARROWER` | 5 |
| `REFUTED` | 0 |
| `UNSUPPORTED` | 0 |
| `NOT-VERIFIABLE-HERE` | 6 |
| **Total occurrences** | **69** |

**No claim in this half is refuted and none is unsupported.** That is recorded as a
finding rather than as an absence, and it is a different result from the first half, which
produced three `UNSUPPORTED` rows and no refutation. The asymmetry has a plain explanation
and it is worth stating: this report's assertions about the tree are almost entirely
assertions about **what the attachments say the tree contains**, and the attachments turned
out to be byte-faithful, so those assertions inherit the attachments' accuracy. Its own
work — the arithmetic, the terminology corrections and the package-internal contradictions
— is where its exposure was, and that work re-derives.

**Six occurrences carry `NOT-VERIFIABLE-HERE`**, and each is routed on the same terms the
first half's register set: `CB-07` (the locked stack's response to a frequency change,
which needs a measurement on this project's own model), `CB-08` and `CB-F2d` and the
literature half of `CB-A11` and of `CB-G11` (published sources this repository cannot
reach), and the componentwise half of `CB-12` (a state only an instrumented run would
produce). **Routing is not authorization**, restated here for this half.

### COMBINED-VERDICT-COUNTS — both halves together

| Verdict | Open-book half | Closed-book half | Combined |
|---|---|---|---|
| `CONFIRMED` | 43 | 58 | 101 |
| `CONFIRMED-SHARPER` | 5 | 0 | 5 |
| `CONFIRMED-NARROWER` | 7 | 5 | 12 |
| `REFUTED` | 0 | 0 | 0 |
| `UNSUPPORTED` | 3 | 0 | 3 |
| `NOT-VERIFIABLE-HERE` | 21 | 6 | 27 |
| **Total occurrences** | **79** | **69** | **148** |
| Ledger rows | 73 | 65 | 138 |

`138` rows carrying `148` verdict occurrences, because ten rows across the two halves carry
two verdicts each. The reconciliation is stated rather than left for a reader to notice.

**The seventy-two anchor verdicts are not in these totals.** They are verdicts about
citations, not about claims, and mixing them in would inflate the confirmed count by
roughly half with rows that establish nothing about any proposition. They are counted under
`BUNDLE-FIDELITY` and stay there.

## The cross-report independence adjudication

**What this section decides, and what it does not.** For every point on which both reports
say something about the same question, it records what each says in its author's own terms
and whether their agreement — where they agree — is **entitled** to be read as
corroboration. That entitlement is decided by the claim's **class**, fixed at
`54-INTAKE.md` under the four-class taxonomy, and by nothing else. It is not decided by how
convincing the agreement looks, by how many words each report spends on it, or by which
report read a tree. It says nothing whatever about whether either position is **true**.

**The classes are applied, not re-derived.** `CLASS-PACKAGE-INTERNAL`,
`CLASS-REPOSITORY-DERIVED`, `CLASS-LITERATURE` and `CLASS-ANALYTIC` are as `54-08` fixed
them, abbreviated in the cells as `PKG-INT`, `REPO-DER`, `LIT` and `ANA`.

**The entitlement is a closed pair.** Every row carries one of exactly two values and
nothing else:

- **`CORROBORATED`** — the class admits independent corroboration and both reports reached
  the point from evidence each could actually see.
- **`NOT-CORROBORATED`** — the class does not admit it. Every row in this bucket states why
  in its own text. For a repository-derived point the reason is always the same and is
  stated in the row: **the matching statement from the engagement that read no tree is
  evidence that the attachment relayed the tree faithfully, not a second reading of the
  tree.** For an analytic point both reports derived from a premise they inherited from the
  same package, the reason is that they are two evaluations of one assumption rather than
  two tests of it, and the shared premise is named.

**The disposition vocabulary is closed at four values, all four defined here:**

- **`RESOLVED-BY-EVIDENCE`** — a verdict in one of this report's two ledgers settles the
  difference. The row names the verdict.
- **`RECONCILABLE`** — the two statements are compatible once a qualifier **both reports
  state** is applied. The row names the qualifier.
- **`OPEN-DISPUTE`** — the two statements are incompatible and no verdict in this report
  settles the difference.
- **`OUT-OF-SCOPE-HERE`** — settleable only by evidence this milestone's scope rows put
  behind an owner decision. The row names what would settle it.

Where the two positions **agree**, the disposition is the entitlement's consequence and is
stated as such.

**Averaging is not available.** There is no disposition meaning "somewhere in between". A
third statement that neither author holds and that no evidence supports is not a
resolution; it is the destruction of the finding the disagreement was. And **no
disagreement is resolved in favour of the engagement that read the tree merely because it
read the tree.** Repository access settles repository questions. It settles no question of
arithmetic, no question of what a published source says, and no question of what the
package's own text says — and three of this ledger's disagreements are of exactly those
kinds, with the closed-book engagement's position the one the evidence supports in two of
them.

**Presentation order.** The open-book report is written first in every row. That is the
convention `54-INTAKE.md` adopted and it carries no evidential weight, stated here so it is
not read as carrying any.

INDEPENDENCE-LEDGER

| Point | What the open-book report says, in its own terms | What the closed-book report says, in its own terms | Claim class | Entitlement (CORROBORATED / NOT-CORROBORATED) | Disposition | Note |
|---|---|---|---|---|---|---|
| X-01 · Whether the master's own record contradicts its `F-02` row | `PC-1`, `OB:56`–`:59`: "The master's own §4.1 `M2` and `F-11` already widened the attribution to **two** factors, and amendment `A-1` records the narrow wording as a *correction* … But `F-02`'s **row text was never updated**." | Finding 3, `CB:38`: "Master F-02 still says `first_omega_0 = 30` 'sets' the derivative magnitude, although M2 explicitly corrected that attribution to include the SQR-SkipResNet stack." | `PKG-INT` | CORROBORATED | agree; the entitlement's consequence is that this is a genuine two-agent reading | Both agents read the same attachment, pinned to the same baseline, and reached the same reading of it from separate readings. This is the class the taxonomy says admits corroboration, and this row is the cleanest instance of it in the round. Confirmed independently here at `CB-F3a` and at `54-09`'s `R-11` |
| X-02 · Whether the round prompt's file-count warning matches the master's table | `PC-2`, `OB:111`: "The prompt states four; master §3's table lists **five**, and amendment `A-11` records the four → five correction explicitly." | Finding 7, `CB:86`: "The prompt's four-copy warning is also stale relative to the master's five-copy table. This is an anchor-resolution issue, not a physical contradiction." | `PKG-INT` | CORROBORATED | agree; the entitlement's consequence | Both read both documents. The open-book report additionally verified the five paths and their line counts in the tree, which is a repository-derived claim the closed-book report makes no counterpart to; that half is one-agent and is recorded as such rather than folded into this agreement |
| X-03 · What the packet says the reference gate actually measured | `OB:405` and `G-2` at `:817`: "the audit's converged-regime datum (Gate B: residual = 0.65 % of `‖a′‖` on a true trajectory, `F-12`)" and "was measured on ground-truth trajectories with a Phase-38 network" | Finding 1, `CB:17`: "The operative diagnosis says Gate B measured a **trained network** … The audit instead says it finite-differenced a **stored Brutus trajectory** … Those descriptions contradict each other." | `PKG-INT` | NOT-CORROBORATED | RESOLVED-BY-EVIDENCE — verdict `CB-F1a`, `CONFIRMED` | The positions differ and the difference resolves against the packet itself: `AUD:109` describes a finite-differenced stored trajectory and `D5:83` describes a trained network, both verbatim, both in the attachments. The closed-book report flagged the contradiction; the open-book report carried the diagnosis's side of it without flagging it. **Resolved on the packet's own text, which both agents held — not on repository access** |
| X-04 · Whether that gate can supply a converged-scale normalizer | `G-2`, `OB:817`–`:821`: "the 14.4-decade traversal is anchored at its lower end by a *target* … not by an observation" | gap 2, `CB:586`: "Gate B is a reference-trajectory consistency check. It cannot fix a converged-scale normalizer or connect a residual tolerance to trajectory error." | `ANA` | NOT-CORROBORATED | agree; the entitlement's consequence, with the shared premise named | Both reached the same conclusion, and the premise-sharing caveat applies: both inherited the single relative-error datum from `F-12` as relayed at `MA:278`, sourced from `AUD:167`. If that datum is wrong they are wrong together. Notably they reached the conclusion from **different** readings of what the gate measured — see X-03 — which is robustness, and robustness is not corroboration |
| X-05 · The float32 smallest-normal exponent boundary | `PC-3`(1), `OB:133`–`:134`: "`ln(smallest normal float32) = ln(1.175494×10⁻³⁸) = −87.33654` — the audit's figure is exactly the **normal-range** boundary, not flush-to-zero." | Finding 5, `CB:62`–`:66`: "For binary32, `−log(smallest normal) = 126 log2 = 87.33654`." | `ANA` | CORROBORATED | agree; the entitlement's consequence | The premise here is IEEE-754 binary32, not anything the package supplied, so the premise-sharing caveat does not bite: two agents computed a machine constant independently and agree to six significant figures, and this pass makes it three. The strongest corroboration in the round |
| X-06 · What lies below that boundary | `PC-3`(1), `OB:135`: "IEEE-754 flush-to-zero for float32 is at `−ln(1.401298×10⁻⁴⁵) = 103.279`." | `CB:68`: "Subnormal values extend to `149 log2 ≈ 103.279`, with round-to-zero near `150 log2 ≈ 103.972` under gradual underflow and ordinary rounding." | `ANA` | CORROBORATED | RECONCILABLE — qualifier: **which** boundary each figure names | Both derive `103.279` independently and it is the exponent of the smallest representable subnormal. The closed-book report additionally names `103.972`, the point below which round-to-nearest returns zero. The two figures are correct for two different quantities; the reports name the same one and one of them names a second. Re-derived here: `149 ln 2` and `150 ln 2` |
| X-07 · The clip's total dynamic range across the two precisions | `PC-3`(3), `OB:146`–`:147`: "The clip's entire dynamic range across the two precisions is `708.40/87.34 = 8.11×` in the exponent = **0.91 decades**." | `D5-B` at `CB:478`: "Normal-floor boundary becomes `708.396`, only `8.11` times the exponent capacity, or `0.91` decades." | `ANA` | CORROBORATED | agree; the entitlement's consequence | Same class and same reasoning as X-05: the inputs are two machine constants, not package premises. Re-derived here as `8.11111` and `0.90908` decades. `54-09` confirmed the same figures at `R-07` from the tree's own floor resolver |
| X-08 · How the exponent depends on the collocation count | `PC-5`, `OB:196`–`:198`: "The collocation budget and the prefix-sum length are **separate quantities in the source and conflated in this project**. The 256× arithmetic is real but removable." | Finding 4, `CB:50`–`:54`: "`4096/16=256` is the cardinality ratio. For equal residuals, the **last exclusive prefix** changes by `(4096−1)/(16−1) = 273`." | `ANA` | NOT-CORROBORATED | RECONCILABLE — qualifier: the two address different aspects, the multiplier's exact value and the coupling's provenance | Shared premise, named: the exclusive-prefix weight form as the package states it at `AR:435` and describes it at `MA:147`. Both inherited it from there; the open-book report additionally verified it in the code, which is a one-agent repository reading. The statements are compatible — one says the figure is not the endpoint multiplier, the other says the coupling is a departure rather than a property of the method — and neither denies the other |
| X-09 · Whether the published method's prefix runs over collocation points or over temporal groupings | `PC-5`, `OB:187`–`:192`: "In the source method the prefix sum runs over `M` temporal segments, not over collocation points" — citing Eq. 2.13 and the Expert's Guide's `M` equal sequential segments | `CB:166`, `:168`: the source uses "an exclusive temporal **sum**, spatial averaging within each temporal residual"; and the later guide "groups residuals into temporal chunks, averaging within each chunk before summing earlier chunks" | `LIT` | CORROBORATED | agree; the entitlement's consequence, subject to the edition caveat recorded in the note | The taxonomy makes literature corroboration conditional on both having read the same edition, recorded per claim rather than assumed. Here it is **partly** satisfied and the shortfall is recorded: both cite the later guide's chunking and agree on it; for the primary paper one cites an equation number and the other a section and algorithm, which are not shown to be the same edition. This pass has read no edition of either, and both reports' equation-level statements stay routed |
| X-10 · The identity of the source method | `PC-4`, `OB:167`–`:169`, quoting the vendored implementation's own reference block: Wang, Sankaran and Perdikaris, *Respecting causality for training physics-informed neural networks*, CMAME 421 (2024) 116813 | `CB:160` and the reference list at `:620`: the same authors, title, journal, volume, article number and year, with the DOI and the preprint both given | `LIT` | CORROBORATED | agree; the entitlement's consequence | **The delivery note's `§5.7(c)` join point is satisfied.** That join point says the source-method identification should converge and that divergence there would be the single most important thing to resolve first, because the whole calibration question is downstream of it. It converges: the two engagements, on different evidence bases, name the same paper by author, title, venue, volume, article number and year |
| X-11 · Whether this project carries an attribution trail for that method | `PC-4`, `OB:155`–`:172`: "the source method **is** cited inside this repository, in `reference-code/` … The gap is a **spec-citation gap**, not an evidence gap." | gap 11, `CB:595`: "The causal formula matches L1, but the project supplies no attribution trail." | `REPO-DER` | NOT-CORROBORATED | RECONCILABLE — qualifier: the specification versus the whole repository including vendored reference code, a distinction **both** reports draw | The class already forbids reading agreement here as a second reading, and these two do not agree on the surface. They reconcile on a qualifier each states for itself: the open-book report calls the gap a *spec-citation* gap; the closed-book gap is titled "Literature transfer is not project validation" and its concern is the project's own documentation. Verdict `CB-G11`; `54-09`'s `PC-4a` sharpened the specification side. **Not resolved in the open-book report's favour for having read the tree** — resolved by both authors' own qualifiers |
| X-12 · How the residual responds to a change in the initialization scale under the locked stack | `PC-1`, `OB:69`–`:86`: "**That law fails under the locked architecture** … LayerNorm is **positively scale-invariant** … A **1000× reduction in `ω₀` buys 1.63 decades of `R̄`** — not the 12 decades `ω₀⁴` would predict." | `CB:353`–`:360`: "If downstream Jacobians, Hessians, amplitudes, and cancellations remain comparable, both contributions have a nominal `ω²` scale … This is therefore neither a measured law nor a guaranteed bound for the specified stack" — and the report then computes with the fourth-power model at `CB:389`–`:401` | `ANA` | NOT-CORROBORATED | OPEN-DISPUTE | **A statement about how a quantity scales, and the reports do not agree.** Both name the same mechanism — the closed-book report writes at `CB:381` that the affine-free normalization "approximately cancels common positive amplitude scaling" and that lowering an upstream amplitude "need not lower every downstream derivative proportionally" — but one concludes the law fails and measures a much weaker response, while the other retains the fourth-power model as an explicitly conditional heuristic and computes capacity from it. Verdicts `CB-07` and `54-09`'s `R-04`, both routed: neither measurement was made on this project's own model. **Menus downstream of this dispute**, located and not reproduced: the initialization-scale menu at `CB:405` and `OB:528`; the exponent menu at `CB:182` and `OB:423`; the reference menu at `CB:308` and `OB:469`, because the capacity arithmetic on both sides is computed at a residual scale this law would move; and both composed recipes, at `CB:516` and `OB:688`. The delivery note's join point at `DELIVERY-NOTE.md:142` classifies this exactly: two agents who disagree on the scaling laws have a physics dispute that must be settled before any menu is trusted |
| X-13 · The bare first-layer derivative form | `PC-9`, `OB:275`–`:276`: "**Agree on form.** `‖a′‖ ∝ (dτ/du)²ω₀² = 4ω₀²` is the right functional statement for a bare SIREN first layer." | `CB:340`–`:345`: the first and second derivatives of a periodic first activation carry one and two powers of the frequency respectively | `ANA` | NOT-CORROBORATED | agree; the entitlement's consequence, with the shared premise named | Shared premise, named: the first layer's functional form as the specification supplies it in the bundle at `AR` §2.1–2.2. Both inherited it from the same excerpt; the open-book report additionally located it in the code. The derivative identity itself is elementary and both got it right — but agreement corroborates the arithmetic, not the premise it runs on |
| X-14 · Whether the residual scales as the square of the acceleration norm | `PC-8`, `OB:261`–`:263`: "`R̄ ∝ ‖a′‖²` means **`R̄` responds to the square of any derivative-scale change**" | Finding 1 at `CB:19`–`:24` and Finding 7 at `CB:82`: the residual equals the squared relative error times the squared acceleration norm over three, and squaring the printed acceleration column reconstructs the printed residual column | `ANA` | NOT-CORROBORATED | agree; the entitlement's consequence, with the shared premise named | Shared premises, named: the residual's definition at `AR:429`, supplied verbatim in the bundle, and the regime in which the acceleration dominates the force, which the audit asserts at `AUD:143` and neither agent measured. A scaling statement both agents derived from one supplied definition is one evaluation of that definition, twice |
| X-15 · Whether the packet's six-row reconstruction agrees to three significant figures | `PC-8`, `OB:259`–`:260`: "`M7`'s arithmetic (`R̄ ≈ ‖a′‖²/3`) re-derived: 1.374, 2.466, 1.613, 2.595, 1.254, 1.733 (×10¹⁰) against the printed 1.37, 2.46, 1.62, 2.60, 1.25, 1.74 `[OWN]`. **Agrees.**" | Finding 7, `CB:82`: "Squaring the printed acceleration medians and dividing by three agrees with the printed residual medians to roughly **0.4%**, not to three significant figures in every row." | `PKG-INT` | NOT-CORROBORATED | RESOLVED-BY-EVIDENCE — verdict `CB-F7a`, `CONFIRMED` | **The two reports compute the same six numbers and reach opposite verdicts on the packet's claim about them.** This pass computed them a third time and got the same six. Four of the six differ from the printed medians at the **third** significant figure, which is the figure `M7` claims agreement to; the maximum relative deviation is `0.414%`. The closed-book report's narrower statement holds and the open-book report's endorsement of `M7`'s wording does not. **Resolved by arithmetic on the packet's own printed numbers — a question repository access does not touch, and the engagement that read no tree is the one the evidence supports** |
| X-16 · Whether a reference that rescales with the residual can stall the front | `PC-7`, `OB:228`–`:232`: "the weight vector under batch-mean normalization is bit-identical at `R̄ ~ 10¹⁰`, `10²` and `10⁻⁴` … `front_idx` therefore becomes a **fixed statistic of the residual profile** that cannot advance as training progresses" | `D2-D` at `CB:317`: "If all residuals decrease by a common factor, numerator and reference decrease together. The weight profile can remain unchanged indefinitely." | `ANA` | NOT-CORROBORATED | agree; the entitlement's consequence, with the shared premise named | Shared premise, named: the exponential-prefix weight form as the package supplies it at `AR:435`. Both derived the same invariance from it. Worth recording that `54-09` narrowed the **stronger** of the two wordings: `R-08` is `CONFIRMED-NARROWER` because the front index remains a function of the per-step residual **shape**, so it does not follow that it is constant. The closed-book report's hedged wording — "can remain unchanged" — survives that narrowing unaltered |
| X-17 · Whether the reported gradient-norm ratio establishes that the data term's gradient disappears | `PC-6`, `OB:210`–`:212`: "At 12.8 decades below, the data term's gradient contributes **nothing** to the accumulated gradient once `λ_phys = 1`." | Finding 6, `CB:76`: "Floating-point addition acts componentwise … The observation strongly supports severe imbalance, but proving complete disappearance requires componentwise evidence, including alignment and actual accumulation behavior." | `ANA` + `REPO-DER` | NOT-CORROBORATED | OPEN-DISPUTE | The ratio itself is agreed and its class forbids that agreement being read as corroboration: the open-book report computed it from the primary log, the closed-book report relayed it from `AUD:132`, so the match is attachment-fidelity evidence. On the **inference** the two are incompatible — one states complete disappearance as established, the other states that the cited evidence cannot establish it — and no verdict in this report settles it. **What would settle it:** per-component gradient statistics for the data and physics terms over the accumulation, which no retained artifact records; the specification already requires logging weighted-loss and gradient statistics before any dominance control, at `AR:690`. Verdicts `CB-F6a`, `CB-F6b` and `CB-12`, all confirming the two positions as stated without deciding between them |
| X-18 · Where a normalization of the residual belongs | `PC-6`, `OB:216`–`:220`: a recipe that repairs the weight vector but leaves the physics loss at its current scale "will **pass GATE-04 (i)–(iii) and still train on the physics term alone** … It is the single strongest argument for locating the normalization on `R̄` itself rather than only inside the exponent." | `CB:330`: "The suggested defaults deliberately do **not** adopt automatic loss reweighting … Consequently, repairing causal weights does not establish that data and IC learning will be adequately balanced"; and `CB:535` keeps the outer physics loss unnormalized | `ANA` | NOT-CORROBORATED | OPEN-DISPUTE | **They agree on the problem and differ on where its remedy sits.** Both state that repairing the weight vector leaves the gradient imbalance unaddressed. One locates the remedy in the residual's own normalization; the other routes it to a control the specification defers at `AR:690` and keeps the outer loss unnormalized. This is a mechanism-location difference and **not** a scaling law, so it is not classified as a physics dispute. Both reports' reference menus already contain an option at the location the other's argument points to; the menus are located at `CB:308` and `OB:469` and neither is reproduced, ranked or marked here. No verdict in this report settles it and none is attempted |
| X-19 · Whether the attachments settle the causal weights' behaviour inside an L-BFGS line search | `G-7`, `OB:837`–`:840`: "Whether a frozen `R_ref` and a normalized residual behave correctly inside a strong-Wolfe line search is **not examined here**." | Finding 8, `CB:90`: "the supplied passages do not settle whether causal weights are recomputed inside its line searches." | `PKG-INT` | CORROBORATED | agree; the entitlement's consequence | A **negative** claim about the same three attachments, which both agents read in full. Both found the question unanswered and both recorded it rather than filling it. Confirmed independently here at `CB-F8b` by negative search over the relevant blocks, with the scope stated. The closed-book report goes further and derives the mechanism by which a detached surrogate would break a line search, which the open-book report explicitly declines to examine; that extension is one-agent and is verdicted at `CB-F8c` |
| X-20 · What the specification says about frozen multipliers and clipping during L-BFGS | `PC-8` at `OB:256` and `G-7` at `OB:837`–`:838`: "During L-BFGS, `λ` values are frozen and no clipping applies (`pinn_architecture.md:698`, `:768`) `[REPO]`" | Finding 8 at `CB:90` and the recipe row at `CB:532`: the specifications "freeze loss multipliers during L-BFGS", citing the same lines, and preserve the existing Adam-only gradient-clipping rule | `REPO-DER` | NOT-CORROBORATED | agree; the entitlement's consequence | **The exemplar row for the taxonomy's central rule.** Both statements are accurate and they match at the line level, and that match is **not** a second reading of the tree: the closed-book agent read those lines inside the bundle's verbatim blocks 5 and 6, which this pass proved byte-identical to the live file. The match is therefore evidence about the bundle, and it is exactly the evidence `BUNDLE-FIDELITY` records. `54-09`'s `CC-4` adds the scoping this pass carries forward — the no-clipping rule is about gradient clipping and not about the causal-exponent clip |
| X-21 · Whether the front index stayed at zero for the whole retained run | `PC-8`, `OB:255`: "`F-05` verified: `front_idx = 0` on **502/502** logged steps, single-valued `[REPO]`" — read from the primary log | register row `CB-02` at `CB:605`, citing `D5:58`: "The reported run halted with no front advancement across 502 logged steps" | `REPO-DER` | NOT-CORROBORATED | agree; the entitlement's consequence | The second textbook instance. One agent read the primary training log; the other relayed a sentence from a planning record reproduced in an attachment. Reading the agreement as two confirmations would credit a check nobody ran on the log. What the agreement does establish is that `D5:58` describes the log accurately — bundle fidelity again — and `54-09`'s `R-13` supplies the actual log reading, which is one-agent plus this pass |
| X-22 · Whether the round's returned output selects a remedy | `OB:19` and `:910`: "It selects no remedy" and "No remedy selected", with all eight decision-sheet rows carrying an empty owner's-pick cell | `CB:626`: "no specification was amended, and no remedy was ratified"; and `CB:541`: "These are proposals only. None was performed" | `PKG-INT` | NOT-CORROBORATED | agree; the entitlement's consequence, and the reason is unusual | Each statement is an attestation by a report **about itself**, so the two are claims about different objects and there is no single proposition for corroboration to attach to. Both attestations are separately confirmed by structural read — `54-09`'s `R-15` for one and the read recorded in this half's hygiene section for the other — and each stands on its own. Recorded rather than omitted, because "both reports say they select nothing" is exactly the kind of sentence a consolidation would be tempted to write as though it were corroborated |
END-INDEPENDENCE-LEDGER

### Statements about how a quantity scales, classified

The delivery note's join point at `DELIVERY-NOTE.md:142` draws a distinction this ledger is
required to apply **before** the consolidation rather than inside it: two agents who
disagree on a marked default but agree on the scaling laws have a resolvable disagreement,
while two who disagree on the scaling laws have a physics dispute that must be settled
before any menu is trusted. Applying it needs every scaling statement classified, not only
the ones that happen to disagree, so all five are listed.

| Scaling statement | Rows | Agree? | Consequence |
|---|---|---|---|
| How the residual responds to a change in the initialization scale, under the locked stack | X-12 | **No** | `OPEN-DISPUTE`. The menus downstream of it are named in the row. This is the round's one physics dispute |
| The bare first-layer derivative form | X-13 | Yes | agreement on the arithmetic; the premise is shared and named, so it is not corroboration |
| The residual as the square of the derivative scale | X-14 | Yes | same treatment; the premise is the supplied residual definition |
| The exponent's dependence on the prefix length and the collocation count | X-08 | Yes on the mechanism; the exact multiplier is sharpened by one report and the coupling's provenance by the other | `RECONCILABLE`, qualifier named |
| The weight vector's invariance under a reference that rescales with the residual | X-16 | Yes | agreement on a closed-form identity; the premise is shared and named |

**Exactly one scaling disagreement exists in this round, and it is X-12.** Four of the five
statements agree; the one that does not is the one the delivery note says must be settled
before the menus downstream of it are trusted, and this report settles nothing about it —
it records it, classifies it, names what sits downstream, and hands it to the premise
adjudication.

### Entitlement split

| Entitlement | Rows | Which |
|---|---|---|
| `CORROBORATED` | 8 | X-01, X-02, X-05, X-06, X-07, X-09, X-10, X-19 |
| `NOT-CORROBORATED` | 14 | X-03, X-04, X-08, X-11, X-12, X-13, X-14, X-15, X-16, X-17, X-18, X-20, X-21, X-22 |
| **Total** | **22** | every point carries exactly one value from the closed pair; `8 + 14 = 22` |

**Disposition split, counted from the same rows.** Fourteen rows record agreement, where
the disposition is the entitlement's consequence; the remaining eight carry a value from
the closed disposition set — `RESOLVED-BY-EVIDENCE` twice (X-03, X-15), `RECONCILABLE`
three times (X-06, X-08, X-11), and `OPEN-DISPUTE` three times (X-12, X-17, X-18). No row
carries `OUT-OF-SCOPE-HERE`; the value is defined and available and nothing in this round
needed it, which is recorded rather than omitted.

**What the split means, and what it does not.** Eight points are entitled to be read as
independently corroborated: three are package-internal readings both agents could make,
two are machine constants neither took from the package, two are literature identifications
subject to the edition caveat recorded per row, and one is a negative claim about the
attachments. Fourteen are not: three are repository-derived, where the closed-book report's
matching statement is attachment-fidelity evidence rather than a second reading; six are
analytic points resting on a premise both agents inherited from the same package; four are
disagreements; and one is a pair of self-attestations about different objects. **A
`CORROBORATED` entitlement is a statement about evidence independence and not about a
claim's truth**, which the closing section restates by name.

**Three disagreements do not go the way a reader might expect, and that is the point of
doing this by class rather than by impression.** In X-15 and X-03 the engagement that read
no tree is the one whose position the evidence supports, because both questions are about
arithmetic and about what the packet's own text says — questions repository access does not
reach. In X-11 the two reconcile on a qualifier both authors state, rather than one
yielding to the other.

## REPORT-CLOSED — what this report, across both halves, establishes

Stated as facts, each with its re-derivation recorded above, and confined to what the
verdicts support. The first half's own establishes-list stands unchanged; this list covers
both halves together.

- **`138` claim rows carry `148` verdicts from a closed six-value vocabulary**, with the
  per-verdict split at `COMBINED-VERDICT-COUNTS`: `101` confirmed, `5` sharpened, `12`
  narrowed, `3` unsupported, `27` unchecked-and-routed, and **no claim refuted in either
  half**. That is recorded as a finding, not as an absence.
- **The bundle the external agents read is byte-faithful to this repository across all
  thirteen of its verbatim reproductions** — ten declared-range excerpts of the two
  specifications, and three planning and evidence documents reproduced in full. The first
  half established ten; this half adds the remaining three.
- **Every one of the seventy-two repository anchors the closed-book report cites has an
  accounted-for provenance and resolves by content against the pinned tree.** Thirteen were
  handed to the agent literally by the master; fifty-nine were computed by offset inside a
  reproduction the agent held, and the offset arithmetic is correct in all fifty-nine. The
  untraceable bucket is empty.
- **The engagement that read no tree nonetheless settled several questions correctly that
  repository access does not reach.** It located a contradiction between two descriptions of
  the same probe inside the packet; it caught an arithmetic overstatement in the packet's own
  consistency check that the other engagement endorsed; it corrected an effective-frequency
  range against the packet's own printed table; and it distinguished a smallest-normal
  boundary from a flush-to-zero boundary. All four re-derive here.
- **Four quantities that this project's own artifacts also state were re-derived a third
  time**, with all three readings recorded side by side at `THREE-WAY-READINGS`, and the
  document that would need amending named in each case.
- **Twenty-two points on which the two reports both speak are adjudicated for
  entitlement**: eight are entitled to be read as independently corroborated and fourteen are
  not, with the reason stated in every row of the second group.
- **Exactly one scaling-law disagreement exists in this round**, at X-12, and it is
  classified, its downstream menus are named, and it is handed forward unsettled.

## What this report does not establish

The first half's disclaimers stand and are restated here for the whole report, with the two
this half adds.

- **Nothing about what should be done with any decision surface.** Verifying a claim
  *about* a surface is not the same act as disposing of that surface, and only the first is
  performed here. This report marks no default, ranks no option, reproduces no menu, and
  names no candidate value of its own. Part II tightens that further: where a quantity under
  verification is itself an option value or a component of a marked default, the quantity is
  located by line and its verdict recorded, and the value is not printed.
- **No causal claim is made or implied anywhere in it.** That a quantity has a value, that a
  departure exists, and that two descriptions of a probe disagree are not statements that any
  of them caused the halt this milestone is addressing.
- **Nothing about the twenty-seven routed rows.** They are unchecked. **An unchecked claim
  is unchecked**, and a routing target is not a result.
- **Nothing about whether a corroborated point is true.** **A `CORROBORATED` entitlement is
  a statement about evidence independence and not about a claim's truth.** Two agents can
  agree independently and both be wrong; the entitlement records only that the agreement is
  the kind that could in principle add evidential weight, and the row's claim verdict, not
  its entitlement, is where truth is addressed.
- **Nothing about the eight open or reconcilable cross-report differences beyond what their
  rows say.** In particular the scaling-law dispute at X-12 is recorded and not settled, and
  no menu downstream of it is thereby endorsed, ranked, or called into question by this
  report.
- **Nothing about what any published source says.** Thirteen occurrences across the two
  halves rest on published literature and this pass has read no edition of any of it.

## What remains

- **`54-11`, wave 4 — the premise adjudication and the re-frame determination.** Governed by
  ERW Rule 17, which places premise-challenge findings ahead of the per-question answers, and
  by the delivery note's own join rule at `DELIVERY-NOTE.md:143` that premise findings merge
  first, before any answers are read, because a contradicted premise invalidates the answers
  built on it however well argued. It is also the plan authorized to route the candidate gap
  rows below into a register; **no register is edited by this report**.
- **`54-12`, wave 5 — the consolidation.** Governed by ERW Rule 11's join points at
  `DELIVERY-NOTE.md:137`–`:147` and by Rule 12, which fixes the consolidated document's name
  and location. The operational rule it inherits is the one stated at `54-INTAKE.md`: a
  consolidated statement may claim two-agent support **only when the claim's class admits
  it**, and every consolidated claim carries its class so a reader can check the entitlement
  rather than trust it. **No claim may be consumed by that plan without a verdict**, and the
  entitlement column of the cross-report adjudication above is what tells it which
  agreements it may lean on.
- **`54-13`, wave 6 — the owner's ratification at checkpoint ②**, recorded in
  `54-RULING.md`. Governed by SCOPE-34: the recalibration decision is owner-ratified and
  never agent-decided. Nothing in this report is a ruling and nothing in it proposes one.

## CANDIDATE-GAP-ROWS-PROPOSED — extended by this half, still proposed and still not filed

Ten further owner-routed questions this half surfaced, numbered on from the first half's
six. As before they are **listed here rather than written into a register**, because the
routing decision and the register edits belong to the wave-4 plan; both gap registers and
the ruling record are byte-unchanged against `HEAD` at this plan's close and the gate
asserts it. None of the ten is adjudicated here. Each carries the STOP-protocol field
schema's required fields, with `Status` and `Resolution note` left as the wave-4 plan will
find them.

**7 — The receiving-end burden for a closed-book round whose uploads carry repository
anchors has no bucket vocabulary for a reproduction that declares no line range.**
*Where in artifact:* `ANCHOR-PROVENANCE-TRIAGE`, the reading paragraph in Bucket 2; the
burden as derived at `54-INTAKE.md` `BURDEN-CLOSED-BOOK`. *Task context:* assigning a
provenance bucket to fourteen anchors into the master and to twenty-three anchors into
three documents the closure-evidence bundle reproduces in full. *Classification:*
process-artifact schema. *Source silence:* the burden's second bucket is defined as a line
falling inside "a range that a verbatim block in an attachment declares for that file"; the
runbook does not contemplate this case at all, and neither the burden nor the plan says
whether a block that declares its range by reproducing a document in full, or an attachment
that **is** the cited file, satisfies that definition. *Grounding:* the third bucket's
stated meaning is that the line number "came from somewhere the attachments do not account
for", and for both of these forms the attachments account for it exactly — by a fixed,
checkable offset in one case and by an offset of zero in the other. Assigning them to the
third bucket would report thirty-seven unaccounted-for anchors where none exists and would
dilute the one bucket whose purpose is to concentrate attention on genuinely unexplained
citations; assigning them to the second bucket requires reading "declares a range" to include
a declaration made by reproduction rather than by numeral. Nothing downstream turns on the
choice — every anchor is content-resolved either way and no claim verdict depends on it —
but the counts a later document quotes do. *Agent was tempted to:* apply the second-bucket
reading silently, since it changes no verdict. *What the owner decides:* (A) the reading
applied here is adopted and the burden's wording is amended to say so; (B) the strict-literal
reading is adopted and the counts are restated as `13 / 45 / 14`; (C) the bucket vocabulary
gains a fourth value for a reproduction supplied whole. *Confidence of impact:* MEDIUM — it
changes three published counts and no verdict. *Status:* proposed, not filed. *Resolution
note:* — .

**8 — The packet's own six-row consistency check claims a precision its own printed values
do not reach.** *Where in artifact:* `CB-F7a` and `THREE-WAY-READINGS`, this report; the
underlying entry at `RESEARCH-CONTEXT-MASTER.md:143`. *Task context:* re-deriving Finding
7's first assertion against the packet's own numbers. *Classification:* operational
coordination. *Source silence:* `M7` claims agreement to three significant figures in all
six rows and prints six computed values, four of which differ from the printed medians at
that very figure; nothing in the packet reconciles the claim with its own table.
*Grounding:* the reconstruction is exact arithmetic on transcribed numbers, so the
disagreement is a rounding-and-claim mismatch rather than a modelling question; the maximum
relative deviation is `0.414%`, which is a perfectly good consistency result and a poor
three-significant-figure result. The distinction matters because `M7` is cited as an
internal-consistency certification of the six-row probe, and a certification stated at the
wrong precision invites a later reader to treat the printed medians as exact.
*Agent was tempted to:* record the row as a plain confirmation of Finding 7 without naming
the artifact the correction lands on. *What the owner decides:* (A) `M7`'s wording is
corrected to state the achieved precision; (B) the mismatch is recorded as known and the
entry is left as written; (C) the check is re-run at full precision from the probe's own
output rather than from the transcribed medians. *Confidence of impact:* MEDIUM — it
changes a certification's wording, not any physical claim. *Status:* proposed, not filed.
*Resolution note:* — .

**9 — The audit's effective-frequency range understates its own printed table.**
*Where in artifact:* `CB-F3c` and `THREE-WAY-READINGS`, this report; the underlying
statements at `2026-08-17-residual-frame-conformance-audit.md:165` and its transcription at
`RESEARCH-CONTEXT-MASTER.md:127`. *Task context:* re-deriving Finding 3's third assertion
from the six probe rows. *Classification:* operational coordination. *Source silence:* the
audit states a range and prints a table from which a different and wider range follows;
neither document reconciles them. *Grounding:* the quantity is a ratio of two printed
columns, so the correct range is fully determined by the table and is `654.84` to `992.88`;
the audit's upper end understates it by about a tenth. The figure is used as the network's
effective angular frequency in the coordinate, and a squared quantity carries that
understatement squared, which is why the ten percent is worth naming rather than waving
through. *Agent was tempted to:* record only that the report's figure re-derives, without
naming where the superseded figure lives. *What the owner decides:* (A) the audit's range is
corrected and the transcription follows it; (B) the range is left and a note records that
it is a round-number summary; (C) the derived quantity is dropped from the transcription
since the table it comes from is reproduced anyway. *Confidence of impact:* MEDIUM — the
figure is descriptive, and it is descriptive of a quantity two later arguments lean on.
*Status:* proposed, not filed. *Resolution note:* — .

**10 — The master's count-coupling figure is a cardinality ratio applied to an
exclusive-prefix quantity.** *Where in artifact:* `CB-F4b` and `THREE-WAY-READINGS`, this
report; the underlying statements at `RESEARCH-CONTEXT-MASTER.md:147` and `:185`. *Task
context:* re-deriving Finding 4's arithmetic. *Classification:* operational coordination.
*Source silence:* the master defines the prefix as **exclusive** in the same paragraph in
which it computes the coupling as a cardinality ratio, and hedges the result with
"roughly"; it does not say which quantity the ratio is a ratio of. *Grounding:* for a flat
profile the endpoint exponent is proportional to the prefix **length**, which is one less
than the count, so the endpoint multiplier between the two counts is `4095/15 = 273` and
not `4096/16 = 256`. Both figures are exact and they are exact about different things. The
hedge makes the master's statement defensible as an order-of-magnitude figure, and the
round's own decision sheet treats the coupling as a joint-ratification requirement, where an
order-of-magnitude figure and an exact multiplier are not interchangeable. *Agent was
tempted to:* record Finding 4 as sharpening the master, which would have asserted an error
where the master's own hedge already covers it. *What the owner decides:* (A) the master's
paragraph is amended to distinguish the two ratios; (B) the hedge is treated as sufficient
and nothing changes; (C) the coupling is restated in terms of prefix length throughout.
*Confidence of impact:* MEDIUM — it changes a mechanism description that a joint
ratification is scoped against. *Status:* proposed, not filed. *Resolution note:* — .

**11 — The packet describes the same probe two incompatible ways.**
*Where in artifact:* `CB-F1a`, `CB-03`, `CB-G02` and cross-report point X-03, this report;
the underlying statements at `2026-08-17-residual-frame-conformance-audit.md:109` and
`.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-DIAG-05-REDERIVATION.md:83`.
*Task context:* content-resolving the anchors Finding 1 sets against each other.
*Classification:* semantic. *Source silence:* the audit describes a finite-differenced
stored trajectory and the operative diagnosis describes a trained network against ground
truth; both are in the packet, neither cites the other, and nothing reconciles them.
*Grounding:* the two descriptions license different inferences. A consistency check on a
stored trajectory measures whether the integrator's output satisfies the force law; a
measurement on a trained network measures how close that network's residual gets. Only the
second could bear on what a converged residual scale is, and the diagnosis's root-cause row
cites the datum as an independent confirmation of exactly that. Both returned reports read
the same packet and took different sides of the contradiction. *Agent was tempted to:*
decide which description is right by reading the probe source in the tree. That would have
been adjudicating a premise, which is wave 4's authority, so the row records the
contradiction and stops. *What the owner decides:* (A) the diagnosis's description is
corrected to match the audit's; (B) the audit's is corrected; (C) the datum is withdrawn
from use as a converged-scale reference and both descriptions are left as historical
record. *Confidence of impact:* HIGH — a converged residual scale is what one whole
decision surface is calibrated against. *Status:* proposed, not filed. *Resolution note:*
— .

**12 — The two reports disagree about how the residual responds to the initialization
scale.** *Where in artifact:* cross-report point X-12 and `CB-07`, this report; the two
positions at `chatgpt-resolution.md:353`–`:360` and `claude-resolution.md:69`–`:86`. *Task
context:* classifying every scaling statement both reports make, as the delivery note's
join rule requires before consolidation. *Classification:* semantic. *Source silence:*
neither measurement was made on this project's own model — one is an explicitly conditional
analytic model, the other a clean-room re-implementation — and no artifact in this
repository measures the response. *Grounding:* the two positions differ by roughly ten
decades in what a large reduction of the initialization frequency would buy, and the
capacity arithmetic on both sides is computed at a residual scale this law would move.
Both reports name the same mechanism for why a naive fourth-power law would fail, so the
disagreement is about the mechanism's **magnitude** under the locked stack, not about its
existence. The delivery note's own join rule says a scaling-law disagreement is a physics
dispute that must be settled before the menus downstream of it are trusted. *Agent was
tempted to:* prefer the measured clean-room sweep over the conditional analytic model,
because a measurement sounds stronger than a heuristic. Neither was made on this project's
model, so that preference would have been an aesthetic one. *What the owner decides:* (A)
the dispute is settled by an owner-authorized characterization on this project's own model
before any menu downstream of it is read; (B) the dispute is recorded and the affected menus
are deferred; (C) the dispute is declared not to block, with the reason recorded.
*Confidence of impact:* HIGH — the delivery note names this exact case as the one that
invalidates downstream menus. *Status:* proposed, not filed. *Resolution note:* — .

**13 — The two reports disagree about whether the reported gradient-norm ratio establishes
that the data term's gradient disappears.** *Where in artifact:* cross-report point X-17,
`CB-F6a`, `CB-F6b` and `CB-12`, this report. *Task context:* adjudicating entitlement on a
point both reports address. *Classification:* semantic. *Source silence:* no retained
artifact records per-component gradient statistics, and the specification requires such
logging only before a future control law is adopted. *Grounding:* floating-point addition
acts componentwise, so a ratio of vector **norms** bounds no individual component; two
vectors with disjoint support have an arbitrary norm ratio and lose nothing on addition.
The audit's inference is nevertheless plausible for aligned, dense gradients. The dispute is
therefore about what the available evidence **proves**, not about what is likely, and it is
settleable by an instrumented measurement that nobody has run. *Agent was tempted to:*
resolve it in favour of the componentwise objection, which is mathematically unimpeachable
as a statement about warrant. That would have been adjudicating, and it would also have
overstated the objection, which does not claim the data gradient survives. *What the owner
decides:* (A) the componentwise statistics are commissioned before the inference is relied
on; (B) the inference is retained with its evidential status downgraded and recorded; (C)
the inference is withdrawn from the diagnosis. *Confidence of impact:* MEDIUM — it changes
what the diagnosis can be said to have established, not what any spec says. *Status:*
proposed, not filed. *Resolution note:* — .

**14 — The two reports place a normalization of the residual in different mechanical
locations.** *Where in artifact:* cross-report point X-18, this report; the two positions at
`chatgpt-resolution.md:330` and `:535`, and `claude-resolution.md:216`–`:220`. *Task
context:* recording a difference between the two reports without resolving it, as the plan
requires. *Classification:* semantic. *Source silence:* both reports agree that repairing
the weight vector leaves a gradient-magnitude imbalance unaddressed; neither the packet nor
the specification says where the remedy for that imbalance belongs, and the specification
explicitly defers the adjacent control at `pinn_architecture.md:690` pending measured
evidence. *Grounding:* the two locations are not equivalent: one changes only the weights,
leaving the outer loss's magnitude and therefore the gradient balance untouched; the other
changes the outer loss's magnitude too, which alters the total-loss balance and the meaning
of the locked multipliers. Both reports' menus contain an option at each location and
neither is named, ranked or marked by this report. *Agent was tempted to:* note which
location the deferred control at `AR:690` more naturally interacts with. That would be an
argument for one option, which SCOPE-34 puts outside this pass. *What the owner decides:*
the disposition of the surface itself, at checkpoint ②, on the consolidated sheet.
*Confidence of impact:* HIGH — it is a difference between the two returned recipes at a
point the specification treats as a locked contract. *Status:* proposed, not filed.
*Resolution note:* — .

**15 — The round prompt's file-count warning is stale, and both engagements noticed.**
*Where in artifact:* `CB-F7c` and cross-report point X-02, this report; the two statements
at `RESEARCH-AGENT-PROMPT.md:87` and `RESEARCH-CONTEXT-MASTER.md:90`. *Task context:*
content-resolving Finding 7's third assertion. *Classification:* operational coordination.
*Source silence:* the master records the count correction as an amendment; the prompt was
not updated, and nothing says which document an agent should treat as governing when they
disagree. *Grounding:* the rule exists to stop an agent silently resolving a specification
citation against a frozen copy rather than the authoritative file, and the fifth path is
the one the amendment says the rule exists to catch. A stale count in the instructions is
low-stakes in itself and is a live premise in the instructions the round was given. *Agent
was tempted to:* fold this into the first half's candidate row about stale anchors, which
is a different artifact and a different failure. *What the owner decides:* (A) the prompt is
corrected for any future round; (B) the discrepancy is recorded and the prompt is left as
the historical record of what this round's agents were told; (C) the anchor-resolution rule
moves to a single home so it cannot diverge again. *Confidence of impact:* LOW — no
citation in either returned report resolved to a frozen copy, so no harm materialised.
*Status:* proposed, not filed. *Resolution note:* — .

**16 — A figure the closed-book report uses at three significant figures is cited to a
locus that carries it at two.** *Where in artifact:* the corrections recorded at the end of
`ANCHOR-PROVENANCE-TRIAGE`, this report. *Task context:* content-resolving Finding 1's
anchors. *Classification:* operational coordination. *Source silence:* the audit prints the
quantity at full precision at one line and rounds it at another; the report uses the precise
form and cites neither line for it. *Grounding:* the figure is a faithful rounding of the
precise locus, so nothing is wrong with the number; what is missing is the citation, and a
verification pass that could not find the locus would have been entitled to record the
figure as unsupported. It was found here, so the row is a completeness note rather than a
defect. *Agent was tempted to:* record the anchor set as complete without noting that one
load-bearing figure sits outside it. *What the owner decides:* (A) nothing is required and
the locus is recorded here for future readers; (B) a later pass adds the citation when it
next touches the round's record. *Confidence of impact:* LOW — the figure is correct and
now has a recorded home. *Status:* proposed, not filed. *Resolution note:* — .

**Sixteen candidate rows now stand across both halves — six from the first, ten from the
second — and none is filed.** The routing decision, the classification confirmations and
every register edit belong to `54-11` in wave 4.

## VERIFICATION-HYGIENE — the standing bars at this report's close

Every bar was re-run at the close of this half. Commands carrying Bar F or Bar G cost
vocabulary are recorded in the fenced blocks the first half already carries, which are
unchanged and are not duplicated here.

| Check | Command | Output | Verdict |
|---|---|---|---|
| Bar D — canonical, index-anchored | `git diff --stat -- <the six canonical pathspecs>` | empty | PASS |
| Bar D — the same six pathspecs anchored to `HEAD` | `git diff HEAD --stat -- <the same six pathspecs>` | empty | PASS — recorded in addition to the index-anchored form, never instead of it |
| Bar E — canonical two-path form, `HEAD`-anchored | `git diff HEAD --stat -- .planning/REQUIREMENTS.md .planning/ROADMAP.md` | empty | PASS — this plan edits neither file, so no narrowing applies and none is taken |
| Bar F — cost vocabulary over the ruling record | the fenced block in the first half's hygiene section, run verbatim | `0` | PASS — equal to the number `54-08` and `54-09` both recorded |
| Bar G1 — no candidate value across any decision surface | the fenced block in the first half's hygiene section, selector `S` byte-unchanged from `54-06-PLAN.md`, file list this pass's six plan files | region cardinality `G1-REGION=0`; remainder after token strip empty | `BAR-G-CLEAN-NO-SURFACE-NAMED` |
| Bar G2 — no ordering vocabulary in the plans' own voice | same fenced block | empty | PASS |
| Bar G3 — no cost framing in the plans' own voice | same fenced block | empty | PASS |
| Bar G preprocessing sanity — fence balance and retained stream size, printed **before** any sub-bar is trusted | `grep -c '^```'` over each of the six plan files; retained line count of the shared stream | fence counts 10, 8, 8, 8, 10, 10 — all even; retained stream `4233` lines | PASS — an odd fence count would make the preprocessing swallow the rest of a file and every sub-bar would then pass vacuously |
| Check R1-w — widened round-root manifest, re-run verbatim | the fenced block in `54-08-PLAN.md`'s verification section | `MANIFEST-OK-W` | PASS — string equality over the seven authorized paths, so an eighth file, a missing file, or a one-for-one substitution all fail |
| Identity proof re-run against the pinned commit | `git diff --stat efe8e590d6c6b2a77cc92abb0b93d625e2b92c49 HEAD -- $(cat <the citable-path block>)`; `git status --porcelain -- $(cat <the same>)`; `CPN` against shell-argument count | both empty; `CPN=21 ARGS=21`; both sentinels found | `PIN-TREE-IDENTICAL` — re-run at this half's close rather than inherited from the first half's run |
| Anchor gap still `OPEN` in both registers | `grep -n 'Status' 54-GAPS.md \| grep -i 'OPEN'`; `grep -n 'GAP-54-01' .planning/milestones/v2.3-GAPS.md \| grep -i 'OPEN'` | `54-GAPS.md:42` carries `**Status:** OPEN`; `v2.3-GAPS.md:11` and `:15` both carry `OPEN` | PASS — both non-empty |
| Ruling record and both gap registers byte-unchanged | `git diff HEAD --stat -- 54-RULING.md 54-GAPS.md .planning/milestones/v2.3-GAPS.md` | empty | PASS — anchored to `HEAD`, so a staged edit cannot leave the assertion empty and passing |
| The whole round root byte-unchanged | `git diff HEAD --stat -- <the trainex-r3 round root>` | empty | PASS — covers both returned reports, all three uploaded attachments, the prompt and the delivery note in one assertion |
| No consolidated document exists | `test ! -f .../trainex-r3/trainex-r3-resolution-doc.md && echo CONSOLIDATION-ABSENT` | `CONSOLIDATION-ABSENT` | PASS |
| Exactly one report file matching the date pattern | `ls -1 <the reviews directory> \| grep -cE '^[0-9]{4}-[0-9]{2}-[0-9]{2}-trainex-r3-rule19-claim-verification\.md$'` | `1` | PASS — the record was extended rather than split, so wave 4 reads all of it |
| Manual structural read of Part II, end to end | read of every section added by this half | No sentence in Part II names a candidate value for any decision surface, reproduces any options menu, reproduces any marked default, ranks anything, or marks a surface as the one to change. Where a quantity under verification is itself an option value or a component of a marked default or a composed recipe, the quantity is **located by line and its verdict recorded, and the value is not printed** — the rule stated at the top of Part II and applied at `CB-09`, `CB-A03` and `CB-A13`. Where a threshold or a machine constant this report re-derives sits numerically near a value some menu also carries, the report records the quantity as the object of the check and thereby endorses, ranks and marks nothing. The two reports are written in a fixed order throughout the cross-report adjudication — open-book first — and that order is a presentation convention with no evidential weight, stated in the adjudication's own preamble so it is not read as one | PASS — Part II names no candidate value, marks nothing, and ranks nothing |

**Bar G's literal and region are unchanged from what `54-08` and `54-09` recorded**, which
is the expected result and is recorded as such rather than reported as a silent pass: this
plan edited no plan file, so the retained stream is the same `4233` lines and the region
over it is still empty. `BAR-G-CLEAN-NO-SURFACE-NAMED` with `G1-REGION=0` is the literal
the gate prints and is not a paraphrase of, or a substitute for, `BAR-G-CLEAN`.

## Halt state at the report's close

**Phase 54 does not close here.** `GAP-54-01` stays `OPEN` in both registers; the ruling
record's checkpoint ② stays unfilled and byte-unchanged; Phase 56 stays closed; no
consolidated document exists. No premise is adjudicated, no menu is merged, no decision
surface is disposed of, no gap is filed, and no entry is made in the ruling record.

**The verification report is complete.** Both burdens the intake record derived are
discharged: the open-book report's repository claims were independently re-derived, and the
closed-book report's anchors were triaged for provenance and resolved by content. Every
claim in both reports carries a verdict from a closed vocabulary, every unchecked claim is
routed, and every point on which the two reports both speak carries an entitlement that
says whether their agreement may be read as corroboration. `54-11` follows in wave 4 with
the premise adjudication, and it may consume no claim from this file that does not carry a
verdict.
