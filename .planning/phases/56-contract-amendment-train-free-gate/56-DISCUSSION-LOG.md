# Phase 56: Contract Amendment & Train-Free Gate - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-06
**Phase:** 56-Contract Amendment & Train-Free Gate
**Mode:** autonomous (owner instruction 2026-09-06 — service every gray area,
choose the best-reasoned option grounded in the mathematics + `54-RULING.md` +
the codebase; surface only what genuinely needs owner review). No AskUserQuestion
turns. Watchdog chain `phase-55-56-work-4e71db4b036eb883` position 2.
**Areas discussed:** contract-amendment structure, GATE-04 implementation
architecture, `R_ref` persistence, secondary spec wordings, SC5 demonstration,
anchor/scope discipline, GATE-04 condition-(ii) acceptance schema, §2.4 table
convention.

---

## Contract-amendment structure (SPEC-01 / SPEC-06, SCOPE-38)

| Option | Description | Selected |
|--------|-------------|----------|
| Transcribe `54-RULING.md` | Copy the four SCOPE-38 blocks and the two verbatim re-issued acceptance criteria into §2.2/§3.2; compose only editorial connective prose | ✓ |
| Re-derive the amendment text | Re-express the ruling's dispositions in fresh spec language | |

**Choice:** Transcribe. The ruling's "SCOPE-38 re-ratification lines" section
already contains finished acceptance-criterion text (Block 1: AC-LOSS-04
re-issued; Block 4: the collocation-allocation AC). Blocks 2 (`first_omega_0`)
and 3 (clip) are ratified NOT AMENDED — recorded as such, not deleted.
**Notes:** one-way reversibility — a published contract amendment FUT-01 and
Phase 57 build against; the mitigation is that the source text is fixed.

## GATE-04 implementation architecture (GATE-04)

| Option | Description | Selected |
|--------|-------------|----------|
| New standalone `pinn/verification/gate04_train_free.py` | `argparse` `main(argv)`, frozen result dataclass, `PASS`/`BLOCK` verdict; imports the Phase 55 probe; not CI-wired; Phase 57 calls it | ✓ |
| Extend `architecture_characterization_probe.py` with gate logic | Fewer modules, but mixes measurement and acceptance concerns | |
| Extend `gate_metrics.py` | Wrong domain (that module is trajectory-gate metrics) | |

**Choice:** new standalone module, matching the established `*_probe.py`
convention (every `pinn/verification/` probe is a standalone script with no
verify-ladder wiring). The ratified-recipe `w_n` arithmetic is added as a pure
function *in the probe module* (peer to the committed `stratified_collocation_times`
/ `bin_mean_residuals` helpers), reusing `resolve_causal_clip_facts` — so the
recipe math has one home and GATE-04 measures the spec'd formula without a
trainer that implements it yet.
**Notes:** no `pinn/train.py` or `pinn/loss_catalog.py` edits (SCOPE-33;
FUT-01 owns the trainer rebuild).

## `R_ref` persistence & governance

| Option | Description | Selected |
|--------|-------------|----------|
| Committed JSON under `pinn/verification/artifacts/` with full provenance | value + 6 cases + 96 bin means + statistic + tree/config identity + invalidation triggers | ✓ |
| Generated-only (git-ignored) artifact | not re-derivable from version control; weak for a run-gating value | |
| Inline in the spec | a measured 96-sample median does not belong in a framework spec | |

**Choice:** committed JSON, GATE-04 writes it. The *procedure* is fully grounded
(`54-RULING.md` B2, GAP-54-03); only the path/format is a Claude call —
flagged for owner visibility, not a blocking gap.

## Secondary spec wordings

**Claude's discretion, grounded:** §4.1 `η_c = 1` default line reworded to
cross-reference the amended §3.2 block (value byte-preserved); §3.2 Listing 3
"recommended: 2048–4096" reconciled with the fixed `n_col = 4096` total (D3).

## SC5 demonstration

| Option | Description | Selected |
|--------|-------------|----------|
| Fire GATE-04 verdict logic on the existing pre-amendment probe output | raw `R̄`, `n_col = 16` → assert `BLOCK` (trips condition (i) + degeneracy) | ✓ |
| Build a synthetic degenerate vector | less faithful — the real pre-amendment recipe is the meaningful negative case | |

**Choice:** use the real pre-amendment path (the audit's six rows, 15/16 weights
at the float32 clamp floor). Committed test in `tests/phase56/` + evidence.

## GATE-04 condition (ii) — acceptance schema  →  SURFACED (GAP-56-01, HIGH)

| Option | Description | Selected |
|--------|-------------|----------|
| A — static dispersion floor (CoV / distinct-count / monotonicity / decade-span) | | |
| B — controlled-reduction response test only | | |
| C — both A and B | *(agent's lean, not adopted)* | |
| D — ship (i)+(iii) blocking, (ii) logged-only until Phase 57 checkpoint ③ | | |
| — | **Not agent-decided.** Recorded as GAP-56-01 for owner ratification. | ✓ |

**Choice:** surface, do not invent. Conditions (i) and (iii) and the non-finite
checks are grounded and precise; condition (ii)'s numeric threshold and the
"controlled residual reduction" test design are acceptance-check pass criteria
fixed by no source, and this threshold is the SCOPE-35 single-look protection.
CLAUDE.md STOP protocol (process-artifact-schema class) is not waived by the
autonomous directive.
**Notes:** dependency-scoped — blocks only the condition-(ii) wiring + SC5
margin; the amendment and GATE-04 scaffolding proceed.

## §2.4 Table 1 locked-vs-default convention  →  SURFACED (GAP-56-02, MEDIUM)

| Option | Description | Selected |
|--------|-------------|----------|
| A — apply `[LOCKED]` markers to the `first_omega_0` row (generalize the convention) | | |
| B — minimal header/footnote clarification, no convention change | *(agent's lean, not adopted)* | |
| C — leave §2.4 untouched, re-route the item | | |
| — | **Not agent-decided.** Recorded as GAP-56-02. | ✓ |

**Choice:** surface. GAP-45-03 consequence 5 explicitly left convention
generalization undecided; `first_omega_0` is NOT AMENDED so this is
consistency-only. Dependency-scoped — blocks only the §2.4 cosmetic edit.

---

## Claude's Discretion

- Section placement / heading text / connective prose of the new §2.2/§3.2
  sub-blocks (facts fixed by `54-RULING.md`).
- `gate04_train_free.py` dataclass field + CLI flag names.
- `ratified_causal_weights` exact signature (settle once — public API two
  phases consume).
- Evidence-directory layout; `tests/phase56/` test locations.
- Whether the controlled-reduction probe (post-GAP-56-01) lives in the probe or
  the gate module.

## Deferred Ideas

- L-BFGS / second-optimizer-phase causal-weight recomputation (GAP-54-06 →
  Phase 57 checkpoint ③).
- Invariant-B window `N = 500` re-ratification + front-monitoring aggregation
  (Phase 57 checkpoint ③).
- EVAL-02 spending-seed pre-registration (Phase 57 checkpoint 4).
- Power-skip stack as a capacity surface (GAP-54-02 closed — future ablation).
- Todos reviewed, not folded: `d-06-static-epsilon-sensitivity-check` (out of
  SCOPE-33), `trainex-r1-research-handoff` (unrelated).
