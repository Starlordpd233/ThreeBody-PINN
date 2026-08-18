# Phase 47: Frame Completion & S_H Pipeline - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-07-29
**Phase:** 47-frame-completion-s-h-pipeline
**Areas discussed:** S_H softening and term source, Where S_H is computed, eps_h threading and h0, Test correction and re-probe

**Session mode:** the owner declined the interactive round —
*"discuss and surface all sections and areas; then, automatically choose the best
option following your own best judgement. I trust you in this, so no need for an
interactive session for discussion and picking the best option."*
All four areas were surfaced and resolved in a single pass.

**Outcome that reshaped the session:** three of the four areas turned out to be
**already answered by `pinn_architecture.md` §3.4 lines 539-542**, which was read
after the areas were framed but before any option was selected. Where grounded
text existed it governed, including in one case against the option the agent had
been leaning toward. Only the mechanism-level choices were genuinely the agent's.

---

## S_H softening and term source

| Option | Description | Selected |
|--------|-------------|----------|
| `EPS_SOFT = 1e-5` (loss-side) | The softening `_matched_plummer_hamiltonian` uses, and therefore what today's per-anchor `h0` already uses. Consistent with the `\|H_0\| + ε_H` denominator `S_H` will sit beside. | ✓ |
| `EPS_INV = 1e-10` (verification-side) | What `compute_invariants` uses for `E` and what gate `ε_H` uses. Attractive because `compute_invariants` already computes structurally identical `T_kin` and `V_pot` terms in the scaled frame, per trajectory, at admission. | |
| Exact Newtonian (no softening) | Formula-literal reading of `K0 + Uabs0`. | |

**Selection:** `EPS_SOFT = 1e-5` — **decided by grounded text, not judgement.**
`pinn_architecture.md:539-542` specifies "the matched-Plummer Hamiltonian
components with `ε_train = 10^-5`", and line 544 (VAL-03) makes conflating
`ε_train = 1e-5` with `ε_inv = 1e-10` an explicit conformance error;
`gate_metrics.py:145` carries the matching "NEVER" warning from the other
direction.

**Notes:** The agent had flagged the `compute_invariants` path as the leading
reusable asset before reading §3.4 — it computes the right shape of quantity in
the right frame at the right moment, and only the softening constant is wrong.
This is recorded because it is the trap most likely to catch a downstream
implementer: the wrong source looks *more* reusable than the right one. Term
source resolved with it — `compute_invariants` returns only the signed `E`, so
the components come from a `loss_catalog` extraction instead (CONTEXT D-11).

---

## Where S_H is computed

| Option | Description | Selected |
|--------|-------------|----------|
| Float64 components at admission, median reduced once at run setup | Mirrors the existing `raw_ic13_population` → `compute_normalization_stats` two-pass, and keeps the float64 capture on the float64 side of the fp32 residency boundary. | ✓ |
| Reduce from residents via `StageIndex.snapshot_positions` | Simplest — the train split is already materialized there and no per-record plumbing is needed. | |
| Compute inside admission pass 2 entirely | Single location, no run-setup step. | |

**Selection:** float64 at admission, reduced once at run setup.

**Notes:** Two constraints eliminated the alternatives rather than agent
preference. Reducing from residents violates §3.4's explicit "computed once in
**float64**" — `StageIndex` accessors return the fp32 resident tensors, so that
option is wrong in a way that would never show up as a test failure. Reducing
inside admission pass 2 is impossible as stated: `S_H` is `median_**train**`, and
the adapter has no split knowledge (`grep split pinn/data/adapter.py` returns
only `str.split` calls). The split arrives via
`StageIndex.from_split(adapter, manifest, "train")`, which is resolved at run
setup. What remained genuinely the agent's call was only *where the per-record
values are carried* — settled on the established `_source_value` accessor
pattern.

---

## eps_h threading and h0

| Option | Description | Selected |
|--------|-------------|----------|
| Run-level constant injected into `_AnchorContext.eps_h`; `abs(h0)` stays in the denominator | Minimal change at `controllers.py:482`; preserves the per-test override seam controller tests use. | ✓ |
| Module-level global read at use site | Fewer moving parts. | |
| Replace `h0` in the denominator as well | Would make the denominator fully dataset-wide. | |

**Selection:** run-level constant injected into `_AnchorContext`.

**Notes:** The third option was ruled out by grounded text — §3.4:542 says
*"Use `ε_H` only in `\|H_0\| + ε_H`"*, so the per-anchor `abs(h0)` is contractually
correct **in the denominator**. The defect is narrower than it first appears:
today's `eps_h = abs(h0) * factor + 1e-12` is wrong because `h0` supplies the
*scale*, making every anchor its own yardstick — not because `h0` appears at all.
The global-variable option was rejected on the existing test seam alone.
Fail-closed **timing** was the agent's call: at setup before step 1, so a run
that cannot produce a valid `ε_H` never emits a step that would later read as
real evidence.

---

## Test correction and re-probe

| Option | Description | Selected |
|--------|-------------|----------|
| Correct `tests/phase46/test_pairing_repair.py` in place; spend the re-probe once as regression evidence | Keeps one oracle per property; confirms the swap reached the surface the probe reads. | ✓ |
| Supersede with a new Phase 47 test file, leaving the Phase 46 test intact | Preserves the CONF-08 acceptance record unmodified. | |
| Skip the re-probe; rely on unit assertions only | Cheapest; the re-probe is no longer a frame test. | |

**Selection:** correct in place, and spend the re-probe once.

**Notes:** Superseding was rejected because it would leave two test files
asserting opposite frames for the same property — the "competing metric oracle"
pattern `46-CONTEXT.md` explicitly warns against. The CONF-08 assertions that
remain true are unaffected; only the clause encoding *"deliberately without
rotation gauge or D/V scaling"* moves. The re-probe is explicitly permitted by
the ROADMAP's Phase 47 boundaries as a regression check with `identity_scaled`
true by construction, and is worth its cost as the only end-to-end confirmation
available; it is recorded as regression evidence and **not** as a new CONF-01
verdict (SCOPE-29).

---

## Claude's Discretion

The owner delegated all selection for this session. Genuinely agent-decided (as
opposed to grounded): CONTEXT D-03, D-06, D-07, D-08 check design, D-11, D-12
placement, D-14, D-16, D-17 timing, D-18, D-21, D-22 spend decision, D-23. Each
is revisable on owner instruction without disturbing a grounded decision.

Both auto-matched todos were **withheld** rather than folded, against auto-mode's
score-based default: `.planning/REQUIREMENTS.md` leaves the carried-forward todos
unlinked to v2.2, and `d-06-static-epsilon-sensitivity-check` in particular is
the tuning-shaped work SCOPE-29 forbids — even though it is thematically adjacent
to §3.4's dual-epsilon note. Phase 46 made the same call on the same todo.

## Deferred Ideas

Carried to CONTEXT.md `<deferred>`: CONF-04..07 (Phase 48, with CONF-05's bound
chosen after both CONF-04 and CONF-09); removal of the now-unused
`r_com_ordered`/`v_com_ordered` fields; the §3.4:542 duplicate-`10^-5` author
comment as a VER-20 routing candidate; the conformance-enforcement regime
(Phase 49); Stage-0 training and the single held-out evaluation (Phases 50-51);
recipe tuning (v2.3).
