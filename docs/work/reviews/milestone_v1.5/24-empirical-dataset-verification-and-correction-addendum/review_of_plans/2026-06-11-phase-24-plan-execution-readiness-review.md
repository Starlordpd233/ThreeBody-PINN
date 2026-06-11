# Phase 24 Plan Execution Readiness Review

**Date:** 2026-06-11
**Scope:** `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-01-PLAN.md` through `24-04-PLAN.md`
**Review mode:** Compound Engineering document review, using coherence, feasibility, scope-guardian, and adversarial lenses (4 parallel reviewer agents; round 1; report-only — no fixes applied).
**Repo snapshot:** HEAD `605c0227` on `milestone/v1.5`.
**Verdict:** Not ready for flawless autonomous execution. Two P0 blockers offer the user choices the plan set cannot legally execute or let a false "all-confirmed" statement ship externally; four P1 findings leave the phase's central integrity checks asserting nothing or failing on correct behavior.

## Snapshot Caveat — Concurrent Editing In Flight

This review ran while another session was actively repointing the Phase 24 plans to the consolidated research master: commit `605c0227` (package consolidation, which retired `ERRATUM-2026-06-10.md`, `claims-table.md`, `framed-research-questions.md`, and the package README) landed mid-review, and `24-04-PLAN.md` was modified at 11:07 while reviewer agents were running. All evidence quotes below were re-verified against the post-`605c0227` state before this report was written. Findings P1-1 (stale erratum references in `24-03-PLAN.md`) may be partially resolved by that in-flight repointing pass — re-verify them once the concurrent session's pass completes, but do not assume it covers the verification-command and gate-semantics findings, which are independent of the consolidation.

## Executive Summary

The Phase 24 plan set is governance-conscious in a way few plan sets are: read-only fences, STOP-gap contingencies, re-derivability headers, byte-stability invariants, and a dedicated human gate are all explicitly designed in, and all 25 locked decisions (D-01..D-25) are cited where implemented. The four reviewer lenses found no problem with the phase's intent or decomposition.

The risk is the same one Phase 23's review found: critical properties are stated in prose but not made deterministic for a literal autonomous executor. Three patterns dominate the findings:

1. **The user gate offers options the plan set cannot execute.** The WR gate presents "direct correction in RESEARCH-CONTEXT-MASTER.md" as a selectable channel, but every plan's invariants forbid modifying that file and no task owns the edit.
2. **The integrity checks don't check the invariant.** The byte-stability acceptance commands contain literal `<research_package>` placeholders (verified to exit 0 against *nothing*), and `git diff --quiet` compares worktree-to-HEAD, not the stated 2026-06-11 baseline.
3. **The verification gates assert the priors the phase exists to test.** Probe verify commands grep stdout for expected pilot values, so a probe that correctly discovers a deviating value — the exact event DATA-07 exists to capture as a `corrected` verdict — fails its own gate.

One reassurance from the feasibility pass: every value prior baked into the plans (2,749/2,565/Δ=184; 4,857; no-footer 701/219/1,550; blacklist 2+63; max IDs 3998/4999; no `_gold_` infix; `config.py` blacklist load; README ~1005 "legacy") was independently re-derived against the live dataset and **holds today**. The prior-coupled gates will pass at current state; the findings below are about design robustness under the branches the plans themselves anticipate, not present-day data drift.

## P0 Blockers

### P0-1: The WR Gate Offers A "Direct Correction" Option No Plan Can Execute

**Found by:** all four lenses (coherence, feasibility, scope-guardian, adversarial). **Confidence:** 100 (text), 75 (consequence severity).

**Evidence:** `24-04-PLAN.md:98-99` offers option "(B) direct correction in RESEARCH-CONTEXT-MASTER.md's current text", and `24-04-PLAN.md:103-104` states `"interim fix NOW" means direct correction in RESEARCH-CONTEXT-MASTER.md`. But:

- No Phase 24 plan lists `RESEARCH-CONTEXT-MASTER.md` in `files_modified`.
- `24-03-PLAN.md` must_haves require "`RESEARCH-CONTEXT-MASTER.md / DELIVERY-NOTE.md / specs/*.md` are unchanged (D-18)" and its governance says corrections are "never an in-place doc edit".
- `24-04-PLAN.md` itself declares "Nothing is built autonomously — this is a governance MUST-surface gate."

**Why this matters:** This is the same failure shape as Phase 23's P0-1 (`exclude-dqa`). If the user selects (c)(B) or (d)="interim fix NOW", the executor holds a recorded user instruction that collides head-on with 24-03's unconditional byte-stability must_have. Wave 3 then either deadlocks under the STOP protocol or violates the phase's central integrity invariant on a delivered external artifact. The user is being offered a viable-looking choice that the plan set cannot honor.

**Fix:** Decide before the gate fires, one of:

- Restrict the live options to (c)(A) "non-CLM appendix in the DATA-07 addendum" and (d)="hold for consolidated addendum" — the only choices implementable within the current four-plan set; or
- Keep (B)/interim-NOW but state explicitly in the option text that selecting it constitutes a user-authorized waiver of D-18 for the named lines, and add a conditional master-edit step to 24-03 (with `files_modified` updated and a scoped diff exception replacing the blanket byte-stability criterion).

### P0-2: Addendum Assembly Has No OPEN-Gap Precondition — A Nil Addendum Can Claim "All Confirmed" Over Held Verdicts

**Found by:** adversarial. **Confidence:** 75.

**Evidence:** `24-03-PLAN.md` must_haves: "if no package-stated claim is contradicted it is a nil addendum recording all-confirmed with the probe index (D-20)". `24-01-PLAN.md` Task 1 anticipates CLM-01 being held: "mark CLM-01 `unverified — nominal-range convention source-silent, gap surfaced` pending user instruction". Nothing in 24-03 checks `24-GAPS.md` or `v1.5-GAPS.md` for OPEN entries before assembly.

**Why this matters:** Same failure shape as Phase 23's P0-2 (delivery proceeding over unresolved STOP gaps). Branch: the DATA-01 (or DATA-05) STOP gap fires, the user has not yet answered by wave 3, and no other claim is contradicted. The D-20 nil logic is binary (contradicted vs. confirmed) with no third state for `unverified`/held verdicts — the addendum then records "all package-stated claims confirmed", a false statement about CLM-01, and is committed and forwarded to external researchers per D-21.

**Fix:** Add a pre-assembly gate to 24-03 Task 1: if any register row is `unverified` due to an OPEN gap entry, the nil/all-confirmed wording is forbidden; the addendum must carry an explicit "unresolved — gap pending user instruction" status for those rows (or assembly halts per protocol and the blocker is surfaced). A concrete check in the spirit of the Phase 23 fix:

```sh
test ! -f .planning/phases/24-*/24-GAPS.md || ! grep -q 'OPEN' .planning/phases/24-*/24-GAPS.md
```

## P1 High-Priority Findings

### P1-1: `24-03-PLAN.md` Still Instructs Reading And Copying A Retired, Nonexistent File

**Found by:** all four lenses. **Confidence:** 100.

**Evidence:** `24-03-PLAN.md:95` read_first: "ERRATUM-2026-06-10.md (the file this addendum supersedes; copy its sibling-file structure; …)". Verified: `research_package/` contains only `DELIVERY-NOTE.md`, `RESEARCH-CONTEXT-MASTER.md`, and `specs/` — the erratum was deleted by consolidation commit `605c0227`. The same stale cluster includes: 24-03's instruction to assert "README per-file hashes valid" (the package README was retired; hashes now live in the master's Per-File Manifest), 24-02 Task 3 `<done>`'s "claims-table.md untouched" (file retired), and `24-PATTERNS.md`'s `ERRATUM:15-42`/`ERRATUM:46-72` line citations.

**Why this matters:** The executor hits a failed read at wave 3 and, under the STOP protocol, will halt or surface a spurious gap — or improvise the addendum structure, which is worse. Note 24-01/24-02/24-04 were already repointed to the consolidated master (24-04 even carries a NOTE about the retirement at line 72/99); 24-03's read_first appears to be the unfinished tail of that repointing pass.

**Fix:** Repoint 24-03 Task 1: structure source → `24-PATTERNS.md` §"DATA-07-CORRECTION-ADDENDUM.md"; supersession target → `RESEARCH-CONTEXT-MASTER.md` §"Correction Provenance And Verification Boundaries"; replace "README per-file hashes valid" with "the master's Per-File Manifest hashes remain valid"; replace 24-02's "claims-table.md untouched" with "delivered package files untouched". Align the objective/done wording from "supersedes the erratum" to "supersedes the master's correction-provenance section" (the must_haves already say this correctly).

### P1-2: Byte-Stability Checks Pass Vacuously — Placeholder Pathspec And Wrong Baseline

**Found by:** feasibility, adversarial (both verified empirically). **Confidence:** 100.

**Evidence:** `24-02-PLAN.md:221` and `24-03-PLAN.md:131` use literal placeholders: `` git diff --quiet -- '<research_package>/RESEARCH-CONTEXT-MASTER.md' ``. Running this command verbatim in the repo exits 0 — git reports no differences for an unmatched pathspec, with no error. Additionally, even with real paths, `git diff --quiet` compares worktree to HEAD: a master edit staged into an earlier wave's atomic commit is invisible to a later wave's check, so the command cannot verify "byte-stable against its 2026-06-11 post-consolidation baseline". The tag `v1.5-pre-phase-24` (`4b6ff913`) cannot serve as the baseline either — `RESEARCH-CONTEXT-MASTER.md` does not exist at that tag (it was created by `605c0227`, after the tag).

**Why this matters:** These commands are the named mitigations for threats T-24-PKG and T-24-BYTE. As written they assert nothing: an executor copying them verbatim gets a false green on the phase's central integrity guarantee, and a D-18 violation on an externally-forwarded package would land silently.

**Fix:** Substitute the concrete repo path (`pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/...`) in both plans, and pin the comparison to the post-consolidation baseline rather than HEAD — e.g. `git diff --quiet 605c0227 -- <full paths>`, or record per-file SHA-256 baselines in the plan text (Phase 23's own baseline practice) and compare hashes.

### P1-3: Probe Verify Gates Hard-Code Pilot Values — The `corrected` Verdict Path Fails Its Own Gate

**Found by:** adversarial (P1), feasibility (tempered). **Confidence:** 75.

**Evidence:** `24-01-PLAN.md` Task 2 verify: `... data03_gold_gap.py | grep -E '184|2749|2565'`; `24-02-PLAN.md` Task 1 verify: `... data04_footers.py | grep -E '219|1550|701'`, with acceptance criteria like "Probe stdout shows the no-footer counts 219 / 1,550 / 701 per variant".

**Why this matters:** This phase exists because documented claims were wrong before. D-08 explicitly provides a `corrected` verdict for the case where the observation deviates from the claim — but if a probe observes a deviating value, the verify gate and acceptance criteria go red on a *correct* probe. An autonomous executor iterating a red gate to green is structurally pushed toward altering the probe until the expected numbers appear — silent corruption of the very evidence the phase produces. Mitigating fact: the feasibility lens re-derived every baked-in prior against the live dataset and all hold today, so this is a latent design inversion rather than an active blocker. It still inverts the phase's epistemics and should not survive into Phase 25+ patterns.

**Fix:** Rewrite the value-coupled verify commands and acceptance criteria to assert output *shape* (labeled fields such as `no_footer[...]=`, `delta=`, presence of a verdict line) and demote the pilot numbers to prose priors, so a `corrected` verdict with divergent observed values still passes the gate.

### P1-4: WR Deferral Semantics Are Contradictory And Have No Re-Entry Path

**Found by:** adversarial (P1), coherence (P2), scope-guardian (residual). **Confidence:** 75.

**Evidence:** Three statements disagree about what an OPEN WR answer means for 24-03:

- must_haves (unconditional): "The WR-01/02/03 corrections are folded into the addendum via the channel the user chose in 24-WR-DECISIONS.md".
- governance (`24-03-PLAN.md:78`): "If any WR answer is still OPEN in 24-WR-DECISIONS.md, STOP and do not assemble that section."
- acceptance (`24-03-PLAN.md:130`): "if any WR answer is OPEN the affected section is absent and noted as blocked."

Meanwhile `24-04-PLAN.md`'s resume-signal explicitly invites deferral ('state your selection (or "defer")').

**Why this matters:** If the user defers — an option the gate offers — 24-03 either can never satisfy its must_haves (phase cannot close) or commits a partial addendum as done, and no task anywhere re-opens the addendum when the answer later arrives. Deferring (a) is worse than deferring (c): the CLM-05 split-vs-amend choice is not a "section" but threads through every CLM-05 reference, leaving "do not assemble that section" undefined.

**Fix:** Define the deferral contract once in 24-03: any OPEN WR answer blocks Task 1 entirely (phase remains open and the blocker is surfaced), rewrite the must_have into the matching conditional form, and state explicitly that an OPEN (a) blocks all CLM-05-referencing addendum rows. If partial assembly is instead the intended behavior, say so in governance and add a re-entry task/obligation artifact for the blocked sections.

## P2 Medium-Priority Findings

### P2-1: A Blocking Human Gate In Wave 1 Stalls The Fully-Autonomous Wave 2

**Evidence:** `24-04-PLAN.md` frontmatter: `wave: 1`, `autonomous: false`; objective: "it runs in Wave 1 (parallel with the probe plan 24-01) so the answers arrive before the Wave 3 addendum needs them". The GSD execute-phase workflow runs each wave in sequence, so wave 2 (24-02, which needs no user input) cannot start until *all* wave-1 plans complete — including the blocking checkpoint. **Confidence:** 75.

**Why this matters:** If the user is absent, the phase stalls after 24-01 even though 24-02 is fully autonomous. The early-answer property the plan wants is already enforced by 24-03's `depends_on: ["24-02", "24-04"]`; wave-1 placement adds only the stall.

**Fix:** Move 24-04 to wave 2 (parallel with 24-02). The `depends_on` edge already guarantees answers land before addendum assembly. Confirm whether the orchestrator honors `depends_on` across waves for deferred plans; if wave barriers are strict, document the serialization in 24-03's governance so the executor expects the wait.

### P2-2: The Recorded Re-Derivability Command Is Not Executable From Any Directory

**Evidence:** `24-01-PLAN.md:219` (Task 3): register rows record "exact probe command (`.venv/bin/python probes/dataNN_*.py`)". Probes live at `.planning/phases/24-*/probes/`; from repo root `probes/...` does not resolve, and from the phase directory `.venv/bin/python` does not resolve. The verify commands work only because they use full paths from repo root. **Confidence:** 75.

**Why this matters:** The register's D-02 guarantee — that every fact is re-derivable from its recorded command — ships commands that fail on re-run from any CWD. Acceptance criteria force this broken relative form into both the probe headers and the register.

**Fix:** Pin the convention everywhere: run from repo root with `.venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/dataNN_*.py`, with dataset paths repo-root-relative inside the probes.

### P2-3: Hardcoded Run Date Falsifies Register Provenance

**Evidence:** `24-01-PLAN.md:219` (Task 3): "… · run date (2026-06-10) · verdict". Execution happens on or after 2026-06-11. **Confidence:** 100.

**Why this matters:** A literal executor stamps the pilot session's date onto independently re-derived probe runs — the D-02 provenance metadata looks complete but is false, and the addendum cites these rows externally.

**Fix (mechanical):** Replace the literal "(2026-06-10)" with "the actual probe execution date, captured at run time".

### P2-4: Grep-Count Gates Are Satisfiable By Boilerplate

**Evidence:** `24-03-PLAN.md` Task 2 verify: `grep -c 'PENDING' … ≥ 18` — but each per-finding note line contributes two matches ("SEED_SHA PENDING -> PENDING") and the verbatim Lifecycle Rules block adds more, so a ledger seeding roughly half the D-23 inventory still passes. `24-02-PLAN.md` Task 3's `grep -c 'CLM-' ≥ 12` similarly counts prose mentions. The plan also never disambiguates whether "G1-G5" and "SCS/SASD/IPR/PSC" are one row or five/four — a plausible compact parse passes the gate while Phase 25 silently never adjudicates G2..G5. **Confidence:** 75.

**Why this matters:** Phase 25 consumes the ledger as the complete inventory. A green gate over an under-seeded ledger is an inheritance defect that surfaces phases later.

**Fix:** Enumerate the exact expected row IDs (G1, G2, G3, G4, G5; SCS, SASD, IPR, PSC as separate rows) with an exact expected row count, and anchor the gates to table rows, e.g. `grep -cE '^\| *[A-Z]' 24-ISSUE-LEDGER.md` compared against that number, and `grep -cE '^\| *CLM-' 24-VERIFIED-FACTS.md` for the register.

### P2-5: CLM-06's Owning Requirement Will Likely Be Mis-Assigned

**Evidence:** Per 24-CONTEXT.md D-04, CLM-05/06 map to DATA-03/04 (folder counts). But 24-02 Task 2 is titled "DATA-05 mass-drift probe (CLM-06 + …)" and records CLM-06 "in passing" there; 24-02 Task 3 files CLM-06 under the "DATA-04/05/06 rows" placeholder; and the explicit D-04 mapping list in `24-01-PLAN.md` Task 3 acceptance ("CLM-01/02/12→DATA-01, CLM-03→DATA-02, CLM-04→DATA-03, CLM-05→DATA-03/04") omits CLM-06 entirely. **Confidence:** 75.

**Why this matters:** An executor filling the CLM-06 register row follows the task-context signal (DATA-05) rather than D-04 (DATA-03/04), corrupting the requirement-traceability the ledger seed depends on.

**Fix:** Add the explicit D-04 note to 24-02 Task 3: "CLM-06's owning DATA requirement is DATA-03/04 per D-04 — not DATA-05, despite being recorded during the mass-drift probe."

### P2-6: STOP-Gap Branches Lack Phase-Exit Semantics

**Evidence:** Both conditional STOP branches (`24-01` Task 1 DATA-01; `24-02` Task 2 DATA-05) correctly halt only the affected verdict — "halt only the DATA-01 verdict, not the other probes" — but neither plan states whether the *plan* completes, whether the wave advances, or whether Phase 24 can close with a held verdict. The roadmap's verification protocol says "no phase exits with an in-scope finding still open". **Confidence:** 75.

**Why this matters:** The executor reaches end-of-plan with a held verdict and has no instruction for the exit state: commit and close, or hold the phase open? Either guess is a governance call the STOP protocol says the agent must not make. This interacts directly with P0-2.

**Fix:** Add one sentence to each STOP branch: the gap halts only the affected CLM verdict; the plan completes and commits with the row marked `unverified — gap OPEN`; Phase 24 closure and Phases 25+ consumption of that row are blocked until the user resolves or defers the gap (consistent with the v1.5 EDL/dependency-scoped-blocking rules).

## P3 / Low

### P3-1: `GIT_AGENT_ID` Export Specified Without A Value

All four governance blocks say "export `GIT_AGENT_ID` (currently UNSET)" but never state the value. Verified: `scripts/agent-commit` exits 1 with "set GIT_AGENT_ID to the active agent, tool, and model" when empty. The executor's first commit attempt per plan fails before it improvises from the error message. **Fix:** state a concrete value form, e.g. `export GIT_AGENT_ID="claude-code/<model-id>"`. **Confidence:** 75.

## FYI — Advisory Observations (No Decision Forced)

These were verified real but nothing breaks outright; they are listed for awareness, not action-gating:

- **D-09 "central value" is undefined for CLM-10 judging.** The plan itself records "pilot std central ≈ 61 vs claim ~59"; whether median or mode governs, and what "~" precision means numerically, flips `confirmed` vs `corrected`. An executor will silently pick a statistic — arguably the verdict-semantics invention the STOP protocol forbids. Cheapest fix: lock the statistic and rounding rule in 24-CONTEXT or alongside the WR decisions before wave 2.
- **No resume guidance for multi-task plans under the single-atomic-commit contract.** If execution dies mid-plan, the worktree holds uncommitted probes/outputs; a resumed executor cannot tell whether to trust stale captures or re-run, and the tree may carry unrelated dirt it must not sweep into the evidence commit.
- **24-02's must_have "plus prose-sweep CLM-14+ rows" reads as unconditional.** If the bounded sweep finds nothing, a literal executor may invent extension rows to satisfy it. Phrase as "any figures found get CLM-14+ IDs; zero is a valid outcome."
- **Verify commands re-run probes after stdout was captured** — divergence between the captured file and the verify-time run passes undetected.
- **The fourth variant (`brutus_hierarchical_gold_standard`) has no stated no-footer expectation** (verified: it has zero no-footer files today); the probe should record it explicitly so the addendum carries no unanchored figure.
- **DATA-06 full-population scan reads ~4.7 GB across ~15k files**; feasible on this machine, but no runtime expectation or timeout posture is stated, and DATA-05's "runtime prohibitive" sampling-fallback threshold is undefined — two executors could produce incomparable evidence records (full vs. sampled).
- **Heading anchor drift:** plans cite master §"Framed Research Questions And Locked Constraints"; the actual heading is "Framed Research Questions" with subsection "Hard Constraints — Locked v1.4 Conventions (verbatim)". Recoverable, consistent with the in-flight repointing.
- **24-02 `@`-includes `24-VERIFIED-FACTS.md`,** which exists only after 24-01 commits — safe under `depends_on`, fails if 24-02 is ever run standalone.

## What Was Checked And Held

To bound the findings above, the feasibility lens verified against the live repo: all `read_first`/`@context` paths except the retired package files exist; `.venv/bin/python` imports numpy 2.2.0; `scripts/agent-commit` exists (and enforces `GIT_AGENT_ID`); tag `v1.5-pre-phase-24` exists at `4b6ff913`; branch is `milestone/v1.5`; `16-ISSUE-LEDGER.md` exists and contains the literal "FIX_APPLIED is not closure"; `23-CLAIMS-INVENTORY.md` exists; the dataset directories and all baked-in value priors were independently re-derived and match (see Executive Summary). The plans' decision-citation discipline (D-01..D-25 cited at point of implementation) was confirmed by all four lenses.

## Coverage

| Lens | Findings emitted | Disposition after synthesis |
|---|---|---|
| coherence | 5 | merged into P0-1, P1-1, P1-4, P2-1 |
| feasibility | 10 | merged into P0-1, P1-1, P1-2, P1-3, P2-1..P2-3, P3-1, FYI |
| scope-guardian | 4 | merged into P0-1, P1-1, P2-5, P2-6 |
| adversarial | 10 | merged into P0-1, P0-2, P1-1..P1-4, P2-3, P2-4, FYI |

Cross-lens agreement: P0-1 and P1-1 were independently found by all four lenses; P1-2 was empirically verified by two lenses running the literal command. No reviewer agent failed or timed out. Findings below confidence 50 were suppressed per the review contract; one contradiction between reviewer fixes was resolved during synthesis (the byte-stability baseline cannot be the `v1.5-pre-phase-24` tag, since the consolidated master does not exist at that tag — the pin must be `605c0227` or later, or a per-file hash).

## Open Questions For The User

1. **(Feeds P0-1)** Should WR options (c)(B)/(d)="interim fix NOW" remain on the menu? If yes, which plan/task performs the master edit, and what exact D-18 waiver is authorized?
2. **(Feeds P0-2 / P2-6)** May Phase 24 close with STOP-gap-held (`unverified`) CLM rows, and what artifact records the re-entry obligation?
3. **(Feeds P1-4)** Is partial addendum assembly (some WR sections blocked) an acceptable committed outcome, or does any OPEN WR answer hold all of 24-03?
4. **(Feeds FYI)** Which statistic (median or mode) is D-09's "central value" for judging `~` claims, and what rounding rule defines "stated precision"?
