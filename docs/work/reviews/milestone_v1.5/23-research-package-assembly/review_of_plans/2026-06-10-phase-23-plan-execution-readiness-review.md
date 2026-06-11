---
status: consumed
purpose: other
created: 2026-06-10
milestone: v1.5
phase: 23-research-package-assembly
retirement_trigger: v1.5 milestone work; active until superseded
---

# Phase 23 Plan Execution Readiness Review

**Date:** 2026-06-10
**Scope:** `.planning/phases/23-research-package-assembly/23-01-PLAN.md` through `23-05-PLAN.md`
**Review mode:** Compound Engineering document review, using coherence, feasibility, scope-guardian, and adversarial lenses.
**Verdict:** Not ready for flawless autonomous execution until the P0 blockers are resolved and the P1 verification gaps are tightened.

## Executive Summary

The Phase 23 plan set is directionally strong: the five-plan sequence is coherent, the D-07 user gate is explicit, DQA is treated read-only, snapshots are intended to remain byte-identical, `pinn/` is excluded, and the framed-questions plan correctly highlights STOP-protocol risk.

The remaining risk is not lack of intent. It is that several critical properties are stated in prose but not made deterministic enough for a literal autonomous executor. Two issues are blocking: the plan offers a valid-looking `exclude-dqa` path that can make the package invalid, and final delivery can open the external gate without checking for unresolved STOP gaps. Several P1 issues would let an executor pass checks while omitting required questions, corrupting package provenance, or producing a Phase 24 checklist that is incomplete or divergent.

## P0 Blockers

### P0-1: `exclude-dqa` Can Produce An Invalid Package

**Evidence:** Plan 02 presents `exclude-dqa` as a normal approval option (`23-02-PLAN.md:76`). But the research notes say DQA is the only written home of the SCS gate and metric definitions relevant to the package (`23-RESEARCH.md:166`, `23-RESEARCH.md:168`), and Plan 04 requires the framed-questions document to cite DQA for the SCS hard constraint (`23-04-PLAN.md:71`).

**Why this matters:** A user can choose an offered option and leave the external package without the only source that supports one of its hard constraints. The downstream executor then must either break self-containment, invent a replacement citation, or weaken the research brief.

**Fix:** Do one of the following:

- Make DQA mandatory in the package.
- Reclassify `exclude-dqa` as an explicit user override that halts normal execution and triggers a STOP/replan path.
- If exclusion must remain possible, require a user-approved replacement package artifact that preserves the SCS gate and metric-definition context without pretending it is a byte-for-byte DQA snapshot.

### P0-2: Final Delivery Can Open The Gate With Unresolved STOP Gaps

**Evidence:** The STOP protocol requires affected work to remain halted until the user resolves or defers the gap (`AGENTS.md:54`, `AGENTS.md:78`, `AGENTS.md:88`). Plan 05 opens the external gate and records state without checking whether `23-GAPS.md` or `.planning/milestones/v1.5-GAPS.md` exists with `OPEN` entries (`23-05-PLAN.md:100`, `23-05-PLAN.md:106`).

**Why this matters:** The package could be marked delivered while an unresolved source-silent decision remains open. That would poison Phases 24-29 by making downstream work believe Phase 23 produced a clean handoff.

**Fix:** Add a Plan 05 pre-delivery gate:

```sh
test ! -f .planning/phases/23-research-package-assembly/23-GAPS.md || ! grep -q '^**Status** -- OPEN\|Status.*OPEN' .planning/phases/23-research-package-assembly/23-GAPS.md
test ! -f .planning/milestones/v1.5-GAPS.md || ! grep -q 'OPEN' .planning/milestones/v1.5-GAPS.md
```

The exact command can be refined, but the requirement should be explicit: if any Phase 23 gap is `OPEN`, do not create the delivery note, do not mutate `STATE.md`, and do not open the external gate.

## P1 High-Priority Findings

### P1-1: Plan 04 Can Pass While Omitting In-Scope Findings

**Evidence:** The issue inventory includes D-03 format, B-06, B-11, M11, M12, M13, D7, severity reclassification, G1-G5, threshold clarifications, SCS, SASD, IPR, PSC, footer/mass-drift protocol, precision handling, global-scale `D = 6.694`, Recommended Resolutions, Dataset Inventory, and DataLoader Requirements (`23-RESEARCH.md:90`-`23-RESEARCH.md:109`). Plan 04's acceptance check only counts a smaller token set and accepts `>= 10` matches (`23-04-PLAN.md:100`, `23-04-PLAN.md:104`).

**Impact:** A literal executor can mention ten tokens and still omit research questions needed by Phases 25-28.

**Fix:** Add a required coverage table in `framed-research-questions.md` with one row per `23-RESEARCH.md` inventory item:

`Inventory item | Disposition | Question block / deferred reference / excluded rationale | CLM IDs | Downstream phase`

Plan 04 should fail unless every inventory row is accounted for.

### P1-2: The D-07 Approval Record Is Too Freeform For Downstream Snapshotting

**Evidence:** Plan 02 appends a freeform `APPROVED` section (`23-02-PLAN.md:88`), while Plan 03 treats that section as the authoritative snapshot list (`23-03-PLAN.md:62`). The current verification only checks for `APPROVED` and the two inclusion verdicts (`23-02-PLAN.md:96`-`23-02-PLAN.md:99`).

**Impact:** Plan 03 and Plan 05 can parse the approved file set differently, especially if the user modifies the list or consolidation boundary.

**Fix:** Require a fixed approval table:

`Include | Package basename | Canonical source path | Treatment | User decision | Grounding note`

For modified approvals, require an "approval grounding" subsection mapping each added/excluded item to D-04/PKG-01 and stating whether STOP was considered.

### P1-3: Snapshot Verification Is Narrower Than The Byte-For-Byte Requirement

**Evidence:** Plan 03's automated check diffs only `ctl_instruction.md` and `pinn_architecture.md` (`23-03-PLAN.md:79`), while its acceptance criteria require byte identity for the issue doc and any approved `sampling_method.md` / `data_quality_assessment.md` snapshots too (`23-03-PLAN.md:82`-`23-03-PLAN.md:84`).

**Impact:** The issue doc, DQA, or sampling snapshot can be corrupted while the automated checkpoint still passes.

**Fix:** After the D-07 approval table exists, loop over every included snapshot and run both `diff -q` and `git hash-object` equality against its canonical source.

### P1-4: Source Provenance Can Mismatch Snapshot Bytes

**Evidence:** Plan 03 permits `cp` from the working tree (`23-03-PLAN.md:75`) but records provenance using `git log -1 --format=%H -- <path>` (`23-03-PLAN.md:76`).

**Impact:** If any source file has uncommitted changes, the snapshot bytes can differ from the recorded commit hash.

**Fix:** Either copy consistently from `HEAD` using `git show HEAD:<path> > <dest>`, or preflight `git diff --quiet -- <all canonical source paths>` before any snapshot copy.

### P1-5: CLM Coverage Is Under-Specified For Extra Figures Introduced By Package Fragments

**Evidence:** D-11 requires every dataset figure stated anywhere in the package to get a CLM row (`23-CONTEXT.md:43`). Plan 01 only mandates the minimum D-12 set (`23-01-PLAN.md:112`), while Plan 03 pulls in numeric-rich fragments from README, blacklist JSON, and metrics/provenance code (`23-03-PLAN.md:120`).

**Impact:** Extra figures can appear in `consolidated-context.md` without stable CLM IDs, making Phase 24's verification checklist incomplete.

**Fix:** Add an append-only CLM policy: existing IDs never renumber; any additional package-stated dataset figure gets the next CLM ID, or the figure is omitted/quoted only as non-claim context.

### P1-6: Packaged `claims-table.md` Is Not Verified Content-Identical

**Evidence:** Plan 03 says the package copy must keep the CLM register table content-identical (`23-03-PLAN.md:98`), but checks only row count, status strings, and header text (`23-03-PLAN.md:104`-`23-03-PLAN.md:106`).

**Impact:** Values, citations, IDs, or statuses can drift between the canonical phase-local register and the package table.

**Fix:** Extract the markdown table body from both files and `diff` them, allowing only the package-specific explanatory header to differ.

### P1-7: Consolidated Context May Drop Relevant SCOPE-07 Evidence Families

**Evidence:** SCOPE-07 includes `metrics_calculation/`, `Validation/prescreening/`, and `brutus_runners/` as grounding (`.planning/REQUIREMENTS.md:93`). Context says the consolidated file may need prescreening thresholds and runner parameter blocks (`23-CONTEXT.md:33`). Plan 03 includes only `calculate_metrics.py` from scripts (`23-03-PLAN.md:116`, `23-03-PLAN.md:120`).

**Impact:** External researchers may lack provenance needed for B-06, D7, prescreening, runner-parameter, or validation-gate adjudication.

**Fix:** Require a per-finding SCOPE-07 inclusion matrix: include the relevant prescreening/runner excerpts, or document why README coverage is sufficient for each affected finding.

### P1-8: Negative `grep -c` Checks Can Fail On Success

**Evidence:** Several checks expect no matches using `grep -c`, including `research_package/specs/` no `data-processing-pipeline` (`23-03-PLAN.md:85`), no `data-processing-pipeline` in consolidated context (`23-03-PLAN.md:129`), and no escaping links in README (`23-05-PLAN.md:86`). `grep -c` prints `0` but exits `1` on no match.

**Impact:** Under `set -e` or command chaining, a correct package can fail verification.

**Fix:** Use `! grep -qE 'pattern' file`, or wrap count checks with `grep -cE 'pattern' file || true` before numeric comparison.

### P1-9: Blacklist Count Is Treated As Verified Before Phase 24

**Evidence:** Context says `problematic_ics_blacklist.json`'s 65-ID count is a claim until DATA-02 (`23-CONTEXT.md:82`), and DATA-02 owns blacklist verification (`.planning/REQUIREMENTS.md:30`). Plan 01 marks blacklist size 65 as `verified` (`23-01-PLAN.md:113`) and Plan 03 derives a composition summary with JSON (`23-03-PLAN.md:120`).

**Impact:** Phase 23 partially duplicates Phase 24 and may ship a Phase-24 empirical claim as already verified.

**Fix:** Mark blacklist count/composition `claimed-unverified` unless the project explicitly treats deterministic JSON reading inside Phase 23 as allowed verification. If retained, state clearly that the JSON excerpt is provenance/source material and DATA-02 still owns the verification verdict.

## P2 Execution-Quality Improvements

### P2-1: Required Pre-Phase Tag Is Not Operationalized

**Evidence:** The roadmap requires `v1.5-pre-phase-NN` before each phase (`.planning/ROADMAP.md:38`), and STATE specifically says to tag `v1.5-pre-phase-23` before Phase 23 begins (`.planning/STATE.md:144`, `.planning/STATE.md:163`). The plans only repeat branch checks.

**Fix:** Add a Plan 01 preflight: verify/create `v1.5-pre-phase-23`; if it exists at a different commit, stop and ask.

### P2-2: Manifest Sequencing And Generated-File Provenance Are Ambiguous

**Evidence:** Plan 05 creates `README.md` first (`23-05-PLAN.md:64`) but requires the manifest to cover `DELIVERY-NOTE.md` (`23-05-PLAN.md:74`), which is created later (`23-05-PLAN.md:92`). Plan 03 records hashes only for snapshots (`23-03-PLAN.md:76`), while the manifest covers every package file.

**Fix:** Either create `DELIVERY-NOTE.md` before the manifest, or add a final README update step. Define manifest rows for generated package files explicitly, for example: canonical source path `generated in Phase 23 Plan 04/05`, source commit hash `package commit`, treatment `generated package artifact`.

### P2-3: STATE Handler Commands Need Exact Syntax And Verification

**Evidence:** Plan 05 names `gsd-tools state add-decision`, `add-blocker`, and `record-session` in prose (`23-05-PLAN.md:101`), and allows `gsd-tools state json` or `get` for verification (`23-05-PLAN.md:110`). Local probing showed `add-decision` requires a `summary` argument and `add-blocker` requires `text`.

**Fix:** Include exact command syntax and require verification against `gsd-tools state get` or direct `.planning/STATE.md` grep for the decision and blocker text.

### P2-4: `Return Format` Needs A Non-Schema Boundary

**Evidence:** Plan 04 asks for a `Return Format` section (`23-04-PLAN.md:97`), while context/research reject prescribing the user's resolution-doc schema (`23-CONTEXT.md:52`, `23-RESEARCH.md:55`).

**Fix:** Constrain Return Format to expectations only: answer each question, cite sources, identify conflicts/uncertainty, and avoid required headings, verdict labels, tables, or file structure.

### P2-5: Summary Outputs Are Omitted From `files_modified`

**Evidence:** Each plan asks for a `23-0N-SUMMARY.md` output, for example Plan 01 (`23-01-PLAN.md:200`), Plan 03 (`23-03-PLAN.md:173`), and Plan 05 (`23-05-PLAN.md:153`), but the frontmatter file lists omit these summary files.

**Fix:** Add each summary to `files_modified`, or state that summaries are workflow-side artifacts outside the plan commit.

## Robust Elements Worth Keeping

- The plan chain `23-01 -> 23-02 user gate -> 23-03 -> 23-04 -> 23-05` is coherent.
- The D-07 gate is clearly modeled as non-autonomous and blocks package creation before approval.
- DQA read-only handling has a direct `git diff --quiet` guard.
- The "annotations in manifest, never inside snapshots" rule is strong and prevents byte-identity drift.
- Plan 04 correctly names the highest STOP-protocol risk and repeatedly says to pose questions rather than answer them.
- The package path, `pinn/` exclusion, Phase 24 parallelism, and Phase 25-29 gate semantics are consistent across the plan set.

## Recommended Remediation Order

1. Resolve P0-1 and P0-2 before any autonomous execution.
2. Make Plan 02's approval record machine-readable, then make Plan 03 consume that table for snapshots, diffs, hashes, and manifest provenance.
3. Add the Plan 04 inventory coverage table so every issue-02 finding has an explicit disposition.
4. Tighten CLM handling: append-only IDs for extra figures and table-body diff for package copy.
5. Fix fragile shell checks (`grep -c` absence checks, all-snapshot byte checks, dirty-source preflight).
6. Clarify generated-file manifest rows, STATE command syntax, and summary-file staging.

