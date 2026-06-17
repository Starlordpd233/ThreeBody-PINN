# Phase 29: Acceptance Checks, Re-verification, and Handoff - Research

**Researched:** 2026-06-17
**Domain:** Milestone-closure verification engineering for a spec-adjudication milestone (v1.5) — acceptance-suite re-execution via disposable grep/dataset probes, issue-ledger terminal-state audit, SI-ledger reconciliation, FUT-01 handoff packaging, milestone-closure gate definition.
**Confidence:** HIGH (the phase is governance/verification over existing, locked artifacts; nearly every figure is grounded by direct observation or a committed planning artifact)

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions (verbatim from 29-CONTEXT.md `## Implementation Decisions`)

- **D-01 (LOCKED 2026-06-16, Option A):** Phase 29 reconciles **only the planning / governance / ledger layer** to the locked **117 validated / 67 permanent `gold_counterpart=absent` / 0 promoted** fact. It does **not** promote the 117 into canonical gold and does **not** edit framework specs or AC counts. The dataset promotion + the 184 → 67 framework-spec/AC cascade is **DEFERRED to a separate explicit user ruling** (GAP-29-01), ruled to execute at the **FUT-01 dataset-finalization gate** (`29-CODE-DIVERGENCE.md` FO-1).
  - **IN scope under D-01:** issue-ledger gold rows (M13/G4) keep `VERIFIED` + OI-7b-partial note; GAP-28-03 + GAP-26-01 rationale reframed; STATE.md gold-framing reconciled; `29-UAT.md` gold-completeness reconciliation table + stale-artifact inventory.
  - **OUT of scope under D-01 (DEFERRED → GAP-29-01):** promote the 117 (gold stays 2,565); edit `standard_quasi_random_ids_not_in_gold.md` (stays 184); `ctl_instruction.md` Step 5 gold note (stays KNOWN-STALE); Set-2b/issue-02 counts (stay 2,565); `AC-PIPE-05` assertion + runner `EXPECTED_ID_COUNT` (stay 184).
- **D-01a:** The M13/GAP-26-01 packet factual-outcome update ("OI-7b executed partial") is planning-layer reconciliation **grounded by `29-SPEC.md`**; the LOCKED M13 *verdict* (Option B — re-simulate, no base→gold substitution) is **untouched**. If a packet edit reads as *re-adjudication*, **STOP and re-surface**.
- **D-02:** Re-run the **full** applicable `AC-PIPE-*` / `AC-VAL-*` suite. Each `29-UAT.md` row records command/function, input data, pass criterion, result, evidence path. Probes are disposable; **no probe touches `pinn/`** (VER-09).
- **D-03:** `AC-PIPE-05` reruns and is recorded **PASS at 184/184** — internally consistent precisely because no promotion occurs under D-01. Note it moves to 67/67 only when GAP-29-01 promotion lands.
- **D-04:** Acceptance checks whose owning contract is user-deferred are recorded **`DEFERRED`** with the exact blocker + decision record, never `PASS`.
- **D-05:** `29-UAT.md` carries the gold-completeness reconciliation table (184 attempted / 117 validated-staged / 67 permanent-absent / 0 promoted) with evidence paths.
- **D-06:** PSC / VAL-04 stays **`DEFERRED`** for AC-VAL-04 numeric execution; blocker reframed to "gold completeness settled; composition ratified; numeric calibration awaits the post-promotion pool." Composition is **NOT invented**.
- **D-07:** Close `24-ISSUE-LEDGER.md` only when every in-scope row is `VERIFIED` or explicitly `DEFERRED`; `29-UAT.md` carries a status-count audit confirming **zero** `PENDING`/`IN_PROGRESS`/`FIX_APPLIED` in-scope rows.
- **D-08:** Review `SI-DQA-002`, `SI-DQA-003`, `SI-PINN-002` (VER-12): each **retired-with-backref** or **preserved-with-written-reason**; none assumed resolved/irrelevant. Source-silent disposition → **surface per STOP protocol**.
- **D-09:** Emit **two** artifacts mirroring v1.4 Phase 21: `29-HANDOFF.md` (fixed/unchanged/deferred + the three SI dispositions) and `29-CODE-DIVERGENCE.md` (FUT-01 divergence — **already authored/committed**). Live `pinn/` appears ONLY as a divergence target.
- **D-10:** The GAP-29-01 deferred promotion + cascade is recorded as a forward obligation in `29-CODE-DIVERGENCE.md` (**done** — FO-1).

### Claude's Discretion (verbatim)

- Table-vs-prose formatting and section ordering within the named artifacts — mechanical; follow the v1.4 Phase 21 precedent where one exists.

### Deferred Ideas (OUT OF SCOPE — verbatim)

- **GAP-29-01 — gold promotion + 184→67 cascade** (DEFERRED to the FUT-01 dataset-finalization gate). Recorded as `29-CODE-DIVERGENCE.md` FO-1.
- **PSC / VAL-04 composition** (dedup-prefer-gold + `1/N_t`) — already ratified and landed; only the construction *constants* + the numeric AC-VAL-04 run are deferred (FO-2). Do NOT re-invent composition.
- `trainex-r1-research-handoff.md` todo — reviewed, not folded; belongs to the *trainex* track, out of Phase 29 scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description (from REQUIREMENTS.md) | Research Support |
|----|-----------------------------------|------------------|
| VER-07 | Every v1.5 contract has a numerically-defined acceptance check naming pass criterion, data, and command/function — not just prose. | The 13 AC checks already exist as numerically-defined probes; 3 persist as runnable `.sh`, the rest ran inline. The planner confirms each AC names a pass criterion + executor. See `## Acceptance-Suite Re-run Mechanics`. |
| VER-08 | The roadmap maps every v1.5 requirement to exactly one phase, beginning at Phase 23. | REQUIREMENTS.md Traceability table already maps 36/36; Phase 29 covers VER-07/08/09/11/12. Confirmation-only at closure. See `## Roadmap Traceability`. |
| VER-09 | Acceptance checks are **executed** via disposable probes, each producing recorded pass/fail evidence; a failing check blocks completion and routes back to the originating phase; probes never touch `pinn/`. | The re-run is the core Phase 29 deliverable (`29-UAT.md`). Mechanics, persistence gap, and probe model documented. See `## Acceptance-Suite Re-run Mechanics` + `## Milestone-Closure Gate`. |
| VER-11 | Milestone handoff identifies fixed / intentionally-unchanged / deferred findings; FUT-01 divergence records updated for every DataLoader-shaped finding. | `29-HANDOFF.md` (to author) + `29-CODE-DIVERGENCE.md` (done). Mirror `21-HANDOFF.md` four-section shape. See `## SI / VER-12 Dispositions` + `## Handoff Packaging`. |
| VER-12 | Remaining SI entries (`SI-DQA-002`, `SI-DQA-003`, `SI-PINN-002`) reviewed for issue-02 relevance — each retired-with-backref or preserved-with-reason; none assumed. | All three definitions located and quoted below; provenance analysis + a source-silence flag for SI-PINN-003 adjacency. See `## SI / VER-12 Dispositions`. |
</phase_requirements>

## Summary

Phase 29 is a **terminal verification/governance phase**, not a build phase. It produces four named closure artifacts — `29-SPEC.md` (done), `29-UAT.md` (to author), `29-HANDOFF.md` (to author), `29-CODE-DIVERGENCE.md` (done/committed) — that re-run the full 13-check `AC-PIPE-*`/`AC-VAL-*` acceptance suite as disposable probes, close the v1.5 issue ledger to terminal states, reconcile the three remaining `SI-*` entries, and reconcile the locked 184→67 standard-gold completeness fact at the planning layer only. No framework-spec edit, no dataset mutation, and no `pinn/` touch is in scope.

The acceptance suite is **grep-based spec-consistency probing** (positive assertions plus negative controls run over `ctl_instruction.md` and `pinn_architecture.md`) combined with **Python dataset probes** over `simulation_data/`. Only 3 of the 13 checks (`ac-pipe-04.sh`, `ac-pipe-08.sh`, `ac-pipe-09.sh`, all from Phase 27) persist as runnable scripts on disk; the other 10 ran inline during their owning phases and recorded results in plan summaries. This persistence gap is the single largest planning risk for VER-09: the planner must decide whether Phase 29 re-derives runnable probes for all 13 or accepts a mix of fresh-run + cited-prior-evidence, and `29-UAT.md` must record an *executed* result for every non-deferred row (not a re-citation of a months-old pass).

Two AC rows carry special handling. **AC-VAL-04 (PSC) is a structural/numeric SPLIT**: the PSC clause physically landed in `ctl_instruction.md` (lines 645-692, citing `psc-coverage-entropy.md`) after the SPEC/CONTEXT were written, so the *structural* check (clause present, well-formed, cites its packet, composition matches the ratified dedup-prefer-gold + `1/N_t`) can EXECUTE and PASS in Phase 29, while the *numeric* AC-VAL-04 run DEFERS to the FUT-01 gate (FO-2) because the construction constants are provisional pending the post-promotion pool. **AC-PIPE-05 is recorded PASS at 184/184** — internally consistent *because* 0 are promoted under D-01; it moves to 67/67 only when GAP-29-01/FO-1 promotion lands.

**Primary recommendation:** Plan Phase 29 as three verification work-streams over locked inputs — (1) re-execute the 13-check AC suite into `29-UAT.md` with persisted-or-fresh disposable probes and explicit DEFERRED handling for AC-VAL-04-numeric; (2) audit the 19 ledger ROWS (not status-token counts) to confirm zero non-terminal in-scope rows; (3) author `29-HANDOFF.md` mirroring the `21-HANDOFF.md` four-section shape with explicit SI-DQA-002/003 + SI-PINN-002 rows — then define a numerically-defined milestone-closure gate whose failure routes back to the originating phase.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| AC spec-consistency re-run | Verification probe (grep over framework-specs) | — | The contracts live as text in `ctl_instruction.md`/`pinn_architecture.md`; the check is a structural assertion over that text. Disposable, no `pinn/` touch. |
| AC dataset re-run | Verification probe (Python over `simulation_data/`) | — | Set-difference / count checks (e.g. AC-PIPE-05) run against the on-disk dataset (SCOPE-06 grounding). |
| Ledger terminal-state audit | Planning/governance layer (`24-ISSUE-LEDGER.md`) | — | The ledger is the authoritative state machine; the audit enumerates each row's current Status field. |
| SI reconciliation | Framework-spec metadata + governance | — | SI entries live in `pinn_architecture.md` (SI-PINN-002) and the read-only `framework-revisions/data_quality_assessment.md` (SI-DQA-002/003); disposition is recorded in `29-HANDOFF.md`, not by editing the read-only DQA. |
| FUT-01 handoff | Forward-pointing hand-off doc | — | `29-CODE-DIVERGENCE.md` + `29-HANDOFF.md` are the only place live-`pinn/` may be referenced (SCOPE-10 carveout). |
| Gold-completeness reconciliation | Planning/governance/ledger layer ONLY (D-01) | Dataset mutation (DEFERRED → FUT-01 FO-1) | The 117-promotion + cascade is a canonical-dataset mutation, ruled to the FUT-01 gate; Phase 29 touches only planning records. |
| Milestone-closure gate | Verification artifact (`29-VERIFICATION.md`, downstream) | — | The gate's *criteria* are defined in the plan; the gsd-verifier produces the recording artifact. |

## Standard Stack

This is a verification/governance phase over an existing repo; there is no external package install. The "stack" is the repo's own probe tooling and conventions.

### Core
| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| `bash` + `grep -qE` | system | Spec-consistency probes (positive assertions + negative controls over framework-specs) | The established AC-probe pattern; see `ac-pipe-09.sh` (`27-...`). `[VERIFIED: .planning/phases/27-sampling-precision-and-global-scale-contracts/ac-pipe-09.sh]` |
| `python3` (stdlib `json`) | system | Dataset probes (counts, set-differences over `simulation_data/`) | The AC-PIPE-05 set-difference probe pattern (`base_ids − gold_ids`); reads `run_manifest.json`/`validation_summary.json`. `[VERIFIED: direct observation 2026-06-17]` |
| `scripts/agent-commit` | repo | Atomic, owned-path commits | Project git policy (CLAUDE.md); `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS` required. `[CITED: CLAUDE.md Git Commit Protocol]` |

### Supporting
| Tool | Version | Purpose | When to Use |
|------|---------|---------|-------------|
| `git log --oneline` / `git grep` | system | Back-reference resolution for SI retirement (resolving phase/commit) | When recording `retired-with-backref` SI dispositions. |
| `find ... -iname "ac-*.sh"` | system | Inventory persisted AC probes | Establishing which of the 13 checks already have runnable scripts. |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| grep spec-consistency probes | A markdown AST parser | Over-engineering; the existing AC pattern is grep + negative controls and is the established convention. Match it. |
| Re-running all 13 from fresh scripts | Citing prior inline pass evidence | VER-09 says checks must be **executed** with recorded pass/fail; a stale citation is not an execution. The planner must surface this (see Open Questions). |

**Installation:** None. No external dependency. (Environment Availability section confirms `python3`/`bash`/`git` presence is the only requirement.)

## Package Legitimacy Audit

Not applicable — Phase 29 installs no external packages. It is a verification/governance phase operating on existing repo files with system `bash`/`python3`/`git`. No npm/PyPI/crates dependency is introduced.

## Architecture Patterns

### System Architecture Diagram

```
LOCKED INPUTS (read-only grounding)
  29-SPEC.md (5 reqs) ─┐
  29-CONTEXT.md (D-01..D-10) ─┤
  29-GAPS.md (GAP-29-01 RESOLVED) ─┤
  29-CODE-DIVERGENCE.md (FO-1, FO-2 — already committed) ─┤
  24-ISSUE-LEDGER.md (19 rows) ─┤
  ctl_instruction.md / pinn_architecture.md (landed contracts) ─┤
  simulation_data/ (+ rerun_staging/...184/) ─┤
  21-HANDOFF.md / 21-CODE-DIVERGENCE.md (precedent) ─┘
                    │
                    ▼
        ┌───────────────────────────────────────┐
        │  PHASE 29 VERIFICATION WORK-STREAMS    │
        ├───────────────────────────────────────┤
        │ (A) AC SUITE RE-RUN                    │
        │   grep probes ──► ctl/arch specs       │
        │   dataset probes ──► simulation_data/  │
        │   → 13 rows: PASS / DEFERRED           │
        │       AC-VAL-04: structural PASS,      │
        │                  numeric DEFERRED      │
        │       AC-PIPE-05: PASS @184/184 (0 promoted)│
        ├───────────────────────────────────────┤
        │ (B) LEDGER ROW AUDIT                    │
        │   enumerate Status field per ROW       │
        │   → 0 PENDING/IN_PROGRESS/FIX_APPLIED   │
        │   → PSC row DEFERRED (named blocker)    │
        ├───────────────────────────────────────┤
        │ (C) SI / VER-12 RECONCILE              │
        │   SI-DQA-002/003, SI-PINN-002          │
        │   → retire-with-backref / preserve     │
        ├───────────────────────────────────────┤
        │ (D) STATE/ROADMAP RECONCILE (D-01)     │
        │   gold framing → 117/67/0-promoted     │
        │   ROADMAP progress row PSC staleness   │
        └───────────────────────────────────────┘
                    │
                    ▼
        ┌───────────────────────────────────────┐
        │  CLOSURE ARTIFACTS                     │
        │   29-UAT.md  (A + B + gold table ref)  │
        │   29-HANDOFF.md  (C + fixed/unchanged/ │
        │                   deferred + SI rows)  │
        │   [29-CODE-DIVERGENCE.md — exists]     │
        └───────────────────────────────────────┘
                    │
                    ▼
        MILESTONE-CLOSURE GATE (numerically-defined)
          all 5 reqs pass ──► v1.5 closes
          any check FAIL ──► route back to originating phase
                            (29-VALIDATION.md / 29-VERIFICATION.md
                             produced downstream by gsd-verifier)
```

### Recommended Artifact Structure

```
.planning/phases/29-acceptance-checks-re-verification-and-handoff/
├── 29-SPEC.md                # exists (locked, 5 reqs)
├── 29-CONTEXT.md             # exists (D-01..D-10)
├── 29-GAPS.md                # exists (GAP-29-01 RESOLVED)
├── 29-CODE-DIVERGENCE.md     # exists, committed (FO-1, FO-2, gold table, stale inventory)
├── 29-RESEARCH.md            # this file
├── 29-UAT.md                 # TO AUTHOR — full AC pass/fail table + ledger audit + gold-table ref
├── 29-HANDOFF.md             # TO AUTHOR — fixed/unchanged/deferred + 3 SI dispositions
└── (optional) ac-*.sh probes # if planner re-derives runnable scripts for VER-09
```

### Pattern 1: grep spec-consistency probe (positive + negative control)
**What:** A bash script that asserts contract text is present in the framework-spec (positive) and that a rejected convention appears ONLY in rejection context (negative control).
**When to use:** Every `AC-*` check that asserts a spec clause landed correctly.
**Example:**
```bash
# Source: .planning/phases/27-sampling-precision-and-global-scale-contracts/ac-pipe-09.sh [VERIFIED]
CTL="pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md"
grep -qE '4\.6416' "$CTL" && echo "[2] PASS: D=4.6416" || { echo "[2] FAIL"; ERR=1; }
# Negative control: 6.694 must appear only in a rejection context
NL=$(grep -nE '6\.694' "$CTL")
if [ -n "$NL" ] && [ -z "$(echo "$NL" | grep -vE 'reject|prohibit|alternative|anti-pattern')" ]; then
    echo "[7] PASS: 6.694 only in rejection"
else echo "[7] FAIL"; ERR=1; fi
```

### Pattern 2: dataset set-difference probe (AC-PIPE-05)
**What:** Compute `base_ids − gold_ids` against `simulation_data/`, cross-check against the documentation list, never hard-coded.
**When to use:** AC-PIPE-05 re-run.
**Example:**
```python
# Source: m13-gold-counterpart.md §3b (probe data03_gold_gap.py) [CITED]
# base_ids − gold_ids set size == 184; doc list lists exactly 184; intersection 184/184
# Under D-01 (0 promoted) this PASSES at 184/184 by construction.
```

### Pattern 3: four-section handoff (mirror 21-HANDOFF.md)
**What:** `## 1. Fixed`, `## 2. Intentionally Unchanged`, `## 3. Deferred`, `## 4. SI Metadata Reconciliation` (+ a `## 5. Consumption Notes` / FUT-01 note).
**When to use:** `29-HANDOFF.md`.
**Example:** `21-HANDOFF.md` lines 13-65 — fixed findings list, intentionally-unchanged statement, deferred list, SI reconciliation table with `Entry | Status | Evidence`. `[VERIFIED: 21-HANDOFF.md]`

### Anti-Patterns to Avoid
- **Counting status tokens instead of rows.** A raw grep over `24-ISSUE-LEDGER.md` returns ~71 "PENDING", 35 "IN_PROGRESS", 27 "FIX_APPLIED" — these are matches over the **per-row status-transition log narrative**, NOT live row statuses. The audit MUST read the current Status field of each row in the Status Table (lines 21-41). `[VERIFIED: direct observation — the transition logs narrate `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED` history per row]`
- **Re-citing months-old inline pass evidence as an "execution."** VER-09 requires executed pass/fail evidence; the planner must fresh-run probes or surface the persistence gap.
- **Promoting the 117 / editing `not_in_gold.md` / flipping AC-PIPE-05 to 67/67.** All DEFERRED to FUT-01 FO-1 (D-01). Doing any of these in Phase 29 violates the locked decision and breaks the set-difference invariant.
- **Re-adjudicating the M13 verdict.** The packet update is factual-outcome only (D-01a); if an edit reads as re-adjudication, STOP.
- **Inventing PSC composition or constants.** Composition is ratified and landed; constants are provisional → FUT-01 FO-2. Do not numerically run AC-VAL-04 in Phase 29.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| AC spec-consistency check | A new markdown parser / AST validator | grep `-qE` positive + negative-control pattern (`ac-pipe-09.sh`) | The established convention; negative controls already encode the rejection-context discipline. |
| Ledger status audit | A bespoke state-machine re-implementation | Read the Status Table column directly + the Lifecycle Rules block | The ledger IS the state machine; re-deriving it risks miscounting. |
| Gold reconciliation table | A fresh derivation of the 117/67 split | Reference the table already in `29-CODE-DIVERGENCE.md` (FO-1) | The settled table exists; `29-UAT.md` references it (per the GAP-29-01 resolution note), it does not duplicate it. |
| Handoff structure | A new doc schema | Mirror `21-HANDOFF.md` four-section shape (D-09) | Precedent locked; planner discretion is formatting only. |
| Staging counts | Re-running the 184 reruns | Read `validation_summary.json` (`passes:117, failures:67, total:184`) | The rerun is done; re-running is explicitly out of scope (no retry). |

**Key insight:** Almost everything Phase 29 needs is already produced and locked. The phase's value is *verification rigor over existing artifacts*, not new derivation. The single genuinely-new engineering task is deciding the VER-09 re-execution model (persist runnable probes vs. fresh-run-and-record).

## Runtime State Inventory

> This phase is governance/verification, not a rename/refactor. But because it reconciles a stale-state boundary (the 184→67 gold framing), the following inventory is included for the reconciliation surface.

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data (staging) | `simulation_data/Data/rerun_staging/standard_gold_missing_184/` — `outputs/` (184 dirs), `run_manifest.json` (313KB, 184 per-ID entries), `validation_summary.json` (`passes:117, failures:67, total:184`). 0 promoted to canonical gold. `[VERIFIED: direct observation 2026-06-17]` | Reference as evidence in `29-UAT.md`; promotion DEFERRED to FUT-01 FO-1. Interim durability backup of the 117 + manifest is a FO-1 "do NOW" item. |
| Stale planning records (left intentionally) | `standard_quasi_random_ids_not_in_gold.md` (still "184 IDs"); `ctl_instruction.md` Step 5 gold note ("backlog expected empty"); Set-2b/issue-02 counts (2,565); AC-PIPE-05 assertion + runner `EXPECTED_ID_COUNT` (184). All KNOWN-STALE under D-01. `[CITED: 29-CODE-DIVERGENCE.md stale-record inventory]` | List each in the `29-UAT.md` stale-artifact inventory with `deferred → GAP-29-01/FO-1` marker. Do NOT edit. |
| Stale planning records (to reconcile NOW, D-01 in-scope) | STATE.md gold framing — **already reconciled** (STATE.md now reads "Gold is final in shape: 117 validatable + 67 permanent-absent"). `[VERIFIED: STATE.md L31]` ROADMAP Progress row for Phase 28 still reads "3/4 ... VAL-04/PSC user-deferred (GAP-28-03)" with footer "Last updated 2026-06-14" — STALE re: PSC resolution. `[VERIFIED: ROADMAP.md L309, L313]` | Reconcile the ROADMAP Phase 28 progress row + footer to reflect PSC landed (4/4 contracts) and Phase 29 in progress. |
| Live service config | None — no external service holds v1.5 state. | None — verified by absence of any service-config reference in the phase scope. |
| Secrets/env vars | None. | None. |
| Build artifacts | The rerun runner `rerun_standard_gold_missing_184.py` (+ its test) is **untracked** (git status). FO-1 step 1 notes it must be preserved/committed before the FUT-01 gate. `[VERIFIED: git status — `?? simulation_data/Scripts/brutus_runners/rerun_standard_gold_missing_184.py`]` | Phase 29 may commit the runner under owned paths if desired, but promotion stays deferred. Surface as a durability note. |

## Common Pitfalls

### Pitfall 1: Token-count ledger audit
**What goes wrong:** Counting "PENDING"/"IN_PROGRESS"/"FIX_APPLIED" string occurrences yields ~71/35/27 hits and falsely suggests dozens of open rows.
**Why it happens:** Each row carries a multi-line status-transition log narrating its full `PENDING→...→VERIFIED` history; those words appear in history even for VERIFIED rows.
**How to avoid:** Audit the **Status column of the Status Table** (lines 21-41) — there are 19 rows; 18 are VERIFIED, 1 (PSC) is DEFERRED. Cross-check the Lifecycle Rules phase-exit gate (only VERIFIED/DEFERRED permitted).
**Warning signs:** Any audit count > 19, or a "PENDING" count not equal to 0 at the row level.

### Pitfall 2: Treating AC-VAL-04 as a blanket DEFER
**What goes wrong:** The SPEC/CONTEXT (written 2026-06-16) say "PSC stays fully DEFERRED." Recording AC-VAL-04 as fully deferred now under-reports the state — the PSC clause has since LANDED in `ctl_instruction.md`.
**Why it happens:** GAP-28-03 was REOPENED and RESOLVED *after* the SPEC/CONTEXT were authored (commits `6eae6422`, `a511c60d`).
**How to avoid:** Record AC-VAL-04 as a SPLIT — structural check EXECUTES + PASSES in Phase 29 (clause present at `ctl_instruction.md:645-692`, well-formed, cites `psc-coverage-entropy.md`, composition = ratified dedup-prefer-gold + `1/N_t`); numeric calibration + numeric AC-VAL-04 run DEFER to FUT-01 FO-2.
**Warning signs:** An AC-VAL-04 row marked `DEFERRED` with no structural sub-result, or a blocker citing "wait for gold completion" (the old, superseded blocker).

### Pitfall 3: Recording AC-PIPE-05 as inconsistent
**What goes wrong:** Reading "184/184" as wrong because the rerun produced 117 successes.
**Why it happens:** Conflating staging validation with canonical promotion.
**How to avoid:** Under D-01, 0 are promoted, so `gold = 2,565` and `base − gold = 184` still holds exactly. AC-PIPE-05 PASS at 184/184 is correct *and* internally consistent. Note it flips to 67/67 only when FO-1 promotion lands.
**Warning signs:** An AC-PIPE-05 row marked FAIL, or an edit to `EXPECTED_ID_COUNT`.

### Pitfall 4: VER-09 satisfied by citation
**What goes wrong:** `29-UAT.md` rows cite the original phase's inline pass without a fresh execution.
**Why it happens:** Only 3 of 13 checks persist as runnable scripts; re-running the other 10 requires re-deriving probes.
**How to avoid:** Decide the re-execution model in the plan and execute it; every non-deferred row gets a fresh recorded result. Surface the persistence gap explicitly.
**Warning signs:** A `29-UAT.md` "result" column that points only to a `2026-06-13`/`-14`/`-16` commit with no Phase-29-dated run.

### Pitfall 5: Editing the read-only DQA during SI reconciliation
**What goes wrong:** Updating SI-DQA-002/003 notes in `framework-revisions/data_quality_assessment.md`.
**Why it happens:** SI reconciliation feels like it should edit the SI's home file.
**How to avoid:** SCOPE-09 makes `data_quality_assessment.md` read-only. The disposition (retire-with-backref / preserve-with-reason) is recorded in `29-HANDOFF.md`, exactly as `21-HANDOFF.md` did (it recorded SI dispositions in a table, citing line ranges, without editing the SI homes for "preserved" entries).
**Warning signs:** Any edit to a file under `framework-revisions/` or `sampling_method.md`.

## Code Examples

### Ledger row-status audit (correct method)
```python
# Audit the Status Table ROWS, not status-token occurrences.
# Status Table: 24-ISSUE-LEDGER.md lines 21-41 (19 rows).
# Expected terminal state at closure:
#   18 rows VERIFIED, 1 row (PSC) DEFERRED, 0 PENDING/IN_PROGRESS/FIX_APPLIED.
# Source: 24-ISSUE-LEDGER.md Status Table [VERIFIED: direct read]
rows = {
  "B-06":"VERIFIED","B-11":"VERIFIED","M11":"VERIFIED","M12":"VERIFIED","M13":"VERIFIED",
  "D7":"VERIFIED","G1":"VERIFIED","G2":"VERIFIED","G3":"VERIFIED","G4":"VERIFIED","G5":"VERIFIED",
  "SCS":"VERIFIED","SASD":"VERIFIED","IPR":"VERIFIED","PSC":"DEFERRED",
  "D-03":"VERIFIED","D=6.694":"VERIFIED","footer":"VERIFIED","mass-drift":"VERIFIED",
}
nonterminal = [k for k,v in rows.items() if v not in ("VERIFIED","DEFERRED")]
assert nonterminal == []      # closure gate
deferred = [k for k,v in rows.items() if v=="DEFERRED"]   # ["PSC"] — name blocker: GAP-28-03 numeric calibration → FUT-01 FO-2
```

### Staging-evidence count derivation (no raw JSON into context)
```python
# Source: direct observation 2026-06-17 [VERIFIED]
import json
b="simulation_data/Data/rerun_staging/standard_gold_missing_184/"
vs=json.load(open(b+"validation_summary.json"))  # keys: details, failures, passes, total
assert (vs["passes"], vs["failures"], vs["total"]) == (117, 67, 184)
rm=json.load(open(b+"run_manifest.json"))         # 184 per-ID entries (one key per ID)
assert len(rm) == 184
```

## State of the Art

| Old Approach (pre-Phase-29 state) | Current Approach | When Changed | Impact |
|--------|------------------|--------------|--------|
| PSC/VAL-04 fully DEFERRED (GAP-28-03) | PSC clause LANDED in `ctl_instruction.md:645-692`; composition ratified; constants provisional→FUT-01 | 2026-06-16/17, commits `6eae6422`, `a511c60d` | AC-VAL-04 becomes a structural-PASS + numeric-DEFER split, not a blanket defer. |
| "gold eventually completable to 184" | "gold final in shape: 117 validatable + 67 permanent-absent; promotion deferred" | 2026-06-14 ruling; STATE.md reconciled | Stale-artifact inventory required; AC-PIPE-05 stays 184/184 under 0-promoted. |
| ROADMAP Phase 28 row "3/4 ... PSC user-deferred", footer 2026-06-14 | (to reconcile) 4/4 contracts; Phase 29 in progress | pending Phase 29 | A D-01 in-scope reconciliation item. |

**Deprecated/outdated:**
- The SPEC/CONTEXT phrasing "PSC stays fully DEFERRED (GAP-28-03)" — partially superseded (see above). The PSC *numeric calibration* and AC-VAL-04 *numeric run* remain deferred; the *clause* and *composition* are landed/ratified.
- The ROADMAP Progress footer "Last updated 2026-06-14" — stale re: Phase 28 PSC landing and Phase 29 start.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | All 19 ledger rows are terminal at Phase 29 start (18 VERIFIED + 1 DEFERRED). | Code Examples / Ledger audit | LOW — directly read from the Status Table; if a row regressed, the audit catches it (that is the audit's job). |
| A2 | The 10 non-persisted AC checks (all except AC-PIPE-04/08/09) ran inline in their owning phases and recorded results in summaries, with no committed runnable script. | Acceptance-Suite Re-run Mechanics | MEDIUM — confirmed by `find` returning only 3 scripts + Phase 28 summaries recording AC-VAL inline; if a script exists elsewhere the planner should still re-run. Drives the VER-09 re-execution decision. |
| A3 | The `29-UAT.md` gold-completeness reconciliation table should REFERENCE the table already in `29-CODE-DIVERGENCE.md` FO-1 rather than duplicate it. | Don't Hand-Roll | LOW — the GAP-29-01 resolution note explicitly says the table was "placed there rather than `29-UAT.md`, since the full Phase 29 UAT ... is Phase 29 execution work; `29-UAT.md` references the divergence doc." `[CITED: 29-GAPS.md resolution note]` |
| A4 | The milestone-closure gate's recording artifact is `29-VERIFICATION.md` (gsd-verifier downstream); the PLAN defines the gate criteria. | Milestone-Closure Gate | LOW — matches the v1.4 Phase 21 shape (`21-VERIFICATION.md`/`21-VALIDATION.md`). |

**No `[ASSUMED]`-tagged factual figures.** Every count (117/67/184, 13 ACs, 19 rows, 36 reqs, 10 gaps) is `[VERIFIED: direct observation]` or `[CITED: <artifact>]`. The assumptions above are about *method/scope*, not about contested facts.

## Open Questions

1. **VER-09 re-execution model — fresh-run vs. cite-prior.**
   - What we know: only `ac-pipe-04.sh`, `ac-pipe-08.sh`, `ac-pipe-09.sh` persist as runnable scripts; the other 10 checks ran inline. VER-09 requires checks to be **executed** with recorded pass/fail evidence.
   - What's unclear: whether Phase 29 must re-derive runnable probes for all 13 (most rigorous, satisfies VER-09 cleanly) or may fresh-run a subset and cite well-documented prior passes for the rest.
   - Recommendation: Plan to re-derive lightweight grep/dataset probes for all 13 and record fresh Phase-29-dated results. This is mechanical (the assertions already exist in each finding's evidence packet/summary) and removes any doubt about VER-09. If the planner chooses the subset path, it must be an explicit, justified plan decision — not a silent shortcut. **This is a process-schema choice; if the planner is unsure whether cite-prior satisfies VER-09, surface per STOP protocol.**

2. **ROADMAP reconciliation scope (D-01 in-scope edit).**
   - What we know: D-01 includes "STATE.md gold-framing reconciled" (done) but the CONTEXT does not name the ROADMAP Progress row explicitly. The orchestrator flagged the ROADMAP Phase 28 row + footer as a "candidate reconciliation item."
   - What's unclear: whether the ROADMAP progress-row reconciliation (PSC landed; footer date) is a Phase 29 in-scope edit or a separate housekeeping commit.
   - Recommendation: Treat it as Phase 29 in-scope governance reconciliation (it is a planning-layer record, exactly the D-01 surface), under a `docs(planning)`/`verify(29)` commit. It is mechanical and grounded by the committed PSC landing — low STOP-risk. Confirm in the plan.

3. **AC-VAL-04 structural-PASS authority.**
   - What we know: the PSC clause is landed and well-formed (`ctl_instruction.md:645-692`, cites `psc-coverage-entropy.md`); composition is ratified.
   - What's unclear: whether a *structural* AC-VAL-04 PASS in Phase 29 (clause present, composition matches ratified rule) is within scope given VAL-04's ledger row is `DEFERRED`.
   - Recommendation: Yes — record AC-VAL-04 as structural-PASS / numeric-DEFERRED, with the numeric run cited to FUT-01 FO-2. This matches the FO-2 note ("AC-VAL-04 structural check executes in Phase 29; numeric sanity executes [at the FUT-01 gate]"). The ledger PSC row may stay `DEFERRED` (numeric authority pending) while the structural check passes — the planner should make this two-axis status explicit and, if it reads as resolving a deferred contract, surface per STOP.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `bash` + `grep` | spec-consistency probes | ✓ | system | — |
| `python3` (stdlib `json`) | dataset/staging probes | ✓ | system (`python3` ran the staging derivation this session) | — |
| `git` / `scripts/agent-commit` | commits, back-ref resolution | ✓ | repo hooks present (`.githooks`) | — |
| `simulation_data/Data/rerun_staging/standard_gold_missing_184/` | gold-reconciliation evidence | ✓ | `outputs/` + `run_manifest.json` (313KB) + `validation_summary.json` (73KB) | — |
| `ctl_instruction.md` PSC clause | AC-VAL-04 structural check | ✓ | lines 645-692, cites `psc-coverage-entropy.md` | — |

**Missing dependencies with no fallback:** None.
**Missing dependencies with fallback:** None. All inputs are present and grounded.

## Validation Architecture

> nyquist_validation is enabled (no `workflow.nyquist_validation:false` found in config). This section maps each Phase 29 requirement/decision to a concrete validation method and observable evidence.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Disposable acceptance probes — `bash`+`grep -qE` spec-consistency checks and `python3` dataset checks (the established AC-PIPE/AC-VAL pattern). No xUnit framework; the "tests" are the AC probes. |
| Config file | None — probes are standalone scripts (e.g. `ac-pipe-09.sh`) or inline blocks recorded in `29-UAT.md`. |
| Quick run command | `bash .planning/phases/27-*/ac-pipe-09.sh` (example of the persisted pattern) |
| Full suite command | (to define in plan) a `29-UAT` driver re-running all 13 AC probes and emitting a pass/fail table — see Wave 0 gap. |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | Evidence Exists? |
|--------|----------|-----------|-------------------|------------------|
| VER-07 | Each of 13 ACs names pass criterion + data + executor | structural review | inspect each AC row in `29-UAT.md` | ✅ ACs defined; ❌ unified table is Wave 0 |
| VER-09 | 13 ACs executed as disposable probes, recorded pass/fail | spec+dataset probe | re-run probes → `29-UAT.md` | ⚠️ 3/13 persisted (`ac-pipe-04/08/09.sh`); 10/13 need re-derivation (Wave 0) |
| VER-09 (AC-PIPE-05) | `base−gold == not_in_gold.md` (184/184, 0 promoted) | dataset probe | Python set-difference over `simulation_data/` | ✅ pattern exists (`data03_gold_gap.py`); ❌ fresh run Wave 0 |
| VER-09 (AC-VAL-04) | PSC clause present/well-formed/cites packet (structural); numeric DEFERRED | grep structural probe | grep over `ctl_instruction.md:645-692` | ✅ clause landed; ❌ structural probe Wave 0 |
| VER-11 | Handoff lists fixed/unchanged/deferred + FUT-01 divergence | doc-structure review | inspect `29-HANDOFF.md` vs `21-HANDOFF.md` shape | ❌ `29-HANDOFF.md` Wave 0; `29-CODE-DIVERGENCE.md` ✅ exists |
| VER-12 | 3 SI entries each retired-with-backref or preserved-with-reason | doc-structure review | inspect `29-HANDOFF.md` §SI table | ❌ Wave 0 (definitions located; dispositions to record) |
| VER-08 | 36/36 reqs map to exactly one phase | traceability review | inspect REQUIREMENTS.md Traceability table | ✅ 36/36 mapped; confirmation-only |
| D-07 (ledger) | 0 non-terminal in-scope rows; PSC DEFERRED named | row-status audit | enumerate Status Table rows (19) | ✅ rows terminal; ❌ audit recorded in `29-UAT.md` Wave 0 |

### Sampling Rate
- **Per task commit:** re-run the AC probe(s) the commit touched + the ledger row-audit if a ledger row was edited.
- **Per artifact (UAT / HANDOFF):** full 13-check AC re-run + full 19-row ledger audit.
- **Phase gate:** all 13 AC rows PASS-or-explicitly-DEFERRED, 0 non-terminal ledger rows, 3 SI dispositions recorded, traceability confirmed — before `/gsd-verify-work`.

### Wave 0 Gaps
- [ ] `29-UAT.md` — full AC pass/fail table (13 rows) + ledger row-status audit + gold-table reference. Covers VER-07/09 + D-07.
- [ ] Re-runnable probes (or inline recorded runs) for the 10 non-persisted ACs (AC-PIPE-01/02/03/05/06/07/10, AC-VAL-01/02/03) + the AC-VAL-04 structural probe. Covers VER-09.
- [ ] `29-HANDOFF.md` — fixed/unchanged/deferred sections + SI-DQA-002/003 + SI-PINN-002 dispositions. Covers VER-11/12.
- [ ] ROADMAP Phase 28 progress row + footer reconciliation (PSC landed; Phase 29 in progress). Covers D-01 in-scope reconciliation.
- [ ] Milestone-closure gate definition (the 5-requirement pass/fail criteria + the route-back-on-fail rule). Covers VER-09 routing clause.

*(STATE.md gold-framing reconciliation is already done — STATE.md L31 reads "Gold is final in shape: 117 validatable + 67 permanent-absent.")*

## Security Domain

> `security_enforcement` is not a configured concern for this milestone (no auth/session/crypto/input-validation surface — the phase reads planning artifacts and the on-disk dataset, edits no executable code, installs no package, exposes no endpoint).

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | — |
| V3 Session Management | no | — |
| V4 Access Control | no | — |
| V5 Input Validation | no | The phase consumes trusted local repo artifacts only. |
| V6 Cryptography | no | — |

**Governance-integrity controls (project-specific, the relevant analogue):**

| Pattern | Risk | Standard Mitigation |
|---------|------|---------------------|
| Silent invention where source is silent | Spec drift across the terminal milestone | STOP protocol (CLAUDE.md) — surface gaps, never invent. AC-VAL-04 composition, the 67 holes, and the 117 promotion are all locked/deferred and must not be re-decided. |
| Re-adjudicating a LOCKED verdict (M13) | Corrupts a settled ruling at closure | D-01a — packet edits are factual-outcome only; STOP if an edit reads as re-adjudication. |
| Touching `pinn/` during probes | SCOPE-10 violation | VER-09 / SPEC Constraint — probes never touch `pinn/`; live-`pinn/` references only in `29-CODE-DIVERGENCE.md`/`29-HANDOFF.md`. |
| Editing frozen/read-only specs | SCOPE-08/09 violation | `sampling_method.md` frozen, `data_quality_assessment.md` read-only — SI dispositions recorded in `29-HANDOFF.md`, not in the SI homes. |
| Broad git staging | Committing unrelated user changes | Project git policy — `scripts/agent-commit`, explicit owned paths, `GIT_AGENT_ID`/`GIT_AGENT_OWNED_PATHS`; the working tree has untracked user files (rerun runner, review dirs) that must NOT be swept in. |

## Acceptance-Suite Re-run Mechanics (detailed — the core VER-09 deliverable)

The full applicable suite is **13 checks**: `AC-PIPE-{01,02,03,04,05,06,07,08,09,10}` + `AC-VAL-{01,02,03,04}`. Note **AC-PIPE-08 DOES exist** as a runnable probe (`ac-pipe-08.sh`, PIPE-08 stage-query contract, PASSED 2026-06-14) — it simply has no dedicated *ledger row* (PIPE-08 metadata-consistency is recorded as a note under the G5 row). The orchestrator note's "no AC-PIPE-08" refers to the ledger-row absence, not a missing check. `[VERIFIED: .planning/phases/27-.../ac-pipe-08.sh; 27-03-SUMMARY.md]`

| AC | Asserts | Executor (probe) | Input data | Pass criterion | Persisted? | Phase-29 disposition |
|----|---------|------------------|-----------|----------------|-----------|----------------------|
| AC-PIPE-01 | Step-1A admission gate (B-06/G1) present | grep spec-consistency | `ctl_instruction.md` Step 1A | clause present, 7-clause gate | ❌ inline (Ph26) | re-run grep → PASS |
| AC-PIPE-02 | ID-resolution contract (B-11/G2) present | grep + CLM-01/04 dataset | `ctl_instruction.md` Step 1 item 7; `simulation_data/` | clause present; ID≠index | ❌ inline (Ph26) | re-run → PASS |
| AC-PIPE-03 | Blacklist-exclusion contract (M11/G3) present | grep + CLM-03 dataset | `ctl_instruction.md` Step-1A; blacklist (65 IDs) | clause present | ❌ inline (Ph26) | re-run → PASS |
| AC-PIPE-04 | `n_pts=min(cap,n_snapshots)` (M12/G5) | grep (8 assertions) | `ctl_instruction.md` Mini-Batch | 8/8 assertions | ✅ `ac-pipe-04.sh` | re-run → PASS |
| AC-PIPE-05 | `base−gold == not_in_gold.md` (M13/G4) | Python set-difference | `simulation_data/`; `not_in_gold.md` | 184/184, intersection exact | ❌ inline (Ph26, `data03_gold_gap.py`) | re-run → **PASS @184/184** (0 promoted; D-03) |
| AC-PIPE-06 | Footer/param-provenance contract (D7) | grep + footer dataset | `ctl_instruction.md` Step 1 item 3, §2.6 | clause + tol-decomposition | ❌ inline (Ph26) | re-run → PASS |
| AC-PIPE-07 | Precision contract (footer/mass-drift) | grep + DATA-05 state | `ctl_instruction.md` §2.1 | clause present; post-rerun partition | ❌ inline (Ph27) | re-run → PASS |
| AC-PIPE-08 | Stage-query interface (`sample_replay`/`sample_lookahead`) | grep signatures | `ctl_instruction.md` §2.6 | signatures + param_provenance + doc-03 ref | ✅ `ac-pipe-08.sh` | re-run → PASS |
| AC-PIPE-09 | `compute_globals` raw-mass D≈4.6416 | grep + negative controls | `ctl_instruction.md` §2.5 | 8 checks incl. 6.694-rejection negative control | ✅ `ac-pipe-09.sh` | re-run → PASS |
| AC-PIPE-10 | HDF5-canonical format decision (D-03) | grep | `ctl_instruction.md` Step 1 item 6 | clause names HDF5 + round-trip | ❌ inline (Ph26) | re-run → PASS |
| AC-VAL-01 | SCS gate `SCS>-5`/`ε_H>1e-5` (SCS) | grep (6 assertions + neg control) | `ctl_instruction.md` Step-1A | 6/6 + ratio-threshold rejected | ❌ inline (Ph28, recorded in 28-01-SUMMARY.md) | re-run → PASS |
| AC-VAL-02 | SASD both-endpoint contract | grep | `ctl_instruction.md` Step-1A subsection | clause present, both-endpoint | ❌ inline (Ph28) | re-run → PASS |
| AC-VAL-03 | IPR raw G=1 units + dual-epsilon note | grep | `ctl_instruction.md` Step-1A; `pinn_architecture.md` §3.4 | clause present, raw units | ❌ inline (Ph28) | re-run → PASS |
| AC-VAL-04 | PSC clause present/well-formed/cites packet | grep (structural) | `ctl_instruction.md:645-692` | clause present; composition=dedup-prefer-gold + 1/N_t; cites `psc-coverage-entropy.md` | ❌ (clause landed post-Ph28) | **STRUCTURAL re-run → PASS; NUMERIC → DEFERRED (FUT-01 FO-2)** |

**Persistence finding (drives VER-09 plan):** 3/13 persisted as `.sh`; 10/13 ran inline. The planner must re-derive grep/dataset probes (or re-run the inline blocks) for the 10, recording Phase-29-dated PASS evidence. The assertions are already specified in each finding's evidence packet/summary, so re-derivation is mechanical.

## Ledger-Close Audit Method (VER-10/D-07 surface)

- **Row schema (Status Table, lines 21-41):** `ID | Title | Phase | Status | Verdict | Sources Disagree? | Evidence Packet | Acceptance Check | Spec Section | Dependents | Last Updated`. **19 rows.**
- **Lifecycle Rules (lines 72-82):** forward path `PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`; `DEFERRED` is absorbing + requires a written blocker; `FIX_APPLIED` is not closure; phase-exit permits only `VERIFIED`/`DEFERRED`.
- **Correct enumeration:** read the Status column per row. Current terminal state: **18 VERIFIED + 1 DEFERRED (PSC) = 19; 0 PENDING/IN_PROGRESS/FIX_APPLIED.** Do NOT count status tokens in the per-row transition logs.
- **PSC DEFERRED blocker (reframe per D-06):** name it "PSC composition ratified + clause landed; AC-VAL-04 numeric calibration + numeric run await the post-promotion pool at the FUT-01 dataset-finalization gate (FO-2)" — NOT the old "wait for gold completion."
- **M13/G4 OI-7b-partial note (D-01/D-01a):** both rows stay VERIFIED; the OI-7b-partial reconciliation note (117 validated-staged, 67 permanent-absent, 0 promoted; promotion ruled to FUT-01) is **already present** in the ledger (M13 row lines 239-247; G4 row lines 335-338). Phase 29 confirms it reads as a factual-outcome record, not re-adjudication. If it reads as re-adjudication of the `accept-third-position`/Option-B verdict → STOP (D-01a).

## SI / VER-12 Dispositions (definitions located + analysis)

All three SI definitions are located. **Note the home-file paths:** SI-PINN-002 lives in the editable spec `pinn_architecture.md`; SI-DQA-002/003 live in the **read-only** `framework-revisions/data_quality_assessment.md` (NOT `framework-specs/` — SCOPE-09). Dispositions are recorded in `29-HANDOFF.md`, mirroring `21-HANDOFF.md`'s SI table; do not edit the read-only DQA.

| SI Entry | Definition (verbatim gist) | Home | Issue-02 relevance | Suggested disposition (planner confirms) |
|----------|---------------------------|------|--------------------|------------------------------------------|
| `SI-DQA-002` | "Superseded — initial audit missed SCS gate inconsistency" — Phase 11 recorded "no source-level concerns" on the SCS gate; that was incorrect; see SI-DQA-003 for the correction. `[VERIFIED: data_quality_assessment.md:318-322]` | `framework-revisions/data_quality_assessment.md` (read-only) | HIGH — directly about the SCS gate that v1.5 VAL-01 adjudicated (EVID-10, `SCS>-5`). | **Retired-with-backref** to VAL-01 / SCS ledger row / commit `bd31dcd` — the SCS gate inconsistency is now resolved in `ctl_instruction.md`. Confirm the backref target. |
| `SI-DQA-003` | "Source-level SCS gate inconsistency corrected" — distinguishes raw drift `ε_H` from `SCS=log10(ε_H)`; gate now `ε_H>1e-5`≡`SCS>-5`; Reject tightened `SCS>-4`→`SCS>-5`. `[VERIFIED: data_quality_assessment.md:324-328]` | `framework-revisions/data_quality_assessment.md` (read-only) | HIGH — this IS the corrected SCS gate v1.5 VAL-01 canonicalized into `ctl_instruction.md`. | **Retired-with-backref** to VAL-01 (the gate is now canonical in the live spec, not just the DQA historical home). The SCS ledger row already names DQA as the "read-only/historical home." Confirm. |
| `SI-PINN-002` | "Author comments preserved in converted body" — 3 `\authcomment{}` editorial notes preserved as bold-bracketed text (omega_0 detail; hidden-layer detail; "batch construction not consistent with CTL instruction plan"). Status: "Documented for future reconciliation — author should resolve before training implementation." `[VERIFIED: pinn_architecture.md:996-1004]` | `pinn_architecture.md` (editable spec) | LOW-to-NONE for issue-02 (data-pipeline) — these are architecture-side author comments, NOT data-pipeline findings. The 3rd comment ("batch construction inconsistent with CTL") is adjacent to data-side mini-batch construction but is an FUT-05/training-implementation reconciliation item, already routed there in v1.4. | **Preserved-with-reason** — out of issue-02 scope; carry forward to FUT-05 (author-comment adjudication, deferred in v1.4 Phase 22) / training implementation. **21-HANDOFF.md already recorded SI-PINN-002 as "Preserved untouched."** Confirm this remains correct under v1.5. |

**Source-silence flags for the planner (surface per STOP, do not invent):**
- **SI-PINN-002 3rd comment ("batch construction not consistent with CTL instruction plan").** v1.5 *did* land the M12 mini-batch construction contract (`n_pts=min(cap,n_snapshots)`). Whether that discharges the author comment, or whether the comment still flags an unresolved training-side inconsistency, is **not explicitly answered** by any grounding source. The safe disposition is "preserved-with-reason (FUT-05/training-impl)" — but if the planner wants to mark it retired-by-M12, that is a **semantic judgment the sources do not make → surface per STOP protocol (D-08).**
- **SI-PINN-003** ("Batch construction inconsistency with CTL instruction plan", `pinn_architecture.md` adjacent block) is NOT in the VER-12 review list (VER-12 names only SI-DQA-002/003 + SI-PINN-002). Do not silently fold it in; it remains an FUT-05 item. If the planner believes it should be in scope, that is a scope change → surface, do not invent.

## Handoff Packaging (mirror 21-HANDOFF.md)

`29-HANDOFF.md` structure (from `21-HANDOFF.md` precedent, D-09):
1. **`## Evidence Used`** — cite `29-UAT.md`, the AC probe results, `24-ISSUE-LEDGER.md`, `29-CODE-DIVERGENCE.md`, the SI home line-ranges.
2. **`## 1. Fixed`** — the v1.5 in-scope findings that landed VERIFIED (B-06/B-11/M11/M12/M13/D7/G1-G5/SCS/SASD/IPR/D-03/D=6.694/footer/mass-drift = 18 rows).
3. **`## 2. Intentionally Unchanged`** — e.g. the KNOWN-STALE records left at pre-promotion values under D-01 (the stale-artifact inventory, cross-ref `29-CODE-DIVERGENCE.md`); the read-only DQA / frozen `sampling_method.md`.
4. **`## 3. Deferred`** — PSC numeric calibration + AC-VAL-04 numeric run (FO-2); the 117-promotion + 184→67 cascade (FO-1); doc-03 items (M16, training-side SCS/SASD/IPR/PSC).
5. **`## 4. SI Metadata Reconciliation`** — the table above (`Entry | Status | Evidence`), exactly the `21-HANDOFF.md:50-58` shape.
6. **`## 5. FUT-01 / Consumption Notes`** — point to `29-CODE-DIVERGENCE.md` FO-1/FO-2; reiterate live-`pinn/` is divergence-target only.

`29-CODE-DIVERGENCE.md` is **already authored and committed** (FO-1 promotion+cascade, FO-2 PSC numeric, gold-completeness table, stale-record inventory). Phase 29 does NOT re-author it; `29-HANDOFF.md` and `29-UAT.md` reference it.

## Milestone-Closure Gate (numerically-defined — the user's explicit ask)

The gate that lets v1.5 close confidently. The PLAN defines these criteria; the gsd-verifier records the result in `29-VERIFICATION.md`/`29-VALIDATION.md` downstream. **A failing check blocks closure and routes back to the originating phase** (VER-09 routing clause).

| # | Gate Condition (numeric) | Pass = | Route-back-on-fail target |
|---|--------------------------|--------|---------------------------|
| G1 (VER-07/09) | All 13 AC checks executed with fresh Phase-29 results | 12 PASS + 1 split (AC-VAL-04 structural PASS / numeric DEFERRED); 0 FAIL | The originating spec-edit phase (26/27/28) for any FAIL |
| G2 (VER-09) | AC-PIPE-05 dataset probe | PASS @184/184 (0 promoted; consistent under D-01) | Phase 26 (M13) if set-difference breaks |
| G3 (D-07/VER-10) | Ledger row-status audit | 19 rows; 18 VERIFIED + 1 DEFERRED; **0** PENDING/IN_PROGRESS/FIX_APPLIED | The owning phase of any non-terminal row |
| G4 (VER-12) | 3 SI dispositions recorded | SI-DQA-002, SI-DQA-003, SI-PINN-002 each retired-with-backref OR preserved-with-reason; 0 assumed | (no spec phase — record in `29-HANDOFF.md`) |
| G5 (VER-11) | Handoff completeness | `29-HANDOFF.md` has fixed/unchanged/deferred + SI table; `29-CODE-DIVERGENCE.md` FO-1/FO-2 present | — |
| G6 (VER-08) | Traceability | 36/36 reqs → exactly one phase; Phase 29 = VER-07/08/09/11/12 | roadmap revision if mismatch |
| G7 (D-05/D-01) | Gold reconciliation recorded | `29-UAT.md` references the 117/67/0-promoted table; stale-artifact inventory present; PSC numeric stays DEFERRED | — |
| G8 (governance) | No `pinn/` touch, no spec edit, no dataset mutation, no read-only/frozen-file edit | grep diff of touched paths shows only `.planning/` (+ optional probe scripts) | STOP if violated |

**Closure rule:** v1.5 closes only when G1-G8 all pass. Any G1/G2/G3 FAIL routes the specific finding back to its originating phase (26/27/28) per VER-09; v1.5 does not ship while any required check fails.

## Project Constraints (from CLAUDE.md)

- **STOP protocol in full** (v1.5 adjudication milestone): source-silent semantic / process-schema / cross-phase decisions → surface as gaps, never invent. Applies especially to: AC-VAL-04 status interpretation, SI-PINN-002 disposition, the VER-09 re-execution model.
- **SCOPE-10:** `pinn/` is NOT grounding and must not be touched; live-`pinn/` references only in `29-CODE-DIVERGENCE.md`/`29-HANDOFF.md`.
- **SCOPE-08/09:** `sampling_method.md` frozen; `data_quality_assessment.md` read-only — SI dispositions recorded in `29-HANDOFF.md`, not by editing the SI homes.
- **Spec-edit targets** are `ctl_instruction.md`/`pinn_architecture.md` only — and Phase 29 edits **neither** (D-01 keeps the gold cascade out; the PSC clause already landed in Phase 28).
- **Git policy:** `scripts/agent-commit`, explicit owned paths, `GIT_AGENT_ID`/`GIT_AGENT_OWNED_PATHS`, no broad staging. The working tree has untracked user files (the rerun runner + its test, review dirs) that must NOT be swept into Phase 29 commits. Commit message `<type>(29): <subject>`; body required for `verify`/`spec`/`plan`; on branch `milestone/v1.5` (do not push from protected branch).
- **Docs placement:** any new `docs/` artifact (none expected) follows `docs/README.md` taxonomy + frontmatter. Phase 29 artifacts live under `.planning/phases/29-.../`, not `docs/`.

## Sources

### Primary (HIGH confidence)
- `29-SPEC.md` (5 locked requirements, boundaries, acceptance criteria) — full read.
- `29-CONTEXT.md` (D-01..D-10, GAP-29-01 Option A, canonical refs) — full read.
- `29-GAPS.md` (GAP-29-01 RESOLVED + embedded promotion sub-ruling) — full read.
- `29-CODE-DIVERGENCE.md` (FO-1 gold table + cascade, FO-2 PSC numeric, stale-record inventory) — full read; **already committed**.
- `24-ISSUE-LEDGER.md` (19-row Status Table, Lifecycle Rules, per-finding transition logs, M13/G4 OI-7b-partial notes) — full read.
- `21-HANDOFF.md` / `21-CODE-DIVERGENCE.md` / `21-UAT.md` (v1.4 precedent structure) — full read.
- `REQUIREMENTS.md` (VER-07..12 text L67-72; Traceability table 36/36; coverage L153-157) — read.
- `ROADMAP.md` §Phase 29 (L282-294) + Progress table (L297-313) — read.
- `STATE.md` (gold framing reconciled L31; v1.5-GAPS 10 resolved/0 deferred) — full read.
- `ctl_instruction.md:640-692` (IPR + landed PSC clause, cites `psc-coverage-entropy.md`) — read.
- `m13-gold-counterpart.md` (LOCKED `accept-third-position`/Option-B verdict; D-01a sensitivity) — read.
- `v1.5-GAPS.md` (GAP-28-03 RESOLVED, GAP-29-01 RESOLVED, all 10 gaps) — read.
- `pinn_architecture.md:996-1004` (SI-PINN-002/003 definitions) — read.
- `framework-revisions/data_quality_assessment.md:318-328` (SI-DQA-002/003 definitions) — read.
- Direct observation: `simulation_data/Data/rerun_staging/standard_gold_missing_184/validation_summary.json` (`passes:117, failures:67, total:184`); `run_manifest.json` (184 entries); `find` AC-probe inventory (3 persisted: `ac-pipe-04/08/09.sh`).

### Secondary (MEDIUM confidence)
- Phase 27/28 plan summaries (AC execution mechanics; inline vs persisted) — `27-03-SUMMARY.md`, `28-01/02/03-SUMMARY.md`.
- `git log --oneline` (commits `6eae6422`, `a511c60d`, `b6feb488` — PSC landing + Phase 29 commits).

### Tertiary (LOW confidence)
- None. No WebSearch-only claims; this is a self-contained governance phase over local artifacts.

## Metadata

**Confidence breakdown:**
- Standard stack (probe tooling): HIGH — the AC-probe pattern is observed in `ac-pipe-09.sh`; no external dependency.
- Architecture (verification work-streams): HIGH — mirrors the v1.4 Phase 21 precedent and the locked D-01..D-10 decisions.
- Pitfalls: HIGH — each pitfall is grounded in a directly-observed discrepancy (token-vs-row count, AC-VAL-04 split, 184/184 consistency, persistence gap).
- AC-VAL-04 split / PSC landing: HIGH — clause physically present at `ctl_instruction.md:645-692`, commits confirmed.
- SI dispositions: MEDIUM — definitions located and quoted; the *final* retire-vs-preserve call for SI-PINN-002's 3rd comment is flagged source-silent (planner surfaces per STOP).

**Research date:** 2026-06-17
**Valid until:** ~7 days — this is a fast-moving terminal phase; the PSC landing and STATE.md reconciliation occurred within the last 24h, and the ROADMAP progress row is still stale. Re-confirm the ledger row statuses and ROADMAP state at plan time.
