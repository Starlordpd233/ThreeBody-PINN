---
title: Trainex R3 Research Context Master — Causal-Weight / SIREN-Scale Recalibration Decision Packet
package_for: trainex-r3 (single sub-package)
role: the owner's single entry point at checkpoint ① and, unchanged, the external research agent's single entry point if the round is commissioned
status: active
created: 2026-08-20
source_baseline: 6a4f9b9902ab62e1d1f57bba0e521f38120c416d
self_contained: true
access_mode: open-book
---

# Trainex R3 Research Context Master — Causal-Weight / SIREN-Scale Recalibration Decision Packet

## 0. Premise qualification — the standing of trainex-r2 in this round

The trainex-r2 round's output contract is quoted here first, verbatim, because it is the standing block every other mention of that round in this packet routes back to. The quotation is an attributed quotation of an externally authored document; it sits above the neutrality-ban markers below because it is that document's voice, not this packet's.

```
3. **Do not recommend a remedy.** Remedy adjudication is owner-governed
   downstream. Your answers inform that decision; they do not make it.
```

`[VERIFIED verbatim: pinn_instruction/markdown_conversion/framework-specs/trainex-r2/research_package/RESEARCH-CONTEXT-MASTER.md:319-320]`

<!-- NEUTRALITY-BAN-BEGIN -->

The consequence of that contract, stated as the absence list it produced: the trainex-r2 round carries no decision sheet, no options menu, no marked defaults, and no one-way/two-way door classification.

The vintage of that round: packaged 2026-07-24 and delivered 2026-07-25, predating the v2.2 conformance repairs, so its observations describe the pre-repair tree.

The standing of its Q3: Q3 framed the diagnosis and independently derived the `first_omega_0 = 30` second-derivative mechanism **as a hypothesis** — since confirmed by the 2026-08-17 residual-frame conformance audit — and it does not contain the answer.

The citation convention this section establishes: every mention of the trainex-r2 round anywhere outside §0 carries the ASCII tag `[r2-QUAL]` appended on the same line, routing the reader back to this section. A mention without the tag is a defect. §0 itself is the qualification block and is exempt.

## 1. Orientation

_Written by plan 54-02._

## 2. Manifest — what this round contains, and what it deliberately does not

_Written by plan 54-04._

## 3. Source tiering — how to treat each kind of content

_Written by plan 54-04._

## 4. The confirmed mechanism and the coupled decision surfaces

_Written by plan 54-02._

## 5. The framed questions

_Written by plan 54-04._

## 6. Claims register

_Written by plan 54-02._

## 7. What the assembled evidence cannot answer

_Written by plan 54-04._

## 8. Provenance

_Written by plan 54-04._

<!-- NEUTRALITY-BAN-END -->

## 9. Output contract

_Written by plan 54-04._

## 10. Neutrality self-audit

This section defines the neutrality checks and records their results. It sits outside the neutrality-ban region because it defines the check; a check definition that names its own tokens is not the packet's voice.

| Check | Scope | Method | Result |
|---|---|---|---|
| Bar A — D-04 Layer-1 scoped lexical ban | the `NEUTRALITY-BAN` region (§0's own voice through §8) | region-scoped case-insensitive grep for: `recommend`, `suggest`, `prefer`, `best`, `most likely`, `primary candidate`, `default to`, `should use`, `ranked`, `leading option`; expected empty | PENDING — run at phase close (plan 54-05) |
| Bar A2 — D-04 Layer-2 Rule-7 carve-out presence | §9 Output contract | case-insensitive count of `suggested default` / `one-way` / `two-way` / `decision sheet` in §9; expected at least 4 once §9 is written | PENDING — run at phase close (plan 54-05) |
| Bar B — D-06 tag discipline | all lines outside §0 | case-sensitive literal `trainex-r2` line match minus lines carrying `[r2-QUAL]`; expected empty | PENDING — run at phase close (plan 54-05) |
| Bar C — D-02 branch-neutrality file absence | the trainex-r3 round root | absence of `research_package/RESEARCH-AGENT-PROMPT.md`, `specs/`, and `research_results/`; expected to print `NEUTRAL` | PENDING — run at phase close (plan 54-05) |
| Bar D — read-only boundary | framework specs, `pinn/`, `simulation_data/`, `tests/` | `git diff --stat` over the cited paths; expected empty | PENDING — run at phase close (plan 54-05) |
| Tree completeness (45-AUDIT Check 1) | the trainex-r3 round root | `find … -type f` prints exactly the two authored paths | PENDING — run at phase close (plan 54-05) |

The two-layer neutrality criterion these checks enforce:

- **Layer 1** is the scoped lexical ban binding the packet's own voice in §0 through §8 — the region delimited by the two region markers defined in the section map.
- **Layer 2** is the explicit ERW Rule-7 carve-out for §9: §9 must carry the vocabulary of marked defaults, door classification, and decision sheets, because roadmap Success Criterion 4 requires this packet to specify the trainex-r3 output contract. A §9 that is lexically clean under Layer 1's vocabulary means the Rule-7 contract was gutted rather than satisfied — which is what Bar A2 exists to catch.

**Excluded 45-AUDIT checks, with reasons.** Check 3 (self-containment / zero repo-path markers) is Route-A-only and does not apply to a Route-B master, whose Rules 1–2 inversion makes repository paths expected. Check 4 (snapshot fidelity) and Check 6 (pin consistency across snapshot files) presuppose the `specs/` bundle D-02 deliberately withholds. These checks are deferred to the ERW-02 audit if the round is commissioned, not waived.
