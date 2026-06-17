---
status: active
purpose: verification-report
created: 2026-06-14
milestone: v1.5
phase: 27-sampling-precision-and-global-scale-contracts
retirement_trigger: >
  Retire after the two flagged process-ledger inconsistencies (compute-globals-D.md
  header Current Status; 27-VALIDATION.md Sign-Off checkboxes) are remediated and
  confirmed by a re-verification pass, OR when this phase's review set is retired
  per docs/README.md audit-and-approval. Not a canonical spec artifact.
---

# Phase 27 Execution Verification — Independent Gatekeeper Review

**Reviewer:** verification gatekeeper (independent of the executing agent)
**Date:** 2026-06-14
**Subject:** Execution of Phase 27 Plans 01–04 (`27-01-PLAN` … `27-04-PLAN`),
branch `milestone/v1.5`
**Scope:** Hard-evidence verification of every claim in the four execution
summaries. No claim is accepted without a fresh command/output backing it.

---

## 1. Executive verdict

| Question | Answer |
|---|---|
| Were the four spec contracts (PIPE-04 / PIPE-07 / PIPE-08 / PIPE-09) actually landed in the framework specs? | **YES** — verified by region extraction + pre-edit git diff. |
| Do the acceptance checks (AC-PIPE-04/07/08/09) pass? | **YES** — all re-run green against the final spec state (exit 0). |
| Are the ACs *genuinely discriminating* (not vacuously passing)? | **YES** — each AC was proven to FAIL against its pre-edit git revision. |
| Are all 5 in-scope ledger rows at a terminal VERIFIED state? | **YES** — M12, G5, mass-drift, footer, D=6.694 all VERIFIED. |
| Are both in-scope gaps resolved? | **YES** — GAP-27-01, GAP-27-02 both RESOLVED-WITH-INSTRUCTION. |
| Are all 13 claimed commits present on `milestone/v1.5`? | **YES.** |
| Was the work done with no hallucination or fabrication? | **YES** — transcribed prose matches locked evidence packets; no invented content detected. |
| Are there any uncompleted steps or inconsistencies? | **YES — 3 defects** (2 MEDIUM, 1 LOW), all process-ledger/presentation, none substantive. |

**Overall: Phase 27 is substantively complete and correctly executed.** The four
contracts are landed, verified, and discriminating. Three minor process-ledger
inconsistencies remain open and should be remediated before the milestone closes,
but none blocks the phase-exit gate on substantive grounds.

---

## 2. Methodology

Every claim below is backed by a command run in this review session. Two
techniques were applied beyond re-running the ACs:

1. **Pre-edit discrimination check.** For each AC, the asserted token was grepped
   against the spec revision *immediately before* the landing commit
   (`git show <commit>^:<file>`). A count of 0 (for added content) or ≥1 (for
   removed content) proves the AC would have failed pre-edit — i.e., it is not a
   vacuous green.
2. **Region-scoped extraction.** AC-PIPE-04's Mini-Batch region and AC-PIPE-08's
   stage-query sub-section were re-extracted with the same `awk` the ACs use, and
   the extracted prose inspected directly (not just grepped).

---

## 3. Per-plan verification matrix

### Plan 01 — PIPE-04 (M12 data-loss sampling contract) — ✅ PASS

| Claim | Evidence | Verdict |
|---|---|---|
| `min(n_pts_cap, n_snapshots)` landed in Mini-Batch Construction | `ctl_instruction.md:1458` is `### Mini-Batch Construction...`; region extraction contains `n_pts(traj) = min(n_pts_cap, n_snapshots(traj))`, `without replacement`, `k_w = floor(n_pts/2)` Gumbel-top-k, cap 32 flagged "not evidence-based…configuration knob" | ✅ |
| `0.5 × n_snapshots` never operative | Region contains "No `0.5 x n_snapshots` factor is imposed" (rejection only) | ✅ |
| DATA-06 medians cited | Region cites "61 standard-base / 127 hierarchical-base / 1003 gold" | ✅ |
| `m11-m12-severity.md` packet cited | Region cites `evidence/m11-m12-severity.md` | ✅ |
| `n_snapshots`/`dt_out` metadata + M16→doc-03 deferral | Region names both; deferral present | ✅ |
| Stale 50/50 prose replaced; curriculum table preserved | Pre-edit `50% uniform` count = 1; post-edit region has `Replay set`/`Look-ahead set` table intact | ✅ |
| `pinn_architecture.md §3.1` code-default note | `pinn_architecture.md:352` note present (PIPE-04 + PIPE-08 visibility) | ✅ |
| M12 ledger row → VERIFIED | `24-ISSUE-LEDGER.md:26` = `**VERIFIED**`, AC-PIPE-04 PASS | ✅ |
| G5 ledger row → VERIFIED (closes with M12) | `24-ISSUE-LEDGER.md:33` = `**VERIFIED**`, D-08 close-with-M12, M16 deferral | ✅ |
| `m11-m12-severity.md` transition log advanced | Lines 180–182: M12 PENDING→IN_PROGRESS→FIX_APPLIED→VERIFIED, SHA `6e81d14f` | ✅ |
| Commits `6e81d14f`, `da2149d9` | Present in `git log` | ✅ |
| AC-PIPE-04 discriminating | Pre-edit `min(n_pts_cap, n_snapshots` count = 0 → AC assertion (1) would have FAILED | ✅ |

### Plan 02 — PIPE-07 (float64 precision contract) — ✅ PASS

| Claim | Evidence | Verdict |
|---|---|---|
| §2.1 precision note landed | `ctl_instruction.md:577–587` blockquote: float64 sufficiency; `decimal.Decimal` classifier-only (`max_i \|Δm_i\| < 1e-15`); current ICs canonical; 70 mismatches = stale artifacts (0.1–1.0 mass units); DATA-05 rerun 70/70 cited; future mismatch = FAIL | ✅ |
| Existing §2.1 `1e-15` mass-invariance gate preserved | Note is additive; preceding gate text intact | ✅ |
| mass-drift row → VERIFIED | `24-ISSUE-LEDGER.md:41` = VERIFIED, AC-PIPE-07, `data05-precision.md` link | ✅ |
| footer row → VERIFIED (both facets) | `24-ISSUE-LEDGER.md:40` = VERIFIED, PIPE-06 via D7 + PIPE-07 via AC-PIPE-07 | ✅ |
| `data05-precision.md` packet → VERIFIED | `:19` Current Status = `VERIFIED`; transition log `:91–93` SHA `b6fe225d` IN_PROGRESS→FIX_APPLIED→VERIFIED; first entry `09e37f8` intact | ✅ |
| Commits `b6fe225d`, `70dd29b0` | Present | ✅ |
| AC-PIPE-07 discriminating | Pre-edit `float64 is the data-side precision contract` absent (only an unrelated pre-existing `DATA-05 rerun` mention at `:374`) → note is genuinely new | ✅ |

### Plan 03 — PIPE-08 (data-side stage-query interface) — ✅ PASS

| Claim | Evidence | Verdict |
|---|---|---|
| `sample_replay(n, max_stage)` + `sample_lookahead(n, stage)` signatures | `ctl_instruction.md` `#### Data-side stage-query interface` sub-section carries both, with cumulative $D_{\le k}$ / next-stage $D_{k+1}$ semantics | ✅ |
| `dt_out`/`n_snapshots` confirmed as §2.6 metadata | Both named in the sub-section + metadata schema | ✅ |
| SCOPE-11 / doc-03 / M16 forward-reference (data-side only, no training policy) | Blockquote "Scope boundary (SCOPE-11)" defers collocation-scaling, replay-fraction, training-loop to doc-03 | ✅ |
| `param_provenance` preserved (PIPE-06 regression) | Still present | ✅ |
| G5 per-finding note appended with PIPE-08 line | `24-ISSUE-LEDGER.md:346`: "2026-06-14 c647fc3 PIPE-08 metadata consistency…" (G5 stays VERIFIED, not reopened) — **append is present** | ✅ |
| `pinn_architecture.md §3.1` FUT-01 visibility note | `:352` one-line note | ✅ |
| Commits `c647fc33`, `8fb87faa`, `3efd840d`, `eb43a418` | Present | ✅ |
| AC-PIPE-08 discriminating | Pre-edit `sample_replay(n, max_stage)` count = 0 → AC would have FAILED | ✅ |

### Plan 04 — PIPE-09 (normative compute_globals contract) — ✅ PASS (core), ⚠️ 2 process-ledger defects

| Claim | Evidence | Verdict |
|---|---|---|
| Normative `compute_globals` contract in §2.5 | `ctl_instruction.md:781`: raw-mass `D = (G T²)^{1/3} ≈ 4.6416` canonical; `6.694`/`M_tot_ref` rejected as pipeline instruction | ✅ |
| "No configuration parameter may select the mass-fraction form" | `:781` exact wording present | ✅ |
| Plummer rule + additive-ε (PHYS-03) prohibition | `:781` r_safe/`ε_inv = 1e-10` + "Additive `+ ε`…is the PHYS-03 anti-pattern and is prohibited" | ✅ |
| Admitted-set scope (GAP-27-02 Option A) | `:781` "post-Step-1A admission, post-blacklist exclusion, post-DATA-05-quarantine" — clean normative text, sign-off caveat NOT in spec (correct) | ✅ |
| `E_scale` floor canonicalized `+1e-10 → +1e-8` | `:785` `E_{scale} = \lvert median(\{E_j\}) \rvert + 10^{-8}`; pre-edit E_scale `1e-10` count = 1 (the outlier) → canonicalization landed | ✅ |
| Plummer `ε_inv = 1e-10` preserved (not corrupted) | Surviving `1e-10` sites at `:899/:909/:917/:1126`; `E_scale`-scoped `1e-10` now 0 | ✅ |
| `compute-globals-D.md` cited | `:781` citation present | ✅ |
| arch §5.2 `E_scale = +1e-8` confirmed (no edit) | `pinn_architecture.md:762` already `+ 10^-8` | ✅ |
| SCS / Phase 28 untouched | AC-PIPE-09 [14] PASS; no SCS threshold text under the contract | ✅ |
| D=6.694 ledger row → VERIFIED | `24-ISSUE-LEDGER.md:39` = `**VERIFIED**`, AC-PIPE-09 | ✅ |
| `compute-globals-D.md` transition log → VERIFIED | `:134` SHA `731c795` PENDING→IN_PROGRESS→FIX_APPLIED→VERIFIED | ✅ |
| Commits `731c795e`, `95575fd9`, `7a2b7ad2`, `81a587c0`, `3e5e7ec7` | Present | ✅ |
| AC-PIPE-09 discriminating | Pre-edit E_scale `1e-10` count = 1 → AC [9] would have FAILED | ✅ |
| `27-VALIDATION.md` flipped (`nyquist_compliant: true`, `wave_0_complete: true`, all Per-Task rows ✅ green, Approval set) | Frontmatter + Per-Task map confirmed | ✅ (core) — see Defect B for the checkbox gap |

---

## 4. Findings — defects and inconsistencies

### Defect A — MEDIUM — `compute-globals-D.md` header "Current Status" not flipped to VERIFIED

- **Location:** `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/compute-globals-D.md:10`
- **Evidence:** `| Current Status | \`PENDING\` |`
- **Problem:** The packet's Status Transition Log (`:134`) correctly records
  `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`, and the Phase 24 ledger
  row (`24-ISSUE-LEDGER.md:39`) is VERIFIED. But the canonical header field that
  a reader checks first still says `PENDING` — directly contradicting the
  verdict-of-record. The sibling packet `data05-precision.md:19` was correctly
  flipped to `Current Status | VERIFIED (AC-PIPE-07 PASS; …)`, so the two
  packets were handled inconsistently.
- **Root cause:** Plan 27-04 Task 3 named only the "Status Transition Log"; it
  did not explicitly call out the header "Current Status" field, and the
  executor did not flip it. Plan 27-02 *did* flip it for `data05-precision.md`.
- **Impact:** Process-ledger inconsistency only. The substantive verdict is
  correctly VERIFIED everywhere else. A reader who trusts the header would
  wrongly conclude D=6.694 is unresolved.
- **Fix:** Flip `compute-globals-D.md:10` `Current Status` from `PENDING` to
  `VERIFIED` (mirroring `data05-precision.md:19`). Trivial, one-line, same-commit
  with a `verify(27-04)` provenance note.

### Defect B — MEDIUM — `27-VALIDATION.md` Validation Sign-Off checkboxes all unchecked

- **Location:** `.planning/phases/27-sampling-precision-and-global-scale-contracts/27-VALIDATION.md:88–93`
- **Evidence:** All 6 Sign-Off boxes are `- [ ]` (unabridged `grep -cE '^- \[ \]'` = 6).
  The last box is literally `* [ ] nyquist_compliant: true set in frontmatter…` —
  yet that condition IS true (`:5 nyquist_compliant: true`), so the box is
  self-evidently stale. The "Approval:" line (`:95`) claims "approved 2026-06-14".
- **Problem:** Plan 27-04 Task 4 explicitly required "check the Wave 0
  Requirements checkboxes." The **Wave 0 Requirements** block (`:68–70`) IS
  correctly checked `[x]`, but the separate **Validation Sign-Off** block
  (`:88–93`) — a 6-item self-audit checklist that gates the "approved" claim —
  was left entirely unchecked. An approved sign-off over an all-empty checklist
  is an internal contradiction in a phase whose entire purpose is
  process-integrity.
- **Impact:** Presentation/process-integrity inconsistency. The actual gate state
  is correctly recorded in the frontmatter, Per-Task Status column, and Approval
  prose. No substantive AC is affected.
- **Fix:** Tick all 6 boxes that are in fact satisfied (`:88–93`). Trivial.

### Defect C — LOW — `m11-m12-severity.md` header "Current Status" not flipped after M12 VERIFIED

- **Location:** `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/m11-m12-severity.md:10`
- **Evidence:** `| Current Status | \`PENDING\` |` while the M12 transition log
  (`:182`) records M12 FIX_APPLIED→VERIFIED on 2026-06-14 (Plan 01).
- **Problem:** Same pattern as Defect A. M11 reached VERIFIED in Phase 26 and M12
  in Phase 27 Plan 01, but the packet's header field was never advanced.
  (Arguably pre-existing from Phase 26, but Phase 27 Plan 01 advanced M12 to
  VERIFIED without flipping the header — so it is in scope for this phase.)
- **Impact:** Low — the transition logs and ledger rows are correct and authoritative.
- **Fix:** Flip the header `Current Status` to reflect M11+M12 both VERIFIED
  (or a combined statement), mirroring the other packets.

### Notes (not defects — acknowledged limitations, recorded for completeness)

- **AC-PIPE-04 negative control (assertion 4) is logically weak.** It checks that
  `reject|unevidenced|not imposed` appears *anywhere* in the region, not adjacent
  to the `0.5` mention. The plan explicitly acknowledges this as **vacuous per
  F-22**; the substantive protection is assertions (1) + (8), both of which
  discriminate correctly. Not a defect — a documented limitation.
- **AC-PIPE-04 `awk` heading-level discrepancy.** Plan 27-01 Task 1 stated the
  region extractor as `awk '/^## Mini-Batch…/` (h2), but the actual heading is
  `###` (h3) at `:1458`. The shipped script correctly uses `###`. The script
  adapted to reality and works; the only inaccuracy is the 27-01 SUMMARY's
  "Plan executed exactly as written / no deviations" claim. Cosmetic.
- **AC-PIPE-07 is inline (no script file).** Consistent with the plan
  (`Codex discretion on inline-vs-script`); verified by direct region read
  above. Not a defect.

---

## 5. No hallucination / fabrication detected

Spot-checked the transcribed prose against the locked evidence packets:

- **PIPE-07 note** (`ctl:577–587`) matches the `data05-precision.md` Locked
  Convention (float64 sufficiency / Decimal-as-classifier / stale-not-precision
  / DATA-05 rerun 70/70) — no invented physics or scope.
- **PIPE-09 contract** (`ctl:781`) matches `compute-globals-D.md` (raw-mass D
  canonical; 6.694/M_tot rejected; Plummer rule). The `E_scale +1e-10 → +1e-8`
  change is the pre-reasoned 2-of-3 edit, NOT a re-adjudication — D-03 honored.
  The locked D value was not reopened. Plummer `ε_inv = 1e-10` was preserved.
- **PIPE-08 sub-section** transcribes only the locked signatures + data-side
  semantics; no return-type/ordering/seeding invented (A1 guard satisfied).
- **No live `pinn/` code cited as grounding** in any Phase 27 edit (FUT-01
  references only). SCOPE-05/SCOPE-10 honored.

---

## 6. Phase-exit gate assessment (F-13 / F-16)

| Gate item | State |
|---|---|
| M12 (`24-ISSUE-LEDGER.md:26`) | ✅ VERIFIED |
| G5 (`:33`) | ✅ VERIFIED (closes with M12; M16 deferred to doc-03) |
| mass-drift (`:41`) | ✅ VERIFIED |
| footer (`:40`) | ✅ VERIFIED (PIPE-06 via D7 + PIPE-07 via AC-PIPE-07) |
| D=6.694 (`:39`) | ✅ VERIFIED |
| D7 (`:28`) regression | ✅ stays VERIFIED (no shared-text regression) |
| B-06 (`:23`) regression | ✅ stays VERIFIED |
| GAP-27-01 | ✅ RESOLVED-WITH-INSTRUCTION (2026-06-13) |
| GAP-27-02 | ✅ RESOLVED-WITH-INSTRUCTION (2026-06-14, Option A) |
| `nyquist_compliant` frontmatter | ✅ `true` |

**Substantive phase-exit gate: MET.** No in-scope row is non-terminal; no OPEN gap.
The three defects above are process-ledger/presentation inconsistencies that do
not alter any verdict, but they should be closed before the *milestone* (v1.5)
closes so the audit trail is internally consistent.

---

## 7. Recommendation

1. **Proceed** — Phase 27's four contracts are correctly landed, verified, and
   discriminating. The executing agent did not hallucinate or fabricate; the
   transcriptions are faithful to the locked verdicts.
2. **Remediate before milestone close** (small, non-blocking):
   - Flip `compute-globals-D.md:10` `Current Status` → `VERIFIED` (Defect A).
   - Tick the 6 `27-VALIDATION.md` Sign-Off boxes that are satisfied (Defect B).
   - Flip `m11-m12-severity.md:10` `Current Status` to reflect M11+M12 VERIFIED
     (Defect C).
   These are `verify(27)` provenance commits, owned-paths-scoped, on
   `milestone/v1.5`. Each is a one-line edit; no spec re-opened.
3. **No re-execution of the spec edits or ACs is required** — all four contracts
   passed their ACs against the final spec, and the ACs were independently
   proven discriminating against pre-edit git state.
