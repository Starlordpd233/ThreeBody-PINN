---
phase: 29
slug: acceptance-checks-re-verification-and-handoff
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-06-17
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

- [ ] All tasks have an `<automated>` AC-probe verify (or an explicit manual-only justification above)
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING probe references (the 10 non-persisted ACs)
- [ ] No watch-mode flags; probes are single-shot
- [ ] Feedback latency < 60s
- [ ] Closure gate G1–G8 defined with numeric pass criteria + route-back-on-fail
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
