---
phase: 54
plan: 07
status: active
created: 2026-08-22
---

# 54-HANDOFF-READINESS — certification that the trainex-r3 round-root artifacts are ready to leave

## Table-cell pipe convention

Every literal pipe character inside a recorded command in this file is written escaped as `\|`. This is not cosmetic. The empty-cell gate splits markdown table rows on the pipe character, so an unescaped shell `||` (Check R1) or an unescaped single pipe in `tr '\n' ' ' \| tr -s ' '` / `grep -o … \| wc -l` yields an empty field and reports `EMPTY-CELL` on a correctly filled row, or silently shifts every cell after it. The repair is the escape, never deleting the command from the cell. This convention governs every later table in this file.

Precondition: `54-RECONCILIATION.md` exists. Check R1 prints `MANIFEST-OK`.

Quoted rule text is from `docs/runbooks/external-research/2026-06-11-external-research-workflow.md`.

## Certification table (H1–H8)

| Check | ERW rule | Command | Output | Verdict | What a failing run looks like |
|---|---|---|---|---|---|
| H1 | Rule 15: "Maximum 5 uploaded attachments per sub-package." Inclusive maximum of five. | Count uploaded names from three places, reduce with `sed 's#.*/##'`, compare as `LC_ALL=C` sorted sets. Packet `## 2`: extract backtick filenames from the three-row Attachment table. Prompt header: extract the three numbered backtick paths above the horizontal rule. Delivery-note handoff table: extract the three Attachment-column paths. | Raw packet: `RESEARCH-CONTEXT-MASTER.md`, `framework-specs-bundle.md`, `v2.2-closure-evidence-bundle.md`. Raw prompt: `research_package/RESEARCH-CONTEXT-MASTER.md`, `specs/framework-specs-bundle.md`, `research_package/v2.2-closure-evidence-bundle.md`. Raw delivery note: same three round-root-relative paths. Normalized set (all three places): `RESEARCH-CONTEXT-MASTER.md` `framework-specs-bundle.md` `v2.2-closure-evidence-bundle.md`. Duplicate basenames: 0. Count: 3 of at most 5. | PASS — identical basename sets of size 3; path-versus-filename difference is notation, not a defect | Count 6 fails the cap. A fourth basename, a missing basename, or a duplicate basename after `sed 's#.*/##'` fails the three-way agreement |
| H2 | Rule 16: "Declare the mode explicitly in the master frontmatter (`access_mode: closed-book` or `open-book`), in the prompt body, and in the delivery note." | `grep -n 'access_mode: open-book'` on master, delivery note, and prompt; plus prompt body heading below the HR | Master frontmatter `RESEARCH-CONTEXT-MASTER.md:9` `access_mode: open-book`. Delivery-note frontmatter `DELIVERY-NOTE.md:7` `access_mode: open-book`; body `DELIVERY-NOTE.md:62` repeats the literal. Prompt frontmatter `RESEARCH-AGENT-PROMPT.md:7` `access_mode: open-book`. Prompt body below HR `RESEARCH-AGENT-PROMPT.md:76` `## Access mode: open-book`. | PASS | Missing literal in master or delivery-note frontmatter, or prompt body silent below the HR, is an undeclared mode |
| H3 | Rule 17: the prompt "must instruct the agent to test the package's own stated premises against the repository and to report contradictions as first-class findings reported up front" and "Phrase it as a duty, not a permission: an agent that finds a false premise and buries it has failed the round." | `grep -n` in the prompt and master `## 9` for the three elements | Prompt duty framing `RESEARCH-AGENT-PROMPT.md:95` "Challenge the premises. This is a duty, not a permission." Prompt up-front placement `RESEARCH-AGENT-PROMPT.md:97` "first-class finding, up front, ahead of your per-question answers". Prompt consequence `RESEARCH-AGENT-PROMPT.md:98` "An agent that finds a false premise and buries it has failed the round." Master `## 9` `RESEARCH-CONTEXT-MASTER.md:336` matching mandate (duty, up-front, buries-it consequence). | PASS — all three Rule-17 elements in the prompt; matching mandate in master `## 9` | A prompt that permits rather than requires premise-challenge, reports contradictions only as footnotes, or omits the buries-it consequence fails |
| H4 | Rule 18: "No file edited, no training run, no evaluation invoked, no command with side effects, no commit" plus standing bars and "Discriminating experiments are proposed as owner-gated options, never performed." Reading recorded: Rule 18 states the training-run prohibition twice (base "no training run" and standing "no new training runs"); this plan counts them as **one obligation stated in two registers**, required count **9**, not 10. | `awk '/^## Hard bars/{f=1;next} /^## /{f=0} f' RESEARCH-AGENT-PROMPT.md \| tr '\n' ' ' \| tr -s ' '` then match the nine literals; same bars in master `## 9` | Flattened hard-bars section nonempty, length 445 characters. Nine literals found: Edit no file; Start no training run; Invoke no evaluation; command with side effects; Make no commit; framework specification; Select no remedy; held-out evaluation governed by owner policy; owner-gated options never performed. Wrap demonstration: "held-out evaluation and it is governed by owner policy" is split across `RESEARCH-AGENT-PROMPT.md:118-119` and is found only after flattening. Master `## 9` `RESEARCH-CONTEXT-MASTER.md:338-343` carries the same bars in the imperative. | PASS — 9/9 under the recorded reading | Flattened section empty, or fewer than 9 required literals, or a required-count of 10 that would fail this compliant package. A line-scoped match that misses the wrapped held-out sentence is the inert-check failure this flattening exists to catch |
| H5 | Rule 5 (attachment baseline) and Rule 20: "Pin the tree the agent saw." | Forty-hex scan of all five round-root files; `git cat-file -e 11b4e0c1^{commit}`; `git rev-parse HEAD`; inspect the live-tree pin table | All five files carry exactly 1 distinct 40-hex string, all equal to `6a4f9b9902ab62e1d1f57bba0e521f38120c416d`. Live-tree table rows: worktree, branch, commit at engagement, access method, engagement date. Recorded commit `11b4e0c1` resolves (`git cat-file -e` exit 0). Current HEAD `b8617a20b499d63958744f9f39ef8fbe911c9cfb`. They do **not** agree — 54-06 committed after the pin was written. The commit cell carries an explicit re-stamp instruction naming `git rev-parse HEAD`. Access method and engagement date remain `PENDING` (owner, at engagement). | PASS — Rule 5 pin identical across five files; Rule 20 table present; recorded commit is a real object; re-stamp instruction present; HEAD has moved | A second 40-hex string in any round-root file; a prefix-only match treated as agreement; `git cat-file -e` failing; a pin cell with no re-stamp instruction after HEAD has moved |
| H6 | Rule 7: options menus (2–4, mechanical-surface trade-offs, cross-decision interactions, suggested default clearly marked); one-way vs two-way door classification; fill-in decision sheet; composed first-run recipe as a cross-menu coherence check; "what the runbook inherits"; claims-and-uncertainty register; prompt must say "suggest defaults; never decide." Required element count **10**. Complementary to inherited Bar A2 (54-06 re-derived 4 matching lines / 11 occurrences in master `## 9`). | Content match of the 10 elements in master `## 9` and in the prompt "What to produce" section | Master `## 9` (`RESEARCH-CONTEXT-MASTER.md:326-351`): 10/10 present. Prompt (`RESEARCH-AGENT-PROMPT.md:126-156`): 10/10 present, including `Suggest defaults; never decide.` Absent elements: none. Bar A2 cross-reference: 54-06 recorded 4 matching lines and 11 occurrences, both ≥ 4, so `## 9` was not gutted to pass Layer 1. | PASS — 10/10 in master `## 9` and in the prompt | Any of the 10 elements missing; a lexically clean `## 9` under Layer-1 vocabulary (Bar A2 below 4) |
| H7 | Rules 1–2 Route-B inversion: "the \"attached files only\" instruction must NOT appear — it directly contradicts the mandate in Rule 17." Route-A zero-repo-path audits apply to Route A packages only. | Wrap-tolerant extract: `tr '\n' ' ' < docs/runbooks/external-research/2026-06-11-external-research-workflow.md \| tr -s ' ' \| grep -o 'Package audits that check[^.]*Route A packages only'`. Opening-fragment line range via `grep -n 'Package audits that check'`. Occurrence count: `grep -o 'attached files only' MASTER SPECS V22 \| wc -l` summed; prompt excluded. | Extracted sentence: "Package audits that check \"zero repo-path markers\" apply to Route A packages only". Citation **line range** `docs/runbooks/external-research/2026-06-11-external-research-workflow.md:141-142` (wraps; a line-scoped grep for the tail returns nothing). `attached files only` occurrences in the three uploaded files: **1**, in the master at `RESEARCH-CONTEXT-MASTER.md:67`: "Nothing here says \"attached files only\" — under ERW Rule 17 that instruction would contradict the mandate." Negating words: "Nothing here says" and "would contradict". Prompt excluded by definition. | PASS — Route-A audit excluded by quoted runbook sentence (not waived); Route-B inversion holds with the denying line quoted | Two occurrences; an occurrence without negation; an occurrence in specs or v2.2 bundle; a line-count (`grep -c`) substituting for occurrence count; a single-line citation of the wrapping runbook sentence |
| H8 | Route-B self-containment: attachments carry every claim the agent must act on; unfilled delivery-note fields are exactly the two the owner fills at engagement. | Assert master `## 2` treatment, `## 3` tiering including the anchor-resolution rule, `## 5` framed questions, `## 7` silences; scan uploaded files for companion references not among the three attachments; `grep -n PENDING DELIVERY-NOTE.md` | Master `## 2` states treatment of each of the three attachments. `## 3` carries source tiering and the five-file anchor-resolution rule (corrected by 54-06 A-11). `## 5` carries the framed questions. `## 7` names what the assembled evidence cannot answer. Uploaded files do not refer the agent to a companion that is not among the attachments (DELIVERY-NOTE / prompt / `research_results/` are named in `## 2` as **not** uploaded). Unfilled markers in `DELIVERY-NOTE.md`: line 45 access method `PENDING — how access was granted …`; line 46 engagement date `PENDING`. Count: **2**. No third unfilled field. | PASS | A third `PENDING` in the delivery note; an uploaded file that sends the agent to an unattached companion as required reading; `## 2`/`## 3`/`## 5`/`## 7` missing |
| R1 | Inherited from 54-06 (authorized five-path manifest; not an H-row, recorded so the empty-cell gate sees the escaped `\|\|`) | `R3=pinn_instruction/markdown_conversion/framework-specs/trainex-r3; A=$(find "$R3" -type f \| LC_ALL=C sort); E=$(printf '%s\n' "$R3/DELIVERY-NOTE.md" "$R3/research_package/RESEARCH-AGENT-PROMPT.md" "$R3/research_package/RESEARCH-CONTEXT-MASTER.md" "$R3/research_package/v2.2-closure-evidence-bundle.md" "$R3/specs/framework-specs-bundle.md" \| LC_ALL=C sort); [ "$A" = "$E" ] && echo MANIFEST-OK \|\| { echo MANIFEST-FAIL; exit 1; }` | `MANIFEST-OK` | PASS | `MANIFEST-FAIL` (sixth file, missing file, or one-for-one substitution) |

## Routing note for the deferred post-delivery replan

The replan is authored **after** delivery. It is not authored now, for two reasons:

1. Its content depends on evidence that does not yet exist (`research_results/<agent>-resolution.md` files, the Rule-19 verification report, and the Rule-12 consolidation).
2. Its **cardinality** depends on how many external agents respond. Whether they agree or conflict determines the ERW Rule-12 consolidation method entirely. A plan authored today would guess the shape of evidence that has not arrived.

What that replan will require, in order, by path and ERW rule number:

- Capture of each returned report as `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_results/<agent>-resolution.md` (ERW Rule 12 naming convention; Rule 14 makes the round root the durable record).
- The mandatory **ERW Rule 19** per-claim in-repo verification report under `docs/work/reviews/milestone_v2.3/54-recalibration-decision-grounding/`, date-prefixed, carrying the `docs/` frontmatter block. Rule 19: every repo-derived claim arrives as a checkable assertion and is verified with the verification recorded **before** any claim informs a decision, a roadmap, or a spec edit. Worked example the runbook cites: `docs/work/reviews/milestone_v2.1/45-trainex-r2-erw-package-assembly/2026-07-24-trainex-r2-report-factw-verification.md`.
- The **ERW Rule 12** consolidation into `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/trainex-r3-resolution-doc.md`, using the join points already recorded in `DELIVERY-NOTE.md` (ERW Rule 11).
- **Owner checkpoint ②** — per-surface disposition plus SCOPE-38 re-ratification of each locked contract the ruling amends, recorded in `.planning/phases/54-recalibration-decision-grounding/54-RULING.md`. The pre-declared completeness rule already in that file remains in force. The consolidated decision sheet is a candidate presented for ratification, never the ratification itself (SCOPE-34). Only the owner fills checkpoint ②.
- Only then does `GAP-54-01` move out of `OPEN`, Phase 54 close, and Phase 56 open.

At the close of this plan, `GAP-54-01` stays `OPEN` in both registers and Phase 56 stays closed.

`GAP-54-01` grep (neither register edited):

- `.planning/phases/54-recalibration-decision-grounding/54-GAPS.md:42` — `**Status:** OPEN`
- `.planning/milestones/v2.3-GAPS.md:11` — `OPEN (checkpoint ① discharged 2026-08-21 — commission trainex-r3; checkpoint ② pending)`

## Standing bars at plan close

Commands that themselves contain Bar F / Bar G3 vocabulary are recorded in fenced blocks so the Task 2 cost-scan gate (which drops fences, then strips backticks) does not trip on the recording of a command this task required.

Check R1 (canonical):

```
R3=pinn_instruction/markdown_conversion/framework-specs/trainex-r3
A=$(find "$R3" -type f | LC_ALL=C sort)
E=$(printf '%s\n' \
  "$R3/DELIVERY-NOTE.md" \
  "$R3/research_package/RESEARCH-AGENT-PROMPT.md" \
  "$R3/research_package/RESEARCH-CONTEXT-MASTER.md" \
  "$R3/research_package/v2.2-closure-evidence-bundle.md" \
  "$R3/specs/framework-specs-bundle.md" | LC_ALL=C sort)
[ "$A" = "$E" ] && echo MANIFEST-OK || echo MANIFEST-FAIL
```

Output: `MANIFEST-OK`. `research_results/` does not exist.

Check R2:

```
R3=pinn_instruction/markdown_conversion/framework-specs/trainex-r3
D=$(grep -m1 -E '^- \*\*Date:\*\*' \
     .planning/phases/54-recalibration-decision-grounding/54-RULING.md \
     | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')
echo "discharge=$D"
for p in DELIVERY-NOTE.md \
         research_package/RESEARCH-CONTEXT-MASTER.md \
         research_package/RESEARCH-AGENT-PROMPT.md \
         research_package/v2.2-closure-evidence-bundle.md \
         specs/framework-specs-bundle.md; do
  echo "$p $(git log --diff-filter=A --format='%ad' --date=short -- "$R3/$p" | tail -1)"
done
```

Output: `discharge=2026-08-21`; `DELIVERY-NOTE.md 2026-08-20`; `research_package/RESEARCH-CONTEXT-MASTER.md 2026-08-20`; `research_package/RESEARCH-AGENT-PROMPT.md 2026-08-21`; `research_package/v2.2-closure-evidence-bundle.md 2026-08-21`; `specs/framework-specs-bundle.md 2026-08-21`.

**R2 limitation (from 54-06):** for the three ERW-02 paths the introducing commit is `11b4e0c1`, which also introduced the discharge record `54-RULING.md`. Both sides of the comparison are that one day. R2 is consistent with post-gate provenance without demonstrating it. The verbatim owner instruction at `54-RULING.md:19` is the evidence that does.

| Check | Command | Output | Verdict |
|---|---|---|---|
| Bar D | `git diff --stat -- pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/sampling_method.md pinn/ simulation_data/ tests/` | empty | PASS |
| Bar E (canonical two-path; this plan does not re-scope it) | `git diff HEAD --stat -- .planning/REQUIREMENTS.md .planning/ROADMAP.md` | empty | PASS |
| Bar F | fenced command below | 0 | PASS |
| Bar G1 | fenced command below, selector `S` as in 54-06 | `G1-REGION=13`; remainder after token strip empty | `BAR-G-CLEAN` |
| Bar G2 | fenced command below | empty | PASS |
| Bar G3 | fenced command below | empty | PASS |
| No plan above 54-07 | `ls .planning/phases/54-recalibration-decision-grounding \| grep -E '^54-(0[89]\|[1-9][0-9])-PLAN\.md$'` | empty | PASS |
| Rule-19 review dir absent | `test ! -d docs/work/reviews/milestone_v2.3` | directory does not exist | PASS |
| Manual structural read of this file | read of `54-HANDOFF-READINESS.md` end to end | no sentence enumerates comparable alternatives for any decision surface; the transcription order of the five surfaces is not given weight | PASS — this file names no candidate value, no option menu, and no ordering of the surfaces |

Bar F command (fenced):

```
grep -ciE 'faster|slower|cheaper|quicker|days|weeks|hours|effort|simpler|harder|easier|more work|less work' \
  .planning/phases/54-recalibration-decision-grounding/54-RULING.md
```

Bar G shared stream and sub-bars (fenced; defined in `54-06-PLAN.md`):

```
P=.planning/phases/54-recalibration-decision-grounding
V=$(cat "$P/54-06-PLAN.md" "$P/54-07-PLAN.md" \
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

Recorded: `G1-REGION=13`; G1 remainder empty; G2 empty; G3 empty; gate literal `BAR-G-CLEAN`.
