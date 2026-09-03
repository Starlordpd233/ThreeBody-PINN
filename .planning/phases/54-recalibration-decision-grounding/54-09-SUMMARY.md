---
phase: 54-recalibration-decision-grounding
plan: 09
subsystem: governance
tags: [erw, rule-19, claim-verification, ledger, re-derivation, trainex-r3, open-book]

requires:
  - phase: 54-recalibration-decision-grounding
    provides: "54-08's intake certification — RESPONSE-COUNT=2, the per-report verification burden, the four-class independence taxonomy, the stamped Rule-20 live-tree pin, the 21-path CITABLE-PATH-SET and the PIN-TREE-IDENTICAL identity proof"
  - phase: 54-recalibration-decision-grounding
    provides: "54-06's Bar G definition and selector, inherited byte-unchanged with the file list extended"
  - phase: 54-recalibration-decision-grounding
    provides: "54-01's and 54-03's Bars D, E and F"
provides:
  - "The mandatory ERW Rule-19 verification report under the v2.3 reviews tree, created before any returned claim informs a decision, a roadmap or a spec edit"
  - "The closed six-verdict vocabulary (D-13) with its per-verdict counts, derived from the ledger rather than asserted"
  - "The open-book claim ledger — 73 rows across four extracted source sets, every row carrying its source-declared evidence label beside the class it maps to"
  - "Independent re-derivation of all 56 repository-settleable rows, each with the command that re-derived it, that command's output, and content resolution and line resolution recorded as two separate findings"
  - "The NOT-RE-DERIVABLE-HERE register — 21 rows, one per unchecked verdict, each routed with what would settle it and who may authorize that, and with routing stated not to be authorization"
  - "Six candidate gap rows, proposed and not filed, carrying the STOP-protocol field schema"
  - "Three UNSUPPORTED findings the returned report does not carry, each with its own per-claim section stating its reach"
affects: ["54-10", "54-11", "54-12", "54-13", "Phase 56"]

actuals:
  tokens: 36060
  tasks: 3
  commits: 2

tech-stack:
  added: []
  patterns:
    - "Derived-not-asserted coverage: every count in the report (source rows, premise findings, distinct citations, verdicts, partition) is produced by parsing the source or the ledger, and the gate re-derives the load-bearing ones independently"
    - "Split verdicts for claims spanning what this repository can settle and what it cannot, with each half named in the cell and each split combination carried as its own bucket in the count table"
    - "Content resolution and line resolution recorded as two separate findings per row, so a true claim at a moved line and a wrong claim at a right line are distinguishable rather than collapsed"
    - "Explicit NEGATIVE-SEARCH-EMPTY markers with the search scope stated, because an empty result and a mistyped pattern are indistinguishable in silence"
    - "Escaped-pipe-aware cell parsing for any count derived from a markdown ledger; commands carrying backticks or pipes recorded in a fenced AWKWARD-COMMANDS block instead of a cell"

key-files:
  created:
    - "docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/2026-09-02-trainex-r3-rule19-claim-verification.md"
  modified: []

key-decisions:
  - "The uncommitted 2026-09-02 partial draft was adopted rather than superseded, because its spine matched the plan's required structure — but not one of its verdicts was inherited: every row was re-derived independently against the tree, which produced five corrections"
  - "The split-verdict convention the plan states for a claim spanning this repository and an outside source is widened, deliberately and on the record, to cover the source report's own clean-room computation and any state only a run would produce — all three are outside this repository's reach in the same sense"
  - "PC-8d is recorded UNSUPPORTED: .planning/REQUIREMENTS.md carries three of the four stale spec anchors the claim attributes to it, not four; the fourth appears nowhere in that file"
  - "PC-5b and D-2b are recorded UNSUPPORTED: the cited line is the L-BFGS single fixed draw, so the per-step re-draw the claim asserts holds for the Adam loop and not for the L-BFGS phase"
  - "PC-9a is narrowed on evidence class rather than on wording: the quotation is faithful but appears in none of the three attachments, so under the report's own label definitions its class is repository-derived and not package-derived — which changes what agreement with the other report would mean under D-14"
  - "PC-1d is narrowed rather than sharpened: the implemented LayerNorm carries a stabiliser, so its positive scale-invariance is exact only in the limit and accurate elsewhere, which is a weaker premise than the finding's wording"
  - "PC-7a is split: exact scale-invariance is confirmed as an elementary identity; bit-identity does not follow from it and generically fails, so it is routed rather than inherited from the weaker statement"
  - "No STOP-protocol gap was recorded and none was warranted — nothing in this pass required deciding anything about the recalibration"

patterns-established:
  - "Re-derive-then-compare on an inherited draft: a pre-existing artifact may supply structure, and none of its verdicts may be inherited; the corrections are the evidence the re-derivation was real"
  - "A sharper finding and a narrower finding in the same row resolve to the narrower verdict, with the sharpening recorded in the note — the verdict states what the wording can carry, not the best available fact"

requirements-completed: []
# ERW-02 is this plan's declared requirement and is deliberately NOT marked complete.
# It stays PARTIALLY DISCHARGED: the closed-book half of the Rule-19 verification,
# the premise adjudication, the Rule-12 consolidation and owner checkpoint ② are all
# outstanding, and 54-10..54-13 also declare it. .planning/REQUIREMENTS.md was not
# edited — the plan prohibits it and Bar E enforces the prohibition.

coverage:
  - id: D1
    description: "The mandatory ERW Rule-19 verification report exists under the v2.3 reviews tree for this phase, date-prefixed, with a complete schema-valid docs frontmatter block"
    requirement: "ERW-02"
    verification:
      - kind: other
        ref: "Task 1 <automated> gate — directory, date-prefixed filename with the exact slug, and every required frontmatter key with an allowed value; printed LEDGER-BUILT REGISTER=15 FINDINGS=9"
        status: pass
    human_judgment: false
  - id: D2
    description: "The closed six-verdict vocabulary is present in full with per-verdict counts derived from the ledger by parsing, and every ledger row carries a verdict from it"
    requirement: "ERW-02"
    verification:
      - kind: other
        ref: "Task 2 <automated> gate — all six literals required present; every identifier-matching row required to carry one; printed REDERIVATION-COMPLETE ROWS=51 UNVERDICTED=0"
        status: pass
    human_judgment: false
  - id: D3
    description: "The open-book claim ledger carries 73 rows whose coverage of the source register, the source premise findings and the source's distinct citations is derived from the source and re-confirmed independently by the gate"
    requirement: "ERW-02"
    verification:
      - kind: other
        ref: "Task 1 gate re-extracts the register row count and every premise-finding identifier from the source report itself and fails unless the ledger carries a row for each; both extractions required non-empty (15 and 9); distinct-citation coverage 18 with 0 uncovered"
        status: pass
    human_judgment: false
  - id: D4
    description: "Every repository-settleable row is re-derived independently against the pinned tree with the command that re-derived it and that command's output recorded, and with content resolution and line resolution recorded as two separate findings"
    requirement: "ERW-02"
    verification:
      - kind: other
        ref: "56 P-A rows, each carrying a non-empty command cell and a non-empty output cell, enforced structurally by the whole-file empty-cell scan; identity proof re-run against the current tip as PIN-TREE-IDENTICAL before any re-derivation"
        status: pass
    human_judgment: true
    rationale: "The gate proves every row has a command, an output and a verdict, and the empty-cell scan proves no cell was left blank. Whether each verdict is the right verdict for its claim is a judgement about evidence, and it is the judgement the wave-4 premise adjudication and the owner will exercise against these rows."
  - id: D5
    description: "The not-re-derivable-here register routes all 21 unchecked verdicts, each with why its class admits no in-repo re-derivation, what would settle it, and who may authorize that; routing is stated not to be authorization"
    requirement: "ERW-02"
    verification:
      - kind: other
        ref: "Task 3 <automated> gate — routing register required present and its row count required at least the not-verifiable verdict count; printed TRIAGE-COMPLETE ROUTED=14 ROUTING-ROWS=45. Independent one-to-one check: 21 ledger rows carrying NOT-VERIFIABLE-HERE, 21 routing rows, empty symmetric difference"
        status: pass
    human_judgment: false
  - id: D6
    description: "Six candidate gap rows proposed and not filed, with both gap registers and the ruling record byte-unchanged and the routing decision stated to belong to the wave-4 plan"
    requirement: "ERW-02"
    verification:
      - kind: other
        ref: "Task 3 gate — CANDIDATE-GAP-ROWS-PROPOSED marker required present; git diff HEAD --stat over 54-RULING.md and both registers empty"
        status: pass
    human_judgment: false
  - id: D7
    description: "The standing bars and the widened round-root manifest check recorded with commands and outputs inside the report's own verification-hygiene section"
    requirement: "ERW-02"
    verification:
      - kind: other
        ref: "Bar D empty in both anchorings; Bar E empty; Bar F = 0; Bar G1 region 0 with empty remainder, G2 empty, G3 empty, verdict literal BAR-G-CLEAN-NO-SURFACE-NAMED; fence counts 10 8 8 8 10 10 all even, retained stream 4233 lines; Check R1-w MANIFEST-OK-W"
        status: pass
    human_judgment: false
  - id: D8
    description: "Phase 54 does not close: GAP-54-01 OPEN in both registers, the ruling record byte-unchanged, no consolidated document, the attachments and both returned reports untouched"
    requirement: "ERW-02"
    verification:
      - kind: other
        ref: "GAP-54-01 greps OPEN in 54-GAPS.md:42 and at two lines of v2.3-GAPS.md; git diff HEAD --stat over the ruling record, both registers, the three attachments and the results directory all empty; test ! -f printed CONSOLIDATION-ABSENT"
        status: pass
    human_judgment: false

duration: 95min
completed: 2026-09-03
status: complete
---

# Phase 54 Plan 09: Rule-19 Open-Book Claim Verification Summary

**The mandatory ERW Rule-19 verification report now exists with a 73-row open-book claim ledger whose coverage is derived from the returned report rather than asserted; all 56 repository-settleable rows are re-derived independently against the pinned tree with commands and outputs recorded, producing 43 confirmations, 5 sharpenings, 7 narrowings, 3 unsupported findings and no refutation; and all 21 unchecked rows are routed with what would settle each and who may authorize it.**

## Performance

- **Duration:** ~95 min
- **Completed:** 2026-09-03T16:02:41+08:00
- **Tasks:** 3 of 3
- **Files created:** 1 (988 lines, 145,744 bytes) · **Files modified:** 0

## Accomplishments

- **The Rule-19 report exists, and it exists before anything consumes a claim from it.** That ordering is the rule's whole point: everything downstream in this pass — the premise adjudication, the consolidation, and the candidate sheet the owner reads at checkpoint ② — draws from this file, and nothing may draw from it before a verdict exists.
- **The ledger's coverage is derived, not claimed.** 73 rows across four extracted source sets: the returned report's 15 register rows carried through with their native identifiers; its 9 premise-challenge findings split into 36 separately checkable sub-rows under a split rule stated once and applied uniformly; its 7 departures rows split into their source side and their project side, 15 rows; and 7 supplementary rows so that every remaining distinct repository citation lands somewhere. **18 distinct cited paths, 0 appearing in no ledger row.**
- **Every repository-settleable claim was re-derived independently.** Not one verdict was inherited from the pre-existing draft. Each row records the command that re-derived it, that command's output, and — separately — whether the claim resolves by content and whether the cited line still carries that content.
- **Three `UNSUPPORTED` findings the returned report does not carry.** The cited stale-anchor set in `.planning/REQUIREMENTS.md` is three anchors and not four; the per-step collocation re-draw the report asserts without qualification holds for the Adam loop and not for the L-BFGS phase, and the line it cites is the fixed-draw path. Each has its own section stating what the contradiction does and does not reach. **No claim was refuted**, which is recorded as a finding rather than as an absence.
- **Five sharpenings that strengthen the record.** The bundle is byte-faithful across **all ten** verbatim excerpts, not the three the report spot-checked; the source method is cited **nowhere in the specification**, not merely nowhere in its reference list; the clamp floor actually applied is the dtype-rounded, once-advanced value and the logged minimum weight matches it to within one unit in the last place; and the double-precision result holds on this project's own retained evidence rather than on a re-implementation of it.
- **Twenty-one unchecked rows, every one routed and none quietly accepted.** Nine rest on the report's own clean-room computation — which the report itself says carries the Rule-19 obligation — eleven on published literature this repository cannot reach, and one on a state only a run would produce. Each row names what would settle it and who may authorize that, and the register states in its own text that **routing is not authorization** and that an unchecked claim is unchecked.

## Ledger statistics

| Quantity | Value | How it was obtained |
|---|---|---|
| Ledger rows | 73 | extraction from four source sets, counted by parsing the ledger |
| Source register rows covered | 15 of 15 | gate re-extracts the count from the source report |
| Source premise findings covered | 9 of 9, as 36 sub-rows | gate greps each finding identifier in the report |
| Departures rows covered | 7 of 7, as 15 sub-rows | source-side / project-side split |
| Distinct repository citations | 18 | the three intake extraction passes re-run against the open-book report |
| Citations appearing in no ledger row | 0 | coverage table, one row per distinct path |
| Partition declared / executed | 56 / 15 / 2, total 73 — reconciles exactly | parsed with escaped-pipe-aware cell splitting |
| Per-claim sections | 20 | one for every row that is not a plain confirmation |
| Candidate gap rows | 6 | proposed, not filed |

**Verdicts — 73 rows, 79 occurrences counting each half of a split row:**

| Verdict | Occurrences |
|---|---|
| `CONFIRMED` | 43 |
| `CONFIRMED-SHARPER` | 5 |
| `CONFIRMED-NARROWER` | 7 |
| `REFUTED` | 0 |
| `UNSUPPORTED` | 3 |
| `NOT-VERIFIABLE-HERE` | 21 |

## Unsupported findings, by identifier, with their reach

- **`PC-8d`** — the claim attributes four stale spec anchors to `.planning/REQUIREMENTS.md` at two named lines; that file carries three, and the fourth appears nowhere in it. **Reaches:** what a later anchor-repair pass must look for, since a pass told to fix "the four anchors there" will find three. **Does not reach:** the three anchors that *are* cited there, each of which is confirmed stale with the replacement the claim gives — which is the part a Phase 56 amendment depends on.
- **`PC-5b`** — the claim asserts a per-step collocation re-draw and cites a line that is the single fixed draw held for an L-BFGS segment. **Reaches:** the phase-dependence of the re-draw, and the numeral the claim supplies, which is fixed at no cited line. **Does not reach:** the structural argument about prefix-sum length, which does not depend on it.
- **`D-2b`** — the same citation, used in the departures table to support a different consequence about front persistence and a guard's high-water mark. **Reaches:** the need to state that departure per optimizer phase, since its premise does not hold where the collocation set is fixed. **Does not reach:** the other six departures, each confirmed at its own locus.

## Routed set, with its targets

| Kind | Rows | Routed to |
|---|---|---|
| The report's own clean-room computation | `R-04`, `R-05`, `R-09` (analytic half), `R-10`, `R-14`, `PC-1e`, `PC-1f` (capacity half), `PC-7a` (bit-identity half), `PC-9c` | the characterization probe this milestone lands as committed tooling in its own phase, run on this project's own model — which the returned report itself lists among its owner-gated proposals, transcribed and attributed, never adopted |
| Published literature | `R-01`, `R-02`, `R-03` (published halves), `PC-5c`, `D-1a`, `D-2a`, `D-3a`, `D-4a`, `D-5a`, `D-6a`, `D-7a` | a reader following the citation, edition and section the report names; where the repository carries a vendored implementation bearing on the same point, that is verified separately and in-repository with its own verdict |
| A state only a run would produce | `PC-6c` | the report's own training-involving owner-gated proposal; this milestone's scope rows make such a run an owner decision |

**Routing is not authorization**, stated in the register's own text for every row routed to a probe run or an owner-gated proposal.

## Candidate gap rows proposed

Six, listed in the report under `CANDIDATE-GAP-ROWS-PROPOSED` with the STOP-protocol field schema's required fields, **not written into either register** — the routing decision belongs to the wave-4 plan.

1. The fourth stale spec anchor is not where the round's own sweep implies it is (from `PC-8d`) — operational coordination, MEDIUM.
2. A repository-read quotation carries a package-derived evidence label (from `PC-9a`) — process-artifact schema, MEDIUM.
3. The per-step collocation re-draw does not hold in both optimizer phases (from `PC-5b`/`D-2b`) — semantic, HIGH.
4. The normalization mechanism's invariance is approximate as implemented (from `PC-1d`) — semantic, MEDIUM.
5. A headline derived figure depends on an edge the source stipulates (from `R-06`) — semantic, MEDIUM.
6. A codification item is larger than the package's own row implies (from `PC-4a`) — operational coordination, LOW.

## Task Commits

Per the plan's `<commit_protocol>`, this plan produces **one** commit for the work at the end of Task 3 rather than one per task, followed by the summary and state commits.

1. **Tasks 1–3 (report creation and ledger, independent re-derivation, triage and bars)** — `22c863ee` `verify(54-09): record the rule-19 open-book claim verification`, made through `scripts/agent-commit` with `GIT_AGENT_ID` and `GIT_AGENT_OWNED_PATHS` set and one explicit path staged.
2. **This summary** — the `docs(54-09)` commit on `milestone/v2.3`, same discipline.

## Files Created/Modified

- `docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/2026-09-02-trainex-r3-rule19-claim-verification.md` — **created.** 988 lines. Why-this-exists, scope with per-source extraction counts, method with the identity proof, a coverage boundary for four paths outside the certified set, the six-verdict closed vocabulary, how the ledger was built, path abbreviations, the ledger in four groups, `AWKWARD-COMMANDS`, `VERDICT-COUNTS`, `CITATION-COVERAGE`, twenty per-claim sections, `NOT-RE-DERIVABLE-HERE-REGISTER`, `CANDIDATE-GAP-ROWS-PROPOSED`, `PARTITION-EXECUTED`, the closing establishes / does-not-establish / what-remains sections, and `VERIFICATION-HYGIENE`.
- Nothing else was written. The three uploaded attachments, both returned reports, every framework spec, everything under `pinn/`, `REQUIREMENTS.md`, `ROADMAP.md`, `54-RULING.md` and both gap registers are byte-unchanged.

## Gate and bar results, verbatim

| Gate / bar | Verdict as printed |
|---|---|
| Task 1 `<automated>` | `LEDGER-BUILT REGISTER=15 FINDINGS=9` |
| Task 2 `<automated>` | `REDERIVATION-COMPLETE ROWS=51 UNVERDICTED=0` |
| Task 3 `<automated>` | `TRIAGE-COMPLETE ROUTED=14 ROUTING-ROWS=45` |
| Plan gate 1 — exactly one report matching the date pattern | `1` |
| Plan gate 2 — untracked under `docs/work/reviews/milestone_v2.3/` after the commit | `0` |
| Plan gate 3 — anchor gap `OPEN` in both registers | `54-GAPS.md:42` `**Status:** OPEN`; `v2.3-GAPS.md` two matching lines |
| Plan gate 4 — consolidation absent | `CONSOLIDATION-ABSENT` |
| Check R1-w — widened round-root manifest | `MANIFEST-OK-W` |
| Bar D — canonical index-anchored, and `HEAD`-anchored | empty / empty |
| Bar E — canonical two-path, `HEAD`-anchored | empty |
| Bar F — cost vocabulary over the ruling record | `0` (equal to the number `54-08` recorded) |
| Bar G1 — region cardinality and remainder | `G1-REGION=0`; remainder empty |
| Bar G2 / Bar G3 | empty / empty |
| Bar G verdict literal | `BAR-G-CLEAN-NO-SURFACE-NAMED` |
| Bar G preprocessing sanity | fence counts 10, 8, 8, 8, 10, 10 — all even; retained stream 4233 lines |
| Identity proof re-run against the current tip | `PIN-TREE-IDENTICAL`, `CPN=21 ARGS=21`, both sentinels found |
| Ruling record, both registers, attachments, returned reports vs `HEAD` | all empty |

**Bar G's literal and region are unchanged from what `54-08` recorded**, which is the expected result and is recorded as such: this plan edited no plan file, and the retained stream is the same 4233 lines.

## Prohibition discharge

Every prohibition in the plan's frontmatter carried `status: flagged-unverified`. Each verification was run and its result recorded.

| Prohibition | Verification run | Result |
|---|---|---|
| No claim is carried forward without a verdict, and no verdict is invented outside the closed vocabulary | Task 2 gate re-derives the row set and matches every verdict cell against the six literals | `ROWS=51 UNVERDICTED=0`. Across the whole 73-row ledger, every cell parses to one or two of the six and nothing else. The vocabulary was **not** widened; only the composition of the six was extended to split rows, and the widening is recorded in the report |
| No returned report and no uploaded attachment is edited; a claim that fails is recorded as failing and the report stays as its author wrote it | `git diff HEAD --stat` over the two returned reports and the three uploaded attachments | Empty for all five. Three claims are recorded `UNSUPPORTED` in full, each with its own section, none softened and none omitted |
| The agent names no candidate value for any decision surface and marks none of them (SCOPE-34) | Bar G over this pass's six plan files with the selector byte-unchanged; manual structural read over the verification report with an explicit verdict | `BAR-G-CLEAN-NO-SURFACE-NAMED` with `G1-REGION=0`, recorded as the literal the gate prints. Manual read verdict recorded inside the report: it names no candidate value, reproduces no options menu and no marked default, ranks nothing, and marks no surface — and it states that where a threshold it verifies sits numerically near a value some menu also carries, recording the threshold endorses nothing |
| No framework-spec file, no file under `pinn/`, and no locked planning source is edited; verification is read-only by construction | Bar D in both anchorings, Bar E, and `git status --porcelain` over the 21-path citable set at task close | All empty. No command with a side effect on the working tree was run; no training was started and no evaluation was invoked |
| Phase 54 does not close, the anchor gap is not touched, and no consolidated document is created | `GAP-54-01` grep in both registers; `git diff HEAD --stat` over the ruling record and both registers; consolidation-absent test | `OPEN` in both; all three files byte-unchanged; `CONSOLIDATION-ABSENT` |

## Decisions Made

- **The uncommitted 2026-09-02 partial draft was adopted, and none of its verdicts was.** Its spine matched what the plan requires — frontmatter, scope, method, the closed vocabulary, the split rule, the keying rule, and a partially built ledger — so discarding it would have thrown away correct structural work. The plan's independence requirement is absolute, so every row was re-derived here against the tree with its own command. **That produced five corrections**, which are the evidence the re-derivation was real rather than a rubber stamp: one arithmetic output in the draft was simply wrong; one verdict was sharpened where the evidence narrows it; and three rows the draft left unfilled resolved to two narrowings and one unsupported finding.
- **The split-verdict convention was widened deliberately and on the record.** The plan states it for a claim spanning this repository and an outside source. It is applied here to three kinds of outside — published literature, the report's own clean-room computation, and a state only a run would produce — because all three are outside this repository's reach in the same sense, and because the plan's own must-haves require clean-room-grounded claims never to be silently accepted or silently dropped. No seventh verdict was introduced; the count table carries each split combination as its own named bucket.
- **A row carrying both a sharpening and a narrowing takes the narrower verdict.** `PC-1d` re-derives more structural detail than the finding claims *and* qualifies its central clause. The verdict states what the claim's wording can carry; the sharpening lives in the note. Recording it the other way would let a narrowing disappear behind a stronger-sounding label.
- **Commands that cannot survive a table cell were moved to a fenced block**, following the convention `54-INTAKE.md` set for the same reason, rather than being reworded until they fit. A reworded command is a different check.
- **Four paths outside the certified 21-path set were read, and their identity was established here rather than assumed.** Three are objects the report cites in prose rather than by path; the fourth is a corroborating locus used only as corroboration. All 18 paths the report cites by path are inside the certified set.

## Deviations from Plan

### 1. [Plan `<commit_protocol>` over the orchestrator's generic instruction] One work commit, not one per task

- **The orchestrator's dispatch** asked for each task to be committed atomically.
- **The plan's `<commit_protocol>` states** "One commit at the end of Task 3, through `scripts/agent-commit`", and Task 3's acceptance criteria repeat "**One commit, through `scripts/agent-commit`**".
- **Resolution:** the plan wins, and the reason is substantive rather than formal. Tasks 1 and 2 write the same file in sequence, and a Task-1 commit would place a ledger whose verdict cells read "pending" into the permanent record of a governance milestone. The plan's ordering exists so that no intermediate, unverdicted ledger is ever committed. Committing three times would also fail Task 3's own acceptance criterion on a literal read.
- **Effect:** the work landed in `22c863ee`; the summary and the state advance are separate commits, which is what lets the summary record the work commit's hash at all.

### 2. [Plan `<commit_protocol>` over the orchestrator's suggested type] `verify(54-09)` rather than `evidence(54)`

- The orchestrator suggested `evidence(54): …` for the report commit. The plan specifies `verify(54-09): <lowercase imperative subject>`, and `docs/README.md` independently prescribes `verify(<scope>)` for review reports. Both `verify` and the task scope `54-09` are allowed by the repository's commit-message policy. The plan's form was used.

### 3. [Orchestrator instruction, recorded] `.planning/ROADMAP.md` was not edited and `.planning/REQUIREMENTS.md` was not updated

- The orchestrator's dispatch explicitly instructs that `ROADMAP.md` is not to be edited in this plan, continuing what `54-08` established for the post-delivery batch, and the plan's Bar E requires the canonical two-path diff to be **empty** at close. Both files are byte-unchanged and Bar E is recorded empty.
- `ERW-02` is correctly left outstanding: it is partially discharged and four further plans in this pass also declare it.
- **Routing:** whoever advances the phase bookkeeping should update the ROADMAP Phase 54 block after this plan's commits, outside this plan's authority.

### 4. [Plan `<state_and_roadmap>` instruction] `STATE.md` was hand-edited rather than advanced by tooling

- The orchestrator records that the `gsd-tools` mutating verbs emit malformed output in this checkout and instructs that `STATE.md` be maintained by hand, as `54-08` did. No mutating `gsd-tools` verb was run. The edit is minimal — the stopped-at line, the two dates, the activity description and the plan counter with its recomputed percentage — and lands in its own commit.

### 5. [Plan `<commit_protocol>` vs generic executor guard] The worktree per-agent-branch assertion was not applied

- The generic executor commit protocol asserts that a worktree `HEAD` must sit on an `agent-*` / `worktree-agent-*` branch. This worktree is the user's own milestone worktree on `milestone/v2.3`, and the orchestrator dispatched this plan explicitly as a **sequential** executor on it with worktree isolation off. Applying the per-agent-branch allow-list here would have produced a false `FATAL` on a correct configuration. Identical to `54-08`'s deviation 3.
- No destructive git operation was run: no `git clean`, no `git stash`, no reset, no force-push, no `--no-verify`, no blanket staging. The pre-existing user-owned working-tree changes were neither staged nor touched.

---

**Total deviations:** 5 — four precedence resolutions recorded rather than taken silently, one instruction acknowledgement. **Impact on plan:** none on scope. The plan's three tasks, all five prohibitions, all four standing bars, Check R1-w and all four of its own gates are discharged as written.

## Issues Encountered

- **An inherited draft is a hazard as well as an asset.** The 2026-09-02 partial carried a verdict cell whose recorded arithmetic output did not match the command beside it, and a verdict that the evidence narrows rather than sharpens. Both would have survived a reviewing read and neither survived re-derivation. Recorded because the plan's independence requirement is exactly the control that caught them, and because a later pass inheriting *this* file owes it the same treatment.
- **A count parsed from a markdown ledger is wrong by default.** The first parser split cells on every pipe and mis-columned every row whose command cell carried an escaped pipe, producing a plausible-looking verdict tally that was quietly wrong. The corrected parser splits on unescaped pipes only, and the report says so where it reports its counts.
- **No STOP-protocol gap was recorded, and none was warranted.** Every question this pass had to settle was answered by re-derivable evidence — file contents at the pinned tree, the retained run's primary log, closed-form arithmetic, or an explicitly recorded reading of a plan instruction. Nothing required deciding anything about the recalibration: no value, form, rescaling, bound, or which surface to change. The six questions the pass surfaced are recorded as **candidate** gap rows inside the report, proposed and not filed, because filing them is the wave-4 plan's authority. `54-GAPS.md` and `.planning/milestones/v2.3-GAPS.md` are byte-unchanged and `GAP-54-01` remains `OPEN`.

## User Setup Required

None — no external service configuration is required.

## Next Phase Readiness

**Ready.** `54-10` follows in wave 3 and extends **this same file** (D-12):

- The closed-book report's **anchor triage** — the three-way provenance question derived at `54-INTAKE.md` under `BURDEN-CLOSED-BOOK` — plus content resolution of each anchor against the pinned tree. `LEDGER-PREFIX-CONTRACT`'s `CB-NN` assignment is the identifier scheme its verdict gate greps for.
- The **cross-report independence adjudication** against the four-class taxonomy. Two rows in this half bear on it directly: `PC-9a`, whose evidence class the re-derivation moves, and the whole `CLASS-REPOSITORY-DERIVED` set, where agreement is bundle-fidelity evidence rather than a second reading.
- The six-verdict vocabulary, the split convention and the empty-cell and escaped-pipe conventions are fixed here and are inherited rather than re-derived.

**Phase 54 does not close.** `GAP-54-01` is `OPEN` in both registers, `54-RULING.md`'s checkpoint ② is unfilled and byte-unchanged, Phase 56 stays closed, no consolidated document exists, and no premise is adjudicated.

**One item for whoever advances the phase bookkeeping:** the ROADMAP Phase 54 block still carries its pre-`54-08` counts, because this plan is forbidden from editing `ROADMAP.md` (deviation 3 above).

## Self-Check: PASSED

- `docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/2026-09-02-trainex-r3-rule19-claim-verification.md` — FOUND (988 lines, 145,744 bytes), tracked, `0` untracked files remaining under `docs/work/reviews/milestone_v2.3/`.
- Commit `22c863ee` — FOUND on `milestone/v2.3`, one file changed, 988 insertions, no deletions.
- All three task `<automated>` gates re-run over the completed file after Task 3: all pass.
- All four standing bars, Check R1-w, the re-run identity proof and all four of the plan's own verification gates: all pass, outputs recorded above and inside the report.
- Independent one-to-one check of the routing register against the ledger: 21 and 21, empty symmetric difference.
- Partition declared 56/15/2 and executed 56/15/2, summing to the 73-row ledger.

---
*Phase: 54-recalibration-decision-grounding*
*Completed: 2026-09-03*
