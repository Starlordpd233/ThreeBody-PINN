# Phase 25: Evidence Framework and Issue Ledger - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-06-11
**Phase:** 25-Evidence Framework and Issue Ledger
**Mode:** `--all --auto` — per the combination rule, `--auto` governs the discussion (Claude selects the recommended option for every question, no AskUserQuestion); `--all` contributes area auto-selection. User instruction for this session: auto-advance through discussion, **stop before planning** (auto-advance to plan-phase explicitly suppressed).
**Areas discussed:** Phase-scope split, Evidence-packet machinery, EVID-10 root-cause adjudications, Ledger operation under VER-10, Gate compliance & sequencing

`[--auto/--all] Selected all gray areas: Phase-scope split; Evidence-packet machinery; EVID-10 adjudications; Ledger operation (VER-10); Gate compliance & sequencing.`

---

## Phase-scope split (what Phase 25 adjudicates vs. enables)

| Option | Description | Selected |
|--------|-------------|----------|
| Machinery + 3 known EVID-10 conflicts (Reading A) | Phase 25 ships the protocol/template/ledger operation and adjudicates only the three roadmap-named conflicts; owning phases 26–28 author per-finding packets+verdicts immediately before their edits | ✓ |
| Full adjudication (Reading B) | Phase 25 authors packets + verdicts for all 19 findings; 26–28 only fix and verify | |

`[auto] Phase-scope split — Q: "Does Phase 25 assign verdicts for all findings or only the known conflicts?" → Selected: "Machinery + 3 known EVID-10 conflicts" (recommended default)`

**Notes:** Selected on: roadmap Verification protocol assigns adjudicate→fix→verify to every phase 25–29; Phase 27/28 criteria reference edits applied "per the EVID-10 record"; Phase 25 goal sentence; v1.4 Phase 16 precedent (no verdicts shipped; EVID-01..05 "defined"). **Tension flagged to user in CONTEXT D-01:** Phase 25 success criteria 1–3 restate EVID-06..09 and admit a literal whole-inventory reading; if the user prefers Reading B, replan Phase 25 before planning proceeds.

---

## Evidence-packet machinery

| Option | Description | Selected |
|--------|-------------|----------|
| Instantiate v1.4 12-section template with v1.5 substitutions | Adapt `16-.../evidence/_TEMPLATE.md`: resolution-doc + issue-doc source positions, NEW dataset-evidence section (EVID-06 4th source), FUT-01 hand-off retained, EVID-10 sections where Sources-Disagree=YES | ✓ |
| Redesign packet schema for v1.5 | New structure tailored to data-pipeline findings | |

Packet location:

| Option | Description | Selected |
|--------|-------------|----------|
| `evidence/` under Phase 25 directory | Mirrors v1.4 (framework phase owns the dir; later phases write into it) | ✓ |
| `evidence/` under Phase 24 directory beside the ledger | Co-locates packets with the ledger | |

`[auto] Evidence-packet machinery — Q: "Template form and packet location?" → Selected: "v1.4 schema with v1.5 substitutions; evidence/ under Phase 25 dir" (recommended default)`

**Notes:** Ledger stays at its roadmap-locked stable path under Phase 24; Evidence Packet column links out. Resolution-doc citations follow the 24.5-RESOLUTION-MAP citation guide.

---

## EVID-10 root-cause adjudications

| Option | Description | Selected |
|--------|-------------|----------|
| Exactly the three roadmap-named conflicts | ratio-SCS vs locked gate; D=6.694 vs PHYS-01; M11/M12 severity reclassifications — full packets each | ✓ |
| Expand work list opportunistically | Also pre-adjudicate any further disagreement found while reading | |

`[auto] EVID-10 adjudications — Q: "Work-list scope for Phase 25 EVID-10 records?" → Selected: "Exactly the three roadmap-named conflicts" (recommended default)`

**Notes:** New conflicts discovered during Phase 25 reading are recorded on the ledger (Sources-Disagree flag) for the owning phase, not silently adjudicated early. Verdict grounding: transcribe the resolution doc unless evidence shows failure; locked conventions are hard constraints — overturning one requires a STOP gap/user decision. Resolution-doc-silent facets → `defer-with-blocker` or STOP gap.

---

## Ledger operation under VER-10

| Option | Description | Selected |
|--------|-------------|----------|
| Keep v1.4 lifecycle verbatim, fix stale applicability text | Re-issue Lifecycle Rules for Phases 26–29; state machine, batch=one plan, transitive-dependent re-verification, exit gate unchanged | ✓ |
| Redesign re-verification policy for v1.5 | New regression rules | |

Sub-decisions: G1–G5 synthesis rows close with parent findings (no separate packets); no new AC-IDs minted (seeded assignments stand); Dependents extensions allowed with per-finding annotation.

`[auto] Ledger operation — Q: "Lifecycle rules and synthesis-row handling?" → Selected: "v1.4 lifecycle verbatim + stale-text fix; G-rows inherit parents; no new AC-IDs" (recommended default)`

---

## Gate compliance & sequencing

| Option | Description | Selected |
|--------|-------------|----------|
| Execution gated on 24.5 pass; tag at execution start | Planning artifacts may be prepared now; executor confirms 24.5 verdict; `v1.5-pre-phase-25` cut after 24.5 passes | ✓ |
| Cut pre-phase tag now (Phase 24 D-25 timing) | Tag during discuss session | |

`[auto] Gate & sequencing — Q: "Tag timing and gate handling?" → Selected: "Tag at execution start after 24.5 passes" (recommended default)`

**Notes:** Deviation from Phase 24's tag-at-discuss precedent is deliberate: Phase 24.5 commits will land between now and Phase 25 start; tagging now would not capture the true pre-phase state. READY-WITH-CAVEATS = pass, with caveats propagated into affected packets.

---

## Claude's Discretion

- Packet filenames for non-letter-number ledger IDs (`SCS`, `D=6.694`, `footer`, `mass-drift`, …) — sanitized, mapping recorded in `evidence/README.md`.
- Template/README wording and section ordering within the locked section set.
- Three separate EVID-10 packets vs packets-plus-summary, provided each conflict has a complete citable record.

## Deferred Ideas

- Spec edits (Phases 26–28); per-finding packets for non-conflict findings (owning phases); AC numeric criteria + execution (VER-07/Phase 29); ledger linter (v1.4 deferral stands); doc-03 items (SCOPE-11).
- **Reviewed todo, not folded:** "PH-1 ML-framework research handoff" (score 0.6, keyword false-positive on "framework") — parallel training-execution stream, outside issue-02 adjudication. Deliberate deviation from the auto-fold ≥0.4 rule, recorded for audit.
