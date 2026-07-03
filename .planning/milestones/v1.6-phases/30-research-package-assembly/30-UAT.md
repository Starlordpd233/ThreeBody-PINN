---
status: complete
phase: 30-research-package-assembly
source: [30-SPEC.md, 30-01-SUMMARY.md, 30-02-SUMMARY.md, 30-03-SUMMARY.md, 30-04-SUMMARY.md, 30-05-SUMMARY.md]
started: 2026-06-18T20:00:00Z
updated: 2026-06-18T20:30:00Z
mode: agent-as-tester (specwork/docs phase — deliverables are inspectable artifacts; checks re-run independently from scratch, not trusting SUMMARY/VERIFICATION claims)
---

## Current Test

[testing complete]

## Tests

<!-- One test per SPEC acceptance criterion (lines 86–95) + 2 cross-cutting integrity checks.
     Every check re-run first-hand against the on-disk package. -->

### 1. ERW package structure exists
expected: A package at `…/research_reports/03-curriculum-and-training-loop/` with DELIVERY-NOTE.md + research_package/{RESEARCH-CONTEXT-MASTER.md, RESEARCH-AGENT-PROMPT.md, 5 companions} + specs/ commit-pinned snapshots.
result: pass
evidence: `find` shows 15 files — DELIVERY-NOTE.md (round root) + master + prompt + 5 companions (framed-research-questions, scope-12-hard-constraints, resolution-doc-skeleton, claims-register, verified-facts-reference) + specs/ (6 snapshots + consolidated-context.md).

### 2. Annotated document list complete + consolidation surfaced at the D-09 gate
expected: A 12-row annotated candidate list; framework specs never consolidated; the consolidation plan presented to the user before assembly (D-09 hard gate) with a FILLED APPROVED record.
result: pass
evidence: `30-CONSOLIDATION-PLAN.md` carries the 12-row list (each role-annotated) + a FILLED D-09 APPROVED record (status + authority + 3 resolved inclusion calls + declined-findings slot). Filled under the user's pre-authorized approve-as-proposed waiver; reversible until assembly. Specs classified NEVER-consolidated (D-04).

### 3. Required package inputs present with correct treatment
expected: Intact issue-03 + ctl_instruction.md + pinn_architecture.md + review_of_framework.md + stage_strat_revision.md + sampling_method.md (FROZEN) + a v1.5-verified-facts reference.
result: pass
evidence: specs/ holds all 6 byte-for-byte snapshots; sampling_method.md annotated FROZEN (SCOPE-08) in the master manifest; standalone `verified-facts-reference.md` present (D-09 inclusion call (b) = STANDALONE). Both reports ship with the baseline-critique mandate (ERW rule 6).

### 4. Framed questions — coverage + neutrality + issue-03 section order
expected: One neutral question per finding in issue-03 section order, covering at least {B-07, B-08, M6, M7, M14, M15, M16, D5, NS-12, NS-13, NS-18, the causal-mode/s_min/epsilon decisions, D=6.694}; the 3 decisions + D-conflict posed UNSETTLED.
result: pass
evidence: 18 `###` section headers; clean header grep confirms ALL 15 required findings present (+3 bonus: adaptive stage-assignment, τ_L/L_max, ALM μ_p-clamp). Each question states BOTH the issue-doc and framework-spec positions + a neutral "Open question"; "state all three; recommend none". The epsilon-strategy and D-conflict questions carry explicit LOCKED-vs-OPEN blocks fencing the SCOPE-12-locked sub-parts (`D ≈ 4.6416`, loss-side `eps_soft = 1e-5`) as not-re-openable. Decisions named descriptively (no internal D-04/05/06 in uploads, F15). No presupposed verdict.

### 5. SCOPE-12 hard-constraints preamble present and verbatim
expected: All 7 locked v1.4+v1.5 outcomes listed verbatim as a fixed boundary set.
result: pass
evidence: `scope-12-hard-constraints.md` §1 lists all 7 verbatim (14D `[τ,IC₁₃]`; Jacobi IC₁₃; mass-weighted COM head; PHYS-03 `eps_soft=1e-5`; SCS gate `ε_H>10⁻⁵`/`SCS>−5`; PHYS-01 raw-mass `D≈4.6416`; PIPE-01..10/VAL-01..04). §2 states the SCOPE-10 live-code override; §3 the locked-vs-revisable distinction; §4 declined-findings (none).

### 6. Non-binding per-finding resolution-doc skeleton
expected: One verdict slot per finding, explicitly non-binding, citing the v1.4/v1.5 resolution docs as format precedents (no schema mandated).
result: pass
evidence: `resolution-doc-skeleton.md` — header marked NON-BINDING; one slot per framed question + a finding→adjudication-phase(32–36) map; v1.4 `ctl_pinn_resolution.md` + v1.5 `02-resolution-doc.md` cited as format precedents only; LOCKED sub-parts pre-marked.

### 7. Claims register — claimed/verified + v1.5 citations + no-in-milestone boundary
expected: Every figure rows as `claimed-unverified` or `verified`; every verified row cites a v1.5 source; register states no in-milestone phase verifies the claims.
result: pass
evidence: `claims-register.md` CLM-01..CLM-20. Verified rows CLM-14..CLM-19 each carry an exact v1.5 citation (`24-VERIFIED-FACTS.md` verdicts + `simulation_data/Documentation/` + `ctl_instruction.md §2.5`); claimed rows (incl. CLM-01 `D=6.694`) flagged FUT. The D-17 no-in-milestone-verification boundary statement is present (lines 19–29). Conservative status-classification rule present.

### 8. Both reports characterized read-only + byte-for-byte unchanged
expected: review_of_framework.md and stage_strat_revision.md characterized (provenance + content map + doc-03 relation), reported to the user, with zero edits (hash-verified).
result: pass
evidence: `30-REPORTS-CHARACTERIZATION.md` covers both (git-log provenance, section map, doc-03-finding relation table, F10 locked-within-baseline flags, package-role recommendation). Re-run independently: `git diff --quiet` exit 0 for both; `cmp -s` snapshot==source IDENTICAL; packaged sha256 == recorded (fe5fdc44… / d875cd66…).

### 9. Delivery note + gate semantics + repo-blind entry points + STATE gate
expected: DELIVERY-NOTE.md states the exact landing path + Phase-31 / Phases-32–36 gate semantics; STATE records the gate open; no UPLOADED file (master/prompt) contains a repo path.
result: pass — acceptance met; the 2 entry-point defects (F-1, F-2) were fixed this pass in commit 34110716
evidence: `DELIVERY-NOTE.md` carries the verbatim landing path `…/research_reports/03-curriculum-and-training-loop/` + the "Phases 32–36 gate on the consolidated doc landing AND Phase 31 passing" sentence + the no-in-milestone-verification note. Repo-blind grep on master + prompt = 0 hits each. STATE.md now reads `completed_plans: 5`, `stopped_at: Phase 30 complete (5/5 plans, verified)`, gate OPEN + Phases-32–36 blocker recorded (the earlier 30-VERIFICATION counter concern has since been resolved by the orchestrator).

### 10. Zero edits to protected sources
expected: No edits to ctl_instruction.md, pinn_architecture.md, sampling_method.md, data_quality_assessment.md, the two reports, issue-03, or pinn/ during the phase.
result: pass
evidence: `git diff --stat e841c958(pre-phase tag)..HEAD` on all protected source paths = EMPTY. Working tree clean.

### 11. Snapshot byte-fidelity (all 6 specs/ snapshots)
expected: Each specs/ snapshot byte-identical to its live source and reproduces its recorded SHA-256.
result: pass
evidence: re-run from scratch — `cmp -s` IDENTICAL for all 6 pairs; re-derived sha256 == recorded for all 6 (94c3c03b / 4ee083fc / 318f297a / 750e625e / fe5fdc44 / d875cd66). source_baseline `522cea71` confirmed an ancestor of HEAD.

### 12. Self-containment both directions (F12)
expected: Every shipped upload appears in the master manifest; every bare-filename reference resolves to a shipped file.
result: pass
evidence: all 14 uploaded files (5 companions + master + prompt + 7 specs/ entries) IN-MANIFEST; the manifest references exactly those 14 shipped files. (30-05 documented the both-directions F12 pass; direction (a) re-confirmed here.)

## Summary

total: 12
passed: 12
issues: 0
pending: 0
skipped: 0
blocked: 0
note: All 10 SPEC acceptance criteria + 2 integrity checks PASS. The 2 entry-point accuracy defects (F-1 newly found this pass; F-2 = prior 30-REVIEW.md WR-01) were FIXED in commit 34110716; the 4 prior INFO items (F-3..F-6) remain as optional polish, none violating any acceptance criterion. Independent re-verification confirms the 30-VERIFICATION.md PASSED verdict.

## Findings (non-blocking — none fail an acceptance criterion)

> These are documentation-accuracy defects in already-delivered files — NOT acceptance failures.
> Per user direction, F-1 and F-2 (the two uploaded-entry-point defects) were FIXED in commit
> `34110716` (verified: master + prompt still repo-blind, 0 hits; no specs/ snapshot touched).
> F-3..F-6 remain as optional polish. The corrections are unambiguous and grounded.

- **F-1 [NEW this pass — minor] Wrong CLM cross-reference for the D-conflict in BOTH uploaded entry points.**
  `RESEARCH-CONTEXT-MASTER.md:66` and `RESEARCH-AGENT-PROMPT.md:63` cite `claims-register.md CLM-13`
  for the `D = 6.694` vs `D ≈ 4.6416` conflict. CLM-13 is the snapshot-counts row (~59/~125/~1000);
  the D-conflict rows are **CLM-01** (claimed `6.694`) and **CLM-19** (locked `4.6416`). The
  framed-questions file and the claims-register Row Notes use CLM-01/CLM-19 correctly. The prior
  `30-REVIEW.md` scoped its CLM-reference check to `framed-research-questions.md` only, so it missed
  these two prose cross-refs. Remediation: change `CLM-13` → `CLM-01/CLM-19` (or `CLM-19`) in both lines. **RESOLVED in `34110716`** — both lines now cite CLM-01/CLM-19.

- **F-2 [= 30-REVIEW.md WR-01 — minor/warning] Master overstates the zero-repo-path guarantee.**
  `RESEARCH-CONTEXT-MASTER.md:26` asserts as an absolute: "No file in this package, other than the
  never-uploaded delivery note, names a repository path." False — the grounding companions
  (claims-register, verified-facts-reference, consolidated-context) deliberately retain repo paths as
  provenance labels (D-10 exempt). Self-contradicted by its own manifest (lines 126–127, 139) and its
  narrower, correct line-160 guarantee. Remediation: scope line 26 to the authored entry points
  (master + prompt name no repo path; grounding companions retain non-navigable provenance labels).
  **RESOLVED in `34110716`** — line 26 rescoped to the authored entry points.

- **F-3 [= 30-REVIEW.md INFO-01 — info] CLM-NN namespace collision.** Package `CLM-NN` IDs coexist with
  the cited `24-VERIFIED-FACTS.md`'s own independent `CLM-NN` numbering; four IDs collide with different
  meanings. Well-mitigated (every cross-namespace cite carries the filename prefix; that source is not
  attached). Remediation: one clarifying sentence in the claims-register provenance note.

- **F-4 [= 30-REVIEW.md INFO-02 — info] Orphan register rows.** CLM-18 (hierarchical 4,857) and CLM-20
  (M16 scaling factors) are referenced by no question/companion; the M16 question cites only CLM-17,
  not the derived CLM-20. Remediation: cite CLM-20 from the M16 question (and CLM-18 where relevant) or
  annotate both as context-only anchors.

- **F-5 [= 30-REVIEW.md INFO-03 — info] Bare-filename claim vs specs/ prefix.** Master:105 asserts "every
  file is referenced by bare filename," but the specs/ manifest rows carry the `specs/` location prefix.
  Remediation: soften line 105 or drop the prefix.

- **F-6 [= 30-REVIEW.md INFO-04 — info, not a defect] Stage-5 absent from stage counts.** Faithful to the
  non-authoritative issue-03 Stage Inventory (which omits Stage 5); consistent across register and
  consolidated context. Optional one-line "faithful to source" note.

## Gaps

<!-- For plan-phase --gaps: only acceptance-criterion FAILURES belong here. -->
none — no acceptance criterion failed. The 6 items above are non-blocking documentation-accuracy
polish in already-delivered artifacts; see Findings. No STOP-protocol gap arose during verification
(these are conformance findings, not source-silent semantic decisions).
