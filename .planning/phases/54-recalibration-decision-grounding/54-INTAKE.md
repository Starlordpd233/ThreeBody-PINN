---
phase: 54
plan: 08
status: active
created: 2026-09-02
---

# 54-INTAKE — certification of the two returned trainex-r3 research reports at intake

## Standing

This record certifies the returned reports **at intake**. It assigns no verdict to any
claim either report makes, adjudicates no premise challenge, consolidates nothing, and
writes nothing to the ruling record. Those belong to later plans in this pass, in that
order.

It names no candidate value for any decision surface, marks none of them, and attaches
no weight to the order in which the reports present them. Where a report's own contracted
output is a marked default or a ranked menu, this record counts it and locates it; it
never reproduces it.

Quoted rule text is from `docs/runbooks/external-research/2026-06-11-external-research-workflow.md`.

`RESPONSE-COUNT=2` — derived at check I1 below, not assumed. `54-07` declined to author
this pass partly because this number was unknown; every consolidation join point
downstream is shaped by it.

## Table-cell pipe convention

Every literal pipe character inside a recorded command in this file is written escaped as
`\|`. This is not cosmetic, and it is the same convention `54-06-PLAN.md` set for
`54-RECONCILIATION.md` and `54-07-PLAN.md` restated for `54-HANDOFF-READINESS.md`. The
empty-cell gate splits every markdown table row on the pipe character, so an unescaped
shell disjunction operator (check I2) or an unescaped single pipe inside a recorded
pipeline yields an empty field and reports `EMPTY-CELL` on a correctly filled row, or
silently shifts every cell after it. The escape leaves a backslash on the left of each
split, so both fragments stay non-empty and the scan sees a filled cell. The repair is
always the escape and never deleting the command from the cell. This convention governs
every table in this file.

Preconditions asserted before the battery ran: the six post-delivery plan files
`54-08` … `54-13` are tracked with no uncommitted delta against `HEAD`;
`git diff HEAD --stat -- .planning/REQUIREMENTS.md .planning/ROADMAP.md` is empty; the
results directory exists and every file in it matches the ERW Rule-12 pattern.

## Intake certification table (I1–I8)

Path abbreviations used in the command cells: `R3` is
`pinn_instruction/markdown_conversion/framework-specs/trainex-r3`; `R` is
`$R3/research_results`; `CB` is `$R/chatgpt-resolution.md`; `OB` is
`$R/claude-resolution.md`.

| Check | ERW rule | Command | Output | Verdict | What a failing run looks like |
|---|---|---|---|---|---|
| I1 | Rule 12: results land as `<agent>-resolution.md` under `research_results/`. The response count is derived here, never assumed. | `ls -1 "$R" \| LC_ALL=C sort`; `ls -1 "$R" \| wc -l`; `ls -1 "$R" \| grep -cE '^[a-z0-9]+-resolution\.md$'`; `wc -c -l "$R"/*.md` | Listing: `chatgpt-resolution.md`, `claude-resolution.md`. Total files 2; files matching the Rule-12 pattern 2; the two counts agree, so the directory holds nothing else. Byte and line counts: `chatgpt-resolution.md` 57500 bytes / 627 lines; `claude-resolution.md` 70102 bytes / 916 lines. Derived `RESPONSE-COUNT=2`. | PASS — two responding agents, both landed under the convention | A file under `research_results/` that does not match the pattern makes the two counts disagree. A count of 1 or 3 changes the entire shape of this pass and must be discovered here rather than assumed away. Renaming a non-conforming file into conformance is forbidden |
| I2 | Rule 14: "The package directory is the durable record: keep master, prompt, delivery note, snapshots, results, and resolution together under the round root." | Check R1 widened once: `A=$(find "$R3" -type f \| LC_ALL=C sort)`; `E=$(printf '%s\n' <the seven authorized paths> \| LC_ALL=C sort)`; `[ "$A" = "$E" ] && echo MANIFEST-OK-W \|\| echo MANIFEST-FAIL-W` | `MANIFEST-OK-W`. Widened expected set (7): `$R3/DELIVERY-NOTE.md`; `$R3/research_package/RESEARCH-AGENT-PROMPT.md`; `$R3/research_package/RESEARCH-CONTEXT-MASTER.md`; `$R3/research_package/v2.2-closure-evidence-bundle.md`; `$R3/research_results/chatgpt-resolution.md`; `$R3/research_results/claude-resolution.md`; `$R3/specs/framework-specs-bundle.md`. The earlier authorized form (`54-06`, re-run by `54-07`) was the same set minus the two `research_results/` entries and printed `MANIFEST-OK` while `research_results/` did not exist | PASS — and this widening is **this pass's first authorized change to that manifest** | `MANIFEST-FAIL-W`. String equality, not cardinality: an eighth file fails, a missing file fails, and a one-for-one substitution preserving the count also fails. `trainex-r3-resolution-doc.md` appearing here would be a failure, not a pass — the plan that creates it widens the manifest again, once, and says so |
| I3 | Rule 5: snapshots are pinned to a commit hash in the master frontmatter — the attachment baseline pin. | `for f in $(find "$R3" -type f \| LC_ALL=C sort); do grep -oE '\b[0-9a-f]{40}\b' "$f" \| LC_ALL=C sort -u; done` | Each of the five package files carries exactly **one distinct** forty-hexadecimal string and it is `6a4f9b9902ab62e1d1f57bba0e521f38120c416d` in all five, compared at full length. Both returned reports independently carry the same value as their only forty-hexadecimal string (`claude-resolution.md:6` frontmatter `package_baseline`; `chatgpt-resolution.md:13` in prose) | PASS — full-length equality across the five package files; the two reports corroborate that they read the same pinned attachments | A second distinct forty-hexadecimal string in a package file; a prefix agreement recorded as a pass. A prefix match is a **non-result** here and is never treated as agreement |
| I4 | Rule 5 and D-15: nothing learned after upload is written back into a file the external agents already read. | `git diff HEAD --stat -- "$R3/research_package/RESEARCH-CONTEXT-MASTER.md" "$R3/specs/framework-specs-bundle.md" "$R3/research_package/v2.2-closure-evidence-bundle.md"`; and `git log -1 --format='%H %ad %s' --date=short -- <each path>` | `git diff HEAD --stat` over the three uploaded paths is **empty**. Last-touching commits: `RESEARCH-CONTEXT-MASTER.md` → `b8617a20b499d63958744f9f39ef8fbe911c9cfb` 2026-08-28 `docs(54-06): reconcile the 2026-08-21 erw-02 assembly pass`; `specs/framework-specs-bundle.md` → `11b4e0c12529efe993143c7dcd9eb08df9a213fd` 2026-08-21; `research_package/v2.2-closure-evidence-bundle.md` → `11b4e0c1…` 2026-08-21. Engagement 2026-08-30 (I-note 2). Readiness certification `efe8e590…` 2026-08-28T13:18:33 | PASS under the engagement reading, with the divergent reading recorded rather than suppressed — see **I4 reading note** below | A non-empty `git diff HEAD --stat` over any uploaded path is a D-15 violation and makes the baseline pin describe a file nobody saw. A last-touching commit dated after the engagement is the same violation seen from the history side |
| I5 | Rule 7, the build-design output contract, asserted **per report separately**. Required element count **10**, the same count `54-07` H6 used for the package side. | Content match of the ten contracted elements against `grep -nE '^#{1,4} '` headings and the marked bold/blockquote lines in each report; heading line recorded per element | **Open-book report: 10/10 present.** **Closed-book report: 10/10 present.** Per-element heading lines are in the **I5 element table** below. Absent elements: none in either report. Menu option counts are within the contracted range of two to four in every menu of both reports | PASS — 10/10 in each report, counted separately | An element absent from one report and present in the other, silently averaged into a single verdict. An element recorded present without the heading line that makes the row re-derivable. A report missing an element is **recorded as returning an incomplete contract and carried forward** — never repaired, never edited |
| I6 | Rule 7 and Rule 16: the evidence labels an agent uses follow from the access mode it ran under, so each report's label set is extracted in that report's own words. | `grep -oF '[<label>]' <report> \| wc -l` per declared label, plus the declaration line for each report | Open-book report declares four labels at `claude-resolution.md:35-38`; exact-token occurrences `[PKG]` 7, `[REPO]` 40, `[LIT]` 13, `[OWN]` 53, plus `[r2-QUAL]` 1; counting split-bracket citation forms as well gives `[PKG` 9 and `[REPO` 42. Closed-book report declares three labels at `chatgpt-resolution.md:9-11`; occurrences `[P]` 21, `[L]` 7, `[A]` 59, and the compound forms `[P/A]` 8, `[A/P]` 5, `[L/A]` 2, `[r2-QUAL]` 2 | PASS — both vocabularies extracted with line citations and per-label counts; **neither is translated into the other** | Any row that maps one report's label onto the other's without the report stating the mapping itself. The two vocabularies partition the evidence differently and flattening them is exactly how a package-derived assertion comes to be read as a repository-verified one |
| I7 | Rule 7: a claims-and-uncertainty register is a contracted element; Rule 19 verification is performed per register row, so the rows need stable references. | `grep -cE '^\| R-[0-9]+ \|' "$OB"`; `grep -nE '^#{1,4} ' "$CB"` to bound the register section, then `sed -n '604,616p' "$CB" \| wc -l` over the data rows the header at `:602` and the separator at `:603` delimit | Open-book register `claude-resolution.md:860`: **15** rows, natively identified `R-01` … `R-15`; its premise findings are natively identified `PC-1` … `PC-9` (9 rows, headings `:50`–`:268`). Closed-book register `chatgpt-resolution.md:600`: **13** data rows at `:604`–`:616`, carrying **no identifiers of their own**; its premise findings are `Finding 1` … `Finding 8` (8 rows, headings `:15`–`:88`) | PASS — counts recorded; positional identifiers assigned for the unlabelled register only, under the contract below | A register row cited without a stable reference, so that a later verdict cannot be mapped back to the row it judges. An assigned identifier presented as though the report carried it |
| I8 | Rule 9: "where attached materials are silent or ambiguous, the agent records the gap in the claims register — never invents." The gaps sections are the raw material the consolidation merges and the premise adjudication routes. | `grep -cE '^- \*\*G-[0-9]+' "$OB"`; `awk 'NR>=585 && NR<=596' "$CB" \| grep -cE '^[0-9]+\. '` | Open-book gaps `claude-resolution.md:808`: **12** rows `G-1` … `G-12`; the section states in its own opening that `G-1`, `G-2` and `G-5` are the package's own gaps unchanged by this round — so **3 inherited, 9 new**. Closed-book gaps `chatgpt-resolution.md:583`: **12** numbered rows at `:585`–`:596`; the section marks none of them as inherited from the package, so the inherited/new split is **0 inherited, 12 new as marked by the report** | PASS — counts recorded with the inherited/new split each report states for itself | A merged count that loses the per-report split, so that a later consolidation cannot be checked for completeness against a number. An inherited/new split assigned by this pass rather than read from the report's own text |

## I4 reading note — "not newer than the handoff", and which handoff

The plan's I4 asks that each uploaded file's last-touching commit be "not newer than the
handoff". Two readings of *handoff* are available and they do not agree, so both are
recorded rather than one being chosen silently.

- **Assembly reading.** The handoff is the ERW-02 assembly commit
  `11b4e0c12529efe993143c7dcd9eb08df9a213fd` (2026-08-21), which `DELIVERY-NOTE.md:44`
  calls "the state of the tree as this package was completed". Under this reading
  `research_package/RESEARCH-CONTEXT-MASTER.md` is **newer**: `b8617a20…` (2026-08-28)
  touched it during the `54-06` reconciliation pass.
- **Engagement reading.** The handoff is the moment the package was actually given to the
  external agents — 2026-08-30, evidenced at I-note 2 below. Under this reading all three
  uploaded paths pass: the newest of them, `b8617a20…`, precedes both `54-07`'s readiness
  certification (`efe8e590…`, 2026-08-28T13:18:33) and the engagement.

**The engagement reading is the one this record relies on, and the reason is what D-15
protects.** D-15 exists so that a reader can reconstruct what the external agents actually
read. The agents read the tree as it stood on 2026-08-30, which is the
`54-06`-reconciled master. An edit landing before the agents read the file cannot have
destroyed that reconstruction; an edit landing after it would. The assembly reading would
report a violation where none occurred, and would do so by treating a pre-upload
correction as though it were a post-upload rewrite.

The assertion that carries the weight is unconditional under either reading and is
recorded as such: `git diff HEAD --stat` over the three uploaded paths is empty, so
nothing this pass has done has touched them.

**Ordering, for the record:** `11b4e0c1…` 2026-08-21 (assembly) → `b8617a20…`
2026-08-28T13:13:32 (`54-06` reconciliation, last touch on the master) → `efe8e590…`
2026-08-28T13:18:33 (`54-07` readiness certification) → 2026-08-30 (engagement and
arrival) → `9f1ad245…` 2026-08-31 (post-delivery plan set).

## I5 element table — the Rule-7 output contract, per report

Both reports are asserted against the same ten elements. `OB` is the open-book report
`claude-resolution.md`; `CB` is the closed-book report `chatgpt-resolution.md`. Line
numbers are the heading or marked line at which the element was found, so every cell is
re-derivable.

| # | Contracted element | Found in OB at | Found in CB at | Both present |
|---|---|---|---|---|
| 1 | Options menus carrying between two and four options | Menu sections `:423`, `:469`, `:528`, `:580`, `:634`, `:672`; six menus with option counts 4, 4, 3, 4, 3, 4 | Menu blocks `:182`, `:308`, `:405`, `:441`, `:473`, `:491`; six menus with option counts 3, 4, 3, 3, 3, 4 | yes — every menu in both reports is inside the contracted range |
| 2 | Mechanical-surface trade-offs | Dedicated `Mechanical trade-off` column, headers at `:441`, `:493`, `:555`, `:608`, `:652` | Dedicated mechanical column, headers at `:186`, `:312`, `:407`, `:445`, `:475`, `:493` | yes |
| 3 | Cross-decision interactions | Dedicated `Cross-decision interaction` column in every menu; plus the cross-menu section at `:674` | Dedicated interaction column at `:186`, `:312`, `:445`, `:475`, `:493`; in the menu at `:407` the interactions are folded into the capacity column rather than given a column of their own | yes — present in both; the CB structural variation at `:407` is recorded, not scored as an absence |
| 4 | A suggested default clearly marked | Marked blockquotes at `:448`, `:503`, `:561`, `:615`, `:658`, `:727` | Marked inside the first row of each menu, e.g. `:188`, `:314`, `:409`, `:447`, `:477`, `:495`, and again at `:545` | yes |
| 5 | One-way versus two-way door classification | Door blockquotes at `:455`, `:511`, `:566`, `:622`, `:662`, `:731`; `Door type` column in the decision sheet | Dedicated `Door` column in all six menus and in the owner-gated table at `:543`; `Door type` column in the decision sheet; the two door senses are defined at `:100`–`:103` | yes |
| 6 | A fill-in decision sheet with its columns named | `:793`, header `:795` — `# \| Decision \| Options \| Suggested default \| Door type \| Owner's pick`; 8 data rows | `:567`, header `:571` — `Decision \| Options \| Suggested default \| Door type \| Owner's pick`; 7 data rows | yes |
| 7 | A composed first-run recipe presented as a cross-menu coherence check | Coherence check at `:674`, composed recipe at `:688` | Combined heading at `:516` | yes |
| 8 | A "what the runbook inherits" section | `:748` | `:553` | yes |
| 9 | A claims-and-uncertainty register | `:860`, 15 rows | `:600`, 13 data rows | yes |
| 10 | Premise-challenge findings placed **ahead of** the per-question answers (Rule 17) | Findings open at `:42`; per-question answers open at `:381` — findings first | Findings open at `:3`; per-question answers open at `:98` — findings first | yes |

**Count found against count required: OB 10 of 10; CB 10 of 10. Absent elements: none in
either report.** Nothing is carried forward as an incomplete-contract finding from this
check, and neither report was edited.

One structural difference is recorded because it is real and will matter to the
consolidation: the closed-book report's menus are explicitly **ranked** (its column is
headed `Rank / option` and its rows are numbered), where the open-book report's menus are
lettered without a rank column. Both are the agent's own contracted output. This record
counts and locates them; it reproduces neither the ranking nor any marked default, and
attaches no weight of its own to either.

## I6 detail — the two evidence-label vocabularies, side by side

Recorded side by side and **not** merged. No label from one report is translated into the
other's vocabulary, because the two vocabularies partition the evidence along different
lines: one of them has a term for "read in the live tree" and the other, by construction,
cannot have one.

| Report | Declared at | Labels, in the report's own words | Occurrence counts |
|---|---|---|---|
| Open-book (`claude-resolution.md`) | `:35`–`:38` | "`[PKG]` package-derived (the three attachments) · `[REPO]` repository-verified by me in the live tree, with `file:line` · `[LIT]` published literature, cited by author / title / venue / year · `[OWN]` my own analysis or clean-room computation." | `[PKG]` 7, `[REPO]` 40, `[LIT]` 13, `[OWN]` 53, `[r2-QUAL]` 1; including split-bracket citation forms, `[PKG` 9 and `[REPO` 42 |
| Closed-book (`chatgpt-resolution.md`) | `:9`–`:11` | "**[P] Package-derived:** statements or repository excerpts supplied in the attachments." · "**[L] Literature:** published sources, with complete references below." · "**[A] Analysis:** independent derivations, interpretations, or proposed defaults." | `[P]` 21, `[L]` 7, `[A]` 59; compounds `[P/A]` 8, `[A/P]` 5, `[L/A]` 2; `[r2-QUAL]` 2 |

**The only mapping recorded here is one a report states itself.** The closed-book report
states at `chatgpt-resolution.md:13`: "No claim below is labeled repository-verified.
Repository citations retain the original `file:line` anchors supplied by the bundles."
That is the report telling the reader, in its own words, that its vocabulary has no
counterpart to the open-book report's live-tree label. No further mapping is asserted by
this record.

## I7 detail — register row identity

`LEDGER-PREFIX-CONTRACT` — fixed here as a contract, not left to the assigning pass.

- **The report whose register rows carry native identifiers keeps them unchanged.** The
  open-book report's register rows are `R-01` … `R-15` and its premise findings are
  `PC-1` … `PC-9`. Neither is renamed, re-prefixed, or shadowed by a parallel identifier.
  Inventing a second identifier for a row that already has one is how two vocabularies get
  flattened into one.
- **The report whose register rows carry no identifiers is assigned positional ones.**
  The closed-book report's 13 register data rows at `chatgpt-resolution.md:604`–`:616` are
  assigned `CB-NN`, numbered from `CB-01`, **in the order the rows appear in that report's
  register**, top to bottom, one identifier per data row, header and separator rows
  excluded. `CB-01` is the row at `:604` and `CB-13` is the row at `:616`.
- **The prefix is `CB-` and the numbering origin is `01`.** `54-10` greps this exact
  prefix to enforce its closed verdict vocabulary; an assignment under any other prefix
  makes that gate match nothing and pass having examined nothing.
- **Assigned identifiers are a citation convenience and never a claim about the report's
  own structure.** The closed-book report does not label its register rows; `CB-NN` is
  this pass's handle for referring to them, and any later document using one must be
  readable as "the Nth row of that report's register", never as "the row that report calls
  `CB-NN`".
- The closed-book report's premise findings **do** carry native identifiers of a kind —
  `Finding 1` … `Finding 8` — and those are used as written. Only the register rows are
  assigned.

## I8 detail — the gaps sections, per report

| Report | Section at | Rows | Marked inherited from the package | Marked new | How the split was determined |
|---|---|---|---|---|---|
| Open-book (`claude-resolution.md`) | `:808` | 12 (`G-1` … `G-12`) | 3 — `G-1`, `G-2`, `G-5` | 9 | The section's own opening sentence at `:810`–`:811` names the three and says "the rest are new" |
| Closed-book (`chatgpt-resolution.md`) | `:583` | 12 (numbered `1.` … `12.` at `:585`–`:596`) | 0 as marked by the report | 12 as marked by the report | The section marks no row as inherited; the split is read from the report's text and is not assigned by this pass |

The two counts coincide at 12 and that coincidence carries no meaning: the two sections
were produced from different evidence bases and the rows are not in correspondence. What
the counts are for is completeness checking — a later merge can be checked against a
number rather than against an impression.

## RULE-16-DIVERGENCE — the declared access mode ceased to describe the round

ERW Rule 16 reads: "**Declare the mode explicitly** in the master frontmatter
(`access_mode: closed-book` or `open-book`), in the prompt body, and in the delivery note.
An undeclared mode is a package defect: the agent's behavior, the evidence labels, and the
receiving-end verification burden all depend on it."
(`docs/runbooks/external-research/2026-06-11-external-research-workflow.md:205`–`:208`.)

The round declared **one** mode in all three required places and `54-07` certified it: see
`54-HANDOFF-READINESS.md` check **H2**, which recorded `access_mode: open-book` at
`RESEARCH-CONTEXT-MASTER.md:9`, `DELIVERY-NOTE.md:7` and `:62`, and
`RESEARCH-AGENT-PROMPT.md:7` and `:76`.

**What this record adds.** The **declared** mode and the **engaged** mode diverged for one
of the two engagements. The defect is therefore not a missing declaration — H2 is right
that the declaration is present in all three places — but a declaration that **ceased to
describe the round** once one engagement ran under a different access instruction. A
reader who trusts the declaration calibrates one verification burden for both reports, and
one of the two burdens would be wrong.

### Evidence — each report's own words, quoted with file and line

**The open-book engagement, in its own words.**

- `claude-resolution.md:8` — frontmatter: `access_mode: open-book (Route B)`.
- `claude-resolution.md:7` — frontmatter: "`live_tree_seen:
  <home>/Desktop/3_body_problem/.worktrees/trainex (read-only, 2026-08-30; git
  metadata not reachable from the mount, so no HEAD hash is recorded — see G-10)`". The
  worktree it read and the date it read it are recorded; repository-level git metadata was
  **not** reachable from the mount it was given, so it could record no tree hash of its
  own.
- `claude-resolution.md:847`–`:851` — gap `G-10`: "no live-tree commit pin. The connected
  mount is a git worktree whose `.git` file points outside the mount, so `git log`/`git
  status` are unreachable and no ERW Rule 20 live-tree hash can be recorded. Every
  citation here is by `file:line` **and** content, and every one was content-matched; a
  Rule 20 pin should be attached by someone with repository-level git access before this
  report is filed."

**The closed-book engagement, in its own words.**

- `chatgpt-resolution.md:7` — "Following your revised access instruction, this report uses
  the attachments and published literature without live repository verification."
- `chatgpt-resolution.md:13` — "No claim below is labeled repository-verified. Repository
  citations retain the original `file:line` anchors supplied by the bundles."
- `chatgpt-resolution.md:596` — gaps row 12: "Additional live implementation
  contradictions are outside this report's verification claim. Repository inspection was
  waived. That limits conformance claims; it does not prevent the calculations and
  candidate dispositions above."

### What follows, and what does not

**What follows.** The two reports do not have the same evidence base. One resolved
repository anchors against the tree; the other relayed anchors it received in the
attachments. They therefore do not carry the same evidential status and they do not
attract the same verification burden. The burdens are derived separately below.

**What does not follow.** Neither agent concealed its mode. Both declared theirs in their
own text, up front — the open-book report in its frontmatter at `:7`–`:8` and again in
`G-10`, the closed-book report in its third paragraph at `:7` and again in its gaps section
at `:596`. This is a defect in the **round's declaration**, not in either agent's conduct,
and the finding is worded that way deliberately: an agent that states its own evidence
base plainly at the top of its report has done the thing the rule exists to make possible.

### Consequence for the record

`54-HANDOFF-READINESS.md` check **H2** certified a property of the package that **was true
when it was checked**: on 2026-08-28 the declaration was present, uniform, and correct for
the round as then constituted. It is **not corrected here**, and this plan does not edit
that file. This record **qualifies** it: H2's certification is sound as a statement about
the package, and it is not a statement about how each engagement subsequently ran. The
qualification arises entirely from evidence that did not exist at certification time —
the two reports landed on 2026-08-30, two days after H2 was recorded.

## The per-report verification burden

The runbook's access-mode comparison table sets the `Receiving-end burden` row as: for
Route B (open-book), "**every repo-derived claim independently verified in-repo before
use** (Rule 19)"; for Route A (closed-book), "none beyond normal channel protocol"
(`docs/runbooks/external-research/2026-06-11-external-research-workflow.md:60`). Neither
line describes this round as it actually ran, so each burden is stated explicitly and
**derived** rather than selected.

### BURDEN-OPEN-BOOK — the report that read the tree

The runbook's Route-B burden applies **unchanged**. Rule 19 states the reason directly: "A
Route B report's repo claims arrive as checkable assertions, not as established facts —
they carry a file:line citation precisely so they can be re-derived independently"
(`…external-research-workflow.md:223`–`:227`).

- Every claim this report labels `[REPO]` is a checkable assertion carrying a citation
  precisely so it can be re-derived, and every one is re-derived independently in the next
  plan of this pass. Occurrence count recorded at I6: 40 exact-token `[REPO]`, 42 counting
  split-bracket citation forms.
- The report **extends the obligation to its own analytic work itself**, and that
  extension is the report's, not this record's: `claude-resolution.md:915`–`:916` states
  that all `[OWN]` computation "is subject to ERW Rule 19 in-repo verification before it
  informs any decision, roadmap, or spec edit", and `G-6` at `:832`–`:836` repeats it per
  figure. The burden recorded here therefore covers the `[REPO]` set by the runbook's own
  line and the `[OWN]` set by the report's own request.
- The report could record no live-tree hash of its own (`G-10`). That does not reduce the
  burden; it relocates the pin obligation to the receiving end, which is what Task 3 of
  this plan discharges.

### BURDEN-CLOSED-BOOK — the report that did not read the tree

The runbook's Route-A line would say the burden is "none beyond normal channel protocol".
**That line does not fit this report**, and the mismatch is specific and checkable: the
report's citations are **repository anchors** — `pinn_architecture.md:429`,
`ctl_instruction.md:1815`, `52-DIAG-05-REDERIVATION.md:58` and so on — even though the
report never resolved them against the repository, and says so at `:13`. Route A normally
carries no such anchors at all, because ERW Rule 1 forbids repository paths in a
closed-book upload; here they arrived inside verbatim bundles and were relayed outward.
An anchor that looks re-derivable but was never resolved is exactly the artefact the
Route-A burden line was never written to cover.

So this report's burden is a **different one**, and it is stated in full:

1. **Provenance triage of every repository anchor, three ways.** For each anchor, decide
   whether it was (a) **supplied verbatim** in one of the three attachments, so the report
   relayed a line the packet gave it; (b) **reconstructed by offset** from a verbatim block
   an attachment carries, so the report computed the line number rather than receiving it;
   or (c) **neither** — an anchor with no provenance in the attachments at all.
2. **Content resolution against the tree.** Then resolve each anchor by content against
   the pinned tree, so that the anchor's correctness is established independently of its
   provenance.

The two steps answer different questions and both are needed. Provenance alone cannot tell
an accurate relay from a lucky reconstruction. Content resolution alone cannot tell a
faithful bundle from a bundle that happened to be right. Together they let a reader
distinguish **an accurate relay** from **a reconstruction that happens to be right** from
**one that is not** — and only the first of the three is evidence about the bundle's
fidelity.

**This burden is derived from the mismatch between the report's actual evidence base and
the citation form it used.** The runbook anticipates neither, because it does not
contemplate a closed-book round whose uploads carry repository anchors. This pass states
the burden rather than inheriting it, and records that it is stated rather than inherited.

## The claim-class independence taxonomy (D-14)

This is the taxonomy every later plan in this pass inherits; the cross-report adjudication
and the consolidation take it as given rather than re-deriving it.

| Class marker | What the class covers | Which agent could evidence it | What agreement between the two reports means | What disagreement means |
|---|---|---|---|---|
| `CLASS-PACKAGE-INTERNAL` | Assertions about what the attachments themselves say, including internal contradictions between one part of the packet and another | **Both.** Both agents read the same three attachments, pinned to the same baseline (I3) | Agreement **is** independent corroboration. Two readers reached the same reading of the same text from separate readings of it | A genuine dispute about what the text says, resolvable by re-reading the attachment and quoting it |
| `CLASS-REPOSITORY-DERIVED` | Assertions about what the tree contains — file contents, line locations, executed values in retained artifacts | **One only.** Only the open-book agent could resolve a repository anchor against the tree; the closed-book agent relayed anchors the bundles supplied and says so at `chatgpt-resolution.md:13` | Agreement is **not** a second confirmation and must never be read as one. The closed-book report's matching statement is evidence that **the attachment relayed the tree faithfully** — a real and useful finding about bundle fidelity — and it is **not a second reading of the tree**. This is the central rule of the taxonomy, because it is the one a careless consolidation would break, and it would break it in the direction of overconfidence | Two different things, and they must be told apart: either the bundle diverges from the tree, or the open-book agent misread the tree. The provenance triage in `BURDEN-CLOSED-BOOK` is what separates them |
| `CLASS-LITERATURE` | Assertions about what a cited published paper says | **Both.** Both agents could reach the published literature independently of this repository | Agreement is independent corroboration, **subject to both having read the same edition** — which is recorded per claim rather than assumed, since the two reports cite journal versions and preprints in different combinations | A dispute about the source, resolvable by naming edition, section and equation number for each side |
| `CLASS-ANALYTIC` | Closed-form derivations and computations each agent performed itself | **Both.** Both could do arithmetic | Agreement corroborates **the arithmetic** and does **not** corroborate the premises the arithmetic ran on. **Premise-sharing caveat:** if both agents inherited the same premise from the same package, agreement between them tells you nothing whatever about that premise — they are two evaluations of one assumption, not two tests of it | A computational error on one side, or two different premises silently in play. Locate the premise before adjudicating the arithmetic |

**The operational rule the consolidation inherits.** A consolidated statement may claim
two-agent support **only when the claim's class admits it**, and every consolidated claim
carries its class so that a reader can **check** the entitlement rather than trust it.
A claim in `CLASS-REPOSITORY-DERIVED` never carries two-agent support on the strength of
agreement alone; where the two reports agree there, the consolidated statement records
one-agent repository support **plus** a bundle-fidelity corroboration, and says which is
which.

**If the reports' own self-descriptions contradict anything in these three sections, the
reports win** — they are the primary record of their own engagements — and the section is
rewritten to match them with both readings recorded as a correction. No such contradiction
was found: each quoted self-declaration above is reproduced from the report's own text at
the cited line, and the gate independently confirms the two load-bearing self-declarations
are present in the reports before this section is accepted.

## The ERW Rule-20 live-tree pin, re-derived

The pin stamped into `DELIVERY-NOTE.md` is derived here, not copied from the cell that was
already there. That cell held a short eight-character hash written at package assembly
together with an explicit instruction to re-stamp it with the actual tip if the branch had
moved. It had moved.

| Step | Command | Output |
|---|---|---|
| The branch tip when the reports arrived, at full forty characters, with author date and subject | `git log -1 --format='%H%n%ad%n%s' --date=iso-strict efe8e590d6c6b2a77cc92abb0b93d625e2b92c49` | `efe8e590d6c6b2a77cc92abb0b93d625e2b92c49`; `2026-08-28T13:18:33+08:00`; `docs(54-07): certify trainex-r3 handoff readiness and halt` |
| No commit landed between that tip and the reports' arrival | `git rev-list efe8e590d6c6b2a77cc92abb0b93d625e2b92c49..HEAD --before='2026-08-30T23:59:59Z'` | **empty** — made explicit here rather than left as a silent absence of output. The next commit on the branch is `9f1ad2453906a97546af02d3be01f3c31f2cd6ad` (2026-08-31T17:51:59+08:00), after both reports had landed |
| Arrival date of each report, from its own recorded creation date and from its modification time | `grep -n 'created:' <report>`; `date -u -r <report> +%Y-%m-%dT%H:%M:%SZ` | Open-book: self-recorded `created: 2026-08-30` at `claude-resolution.md:5`, reading date `2026-08-30` at `:7`; modification time `2026-08-30T10:28:01Z`. Closed-book: no frontmatter and no self-recorded date; modification time `2026-08-30T14:35:44Z` |
| The stamped value | the full forty-character hash from step 1 | `efe8e590d6c6b2a77cc92abb0b93d625e2b92c49`, written into the delivery note under the name `LIVE-TREE-PIN`. The short form `efe8e590` is recorded there only as a reading aid and is nowhere used as the pin |
| The pin resolves to a real commit object | `git cat-file -e efe8e590d6c6b2a77cc92abb0b93d625e2b92c49^{commit}` | exit 0 |
| The attachment baseline resolves to a real commit object and differs from the pin | `git cat-file -e 6a4f9b9902ab62e1d1f57bba0e521f38120c416d^{commit}` | exit 0; and the two forty-character values differ, so the Rule-20 distinction between the snapshot pin and the live-tree pin is preserved |

**Which arrival evidence is relied on, and why.** The modification times. They are the only
per-file arrival evidence that exists for **both** reports — the closed-book report carries
no frontmatter and records no date of its own — and the pin needs the moment the reports
landed in this tree relative to the branch, which is what a modification time records and
what an authoring date does not. The open-book report's self-recorded date corroborates
them to the day. Modification times are observed state rather than committed state, so the
command that read them is recorded above so a reader can see what was read.

**Why the pin is per engagement.** Rule 20 pins the tree the agent saw. Only one of the two
agents saw a tree. A single-row pin would assert that both saw the same one, which is
false, and would make the closed-book report's anchors look re-derivable against a tree it
never read. The delivery note therefore carries one block per report, and the block for the
report that read no tree records that it has **no live-tree pin** and names the attachment
baseline at full length as its only baseline.

## The citable-path set

The set is **extracted from the two reports**, not listed from memory. Extraction ran in
two passes over each report. The first matched full-path tokens with an extended regular
expression alternating the repository's top-level directory names against a path tail and a
markdown, Python, YAML, JSON or JSONL suffix; the exact commands are in the fenced block
below, recorded outside any table cell so that no escaping convention distorts them. The
second collected
abbreviated citations — bare filenames inside backticks, and paths elided with a leading ellipsis —
collected separately and resolved by locating the file in the tree. The closed-book report
returned **zero** full-path tokens, which is itself consistent with its own statement at
`:13` that its repository citations are anchors the bundles supplied.

**Every abbreviation resolved, with the full path it resolved to:**

| Abbreviated citation as written | Cited by | Resolved to |
|---|---|---|
| `pinn_architecture.md` | both reports | `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` — the closed-book report fixes this resolution itself at `:13` ("the authoritative files under `pinn_instruction/markdown_conversion/framework-specs/` … they do not mean the frozen copies") |
| `ctl_instruction.md` | both reports | `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` — same sentence at `chatgpt-resolution.md:13` fixes it |
| `RESEARCH-CONTEXT-MASTER.md` | both reports | `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md` |
| `2026-08-17-residual-frame-conformance-audit.md` | closed-book | `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md` — unique match under `find . -name` |
| `52-DIAG-05-REDERIVATION.md` | closed-book | `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-DIAG-05-REDERIVATION.md` — unique match |
| `52-VER-20-ROUTING-HANDOFF.md` | closed-book | `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md` — unique match |
| `.../framework-specs/integrity-r1/specs/pinn_architecture.md` | open-book | `pinn_instruction/markdown_conversion/framework-specs/integrity-r1/specs/pinn_architecture.md` |
| `.../framework-specs/integrity-r2/specs/pinn_architecture.md` | open-book | `pinn_instruction/markdown_conversion/framework-specs/integrity-r2/specs/pinn_architecture.md` |
| `.../framework-specs/trainex-r1/specs/pinn_architecture.md` | open-book | `pinn_instruction/markdown_conversion/framework-specs/trainex-r1/specs/pinn_architecture.md` |
| `.../framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/specs/pinn_architecture.md` | open-book | `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/specs/pinn_architecture.md` |
| `.../stage0-rerun-seed41-attempt-02/config.yaml` | open-book | `.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/evidence/attempts/stage0-rerun-seed41-attempt-02/config.yaml` — resolved from the sibling full path the same report writes out at `:142` and `:205` |
| bare `REQUIREMENTS.md`, bare `causal_pinn.py`, `collocation_sampler.py`, `controllers.py`, `guards.py`, `loss_catalog.py`, `tb_sink.py` | open-book | already written out in full elsewhere in the same report; the bare forms are shorthand for those same paths and add no new path |

All 21 resolved paths exist in the tree and are tracked. None resolved ambiguously; each
abbreviated filename had exactly one match under `find . -name`, except the five copies of
`pinn_architecture.md`, which the open-book report itself enumerates and distinguishes at
`:116`–`:120` and which are therefore carried as five separate entries rather than
collapsed.

The three extraction commands, verbatim (`$f` is each report in turn):

```
grep -oE '(\.planning|pinn|pinn_instruction|docs|reference-code|simulation_data|tests|runs)(/[A-Za-z0-9._@+-]+)+\.(md|py|yaml|yml|jsonl|json|txt)' "$f" | LC_ALL=C sort -u
grep -oE '`[^`]*`' "$f" | tr -d '`' | grep -oE '(^|[^/A-Za-z0-9._-])([A-Za-z0-9._@+-]+\.(md|py|yaml|yml|jsonl|json))' | sed -E 's/^[^A-Za-z0-9._-]//' | LC_ALL=C sort -u
grep -oE '`?\.\.\.[/A-Za-z0-9._@+-]+`?' "$f" | tr -d '`' | LC_ALL=C sort -u
```

`CITABLE-PATH-SET` — the closed list, one path per line, pasteable verbatim into later
checks:

```
.planning/REQUIREMENTS.md
.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/evidence/attempts/stage0-rerun-seed41-attempt-02/config.yaml
.planning/milestones/v2.2-phases/50-valid-stage-0-re-run/evidence/attempts/stage0-rerun-seed41-attempt-02/logs/train.log.jsonl
.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-DIAG-05-REDERIVATION.md
.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md
docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md
pinn/constants.py
pinn/loss_catalog.py
pinn/network.py
pinn/training/collocation_sampler.py
pinn/training/controllers.py
pinn/training/guards.py
pinn/training/tb_sink.py
pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/specs/pinn_architecture.md
pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
pinn_instruction/markdown_conversion/framework-specs/integrity-r1/specs/pinn_architecture.md
pinn_instruction/markdown_conversion/framework-specs/integrity-r2/specs/pinn_architecture.md
pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md
pinn_instruction/markdown_conversion/framework-specs/trainex-r1/specs/pinn_architecture.md
pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md
reference-code/reference_NNs/PINA-master/pina/solver/physics_informed_solver/causal_pinn.py
```

**The set is closed at 21 paths, and how it was closed is recorded above so a later reader
can re-open it if a new citation appears.** A path cited by a later document — the
consolidation, or a verification pass following a citation this extraction did not see — is
not covered by anything asserted here until the set is widened and the identity proof
re-run over the widened set.

## The identity proof — `PIN-TREE-IDENTICAL`

| Check | Command | Output | Verdict |
|---|---|---|---|
| The pinned commit and the current tip agree over the citable-path set | `git diff --stat efe8e590d6c6b2a77cc92abb0b93d625e2b92c49 HEAD -- $(cat <the block above>)` | empty | `PIN-TREE-IDENTICAL` |
| The working tree is clean over the same set | `git status --porcelain -- $(cat <the block above>)` | empty | `PIN-TREE-IDENTICAL` |
| The pathspec did not silently collapse | 21 recorded entries; 21 shell arguments after word splitting; both counts printed and compared | `CPN=21 ARGS=21` | PASS — no recorded path contains whitespace, so no entry was split or swallowed |
| The set is non-empty and contains its two sentinels | `grep -qF` for the live authoritative architecture spec and for the requirements file | both found | PASS — an extraction that silently matched nothing would certify a claim it could not see |

Success prints the marker rather than relying on the absence of output, because an empty
result and a mistyped path produce the same silence. Both commands and both outputs are
recorded here and in the delivery note's pin section.

**The conclusion these checks license, in one sentence:** a re-derivation performed against
the working tree is a re-derivation against the pinned tree, for every path either report
cites. Nothing is claimed about any path outside the set.

## Standing bars at plan close

Commands carrying Bar F / Bar G3 cost vocabulary are recorded in fenced blocks, matching
the convention `54-07` used, so that recording a command does not trip the check the
command defines.

| Check | Command | Output | Verdict |
|---|---|---|---|
| Bar D — canonical (`54-01-PLAN.md`), index-anchored | `git diff --stat -- pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/sampling_method.md pinn/ simulation_data/ tests/` | empty | PASS |
| Bar D — the same paths anchored to `HEAD` | `git diff HEAD --stat -- <the same six pathspecs>` | empty | PASS — recorded in addition to, never instead of, the canonical form, because a staged-but-uncommitted edit is invisible to the index-anchored form and this plan's prohibitions require the `HEAD` anchor |
| Bar E — canonical two-path form, `HEAD`-anchored as `54-07` recorded it | `git diff HEAD --stat -- .planning/REQUIREMENTS.md .planning/ROADMAP.md` | empty | PASS — this plan edits neither file, so no narrowing applies and none is taken |
| Bar F — cost vocabulary over the ruling record | fenced block below | `0` | PASS — equal to the number `54-07` recorded |
| Bar G1 — no candidate value across any decision surface | fenced block below, selector `S` byte-unchanged from `54-06-PLAN.md`, file list extended to this pass's six plan files | region cardinality `G1-REGION=0`; remainder after token strip empty | `BAR-G-CLEAN-NO-SURFACE-NAMED` |
| Bar G2 — no ordering vocabulary in the plans' own voice | fenced block below | empty | PASS |
| Bar G3 — no cost framing in the plans' own voice | fenced block below | empty | PASS |
| Bar G preprocessing sanity — fence balance and retained stream size | `grep -c '^```' ` over each of the six plan files; retained line count of the shared stream | fence counts 10, 8, 8, 8, 10, 10 — all even; retained stream `4233` lines | PASS — an odd fence count would make the preprocessing swallow the rest of a file and every sub-bar would then pass vacuously |
| Check R1-w — widened round-root manifest | the fenced block in `54-08-PLAN.md`'s verification section, run verbatim | `MANIFEST-OK-W` | PASS |
| Anchor gap still `OPEN` in both registers | `grep -n 'Status' 54-GAPS.md \| grep -i 'OPEN'`; `grep -n 'GAP-54-01' .planning/milestones/v2.3-GAPS.md \| grep -i 'OPEN'` | `54-GAPS.md:42` `**Status:** OPEN`; `v2.3-GAPS.md:11` and `:15` both carry `OPEN` | PASS — both non-empty |
| Ruling record and both gap registers byte-unchanged | `git diff HEAD --stat -- 54-RULING.md 54-GAPS.md .planning/milestones/v2.3-GAPS.md` | empty | PASS — anchored to `HEAD` rather than to the index, so a staged edit cannot leave the assertion empty and passing |
| No consolidated document exists | `test ! -f pinn_instruction/markdown_conversion/framework-specs/trainex-r3/trainex-r3-resolution-doc.md && echo CONSOLIDATION-ABSENT` | `CONSOLIDATION-ABSENT` | PASS |
| Manual structural read of this file, end to end | read of `54-INTAKE.md` in full | no sentence in this record names a candidate value for any decision surface, reproduces any menu option, reproduces any marked default, or attaches weight to the order in which either report presents them. Where a report's contracted output is a ranked menu or a marked default, this record counts it and locates it by line and does not carry it. The two reports are presented in a fixed order throughout — open-book first — and that order is a presentation convention with no evidential weight, stated here so it is not read as one | PASS — this file names no candidate value, marks nothing, and ranks nothing |

**Bar G verdict literal, recorded exactly as the gate prints it:**
`BAR-G-CLEAN-NO-SURFACE-NAMED`, with `G1-REGION=0`. This is not a paraphrase and not a
substitute for `BAR-G-CLEAN`. The two literals mean different things: `BAR-G-CLEAN` states
that the plan files named a decision surface and named no value for it;
`BAR-G-CLEAN-NO-SURFACE-NAMED` states that this pass's six plan files named **no decision
surface at all**, so the bar's region over them is empty. `54-07` recorded
`G1-REGION=13` / `BAR-G-CLEAN` over the two plan files of the previous pass; the change to
a zero region is a property of how this pass's plans are written, and it is recorded under
its own verdict rather than reported as a silent pass.

Bar F command (fenced):

```
grep -ciE 'faster|slower|cheaper|quicker|days|weeks|hours|effort|simpler|harder|easier|more work|less work' \
  .planning/phases/54-recalibration-decision-grounding/54-RULING.md
```

Bar G shared stream and sub-bars (fenced; defined in `54-06-PLAN.md`, selector unchanged,
file list extended to this pass):

```
P=.planning/phases/54-recalibration-decision-grounding
V=$(cat "$P/54-08-PLAN.md" "$P/54-09-PLAN.md" "$P/54-10-PLAN.md" \
        "$P/54-11-PLAN.md" "$P/54-12-PLAN.md" "$P/54-13-PLAN.md" \
     | awk '/^```/{f=!f; next} !f' \
     | grep -v 'planner-discipline-allow' | grep -v '<automated>')
S='eta_c|η_c|η|first_omega_0|omega_0|ω₀|n_col|N_t|collocation_count|Rbar|R̄|normaliz|reference scale|clip|clamp'
printf '%s\n' "$V" | grep -icE "$S"
printf '%s\n' "$V" | grep -iE "$S" | sed -E "s/($S)//gI" | grep -E '[0-9]'
printf '%s\n' "$V" | sed 's/`[^`]*`//g' \
  | grep -inE 'recommend|suggest|prefer|best|most likely|primary candidate|default to|should use|ranked|leading option'
printf '%s\n' "$V" | sed 's/`[^`]*`//g' \
  | grep -inE 'faster|slower|cheaper|quicker|days|weeks|hours|effort|simpler|harder|easier|more work|less work'
```

## Halt state at plan close

Phase 54 does **not** close in this plan. `GAP-54-01` stays `OPEN` in both registers; the
ruling record's checkpoint ② stays unfilled and byte-unchanged; Phase 56 stays closed; no
consolidated document exists. No claim in either report has a verdict, no premise challenge
is adjudicated, and no entry is made in the ruling record. The Rule-19 verification pass
follows in wave 2.
