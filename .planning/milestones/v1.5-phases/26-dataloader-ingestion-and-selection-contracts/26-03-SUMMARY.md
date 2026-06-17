---
phase: 26-dataloader-ingestion-and-selection-contracts
plan: 03
subsystem: framework-specs / data-pipeline contracts
tags: [PIPE-06, D7, footer-heterogeneity, param_provenance, ctl_instruction, adjudication]
requires: ["26-01 (Step-1A admission gate)", "26-02 (Step-1 item-7 ID-resolution)"]
provides: ["PIPE-06 footer/parameter-heterogeneity contract", "AC-PIPE-06 definition + passing probe", "D7 VERIFIED"]
affects: ["Phase 27 Q-B2/Q-B3 (shared footer evidence base)", "Phase 29 VER-09 acceptance suite"]
tech_stack:
  added: []
  patterns: ["packet-before-edit", "candidate-text transcription (D-01)", "per-field provenance map", "OI caveat propagation (D-13)"]
key_files:
  created:
    - .planning/phases/25-evidence-framework-and-issue-ledger/evidence/d7-footer-heterogeneity.md
    - .planning/phases/26-dataloader-ingestion-and-selection-contracts/probes/outputs/ac-pipe-06_data04_footers.stdout.txt
  modified:
    - pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
    - .planning/phases/25-evidence-framework-and-issue-ledger/evidence/README.md
    - .planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md
decisions:
  - "D7 verdict accept-resolution: all-or-nothing footer contract transcribed from 02-resolution-doc.md §3.5 Q-A5:315-341"
  - "OI-12 slip excluded; corrected decomposition 1,754@1e-13 + 592@1e-14 = 2,346 with-footer cited"
  - "OI-9 hier-base supersession (1,550→1,480 no-footer) propagated; resolution-doc 3,307/1,550 targets are pre-rerun stale"
metrics:
  duration: "~25 min"
  completed: 2026-06-13
  tasks: 3
  files: 5
---

# Phase 26 Plan 03: Footer / Parameter-Heterogeneity Contract (PIPE-06 / D7) Summary

PIPE-06 footer/parameter-heterogeneity contract locked into `ctl_instruction.md` (all-or-nothing footer model with folder-default fallback, per-field `param_provenance`, `dt_out` measured-median cross-check, and footer-as-metadata-only), D7 adjudicated `accept-resolution` and VERIFIED via a passing AC-PIPE-06 footer-presence probe — completing the four-finding autonomous chain (B-06, B-11, M11, D7).

## What was done

1. **D7 evidence packet** (`evidence/d7-footer-heterogeneity.md`) — 12-section packet, both primary sources cited with line ranges (`02-resolution-doc.md §3.5 Q-A5:294-343`; issue doc `:68,85,291,301,345`), §3b dataset evidence (CLM-07:22, CLM-08:23, CLM-09:24, CLM-05b:20, CLM-06:21). Verdict `accept-resolution`. Not EVID-10 (sources agree on the contract mechanism; the issue doc's "minimal footer" premise is corrected by CLM-07, not in conflict). README ID→filename map row added.

2. **`ctl_instruction.md` edits (the contract):**
   - **Step 1 item 3 (replacement):** footer OPTIONAL + metadata-only; present → full schema, provenance `direct`; absent → folder defaults (std base tol=1e-13/Lw=118/dt_out=0.17; hier base 1e-15/130/0.08; gold both 1e-13/130/0.01), provenance `inferred`; `eta` null/`absent` (no fabrication); partial-schema → `footer_anomalous=true` + default fallback; independent `dt_out` median-spacing measurement (provenance `measured`) with >1% warn; footers NEVER a completeness signal (defers to Step-1A clause 4) or mapping source (defers to Step-1 item 7).
   - **§2.6 amendment:** `param_provenance` map over `{brutus_tolerance, word_length, dt_out, eta}` ∈ `{direct, inferred, absent, measured}`; `trustworthy_horizon` marked RESERVED (OI-4; writers null, readers forbidden).

3. **AC-PIPE-06 executed (PASS)** — `data04_footers.py` over 15,028 files; output captured at `probes/outputs/ac-pipe-06_data04_footers.stdout.txt`. std-base 2,048/701 ✓, std-gold 2,346/219 with tol `{1e-13:1754, 1e-14:592}` ✓ (corrected decomposition), hier-gold 4,857/0 ✓, hier-base 3,377/1,480 (OI-9 post-rerun state ✓). Spec-consistency grep PASS. AC-PIPE-01 regression re-check PASS (Step-1A clause 4 intact; B-06 stays VERIFIED).

4. **Ledger transition** — `24-ISSUE-LEDGER.md` D7 row PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED; status table + per-finding subsection updated in the same commit (D-08).

## Deviations from Plan

None — plan executed as written. The one numeric tension encountered (resolution-doc part-5 target `3,307/1,550` for hier-base vs probe `3,377/1,480`) was resolved as a **grounded OI-9 supersession**, not a gap: `24-DATA05-RERUN-REMEDIATION.md:130-134` explicitly documents the 70-file rerun shifting these counts and flags the 1,550/3,307 figures as stale. No source-silent decision was invented; no STOP gap was raised.

## TDD Gate Compliance

N/A — spec-adjudication phase, no code/test cycle.

## Threat Flags

None. T-26-09 (OI-12 slip), T-26-10 (fabricated eta), T-26-11 (F-1 table untouched), T-26-13 (footer-as-completeness) all mitigated as planned; perimeter clean.

## Phase-27 boundary

Footer evidence base is shared with Phase 27 Q-B2/Q-B3 (mass-drift + precision). D7 contract kept strictly data-side (parsing/provenance/metadata); no collision with Phase 27 footer/precision candidate text found.
