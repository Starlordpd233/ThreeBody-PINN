# Phase 26: DataLoader Ingestion and Selection Contracts - Pattern Map

**Mapped:** 2026-06-12
**Files analyzed:** 11 artifacts (5 new packets, 1 packet extension, 2 spec files, 1 ledger, 1 gap register, probe captures)
**Analogs found:** 11 / 11 (every artifact has a committed Phase 25 / Phase 24 analog)

> **Nature of this phase.** This is a docs/spec-adjudication phase. The "files to create/modify" are
> markdown artifacts (evidence packets, spec sections, ledger rows, a gap register) plus disposable
> probe captures — NOT source code. "Role" and "Data Flow" below are repurposed: role = artifact kind,
> data flow = the adjudication-loop step the artifact serves. The pattern excerpts are structural
> templates the executor must replicate verbatim (heading sets, citation format, transition-log line
> format), not code to copy. Live code in `pinn/` is NOT a grounding source and NOT a pattern target.

## File Classification

| Artifact (create/modify) | Role | Data Flow (loop step) | Closest Analog | Match Quality |
|--------------------------|------|------------------------|----------------|---------------|
| `evidence/{b-06}.md` (new) | evidence-packet | adjudicate | `evidence/m11-m12-severity.md` + `_TEMPLATE.md` | exact (same schema) |
| `evidence/{b-11}.md` (new) | evidence-packet | adjudicate | `evidence/m11-m12-severity.md` + `_TEMPLATE.md` | exact |
| `evidence/{m13}.md` (new, STOP-gap candidate) | evidence-packet (defer-with-blocker) | adjudicate→gate | `evidence/m11-m12-severity.md` (Verdict + GUARD sections) + `_TEMPLATE.md` | exact |
| `evidence/{d7}.md` (new) | evidence-packet | adjudicate | `evidence/m11-m12-severity.md` + `_TEMPLATE.md` | exact |
| `evidence/{d-03}.md` (new, user-gate) | evidence-packet (user-decision) | adjudicate→gate | `evidence/m11-m12-severity.md` + `_TEMPLATE.md` | exact |
| `evidence/m11-m12-severity.md` (extend M11 only) | evidence-packet extension | adjudicate (extend) | the M11 sub-part already in that file | exact (self-analog) |
| `evidence/README.md` (ID→Filename map row per new packet) | protocol-index | index update | existing ID→Filename Map table | exact |
| `ctl_instruction.md` (primary spec edits) | framework-spec | edit | v1.4-locked contract sections; landing anchors in §RESEARCH Edit Targets | role-match |
| `pinn_architecture.md` (secondary, only if candidate requires) | framework-spec | edit | §3.1 / §5.2 / §5.3.1 contract sections | role-match |
| `24-ISSUE-LEDGER.md` (status + Per-Finding rows for 10 rows) | status-ledger | ledger-same-commit | M11 row + M11 Per-Finding subsection (transition log) | exact |
| `26-GAPS.md` (create on first gap; M13 most likely) | gap-register | STOP | `25-GAPS.md` (GAP-25-01/02 entries) | exact |
| disposable probe captures (inline in packet or script under phase dir) | probe-evidence | verify | M11/M12 §First-Principles arithmetic block; Phase 24 probe commands in `24-VERIFIED-FACTS.md` | role-match |

## Pattern Assignments

### `evidence/{b-06,b-11,m13,d7,d-03}.md` — new evidence packets (adjudicate)

**Analog:** `evidence/_TEMPLATE.md` (schema, copy source) + `evidence/m11-m12-severity.md` (a fully filled real instance).

**Start procedure** (from `evidence/README.md:127-135`): copy `_TEMPLATE.md` → `evidence/{finding-id}.md` using the sanitized filename; fill header; cite BOTH primary sources with line ranges BEFORE a verdict; add §3b dataset evidence (CLM/DATA rows); record verdict + before/after + AC + transition log; update `24-ISSUE-LEDGER.md` in the SAME commit.

**12-section heading set** (replicate exactly, in order — `_TEMPLATE.md:1-111`):
```
# Evidence Packet: <ID> - <Title>
## Header                              (table: ID, Title, Severity, Current Status, Current Verdict, Phase, Acceptance Check ID, Spec Sections Touched, Code Paths Touched)
## Source Positions                    (side-by-side table: resolution-doc row + issue-doc row, both line-ranged)
## Spec Evidence
### Dataset Evidence (§3b)             (CLM-/DATA- rows from 24-VERIFIED-FACTS.md with line ranges)
## FUT-01 Hand-off Note                (forward-pointing live-code refs ONLY; never grounding)
## First-Principles Physics Check      (REQUIRED only if EVID-10; else optional)
## Verdict                             (exactly one enum value)
## Root-Cause Framework Ambiguity      (EVID-10 only)
## Locked Convention                   (EVID-10 only)
## Which Source Was Correct / Wrong    (EVID-10 only)
## Before / After Spec Note            (doubles as EVID-08 false-positive record)
## Named Acceptance Check
## Status Transition Log
```

**Header table format** (copy column structure from `m11-m12-severity.md:5-15`):
```
| Field | Value |
|---|---|
| ID | `B-06` |
| Title | `Stage 4→5 trajectory-validation / admission gate` |
| Severity | `BLOCKING` / `MAJOR` / `MINOR` / `INFO` |
| Current Status | `IN_PROGRESS` -> `FIX_APPLIED` -> `VERIFIED` (advance as the loop runs) |
| Current Verdict | one of: accept-resolution / accept-issue-doc / accept-third-position / reject-both-as-unsupported / defer-with-blocker |
| Phase | `Phase 26` |
| Acceptance Check ID | `AC-PIPE-01` (cite reserved ID; mint none) |
| Spec Sections Touched | exact ctl_instruction.md section names |
| Code Paths Touched | `Not code-applicable` |
```

**Source Positions table** (both primary sources required even for uncontested verdicts — `_TEMPLATE.md:28`; format from `m11-m12-severity.md:21-24`). Citation format for the resolution doc is `path §N Q-XX:Lx-Ly`; for the issue doc `path:Lx-Ly`; the §3b dataset rows are `CLM-NN:Lx-Ly` / `DATA-NN:Lx-Ly`. Use directory-qualified paths (Specific Ideas: a v1.4 "B-06" namesake exists — never bare).

**Verdict enum** (exactly one — `evidence/README.md:33-45`): `accept-resolution`, `accept-issue-doc`, `accept-third-position`, `reject-both-as-unsupported`, `defer-with-blocker`. Per D-01, a candidate that fails current-spec / verified-facts / first-principles review routes to `accept-third-position` or `reject-both-as-unsupported`; a newly discovered cross-source conflict triggers EVID-10 (fill the four conflict sections BEFORE the verdict).

**Status Transition Log line format** (copy verbatim — `m11-m12-severity.md:143-144`, `_TEMPLATE.md:108-109`):
```text
2026-MM-DD <SHA> PENDING -> IN_PROGRESS (Phase 26 PNN by agent-or-user)
```
Each entry: `date`, `commit short SHA`, `status transition`, `(actor / plan reference)`. Every transition is mirrored in `24-ISSUE-LEDGER.md` with the same SHA + plan ref in the same commit.

**EVID-10 note:** B-06/B-11/D7/M13/D-03 are NOT pre-flagged EVID-10 (the three pre-flagged were SCS/D=6.694/M11-M12, already done in Phase 25). The four conflict sections (First-Principles, Root-Cause, Locked Convention, Which Source) stay empty/optional UNLESS a new cross-source conflict surfaces during adjudication — then they become required before verdict (`evidence/README.md:69-79`).

---

### `evidence/{m13}.md` — STOP-gap-shaped packet (special handling, D-12)

**Analog:** same 12-section schema, but the **Verdict** section follows the `defer-with-blocker` path and the **M11 GUARD block pattern** (`m11-m12-severity.md:95`) is the model for documenting that the source-silence guard triggers were checked.

**D-12 decision rule (replicate the GUARD discipline):** author from a full read of `02-resolution-doc.md:255-293` (§3.4 Q-A4) + OI-7. Then either (a) adopt the no-fallback candidate verdict IF fully grounded and consistent with locked conventions, OR (b) if ANY facet is source-silent/conflicting — including whether OI-7's label-semantics defeater disposes of the roadmap's STOP-gap expectation (Phase 26 success criterion 4 controls) — surface `GAP-26-NN` and set the packet verdict to `defer-with-blocker`, ledger status `DEFERRED` with written blocker. **Never invent the label-semantics ruling.** The parent agent (not this packet) writes `26-GAPS.md`.

**Proposed-spec-text is explicitly conditional** (`02-resolution-doc.md:274-290`): if adopted, a note under Step-5 stage-assignment "conditional on the label-semantics ruling; if the ruling goes the other way, replace with a STOP-gap marker." Record this conditionality in the Before/After Spec Note.

---

### `evidence/{d-03}.md` — user-gate packet (D-11)

**Analog:** same 12-section schema. The differentiator is process, not structure: the **Verdict is not selected by any execution mode** (including `--auto`). The packet presents HDF5 vs `.npy`/`.npz` vs txt/json as **candidate recommendation** with verified evidence (DATA-06 distributions, scale facts from `24-VERIFIED-FACTS.md`), authored inside a dedicated `autonomous: false` plan (precedent 23-02, 24-04). The user-locked choice is then recorded in `ctl_instruction.md`, this packet, and the ledger in ONE commit.

---

### `evidence/m11-m12-severity.md` — M11 extension (D-06, modify-not-duplicate)

**Analog:** the file's own existing M11 sub-parts (the M11/M12 dual-finding pattern is already established in it).

**What to add (M11 only — NEVER touch M12 content, Phase 27 owns it):**
- An M11-specific **Before/After Spec Note** for the PIPE-03 edit (the existing §Before/After at lines 122-132 has M11 Before/After but states "no framework-spec edit (D-02)"; Phase 26 adds the actual PIPE-03 spec landing — Step-1A clause 1 + a loader-contract note in `ctl_instruction.md`, per `02-resolution-doc.md:242-251`).
- New **Status Transition Log** entries (append below line 144) advancing M11: `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`, each with SHA + Phase 26 plan ref.
- OI-8 stays in the **§4 FUT-01 Hand-off Note** ONLY (`m11-m12-severity.md:49`); never promoted to grounding.
- The existing **M11 GUARD** record (line 95, not-triggered) is preserved; do not re-run unless new silence surfaces.

The locked M12 rule in this file (`m11-m12-severity.md:105-113`, `n_pts = min(n_pts_cap, n_snapshots)`) is the thing **B-06's packet CITES** for snapshot minimums (D-02) — cite by path+line, never re-decide.

---

### `evidence/README.md` — ID→Filename Map row (modify, same commit as each new packet)

**Analog:** the existing map table (`evidence/README.md:119-125`):
```
| Ledger ID(s) | Packet Filename |
|---|---|
| `SCS` | `evidence/scs-thresholds.md` |
| `D=6.694` | `evidence/compute-globals-D.md` |
| `M11`, `M12` | `evidence/m11-m12-severity.md` |
```
**Sanitization rule** (`evidence/README.md:117,125`): replace any char not in `[A-Za-z0-9_-]` with `-`, trim repeated `-`, lower-case. Five new filenames (B-06, B-11, M13, D7, D-03) are the planner's discretion (D-05); add each map row in the SAME commit that adds its packet.

---

### `ctl_instruction.md` — primary spec edits (edit)

**Analog:** v1.4-locked contract sections (existing Step 1 / §2.6 / Step 5 structure). Landing anchors are pre-mapped in `26-RESEARCH.md` "Edit Targets" — re-confirm line numbers at edit time (formatting passes shift lines):

| Finding | Landing point | Current anchor |
|---------|---------------|----------------|
| B-06 | new "Step 1A — Trajectory Admission Gate" after Step 1 item list, before Step 2 | between L381 and L383 (`## Step 2`) |
| B-11 | Step 1 appended item + cross-ref from Step 5 | after Step 1 item 6 (L378); Step 5 L1061-1068 |
| M11 | inside Step-1A clause 1 + loader-contract note | Step-1A region (co-located with B-06) |
| M13 | conditional note under Step-5 paragraph (or STOP-gap marker) | Step 5 L1061-1068; Stage 5/6 L229-249 |
| D7 | Step 1 item 3 (replacement) + §2.6 amendment | item 3 = L351-360; §2.6 = L628-648 |
| D-03 | Step 1 item 6 (replacement) | L374-378 ("HDF5 or NumPy (.npy)") |

**Edit perimeter (D-04):** zero edits outside `ctl_instruction.md` / `pinn_architecture.md`. `data_quality_assessment.md` citable, NEVER editable (SCOPE-09). Keep edits data-side and OUT of the batch-construction text (§3.1 / Mini-Batch Construction L1197-1212) — that surface is Phase 27 (M12/PIPE-04). Do NOT fold the F-1 stratification-table transposition fix (`ctl_instruction.md:26-27`) into any Phase 26 edit — it has no Phase 26 requirement ID.

**Packet-before-edit (hard rule, `evidence/README.md:99-101`):** no spec edit without a completed packet + verdict for that finding.

---

### `pinn_architecture.md` — secondary spec edits (edit only if required)

**Analog:** §3.1 / §5.2 Network Input Contract (L749-763) / §5.3.1 PHYS-02 region (L833). D-04: edit ONLY where a candidate text requires an architecture-side statement; the six candidates are predominantly data-side (`ctl`). Any B-06/B-11 cross-reference must avoid the §3.1 batch-construction surface (Phase 27).

---

### `24-ISSUE-LEDGER.md` — status + Per-Finding rows (modify, same commit as edit)

**Analog:** the M11 row (`24-ISSUE-LEDGER.md:25`) and the M11 Per-Finding subsection (`:113-140`) — the only row already carrying a verdict and a forward-looking transition.

**Status Table row format** (`:21-22` header; copy column set):
```
| ID | Title | Phase | Status | Verdict | Sources Disagree? | Evidence Packet | Acceptance Check | Spec Section | Dependents | Last Updated |
```
Evidence Packet is a relative markdown link, e.g. `[m11-m12-severity.md](../25-evidence-framework-and-issue-ledger/evidence/m11-m12-severity.md)`.

**Per-Finding subsection format** (copy from `:95-140`): heading `### <ID>: <Title> (Phase 26 PIPE-0X)`, then `Acceptance check:`, `Owning requirement:`, optional `Note:`/`Verdict:` prose, then a `Status transition log:` bullet list. **Transition-log line format** (`:139-140`):
```
- 2026-06-NN <SHA> IN_PROGRESS -> FIX_APPLIED (Phase 26 PNN by agent; AC-PIPE-0X; <one-line audit label>)
```
**Synthesis rows (D-07):** G1/G2/G3/G4 get NO packet; each closes with its parent (B-06/B-11/M11/M13) and the closure is annotated in the parent's Per-Finding note — e.g. `D-12 (synthesis-view close-with-parent): G1 closes with B-06 — no separate evidence packet` (model: M11's `:131` G3 annotation).

**Same-commit discipline (D-08):** ledger status edits + Evidence-Packet links travel in the SAME commit as the spec edit. Splitting them is a process defect.

**Phase-exit gate (`24-ISSUE-LEDGER.md:82`):** the ten in-scope rows may exit ONLY at `VERIFIED` or `DEFERRED`. `FIX_APPLIED` is not closure.

---

### `26-GAPS.md` — STOP-gap register (create on first gap; M13 most likely)

**Analog:** `25-GAPS.md` (GAP-25-01, GAP-25-02 are complete worked examples).

**Per-gap field set (replicate ALL fields — `25-GAPS.md:7-26`):**
```
## GAP-26-NN - <one-line title>

- **Decision point:** <what is decided, 1-2 sentences>
- **Where in artifact:** <file:section/line>
- **Task context:** <task running when gap hit>
- **Classification:** semantic / operational coordination / process-artifact schema / cross-phase reframing
- **Source silence:** <citation per consulted source + why it did not answer (file:line)>
- **Mathematical / engineering grounding:** <articulation of the math/physics/engineering at stake>
- **Agent was tempted to:** <what + rationale>
- **What the user needs to decide:** <A./B./C. concrete options>
- **Confidence of impact:** HIGH/MEDIUM/LOW with one-sentence reason
- **Status:** OPEN  (→ RESOLVED-WITH-INSTRUCTION / DEFERRED)
- **Resolution note:** <empty until user instruction>
```
End with a `## Milestone-wide index` note mirroring to `.planning/milestones/v1.5-GAPS.md` (`25-GAPS.md:51-53`). **Only the parent agent writes this file** — subagents return findings (Governance). Before recording, pass the three-question understanding check (CLAUDE.md STOP protocol step 2).

---

### Disposable probe captures (verify step, D-14/D-15)

**Analog:** the M11/M12 **First-Principles Physics Check** arithmetic block (`m11-m12-severity.md:54-69`) for inline spec-consistency probes, and Phase 24 probe commands recorded per-row in `24-VERIFIED-FACTS.md` for dataset probes.

**Pattern:** each packet's **Named Acceptance Check** section defines the reserved AC (AC-PIPE-01/02/03/05/06/10 — mint none) numerically per VER-07: pass criterion + data it runs on + exact command/function (candidate design = resolution-doc part-5 "verification suggestion"). Phase 26 EXECUTES the check via a disposable probe to move the row to `VERIFIED`; capture command + output re-derivably in the packet (SCOPE-06). If a script is used, it lives under the phase directory, NEVER under `pinn/`.

## Shared Patterns

### Citation discipline (apply to every packet, ledger row, gap entry)
**Source:** `evidence/README.md:24-31`, Specific Ideas (ID-namespace caution).
- BOTH primary sources cited with line ranges before any verdict; `data_quality_assessment.md` citable but never editable.
- §3b dataset evidence cites CLM-/DATA- rows from `24-VERIFIED-FACTS.md` — cite rows, never re-derive.
- Every citation directory-qualified (a v1.4 "B-06" namesake exists; never bare line-range or bare ID).
- Resolution-doc line anchors are stable to the 820-line 2026-06-11 revision; re-verify if re-delivered; §/Q-ID anchors are stable.

### Status lifecycle + same-commit ledger (apply to all 10 in-scope rows)
**Source:** `evidence/README.md:48-67`, `24-ISSUE-LEDGER.md:72-82`, D-08.
- Forward path `PENDING -> IN_PROGRESS -> FIX_APPLIED -> VERIFIED`; `DEFERRED` absorbing with written blocker.
- Each transition in BOTH the packet transition log AND the ledger Per-Finding log, same SHA + plan ref, same commit as the underlying edit.
- After each plan, re-verify previously `VERIFIED` findings sharing edited spec sections / `Dependents`; regression demotes to `IN_PROGRESS` (B-06 & B-11 share the Step-1 region; D7 & B-06 touch the footer/completeness boundary — order accordingly).

### Commit machinery (apply to every plan)
**Source:** D-10, CLAUDE.md Git governance.
- One atomic commit per plan via `scripts/agent-commit` (`GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`; explicit owned paths only, no `git add .`/`-A`/`-u`).
- Commit scope `26` or `26-NN`; body required (`.planning/` + spec edits). Tag `v1.5-pre-phase-26` cut from `milestone/v1.5` HEAD at execution start.
- STATE.md mutations only via gsd-tools handlers.

### Cross-phase file writes are BY DESIGN (do not "fix")
**Source:** Specific Ideas, Phase 25 D-05/D-06.
- Packets live under the **Phase 25** `evidence/` dir; the ledger lives under the **Phase 24** dir; Phase 26 writes into both. Locked by roadmap — do not relocate.

### Caveat propagation (D-13)
**Source:** 26-CONTEXT D-13, 24.5-READINESS-REPORT.
- OI-6 (no-footer probe-coverage gap) → B-06 and D7 packets; OI-7 → M13; OI-8 (M11 live-loader) → M11 §4 FUT-01 Hand-off ONLY; OI-9 (DATA-05 70-file rerun validated 2026-06-11) → wherever D7 footer evidence touches rerun files; OI-12 (CLM-08 transcription slip) → cite corrected decomposition (1,754@1e-13 + 592@1e-14), do not propagate the slip.

## No Analog Found

None. Every Phase 26 artifact has a committed Phase 25 / Phase 24 analog (the evidence machinery was
purpose-built in Phase 25 for exactly this consumption). The only "novel" elements are the five new
finding-specific filenames and the spec-section landing prose — both are instantiations of existing
patterns, not new structures.

## Metadata

**Analog search scope:** `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/` (template, README, 3 committed packets), `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md`, `.planning/phases/25-evidence-framework-and-issue-ledger/25-GAPS.md`.
**Files scanned:** 7 analog files read in full + 2 phase-context files.
**Pattern extraction date:** 2026-06-12
**Read-only constraint honored:** no source/spec/ledger/packet/gap file modified; only `26-PATTERNS.md` written.
