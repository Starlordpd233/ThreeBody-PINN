---
phase: 24
phase_name: "Empirical Dataset Verification and Correction Addendum"
project: "3-body-problem"
generated: "2026-06-17"
counts:
  decisions: 9
  lessons: 7
  patterns: 6
  surprises: 5
missing_artifacts: []
---

# Phase 24 Learnings: Empirical Dataset Verification and Correction Addendum

## Decisions

### D-13 Nominal-Range Convention Grounded in README, Not Re-Derived
The ID-gap probe computes gaps[0..max] against the observed max ID (e.g., 3,998 for standard, 4,999 for hierarchical), not against the nominal-range end (e.g., 3,999 / 4,999). The conditional D-13 STOP-gap branch did NOT fire because README.md:146-153 declares ID ranges 0000-3998 / 0000-4999 with gaps 1,250 / 143.

**Rationale:** The README's stated ranges provide the authoritative nominal end. Adopting the observed max as the nominal end (with a 1,251 non-canonical artifact also emitted) avoids a source-silent decision and keeps the gap count reproducible.
**Source:** 24-01-SUMMARY.md, 24-VERIFIED-FACTS.md, CLM-01/02/12

---

### DATA-02 Consumption Recorded as a Nuanced Map, Not a Flat Yes/No
The blacklist json is loaded by `dataset_readiness_checks`; current Brutus runners do NOT load the json (they use `Documentation/problematic_ics/{type}/`); the README:1005 calls the json "legacy"; the M11 training-time aspect is `unverified` per SCOPE-10/D-10.

**Rationale:** A flat yes/no on blacklist consumption would mislead the downstream agent about which code paths actually load the json and which rely on directory-based exclusion. The nuanced map preserves the operational reality.
**Source:** 24-01-SUMMARY.md, 24-VERIFIED-FACTS.md (DATA-02 row)

---

### CLM-05 Split Into CLM-05a / CLM-05b Per WR-04 User Decision
CLM-05 was originally a single row (IC folder count = 2,749; Brutus output folder count = 2,749). The user split it into CLM-05a (IC folder counts) and CLM-05b (Brutus output folder/file counts) as separate rows, with CLM-05 preserved as historical parent/alias. No renumber.

**Rationale:** IC folders and Brutus output folders are distinct observables that happen to share a count today. Splitting them protects against future divergence and makes the observation traceable to its probe.
**Source:** 24-04-SUMMARY.md, 24-WR-DECISIONS.md, 24-VERIFIED-FACTS.md

---

### DATA-05 70-ID Gap Surfaced as Semantic STOP, Not Silently Resolved
The 70 base-hier mass-drift files (abs diff 0.1-1.0) were surfaced as GAP-24-01 (semantic STOP) rather than silently picking a baseline. The provenance was source-silent: perturbation does not touch masses (`ic_generation_utils.py:417-420`), and the gold variant matches the same IDs perfectly.

**Rationale:** A drift of 0.1-1.0 mass units cannot be a round-trip or perturbation artifact. Silently choosing a baseline would have violated D-16 (semantic STOP for source-silent cases). The STOP protocol held.
**Source:** 24-02-SUMMARY.md, 24-GAPS.md (GAP-24-01), 25-GAPS.md (cross-reference)

---

### CLM-10 Corrected at Integer-Rounded MEDIAN, Not Mode or Pilot
CLM-10 was originally "~59 / ~125 / ~1000" for standard / hier / gold snapshot counts. The empirical integer-rounded medians (61 / 127 / 1003) corrected CLM-10. The `~` prefix is preserved; the medians are the authoritative fact.

**Rationale:** D-09 lock 2026-06-11 made the integer-rounded median the authoritative value for snapshot counts. Mode and pilot central value are recorded as evidence only, not as the figure of record.
**Source:** 24-02-SUMMARY.md, CLM-10 row in 24-VERIFIED-FACTS.md

---

### DATA-07 Addendum as Sibling File, Not In-Place Master Edit
The DATA-07 correction addendum is a NEW file at `research_package/DATA-07-CORRECTION-ADDENDUM.md`, intentionally NOT added to the master's Per-File Manifest (D-18 sibling-file pattern). The master's per-file source hashes remain valid.

**Rationale:** Adding the addendum to the master's manifest would invalidate the master's source-hash integrity check. A sibling file preserves the master's byte-stability and makes the addendum's relationship to the master explicit.
**Source:** 24-03-SUMMARY.md, 24-03-PLAN.md, D-18

---

### WR-01/02/03 Routed Through Non-CLM Appendix, Not New CLM Rows
WR-01 (1000-vs-100 sample-size conflict), WR-02 (spec-citation typo), WR-03 (spec-citation typo) are NOT new CLM rows. They are routed through the DATA-07 non-CLM appendix keyed by WR ID. CLM is scoped to dataset claims, not issue-doc-internal methodology conflicts.

**Rationale:** CLM rows track observable dataset facts. A sample-size methodology conflict inside the issue doc is not a dataset fact and does not belong in CLM. The non-CLM appendix preserves the findings without polluting the dataset-claims register.
**Source:** 24-04-SUMMARY.md, 24-WR-DECISIONS.md

---

### Ledger Lifecycle Rules Block Copied Verbatim From v1.4 16-ISSUE-LEDGER.md
The v1.4 16-ISSUE-LEDGER.md Lifecycle Rules block (state machine PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED, "FIX_APPLIED is not closure", batch definition, transitive-dependent re-verification, phase-exit gate) was copied VERBATIM. The D-11 KEEP-VERBATIM list held.

**Rationale:** Re-designing the Lifecycle Rules in v1.5 would risk drift from v1.4. Copying verbatim is the only path that lets v1.5 inherit v1.4's state-machine semantics without inventing.
**Source:** 24-03-SUMMARY.md, 24-ISSUE-LEDGER.md, D-22/D-24

---

### Closing Statement Explicit on Unresolved Data Repair
The DATA-07 addendum does NOT use "all package-stated claims confirmed" wording. CLM-10 is corrected, CLM-13 is pending, and DATA-05 is resolved with remediation still required (the targeted rerun had not yet completed at this addendum's authoring).

**Rationale:** A summary that claims full confirmation when parts of the package are still pending misrepresents the work. Explicit closing is the only honest posture.
**Source:** 24-03-SUMMARY.md, 24-03-PLAN.md (verification)

---

## Lessons

### D-16 STOP Gap Fired as Expected — This Is Governed Behavior, Not a Failure
DATA-05 raised GAP-24-01 (semantic STOP) per the plan's D-16 contingency. The contingency was exercised deliberately; GAP-24-01 was raised; the verdict was held; Phase 24 closure and PIPE-07 consumption were blocked until user instruction.

**Context:** The contingency branch is the expected path when a probe finds source-silent empirical facts. The agent should not "rescue" the plan by choosing a baseline.
**Source:** 24-02-SUMMARY.md (Deviations), 24-GAPS.md

---

### probes/outputs/* Stdout Not Committed Per Git Policy
The git policy (`scripts/git_policy/validate_staged_paths.py`) blocks `outputs/*` from staging. The verified-facts register rows carry the probe command + dataset path as the committed, re-derivable evidence; stdout is regenerated on demand.

**Context:** A future agent who needs the probe output must re-run the probe. The committed evidence is the command, not the output.
**Source:** 24-01-SUMMARY.md, 24-02-SUMMARY.md, 24-03-SUMMARY.md (deviations)

---

### DATA-05 70-ID Rerun Validated 2026-06-11 (Same Day as Surfacing)
After the user resolved GAP-24-01, the targeted rerun of the 70 affected base-hier outputs was executed and validated the same day. Post-swap probe reported 0/4,857 mismatches (i.e., the rerun fixed the drift). The remediation was tracked separately in `24-DATA05-RERUN-REMEDIATION.md`.

**Context:** The rerun speed was a function of the dataset size (70 files × Brutus runtime). The same-day turnaround was a feature of the dataset's small affected scope.
**Source:** 24-02-SUMMARY.md (Issues Encountered), 24-DATA05-RERUN-REMEDIATION.md

---

### WR-04 Resolution-Note Accuracy Nit Resolved at Closure
The original WR-04 resolution note said the verified-facts register renders CLM-05a/05b as separate rows, but the register initially kept a single CLM-05 row. This was surfaced as a UAT finding (test 7) and resolved during Phase 24 closure by splitting the register's CLM-05 row.

**Context:** The split required a closure edit, not a re-plan. The register and the addendum now both render the split consistently.
**Source:** 24-04-SUMMARY.md (Issues Encountered), 24-VERIFIED-FACTS.md "Closure edits (2026-06-11)"

---

### Interpreter Gate Required for DATA-05 (numpy)
`data05_mass_drift.py` uses float64 `np.allclose(rtol=1e-15)` and only runs under `.venv/bin/python` (numpy). System `python3` aborts. The interpreter gate is a hard prerequisite; a future agent who runs the probe under system python3 will see a confusing error.

**Context:** The venv gate is project-wide; the DATA-05 probe inherits it. Documenting the gate in the SUMMARY.md is the only way to surface it to a future reader.
**Source:** 24-02-SUMMARY.md (tech-stack added), probes/data05_mass_drift.py

---

### No-Footer Population Characterized as Files With NO Result: Footer AND NO Parameter Fields
The "no-footer" population is files with NO `Result:` footer at all AND NO parameter fields, not "partial/minimal footer" (D-07). The 1,550 / 701 / 219 counts across variants reflect this strict definition.

**Context:** A loose definition would inflate the no-footer count by including files with a partial schema. D-07 holds the line at "no footer at all."
**Source:** 24-02-SUMMARY.md, 24-VERIFIED-FACTS.md (CLM-07/08/09)

---

### Prose Sweep Across Package Found Zero Unregistered Figures
The D-06 prose sweep over RESEARCH-CONTEXT-MASTER.md and DELIVERY-NOTE.md found zero unregistered figures — no CLM-14+ rows were needed. The package was byte-stable against 605c0227.

**Context:** The sweep is a defense against package claims that lack CLM coverage. Zero unregistered figures is the expected outcome when the package was assembled from a known set of claims.
**Source:** 24-02-SUMMARY.md, 24-VERIFIED-FACTS.md

---

## Patterns

### Disposable Read-Only Probe with D-02 Re-Derivability Header
Every probe in `probes/` carries a D-02 re-derivability header: repo-root run command + dataset paths + what the probe records. The header makes the probe re-runnable by any future agent without this session's context.

**When to use:** When authoring dataset probes for a milestone whose claims may be re-verified in a later phase, or by an external auditor.
**Source:** 24-01-SUMMARY.md (tech-stack added), probes/data01..data06

---

### Authoritative Set-Diff Over Grep Counting for Gold-Gap
`base_ids − gold_ids` as a SET difference (parsed from filenames) is the authoritative count, not a 4-digit grep that captures summary numbers (Pitfall 5). The set diff gives 184 exactly, matching `standard_quasi_random_ids_not_in_gold.md` 184/184.

**When to use:** When verifying a "X is missing from Y" claim, the only reliable method is parsing the IDs and computing the set diff. Grep is the wrong tool.
**Source:** 24-01-SUMMARY.md, probes/data03_gold_gap.py

---

### Verified-Facts Register Row Schema
Each row carries: CLM ID · owning DATA · claimed · observed · probe command · dataset path · run date · verdict. The schema makes every claim re-derivable from the row alone, without external context.

**When to use:** When tracking a research milestone's claims and verdicts, and downstream agents need to re-verify a subset of claims without re-reading the entire milestone.
**Source:** 24-01-SUMMARY.md, 24-VERIFIED-FACTS.md

---

### CLM-Keyed Correction Addendum (Sibling-File Pattern)
The DATA-07 correction addendum is keyed by CLM ID: each corrected/confirmed row carries claimed value, observed value, probe command-path, verdict, run date. The addendum is a sibling file to RESEARCH-CONTEXT-MASTER.md, not an in-place master edit.

**When to use:** When a research package needs to record post-assembly corrections without invalidating the master's source-hash integrity.
**Source:** 24-03-SUMMARY.md, research_package/DATA-07-CORRECTION-ADDENDUM.md

---

### STOP-Gap Field Set With Mathematical/Engineering Grounding
Each STOP-gap entry carries the full required field set: decision point, source silence with file:line, math/engineering grounding, options A/B/C, confidence. The grounding is not optional — the agent must demonstrate understanding of why the gap is consequential.

**When to use:** When raising a STOP gap on a source-silent semantic decision. The grounding is what distinguishes a real gap from a recording error.
**Source:** 24-02-SUMMARY.md (patterns-established), 24-GAPS.md (GAP-24-01), project CLAUDE.md (STOP protocol)

---

### Erratum Corrections Re-Probed From Phase 24's Own Evidence
Two erratum corrections (no-`_gold_`-infix; 1,550/701/219 no-footer populations) are re-stated from Phase 24's re-probed evidence (D-07), not transcribed from the master. Counts are unchanged; characterizations are corrected.

**When to use:** When a master document carries an inaccurate characterization that is contradicted by direct empirical observation. The correction must come from the phase's own probes, not a re-transcription.
**Source:** 24-02-SUMMARY.md (key-decisions), 24-03-SUMMARY.md (key-decisions)

---

## Surprises

### 70 Base-Hier Mass-Drift Files Were Not Explained by Perturbation
The DATA-05 probe found 70 base-hier files with `m_Brutus(t=0) != m_IC` at `rtol=1e-15` (abs diff 0.1-1.0). Gold-hier matched 0/4,857; base-std matched 0; gold-std matched 0. The asymmetry (only base-hier affected) pointed to a generation or perturbation quirk specific to one variant, but the provenance was source-silent.

**Impact:** The drift was too large to be a `decimal.Decimal` precision issue (diffs 0.1-1.0). The targeted rerun fixed it, but the original cause remains an open question for the project.
**Source:** 24-02-SUMMARY.md, 24-GAPS.md, 24-DATA05-RERUN-REMEDIATION.md

---

### CLM-10 Was Off by ~2 Across All Three Variants
The claimed snapshot counts (~59 / ~125 / ~1000) were systematically under-counted by ~2 across standard / hier / gold. The integer-rounded medians (61 / 127 / 1003) were close to but not equal to the claimed values.

**Impact:** A future agent reading the claim vs the observation will see a consistent ~2% bias. The `~` prefix in the original claim acknowledged the imprecision; the correction made the precision explicit.
**Source:** 24-02-SUMMARY.md, CLM-10 row

---

### 184 Base-Only Standard IDs Entangled With PSC and Gold-Completion
The DATA-03 probe found 184 base-only standard IDs (no gold counterpart). This count entangled with the Phase 28 PSC pooled-population question and the Phase 26-04 M13 gold-counterpart decision.

**Impact:** The 184 became a cross-phase coordination point. The v1.5 closure accepted the 184 as a known backlog (gold re-simulation deferred to OI-7b / FUT-01 FO-1).
**Source:** 24-01-SUMMARY.md, 26-04-SUMMARY.md (Resolution), 29-01-SUMMARY.md (reframe)

---

### Blacklist Consumption Map Did Not Match the M11 Severity Assumption
The M11 evidence-packet verdict assumed training-time blacklist exclusion (BLOCKING). DATA-02's nuanced map showed the json is loaded only by `dataset_readiness_checks`; current Brutus runners use `Documentation/problematic_ics/{type}/`; the M11 live-loader consumption question is OUTSIDE grounding limits (SCOPE-10).

**Impact:** The M11 verdict grounds in data-integrity arguments (byte-identical-subset, before-statistics ordering, fail-closed), not in operational blacklist load. The architectural-harm narrative is explicitly NOT load-bearing.
**Source:** 24-01-SUMMARY.md, 25-02-SUMMARY.md (M11 verdict), 25-GAPS.md (OI-8 carry-forward)

---

### Standard 2,749-vs-2,750 Wrinkle Resolved as No Off-By-One
The data04_footers probe initially suggested a 2,749-vs-2,750 mismatch that looked like an off-by-one. Closer inspection (CLM-01 nominal range vs observed max) showed it was the README's stated range, not a count error. The wrinkle resolved as "no off-by-one" and was recorded in the Anomalies section.

**Impact:** A future agent reading the Anomalies entry can verify the resolution by re-reading CLM-01 and the README ranges. The wrinkle is closed.
**Source:** 24-03-SUMMARY.md, 24-ISSUE-LEDGER.md (Anomalies section)
