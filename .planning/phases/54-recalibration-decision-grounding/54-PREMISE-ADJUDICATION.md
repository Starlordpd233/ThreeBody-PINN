---
phase: 54
plan: 11
status: active
created: 2026-09-03
---

# 54-PREMISE-ADJUDICATION — the two returned reports' premise challenges, adjudicated against the packet's own premises

## The rule being applied

The ERW runbook's handoff quick reference, step 6, quoted rather than paraphrased
because it is the rule this record applies:

> **Route B only:** before consolidating or acting, have the in-repo agent produce the
> per-claim verification report (Rule 19). Repo-derived claims are checkable assertions
> until verified — the report's own file:line citations exist so you can hold it to that.
> If a verified claim contradicts a package premise, re-frame the round before using its
> answers; a false premise invalidates the answers built on it, however well-reasoned.

(`docs/runbooks/external-research/2026-06-11-external-research-workflow.md:261`–`:265`.)

The duty the challenges discharge is Rule 17, also quoted:

> **Route B carries a premise-challenge mandate, and it is not optional.** The prompt
> must instruct the agent to test the package's own stated premises against the
> repository and to report contradictions as **first-class findings reported up front**,
> not as per-question footnotes. Phrase it as a duty, not a permission: an agent that
> finds a false premise and buries it has failed the round.

(`…external-research-workflow.md:209`–`:215`.)

## The boundary this record does not cross

This record determines **whether premises hold** and **which answers rest on them**. It
determines nothing about what any answer should be. It disposes of no decision surface,
names no value, form, rescaling, bound or ordering for any surface, marks nothing and
ranks nothing (SCOPE-34, `.planning/REQUIREMENTS.md:119`). Where a quantity under
adjudication is itself an option value, a component of a marked default, or a stipulated
threshold that could read as one, the quantity is **located by citation and not printed** —
the discipline the verification report's Part II adopted for the same reason.

Two acts are kept apart deliberately and the record says so in as many words:
**verification** says what is true of the tree and of the attachments; **adjudication**
says what that does to the question the round was asked. Collapsing them would let a
strong verdict silently rewrite the packet's framing.

## Table-cell pipe convention

Every literal pipe character inside a table cell in this file is written escaped as `\|`.
This is the convention `54-06-PLAN.md` set for `54-RECONCILIATION.md`, `54-07-PLAN.md`
restated for `54-HANDOFF-READINESS.md` and `54-INTAKE.md` restated again. The empty-cell
gate splits every markdown table row on the pipe character, so an unescaped pipe inside a
cell yields an empty field and reports `EMPTY-CELL` on a correctly filled row, or silently
shifts every cell after it. The repair is always the escape, never deleting the content
from the cell. Note that `‖` (double vertical line) is a different character and needs no
escape.

## Path and identifier abbreviations

Bound here to exactly one target each, so no citation is reachable only through an
abbreviation.

| Abbrev. | Full path or namespace |
|---|---|
| `MA` | `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md` — **the packet** |
| `PR` | `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-AGENT-PROMPT.md` |
| `BU` | `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/specs/framework-specs-bundle.md` |
| `OB` | `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_results/claude-resolution.md` — the open-book report |
| `CB` | `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_results/chatgpt-resolution.md` — the closed-book report |
| `V` | `docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/2026-09-02-trainex-r3-rule19-claim-verification.md` — the ERW Rule-19 verification report |
| `AR` | `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` |
| `CT` | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` |
| `AUD` | `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md` |
| `D5` | `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-DIAG-05-REDERIVATION.md` |
| `REQ` | `.planning/REQUIREMENTS.md` |
| `PREM-nn` | **this record's own** premise identifiers. They are not the packet's, not the reports', and not `V`'s partition labels `P-A` / `P-B` / `P-C` |

Ledger identifiers are `V`'s and are carried through unchanged: `R-01`…`R-15`,
`PC-1`…`PC-9` with lettered sub-rows, `D-1`…`D-7` with lettered sub-rows (`V`'s own
departures-table labels, **not** this project's decision identifiers `D-01`…`D-18` in
`54-CONTEXT.md`), `CC-1`…`CC-7`, `CB-01`…`CB-13`, `CB-F1`…`CB-F8` with lettered sub-rows,
`CB-G01`…`CB-G12`, and cross-report points `X-01`…`X-22`.

## ADJUDICATION-COUNTS

Derived from the tables below rather than asserted, so the document states its own result.

| Quantity | Value |
|---|---|
| Premise-challenge findings extracted, both reports, top level | `CHALLENGE-TOTAL=17` — 9 from `OB` (`PC-1`…`PC-9`), 8 from `CB` (`Finding 1`…`Finding 8`) |
| The same findings as separately checkable sub-assertions, per `V`'s split rule | 63 — 36 open-book sub-rows and 27 closed-book sub-rows |
| Packet premises adjudicated | 19 (`PREM-01`…`PREM-19`) |
| Premises `CONTRADICTED` | 3 — `PREM-01`, `PREM-09`, `PREM-12` |
| Premises `QUALIFIED` | 11 — `PREM-03`, `PREM-04`, `PREM-05`, `PREM-06`, `PREM-07`, `PREM-08`, `PREM-10`, `PREM-11`, `PREM-13`, `PREM-14`, `PREM-16` |
| Premises `INTACT` | 4 — `PREM-15`, `PREM-17`, `PREM-18`, `PREM-19` |
| Premises `UNSETTLED` | 1 — `PREM-02` |
| Packet premises recorded `UNCHALLENGED` | 11 (enumerated under *Closing the loop*) |
| Answers marked `NOT-USABLE-UNTIL-REFRAMED` | `ANSWERS-NOT-USABLE=0` |
| Challenges reaching no packet premise | 2 groups, enumerated under *Challenges that reach no packet premise* |
| Candidate decision points assessed | 19 — `V`'s 16 proposed-and-not-filed rows plus 3 this pass surfaced |
| Candidates routed as new gap records | 10 — `GAP-54-02`…`GAP-54-11` |
| Candidates routed to the existing anchor | 1 |
| Candidates disposed of as operational coordination and logged | 7 |
| Candidates that failed the STOP-protocol step-2 understanding test | 0 |

`3 + 11 + 4 + 1 = 19`, the premise-row total. `10 + 1 + 7 = 18`; the nineteenth candidate
was folded into `GAP-54-06` with the candidate it duplicates, and the fold is recorded
where it happens rather than left to be inferred from the arithmetic.

## The closed adjudication vocabulary

Four values. No row carries anything else. The adjudication **follows from the recorded
verdict**: no row is adjudicated `INTACT` because a challenge reads as unpersuasive, and
none is adjudicated `CONTRADICTED` because a challenge reads as persuasive. The verdict is
the evidence and the row cites it.

| Value | Meaning |
|---|---|
| `CONTRADICTED` | A verified claim contradicts the premise as the packet states it. |
| `QUALIFIED` | The premise holds only under a narrower reading than the packet's wording. The narrower reading is stated in the row. |
| `INTACT` | The challenge does not survive its own verdict, or survives and does not reach the premise, or survives and — being a negative or confirmatory finding — reaches the premise and upholds it. The row states which of the three. |
| `UNSETTLED` | The challenging claim's verdict is `NOT-VERIFIABLE-HERE`, so the premise is neither upheld nor contradicted by anything checked. The row states what would settle it and cites the routing `V` recorded. |

## The closed consequence vocabulary

Three values, recorded per answer the premise reaches, by the packet's own question
numbering (`MA:221`–`:257`, questions `§5.1`–`§5.6` plus the cross-cutting form
requirements `§5.7(a)`–`§5.7(e)`).

| Value | Meaning |
|---|---|
| `USABLE` | The answer does not rest on the part of the premise that failed, and carries no qualification from this adjudication. |
| `USABLE-QUALIFIED` | The answer is usable with a stated qualification, which travels with it into the consolidation. |
| `NOT-USABLE-UNTIL-REFRAMED` | The answer rests on a premise the evidence contradicts and cannot be used until the round is re-framed. |

A premise adjudicated `CONTRADICTED` whose dependent answers are **all** recorded `USABLE`
would be a contradiction in this record. No such row exists, and the explicit read for it
is recorded under *Acceptance reads performed*.

## How this table was built

Working from the challenges to the premises, then closing the loop.

1. **Extraction, not summary.** Both reports' premise-challenge sections were extracted
   whole — `OB` §1 at `:42`–`:291` and `CB` §1 at `:15`–`:94` — using the identifiers and
   the sub-assertion split `V` already fixed. Both extractions are non-empty and their
   sizes are recorded above, so an extraction that silently matched nothing cannot pass
   coverage by producing zero on both sides.
2. **Each challenge is mapped to the packet premise it challenges**, cited into the packet
   by file and line and **resolved by content** — every anchor in this record was read at
   its line before being cited, because the packet's own amendment record shows text
   moving and its `§3` anchor-resolution rule (`MA:90`) makes content resolution the house
   rule.
3. **Duplicates merge on the premise.** Where both reports challenge the same premise that
   is **one** row carrying both challenges, both ledger identifiers, both verdicts and the
   entitlement `V`'s independence ledger recorded for that point. Two rows would let a
   premise be recorded as contradicted twice and would double-count the evidence against
   it.
4. **The verdict is the only admissible evidence about a claim.** Every row names the
   ledger identifier it relies on and the verdict `V` assigned it. A row citing a claim
   that carries no verdict in `V` is a coverage failure and the gate rejects it.
5. **Row order follows the packet's own premise numbering** — the `F-` register order,
   then the `M-` entries, then the sections. That order carries no precedence, exactly as
   `54-RULING.md` states of the surface order.
6. **The packet is not edited.** It is an uploaded attachment, frozen since upload (D-15).
   Every defect found in it is recorded here with its correction stated in this record and
   attributed to this pass. Naming a document that would need amending is not amending it,
   and no amendment is performed or proposed.

## The premise adjudication table

| Premise | Where the packet states it | Challenged by | Ledger ID and verdict | Adjudication | Answers built on it | Consequence | Note |
|---|---|---|---|---|---|---|---|
| `PREM-01` — `F-02`: "`first_omega_0 = 30` **sets** the second-derivative magnitude", tiered *established* | `MA:268` (the `F-02` register row); the packet's own correction note at `MA:129`; amendment `A-1` at `MA:414` | `OB` `PC-1`; `CB` `Finding 3` | `PC-1a` CONFIRMED; `PC-1b` CONFIRMED; `CB-F3a` CONFIRMED. Entitlement `X-01` **CORROBORATED** (`CLASS-PACKAGE-INTERNAL`; `V` calls it the cleanest two-agent reading in the round) | **CONTRADICTED** | `§5.3`; `§5.6`; `§5.7(a)` | `USABLE-QUALIFIED` for all three | The register table `MA:261` tiers as "established evidence a reader may rely on" still carries the exact sentence `A-1` classifies as a **correction** — "The packet was narrower than its source, in a direction that overstates one decision surface." The amendment record makes the two-factor reading (`M2` at `MA:121`, `F-11` at `MA:277`) authoritative. Qualification: any answer to `§5.3` is read against the two-factor attribution. Both reports flagged the contradiction up front, so neither built an answer on the superseded wording — see the per-premise detail |
| `PREM-02` — `§4.3`'s five-surface enumeration as the decision's surface set, with `S3` naming the SIREN initialization scale alone | `MA:151`–`:193`, `S3` at `MA:171`; the packet's own `§7` `S3-adjacent` entry at `MA:311`; the fourth-remedy-family transcription at `MA:211`–`:215` | `OB` `PC-1`; `OB` `PC-6` | `PC-1f` **CONFIRMED-NARROWER (locus and scope) · NOT-VERIFIABLE-HERE (the capacity attribution)**; `PC-6c` NOT-VERIFIABLE-HERE. Supporting routed rows `R-05` and `R-04`, both NOT-VERIFIABLE-HERE. One-agent — `CB` makes no counterpart | **UNSETTLED** | `§5.2`; `§5.3`; `§5.6`; `§5.7(a)`; `§5.7(d)` | `USABLE-QUALIFIED` for all five | Three of `PC-1f`'s four assertions re-derive exactly — `AR` `§2.3` occupies `:204`–`:261`, SCOPE-33's enumeration (`REQ:118`) does not reach it, and `MA:311` records the stack as an unsurfaced gap in the packet's own words. The half that would contradict the enumeration rests on a clean-room sweep and on a prediction about a run this milestone does not authorize, and `V` routed both. Routed as **`GAP-54-02`**, cross-phase reframing — the enumeration is the owner's to widen |
| `PREM-03` — `M2`'s effective angular-frequency range as transcribed | `MA:123` (the verbatim `AUD:165` quotation); `MA:127` (the packet's restatement) | `CB` `Finding 3` | `CB-F3c` CONFIRMED (exact; the ratios over the six printed rows are re-derived in `V`'s `THREE-WAY-READINGS`). One-agent | **QUALIFIED** | `§5.3`; `§5.7(a)` | `USABLE-QUALIFIED` for both | Narrower reading: the transcribed range is a round-number summary and its upper end understates the range implied by the audit's own printed table by about a tenth. The quantity is the network's effective angular frequency in the coordinate, and a squared quantity carries that understatement squared — which is why the difference is named rather than waved through. Correction attributed to this pass; nothing is edited |
| `PREM-04` — `M2`'s per-odd-layer scalar-gain attribution as a quantitative account of the stack's contribution | `MA:123` (inside the same verbatim audit quotation) | `CB` `Finding 3`; `OB` `PC-1` on a different property of the same operation | `CB-F3b` CONFIRMED; `PC-1d` **CONFIRMED-NARROWER**. One-agent on each half | **QUALIFIED** | `§5.3`; `§5.7(a)`; `§5.7(e)` | `USABLE-QUALIFIED` for all three | Narrower reading: the attribution holds **qualitatively** — that the stack compounds the derivative magnitude is separately carried by `F-11` and measured as a compound effect by the audit — and does not hold as a quantitative prediction, because the branch's Jacobian is a matrix with cross-coordinate structure and a product of six scalar gains is not that. `PC-1d` adds a second narrowing from the other direction: the invariance the competing argument rests on is exact only in a limit. Routed as **`GAP-54-08`** |
| `PREM-05` — `F-03` / `M3`: the causal weight **underflows** float32 above the stated bound | `MA:269` (`F-03`); `MA:131` (`M3`) | `OB` `PC-3`; `CB` `Finding 5` | `PC-3a` CONFIRMED; `PC-3b` **CONFIRMED-SHARPER**; `PC-3d` CONFIRMED; `CB-F5a` CONFIRMED; `CB-F5b` CONFIRMED; `CB-F5c` CONFIRMED; `CB-F5d` CONFIRMED. Entitlements `X-05` **CORROBORATED** (machine constant, no shared package premise), `X-06` CORROBORATED / RECONCILABLE, `X-07` CORROBORATED | **QUALIFIED** | `§5.1`; `§5.5`; `§5.7(a)` | `USABLE-QUALIFIED` for all three | Narrower reading: the **value** is right and the **label** is too broad. The bound is the smallest-normal boundary, which is also the floor the implementation actually clamps at (`PC-3b` sharpens the observed minimum weight to within one unit in the last place of the exponential of that floor); the point at which the exponential reaches zero lies further down, and `CB-F5b` distinguishes the two further boundaries below it. Both reports carry the correction and both record that it does not rescue the baseline (`CB-F5d`), so the capacity arithmetic on both sides already uses the clamp binding |
| `PREM-06` — `F-13` plus `§7`'s "the silence recorded here is this package's, not the literature's" | `MA:279` (`F-13`); `MA:313` (the `§7` cross-cutting entry) | `OB` `PC-4` | `PC-4a` **CONFIRMED-SHARPER**; `PC-4b` CONFIRMED. Entitlements `X-10` **CORROBORATED** (`CLASS-LITERATURE`; `V` records the delivery note's `§5.7(c)` join point as satisfied) and `X-11` NOT-CORROBORATED / RECONCILABLE on a qualifier both authors state | **QUALIFIED** | `§5.7(c)` | `USABLE` | `F-13` is literally true and is sharpened: a scoped negative search over the whole live specification returns nothing, so the source is cited nowhere in it rather than merely nowhere in its reference list. What is qualified is `§7`'s characterization — the repository already carries both the citation and a working reference implementation, so the silence is the **specification's** and the gap is a spec-citation gap rather than an evidence gap. The challenge discharges `§5.7(c)` rather than undermining it, which is why the consequence is unqualified |
| `PREM-07` — `F-06` / `F-07` and `§4.2`: the exponent grows with the count of preceding points, and the two fixed counts differ by the stated factor | `MA:272` (`F-06`); `MA:273` (`F-07`); `MA:147` (`§4.2`); restated at `MA:185` | `OB` `PC-5`; `CB` `Finding 4` | `PC-5a` CONFIRMED; `PC-5b` **UNSUPPORTED**; `PC-5c` NOT-VERIFIABLE-HERE; `PC-5d` **CONFIRMED-NARROWER**; `CB-F4a` CONFIRMED; `CB-F4b` CONFIRMED. Supporting `D-1b` CONFIRMED, `D-2b` **UNSUPPORTED**, `D-6b` CONFIRMED, `D-6c` CONFIRMED. Entitlements `X-08` NOT-CORROBORATED / **RECONCILABLE** with the shared premise named, `X-09` CORROBORATED subject to the edition caveat | **QUALIFIED** | `§5.1`; `§5.4`; `§5.6`; `§5.7(a)`; `§5.7(d)` | `USABLE-QUALIFIED` for all five | Two narrowings, both from confirmed verdicts, and they point in different directions — both are carried, neither is resolved. (i) The stated factor is the **cardinality** ratio; for a flat profile the endpoint exclusive prefix changes by a different and larger exact factor, which `CB-F4b` derives from the packet's own exclusive-prefix definition at `MA:147`. (ii) The coupling is a consequence of a **departure** from the source's per-segment formulation rather than a property of the published method — established in this repository against the vendored reference implementation (`PC-5d`) and routed for the published half (`PC-5c`). See the per-premise detail |
| `PREM-08` — that the specified count and the executed count name comparable quantities, so their ratio is the coupling | `MA:147`; `MA:179`–`:185` (`S4`); `MA:303` (`§7` `S4`) | `CB` `Finding 4` | `CB-F4c` CONFIRMED (negative search over both specification blocks and the curriculum block, `NEGATIVE-SEARCH-EMPTY` with scope stated; `V` adds that the silence also holds of the specification files themselves at the pinned tree). One-agent | **QUALIFIED** | `§5.1`; `§5.4`; `§5.6` | `USABLE-QUALIFIED` for all three | Narrower reading: the ratio is a ratio of two numbers whose **unit** no consulted source fixes — per batch or per trajectory — and the two readings are numerically confusable because the cardinality ratio times the executed count equals the specified count exactly. A disposition of the count that does not state its unit leaves the exponent magnitude under-determined by exactly the factor the joint-ratification requirement exists to pin. Routed as **`GAP-54-05`**, semantic |
| `PREM-09` — `F-12` / `M6`: the audit's converged-regime comparison scale, transcribed as the only converged-network residual scale any source in the package states | `MA:278` (`F-12`); `MA:139`–`:141` (`M6`) | `CB` `Finding 1` | `CB-F1a` CONFIRMED; `CB-F1b` CONFIRMED; `CB-F1c` CONFIRMED. Entitlements `X-03` NOT-CORROBORATED / **RESOLVED-BY-EVIDENCE** on verdict `CB-F1a`, and `X-04` NOT-CORROBORATED with the shared premise named | **CONTRADICTED** | `§5.1`; `§5.2`; `§5.6`; `§5.7(a)` | `USABLE-QUALIFIED` for all four | The packet reproduces two descriptions of the same reference probe verbatim and they are incompatible — one finite-differences a stored integrator trajectory, the other measures a trained network against ground truth — and `F-12` transcribes the inference that only the second could support. **Unlike `PREM-01`, the packet's amendment record does not make either reading authoritative**: all sixteen entries at `MA:412`–`:429` are silent on it. Both reports independently concluded the gate cannot supply a normalizer, so no returned answer rests on the contradicted reading; the exposure is forward. Routed as **`GAP-54-03`**, semantic. See the per-premise detail |
| `PREM-10` — `§3`'s tiering of the operative diagnosis as settled and not re-litigated | `MA:85` (the hard-constraint tier); the diagnosis's own statements at `D5:84` and `D5:80`, reproduced in attachment 3 | `CB` `Finding 2` | `CB-F2a` CONFIRMED; `CB-F2b` CONFIRMED; `CB-F2c` CONFIRMED; `CB-F2d` NOT-VERIFIABLE-HERE. One-agent | **QUALIFIED** | `§5.1`; `§5.6`; `§5.7(b)` | `USABLE-QUALIFIED` for all three | Narrower reading: the tiering holds as an instruction, and two of the diagnosis's own statements are stronger than the record they rest on. The record establishes six initialization cases, one halted run of the length the log carries, and a fitted decline over the full-weight segment; that supports failure throughout the observed budget and does not by itself support budget-independence or a universal claim over initial conditions. `§3` itself anticipates this class: attachment 3 is tiered "**Hard constraint** for the evidence; the *reasoning* is testable under ERW Rule 17" (`MA:63`), so the challenge exercises the packet's premise structure rather than breaking it |
| `PREM-11` — the audit's `§6a` conclusion that the data term contributes nothing to the accumulated float32 gradient, carried as hard-constraint evidence | `AUD:132` and `:134`, reproduced verbatim in attachment 3; tiered at `MA:63` | `OB` `PC-6`; `CB` `Finding 6` | `PC-6a` CONFIRMED; `PC-6b` CONFIRMED; `PC-6c` NOT-VERIFIABLE-HERE; `CB-F6a` CONFIRMED; `CB-F6b` CONFIRMED; `CB-F6c` CONFIRMED; `CB-12` **CONFIRMED (the reported imbalance) · NOT-VERIFIABLE-HERE (componentwise disappearance)**. Entitlement `X-17` NOT-CORROBORATED / **OPEN-DISPUTE** | **QUALIFIED** | `§5.2`; `§5.6`; `§5.7(a)`; `§5.7(b)` | `USABLE-QUALIFIED` for all four | Narrower reading: the reported ratio establishes severe imbalance; complete componentwise disappearance is an inference the cited evidence does not prove, because floating-point addition acts componentwise and a ratio of norms bounds no component. Both consequences are carried and neither is chosen: one report treats the disappearance as established and derives a normalization-location argument from it, the other holds the evidence cannot establish it, and `V` settles neither. Routed as **`GAP-54-07`**, semantic; the location difference it feeds is `X-18` and is routed to the anchor |
| `PREM-12` — `M7`'s claim of agreement to three significant figures in all six rows | `MA:143` | `CB` `Finding 7`; `OB` `PC-8` endorsing `M7` | `CB-F7a` CONFIRMED; `PC-8g` CONFIRMED (of the arithmetic, with `V` recording one last-place difference and agreement within half a percent). Entitlement `X-15` NOT-CORROBORATED / **RESOLVED-BY-EVIDENCE** on verdict `CB-F7a` | **CONTRADICTED** | `§5.1`; `§5.3`; `§5.7(a)` | `USABLE-QUALIFIED` for all three | The two reports computed the same six numbers and reached opposite verdicts on the packet's claim about them; `V` computed them a third time and the narrower statement holds. Four of the six differ from the printed medians at the very figure `M7` claims agreement to, with a maximum relative deviation well under one percent. The consistency check remains a good consistency result and only the stated precision fails, which is why nothing downstream is unusable. **This is one of the round's two cases where the engagement that read no tree is the one the evidence supports.** Correction attributed to this pass; nothing is edited. See the per-premise detail |
| `PREM-13` — the retained median residual read as the initialization value | `MA:169` and `MA:299` (the packet's "at initialization" framing); `AUD:125` and `:159`, reproduced in attachment 3 | `CB` `Finding 7` | `CB-F7b` CONFIRMED; supporting `R-13` CONFIRMED, which established the causal fields single-valued across every retained record. One-agent | **QUALIFIED** | `§5.1`; `§5.2`; `§5.3`; `§5.7(a)`; `§5.7(b)` | `USABLE-QUALIFIED` for all five | Narrower reading: the quoted quantity is a median over the whole retained run, not an initialization-only measurement. The two summaries coincide numerically **here** because the field is single-valued across the record, and that coincidence is a fact about this run rather than a property of the statistic. It matters for `§5.7(b)`, which asks precisely about behaviour away from initialization |
| `PREM-14` — `§7`'s `S2` entry, which ends at the statement of absence and attaches no hazard to a normalization | `MA:299`; the surface itself at `MA:163`–`:169` | `OB` `PC-7` | `PC-7a` **CONFIRMED (exact invariance) · NOT-VERIFIABLE-HERE (bit-identity)**; `PC-7b` CONFIRMED; `PC-7c` CONFIRMED; supporting `R-08` **CONFIRMED-NARROWER**. Entitlement `X-16` NOT-CORROBORATED with the shared premise named | **QUALIFIED** | `§5.2`; `§5.6`; `§5.7(b)` | `USABLE-QUALIFIED` for all three | Narrower reading: `§7`'s entry is not falsified, it is incomplete in a direction that matters. A reference that rescales with the residual makes the weight vector exactly invariant to the residual's overall magnitude — an elementary identity, confirmed — so the front index stops responding to descent, and the invariant trips on the high-water mark of exactly that index. Two narrowings travel with it: **bit-identity** is a different claim from exact invariance and generically fails, and it does **not** follow that the front index is constant, since it remains a function of the per-step residual shape. The finding is the stated reason for one report's marked default on this surface; that menu is located by `V` and neither reproduced, ranked nor marked here |
| `PREM-15` — `H-01`'s standing: the trainex-r2 round's interpretive content is prior analysis and not established fact | `MA:289` (`H-01`, labelled "agent analysis — not established fact"); `MA:86` (the challengeable tier); `MA:315` (`§7`'s construction-limit entry); `§0` at `MA:14`–`:33` | `OB` `PC-9` | `PC-9a` **CONFIRMED-NARROWER**; `PC-9b` CONFIRMED; `PC-9c` NOT-VERIFIABLE-HERE; `PC-9d` CONFIRMED. One-agent | **INTACT** — the challenge survives its own verdicts and, testing a row the packet explicitly tiers *challengeable*, upholds the premise about that row's standing | `§5.3`; `§5.7(e)` | `USABLE` for both | The packet's premise is about `H-01`'s **standing**, not its magnitude, and the challenge confirms that standing by doing exactly what the tier invited: deriving independently first and then comparing. The quotation is faithful; the quantitative half is routed; the two retirements the packet already records are confirmed. One narrowing is recorded and routed separately because it is about the round's own labelling rather than about the premise: the sentence carries a package-derived evidence label and appears in none of the three attachments. Routed as **`GAP-54-10`**, process-artifact schema |
| `PREM-16` — `§7`'s enumeration: "This section names the gaps the assembled evidence leaves open, one entry per decision surface plus the cross-cutting entries" | `MA:295` | `CB` `Finding 8`; `OB` `G-7` | `CB-F8a` CONFIRMED; `CB-F8b` CONFIRMED (negative search across the loss-contract and optimizer blocks, `NEGATIVE-SEARCH-EMPTY` with scope stated); `CB-F8c` CONFIRMED; `CB-F8d` CONFIRMED. Entitlement `X-19` **CORROBORATED** — a negative claim about attachments both agents read in full | **QUALIFIED** | `§5.5`; `§5.6`; `§5.7(b)` | `USABLE-QUALIFIED` for all three | Narrower reading: the enumeration holds as far as its own scoping sentence reaches — one entry per surface plus the named cross-cutting entries — and does not exhaust the implementation-behaviour questions the supplied contract leaves open. Both reports independently found one it does not carry, and `X-19` records that agreement as entitled corroboration precisely because it is a negative claim about the shared attachments. Routed, folded with a second per-phase finding, as **`GAP-54-06`**, semantic |
| `PREM-17` — `F-04` / `M4`: the collocation weight vector sits at the numerical floor except for its leading entry, on every logged step | `MA:270` (`F-04`); `MA:133` (`M4`) | `OB` `PC-3` (tested rather than disputed) | `PC-3b` **CONFIRMED-SHARPER**; `PC-3c` CONFIRMED; `PC-3e` **CONFIRMED-SHARPER**; supporting `R-07` CONFIRMED, `R-13` CONFIRMED | **INTACT** — the challenge survives and, being a confirmatory finding, reaches the premise and upholds it, sharpened twice | `§5.1`; `§5.5`; `§5.7(a)` | `USABLE` for all three | Checked against the primary log rather than against any summarising document, single-valued across every retained record, and pinned to the clamp to within one unit in the last place. `PC-3e` sharpens further: the floored-weight result holds on repository evidence at the project's own retained residual scale and does not depend on the clean-room vector at all. Recorded as an intact premise rather than omitted, because an omitted premise and an intact one are different findings and only one of them is a result |
| `PREM-18` — `F-05` / `M5`: the causal front index stayed at zero across the whole retained run, and the invariant halted | `MA:271` (`F-05`); `MA:135` (`M5`) | `OB` `PC-8`; `CB` register row | `PC-8e` CONFIRMED; `CB-02` CONFIRMED; supporting `R-13` CONFIRMED, `PC-7b` CONFIRMED for the index's definition. Entitlement `X-21` **NOT-CORROBORATED** — one agent read the primary log, the other relayed a planning sentence reproduced in an attachment, so the match is bundle-fidelity evidence | **INTACT** — the challenge survives and upholds the premise | `§5.1`; `§5.4`; `§5.7(a)` | `USABLE` for all three | Single-valued at zero over the whole retained record, so the stated proportion is exact rather than approximate. Recorded here with its entitlement because "both reports confirm it" is exactly the sentence a consolidation would be tempted to write as though it were two readings of the log; it is one reading plus this pass's own |
| `PREM-19` — the spec-anchor set, the five-copy anchor-resolution table, and the specs bundle's verbatim fidelity — `F-08`, `F-09`, `F-10`, `F-14`, `F-15` | `MA:274`–`:276`, `MA:280`–`:281`; the anchor-resolution rule at `MA:90` with its table at `MA:94`–`:98` | `OB` `PC-8`; `OB` `PC-2` | `PC-8a` CONFIRMED; `PC-8b` **CONFIRMED-SHARPER**; `PC-8c` CONFIRMED; `PC-8f` CONFIRMED; `PC-2b` CONFIRMED; supporting `R-12` CONFIRMED-NARROWER | **INTACT** — the challenge survives and, being a negative finding, reaches the premise and upholds it | `§5.1`; `§5.3`; `§5.4`; `§5.5` | `USABLE` for all four | A negative finding recorded because its absence would otherwise be invisible. All eight spec anchors the packet cites resolve by content in the live file; `PC-8b` sharpens the bundle check from three spot-checked boundary pairs to all ten blocks line-for-line; the five paths and their line counts resolve, and the tree-wide count confirms the set closed at five. This is the premise every other citation in this record depends on, and it is the one the round tested hardest |

## Per-premise detail — the rows whose adjudication carries more than the cell holds

### `PREM-01` — a corrected packet still carrying its uncorrected register row

The contradiction is entirely internal to the packet and is settleable from the
attachments alone, which is why both engagements could reach it and why `X-01` records
their agreement as genuine two-agent corroboration rather than as bundle fidelity.

The packet corrected itself at `MA:129` and recorded the correction at `MA:414`, but the
correction did not reach the register row at `MA:268`. Which reading is authoritative is
answered by the packet's own amendment record: `A-1` classifies the narrow wording as a
**correction**, so the two-factor reading governs.

The correction this pass records, attributed to this pass and not performed: the `F-02`
row's claim clause should read as `F-11` at `MA:277` reads. The packet is not edited
(D-15).

What the contradiction does **not** establish is worth stating, because the finding's
headline reads wider than its verdicts. Nothing here says the initialization scale is not
a lever; it says the packet's register attributes the whole magnitude to it while the
packet's own evidence attributes it to two compounding factors. How the two factors divide
the measured quantity is unestablished — the packet says so itself at `MA:311` — and the
one measurement offered for it is routed (`R-05`).

### `PREM-02` — the enumeration's completeness, which is not this pass's to settle

Two findings bear on the same question from opposite directions and neither is
agent-disposable.

`PC-1f` re-derives that the architectural section carrying the capacity attributed to an
authorized surface is not inside the authorized enumeration — locus and scope both
`CONFIRMED-NARROWER` — while the claim that the capacity **lives** there rests on a
clean-room depth sweep routed `NOT-VERIFIABLE-HERE` at `R-05`.

`PC-6c` asserts that a recipe repairing the weight vector while leaving the outer physics
loss at its current magnitude would satisfy the train-free gate's three conditions and
still train on the physics term alone. Its arithmetic inputs are confirmed at `PC-6a` and
`PC-6b`; the prediction is routed. The gate's three conditions (`CC-2`, quoting `REQ:100`)
are conditions on the **weight vector** and none is a condition on the magnitude of the
physics loss — which is the mechanical reason the assertion is not obviously wrong and the
reason it cannot be dismissed here.

The packet is not silent about the shape of this question. `MA:311` says in its own words
that whether the stack constitutes a surface of its own "is not settled by anything in
this package", and `MA:211`–`:215` transcribes the routing authority's fourth remedy
family and records that the five surfaces were assembled from the requirement text rather
than from that authority. So the packet's **framing** already admits more than five
surfaces' worth of remedy space. What is unsettled is whether the authorized **surface
set** must be widened, which is a scope question and therefore the owner's. Routed as
`GAP-54-02`.

### `PREM-07` — two narrowings that point in different directions, both carried

`CB-F4b` sharpens the multiplier: for a flat residual profile the endpoint exponent is
proportional to the prefix **length**, which is one less than the count, so the endpoint
multiplier and the cardinality ratio are different exact numbers. The packet's own hedge
at `MA:147` makes its figure defensible as an order-of-magnitude statement; a
joint-ratification requirement is not scoped against an order-of-magnitude statement, and
`V` names that tension in its own candidate row rather than resolving it.

`PC-5` argues the coupling is a **departure** and therefore removable. Its published half
is routed (`PC-5c`), and its in-repository half is `CONFIRMED-NARROWER` at `PC-5d`: the
vendored reference implementation does form one residual per time level rather than one
per collocation point, but it chunks on the distinct time values present in the sampled
batch, which realizes the paper's per-time-level form and not the practitioner guide's
fixed equal segments. The two readings the finding offers are not equivalent and only the
first is implemented here.

`X-08` records the two as **`RECONCILABLE`** — they address different aspects and neither
denies the other — and names the premise both inherited from the same package. Both
consequences travel; neither is chosen. Averaging is unavailable here for the same reason
it was unavailable in `V`'s independence ledger: a third statement neither author holds is
the destruction of the finding the disagreement was, not a resolution of it.

One sub-row of `PC-5` is `UNSUPPORTED` and its consequence is routed rather than repaired.
`PC-5b` and `D-2b` state a per-step re-draw without qualification and cite a line that is
the fixed-draw path of the other optimizer phase; the substance resolves at a different
line and the citation does not carry it. Treating the citation as a typo and verifying at
the line that does carry it would have converted an `UNSUPPORTED` verdict into a
confirmation and erased the per-phase distinction the mis-citation exposed. Routed as
`GAP-54-06`.

Recorded so the row is not read as more than it is: `PC-5`'s opening characterizes the
packet as treating the count dependence as **intrinsic** to the mechanism. That is the
report's reading of the packet's framing. The packet's own sentence at `MA:147` attributes
the exclusive-prefix form to the implementation and cites it there, and `F-06` at `MA:272`
does the same; neither asserts the form is the published method's. The distinction is
recorded rather than resolved, because it bears on `§5.7(d)` and the fourth remedy family.

### `PREM-09` — one probe, two incompatible descriptions, and no authoritative reading

Both descriptions are in the packet, both are quoted accurately by the challenge, and they
are incompatible. `V` verified each at its own line and stopped there deliberately: reading
the probe's source in the tree "would have been adjudicating a premise, which is wave 4's
authority."

This pass has that authority for the **premise** and does not have it for the **surface**.
The premise question — do two verified statements in the packet contradict each other —
is answered: they do. The surface question — which description is right, and whether the
datum may serve as a reference scale for anything — is an `S2` disposition and SCOPE-34
reserves it to the owner. Both were considered separately and only the first is answered
here.

Why the difference is consequential rather than cosmetic. A consistency check that
finite-differences a stored integrator trajectory measures whether the integrator's own
output satisfies the force law; it is a property of the data and the differencing stencil,
not of any network. A measurement on a trained network measures how small that network's
residual gets. Only the second could bear on what a converged residual scale is, and `F-12`
transcribes exactly that inference. `CB-F1b` adds the dimensional point independently: with
the residual defined at `AR:429` as a mean squared force-balance discrepancy over three
bodies, a **relative** acceleration error determines the residual only once multiplied by
the squared acceleration norm it is relative to, so a dimensionless figure alone
under-determines it.

The distinguishing fact against `PREM-01`: there, amendment `A-1` makes one reading
authoritative. Here the amendment record is silent — all sixteen entries at `MA:412`–`:429`
were read and none addresses the contradiction — so the packet offers no way to choose, and
choosing is not this pass's to do. Routed as `GAP-54-03`.

Both reports concluded, on different readings of what the probe measured, that the gate
cannot fix a converged-scale normalizer (`X-04`). `V` records that as robustness rather
than corroboration, and notes the premise-sharing caveat: both inherited the single
relative-error datum from the same transcription, so if that datum is wrong they are wrong
together. The consequence recorded above follows from this: no returned answer rests on the
contradicted description, and the exposure is forward, to any later use of `F-12` as a
converged-scale reference.

### `PREM-12` — the packet's own consistency check, overstated

`M7` is cited as an internal-consistency certification of the six-row probe. The
certification survives; its stated precision does not. `V` computed the six reconstructed
values a third time, independently of both reports, and four of them differ from the
printed medians at the very figure `M7` claims agreement to.

Two things are worth recording beyond the verdict. First, the open-book report **endorsed**
`M7`'s wording (`PC-8g`) while the closed-book report contradicted it, and the closed-book
report is the one the evidence supports — a question about arithmetic on the packet's own
printed numbers, which repository access does not reach. `V` records this and one other as
the round's two cases of that shape, and records them as the point of adjudicating by class
rather than by impression.

Second, the correction lands on the packet, which D-15 bars this pass from editing. The
achieved precision is therefore stated here, attributed to this pass, and the disposition
of the packet's wording is logged below as an operational-coordination item with the
options that remain available to a pass that is permitted to touch it.

## Challenges that reach no packet premise

Recorded in their own group rather than forced into a premise row, because a challenge that
corrects something outside the packet is a different finding from a challenge that
contradicts a packet premise.

| Challenge | Ledger ID and verdict | What it actually reaches | Disposition |
|---|---|---|---|
| `OB` `PC-2` and `CB` `Finding 7`, third assertion — the round prompt's file-count warning is stale relative to the packet's own table | `PC-2a` CONFIRMED; `CB-F7c` CONFIRMED. Entitlement `X-02` **CORROBORATED** | `PR:87`–`:88`, the **prompt** — which `MA:65` records as pasted rather than attached, and which is not the packet. The packet's own count at `MA:90` is correct and amendment `A-11` at `MA:424` records the correction that made it so | No packet premise is contradicted. The packet-side fact is carried in `PREM-19`, which the same challenge verifies. No `§5` answer rests on the prompt's count, and `V` records that no citation in either report resolved to a frozen copy, so nothing materialised. Logged as operational coordination below |
| `OB` `PC-8`, fourth bullet — the four stale spec anchors are confirmed stale in the requirements file | `PC-8d` **UNSUPPORTED** | `.planning/REQUIREMENTS.md`, a planning artifact, not the packet. Three of the four anchors are cited there and every one of the three is confirmed stale with the replacement the claim gives; the fourth appears nowhere in that file | No packet premise is reached. The staleness of the fourth anchor is independently true and is already recorded in `54-RULING.md`'s anchor-drift warning, so no repair item is lost by the narrowing. Logged as operational coordination below |

## Closing the loop — the packet premises no report challenged

Both reports were under a **duty** to challenge premises (Rule 17, quoted above), so
silence about a premise is evidence of a kind. It is **weak** evidence that the premise
holds, and it is **not verification of it**. Nothing in this section was checked by this
pass, by either report, or by `V`; each entry is recorded as `UNCHALLENGED` and as nothing
more.

| Packet premise | Where the packet states it | Standing |
|---|---|---|
| `F-01` / `M1` — the six-row seed/IC initialization probe and its columns | `MA:267`; `MA:108`–`:119` | `UNCHALLENGED`. One report reproduced it within spread from a clean-room model, and that corroboration is routed `NOT-VERIFIABLE-HERE` at `PC-1e`; `CB-F2a` confirms the record establishes the six cases. Neither is verification of the probe |
| `F-11` — the audit's two-factor attribution of the initialization derivative magnitude | `MA:277` | `UNCHALLENGED`. It is the corrected reading both reports rely on when challenging `F-02`, which is a different thing from its having been tested |
| `§7`'s `S1` entry — the evidence pins the failure signature and pins no value, form or normalization under which the mechanism would not saturate | `MA:297` | `UNCHALLENGED` |
| `§7`'s `S4` entry — the evidence pins the two fixed numbers and pins no count a recalibrated recipe would use | `MA:303` | `UNCHALLENGED` |
| `§7`'s `S5` entry — the evidence pins the underflow-only purpose and pins no numeric bound | `MA:305` | `UNCHALLENGED` |
| `§7`'s cross-cutting entry on interactions beyond the arithmetic — no source tests combined dispositions | `MA:307` | `UNCHALLENGED` |
| `§7`'s cross-cutting entry on behaviour after initialization — no such run exists | `MA:309` | `UNCHALLENGED`. Both reports treat it as binding rather than testing it, and one report's own gaps section repeats it |
| `§3`'s external-published-literature tier | `MA:87` | `UNCHALLENGED`. Both reports used the tier; neither disputed it |
| `§3`'s repo-derived Route-B tier, including the statement that live code is not a grounding source for spec decisions | `MA:88` | `UNCHALLENGED` |
| `§0`'s trainex-r2 qualification block and its citation convention | `MA:14`–`:33` | `UNCHALLENGED`. Both reports carried the tag where they cited that round |
| `§5`'s framing of what a complete answer specifies, for every question | `MA:219`–`:257` | `UNCHALLENGED` as a framing. `PC-6c` challenges the **surface enumeration** `§5` is built on, which is `PREM-02`, and not the question forms themselves |

## Acceptance reads performed

Recorded with an explicit verdict rather than asserted, because each is a check the gate
cannot make.

| Read | Verdict |
|---|---|
| No row is adjudicated on persuasiveness. Every adjudication cell was checked against the verdict its row cites, and the four rows whose challenges read most forcefully — `PREM-02`, `PREM-07`, `PREM-09`, `PREM-11` — were each re-checked to confirm the value follows from the recorded verdict and not from the argument's force | **PASS** |
| No `CONTRADICTED` row records every dependent answer as `USABLE`. `PREM-01`, `PREM-09` and `PREM-12` each carry `USABLE-QUALIFIED` on **every** dependent answer, with the qualification stated in the row. No contradicted row has an empty dependent-answer set, so the vacuous case does not arise | **PASS** |
| Duplicates merge on the premise. Five premises are challenged by both reports — `PREM-01`, `PREM-05`, `PREM-07`, `PREM-11`, `PREM-16` — and each is one row carrying both challenges, both verdicts and the entitlement `V` recorded | **PASS** |
| Every premise is cited into the packet by file and line and resolved by content. All twenty-nine distinct `MA` anchors this record cites were read at their line before being cited; the amendment record's bearing is stated for `PREM-01` (where `A-1` settles the authoritative reading) and for `PREM-09` (where it is silent, which is the load-bearing difference between the two rows) | **PASS** |
| Disagreements about consequence are carried, not averaged. `PREM-07` carries both narrowings and `PREM-11` carries both positions; neither row resolves its disagreement and no third statement is introduced | **PASS** |
| The packet is not edited and no round-root file is modified | **PASS** — recorded with its command under *Standing bars at close* |
| No sentence in this record names a candidate value, form, rescaling, bound or ordering for any decision surface, reproduces any menu option, or reproduces any marked default. Menus and marked defaults that bear on a row are **located** by the citation `V` recorded and are not carried. Quantities that are or could read as candidate components — including the stipulated threshold at `R-06` — are located and not printed | **PASS** |
| The five surfaces are referred to in the packet's own transcription order throughout, and that order is stated to carry no precedence wherever it appears | **PASS** |

## The candidate list, and where each candidate came from

Nineteen candidate decision points. Three sources, recorded per candidate rather than
pooled, because a candidate `V` proposed and a candidate this pass surfaced carry different
provenance and a reader must be able to tell them apart.

| # | Candidate, in one line | Source | Grounded? |
|---|---|---|---|
| C-01 | The fourth stale spec anchor is not where the round's own sweep implies it is | `V` candidate row 1 | No — ungrounded, **operational coordination** |
| C-02 | A repository-read quotation carries a package-derived evidence label | `V` candidate row 2 | No — ungrounded, **process-artifact schema** |
| C-03 | The per-step collocation re-draw does not hold in both optimizer phases | `V` candidate row 3 | No — ungrounded, **semantic** |
| C-04 | The normalization mechanism's invariance is approximate, not exact, as implemented | `V` candidate row 4 | No — ungrounded, **semantic** |
| C-05 | A headline derived figure depends on an edge the source stipulates | `V` candidate row 5 | No — ungrounded, **semantic** |
| C-06 | A codification item is larger than the package's own row implies | `V` candidate row 6 | No — ungrounded, **operational coordination** |
| C-07 | The closed-book burden's provenance-bucket vocabulary has no value for a reproduction supplied whole | `V` candidate row 7 | No — ungrounded, **process-artifact schema** |
| C-08 | The packet's six-row consistency check claims a precision its own printed values do not reach | `V` candidate row 8 | No — ungrounded, **operational coordination** |
| C-09 | The audit's effective-frequency range understates its own printed table | `V` candidate row 9 | No — ungrounded, **operational coordination** |
| C-10 | The packet's count-coupling figure is a cardinality ratio applied to an exclusive-prefix quantity | `V` candidate row 10 | No — ungrounded, **operational coordination** |
| C-11 | The packet describes the same reference probe two incompatible ways | `V` candidate row 11 | No — ungrounded, **semantic** |
| C-12 | The two reports disagree about how the residual responds to the initialization scale | `V` candidate row 12 | No — ungrounded, **semantic** |
| C-13 | The two reports disagree about whether the reported gradient-norm ratio establishes that the data term's gradient disappears | `V` candidate row 13 | No — ungrounded, **semantic** |
| C-14 | The two reports place a normalization of the residual in different mechanical locations | `V` candidate row 14 | No — ungrounded, **semantic**, and **inside the anchor's scope** |
| C-15 | The round prompt's file-count warning is stale, and both engagements noticed | `V` candidate row 15 | No — ungrounded, **operational coordination** |
| C-16 | A figure used at three significant figures is cited to a locus that carries it at two | `V` candidate row 16 | No — ungrounded, **operational coordination** |
| C-17 | Whether the authorized decision-surface set is complete | this record, `PREM-02` | No — ungrounded, **cross-phase reframing** |
| C-18 | The collocation budget's unit is fixed by no consulted source | this record, `PREM-08` | No — ungrounded, **semantic** |
| C-19 | Whether the causal weights are recomputed inside the second optimizer phase's line searches | this record, `PREM-16` | No — ungrounded, **semantic** |

**Grounding test applied, and its result.** A candidate is grounded only if a source
explicitly answers it — the packet, a prior owner decision, a planning artifact, a
framework-spec section revised in an authorized milestone, or a short uncontroversial
first-principles derivation. Every one of the nineteen was tested against that list and
**none is grounded**; the per-candidate source silence is recorded in the gap record for
the ten that are routed, and inline below for the nine that are not. No candidate was
silently dropped: every row of this table has a disposition in the next section.

Two candidates deserve their non-grounding stated rather than assumed, because a reader
might expect them to be grounded and they are not. **C-18** looks as though the
specification must fix it — it does not; the negative search that established the silence
is `CB-F4c`, `V` records that the silence also holds of the specification files themselves
at the pinned tree, and no planning artifact names a unit either. **C-17** looks as though
SCOPE-33 (`REQ:118`) must answer it — SCOPE-33 enumerates the authorized items but states
no rule for admitting a surface the evidence later identifies, and the packet's own `§7`
entry at `MA:311` says in its own words that the question "is not settled by anything in
this package".

## UNDERSTANDING-TEST

The STOP protocol's step 2, applied to each candidate that reaches a surfacing class,
**before** any gap was written. Three questions per candidate, answered explicitly. A "no"
to any of them produces an understanding question to the owner and **no** gap entry,
because a gap recorded out of ignorance misleads the owner and wastes attention.

| Candidate | Q1 — can the principles at stake be articulated? | Q2 — can the different downstream consequences of each candidate resolution be explained? | Q3 — which sources were consulted, and why did each fail to answer? | Outcome |
|---|---|---|---|---|
| C-17 → `GAP-54-02` | **Yes.** The train-free gate's conditions are conditions on the weight vector, not on the magnitude of the outer physics loss, so a weight-vector repair satisfies them by construction while leaving a gradient-magnitude imbalance the gate does not measure. Separately, the architectural section carrying the disputed capacity sits outside the authorized enumeration | **Yes.** Widening the set opens a spec-edit surface Phase 56 may then amend and obliges the gate to measure something it does not measure today; declining leaves both findings on record and unaddressed, and the gate is spent against the single remaining Stage-0 run either way | `REQ:118`; `MA:311`; `MA:211`–`:215`; `MA:151`–`:193`; `54-RULING.md`'s surface table and completeness rule; `.planning/ROADMAP.md` Phase 56 criteria; `V`'s routing of `PC-1f` and `PC-6c`. Each fixes what is authorized or records the absence; none states a rule for admitting a surface | **PASS** — gap written |
| C-11 → `GAP-54-03` | **Yes.** A finite-differenced stored trajectory measures the integrator against the force law; a trained network measures that network's residual. Only the second bears on a converged residual scale, and a relative error fixes an absolute residual only once multiplied by the squared acceleration norm | **Yes.** Correcting either description changes which inference the packet's only converged-regime datum supports; withdrawing the datum leaves the reference-scale question with no candidate in the package; folding it into the surface disposition defers it to the owner's own gate | `AUD:109`; `D5:83`; `MA:278`; `MA:139`–`:141`; the packet's whole amendment record at `MA:412`–`:429`; `REQ`; `.planning/ROADMAP.md`. The two descriptions are both present and neither cites the other; the amendment record is silent; no governance artifact names a reference scale | **PASS** — gap written |
| C-12 → `GAP-54-04` | **Yes.** Both positions name the same mechanism and differ on its magnitude under the locked stack: one derives a power law for a bare periodic first layer at fixed weights and keeps it as a conditional heuristic; the other argues the law fails because the first operation on the first hidden activation is a positively scale-invariant normalization followed by a square, and measures a much weaker response in a clean-room re-implementation | **Yes.** The capacity accounting is computed **through** this law while its requirement side is fixed by re-derived repository quantities, so the two laws give different answers to whether a surface can reach its threshold at all — the difference between a lever and an irrelevance. Settling it first, deferring the affected menus, or declaring it non-blocking each change what the consolidated sheet may present as trusted | `OB` `:69`–`:86`; `CB` `:353`–`:360`; `AR:181`; `MA:301`; `DELIVERY-NOTE.md:142`; `V`'s `R-04`, `R-05` and `CB-07`, all routed. Neither measurement was made on this project's model, no repository artifact measures the response, and the join rule states the obligation without naming a procedure | **PASS** — gap written |
| C-18 → `GAP-54-05` | **Yes.** The exponent at the last point is proportional to the prefix length, one less than the count; the two candidate units are numerically confusable because the cardinality ratio times the executed count equals the specified count exactly, so the same total is reached by two configurations with entirely different prefix lengths per weight vector | **Yes.** Stating the unit inside the disposition, settling it first as a codification item, folding it into the anchor, or accepting the under-determination each change whether the joint ratification the roadmap requires is actually joint | `AR:454`, `:461`; `CT:1815`, `:1840`; `MA:147`, `:179`–`:185`, `:303`; `REQ:95`; `54-RULING.md`'s completeness rule; `CB-F4c`'s scoped negative search. Every one fixes or discusses a number and none states a unit | **PASS** — gap written |
| C-03 + C-19 → `GAP-54-06` | **Yes.** The front index is defined per step over the sampled set and the invariant accumulates its high-water mark across steps, so a per-step re-draw and a held-fixed set give the index different semantics. Separately, differentiating a weighted mean gives a residual term and a weight term; detaching the weights suppresses the second, so a weight recomputed on trial parameters inside a line search makes the supplied gradient the gradient of a different function than the scalar being compared | **Yes.** Re-stating per phase changes what a later re-ratification of the invariant window binds to; scoping to the characterized phase records the other as unexamined and leaves a composed recipe's second phase unqualified; leaving it as written carries a conditional risk into the run that spends the single preserved evaluation's precondition | `AR:698`, `:741`; `AR:435`, `:445`; `MA:293`–`:317`; `REQ:118`; `CB-F8b`'s scoped negative search and the other report's own gaps row; `V`'s `PC-5b` and `D-2b`, both `UNSUPPORTED`. The contract freezes the multipliers and states the handoff and addresses neither mechanism | **PASS** — gap written, with the two candidates folded because they are one decision point seen twice |
| C-13 → `GAP-54-07` | **Yes.** Floating-point addition acts componentwise, so a ratio of vector norms bounds no individual component — two vectors with disjoint support have an arbitrary norm ratio and lose nothing on addition. The inference is nevertheless plausible for aligned, dense gradients | **Yes.** Commissioning the statistics establishes or refutes it; downgrading its status changes what a later amendment may cite; withdrawing it removes a load-bearing step from one report's argument about where a normalization belongs | `AUD:132`, `:134`, `:169`; `AR:690`; `MA:63`; `V`'s `PC-6a`, `PC-6b`, `PC-6c`, `CB-F6a`, `CB-F6b`, `CB-12` and `X-17`. No retained artifact records per-component statistics and the specification requires that logging only before a future control is adopted | **PASS** — gap written |
| C-04 → `GAP-54-08` | **Yes.** A layer normalization carrying a positive stabiliser satisfies the amplitude-invariance identity only to the extent that the squared pre-activation scale dominates the stabiliser; the identity is exact only in the limit where the stabiliser vanishes, and the approximation degrades exactly where the pre-activation scale collapses | **Yes.** Carrying the narrowing keeps the mechanism's scope honest wherever the consolidation cites it; re-stating the clause changes the round's own text; judging it immaterial requires a reason that survives the small-amplitude regime the capacity argument is about | The finding's own text; the constructed operation and its stabiliser field; `V`'s `PC-1d` `CONFIRMED-NARROWER` and its per-claim section. No source in the package addresses the difference | **PASS** — gap written |
| C-05 → `GAP-54-09` | **Yes.** One of two figures presented as a single comparison is bounded at both ends by quantities re-derived from the tree; the other is bounded at one end by a threshold the report stipulates, and the derived width moves decade for decade as that edge moves | **Yes.** Letting the figure travel with its stipulation recorded, routing the stipulation for disposition first, or restricting the figure to the direction the fully-grounded number supports each change how a prominent capacity figure may be cited | `V`'s `R-06` `CONFIRMED-NARROWER` and its per-claim section; the report's own confidence cell, which concedes the edge is a judgement; `CC-1`'s note that the specification's own stage thresholds are provisional. No repository fact bears on the stipulated edge | **PASS** — gap written |
| C-02 → `GAP-54-10` | **Yes.** The four-class taxonomy decides entitlement from the claim's class, the class is read from the declared label, and a mislabelled row is therefore consumed under the wrong entitlement — invisibly, once the label is trusted | **Yes.** Recording both label and provenance and consuming the provenance preserves the entitlement check; asking the round to re-label changes the source document; excluding the row from agreement claims loses a real finding; a standing convention binds future rounds | `OB:35`–`:38`; `54-INTAKE.md`'s taxonomy and `LEDGER-PREFIX-CONTRACT`; the ERW runbook; `V`'s `PC-9a`. None says what to do when a declared label and the provenance disagree | **PASS** — gap written |
| C-07 → `GAP-54-11` | **Yes.** The three provenance buckets partition citations by whether the attachments account for the line number: literally, by a checkable offset, or not at all. A reproduction that declares its range by reproducing a document whole accounts for it by an offset of zero, which the bucket definition's wording does not obviously cover | **Yes.** Each reading changes the published bucket counts a later document quotes; none changes a verdict, because every anchor is content-resolved either way | `54-INTAKE.md`'s `BURDEN-CLOSED-BOOK`; the ERW runbook's access-mode comparison; `V`'s `ANCHOR-PROVENANCE-TRIAGE` reading paragraph and its candidate row 7. The runbook does not contemplate a closed-book round whose uploads carry repository anchors at all | **PASS** — gap written |

**Result: ten of ten surfacing candidates PASS the step-2 test; none failed; no
understanding question to the owner is raised by this pass.** Recorded as a result rather
than left as an absence, because "no understanding questions" and "the test was not run"
look identical in a document that omits the section.

The three quantitative items where an in-repository fact would have been tempting but was
declined are named so the declining is visible: reading the probe's source to settle
`GAP-54-03`; verifying the mis-cited re-draw line to settle the `UNSUPPORTED` half of
`GAP-54-06`; and preferring the clean-room sweep to the analytic model in `GAP-54-04`. Each
would have decided something the owner has not delegated.

## GRANULARITY-OFFERED

`54-CONTEXT.md` D-10 chose **one anchor gap** covering both owner checkpoints rather than
one record per recalibration sub-question, and its **Open Item 2** keeps the exhaustive
alternative available on request: *"Gap-register granularity (D-10). One anchor gap for
checkpoints ①/② rather than one record per recalibration sub-question. … Say the word and
it expands to per-surface records."*

The ten records this pass files are recorded as **separate gaps** because they are **not
sub-questions of the anchor record's decision point**. The anchor's decision point is which
of the five surfaces change and to what; none of the ten asks that. They ask whether the
surface set is complete, which of two packet descriptions of a probe is right, whether a
scaling dispute must be settled before menus are read, what unit a count carries, whether a
characterization holds in both optimizer phases, what a gradient-norm ratio proves, whether
an invariance is exact, whether a stipulated edge may travel as a fact, and two questions
about the receiving process's own schemas. That is D-17's boundary, which extends D-10
rather than overriding it.

**The granularity choice is offered back rather than assumed.** The owner may instead fold
any or all of these into `GAP-54-01` as sub-entries, and may equally split any of them
further. The statement is repeated in each new record so it travels with the record and not
only with this document.

One candidate went the other way and is recorded here for symmetry: **C-14** asks where a
normalization of the residual belongs, which is a disposition of one of the five surfaces
and therefore **inside** the anchor's scope. It is routed to `GAP-54-01` by appending to
that record's resolution note rather than given an identifier of its own, and `V`'s own
"what the owner decides" for that row says the same — the disposition of the surface
itself, at checkpoint ②, on the consolidated sheet.

## Candidate dispositions in full

Every candidate has exactly one disposition and none is silently dropped.

| Candidate | Class | Disposition | Reason |
|---|---|---|---|
| C-01 | operational coordination | **Disposed** — option (B): the claim stands as narrowed to the anchors actually cited in the requirements file, which is what `PC-8d`'s `UNSUPPORTED` verdict already records | Minimal and factual. It opens no work and decides nothing about any spec: the staleness of the fourth anchor is independently true and is already recorded in `54-RULING.md`'s anchor-drift warning, so the narrowing loses no repair item |
| C-02 | process-artifact schema | **Routed** — `GAP-54-10` | A surfacing class; never agent-disposable |
| C-03 | semantic | **Routed** — `GAP-54-06`, folded with C-19 | A surfacing class; the two are one decision point seen through two mechanisms |
| C-04 | semantic | **Routed** — `GAP-54-08` | A surfacing class |
| C-05 | semantic | **Routed** — `GAP-54-09` | A surfacing class |
| C-06 | operational coordination | **Disposed** — option (C): the sharpening is recorded and the scoping of the eventual fix is deferred | Scoping the fix would widen what a later pass must do, which is more than minimal. Phase 53's unswept inventory already owns the adjacent routing, and `PC-4a`'s sharpening is on the record here for whoever takes it up |
| C-07 | process-artifact schema | **Routed** — `GAP-54-11` | A surfacing class |
| C-08 | operational coordination | **Disposed** — option (B): the mismatch is recorded as known and the packet's entry is left as written | The other two options are unavailable to this pass rather than rejected by it: (A) edits the packet, which D-15 bars, and (C) re-runs the probe, which is INST-04's charter. The achieved precision is recorded at `PREM-12` |
| C-09 | operational coordination | **Disposed** — option (B): the range is left and this record notes that it is a round-number summary | (A) edits a v2.2 review artifact and the packet's transcription of it; (C) edits the packet. Both are barred here. The correct range is recorded at `PREM-03` with its citation |
| C-10 | operational coordination | **Disposed** — option (B): the packet's own hedge stands and the exact endpoint multiplier is recorded at `PREM-07` | (A) and (C) edit the packet, barred by D-15. The residual concern `V` named — that an order-of-magnitude figure and an exact multiplier are not interchangeable for a joint ratification — is carried into `GAP-54-05`, which is where the count question sits |
| C-11 | semantic | **Routed** — `GAP-54-03` | A surfacing class |
| C-12 | semantic | **Routed** — `GAP-54-04` | A surfacing class |
| C-13 | semantic | **Routed** — `GAP-54-07` | A surfacing class |
| C-14 | semantic, inside the anchor's scope | **Routed to `GAP-54-01`** by appending to its resolution note; no new identifier | Where a normalization of the residual belongs is a disposition of one of the five surfaces, which the anchor covers and which checkpoint ② closes. A second identifier would record the same decision twice and would let it be closed in one register while open in the other |
| C-15 | operational coordination | **Disposed** — option (B): the discrepancy is recorded and the prompt is left as the historical record of what this round's agents were told | Minimal and factual; the round root is frozen by this plan's own bars, and `V` records that no citation in either report resolved to a frozen copy |
| C-16 | operational coordination | **Disposed** — option (A): nothing is required; the locus `V` recorded is pointed at here so a later reader does not rediscover it | The figure is a faithful rounding of a locus that exists; only the citation was missing, and it now has a recorded home |
| C-17 | cross-phase reframing | **Routed** — `GAP-54-02` | A surfacing class, and the one the threat register names first: an agent that answers whether the enumeration is complete has widened the owner's authorized scope by writing a sentence |
| C-18 | semantic | **Routed** — `GAP-54-05` | A surfacing class |
| C-19 | semantic | **Routed** — `GAP-54-06`, folded with C-03 | A surfacing class |

**Scope-boundary check.** Each routed candidate was tested against the STOP protocol's
scope-boundary rule — a gap belongs to the phase whose content it is about. All ten are
about Phase 54's own content: the round this phase commissioned, the packet this phase
assembled, or the receiving process this phase is executing. **None belongs to another
phase's register.** Two touch downstream phases in their *consequences* rather than in
their content — `GAP-54-02` bears on what Phase 56 may amend and what the gate Phase 56
wires must measure, and `GAP-54-06` bears on the invariant-window re-ratification chartered
for Phase 57 — and both are recorded in this phase's register with the downstream reach
stated inside the record, because the decision is about this round's own findings and not
about those phases' content. The routing decision and its reason are recorded here rather
than left to be inferred.

## The re-frame determination

The runbook's step 6 asks one question: does a verified claim contradict a package premise
such that the round must be re-framed before its answers are used? It is answered at two
levels, both required, because a false premise can invalidate the answers on one surface
while leaving another untouched.

### The closed determination set

| Value | Meaning |
|---|---|
| `NO-REFRAME` | No premise is adjudicated contradicted and no qualification reaches an answer the round returned. The answers may be consolidated as returned. |
| `REFRAME-PARTIAL` | One or more premises are contradicted or qualified and the answers built on them are identified. The round may be consolidated, and the affected answers travel with their premise finding attached, marked unusable or usable-qualified per the adjudication. |
| `REFRAME-REQUIRED` | A contradicted premise reaches the round's framing itself rather than an individual answer, so consolidating the answers as returned would present a candidate sheet answering a question the evidence shows was the wrong question. **Halts the pass** and routes to the owner. |
| `UNDETERMINED` | The evidence needed to decide between the above is itself unsettled. **Halts the pass** and routes to the owner, and is a legitimate outcome rather than a failure to conclude. |

### Round level

`REFRAME-DETERMINATION=REFRAME-PARTIAL`

**The rows it rests on, and the reasoning.**

Three premises are adjudicated `CONTRADICTED` — `PREM-01`, `PREM-09`, `PREM-12` — and
eleven `QUALIFIED`. The question the determination turns on is whether any of the three
reaches the round's **framing** rather than an individual answer. Each was tested
separately.

- `PREM-01` reaches `§5.3`'s evidence base, not its framing. The packet had already
  corrected itself at `MA:129` and recorded the correction at `MA:414`; what failed is that
  the correction did not reach the register row. The surface remains enumerated on a ground
  the contradiction does not touch — `MA:129` records that only that quantity carries an
  owner-ratified contract marker — and **both reports flagged the contradiction up front
  and answered against the corrected reading**. An answer is affected in its qualification,
  not in its validity.
- `PREM-09` reaches `§5.2`'s only offered reference datum, not `§5.2`'s question. The
  question — whether a normalization is supported and against what reference scale — is
  well-posed with or without the datum, and both reports answered it while concluding that
  the datum cannot serve (`X-04`). The exposure is forward, to any later use of the datum,
  and it is routed as `GAP-54-03`.
- `PREM-12` reaches a certification's stated precision and nothing downstream depends on
  the figure it overstates.

**The one finding that would have reached the framing does not carry a contradicting
verdict.** `PC-6c` asserts a pathology surviving every enumerated surface, and `PC-1f`
asserts that the capacity attributed to one surface lives outside the authorized set. If
either were `CONFIRMED` the enumeration would be established incomplete and the round would
have been answering a narrower question than the evidence supports — which is the
`REFRAME-REQUIRED` case exactly. Both are routed `NOT-VERIFIABLE-HERE`, so `PREM-02` is
`UNSETTLED` and not `CONTRADICTED`. Two further facts bear on it and are recorded rather
than assumed: the packet's **own** `§4.3` already transcribes a fourth remedy family and
records at `MA:215` that the five surfaces were assembled from the requirement text rather
than from the routing authority, and `MA:213` records that all four families sit inside the
authorized set. So the packet's framing does not assert that the five surfaces exhaust the
remedy space, and a finding that they do not is not a contradiction of it.

**Why this is not `UNDETERMINED`.** `UNDETERMINED` is reserved for the case where the
evidence needed to choose among the four values is itself unsettled. Here the choice turns
on whether a contradicted premise reaches the framing, and that is answerable from
`CONFIRMED` verdicts and from the packet's own text, both read above. What is unsettled is
`PREM-02`'s substance and the round's one scaling dispute — and both are routed to the
owner as gaps rather than left to move a determination they do not decide. Recording
`UNDETERMINED` here would have converted "one premise is unsettled" into "the determination
is unsettled", which are different statements.

**Why this is not `NO-REFRAME`.** Three premises are contradicted and eleven qualified, and
several of those qualifications reach answers the round returned. `NO-REFRAME` would assert
that nothing travels with the answers into the consolidation, which this record contradicts
row by row.

### Surface level

One value for each of the five enumerated decision surfaces, taken separately. The surfaces
appear in the packet's own transcription order (`MA:151`–`:193`), and **that order carries
no precedence, no priority and no sequencing implication** — the same statement
`54-RULING.md` makes of the same order. No value is attached to any surface and none is
marked.

`SURFACE-DETERMINATION[S1]=REFRAME-PARTIAL`
`SURFACE-DETERMINATION[S2]=REFRAME-PARTIAL`
`SURFACE-DETERMINATION[S3]=REFRAME-PARTIAL`
`SURFACE-DETERMINATION[S4]=REFRAME-PARTIAL`
`SURFACE-DETERMINATION[S5]=REFRAME-PARTIAL`

| Surface, in the packet's transcription order | Determination | The premise rows it rests on | What travels with this surface's answers |
|---|---|---|---|
| `S1` (`MA:155`) | `REFRAME-PARTIAL` | `PREM-05` `QUALIFIED`; `PREM-07` `QUALIFIED`; `PREM-08` `QUALIFIED`; `PREM-09` `CONTRADICTED`; `PREM-10` `QUALIFIED`; `PREM-13` `QUALIFIED`; `PREM-17` `INTACT` | The clamp-binding correction to the threshold label; the endpoint-versus-cardinality distinction and the unit question; the reference datum's contradicted provenance; the budget-independence narrowing; the median-versus-initialization distinction. `GAP-54-03` and `GAP-54-05` attach |
| `S2` (`MA:163`) | `REFRAME-PARTIAL` | `PREM-02` `UNSETTLED`; `PREM-09` `CONTRADICTED`; `PREM-11` `QUALIFIED`; `PREM-13` `QUALIFIED`; `PREM-14` `QUALIFIED` | The contradicted provenance of the package's only converged-regime datum; the invariance hazard `§7`'s entry does not carry, with both of its narrowings; the open dispute over what the gradient-norm ratio proves and the unresolved difference over where a remedy sits. `GAP-54-03`, `GAP-54-07` and the anchor-routed `C-14` attach |
| `S3` (`MA:171`) | `REFRAME-PARTIAL` | `PREM-01` `CONTRADICTED`; `PREM-02` `UNSETTLED`; `PREM-03` `QUALIFIED`; `PREM-04` `QUALIFIED`; `PREM-12` `CONTRADICTED`; `PREM-13` `QUALIFIED`; `PREM-15` `INTACT` | The two-factor attribution replacing the register row's one-factor wording; the unsettled question of whether the capacity lives on an authorized surface at all; the corrected frequency range and the qualified scalar-gain account; the corrected precision of the consistency certification. `GAP-54-02`, `GAP-54-04` and `GAP-54-08` attach. **This is the surface the round's one scaling-law dispute sits on** |
| `S4` (`MA:179`) | `REFRAME-PARTIAL` | `PREM-07` `QUALIFIED`; `PREM-08` `QUALIFIED`; `PREM-18` `INTACT`; `PREM-19` `INTACT` | The endpoint-prefix multiplier alongside the cardinality ratio, and the unstated unit that makes the two readings numerically confusable. `GAP-54-05` attaches, and the roadmap's own completeness rule already binds this surface |
| `S5` (`MA:187`) | `REFRAME-PARTIAL` | `PREM-05` `QUALIFIED`; `PREM-16` `QUALIFIED`; `PREM-17` `INTACT`; `PREM-19` `INTACT` | The correction that the bound is a clamp binding rather than the point at which the exponential reaches zero, with the two boundaries below it distinguished; the conditional second-optimizer-phase risk neither the contract nor `§7` addresses. `GAP-54-06` attaches |

**On the fourth remedy family.** `MA:211` transcribes a fourth remedy family from the
routing authority and `MA:213` records that all four families sit inside the authorized
set. The packet records it as a **family**, not as a sixth surface, and this record neither
promotes it to one nor withdraws it: promoting it would widen the authorized surface set,
which is exactly what `GAP-54-02` hands to the owner. Its answers are covered in the rows
above wherever `§5.7(d)` appears in a premise row's dependent-answer cell.

### The consolidation precondition

`CONSOLIDATION-AUTHORIZED=YES`

**What each determination authorizes wave 5 to do**, stated so a later plan's gate can read
it mechanically and a later reader can check the reasoning:

- Under `NO-REFRAME` or `REFRAME-PARTIAL`, wave 5 **proceeds**. Under the latter it carries
  every premise finding into the consolidation attached to the answers it reaches.
- Under `REFRAME-REQUIRED` or `UNDETERMINED`, wave 5 does **not** proceed. The pass halts,
  the owner is told what was found and what it invalidates, and the consolidation waits on
  the owner's instruction.

**Halting is a correct outcome in those two cases and not a failure of the pass.** A
consolidated candidate sheet built on a premise the evidence contradicts is worse than no
sheet, because it is persuasive: it presents a well-reasoned answer to a question the
evidence has already shown was the wrong one, and it presents it in the form an owner is
being asked to ratify. That statement is recorded here even though this pass did not reach
those values, so the record carries the standard rather than only the outcome.

**What the authorization obliges wave 5 to carry**, because `REFRAME-PARTIAL` is not a
clean bill:

1. Every premise finding in the table above travels with the answers it reaches, and each
   affected answer carries its consequence value.
2. The three contradicted premises travel with the corrections stated in this record,
   attributed to this pass, and with the fact that none of them was corrected in the packet
   because D-15 bars it.
3. The routed gaps travel by identifier with the answers and menus they bear on, so the
   owner meets them at checkpoint ② beside the surfaces they qualify.
4. The delivery note's own join rule at `DELIVERY-NOTE.md:142` binds independently of this
   determination: the round's one scaling-law disagreement is a physics dispute, and the
   menus `V` located downstream of it are not to be presented as trusted while
   `GAP-54-04` is `OPEN`. That is a transcription of the join rule, not an addition to it,
   and it constrains how wave 5 presents rather than whether wave 5 runs.
5. The entitlement column of `V`'s cross-report adjudication governs what may be claimed as
   two-agent support, unchanged by anything here.

### What this determination does not do

Stated explicitly, because each of these is something a reader might reasonably assume a
"determination" had done.

- **It disposes of no decision surface.** No surface is dispositioned, narrowed, ordered or
  marked, and no value, form, rescaling, bound or ordering is named for any of them.
- **It selects nothing.** No option is chosen, no default is marked, no menu is reproduced
  and no candidate is carried. Menus and marked defaults that bear on a premise row are
  located by the citation `V` recorded and left where they are.
- **It does not close the anchor gap.** `GAP-54-01` stays `OPEN` in both registers, because
  checkpoint ② is what closes it and checkpoint ② is unfilled.
- **It does not touch the ruling record.** `54-RULING.md` is byte-unchanged. Its
  checkpoint-② section stays unfilled and its **pre-declared completeness rule** stands
  exactly as written — a ruling that does not dispose of the collocation count remains
  incomplete, and `GAP-54-05` sharpens what disposing of it requires without altering the
  rule.
- **It does not widen scope.** Whether the authorized surface set should be widened is
  `GAP-54-02`, handed to the owner unresolved.
- **It resolves no cross-report disagreement.** The three open disputes `V` recorded stay
  open; two of them are routed here and the third is routed to the anchor.

## Standing bars at close

Commands carrying Bar F or Bar G cost vocabulary are recorded in fenced blocks, matching
the convention `54-07`, `54-08` and `54-INTAKE.md` used, so that recording a command does
not trip the check the command defines. Success prints a marker wherever one exists, because
an empty result and a mistyped path produce the same silence.

| Check | Command | Output | Verdict |
|---|---|---|---|
| Bar D — canonical, as defined in `54-01-PLAN.md` | `git diff --stat -- <the six pathspecs: the three framework specs, `pinn/`, `simulation_data/`, `tests/`>` | empty | PASS |
| Bar D — the same six pathspecs anchored to `HEAD` | `git diff HEAD --stat -- <the same six pathspecs>` | empty | PASS — recorded in addition to, never instead of, the index-anchored form, because a staged-but-uncommitted edit is invisible to the index-anchored form and this plan's prohibitions require the `HEAD` anchor |
| Bar E — canonical two-path form, `HEAD`-anchored | `git diff HEAD --stat -- .planning/REQUIREMENTS.md .planning/ROADMAP.md` | empty | PASS — this plan edits neither file, so the canonical form applies unchanged and no narrowing is taken |
| Bar F — cost vocabulary over the ruling record | fenced block below | `0` | PASS — equal to the number `54-07`, `54-08`, `54-09` and `54-10` each recorded |
| Bar G1 — no candidate value across any decision surface | fenced block below; selector `S` byte-unchanged from `54-06-PLAN.md`, file list extended to this pass's six plan files | region cardinality `G1-REGION=0`; remainder after token strip empty | `BAR-G-CLEAN-NO-SURFACE-NAMED` |
| Bar G2 — no ordering vocabulary in the plans' own voice | fenced block below | empty | PASS |
| Bar G3 — no cost framing in the plans' own voice | fenced block below | empty | PASS |
| Bar G preprocessing sanity — fence balance and retained stream size | `grep -c '^```'` over each of the six plan files; retained line count of the shared stream | fence counts 10, 8, 8, 8, 10, 10 — all even; retained stream `4233` lines | PASS — an odd fence count would make the preprocessing swallow the rest of a file and every sub-bar would then pass vacuously |
| Check R1-w — the widened round-root manifest, run verbatim from `54-08-PLAN.md` | fenced block in that plan's verification section | `MANIFEST-OK-W` | PASS |
| No consolidated document exists | `test ! -f <the round root>/trainex-r3-resolution-doc.md && echo CONSOLIDATION-ABSENT` | `CONSOLIDATION-ABSENT` | PASS |
| **The narrowed register assertion** — appending is authorized, rewriting is not | `git diff HEAD -- 54-GAPS.md .planning/milestones/v2.3-GAPS.md \| grep -E '^-[^-]'` | empty | PASS — and independently: `git diff HEAD --numstat` over the two files returns `285 0` and `20 0`, so both edits are **pure additions with zero deletions** |
| Anchor gap still `OPEN` after the edits | `grep -cE '^- \*\*Status:\*\* OPEN' 54-GAPS.md`; `grep -c 'OPEN' .planning/milestones/v2.3-GAPS.md` | `11` and `11` | PASS — `GAP-54-01` plus the ten records this pass filed, in both registers |
| Ruling record, verification report and round root byte-unchanged | `git diff HEAD --stat -- 54-RULING.md docs/work/reviews/milestone_v2.3/ <the round root>` | empty | PASS — anchored to `HEAD` rather than to the index, so a staged edit cannot leave the assertion empty and passing |

**Bar G verdict literal, recorded exactly as the gate prints it:**
`BAR-G-CLEAN-NO-SURFACE-NAMED`, with `G1-REGION=0`. This is not a paraphrase and not a
substitute for `BAR-G-CLEAN`. The two literals mean different things: `BAR-G-CLEAN` states
that the plan files named a decision surface and named no value for it;
`BAR-G-CLEAN-NO-SURFACE-NAMED` states that this pass's six plan files named **no decision
surface at all**, so the bar's region over them is empty. The value is unchanged from the
one `54-08`, `54-09` and `54-10` each recorded, which is expected because the bar's file
list and selector are unchanged and no plan file was edited by this plan.

Bar F command (fenced):

```
grep -ciE 'faster|slower|cheaper|quicker|days|weeks|hours|effort|simpler|harder|easier|more work|less work' \
  .planning/phases/54-recalibration-decision-grounding/54-RULING.md
```

Bar G shared stream and sub-bars (fenced; defined in `54-06-PLAN.md`, selector unchanged,
file list extended to this pass):

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

## The manual structural read

Bar G runs over plan files. This record and the ten new gap entries are not plan files, so
the neutrality property is asserted here by a read, with an explicit verdict and with the
mechanical aid that supported it recorded so a later reader can re-run it.

**Aid.** Bar G's selector `S` was run over this record and over the new gap sections, and
every line matching it was re-examined after the selector tokens were stripped, for a
retained digit. Twenty lines in this record and twelve in the gap sections retained one.
Each was read individually.

**Verdict — this record: PASS.** No sentence names a candidate value, form, rescaling,
bound, ordering or marked choice for any decision surface. Every retained digit is one of
four things, and the read records which: a `file:line` citation; a ledger, cross-report,
premise, candidate, gap, requirement, scope or surface **identifier**; a word-form quantity
carrying no numeral; or a **currently locked fact** quoted from a grounding source. Two
instances of the fourth kind are named individually rather than left inside the count, so
the judgement can be checked:

- `PREM-01`'s row quotes the packet's `F-02` claim clause, which contains the locked
  initialization scale as a numeral. It is quoted because the adjudication **is about that
  sentence's wording**, and abridging the quotation would make the row unreadable. The
  numeral is the value the specification currently fixes at `AR:181` and that
  `54-RULING.md` Block 2 already quotes in its contract marker; it is not a candidate and
  nothing in this record proposes changing it.
- `GAP-54-05`'s grounding field states the two currently fixed collocation counts and their
  exact ratio. `GAP-54-01`'s own grounding field already states the same three numbers, and
  the packet states them at `MA:147` and `F-07`. They are the fixed numbers the coupling is
  computed **from**, not a count anything proposes.

**Verdict — each new gap entry: PASS, entry by entry.** Every `What the user needs to
decide` field was read against the standard the existing anchor record sets: the only
options it names are the branches of the checkpoint it serves, and no candidate value is
offered for any surface. All numerals appearing in those ten fields were extracted
mechanically and are exclusively identifier fragments — `GAP-54-01` and `GAP-54-04`,
`54-CONTEXT.md`, `Open Item 2`, `D-17`, `SCOPE-33`, `SCOPE-38` and `Phase 55`. **No option
in any of the ten names a value, a form, a bound, an ordering or a marked choice for any
decision surface**, and the two options that come closest — commissioning a
characterization, and routing a stipulation for disposition — name a governance act and an
existing chartered instrument, not a quantity.

| Entry | Read verdict |
|---|---|
| `GAP-54-02` | PASS — options are widen / decline / defer / commission-the-evidence. No surface is named, proposed or scoped, and the record states in its own text that the enumeration is the owner's to widen |
| `GAP-54-03` | PASS — options correct one description, correct the other, withdraw the datum, or fold into the checkpoint. No reference scale is named |
| `GAP-54-04` | PASS — options settle, defer, declare non-blocking, or carry to the checkpoint. Neither position is endorsed, ranked or reproduced, and no scaling law is asserted |
| `GAP-54-05` | PASS — options bear on **where and whether the unit is settled**, never on which unit or which count |
| `GAP-54-06` | PASS — options bear on whether a characterization is stated per phase; no recipe element is proposed |
| `GAP-54-07` | PASS — options bear on the inference's evidential status; no remedy is proposed |
| `GAP-54-08` | PASS — options bear on how a qualified mechanism travels; no scaling law is asserted |
| `GAP-54-09` | PASS — the stipulated quantity is **located and deliberately not printed**, and the options bear on how the figure may be cited |
| `GAP-54-10` | PASS — options bear on a receiving convention; no claim is re-labelled by this pass |
| `GAP-54-11` | PASS — options bear on a bucket vocabulary; the alternative counts are cited to the verification report rather than restated, because this pass did not derive them |

**Verdict — order neutrality: PASS.** The five surfaces are referred to in the packet's own
transcription order throughout, and every place that order appears states that it carries
no precedence, no priority and no sequencing implication. The two reports are presented
open-book first throughout, which is `54-INTAKE.md`'s presentation convention and carries no
evidential weight; that is stated here so it is not read as carrying any.

**Verdict — menu containment: PASS.** Menus, marked defaults and ranked rows exist in both
returned reports and are relevant to several rows of this record. Every one of them is
**located** by the citation the verification report recorded and **none is reproduced,
counted into a preference, ranked or marked** anywhere in this record or in any gap entry.

## Halt state at plan close

Phase 54 does **not** close in this plan. `GAP-54-01` stays `OPEN` in both registers, and so
do the ten records this pass filed. The ruling record is byte-unchanged: its checkpoint-②
section stays unfilled and its pre-declared completeness rule stands exactly as written. No
consolidated document exists. Phase 56 stays closed. No framework-spec file, no file under
`pinn/`, no locked planning source, no returned report, no uploaded attachment and no
consolidated document was created or edited.

The round-level determination is `REFRAME-PARTIAL` and the consolidation authorization
literal is `CONSOLIDATION-AUTHORIZED=YES`, so this plan's conditional owner gate does **not**
fire and wave 5 is authorized to proceed — carrying every premise finding attached to the
answers it reaches, and carrying the routed gaps by identifier to the menus and answers they
bear on. Checkpoint ② remains PENDING and is nobody's but the owner's.



