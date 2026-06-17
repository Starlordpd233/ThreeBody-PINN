# 29-CODE-DIVERGENCE.md — FUT-01 Forward Obligations (Phase 29)

**Phase:** 29 — Acceptance Checks, Re-verification, and Handoff
**Created:** 2026-06-17
**Purpose:** Forward-pointing FUT-01 hand-off record (the code-divergence half of the v1.4
Phase-21 two-artifact pattern; companion: `29-HANDOFF.md`). Records obligations v1.5
deliberately defers to FUT-01 implementation so they survive milestone closure. This is a
permitted forward-pointing hand-off document; live-`pinn/` and data-mutation references are
allowed here (SCOPE-10 carveout applies to hand-off docs only).

---

## FO-1 — Promote the 117 validated reruns + apply the 184 → 67 cascade

**Origin:** GAP-29-01 — Option A locked 2026-06-16 (Phase 29 reconciles the planning layer
only); the embedded promotion sub-decision was **ruled 2026-06-16 (advisor session)**. The
2026-06-14 missing-67 ruling (keep base; 67 permanent Stage-5 holes; no base→gold
substitution; no retry) is unchanged.

**Ruling — promote = yes, venue = the FUT-01 dataset-finalization gate, not v1.5.** v1.5 is
spec-construction; promotion is a canonical-`simulation_data/` mutation whose first consumer
is the FUT-01 training pipeline. Execute it as the **first FUT-01 step, before any
DataLoader/training code reads gold**, as ONE atomic transaction — the cascade is indivisible
(promoting without flipping `AC-PIPE-05` to 67/67 makes `AC-PIPE-05` fail). Nothing in v1.5
consumes gold numerically, so deferral costs nothing; a partial cascade would break the
set-difference invariant.

**Gold-completeness reconciliation (settled, final in shape):**

| Quantity | Value | Evidence |
|---|---|---|
| Standard quasi-random ICs | 2,749 | 24-VERIFIED-FACTS CLM-05b |
| Gold counterparts present (canonical) | 2,565 | CLM-05b; AC-PIPE-05 (184/184) |
| Missing gold (pre-rerun) | 184 | CLM-04; `not_in_gold.md` (184/184) |
| Rerun attempted | 184 | `run_manifest.json` |
| Rerun validated — staged, unpromoted | 117 | `validation_summary.json` (117 pass) |
| Rerun permanent-absent (MNAR holes) | 67 | 35 timeout + 10 stall + 22 signal-killed; all "missing full Result footer"; gold runs die median t≈1.32 vs horizon t=10 |
| Promoted into canonical gold | 0 | deferred to this gate |
| Gold after promotion | 2,682 | 2,565 + 117 |
| Permanent gold holes after promotion | 67 | 2,749 − 2,682 |

The 117 are gold-config-homogeneous **by construction** (footer `tol=1e-13`/`Lw=130`/`dt=0.01`;
`final_time≈10.01`), enforced by the rerun validation gate — so promotion adds no provenance
heterogeneity. The 67 are informatively censored (MNAR): the chaotic close-encounter tail
where 130-digit gold integration is non-terminating; their base trajectories are kept per the
2026-06-14 ruling.

**Atomic cascade to execute at the gate (all-or-nothing):**

1. `--validate-only` re-check, then `--promote` the 117 → canonical gold 2,565 → 2,682.
   Runner: `simulation_data/Scripts/brutus_runners/rerun_standard_gold_missing_184.py`
   (currently untracked — ensure it and its test are preserved/committed before the gate).
2. `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md`: 184 → 67 IDs.
3. `ctl_instruction.md` Step 5 gold-counterpart note: "remediation backlog expected empty
   post-rerun" → "reduced 184→67; residual 67 irreducible (gold integration non-terminating
   at close encounters), permanent Stage-5 holes."
4. Set-2b / issue-02 count fields: 2,565 → 2,682.
5. `AC-PIPE-05` assertion + runner `EXPECTED_ID_COUNT`: 184 → 67, **and re-derive the count
   from the parsed `not_in_gold.md` content rather than re-hardcoding `67`** (mirrors the
   blacklist-contract anti-hardcode rule, `ctl_instruction.md` Step-1A); then re-run
   AC-PIPE-05 — it must pass at 67/67.
6. M13 / GAP-26-01 packet (`m13-gold-counterpart.md`) + ledger M13/G4 rows: record OI-7b final
   outcome — 117 gold counterparts restored (promoted), 67 permanently absent (irreducible);
   the 1:1 base:gold target is met for 117/184, the remaining 67 are permanent Stage-5 holes.
   **Factual-outcome record only — the LOCKED M13 verdict (GAP-26-01 = Option B; re-simulate;
   no base→gold substitution) is untouched.** If the edit reads as re-adjudication, STOP and
   re-surface (D-01a).

**Interim durability action — do NOW, independent of the gate:** the 117 staged outputs +
`run_manifest.json` (per-file `output_sha256` recorded) live under
`simulation_data/Data/rerun_staging/standard_gold_missing_184/` — a bulky simulation payload
the migration runbook excludes from the normal copy. Add them to the separate
simulation-payload backup set; regenerating a lost output costs ~1 Brutus-hour each.

## FO-2 — PSC/SCR first-run sanity check + validation-constant recalibration

**Origin:** GAP-28-03 (reopened + RESOLVED 2026-06-16; canonical PSC clause landed in
`ctl_instruction.md` `Data-side quality-metric contracts`). The PSC composition
(dedup-prefer-gold + `1/N_t`) is ratified and promotion-invariant; only the construction
constants are calibrated here.

At the same dataset-finalization gate, AFTER FO-1 (the pool is then final):

- Compute PSC + SCR on the final post-promotion pool; confirm or revise the resolution doc's
  provisional candidate (sorted scaled pair-distance coordinates, permutation-invariant;
  log-bins `[1e-3, 1e2]`, 25 per axis, `K = 625`; `H_norm = H / ln K`; Miller-Madow
  finite-sample correction; SCR `d_min < 0.5` anchor).
- Recalibrate the SASD `0.5` and IPR `1e-3` flag thresholds against the admitted-set
  distributions (both already landed provisional).
- AC-VAL-04 **numeric** sanity executes here; the AC-VAL-04 **structural** check executes in
  Phase 29.

## Stale-record inventory (known-stale until FO-1 lands)

Each record below is deliberately left at its pre-promotion value during v1.5; FO-1 is the
single corrective transaction. Listed so the staleness is documented, never silent:

| Record | Current (stale) value | Corrective (FO-1 step) |
|---|---|---|
| `standard_quasi_random_ids_not_in_gold.md` | 184 IDs | → 67 (step 2) |
| `AC-PIPE-05` assertion | 184/184 | → 67/67 (step 5) |
| runner `EXPECTED_ID_COUNT` | 184 | → 67, re-derived (step 5) |
| `ctl_instruction.md` Step 5 gold note | "backlog expected empty" | → 67 irreducible (step 3) |
| Set-2b / issue-02 counts | 2,565 | → 2,682 (step 4) |
| M13/G4 ledger + packet | OI-7b "not yet executed" | → OI-7b final outcome (step 6, factual) |

During v1.5 the M13/G4 ledger rows + packet carry an OI-7b-**partial** reconciliation note
(117/184 validated-staged, 67 permanent-absent, 0 promoted; promotion ruled to this gate).
M13/G4 stay VERIFIED; the verdict is untouched.

---

*Cross-refs:* GAP-29-01 (`29-GAPS.md`), GAP-28-03 (`28-GAPS.md`), M13/GAP-26-01
(`.planning/phases/25-evidence-framework-and-issue-ledger/evidence/m13-gold-counterpart.md`),
agent-memory `missing-67-gold-decision` (2026-06-14 ruling).
*Phase: 29-acceptance-checks-re-verification-and-handoff*
