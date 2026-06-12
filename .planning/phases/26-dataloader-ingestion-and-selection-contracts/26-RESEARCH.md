# Phase 26: DataLoader Ingestion and Selection Contracts - Research

**Researched:** 2026-06-12
**Domain:** Spec-adjudication (in-repo corpus pre-mapping; NOT web/technology research)
**Confidence:** HIGH (corpus is fixed and fully cited; the two USER-decision findings are deliberately left open)

> **Nature of this research.** Phase 26 adjudicates six Issue-02 Cluster-A findings against a fixed
> in-repo corpus and transcribes the surviving candidate verdicts into `ctl_instruction.md`
> (primary) / `pinn_architecture.md` (secondary). This document pre-maps that corpus — candidate
> verdict direction, proposed-spec-text location, verification suggestion, caveats, edit landing
> points, ledger state, and acceptance-check design — so the planner can write precise,
> citation-grounded plans. It proposes **no** verdicts and fills **no** source silence. Two findings
> (D-03 / PIPE-10 format, M13 / PIPE-05 fallback) are USER decisions and are presented as evidence +
> candidate positions only. Subagent governance: this file is the only output; no gap-register, spec,
> ledger, or evidence-file writes were made.

---

<user_constraints>
## User Constraints (from 26-CONTEXT.md)

> 26-CONTEXT.md is `--all --auto`: all gray areas auto-selected by Claude under "provide context,
> stop before planning"; the two user-reserved findings (D-03, M13) are explicitly NOT auto-decided.
> Decisions below are copied verbatim in substance from 26-CONTEXT.md `<decisions>`.

### Locked Decisions

- **D-01 — Candidate-edit consumption.** Each finding's spec edit starts from the resolution doc's
  part-6 "proposed specification text" as the *candidate* edit. Transcribe unless current-spec
  evidence, `24-VERIFIED-FACTS.md` CLM/DATA rows, or first principles show the position fails. A
  failing candidate routes to `accept-third-position` / `reject-both-as-unsupported`; any newly
  discovered cross-source conflict triggers EVID-10 (full conflict sections before any edit).
- **D-02 — Hard constraints, not re-adjudicable.** v1.4-locked conventions (14D input, Jacobi IC₁₃,
  mass-weighted COM head, PHYS-03 softening, PHYS-01 raw-mass D, post-v1.3 SCS gate) AND Phase 25
  EVID-10 locks (SCS log gate stands; raw-mass `D ≈ 4.6416`; M12 `n_pts = min(n_pts_cap, n_snapshots)`;
  M11 BLOCKING). Where B-06's admission gate touches snapshot minimums, the packet **cites** the locked
  M12 rule (`evidence/m11-m12-severity.md`) — Phase 26 does NOT re-decide sampling feasibility (M12's
  edit is Phase 27's). Overturning a locked convention is a STOP gap, never an autonomous verdict.
- **D-03 (context) — Placement.** `ctl_instruction.md` is the primary home for all six contracts;
  `pinn_architecture.md` edited only where the candidate text requires an architecture-side statement.
  Exact heading/numbering placement is presentation-level discretion, recorded in each packet's
  before/after note.
- **D-04 — Edit perimeter.** Zero edits outside `ctl_instruction.md` / `pinn_architecture.md`.
  `data_quality_assessment.md` citable but never editable; live-loader facts (OI-8) appear only in §4
  FUT-01 Hand-off Notes, never as grounding.
- **D-05 — Packet-before-edit.** One packet per finding at `evidence/{finding-id}.md` (copied from
  `_TEMPLATE.md`), authored immediately before that finding's spec edit. New packets expected for
  B-06, B-11, M13, D7, D-03; M11 reuses its existing packet (D-06).
- **D-06 — M11 reuses its existing packet** (`evidence/m11-m12-severity.md`); Phase 26 EXTENDS (M11
  before/after note + status transitions), never duplicates. M12 content in that file is untouched.
- **D-07 — Synthesis rows.** G1/G2/G3/G4 get no separate packets; each closes with its parent
  (B-06/B-11/M11/M13), annotated in per-finding ledger notes.
- **D-08 — Batch and regression discipline.** Batch = one GSD plan. Ledger status edits + evidence-packet
  links travel in the same commit as the underlying change. After each plan, re-verify previously
  `VERIFIED` findings sharing edited spec sections / `Dependents`; regression demotes to `IN_PROGRESS`.
  Phase exit permits only `VERIFIED` or `DEFERRED` for the ten in-scope rows.
- **D-09 — Ordering.** Autonomous, well-grounded first: B-06 and B-11 (interlinked), M11 (verdict
  locked, edit-ready), then D7. The two user-interaction findings (M13, D-03) sit in dedicated plans
  isolated from the autonomous chain (dependency-scoped blocking). Wave structure is the planner's call.
- **D-10 — Operational mechanics.** Tag `v1.5-pre-phase-26` from `milestone/v1.5` HEAD at execution
  start; one atomic commit per plan via `scripts/agent-commit` (`GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`;
  no broad staging); commit scopes `26` / `26-NN`; STATE.md mutations only via gsd-tools handlers.
- **D-11 — PIPE-10 / D-03 is a mandatory USER gate.** Dedicated `autonomous: false` plan (precedent
  23-02, 24-04) presenting HDF5 vs `.npy`/`.npz` vs txt/json with verified evidence and the §3.6 Q-A6
  position (HDF5 canonical, `.npy`/`.npz` derived, JSON inspection-only) as **candidate recommendation,
  not pre-locked choice**. No execution mode (including `--auto`) may select for the user. User-locked
  choice recorded in `ctl_instruction.md`, the D-03 packet, and the ledger in one commit.
- **D-12 — PIPE-05 / M13 decision rule.** Packet authored from a full read of §3.4 Q-A4
  (`02-resolution-doc.md:255–293`) plus OI-7. Then: (a) if the resolution doc's no-fallback position is
  fully grounded and consistent with locked conventions, adopt it as candidate verdict (Stage-5
  gold-existence check + explicit no-fallback policy); (b) if ANY facet of the fallback choice remains
  source-silent or conflicting — including whether OI-7's "defeater" genuinely disposes of the roadmap's
  STOP-gap expectation (Phase 26 success criterion 4 controls) — surface as `GAP-26-NN` for user
  decision, never invented. **Pre-registered as the phase's most likely STOP gap.**
- **D-13 — Caveat propagation.** Before adjudicating each finding, propagate carried resolution-doc
  caveats into its packet: OI-6 → D7; OI-7 → M13; OI-8 → M11 §4 FUT-01 Hand-off only; OI-9 (DATA-05
  70-file rerun executed+validated 2026-06-11; quarantine clause liftable on re-verification) →
  wherever D7's footer evidence touches the rerun files.
- **D-14 — Define AND run per finding.** Each packet defines its reserved acceptance check
  (AC-PIPE-01/02/03/05/06/10 — no new AC-IDs) numerically per VER-07: pass criterion, data it runs on,
  exact command/function. Resolution-doc part-5 "verification suggestion" is the candidate check design.
  Phase 26 **executes** each check via a disposable probe to move its row to `VERIFIED` before phase
  exit; Phase 29 later rebuilds and re-executes the full suite (VER-09). Checks are spec-consistency
  and/or dataset probes reusing Phase 24 commands; no probe touches `pinn/`.
- **D-15 — Probe hygiene.** Every probe's command + output is captured re-derivably in the packet
  (SCOPE-06); disposable probe scripts, if any, live under the phase directory, never under `pinn/`.

### Claude's Discretion
- Exact packet filenames for the five new packets (README sanitization rule; mapping recorded in
  `evidence/README.md`).
- Exact spec heading/numbering placement inside `ctl_instruction.md` (presentation-level; before/after
  notes).
- Wave structure and plan count (subject to D-09 ordering and D-11/D-12 isolation of user-gate work).
- Whether per-finding probes are inline commands in packets or small scripts under the phase dir
  (subject to D-15).

### Deferred Ideas (OUT OF SCOPE)
- M12 points-per-trajectory, precision/Decimal, dt_out/stage-query, `compute_globals` spec edits —
  **Phase 27** (PIPE-04/07/08/09; G5 closes there with M12).
- SCS/SASD/IPR/PSC canonical metric contracts — **Phase 28** (VAL-01..04).
- Acceptance-suite build + full execution, ledger close, SI-ledger reconciliation, FUT-01 handoff —
  **Phase 29** (VER-07/09/11/12).
- M16 collocation scaling, G6 causal training, training-loop usage of validation metrics — **doc-03**
  (SCOPE-11), each with a recorded forward-reference.
- DataLoader/TrajectoryValidator/TrajectoryIndex implementation — **FUT-01**.
- OI-3 calibration constants (SASD 0.5, IPR 1e-3, PSC grid, n_pts_cap=32) — Phases 27/28, not Phase 26.
</user_constraints>

---

<phase_requirements>
## Phase Requirements

Verbatim from `.planning/REQUIREMENTS.md:47–56` (PIPE rows) and `:67` (VER-07).

| ID | Description (verbatim) | Finding | AC-ID | Research Support |
|----|-----------------------|---------|-------|------------------|
| **PIPE-01** | Framework specs define the Stage 4→5 trajectory-validation gate contract (B-06): final-timestamp threshold, stage-dependent snapshot minimums, and rejection logging — as a DataLoader design contract. | B-06 (+G1) | AC-PIPE-01 | §B-06 below: candidate "Step 1A — Trajectory Admission Gate"; 7-clause gate; `>=200` floor rejected; cites locked M12 rule for snapshot minimums |
| **PIPE-02** | Framework specs define the ID-resolution contract (B-11): `id_to_path` mapping built from filesystem scan, with the explicit invariant that trajectory ID is never assumed equal to array index. | B-11 (+G2) | AC-PIPE-02 | §B-11 below: candidate Step-1 appended item; scan-built `id_to_path`; dual physical/record keys; CLM-04 (ID 3958 > 2749 count) grounds non-density |
| **PIPE-03** | Framework specs define the blacklist-exclusion contract (M11): load at DataLoader init, exclude, log the exclusion count, fail loudly if a blacklisted ID reaches a batch. | M11 (+G3) | AC-PIPE-03 | §M11 below: verdict already locked (BLOCKING STANDS); reuse `m11-m12-severity.md`; CLM-03 (65 IDs) grounds count |
| **PIPE-05** | Framework specs define the gold-counterpart contract (M13): Stage-5 gold-existence check plus the fallback policy (skip to Stage 6 vs flagged low-fidelity fallback). If sources are silent/conflicting on the fallback, surfaced as a gap for user decision, not invented. | M13 (+G4) | AC-PIPE-05 | §M13 below: candidate = no-fallback-by-entailment; OI-7 defeater (label semantics) live; **STOP-gap candidate** (D-12) |
| **PIPE-06** | Framework specs define the footer/parameter-heterogeneity contract (D7): `Result:` footer precedence, folder-default fallback, `tol_confidence` flag (`direct` vs `inferred`), and footer-as-metadata-only (completeness gate never depends on footer presence). | D7 | AC-PIPE-06 | §D7 below: candidate all-or-nothing footer model; per-field provenance; OI-6 no-footer probe-coverage caveat |
| **PIPE-10** | The training-data format decision (D-03: HDF5 vs .npy vs txt/json) is presented to the user with verified evidence; the user decides; the locked choice is recorded in the framework specs. | D-03 | AC-PIPE-10 | §D-03 below: **USER gate** (D-11); candidate = HDF5 canonical / `.npy` derived / JSON inspection-only; presented as evidence, never selected |
| **VER-07** | Every v1.5 contract has a numerically-defined acceptance check naming its pass criterion, the data it runs on, and the command or function that executes it — not just prose. | (all) | — | See "## Validation Architecture" below |
</phase_requirements>

---

## Summary

Phase 26 transcribes six Cluster-A ingestion/selection contracts from the candidate verdict source
(`02-resolution-doc.md` §3 Q-A1..Q-A6, lines 101–382) into the framework specs, gated by the Phase 25
evidence-packet machinery and grounded in Phase 24 verified facts. Four findings are well-grounded and
edit-ready under the locked verdicts (B-06, B-11, M11, D7); two are USER decisions (D-03 format; M13
fallback) that this research presents as evidence + candidate positions only.

The corpus is internally coherent and the candidate verdict directions are unambiguous for the four
autonomous findings: B-06 proposes a new "Step 1A — Trajectory Admission Gate" (7 clauses, `>=200`
floor rejected on verified cadence arithmetic); B-11 proposes scan-built `id_to_path` with a
dual-key (`physical_key`/`record_key`) abstraction and an explicit ID≠index invariant; M11 already
carries a locked BLOCKING verdict in `evidence/m11-m12-severity.md` and only needs its PIPE-03 spec
edit + status transitions; D7 proposes an all-or-nothing footer model with per-field provenance and a
`measured` `dt_out` cross-check. All four cite confirmed CLM rows from `24-VERIFIED-FACTS.md`.

The two open findings are the planning fulcrum. **M13 is the phase's pre-registered STOP-gap
candidate**: the resolution doc reaches a `defers-with-contract` direction (no fallback exists under
locked stage definitions) but explicitly preserves a live defeater (OI-7: whether Step-5 labels attach
to *simulations* or *IDs*) whose resolution flips the verdict; D-12(b) requires this to surface as
`GAP-26-NN` if any facet is source-silent or conflicting, and Phase 26 success criterion 4 wording
controls. **D-03 is a mandatory non-autonomous user gate** (D-11): the candidate is HDF5-canonical but
no execution mode may select for the user. Both must be isolated in dedicated plans so the autonomous
chain never blocks on user availability.

**Primary recommendation:** Order the plans B-06+B-11 (interlinked) → M11 (locked, edit-ready) → D7
(autonomous chain), with M13 and D-03 in dedicated isolated plans; for every finding follow the strict
loop adjudicate(packet)→edit→verify(disposable probe)→ledger-same-commit, citing — never re-deciding —
the D-02 locked conventions and the Phase 25 EVID-10 records.

## Architectural Responsibility Map

This is a documentation/spec-adjudication phase. Capabilities are **spec contracts**, not running
software; the "tier" is the contract's conceptual owner in the eventual DataLoader. Mapping prevents
the planner from drifting into FUT-01 implementation scope.

| Capability (contract) | Primary Tier | Secondary Tier | Rationale |
|------------------------|-------------|----------------|-----------|
| B-06 admission gate | DataLoader init (data-side) | — | Runs once at init, before stage assignment / `compute_globals` / batching (resolution §3.1 clause ordering) |
| B-11 ID resolution / `id_to_path` | DataLoader init (data-side) | — | Scan-built index at init; never positional; Step-5 stage labels keyed by `record_key` |
| M11 blacklist exclusion | DataLoader init + batch assembly | — | Load+exclude at init (before statistics); defense-in-depth assertion at batch assembly |
| M13 gold-counterpart / Stage-5 stratum | Stage-assignment (curriculum) | DataLoader init | Stratum built by iterating gold folder files; gold-missing set computed at init |
| D7 footer/parameter metadata | Parse/preprocess (Step 1, §2.6 metadata) | — | Per-record metadata; explicitly metadata-only, never a gate input |
| D-03 storage format | Processed-data store (Step 1 item 6) | — | HDF5/`.npy`/JSON choice for the processed-training-data artifact |

**Scope boundary (binding):** every contract is a *data-side spec statement*. FUT-01 builds the actual
DataLoader/TrajectoryValidator/TrajectoryIndex; the live loader (`pinn/`) is NOT grounding (SCOPE-10).
Live-loader facts appear only in each packet's §4 FUT-01 Hand-off Note (e.g., M11 OI-8).

## Candidate Verdict Source Map (the six findings)

> Source: `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md`
> (820 lines, 2026-06-11 revision; **NOT authoritative — candidate only**). Line anchors are stable to
> this revision; re-verify if the doc is re-delivered (§/Q-ID anchors are stable across re-pagination).
> 7-part subsection structure: 1=verdict · 2=reasoning · 3=evidence · 4=confidence · **5=verification
> suggestion** · **6=proposed spec text** · 7=consolidation provenance.

Each subsection below records: candidate verdict direction, proposed-spec-text location (part 6),
verification suggestion (part 5), and the caveats/open items touching it. **`[CITED: ...]`** tags mark
references into the fixed corpus; **`[ASSUMED]`** is used only where this research relies on training
knowledge (rare here — this is a corpus-mapping task).

### B-06 (Q-A1) — Stage 4→5 trajectory-validation / admission gate [PIPE-01, AC-PIPE-01]

- **Candidate verdict direction:** *recommends-change* `[CITED: 24.5-RESOLUTION-MAP.md:96]`. A
  trajectory admission gate runs at DataLoader init between Stage-4 metric generation and any training
  use; a record `(variant, fidelity, id)` is admitted iff all 7 clauses hold, every rejection logged
  `(variant, id, reason_code)`, per-variant counts logged at init `[CITED: 02-resolution-doc.md:105–117]`.
  **The issue doc's `snapshot_count >= 200` floor (P1-1) is rejected** `[CITED: 02-resolution-doc.md:117]`.
- **7 gate clauses** `[CITED: 02-resolution-doc.md:107–115]`: (1) identity & blacklist (per Q-A2/Q-A3,
  before stage assignment and `compute_globals`; missing blacklist = hard init failure); (2) DATA-05
  quarantine of the 70 base-hier IDs `0005–0059, 0061–0075`; (3) structural integrity (≥2 snapshots,
  3 body rows, finite, strictly increasing timestamps — the issue doc's "≥2 for Stage 0–3 only"
  tiering is dropped); (4) completeness `final_timestep >= 9.5` from parsed block times, never footer/
  line counts; (5) conservation gate (locked HC-5: reject `ε_H > 1e-5` ≡ `SCS > -5`; `|H(0)|≈0` ⇒
  quarantine); (6) physical-invariant gates (§2.1 mass-invariance `<1e-15`, Q-B2 IC↔Brutus t=0 mass
  gate, §2.6 COM/momentum); (7) grid-consistency at **WARN** (not reject): warn if `max Δt > 1.5·dt_out`
  or `n_snapshots < 0.9·(final_timestep/dt_out + 1)`.
- **Proposed spec text (part 6):** new "Step 1A — Trajectory Admission Gate" inserted **after Step 1's
  item list, before Step 2** in `ctl_instruction.md` `[CITED: 02-resolution-doc.md:127–174]`. (Landing
  point in current spec: between line 381 end-of-Step-1 and line 383 "## Step 2" — see Edit Targets.)
- **Verification suggestion (part 5)** `[CITED: 02-resolution-doc.md:125]`: extend DATA-06 probe to
  no-footer files; publish per-variant `final_timestep`/`n_snapshots`/`max Δt/dt_out` distributions
  split by footer presence. Unit tests enumerated (truncated-at-t=5 rejects `completeness`; 1-snapshot
  rejects `structure`; injected `ε_H=2e-5` rejects `scs_gate`; interior gap `3·dt_out` admits with
  `grid_irregular`; base-hier `0005` quarantines `data05_stale`; complete 59-snapshot standard-base
  **admits**).
- **Caveats / open items:** **OI-6** `[CITED: 02-resolution-doc.md:767]` — the no-footer populations
  (2,470 files) are uncharacterized by the CLM-10 snapshot probe (sample sizes coincide exactly with
  footer-bearing counts; F-8 `[CITED: 02-resolution-doc.md:750]`); this is exactly why clause 7 is WARN
  not reject (escalation conditional on characterizing those distributions). **D-02 interaction:** the
  gate's snapshot-minimum handling must **cite** the locked M12 rule (`n_pts = min(n_pts_cap,
  n_snapshots)`, `evidence/m11-m12-severity.md`) and must NOT re-open sampling feasibility — see
  26-CONTEXT §specifics "B-06 preview". **OI-9** — DATA-05 quarantine clause (clause 2) is liftable on
  re-verification (rerun executed+validated 2026-06-11; `24-ISSUE-LEDGER.md:65–70`).
- **Dataset grounding:** CLM-10 corrected medians 61/127/1003 `[CITED: 24-VERIFIED-FACTS.md:25]`;
  CLM-11 prevalence 1.000 across probe-applicable population `[CITED: 24-VERIFIED-FACTS.md:26]`; DATA-05
  70-ID quarantine `[CITED: 24-VERIFIED-FACTS.md:35]`.
- **Issue-doc source position (§2 of packet):** P1-1 `>=200` floor at issue-doc lines 57, 74, 283,
  337–348, 357 `[CITED: 02-resolution-doc.md:121]`.

### B-11 (Q-A2) — Non-contiguous IDs (ID ≠ array index) [PIPE-02, AC-PIPE-02]

- **Candidate verdict direction:** *recommends-change* `[CITED: 24.5-RESOLUTION-MAP.md:97]`. Identity =
  `(variant_folder, zero-padded 4-digit numeric ID)`; folder is the sole authority for variant/gold
  status `[CITED: 02-resolution-doc.md:180]`.
- **7-clause mapping contract** `[CITED: 02-resolution-doc.md:182–188]`: (1) build
  `id_to_path[variant][fidelity][id]` by **scanning** the four Brutus folders, regex
  `^brutus_(hierarchical|standard)_(\d{4})\.txt$` (anchored; non-matching logged+ignored); (2) IDs →
  `int` internally, `%04d` at boundaries; duplicate `(variant, fidelity, id)` = hard init error; (3)
  absent-key lookup = explicit miss, no positional fallback / no `paths[id]` / no
  density/contiguity/zero-base assumption; (4) deterministic iteration over **sorted present keys**,
  never `range(n_files)`; (5) dual keys — `physical_key = (family, id)` (blacklist, gold availability,
  IC labels) vs `record_key = (family, fidelity, id)` (file lookup, per-record metadata); (6) `Result:`
  footer paths never used for mapping; (7) init logs per folder: files found, IDs parsed, duplicates
  (must be 0), min/max ID span vs file count.
- **Proposed spec text (part 6):** `ctl_instruction.md` Step 1, **appended item** (cross-referenced
  from Step 5) `[CITED: 02-resolution-doc.md:200–217]`. (Landing point: after Step 1 item 6 at line 378,
  with cross-ref into Step 5 §line 1068 "mapping from each simulation ID to its assigned stage index").
- **Verification suggestion (part 5)** `[CITED: 02-resolution-doc.md:198]`: property test
  `max(parsed IDs) >= file_count` on standard base; unit tests (10 CLM-04 IDs miss against gold,
  resolve against base; planted duplicate triggers init error; base-only ID reports gold absent not
  error).
- **Caveats / open items:** none blocking; only modifying factor = a future >4-digit ID extension
  (widens regex, nothing else) `[CITED: 02-resolution-doc.md:196]`. Provenance: 8/8 unanimous
  `[CITED: 02-resolution-doc.md:219]`.
- **Dataset grounding:** CLM-04 (ID 3958 present while standard base count = 2,749 ⇒ ID space cannot be
  dense) `[CITED: 24-VERIFIED-FACTS.md:18]`; CLM-01 (1,250 gaps/2,749) `[CITED: 24-VERIFIED-FACTS.md:15]`;
  CLM-02 (143/4,857) `[CITED: 24-VERIFIED-FACTS.md:16]`; CLM-12 max IDs 3,998/4,999
  `[CITED: 24-VERIFIED-FACTS.md:27]`; CLM-05b base 2,749 / gold 2,565 / diff 184
  `[CITED: 24-VERIFIED-FACTS.md:20]`.
- **B-06↔B-11 coupling (planner note):** B-06 gate clause 1 ("the ID resolves per the Q-A2 contract")
  depends on B-11. They share the Step-1 region and are explicitly interlinked (D-09 orders them
  together). Plan them in one wave so the candidate texts are reconciled in a single before/after note.

### M11 (Q-A3) — Blacklist loading / consumption [PIPE-03, AC-PIPE-03]

- **Candidate verdict direction:** *recommends-change* `[CITED: 24.5-RESOLUTION-MAP.md:98]`;
  **verdict already LOCKED by Phase 25**: M11 MAJOR→BLOCKING reclassification **STANDS** on
  data-integrity grounds `[CITED: evidence/m11-m12-severity.md:91–95]` `[CITED: 24-ISSUE-LEDGER.md:25]`.
- **6-clause contract** `[CITED: 02-resolution-doc.md:223–231]`: (1) load
  `problematic_ics_blacklist.json` at init before stage assignment / `compute_globals`; (2) validate
  schema (exactly keys `hierarchical`+`standard`, integer-like IDs; else hard config error; normalize
  `int`, dedup); (3) IC-level exclusion — listed `(family, id)` excludes every realization base+gold of
  that `physical_key`; (4) missing/unreadable/invalid blacklist = hard init failure; override must be
  explicit, logged, dev-only; (5) logging per family (`n_blacklist_entries`, `n_present_on_disk` per
  fidelity, `n_excluded`); checklist's "exactly 65" re-keyed to parsed file content, never hard-coded;
  (6) defense-in-depth — set-membership assertion at batch assembly; a blacklisted sample in an emitted
  batch raises a hard error.
- **Proposed spec text (part 6):** carried inside the Step-1A gate (clause 1) PLUS a loader-contract
  note in `ctl_instruction.md` `[CITED: 02-resolution-doc.md:242–251]`.
- **Verification suggestion (part 5)** `[CITED: 02-resolution-doc.md:240]`: live-loader probe (does a
  blacklisted ID appear in any emitted batch?) is FUT-01/SCOPE-10; spec-side unit tests (init fails on
  absent file / third top-level key; listed ID never in manifest/batch; batch assertion trips when
  exclusion disabled; listed-but-absent-on-disk logs and proceeds).
- **Caveats / open items (CRITICAL for D-06):** **reuse** `evidence/m11-m12-severity.md` — do NOT
  author a new packet; Phase 26 EXTENDS it (M11 before/after note for the PIPE-03 edit + status
  transitions); M12 content in that file is **Phase 27's** and must not be touched. **OI-8** (live-loader
  consumption status) is outside grounding (SCOPE-10) → goes ONLY in the §4 FUT-01 Hand-off Note, never
  as grounding `[CITED: evidence/m11-m12-severity.md:43,151]`. The existing packet already records the
  M11 GUARD (D-10) as not-triggered `[CITED: evidence/m11-m12-severity.md:95]`.
- **Dataset grounding:** CLM-03 = 65 IDs (`{hierarchical: 2, standard: 63}`)
  `[CITED: 24-VERIFIED-FACTS.md:17]`; DATA-02 consumption map (legacy json; runners use
  `Documentation/problematic_ics/{type}/` dirs; `pinn/` unverified SCOPE-10)
  `[CITED: 24-VERIFIED-FACTS.md:64–72]`.

### M13 (Q-A4) — 184 standard IDs without gold counterpart [PIPE-05, AC-PIPE-05] — STOP-GAP CANDIDATE

- **Candidate verdict direction:** *defers-with-contract* `[CITED: 24.5-RESOLUTION-MAP.md:100]`.
  Per the master's annotation **no fallback is asserted**: under the locked stage definitions there is
  no fallback to choose — the spec's own semantics determine behavior, and both issue-doc options
  presuppose a per-ID Stage-5 obligation the spec does not create `[CITED: 02-resolution-doc.md:257]`.
  Both issue-doc options rejected: Option 2 (flagged low-fidelity into Stage 5) contradicts Stage-5
  data source + double-counts; Option 1 ("skip to Stage 6") vacuous (nothing skips; base label
  unchanged; reaches Stage 6 via replay) `[CITED: 02-resolution-doc.md:260–261]`.
- **Mandatory data-side contract (adopted unconditionally)** `[CITED: 02-resolution-doc.md:262]`:
  (i) compute gold-missing set at init as set difference of scanned base/gold ID sets, cross-checked
  vs CLM-04 184-ID list, never hard-coded; (ii) per-`physical_key` metadata `gold_counterpart ∈
  {present, absent}`; (iii) build Stage-5 stratum by iterating the **gold folder's actual files**,
  never by base-ID lookup into the gold index (which manufactures 184 spurious misses); (iv) never
  silently substitute a base-fidelity record into a gold-resolution slot.
- **THE STOP-GAP TRIGGER (preserved verbatim by the doc)** `[CITED: 02-resolution-doc.md:263]`: the
  entailment rests on stage labels attaching to *simulations* (`record_key`). **If** Phase-26
  adjudication rules labels attach to *IDs* (every Stage-4 ID must yield a Stage-5 sample), the
  no-fallback reading fails, neither issue-doc option is spec-derivable, and Q-A4 must surface as the
  Phase-26 STOP gap — not be resolved by invention. The textual hinge is `ctl` Step 5 line 1068 "a
  mapping from **each simulation ID** to its assigned stage index" `[CITED: ctl_instruction.md:1068]` —
  "simulation" vs "ID" readings diverge exactly here `[CITED: 02-resolution-doc.md:266]`. Confidence:
  **Medium** `[CITED: 02-resolution-doc.md:270]`.
- **Genuinely open residue (routed to user gate)** `[CITED: 02-resolution-doc.md:264]`: whether the
  project *wants* gold coverage for any of the 184 ICs (a re-simulation/resourcing decision outside
  loader policy); recommended selection input = intersection of gold-missing set with the SASD resample
  queue (Q-C2, a Phase 28 metric).
- **Proposed spec text (part 6) — explicitly conditional** `[CITED: 02-resolution-doc.md:274–290]`:
  a note under the Step-5 stage-assignment paragraph, **"conditional on the label-semantics ruling; if
  the ruling goes the other way, replace with a STOP-gap marker."** Landing point: under Step 5
  (line 1068) and/or the Stage 5/6 stratification text (lines 229–249).
- **Verification suggestion (part 5)** `[CITED: 02-resolution-doc.md:272]`: obtain a one-line
  framework-owner ruling on Step-5 label semantics (simulations vs IDs) — closes the conditional either
  way; re-verify gold-missing set by set difference (DATA-03 already did); unit test (Stage-5 stratum
  over a gold-less-ID fixture emits zero misses; that ID's base sample appears in Stage-5 training set
  via replay exactly once).
- **Caveats / open items — DECISIVE for D-12:** **OI-7** has two parts `[CITED: 02-resolution-doc.md:768]`:
  (a) the Step-5 label-semantics ruling — the entailment's defeater (framework owner, one line); (b)
  gold-rerun resourcing (user gate). The "Additional Input Needed" register names Q-A4 as the
  **#1 question warranting consultation of the original R1–R8 reports** (genuine three-way upstream
  split: entailment 3 / STOP-gap declaration 4 / low-fidelity-fallback 1)
  `[CITED: 02-resolution-doc.md:777]` `[CITED: 02-resolution-doc.md:292]`. **Planner directive (D-12):**
  the M13 packet is authored from a full read of §3.4 + OI-7; then either (a) adopt the no-fallback
  candidate IF fully grounded and consistent with locked conventions, OR (b) surface `GAP-26-NN` if ANY
  facet remains source-silent/conflicting — including whether OI-7's defeater genuinely disposes of the
  **roadmap's STOP-gap expectation** (Phase 26 success criterion 4 wording controls: it says "if the
  sources are silent or conflicting on the fallback choice, it is surfaced as a STOP gap for user
  decision"). The 26-CONTEXT pre-registers this as "the phase's most likely STOP gap" and "defers-with-
  contract" (§specifics). **Do not force a verdict; do not invent the label-semantics ruling.**
- **Dataset grounding:** CLM-04 = 184 (set difference exact match to
  `standard_quasi_random_ids_not_in_gold.md`) `[CITED: 24-VERIFIED-FACTS.md:18]`; CLM-05b base 2,749 /
  gold 2,565 / diff 184 `[CITED: 24-VERIFIED-FACTS.md:20]`.

### D7 (Q-A5) — Footer / parameter heterogeneity [PIPE-06, AC-PIPE-06]

- **Candidate verdict direction:** *recommends-change* `[CITED: 24.5-RESOLUTION-MAP.md:101]`.
  Footers are all-or-nothing; absent → verified folder defaults with per-field provenance
  `[CITED: 02-resolution-doc.md:296–305]`.
- **6-clause footer contract** `[CITED: 02-resolution-doc.md:298–303]`: (1) footer present → parse full
  schema `(tol, Lw, dt_out, t_end, eta, energies)`, provenance `direct` (presence ⇒ full schema under
  corrected facts); (2) footer absent (verified: 1,550 hier-base / 701 std-base / 219 std-gold) →
  folder defaults [std base `tol=1e-13,Lw=118,dt_out=0.17`; hier base `tol=1e-15,Lw=130,dt_out=0.08`;
  gold both `tol=1e-13,Lw=130,dt_out=0.01`], provenance `inferred`; **`eta` has no default → `null`,
  provenance `absent`** (fabrication prohibited); (3) partial-schema present footer = anomaly (log,
  `footer_anomalous=true`, default-fallback, surface — should be empty); (4) per-field
  `param_provenance` dict over `{tol, Lw, dt_out, eta}` ∈ `{direct, inferred, absent, measured}`; for
  `dt_out` additionally **measure** median inter-snapshot spacing (`measured`), warn on >1% disagreement;
  (5) negative uses — footers never a completeness signal (Q-A1) and never a mapping source (Q-A2); (6)
  destination — fields populate `ctl` §2.6 per-record metadata; `trustworthy_horizon` is **RESERVED**
  (undefined anywhere, OI-4/F-5).
- **Proposed spec text (part 6):** `ctl_instruction.md` **Step 1 item 3 (replacement)** PLUS a **§2.6
  amendment** `[CITED: 02-resolution-doc.md:315–341]`. Landing points: Step 1 item 3 is current
  lines 351–360 (the "optional trailing 'Result:' line" text); §2.6 metadata block is lines 628–648
  (the `param_provenance` map over `{brutus_tolerance, word_length, dt_out, eta}` and the
  `trustworthy_horizon` RESERVED marker land here; `trustworthy_horizon` currently named at line 648).
- **Verification suggestion (part 5)** `[CITED: 02-resolution-doc.md:313]`: footer scan over all 15,028
  files (already executed by `data04_footers.py`) — presence counts must reproduce
  3,307/1,550 — 2,048/701 — 2,346/219 — 4,857/0; tuple histogram matches; unit tests (footerless
  std-base → `tol=1e-13(inferred), Lw=118(inferred), eta=null(absent), dt_out measured≈0.17`; footer
  missing only `eta` sets `footer_anomalous`).
- **Caveats / open items:** **OI-6** (no-footer probe-coverage gap — the 2,470 no-footer files'
  distributions uncharacterized) `[CITED: 02-resolution-doc.md:767]` propagates into D7 per D-13.
  **OI-9** (DATA-05 70-file rerun executed+validated 2026-06-11) recorded wherever D7's footer evidence
  touches the rerun files per D-13 `[CITED: 02-resolution-doc.md:770]`. **OI-12** (addendum CLM-08
  summary-row transcription slip "2,346 tol=1e-13" — should read "2,346 with-footer"; the 592@1e-14
  verification is unaffected) `[CITED: 02-resolution-doc.md:773]` — do not let it propagate into the
  spec edit; cite the corrected decomposition (1,754@1e-13 + 592@1e-14 = 2,346 with-footer).
- **Dataset grounding:** CLM-07 = 219 std-gold no-footer (NO footer at all, NO param fields — D-07
  characterization corrects "partial/minimal footer") `[CITED: 24-VERIFIED-FACTS.md:22]`; CLM-08 = 592
  std-gold `tol=1e-14` (remaining 2,346 present-footer carry `tol=1e-13`) `[CITED: 24-VERIFIED-FACTS.md:23]`;
  CLM-09 folder-default `tol`/`dt_out` per variant `[CITED: 24-VERIFIED-FACTS.md:24]`.

### D-03 (Q-A6) — Processed training-data format [PIPE-10, AC-PIPE-10] — USER GATE

- **Candidate verdict direction (NOT a selected answer — D-11):** *recommends-change*
  `[CITED: 24.5-RESOLUTION-MAP.md:106]`. The framework names HDF5 **or** `.npy` (`ctl` Step 1 item 6),
  so both are spec-compliant; txt/json as a primary store is outside the recommendation
  `[CITED: 02-resolution-doc.md:347]`. Within the compliant pair, candidate recommendation: (1) HDF5
  canonical (groups `/{variant}/{fidelity}/{id}`, float64 datasets, per-group §2.6 metadata +
  `param_provenance` + raw-file SHA-256 + `schema_version`; chunked+compressed); (2) `.npy`/`.npz`
  acceptable as derived cache/export (awkward as sole store); (3) JSON/text inspection-only, never a
  training input path; (4) methodology consequences — float64 end-to-end (bitwise round-trip),
  auditability (store §2.6 transform metadata), determinism `[CITED: 02-resolution-doc.md:347–352]`.
- **Proposed spec text (part 6):** `ctl_instruction.md` **Step 1 item 6 (replacement)**
  `[CITED: 02-resolution-doc.md:362–377]`. Landing point: current lines 374–378 ("HDF5 or NumPy (.npy)").
  The D-03 ledger row names `ctl_instruction.md` **alone** (no architecture-side component)
  `[CITED: 24-ISSUE-LEDGER.md:38]` (26-CONTEXT §specifics confirms).
- **Verification suggestion (part 5)** `[CITED: 02-resolution-doc.md:360]`: round-trip test
  (parse raw → write store → read back → bitwise `np.array_equal` vs directly parsed float64, incl.
  times); schema test (every group carries full attribute set + `schema_version`); negative test
  (loader refuses a JSON path).
- **USER-GATE machinery (D-11):** dedicated `autonomous: false` plan (precedent 23-02, 24-04) presenting
  HDF5 vs `.npy`/`.npz` vs txt/json with **verified evidence** (DATA-06 snapshot/`dt_out`
  distributions, dataset-scale facts from `24-VERIFIED-FACTS.md`) and the §3.6 Q-A6 position as
  **candidate recommendation, not pre-locked choice**. **No execution mode (including `--auto`) may
  select for the user.** The user-locked choice is then recorded in `ctl_instruction.md`, the D-03
  packet, and the ledger in one commit.
- **Caveats / open items:** the only verdict-flipping factor named is "an unstated operational
  constraint forbidding HDF5 dependencies" `[CITED: 02-resolution-doc.md:358]` — exactly the kind of
  constraint only the user can supply, reinforcing the user-gate structure. External refs carried:
  h5py docs, NumPy `.npy`/`.npz` format docs `[CITED: 02-resolution-doc.md:356,801–802]`.
- **Dataset grounding:** the Q-A6 block itself carries no dataset facts `[CITED: 02-resolution-doc.md:357]`;
  evidence to present = scale facts (CLM-10 snapshot distributions `[CITED: 24-VERIFIED-FACTS.md:25]`,
  total 15,028 files, ragged-array nature).

## Evidence-Packet Machinery (the operating rules for every edit)

> Source: `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/README.md` +
> `_TEMPLATE.md` + `m11-m12-severity.md`.

- **Four EVID-06 sources** (every packet cites all applicable, with line ranges, before any verdict)
  `[CITED: evidence/README.md:24–29]`: (1) issue doc `02-data-pipeline-and-validation.md`; (2)
  resolution doc `02-resolution-doc.md` (`§N Q-XX:Lx-Ly`); (3) framework specs (`ctl_instruction.md` /
  `pinn_architecture.md` / read-only `data_quality_assessment.md`); (4) dataset-evidence annex
  `24-VERIFIED-FACTS.md` (CLM-/DATA-row IDs + line ranges — the §3b source, new in v1.5). BOTH primary
  citations required even for uncontested verdicts `[CITED: _TEMPLATE.md:28]`.
- **Verdict enum** (exactly one) `[CITED: evidence/README.md:33–45]`: `accept-resolution`,
  `accept-issue-doc`, `accept-third-position`, `reject-both-as-unsupported`, `defer-with-blocker`.
- **Status lifecycle** `[CITED: evidence/README.md:48–61]`: `PENDING → IN_PROGRESS → FIX_APPLIED →
  VERIFIED` (or `DEFERRED` with written blocker). `FIX_APPLIED` is NOT closure; `VERIFIED` requires a
  passing acceptance check. Every transition recorded in the packet's Status Transition Log AND mirrored
  in `24-ISSUE-LEDGER.md` with commit short SHA + plan reference.
- **EVID-10 trigger** `[CITED: evidence/README.md:69–79]`: pre-flagged for SCS, D=6.694, M11/M12
  severity (all already adjudicated in Phase 25). **Any further conflict** discovered between the two
  primary sources also triggers EVID-10 → fill `First-Principles Physics Check`, `Root-Cause Framework
  Ambiguity`, `Locked Convention`, `Which Source Was Correct/Wrong` BEFORE verdict/edit. Per D-01, a
  failing B-06/B-11/D7 candidate or a newly discovered cross-source conflict triggers this.
- **Packet-before-edit (EVID-06 D-03 enforcement)** `[CITED: evidence/README.md:99–101]`: no spec edit
  without a completed packet + verdict for that finding; ledger status edits + evidence-packet links
  travel in the same commit as the underlying change (splitting = process defect).
- **Phase-exit rule** `[CITED: evidence/README.md:89–93]`: no plan exits with an in-scope finding at
  `IN_PROGRESS` or `FIX_APPLIED`; allowed exit states are only `VERIFIED` / `DEFERRED`.
- **AC-ID reservations** `[CITED: evidence/README.md:103–113]`: Phase 25 minted **no new AC-IDs**;
  the seeded `AC-PIPE-01..10` / `AC-VAL-01..04` stand. **Phase 26 mints no new AC-IDs** — it cites the
  reserved ID its fix targets and defines its runnable pass criteria.
- **ID→Filename map + sanitization** `[CITED: evidence/README.md:115–125]`: existing `scs-thresholds.md`,
  `compute-globals-D.md`, `m11-m12-severity.md`. New packets sanitize the finding ID (replace non
  `[A-Za-z0-9_-]` with `-`, trim repeats, lower-case); the map in `evidence/README.md` is updated in
  the same commit that adds each packet. **Discretion (D-05):** the five new filenames (B-06, B-11, M13,
  D7, D-03) are the planner's call.
- **12-section packet schema** `[CITED: _TEMPLATE.md:1–111]`: Header; Source Positions; Spec Evidence
  (+ §3b Dataset Evidence); FUT-01 Hand-off Note; First-Principles Physics Check (EVID-10); Verdict;
  Root-Cause Framework Ambiguity (EVID-10); Locked Convention (EVID-10); Which Source Correct/Wrong
  (EVID-10); Before/After Spec Note (doubles as EVID-08 false-positive record); Named Acceptance Check;
  Status Transition Log.
- **M11 packet reuse (D-06):** `m11-m12-severity.md` already records M11 BLOCKING STANDS + M12
  accept-third-position; Phase 26 EXTENDS the M11 sub-part (PIPE-03 before/after note + status
  transitions); M12 sub-part is Phase 27's and stays untouched; the locked M12 rule is the thing B-06's
  packet **cites** for snapshot minimums `[CITED: evidence/m11-m12-severity.md:105–113]`.

## Ledger State (the ten in-scope rows)

> Source: `24-ISSUE-LEDGER.md` (stable path under the Phase 24 directory). All ten rows are currently
> `PENDING`. Synthesis rows G1–G4 close with parents (no separate packets, D-07). G5 is Phase 27's.

| Row | Status | Verdict (current) | AC-ID | Spec Targets | Dependents | Packet |
|-----|--------|-------------------|-------|--------------|-----------|--------|
| B-06 | PENDING | — | AC-PIPE-01 | ctl; pinn_arch | Q-A1 | new |
| B-11 | PENDING | — | AC-PIPE-02 | ctl; pinn_arch | Q-A2 | new |
| M11 | PENDING | **BLOCKING STANDS** (Phase 25) | AC-PIPE-03 | ctl; pinn_arch | Q-A3 | `m11-m12-severity.md` (extend) |
| M13 | PENDING | — | AC-PIPE-05 | ctl; pinn_arch | Q-A4 | new (STOP-gap candidate) |
| D7 | PENDING | — | AC-PIPE-06 | ctl; pinn_arch | Q-A5 | new |
| D-03 | PENDING | — | AC-PIPE-10 | ctl **alone** | Q-A6 | new (user gate) |
| G1 | PENDING | — | AC-PIPE-01 (synthesis over B-06) | ctl; pinn_arch | B-06 | close with B-06 |
| G2 | PENDING | — | AC-PIPE-02 (synthesis over B-11) | ctl; pinn_arch | B-11 | close with B-11 |
| G3 | PENDING | — | AC-PIPE-03 (synthesis over M11) | ctl; pinn_arch | M11 | close with M11 |
| G4 | PENDING | — | AC-PIPE-05 (synthesis over M13) | ctl; pinn_arch | M13 | close with M13 |

`[CITED: 24-ISSUE-LEDGER.md:23–32]`. Per-finding notes carry the AC-ID, owning requirement, and the
seeded `PENDING -> PENDING (seeded by Phase 24 P03)` transition `[CITED: 24-ISSUE-LEDGER.md:95–227]`.
M11's row already carries the BLOCKING-STANDS verdict and the OI-8 carry-forward
`[CITED: 24-ISSUE-LEDGER.md:124–140]`.

**Regression surface (D-08):** spec sections edited in Phase 26 become the regression surface for
Phases 27–28 (the `Dependents` field). After each Phase-26 plan, re-verify any previously `VERIFIED`
finding sharing an edited section; demote regressions to `IN_PROGRESS`
`[CITED: 24-ISSUE-LEDGER.md:80]`. Within Phase 26, B-06 and B-11 share the Step-1 region; D7 and B-06
both touch the footer/completeness boundary — order accordingly.

## Edit Targets (where each contract lands)

> Primary: `ctl_instruction.md`. Secondary: `pinn_architecture.md` (only where a candidate text requires
> an architecture-side statement). Exact heading/numbering is presentation-level discretion (D-03 of
> 26-CONTEXT). Line numbers below are anchored to the current spec; the planner should re-confirm at
> edit time (formatting passes can shift lines).

### `ctl_instruction.md` (primary)

| Finding | Candidate landing point | Current spec anchor |
|---------|------------------------|---------------------|
| B-06 | new "Step 1A — Trajectory Admission Gate" after Step 1 item list, before Step 2 | between line 381 (end of Step 1) and line 383 (`## Step 2`) |
| B-11 | Step 1 appended item, cross-ref from Step 5 | after Step 1 item 6 (line 378); Step 5 at line 1061–1068 |
| M11 | inside Step-1A clause 1 + a loader-contract note | Step-1A region (co-located with B-06) |
| M13 | conditional note under Step-5 stage-assignment paragraph (or STOP-gap marker) | Step 5 line 1061–1068; Stage 5/6 stratification lines 229–249 |
| D7 | Step 1 item 3 (replacement) + §2.6 amendment | Step 1 item 3 = lines 351–360; §2.6 metadata = lines 628–648 (`trustworthy_horizon` at line 648) |
| D-03 | Step 1 item 6 (replacement) | lines 374–378 ("HDF5 or NumPy (.npy)") |

`[CITED: ctl_instruction.md:340–382]` (Step 1), `[CITED: ctl_instruction.md:615–649]` (§2.6),
`[CITED: ctl_instruction.md:1061–1068]` (Step 5), `[CITED: ctl_instruction.md:229–249]` (Stage 5/6).

### `pinn_architecture.md` (secondary — architecture-side statements only)

The candidate texts for the six findings are predominantly data-side (`ctl`). `pinn_architecture.md`
edits are permitted but not mandated (ledger Spec Targets list it for B-06/B-11/M11/M13/D7 but D-04 of
26-CONTEXT scopes edits to "where the candidate text requires an architecture-side statement").
Relevant architecture-side anchors if a candidate text reaches them:
- §3.1 Data Fidelity Term / `get_batch(... points_per_trajectory=32)` and the author comment
  "batch construction is not consistent with the CTL instruction plan"
  `[CITED: pinn_architecture.md:292–351]` — note this is the M12/batch-construction surface (Phase 27);
  any B-06/B-11 cross-reference must avoid re-deciding it (D-02).
- §5.2 Network Input Contract `[CITED: pinn_architecture.md:749–763]`.
- §10.2-style acceptance-check region (the doc states "§10.2 acceptance checks" per the resolution
  doc's spec inventory `[CITED: 02-resolution-doc.md:790]`; the live anchor near §5.3.1 PHYS-02 is at
  `[CITED: pinn_architecture.md:833]`).

**Planner note:** keep Phase 26 edits data-side and out of the batch-construction text (§3.1 / Mini-Batch
Construction lines 1197–1212) — that surface belongs to Phase 27 (M12/PIPE-04). Flag to the planner if
a B-06 or B-11 candidate cross-reference would collide with it.

## Source-Silence and Cross-Source Findings (for the planner — never auto-filled)

Per the governance constraint, where source silence or cross-source conflict touches planning it is
DOCUMENTED here precisely; this research never proposes to fill it.

1. **M13 label-semantics ruling (OI-7a) — LIVE DEFEATER, pre-registered STOP-gap.** The no-fallback
   entailment depends on Step-5 labels attaching to *simulations* (`record_key`); the spec's own words
   "each simulation ID" (`ctl_instruction.md:1068`) are the ambiguous hinge. The resolution doc's own
   confidence is **Medium** and it names Q-A4 the #1 question warranting the (unavailable) R1–R8 reports
   `[CITED: 02-resolution-doc.md:266,270,777]`. **Disposition:** D-12 requires the M13 packet to surface
   `GAP-26-NN` for user decision if any facet is source-silent/conflicting; Phase 26 success criterion 4
   wording ("surfaced as a STOP gap for user decision") controls. The planner must NOT let any execution
   mode invent the ruling.
2. **M13 gold-rerun resourcing (OI-7b) — user gate, out of loader scope.** Whether to commission gold
   re-simulation for any of the 184 ICs is a resourcing decision `[CITED: 02-resolution-doc.md:264,768]`.
   Out of Phase 26's loader-contract scope; note as forward reference, do not decide.
3. **D-03 format choice — mandatory user gate (PIPE-10).** Not source-silence (the candidate is clear)
   but a requirement-mandated user decision: "the user decides" `[CITED: REQUIREMENTS.md:56]`. No
   execution mode may select (D-11).
4. **OI-6 no-footer probe-coverage gap.** The 2,470 no-footer files' snapshot distributions are
   uncharacterized; this is why B-06 clause 7 is WARN-not-reject and why D7's all-or-nothing model is
   "High confidence with one named overturning factor" `[CITED: 02-resolution-doc.md:123,311,767]`.
   **Not a Phase-26 blocker** (the candidate contracts are stated at WARN level precisely to avoid
   depending on it); record as a caveat in the B-06 and D7 packets (D-13). Escalating clause 7 to a hard
   floor would require the OI-6 probe extension — out of Phase 26 scope unless the planner chooses to run
   it as the AC-PIPE-01 disposable probe (see Validation Architecture).
5. **F-1 transposition (planner awareness, NOT a Phase 26 finding).** The `ctl` stratification table
   labels Set 1b as 4857/Standard and Set 2a as 2749/Hierarchical `[CITED: ctl_instruction.md:26–27]`,
   transposed relative to the verified counts (hier base 4,857 / std base 2,749). The resolution doc
   classifies this as a §6 cross-cutting spec-hygiene item (F-1), **not** one of the six Cluster-A
   findings `[CITED: 02-resolution-doc.md:736]`. **Disposition:** out of Phase 26's six-requirement
   scope; do NOT fold a table fix into a Phase 26 finding edit. If a D7/B-06 edit must reference these
   counts, cite `24-VERIFIED-FACTS.md` (CLM-05b/06), not the transposed table. Flag to the planner so it
   is not silently "corrected" inside a Phase 26 commit (it has no Phase 26 requirement ID).
6. **OI-12 addendum CLM-08 slip.** "2,346 tol=1e-13" should read "2,346 with-footer"; the 592@1e-14
   verification is unaffected `[CITED: 02-resolution-doc.md:773]`. The D7 packet must cite the corrected
   decomposition (1,754@1e-13 + 592@1e-14), not the slipped phrasing; do not propagate the slip.

## Validation Architecture

> VER-07: every contract needs a numerically-defined acceptance check naming its pass criterion, the
> data it runs on, and the executing command/function. Per D-14, each packet **defines AND runs** its
> reserved AC via a disposable probe to reach `VERIFIED` before phase exit; Phase 29 rebuilds the full
> suite (VER-09). No new AC-IDs (D-13/D-14). No probe touches `pinn/` (SCOPE-10).

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Disposable Python probes (`.venv/bin/python`), pattern of Phase 24 `probes/dataNN_*.py` over `simulation_data/` read-only; plus spec-consistency text probes (grep/parse over `ctl_instruction.md`) |
| Config file | none — probes are standalone scripts under the phase dir (D-15); stdout NOT committed (git policy blocks `outputs/*`), register/packet rows ARE the committed evidence `[CITED: 24-VERIFIED-FACTS.md:100–104]` |
| Quick run command | `.venv/bin/python .planning/phases/26-*/probes/<probe>.py` |
| Full suite command | Phase 29 builds the runnable AC suite (VER-09) — out of Phase 26 scope |

### Phase Requirements → Test Map (candidate AC designs from resolution-doc part-5)
| Req | AC-ID | Behavior | Test type | Candidate command / function | Data it runs on |
|-----|-------|----------|-----------|------------------------------|-----------------|
| PIPE-01 | AC-PIPE-01 | admission gate clauses; `>=200` rejected; complete 59-snapshot std-base admits | dataset + spec-consistency | extend `data06_snapshots.py` (per-variant `final_timestep`/`n_snapshots`/`max Δt/dt_out` split by footer presence); unit fixtures per §3.1 part-5 | `simulation_data/Data/brutus_output/{4 variants}` |
| PIPE-02 | AC-PIPE-02 | `max(parsed IDs) >= file_count`; absent-key miss; no positional fallback | dataset property + spec-consistency | reuse `data01_id_gaps.py` (max ID vs count); scan-regex property over folders | `brutus_standard_quasi_random` (+ 3 others) |
| PIPE-03 | AC-PIPE-03 | blacklist load/exclude/log; fail-loud on absent/invalid; batch assertion | dataset + spec-consistency | reuse `data02_blacklist.py` (65 IDs `{hier:2,std:63}`); spec-text assertion that the contract names init-load + batch assertion | `Documentation/problematic_ics_blacklist.json` |
| PIPE-05 | AC-PIPE-05 | gold-missing set = set difference; Stage-5 stratum emits zero misses; **+ label-semantics ruling obtained** | dataset + governance | reuse `data03_gold_gap.py` (184 set diff vs `standard_quasi_random_ids_not_in_gold.md`); the framework-owner ruling is the gating input, not a probe | `brutus_standard_quasi_random{,_gold_standard}` |
| PIPE-06 | AC-PIPE-06 | presence counts reproduce 3,307/1,550 — 2,048/701 — 2,346/219 — 4,857/0; provenance assignment | dataset | reuse `data04_footers.py` (footer presence + tuple histogram); unit fixtures per §3.5 part-5 | `simulation_data/Data/brutus_output/{4 variants}` |
| PIPE-10 | AC-PIPE-10 | (after user choice) round-trip bitwise float64; schema attrs present; loader refuses JSON | spec-consistency (data round-trip is FUT-01) | spec-text check that Step-1-item-6 names the chosen format + round-trip acceptance clause | the user-locked format text in `ctl_instruction.md` |

### Sampling Rate
- **Per finding (D-14):** run that finding's disposable probe before its row moves to `VERIFIED`.
- **Per plan (batch, D-08):** re-run any previously `VERIFIED` finding's check whose section/`Dependents`
  the batch could regress.
- **Phase gate:** all ten in-scope rows at `VERIFIED` or `DEFERRED` before phase exit (M13 may be
  `DEFERRED` with a written `GAP-26-NN` blocker if the label-semantics ruling is not obtained).

### Wave 0 Gaps
- [ ] Five new evidence packets (B-06, B-11, M13, D7, D-03) copied from `_TEMPLATE.md`; filenames +
  `evidence/README.md` ID→filename map (D-05).
- [ ] M11 packet extension stub (PIPE-03 before/after note + transitions) inside the existing
  `m11-m12-severity.md` (D-06) — do NOT create a new M11 file.
- [ ] Disposable probe scripts (or inline-in-packet commands, D-15) reusing Phase 24
  `data01/02/03/04/06_*.py` patterns under the phase dir.
- [ ] `26-GAPS.md` is created by the PARENT on first gap (M13 is the pre-registered candidate); the
  subagent never writes it.
- Framework install: none — `.venv` + Phase 24 probe patterns already exist.

*Existing test infrastructure (Phase 24 probes + verified-facts register) covers the dataset side of
every AC; the spec-consistency side is new lightweight grep/parse probes.*

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `.venv` Python + NumPy | dataset probes (AC-PIPE-01/02/03/05/06) | ✓ (Phase 24 ran all probes 2026-06-11) | per `.venv` | — |
| `simulation_data/` dataset (read-only) | dataset probes | ✓ (SCOPE-06 grounding) | 15,028 files | — |
| `git` + `scripts/agent-commit` | atomic per-plan commits (D-10) | ✓ | — | — |
| h5py / NumPy `.npy` (for D-03 *evidence presentation only*) | D-03 user-gate evidence | not required to run | — | present candidate as text; round-trip is FUT-01, not Phase 26 |

**Missing dependencies with no fallback:** none — all dataset probes already executed in Phase 24;
Phase 26 re-runs them as disposable acceptance probes.
**Out-of-scope-by-design:** the live DataLoader (`pinn/`) — never probed (SCOPE-10).

## Project Constraints (from CLAUDE.md / AGENTS.md)

- **STOP protocol (v1.5 applicability).** Source-silent semantic / process-schema / cross-phase
  decisions are surfaced in `26-GAPS.md` (phase-local, parent creates on first gap) + `v1.5-GAPS.md`
  (milestone index), never invented. **Subagents return findings to the parent; only the parent writes
  gap registers.** M13 is the pre-registered candidate.
- **Grounding test.** A decision is grounded only if answered by the resolution doc, the issue doc, a
  prior user decision, a planning artifact, a v1.4/v1.5-revised framework-spec section, or short
  first-principles physics. **Live code in `pinn/` is NOT grounding.** `data_quality_assessment.md` is
  read-only citable evidence (SCOPE-09); `sampling_method.md` is frozen (SCOPE-08).
- **Edit perimeter.** `ctl_instruction.md` and `pinn_architecture.md` ONLY.
- **Git policy.** `scripts/agent-commit` with `GIT_AGENT_ID` + `GIT_AGENT_OWNED_PATHS`; no broad staging
  (`git add .`/`-A`/`-u`); commit scopes `26` / `26-NN`; body required for `.planning/` + spec commits;
  no push from `milestone/*`. Cross-phase writes are by design (ledger under Phase 24 dir; packets under
  Phase 25 `evidence/`) — do not "fix" by relocating.
- **ID-namespace caution.** v1.4/issue-01 also had a "B-06"; every citation must be directory-qualified
  so a v1.5 packet is never confused with its v1.4 namesake (26-CONTEXT §specifics).
- **Sequentialthinking MCP** for any multi-step task (project tooling directive).
- **Public-release mindfulness.** No secrets/personal paths in new artifacts.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Current spec line anchors (Step 1 = 340–382, §2.6 = 615–649, Step 5 = 1061–1068, Stage 5/6 = 229–249) are correct landing points | Edit Targets | LOW — re-confirm at edit time; formatting passes can shift lines; section/heading anchors are stable |
| A2 | `pinn_architecture.md` edits are likely unnecessary for the six findings (candidate texts are data-side) but PERMITTED where a candidate requires an architecture statement | Edit Targets | LOW — D-04 of 26-CONTEXT governs; planner confirms per-finding from each candidate text |

**Note:** This is a corpus-mapping task; nearly every claim is `[CITED: ...]` into the fixed in-repo
corpus. The two `[ASSUMED]`-class items above are line-anchor and edit-scope predictions, both
low-risk and explicitly re-confirmable at edit time. The genuinely open *decisions* (M13 label
semantics, M13 gold-rerun, D-03 format) are USER/framework-owner calls documented in "Source-Silence
and Cross-Source Findings", not assumptions this research makes.

## Open Questions

1. **M13 Step-5 label semantics (simulations vs IDs) — THE phase pivot.**
   - What we know: the resolution doc reaches a no-fallback-by-entailment direction at Medium confidence
     and preserves the defeater verbatim `[CITED: 02-resolution-doc.md:257–266]`.
   - What's unclear: whether labels attach to simulations (entailment holds → conditional note) or IDs
     (entailment fails → STOP-gap marker). The spec text "each simulation ID" is genuinely ambiguous.
   - Recommendation: per D-12, author the M13 packet from §3.4 + OI-7, then surface `GAP-26-NN` unless
     fully grounded and consistent with locked conventions; never invent the ruling. Isolate in a
     dedicated plan (D-09) so the autonomous chain does not block.
2. **D-03 format choice (PIPE-10).**
   - What we know: candidate is HDF5-canonical / `.npy` derived / JSON inspection-only.
   - What's unclear: any unstated operational constraint forbidding HDF5 — only the user can supply this.
   - Recommendation: dedicated `autonomous: false` user-gate plan (D-11); present candidate + verified
     evidence; record the user-locked choice in `ctl`, the packet, and the ledger in one commit.
3. **Whether to run the OI-6 no-footer probe extension as part of AC-PIPE-01.**
   - What we know: it is optional; the candidate contracts (B-06 clause 7 WARN; D7 all-or-nothing) are
     stated so as not to depend on it.
   - What's unclear: whether the planner wants to characterize the 2,470 no-footer files now or defer.
   - Recommendation: optional; if run, it doubles as the AC-PIPE-01 disposable probe and tightens the
     B-06/D7 caveats; if deferred, record OI-6 as a carried caveat (D-13) and keep clause 7 at WARN.

## State of the Art

Not applicable — this is an in-repo spec-adjudication phase against a fixed corpus, not a
technology-selection task. The only external libraries referenced are h5py and NumPy `.npy`/`.npz`
(for the D-03 format evidence), carried from the resolution doc's References
`[CITED: 02-resolution-doc.md:801–802]`; their selection is the user's call (D-11), not a research
recommendation.

## Sources

### Primary (HIGH confidence — fixed in-repo corpus, line-cited)
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` — §3 Cluster A (101–382), §6 cross-cutting (732–753), Open Items register (756–779), References (782–818). Candidate verdict source, NOT authoritative.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — Step 1 (340–382), Stage 5/6 stratification (229–260), §2.5/§2.6 (574–649), Step 5 (1061–1068), stratification table (26–27).
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — §3.1 batch (292–351), §5.2 input contract (749–763), §5.3.1 PHYS-02 (833).
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md` — CLM-01..13, DATA-05, DATA-02 consumption map.
- `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` — the ten in-scope rows + per-finding notes + lifecycle rules.
- `.planning/phases/25-evidence-framework-and-issue-ledger/evidence/README.md`, `_TEMPLATE.md`, `m11-m12-severity.md` — evidence machinery + M11/M12 locked verdicts.
- `.planning/phases/24.5-resolution-doc-readiness-verification/24.5-RESOLUTION-MAP.md` — Q-A1..A6 line map, 7-part structure, verdict-direction preview.
- `.planning/REQUIREMENTS.md` (PIPE-01/02/03/05/06/10, VER-07, SCOPE-06..11), `.planning/ROADMAP.md` (Phase 26, source-treatment + verification protocols), `.planning/phases/26-*/26-CONTEXT.md`.

### Secondary (MEDIUM confidence)
- None — every claim is line-cited into the primary corpus.

### Tertiary (LOW confidence)
- None.

## Metadata

**Confidence breakdown:**
- Candidate verdict mapping (6 findings): HIGH — directly transcribed from `02-resolution-doc.md` §3 parts 1/5/6 with line cites.
- Edit-target landing points: HIGH on section identity, MEDIUM on exact line numbers (re-confirm at edit time; A1).
- Ledger / machinery state: HIGH — current files read in full.
- M13 + D-03 openness: HIGH that they are open (the corpus itself flags them); the *resolutions* are deliberately not researched (user/framework-owner calls).

**Research date:** 2026-06-12
**Valid until:** stable while the resolution doc, specs, ledger, and Phase 25 evidence files are
unchanged. Re-verify line anchors if `02-resolution-doc.md` or the specs are re-delivered (§/Q-ID
anchors are stable across re-pagination). No external/fast-moving dependencies.
