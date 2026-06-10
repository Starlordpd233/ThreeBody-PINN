# Phase 24: Empirical Dataset Verification and Correction Addendum - Context

**Gathered:** 2026-06-10
**Status:** Ready for planning
**Mode:** `--all --auto` — all gray areas auto-selected; recommended options chosen by Claude per explicit user instruction ("pick the best option yourself following your best judgement") and logged in `24-DISCUSSION-LOG.md`. Decisions are grounded in REQUIREMENTS.md / ROADMAP.md / PROJECT.md / committed Phase 23 artifacts wherever possible and marked Claude's discretion otherwise.

<domain>
## Phase Boundary

Establish verified, re-derivable dataset facts by probing every package-stated ("claimed, unverified") issue-02 figure against the on-disk `simulation_data/` dataset (DATA-01..06); compile the CLM-keyed DATA-07 correction addendum for any contradicted package claim and deliver it to the user for forwarding to the in-flight external research (nil addendum if nothing contradicted); and seed the issue ledger — verified facts plus the enumerated issue-02 finding inventory — at its stable path under this phase directory for Phase 25 to consume. Runs **in parallel with the external-research gate window**; gates on nothing external; depends only on the delivered Phase 23 package.

**Not this phase:** adjudication verdicts on any finding (Phase 25); framework-spec edits (Phases 26–28); contract acceptance checks (Phase 29); resolution of the CLM-13 `D = 6.694` and ratio-based-SCS convention conflicts (Phases 25/27/28); any edit to `sampling_method.md` (SCOPE-08), `data_quality_assessment.md` (SCOPE-09), or `pinn/` (SCOPE-10); any data regeneration; any autonomous edit to `simulation_data/Documentation/` (user sign-off required — see D-11).

**Governance:** v1.5 runs under the full STOP protocol (AGENTS.md "CRITICAL GOVERNANCE", v1.5 applicability section). Source-silent semantic / process-schema / cross-phase decisions are surfaced as gaps in `24-GAPS.md` (phase-local, create on first gap) + `.planning/milestones/v1.5-GAPS.md` (milestone index), never invented.

</domain>

<decisions>
## Implementation Decisions

### Probe implementation & evidence capture
- **D-01:** DATA-01..06 are executed as **disposable, read-only probes**: scripts (Python or shell, per-probe judgment) committed under this phase directory (e.g., a `probes/` subfolder), with captured outputs committed beside them. Probes never write inside `simulation_data/` and never touch `pinn/` (VER-09). One-liner probes may be recorded as inline commands in the verified-facts register instead of script files.
- **D-02:** Re-derivability standard (roadmap success criterion 3, SCOPE-06): every recorded fact carries the exact probe command/script reference AND the dataset path it ran against, alongside the observed value and run date — so the user or a later probe can reproduce every count without this session's context.
- **D-03:** Probes stay v1.5-disposable: no packaging into reusable validation tooling (that is FUT-03), no edits to `simulation_data/Scripts/` or `simulation_data/Validation/`. Existing audit artifacts (e.g., `footer_audit_20251224_170141.md`, `check_missing_results*.py`) may be READ as cross-checks/reference, but Phase 24 executes its own probes so the ledger evidence is self-contained — it never cites the doc-integrity audit workstream as a substitute for a probe run.

### Verification checklist scope
- **D-04:** The primary checklist is `research_package/claims-table.md` rows **CLM-01..CLM-12**, each verified via the action in its "Phase-24 check" column and mapped to its owning DATA requirement (CLM-01/02/12→DATA-01, CLM-03→DATA-02, CLM-04→DATA-03, CLM-05/06→DATA-03/04 folder counts, CLM-07/08/09→DATA-04 (footer/parameter probes; the table's column labels these DATA-05 — the requirement mapping in REQUIREMENTS.md governs), CLM-10/11→DATA-06.
- **D-05:** **CLM-13 (`D = 6.694`) is NOT empirically probed.** The claims table's own row note classifies it as a convention conflict routed to Phase 25 (EVID-10) / Phase 27 (PIPE-09). The ledger seed records it as `PENDING` with that routing; Phase 24 takes no position.
- **D-06:** **Bounded prose sweep** beyond the table: `consolidated-context.md`, `framed-research-questions.md`, the package `README.md` (manifest), and `DELIVERY-NOTE.md` are swept for empirical dataset figures that have no CLM row (precedent: the gold-`_gold_`-infix claim escaped the register and surfaced only via the erratum). DATA-07's scope is "every package-stated dataset claim", which is broader than the 13 registered rows. Newly found figures get extension IDs (`CLM-14`, `CLM-15`, …) recorded in the Phase 24 verified-facts register — the delivered `claims-table.md` stays byte-stable — so the addendum remains CLM-keyed (Phase 23 D-12).
- **D-07:** The two **ERRATUM-2026-06-10 corrections fold into the DATA-07 addendum** regardless of re-probe outcomes (STATE.md decision 2026-06-10): (1) gold filenames carry no `_gold_` infix — gold status is folder-encoded only; (2) the 1,550/701/219 "partial/minimal footer" populations have **no `Result:` footer at all** (no `eta`/`tol`/`Lw`/energy fields anywhere). Phase 24 re-executes both probes itself (per D-03) and the addendum supersedes the erratum.

### Verdict semantics
- **D-08:** Per-claim verdict vocabulary is fixed by roadmap success criterion 1: **`confirmed` / `corrected` / `unverified`**. `corrected` rows enter the addendum with claimed value, observed value, and probe method. `unverified` is used ONLY when a probe cannot run within grounding limits, with the reason recorded — it is never a shortcut for "didn't get to it".
- **D-09:** Approximate claims (`~59`/`~125`/`~1000` snapshots, `~4,000`/`~5,000` nominal ICs): the probe records the **full distribution** (DATA-06 mandates distributions, not single examples — per-variant min/median/mode/max plus counts at modal values); the verdict is judged at the claim's stated precision (e.g., `~59` is `confirmed` iff the observed central value rounds to it). Exact observed values are always recorded; if an approximation is materially off, the row is `corrected` with exact figures.
- **D-10:** DATA-02 blacklist **consumption status** is checked across `simulation_data/Scripts/` only (SCOPE-07 grounding — grep runners/prescreening/metrics for blacklist loading). The M11 claim that the blacklist is "not loaded at training time" concerns `pinn/`, which is outside v1.5 grounding (SCOPE-10): that aspect is recorded as `unverified — outside grounding limits, deferred to Phase 25 adjudication and the FUT-01 handoff`, exactly as DATA-02's own text anticipates.
- **D-11:** If a probe contradicts `simulation_data/Documentation/` content: the empirical observation outranks the documentation text (SCOPE-06), the contradiction is recorded in the register, and a README correction is **proposed to the user for sign-off** — never applied autonomously (precedent: audit-workstream corrections `d18f676`, `31b2cff`, `ae609f3` all landed on user sign-off). If the contradicted figure is package-stated, it also enters the addendum.
- **D-12:** New discrepancies that contradict **no** package-stated claim (e.g., if ID parsing shows the standard base folder's 2,749 entries do not reconcile with the gap arithmetic implying 2,750 trajectories) are recorded in the ledger's anomalies section and surfaced in the phase summary — NOT in the DATA-07 addendum, whose scope is package-stated claims only.

### DATA-01 ID-gap counting method
- **D-13:** Gap counting parses numeric IDs from filenames (`brutus_standard_XXXX.txt` / `brutus_hierarchical_XXXX.txt`) and computes the missing-ID set against the nominal ID range — **not** bare file counts, which duplicates or non-trajectory entries could confound. The nominal range convention (0-based vs 1-based, range end) is read off the observed data and `simulation_data/Scripts/ic_generation/` provenance, and the method is recorded with the result.

### DATA-05 mass-drift probe design
- **D-14:** Comparison fixed by DATA-05: `m_IC` (mass slots in `simulation_data/Data/ic_final/` files) vs the mass column of the t=0 snapshot block in the corresponding Brutus output file, compared with `np.allclose(rtol=1e-15)` on float64-parsed values.
- **D-15:** Sample: **default full population** — every trajectory with an IC counterpart, across all four Brutus output variants (first-block parsing is cheap; full coverage eliminates sampling-bias questions and satisfies "documented sample" a fortiori). Fall back to a seeded stratified sample (≥100 per variant, RNG seed recorded) only if runtime proves prohibitive; either way the sample definition is documented with the result.
- **D-16:** Baseline contingency: Phase 23's consolidated context documents **hierarchical IC perturbations** applied between IC generation and Brutus input. If mass mismatches cluster in hierarchical variants, the executor checks `simulation_data/Scripts/ic_generation/` provenance to determine whether masses were perturbation-invariant BEFORE recording a verdict. If the provenance is ambiguous about what Brutus actually consumed, that is a **STOP gap (semantic)** — surfaced, not resolved by choosing a baseline.
- **D-17:** Verdict interpretation (feeds PIPE-07, Phase 27): allclose pass ⇒ "IC masses canonical at float64"; fail ⇒ characterize whether the mismatch is float64 round-trip/parse precision (⇒ "`decimal.Decimal` parsing required") or genuine value drift (⇒ anomaly per D-12 and candidate STOP gap). The verdict is recorded with its evidence in the ledger.

### DATA-07 addendum form & delivery
- **D-18:** One canonical addendum file placed **beside the package files inside `research_package/`** (erratum precedent: sibling file, NOT added to the manifest, all originally-delivered package files byte-stable). Self-describing name, e.g. `DATA-07-CORRECTION-ADDENDUM.md` (exact name = Claude's discretion).
- **D-19:** Addendum structure: CLM-keyed rows — claimed value, observed value, probe command/path, verdict — plus an explicit supersession statement over `ERRATUM-2026-06-10.md` folding in its two corrections (D-07). A confirmed-claims summary section records what verification upheld, so the external researcher can also stop discounting confirmed figures.
- **D-20:** Nil-addendum case (grounded in DATA-07): if no package-stated claim is contradicted, the same file records that all package-stated claims were confirmed, with the probe index.
- **D-21:** Delivery semantics: the addendum ships **as soon as the probes finish** — never waiting on the resolution doc — as a commit plus a notification to the user, who forwards it to the in-flight external research. The agent sends nothing externally itself.

### Issue-ledger seeding
- **D-22:** Path: `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-ISSUE-LEDGER.md` — the "stable path under the Phase 24 directory" named by the roadmap, following the v1.4 precedent (`16-ISSUE-LEDGER.md`).
- **D-23:** Seed scope: the full enumerated in-scope issue-02 finding inventory — B-06, B-11, M11, M12, M13, D7, G1–G5, D-03 (training-data format), the SCS/SASD/IPR/PSC validation-metric claims, `compute_globals` `D = 6.694`, the footer/mass-drift protocol, and precision handling (per REQUIREMENTS.md and `23-CLAIMS-INVENTORY.md`) — each initialized `PENDING` with its owning requirement and adjudication phase noted; plus the verified-facts register (CLM/DATA-keyed, per-row probe citations) as the dataset-evidence annex; plus the anomalies section (D-12).
- **D-24:** Schema: v1.4 `16-ISSUE-LEDGER.md` format with the roadmap-prescribed state machine (`PENDING → IN_PROGRESS → FIX_APPLIED → VERIFIED`, or `DEFERRED` with a written blocker). Phase 24 **initializes states only** — the operating protocol (evidence-packet format, verdict recording, re-verification rules) is Phase 25's to establish; Phase 24 does not over-specify columns Phase 25 owns.

### Workflow
- **D-25:** Tag `v1.5-pre-phase-24` cut from `milestone/v1.5` HEAD (`4b6ff913`) during this discuss session (Phase 23 precedent; STATE.md standing instruction). One atomic commit per plan via `scripts/agent-commit`. Phase 24 gates on nothing external and runs during the gate window.

### Claude's Discretion
- Probe language per probe (Python vs shell), probe/evidence file names, `probes/` subfolder layout, and the exact addendum filename — presentation-only; keep names self-describing and consistent with `NN-*` phase-artifact conventions.
- Verified-facts register placement: standalone `24-VERIFIED-FACTS.md` vs a section of `24-ISSUE-LEDGER.md` — either satisfies roadmap criterion 5 as long as the ledger file links it at the stable path.
- Prose-sweep recording format (how non-table claims and their CLM-14+ IDs are listed).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase requirements & protocol (read first)
- `.planning/REQUIREMENTS.md` — DATA-01..07 (this phase's seven requirements, verbatim), source-treatment policy, SCOPE-06..11 boundaries.
- `.planning/ROADMAP.md` §"Phase 24: Empirical Dataset Verification and Correction Addendum" — goal, five success criteria, parallel-with-gate semantics; §"Source treatment & STOP protocol"; §"Verification protocol".
- `AGENTS.md` / `CLAUDE.md` §"CRITICAL GOVERNANCE: v1.4 and similar adjudication milestones" — STOP protocol with v1.5 substitutions (gap registers: `24-GAPS.md` phase-local, `.planning/milestones/v1.5-GAPS.md` milestone index — neither exists yet; create on first gap).

### Verification checklist (the package under test)
- `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/claims-table.md` — THE checklist: CLM-01..13 with per-row Phase-24 check actions (CLM-13 excluded from probing per its row note).
- `.../research_package/ERRATUM-2026-06-10.md` — two interim corrections the DATA-07 addendum must fold in and supersede; also lists what the audit re-verified as correct (CLM-05/06/07-count/08/09).
- `.../research_package/consolidated-context.md` — prose-sweep subject (D-06); carries the corrected-by-erratum naming and footer narratives.
- `.../research_package/framed-research-questions.md` — prose-sweep subject; uses CLM references that must stay consistent with verification outcomes.
- `.../research_package/README.md` — package manifest with per-file source hashes (byte-stability reference; addendum stays out of it).
- `.../research_package/DELIVERY-NOTE.md` — announced the DATA-07 addendum channel to the user; addendum delivery must match what was promised.
- `.planning/phases/23-research-package-assembly/23-CLAIMS-INVENTORY.md` — claims provenance and finding-inventory source for the ledger seed (D-23).

### Dataset under probe (SCOPE-06 grounding)
- `simulation_data/Data/brutus_output/brutus_standard_quasi_random/` (2,749 entries at discussion time), `brutus_standard_quasi_random_gold_standard/` (2,565), `brutus_hierarchical/` (4,857), `brutus_hierarchical_gold_standard/` (4,857) — probe targets; entry counts here are informal `ls` observations, NOT evidence (probes must parse IDs per D-13).
- `simulation_data/Data/ic_final/ic_standard_quasi_random/`, `ic_final/ic_hierarchical/` — `m_IC` side of DATA-05.
- `simulation_data/Documentation/README.md` — dataset spec (corrected 2026-06-10 on user sign-off; commits `d18f676`, `31b2cff`, `ae609f3`); grounding source for verified-status citations, but D-11 governs new contradictions.
- `simulation_data/Documentation/standard_quasi_random_ids_not_in_gold.md` — the 184-ID gold-gap record (DATA-03 cross-check).
- `simulation_data/Documentation/problematic_ics_blacklist.json` — DATA-02 subject (claimed 65 IDs = 2 hierarchical + 63 standard).

### Provenance scripts (SCOPE-07 grounding)
- `simulation_data/Scripts/ic_generation/` (incl. `ic_generation_utils.py`, perturbation provenance for D-16) — ID-range conventions, mass handling.
- `simulation_data/Scripts/brutus_runners/` — runner parameter blocks (folder-default tol/dt_out provenance for CLM-09).
- `simulation_data/Scripts/metrics_calculation/calculate_metrics.py` — metrics provenance; DATA-02 consumption-status grep target.
- `simulation_data/Validation/prescreening/` — prescreening thresholds; DATA-02 consumption-status grep target.
- `simulation_data/Validation/audit_reports/footer_audit_20251224_170141.md` — prior footer audit whose "Missing Footer" column (1,550/701/219) cross-checks the DATA-04 probe (read-only reference per D-03).

### Adjudication subject (claims provenance only — no adjudication this phase)
- `pinn_instruction/issues/02-data-pipeline-and-validation.md` — NON-authoritative issue doc; line-cited source of the claimed figures (lines 13, 57–60, 202, 231, 258, 289, 297, 311–312, 326 per claims table).

### Precedents
- `.planning/milestones/v1.4-phases/16-evidence-framework-and-issue-adjudication/16-ISSUE-LEDGER.md` — ledger schema precedent (D-24).
- `research_package/ERRATUM-2026-06-10.md` sibling-file pattern — addendum placement precedent (D-18).

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `claims-table.md` CLM rows with per-row "Phase-24 check" actions — the probe checklist arrives pre-specified; plans can map probes 1:1 onto rows.
- Existing audit scripts/reports under `simulation_data/Validation/` (`check_missing_results*.py`, footer audits) — readable cross-checks and method reference; Phase 24 still runs its own probes (D-03).
- `scripts/agent-commit` — mandatory commit path; one atomic commit per plan.
- v1.4 ledger format (`16-ISSUE-LEDGER.md`) — schema to instantiate, not redesign.

### Established Patterns
- Phase artifacts named `24-*.md` in `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/`.
- STATE.md mutations only via gsd-tools handlers (universal anti-pattern 15).
- Probe evidence recorded with command + path + output (v1.4 disposable-probe style; SCOPE-06 re-derivability).
- Package byte-stability: delivered files are never modified; corrections travel as sibling files (erratum precedent).

### Integration Points
- DATA-07 addendum → user forwards to the in-flight external research (the package's DELIVERY-NOTE promised this channel).
- `24-ISSUE-LEDGER.md` → consumed by Phase 25 (evidence framework operates the protocol on this seed).
- DATA-05 mass-drift verdict → PIPE-07 precision contract (Phase 27).
- DATA-06 snapshot/dt_out distributions → PIPE-04 points-per-trajectory contract (Phase 27).
- DATA-02 blacklist verification → PIPE-03 blacklist-exclusion contract (Phase 26).
- DATA-04 footer facts → PIPE-06 footer-heterogeneity contract (Phase 26).

</code_context>

<specifics>
## Specific Ideas

- The erratum's "Not affected" list (CLM-09 defaults, the 2,749/4,857/219/592 counts, full-schema footer tuples) means several probes have a strong prior of `confirmed` — but Phase 24 still re-derives each one independently (D-03); the prior is noted, not relied upon.
- Standard-base arithmetic wrinkle to watch: claimed 1,250 gaps / 4,000 nominal implies 2,750 present, while the folder shows 2,749 entries — exactly the kind of off-by-one the ID-parsing method (D-13) exists to settle; route the outcome via D-08 (corrected claim) or D-12 (anomaly) as the evidence dictates.
- The `final_timestep >= 9.5` RULE is grounded in README Completeness Checks; only its PREVALENCE is unverified (CLM-11 row note) — the probe quantifies prevalence, it does not re-adjudicate the rule.
- Footer probes must treat "minimal/partial footer" language as superseded: the corrected disk fact is NO footer at all in the 1,550/701/219 populations; "footers that are present carry the full schema, including `eta` and `tol`" (erratum Correction 2).

### Deferred Phase-23 review items (WR-01..04)

The Phase 23 verifier (`23-REVIEW.md:115-173`) classified four package warnings as non-blocking but routed them to "a Phase 24 DATA-07 correction pass." They are not yet in Phase 24's discuss artifacts; this subsection carries them in so the plan incorporates them. All corrections are grounded (no invention needed); two schema questions and one channel question are surfaced as open decisions in `24-DISCUSSION-LOG.md` (not pre-decided).

| ID | What | Where | Grounded disposition | Open decision (surfaced) |
|----|------|-------|----------------------|--------------------------|
| WR-01 | Q-B2 attributes "1000 IC–Brutus pairs" to both citations; issue doc says 1000 at line 204 but P2-2 (line 292) says **100** — conflict unsurfaced | `framed-research-questions.md:304-309` | Report both figures neutrally; surface the issue-doc-internal conflict (the package's stated job) | Register sample-size as a new CLM row? (**schema → surfaced**) |
| WR-02 | Hard Constraint 3 cites COM-Invariance check at line **972**; it's at **967** (972 is §10.3) | `framed-research-questions.md:92-94` | Correct to "§10.2 'COM Invariance' (lines 967–971)" — verifiable against `pinn_architecture.md` snapshot | Channel: citation fix is not a dataset/CLM claim (see WR-02/03 channel decision below) |
| WR-03 | Q-B1 cites nonexistent ctl "§5.3.2"; actual text is Step 5 / "(e.g., 32)" at line ~1201 — an example, not a hard 32-pt contract (affects how contested M12 is) | `framed-research-questions.md:292-293` | Replace with Step 5 "Mini-Batch Construction…" line ~1201 wording — verifiable against `ctl_instruction.md` snapshot | Channel: same as WR-02 (see below) |
| WR-04 | CLM-05 used for two observables: IC folder counts vs Brutus output file counts (coincide today, can diverge) | `claims-table.md:25`, `consolidated-context.md:89,98` | DATA-03/04 probe must count IC folders **and** Brutus output folders separately and report both | Split CLM-05 → CLM-05a/05b vs amend CLM-05 text (**schema → surfaced**) |

**Downstream mapping:**
- **WR-04 → DATA-03/04 probe design:** count IC and Brutus folders separately; this is the one with direct probe impact. Whichever schema choice the user makes, the probe must report both observables independently.
- **WR-01/02/03 → DATA-07 addendum scope:** these are correction candidates that must reach the in-flight external research. WR-01 also raises a schema question (new CLM row). WR-02/03 are spec-citation typos in the framed-questions doc — not dataset claims — so their channel inside the addendum is an open decision.

**Byte-stability preserved:** all corrections travel through the correction channel (sibling files), never as in-place edits to delivered package files.

</specifics>

<deferred>
## Deferred Ideas

- Adjudication verdicts, evidence packets, and root-cause conflict resolution (ratio-SCS vs locked gate; `D = 6.694` vs PHYS-01) — Phase 25 (EVID-06..10), spec edits Phases 26–28.
- Any README/dataset-documentation correction — proposed to user for sign-off only (D-11); the edit itself is not Phase 24 work.
- Packaging probes into reusable validation tooling — FUT-03.
- M16 collocation-scaling, G6 causal-training, training-loop metric usage — doc-03 milestone (SCOPE-11).
- Prescribing structure for the user's resolution doc — rejected in Phase 23 (D-16 there); remains out of scope.

</deferred>

---

*Phase: 24-Empirical Dataset Verification and Correction Addendum*
*Context gathered: 2026-06-10*
