# Phase 28 EDL Findings — SASD endpoint (GAP-28-01) & IPR units (GAP-28-02)

**Status:** NON-CANONICAL EDL decision-support. Does NOT resolve the gaps and authorizes no
spec edit. Produces the resolution-doc-specified verification numbers so the user can rule on
two source-silent semantic forks with data in hand. Per CLAUDE.md, the gap registers remain
the authoritative blocking/resolution record.

**Produced:** 2026-06-16 · **Script:** `compute_sasd_ipr_distributions.py` · **Data:** `results.json`
**Runtime:** `.venv/bin/python` (numpy 2.2.0, scipy 1.17.1)

## Method

- Construction is the **settled** part of each contract (02-resolution-doc.md §5.2/§5.3 + the two
  EVID-06 packets). Only the endpoint (SASD) and the units (IPR) are the open forks.
  - SASD_i = `dt_i · max_body[ ||a_b|| / max(||v_b||,1e-12) ]`, per-body max, full-norm, flag `>0.5`.
    left = ratio at `t_i`; both = `max(ratio(t_i), ratio(t_{i+1}))`. SASD is scale-invariant.
  - IPR = `mean_k || q''_spline(τ_k) − F_grav^ε(q_spline(τ_k)) ||²`, `CubicHermiteSpline(t,q,dydx=v)`,
    10 mid-offset points/interval, ε=1e-10, G=1, flag `>1e-3` (raw). Open fork: raw vs scaled (~464×).
- **Validation (code correctness):** analytic equal-mass circular binary, well-resolved → IPR = **1.1e-10**;
  coarsened to dt=0.17 → **8.9e-6**. The machinery is correct and 1e-3 is a meaningful threshold for clean dynamics.
- **Population:** "clean" = `min_sep ≥ 0.01` (no collision) & `max_sep ≤ 100` (no escape), a stated proxy
  for the Stage-gate admitted set. Sample 150 trajectories/tier, seed 42.

## Results (clean subset)

| Tier | n | IPR(raw) p50 | IPR flag raw>1e-3 | IPR flag scaled>1e-3 | SASD left>0.5 | SASD both>0.5 | cross-only-both |
|------|---|--------------|-------------------|----------------------|---------------|---------------|-----------------|
| std_base  | 150 | 2.6e4 | 100% | 100% | 100% | 100% | **0** |
| std_gold  | 137 | 1.2e4 | 100% | 100% | 99%  | 99%  | **0** |
| hier_base | 150 | 2.6e2 | 100% | 100% | 100% | 100% | **0** |
| hier_gold | 150 | 2.2e2 | 100% | 100% | 73%  | 73%  | **0** |

Gold IPR(raw) median stratified by minimum approach distance (intrinsic close-encounter dependence):

| min_sep ∈ | n | median IPR(raw) |
|-----------|---|-----------------|
| [0.01,0.05) | 121 | 2.6e4 |
| [0.05,0.1)  | 33  | 8.0e1 |
| [0.1,0.3)   | 129 | 1.8e2 |
| [0.3,1.0)   | 4   | 5.1e1 |

## Interpretation (evidence, NOT a decision)

**GAP-28-01 / SASD endpoint — clean signal favoring BOTH-endpoint.**
`cross-only-both = 0` in **every** tier, including the non-saturated hier_gold (73%): no trajectory
crosses the 0.5 flag only under both-endpoint evaluation. The resolution doc's claim that both-endpoint
*strictly dominates* (monotone; closes the final-snapshot blind spot; one extra eval) is confirmed, and
on this dataset it expands the flagged set by **zero**. Adopting both-endpoint is empirically free; the
DQA-literal left endpoint yields the same flag set here. → Endpoint choice is low-risk either way; both
gains the theoretical blind-spot closure at no observed cost.

**GAP-28-02 / IPR units — the proposed tripwire is INCONCLUSIVE; decide on grounded convention.**
The resolution doc proposed the *gold flag-rate tripwire* as the decisive test ("raw-1e-3 flagging a
large fraction of gold ⇒ wrong unit pin"). Empirically it **saturates in both conventions**: 100% of
clean gold flags at raw-1e-3 *and* at scaled-1e-3. The stratification shows why and shows it is
intrinsic, not a filter artifact — IPR is dominated by close-encounter under-resolution, and this
dataset's trajectories almost all have close approaches < 0.3 (only 4/287 gold beyond it), so even the
gentlest clean trajectories sit at median raw IPR ≈ 50, i.e. 4–7 orders above either threshold. Two
consequences:
1. **Flag-rate cannot arbitrate raw vs scaled.** The grounded basis for the units choice is
   convention-consistency: the pipeline (a SCOPE-06/07 grounding source) computes energy/conservation
   in **raw G=1 units** (verified in `calculate_metrics.py`), which is the resolution doc's primary raw
   argument — now grounded rather than asserted. On that basis raw is the better-grounded pick.
2. **NEW finding — the `1e-3` IPR threshold is empirically mis-calibrated in both conventions** and must
   be re-anchored to the admitted-set distribution. The resolution doc anticipated this ("1e-3 …
   provisional pending the admitted-set distribution"). Re-anchoring toward *scaled* makes it worse
   (scaled-1e-3 = raw>2.16e-6, a stricter raw threshold). Threshold calibration is a separate axis from
   the units pin and is forward work (doc-03 / FUT-01), independent of which unit convention is canonized.

**Parallel note (SASD threshold):** SASD's `0.5` flag also over-flags on the clean proxy set (73–100%),
consistent with the resolution doc marking it "provisional pending the admitted-set distribution." Like
IPR's 1e-3, the SASD *definition/endpoint* is landable; the *threshold constant* is provisional/forward work.

## Caveats

- "Clean" is a proxy for the admitted set (no-collision/no-escape), not the exact Stage-gate output; the
  stratification shows the threshold saturation is intrinsic to the dynamics, not an artifact of the proxy.
- The raw↔scaled factor (~464) is the resolution doc's stated value under the locked constants; the
  empirical conclusion (both conventions saturate) is robust to its exact value by many orders of magnitude.
