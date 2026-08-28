---
phase: 54
plan: 06
status: active
created: 2026-08-22
---

# 54-RECONCILIATION — ledger record of the 2026-08-21 out-of-band ERW-02 assembly pass

## Table-cell pipe convention

Every literal pipe character inside a recorded command in this file is written escaped as `\|`. This is not cosmetic. The empty-cell gate splits markdown table rows on the pipe character, so an unescaped shell `||` (Check R1) or an unescaped regex `|` yields an empty field and reports `EMPTY-CELL` on a correctly filled row. The repair is the escape, never deleting the command from the cell. This convention governs every later table in this file, including Section 5's re-derivation table, Section 6's amendment table, and Section 8's bar results.

## 1. Standing and non-authorization

Commits `11b4e0c1` and `ad51968e` landed on 2026-08-21 on branch `milestone/v2.3` outside the plan ledger under direct owner instruction, with no authorizing plan, no plan-checker pass, and no SUMMARY.

**This plan does not retroactively authorize them.** A plan written after the work is not a plan, and presenting it as an authorization would record a false sequence in the ledger.

What this plan authorizes is the **reconciliation**: recording what landed and when, retiring the guard the pass invalidated and installing a replacement, re-deriving by command every audit result the pass recorded by hand, verifying the packet's own amendment record against its cited sources, and correcting the phase accounting.

Both commits are ancestors of `HEAD` in this worktree. The precondition was asserted before any file was written:

| Check | Command | Result |
|---|---|---|
| ancestor `11b4e0c1` | `git merge-base --is-ancestor 11b4e0c1 HEAD` | exit 0 |
| ancestor `ad51968e` | `git merge-base --is-ancestor ad51968e HEAD` | exit 0 |

## 2. What landed

Derived with `git show --stat --format='%H%n%ad%n%s' --date=short <hash>`, not from memory.

### Commit 11b4e0c1

| Field | Value |
|---|---|
| Full hash | `11b4e0c12529efe993143c7dcd9eb08df9a213fd` |
| Author date | `2026-08-21` |
| Subject | `docs(54): discharge checkpoint one and assemble the trainex-r3 package` |
| Per-file statistics | `.planning/milestones/v2.3-GAPS.md` 2 +-; `.planning/phases/54-recalibration-decision-grounding/54-GAPS.md` 4 +-; `.planning/phases/54-recalibration-decision-grounding/54-RULING.md` 12 +-; `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/DELIVERY-NOTE.md` 72 +-; `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-AGENT-PROMPT.md` 167 ++++; `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md` 127 ++-; `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/v2.2-closure-evidence-bundle.md` 489 ++++++++++++; `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/specs/framework-specs-bundle.md` 877 +++++++++++++++++++++; 8 files changed, 1715 insertions(+), 35 deletions(-) |

### Commit ad51968e

| Field | Value |
|---|---|
| Full hash | `ad51968eaa37c246d0692bdd04c3ac381a4aa41e` |
| Author date | `2026-08-21` |
| Subject | `docs(54): stamp the rule-20 live-tree pin for the trainex-r3 handoff` |
| Per-file statistics | `pinn_instruction/markdown_conversion/framework-specs/trainex-r3/DELIVERY-NOTE.md` 4 ++--; 1 file changed, 2 insertions(+), 2 deletions(-) |

### Round-root resulting five paths

After both commits, the authorized round-root set under `pinn_instruction/markdown_conversion/framework-specs/trainex-r3` is exactly:

1. `DELIVERY-NOTE.md`
2. `research_package/RESEARCH-AGENT-PROMPT.md`
3. `research_package/RESEARCH-CONTEXT-MASTER.md`
4. `research_package/v2.2-closure-evidence-bundle.md`
5. `specs/framework-specs-bundle.md`

## 3. The retired guard

The two assertions being retired are quoted verbatim from `54-05-PLAN.md`. They are one of four named mitigations of threat **T-54-12** — *Elevation of privilege (scope) / ERW-02 work created pre-gate / high*. The four mitigations named in that threat row were: Bar C, the two-file tree-completeness check, the no-plan-above-54-05 check, and the absence of `docs/work/reviews/milestone_v2.3/`.

**Retired assertion 1 — `<verification>` block of `54-05-PLAN.md`:**

> ```
> find pinn_instruction/markdown_conversion/framework-specs/trainex-r3 -type f | sort
> ```
> → expected: exactly the two authored paths. A third path means an ERW-02 artifact
> was created against D-02 and D-11.

**Retired assertion 2 — `<acceptance_criteria>` line of `54-05-PLAN.md`:**

> Tree completeness: `find pinn_instruction/markdown_conversion/framework-specs/trainex-r3 -type f | sort` prints exactly two paths.

### Four reasons for retirement

1. The guard **fired correctly**. The tree holds five paths where it asserted two.
2. The threat it was written for **did not materialize** — but Check R2 alone does not establish that. T-54-12's threat is ERW-02 work created *pre-gate*. Checkpoint ① was discharged 2026-08-21 and commit `11b4e0c1` carries author date 2026-08-21 — but that same commit contains `54-RULING.md`, the discharge record itself, alongside three of the five round-root artifacts. Both sides of R2's comparison are therefore the same day, and `54-RULING.md:18` records a date with no time, so no finer comparison exists in the data. **R2 cannot falsify T-54-12 for `11b4e0c1`, and this record does not claim it can.** What establishes that the work was owner-directed and post-gate is the verbatim owner instruction recorded at `54-RULING.md:19`: *"let's do the r3 and assemble the research pacakge to be handed off to the external research agent. make sure that the information inlcuded in that package is accurate and faithful"*. That instruction is named here as the provenance evidence. R2's force falls on the two ERW-01 artifacts, whose introducing date is strictly earlier than the discharge, and on any artifact that appears at the round root later — for those the comparison discriminates.
3. What failed is that the guard **could not distinguish "post-gate but unplanned" from "pre-gate"** — a two-path count carries no provenance.
4. The guard was previously marked superseded **inside the document it protects**, via the packet's own `## 11` entry `A-10`, with no re-authorizing plan. That is the governance defect; retiring it here, in the ledger, with a replacement, is the repair. The packet's own `A-10` text is not withdrawn — it is superseded in turn by this record, and Task 2 adds a numbered amendment entry in the packet pointing here.

## 4. The replacement: Checks R1 and R2

Checks R1 and R2 together replace the retired tree-completeness assertion. Both are inherited by `54-07` and by any later plan in this phase.

### Check R1 — round-root authorized manifest

Compare the sorted list of files under `pinn_instruction/markdown_conversion/framework-specs/trainex-r3` against a literal five-path manifest, as a string, under `LC_ALL=C`. A count comparison is explicitly rejected (edge E5): a sixth file fails, a missing file fails, and a one-for-one substitution that preserves the count also fails.

| Check | Command | Recorded output | Failing run |
|---|---|---|---|
| R1 | `R3=pinn_instruction/markdown_conversion/framework-specs/trainex-r3; A=$(find "$R3" -type f \| LC_ALL=C sort); E=$(printf '%s\n' "$R3/DELIVERY-NOTE.md" "$R3/research_package/RESEARCH-AGENT-PROMPT.md" "$R3/research_package/RESEARCH-CONTEXT-MASTER.md" "$R3/research_package/v2.2-closure-evidence-bundle.md" "$R3/specs/framework-specs-bundle.md" \| LC_ALL=C sort); [ "$A" = "$E" ] && echo MANIFEST-OK \|\| { echo MANIFEST-FAIL; exit 1; }` | `MANIFEST-OK` | Four-path manifest (omitting `specs/framework-specs-bundle.md`): prints `MANIFEST-FAIL` and exits 1 |

### Check R2 — pre-gate / post-gate provenance

For each of the five paths, print the author date of the commit that introduced it, using `git log --diff-filter=A --format='%ad' --date=short -- <path> | tail -1`. The checkpoint ① discharge date is read out of `54-RULING.md` rather than hard-coded: `grep -m1 -E '^- \*\*Date:\*\*' .planning/phases/54-recalibration-decision-grounding/54-RULING.md | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}'` → `2026-08-21`.

| Path | Introducing-commit author date | Relation to discharge `2026-08-21` |
|---|---|---|
| `DELIVERY-NOTE.md` | `2026-08-20` | strictly earlier (ERW-01, authorized by plan `54-01` before the gate) |
| `research_package/RESEARCH-CONTEXT-MASTER.md` | `2026-08-20` | strictly earlier (ERW-01, authorized by plan `54-01` before the gate) |
| `research_package/RESEARCH-AGENT-PROMPT.md` | `2026-08-21` | on or after (ERW-02) |
| `research_package/v2.2-closure-evidence-bundle.md` | `2026-08-21` | on or after (ERW-02) |
| `specs/framework-specs-bundle.md` | `2026-08-21` | on or after (ERW-02) |

Command:

`R3=pinn_instruction/markdown_conversion/framework-specs/trainex-r3; D=$(grep -m1 -E '^- \*\*Date:\*\*' .planning/phases/54-recalibration-decision-grounding/54-RULING.md \| grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}'); echo "discharge=$D"; for p in DELIVERY-NOTE.md research_package/RESEARCH-CONTEXT-MASTER.md research_package/RESEARCH-AGENT-PROMPT.md research_package/v2.2-closure-evidence-bundle.md specs/framework-specs-bundle.md; do echo "$p $(git log --diff-filter=A --format='%ad' --date=short -- "$R3/$p" \| tail -1)"; done`

Recorded output: `discharge=2026-08-21` plus the five rows above.

A failing run shows an ERW-02 artifact dated before the discharge — which is T-54-12's threat — or an empty date, meaning the path is uncommitted.

**Limitation of Check R2 (stated immediately under the table).** For the three ERW-02 artifacts the introducing commit is `11b4e0c1`, which also introduced the discharge record `54-RULING.md`. Both sides of the comparison are that one day, and the ruling records a date without a time, so for those three paths R2 returns a result *consistent with* post-gate provenance without demonstrating it. This record does not present R2 as proof of post-gate provenance for them. The provenance evidence for those three is the verbatim owner instruction at `54-RULING.md:19`, quoted in Section 3. R2 discriminates for the two ERW-01 artifacts and for any path that appears at the round root later, which is the forward-looking job the replacement is installed to do — nothing more is claimed.

## 5. Re-derivation of the ERW-02 audit results

`MASTER=pinn_instruction/markdown_conversion/framework-specs/trainex-r3/research_package/RESEARCH-CONTEXT-MASTER.md`. Matching relations (edge E3): Bar A and Bar F are case-insensitive extended-regex; Bar B is a case-sensitive literal substring match on `trainex-r2`; snapshot fidelity is byte-for-byte string equality; pin consistency is exact equality over all forty hexadecimal characters (edge E4). Bar E is re-derived here in its **canonical two-path form** `git diff HEAD --stat -- .planning/REQUIREMENTS.md .planning/ROADMAP.md`; the Task 3 narrowing is not applied.

Region non-emptiness (edge E2) is asserted before every region-scoped negative grep. A zero-line region would be recorded as INERT and repaired, never as PASS.

| Check | Command | Re-derived | Recorded in the packet | Verdict |
|---|---|---|---|---|
| Bar A region guard | `sed -n '/NEUTRALITY-BAN-BEGIN/,/NEUTRALITY-BAN-END/p' "$MASTER" \| wc -l` | 301 lines (> 0) | not separately recorded | region non-empty |
| Bar A | `sed -n '/NEUTRALITY-BAN-BEGIN/,/NEUTRALITY-BAN-END/p' "$MASTER" \| grep -nEi 'recommend\|suggest\|prefer\|best\|most likely\|primary candidate\|default to\|should use\|ranked\|leading option'` | empty (grep exit 1) | §10 PASS empty; §11 PASS 0 hits | PASS — empty |
| Bar A2 region guard | `sed -n '/^## 9\. Output contract/,/^## 10\./p' "$MASTER" \| wc -l` | 28 lines (> 0) | not separately recorded | region non-empty |
| Bar A2 line count | `sed -n '/^## 9\. Output contract/,/^## 10\./p' "$MASTER" \| grep -cEi 'suggested default\|one-way\|two-way\|decision sheet'` | 4 matching lines (≥ 4) | §10 PASS 4 matching lines | PASS — reproduces §10 |
| Bar A2 occurrence count | `sed -n '/^## 9\. Output contract/,/^## 10\./p' "$MASTER" \| grep -oEi 'suggested default\|one-way\|two-way\|decision sheet' \| wc -l` | 11 occurrences (≥ 4) | §11 originally PASS 11 described as line-anchored | FAIL then repaired — §11 method did not reproduce 11 as a line count; corrected at source to record both numbers; new entry A-12 |
| Bar B region guard | `S0=$(grep -n '^## 0\.' "$MASTER" \| cut -d: -f1); S1=$(grep -n '^## 1\.' "$MASTER" \| cut -d: -f1); awk -v a="$S0" -v b="$S1" 'NR < a \|\| NR >= b' "$MASTER" \| wc -l` | 421 lines (> 0) | not separately recorded | region non-empty |
| Bar B | `S0=$(grep -n '^## 0\.' "$MASTER" \| cut -d: -f1); S1=$(grep -n '^## 1\.' "$MASTER" \| cut -d: -f1); awk -v a="$S0" -v b="$S1" 'NR < a \|\| NR >= b' "$MASTER" \| grep -n 'trainex-r2' \| grep -v 'r2-QUAL'` | empty (grep exit 1); case-sensitive literal substring | §10 PASS empty; §11 PASS 0 untagged | PASS — empty |
| Bar D | `git diff --stat -- pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md pinn_instruction/markdown_conversion/framework-specs/sampling_method.md pinn/ simulation_data/ tests/` | empty | §10 PASS empty | PASS — empty |
| Bar E | `git diff HEAD --stat -- .planning/REQUIREMENTS.md .planning/ROADMAP.md` | empty (canonical two-path form) | §10 PASS empty | PASS — empty |
| Bar F | `grep -ciE 'faster\|slower\|cheaper\|quicker\|days\|weeks\|hours\|effort\|simpler\|harder\|easier\|more work\|less work' .planning/phases/54-recalibration-decision-grounding/54-RULING.md` | 0 | §10 PASS 0 | PASS — 0 |
| Snapshot fidelity (Check 4) | For each `BEGIN VERBATIM` marker: range payload `path:a-b` compared with `git show 6a4f9b9902ab62e1d1f57bba0e521f38120c416d:path \| sed -n 'a,bp'`; bare-path payload compared with `git show 6a4f9b9902ab62e1d1f57bba0e521f38120c416d:path`; block body is the text between BEGIN and END with one leading blank after BEGIN and one trailing blank before END stripped; relation is byte-for-byte string equality | specs bundle: 10 blocks, 10 identical, 0 mismatched; v2.2 bundle: 3 blocks, 3 identical, 0 mismatched; total 13 blocks, 13 identical, 0 mismatched | §11 PASS 13 excerpts, 0 mismatches; delivery-note attachment table originally 13 for the specs file; obligations table 10 + 3 | PASS — 13/13 identical. Delivery-note attachment table attributed 13 to the specs file alone (actual 10); corrected at source; new entry A-15. Fail-demo: shifting the source range by one line yields mismatched=10 and mismatched=3 |
| Pin consistency (Check 6) | `python3` scan of all five round-root files for `\b[0-9a-f]{40}\b`; full forty-character equality, never a prefix | each of the five files has distinct_40hex=1 and the value `6a4f9b9902ab62e1d1f57bba0e521f38120c416d` | §11 originally "all four round files" naming master, delivery note, and both bundles | PASS over five files. Packet said four; omitted `RESEARCH-AGENT-PROMPT.md`; corrected at source; new entry A-13 |
| Baseline currency | `git diff --stat 6a4f9b99..HEAD -- pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md .planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md .planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-DIAG-05-REDERIVATION.md` | empty | §11 PASS empty | PASS — empty |
| Citation resolution | `grep -oE '[A-Za-z0-9_./-]+\.(md\|py):[0-9]+' "$MASTER" \| sort -u \| wc -l` then resolve each pair against the live tree | 52 distinct; 52/52 resolve; 0 out of range | §11 originally 49/49 with no command | FAIL then repaired — 52 ≠ 49; packet cell corrected at source with this command; new entry A-14 |
| Attachment count (Rule 15) | count of uploaded attachments named in the delivery-note attachment table and master §2 | 3 of at most 5 | §11 PASS 3 of at most 5 | PASS — 3 ≤ 5 |

## 6. Verification of the packet's amendment record

Existing `A-1` through `A-10` row texts are not edited. Corrections are appended as `A-11` through `A-16`.

| Entry | Class as recorded | Cited source | Re-derived verdict |
|---|---|---|---|
| A-1 | correction | `docs/work/reviews/milestone_v2.2/50-valid-stage-0-re-run/2026-08-17-residual-frame-conformance-audit.md:165` | CONFIRMED. The attributing sentence is: "A SIREN carries broadband high-frequency content by design (`first_omega_0 = 30`, ARCH-01, §2.2: \"a high initial frequency injects a high-frequency Fourier basis\"), and the 12-layer SQR-SkipResNet stack compounds it — the `LayerNorm(x)^p` skip branch with `p = 2` has Jacobian `2·LN(x)/std(x)` ≈ 3 per odd layer, six of them." Two causes, not one. |
| A-2 | correction | `.planning/milestones/v2.2-phases/52-diagnosis-re-derivation-handoff/52-VER-20-ROUTING-HANDOFF.md` item (e) | CONFIRMED. The authorizing sentence is: "It is a request to recalibrate one or more of: `η_c` / the causal-exponent form, an explicit normalization of `R̄` (e.g. by a converged-scale reference), or the SIREN initialization scale — or to redesign the curriculum mechanism so it does not require the two to already agree at initialization." The fourth remedy family (mechanism redesign) is in the source. |
| A-3 | addition | audit `:167` (Gate B residual 0.65 % of `‖a′‖`; `R̄ = O(1)` on a converged network) | CONFIRMED. The audit states: "The causal weight `exp(−η_c R̄)` with `η_c = 1` and an **unnormalized** `R̄` presumes `R̄ = O(1)`, which is what a *converged* network gives (Gate B: residual = 0.65 % of `‖a′‖` on a true trajectory)." |
| A-4 | verification | arithmetic on M1 transcribed medians; no new source | CONFIRMED as a self-check. No external source to quote. The packet's stated comparison is arithmetic on already-transcribed numbers. |
| A-5 | addition | `pinn_architecture.md:1017-1035` `## References` | CONFIRMED. `grep -c '^\[[0-9]\+\]' pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md` in that section yields 17 numbered entries; none names a causal-weighting scheme source. |
| A-6 | correction | `find . -name 'pinn_architecture.md' -not -path './.git/*' -exec wc -l {} \;` | DIVERGENCE then repaired. Live output: 1098 live spec; 1064 integrity-r2 snapshot; 1013 trainex-r1 snapshot; 1010 integrity-r1 snapshot; 1010 `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/research_package/specs/pinn_architecture.md`. Five paths, not four. A-6 row text left unchanged. §3 anchor-resolution rule corrected at source (Five files; fifth path added). New entry A-11. |
| A-7 | addition | master §5.7 as authored | CONFIRMED present: cross-cutting form requirements (capacity, residual range, source method, mechanism-redesign family, independent derivation). |
| A-8 | addition | master §6 `F-11`…`F-15` and §7 two new entries | CONFIRMED present: `F-11` through `F-15` exist; §7 carries the SQR-SkipResNet contribution and the source-method calibration silences. |
| A-9 | status | master §2 commissioned three-attachment list | CONFIRMED. §2 now states Status: commissioned and lists three uploaded attachments. |
| A-10 | status / verification | master §10 Bar C and Tree completeness rows | CONFIRMED as the packet's own supersession of the pre-commission bars. That supersession is itself superseded by this ledger record (Section 3 and Checks R1/R2). A-10 row text left unchanged. New entry A-16. |

## 7. Disk-derived accounting

These listings were taken during Task 3 **before** any SUMMARY for `54-06` or `54-07` existed. They are the single source `.planning/ROADMAP.md` and `.planning/STATE.md` are reconciled against. Neither document is copied from the other.

**Before counts** (recorded so the later transition to 0 is evidence the edit landed):

| Pattern | File | Before |
|---|---|---|
| `ERW-02 is deliberately unplanned` | `.planning/ROADMAP.md` | 1 |
| `ERW-02 artifact exists` (case-insensitive) | `.planning/STATE.md` | 1 |
| `ERW-02 work exists` (case-insensitive) | `.planning/STATE.md` | 1 |
| `ERW-02 is deliberately unplanned` (case-insensitive) | `.planning/STATE.md` | 1 |
| `last task of this execution pass` (case-insensitive) | `54-VALIDATION.md` | 1 |

**Counter semantics.** Frontmatter `total_phases` is `6`. `grep -cE '^### Phase [0-9]' .planning/ROADMAP.md` is `6`. They agree, so the STATE counters are **milestone-wide**. Therefore `total_plans` must equal the milestone-wide `*-PLAN.md` count.

The pre-existing `total_plans: 6` **was consistent with disk at the time it was last written** (2026-08-20): six plan files then (`53-01` plus `54-01` through `54-05`). It is no longer consistent, because `54-06-PLAN.md` and `54-07-PLAN.md` now exist. That is a derivation that corrects a previously-correct value after the tree grew, not a finding that the previous value was invented.

Command: `find .planning/phases -name '*-PLAN.md' | LC_ALL=C sort`

```
.planning/phases/53-narrow-spec-codification/53-01-PLAN.md
.planning/phases/54-recalibration-decision-grounding/54-01-PLAN.md
.planning/phases/54-recalibration-decision-grounding/54-02-PLAN.md
.planning/phases/54-recalibration-decision-grounding/54-03-PLAN.md
.planning/phases/54-recalibration-decision-grounding/54-04-PLAN.md
.planning/phases/54-recalibration-decision-grounding/54-05-PLAN.md
.planning/phases/54-recalibration-decision-grounding/54-06-PLAN.md
.planning/phases/54-recalibration-decision-grounding/54-07-PLAN.md
```

Length: **8**.

Command: `find .planning/phases -name '*-SUMMARY.md' | LC_ALL=C sort`

```
.planning/phases/53-narrow-spec-codification/53-01-SUMMARY.md
.planning/phases/54-recalibration-decision-grounding/54-01-SUMMARY.md
.planning/phases/54-recalibration-decision-grounding/54-02-SUMMARY.md
.planning/phases/54-recalibration-decision-grounding/54-03-SUMMARY.md
.planning/phases/54-recalibration-decision-grounding/54-04-SUMMARY.md
.planning/phases/54-recalibration-decision-grounding/54-05-SUMMARY.md
```

Length: **6**. This listing is the comparison basis for ROADMAP checked boxes. Phase-54 summaries in it: **5**. `grep -cE '^- \[x\] 54-0' .planning/ROADMAP.md` must equal 5. The appended `54-06` and `54-07` boxes are left unchecked.

Derived STATE `progress` values: `total_phases=6`, `completed_phases=1`, `total_plans=8`, `completed_plans=6`, `percent=17` (phase ratio `1/6`).

## 8. Plan-file neutrality bar (Bar G) and close-out re-runs

Preprocessing: fence markers balanced (`54-06-PLAN.md` 12 fences, `54-07-PLAN.md` 6 fences, both even). Concatenated raw line count 1647; retained stream `RETAINED=1568`; removed 79 (fenced code blocks, the planner-discipline allow-comment, and `<automated>` command lines). Retained count is above the floor of 200.

| Check | Command | Re-derived | Verdict |
|---|---|---|---|
| Bar G1 region cardinality | `printf '%s\n' "$V" \| grep -icE "$S"` with `S='eta_c\|η_c\|η\|first_omega_0\|omega_0\|ω₀\|n_col\|N_t\|collocation_count\|Rbar\|R̄\|normaliz\|reference scale\|clip\|clamp'` | `G1-REGION=13` | recorded with the gate verdict below |
| Bar G1 no candidate value | `printf '%s\n' "$V" \| grep -iE "$S" \| sed -E "s/($S)//gI" \| grep -E '[0-9]'` | empty | PASS |
| Bar G2 no ordering vocabulary | `printf '%s\n' "$V" \| sed 's/`[^`]*`//g' \| grep -inE 'recommend\|suggest\|prefer\|best\|most likely\|primary candidate\|default to\|should use\|ranked\|leading option'` | empty | PASS |
| Bar G3 no cost framing | `printf '%s\n' "$V" \| sed 's/`[^`]*`//g' \| grep -inE 'faster\|slower\|cheaper\|quicker\|days\|weeks\|hours\|effort\|simpler\|harder\|easier\|more work\|less work'` | empty | PASS |
| Bar G gate | Task 3 `<automated>` block over `54-06-PLAN.md` and `54-07-PLAN.md` | printed `RETAINED=1568 G1-REGION=13` then `BAR-G-CLEAN` | `BAR-G-CLEAN` |
| Manual structural read | read of `54-06-PLAN.md`, `54-07-PLAN.md`, `54-RECONCILIATION.md`, and the 54-07-planned `54-HANDOFF-READINESS.md` (not yet written) | no sentence enumerates comparable alternatives for any decision surface | PASS — neither plan file, nor `54-RECONCILIATION.md`, enumerates comparable alternatives; `54-HANDOFF-READINESS.md` does not exist yet and is bound by the same bar over `54-07-PLAN.md` |
| Check R1 at plan close | same five-path string-equality command as Section 4 | `MANIFEST-OK` | PASS |
| Check R2 at plan close | introducing-commit dates vs discharge date read from `54-RULING.md` | discharge=`2026-08-21`; ERW-01 paths `2026-08-20`; ERW-02 paths `2026-08-21` | PASS, with the Section 4 limitation: R2 cannot falsify T-54-12 for `11b4e0c1` |
| Bar D at plan close | `git diff --stat --` over the 54-01 spec/`pinn/`/`simulation_data/`/`tests/` paths | empty | PASS |
| Bar E at plan close (Task 3 narrowing) | `git diff HEAD --stat -- .planning/REQUIREMENTS.md` only | empty | PASS — narrowed because this task edits `.planning/ROADMAP.md` under plan authority, so the canonical two-path form is necessarily non-empty until the end-of-task commit, and the bar's result is recorded in this file which that same commit carries. The narrowing removes exactly the one file Task 3 is authorized to change. ROADMAP is guarded by the Phase-54-block confinement and unchanged heading count of 6. |
| Bar F at plan close | `grep -ciE` cost vocabulary over `54-RULING.md` | 0 | PASS |

Fail-demo (scratch copies, not the live plan files): a single G1 violating line `the eta_c value is 1` prints `the  value is 1`; a G2 line `I recommend this option as the leading option` prints that sentence; a G3 line `this path is cheaper and faster with less work` prints that sentence. Five-surface G1 injections all fire: `the eta_c coefficient is 1`; `the Rbar normalization uses a reference scale of 2`; `first_omega_0 is 30`; `n_col is 4096`; `the clip bound is 87`. Real-text G1 remainder after token strip is empty.
