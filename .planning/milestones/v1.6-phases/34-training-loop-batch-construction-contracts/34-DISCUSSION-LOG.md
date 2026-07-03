# Phase 34: Training-Loop & Batch-Construction Contracts - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-24
**Phase:** 34-training-loop-batch-construction-contracts
**Mode:** `/gsd-discuss-phase 34 --all` (all gray areas auto-selected)
**Areas discussed:** LOOP-04/M14 grounding correction, clipping canonical home, SI-PINN-003 mechanics, transcription convention, packet-before-edit & ledger lifecycle, LOOP-07/08 handling, total-loss skeleton, source-silent routing & probe scope, LOOP-06/M16 grounding correction

---

## LOOP-04 / M14 — gradient-clipping C-value (headline grounding finding)

Grounding-verification caught the SPEC transcribing the rejected issue-doc midpoint `8.5` against the Phase 32 M14 verdict + resolution-doc §1.8.

| Option | Description | Selected |
|--------|-------------|----------|
| Follow M14, fix SPEC | Lock only the structural merge; preserve 7-10/5/3; 5.0 = Stage-2/3 instance; defer exact C/bootstrap/floor/history-reset → FUT; correct 34-SPEC LOOP-04 | ✓ |
| Follow M14, CONTEXT-only | Same contract, but leave the SPEC's 8.5 text and record the correction only in CONTEXT | |
| Keep 8.5 (needs new grounding) | Canonize 8.5 — contradicts M14 + §1.8 + AC-LOOP-04 | |

**User's choice:** Follow M14, fix SPEC.
**Notes:** 8.5 is the midpoint of 7-10 — false precision the source explicitly refuses; canonizing it would also fail AC-LOOP-04 and SPEC Prohibition #1. SPEC LOOP-04 Target + Acceptance rewritten (commit `0ffa3d8`).

---

## Clipping canonical home (LOOP-04 cross-file split)

| Option | Description | Selected |
|--------|-------------|----------|
| pinn canonical, ctl cross-refs | Mechanism canonical in pinn §4.4; C-schedule in ctl; bidirectional cross-refs; all three current locations reconciled | ✓ |
| ctl canonical, pinn refs it | Departs from SCOPE-13 | |
| Planner decides within SCOPE-13 | SCOPE-13 already decides it | |

**User's choice:** pinn-canonical mechanism + ctl C-schedule (Option 1), with a SPEC-acceptance rephrase and a duplication guardrail.
**Notes:** SCOPE-13 governs (clipping → pinn; curriculum → ctl). **Guardrail (must NOT become a second SI-PINN-003):** one canonical statement per half; the two ctl locations collapse to one canonical schedule + pointer; bidirectional STABLE-anchor cross-refs (heading + AC-LOOP-04, never line numbers); status-tag parity; a disposable SPEC-CONSISTENCY check (a–e: mechanism once in pinn §4.4; 7-10/5/3 in ctl + 8.5 absent from both; cross-refs resolve; no duplication; status parity) re-run after every batch + at Phase 36. Win condition = recoverable as one coherent rule with zero duplicated normative text. Acceptance rephrased so it no longer presupposes ctl-canonical.

---

## SI-PINN-003 reconciliation (R9)

| Option | Description | Selected |
|--------|-------------|----------|
| ctl canonical, pinn points to it | Remove the author comment (351), replace Listing-2 with a pointer extending PIPE-04 (352), mark SI-PINN-003 (1005) RESOLVED | ✓ |
| Align text in both files | Two synchronized copies = the hazard SI-PINN-003 names | |
| You decide | SCOPE-13 + B07-04 + R9 already decide it | |

**User's choice:** ctl canonical, pinn points to it.
**Notes:** SCOPE-13 (batch construction → ctl); resolution-doc claim matrix B07-04 rejects the pinn §3.1 batch construction. Matches the SPEC's already-locked R9.

---

## Transcription convention

| Option | Description | Selected |
|--------|-------------|----------|
| Reuse Phase-33 convention verbatim | Blockquote callout + inline status tag + grounded-by citation; pseudocode labeled "normative spec contract — not executable" | ✓ |
| Reuse callout, adapt per contract | Open-ended adaptation invites drift | |
| You decide | | |

**User's choice:** Reuse Phase-33 verbatim, with one bounded allowance.
**Notes:** Allowance — pure-deferral/owner-pending contracts (LOOP-03 collocation-50/50, LOOP-05 ALM-default, LOOP-06 M16, LOOP-08 SASD) use a status-tagged body + forward-reference instead of a pseudocode block. Only adaptation; no other restructuring.

---

## Packet-before-edit & ledger lifecycle

| Option | Description | Selected |
|--------|-------------|----------|
| Separate packet per finding (Phase-33 pattern) | One packet each for B-07/B-08/M16/ALM in 34/evidence/ before edits; close ledger rows with packet link + AC ID; LOOP-04 consumes the existing M14 verdict | ✓ |
| One combined LOOP packet | Couples findings with different owners/STOP risk (Phase-32 D-04 rejected umbrella packets) | |
| You decide granularity | Precedent already decides it | |

**User's choice:** Separate packet per finding.
**Notes:** EVID-15 + Phase-32 precedent + ledger Non-Headline Packet Mandate. Packets CONSUME the resolution-doc verdicts (§1.4 B-07 modified; §1.5 B-08 modified; §1.10 M16 defer; §1.18 ALM defer) — formalize, do not re-litigate. Use the existing EVID/AC reservation scheme (no new ID schema). If a packet surfaces a NEW conflict (e.g., a v1.5-verified fact vs the resolution verdict) → STOP per EVID-15 + 34-GAPS gap.

---

## LOOP-07 (IPR/PSC) & LOOP-08 (SASD)

| Option | Description | Selected |
|--------|-------------|----------|
| Direct transcription, provisional + v1.5 citation | v1.5 carry-forwards (VAL-02/03/04), no ledger row, no packet; recalibration FUT | ✓ |
| Author Phase-34 packets for them too | They aren't adjudication findings | |
| You decide | | |

**User's choice:** Direct transcription, provisional + v1.5 citation.
**Notes:** VERIFY each training-side role against v1.5 VAL-02/03/04 + existing spec. Source establishes role → transcribe provisional; source SILENT on a role → 34-GAPS STOP gap (owner-pending), NOT invented. LOOP-08 (SASD) consistent with M16 deferral — record the role + VAL-02/M16 citation, NO weighting formula. Default = no packet; a v1.5-vs-current-spec role conflict → packet + EVID-15.

---

## Per-step total-loss assembly skeleton

| Option | Description | Selected |
|--------|-------------|----------|
| Augment the existing ctl section (~1718-1745) | Extend Total-Loss/Data-Flow with the ordering skeleton; keeps the training-step narrative in one place | ✓ |
| New dedicated skeleton subsection | Fragments the narrative | |
| You decide | | |

**User's choice:** Augment the existing ctl section.
**Notes:** Ordering skeleton ONLY (forward → L_total → backward → Adam-only clip → step → optional ALM). Loss terms opaque with a Phase-35 forward-ref; do NOT define loss components / λ_E / Huber-δ; don't disturb PHYS-05 forward-refs. Clip step cross-references pinn §4.4; ALM step optional/deferred.

---

## Source-silent routing & probe scope

| Option | Description | Selected |
|--------|-------------|----------|
| Split: 34-GAPS for (a), in-body FUT for (b); probes for checkable formulas | (a) batch edges = STOP gap; (b) M14-deferred constants = body-deferred; formula-sanity probes only where checkable | ✓ |
| Both (a) and (b) as 34-GAPS entries | Pollutes the register with items the source already routed | |
| You decide | | |

**User's choice:** Option 1, with two corrections.
**Notes:**
- **Correction 1 (probe list):** the proposed `n_col ∝ dt_base/dt_out` probe is WRONG — LOOP-06/M16 is `defer`, formula not transcribed, nothing to probe. Probe ONLY: LOOP-01 `min(n_pts_cap, n_snapshots)`; LOOP-03 data-fidelity 50/50 split; LOOP-04 `clip_value = C_stage·median(...)`. LOOP-05/06/08 deferred (no probe). LOOP-02/07 structural (grep). LOOP-07 provisional values carried, not recalibrated.
- **Correction 2 (citation):** route (b) via the M14 packet's "Locked Convention or Owner Route" + resolution-doc §1.8, confirming the gap-ID — verified GAP-08 is present in the M14 packet (not assumed).

---

## LOOP-06 / M16 — collocation-scaling (parallel grounding finding, surfaced after batch 2)

The batch-2 answers exposed that 34-SPEC LOOP-06 said "transcribe `n_col ∝ dt_base/dt_out` provisional" while the cited M16 verdict (§1.10) is `defer` — the same preview→verdict failure mode as LOOP-04's 8.5.

| Option | Description | Selected |
|--------|-------------|----------|
| Fix SPEC (parallel to LOOP-04) | Reframe LOOP-06 Target + acceptance line to M16 = defer; formula not transcribed/probe-able; realized-as-deferred | ✓ |
| CONTEXT-only | Leaves the SPEC/verdict mismatch | |
| Keep transcribe-provisional (needs grounding) | Contradicts §1.10 + Correction 1 | |

**User's choice:** Fix SPEC (parallel to LOOP-04).
**Notes:** SPEC LOOP-06 Target + acceptance + checklist line rewritten to record the M16 `defer` (commit `0ffa3d8`); `defer` confirmed against §1.10 at packet-authoring.

---

## Claude's Discretion

- Number of Phase-34 plan files + task grouping (every LOOP-01..08 + SI-PINN-003 in a plan `requirements` field; packet-before-edit precedes each edit; executable by `gsd-execute-phase`).
- Exact evidence-packet filename slugs, ledger Markdown layout, and deterministic check commands.

## Deferred Ideas

- Phase 35 (LOSS): loss-component scaling, capped-hybrid `λ_E`, Huber-δ, causal-training-mode (D-04).
- FUT-01/FUT-04 (trainex): DataLoader, batch constructor, ALM mechanics, causal-window mechanics, Stage-0 pilot.
- FUT/SCOPE-15: adaptive-stage-assignment EDA + IPR/PSC/SASD recalibration.
- Owner-pending/deferred contract holes carried (not filled): M14-deferred clipping constants (body-deferred); source-silent batch edge cases (`34-GAPS.md`).
- Reviewed, not folded: `trainex-r1-research-handoff.md` (score 0.2) — trainex-track item, not Phase-34 specwork scope.
