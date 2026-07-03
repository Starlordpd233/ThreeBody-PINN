# Phase 35: Loss & Energy-Weight Contracts - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-27
**Phase:** 35-loss-energy-weight-contracts
**Mode:** `--all --auto` (all gray areas auto-selected; recommended option taken per area; **stopped before planning** per user instruction)
**Areas discussed:** Verdict-status transcription convention, Canonical-home split & anti-duplication, Per-contract transcription targets, Packet-before-edit & ledger lifecycle, Source-silent STOP obligation, Plan decomposition

> **Why auto was safe here:** `35-SPEC.md` (ambiguity 0.11) locks WHAT; the four
> loss verdicts are already settled by the resolution doc. Every gray area below
> is HOW-level (transcription/process) and resolves to "follow the Phase 32/33/34
> precedent + SPEC boundaries." No gray area required inventing semantic spec
> content. A STOP-protocol scan found **no new source-silent gap** at discuss time.

---

## Verdict-status transcription convention

| Option | Description | Selected |
|--------|-------------|----------|
| Reuse Phase 33/34 blockquote callout (LOOP→LOSS) | `> **Phase 35 contract: <name> (LOSS-NN; <verdict>; AC-LOSS-NN; grounded by <source>).**` + status tag | ✓ |
| Invent a new Phase 35 callout/table format | Fresh tagging scheme for the loss contracts | |

**Choice:** Reuse the existing convention verbatim (D-35-02) — file-internal consistency with existing CURR/LOOP callouts.
**Notes:** Recommended default. Pseudocode (if any) labeled "normative spec contract — not executable; FUT-01/FUT-04 implements" (D-35-03).

---

## Canonical-home split & anti-duplication (SI-PINN-003 guardrail)

| Option | Description | Selected |
|--------|-------------|----------|
| Component math in `pinn_architecture`, assembly in `ctl_instruction`, bidirectional stable-anchor cross-refs, zero duplicated text | Phase 34 D-34-04/05/06 discipline | ✓ |
| Duplicate the loss math into both specs | Two synchronized copies | |
| Move all loss math into one spec | Consolidate into a single file | |

**Choice:** Single canonical home per value/formula + pointer; never line numbers; status-tag parity; verifier proves no duplication (D-35-04/05).
**Notes:** Recommended default. Avoids creating a second SI-PINN-003; matches SPEC boundaries.

---

## Per-contract transcription targets

| Option | Description | Selected |
|--------|-------------|----------|
| Transcribe the adjudicated verdict + status from the resolution doc | NS-18 `modified`, M15 `rejected`-as-replacement, NS-13 `defer`, D-04 Option A `RESOLVED-WITH-INSTRUCTION` | ✓ |
| Copy the roadmap/issue-doc "preview" wording | Cap table, `0.01–0.1` per-stage table, Option-C preserved | |

**Choice:** Verdict + status only (D-35-06/07/08/08b). Make the `τ`/`u` chain-factor `2`/`4` distinction explicit; add M15 logging requirement; keep `delta_E = 1.0`; lock Option A causal weighting; keep dense-residual ALM rejected and scalar ALM deferred P2.
**Notes:** Recommended default. The stale REQUIREMENTS/ROADMAP phrasing is superseded by `35-SPEC.md`; the cap table / Huber-δ table / Option-C / numeric clip bound appear only as rejected/deferred.

---

## Packet-before-edit & ledger lifecycle

| Option | Description | Selected |
|--------|-------------|----------|
| One packet per finding (M15, NS-12, NS-13, NS-18) before edits; D-04 consumes existing packet; reuse Phase 32 schema | Phase 34 D-34-10/11/12 sequencing | ✓ |
| Edit specs first, document evidence after | Skip packet-before-edit | |

**Choice:** Packet-before-edit using the Phase 32 `evidence/_TEMPLATE.md` schema and the existing EVID/AC IDs; advance ledger rows `IN_PROGRESS → FIX_APPLIED → VERIFIED`; confirm GAP-32-01 resolved in both registers (D-35-09/10/11).
**Notes:** Recommended default. Sequencing is what prevents transcribing a stale "preview" as locked.

---

## Source-silent STOP obligation (live governance guardrail)

| Option | Description | Selected |
|--------|-------------|----------|
| Keep STOP armed during execution; record a `35-GAPS.md` gap on any new source-silent decision | Never invent deferred numerics | ✓ |
| Auto-pick a reasonable default for any source-silent value | Fill white space to keep moving | |

**Choice:** STOP stays armed (D-35-09/12). Hard prohibitions: no `λ_E` cap table, no Huber-δ table, no Option-C mechanics, no numeric causal-exponent clip bound, no default dense-residual ALM.
**Notes:** Recommended default — this is non-negotiable project governance and **overrides the `--auto` "pick a default" behavior**.

---

## Claude's Discretion

- **Plan decomposition** — number of plan files, task grouping, exact packet
  filename slugs, ledger Markdown layout, and deterministic check commands are
  left to the planner/executor, provided packet-before-edit precedes each spec
  edit and every `LOSS-01..04` appears in a plan `requirements` field. Suggested
  (non-binding) wave shape and packet slugs recorded in CONTEXT.md D-35
  Discretion.

## Deferred Ideas

- Energy-δ quantile calibration (`0.01–0.1` per stage) — FUT/calibration.
- Automatic dominance reweighting (`λ_E·L_energy > 10·L_data`) — deferred pending evidence.
- Numeric causal-exponent clip bound — FUT (resolution GAP-01).
- Optional scalar-conservation ALM — deferred P2 only.
- Option C time-windowed causal-ALM hybrid — not commissioned (owner ratified A).
- Numeric acceptance-check execution via disposable probes — Phase 36 (VER-15).
- Training-loop / DataLoader / ALM implementation — FUT-01/FUT-04 (trainex).
