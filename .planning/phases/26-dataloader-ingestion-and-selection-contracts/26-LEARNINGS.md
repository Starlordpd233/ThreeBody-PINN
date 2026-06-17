---
phase: 26
phase_name: "Dataloader Ingestion and Selection Contracts"
project: "3-body-problem"
generated: "2026-06-17"
counts:
  decisions: 10
  lessons: 6
  patterns: 6
  surprises: 3
missing_artifacts: []
---

# Phase 26 LEARNINGS — Dataloader Ingestion and Selection Contracts

## Decisions

### B-06 + B-11 adjudicated accept-resolution
Both Step-1-region DataLoader contracts (PIPE-01 admission gate, PIPE-02 ID resolution) were adjudicated `accept-resolution`; both candidate texts survived independent CLM verification unchanged from the resolution-doc §3.1/§3.2 source. The B-06 packet existed as an untracked draft from a prior interrupted run; it was validated against the Phase 25 evidence protocol and `_TEMPLATE.md`, premature probe-output line numbers were corrected to post-edit values, and the Before/After note was re-anchored.

**Rationale:** Transcribe resolved candidate text verbatim (D-01) and ground every clause in a verified CLM/DATA fact — no re-derivation, no invention.

**Source:** 26-01-SUMMARY.md (decisions, What Was Built)

---

### Step-1A snapshot minimums cite the locked M12 rule, not re-derived
The Step-1A admission gate states snapshot minimums by citing the locked M12 rule in `m11-m12-severity.md` (Phase 27 PIPE-04 forward reference), not by re-deriving them in the spec. The issue doc's `>= 200` floor is explicitly rejected on CLM-10 and appears only in rejection prose, never as a contract clause.

**Rationale:** Locked conventions (D-02) must be cited, not re-derived; the `>= 200` floor fails CLM-10 and is rejected at the spec level, not merely undocumented.

**Source:** 26-01-SUMMARY.md (What Was Built, AC-PIPE-01 spec-consistency grep)

---

### ID-resolution contract prohibits dense/positional/array-index addressing
The Step 1 item 7 contract hard-prohibits dense/positional/array-index addressing via anchored regex `^brutus_(hierarchical|standard)_(\d{4})\.txt$` + scan-built `id_to_path` + dual `physical_key`/`record_key` + explicit `ID ≠ array index` invariant. Grounded in CLM-01 non-density (max_id 3,998 vs 2,749 files makes dense indexing impossible).

**Rationale:** A contract must reflect the empirical structure of the on-disk dataset, not a textbook model; the CLM-01 fact settles the prohibition, not a stylistic preference.

**Source:** 26-01-SUMMARY.md (What Was Built, AC-PIPE-02 dataset fact)

---

### PIPE-03 blacklist contract co-located with Step-1A gate (D-03)
The 6-clause blacklist-exclusion contract lands as a `### Blacklist-exclusion contract (clause 1 detail; M11 / PIPE-03)` sub-section after the Step-1A clause list and before Step 2 — co-located with the gate that consumes it. 65-ID figure (2 hierarchical + 63 standard) cited as a DATA-02/CLM-03 dataset fact, never hard-coded as a contract constant.

**Rationale:** D-03 presentation discretion; the contract's natural reading site is the gate that invokes it. Numbers that can drift (rerun supersession, OI-9) must be cited, not baked in.

**Source:** 26-02-SUMMARY.md (decisions, What Was Built)

---

### M11 packet EXTENDED, not duplicated; M12 sub-part byte-stable
The PIPE-03 work added an M11-specific PIPE-03 Before/After Spec Note to the existing M11 packet, recording the real spec landing. The M12 sub-part of the same packet is byte-stable. M11 → VERIFIED with packet link + transition log; G3 → VERIFIED (close-with-parent, D-07, no separate packet).

**Rationale:** D-06 forbids duplication when an existing packet already covers the finding; D-07 lets G-rows close with the issue row they synthesize.

**Source:** 26-02-SUMMARY.md (decisions, m11-m12-severity.md extension)

---

### D7 footer contract: all-or-nothing with folder-default fallback + per-field provenance
The PIPE-06 footer contract in Step 1 item 3 is: footer OPTIONAL + metadata-only; present → full schema with `param_provenance=direct`; absent → folder defaults with `param_provenance=inferred`; partial-schema → `footer_anomalous=true` + default fallback; `eta` null/absent (no fabrication); independent `dt_out` median-spacing measurement (`measured`) with >1% warn; footers NEVER a completeness signal (defer to Step-1A clause 4) or mapping source (defer to Step 1 item 7). §2.6 carries the `param_provenance` map over `{brutus_tolerance, word_length, dt_out, eta}` ∈ `{direct, inferred, absent, measured}`; `trustworthy_horizon` RESERVED (OI-4; writers null, readers forbidden).

**Rationale:** A contract must cover every observed footer state (present, absent, partial, anomalous) without leaking the footer into a step that owns a different concern (completeness, ID resolution).

**Source:** 26-03-SUMMARY.md (What was done, §2.6 amendment)

---

### OI-9 hier-base supersession propagated; resolution-doc 3,307/1,550 targets flagged stale
The 70-file DATA-05 rerun shifted hier-base no-footer from 1,550 → 1,480; this is documented in `24-DATA05-RERUN-REMEDIATION.md:130-134`, which flags the resolution-doc part-5 target figures as pre-rerun stale. The PIPE-06 contract uses the post-rerun numbers and treats the stale figures as a known supersession (OI caveat propagation, D-13), not a gap.

**Rationale:** Dataset reruns supersede prior numeric targets (OI-9); the resolution-doc is a historical record whose numbers can be stale and must be flagged, not silently corrected.

**Source:** 26-03-SUMMARY.md (Deviations from Plan, AC-PIPE-06 dataset half)

---

### M13 mandatory data-side contract lands regardless of path; conditional fallback NOT landed
The 4-clause mandatory data-side gold-counterpart contract (set-difference gold-missing set cross-checked vs the 184-ID list, per-`physical_key` `gold_counterpart`, gold-folder-iterated Stage-5 stratum, no silent base→gold substitution) lands in `ctl_instruction.md` Step 5 unconditionally. The conditional fallback text (resolution-doc:274-290) is deliberately NOT landed because its precondition (a settled label-semantics ruling) is unmet. The mandatory contract and the fallback policy are orthogonal — one can be locked while the other is a STOP gap.

**Rationale:** Data-side correctness does not depend on a semantic ruling; landing the contract preserves the data integrity invariant while the ruling remains an open question.

**Source:** 26-04-SUMMARY.md (decisions, What was done)

---

### GAP-26-01 RESOLVED-WITH-INSTRUCTION Option B (per-ID Stage-5 labels; 184-ID re-simulation activated)
The pre-registered STOP gap (OI-7a label-semantics: do Stage-5 labels attach to *simulations*/`record_key` or to *IDs*?) was resolved by the framework owner on 2026-06-13 = **Option B: Stage-5 curriculum stage labels attach to IDs** — every Stage-4-admitted ID owes a Stage-5 gold sample. Owner directed: re-simulate the 184 missing gold counterparts to restore 1:1 base:gold correspondence (OI-7b ACTIVATED, not yet executed). M13 packet Verdict `defer-with-blocker` → `accept-third-position`; ledger M13 + G4 → VERIFIED with full user-decision provenance. Per-ID stage-label clarification added on the Step-5 hinge; no `pinn_architecture.md` edit.

**Rationale:** A resolved user ruling is transcribed verbatim into spec + packet + ledger (D-08, T-26-20); the data-generation remediation is a forward dependency, not a loader fallback.

**Source:** 26-04-SUMMARY.md (Resolution 2026-06-13, GAP-26-01 = Option B)

---

### D-03 HDF5 canonical user-locked at PIPE-10 mandatory gate; never auto-selected
D-11 forbids any execution mode (including `--auto`/yolo) from choosing the training-data format. The PIPE-10 gate presented HDF5 vs `.npy`/`.npz` vs txt/json with verified evidence and the §3.6 Q-A6 candidate as a recommendation, halted at `checkpoint:decision`, and the user supplied `hdf5-canonical` on 2026-06-13. The contract was transcribed into `ctl_instruction.md` Step 1 item 6 alone (D-03 names ctl, no `pinn_architecture.md` edit) with user-decision provenance in both the spec ("user-locked 2026-06-13") and the D-03 packet Verdict. A bitwise-float64 round-trip acceptance clause is the spec-side contract; the data round-trip implementation (parse raw → write → read → `np.array_equal`) is FUT-01.

**Rationale:** D-11 is a hard gate; user-decision provenance must be recorded in both spec and packet (T-26-20) to prevent later confusion about whether the format was auto-selected.

**Source:** 26-05-SUMMARY.md (decisions, The user decision, D-04 perimeter)

---

## Lessons

### Source-conflicting semantic decisions surface as STOP gaps; subagents return draft fields to parent
When the resolution doc and issue doc conflict at the hinge (M13: per-ID vs per-simulation Stage-5 obligation), the D-12(b) decision rule + ROADMAP Phase 26 success criterion 4 require a STOP gap, not invention. Per project governance, **subagents return findings; only the parent writes gap registers**. The M13 plan-26-04 executor authored the full GAP-26-NN field set in the SUMMARY's "Resolution" section but did NOT create or edit `26-GAPS.md` / `.planning/milestones/v1.5-GAPS.md` — those are parent-owned (threat T-26-16). The 3-question understanding check (STOP step 2: math/engineering, downstream consequences, source silence) must be documented in the packet before recording any gap.

**Context:** Use this rule whenever a verdict is `defer-with-blocker` or a candidate is source-conflicting; treat the gap field set as a finding, not a subagent-owned artifact.

**Source:** 26-04-SUMMARY.md (Governance posture CRITICAL, STOP step 2, Deviations from Plan)

---

### Mandatory contracts can land independently of unresolved fallback policy
The M13 mandatory data-side gold-counterpart contract (4 clauses) and the M13 fallback policy are orthogonal axes. The data-side contract was landed and verified (AC-PIPE-05 184/184 PASS) even while the fallback policy was an unresolved STOP gap. This means a phase can advance a finding to IN_PROGRESS-with-note (not DEFERRED) when the data-side work is verified but a semantic ruling is pending — G4 inherits the pending disposition via close-with-parent.

**Context:** Apply when an issue mixes a decidable data-side clause with a source-conflicting semantic clause; advance the data-side work, defer only the semantic ruling.

**Source:** 26-04-SUMMARY.md (decisions, What was done, ledger transitions)

---

### Acceptance-check regression chain (D-08) catches anchor shifts
After every spec edit, the previously-VERIFIED acceptance checks (AC-PIPE-01/02/06 in Phase 26) must be re-run as regression probes. In 26-05, the Step 1 item 6 expansion shifted downstream line numbers but disturbed no neighboring Step-1 contract content; the re-grep confirmed the B-06 gate clauses (`:452/471/477`), the B-11 `id_to_path`/regex/invariant (`:429-441`), and the D7 footer-metadata-only contract (`:359/392, :814`) all stayed intact. AC-PIPE-01/02/06 regression re-checks PASS, no regression.

**Context:** Apply after every `ctl_instruction.md` edit in a multi-wave phase; the chain-regression is cheap (spec-consistency grep) and catches accidental clause deletion or content drift.

**Source:** 26-05-SUMMARY.md (D-08 chain-regression re-checks)

---

### Line-anchor drift across multi-wave edits requires A1 re-confirmation
The 26-04 plan cited `ctl_instruction.md:1068` for the Step-5 "each simulation ID" hinge, but Waves 1-3 (Step-1A gate, B-11 item 7, D7 §2.6) shifted the content; the hinge is now at line 1227 and the B-11 `record_key` annotation at 1228. The plan's Task-3 `read_first` (A1 directive) required re-confirming the anchor at edit time — the edit landed at the correct current location. Similarly, the 26-05 plan cited item 6 at lines 374-378; the live anchor was 406-410 (Plan 26-01 inserted Step 1 item 7 between Task-1 authoring and the edit).

**Context:** In any multi-plan phase where earlier plans edit a shared spec, treat all plan-cited line anchors as stale-by-default; re-grep / re-read at edit time.

**Source:** 26-04-SUMMARY.md (Line-anchor deviation), 26-05-SUMMARY.md (A1 anchor correction)

---

### OI-9 dataset rerun supersedes prior numeric targets — propagate, do not silently correct
The DATA-05 70-ID rerun shifted hier-base no-footer from 1,550 → 1,480 and std-base / std-gold counts. The 24-DATA05-RERUN-REMEDIATION.md explicitly documents the supersession and flags the 1,550/3,307 resolution-doc figures as stale. The PIPE-06 contract uses post-rerun numbers and treats the stale figures as a known OI caveat, not a source-silent gap. Same pattern in 26-04 with OI-12: the 2,346 std-gold with-footer decomposes as 1,754@1e-13 + 592@1e-14, not homogeneous.

**Context:** When a dataset rerun changes counts, the spec must use post-rerun numbers and flag the prior figures as stale in the resolution-doc OI notes; never silently edit the resolution doc.

**Source:** 26-03-SUMMARY.md (Deviations from Plan), 26-01-SUMMARY.md (OI-9 propagation)

---

### SHA backfill follow-up is the one unavoidable exception to same-commit
A spec+packet+ledger commit cannot reference its own SHA inline (the SHA does not exist until the commit lands). Phase 25 set the precedent: the substantive commit lands without the SHA, and a single mechanical follow-up commit backfills `<PLAN-26-01-SHA>` placeholder tokens in the packets' Status Transition Logs and the ledger per-finding subsections. D-08 same-commit discipline holds for the work itself; the SHA backfill is the pre-approved exception.

**Context:** Whenever a commit asserts a verifiable invariant (commit SHA, dataset count, byte-for-byte preservation) inline, plan for the SHA backfill as a separate mechanical commit.

**Source:** 26-01-SUMMARY.md (Notes), 26-05-SUMMARY.md (Commits exist)

---

## Patterns

### Packet-before-edit (Phase 25 evidence protocol)
Author a 12-section evidence packet (Verdict, Locked Convention, Which-Source-Correct, Before/After, Named-Acceptance-Check, §3b dataset evidence, Status Transition Log, etc.) before any spec change. The packet's `accept-resolution` verdict is the gate that authorizes the spec edit; `defer-with-blocker` halts for user decision; `deferred` is reserved for cases the user has explicitly deferred. Every Phase 26 plan followed this: B-06 + B-11 in 26-01, M11 (EXTENDED) in 26-02, D7 in 26-03, M13 in 26-04, D-03 in 26-05.

**When to use:** Every framework-spec edit in an adjudication milestone; the packet is the audit trail and the spec edit is downstream of the verdict.

**Source:** 26-01/26-02/26-03/26-04/26-05-SUMMARY.md (key_files created, evidence packets)

---

### Same-commit ledger edits (D-08)
Spec + packet + README + ledger move together in a single atomic commit. Phase 26 used `scripts/agent-commit` (scope `26-NN`, type `spec`, body required) for every substantive commit. The `24-ISSUE-LEDGER.md` row PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED transition log is written in the same commit as the spec edit; README ID→filename map row is added in the same commit as the packet; provenance is unbroken.

**When to use:** Every phase that modifies a framework spec; never split spec/packet/ledger across commits.

**Source:** 26-01/26-02/26-03/26-04/26-05-SUMMARY.md (D-08 same-commit discipline)

---

### Close-with-parent (D-07)
G-rows (synthesis findings like G1, G2, G3, G4) close with the issue row they synthesize, with no separate evidence packet. G1 closes with B-06; G2 with B-11; G3 with M11; G4 with M13 (initially DEFERRED → VERIFIED close-with-parent after the 184-ID re-simulation directive). The G-row ledger entry inherits the parent row's disposition (VERIFIED, or IN_PROGRESS-with-note when the parent is in that state).

**When to use:** Whenever a synthesis finding does not warrant its own packet; the G-row is a status-only record that mirrors the parent.

**Source:** 26-01-SUMMARY.md (G1/G2 close-with-parent), 26-02 (G3), 26-04 (G4 inherits M13 pending disposition)

---

### Directory-qualified citations (file:line on every CLM/DATA/OI cite)
Every CLM, DATA, OI, and resolution-doc cite carries a file:line anchor. Examples: `02-resolution-doc.md:223-251` (M11 clauses), `:255-293` (M13 Q-A4), `:362-377` (D-03 HDF5), `:1068` / `:1227` (Step-5 hinge, drift example), `24-DATA05-RERUN-REMEDIATION.md:130-134` (OI-9 supersession), `m11-m12-severity.md` (M12 locked rule). The OI-7a ruling is cited as `OI-7:768` and `OI-7b` as a forward dependency.

**When to use:** Every packet, every ledger row, every SUMMARY; reviewers must be able to verify each claim in one click.

**Source:** 26-01/26-02/26-03/26-04/26-05-SUMMARY.md (citations throughout)

---

### User-decision provenance in both spec and packet (T-26-20)
When a PIPE gate (D-11) requires user input, the user's selection is recorded in two places: (a) the spec gets an in-spec attribution line ("user-locked 2026-06-13" for D-03 in `ctl_instruction.md` Step 1 item 6), and (b) the evidence packet's Verdict / Before-After sections get an explicit user-decision provenance line. M13 GAP-26-01 Option B was recorded the same way (per-ID stage-label clarification in spec + "GAP-26-01 RESOLVED 2026-06-13 = Option B" in ledger and packet).

**When to use:** Every PIPE-mandated user gate; the duplication is intentional to prevent later confusion about whether a choice was user-locked or auto-selected.

**Source:** 26-05-SUMMARY.md (D-03 user-locked), 26-04-SUMMARY.md (GAP-26-01 Option B)

---

### Spec-consistency grep as a cheap AC
Acceptance checks for spec edits are spec-consistency `grep` probes, not runtime tests. AC-PIPE-01 greps for `## Step 1A` + `final_timestep >= 9.5` + `SCS > -5` + absence of `>= 200` floor. AC-PIPE-02 greps for `id_to_path` + `record_key` + `physical_key` + `array index` prohibition. AC-PIPE-06 greps for `footer` + `metadata-only` + `param_provenance`. AC-PIPE-10 greps for `HDF5` + a round-trip clause. The dataset-half of AC-PIPE-06 (`data04_footers.py`) and the AC-PIPE-05 set-difference probe (`data03_gold_gap.py`) are one-shot captures from the data-probes directory, not re-runs on every edit.

**When to use:** Every AC for a framework-spec edit in this project; the grep is the regression check, the dataset probe is the one-shot evidence capture.

**Source:** 26-01-SUMMARY.md (AC-PIPE-01/02), 26-03 (AC-PIPE-06), 26-05 (AC-PIPE-10)

---

## Surprises

### OI-12: std-gold with-footer decomposes as 1,754@1e-13 + 592@1e-14, not 2,346 homogeneous
The issue doc's claim of 2,346 with-footer for std-gold is correct in count but hides a non-trivial tolerance decomposition: 1,754 files at tolerance 1e-13 plus 592 files at tolerance 1e-14. The PIPE-06 contract and AC-PIPE-06 probe must record this decomposition explicitly; a "2,346 homogeneous" framing would have been an invention. The slip (OI-12) was excluded by the corrected decomposition, not by re-deriving the 2,346 number.

**Impact:** A spec that summarizes a heterogeneous distribution as a single number silently loses the structure the data-pipeline depends on; explicit decomposition is the contract.

**Source:** 26-03-SUMMARY.md (decisions OI-12 slip excluded, corrected decomposition)

---

### B-11's `record_key` annotation settled key TYPE, not obligation granularity
A natural-but-wrong reading of the B-11 edit at `ctl_instruction.md:1228` is that the `record_key` annotation disposes of the M13 OI-7a label-semantics defeater. It does not: B-11 adjudicated **key TYPE** (content key vs positional index), and OI-7a is the **obligation-granularity axis** (per-simulation vs per-ID). These are distinct axes; treating B-11 as also disposing of OI-7a is invention by side-effect (threat T-26-14). The M13 plan-26-04 packet documents this distinction explicitly in the STOP step 2 understanding check.

**Impact:** Cross-edit inference across distinct semantic axes is a frequent failure mode; every cross-axis read must be justified by an explicit two-axis analysis in the packet.

**Source:** 26-04-SUMMARY.md (Three-question understanding check, Tempted to / Rejected)

---

### The 184 gold-less IDs are a data-generation remediation, not a loader fallback
The M13 fallback policy could plausibly have been "silently substitute base for missing gold" or "skip gold-less IDs at runtime." Neither is the correct resolution. The framework owner's ruling (Option B) treats the 184 gold-less IDs as a **data-generation remediation backlog** (OI-7b ACTIVATED) — the 184 gold counterparts must be re-simulated to restore 1:1 base:gold correspondence. The mandatory data-side contract (set-difference cross-check, `gold_counterpart=absent` per affected ID, no base→gold substitution) stays in force; each affected ID carries `gold_counterpart=absent` and contributes no gold Stage-5 sample until re-simulation. A "loader fallback" framing would have been invention; the remediation is a forward dependency for Phase 27 Q-C2 SASD resample queue.

**Impact:** A semantic decision can reframe a problem from "loader behavior" to "data generation," with downstream phase-scope consequences; surfacing the framing choice in the gap is essential.

**Source:** 26-04-SUMMARY.md (Resolution 2026-06-13, OI-7b ACTIVATED, forward dependency)
