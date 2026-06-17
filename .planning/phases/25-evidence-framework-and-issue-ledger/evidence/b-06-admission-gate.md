# Evidence Packet: B-06 - Stage 4→5 Trajectory Admission Gate

## Header

| Field | Value |
|---|---|
| ID | `B-06` (v1.5 Issue-02; directory-qualified — distinct from the v1.4 issue-01 "B-06" namesake) |
| Title | `Stage 4→5 trajectory admission gate (TrajectoryValidator at DataLoader init)` |
| Severity | `BLOCKING` (per `24-ISSUE-LEDGER.md:23` and issue doc `02-data-pipeline-and-validation.md:57`) |
| Current Status | `VERIFIED` |
| Current Verdict | `accept-resolution` |
| Phase | `Phase 26` (PIPE-01; Plan 26-01) |
| Acceptance Check ID | `AC-PIPE-01` |
| Spec Sections Touched | `ctl_instruction.md` new `## Step 1A — Trajectory Admission Gate` (inserted after Step 1's item list, before Step 2). `pinn_architecture.md`: None (D-04 — the gate is data-side; no architecture-side statement required). |
| Code Paths Touched | `Not code-applicable` (framework-spec contract only; loader implementation is FUT-01) |

## Source Positions

| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` | `§3.1 Q-A1:105-174` (7-clause gate; `>= 200` floor rejected at `:117`; proposed spec text `:127-174`) | A trajectory admission gate runs at DataLoader init, between Stage-4 metric generation and any training use, with 7 admission clauses (identity+blacklist, DATA-05 quarantine, structural integrity `n_snapshots >= 2`, completeness `final_timestep >= 9.5` from parsed block times, conservation gate `SCS > -5`, physical-invariant gates, grid-consistency at WARN). Every rejection/quarantine logged `(variant, id, reason_code)`; per-variant admitted/rejected/quarantined counts logged at init. The issue doc's `snapshot_count >= 200` floor (P1-1) is **rejected** — no absolute snapshot-count floor above 2 is imposed. |
| `pinn_instruction/issues/02-data-pipeline-and-validation.md` | `:57` (B-06 row), `:283` (P1-1), `:337-348` (DataLoader Requirements), `:357` | Insert `TrajectoryValidator` at DataLoader init enforcing `snapshot_count >= 200` for Stage 4+, `>= 2` for Stage 0-3, AND `final_timestep >= 9.5`; log rejections. The `>= 200` floor is the contested clause. |

BOTH citations are present (D-04 §2), even though this verdict is uncontested (ledger Sources Disagree? = NO).

## Spec Evidence

Current framework-spec evidence for the convention being added/changed:

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:340-381` — Step 1 ("Parse Raw Simulation Data"): item 3 (`:351-360`) already handles short/incomplete files (`< 2` snapshots) gracefully by returning empty arrays and logging; item 6 (`:374-378`) saves parsed objects. There is **no** admission gate between Step 1 (parse) and Step 2 (preprocessing) / Step 5 (stage assignment) — the Stage 4→5 gap the issue doc names. The new Step 1A lands between the Step-1 item list (ending `:381`) and `## Step 2` (`:383`).
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:1061-1068` — Step 5 ("Curriculum Stage Assignment") consumes a per-ID stage mapping; the admission gate must run before stage assignment (ordering established by the candidate).
- `pinn_instruction/markdown_conversion/framework-revisions/data_quality_assessment.md §5.1` — gate-before-analysis ordering rationale and the locked SCS gate's sole written home (READ-ONLY, SCOPE-09; citable, never editable).

### Dataset Evidence (§3b)

- `24-VERIFIED-FACTS.md CLM-10:25` — per-variant snapshot medians: `brutus_standard_quasi_random` median **61** (min 59, max 61); `brutus_hierarchical` median **127** (min 126, max 127); both gold variants median **1003**. A `snapshot_count >= 200` floor rejects **100%** of both base populations (61 < 200 and 127 < 200) — the populations the locked stratification assigns to Stages 3–4. This **falsifies the issue-doc P1-1 floor on verified facts**, independent of any source citation.
- `24-VERIFIED-FACTS.md CLM-11:26` — prevalence of `final_timestep >= 9.5` = **1.000** across the probe-applicable population (701/701 std base no-footer; 219/219 std-gold no-footer; 1,550/1,550 hier base no-footer). The completeness clause is therefore currently non-binding in practice but stays mandatory as the catch for future partial runs. "probe-applicable" is an uncharacterized qualifier (OI-6, carried below).
- `24-VERIFIED-FACTS.md DATA-05:35` — the 70 `brutus_hierarchical` base outputs (IDs `0005`–`0059`, `0061`–`0075`) were quarantined; the rerun was executed and validated 2026-06-11 (RESOLVED-WITH-INSTRUCTION; post-swap DATA-05 probe 0/4857). The candidate quarantine clause (clause 2) is transcribed as a standing configuration gate; OI-9 (quarantine liftable on re-verification — and in fact lifted by the validated rerun) is carried below.

## FUT-01 Hand-off Note (formerly "Code Evidence")

Live code in `pinn/` is NOT a v1.5 evidence source (user directive 2026-05-19). Forward-pointing only:

- `pinn/data-processing-pipeline-full.py` — the v1.3-era data pipeline performs Step-1 parsing but implements **no** Stage 4→5 admission gate (the gap B-06 names). FUT-01 must build a `TrajectoryValidator` that runs at DataLoader init implementing the seven Step-1A clauses, ordered before `compute_globals` and stage assignment. Indexed for the eventual `NN-CODE-DIVERGENCE.md` / `pinn/STATUS.md`. NOT v1.5 evidence.
- The M11 live-loader blacklist-consumption status (OI-8, SCOPE-10) is carried forward to PIPE-03 / FUT-01 (see `evidence/m11-m12-severity.md:49`); clause 1 of this gate names the blacklist exclusion but its live-loader enforcement is the PIPE-03 question, not this packet's verdict basis.

## First-Principles Physics Check

Not an EVID-10 finding (ledger `Sources Disagree? = NO`); this section is optional. One short arithmetic check anchors the floor rejection:

```
Issue-doc P1-1 floor:        snapshot_count >= 200  (Stage 4+)
Verified medians (CLM-10):   standard base = 61,  hierarchical base = 127
61 < 200  and  127 < 200  =>  the floor rejects every admitted base trajectory
```

The floor conflates per-file *validity* with curriculum *membership* (a complete standard-base run is a valid 61-snapshot trajectory; it is simply not a 200-snapshot trajectory). The cadence arithmetic `n_snapshots >= 1 + ceil(9.5/dt_nom)` yields 57/120/951 for dt_nom 0.17/0.08/0.01 — consistent with the observed medians and retained at WARN level (clause 7), not promoted to a hard reject (OI-6 dependency).

## Verdict

`accept-resolution`

The resolution doc's 7-clause admission gate (`02-resolution-doc.md §3.1 Q-A1:105-174`) is adopted after independent verification. The decisive independent check is the CLM-10 falsification of the issue-doc `>= 200` floor (`24-VERIFIED-FACTS.md:25`): a 200-snapshot floor rejects 100% of both base populations, so the issue-doc P1-1 clause fails on verified facts and is rejected; every other clause is either a locked convention transcribed by citation (conservation gate = HC-5; snapshot minimums = M12) or a structural/completeness check grounded in CLM-10/CLM-11 and the README's completeness rule. No new cross-source conflict surfaced (so no EVID-10 sections are required), and no candidate clause is source-silent. The verdict is `accept-resolution`, not `accept-third-position`, because the candidate text survives every check unchanged. The one live judgment call the candidate itself flags — clause 7 WARN-vs-reject for the cadence check — is preserved as conditional on OI-6, not re-decided here.

## Root-Cause Framework Ambiguity

Optional (not EVID-10). The Stage 4→5 gap exists because `calculate_metrics.py` (SCOPE-07) processes every Brutus file with no completeness check, and the only validity signal (`final_timestep >= 9.5`) runs at the Stage-3 runner scripts, never re-validated at DataLoader init (issue doc `:57`). The current `ctl_instruction.md` Step 1 (`:340-381`) parses but never gates. Step 1A closes the gap with a single enforcement point ordered before `compute_globals` and stage assignment.

## Locked Convention

Optional (not EVID-10). The contract adopted is the verbatim candidate spec text at `02-resolution-doc.md:127-174` (the seven Step-1A clauses), with snapshot minimums stated by citation to the locked M12 rule rather than re-derived (D-02), and the conservation gate transcribing — not re-opening — Hard Constraint 5 (`SCS > -5` ≡ `ε_H > 1e-5`).

## Which Source Was Correct / Wrong

- **Resolution doc:** correct. The 7-clause gate is grounded; the `>= 200` rejection is verified on CLM-10; the WARN-level cadence check correctly preserves the OI-6 dependency rather than over-committing.
- **Issue doc:** correct that a Stage 4→5 gate is missing (real BLOCKING gap) and that `final_timestep >= 9.5` belongs in it; **wrong** on the `snapshot_count >= 200` floor (P1-1) — falsified by CLM-10 (rejects 100% of both base populations). The issue doc's `>= 2` for Stage 0-3 stage-tiering is dropped because the completeness condition dominates it.

## Before / After Spec Note

**Affected section:** `ctl_instruction.md` — new `## Step 1A — Trajectory Admission Gate` (post-edit `:404`), inserted immediately after the Step 1 item list (pre-edit ending `:381`; the B-11 ID-resolution item 7 was appended to that list in the same edit, post-edit `:381-405`) and before `## Step 2` (pre-edit `:383`, post-edit `:458`).

**Before:** `ctl_instruction.md` Step 1 (pre-edit `:340-381`) parses raw simulation data and gracefully handles `< 2`-snapshot files (item 3, `:351-360`) but contains **no** admission gate; there is no enforcement point between Stage-4 metrics and Stage-5 stage assignment / `compute_globals`. The Stage 4→5 gap is unguarded.

**After:** a `## Step 1A — Trajectory Admission Gate` section (post-edit `:404-452`) states the 7-clause data-side gate (identity+blacklist, DATA-05 quarantine, structural integrity, completeness `final_timestep >= 9.5`, conservation `SCS > -5`, physical-invariant gates, grid-consistency at WARN), with per-trajectory reason-coded rejection logging and per-folder admitted/rejected/quarantined counts at init, ordered before stage assignment and `compute_globals`. Clause 1 depends on the Step-1 item-7 ID-resolution contract (B-11), reconciled in the same edit.

**Snapshot minimums (D-02 — cite, do not re-decide):** Step 1A imposes no absolute snapshot-count floor beyond clause 3's `>= 2`. The per-trajectory *sampling* point count is governed by the locked M12 rule `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))` (the locked-convention prose at `evidence/m11-m12-severity.md:105-113`, line 107). Phase 26 cites that rule and does **not** re-open sampling feasibility; M12's spec transcription is owned by Phase 27 PIPE-04. The issue-doc `>= 200` floor is explicitly not restated as the contract.

## Named Acceptance Check

**AC-PIPE-01** (reserved in `24-ISSUE-LEDGER.md:23`; no new AC-ID minted — VER-07).

- **Pass criterion:** (a) the `>= 200` snapshot floor is absent from the Step-1A contract and from `ctl_instruction.md`; (b) the Step-1A gate states `final_timestep >= 9.5` computed from parsed block times (never footer/line-count), the locked `SCS > -5` conservation gate, structural `>= 2` snapshots, the DATA-05 quarantine, and snapshot minimums by citation to the locked M12 rule; (c) the verified medians (CLM-10: 61/127 base) confirm a `>= 200` floor would reject 100% of both base populations — i.e. the rejected floor is empirically incompatible with the data.
- **Data it runs on:** the edited `ctl_instruction.md` (spec-consistency probe) and the recorded CLM-10 medians in `24-VERIFIED-FACTS.md:25` (dataset facts; re-derivable via the CLM-10 probe `data06_snapshots.py`, not re-run here per the Phase-24 probe-capture convention `24-VERIFIED-FACTS.md:100-104`).
- **Exact command + captured output (re-derivable, D-15):**

```
$ grep -nE '## Step 1A|Admission Gate|final_timestep >= 9.5|SCS > -5|>= 200|snapshot_count >= 200' \
    pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
404:## Step 1A — Trajectory Admission Gate (data-side; runs at DataLoader init)
423:4. Completeness. `final_timestep >= 9.5`, computed from parsed snapshot block
429:   REJECT if `SCS > -5` (equivalently `eps_H > 1e-5`). `SCS = -5` exactly is
446:`>= 200` floor is rejected: verified base medians are 61 standard-base / 127
447:hierarchical-base / 1003 gold, so floors such as `>= 200` are arithmetically
```

Interpretation: the `## Step 1A — Trajectory Admission Gate` heading and the completeness (`final_timestep >= 9.5`) and conservation (`SCS > -5`) clauses are present; the only `>= 200` tokens in the file appear inside the prose that **rejects** the floor (lines 446-447 "floors such as `>= 200` are arithmetically incompatible with the base populations"), never as a contract clause — there is no `snapshot_count >= 200` admission requirement. PASS.

```
$ grep -nE 'min\(n_pts_cap|n_pts\(traj\)|m11-m12-severity' \
    pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
450:M12 rule `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))` (locked M12 rule, see
451:Phase 27 PIPE-04; transcribed in `m11-m12-severity.md`), not by any admission
```

Interpretation: snapshot minimums are stated by citing the locked M12 rule (`m11-m12-severity.md`, Phase 27 PIPE-04), not re-derived. PASS.

AC-PIPE-01 is a spec-consistency + dataset-fact probe; it touches no `pinn/` path. Phase 29 (VER-09) builds and re-executes the full runnable acceptance suite from this AC-ID.

## Status Transition Log

```text
2026-06-13 b1852b0f PENDING -> IN_PROGRESS (Phase 26 P01 by gsd-executor; B-06 packet authored, accept-resolution verdict, AC-PIPE-01 defined)
2026-06-13 b1852b0f IN_PROGRESS -> FIX_APPLIED (Phase 26 P01; Step 1A admission gate transcribed into ctl_instruction.md from 02-resolution-doc.md:127-174)
2026-06-13 b1852b0f FIX_APPLIED -> VERIFIED (Phase 26 P01; AC-PIPE-01 spec-consistency + CLM-10 dataset probe PASS; G1 closes with B-06)
```

The Plan 26-01 commit SHA is `b1852b0f` — all three transitions, the spec edit, and the ledger edits travelled in that one commit (D-08); this SHA was backfilled into the packets and the ledger per-finding subsections in the immediately following provenance commit (a commit cannot reference its own hash inline).

**Carried caveats (D-13):**
- **OI-6** (`02-resolution-doc.md:767`) — the no-footer populations' snapshot distributions are uncharacterized; clause 7 (grid-consistency) is held at WARN, and escalation to a hard cadence reject is conditional on closing OI-6. Carried, not resolved.
- **OI-9** (`24-DATA05-RERUN-REMEDIATION.md`; validated 2026-06-11) — the DATA-05 70-ID rerun passed; the quarantine (clause 2) is stated as standing configuration but the trajectory-file quarantine was in fact lifted by the validated rerun. Carried where the gate's DATA-05 clause touches the rerun files.

**Dependents / regression (D-08):** B-06 shares the Step-1 region with B-11 (this plan's other finding) — B-06 clause 1 ("the ID resolves per the Step-1 ID-resolution contract") depends on B-11's appended Step-1 item. The two were reconciled in one before/after pass (mutually consistent). No previously-VERIFIED Phase 26 row exists yet, so the regression surface is internal to this plan.

**G1 close-with-parent (D-07):** G1 (synthesis view over B-06) closes with B-06 — no separate evidence packet; annotated in the ledger's G1 per-finding note.
