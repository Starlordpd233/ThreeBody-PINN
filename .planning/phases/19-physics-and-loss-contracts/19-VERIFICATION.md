---
phase: 19-physics-and-loss-contracts
verified: 2026-05-30T18:56:22Z
status: passed
score: 6/6 must-haves verified
overrides_applied: 0
---

# Phase 19: Physics and Loss Contracts Verification Report

**Phase Goal:** Framework specs state physically consistent scaling, derivative,
softening, energy, and loss-balancing contracts, each adjudicated against both
source documents and locked at the root cause.
**Verified:** 2026-05-30T18:56:22Z
**Status:** passed
**Re-verification:** No - initial phase-goal verification added over the existing
structural AC-PHYS record.

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | Raw-mass nondimensionalization is locked and `D=(G*T^2)^(1/3)` is retained, with the mass-fraction alternative future-only and B-02 adjudicated. | VERIFIED | `ctl_instruction.md:591` locks PHYS-01, `ctl_instruction.md:597` confines `D=(G*M_tot*T²)^(1/3)` to the future mass-fraction rewrite, `evidence/B-02.md:10` is `VERIFIED`, and the issue row is annotated at `01-architecture-and-physics-foundations.md:72`. |
| 2 | Normalized-time derivative contract is traceable, including canonical `u`, conditional `tau` chain factors, componentwise derivatives, anti-pattern warning, and synthetic trajectory. | VERIFIED | `pinn_architecture.md:843` through `pinn_architecture.md:881` define PHYS-02, and `ctl_instruction.md:988` cross-references the architecture contract without duplicating math. |
| 3 | Physics residual and energy regularizer use a matched Plummer force/potential pair, with `epsilon_train`, `epsilon_inv`, and unsoftened `s_min` separated after B-09 adjudication. | VERIFIED | `pinn_architecture.md:377` through `pinn_architecture.md:420` define the Plummer residual and causal loss; `pinn_architecture.md:511` through `pinn_architecture.md:539` define matched-Plummer energy and D-20 metadata; `ctl_instruction.md:675` through `ctl_instruction.md:695` define static Plummer `epsilon_inv` and unsoftened `s_min`; `evidence/B-09.md:10` is `VERIFIED`. |
| 4 | Energy term is a soft conservation regularizer, not HNN framing. | VERIFIED | `pinn_architecture.md:496` through `pinn_architecture.md:520` and `pinn_architecture.md:956` describe `L_E` as a soft conservation regularizer using analytic `H_ε`; negative checks for `HNN-style`, `HNN architecture`, and `Hamiltonian Neural Network` returned no active-prose matches. |
| 5 | ALM is not in the default loss; scalar-conservation-only ALM is optional P2, while dense residuals use causal weighting and optimizer phase semantics are named. | VERIFIED | `pinn_architecture.md:407` through `pinn_architecture.md:420` make causal `L_phys` the default, `pinn_architecture.md:626` through `pinn_architecture.md:685` define the total loss, warmup, optimizer semantics, and optional P2 ALM only; pseudo-ALM default negative checks passed. |
| 6 | M4 constraint-counting passage is replaced with evidence-backed reconstructive gauge-fixed IC13 validity prose after EVID-05 adjudication. | VERIFIED | `ctl_instruction.md:941` replaces the stale passage with PHYS-06 reconstructive fixed-gauge prose and Phase 17/18 cross-references; stale `13 constraints for an 8-dimensional reduced phase` check returned no matches; `evidence/M4.md:10` is `VERIFIED`. |

**Score:** 6/6 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` | PHYS-01, PHYS-03 static invariant, PHYS-06, cross-references, and CTL-side loss contract | VERIFIED | Substantive spec sections verified at lines 591, 675, 941, 988, 1266, and 1301. |
| `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` | PHYS-02/03/04/05 architecture-side contracts | VERIFIED | Substantive spec sections verified at lines 377, 496, 626, 675, 843, and 948. |
| `evidence/B-02.md`, `evidence/B-07.md`, `evidence/B-08.md`, `evidence/B-09.md`, `evidence/M4.md` | EVID-05 or uncontested evidence packets with final lifecycle status | VERIFIED | All five packets show `Current Status` = `VERIFIED` and `Current Verdict` = `accept-resolution`. |
| `.planning/phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` | VER-05 lifecycle closure and AC-PHYS reservations | VERIFIED | B-02, B-07, B-08, B-09, and M4 rows are `VERIFIED`; no in-scope Phase 19 finding remains `IN_PROGRESS` or `FIX_APPLIED`. |
| `.planning/phases/19-physics-and-loss-contracts/19-CODE-DIVERGENCE.md` | FUT-01 handoff only, not v1.4 grounding evidence | VERIFIED | Contains the required five-column schema and explicitly says live `pinn/` code is not v1.4 evidence. |

### Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| `ctl_instruction.md` | `pinn_architecture.md` | Total-loss and PHYS cross-references | WIRED | SDK key-link checks for plans 19-01 and 19-03 passed; CTL links PHYS-02 at `ctl_instruction.md:988` and loss schedule at `ctl_instruction.md:1274`. |
| `pinn_architecture.md` | `ctl_instruction.md` | Coordinated total-loss and IC contracts | WIRED | SDK key-link checks for plans 19-02 and 19-03 passed; architecture links the default total loss and shared framework contracts. |
| `19-CODE-DIVERGENCE.md` | `pinn/basic_architecture.py` and `pinn/data-processing-pipeline-full.py` | FUT-01 handoff references only | WIRED | Manual check verified `pinn/basic_architecture.py` and `pinn/data-processing-pipeline-full.py` are present only as FUT-01 handoff coordinates; SDK false-negative was caused by an escaped-pattern mismatch. |

### Data-Flow Trace

| Artifact | Data Variable | Source | Produces Real Data | Status |
|---|---|---|---|---|
| Framework specs and planning artifacts | N/A | Documentation/spec contracts | N/A | Not applicable: Phase 19 delivers Markdown framework contracts, not runtime data flow. |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| AC-PHYS structural suite remains present | `rg "PASS: AC-PHYS-01"... "PASS: AC-PHYS-06" 19-VERIFICATION.md` | All six markers present; no failure marker. | PASS |
| No `pinn/` files modified | `git diff --name-only -- pinn` and `git diff --name-only --cached -- pinn` | Both returned empty output. | PASS |
| Markdown whitespace sanity | `git diff --check` | Passed. | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|---|---|---|---|---|
| PHYS-01 | `19-01`, `19-04` | Raw-mass scaling convention and B-02 adjudication | SATISFIED | `ctl_instruction.md:591`; `evidence/B-02.md:10`; ledger B-02 row `VERIFIED`. |
| PHYS-02 | `19-02`, `19-04` | Normalized-time derivative contract | SATISFIED | `pinn_architecture.md:843`; `ctl_instruction.md:988`; AC-PHYS-02 reserved in ledger. |
| PHYS-03 | `19-01`, `19-02`, `19-04` | Matched Plummer softening and epsilon split | SATISFIED | `pinn_architecture.md:377`; `ctl_instruction.md:675`; `evidence/B-09.md:10`. |
| PHYS-04 | `19-02`, `19-03`, `19-04` | Energy as soft conservation regularizer | SATISFIED | `pinn_architecture.md:496`; `evidence/B-07.md:10`; HNN negative checks passed. |
| PHYS-05 | `19-02`, `19-03`, `19-04` | Default loss, causal residual, P2-only ALM, optimizer semantics | SATISFIED | `pinn_architecture.md:626`; `pinn_architecture.md:675`; `evidence/B-08.md:10`. |
| PHYS-06 | `19-01`, `19-04` | M4 constraint-counting replacement | SATISFIED | `ctl_instruction.md:941`; `evidence/M4.md:10`; ledger M4 row `VERIFIED`. |
| VER-05 | All Phase 19 plans | Iterative lifecycle closure through `VERIFIED` | SATISFIED | Ledger rows for B-02, B-07, B-08, B-09, and M4 are `VERIFIED`; all five packet logs have `FIX_APPLIED -> VERIFIED`. |

Lifecycle note: `.planning/REQUIREMENTS.md` still shows PHYS rows unchecked and
`.planning/ROADMAP.md` progress metadata still shows Phase 19 as in progress. The
actual files and ledger satisfy the requirements; checkbox/progress updates are a
phase-completion lifecycle step, not a Phase 19 spec-contract blocker.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---:|---|---|---|
| `ctl_instruction.md` | 690 | Additive softening text appears only inside an explicit PHYS-03 anti-pattern warning. | INFO | Not an active formula; no blocker. |
| `19-CODE-DIVERGENCE.md` | 14-26 | Live `pinn/` paths referenced. | INFO | Correct FUT-01 handoff usage; file explicitly says live code is not v1.4 evidence. |

### Human Verification Required

None. This phase is a documentation/specification contract phase; all must-haves
are verifiable through repository text, evidence packets, ledger status, and
structural grep checks. Numeric acceptance probes are explicitly Phase 21 scope.

### Gaps Summary

No blocking gaps found. `GAP-19-01` is resolved in `19-GAPS.md`, the milestone
gap index, and `19-CONTEXT.md` as `epsilon_H = 1e-4 * S_H`; Phase 21 is limited
to denominator activation reporting unless a new user-instruction gap is opened.

---

_Verified: 2026-05-30T18:56:22Z_
_Verifier: the agent (gsd-verifier)_

---

# Phase 19 Structural Verification

This file records the Phase 19 structural acceptance checks for `AC-PHYS-01` through
`AC-PHYS-06`. Phase 19 records structural criteria only; Phase 21 owns numeric pass
criteria and disposable probe execution.

Notation note: the current specs use Unicode notation in two places covered by the plan
probes (`T²` for the mass-fraction alternative and `2πu` for the synthetic trajectory).
The structural suite checked those existing notations with equivalent `rg` patterns
without editing the framework specs.

| AC ID | Command or manual check | Expected result | Actual result | Result |
|---|---|---|---|---|
| AC-PHYS-01 | `rg` checks for `Governing Mathematical Convention`, raw-mass nondimensionalization, future-rewrite-only mass-fraction alternative, `D=(G*T**2)^(1/3)`, and the alternative `D=(G*M_tot*T²)^(1/3)` only in that alternative context. | CTL spec locks raw-mass scaling and documents the mass-fraction path as future rewrite only. | Lines 591-600 of `ctl_instruction.md` match the required structural anchors. PASS: AC-PHYS-01 | PASS |
| AC-PHYS-02 | `rg` checks for the normalized-time derivative contract, canonical `u=t/T` leaf, conditional `tau` chain-rule factors, componentwise derivative requirement, forbidden all-ones vector-Jacobian product, `2πu` synthetic trajectory, and CTL cross-reference. | Architecture spec owns PHYS-02 and CTL cross-references it without duplicating the contract. | `pinn_architecture.md` lines 843-881 and `ctl_instruction.md` line 989 match the required structural anchors. PASS: AC-PHYS-02 | PASS |
| AC-PHYS-03 | `rg` checks for Plummer `r_safe` in both specs, `epsilon_train=10^-5`, `epsilon_inv=10^-10`, unsoftened `s_min`, anti-pattern warnings, and stale additive-softening negative checks. | Both specs use the matched Plummer form and no stale softening symbols remain. | `ctl_instruction.md` lines 684-695 and `pinn_architecture.md` lines 378-586 match required anchors; stale softening negative checks returned no matches. PASS: AC-PHYS-03 | PASS |
| AC-PHYS-04 | Negative `rg` checks for HNN-style architecture claims, plus positive checks for soft conservation regularizer, Energy Conservation Regularizer, matched-Plummer Hamiltonian, and `H_ε`. | HNN-style framing is removed and energy is framed as a soft conservation regularizer. | HNN negative checks returned no matches; `pinn_architecture.md` lines 496-520 and 956 match required anchors. PASS: AC-PHYS-04 | PASS |
| AC-PHYS-05 | Negative `rg` checks for pseudo-ALM default-loss terms, plus positive checks for Optional ALM Ablation, P2, scalar conservation constraints only, and optimizer-phase semantics for Adam/L-BFGS. | Default loss excludes pseudo-ALM and optional ALM is P2 scalar-conservation-only. | Pseudo-ALM default negative checks returned no matches; `pinn_architecture.md` lines 662-677 and 960 match required anchors. PASS: AC-PHYS-05 | PASS |
| AC-PHYS-06 | `rg` checks for IC13 Validity, reconstructive fixed-gauge / gauge-fixed prose, no constraint-counting justification, Phase 17/18 cross-reference, and absence of the stale 8D passage. | CTL M4 text uses reconstructive gauge-fixed encoding and removes the old constraint-counting claim. | `ctl_instruction.md` line 941 matches required anchors; stale M4 text negative check returned no matches. PASS: AC-PHYS-06 | PASS |

## Closure Guards

- All six exact markers are present: `PASS: AC-PHYS-01`, `PASS: AC-PHYS-02`, `PASS: AC-PHYS-03`, `PASS: AC-PHYS-04`, `PASS: AC-PHYS-05`, `PASS: AC-PHYS-06`.
- No `pinn/` diff is present in staged or unstaged changes.
- `GAP-19-01` is resolved: `19-GAPS.md`, `v1.4-GAPS.md`, and `19-CONTEXT.md` carry the canonical D-20 decision.
- Phase 21 handoff validates denominator activation behavior only: `Pr(|H0| < epsilon_H)` and quantiles of `|H0| / S_H`.
- Phase 21 does not reopen epsilon selection unless a new user-instruction gap is created.
- The final acceptance guards use the resolved numeric contract `epsilon_H = 1e-4 * S_H`, not a symbolic placeholder.
- The closure plan no longer treats `GAP-19-01` as open or blocking.

## Post-Review Revalidation

After the Phase 19 code review, the structural verifier was rerun with additional guards for the reviewed defects:

| Review guard | Expected result | Actual result | Result |
|---|---|---|---|
| Causal physics loss default | `pinn_architecture.md` defines `L_{phys}^{causal}`, causal weights, and `stopgrad`; the old unweighted `N_col` formula is absent as the default. | `pinn_architecture.md:407` through `pinn_architecture.md:423` match the required causal-loss anchors. | PASS |
| Normalized physics-time sampling and inference | Collocation and inference use `u in [0, 1]`, canonical trajectory field `traj_data['u']`, wrapper-computed `tau=2u-1`, and canonical autograd leaf `u`. | `pinn_architecture.md:432`, `pinn_architecture.md:460`, `pinn_architecture.md:742`, and `pinn_architecture.md:752` match; stale `t_min, t_max`, noncanonical adaptive-time field naming, and model-input-range normalization text are absent. | PASS |
| Energy denominator floor in CTL gate | Stage-transition energy drift divides by `|H_j(0)| + epsilon_H` with `epsilon_H = 1e-4 * S_H`. | `ctl_instruction.md:1266` through `ctl_instruction.md:1268` match the D-20 denominator-floor contract. | PASS |
| PHYS-05 reproducibility wording | Both `loss.yaml` bullets refer to default weights, PHYS-05 warmup, causal residual settings, and conservation regularizer scales. | `ctl_instruction.md:1301` and `ctl_instruction.md:1408` match. | PASS |
| Edited Python listing structure | `TrajectoryDataset.__init__` and `compute_initial_energy` are indented under `class TrajectoryDataset`. | `pinn_architecture.md:554` through `pinn_architecture.md:588` have valid class-level indentation. | PASS |

Additional guards: `git diff --check` passed, and no staged or unstaged `pinn/` diff exists.
