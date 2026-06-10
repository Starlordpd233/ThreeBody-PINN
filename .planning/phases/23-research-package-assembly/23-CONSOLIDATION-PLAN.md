# Phase 23: Document-List & Consolidation Plan

**Purpose:** This document enumerates the candidate research-package deliverables, classifies each as consolidated or standalone, and states the two open inclusion decisions for the D-07 user checkpoint. It will be surfaced verbatim at the D-07 gate (Plan 02). No package directory is created in this plan — assembly is Plans 03-05, gated on Plan 02 approval.

**Prepared:** 2026-06-10
**Governance:** v1.5 STOP protocol applies. Mechanical/presentation choices noted in-artifact. Semantic or process-schema decisions that are source-silent would trigger a STOP gap; none were encountered in preparing this plan.

---

## Final Candidate Document List

| # | Document | Role annotation | Treatment | Recommendation |
|---|----------|-----------------|-----------|----------------|
| 1 | `02-data-pipeline-and-validation.md` | Adjudication subject — NON-authoritative; may contain errors | Intact copy | Required |
| 2 | `ctl_instruction.md` | Spec-edit target; carries 14D input contract, Jacobi IC13, PHYS-01 D convention, dual-epsilon | Intact, byte-for-byte (D-03) | Required |
| 3 | `pinn_architecture.md` | Spec-edit target; carries COM projection head, PHYS-03 softening, loss contracts | Intact, byte-for-byte (D-03) | Required |
| 4 | `sampling_method.md` | FROZEN (SCOPE-08); historical record of dataset generation; not a revision target | Intact if included | RECOMMEND YES (A4) |
| 5 | `data_quality_assessment.md` | Research report, NOT authoritative spec (SCOPE-09); sole written home of post-v1.3 SCS gate + metric definitions | Intact copy if included | RECOMMEND YES (A3, informed by DQA characterization) |
| 6 | Consolidated context file (one file) | Scattered dataset facts, each fragment labeled with source path | Consolidation (D-05) | Required |

**Total deliverable files:** 6 (if both inclusion calls are YES). This triggers the consolidation rule (D-07, see below).

---

## What Is Consolidated vs Standalone

### Standalone (byte-for-byte intact snapshots — D-03)

Framework specs are NEVER consolidated (D-03). They ship as intact, byte-for-byte copies. All role/FROZEN/non-authoritative annotations live in the manifest's annotation column, never inside the copied files (this reconciles D-03 byte-for-byte with D-05 annotation).

- Documents 1-5 above: each becomes a standalone file in `research_package/specs/`.

### Consolidated (one file — D-05)

The consolidated context file holds scattered fragments from multiple sources, each fragment labeled with its source path and line range. This is the sole consolidated deliverable.

**Fragments to include:**

| Fragment | Source | Lines | Content |
|----------|--------|-------|---------|
| Dataset Sizes | `simulation_data/Documentation/README.md` | 81-90 | Standard/hierarchical/gold dataset counts and sizes |
| File Naming/Mapping | `simulation_data/Documentation/README.md` | 193-231 | ID-to-folder mapping convention, gold variant naming |
| Brutus Parameters by Variant | `simulation_data/Documentation/README.md` | 584-628 | Per-variant tolerance, dt_out, footer schema, minimal-footer count (219), tol=1e-14 count (592), hierarchical file count (~4,857) |
| Completeness Checks | `simulation_data/Documentation/README.md` | 637-660 | `final_timestep >= 9.5` gate rule; snapshot-count warning |
| Gold-gap record (full) | `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` | full file | 184 IDs excluded from gold; 2,749 base / 2,565 gold folder counts |
| Blacklist summary | `simulation_data/Documentation/problematic_ics_blacklist.json` | summary | 65 IDs = 2 hierarchical + 63 standard (derived count) |
| Metrics calculation provenance | `simulation_data/Scripts/metrics_calculation/calculate_metrics.py` | relevant excerpt (SCOPE-07) | Provenance grounding for metrics-related findings |

**Excluded from consolidation:**
- `pinn/` live code — EXCLUDED per D-06/SCOPE-10. The package explicitly states that issue-02's "Canonical" citation of `pinn/data-processing-pipeline-full.py` is overridden (directive 2026-05-19; SCOPE-10) and framework specs are the source of truth.
- Framework specs — NEVER consolidated (D-03), shipped as intact snapshots.

---

## Two Open Inclusion Calls (D-07 User Checkpoint)

These are the two decisions the D-07 checkpoint asks the user to ratify. Both are RECOMMEND YES; the final call is the user's.

### Inclusion Call 1: Ship `sampling_method.md`?

**Recommendation: YES**

- The issue-02 findings concern the dataset that `sampling_method.md` generated. External researchers need the generation methodology to adjudicate data-pipeline claims (B-06, M11, M12, G1-G5).
- It is FROZEN (SCOPE-08): the annotation in the manifest will state "FROZEN — historical record of dataset generation; not a revision target."
- Claude's discretion (A4), per CONTEXT.md.

### Inclusion Call 2: Ship `data_quality_assessment.md`?

**Recommendation: YES** (informed by the DQA characterization, D-15)

- Section 3 is the most complete existing statement of the four validation metrics (SCS/SASD/IPR/PSC) the external research must adjudicate.
- The locked post-v1.3 SCS gate (`epsilon_H > 1e-5` / `SCS > -5`) — the known seed conflict with issue-02's ratio-based thresholds — is documented only here and in the issue doc. Excluding DQA would require adjudicating SCS without the metric's canonical definition.
- It will be annotated: "research report, not authoritative spec (SCOPE-09); sole written home of the post-v1.3 SCS gate; metric definitions unverified against dataset."
- Advisory only (A3), per the DQA characterization's inclusion recommendation.

---

## Why the Consolidation Rule Fires

The candidate list is 6 deliverable files (Documents 1-6 above). PKG-01's consolidation criterion is "consolidate if >~5 files / scattered fragments." With 6 files, the rule fires.

The scattered fragments in Document 6 come from 3 distinct source paths (`README.md` sections, `standard_quasi_random_ids_not_in_gold.md`, `problematic_ics_blacklist.json`, `calculate_metrics.py` excerpt) — these are consolidated into one file rather than shipped as 4 separate fragment files, keeping the total deliverable count manageable for external researchers.

Surfacing this consolidation plan to the user before assembly is a PKG-01 requirement (D-07), not a courtesy. The user's approval at the D-07 gate locks the final document list.

---

## What This Plan Does NOT Do

- **No package directory is created.** Assembly is Plans 03-05, gated on Plan 02 approval.
- **No snapshots are taken.** Byte-for-byte copies happen during assembly.
- **No empirical probes are run.** All figures remain at their CLM-registered status (`claimed-unverified` or `verified`); Phase 24 performs empirical verification.
- **No framework specs are edited.** Spec-edit work happens in Phases 26-28, gated on the resolution doc and Phase 24.
- **No `data_quality_assessment.md` edits.** SCOPE-09 read-only; the DQA characterization (23-DQA-CHARACTERIZATION.md) is the phase artifact, not the source file.

---

*This document is surfaced at the D-07 user checkpoint (Plan 02). The user's decision on the two inclusion calls locks the final package contents for assembly.*

---

## D-07 APPROVED Record

**Date:** 2026-06-10
**Decision authority:** User (Starlordpd233)
**Status:** APPROVED

### Approved Document List (6 files)

| # | Document | Role annotation | Treatment |
|---|----------|-----------------|-----------|
| 1 | `02-data-pipeline-and-validation.md` | NON-authoritative; adjudication subject | Intact copy |
| 2 | `ctl_instruction.md` | Spec-edit target; D-03 byte-for-byte | Intact snapshot |
| 3 | `pinn_architecture.md` | Spec-edit target; D-03 byte-for-byte | Intact snapshot |
| 4 | `sampling_method.md` | FROZEN (SCOPE-08); historical record | Intact snapshot |
| 5 | `data_quality_assessment.md` | Research report (SCOPE-09); non-authoritative | Intact copy |
| 6 | Consolidated context file | Scattered dataset fragments, source-labeled | Consolidation (D-05) |

### Inclusion Decisions

- **Inclusion Call 1 (sampling_method.md):** APPROVED — YES, include with FROZEN annotation
- **Inclusion Call 2 (data_quality_assessment.md):** APPROVED — YES, include with research-report annotation

**Total deliverable files: 6.** Plan 03 may proceed with snapshot assembly.
