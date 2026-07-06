# Integrity-R2 — Output Contract (LOCKED)

**Status:** Output contract **locked 2026-07-07.** This document defines *what the external
agent must produce.* It is **not** the prompt and **not** the research package — those are
written by later agents **against** this contract. Do not re-open the decisions here without
owner instruction; adapt the prompt to fit them. (This contract's *silence* on an item listed
in §8 is deliberate, not a STOP-protocol gap.)

**Provenance:** Settled by a `/grilling` interview with the project owner (2026-07-06 →
2026-07-07), continued from an earlier GLM session that was cut off mid-interview. Skill flow:
**grilling (this contract) → `adapting-storm-research-prompts` (the prompt) → ERW runbook
(assemble + deliver the package).** Template/precedent: **`integrity-r1`** — read-only, do not
edit it.

**Home:** the `trainex` worktree (`.worktrees/trainex`), at
`pinn_instruction/markdown_conversion/framework-specs/integrity-r2/`.

---

## 1. What integrity-r2 is

One highly capable **external** agent performs a **disruption-first, adversarial
math / physics / engineering audit** of the **locked CTL-PINN framework foundation**, run
**once, before v2.0 Phase 37** — the project's first *build* milestone (the CTL-PINN Training
Viability Slice).

It is **not** a literature-gathering task. The agent reasons over the attached foundation
documents and tells the owner where the foundation is **sound** and where it **must be fixed
before** any build code is written. Purpose: firm, evidence-based confidence going into the
build, and catching foundation problems while they are still cheap to fix.

The audited foundation:
- the locked framework **specs** — `ctl_instruction.md`, `pinn_architecture.md` (and
  `sampling_method.md` as frozen data-generation context);
- the **v2.0 roadmap** — Phases 37–43;
- the **ratified trainex-r1a build decisions** — D1–D7 / B-1–B-11 + the §5 first-run recipe;
- the **dataset facts** (as context).

## 2. Standing — the audit has teeth (owner-enforced)

integrity-r1 was advisory ("a findings register that decides nothing"). integrity-r2 is a
**pre-build gate**:

- **Rule:** v2.0 Phase 37 does not start until every *serious, proven* problem is either
  **fixed** or **waived by the owner with a recorded reason.**
- **Teeth are owner discipline, not agent veto.** The agent decides nothing. It produces
  findings + a recommended verdict; the **owner** disposes of each one. This preserves the
  project's standing rule that external research is a *candidate*, never an authority — the gate
  is a checklist the owner must clear, not a block the agent imposes.
- **The verdict is a snapshot; the punch-list is the living record.** A later reader treats the
  delivered verdict as "the agent's view at delivery" and checks whether the punch-list was
  subsequently cleared. A stale NO-GO on an already-fixed problem is not binding.

## 3. What it audits, and how hard (coverage)

- **The 3 specs → full coverage.** Every heading (H1/H2) of every spec gets an explicit verdict:
  `audited-clean` / `see problem IR2-NNN` / `skimmed-only + reason`. This is integrity-r1's
  coverage matrix, kept.
- **The roadmap + trainex-r1a decisions → problem-hunt, not a matrix.** The agent examines them
  deeply enough to catch anything that would hinder later work, and **shows its work**: which
  phases/decisions it examined, to what depth, and an explicit "checked this, found nothing"
  register. No per-item verdict table — but "no problems here" must be **falsifiable**, not
  merely asserted.
- **Depth stopping-rule ("sufficient extent").** For the roadmap/decisions, the agent examines
  each item only deeply enough to answer: *"does this contain a defect that would hinder later
  work — invalidate a result, block the build, force a spec-unfreeze, or derail a later
  phase?"* It does **not** copy-edit the roadmap or re-optimize phase ordering for elegance. The
  severity lens is the depth calibration.

## 4. Proof rule — only proven problems (rule A)

- A problem enters the **problem list only if the agent can prove it** — with a worked
  derivation (`derived-math`) or a current primary source (`literature-cited`), quoting the
  relevant document text. **No judgment-only findings** in the problem list.
- **Locked decisions are challengeable — with a high bar.** The specs and the ratified
  trainex-r1a decisions may be challenged, but only via **proof** (math or literature, not
  judgment), and the agent must **steelman** the locked choice — argue *for* it — before arguing
  against it. Flag every such challenge as a locked-decision challenge.
- **Fixed facts (not challengeable):** the verified dataset empirical baseline. (The only
  data-change exception is the explicitly staged missing-gold remediation.)
- The steelman-first discipline is what makes an aggressive problem-hunt **trustworthy** rather
  than noisy: a surfaced challenge is one that survived the agent's own devil's advocacy.

## 5. The side-list — honest doubts it cannot prove (EDL-style)

Genuine doubts the agent cannot settle from the documents do **not** go in the problem list (no
proof) and are **not** discarded. They go on a separate **side-list**, shaped like the project's
Empirical Decision Loop:

- Each entry = **(a)** the doubt, **(b)** why paper can't settle it, **(c)** the *quick empirical
  test* that would settle it and what a bad result looks like, **(d)** a confidence note.
- These feed the v2.0 **verify ladder / Stage-0 pilot** — extra things to watch in tests the
  build already runs.
- **The agent proposes the test; it never claims the answer.** (Same boundary as an EDL brief:
  support, not authority.)
- A doubt with **no cheap test** is simply noted as "out of scope / can't resolve now."

## 6. Severity

- Two levels only: **Serious** (would hinder later work — a wrong result, a blocked build, or a
  phase that falls apart) or **Minor** (real and proven, but harmless).
- The **Serious** ones drive the verdict. Each Serious problem also carries
  **stops-the-build?**: *must-fix-first* (→ drives NO-GO) or *handle-with-a-condition* (→ drives
  GO-WITH-CONDITIONS).
- Confidence levels are **not** used on proven problems (all high-confidence by construction) —
  confidence lives only on the side-list.

## 7. The deliverable — report shape

A single self-contained markdown report, in this reading order:

1. **Verdict (bottom line).** One of **GO** / **NO-GO** / **GO-WITH-CONDITIONS**, framed as the
   agent's **recommendation** (not binding), with a one-line reason naming the blocking problems
   (e.g., "NO-GO — blocked on IR2-001 and IR2-004").
   - **GO** = nothing serious in the way. **NO-GO** = at least one serious *must-fix-first*
     problem. **GO-WITH-CONDITIONS** = serious problems exist but all are *handle-with-a-condition*
     (a roadmap tweak, a waiver, or a test to run).
2. **Pre-build punch-list.** The exact set of things the owner must fix-or-waive before Phase 37
   — each written as a decision with options (A/B/C), trade-offs, and the agent's recommended
   pick. (integrity-r1's minimum-decision-list, reframed as the gate's clearance checklist.)
3. **Proven problems, in full.** Every proven problem, worst first. Each entry carries exactly
   these fields:
   - **ID** — stable, `IR2-NNN`.
   - **What's wrong** — one plain sentence.
   - **Where** — file + heading.
   - **The proof** — the offending text quoted, plus the derivation or the citation.
   - **How serious** — Serious / Minor.
   - **Which file it points at** — a spec / the roadmap / a locked decision / the data.
   - **Stops the build?** — (Serious only) must-fix-first / handle-with-a-condition.
   - **Suggested fix** — a direction to consider, flagged as a suggestion, not a decision.
4. **Spec check-everything table.** A verdict for every H1/H2 of the 3 specs (see §3).
5. **Numbers cross-check.** One table lining up the key constants and shared definitions across
   the specs, flagging any that disagree. (integrity-r1's constants concordance — where
   cross-document contradictions hide.)
6. **Build-plan problem-hunt.** What the agent examined in the roadmap and the ratified
   decisions, what it checked for, and what it found — including the explicit "checked, found
   nothing" register (see §3).
7. **Side-list.** The empirical doubts and their proposed tests (see §5); plus any out-of-scope
   doubts.
8. **Sources.** References behind any citation-based proof, date-stamped.

## 8. Left to the assembly agents (deliberately NOT decided here)

Decide these at the prompt-writing / package-assembly step — do **not** treat this contract's
silence on them as a gap:

- **Review angles (dimensions).** integrity-r1's eight review dimensions (RD-1 viability
  red-team … RD-8 load-bearing assumptions) carry over, **adapted**: drop the
  `against-in-flight-edit` novelty tag (specs are locked; no in-flight edits) and add the
  roadmap/decisions problem-hunt as an explicit dimension. The STORM personas map onto these
  angles. Finalize the exact list in the prompt.
- **The "new / already-known" tag** on findings. Only useful *if* the package hands the agent a
  list of problems the owner already knows about (an integrity-r1-style known-issues bundle), so
  it can flag which finds are fresh. Whether to attach such a bundle is a package-assembly call.
- **Source-tier framing, the exact attachment list,** and the ERW upload mechanics (zero repo
  paths in authored uploads; verbatim spec snapshots; one shared `specs/` per round) — per the
  ERW runbook.
- **Finding-ID prefix** — `IR2-NNN` is the working default; cosmetic.

## 9. Decision ledger (the *why*, so later agents don't "improve" it into incoherence)

| Decision | Why |
|---|---|
| Teeth (pre-build gate), owner-enforced | The foundation everything is built on deserves a check that can't be quietly ignored; owner-disposes keeps external research a candidate, not an authority. |
| Spec-only coverage matrix; roadmap/decisions = problem-hunt | Full certification effort goes to the science; the plan is cheaper to change and gets a shown-work hunt instead. |
| Proof-only problem list (rule A) | The owner wants a fully-trustworthy list — every listed problem is proven, so none can be dismissed as a guess. |
| Unprovable doubts → EDL side-list, not dropped | An honest doubt that needs a run to settle is valuable; route it to the build's test ladder instead of discarding it or fabricating proof. |
| Three-way verdict, recommendation-not-binding | Fast orientation for the owner and later agents, without crying wolf (GO-WITH-CONDITIONS) and without the agent overstepping into deciding. |
| Serious/Minor only; confidence → side-list | Proven problems are all high-confidence; two-level severity keeps the signal clean. |

---

*End of locked contract. Next: `adapting-storm-research-prompts` writes the prompt against
this; then the ERW runbook assembles the `integrity-r2/` package (research package + verbatim
`specs/` snapshots + delivery note).*
