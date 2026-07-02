# Phase 36: Ledger Closure Record (D-05 / D-06 Transcription Verification & Promotion)

**Plan:** Plan 36-03, Tasks 1-2

**Executed:** 2026-07-02

**Transcription verdict:** CLEAN (both D-05 and D-06 transcribed correctly into `ctl_instruction.md`)

**Pre-write ledger SHA-256:** `fb804f8b53c57dd71eda7ed70402670ca534fd85acdc0de0dd7e79fcd8d4c7fe`

## Task 1: Verify D-05/D-06 downstream transcription

### D-05 Verdict

- **Locked verdict (RESOLVED-WITH-INSTRUCTION 2026-06-21):** Option A — unsoftened geometric `s_min` stage gate + matched-Plummer (`epsilon_train = 1e-5`) softening in training residual/energy only; issue-doc `max(s_min, epsilon)` phrasing rejected per PHYS-03.
- **Owner:** Phase 32; **Downstream consumer:** Phase 33 CURR-05; **AC ID:** AC-EVID-15-D05.
- **Transcription anchor (`ctl_instruction.md`):**
  - Lines 287-303 (`## Step 3: Necessary Calculations of Invariants (for Stage Assignment and Input Vector Formulation)`): geometric gate + matched-Plummer loss-side reference (Option A carried verbatim).
  - Lines 1175-1213 (`## Step 4: ...` / CURR-04 / CURR-05 stage-inventory block): raw un-clipped L_norm storage context; `np.clip(L_norm, 0, 1)` "NOT locked" / "owner-pending" state.
- **Phase 33 verification record:** `33-VERIFICATION.md` records **AC-CURR-05 PASS** ("Unsoftened geometric s_min stage-gate frame" — verbatim).
- **Phase 36 transcription probe result:** `AC-EVID-15-D05: PASS` (re-run 2026-07-02T00:39:33Z; SHA-256 `e6ccc642e55591f8f42612e9cc045517b1892677fdda1bc1b73d4de5f3d8c77f`). Two sub-checks: Owner Option A (geometric gate) cited; matched-Plummer loss-side reference present.
- **Verdict:** **CLEAN** — D-05 transcription verified. SPEC anchor + 33-VERIFICATION citation + Phase 36 probe evidence all align.

### D-06 Verdict

- **Locked verdict (RESOLVED-WITH-INSTRUCTION 2026-06-21):** Dual-context — offline invariants/validation keep `epsilon_inv = 1e-10` (consistent with v1.5-locked IPR GAP-28-02), training keeps locked `epsilon_train = 1e-5`; Option C (collapse static `epsilon_inv` to `1e-5`) rejected.
- **Owner:** Phase 32; **Downstream consumers:** Phase 33 static invariants; Phase 35 loss consistency; **AC ID:** AC-EVID-15-D06.
- **Transcription anchor (`ctl_instruction.md`):**
  - Lines 287-303 (CURR-05 s_min stage gate section): `epsilon_inv = 1e-10` (offline invariants/validation) alongside `epsilon_train = 1e-5` (matched-Plummer loss-side); Option C rejected.
  - Line 708: `eps_inv = 1e-10` (§2.5); the training-time `epsilon_train = 1e-5`.
  - Lines 1346-1347 (CURR-02 / τ_L exclusion section): static invariant epsilon carries the v1.5-locked IPR contract.
- **Phase 33 verification record:** `33-VERIFICATION.md` records **AC-CURR-05 PASS** (transcription verified); Phase 35 verification records **AC-LOSS-03** + AC-LOSS-01 carry `epsilon_train = 1e-5` loss-side reference.
- **Phase 36 transcription probe result:** `AC-EVID-15-D06: PASS` (re-run 2026-07-02T00:39:33Z; SHA-256 `f915c08041f9e092bf73f7dfa9a292333e255d601aa2cd8f679b3eaac0490f61`). Three sub-checks: owner dual-context cited; `epsilon_inv = 1e-10` (offline) present; `epsilon_train = 1e-5` (training) present.
- **Verdict:** **CLEAN** — D-06 transcription verified. SPEC anchor + 33/35-VERIFICATION citations + Phase 36 probe evidence all align.

### Owner-Verdict Citation Discipline

Per Plan 36-03 Prohibition 1 ("MUST NOT re-litigate the locked D-05/D-06 verdicts"), this record cites only the **RESOLVED-WITH-INSTRUCTION** owner verdicts (GAP-32-02 Option A for D-05; GAP-32-03 dual-context for D-06) as authority. No new semantic decision is proposed.

## Task 2: Promote D-05 / D-06 to VERIFIED under a freshness-checked write

### Pre-write freshness check

- **Pre-write SHA-256:** `fb804f8b53c57dd71eda7ed70402670ca534fd85acdc0de0dd7e79fcd8d4c7fe` (BEFORE the promotion edit).
- **Status:** 18 rows total; 16 VERIFIED + 2 PENDING (D-05, D-06).

### Promotion

Following Plan 36-03 Task 2 procedure:

1. **D-05 row** (`s_min frame owner decision`, Phase 32): `PENDING → VERIFIED`, preserving the existing `accept-resolution` verdict. Transition log appended: "2026-07-02 Phase 36 Plan 36-03 Task 2: PENDING → VERIFIED by Phase 36, citing AC-EVID-15-D05 PASS (re-run 2026-07-02T00:39:33Z), the CURR-05 transcription check in `36-LEDGER-CLOSURE.md`, and the Phase 36 promotion. Acceptance Check: AC-EVID-15-D05. Evidence Packet: `evidence/d-05-s-min-frame.md`."

2. **D-06 row** (`Epsilon strategy owner decision`, Phase 32): `PENDING → VERIFIED`, preserving the existing `accept-resolution` verdict. Transition log appended: "2026-07-02 Phase 36 Plan 36-03 Task 2: PENDING → VERIFIED by Phase 36, citing AC-EVID-15-D06 PASS (re-run 2026-07-02T00:39:33Z), the static-invariant epsilon transcription check in `36-LEDGER-CLOSURE.md`, and the Phase 36 promotion. Acceptance Check: AC-EVID-15-D06. Evidence Packet: `evidence/d-06-epsilon-strategy.md`."

No new status enum, verdict value, or AC ID was minted; only the two existing statuses (`PENDING → VERIFIED`) were flipped under the freshness-checked write.

### Post-write count (fresh re-parse)

After the ledger edit, re-parsing `32-ISSUE-LEDGER.md`:
- 18 rows total (no duplicate finding-ID rows, per cycle-4 HIGH-B).
- 18 VERIFIED.
- 0 PENDING.
- 0 IN_PROGRESS.
- 0 FIX_APPLIED.
- 0 DEFERRED.

Ledger is **TERMINAL** (VER-16 satisfied).

### Demote-on-regression check

No previously-VERIFIED row changed verdict or status other than the two intended promotions (D-05 and D-06 PENDING → VERIFIED). All 16 other rows remain `VERIFIED` with their existing `accept-resolution` / `defer-with-blocker` verdicts preserved.

### Post-write SHA-256

- **Post-write SHA-256 of `32-ISSUE-LEDGER.md`:** `184cb56ff62caba140e9f35e9ddd857cd924d56354eed49f6de7d4144b5a7e10`.
- **Freshness-check status:** post-write hash differs from pre-write (as expected — only those two rows were edited). Hashes were captured before and after the edit by independent `sha256sum` invocations.

## Artifacts

| Artifact | Path |
|----------|------|
| Closure record | `.planning/phases/36-acceptance-checks-re-verification-handoff/36-LEDGER-CLOSURE.md` (this file) |
| Phase 32 issue ledger (terminal) | `.planning/phases/32-evidence-framework-issue-ledger-conflict-adjudication/32-ISSUE-LEDGER.md` (D-05/D-06 promoted to VERIFIED) |
| D-05 transcription probe evidence | `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-EVID-15-D05.stdout.txt` (SHA-256 `e6ccc642e55591f8f42612e9cc045517b1892677fdda1bc1b73d4de5f3d8c77f`) |
| D-06 transcription probe evidence | `.planning/phases/36-acceptance-checks-re-verification-handoff/evidence/AC-EVID-15-D06.stdout.txt` (SHA-256 `f915c08041f9e092bf73f7dfa9a292333e255d601aa2cd8f679b3eaac0490f61`) |
