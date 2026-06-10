# Phase 24: Empirical Dataset Verification and Correction Addendum - Research

**Researched:** 2026-06-10
**Domain:** Empirical dataset probing / claim verification / issue-ledger seeding (no external packages; internal repo + on-disk dataset only)
**Confidence:** HIGH

## Summary

Phase 24 is a verification-and-bookkeeping phase, not a design or spec-edit phase. It runs a fixed checklist of read-only probes (DATA-01..06) against the on-disk `simulation_data/` dataset to confirm/correct/mark-unverified every package-stated dataset figure, then compiles a CLM-keyed DATA-07 correction addendum (or nil addendum) beside the Phase 23 package and seeds the `24-ISSUE-LEDGER.md` at the stable path Phase 25 consumes. The "stack" is the repository's dataset files, the existing `simulation_data/Scripts/` provenance (SCOPE-07 grounding), the Phase 23 `claims-table.md` checklist (CLM-01..13), and the v1.4 `16-ISSUE-LEDGER.md` schema precedent. No web research and no external libraries — consistent with the Phase 23 precedent (`23-RESEARCH.md`: "No web sources; no external libraries").

The single most important runtime fact for the planner: **probes that call `np.allclose` (DATA-05, D-14) MUST run under `.venv/bin/python` (numpy 2.2.0); the system `python3` (3.14.5, homebrew) has NO numpy.** [VERIFIED: `.venv/bin/python -c "import numpy"` → 2.2.0; `python3 -c "import numpy"` → ModuleNotFoundError]. Several probes (DATA-01 gap-set arithmetic, DATA-03 ID-set diff, DATA-06 snapshot-count via block split) need only the standard library and can run under either interpreter, but standardizing on `.venv/bin/python` for all probes removes the failure mode.

Most probes have a strong `confirmed` prior already established by pilot runs in this research session (folder counts, ID gaps, blacklist composition, t=0 mass match), but each must be re-derived independently and recorded re-derivably (D-02/D-03). Two genuine planner-facing decision risks surfaced and are recorded as Open Questions, NOT resolved: (1) the **DATA-01 nominal-range convention** — the "1,250 gaps / 4,000 nominal" claim is sensitive to whether the nominal range is `[0..3999]` (gives 1,251) or `[0..max_id=3998]` (gives exactly 1,250), and the generation script's `N_SAMPLES_STANDARD=2500` does not obviously ground a 4,000 nominal; and (2) the **DATA-03 184-vs-185 ID-count** off-by-one a naive grep produces, which the real set-diff probe must settle. Both are exactly the kind of off-by-one the D-13 ID-parsing method exists to resolve, and both must be routed through D-08 (corrected claim) / D-12 (anomaly) by the executor on evidence — or surfaced as a STOP gap if the nominal-range convention proves source-silent.

**Primary recommendation:** Plan one disposable probe per DATA requirement under a `probes/` subfolder, all run with `.venv/bin/python`, each emitting a recorded command + dataset path + observed value into the verified-facts register; map probes 1:1 onto CLM-01..12 rows (CLM-13 is `PENDING`, not probed, per D-05); fold the two erratum corrections into the addendum unconditionally (D-07); and instantiate — not redesign — the v1.4 ledger schema for `24-ISSUE-LEDGER.md`. Treat the nominal-range convention and the 184/185 count as evidence-driven branch points with a STOP-gap escape hatch, never as figures to silently choose.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Probe implementation & evidence capture**
- **D-01:** DATA-01..06 executed as **disposable, read-only probes**: scripts (Python or shell) committed under this phase directory (e.g. a `probes/` subfolder), captured outputs committed beside them. Probes never write inside `simulation_data/` and never touch `pinn/` (VER-09). One-liner probes may be recorded as inline commands in the verified-facts register instead of script files.
- **D-02:** Re-derivability standard (roadmap criterion 3, SCOPE-06): every recorded fact carries the exact probe command/script reference AND the dataset path it ran against, alongside the observed value and run date.
- **D-03:** Probes stay v1.5-disposable: no packaging into reusable validation tooling (FUT-03), no edits to `simulation_data/Scripts/` or `simulation_data/Validation/`. Existing audit artifacts (`footer_audit_20251224_170141.md`, `check_missing_results*.py`) may be READ as cross-checks; Phase 24 executes its own probes so ledger evidence is self-contained — it never cites the doc-integrity audit workstream as a substitute for a probe run.

**Verification checklist scope**
- **D-04:** Primary checklist is `research_package/claims-table.md` rows CLM-01..CLM-12, each verified via its "Phase-24 check" column, mapped to its owning DATA requirement (CLM-01/02/12→DATA-01, CLM-03→DATA-02, CLM-04→DATA-03, CLM-05/06→DATA-03/04 folder counts, CLM-07/08/09→DATA-04 footer/parameter probes (table column labels say DATA-05; REQUIREMENTS.md mapping governs), CLM-10/11→DATA-06).
- **D-05:** CLM-13 (`D = 6.694`) is NOT empirically probed — convention conflict routed to Phase 25 (EVID-10) / Phase 27 (PIPE-09). Ledger records it `PENDING` with that routing; Phase 24 takes no position.
- **D-06:** **Bounded prose sweep** beyond the table: `consolidated-context.md`, `framed-research-questions.md`, package `README.md`, `DELIVERY-NOTE.md` swept for empirical dataset figures with no CLM row. DATA-07 scope is "every package-stated dataset claim", broader than the 13 rows. Newly found figures get extension IDs (`CLM-14`, `CLM-15`, …) recorded in the Phase 24 verified-facts register — the delivered `claims-table.md` stays byte-stable — so the addendum stays CLM-keyed.
- **D-07:** The two **ERRATUM-2026-06-10 corrections fold into the DATA-07 addendum** regardless of re-probe outcomes: (1) gold filenames carry no `_gold_` infix — gold status is folder-encoded only; (2) the 1,550/701/219 populations have **no `Result:` footer at all**. Phase 24 re-executes both probes itself; the addendum supersedes the erratum.

**Verdict semantics**
- **D-08:** Verdict vocabulary fixed by roadmap criterion 1: **`confirmed` / `corrected` / `unverified`**. `corrected` rows enter the addendum with claimed value, observed value, probe method. `unverified` is used ONLY when a probe cannot run within grounding limits, with reason recorded — never a shortcut for "didn't get to it".
- **D-09:** Approximate claims (`~59`/`~125`/`~1000` snapshots, `~4,000`/`~5,000` ICs): probe records the **full distribution** (DATA-06 mandates distributions — per-variant min/median/mode/max plus counts at modal values); verdict judged at the claim's stated precision. Exact observed values always recorded; if an approximation is materially off, row is `corrected` with exact figures.
- **D-10:** DATA-02 blacklist **consumption status** checked across `simulation_data/Scripts/` only (SCOPE-07 — grep runners/prescreening/metrics for blacklist loading). The M11 claim "not loaded at training time" concerns `pinn/` (outside grounding, SCOPE-10): recorded `unverified — outside grounding limits, deferred to Phase 25 adjudication and the FUT-01 handoff`.
- **D-11:** If a probe contradicts `simulation_data/Documentation/`: empirical observation outranks documentation (SCOPE-06), contradiction recorded, README correction **proposed to user for sign-off** — never applied autonomously. If the contradicted figure is package-stated, it also enters the addendum.
- **D-12:** Discrepancies contradicting **no** package-stated claim are recorded in the ledger's anomalies section + surfaced in the phase summary — NOT in the DATA-07 addendum (whose scope is package-stated claims only).

**DATA-01 ID-gap counting method**
- **D-13:** Gap counting parses numeric IDs from filenames (`brutus_standard_XXXX.txt` / `brutus_hierarchical_XXXX.txt`) and computes the missing-ID set against the nominal ID range — NOT bare file counts. The nominal range convention (0-based vs 1-based, range end) is read off observed data and `simulation_data/Scripts/ic_generation/` provenance; method recorded with the result.

**DATA-05 mass-drift probe design**
- **D-14:** Comparison fixed by DATA-05: `m_IC` (mass slots in `simulation_data/Data/ic_final/` files) vs the mass column of the t=0 snapshot block in the corresponding Brutus output file, compared with `np.allclose(rtol=1e-15)` on float64-parsed values.
- **D-15:** Sample: **default full population** — every trajectory with an IC counterpart, across all four Brutus output variants. Fall back to a seeded stratified sample (≥100 per variant, RNG seed recorded) only if runtime is prohibitive; sample definition documented with the result either way.
- **D-16:** Baseline contingency: Phase 23 context documents **hierarchical IC perturbations** between IC generation and Brutus input. If mass mismatches cluster in hierarchical variants, the executor checks `simulation_data/Scripts/ic_generation/` provenance to determine whether masses were perturbation-invariant BEFORE recording a verdict. If provenance is ambiguous about what Brutus consumed, that is a **STOP gap (semantic)** — surfaced, not resolved by choosing a baseline.
- **D-17:** Verdict interpretation (feeds PIPE-07, Phase 27): allclose pass ⇒ "IC masses canonical at float64"; fail ⇒ characterize whether mismatch is float64 round-trip/parse precision (⇒ "`decimal.Decimal` parsing required") or genuine value drift (⇒ anomaly per D-12 and candidate STOP gap). Verdict recorded with evidence.

**DATA-07 addendum form & delivery**
- **D-18:** One canonical addendum file placed **beside the package files inside `research_package/`** (erratum precedent: sibling file, NOT added to the manifest, all originally-delivered files byte-stable). Self-describing name, e.g. `DATA-07-CORRECTION-ADDENDUM.md` (exact name = Claude's discretion).
- **D-19:** Addendum structure: CLM-keyed rows — claimed value, observed value, probe command/path, verdict — plus an explicit supersession statement over `ERRATUM-2026-06-10.md` folding in its two corrections (D-07). A confirmed-claims summary section records what verification upheld.
- **D-20:** Nil-addendum case: if no package-stated claim is contradicted, the same file records that all package-stated claims were confirmed, with the probe index.
- **D-21:** Delivery: addendum ships **as soon as the probes finish** — never waiting on the resolution doc — as a commit plus a notification to the user, who forwards it to the in-flight external research. The agent sends nothing externally itself.

**Issue-ledger seeding**
- **D-22:** Path: `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` — the "stable path under the Phase 24 directory" (v1.4 precedent `16-ISSUE-LEDGER.md`).
- **D-23:** Seed scope: full enumerated in-scope issue-02 finding inventory — B-06, B-11, M11, M12, M13, D7, G1–G5, D-03 (training-data format), the SCS/SASD/IPR/PSC validation-metric claims, `compute_globals` `D = 6.694`, the footer/mass-drift protocol, precision handling — each initialized `PENDING` with owning requirement + adjudication phase; plus the verified-facts register (CLM/DATA-keyed, per-row probe citations) as the dataset-evidence annex; plus the anomalies section (D-12).
- **D-24:** Schema: v1.4 `16-ISSUE-LEDGER.md` format with the roadmap state machine (`PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`, or `DEFERRED` with a written blocker). Phase 24 **initializes states only** — the operating protocol is Phase 25's to establish; Phase 24 does not over-specify columns Phase 25 owns.

**Workflow**
- **D-25:** Tag `v1.5-pre-phase-24` cut from `milestone/v1.5` HEAD (`4b6ff913`) during the discuss session. One atomic commit per plan via `scripts/agent-commit`. Phase 24 gates on nothing external; runs during the gate window.

### Claude's Discretion
- Probe language per probe (Python vs shell), probe/evidence file names, `probes/` subfolder layout, exact addendum filename — presentation-only; keep names self-describing, consistent with `NN-*` conventions.
- Verified-facts register placement: standalone `24-VERIFIED-FACTS.md` vs a section of `24-ISSUE-LEDGER.md` — either satisfies roadmap criterion 5 as long as the ledger file links it at the stable path.
- Prose-sweep recording format (how non-table claims and their CLM-14+ IDs are listed).

### Deferred Ideas (OUT OF SCOPE)
- Adjudication verdicts, evidence packets, root-cause conflict resolution (ratio-SCS vs locked gate; `D=6.694` vs PHYS-01) — Phase 25 (EVID-06..10), spec edits Phases 26–28.
- Any README/dataset-documentation correction — proposed to user for sign-off only (D-11); the edit itself is not Phase 24 work.
- Packaging probes into reusable validation tooling — FUT-03.
- M16 collocation-scaling, G6 causal-training, training-loop metric usage — doc-03 milestone (SCOPE-11).
- Prescribing structure for the user's resolution doc — rejected in Phase 23 (D-16 there); remains out of scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DATA-01 | ID-gap claims verified against disk (claimed 1,250/4,000 std; 143/5,000 hier), with counts + method | Pilot probe: std n=2,749, max_id=3998 → gaps `[0..3998]`=**1,250** (matches), gaps `[0..3999]`=**1,251**; hier n=4,857, max_id=4999 → gaps=**143** either way. Nominal-range convention is the decision point (Open Q1). Filenames are zero-padded 4-digit `brutus_{type}_NNNN.txt` → ID-parse method (D-13) is trivial std-lib. |
| DATA-02 | Blacklist verified — 65-ID claim + consumption status (`simulation_data/Scripts/` grounding) | `problematic_ics_blacklist.json` = exactly **2 hierarchical + 63 standard = 65** (direct read). Consumption: README line 1005 states json is "Legacy blacklist … **not** used by current runners"; runners load from `Documentation/problematic_ics/{type}/` dirs instead; `Validation/dataset_readiness_checks/config.py:139` DOES load the json. M11 training-time aspect → `unverified` (SCOPE-10, D-10). |
| DATA-03 | Gold-counterpart gap — 184 std-without-gold, 2,565 vs 2,749 folder counts, cross-check `standard_quasi_random_ids_not_in_gold.md` | Folder counts confirmed: base 2,749, gold 2,565 (Δ=184). Doc claims 184; naive 4-digit grep yields **185** (summary numbers `2565`/`2749` pollute the grep) — the real ID-set diff (`base_ids − gold_ids`) is the authoritative method (Open Q2). |
| DATA-04 | Footer-schema variance — 219 minimal std-gold, eta/tol omissions, folder defaults, OS-dependent paths | Sample std file: footer present carries full schema (`eta`, `tol`, `Lw`, energy). Erratum (folded by D-07): 1,550 hier / 701 std / 219 std-gold have NO `Result:` footer at all. `footer_audit_20251224_170141.md` cross-check (read-only). Footer is last line; `Result:` filename field exposes original OS path (`<home>/Desktop/cursor/...`) → OS-dependent path fact. |
| DATA-05 | Mass-drift probe — `m_IC` vs `m_Brutus(t=0)` via `np.allclose(rtol=1e-15)`, verdict feeds PIPE-07 | File format decoded: Brutus t=0 block = lines 1–3 (mass = col 0); IC file = 3 lines (mass = col 0). Pilot n=50 std → **0 mismatches** at rtol=1e-15 → strong "IC masses canonical at float64" prior. REQUIRES `.venv/bin/python` (numpy). Full-population sample feasible (first-block parse is cheap). |
| DATA-06 | Snapshot-count + `dt_out` distributions per variant (claimed ~59/~125/~1000; `final_timestep>=9.5` prevalence) — distributions not single examples | Snapshot count = count of `\n\n`-separated non-empty blocks. Pilot std sample = **61** (claim `~59`). Each block header line carries the snapshot time → `final_timestep` = first token of last block; prevalence = fraction with last-time ≥ 9.5. Std-lib only. Distribution recorded per D-09. |
| DATA-07 | Correction addendum (CLM-keyed) for every contradicted package claim; nil addendum otherwise; ships as soon as probes finish | Addendum form/placement fully specified by D-18..D-21; erratum sibling-file precedent; two erratum corrections fold in unconditionally (D-07). Delivery = commit + user notification (DELIVERY-NOTE.md announced this channel). |
</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| ID-gap / folder-count probes | Disposable probe scripts (`probes/`) | On-disk dataset (`simulation_data/Data/`) | Read filesystem, parse filenames, set arithmetic — no service, no DB |
| Footer / parameter parsing | Disposable probe scripts | Brutus `.txt` files (last-line footer) | Pure text parse of trailing `Result:` line; folder defaults for footer-less files |
| Mass-drift comparison | Disposable probe scripts (`.venv` numpy) | `ic_final/` + `brutus_output/` t=0 blocks | Numerical float64 compare; needs numpy (`np.allclose`) |
| Blacklist consumption check | grep over `simulation_data/Scripts/` + `Validation/` | README provenance note | SCOPE-07 grounding; `pinn/` consumption is out-of-grounding |
| Correction addendum | Markdown sibling file in `research_package/` | Verified-facts register | CLM-keyed bookkeeping; package stays byte-stable |
| Issue ledger seed | `24-ISSUE-LEDGER.md` (planning tier) | `23-CLAIMS-INVENTORY.md` finding inventory | Initialize state machine; Phase 25 operates it |

## Standard Stack

This phase installs **no external packages**. The "stack" is the repository toolchain already present.

### Core
| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| `.venv/bin/python` | 3.x + numpy 2.2.0 | All DATA-01..06 probes | The ONLY interpreter with numpy; DATA-05 `np.allclose` requires it [VERIFIED: `.venv/bin/python -c "import numpy"` → 2.2.0] |
| Python stdlib (`os`, `re`, `glob`, `json`, `math`) | bundled | ID parsing, set diff, footer parse, blacklist read | No third-party dependency needed for DATA-01/02/03/04/06 |
| `scripts/agent-commit` | repo | Mandatory commit path (one atomic commit per plan, D-25) | CLAUDE.md Git Commit Protocol; raw `git commit` forbidden |

### Supporting
| Tool | Purpose | When to Use |
|------|---------|-------------|
| `grep -rniE` | Blacklist-consumption sweep (DATA-02, D-10) | SCOPE-07 grounding scan over `simulation_data/Scripts/` + `Validation/` |
| Existing audit scripts (`check_missing_results*.py`, `footer_audit_20251224_170141.md`) | Read-only cross-check ONLY (D-03) | Compare probe outputs against prior audit; never cite as a probe substitute |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `.venv/bin/python` for all probes | system `python3` for std-lib-only probes | System python3 lacks numpy → DATA-05 fails; standardizing on `.venv` avoids a split-interpreter footgun for zero cost |
| Per-requirement probe scripts | One monolithic probe script | Per-requirement scripts map 1:1 onto CLM rows and DATA IDs (cleaner re-derivability per D-02); CONTEXT Claude's-discretion allows either layout |

**Installation:** None — no `npm install` / `pip install`. numpy already present in `.venv`. [VERIFIED: pilot probe ran under `.venv/bin/python` successfully]

## Package Legitimacy Audit

Not applicable — Phase 24 installs no external packages. All probes use the repository's existing `.venv` and Python stdlib. (Consistent with Phase 23 precedent: internal-repository research only, no external libraries.)

## Architecture Patterns

### System Data Flow

```
Phase 23 claims-table.md (CLM-01..13)  ──┐
ERRATUM-2026-06-10.md (2 corrections)   ──┤
prose sweep (consolidated-context.md,   ──┤
  framed-research-questions.md, README, ──┤
  DELIVERY-NOTE)  → CLM-14+ extension IDs ─┤
                                          ▼
                        ┌─────────────────────────────────┐
                        │  probes/ (one per DATA-01..06)   │
                        │  run with .venv/bin/python       │
                        │  read-only over simulation_data/ │
                        └─────────────────────────────────┘
                                          │
                  observed value + command + dataset path + date
                                          ▼
                        ┌─────────────────────────────────┐
                        │ Verified-Facts Register          │
                        │ (24-VERIFIED-FACTS.md or ledger  │
                        │  annex) — verdict per CLM/DATA    │
                        │  confirmed / corrected / unverified│
                        └─────────────────────────────────┘
                          │                       │
            contradicted package claim?     anomaly (no pkg claim)?
                          │ yes                   │ yes
                          ▼                       ▼
       ┌──────────────────────────────┐   ┌──────────────────────┐
       │ DATA-07-CORRECTION-ADDENDUM  │   │ ledger anomalies      │
       │ .md (sibling in              │   │ section + phase       │
       │ research_package/, CLM-keyed,│   │ summary (D-12)        │
       │ supersedes erratum)          │   └──────────────────────┘
       │  → commit + user notify      │
       └──────────────────────────────┘
                          │
                          ▼
       24-ISSUE-LEDGER.md (D-22): full finding inventory PENDING
       + verified-facts annex + anomalies  →  consumed by Phase 25
```

### Recommended Project Structure
```
.planning/phases/24-empirical-dataset-verification-and-correction-addendum/
├── 24-RESEARCH.md            # this file
├── 24-NN-PLAN.md / SUMMARY   # GSD plan artifacts
├── probes/                   # disposable read-only probe scripts (D-01)
│   ├── data01_id_gaps.py
│   ├── data02_blacklist.py
│   ├── data03_gold_gap.py
│   ├── data04_footers.py
│   ├── data05_mass_drift.py  # MUST run under .venv/bin/python
│   ├── data06_snapshots.py
│   └── outputs/              # captured probe outputs (committed)
├── 24-VERIFIED-FACTS.md      # verified-facts register (or ledger annex)
├── 24-ISSUE-LEDGER.md        # D-22 stable path; Phase 25 consumes
└── 24-GAPS.md                # created ONLY on first STOP gap
```

### Pattern 1: Disposable re-derivable probe (D-01/D-02)
**What:** A self-contained script that prints `{value, command, dataset_path, date}` and writes nothing into `simulation_data/`.
**When to use:** Every DATA-01..06 fact that isn't a trivial inline one-liner.
**Example:**
```python
# probes/data01_id_gaps.py — run: .venv/bin/python probes/data01_id_gaps.py
import os, re
DATA = "simulation_data/Data/brutus_output"
def ids(folder, pat):
    return sorted(int(re.match(pat, f).group(1))
                  for f in os.listdir(folder) if re.match(pat, f))
std = ids(f"{DATA}/brutus_standard_quasi_random", r"brutus_standard_(\d+)\.txt")
hier = ids(f"{DATA}/brutus_hierarchical", r"brutus_hierarchical_(\d+)\.txt")
for label, arr, nominal_end in [("standard", std, 3999), ("hierarchical", hier, 4999)]:
    present = set(arr)
    # Record BOTH conventions; verdict per Open Q1 / D-13
    gaps_to_max = len(set(range(arr[0], arr[-1] + 1)) - present)
    gaps_to_nominal = len(set(range(0, nominal_end + 1)) - present)
    print(f"{label}: n={len(arr)} min={arr[0]} max={arr[-1]} "
          f"gaps[0..max]={gaps_to_max} gaps[0..{nominal_end}]={gaps_to_nominal}")
```
[VERIFIED: this exact logic ran in-session — std gaps[0..max]=1250, gaps[0..3999]=1251; hier=143 both]

### Pattern 2: Mass-drift probe (D-14/D-17) — numpy-gated
**What:** Parse mass column (col 0) from IC file rows 1–3 and from the Brutus t=0 block (lines 1–3), compare `np.allclose(rtol=1e-15)`.
**When to use:** DATA-05 only.
**Example:**
```python
# probes/data05_mass_drift.py — run: .venv/bin/python probes/data05_mass_drift.py
import os, re, numpy as np
def ic_masses(p):
    rows = [l.split() for l in open(p).read().strip().splitlines() if l.strip()]
    return [float(r[0]) for r in rows[:3]]
def brutus_t0_masses(p):
    L = open(p).read().splitlines()   # block 0: header=L[0], bodies=L[1..3]
    return [float(L[i].split()[0]) for i in (1, 2, 3)]
# iterate all four variants, full population (D-15); record mismatches + cluster-by-variant (D-16)
```
[VERIFIED: pilot n=50 standard → 0 mismatches at rtol=1e-15]

### Pattern 3: Snapshot-count + final-timestep distribution (D-09)
**What:** Split file on `\n\n`, count non-empty blocks (= snapshots); the first token of the last block's header is the final time.
**When to use:** DATA-06.
**Example:**
```python
blocks = [b for b in open(path).read().split("\n\n") if b.strip()]
n_snapshots = len(blocks)
final_time = float(blocks[-1].splitlines()[0].split()[0])  # >= 9.5 gate
```
[VERIFIED: pilot std file → 61 snapshots; note claim is `~59`]

### Anti-Patterns to Avoid
- **Bare file-count for ID gaps:** D-13 forbids it — parse IDs and diff against the nominal range; the std 2,749-vs-2,750 wrinkle is exactly why.
- **Running DATA-05 under system `python3`:** ModuleNotFoundError (no numpy). Always `.venv/bin/python`.
- **Grepping the gold-gap doc for "184":** summary numbers (`2565`, `2749`) pollute a naive 4-digit grep → 185. Do the real `base_ids − gold_ids` set diff.
- **Treating "minimal/partial footer" language as current:** superseded by erratum — those populations have NO footer at all (D-07).
- **Editing `simulation_data/Documentation/` autonomously on a contradiction:** D-11 forbids — propose to user, never apply.
- **Writing to a gap register as a subagent / inventing a nominal-range convention:** STOP protocol — surface, never invent.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Issue-ledger schema | A new ledger format | Instantiate v1.4 `16-ISSUE-LEDGER.md` (status table + lifecycle rules + per-finding log) | D-24: Phase 24 initializes states only; Phase 25 owns the operating protocol — redesigning columns oversteps |
| Finding inventory | Re-deriving the issue-02 finding list | `23-CLAIMS-INVENTORY.md` + REQUIREMENTS.md (B-06, B-11, M11–M13, D7, G1–G5, SCS/SASD/IPR/PSC, D=6.694, etc.) | D-23 enumerates the exact seed scope |
| Footer-population counts | A fresh full-corpus footer scanner from scratch | Read `footer_audit_20251224_170141.md` as cross-check, run a minimal own probe | D-03: own probe for self-containment, but the audit confirms the 1,550/701/219 figures |
| Blacklist consumption verdict | Re-implementing runner logic | Read README line 1005 + grep runners | README already states json is legacy/unused-by-runners; SCOPE-07 grounding settles it |
| `np.allclose` semantics | Hand-rolled tolerance loop | numpy in `.venv` (D-14 mandates `np.allclose(rtol=1e-15)`) | DATA-05 spec fixes the exact comparator |

**Key insight:** Phase 24 is verification + transcription, not design. Every artifact it produces either re-derives a fact (probe) or instantiates an existing schema (ledger). The danger is over-building (redesigning the ledger, packaging probes) or under-grounding (choosing a nominal-range convention the source is silent on).

## Runtime State Inventory

Not a rename/refactor/migration phase — section omitted. Phase 24 writes only into its own phase directory and a sibling addendum file in `research_package/`; it mutates no stored data, no live-service config, no OS-registered state. (The only state mutation is STATE.md via gsd-tools handlers, per CONTEXT code_context.)

## Common Pitfalls

### Pitfall 1: Numpy-less interpreter
**What goes wrong:** DATA-05 probe aborts with `ModuleNotFoundError: No module named 'numpy'`.
**Why it happens:** System `python3` is homebrew 3.14.5 without numpy; only `.venv/bin/python` has numpy 2.2.0.
**How to avoid:** Run ALL probes with `.venv/bin/python`; document the interpreter in the probe header (D-02 re-derivability).
**Warning signs:** A probe command recorded as `python3 ...` instead of `.venv/bin/python ...`.

### Pitfall 2: Nominal-range off-by-one decided silently
**What goes wrong:** CLM-01 is marked `confirmed` (1,250) or `corrected` (1,251) depending on an unstated `[0..3999]`-vs-`[0..3998]` choice — and that choice is not obviously grounded.
**Why it happens:** Claimed "4,000 nominal" does not match the generation script's `N_SAMPLES_STANDARD=2500` (`generate_ics.py:15`); the convention behind "4,000" is not self-evident.
**How to avoid:** Record BOTH counts; check `ic_generation/` provenance for the ID-allocation convention; if the convention is source-silent, **surface a STOP gap (Open Q1)** rather than picking.
**Warning signs:** A probe that emits only one gap count, or a verdict with no cited nominal-range basis.

### Pitfall 3: Stale footer narrative
**What goes wrong:** The addendum repeats "minimal/partial footers" language the erratum already retired.
**Why it happens:** `consolidated-context.md` still carries pre-correction "partial footer" prose (lines 73–105).
**How to avoid:** Apply D-07 — the 1,550/701/219 populations have NO `Result:` footer; footers present carry the full schema. Fold both erratum corrections in unconditionally.
**Warning signs:** Addendum text mentioning "partial footer" or `_gold_` infix as a live fact.

### Pitfall 4: Blacklist consumption over-claimed
**What goes wrong:** Recording "blacklist not consumed" or "blacklist consumed" as a flat verdict.
**Why it happens:** The json IS consumed by `Validation/dataset_readiness_checks/config.py:139` but NOT by current Brutus runners (which use `Documentation/problematic_ics/{type}/` dirs); README line 1005 calls the json "legacy … not used by current runners".
**How to avoid:** Record the nuanced consumption map within SCOPE-07; mark the `pinn/` training-time aspect `unverified` per D-10.
**Warning signs:** A single yes/no consumption verdict with no source split.

### Pitfall 5: 184-vs-185 grep artifact
**What goes wrong:** DATA-03 marked `corrected` to 185 on a grep artifact.
**Why it happens:** Naive 4-digit grep of `ids_not_in_gold.md` captures summary numbers `2565`/`2749`.
**How to avoid:** Compute `base_ids − gold_ids` as the authoritative set; cross-check the doc's listed block separately.
**Warning signs:** An ID count that disagrees with `len(base_ids) − len(gold_ids) = 2749 − 2565 = 184`.

## Code Examples

All examples are pilot-verified in this research session (see Patterns 1–3 above). Folder-count one-liner (DATA-04 base counts, recordable inline per D-01):

```bash
# run from repo root; record command + path + date in the register
for d in simulation_data/Data/brutus_output/*/; do
  echo "$(ls "$d" | wc -l | tr -d ' ')  $d"
done
# [VERIFIED]: 4857 hier_gold, 4857 hier, 2565 std_gold, 2749 std
```

Blacklist composition (DATA-02, inline one-liner):
```bash
.venv/bin/python -c "import json; b=json.load(open('simulation_data/Documentation/problematic_ics_blacklist.json')); print({k:len(v) for k,v in b.items()}, 'total', sum(len(v) for v in b.values()))"
# [VERIFIED]: {'hierarchical': 2, 'standard': 63} total 65
```

## State of the Art

Not applicable — no fast-moving external technology. The relevant "state" is the repository's own evolving documentation:

| Old Claim | Corrected Fact | When Changed | Impact |
|-----------|----------------|--------------|--------|
| Gold filenames carry `_gold_` infix | No `_gold_` infix; folder-encoded only | Erratum 2026-06-10 (README commits `d18f676`/`31b2cff`) | Fold into addendum (D-07); 0 of 4,857/2,565 files match `_gold_` |
| 1,550/701/219 = "partial/minimal footers" | NO `Result:` footer at all in those files | Erratum 2026-06-10 (README commit `ae609f3`) | Fold into addendum (D-07); CLM-07 count (219) stands, characterization corrected |
| json blacklist used by runners | json is legacy; runners use `problematic_ics/{type}/` dirs | README line 1005 (current) | DATA-02 consumption nuance |

**Deprecated/outdated (do not rely on as live facts):**
- `consolidated-context.md` "partial footer" prose (lines 73–105) — superseded by erratum.
- `pinn/data-processing-pipeline-full.py`, `pinn/basic_architecture.py` — NOT grounding (SCOPE-10).

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The snapshot count = count of `\n\n`-delimited non-empty blocks; final time = first token of last block's header | DATA-06 pattern | If block delimiting differs across variants (e.g. gold files), the count/final-time parse needs per-variant validation; pilot only covered standard |
| A2 | The Brutus t=0 mass column is col 0 of body lines 1–3 of the first block, matching IC col 0 | DATA-05 pattern | If any variant reorders columns or bodies, the mass alignment is wrong; pilot covered 50 standard files only — full-population run (D-15) is the real check |
| A3 | "Nominal 4,000/5,000" is an ID-range/allocation convention, not the generation-script `n_samples` (2,500/1,500) | DATA-01 / Open Q1 | If the nominal basis is genuinely undefined in grounding sources, the CLM-01/CLM-12 verdict is source-silent → STOP gap, not a free choice |

*A1–A3 are pilot-derived and must be re-confirmed by the full probes; none is a locked decision. They are flagged so the planner gates each on its own probe.*

## Open Questions

1. **DATA-01 nominal-range convention (potential STOP gap — semantic).**
   - What we know: std has 2,749 files, max ID 3998; gaps `[0..3998]`=1,250 (matches claim exactly), gaps `[0..3999]`=1,251. Hier has 4,857 files, max ID 4999, gaps=143 either way (full range). Generation script sets `N_SAMPLES_STANDARD=2500` / `N_SAMPLES_HIERARCHICAL=1500` (`generate_ics.py:15-16`) with `start_from_last=True` (continuation), so multiple runs accumulate — 2,500 ≠ 4,000.
   - What's unclear: what defines the "4,000 standard / 5,000 hierarchical nominal" range against which gaps are counted, and therefore whether the nominal end is 3999 (gaps=1,251 → CLM-01 `corrected`) or the observed max 3998 (gaps=1,250 → CLM-01 `confirmed`). The convention is not self-evidently grounded in the generation script.
   - Recommendation: the executor checks `ic_generation/` (incl. `ic_generation_utils.py`) and README for an explicit nominal/ID-range statement. If found, record the method (D-13) and route via D-08. **If the nominal-range convention is genuinely source-silent, this is a STOP gap (semantic) — surface in `24-GAPS.md` + `v1.5-GAPS.md`, do NOT pick a convention.** Either way, record BOTH counts so the verdict is re-derivable. (Subagent does not write the gap register — the executor/orchestrator does.)

2. **DATA-03 184-vs-185 ID count.**
   - What we know: folder counts give Δ = 2749 − 2565 = 184; the gold-gap doc claims 184; a naive 4-digit grep of the doc yields 185 (captures summary numbers).
   - What's unclear: whether the doc's listed ID block is exactly 184 once summary numbers are excluded, and whether the true `base_ids − gold_ids` set equals the doc's list.
   - Recommendation: compute the authoritative set diff and compare to the doc's parsed ID block; this is a normal `confirmed`/`corrected` outcome (D-08), not a gap — but record the method explicitly.

3. **DATA-05 hierarchical mass baseline (conditional STOP gap — semantic, per D-16).**
   - What we know: pilot mass match was on standard files only (0 mismatches). Phase 23 context documents hierarchical IC perturbations between IC generation and Brutus input.
   - What's unclear: whether masses are perturbation-invariant for hierarchical variants — i.e. whether the `ic_final/ic_hierarchical/` mass equals what Brutus consumed.
   - Recommendation: if mismatches cluster in hierarchical variants, check `ic_generation/` provenance BEFORE recording a verdict (D-16). If provenance is ambiguous about what Brutus consumed, surface a STOP gap — do not pick a baseline.

4. **Verified-facts register placement (Claude's discretion, presentation-only).**
   - Recommendation: standalone `24-VERIFIED-FACTS.md` linked from `24-ISSUE-LEDGER.md` at the stable path — keeps the ledger's status-machine clean and the dataset annex separately re-derivable. Either option satisfies roadmap criterion 5.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `.venv/bin/python` + numpy | DATA-05 `np.allclose` | ✓ | numpy 2.2.0 | none needed |
| Python stdlib | DATA-01/02/03/04/06 | ✓ | 3.14.5 (system) / .venv | use `.venv` to be uniform |
| `simulation_data/Data/brutus_output/*` (4 variants) | DATA-01/03/04/05/06 | ✓ | 2,749 / 2,565 / 4,857 / 4,857 files | none |
| `simulation_data/Data/ic_final/*` (2 variants) | DATA-05 | ✓ | 2,749 / 4,857 files | none |
| `problematic_ics_blacklist.json` | DATA-02 | ✓ | 65 IDs (2 hier + 63 std) | none |
| `standard_quasi_random_ids_not_in_gold.md` | DATA-03 | ✓ | 184-ID doc | none |
| `footer_audit_20251224_170141.md` | DATA-04 cross-check | ✓ | present (read-only) | own probe is primary |
| `16-ISSUE-LEDGER.md` precedent | D-24 ledger schema | ✓ | v1.4 archived | none |
| `scripts/agent-commit` | D-25 commit | assumed ✓ | repo | raw commit forbidden — must exist |

**Missing dependencies with no fallback:** none — every probe target is present on disk.
**Missing dependencies with fallback:** numpy absent in system python3 → use `.venv/bin/python` (uniform recommendation).

## Validation Architecture

Phase 24 IS the validation phase — its probes ARE the acceptance checks (VER-09 disposable-probe model). There is no separate unit-test framework; the probes produce the recorded pass/fail evidence.

### "Test Framework"
| Property | Value |
|----------|-------|
| Framework | Disposable probe scripts under `probes/` (no pytest/unittest harness) |
| Config file | none — each probe is self-contained (D-01) |
| Quick run command | `.venv/bin/python probes/dataNN_*.py` |
| Full suite command | run all six probes; capture outputs under `probes/outputs/` |

### Requirements → Probe Map
| Req ID | Behavior | Probe | Command | Exists? |
|--------|----------|-------|---------|---------|
| DATA-01 | ID-gap counts + method | `data01_id_gaps.py` | `.venv/bin/python probes/data01_id_gaps.py` | ❌ Wave 0 (pilot logic verified) |
| DATA-02 | blacklist 65 + consumption | `data02_blacklist.py` + grep | inline + grep | ❌ Wave 0 (pilot verified) |
| DATA-03 | 184 gold-gap + folder counts | `data03_gold_gap.py` | `.venv/bin/python probes/data03_gold_gap.py` | ❌ Wave 0 |
| DATA-04 | footer schema + counts | `data04_footers.py` | `.venv/bin/python probes/data04_footers.py` | ❌ Wave 0 |
| DATA-05 | mass-drift allclose | `data05_mass_drift.py` | `.venv/bin/python probes/data05_mass_drift.py` | ❌ Wave 0 (pilot n=50 verified) |
| DATA-06 | snapshot + final-time dist | `data06_snapshots.py` | `.venv/bin/python probes/data06_snapshots.py` | ❌ Wave 0 |
| DATA-07 | addendum compiled + shipped | manual compile from register | n/a (bookkeeping) | ❌ Wave 0 |

### Sampling Rate
- **Per probe:** capture output into `probes/outputs/`, fold result into the verified-facts register with command + path + date (D-02).
- **Phase gate:** all six probes run, every CLM-01..12 row has a `confirmed`/`corrected`/`unverified` verdict, addendum (or nil) shipped, ledger seeded.

### Wave 0 Gaps
- [ ] `probes/` scripts for all six DATA requirements (pilot logic verified in-session; needs committing as disposable scripts)
- [ ] `24-VERIFIED-FACTS.md` register (or ledger annex)
- [ ] `24-ISSUE-LEDGER.md` instantiated from v1.4 schema
- [ ] No framework install needed (numpy already in `.venv`)

## Security Domain

`security_enforcement` is not engaged for this phase: Phase 24 is read-only dataset verification and Markdown bookkeeping inside a research repository. No authentication, network, input-validation, cryptography, or access-control surface. The only "input validation" concern is parser robustness against malformed dataset files — handled by the probes recording per-file parse failures rather than crashing. No ASVS category applies. (Stated explicitly rather than omitted, per protocol.)

## Sources

### Primary (HIGH confidence — direct disk/file verification this session)
- `simulation_data/Data/brutus_output/*` folder counts + filename format — direct `ls`/probe [VERIFIED]
- `simulation_data/Data/ic_final/*` format + counts — direct read [VERIFIED]
- `problematic_ics_blacklist.json` — direct read: 2 hier + 63 std = 65 [VERIFIED]
- `generate_ics.py:15-16` — `N_SAMPLES_STANDARD=2500`, `N_SAMPLES_HIERARCHICAL=1500` [VERIFIED]
- `simulation_data/Documentation/README.md:1005` — json blacklist "legacy … not used by current runners" [VERIFIED]
- `simulation_data/Scripts/brutus_runners/*` blacklist consumption (dir-based) — grep [VERIFIED]
- `Validation/dataset_readiness_checks/config.py:139` — json blacklist loaded by readiness checks [VERIFIED]
- Pilot probes: DATA-01 (gaps 1250/1251/143), DATA-05 (n=50, 0 mismatches), DATA-06 (61 snapshots) [VERIFIED]
- `claims-table.md` CLM-01..13 — the checklist [CITED]
- `ERRATUM-2026-06-10.md` — two corrections to fold in [CITED]
- `23-CLAIMS-INVENTORY.md` — finding-inventory seed source [CITED]
- `16-ISSUE-LEDGER.md` — ledger schema precedent [CITED]
- `DELIVERY-NOTE.md` — addendum delivery channel [CITED]
- `.planning/REQUIREMENTS.md` DATA-01..07, SCOPE-06..11 [CITED]
- `24-CONTEXT.md` D-01..D-25 [CITED]

### Secondary (MEDIUM confidence)
- `consolidated-context.md` prose figures (3,307 / 2,048 full-schema, etc.) — non-CLM figures candidate for CLM-14+ (D-06); some superseded by erratum [CITED]

### Tertiary (LOW confidence)
- None. No web sources, no external libraries (per the milestone internal-only directive and Phase 23 precedent).

## Metadata

**Confidence breakdown:**
- Standard stack (probe toolchain): HIGH — pilot-verified `.venv` + stdlib; numpy gating confirmed empirically.
- Architecture (probe → register → addendum → ledger flow): HIGH — fully fixed by CONTEXT D-01..D-24 and v1.4 precedent.
- Pitfalls: HIGH — three of the five (numpy, nominal-range, 184/185) were reproduced this session.
- Open questions (nominal-range, hier mass baseline): flagged as candidate STOP gaps — HIGH confidence they are real decision points, deliberately left unresolved per STOP protocol.

**Research date:** 2026-06-10
**Valid until:** stable until the dataset or Phase 23 package changes (no fast-moving dependency). Re-confirm folder counts if `simulation_data/` is touched. ~30 days.
