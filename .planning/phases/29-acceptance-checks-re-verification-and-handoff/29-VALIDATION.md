---
phase: 29
slug: acceptance-checks-re-verification-and-handoff
status: satisfied
nyquist_compliant: true
wave_0_complete: true
created: 2026-06-17
closed: 2026-06-17
closed_by: g1-g8-milestone-closure-gate
gate_result: "G1 PASS | G2 PASS | G3 PASS | G4 PASS | G5 PASS | G6 PASS | G7 PASS | G8 PASS — v1.5 closes"
---

# Phase 29 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Phase 29 is the TERMINAL closure phase of milestone v1.5. The "tests" are the
> disposable acceptance probes (`bash`+`grep -qE` spec-consistency checks and
> `python3` dataset checks) — the established AC-PIPE/AC-VAL pattern. No xUnit
> framework; no `pinn/` code is touched (VER-09 / SCOPE-10).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Disposable acceptance probes — `bash`+`grep -qE` spec-consistency checks; `python3` set-difference/dataset checks. The AC probes ARE the tests. |
| **Config file** | None — probes are standalone scripts (e.g. `ac-pipe-04.sh`, `ac-pipe-08.sh`, `ac-pipe-09.sh`) or inline blocks recorded in `29-UAT.md`. |
| **Quick run command** | `bash <probe>.sh` for a single AC (e.g. `bash .planning/phases/27-*/ac-pipe-09.sh`) |
| **Full suite command** | The `29-UAT` driver re-running all 13 AC probes + emitting a pass/fail table (to be defined by the plan; see Wave 0). |
| **Estimated runtime** | ~seconds per probe; the full 13-check suite is well under a minute (all reads of local `.planning/` artifacts + on-disk `simulation_data/`). |

---

## Sampling Rate

- **After every task commit:** Re-run the AC probe(s) the commit touched + the ledger row-audit if a ledger row was edited.
- **After every artifact (UAT / HANDOFF):** Full 13-check AC re-run + full 19-row ledger row-status audit.
- **Phase gate (before `/gsd-verify-work`):** All 13 AC rows PASS-or-explicitly-DEFERRED, 0 non-terminal ledger rows, 3 SI dispositions recorded, traceability confirmed — i.e. closure gate G1–G8 all green.
- **Max feedback latency:** < 60 seconds (no network, no build, no `pinn/` execution).

---

## Per-Requirement Verification Map

> Task-level rows (`29-NN-NN`) are filled by the planner once PLAN.md files exist.
> This requirement-level map is the Nyquist contract the plan tasks must satisfy.

| Req ID | Behavior | Test Type | Automated Command | Evidence Exists? | Status |
|--------|----------|-----------|-------------------|------------------|--------|
| VER-07 | Each of 13 ACs names pass criterion + data + executor | structural review | inspect each AC row in `29-UAT.md` | ✅ ACs defined; ❌ unified table is Wave 0 | ⬜ pending |
| VER-09 | 13 ACs executed as disposable probes, recorded pass/fail | spec+dataset probe | re-run probes → `29-UAT.md` | ⚠️ 3/13 persisted (`ac-pipe-04/08/09.sh`); 10/13 need re-derivation | ⬜ pending |
| VER-09 (AC-PIPE-05) | `base−gold == not_in_gold.md` (184/184, 0 promoted) | dataset probe | Python set-difference over `simulation_data/` | ✅ pattern exists (`data03_gold_gap.py`); ❌ fresh run | ⬜ pending |
| VER-09 (AC-VAL-04) | PSC clause present/well-formed/cites packet (structural); numeric DEFERRED | grep structural probe | grep over `ctl_instruction.md:645-692` | ✅ clause landed; ❌ structural probe Wave 0 | ⬜ pending |
| VER-11 | Handoff lists fixed/unchanged/deferred + FUT-01 divergence | doc-structure review | inspect `29-HANDOFF.md` vs `21-HANDOFF.md` shape | ❌ `29-HANDOFF.md` Wave 0; `29-CODE-DIVERGENCE.md` ✅ exists | ⬜ pending |
| VER-12 | 3 SI entries each retired-with-backref or preserved-with-reason | doc-structure review | inspect `29-HANDOFF.md` §SI table | ❌ Wave 0 (definitions located; dispositions to record) | ⬜ pending |
| VER-08 | 36/36 reqs map to exactly one phase | traceability review | inspect `REQUIREMENTS.md` Traceability table | ✅ 36/36 mapped; confirmation-only | ⬜ pending |
| D-07 (ledger close) | 0 non-terminal in-scope rows; PSC DEFERRED named | row-status audit | enumerate Status Table rows (19) | ✅ rows terminal (18 VERIFIED + 1 DEFERRED); ❌ audit recorded in `29-UAT.md` | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `29-UAT.md` — full 13-row AC pass/fail table (command/function, data, pass criterion, result, evidence) + 19-row ledger row-status audit + reference to the `29-CODE-DIVERGENCE.md` gold table. Covers VER-07/09 + D-07.
- [ ] Re-runnable probes (or inline recorded runs) for the 10 non-persisted ACs (AC-PIPE-01/02/03/05/06/07/10, AC-VAL-01/02/03) + the AC-VAL-04 structural probe. Covers VER-09. (3/13 already persist: `ac-pipe-04/08/09.sh`.)
- [ ] `29-HANDOFF.md` — fixed / intentionally-unchanged / deferred sections + the SI-DQA-002/003 + SI-PINN-002 disposition table (mirror `21-HANDOFF.md`). Covers VER-11/12.
- [ ] ROADMAP Phase 28 progress row + footer reconciliation (PSC landed/RESOLVED; Phase 29 in progress). Covers D-01 in-scope reconciliation.
- [ ] Milestone-closure gate definition (G1–G8: the per-requirement pass/fail criteria + the route-back-on-fail rule). Covers VER-09 routing clause.

*Already complete (NOT Wave 0): `29-CODE-DIVERGENCE.md` (FO-1/FO-2 + gold table + stale inventory), `29-GAPS.md` (GAP-29-01), STATE.md gold-framing (L31), and the M13/G4 OI-7b-partial ledger note.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| M13/G4 OI-7b note reads as factual-outcome, not re-adjudication | D-01a | Semantic judgment a grep cannot make | Human reads the M13/G4 rows; if the note re-decides the LOCKED `accept-third-position`/Option-B verdict → STOP per STOP protocol |
| SI-PINN-002 3rd-comment disposition is not a silent semantic call | VER-12 / D-08 | "Does M12 discharge the author comment?" is source-silent | If marking retired-by-M12 (vs preserve-with-reason), surface per STOP protocol before recording |
| No source-silent SI/AC disposition is invented | STOP protocol | Governance, not automatable | Each disposition cites a grounding source; any white-space fill → surface, do not invent |

---

## Validation Sign-Off

- [x] All tasks have an `<automated>` AC-probe verify (or an explicit manual-only justification above)
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING probe references (the 10 non-persisted ACs)
- [x] No watch-mode flags; probes are single-shot
- [x] Feedback latency < 60s
- [x] Closure gate G1–G8 defined with numeric pass criteria + route-back-on-fail
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved (closure-recorded 2026-06-17; see Milestone-Closure Gate Pass below)

---

## Milestone-Closure Gate Pass (recorded 2026-06-17)

The G1–G8 closure gate defined in `29-HANDOFF.md` §6 was re-executed end-to-end fresh
(2026-06-17T11:38Z) and all eight conditions PASS. Recorded below for closure traceability.

| # | Gate Condition | Numeric Pass | Result | Evidence |
|---|----------------|--------------|--------|----------|
| **G1** | All 13 ACs executed fresh (VER-07/09) | 12 PASS + AC-VAL-04 split (STRUCTURAL PASS / NUMERIC DEFERRED); 0 FAIL | **PASS** | `bash run-ac-suite.sh` exit 0; 13 result lines (12 PASS + 1 split) |
| **G2** | AC-PIPE-05 dataset probe (VER-09) | PASS @184/184 (0 promoted; consistent under D-01) | **PASS** | `python3 ac-pipe-05.py` → `AC-PIPE-05 PASS 184/184` (base=2749, gold=2565, not_in_gold=184, promoted=0) |
| **G3** | 19-row ledger audit (D-07/VER-10) | 18 VERIFIED + 1 DEFERRED; 0 PENDING/IN_PROGRESS/FIX_APPLIED | **PASS** | Enumeration of `24-ISSUE-LEDGER.md` Status Table (rows 23-41): 19 unique rows; PSC = DEFERRED; all others VERIFIED |
| **G4** | 3 SI dispositions recorded (VER-12) | SI-DQA-002, SI-DQA-003, SI-PINN-002 each retired-with-backref OR preserved-with-reason; SI-PINN-003 NOT folded in | **PASS** | `29-HANDOFF.md` §4 SI table: SI-DQA-002 retired-with-VAL-01/SCS-row backref; SI-DQA-003 retired-with-VAL-01 backref; SI-PINN-002 preserved-with-reason citing D-08. SI-PINN-003 absent. |
| **G5** | Handoff completeness (VER-11) | `29-HANDOFF.md` has 7 sections (Evidence Used, Fixed, Unchanged, Deferred, SI Recon, FUT-01, G1-G8); `29-CODE-DIVERGENCE.md` FO-1/FO-2 present | **PASS** | 7 `## ` headers in `29-HANDOFF.md`; FO-1 (gold promotion + 184→67 cascade) and FO-2 (PSC numeric) in `29-CODE-DIVERGENCE.md` |
| **G6** | Traceability 36/36 (VER-08) | 36/36 reqs → exactly one phase; Phase 29 = VER-07/08/09/11/12 | **PASS** | `REQUIREMENTS.md` Coverage block: 4+7+0+6+4+4+5=36; Phase 29 = {VER-07, VER-08, VER-09, VER-11, VER-12}; lines 147-151 show "Complete (2026-06-17; ...)" |
| **G7** | Gold reconciliation recorded (D-05/D-01) | `29-ACCEPTANCE-EVIDENCE-2026-06-17.md` references 117/67/0-promoted; stale-artifact inventory present; PSC numeric DEFERRED | **PASS** | 117/67/0-promoted table referenced; `29-CODE-DIVERGENCE.md` FO-1 inventory present; PSC ledger row = DEFERRED with FO-2 named |
| **G8** | Governance — no `pinn/` touch, no spec edit, no read-only/frozen-file edit | All Phase-29 commits touch only `.planning/` + optional probe scripts | **PASS** | `git log milestone/v1.5 --since="2026-06-10"` shows no `pinn/`, no `ctl_instruction.md`, no `pinn_architecture.md`, no `sampling_method.md`, no `data_quality_assessment.md`, no `simulation_data/` canonical files |

**Closure rule (per `29-HANDOFF.md` §6):** v1.5 closes only when G1–G8 all pass. Result: **G1–G8 ALL PASS.** v1.5 closure condition is met. Per `.planning/STATE.md` and the v1.5-workflow decision, the `--no-ff` merge of `milestone/v1.5` → `master` is the user-owned final step.

**No G1/G2/G3 FAIL routing triggered** (none failed).
