---
title: "Trainex R4 Consolidated Resolution Document — the round's joined diagnoses, experiments and options, presented as a candidate decision sheet for the owner's ruling"
round: trainex-r4
role: "ERW Rule-12 consolidated output of the trainex-r4 round; a candidate decision sheet for the owner's ruling, never the ruling"
status: candidate-for-ratification
created: 2026-10-07
responding_agents: 2
access_mode_declared: open-book
attachment_baseline_pin: 735e2ae8d5ec30b9915ec9172ac06965fbaa8afb
live_tree_pin_codex: b09c4c8cfd22429e0d14482c355719f862a54e6f
live_tree_pin_claude: 9bebe667b520e25e0bea5b84eeb0a4fc7168a9e5
consolidation_tree_pin: ce2ebb0fac3ef891f333c6f5c21c862ee0293fa5
verification_report: docs/work/reviews/cross_cutting/trainex-r4/2026-10-07-trainex-r4-rule19-claim-verification.md
reframing_ruling: "DELIVERY-NOTE.md, section 'Re-framing ruling (2026-10-07)', items R-1 to R-7"
consolidator: Claude Code (claude-opus-5-5), the in-repo agent
---

# Trainex R4 — Consolidated Resolution Document

## What this document is

This is the trainex-r4 round's consolidated output (ERW Rule 12). It joins the
two returned reports at the six join points the delivery note records (ERW
Rule 11; `DELIVERY-NOTE.md`, "Consolidation join points"). It lives at the round
root because ERW Rule 14 makes the round root the durable record.

Three records constrain it:

- **The Rule-19 verification report** (`verification_report` above). Part 1
  checked 122 premise rows and refuted none. Part 2 checked 137 rows on the
  diagnoses, the facts behind each option, the gaps and the registers: one
  figure was refuted and 13 were narrowed. Wherever the verification narrowed
  or refuted a claim, this document uses the verified form and says so.
- **The re-framing ruling** (R-1 to R-7 in the delivery note). It was made on
  2026-10-07 by the in-repo agent under the owner's delegation. R-2 says how
  each kind of answer may be used, and this document applies it to every
  diagnosis and option. R-3 puts conformance first on the decision sheet and
  makes the IC term's batch behavior a decision of its own.
- **R-7's literature instruction.** The consolidation includes a
  primary-source reading of the published facts about the source method
  that the reports state. That reading is this document's own work, and
  JOIN-2 records it.

**What this document does not do.** It selects no option and fills no pick.
It changes no recipe value and authorizes no training run, evaluation or
model computation. It amends no specification.

## Reading guide — the decision sheet in brief

- **The two reports do not dispute any diagnosis.** Wherever both name a
  mechanism for an observation, they name the same one. Their differences are
  confidence and emphasis, and the pooled experiments in JOIN-4 can settle them.
- **The candidate decision sheet has twelve decisions** (`JD-0` to `JD-11`,
  JOIN-5), plus five owner questions that neither report gives a menu for
  (`OQ-1` to `OQ-5`).
  - **Agreed or fixed defaults:**
    - **JD-0, conformance.** Its default is fixed by the owner's
      2026-09-07 Option A instruction (R-3), and both reports suggest it.
    - **JD-3, front meaning;** **JD-5, schedule;** **JD-9, architecture;**
      **JD-10, telemetry;** **JD-11, which experiments come first.**
    - **JD-2, balancing:** the two reports agree to measure before choosing
      a remedy.
  - **Disputed between the reports:**
    - **JD-4:** whether the invariant-B guard may halt the next run.
    - **JD-6:** whether the next run exercises L-BFGS.
    - **JD-7:** whether the next run is a single-seed control or a
      multi-seed calibration pilot.
    - **JD-2:** whether a balancing remedy is named before the measurement.
  - **Offered by one report only:**
    - **JD-1,** the IC term's batch semantics: Claude only. Codex is silent.
    - **JD-8,** the causal coefficient: Codex only.
- **Mixing picks across the disputes builds a recipe neither report wrote.**
  JOIN-6 names the combination that matters: an active raw-step guard
  together with a reachable L-BFGS phase.
- **The literature holds.** Every fact the reports state about the source
  method matches the paper, the authors' code, or the authors' later guide
  (`LR-1` to `LR-17`). The papers that individual options cite hold too
  (`LR-18` to `LR-21`), with one citation narrowed (`LR-18`). Four items
  could not be read (`LR-22` to `LR-25`).

## STANDING — this document is a candidate, not a ruling

The delivery note states this document's standing. It is quoted, not
paraphrased (`DELIVERY-NOTE.md`, "Standing of the eventual resolution doc"):

> This is a build-design round. The consolidated resolution doc offers findings,
> experiment proposals, and options menus, not verdicts. The owner fills the
> decision sheet, and those picks are the decisions. The report is not a
> grounding source for framework-spec adjudication. Any spec change it leads to
> is a formal amendment requiring explicit owner re-ratification.

**So the owner's-pick column in the candidate decision sheet is empty in every
row, and stays empty here.** The owner's picks are recorded as project Key
Decisions (`.planning/PROJECT.md`, "Key Decisions"; ERW Rule 13) and carried
into the next milestone.

The standing boundaries of the v2.3 close are unchanged by this document
(`DELIVERY-NOTE.md`, "Standing boundaries, in plain terms"):

- no recipe value moves without an owner ruling;
- the single held-out evaluation stays unspent;
- Stage-1+ and PLAT-01..07 stay blocked until a `go` verdict;
- no training run happens before the owner rules.

## ATTRIBUTION — how to read the tags

Every element below carries a tag naming whose it is.

| Tag | Whose element it is |
|---|---|
| `{codex}` | The Codex report, `research_results/codex-resolution.md` |
| `{claude}` | The Claude report, `research_results/claude-resolution.md` |
| `{both}` | Both reports produced it independently; it is one element with two authors |
| `{verify}` | The Rule-19 verification report: a verdict, a narrowing, or a fact it found |
| `{ruling R-n}` | The 2026-10-07 re-framing ruling, item R-n |
| `{lit}` | This document's primary-source literature reading (R-7), recorded in JOIN-2 |
| `{join}` | Consolidation mechanics: an R-2 class, a flag on an option's presupposition, an agreement or dispute marker, or a coherence observation. A `{join}` element is never a suggested default and never a pick |

**R-2 classes.** R-2 sorts the round's answers into three kinds. Every
diagnosis row below carries one, and option flags name one where it matters:

| Class | What it covers (R-2's own list) | How this document uses it |
|---|---|---|
| `S` structural | Properties of the configuration, code, specs or guard that hold whichever trajectories the loss evaluates: L-BFGS unreachable when `max_epochs == n_adam`; the cosine schedule and the guard window interact; an `R_ref`-relative front cannot certify absolute accuracy; the guard is a high-water record statistic; the conformance verifier tested the sampler, not the loss; the IC gradient dominates under residual-wide normalization (a design concern, to be re-measured once the run conforms) | Usable as findings, including in an option's rationale |
| `E` empirical | Rates and magnitudes measured on generations 6 and 7: front pace, residual reductions, budget estimates, oscillation statistics, the natural experiment | They describe the single-anchor run. They may motivate a hypothesis or an experiment. They may not set or justify a recipe value; an option whose rationale leans on one is flagged |
| `V` void | Answers about the ratified recipe's own behavior: the Q4 step budget, and Q5's oscillation as a property of the recipe | Carried forward as open questions, not as answers |

**Independence.**

- **Both engagements were open-book on the same branch.** Their tree pins
  differ (frontmatter), but every code file the diagnoses rely on is
  byte-identical to the generation-7 run commit `629b1a6c…`. Both reports
  state this, and Part 1 of the verification confirmed it with a
  whole-directory diff.
- **The two reports were written independently.** Codex returned first.
  Claude disclosed that it did not read the Codex report
  (`claude:94-98`).
- **What agreement does and does not show.** An agreement is two independent
  readings of the same tree. It is not independent of the package framing,
  which both agents received.

**The reports' labels collide, and this document never uses them bare.** The
two reports number their decisions differently, and the same label means
different things:

| Topic | Codex label | Claude label | Joined ID |
|---|---|---|---|
| Conformance | D0 | D0 | `JD-0` |
| IC term batch semantics | — | inside D0-A; gap G-1 | `JD-1` |
| Loss-gradient balance | D1 | D1 | `JD-2` |
| Front meaning and stage success | D3 | D2 | `JD-3` |
| Invariant-B guard | D2 (window), D7 | D3 | `JD-4` |
| Learning-rate schedule | D2 (schedule) | D4 (schedule) | `JD-5` |
| L-BFGS reachability and plateau input | D6-B | D4-A (L-BFGS, plateau) | `JD-6` |
| Budget, seeds, what the next run is | D6 | D5 | `JD-7` |
| Causal coefficient | D4 | inside D2-B | `JD-8` |
| Architecture | D5 | D6 | `JD-9` |
| Telemetry and verification gates | D7-A, D0's verification | D7 | `JD-10` |
| First authorizations | (decomposition first) | D8 | `JD-11` |

Claude's evidence analyses are `E-A` to `E-H`, and its proposed experiments are
`E2` to `E9`. Its gaps are `G-1` to `G-15`; Codex's are numbered 1 to 10. The
pooled experiments here are `JX-1` to `JX-10`, the merged gaps `JG-1` to
`JG-22`, and the literature rows `LR-1` to `LR-25`. Verification rows keep their
own IDs (for example `B-PC1t`).

One clash remains. The verification report's Group-G rows (`G-1` to `G-9`)
share labels with Claude's gaps (`G-1` to `G-15`), so this document always
writes the first as "verification `G-n`" and the second as "Claude G-n".

**Citation shorthand.**

| Shorthand | File |
|---|---|
| `codex:N`, `claude:N` | line N of `research_results/codex-resolution.md` or `research_results/claude-resolution.md` (this round root) |
| `V:N` | line N of the verification report named in the frontmatter |
| `pinn_architecture.md:N`, `ctl_instruction.md:N` | the framework specs under `pinn_instruction/markdown_conversion/framework-specs/` |
| `controllers.py:N`, `batches.py:N` | `pinn/training/controllers.py`, `pinn/data/batches.py` |
| `54-RULING.md:N`, `54-GAPS.md:N` | `.planning/phases/54-recalibration-decision-grounding/` |
| `57-GAPS.md:N`, `57-02-PLAN.md:N`, `57-RULING.md` | `.planning/phases/57-corrected-re-run-the-preserved-evaluation/` |
| `r3-resolution:N` | `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/trainex-r3-resolution-doc.md` |
| any other `path:N` | repository-relative |

The delivery note is cited by section name, not line number, because its
status block changes when this document lands. Literature locations are
given as file and line inside each source's arXiv TeX or code archive;
JOIN-2 lists the archives with their SHA-256 digests.

## The order of the joins, and why

The delivery note lists six join points. This document runs them in the
order their reasons set, not their bullet order. The source-method bullet is
fifth in the list, but its own text says "A disagreement here is resolved
first, because several answers depend on what the source method says about
scheduling". It therefore runs second: after the premises, which "merge
first, before any diagnosis is read", and before the diagnoses that use it.

| Join | Section | The delivery note's reason, quoted |
|---|---|---|
| 1 | `JOIN-1-PREMISES` | "Premise-challenge findings merge first, before any diagnosis is read. A contradicted premise invalidates the answers built on it." |
| 2 | `JOIN-2-SOURCE-METHOD` | "The source-method identification should converge, and should be compared with trainex-r3's JOIN-2 identification. A disagreement here is resolved first, because several answers depend on what the source method says about scheduling." |
| 3 | `JOIN-3-DIAGNOSES` | "The diagnoses join per question (Q1–Q5). … Two who name different mechanisms for the same observation have a diagnostic dispute. Route that dispute to the discriminating experiments, not to a vote." |
| 4 | `JOIN-4-EXPERIMENTS` | "The discriminating experiments are pooled. Merge duplicates, and keep each one's stated cost and whether it needs a training run." |
| 5 | `JOIN-5-OPTIONS` | "The options join on the decision. Each option carries the diagnostic outcome it presupposes, so options whose presuppositions conflict with the merged diagnosis are flagged, not silently dropped." |
| 6 | `JOIN-6-COHERENCE` | "The composed next-run recipes are the coherence check. Compare them directly. A recipe that no agent's own menus compose into is a signal that the menus interact in a way the per-question answers missed." |

## JOIN-1-PREMISES — the premise findings, merged first

**This join is already settled, and this section transcribes it.**

- **Verified.** Part 1 of the verification checked both reports' premise
  findings and refuted none (`V:272-296`).
- **Ruled on.** The re-framing ruling decided how the round's answers may be
  used.

What follows is the merged list, with the verified form of each finding and
the decision each one feeds. Nothing here is re-decided.

### The joined premise findings

| # | Joined finding | Codex | Claude | Verified form (Part 1) | Feeds |
|---|---|---|---|---|---|
| P-1 | The physics term was evaluated on one trajectory per step: the lowest-ID of that step's 240 replay draws. Only the collocation times came from the per-slot allocation | P1 (`codex:31-51`) | PC-1 (`claude:206-320`) | **Holds** `{verify}`. The IC term is also anchored, but that is preserved design, not part of the verified defect (`B-PC1t`, narrower) | `JD-0`, `JD-1` |
| P-2 | The invariant-B monitor scored one trajectory (ID 28); validation physics is one time point on one trajectory (ID 12) | P3 (`codex:59-63`) | PC-1 | **Holds** `{verify}` | `JD-0`, `JD-4` |
| P-3 | The Phase-57 conformance verifier tested the sampler's keys, not what the loss evaluates; its `anchor_only` field is a constant | P2 (`codex:53-57`) | PC-1, C-10 | **Holds** `{verify}` | `JD-0`, `JD-10` |
| P-4 | L-BFGS could not run: at budget exhaustion its budget is zero (`max_epochs == n_adam`), and the plateau trigger's longest qualifying streak was 6 of the required 50 | P4 (`codex:65-69`) | PC-3 (`claude:390-414`) | **Holds** `{verify}` | `JD-6` |
| P-5 | Generations 6 and 7 are one experiment: identical batches, anchors, validation draws and monitor. Generation 6 died at step 513 without completing a window | P5 (`codex:71-73`) | PC-4 (`claude:416-456`) | **Holds, sharper** `{verify}`: identical for all 513 shared steps | `R-4`; evidence limits; `JD-7` |
| P-6 | The logged gradient figures are pre-Adam global norms; the total-loss identity holds to float32 rounding | P6 (`codex:75-79`) | (PC-2 discusses Adam) | **Holds** `{verify}`; the largest discrepancy is at log line 53, not 57 | how F-08 is read |
| P-7 | The causal physics term was effectively not trained; the IC term dominated the update | (Q1: "high for gradient domination", `codex:107`) | PC-2 (`claude:322-388`) | **Holds, narrower** `{verify}`: the data term trained on all selected slots; the input layer grew ×1.080 while the output layer shrank ×0.668; the dominance is shown in global norms, not per parameter | `JD-2`; class `S` as a design concern, re-measured under conformance (R-2) |
| P-8 | An in-run absolute measurement exists: the validation gate's median `eps_H` stayed at 0.983–0.990 while the front went 0 → 2 | — | PC-5 (`claude:458-479`) | **Holds** `{verify}` | `JD-3` |
| P-9 | "No further progress after step 450" holds for the guard statistic, not for the residuals | — | PC-6 (`claude:481-503`) | **Holds, narrower** `{verify}`: the prefix sums declined from block to block but are noisy from step to step | `JD-4` |
| P-10 | F-09's "resampled training batches" is incomplete: anchor identity dominates the training-batch front's variation | — | PC-7 (`claude:505-519`) | **Holds, narrower** `{verify}` | — |
| P-11 | "Proven healthy at initialization" is narrower than it sounds: GATE-04's controlled-reduction condition passes by construction, and its probe cases are single-trajectory | — | PC-8 (`claude:521-536`) | **Holds, narrower** `{verify}`: five distinct network seeds, not six; five of the six cases are synthetic | `JD-0`; `OQ-1` |
| P-12 | Every "epoch" in the code is one optimizer step | — | PC-9 (`claude:538-552`) | **Holds, narrower** `{verify}`: the spec's Phase-34 rule of once-per-epoch replay coverage presupposes a pass over the pool | `OQ-2`; `JD-7` |
| P-13 | `B2` improved the physics/data balance, but the binding imbalance was always IC against the rest | — | PC-10 (`claude:554-563`) | **Holds, narrower** `{verify}`: per-step physics/data ratio 21.6–243× (not 16–520×); IC/data 2.1 × 10⁶ – 2.1 × 10⁸ | `JD-2` |
| P-14 | The package's verbatim and arithmetic premises hold | (register, `codex:410-446`) | PC-11 (`claude:565-580`), §2.13 | **Holds** `{verify}` | — |
| P-15 | Monitor robustness was never part of invariant B's test surface | — | PC-12 (`claude:582-594`) | **Holds** `{verify}`; the learning-rate scaling of the noise was not tested | `JD-4` |

**Four facts the verification found that neither report states** `{verify}`
(`V:309-327`):

1. **The replay-coverage rule.** The spec's Phase-34 batch contract says
   the replay set is "sampled without replacement across the epoch
   (standard once-per-epoch coverage)" (`ctl_instruction.md:1829`). The
   code instead draws each batch independently. The rule is met only under
   the code's one-step reading of "epoch".
2. **The data term is per-slot.** It fits 32 observed snapshots from each
   of the 256 selected trajectories every step (`controllers.py:1865`). So
   the run was per-slot data fitting with single-anchor IC and physics.
3. **The input layer grew ×1.080 while the output layer shrank ×0.668.**
   This works against a pure amplitude-shrinkage account.
4. **The IC term's anchoring is preserved design.** Phase 57 kept it on
   purpose (`57-02-PLAN.md:87`, "Preserve IC, angular-momentum, optimizer,
   and curriculum behavior outside this bounded seam per D-01/D-16"), and
   the spec's `L_IC` states no batch rule.

### The re-frame determination, carried

The ruling is quoted in its essentials (`DELIVERY-NOTE.md`, "Re-framing ruling
(2026-10-07)"):

- **R-1** `{ruling R-1}`: "The round is re-framed, not re-commissioned." The
  answers "are read through the re-framed question: *what did the executed run
  show, and what must change, starting with conformance, before a run can test
  the ratified recipe?*"
- **R-2** `{ruling R-2}`: the three answer classes in the attribution table
  above.
- **R-3** `{ruling R-3}`:
  - **The default.** "The owner's 2026-09-07 Option A instruction stands:
    physics contributions come from every selected slot." "The
    consolidation presents conformance as decision D0 with that instruction
    as its default."
  - **Consequences, not choices.**
    - Any fix to selected-slot semantics triggers re-measuring `R_ref` and
      re-running GATE-04.
    - A graded run before conformance is restored would again not test the
      recipe.
    - The next conformance gate must test what the loss evaluates.
  - **The IC term.** "The IC term's batch behavior is its own decision."
- **R-4** `{ruling R-4}`: the v2.3 verdict `rethink` stands. Its recorded
  rationale is annotated as unsupported, because the corrected recipe's
  physics term did not run.
- **R-5** `{ruling R-5}`: Claude's training- and validation-data reads are
  permitted, since they spend nothing and no test-split file was opened.
- **R-6** `{ruling R-6}`: fan-out is closed. The two reports are the round's
  evidence.

**Consequence for the joins below** `{join}`:

- No answer is discarded for resting on the false premise. Both reports
  found that premise themselves and built their diagnoses on the corrected
  one.
- Every diagnosis row carries its R-2 class instead, and option flags name it
  where it matters.

## JOIN-2-SOURCE-METHOD — the identification, and the primary-source reading

### The identification converges

| Element | Codex | Claude | trainex-r3 JOIN-2 | Verdict |
|---|---|---|---|---|
| The method | Sifan Wang, Shyam Sankaran, Paris Perdikaris, *Respecting causality for training physics-informed neural networks*, *Computer Methods in Applied Mechanics and Engineering* 421, 116813 (2024); preprint arXiv:2203.07404 (2022) (`codex:85`) | the same; the preprint title is "Respecting causality is all you need for training physics-informed neural networks", v1 only; journal text not accessed (`claude:963-973`) | the same paper (`r3-resolution:246`) | verification rows `D-L1`, `G-1`: `CONFIRMED` · `NOT-VERIFIABLE-HERE` `{verify}`; **`LR-1` `CONFIRMED`** `{lit}` |
| The practitioner restatement | Wang, Sankaran, Wang, Perdikaris, *An Expert's Guide to Training Physics-informed Neural Networks*, arXiv:2308.08468 (2023) (`codex:89`) | the same (`claude:977-979`) | the same (`r3-resolution:247`) | **`LR-13` `CONFIRMED`** `{lit}` |
| The authors' code | `PredictiveIntelligenceLab/CausalPINNs`, `KS/chaotic_KS.py` (`codex:87`) | the same repository at `0d1d83f`, plus `jaxpi` (`claude:982-984`) | the vendored PINA solver, which cites the same paper (`r3-resolution:250`) | **`LR-6`, `LR-12` `CONFIRMED`** `{lit}`; `jaxpi` not read (`LR-24`) |

**The join point's resolve-first condition is met** `{join}`.

- Both reports name the same method by authors, title, venue, volume,
  article number and year, and so did trainex-r3.
- Nothing about the identification needs resolving before the diagnoses are
  read.

### How the primary-source reading was done

R-7 requires a primary-source reading of the facts about the source method
that the reports state. The Rule-19 verification had routed all of them
`NOT-VERIFIABLE-HERE` (`V:517-530`).

- **What was read.** On 2026-10-07 the consolidator downloaded each source's
  arXiv TeX source or code archive. Each went into its own empty directory
  in the session scratchpad, was hashed, and was searched by text.
- **What was not run.** No downloaded file was executed.
- **Where the files are.** They are not committed, since they are other
  people's copyrighted work. The digests below let anyone re-fetch them and
  confirm the same bytes.
- **How quotations are located.** By file and line inside the TeX source or
  code. The reports' PDF page numbers were not re-checked, because no
  PDF-text tool was available.

| ID | Source | Retrieved from | SHA-256 of the retrieved file |
|---|---|---|---|
| `S-A` | Wang, Sankaran, Perdikaris, arXiv:2203.07404**v1** (TeX source; the only arXiv version) | `https://arxiv.org/e-print/2203.07404v1` | `7dafba6f20280a2b54da6c8f02e2f77bca0de6773eb8d7c59cb307f89da5750b` |
| `S-B` | The authors' code, `PredictiveIntelligenceLab/CausalPINNs` at commit `0d1d83f87f6fa2d6756d0e35cac94a7be6183841` (2024-02-16, the `main` head on 2026-10-07) | `https://codeload.github.com/PredictiveIntelligenceLab/CausalPINNs/tar.gz/0d1d83f87f6fa2d6756d0e35cac94a7be6183841` | `ed5e4b10492f4560e2dc36b5aac558c00f53f92f11a871725db567ed6103712d` |
| `S-C` | Wang, Sankaran, Wang, Perdikaris, arXiv:2308.08468**v1** (TeX; the only version) | `https://arxiv.org/e-print/2308.08468` | `6b0c45a5a176ef33ce877be536a58ef9f9a003d2067e2e787ae5bfb88bd90821` |
| `S-D` | Crossref record for DOI `10.1016/j.cma.2024.116813` (metadata only) | `https://api.crossref.org/works/10.1016/j.cma.2024.116813` | — (metadata quoted below) |
| `S-E` | Wang, Teng, Perdikaris, arXiv:2001.04536**v1** (TeX); Crossref record for DOI `10.1137/20M1318043` | `https://arxiv.org/e-print/2001.04536` | `fe0a68f67eb98318c3d32d06e47c0218efdd8beba463bfd4cf15f3678d0b2316` |
| `S-F` | Wang, Li, Chen, Perdikaris, *PirateNets*, arXiv:2402.00326**v3** (TeX) | `https://arxiv.org/e-print/2402.00326` | `09e4f59cdefedbafa5c936c82d2aa5bd7fadf3cc79c6032a8ee8497eb439e537` |
| `S-G` | Sitzmann, Martel, Bergman, Lindell, Wetzstein, arXiv:2006.09661**v1** (TeX) | `https://arxiv.org/e-print/2006.09661` | `4d1f1af51c8af7cf593d5293d5e7f9b78184cfb0e992fda4e137ffb83b88d992` |
| `S-H` | Noorizadegan, Young, Hon, Chen, arXiv:2310.15690**v2** (TeX) | `https://arxiv.org/e-print/2310.15690` | `7e8ba497f5b88cabe95ca5bb8b9a89094d6d56410a185b3ed3abb1b286101512` |

The version of each unsuffixed download is the latest arXiv version on the
retrieval date, as the arXiv API reported it. A later revision would change
the digest.

**Verdict vocabulary for this reading.** It uses the round's closed set,
with one addition:

- `CONFIRMED`, `CONFIRMED-NARROWER` and `REFUTED` have their usual meanings.
- `NOT-READ` means the source was not reached in this reading. It says
  nothing about whether the claim is true.

### The literature ledger

| ID | Claim, as the reports state it | Stated by | What the primary source says, and where | Verdict |
|---|---|---|---|---|
| `LR-1` | The method is Wang, Sankaran & Perdikaris: arXiv:2203.07404 (2022), published in *CMAME* 421 (2024), article 116813 | `{both}` | `S-A` `main.tex:81` gives the preprint title "Respecting causality is all you need for training physics-informed neural networks". `S-D` gives the title "Respecting causality for training physics-informed neural networks", *Computer Methods in Applied Mechanics and Engineering*, volume 421, article 116813, issued March 2024, authors Sifan Wang, Shyam Sankaran, Paris Perdikaris. The authors' own README at `S-B` cites the same journal record | `CONFIRMED` |
| `LR-2` | The weights are exclusive-prefix exponentials, `w_i = exp(−ε Σ_{k<i} L_r(t_k, θ))`, with ε called the causality parameter | `{both}` | `S-A` `main.tex:288-291`: "w_i = exp(−ε Σ_{k=1}^{i−1} L_r(t_k, θ)) … where ε will be referred to as a *causality parameter* that controls the steepness of the weights". In the code (`S-B`), `M = np.triu(np.ones((n_t, n_t)), k=1).T` is strictly lower-triangular, so the prefix is exclusive | `CONFIRMED` |
| `LR-3` | The weights are detached from the gradient | `{codex}` (`codex:85`) | `S-A` `main.tex:367`: "We use `lax.stop_gradient` in our JAX implementation to prevent gradient back-propagation through the computation of w_i." All four scripts in `S-B` wrap the weights in `lax.stop_gradient`, and `S-C` says the same at `main.tex:297` and `:435` | `CONFIRMED` |
| `LR-4` | The paper reports sensitivity to ε and prescribes annealing it upward | `{claude}` (`claude:999-1004`) | `S-A` `main.tex:356-357`, verbatim: "choosing a large ε value can result in a more difficult optimization problem, because the temporal residuals at earlier times have to decrease to a very small value … we employ an annealing strategy for adjusting ε using an increasing sequence of values {ε_i}, which gradually increases the strength with which the PDE residual constraint is enforced" | `CONFIRMED` |
| `LR-5` | Algorithm 1: ε runs over [10⁻², 10⁻¹, 1, 10, 10²] with at most S steps each; a stage ends when `min_i w_i > δ`; the recommended values are λ_ic = 10³ and δ = 0.99 | `{both}` (`codex:85`; `claude:1005-1009`) | `S-A` `main.tex:374-407`: "The recommended hyper-parameters are λ_ic=10³, δ = 0.99 and {ε_i} = [10⁻², 10⁻¹, 10⁰, 10¹, 10²]". **Detail:** in the printed algorithm, the IC term `λ_ic L_ic` is the `t_0` term of the weighted loss with `w_0 = 1`, and the printed exponent sums residual terms `k ≥ 1` only | `CONFIRMED` |
| `LR-6` | The authors' code includes the IC loss in the causal exponent | `{codex}` (`codex:87`); Claude does not discuss it | `S-B`: `W = lax.stop_gradient(np.exp(- tol * (self.M @ L_t + L_0)))` with `L_0 = 1e4 * self.loss_ics(params)` (`KS/chaotic_KS.py:165-168`). The same form is at `KS/regular_KS.py:191` and `NS/NS.py:299`, with `L_0` weighted 10³ (`KS/regular_KS.py:188`) and 10⁵ (`NS/NS.py:296`). The Lorenz script imposes the IC exactly and has no IC loss (`Lorentz/Causal_PINNs_lorentz.py:198`). So in every soft-IC script the IC loss multiplies every causal weight by `exp(−ε·L_0)`. **The printed Algorithm 1 differs on this point** (`LR-5` detail) | `CONFIRMED` |
| `LR-7` | The optimizer is Adam with exponential decay of 0.9 every 5,000 iterations; time-marching windows are used | `{both}` (`codex:85-87`; `claude:1046-1048`) | `S-A` `main.tex:488`: "the Adam optimizer with default settings and an exponential learning rate decay with a decay-rate of 0.9 every 5,000 training iterations … we will also employ time-marching". `S-B` matches for KS and Lorenz (`decay_steps=5000`). The NS script uses 10,000 (`NS/NS.py:221-223`) | `CONFIRMED` |
| `LR-8` | Budgets are 10⁵–3 × 10⁵ iterations per ε stage per time window | `{both}` (Codex: "much larger", `codex:215`; Claude `claude:1049-1050`) | `S-A` `appendix.tex:70-91`, maximum iterations per tolerance per window: Allen–Cahn 3 × 10⁵ (1 window), Lorenz 1 × 10⁵ (40 windows), KS 2 × 10⁵, NS 1 × 10⁵. The caption: "'Max Iteration' is the maximum iteration for every tolerance ε in each time window" | `CONFIRMED` |
| `LR-9` | Training is expected to open the weights progressively until all reach 1; `min_i w_i > δ` is the stopping and convergence criterion | `{both}` (Codex: "Earlier residual descent opens later weights", `codex:85`; Claude `claude:1026-1042`) | `S-A` `main.tex:351-353`: "the initial temporal weights are all zero except for t = 0 … Throughout the rest of the training, more temporal weights are activated, and eventually, all of them converge to 1 as the PDE residual loss is properly minimized … one can choose to terminate training of min_i w_i > δ … this stopping criterion not only helps to train a PINNs model faster, but it actually yields trained models with superior predictive accuracy" | `CONFIRMED` |
| `LR-10` | Training past the criterion gave slightly lower loss but less accurate Lorenz predictions | `{claude}` (`claude:1036-1038`) | `S-A` `main.tex:503`: "the training losses can achieve slightly lower values … However, the model predictions are less accurate … it appears that training the model for more iterations after the proposed stopping criterion has been met seems to give rise to over-fitting" | `CONFIRMED` |
| `LR-11` | Lorenz used 40 windows of Δt = 0.5, a 5 × 512 MLP, an exact IC, N_t = 256 full batch, and reached relative L² errors of about 10⁻² | `{claude}` (`claude:1051-1053`) | `S-A` `appendix.tex:51` (MLP, depth 5, width 512, N_t 256); `appendix.tex:127-142` (40 windows of Δt = 0.5; exact IC `x̂ = x_θ·t + x(0)`; N_t = 256, full batch); `main.tex:503` (relative L² 1.139 × 10⁻², 1.656 × 10⁻², 7.038 × 10⁻³) | `CONFIRMED` |
| `LR-12` | The authors' Lorenz code differs from the printed settings (σ, T, ε list, iteration caps); the smallest ε in the authors' code is 10⁻³ | `{claude}` (Claude G-13, `claude:1624`; L-2, `claude:1074`) | `S-B` `Lorentz/Causal_PINNs_lorentz.py`: σ = 10 (`:263`) against the printed σ = 3 (`S-A` `main.tex:501`); T = 30 (`:268`) against 20; `tol_list = [1e-3, …, 1e1]` (`:277`) against the printed default [10⁻², …, 10²]; 300,000 iterations per tolerance (`:298`) against 1 × 10⁵; `n_t = 300` (`:122`) against 256. 10⁻³ is also the smallest tolerance in `KS/chaotic_KS.py:276` and `NS/NS.py:419` | `CONFIRMED` |
| `LR-13` | The later guide uses a fixed causal tolerance (default 1.0) with 16 or 32 chunks and 10⁵–3 × 10⁵ steps, and advises reducing ε when the weights cannot reach 1 | `{both}` (`codex:89`; `claude:1010-1016`) | `S-C` `main.tex:297`: "The recommended default values for hyper-parameters are as follows: f=1,000, α=0.9, γ=1.0, ε=1.0". `main.tex:438`: "we recommend choosing a moderately large ε to ensure that all temporal weights can properly converge to 1 at the end of training. If this is not the case, it would be advisable to slightly reduce the value of ε". `appendix.tex:239-517`: every listed example uses causal tolerance 1.0, 16 chunks in three examples and 32 in two, with 1 × 10⁵ to 3 × 10⁵ training steps. Claude's values from `jaxpi` (0.1, 5.0, 10⁻²) were not read (`LR-24`) | `CONFIRMED` |
| `LR-14` | The guide balances losses by gradient norm and says residual losses cannot be normalized in pre-processing | `{both}` (`codex:89`; `claude:1017-1023`, `:1093-1095`) | `S-C` `main.tex:268-284`: λ̂_ic = (‖∇L_ic‖ + ‖∇L_bc‖ + ‖∇L_r‖)/‖∇L_ic‖ (likewise for each term), updated every f steps by the moving average λ_new = α·λ_old + (1 − α)·λ̂_new. `main.tex:447`: "These losses cannot be normalized during the pre-processing step" | `CONFIRMED` |
| `LR-15` | The guide's optimizer is Adam at 10⁻³ with exponential decay of 0.9 every 2,000 steps | `{claude}` (`claude:1054-1056`) | `S-C` `main.tex:588`: "the Adam optimizer, starting with a learning rate of 10⁻³ and an exponential decay with a decay rate of 0.9 for every 2,000 decay steps" | `CONFIRMED` |
| `LR-16` | No causal-training source uses cosine annealing or an L-BFGS hand-off | `{both}` (Codex: "not this project's cosine schedule", `codex:85`; Claude, silences 6–7, `claude:1057-1059`) | No occurrence of "cosine" or "L-BFGS" in `S-A`, `S-C`, or any script in `S-B`. A silence can only be confirmed for the sources read | `CONFIRMED` |
| `LR-17` | ε multiplies raw residual losses, and no source normalizes by a reference measured at initialization | `{both}` (Codex: η_raw = 1/`R_ref` ≈ 5.06 × 10⁻¹¹, `codex:91-95`; Claude `claude:1017-1020`) | `S-A` `main.tex:288-291` (ε on `L_r`, a raw mean square); `S-B` `KS/chaotic_KS.py:165-167` (`L_t = np.mean(r_pred**2, axis=1)`); `S-C` `main.tex:447`. No initialization-reference normalization in the sources read | `CONFIRMED` |
| `LR-18` | Gradient imbalance is a documented failure mode; Claude's `D1-A` cites "the gradient-norm balancing of Wang, Teng & Perdikaris 2021 and the 2023 expert's guide"; the two papers use opposite moving-average conventions | `{claude}` (`claude:1086-1097`, `:1410`) | `S-E` (Crossref: *Understanding and Mitigating Gradient Flow Pathologies in Physics-Informed Neural Networks*, *SIAM J. Sci. Comput.* 43(5), A3055–A3081, 2021). `main.tex:102-104`: "stiffness in the gradient flow dynamics", "an unstable imbalance in the magnitude of the back-propagated gradients", "an adaptive learning rate annealing algorithm". **But its rule is not a norm ratio:** λ̂_i = max_θ\|∇_θ L_r\| / mean\|∇_θ L_i\| (`main.tex:425-430`), updated as λ_i = (1 − α)λ_i + α·λ̂_i with α = 0.9 (`main.tex:432-445`). The norm-equalizing form is the guide's (`LR-14`). The conventions are indeed opposite | `CONFIRMED-NARROWER` |
| `LR-19` | PirateNets attributes deep-PINN degradation to initialization; it starts its residual gates at α = 0, and α = 1 collapses deeper models | `{claude}` (`claude:1105-1114`) | `S-F` `main.tex:149`: "non-suitable initialization schemes, which result in poor trainablity [sic] for the network derivatives". `main.tex:531`: "we initialize α^(l) to zero for all blocks, leading to the final output of a PirateNet … being a linear combination of the first layer embeddings at initialization". `main.tex:880`: "setting α=1 at initialization results in complete model collapse for deeper networks". The journal venue was not checked | `CONFIRMED` |
| `LR-20` | SIREN chose ω₀ = 30 so the first layer's sine spans multiple periods over [−1, 1] | `{both}` (`codex:180`; `claude:1115-1124`) | `S-G` `sections/representation.tex:104`: "we propose to initialize the first layer of the sine network with weights so that the sine function sin(ω₀·Wx + b) spans multiple periods over [−1,1]. We found ω₀=30 to work well for all the applications in this work." Claude's "5-layer MLPs" detail was not checked | `CONFIRMED` |
| `LR-21` | The power-enhanced skip-network source uses tanh and no LayerNorm, and finds a power of 2 effective below 30 hidden layers | `{claude}` (`claude:1125-1136`) | `S-H` (arXiv journal reference: *Applied Mathematics and Computation* 480 (2024) 128910). `Amir-et-al-24.tex:194` (tanh); `:432`: "a power of 2 is effective for networks with fewer than 30 hidden layers"; no occurrence of LayerNorm, BatchNorm or "normaliz" in the source. This agrees with the spec's statement that the LayerNorm is the project's own addition (`pinn_architecture.md:211-213`) | `CONFIRMED` |
| `LR-22` | Any change of method in the 2024 journal text | `{claude}` (Claude G-13) | The DOI resolves to a publisher redirect page with no article text; not read | `NOT-READ` |
| `LR-23` | PINNs on a chaotic double pendulum converge to solutions that violate the IC "only marginally" yet diverge (Steger, Rohrhofer & Geiger, NeurIPS 2022 workshop) | `{claude}` (`claude:1098-1104`) | Not found on arXiv or in Crossref. Claude's own reading was abstract-only. Its R2.4 argument (`claude:780`) is first-principles and does not depend on it | `NOT-READ` |
| `LR-24` | The `jaxpi` configurations use tolerances 1.0, 0.1, 5.0 and 10⁻² | `{claude}` (`claude:1015-1016`) | Not downloaded. The decision-relevant point, a fixed tolerance of 1.0, is confirmed from the guide's own tables (`LR-13`) | `NOT-READ` |
| `LR-25` | Krishnapriyan et al. (NeurIPS 2021), Penwarden et al. (*J. Comput. Phys.* 2023), Breen et al. (*MNRAS* 2020), Greydanus et al. (NeurIPS 2019) | `{claude}` (`claude:1137-1153`) | Context only; no option rests on them | `NOT-READ` |

### What the reading changes

- **It refutes no fact either report states.** Seventeen of the
  source-method facts are confirmed, as are three of the four papers that
  options cite.
- **One citation is narrowed (`LR-18`).** Claude's `D1-A` attributes
  "gradient-norm balancing" to both the 2021 paper and the 2023 guide. Only
  the guide's rule is a norm ratio. The option itself is unaffected,
  because the guide is a sufficient source for it.
- **One source fact matters for the IC decisions, and neither report builds
  an option on it** `{join}`.
  - **The fact.** In the authors' soft-IC code, the IC loss sits inside the
    exponent and gates every causal weight (`LR-6`).
  - **What it means.** The causal sweep cannot open until the IC fit is
    good. The printed algorithm instead keeps the IC as an always-weighted
    separate term.
  - **Who states it.** Codex states the fact. Claude's L-5 departure row
    frames the source's IC treatment as "strongly enforced" through λ_ic or
    a hard IC.
  - **Where it is recorded.** As an observation bearing on `JD-1` and
    `JD-2`, not as an option.
- **The earlier round's unchecked rows are now settled** `{join}`.
  - **Calibration facts.** trainex-r3's verification routed the published
    half of its source-method rows `NOT-VERIFIABLE-HERE`
    (`r3-resolution:244-251`). This reading confirms the ε sequence, δ =
    0.99, λ_ic = 10³ and the guide's ε = 1.0 (`LR-5`, `LR-13`).
  - **Departures r3 called faithful.** Its open-book report said the
    project's exclusive prefix and its stop-gradient on the weights are
    faithful to the source; the paper's side of both is now confirmed
    (`LR-2`, `LR-3`).
  - **New in this round.** The trainex-r3 record states no source
    learning-rate schedule or iteration count (`F-H4c`, `V:503`). This round
    adds them (`LR-7`, `LR-8`).

### The departures from the source, joined

The reports list the points where this project departs from the source. Both
lists are joined here; nothing is adjudicated.

| Departure | Codex | Claude | Source side (`LR` rows) | Project side (verification rows) |
|---|---|---|---|---|
| **The causal coefficient.** The source anneals it over four decades with a δ stop (2022), or fixes 1.0 with long budgets (2023). Here `η_c = 1` is fixed and continuation was explicitly declined | the fixed value "is not itself a violation of the published method family" (`codex:89`) | L-1 | `LR-5`, `LR-13` | verification `G-5` `CONFIRMED` (`54-RULING.md:50`, "do not add coefficient continuation") |
| **What ε multiplies.** In the source, raw residuals, which makes ε an absolute tolerance. Here residuals are divided by a frozen initialization reference, so the effective raw coefficient is 1/`R_ref` ≈ 5.06 × 10⁻¹¹ | `codex:91-95` | L-2 | `LR-17`, `LR-12` | verification `G-6` `CONFIRMED-NARROWER`: 7.3–8.3 orders below the smallest published values (10⁻³ in code, 10⁻² in print), not 8–9 |
| **The progress indicator.** The source's `min w → 1` is a success and stopping criterion. Here the front `max{n : w_n > 0.5}` carries a 500-step no-advance failure guard | "half-weight front, timeout" (`codex:98`) | L-3 | `LR-9` | verification `G-7` `CONFIRMED` |
| **The optimizer schedule.** The source uses Adam with slow exponential decay over 10⁵–3 × 10⁵ steps. Here a cosine decays to zero over 1,000 steps, and the L-BFGS hand-off is unreachable | "short cosine horizon" (`codex:98`) | L-4 | `LR-7`, `LR-8`, `LR-16` | verification `G-7`, `A-P4b` |
| **The IC treatment.** The source enforces the IC strongly: λ_ic of 10²–10⁴ in print (10³–10⁵ in its code), an exact IC, or the IC loss inside the exponent in its code. Here λ_IC = 1 on an un-normalized IC term | "separate IC loss" (`codex:98`) | L-5 | `LR-5`, `LR-6`, `LR-11` | verification `G-7` |
| **How many trajectories.** The source solves single-IC problems with one network per problem or window. Here one IC-conditioned network covers many trajectories, and the run executed it on one anchor | "single-anchor execution" (`codex:98`) | L-6 | silent in the sources read | verification `G-7` |
| **A supervised data term.** The source has none; the project has a Huber data term | — | L-7 | silent | verification `G-7` |
| **The order of the system.** The source's systems are first-order in time; the project's ODE is second-order | — | L-8 | silent | verification `G-7` |
| **The architecture.** The source uses a tanh MLP or modified MLP with tuned Fourier features. The project uses SIREN with ω₀ = 30, 12 layers and an `LN(x)²` power skip | — | L-9 | `LR-20`, `LR-21` | verification `G-7`, `G-8` |
| **The number of chunks.** The source uses 16–32 chunks with tolerance 1. The project uses M = 16 | "16 chunks" (`codex:89`) | L-10 | `LR-13` | verification `G-7` |

## JOIN-3-DIAGNOSES — the diagnoses, joined per question

**How this join reads** `{join}`:

- **Two kinds of difference.** The delivery note separates two cases:
  - **A resolvable disagreement:** both reports name the same mechanism but
    weigh its evidence differently.
  - **A diagnostic dispute:** they name different mechanisms for the same
    observation. A dispute goes to an experiment, never to a vote.
- **The "Join" column records which case applies.**
  - `same` means the same mechanism with compatible confidence.
  - `same, weighed differently` means the same mechanism with different
    confidence or evidence. That is resolvable, and the column names the
    experiment that resolves it.
  - `one report` means only one report names the mechanism.
- **The "Class" column is the R-2 class of the evidence the row rests on.**
- **Row IDs** (`J1.a`, …) are this document's own.

**No question has a diagnostic dispute.** In every question where both reports
name a mechanism for an observation, they name the same mechanism.

### Q1 — the invariant-B window and the learning-rate schedule

**Joined answer.**

- **Where both stand.** Neither report finds the decaying learning rate to
  be the established cause of the trip.
  - Codex calls it "a plausible contribution to slowing" that "the evidence
    does not isolate" (`codex:102`).
  - Claude rates it LOW as the cause of the trip, though MEDIUM–HIGH as a
    throttle on the last ~100–150 steps (`claude:692`).
  - Both rank the identity failure and the IC-directed gradient as stronger.
- **What Claude adds.** It states the window/schedule pairing as a
  structural flaw: a unit mismatch between raw steps and optimizer motion
  (`claude:667-686`). R-2 lists that interaction among the structural
  findings.

| Row | Joined mechanism | Codex | Claude | Join | Class | Verified form; what settles it |
|---|---|---|---|---|---|---|
| `J1.a` | **Learning-rate starvation.** The decay inside the window reduces optimization opportunity | medium as a contributor, low as the sole cause (`codex:106`) | M1.1: LOW as the cause of the trip; MEDIUM–HIGH that it throttled the last ~100–150 steps (`claude:692`) | same | `E` | `F-Q1b` narrowed: trajectory 28's late steepening reproduces, but anchor 1 peaks in the middle third. `F-Q1j` **refuted**: the schedule held 0.09 full-rate steps after step 951, not 0.6, which strengthens the point that it could not supply the ~340 steps the trend needed. Settled by `JX-7` |
| `J1.b` | **Unit mismatch.** The window is 500 raw steps; the cosine over 1,000 steps holds about 500 full-rate-equivalent steps in total, and a window opening at step 450 held 118 of them (23.6 %) | not quantified; "a longer timeout alone does not correct the zero-refinement-budget issue" (`codex:294`) | the structural flaw (`claude:676-686`) | one report | `S` | `F-N1`: N_eff 118.0 of 499.4 `CONFIRMED` |
| `J1.c` | **Record-statistic artefact.** The guard is a monotone high-water mark of one trajectory's thresholded, noisy prefix sum: noise sets records at high learning rate, and only trend can at low | as Q5's threshold sensitivity (`codex:227`); not named under Q1 | M1.2: HIGH (`claude:693`) | one report under Q1; the same phenomenon as Codex's Q5 row | `S` for the statistic; `E` for the timing evidence | Generations 6 and 7 advanced at steps 353 and 450 on identical batches (`B-PC4e`). Settled by `JX-2`, and by a per-step monitor trace (`JD-10`) |
| `J1.d` | **The IC term dominated the update; physics was not trained** | high for gradient domination, medium for its causal contribution; "pre-Adam gradient domination, not zero physics influence after coordinatewise moment normalization" (`codex:107`, `:119`) | M1.3: HIGH that physics learning was negligible; MEDIUM that head shrinkage is the main channel (`claude:694`) | same, weighed differently: Claude adds Adam's algebra, the optimizer-state statistic and the natural experiment | `S` as a design concern; `E` for the magnitudes | P-7 narrower: the data term trained on all slots; the input layer grew. Settled by `JX-1` (the Adam-preconditioned share) |
| `J1.e` | **Biased, changing anchors.** The objective is uneven, and the monitor trajectory was the anchor on only 31 of 951 steps | high for the mechanism; contribution unquantified (`codex:108`) | M1.4: MEDIUM; exposure and difficulty are confounded (`claude:695`) | same | `S` for the mechanism (it is the non-conformance); `E` for the rates | `F-Q1f` narrowed: the \|Δv′\| figures are √(IC loss). Settled by `JX-3` |
| `J1.f` | **Gradient clipping** suppressed progress | contradicted: the clip never binds; the largest norm/threshold ratio is 0.741 (`codex:109`, `:121`) | the clip never bound; peak 0.73 (`claude:341`) | same: rejected by both | `S` | `D-Q1c`, `B-PC2c` `CONFIRMED` |

**Against the front-advance condition** `{both}`: at the trip, the prefix over
bins 0–2 was 1.1891 and must fall below 0.6931, a 41.7 % fall (`codex:123-129`;
`claude:697-709`). `D-Q1h` `CONFIRMED`.

**How the two should relate.** This is an options question, carried into
`JD-4` and `JD-5`.

### Q2 — relative front or absolute accuracy

**Joined answer** `{both}`.

- **What the front is.** Both call the `R_ref`-relative front an
  optimization or pacing diagnostic that cannot certify physical accuracy
  (`codex:137`; `claude:741-752`).
- **What a full front permits.** A full front requires only that the mean
  normalized residual over bins 0–14 be below 0.0462, a raw mean below
  9.1263 × 10⁸. That bounds neither bin 15, nor the IC error, nor the
  trajectory error.
- **Class.** This is structural (R-2 lists it).

| Row | Joined mechanism or reading | Codex | Claude | Join | Class | Verified form; what settles it |
|---|---|---|---|---|---|---|
| `J2.a` | **The front cannot certify accuracy.** A full front still permits large residuals | the algebra (`codex:139-155`) | the same, plus the physical scale: the permitted RMS residual is 190× the median true acceleration and 15× its 99th percentile (`claude:754-771`) | same | `S` | `D-Q2a`–`D-Q2c`, `F-Q2a` `CONFIRMED`; Claude's physical-scale figures (`E-E`) reproduce exactly from the 1,812 Stage-0 training trajectories |
| `J2.b` | **The front depends on the reference.** Equal raw errors give different fronts under different `R_ref` | "follows algebraically" (`codex:161`) | implicit in L-2 (`claude:1074`) | same | `S` | `CONFIRMED` |
| `J2.c` | **Shedding initialization amplitude alone moves the front** | relative descent without useful accuracy; "the retained replay and IC telemetry support this possibility" (`codex:159`) | R2.1: HIGH. GATE-04's own condition-(iii) diagnostics show fronts 9–15 after a uniform 0.05 scaling, and 15 in all six cases after 0.01 (`claude:777`, `:765-769`) | same; Claude adds the GATE-04 evidence | `S` (a property of the reference construction) | `F-Q2c` `CONFIRMED` |
| `J2.d` | **Relative progress did not move the in-run absolute metric** | useful accuracy emerging with relative descent is "not established" (`codex:160`) | R2.2: MEDIUM; `eps_H` flat at 0.983–0.990 (`claude:778`) | same | `E` | P-8 `CONFIRMED`. Settled by `JX-4` |
| `J2.e` | **A front can advance with the IC unmet once physics is rebalanced** | the front "does not bound … IC error" (`codex:155`) | R2.4: MEDIUM (analysis) (`claude:780`) | same | `S` (first principles) | The literature support Claude cites is `LR-23` `NOT-READ`; the argument does not depend on it |

### Q3 — the SIREN scale and the power-skip stack

**Joined answer** `{both}`.

- **No proven root.** Neither `first_omega_0 = 30` nor the skip stack is
  established as the root cause (`codex:167`; `claude:801-805`).
- **No universal fourth-power law.** Both reject a universal ω₀⁴ law for
  this stack, for the same reason: LayerNorm's scale invariance
  (`codex:182-196`; `claude:826-833`).
- **What would settle it.** A decomposition on the project's own model,
  which neither report could run (Claude G-3).

| Row | Joined mechanism | Codex | Claude | Join | Class | Verified form; what settles it |
|---|---|---|---|---|---|---|
| `J3.a` | **The initialization derivative scale created the conditions for IC dominance** | compatible with the telemetry (`codex:175`) | M3.1: HIGH that the scale feeds them; MEDIUM on "root" (`claude:844`) | same | `S` | `F-Q3a` `CONFIRMED` (‖v′‖ 239–327 at initialization) |
| `J3.b` | **Where the amplification sits.** The first layer contributes at most 2.14 per unit τ, against an effective 585–847 per unit u, so most amplification arises after the first layer | lists high first-layer frequency as an admitted mechanism, with no position/velocity split (`codex:175`) | M3.2a: LOW that the first layer is where it happens; M3.3: MEDIUM that the stack builds most of it (`claude:845`, `:847`) | same, weighed differently: Claude's bound narrows Codex's row to ω₀ acting as a lever through the stack. Codex's mechanism is not excluded, because ω₀ multiplies the derivatives the stack passes on | `S` | `F-Q3b`, `F-Q3c` `CONFIRMED` (v′/r′ narrowed to 221–359). The input layer grew ×1.080 in training. Settled by `JX-5` |
| `J3.c` | **How strong a lever ω₀ is** | rejects a universal extrapolation "without proving the prior alternative empirical exponent" (`codex:196`) | M3.2b: UNDETERMINED; LayerNorm crossover near ω₀ ≈ 7 (rough estimate) (`claude:846`) | same | `S` (analysis) | `F-H4d`: the trainex-r3 clean-room figures remain `NOT-VERIFIABLE-HERE`. Settled by `JX-5` |
| `J3.d` | **The residual's composition.** Force/acceleration cancellation (Codex), against curvature domination at initialization, R̄ ≈ ‖a′‖²/3 (Claude) | "no retained component decomposition" (`codex:177`) | R2.1's identity holds to four figures at initialization (`claude:777`) | related: Claude's identity shows the residual is curvature-dominated at initialization, which argues against cancellation there; no decomposition exists after training | `S` | `F-Q2d` `CONFIRMED`. Settled by `JX-5` (the component split) |
| `J3.e` | **Uneven single-anchor exposure drives the behavior** | needs measurement (`codex:178`) | as M1.4 and M5.2 | same | `S` / `E` | `JX-3` |
| `J3.f` | **The AD path and IC reduction carry no stray factor** that would explain the large IC term | `codex:169` | — | one report | `S` | `D-Q3a` `CONFIRMED` |

### Q4 — the Stage-0 step budget

**Class `V`: the answer is void, and the question stays open** `{ruling R-2}`.

- **What both reports say.** No defensible budget follows from this
  evidence (`codex:202`; `claude:867-871`), and the budget must be measured
  under the corrected recipe (`codex:217`; `claude:899`, `:902`).
- **What the ruling adds.** It voids any number derived here.
- **What is carried as findings:**
  - **Structural (`S`) facts:**
    - The configuration had no refinement headroom (P-4).
    - The spec's per-stage budget is provisional (`ctl_instruction.md:1994-1997`).
    - "Epoch" means one optimizer step in the code (P-12), and the spec's
      once-per-epoch replay rule assumes otherwise (`OQ-2`).
  - **Empirical (`E`) figures, labelled as such by their authors:**
    - Codex's 5.60× further reduction needed on the first six bins
      (`codex:204`).
    - Claude's 1,900-step amplitude-shedding extrapolation (`claude:881-888`).
  - **Literature.** Published budgets of 10⁵–3 × 10⁵ iterations per stage
    per window are confirmed (`LR-8`). Both reports say they do not
    transfer as a number (`codex:215`; `claude:889-892`).
  - **Cost.** About 12 s per step on this hardware (mean 12.07; `F-Q4a`).
    That is a cost figure for planning, not a recipe value.

### Q5 — the oscillation between bins 1 and 2

**Class: R-2 voids Q5's oscillation as a property of the recipe, so it stays
an open question.** What carries over is what the oscillation shows about the
executed run and the guard.

**Joined answer** `{both}`.

- **Threshold hovering, not instability.** The 1↔2 oscillation is a single
  trajectory's prefix hovering near the threshold, not a demonstrated
  dynamical instability (`codex:221`; `claude:911-925`).
- **The training-batch and monitor fronts disagree because they measure
  different trajectories.**
  - Codex rates "Changing training anchors explain batch/monitor
    disagreement" as "Strongly supported by executed identity selection"
    (`codex:229`).
  - Claude rates resampling-hidden instability HIGH against: same-parameter
    resampling moves the prefix only 4–8 % (`claude:933`).

| Row | Joined mechanism | Codex | Claude | Join | Class | Verified form; what settles it |
|---|---|---|---|---|---|---|
| `J5.a` | **Threshold hovering** near ln 2 | supported near the bin-2 boundary; the prefix was 0.7277 at step 900 and 0.5505 at step 951 (`codex:223`, `:227`) | M5.1: HIGH (`claude:931`) | same | `S` for the statistic; `E` for the values | `F-Q5a` narrowed: 0.549–0.553 at steps 931–951 |
| `J5.b` | **Updates on other trajectories perturb the fixed anchor** | compatible with retained snapshots (`codex:228`) | M5.2: MEDIUM–HIGH, cross-anchor interference (`claude:932`) | same | `E` | `JX-3` |
| `J5.c` | **Batch/monitor disagreement comes from changing trajectories, not from hidden instability** | strongly supported (`codex:229`) | M5.3: HIGH against the resampling reading (`claude:933`) | same | `S` (it follows from P-1) | `B-PC1q` `CONFIRMED` (time-resampling noise 4–8 %) |
| `J5.d` | **Numerical instability** | no supporting evidence (`codex:230`) | not claimed | same | `S` | — |
| `J5.e` | **Optimization chaos.** Identical-data runs diverge 3× within about 140 steps | — | M5.4: HIGH (`claude:934`) | one report | `S` as an evidence-design fact (replicates are needed); `E` for the magnitude | `B-PC4e` `CONFIRMED` |
| `J5.f` | **IC hypersensitivity.** The same anchor's IC loss changes about 2× per recurrence at every learning rate | — | `claude:715-720` | one report | `E` | `F-Q1k` narrowed: about 2× holds in every band; the per-band values depend on band edges |

### The prior-analysis rows (H-01 to H-03), joined

Both reports derived each H-row before comparing, as §5.6(e) asked
(`codex:236-250`; `claude:1165-1325`).

| H-row reading | Codex | Claude | Join |
|---|---|---|---|
| H-01 point 1: the flat-profile endpoint arithmetic | agree | agree; the clip never bound | same |
| H-01 point 2: normalization "addresses the established severe physics/data conditioning mismatch" | agree narrowly; IC domination remains severe | agree on physics/data; disagree that conditioning was addressed, because the IC term binds | same |
| H-01 point 3: retain ω₀ = 30 | supported as a cautious diagnostic choice | agree as untested, not refuted; disagree that the frozen reference neutralizes the initialization scale | same |
| H-01 point 4: the 16-bin prefix | agree algebraically; the executed instance differs | agree in principle; the executed instance differs | same |
| H-01 point 5: the clip is a numerical guard | agree | agree | same |
| H-02: "not a near miss" | agree for the trip moment | agree for the trip moment; the prefix was still falling | same |
| H-02: "oscillates; it does not creep" | narrow to observed regression and recovery | disagree with "does not creep" | same direction, different strength |
| H-02: "Two independent runs (gens 6 and 7) stalled at the same index" | disagree | disagree | same |
| H-02: a full front means about a 20× reduction, raw about 10⁹ | a flat profile needs 21.64×; the raw value is an upper bound on a mean | agree (21.6×, or 23.9× from the monitor's start); add the 190× physical scale | same |
| H-03: the source identification | agree after a primary-source reading | agree | same; `LR-1` `CONFIRMED` |
| H-03: the scaling-law dispute | unresolved empirically | unresolved; only `JX-5` settles it | same |

**What Claude adds** `{claude}` (`claude:1264-1325`).

- **The method.** Claude compares trainex-r3's forward statements with the
  outcome of generation 7.
- **The finding.** The r3 open-book report's warning that the IC term would
  dominate (its gap G-9) and its λ_phys-equivalence warning were not
  carried into `54-RULING`'s scientific basis. The run then failed the way
  G-9 anticipated (`claude:1317-1325`).
- **Verification.** The verification rows `F-H4a` to `F-H4j` hold, with two ranges narrowed:
  `F-H4g` (physics/data 1.33–2.39 decades) and `F-H4h` (IC/data 6.3–8.3
  decades).

### Evidence limits, joined

Both reports state that one graded seed and a shared trajectory support no
seed-general conclusion (Codex gap 9, `codex:405`; `claude:1327-1356`).
Claude adds four limits:

- **Event timings.** Because the training dynamics are chaotic, single-run
  event timings ("advanced at step 450") are not estimable quantities.
- **The natural experiment** (n = 57 and 32) bounds a large direct
  physics effect, but cannot exclude a small one.
- **Coverage.** Generalization to never-anchored trajectories was
  measured only through `eps_H`.
- **The "physics untrained" conclusion** rests on global norms, Adam's
  algebra and the natural experiment, not on a direct measurement of the
  update. That is `JX-1`.

## JOIN-4-EXPERIMENTS — the discriminating experiments, pooled

**This list proposes; it performs nothing.** Every experiment here is an
owner-gated proposal.

- **Model computation.** Several of them need forward or backward passes of
  the network on retained checkpoints. That is model computation, which no
  agent may run without the owner's authorization.
- **What a read-only experiment on retained checkpoints can show** `{ruling R-2}`.
  It measures the parameters the single-anchor run produced. It can
  therefore falsify a reading of that run, for example the reading that
  physics was a passenger in the update. Run at initialization, it can measure an architecture
  property. It cannot set or justify a recipe value.
- **Duplicates are merged.** Each stated cost is kept, and so is whether a
  training run is needed.

| ID | What it measures | Codex | Claude | Needs a training run? | Model computation | Runs on | Stated cost | What it can settle |
|---|---|---|---|---|---|---|---|---|
| `JX-1` | **Per-term gradient decomposition** at retained checkpoints (0, 900, 951): g_IC, g_phys and g_data; their cosines; the share of the Adam-preconditioned update along −g_phys (from the stored moments); and the IC term's position/velocity split | fixed-panel decomposition "without training" (`codex:133`); `D1-A` (`codex:270-282`) | `E2` (`claude:1362`) | no | yes: forward and backward on checkpoints | the frozen monitor batch, **and** a conformant multi-slot batch. The second half needs the per-slot code path of `JD-0`, or a verification-only path | minutes (Claude) | whether physics's share of the update was negligible. Claude reads a share of 10⁻⁴ or less as confirming PC-2, and 10⁻² or more as PC-2 overstated (`claude:1362`). Settles `J1.d`, and gives `JD-2` its branch |
| `JX-2` | **Monitor-estimator noise:** trajectory 28's prefix sums under K = 20 fresh stratified time draws at each retained checkpoint | — | `E4` (`claude:1364`) | no | yes: forward | the executed monitor | about 15 min | separates estimator noise from parameter motion (`J1.c`, `J5.a`). The corrected multi-slot monitor's noise band must be re-measured after `JD-0` `{join}` |
| `JX-3` | **Exposure and generalization panel:** prefix profile and IC error at checkpoints 0 and 951 for high-exposure anchors, never-anchored training trajectories, and (Claude) validation-split trajectories | a fixed-panel comparison "whether regressions occur across several ICs or primarily the current monitor anchor" (`codex:234`) | `E3` (`claude:1363`) | no | yes: forward | checkpoint parameters, scored per trajectory | about 1 h for 40 trajectory-checkpoints (Claude; its per-unit timing is `F-X2` `NOT-VERIFIABLE-HERE`) | whether the improvement was global (amplitude shedding) or exposure-specific (`J1.e`, `J3.e`, `J5.b`). Validation-split trajectories are not the held-out test split |
| `JX-4` | **Relative against absolute, at retained checkpoints.** Codex: raw residuals, IC errors and trajectory errors on fixed training-only fixtures. Claude: the monitor batch with each slot's residual divided by its true ‖a′‖² scale | `codex:163` | `E9` (`claude:1369`) | no | yes: forward | checkpoint parameters | minutes (Claude) | where an absolute criterion would sit against the front (`J2.d`). It informs the choice of physical normalization in `JD-3`. Tolerance values are recipe values that a single-anchor measurement may not set `{ruling R-2}` |
| `JX-5` | **Initialization-only architecture decomposition.** Codex: separate acceleration, force, IC position/velocity error, mixed derivatives and skip contributions on the actual stack. Claude: ‖v′‖, ‖a′‖, bin-mean R̄ and per-term gradients on the six GATE-04 cases for ω₀ ∈ {1, 5, 10, 30} × power branch {on, off} × LayerNorm {on, off} (and depth {4, 8, 12}) | `codex:198` | `E5` (`claude:1365`) | no | yes: initialization only | Codex's split runs at the default architecture; Claude's sweep needs a verification-only path that admits non-default `ArchitectureSpec` values (`pinn/architecture_spec.py:71-130` rejects them today) | minutes | apportions the derivative scale between ω₀ and the stack (`J3.b`–`J3.d`). It is not a generation-7 measurement, so its result is structural evidence |
| `JX-6` | **λ_phys = 0 control:** IC and data only, same seed and batch sequence, about 500 steps | — | `E6` (`claude:1366`) | **yes** (diagnostic, not graded) | training | **the executed code** | about 1.7 h | whether the causal physics term mattered to the executed run (tests PC-2 causally). Claude's `D8-C` notes that it "spends compute on a nonconformant recipe" (`claude:1501`) |
| `JX-7` | **Matched constant-rate against cosine arms.** Codex: after conformance verification, identical initialization, draws, monitor, warm-up and update count. Claude: constant lr 5.8 × 10⁻⁴ against the executed cosine on the same batch sequence, at least two numeric replicates each | `codex:131` | `E7` (`claude:1367`) | **yes** | training | Codex: **conformant** code. Claude: unstated in `E7`; its `D8-C` groups E7 with diagnostic runs on the current code | Codex: about 100 min per 500-update arm. Claude: about 3.3 h per 1,000-step replicate | `J1.a` against `J1.c`, and record-timing variance. The presuppositions differ `{join}`: on the current code, the result describes the single-anchor run |
| `JX-8` | **Calibration pilot, or staged diagnostic extensions, under the corrected recipe.** Measure prefix reduction per update, per unit time and per full-rate-equivalent step; keep a per-step monitor trace | "staged diagnostic extensions after conformance and conditioning checks" (`codex:217`); the composed control (`codex:348-371`) | `E8` (`claude:1368`); `D5-A` (`claude:1475`) | **yes** | training | conformant code | n_steps × about 12 s (10⁴ steps ≈ 1.4 days) | the budget (Q4, class `V` until measured), and whether the front tracks physics once physics trains. Its configuration is where the disputes in `JD-2`, `JD-4`, `JD-6` and `JD-7` land |
| `JX-9` | **Instrumentation on the next run:** continuous monitor prefixes and threshold margins, evaluated identities, per-term gradients with Adam-preconditioned shares, the IC position/velocity split | `codex:234`, `D7-A` (`codex:344`), recipe observations (`codex:366`) | `D7-A` (`claude:1492`) | rides on the next run | — | the next run | — | routed to `JD-10` as a requirement, not run as a separate experiment |
| `JX-10` | **Verification completion:** re-score the smoke's frozen monitor at steps 100, 200 and 300, and reproduce the monitor-recompute values Claude's sub-agent reported, from checkpoint contents only | — | (its sub-agent ran these, `claude:77-81`) | no | yes: forward | retained checkpoints | minutes | settles the verification's open forward-pass rows (`C-F14`, `F-H2b`, `C-07` numeric) `{verify}`. Not a decision input |

**The orderings the reports propose.**

- **Claude** `{claude}`: "E2 → E4 → E3 → E9 are read-only and cheap, and
  could falsify PC-2 or the M1.2 reading before any run. E5 needs a narrow
  code path. E6–E8 are runs" (`claude:1371-1373`). In this document's IDs:
  `JX-1` → `JX-2` → `JX-3` → `JX-4`, then `JX-5`, then runs.
- **Codex** `{codex}`: the decomposition first (`codex:133`; `D1-A`), then the
  conformance correction and a corrected control. "A matched constant-rate
  arm belongs after that choice" (`codex:371`).

**The two orderings agree on the first step** `{join}`: read-only
measurement on retained checkpoints, before any code change or run. They
differ on where the schedule experiment `JX-7` sits:

- **Codex:** after conformance and after the balancing choice.
- **Claude:** its `D8-C` option allows it on the current code.

## JOIN-5-OPTIONS — the options, joined on the decision

**How to read the menus.**

- **Each joined decision (`JD-n`) lists every option either report offers,**
  under its author's tag, with:
  - the diagnosis it presupposes, quoted or closely paraphrased;
  - its door classification;
  - any `{join}` flag.
- **A flag marks** an option whose presupposition conflicts with the merged
  diagnosis or with an owner ruling, or whose rationale leans on class-`E`
  evidence. A flagged option stays on the menu: the join point says
  conflicting options "are flagged, not silently dropped".
- **The two reports define the doors differently** `{join}`. Read the door
  columns with that in mind.
  - **Codex:** "'Two-way' means the configuration or implementation choice
    is reversible with preserved artifacts. Executed compute cannot be
    recovered. Spending the held-out evaluation is a one-way evidence
    decision" (`codex:256`).
  - **Claude:** "One-way door — committing changes a locked contract,
    consumes a non-renewable resource (the held-out evaluation, a baseline's
    comparability), or sets a precedent that later rulings inherit". Claude
    flags contract changes separately as "amendment" (`claude:1379-1388`).
  - **Consequence.** Most of the door disagreements below follow from these
    definitions. Codex calls every reversible change two-way. Claude
    reserves one-way for changes that invalidate the reference or the
    baselines later runs inherit, such as the architecture, the output head,
    or rulings A1 and B2. It marks other contract changes as two-way, with
    a separate amendment flag.

### JD-0 — conformance of the physics term, the monitor, validation and the verifier

**The default is fixed by an owner instruction** `{ruling R-3}`.

- **The instruction.** Option A of 2026-09-07: "replacing the current
  one-anchor physics-loss execution with contributions from all selected
  slots" (`57-GAPS.md:214-218`).
- **Both reports agree.** Each independently suggests the same default.
- **Reversal.** Any other option is available only as the owner's explicit
  reversal of Option A.
- **Claude's gap G-2 is answered by the same instruction.** Claude G-2 asks whether
  the Phase-56 contract requires per-slot evaluation or only per-slot time
  allocation.

| Option | Proposed by | Presupposes | What it does and costs | Door | Flag `{join}` |
|---|---|---|---|---|---|
| **A. Per-slot conformance.** Evaluate every physics row on its own slot's IC13 and masses; score the monitor over its 256 frozen identities; make validation conformant (no `collocation_count=1`, no fixed anchor); verify what the loss evaluates (Codex: "observe evaluated IC/mass inputs"; Claude: perturbing a non-anchor slot's IC13 must change the physics loss); then re-measure `R_ref` and re-run GATE-04 | `{both}` (`codex:264`; `claude:1396`) | P-1, verified | Same row count, so per-step cost is about the same; physics and monitor estimates average 256 trajectories per bin; `R_ref` changes value (Claude) | Codex: two-way implementation. Claude: two-way in code; no amendment, because it implements the ratified contract; **one-way for evidence**, because generations 6 and 7 stop being comparable baselines | Claude's `D0-A` also aggregates the IC term over all slots. Under R-3 that is split out as `JD-1` |
| **B. One trajectory per step, unbiased.** A uniformly random or round-robin anchor; the monitor scores K fixed trajectories | `{claude}` (`claude:1397`) | "that single-trajectory SGD on physics/IC is acceptable, and only the bias is the defect" | Cheapest change; the physics gradient stays a one-trajectory estimate per step | Claude: two-way in code; amendment | **Conflicts with Option A** ("contributions from all selected slots"). Available only as an explicit reversal (R-3) |
| **C. Ratify the executed single-anchor semantics** as a new design | `{both}` (`codex:265`; `claude:1398`) | Codex: "Owner deliberately accepts biased, narrower training". Claude: "that PC-1 is a reading choice, not a defect" | No code change; training stays concentrated on about 10–40 trajectories; the monitor stays one trajectory | Codex: two-way design; it "cannot retroactively make old execution conformant". Claude: **one-way in practice**, because it canonizes a biased estimator | **Conflicts with Option A**; available only as an explicit reversal. Claude's stated presupposition, "a reading choice", conflicts with the verified record: Phase 57 required per-slot evaluation (`B-PC1l`) |
| **D. A broader trainer rebuild** | `{codex}` (`codex:266`) | "Bounded correction proves impractical" | Larger scope and verification cost | Codex: two-way, expensive | — |

**Consequences that are not choices** `{ruling R-3}`:

- Any fix to selected-slot semantics triggers re-measuring `R_ref` and
  re-running GATE-04. The invalidation list at `pinn_architecture.md:454`
  names "selected-slot semantics", and `:456` repeats it.
- A graded run before conformance is restored would again not test the
  recipe.
- The next conformance gate must test what the loss evaluates.

**Interactions** `{both}`:

- `JD-0` resets `R_ref`, which `JD-3` reads, and the monitor (`JD-4`).
- It changes the IC gradient's variance but not its magnitude problem
  (`JD-2`).
- It invalidates any budget extrapolated from generation 7 (`JD-7`)
  (`claude:1400-1404`).
- Codex: the reference and gate provenance must be reviewed before further
  diagnosis (`codex:264`).

**Attached owner question `OQ-1`** (no menu in either report): the
re-measured `R_ref` uses "the fixed six-case GATE-04 probe"
(`pinn_architecture.md:454`). Five of those six cases use synthetic zero IC13
and unit masses (`B-PC8a`; Claude G-8, `claude:1619`). Whether the probe
should use dataset ICs is the owner's call.

### JD-1 — the IC term's batch semantics

**This is a decision of its own** `{ruling R-3}`.

- **Current behavior.** The IC term evaluates one trajectory, the anchor,
  per step.
- **Why it was kept.** Phase 57 kept this on purpose (`57-02-PLAN.md:87`).
- **What the spec says.** Its `L_IC` is written for one trajectory and
  states no batch rule (`pinn_architecture.md:509-515`; `B-PC1t`).
- **Why it matters.** The term carries the dominant gradient (P-7, P-13).

| Option | Proposed by | Presupposes | What it does and costs | Door | Flag `{join}` |
|---|---|---|---|---|---|
| **A. Keep the anchored IC term** as Phase 57 preserved it | the status quo named by `{ruling R-3}`; no report proposes it | that the IC term's one-trajectory evaluation is acceptable alongside per-slot physics | No change; the IC term stays a one-trajectory estimate per step with the about-2× recurrence swings (`J5.f`) | — | No report argues for it. It is listed because R-3 makes the batch behavior an owner decision rather than part of the defect |
| **B. Aggregate the IC term over all selected slots,** with a reduction rule: (B1) mean over slots, (B2) mean over unique identities, or (B3) weighted by replacement multiplicity | `{claude}` (`D0-A`, `claude:1396`; Claude G-1, `claude:1612`) | PC-1 as Claude states it, which groups the IC term with the physics term (`claude:1396`) | 256 first derivatives at u = 0, which is cheap; lowers the IC estimate's variance, but not its magnitude (`claude:1400-1404`) | Claude: inside `D0-A`, "no amendment" | Claude's "no amendment" door rests on grouping the IC term with the physics term. The verification narrowed that grouping (`B-PC1t`): the spec is silent, so the choice of reduction is semantic. That is Claude G-1's own conclusion: "Owner ruling (semantic)" |

**Suggested defaults:**

- **Codex:** none. It is silent on the IC term's batch semantics; its P1
  concerns the physics rows.
- **Claude:** **B**, with the reduction rule left to the owner.

**Joined: one report only.**

**Bearing from the literature** `{join}`: in the authors' soft-IC code the IC
loss sits inside the causal exponent and gates every weight (`LR-6`).
Neither report builds an option on this. It is recorded so that the
choice of IC treatment is made knowing it.

### JD-2 — the balance of the loss gradients among IC, physics and data

| Option | Proposed by | Presupposes | What it does and costs | Door | Flag `{join}` |
|---|---|---|---|---|---|
| **A. Measure first** (`JX-1`), then branch | `{both}` (`codex:276`; Claude's branch on E2, `claude:1415-1420`) | "Contribution of imbalance remains unresolved" (Codex) | Separates IC position/velocity, gradient alignment and Adam effects | two-way, diagnostic | The branch must be read on the conformant batch: R-2 makes the IC dominance a design concern "to be re-measured once the run conforms". Claude's E2 includes a conformant batch; a branch taken on the executed batch alone rests on class-`E` evidence |
| **B. Retain the current weights** (λ_IC = λ_phys^max = 1) in a controlled corrected run | `{codex}` (`codex:277`); Claude's `D1-D` "change nothing" (`claude:1413`) | Codex: "Panel does not justify a balancing change, or owner wants a control". Claude: "E2 shows physics share ≳ 10⁻² (PC-2 overstated)" | Preserves the locked weights | two-way | — |
| **C. Adaptive λ_IC by a gradient-norm EMA** on a fixed cadence, keeping λ_phys^max = 1 and λ_data = 1 | `{claude}` `D1-A` (`claude:1410`) and Codex's "ratify fixed or adaptive balancing" (`codex:278`) | Claude: "PC-2: physics share of the update ≲ 10⁻⁴ (E2 confirms)". Codex: "Corrected objective still has harmful gradient imbalance" | Directly targets the imbalance. Adds one state variable and a cadence. The weight would sit 3–5 orders below the spec's [0.1, 10] ablation range (`H-D1b`), so IC enforcement weakens and an IC success criterion (`JD-3`) becomes essential (Claude). Codex: "Requires explicit scales/control law; interacts with warmup and causal descent" | Claude: two-way in code; **amendment** (the Phase-35 deferral, "automatic dominance reweighting is deferred until measured weighted-loss/gradient evidence exists", `pinn_architecture.md:708`, `:710`; and the λ_IC range). Codex: two-way, "changed objective provenance required" | `LR-18`: the norm-equalizing rule is the 2023 guide's, not the 2021 paper's; the option is unaffected |
| **D. Freeze an initialization reference for the IC term** (`IC_ref`, mirroring `B2`) | `{claude}` `D1-B` (`claude:1411`) | "that loss-*value* parity is enough" | Equalizes values, not gradients; Claude estimates IC would still be about 50× physics in gradient at initialization | two-way; **amendment** (the `L_IC` definition) | Claude's 50× estimate uses the initialization record of the single-anchor production path; it may motivate but not decide (class `E`) |
| **E. A hard IC through an output ansatz,** removing `L_IC` | `{claude}` `D1-C` (`claude:1412`) | "that IC dominance *and* IC hypersensitivity must both go" | Removes the term and its swings; changes the output-head contract and the derivative structure; `R_ref` and GATE-04 must be redone | Claude: **one-way** (architecture or output-contract amendment) | The source's Lorenz benchmark used an exact IC (`LR-11`) |

**Suggested defaults:**

- **Codex:** "A first; then branch on its result" (`codex:272`). B if the
  decomposition does not justify a change; C if harmful imbalance persists.
  Codex adds that lowering λ_IC to 0.1 alone would leave the IC/physics
  ratio at 2,780 or more (`codex:280`). That figure is class `E`, and so
  are the ratios behind it.
- **Claude:** **C (adaptive λ_IC), on the branch where E2 confirms PC-2.**
  B (Claude's D1-D) if E2 refutes PC-2, and E (Claude's D1-C) if IC
  hypersensitivity persists after rebalancing (`claude:1415-1420`).

**Joined:**

- **Agreed:** measure before changing any weight, and branch on the
  measurement.
- **Disputed:** whether the default names a remedy now. Claude names
  adaptive λ_IC conditionally; Codex leaves the remedy to a later ruling.

**Locked constraints both respect:**

- `λ_phys^max = 1` is locked (`pinn_architecture.md:699-701`). Codex: raising
  the physics cap silently "is also unavailable" (`codex:280`).
- `λ_data = 1` (`pinn/loss_catalog.py:169-173`).

**Interactions:**

- `JD-1`: which IC term is being balanced.
- `JD-3`: an IC criterion is needed if IC enforcement weakens.
- `JD-9`: a lower initialization derivative scale shrinks the rebalancing
  needed.
- `JD-5`: the EMA cadence must be shorter than the learning-rate timescale
  (`claude:1422-1429`).
- Codex: at initialization the scheduled λ_phys is 0, so scheduled
  gradients must be told apart from standardized comparisons (`codex:282`).

### JD-3 — what the front means, and what decides stage success

| Option | Proposed by | Presupposes | What it does and costs | Door | Flag `{join}` |
|---|---|---|---|---|---|
| **A. Relative front as a progress or pacing diagnostic; stage success gated separately on absolute criteria** | `{both}` (`codex:302`; `claude:1435`) | Codex: "Q2 arithmetic accepted". Claude: R2.1 and R2.2 | Codex: raw-residual and IC reporting alongside the front, with separate accuracy gates. Claude: a physically normalized residual tolerance, the IC error and the existing `eps_H` gate; needs a physical-scale definition (Claude G-7) and tolerances; the ADVANCE thresholds are already provisional | Codex: two-way. Claude: two-way; owner calibration of provisional thresholds, with no locked value moving | The scale and the tolerances are open (`JG-12`). `JX-4` informs the scale; it cannot set a tolerance (R-2) |
| **B. Replace the front threshold with an absolute-error criterion** | `{codex}` (`codex:303`) | "Owner supplies a justified physical tolerance" | Changes the monitor's semantics and its dependence on the reference | Codex: two-way amendment | — |
| **C. Require both relative and absolute conditions** | `{codex}` (`codex:304`) | "Owner wants a combined operational gate" | More explicit criteria; the thresholds need grounding | Codex: two-way amendment | — |
| **D. Re-base the causal normalization on a physical scale,** treating η_c as an accuracy tolerance with continuation from loose to strict | `{claude}` (`claude:1436`) | "that the causal weights should *be* the accuracy schedule, as in the published method" | Aligns with the source method; discards the `R_ref` construction; reopens `A1` ("do not add coefficient continuation", `54-RULING.md:50`) and `B2` | Claude: **one-way** (amends A1 and B2; new gate design) | The literature facts under it hold (`LR-2`, `LR-5`, `LR-9`, `LR-17`). "Faithful reading" is Claude's interpretation of them |
| **E. Keep the relative front for both pacing and success** | `{claude}` (`claude:1437`) | "that relative progress tracks absolute accuracy" | No change | two-way | **Presupposes a reading the merged diagnosis contradicts** (`J2.a`, `J2.c`). Claude flags this itself |

**Suggested defaults:** Codex **A**; Claude **A**. **Joined: agreed.**

**Interactions:** D couples to `JD-2`, because the physics-loss
normalization sets the balance. A's IC criterion is the safeguard that
`JD-2`'s option C needs (`claude:1439`).

### JD-4 — the invariant-B guard, for the next run and after it

| Option | Proposed by | Presupposes | What it does and costs | Door | Flag `{join}` |
|---|---|---|---|---|---|
| **A. A corrected control under the existing rule:** cosine schedule and 500-step high-water timeout kept; the monitor corrected to multi-identity; continuous prefixes and evaluated identities recorded | `{codex}` (`D2-A`, `codex:290`; `D7-A`, `codex:344`) | "Need a comparable control" | "May halt again; does not promise completion" | Codex: two-way | The run inherits by design the schedule/guard interaction R-2 calls structural (`J1.b`). Codex accepts a halt as a control outcome, and its continuous-prefix recording is what lets a halt be read against the trend |
| **B. High-water semantics on the multi-slot monitor, with N in full-rate-equivalent (N_eff) units** | `{claude}` `D3-B` (`claude:1447`) | "that a population monitor removes enough noise for a record statistic" | Smallest change; records stay biased upward by noise at high learning rate | Claude: two-way; **re-ratification** of N's unit | — |
| **C. A continuous, smoothed trend statistic:** the slope of ln S_k for the next prefix must be negative beyond a noise band (from `JX-2`/`JX-8`); window in N_eff; guard suspended during warm-up and the annealing tail; per-step trace logged | `{claude}` `D3-A` (`claude:1446`) | M1.2 and M5.1 (HIGH) | Robust to transients and learning-rate-scaled noise; needs a noise band and a slope threshold, which are new parameters | Claude: two-way in code; **re-ratification** of 57-RULING checkpoint ③ semantics | — |
| **D. Observe-only for the next (calibration) run;** choose B or C afterwards from its traces | `{claude}` `D3-C` (`claude:1448`) | "that the next run is diagnostic, not graded" | Prevents a guard verdict before the statistic is calibrated; needs an owner decision that the pilot spends no graded slot and no evaluation | Claude: two-way | — |
| **E. Several fixed training-only panels** | `{codex}` `D7-B` (`codex:345`) | "One panel inadequately represents population behavior" | Needs aggregation and advancement rules | Codex: two-way amendment | Partly overtaken by A of `JD-0`, which already makes the monitor a 256-identity population |
| **F. Hysteresis or persistence** on the front | `{codex}` `D7-C` (`codex:346`) | "Corrected traces show operational threshold chatter" | "Could hide real regressions; requires explicit justification" | Codex: two-way amendment | — |
| **G. A phase-aware deadline or schedule** | `{codex}` `D2-C` (`codex:292`) | "Matched evidence supports inadequate opportunity" | Needs an explicit new monitoring/window contract | Codex: two-way policy | Overlaps C's N_eff window and `JD-5` |
| **H. Keep as executed:** 500 raw steps; single-trajectory high-water | `{claude}` `D3-D` (`claude:1449`) | "M1.1 dominant and the statistic sound" | — | two-way | **Presupposes readings the merged diagnosis contradicts** (`J1.c`); a single-trajectory monitor also conflicts with A of `JD-0`. Claude flags this itself |

**Suggested defaults:**

- **Codex:** **A**, "for a diagnostic control; B only after a matched
  comparison supports it" (`codex:286`).
  - Its D2-B is the constant-rate comparison arm (here `JD-5` B).
  - Its D2-C, a phase-aware deadline (here G), presupposes that "matched
    evidence supports inadequate opportunity" (`codex:292`).
- **Claude:** **D** for the next run only, then C or B by the pilot's traces
  (`claude:1448-1455`).

**Joined: DISPUTED.** The point in dispute is whether the guard can halt
the next run.

- **The difference follows from the run's purpose** `{join}`.
  - Codex designs the next run as a control of the corrected invocation
    under otherwise-ratified rules.
  - Claude designs it as a calibration pilot whose guard statistic is not
    yet calibrated.
- **Neither default rests on a refuted reading.**
- **The dispute couples to `JD-7`,** which decides what the next run is.

**Attached owner question `OQ-5`** (Claude G-4, `claude:1615`; no menu): no
source records why the front threshold is 0.5, equivalently a prefix of
ln 2, or why N = 500. The current values are owner rulings
(`57-RULING.md` §2).

**Interactions:**

- `JD-0`: the monitor's composition.
- `JD-5`: what an N_eff window spans.
- `JD-6`: whether the guard reads into an annealing tail or an L-BFGS phase
  (`claude:1457`).

### JD-5 — the learning-rate schedule

| Option | Proposed by | Presupposes | What it does and costs | Door | Flag `{join}` |
|---|---|---|---|---|---|
| **A. Keep the spec's cosine over the Adam phase** ("a cosine annealing scheduler to decay the learning rate over the phase", `ctl_instruction.md:1805`). Claude would calibrate T_max = n_adam from the pilot | `{both}` (`codex:290`; `claude:1464`) | Codex: a comparable control. Claude: PC-3, and "that within-spec choices suffice once D0/D1/D3 fix the larger issues" | Stays inside the spec text | two-way | — |
| **B. A matched constant-rate comparison arm** (`JX-7`) | `{codex}` (`codex:291`); Claude's E7 | "Schedule starvation remains plausible after D0/D1" (Codex) | Changes the schedule while matching the other inputs | two-way | — |
| **C. Constant (or warm-up then constant) during the guarded exploration phase;** anneal only in a final segment outside the liveness window; then L-BFGS | `{claude}` `D4-B` (`claude:1465`) | "M1.1 matters more than the evidence shows" | Removes the window/schedule coupling by construction; departs from "cosine … over the phase" | Claude: two-way in code; **amendment** (schedule text) | Its rationale cites low learning rate making progress "*more* efficient per unit lr" (E-G): class `E`, and narrowed (`F-Q1b`: anchor 1 peaks in the middle third) |
| **D. Literature-style slow exponential decay over a long budget** | `{claude}` `D4-C` (`claude:1466`) | "that the source method's schedule should be adopted wholesale" | Matches published practice (`LR-7`, `LR-15`); heavy on budget at about 12 s per step | Claude: two-way in code; **amendment** | — |
| **E. Ratify a phase-aware schedule or deadline** | `{codex}` `D2-C` (`codex:292`) | as in `JD-4` G | | Codex: two-way policy | Same option as `JD-4` G |

**Suggested defaults:**

- **Codex:** A, with B "only after a matched comparison supports it"
  (`codex:286`).
- **Claude:** A, with T_max calibrated by the pilot.

**Joined: agreed.** Keep the cosine for now.

### JD-6 — whether the next run can reach L-BFGS, and what feeds the plateau trigger

| Option | Proposed by | Presupposes | What it does and costs | Door | Flag `{join}` |
|---|---|---|---|---|---|
| **A. An Adam-only next run** (`max_epochs = n_adam = 1000`, "explicitly an Adam-only diagnostic control") | `{codex}` (recipe, `codex:363`; `D6-A`, `codex:334`) | that refinement is not the next question | The configuration trap (P-4) stays, by design, for a control | two-way | — |
| **B. Make L-BFGS reachable with explicit headroom** (`max_epochs > n_adam`), raising the total budget separately from the Adam duration | `{both}` (Codex `D6-B`, `codex:335`; Claude `D4-A`, `claude:1464`) | Codex: "Refinement is the next question". Claude: PC-3 | Codex: "closure cost uncertain", since one outer call can take several closures (`codex:217`) | Codex: two-way. Claude: two-way (provisional values) | — |
| **C. Feed the plateau detector a smoothed physics statistic,** or the population monitor after `JD-0`, not the per-step single-anchor loss | `{claude}` (`D4-A`, `claude:1464`) | that the 50-step plateau rule cannot fire on a per-step single-trajectory loss | Changes a CTX-46 detail in code | Claude: two-way (a code fix) | — |

**Suggested defaults:**

- **Codex:** **A** for the next run. Refinement only "if the owner instead
  commissions refinement", with explicit total-budget headroom
  (`codex:371`).
- **Claude:** **B + C** as part of `D4-A`.

**Joined: DISPUTED.** The point in dispute is whether the next run
exercises L-BFGS.

- **Both agree the trap is structural** (`S`; P-4), and that a longer
  timeout alone does not fix it (`codex:294`).
- **Interaction:** see `JOIN-6` on combining B with `JD-4` A.

### JD-7 — the budget, the seeds, and what the next run is

| Option | Proposed by | Presupposes | What it does and costs | Door | Flag `{join}` |
|---|---|---|---|---|---|
| **A. Staged diagnostic budgets, with no completion forecast;** the next run is a corrected control on a fresh seed 42 | `{codex}` (`D6-A`, `codex:334`; recipe, `codex:354`) | "Current evidence insufficient" | Limits spend while measuring marginal progress | Codex: two-way | — |
| **B. A calibration pilot** (`JX-8`) under the corrected recipe, preferably on at least two seeds; set `n_adam` as a stated multiple of the measured N_eff per full front crossing | `{claude}` `D5-A` (`claude:1475`) | M4.1 and M4.2: "no defensible budget exists before the recipe trains physics" | 10⁴ steps ≈ 1.4 days per seed; yields a measured number | Claude: two-way (diagnostic; no evaluation spent) | The two-seed preference rests on a verified structural fact: same-seed replicates share batches (P-5) |
| **C. A literature-scale budget a priori** (about 10⁵ steps) | `{claude}` `D5-B` (`claude:1476`) | "that published budgets transfer to this problem and hardware" | About 14 days per seed per attempt at about 12 s per step | two-way in principle; costly | Published budgets are confirmed (`LR-8`), and both reports say they do not transfer as a number |
| **D. Extend the Adam duration** | `{codex}` `D6-C` (`codex:336`) | "Corrected prefixes keep descending under adequate optimization" | Also changes the cosine horizon and the warm-up unless controlled | two-way | — |
| **E. Keep 1,000 steps** | `{claude}` `D5-C` (`claude:1477`) | "that 1000 steps suffice under the corrected recipe" | "No evidence supports it" | two-way | Presupposes an answer R-2 voids |

**Suggested defaults:** Codex **A**; Claude **B**.

**Joined:**

- **Agreed:** measure before setting any budget. R-2 voids the Q4 answer
  in any case.
- **Disputed:** the next run's design.
  - **Seeds:** one fresh seed 42, against at least two seeds.
  - **Configuration:** carried by `JD-2`, `JD-4` and `JD-6`.

**Attached owner question `OQ-2`:** what "epoch" means under replay
batching. It bears on every budget figure here.

### JD-8 — the causal coefficient η_c

| Option | Proposed by | Presupposes | What it does and costs | Door | Flag `{join}` |
|---|---|---|---|---|---|
| **A. Retain η_c = 1** | `{codex}` (`codex:312`) | "Current coefficient not isolated as cause" | Preserves the contract during conformance diagnosis | two-way | The fixed value is within the source's method family (`LR-13`), but here it multiplies a reference-normalized residual (`LR-17`; departure L-2) |
| **B. Compare a weaker fixed coefficient** | `{codex}` (`codex:313`) | "Corrected, adequately optimized prefixes remain over-restricted" | Opens later bins at equal residuals; does not improve accuracy by itself | two-way | Codex: "Front movement induced by changing the coefficient cannot be counted as equivalent residual improvement" (`codex:316`) |
| **C. Ratify continuation** | `{codex}` (`codex:314`); Claude's `JD-3` D includes continuation | "Source-style staged strength fits the corrected problem" | Adds a parameter schedule and stopping semantics | Codex: two-way, with greater policy complexity | Reverses the owner's A1 ruling ("do not add coefficient continuation", `54-RULING.md:50`), so it needs re-ratification. The source's annealing is confirmed (`LR-5`) |

**Suggested defaults:**

- **Codex:** **A**, "until corrected evidence supports a change"
  (`codex:308`).
- **Claude:** no separate menu. Its recipe moves no locked value, so it
  keeps η_c = 1 implicitly (`claude:1562-1567`).

**Joined: one menu,** with no conflict.

### JD-9 — the architecture: `first_omega_0` and the power-skip stack

| Option | Proposed by | Presupposes | What it does and costs | Door | Flag `{join}` |
|---|---|---|---|---|---|
| **A. Keep the architecture during conformance diagnosis, and decompose first** (`JX-5`). Claude: authorize E5 through a verification-only path that admits non-default `ArchitectureSpec` values | `{both}` (`codex:324`; `claude:1483`) | that the architecture's contribution is unresolved (Codex); M3.2b undetermined and M3.3 MEDIUM (Claude) | Avoids changing the representation at the same time. Claude's sweep needs a narrow code path outside production | two-way | The verification-only path is a code change and needs owner authorization (`pinn/architecture_spec.py:71-130`) |
| **B. A fresh-initialization frequency ablation** (lower `first_omega_0`) | `{both}` (`codex:325`; Claude `D6-C`, `claude:1486`) | that frequency-sensitive derivatives dominate (M3.2b) | Invalidates the reference; needs a fresh gate and raw-unit comparisons. Claude: effect size undetermined, and it weakens SIREN's spectral-bias rationale (`pinn_architecture.md:180-186`) | Codex: two-way, compute cost. Claude: **one-way** (the ω₀ contract, `R_ref`) | Door difference is definitional (see the top of this section). `first_omega_0` is on the invalidation list (`pinn_architecture.md:454`) |
| **C. A fresh-initialization skip ablation** (remove or alter the `LN(x)²` branch) | `{both}` (`codex:326`; Claude `D6-B`, `claude:1484`) | that the skip and LayerNorm derivatives dominate (M3.3) | Changes the backbone behavior and the reference calibration; possibly the larger lever if M3.3 holds | Codex: two-way, larger verification cost. Claude: **one-way** (architecture contract; new baselines) | As B |
| **D. Zero-initialized trainable gates on the six `LN(x)²` branches** (the PirateNets α = 0 practice) | `{claude}` `D6-D` (`claude:1485`) | M3.3 | Removes the initial amplification while keeping depth capacity | Claude: **one-way** (architecture contract; `R_ref`) | The source practice is confirmed (`LR-19`), but on a different architecture (no LayerNorm, no power term) |

**Suggested defaults:** Codex **A**; Claude **A**.

**Joined: agreed on the default.** The door types of B and C differ, by
definition.

### JD-10 — the telemetry and verification gates required before the next run

| Option | Proposed by | What it requires | Door | Flag `{join}` |
|---|---|---|---|---|
| **A. The full set** | `{claude}` `D7-A` (`claude:1492`), with Codex's equivalent requirements (`codex:268`, `:344`, `:366`) | per-step slot or anchor identity; a per-step monitor prefix trace; per-term gradient norms with Adam-preconditioned shares on a cadence; the identity-dependent conformance assertion; the `train.log` hand-off message fix; the spec cross-reference fix at `pinn_architecture.md:452`. **Codex adds** the IC position/velocity split, the threshold margins, and a verifier that observes evaluated IC and mass inputs | two-way | The spec cross-reference fix is a spec edit, so it needs an owner amendment (`OQ-3`). R-3: the gate must test what the loss evaluates |
| **B. A minimal set:** the conformance assertion and slot logging | `{claude}` `D7-B` (`claude:1493`) | — | two-way | — |

**Suggested defaults:** Claude **A**. Codex has no separate menu, and its
requirements match A.

**Joined: agreed.** The joined set is the union of both lists.

### JD-11 — which experiments to authorize first

| Option | Proposed by | What it does | Door | Flag `{join}` |
|---|---|---|---|---|
| **A. The read-only experiments on retained checkpoints first** (`JX-1` to `JX-4`), before any code change | `{claude}` `D8-A` (`claude:1499`); Codex's decomposition-first order (`codex:133`) | Each can falsify a load-bearing reading (PC-2, M1.2, M1.4, R2.1) in minutes to about an hour | two-way | Each needs model computation on checkpoints, which the owner must authorize. They describe the executed run (R-2). `JX-1`'s conformant half needs `JD-0`'s code path. `JX-10` can run alongside |
| **B. Skip to the conformance fix and the pilot** | `{claude}` `D8-B` (`claude:1500`) | Forgoes cheap falsification | two-way | — |
| **C. Also authorize diagnostic runs on the current code** (`JX-6`, `JX-7`) | `{claude}` `D8-C` (`claude:1501`) | About 1.7–7 h of compute | two-way | Spends compute on the non-conformant objective; the results describe the single-anchor run (R-2, R-3) |

**Suggested defaults:** Claude **A**. Codex's order is compatible.
**Joined: agreed.**

### Owner questions with no menu in either report

| ID | Question | Source | Bears on |
|---|---|---|---|
| `OQ-1` | Should the six GATE-04 probe cases behind the re-measured `R_ref` use dataset ICs? Five of the six now use synthetic zero IC13 and unit masses | Claude G-8 (`claude:1619`); `B-PC8a` | `JD-0` |
| `OQ-2` | What is an "epoch" under replay batching? The code uses optimizer steps. The spec's Phase-34 rule says the replay set "is sampled without replacement across the epoch (standard once-per-epoch coverage)" (`ctl_instruction.md:1829`), and the code satisfies that only under the one-step reading | Claude G-6 (`claude:1617`); `{verify}` (`V:311-315`) | `JD-6`, `JD-7` |
| `OQ-3` | Spec hygiene. `pinn_architecture.md:452` cites "the fixed-monitor boundary above", which does not exist in that file; the invariant-B monitor contract lives only in `57-RULING.md`. A fix is a spec amendment | Claude G-15 (`claude:1626`); `C-F10` | `JD-4`, `JD-10` |
| `OQ-4` | How causal weights should aggregate across many trajectories per batch. The ratified recipe fixes one batch-global 16-term prefix (F-12), and every causal-training source read is single-IC (departure L-6). The ratified rule stands unless the owner reopens it | Claude G-9 (`claude:1620`) | `JD-0`, `JD-3` |
| `OQ-5` | Why the front threshold is 0.5 (a prefix of ln 2) and why N = 500 | Claude G-4 (`claude:1615`) | `JD-4` |

## CANDIDATE-SHEET — the consolidated decision sheet

- **The owner's-pick column is empty in every row, and must stay empty in
  this document** (see STANDING). The owner records picks as project Key
  Decisions.
- **"Joined" uses four values** `{join}`:
  - `fixed`: an owner instruction already sets the default;
  - `agreed`: both reports suggest the same default;
  - `disputed`: the reports suggest different defaults;
  - `one report`: only one report offers a menu.
- **Every cell except "Joined" and "Flags" comes from the reports,** or
  from R-3 where the per-decision table says so. The attributions are in
  the per-decision tables above.

| Decision | Options | Codex's suggested default | Claude's suggested default | Joined | Door of the defaults | Presupposed diagnosis | Flags | Owner's pick |
|---|---|---|---|---|---|---|---|---|
| `JD-0` Conformance | A per-slot fix, then `R_ref` + GATE-04 · B unbiased single anchor · C ratify single anchor · D rebuild | A | A | **fixed** (Option A, R-3) and agreed | Codex: two-way. Claude: two-way in code, no amendment; one-way for evidence | P-1, verified | B and C are available only as an explicit reversal of Option A; `OQ-1` attached | |
| `JD-1` IC term batch semantics | A keep anchored (status quo) · B aggregate over slots (B1 mean over slots · B2 over unique identities · B3 multiplicity-weighted) | — (silent) | B, rule open | **one report** | Claude: inside D0-A, "no amendment" | PC-1 as Claude states it, including the IC term (narrowed, `B-PC1t`) | The spec is silent and the choice is semantic (`B-PC1t`; Claude G-1). `LR-6`: the source's code gates the causal weights on the IC loss | |
| `JD-2` Loss-gradient balance | A measure first (`JX-1`) · B retain weights · C adaptive λ_IC by gradient norm · D frozen `IC_ref` · E hard IC ansatz | A, then B or C | C, on the branch where `JX-1` confirms PC-2; B if refuted; E if hypersensitivity persists | **agreed** on measuring first; **disputed** on naming a remedy now | Codex: two-way. Claude: C two-way + amendment; E one-way | PC-2 (Codex: unresolved contribution) | Read the branch on the conformant batch (R-2). Codex's 2,780 figure is class `E`. `LR-18` narrows a citation | |
| `JD-3` Front meaning and stage success | A relative for pacing + absolute success gates · B absolute only · C both · D physical normalization + η_c continuation · E relative for both | A | A | **agreed** | two-way (Claude: owner calibration of provisional thresholds) | `J2.a`–`J2.d` | E presupposes a contradicted reading; D reopens A1 and B2; the scale and tolerances are open (`JG-12`) | |
| `JD-4` Invariant-B guard | A corrected control under the existing 500-step rule · B high-water in N_eff · C smoothed trend in N_eff · D observe-only pilot · E several panels · F hysteresis · G phase-aware deadline · H as executed | A | D for the next run; then B or C | **disputed**: may the guard halt the next run? | two-way (Claude: B and C need re-ratification) | Codex: a comparable control. Claude: M1.2 and M5.1 | A inherits the structural schedule/guard interaction (`J1.b`) by design; H presupposes a contradicted reading; couples to `JD-7`; `OQ-5` attached | |
| `JD-5` Learning-rate schedule | A keep cosine · B constant-rate comparison arm · C constant then anneal · D slow exponential · E phase-aware | A; B only after a matched comparison | A, with T_max calibrated | **agreed** | two-way | PC-3; M1.1 partial | C's rationale is class `E` and narrowed (`F-Q1b`) | |
| `JD-6` L-BFGS reachability and plateau input | A Adam-only next run · B reachable L-BFGS with explicit headroom · C smoothed plateau input | A | B + C | **disputed**: does the next run exercise L-BFGS? | two-way | P-4 | Combining B with `JD-4` A gives a recipe neither report wrote (`JOIN-6`) | |
| `JD-7` Budget, seeds, the next run | A staged diagnostics, fresh seed 42 · B calibration pilot on ≥ 2 seeds · C literature-scale budget · D longer Adam · E keep 1,000 | A | B | **agreed** on measuring first; **disputed** on the run's design | two-way | Q4 is void until measured (R-2) | E presupposes a voided answer; `OQ-2` attached | |
| `JD-8` Causal coefficient | A retain η_c = 1 · B a weaker fixed coefficient · C continuation | A | (no menu; keeps η_c = 1) | **one report** | two-way | the coefficient not isolated as a cause | C reverses the owner's A1 ruling | |
| `JD-9` Architecture | A keep, decompose first (`JX-5`) · B lower ω₀ · C skip ablation · D zero-initialized branch gates | A | A | **agreed** | A: two-way. B, C, D: Codex two-way, Claude one-way (definitional) | M3.2b undetermined; M3.3 MEDIUM | A needs a verification-only code path; B, C and D trigger `R_ref` + GATE-04 | |
| `JD-10` Telemetry and verification gates | A full set (union of both lists) · B minimal | (matches A) | A | **agreed** | two-way | P-3; the guard readings | The spec cross-reference fix needs an amendment (`OQ-3`) | |
| `JD-11` First authorizations | A read-only `JX-1`–`JX-4` first · B skip to the fix and pilot · C add runs on the current code | (decomposition first) | A | **agreed** | two-way | PC-2, M1.2, M1.4, R2.1 can be falsified | A needs owner-authorized model computation; C spends compute on the non-conformant objective | |
| `OQ-1` GATE-04 probe realism | — | — | — | no menu | — | — | five of six cases are synthetic | |
| `OQ-2` What an "epoch" is | — | — | — | no menu | — | — | the Phase-34 once-per-epoch rule (`ctl_instruction.md:1829`) | |
| `OQ-3` Spec cross-reference hygiene | — | — | — | no menu | — | — | needs a spec amendment | |
| `OQ-4` Causal weights across trajectories | — | — | — | no menu | — | — | the ratified batch-global prefix stands unless reopened | |
| `OQ-5` Why 0.5 and N = 500 | — | — | — | no menu | — | — | owner rationale or a redesign through `JD-4` | |

## JOIN-6-COHERENCE — the composed recipes, compared directly

### The two recipes, in their authors' terms

- **Codex** `{codex}` (`codex:348-371`) composes a "Suggested diagnostic
  configuration, conditional on owner approval and D0 verification":
  - **What it is.** A corrected control under otherwise-ratified settings.
  - **What it changes.** Conformance, plus any `R_ref` re-measurement it
    triggers.
  - **What it tests, in Codex's words:** it "tests corrected invocation plus
    any required reference recalibration. It does not isolate identity
    correction alone if the reference changes, and it does not promise a
    full front or L-BFGS" (`codex:369`).
- **Claude** `{claude}` (`claude:1517-1567`) composes an ordered sequence:
  read-only experiments, then conformance and telemetry, then rebalancing, a
  success gate, the schedule and L-BFGS, an observe-only guard, the
  architecture unchanged, and a calibration pilot on at least two seeds.

### Does each recipe compose from its own menus?

- **Codex: yes.**
  - **Composition.** The recipe takes `D0-A`, `D1`'s retain branch
    (explicitly conditional, `codex:360`, `:371`), `D2-A`, `D4-A`, `D5-A`,
    `D6-A` and `D7-A`.
  - **The front's meaning.** `D3-A` asks for raw-residual and IC reporting
    alongside the front. The recipe already covers it `{join}`:
    - The run already logs the training batch's per-bin raw residuals to
      TensorBoard (`raw_residuals/bin_XX`; verification Part 1, A.4).
    - The recipe's continuous monitor prefixes give the monitor's raw values
      once multiplied by the constant `R_ref`.
    - The recipe adds the IC position/velocity split.
- **Claude: yes, by construction.** Each step names the menu default it
  implements (`claude:1521-1551`). Its own coherence checks are stated at
  `claude:1553-1567`.

### The recipes compared, surface by surface

| Surface | Codex | Claude | Same? |
|---|---|---|---|
| First step | (decomposition first, `codex:133`) | read-only experiments `JX-1`–`JX-4` | same direction |
| Conformance | each row uses its own IC and masses; multi-identity monitor | per-slot physics, IC, monitor and validation; identity-dependent verifier | same (Claude adds the IC term: `JD-1`) |
| `R_ref` and GATE-04 | revalidate or reissue under corrected execution | re-measure and re-run; probe realism is open (`OQ-1`) | same |
| Architecture, η_c | unchanged; η_c = 1 | unchanged; `JX-5` in parallel | same |
| Loss weights | existing values, on the retain branch only | adaptive λ_IC (amendment) | **different** (`JD-2`) |
| Stage success | existing gates; raw and IC reporting | absolute criteria: residual, IC error, `eps_H` | same direction (`JD-3` A); Claude's pilot uses them as the success gate |
| Schedule | cosine over `n_adam = 1000` | cosine over a calibrated `n_adam` | same shape; different length |
| L-BFGS | Adam-only (`max_epochs = 1000`) | reachable (`max_epochs > n_adam`); smoothed plateau input | **different** (`JD-6`) |
| Guard | existing 500-step high-water rule | observe-only | **different** (`JD-4`) |
| Seeds | fresh seed 42 | at least two seeds | **different** (`JD-7`) |
| Added observations | continuous prefixes, evaluated identities, IC position/velocity split | per-step identity and monitor trace, gradient shares, N_eff accounting | same direction; union in `JD-10` |
| Held-out evaluation | preserved unspent | preserved unspent | same |
| Amendments needed | none beyond conformance | the λ_IC range, the Phase-35 deferral, later the invariant-B re-ratification (`claude:1562-1567`) | different |

### What the comparison shows `{join}`

1. **The recipes differ by design, not by accident.**
   - Codex changes the fewest surfaces, so that a result can be attributed:
     it names that limit itself (`codex:369`).
   - Claude changes more surfaces at once, so that the next run is
     informative about the corrected recipe. That costs attribution: a
     change in front behavior in its pilot cannot be pinned on one surface.
   - The owner's picks in `JD-2`, `JD-4`, `JD-6` and `JD-7` choose between
     these two purposes.
2. **Mixing picks across the disputes composes a recipe neither report
   wrote.** Picking a reachable L-BFGS phase (`JD-6` B) together with an
   active raw-step guard (`JD-4` A):
   - lets the guard window run into the annealing tail and the L-BFGS
     phase;
   - which Claude's own `D3-A` suspends the guard to avoid ("Guard
     suspended during warm-up and the annealing tail", `claude:1446`), and
     which Codex's control avoids by staying Adam-only.

   Claude's coherence check states the constraint directly: "Steps 5 and 6
   are coherent only together. The guard must not read a window that the
   schedule starves" (`claude:1559-1560`). This is the interaction the join
   point asks to surface.
3. **Both recipes respect R-3.**
   - Conformance comes first.
   - `R_ref` and GATE-04 are redone before any run.
   - The next conformance gate tests what the loss evaluates.
   - Neither spends the held-out evaluation.

## RUNBOOK-INHERITS — what the runbook inherits, merged

Both lists are merged here (`codex:373-380`; `claude:1569-1603`). Facts the
verification added are marked `{verify}`.

- **Emitted identity provenance does not prove evaluated identity
  conformance** `{both}`. The conformance gate must observe what the loss
  evaluates (R-3).
- **One seed is one batch sequence** `{claude}`. Batch selection consumes
  random numbers independently of the model, so same-seed replicates share
  batches and anchors and differ only by floating-point nondeterminism.
  - Independent replicates need different seeds.
  - Timing statistics need replicates.
  - Verified (P-5).
- **The per-step training identity can be rebuilt exactly** `{claude}` from
  `splits.json`, the snapshot counts and the seed, and checked against the
  RNG state in the checkpoints. Verified independently: Part 1, A.2. Log it
  directly next time (`JD-10`).
- **The monitor can be scored from checkpoint contents alone** `{claude}`.
- **Cost** `{claude}`: about 12 s per step on MPS float32 at 4,096 rows
  (mean 12.07; `F-Q4a`).
- **Configuration traps:**
  - `max_epochs == n_adam` silently removes L-BFGS `{both}`.
  - The plateau detector cannot fire on a per-step single-trajectory
    loss `{claude}`.
  - `train.log` misreports a budget-exhausted hand-off after a guard
    HALT `{claude}` (`C-F05`).
  - Adam and refinement budgets must be stated explicitly `{codex}`.
- **Code paths that do not match their names or claims** `{claude}`:
  - `_build_anchor_context` consumes times only;
  - the verifier's `anchor_only: False` is a literal;
  - validation uses `collocation_count=1` on fixed trajectory 12.
- **The data term already runs per slot** `{verify}`. Only the IC and
  physics terms were anchored.
- **Invalidation discipline** `{both}`. Any change to conformance, to the
  architecture, or to the count or slot semantics invalidates `R_ref` and
  GATE-04 (`pinn_architecture.md:454`, `:456`). Review the reference and gate
  provenance after the correction.
- **Keep four measurements separate** `{codex}`: the front diagnostic, the
  raw physical errors, the IC fit, and the held-out accuracy.
- **Spec hygiene** `{claude}` `{verify}`. These are the owner questions
  `OQ-2` and `OQ-3`:
  - the dangling cross-reference at `pinn_architecture.md:452`;
  - the undefined "epoch", together with the Phase-34 once-per-epoch rule.
- **Prompt boundary** `{ruling R-5}`. Future research prompts should state
  explicitly that reading training- and validation-split files is
  permitted, and test-split files are not.
- **Standing boundaries carried forward** `{both}`:
  - no run before an owner ruling;
  - the single held-out evaluation stays unspent;
  - Stage-1+ and PLAT-01..07 stay blocked;
  - no locked value moves without re-ratification.

## GAPS-MERGED — the gaps, merged

Codex numbers its gaps 1–10 (`codex:397-406`); Claude's are G-1 to G-15
(`claude:1612-1626`). A gap closed here is closed by an existing ruling or by
the literature reading, never by this document's own choice.

| ID | Gap | Codex | Claude | Status after this consolidation |
|---|---|---|---|---|
| `JG-1` | The scientific effect of correcting identity consumption; no conformant run exists | 1 | — | open; `JX-8` |
| `JG-2` | How the IC term reduces over a batch | — | G-1 | an owner decision: `JD-1` |
| `JG-3` | Whether the Phase-56 contract requires per-slot evaluation or only per-slot time allocation | — | G-2 | **answered** by the owner's Option A (R-3), unless reversed |
| `JG-4` | The IC term's position/velocity split, and its hypersensitivity | 2 | G-12 | open; `JX-1` |
| `JG-5` | Optimizer allocation (alignment, Adam effects) and missing measurements (no per-step monitor trace, no never-anchored generalization, global norms only) | 3 | G-5 | open; `JX-1` to `JX-4`, `JD-10` |
| `JG-6` | Reference disposition after the correction; realism of the probe cases | 4 | G-8 | `JD-0`; `OQ-1` |
| `JG-7` | Schedule causality | 5 | — | open; `JX-7` |
| `JG-8` | Architecture causality; no decomposition on the project's model, because `ArchitectureSpec` refuses non-default values | 6 | G-3 | open; `JX-5`, `JD-9` |
| `JG-9` | The completion budget | 7 | — | **void as an answer** (R-2); `JX-8` |
| `JG-10` | Monitor dynamics from sparse snapshots | 8 | — | open; `JX-2`, `JD-10` |
| `JG-11` | Population and seed coverage | 9 | (evidence limits) | `JD-7` |
| `JG-12` | Accuracy calibration: what physical normalization and tolerance an absolute criterion uses | 10 | G-7 | open; `JX-4`, `JD-3` |
| `JG-13` | Where the 0.5 threshold and N = 500 come from | — | G-4 | `OQ-5`, `JD-4` |
| `JG-14` | "Epoch" under replay batching | — | G-6 (narrowed by the verification) | `OQ-2` |
| `JG-15` | Causal weighting across many trajectories per batch | — | G-9 | `OQ-4` |
| `JG-16` | The source of float32/MPS nondeterminism | — | G-10 | engineering investigation; bears on replicate design |
| `JG-17` | Whether external agents may read training- and validation-split files | — | G-11 | **resolved** by R-5 |
| `JG-18` | The 2024 journal text of the source method | — | G-13 | open: `LR-22` `NOT-READ` (publisher access) |
| `JG-19` | Literature silences: second-order systems, a supervised data term with causal weights, SIREN or LayerNorm stacks with causal weights, how the schedule should interact with the weights | — | G-14 | **confirmed silent** in the sources read (`LR-16`; departures L-7 to L-9); empirical only (`JX-8`) |
| `JG-20` | The invariant-B monitor contract lives only in 57-RULING, and the spec's cross-reference dangles | — | G-15 | `OQ-3` |
| `JG-21` | Q5's oscillation as a property of the ratified recipe | (Q5) | (Q5) | **void as an answer** (R-2); the per-step trace in `JX-8` |
| `JG-22` | The verification's open forward-pass items: the smoke monitor's fronts at steps 100, 200 and 300, and the monitor-recompute values | — | — | `{verify}`; `JX-10` |

## REGISTERS — the claims registers

The two claims registers (Codex §5, `codex:410-446`; Claude §6,
`claude:1630-1699`) are not duplicated here.

- **Where they were checked.** The verification report maps every register
  row to its verdict (`V:573-602`).
- **What this document adds to that mapping.** The literature verdicts from
  JOIN-2, for the rows the verification routed to it:

| Claude register row | Literature verdict |
|---|---|
| `C-39` | `LR-1` `CONFIRMED` |
| `C-40` | `LR-5` `CONFIRMED` |
| `C-41` | `LR-13` `CONFIRMED` (the `jaxpi` part `NOT-READ`, `LR-24`) |
| `C-42` | `LR-17` `CONFIRMED` |
| `C-43` | `LR-7`, `LR-15`, `LR-16` `CONFIRMED` |
| `C-44` | `LR-9` `CONFIRMED` |
| `C-45` | `LR-14` `CONFIRMED`; `LR-18` `CONFIRMED-NARROWER` |
| `C-46` | `LR-23` `NOT-READ` |
| `C-47` | `LR-19` `CONFIRMED` |
| `C-48` | `LR-20` `CONFIRMED` |
| `C-49` | `LR-21` `CONFIRMED` |

Codex's register records its literature claims as "Method identification
confirmed" (H-03). Those claims are `LR-1` to `LR-3`, `LR-5` to `LR-9`,
`LR-13`, `LR-14`, `LR-16`, `LR-17` and `LR-20`, all `CONFIRMED`.

## DOC-CLOSED — what this document establishes, what it does not, and what happens next

### What it establishes

These are facts about the round, not rulings.

1. **The reports do not dispute any diagnosis.**
   - In every question, where both name a mechanism they name the same one.
   - Their differences are confidence and emphasis, and the pooled
     experiments can settle them.
2. **The decision sheet's state.**
   - **Fixed:** `JD-0`.
   - **Agreed:** `JD-3`, `JD-5`, `JD-9`, `JD-10`, `JD-11`, and the
     measure-first order in `JD-2`.
   - **Disputed:** `JD-4`, `JD-6`, `JD-7`, and whether `JD-2` names a
     remedy now.
   - **One report only:** `JD-1`, `JD-8`.
   - **No menu:** five owner questions.
3. **The literature holds.** It refutes none of the source-method facts the
   reports state. One citation is narrowed (`LR-18`). One source fact bears
   on the IC decisions without being an option in either report (`LR-6`).
4. **R-2's effects are applied.**
   - The Q4 budget and Q5's oscillation as a recipe property stay open.
   - Class-`E` evidence appears only as motivation, and is flagged where an
     option leans on it (`JD-2`, `JD-5`).
5. **The recipes differ by purpose.** Codex's control buys attribution and
   Claude's pilot buys information. One mixed pick builds a recipe neither
   report wrote: `JD-4` A together with `JD-6` B.

### What it does not establish

- Any pick, or any default beyond the one R-3 fixes.
- Whether physics was literally a passenger in the update. `JX-1` measures
  it.
- Whether conformance alone restores front progress (`JG-1`).
- Any budget, tolerance or architecture effect size.
- Anything resting on the four literature items not read (`LR-22` to
  `LR-25`).

### What must happen next

1. **The owner rules** on the candidate decision sheet (`JD-0` to `JD-11`)
   and the owner questions (`OQ-1` to `OQ-5`), and decides which of `JX-1`
   to `JX-10` to authorize. That includes whether model computation on
   retained checkpoints is authorized.
2. **The picks are recorded** as project Key Decisions
   (`.planning/PROJECT.md`, "Key Decisions"; ERW Rule 13) and carried into
   the next milestone. Under R-3 its first work is `JD-0`.
3. **Any pick that needs a spec change goes through formal amendment** and
   explicit owner re-ratification.

## VERIFICATION — the checks run at this document's close

**How the checks were run.**

- **On which file.** The script in Appendix A ran on this file, from the
  repository root, with the downloaded literature sources alongside:
  `python3 -I r4c_check.py <this file> <literature dir>`.
- **The output.** It is reproduced in full in Appendix A.
- **What the results show:**
  - **Citations.** Every report, verification and repository citation in
    this document resolves to an existing file and line range: 328
    citations, none unresolved. While drafting, each cited report line was
    also read to confirm it says what this document attributes to it.
  - **Verification rows.** Every verification row this document names
    exists in the verification report's ledger.
  - **Identifiers.** Every `JD`, `OQ`, `JX`, `JG` and `LR` identifier that
    is referenced is also defined.
  - **The decision sheet.** It has 17 rows, and the owner's-pick cell is
    empty in every one. Every JOIN-5 option row carries an attribution tag.
  - **The literature.**
    - All seven downloaded sources match the digests recorded in JOIN-2.
    - Every quoted literature location contains the quoted text.
    - The guide's appendix lists causal tolerance 1.0 five times, with 16
      chunks three times and 32 twice.
    - The power-skip source contains no normalization layer.
    - No source read mentions cosine annealing or L-BFGS.
  - **Whitespace.** No line ends in whitespace.

**Read-only assertions** about the commit that adds this document:

- It adds this file only.
- It changes no code, configuration, framework spec or run artifact.
- It runs no training, evaluation or model computation.
- The delivery note's status and the planning state are updated in a
  separate commit.

## Appendix A — the close-check script and its output

`r4c_check.py`, SHA-256 `8ecafed78d04ca92d54498b9510cefaf1461d2b46975a2f8b3391904cc2802bd`. It was run from the repository root:
`python3 -I r4c_check.py pinn_instruction/markdown_conversion/framework-specs/trainex-r4/trainex-r4-resolution-doc.md <literature dir>`.
Here `<literature dir>` holds the downloaded sources listed in JOIN-2. Each
arXiv source is at `<id>/eprint.bin`, extracted into `<id>/src/`. The code
archive is at `CausalPINNs/repo.tar.gz`, extracted into `CausalPINNs/src/`.

```python
"""Checks run at the close of the trainex-r4 consolidated resolution document.

Usage (from the repository root):
    python3 -I r4c_check.py <resolution-doc.md> [<literature-dir>]

1. Every report, verification and repository citation `file:N` or `file:N-M`
   resolves to an existing file with at least M lines. A bare `:N` continues
   the previous citation on the same line.
2. Every verification row ID the document names exists in the verification
   report's ledger.
3. Every JD/JX/JG/OQ/LR identifier that is referenced is also defined.
4. The candidate decision sheet's owner's-pick cell is empty in every row,
   and every JOIN-5 option row carries an attribution tag.
5. No line ends in whitespace, and the file ends with a newline.
6. With <literature-dir>: every downloaded source matches its recorded
   SHA-256, and every literature location quoted in the ledger contains the
   expected text.
Read-only.
"""
import hashlib
import re
import sys
from pathlib import Path

doc_path = Path(sys.argv[1])
doc = doc_path.read_text()
lines = doc.splitlines()
R4 = "pinn_instruction/markdown_conversion/framework-specs/trainex-r4/"
FS = "pinn_instruction/markdown_conversion/framework-specs/"
VR = "docs/work/reviews/cross_cutting/trainex-r4/2026-10-07-trainex-r4-rule19-claim-verification.md"
SHORT = {
    "codex": R4 + "research_results/codex-resolution.md",
    "claude": R4 + "research_results/claude-resolution.md",
    "V": VR,
    "r3-resolution": FS + "trainex-r3/trainex-r3-resolution-doc.md",
    "pinn_architecture.md": FS + "pinn_architecture.md",
    "ctl_instruction.md": FS + "ctl_instruction.md",
    "controllers.py": "pinn/training/controllers.py",
    "batches.py": "pinn/data/batches.py",
    "54-RULING.md": ".planning/phases/54-recalibration-decision-grounding/54-RULING.md",
    "54-GAPS.md": ".planning/phases/54-recalibration-decision-grounding/54-GAPS.md",
    "57-GAPS.md": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/57-GAPS.md",
    "57-02-PLAN.md": ".planning/phases/57-corrected-re-run-the-preserved-evaluation/57-02-PLAN.md",
}
LIT_FILES = re.compile(r"^(main\.tex|appendix\.tex|sections/|Amir-et-al-24\.tex|KS/|NS/|Lorentz/)")
nlines = {}


def length(path):
    if path not in nlines:
        p = Path(path)
        nlines[path] = len(p.read_text().splitlines()) if p.is_file() else -1
    return nlines[path]


# 1. Citations.
cites, bad = 0, []
for ln, line in enumerate(lines, 1):
    last = None
    for span in re.findall(r"`([^`]+)`", line):
        m = re.fullmatch(r"([A-Za-z0-9_./-]+):(\d+)(?:-(\d+))?", span)
        c = re.fullmatch(r":(\d+)(?:-(\d+))?", span)
        if m:
            name, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
            if LIT_FILES.match(name):
                last = None
                continue
            path = SHORT.get(name, name)
            if name not in SHORT and not re.match(r"(pinn|\.planning|docs|configs|runs|pinn_instruction)/", name):
                last = None
                continue
            last = path
        elif c and last:
            path, a, b = last, int(c.group(1)), int(c.group(2) or c.group(1))
        else:
            continue
        cites += 1
        n = length(path)
        if n < 0 or not (1 <= a <= b <= n):
            bad.append(f"line {ln}: {span} -> {path} (file lines {n})")
print(f"1. citations checked: {cites}; unresolved: {len(bad)}")
for b in bad:
    print("   UNRESOLVED", b)

# 2. Verification row IDs.
ver = Path(VR).read_text()
ledger_ids = set(re.findall(r"^\| ([A-H]-[A-Za-z0-9]+) \|", ver, re.M))
named = set(re.findall(r"`((?:[A-H])-(?:P\d[a-z]?|PC\d+[a-z]?|F\d\d|[A-Z]{1,2}\d[a-z0-9]*|[A-Z]\d+[a-z]?|E-?\d|L\d|N\d|X\d|O\d|V\d))`", doc))
named |= {m for m in re.findall(r"verification `([A-H]-\d+)`", doc)}
named |= {m for m in re.findall(r"`([A-H]-[A-Z]+\d+[a-z]?)`", doc)}
missing = sorted(i for i in named if i not in ledger_ids and not re.fullmatch(r"[A-H]-\d\d", i))
print(f"2. verification row IDs named: {len(named)}; not found in the ledger: {missing or 'none'}")

# 3. Identifier consistency.
def ids(pat):
    return set(re.findall(pat, doc))
problems = []
for kind, define_pat in [("JD", r"^### (JD-\d+) "), ("OQ", r"^\| `(OQ-\d+)` \| [A-Z]"),
                         ("JX", r"^\| `(JX-\d+)` \|"), ("JG", r"^\| `(JG-\d+)` \|"),
                         ("LR", r"^\| `(LR-\d+)` \|")]:
    defined = set(re.findall(define_pat, doc, re.M))
    used = ids(rf"\b({kind}-\d+)\b")
    if used - defined:
        problems.append(f"{kind} used but not defined: {sorted(used - defined)}")
    print(f"3. {kind}: defined {len(defined)}, referenced {len(used)}")
for p in problems:
    print("   PROBLEM", p)

# 4. Sheet and attribution.
start = doc.index("## CANDIDATE-SHEET")
end = doc.index("## JOIN-6-COHERENCE")
rows = [r for r in doc[start:end].splitlines() if re.match(r"^\| `(JD|OQ)-\d+`", r)]
nonempty = [r[:30] for r in rows if r.rstrip().split("|")[-2].strip()]
print(f"4. decision-sheet rows: {len(rows)}; owner's-pick cells not empty: {nonempty or 'none'}")
j5 = doc[doc.index("## JOIN-5-OPTIONS"):start]
opt_rows = [r for r in j5.splitlines() if r.startswith("| **")]
untagged = [r[:40] for r in opt_rows if not re.search(r"`\{(codex|claude|both|ruling R-\d)\}`|the status quo named by", r)]
print(f"   JOIN-5 option rows: {len(opt_rows)}; without an attribution tag: {untagged or 'none'}")
lr_rows = [r for r in doc.splitlines() if re.match(r"^\| `LR-\d+` \|", r)]
verdicts = {}
for r in lr_rows:
    v = r.rstrip().split("|")[-2].strip()
    verdicts[v] = verdicts.get(v, 0) + 1
print(f"   literature ledger rows: {len(lr_rows)}; verdicts: {verdicts}")

# 5. Whitespace.
trailing = sum(1 for l in lines if l != l.rstrip())
print(f"5. lines with trailing whitespace: {trailing}; ends with a newline: {doc.endswith(chr(10))}")

# 6. Literature sources.
if len(sys.argv) > 2:
    L = Path(sys.argv[2])
    CP = "CausalPINNs/src/CausalPINNs-0d1d83f87f6fa2d6756d0e35cac94a7be6183841/"
    digests = dict(re.findall(r"^\| `S-[A-H]` \| .*?\| `(https://[^`]+)` \| `([0-9a-f]{64})` \|", doc, re.M))
    files = {"2203.07404v1": "2203.07404/eprint.bin", "CausalPINNs/tar.gz": "CausalPINNs/repo.tar.gz",
             "2308.08468": "2308.08468/eprint.bin", "2001.04536": "2001.04536/eprint.bin",
             "2402.00326": "2402.00326/eprint.bin", "2006.09661": "2006.09661/eprint.bin",
             "2310.15690": "2310.15690/eprint.bin"}
    ok = 0
    for url, sha in digests.items():
        local = next(v for k, v in files.items() if k in url)
        got = hashlib.sha256((L / local).read_bytes()).hexdigest()
        ok += got == sha
        if got != sha:
            print("   DIGEST MISMATCH", url)
    print(f"6. source digests matching the document: {ok} of {len(digests)}")
    CHECKS = [
        ("2203.07404/src/main.tex", 81, 81, "Respecting causality is all you need"),
        ("2203.07404/src/main.tex", 288, 291, "causality parameter"),
        ("2203.07404/src/main.tex", 367, 367, "lax.stop\\_gradient"),
        ("2203.07404/src/main.tex", 356, 357, "annealing strategy for adjusting"),
        ("2203.07404/src/main.tex", 374, 407, "\\delta = 0.99"),
        ("2203.07404/src/main.tex", 374, 407, "[10^{-2}, 10^{-1}, 10^{0}, 10^{1}, 10^{2}]"),
        ("2203.07404/src/main.tex", 351, 353, "all of them converge to $1$"),
        ("2203.07404/src/main.tex", 488, 488, "decay-rate of 0.9 every $5,000$"),
        ("2203.07404/src/main.tex", 501, 501, "\\sigma=3"),
        ("2203.07404/src/main.tex", 503, 503, "over-fitting"),
        ("2203.07404/src/main.tex", 503, 503, "1.139e-02"),
        ("2203.07404/src/appendix.tex", 51, 51, "512"),
        ("2203.07404/src/appendix.tex", 70, 91, "Max Iteration"),
        ("2203.07404/src/appendix.tex", 127, 142, "\\Delta t = 0.5"),
        ("2203.07404/src/appendix.tex", 127, 142, "N_t = 256"),
        (CP + "KS/chaotic_KS.py", 165, 168, "L_0 = 1e4 * self.loss_ics(params)"),
        (CP + "KS/chaotic_KS.py", 165, 168, "lax.stop_gradient(np.exp(- tol * (self.M @ L_t + L_0) ))"),
        (CP + "KS/chaotic_KS.py", 165, 167, "np.mean(r_pred**2, axis=1)"),
        (CP + "KS/chaotic_KS.py", 276, 276, "tol_list = [1e-3"),
        (CP + "KS/regular_KS.py", 191, 191, "self.M @ L_t + L_0"),
        (CP + "KS/regular_KS.py", 188, 188, "L_0 = 1e3 * self.loss_ics(params)"),
        (CP + "NS/NS.py", 296, 296, "L_0 = 1e5 * (loss_u0 + loss_v0 + loss_w0)"),
        ("2203.07404/src/appendix.tex", 187, 187, "\\lambda_{ic} = 10^4"),
        ("2203.07404/src/appendix.tex", 249, 249, "\\lambda_{ic}=10^4"),
        ("2203.07404/src/main.tex", 197, 197, "\\lambda_{ic} = 100"),
        (CP + "NS/NS.py", 299, 299, "self.M @ L_t + L_0"),
        (CP + "NS/NS.py", 221, 223, "decay_steps=10000"),
        (CP + "NS/NS.py", 419, 419, "tol_list = [1e-3"),
        (CP + "Lorentz/Causal_PINNs_lorentz.py", 198, 198, "lax.stop_gradient"),
        (CP + "Lorentz/Causal_PINNs_lorentz.py", 122, 122, "n_t = 300"),
        (CP + "Lorentz/Causal_PINNs_lorentz.py", 263, 263, "sigma = 10.0"),
        (CP + "Lorentz/Causal_PINNs_lorentz.py", 268, 268, "T = 30"),
        (CP + "Lorentz/Causal_PINNs_lorentz.py", 277, 277, "tol_list = [1e-3, 1e-2, 1e-1, 1e0, 1e1]"),
        (CP + "Lorentz/Causal_PINNs_lorentz.py", 298, 298, "nIter=300000"),
        ("2308.08468/src/main.tex", 297, 297, "\\epsilon=1.0"),
        ("2308.08468/src/main.tex", 435, 435, "lax.stop\\_gradient"),
        ("2308.08468/src/main.tex", 438, 438, "slightly reduce the value of $\\epsilon$"),
        ("2308.08468/src/main.tex", 268, 284, "moving average"),
        ("2308.08468/src/main.tex", 447, 447, "cannot be normalized during the pre-processing step"),
        ("2308.08468/src/main.tex", 588, 588, "decay rate of 0.9 for every $2,000$"),
        ("2001.04536/src/main.tex", 102, 104, "stiffness in the gradient flow dynamics"),
        ("2001.04536/src/main.tex", 102, 104, "unstable imbalance in the magnitude of the back-propagated gradients"),
        ("2001.04536/src/main.tex", 425, 430, "\\max_{\\theta}"),
        ("2001.04536/src/main.tex", 432, 445, "(1 - \\alpha ) \\lambda_i + \\alpha \\hat{\\lambda}_i"),
        ("2001.04536/src/main.tex", 432, 445, "\\alpha=0.9"),
        ("2402.00326/src/main.tex", 149, 149, "non-suitable initialization schemes, which result in poor trainablity"),
        ("2402.00326/src/main.tex", 531, 531, "linear combination of the first layer embeddings"),
        ("2402.00326/src/main.tex", 880, 880, "complete model collapse for deeper networks"),
        ("2006.09661/src/sections/representation.tex", 104, 104, "spans multiple periods over $[-1,1]$"),
        ("2310.15690/src/Amir-et-al-24.tex", 194, 194, "$\\tanh$"),
        ("2310.15690/src/Amir-et-al-24.tex", 432, 432, "a power of 2 is effective for networks with fewer than 30 hidden layers"),
    ]
    passed = 0
    for rel, a, b, text in CHECKS:
        seg = "\n".join((L / rel).read_text().splitlines()[a - 1:b])
        if text in seg:
            passed += 1
        else:
            print("   LOCATION FAILED", rel, a, b, repr(text))
    print(f"   literature locations containing the quoted text: {passed} of {len(CHECKS)}")
    tex_appendix = (L / "2308.08468/src/appendix.tex").read_text()
    print("   guide appendix: 'Causal tolerance & 1.0' x", tex_appendix.count("Causal tolerance & 1.0"),
          "; 'Number of chunks & 16' x", tex_appendix.count("Number of chunks & 16"),
          "; 'Number of chunks & 32' x", tex_appendix.count("Number of chunks & 32"))
    amir = (L / "2310.15690/src/Amir-et-al-24.tex").read_text().lower()
    print("   power-skip source: 'layernorm'/'layer norm'/'batchnorm'/'batch norm'/'normaliz' occurrences:",
          sum(amir.count(w) for w in ("layernorm", "layer norm", "batchnorm", "batch norm", "normaliz")))
    silent = []
    for rel in ["2203.07404/src/main.tex", "2203.07404/src/appendix.tex", "2308.08468/src/main.tex",
                "2308.08468/src/appendix.tex"] + [str(p.relative_to(L)) for p in (L / CP).rglob("*.py")]:
        t = (L / rel).read_text().lower()
        if "cosine" in t or "l-bfgs" in t or "lbfgs" in t:
            silent.append(rel)
    print(f"   sources mentioning cosine or L-BFGS: {silent or 'none'}")
```

Output:

```text
1. citations checked: 328; unresolved: 0
2. verification row IDs named: 41; not found in the ledger: none
3. JD: defined 12, referenced 12
3. OQ: defined 5, referenced 5
3. JX: defined 10, referenced 10
3. JG: defined 22, referenced 22
3. LR: defined 25, referenced 25
4. decision-sheet rows: 17; owner's-pick cells not empty: none
   JOIN-5 option rows: 49; without an attribution tag: none
   literature ledger rows: 25; verdicts: {'`CONFIRMED`': 20, '`CONFIRMED-NARROWER`': 1, '`NOT-READ`': 4}
5. lines with trailing whitespace: 0; ends with a newline: True
6. source digests matching the document: 7 of 7
   literature locations containing the quoted text: 51 of 51
   guide appendix: 'Causal tolerance & 1.0' x 5 ; 'Number of chunks & 16' x 3 ; 'Number of chunks & 32' x 2
   power-skip source: 'layernorm'/'layer norm'/'batchnorm'/'batch norm'/'normaliz' occurrences: 0
   sources mentioning cosine or L-BFGS: none
```
