# Milestone v1.5 — Project Summary

**Generated:** 2026-06-17
**Purpose:** Team onboarding and project review
**Milestone:** v1.5 Resolving 02 Data Pipeline and Validation
**Branch:** `milestone/v1.5` (cut from master HEAD `b8b39a4`)
**Audit Verdict (2026-06-17):** `tech_debt` — 36/36 requirements satisfied, 8/8 phases complete, G1–G8 closure gate PASS, 0 open gaps. Three non-blocking tech-debt items documented for the user/orchestrator before the `--no-ff` merge.

---

## 1. Project Overview

### What This Is

A research project that generates high-precision three-body gravitational simulation data using the Brutus N-body integrator (C++, arbitrary precision) and uses that data to fine-tune a language model (Qwen 3.5 2B) so it can predict three-body trajectories numerically from initial conditions. The project spans the full pipeline: simulation data generation → PINN training data curation → framework-spec authoring → (future) LLM training.

### v1.5 Goal

Critically examine each finding in `pinn_instruction/issues/02-data-pipeline-and-validation.md`; verify every claim empirically against the on-disk dataset; adjudicate against the user-produced external resolution doc; apply evidence-backed edits limited to `ctl_instruction.md` and `pinn_architecture.md`; verify each fix with disposable acceptance probes.

### What v1.5 Delivered

- **A consolidated, citable resolution doc** for issue 02 (820 lines, 157,460 bytes) — the candidate verdict source for all 19 issue-02 findings
- **An empirical-verification pass** over 19 issue-02 findings against the on-disk dataset (12/12 acceptance checks PASS, 70/70 DATA-05 mass-drift rerun validated)
- **An evidence-packet + ledger protocol** (`24-ISSUE-LEDGER.md` as canonical verification artifact, 11-field gap register schema with math/engineering grounding required)
- **Eight framework-spec edits** to `ctl_instruction.md` (admission gate, ID resolution, blacklist-exclusion, gold-counterpart, footer, parameter provenance, HDF5 format, points-per-trajectory, mass-encoding, energy-normalization, conservation gate, sampling density, interpolation residual)
- **A re-verified v1.5 contract suite** (13 acceptance checks; 12 PASS + AC-VAL-04 split; 18 VERIFIED + 1 DEFERRED in the ledger)
- **A milestone handoff + code-divergence record** feeding FUT-01 (gold promotion FO-1, PSC numeric FO-2)

### Where v1.5 Stops

- **No `pinn/` code edits** (FUT-01 owns the rewrite; v1.3-era live code is NOT a grounding source)
- **No edits to `sampling_method.md`** (frozen-by-default, SCOPE-08; this milestone records the historical record of how existing data was produced)
- **No edits to `data_quality_assessment.md`** (read-only research report, SCOPE-09)
- **No data regeneration** beyond the 70-file DATA-05 forensic rerun (gold counterpart re-simulations of 184 IDs are FUT-01 FO-1)

---

## 2. Architecture & Technical Decisions

### Governance Decisions (user directives that frame v1.5)

| Decision | Description | Why | Phase |
|----------|-------------|-----|-------|
| **STOP protocol active** | For every semantic, process-schema, or cross-phase reframing decision where source materials are silent/ambiguous, the agent stops, records a gap with 11 fields (including math/engineering grounding), and surfaces to user. | User does not trust the agent to make spec-engineering or physics-adjudication calls without explicit grounding. Cost of asking is small; cost of silently inventing is irreparable spec drift. | 23, 24, 25, 26, 27, 28, 29 |
| **Spec-edit perimeter** | Only `ctl_instruction.md` and `pinn_architecture.md` may be edited. `sampling_method.md` is frozen (SCOPE-08), `data_quality_assessment.md` is read-only (SCOPE-09). | v1.5 is an adjudication milestone; it produces authoritative spec text, not code or new sampling. | 23+ |
| **`pinn/` live code banned as grounding** | v1.3-era `data-processing-pipeline-full.py` / `basic_architecture.py` are NOT evidence or source-of-truth. Forward-pointing references only in `NN-CODE-DIVERGENCE.md` / `pinn/STATUS.md`. | Live code is what v1.5 is helping to revise. Treating it as a spec would freeze the very thing under review. | 23+ |
| **Issue-02 resolution doc as candidate verdict source** | The user-produced `02-resolution-doc.md` (820 lines) is the *candidate* verdict source — agent transcribes what is explicit, never fills white space. | Same trust calibration as the STOP protocol; user owns the authoritative interpretation. | 24.5 |
| **SCOPE-05 narrow carveout** | `simulation_data/Scripts/ic_generation/` is permitted grounding for `sampling_method.md` data-generation specs. | Required to verify the existing training data is trainable against the new spec text. | 23 |

### Process / Tooling Decisions

| Decision | Description | Why | Phase |
|----------|-------------|-----|-------|
| **Per-phase preflight tag** | Tag `v1.5-pre-phase-NN` from branch HEAD before each phase begins (D-10 GUARD discipline). | Recovery point for any destructive operation; audit-trail of phase boundaries. | 25, 26, 27, 28, 29 |
| **`scripts/agent-commit` wrapper** | All atomic commits go through the wrapper; agents set `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS`; explicit-path staging only. | Concurrent-sessions safety; ownership prevents agent races. | all |
| **24-ISSUE-LEDGER.md as canonical verification artifact** | The 19-row ledger (PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED) is the verification record. Per-phase VERIFICATION.md is optional for v1.5 adjudication phases. | Ledger is the single source of truth that all 8 phases share; a per-phase VERIFICATION duplicates the same evidence 8 times. | 24, 25, 29 |
| **Issue-02 evidence packet template** | `evidence/{id}.md` with `## Verdict` section; verdict enum `accept-resolution` / `accept-third-position` / `BLOCKING STANDS`. Thin-pointer packets allowed for findings whose verdict predates the packet system (GAP-27-01). | Audit trail for adjudication; later phases can re-derive the verdict. | 25, 27 |
| **Two-stage external research pipeline** | Stage 1: generic prompt + self-contained research package → 8 independent research agents. Stage 2: 8 reports (anonymized R1–R8) + package → 1 consolidation agent. | Reduces anchoring; reproducibility; byte-verifiable; explicit. | 23 |
| **Phase 24.5 inserted** | Lightweight readiness gate that verifies the resolution doc is *fit for adjudication* before Phases 25–29 commit to it. | v1.4 retrospective insight: a missing gate let consolidation defects propagate into 5 phases of adjudication work. | 24.5 |
| **PENDING + Verdict convention** | Verdict + Evidence-Packet fields filled, Status kept `PENDING`; "adjudicated-but-unfixed". | Preserves the state machine; lets Phase 25 own records while 26-28 own the fixes. | 25 (GAP-25-01) |

### Adjudication Decisions (resolved gaps)

| Gap | Decision | Why | Phase |
|-----|----------|-----|-------|
| **GAP-23-01** | R6 crosswalk non-mechanical mappings: lock crosswalk vocabulary at plan-authoring time (not execution). | 30-min detour cost; future Issue-03 prep benefit. | 23 |
| **GAP-24-01** | DATA-05 mass-drift baseline: current ICs are canonical; 70 old base-hier outputs are invalid/stale; rerun them. | Mass-drift is real (0.0056% on 4-bit tolerance), not a Decimal precision artifact. | 24 |
| **GAP-25-01** | Phase-scope split: Phase 25 = machinery + 3 known EVID-10 records (SCS, D=6.694, M11/M12); Phases 26-28 author remaining packets immediately before their edits. | Avoids 19 packets authored in Phase 25 that 26-28 would then need to update. | 25 |
| **GAP-26-01** | M13 gold-counterpart fallback (OI-7a): Stage-5 labels attach to *IDs* (not simulations); the 184 gold-less standard IDs are real Stage-5 holes, resolved by **re-simulating their gold counterparts 1:1** (OI-7b activated). | Per-ID `gold_counterpart ∈ {present, absent}`; no base→gold substitution; no silent skip. Forward dep: 184 re-simulations (data generation, OI-7b) are pending → FUT-01. | 26 |
| **GAP-27-01** | PIPE-07 evidence-packet: thin-pointer pattern (template-compliant packet that cites the Phase 24 verdict source without re-deriving). | EVID-06 packet-before-edit gate must be honored; verdict predates the packet system. | 27 |
| **GAP-27-02** | PIPE-09 `compute_globals` admitted-set scope: per-IC energies evaluated with raw masses over the admitted set after Step-1A admission, blacklist exclusion, and DATA-05 quarantine. | User follow-up approved as Option A; the "flagged for spec-author sign-off" caveat does not survive into normative spec text. | 27 |
| **GAP-28-03** | PSC composition ratified; constants remain provisional → FUT-01 FO-2. AC-VAL-04 split: STRUCTURAL PASS / NUMERIC DEFERRED. | Composition is well-defined; the empirical numeric calibration requires training-side data the v1.5 milestone did not produce. | 28 |
| **GAP-29-01** | FO-1 Option A: no gold promotion during v1.5; gold stays at 2,565, base at 2,749, 184 gold missing. Re-run 184 in FUT-01. | v1.5 is an adjudication milestone, not a data-generation milestone. FO-1 carries the work forward. | 29 |
| **D-08 SI-PINN-002** | Preserve-with-reason (not retired-by-M12). User explicitly approved preserve-with-written-reason 2026-06-17. | Source-silent; agent must not silently fold records. | 29 |

---

## 3. Phases Delivered

| # | Phase | Status | Plans | One-Liner |
|---|-------|--------|-------|-----------|
| **23** | Research Package Assembly | complete (5/5) | 5 | DQA characterization, 13-row CLM claims register, consolidation plan with user-approved document list, external-research + consolidation agent prompts, package directory + SHA-256 self-test |
| **24** | Empirical Dataset Verification & Correction Addendum | complete (4/4, 12/12 UAT) | 4 | 19/19 finding seeding in 24-ISSUE-LEDGER.md, 24-VERIFIED-FACTS.md, DATA-05 70/70 mass-drift rerun validated, DATA-07 addendum (4 new findings: footer, mass-drift, D-08 SI, D-04 hierarchical split) |
| **24.5** | Resolution Doc Readiness Verification | complete (1/1) | 1 | READY-WITH-CAVEATS gate; 19/19 finding coverage; 0 contradictions; 0 HC violations; resolution doc 820 lines / 157,460 bytes; Phases 25-29 unblocked |
| **25** | Evidence Framework & Issue Ledger | complete (2/2) | 2 | Evidence-packet template + verdict enum, 24-ISSUE-LEDGER.md operating protocol, 3 known EVID-10 records authored (SCS, D=6.694, M11/M12), ledger wiring live, D-12 close-with-parent discipline, D-09 + D-10 GUARD discipline honored |
| **26** | DataLoader Ingestion & Selection Contracts | complete (5/5) | 5 | 6 PIPE contracts landed in ctl_instruction.md (admission gate, ID resolution, blacklist-exclusion, gold-counterpart, footer/param_provenance, HDF5), 10/10 in-scope ledger rows VERIFIED, M13 user-ruled Option B (per-ID stage labels, re-simulate 184) |
| **27** | Sampling, Precision & Global-Scale Contracts | complete (4/4) | 4 | Full-suite re-run 2026-06-14: AC-PIPE-04/07/08/09 + regression AC-PIPE-01/06/10 all PASS; M12/G5/mass-drift/footer/D=6.694 all VERIFIED; `compute_globals` admitted-set scope signed off; PIPE-07 thin-pointer packet precedent set |
| **28** | Validation-Metrics Contracts | complete (4/4) | 4 | SCS/SASD/IPR VERIFIED (Plans 01-03); VAL-04/PSC GAP-28-03 reopened+RESOLVED 2026-06-17 (composition ratified; constants provisional→FUT-01); AC-VAL-04 numeric DEFERRED to FUT-01 FO-2 |
| **29** | Acceptance Checks, Re-verification & Handoff | complete (2/2) | 2 | 13-check AC suite (12 PASS + AC-VAL-04 split); 18 VERIFIED + 1 DEFERRED ledger audit; 36/36 traceability; 3 SI dispositions; G1–G8 closure gate re-executed fresh 2026-06-17; 29-HANDOFF.md (7 sections) + 29-CODE-DIVERGENCE.md (FO-1 + FO-2) |

**Total:** 8 phases, 28 plans, 36/36 requirements satisfied, 0 open gaps.

---

## 4. Requirements Coverage

**Score: 36/36 satisfied** (3-source cross-reference: VERIFICATION × SUMMARY frontmatter × REQUIREMENTS.md traceability table).

| Req-Group | Count | Phase(s) | Status | Notes |
|-----------|-------|----------|--------|-------|
| **PKG-01..04** | 4 | 23 | ✅ satisfied | DQA characterization, CLM register, consolidation plan, package |
| **DATA-01..07** | 7 | 24 | ✅ satisfied | 12/12 acceptance checks PASS; DATA-05 70/70 rerun |
| **EVID-06..10, VER-10** | 5 | 25 | ✅ satisfied (label stale) | Machinery + 3 EVID-10 records; REQUIREMENTS.md row says "Pending (gated on Phase 24.5)" — bookkeeping only |
| **PIPE-01..03, 05, 06, 10** | 6 | 26 | ✅ satisfied | 5/5 must-haves VERIFIED |
| **PIPE-04, 07, 08, 09** | 4 | 27 | ✅ satisfied (label stale) | Full-suite re-run 2026-06-14 PASS; REQUIREMENTS.md row says "Pending (gated on Phase 24.5)" — bookkeeping only |
| **VAL-01..04** | 4 | 28 | ✅ satisfied | SCS/SASD/IPR/PSC composed; AC-VAL-04 numeric DEFERRED to FUT-01 FO-2 |
| **VER-07, 08, 09, 11, 12** | 5 | 29 | ✅ satisfied (upper-section stale) | 13-check AC suite PASS; REQUIREMENTS.md lines 67-72 checkboxes still `[ ]` — bookkeeping only |
| **VER-10** | 1 | 25 | ✅ satisfied | (counted with EVID-06..10 above) |

**Audit Verdict (`.planning/v1.5-MILESTONE-AUDIT.md`):** `tech_debt` — no critical blockers, 8/8 phases complete, G1–G8 milestone-closure gate PASS 2026-06-17, 0 open gaps, 10/10 gaps RESOLVED-WITH-INSTRUCTION.

**Orphan detection:** None. All 36 requirements appear in exactly one phase per the traceability table. Coverage block: 4+7+0+6+6+4+4+5=36.

---

## 5. Key Decisions Log

The full gap index is in `.planning/milestones/v1.5-GAPS.md` (10 gaps, 0 open, 10 RESOLVED-WITH-INSTRUCTION). The complete key-decisions log is in each phase's `CONTEXT.md` and `*-GAPS.md`. This summary lists the most consequential decisions:

| ID | Phase | Decision | Impact |
|----|-------|----------|--------|
| **GAP-23-01** | 23 | Lock crosswalk vocabulary at plan-authoring time | Process; ~30-min detour cost once; ~30 min saved on next milestone |
| **GAP-24-01** | 24 | DATA-05 mass-drift: current ICs canonical; 70 invalid base-hier outputs quarantined and rerun | Data-integrity; 70/70 rerun PASS; 0/4857 post-swap mismatches |
| **D-04** | 24 | Hierarchical split: 4,857 hierarchical Brutus outputs ≠ 2,749 standard base | Closes CLM-05 false-equivalence; affects PIPE-04 (M12) |
| **D-09, D-10** | 25 | GUARD discipline: no fresh evidence after phase EXIT, no commit between EXIT and preflight tag | Process; audit-trail integrity |
| **D-12** | 25 | Close-with-parent for G1-G5: G-rows close when their constituent finding closes | State machine preserved verbatim; avoids duplicate packets |
| **GAP-25-01** | 25 | Phase-scope split: Phase 25 = machinery, 26-28 author packets immediately before edits | Plan-task structure; avoids packet churn across phases |
| **D-02** | 25 | M12 LOCKED: `n_pts = min(cap, n_snapshots)`; BLOCKING-infeasibility claim rejected; P1-4 0.5× factor rejected | Spec; affects PIPE-04 AC and `pinn_architecture.md §3.1` code default |
| **D-08** | 25, 29 | SI metadata as forward record (not spec edit) | Avoids silent retirement; SI-PINN-002 preserved-with-reason by user |
| **D-07** | 25 | G1-G5 rendered as separate rows; each G-row's AC is the corresponding PIPE-0X AC (synthesis view) | Avoids duplicate contract work |
| **GAP-26-01** | 26 | M13 Option B: Stage-5 labels attach to IDs; re-simulate 184 gold counterparts 1:1 | Spec; OI-7b activated; forward dep on data generation |
| **D-11** | 26 | Lifecycle Rules block: state machine preserved verbatim; only stale v1.4 applicability text updated | Process; per D-11 KEEP-VERBATIM list |
| **GAP-27-01** | 27 | PIPE-07 thin-pointer packet (template-compliant, cites Phase 24 verdict) | Process-schema; precedent for non-conflict findings |
| **GAP-27-02** | 27 | PIPE-09 `compute_globals` admitted-set scope: per-IC energies with raw masses over admitted set | Spec; locks convention for `ctl §2.5` |
| **GAP-28-03** | 28 | PSC composition ratified; constants provisional; AC-VAL-04 split (STRUCTURAL PASS / NUMERIC DEFERRED) | Spec; FO-2 carries numeric work to FUT-01 |
| **GAP-29-01** | 29 | FO-1 Option A: no gold promotion during v1.5; gold stays 2,565; 184 missing; re-run in FUT-01 | Data generation deferred; preserves v1.5 scope |
| **D-08 SI-PINN-002** | 29 | Preserve-with-reason (not retired-by-M12); user explicit 2026-06-17 | Audit-trail; prevents silent fold-in |

---

## 6. Tech Debt & Deferred Items

### Non-Blocking Tech Debt (per `.planning/v1.5-MILESTONE-AUDIT.md`)

| Item | Severity | Location | Recommended Action |
|------|----------|----------|--------------------|
| **FO-1 durability** | WARNING | `simulation_data/Scripts/brutus_runners/rerun_standard_gold_missing_184.py` + its test remain **untracked on disk** | Commit before FUT-01 gate; 29-CODE-DIVERGENCE.md FO-1 flags as "do NOW" interim action |
| **Stale REQUIREMENTS.md checkboxes** | INFO | `.planning/REQUIREMENTS.md` lines 67-72 (VER-07..12 still `[ ]`); ROADMAP.md Phase 29 bullet at line 77 still `[ ]` | 29-VERIFICATION "Reconciliation Recommendation" warrants the flip; defers to user because REQUIREMENTS.md was outside plan owned-paths |
| **Working-tree STATE.md rollback** | INFO | `.planning/STATE.md` (uncommitted) reads `status: verifying`; committed `d558e1a6` correctly reads `closure-ready` | Uncommitted artifact, not committed-state defect. Either commit current (if rollback is correct) or restore from `d558e1a6` (if committed is correct). User judgment. |
| **4/8 phases lack phase-level VERIFICATION.md** (24, 25, 27, 28) | DESIGN | per-phase directories | Treated as design choice consistent with v1.4/v1.5 adjudication model; the 19-row 24-ISSUE-LEDGER.md is the canonical verification artifact. Phase 29 G3 enumerates 18 VERIFIED + 1 DEFERRED. |
| **Nyquist compliance is PARTIAL** by frontmatter | DESIGN | per-phase frontmatter | Frontmatter reflects planning-time state; behavior is verified via Phase 29 G1–G8 closure gate + per-phase ledger audits. |

### Deferred to FUT-01 (per `29-CODE-DIVERGENCE.md` and `29-HANDOFF.md`)

| # | Item | Deferred From | Documented In |
|---|------|---------------|---------------|
| 1 | **PSC numeric calibration + AC-VAL-04 numeric run** (FO-2) | Phase 28 (VAL-04) | 29-CODE-DIVERGENCE.md FO-2; 29-HANDOFF.md §3 Deferred; PSC ledger row stays DEFERRED |
| 2 | **Gold promotion (117 reruns) + 184→67 cascade** (FO-1) | Phase 26 (M13) | 29-CODE-DIVERGENCE.md FO-1; GAP-29-01 RESOLVED-WITH-INSTRUCTION Option A |
| 3 | **doc-03 training-side metric contracts** (M16, SCS/SASD/IPR/PSC training-side) | Phase 28 | 29-HANDOFF.md §3 Deferred; future doc-03 milestone |

### Lessons Learned (per `.planning/milestones/v1.5-LESSONS-LEARNED.md`)

Six themes for the next milestone (v1.6 / Issue-03):

1. **The two-stage external-research pipeline is reproducible** — 4-file bundle, R-anonymization, in-prompt crosswalk, 3-pass Method (consistency / completeness / output-contract conformance) all worked. Lock crosswalk vocabulary at plan-authoring time, not execution time.
2. **Mechanical work is a first-class deliverable** — `make_bundles.py` with SHA-256 self-verification, BUNDLE-MANIFEST with self-ID scan, forensic quarantine pattern (`simulation_data/Data/forensic/`) each required design attention. The byte-verbatim guarantee eliminated an entire class of "did the upload corrupt?" questions.
3. **STOP protocol + gap registers worked as designed, but both gaps that fired were planning-time gaps caught at execution time** — GAP-23-01 and GAP-24-01 surfaced during consolidation/packaging, not planning. Pre-emptive scans during the discuss phase would have caught them earlier. The 11-field gap register schema (including math/engineering grounding) forced the agent to demonstrate *why* each gap was consequential.
4. **Commit hygiene and concurrent-sessions awareness are mandatory infrastructure** — `scripts/agent-commit` wrapper, `Agent-Assisted-By` trailer, atomic-commit discipline kept a 24-commit Phase 23-24 trace re-derivable. The concurrent-sessions commit race is now in MEMORY.md; mitigation is `git status --short --branch` + `git log --oneline -5` at session start.
5. **Tooling decisions compound across phases** — `ctx_batch_execute` with concurrency 4, claude-mem's 3-layer workflow, parallel `Explore` subagents for read-only crosswalk verification (8 columns in ~5 min instead of ~30 min).
6. **Insert a resolution-doc readiness-verification phase before adjudication** — the Stage-2 consolidation agent produces the candidate verdict source, but a lightweight Phase-24.5-style gate verifies it is *fit for adjudication* before Phases 25-29 commit. This was the single biggest v1.5 improvement over v1.4.

---

## 7. Getting Started

### Repository Layout (v1.5-relevant)

```
3_body_problem/
├── pinn_instruction/
│   ├── issues/02-data-pipeline-and-validation.md          # Issue doc (non-authoritative; some claims suspect)
│   ├── markdown_conversion/
│   │   ├── framework-specs/                               # Spec-edit perimeter
│   │   │   ├── ctl_instruction.md                         # EDITED in v1.5 (8 contracts landed)
│   │   │   ├── pinn_architecture.md                       # NOT edited in v1.5 (in-scope, deferred to FUT-01 if any)
│   │   │   ├── sampling_method.md                         # FROZEN (SCOPE-08)
│   │   │   └── data_quality_assessment.md                 # READ-ONLY (SCOPE-09)
│   │   └── framework-revisions/research_reports/02-data-pipeline-and-validation/
│   │       └── ctl_pinn_resolution.md                     # User-produced candidate verdict source (820 lines)
├── simulation_data/                                       # On-disk dataset + scripts (SCOPE-05 carveout)
│   ├── Data/                                              # Brutus outputs (base + gold)
│   ├── Documentation/                                     # Dataset README, blacklists, ID lists
│   ├── Scripts/                                           # ic_generation/, metrics_calculation/, Validation/, brutus_runners/
│   └── Data/forensic/data05_gap24-01_old_outputs/         # Quarantined 70 invalid base-hier outputs
├── pinn/                                                  # v1.3-era live code — NOT grounding; reference only for FUT-01
├── .planning/
│   ├── phases/                                            # 8 v1.5 phase directories
│   │   ├── 23-research-package-assembly/
│   │   ├── 24-empirical-dataset-verification-and-correction-addendum/
│   │   │   ├── 24-ISSUE-LEDGER.md                         # Canonical verification artifact (19 rows)
│   │   │   └── 24-VERIFIED-FACTS.md                       # Dataset-evidence annex (D-23)
│   │   ├── 24.5-resolution-doc-readiness-verification/
│   │   ├── 25-evidence-framework-and-issue-ledger/
│   │   │   └── evidence/                                  # 11 evidence packets
│   │   ├── 26-dataloader-ingestion-and-selection-contracts/
│   │   ├── 27-sampling-precision-and-global-scale-contracts/
│   │   ├── 28-validation-metrics-contracts/
│   │   └── 29-acceptance-checks-re-verification-and-handoff/
│   │       ├── 29-HANDOFF.md                              # Milestone handoff (7 sections)
│   │       ├── 29-CODE-DIVERGENCE.md                      # FUT-01 forward obligations (FO-1, FO-2)
│   │       └── 29-ACCEPTANCE-EVIDENCE-2026-06-17.md       # Fresh 13-check AC run
│   ├── milestones/
│   │   ├── v1.5-GAPS.md                                   # Milestone-wide gap index (10/10 RESOLVED)
│   │   └── v1.5-LESSONS-LEARNED.md                        # Meta-workflow retrospective (6 themes)
│   ├── v1.5-MILESTONE-AUDIT.md                            # Audit report (verdict: tech_debt)
│   ├── STATE.md                                           # Current project state
│   ├── ROADMAP.md                                         # Phase 23-29 defined
│   ├── REQUIREMENTS.md                                    # 36 requirements
│   └── PROJECT.md                                         # Project narrative
├── docs/                                                  # Lifecycle-managed project docs (runbooks, plans, reviews, designs)
├── tools/spec-render-check/                               # Spec-render detector suite
├── brutus_Newton-main/                                    # C++ N-body integrator (untouched)
└── reference-code/                                        # Lyapunov + NN baselines
```

### Where to Look First (by role)

- **New to the project?** Start with `.planning/PROJECT.md` (project narrative) and `.planning/STATE.md` (current position). Then skim `.planning/RETROSPECTIVE.md` for v1.0/v1.4 lessons.
- **Auditing v1.5?** Read `.planning/v1.5-MILESTONE-AUDIT.md` (the audit report). Then cross-check `.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md` against the ledger and audit verdict.
- **Implementing FUT-01?** Read `.planning/phases/29-acceptance-checks-re-verification-and-handoff/29-HANDOFF.md` (consumption notes), then `29-CODE-DIVERGENCE.md` (FO-1 gold promotion, FO-2 PSC numeric), then `pinn/basic_architecture.py` and `pinn/data-processing-pipeline-full.py` to compare live code against the new spec.
- **Adjudicating the next issue (Issue-03)?** Read `.planning/milestones/v1.5-LESSONS-LEARNED.md` (6 themes), then `.planning/milestones/v1.5-GAPS.md` (process example), then plan with a Phase N-1-style readiness gate before adjudication phases.
- **Tracing a specific finding?** Search `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` for the finding ID, then follow the Evidence Packet link to `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/{id}.md`, then follow the "Spec Section" pointer into `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md`.

### Common Commands

| Purpose | Command |
|---------|---------|
| Check current branch + working tree | `git status --short --branch` |
| List v1.5 phase preflight tags | `git tag -l 'v1.5-pre-*' \| sort -V` |
| See milestone gap index | `head -8 .planning/milestones/v1.5-GAPS.md` |
| See milestone audit verdict | `head -5 .planning/v1.5-MILESTONE-AUDIT.md` |
| See milestone handoff structure | `grep -E '^## (Evidence Used\|1\. Fixed\|2\. Intentionally Unchanged\|3\. Deferred\|4\. SI\|5\. FUT-01\|6\. Milestone)' .planning/phases/29-acceptance-checks-re-verification-and-handoff/29-HANDOFF.md` |
| See FUT-01 forward obligations | `grep -E '^(FO-1\|FO-2\|## )' .planning/phases/29-acceptance-checks-re-verification-and-handoff/29-CODE-DIVERGENCE.md` |
| See v1.5 commit timeline | `git log --oneline --grep='v1.5' \| tail -10` (latest); `git log --oneline --reverse --grep='v1.5' \| head -10` (earliest) |

### Validation Evidence

- **Audit:** `.planning/v1.5-MILESTONE-AUDIT.md` — `tech_debt` verdict, 36/36 requirements, 8/8 phases, G1–G8 PASS
- **Acceptance:** `.planning/phases/29-acceptance-checks-re-verification-and-handoff/29-ACCEPTANCE-EVIDENCE-2026-06-17.md` — fresh 13-check AC run, 12 PASS + 1 split
- **Ledger:** `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` — 19 rows, 18 VERIFIED + 1 DEFERRED (PSC), 0 PENDING/IN_PROGRESS/FIX_APPLIED

---

## Stats

- **Milestone:** v1.5 Resolving 02 Data Pipeline and Validation
- **Branch:** `milestone/v1.5` (cut from master HEAD `b8b39a4`)
- **Timeline:** 2026-06-06 → 2026-06-17 (~11 days; 366 commits since 2026-06-01)
- **Phases:** 8 / 8 complete (23, 24, 24.5, 25, 26, 27, 28, 29)
- **Plans:** 28 / 28 complete
- **Requirements:** 36 / 36 satisfied (4 PKG + 7 DATA + 5 EVID + 10 PIPE + 4 VAL + 6 VER)
- **Gaps:** 10 / 10 RESOLVED-WITH-INSTRUCTION, 0 open, 0 deferred
- **Commits:** 366 (since 2026-06-01, includes pre-milestone planning commits); milestone-body commits cover Phases 23-29
- **Files changed (full repo since v1.5 start):** 399 files, +160,822 / -11,081 (this includes pre-milestone planning, the data-05 forensic quarantine, and the docs-update pass)
- **Contributors:** 1 (Starlordpd233)
- **Acceptance suite:** 13 ACs, 12 PASS + 1 split (AC-VAL-04 STRUCTURAL PASS / NUMERIC DEFERRED)
- **Closure gate:** G1–G8 PASS 2026-06-17
- **Audit verdict:** `tech_debt` (3 non-blocking items; `--no-ff` merge unblocked)
- **Forward work:** FUT-01 (gold promotion FO-1; PSC numeric FO-2); future doc-03 milestone (training-side metrics)

---

## Operator Next Steps

The v1.5 milestone is **closure-ready**. The user-owned final step is the `--no-ff` merge of `milestone/v1.5` → `master`. Before the merge, address (or accept) the 3 tech-debt items:

1. **Commit `rerun_standard_gold_missing_184.py` + its test** (FO-1 durability, WARNING)
2. **Flip the stale `REQUIREMENTS.md` and `ROADMAP.md` checkboxes** (VER-07..12 and Phase 29 bullet)
3. **Resolve the working-tree `STATE.md` rollback** (commit or restore from `d558e1a6`)

After the merge, `/gsd-complete-milestone v1.5` to archive this milestone (v1.5-ROADMAP.md / v1.5-REQUIREMENTS.md / v1.5-MILESTONE-AUDIT.md) and start `/gsd-new-milestone` for v1.6 / Issue-03.
