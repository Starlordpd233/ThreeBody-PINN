---
phase: 22
slug: framework-spec-cleanup
artifact: comment-handoff
status: committed
created: 2026-06-09
owner: FUT-05 (post-v1.4 adjudication)
consumes:
  - .planning/phases/22-framework-spec-cleanup/22-COMMENT-CENSUS-PRE.md
  - .planning/phases/22-framework-spec-cleanup/22-COMMENT-CENSUS-POST.md
  - .planning/phases/22-framework-spec-cleanup/22-COMMENT-DIFF.md
---

# Phase 22 Author-Comment Handoff (for FUT-05 adjudication)

> **PRESERVE-AND-DEFER NOTICE.** This document is an **inventory-only handoff** from Phase 22 to
> **FUT-05** (post-v1.4 phase). Phase 22 performs **NO basis classification**, **NO adjudication**,
> **NO keep/remove/revise/resurface verdict**, and **NO deletion** on any author comment. All of that
> is FUT-05's work per `.planning/REQUIREMENTS.md` FUT-05 and design §6. Phase 22's only job is to
> (a) census every author-flagged comment in any form/format across the three framework specs,
> (b) prove every comment survived WS-A edits verbatim (or with a documented mechanical D-05 wrapper
> repair only), and (c) hand the inventory to FUT-05 cleanly. This document is the handoff.

**Census basis (all-forms marker set):** `Author Comment`, `Author note`, `Historical author note`,
`\authcomment`, and the derived `**[Author Comment: …]**` bold-bracketed form recognized by design §6.1 step 1
(SI-PINN-002 cross-reference).

**Re-derived at execution:** 2026-06-09 against live HEAD 7fe572e (post-WS-A).

**Total comments: 26** (ctl: 13, pinn: 13, sampling: 0)

**Preservation verdict:** 0 lost, 0 semantically changed. 23/26 hashes byte-identical between PRE
and POST; 3/26 carry documented D-05 mechanical wrapper repairs (surrounding prose syntax
normalized by 22-02 math cleanup; the author-comment clause itself byte-identical in all 3).
Full evidence: `22-COMMENT-CENSUS-PRE.md`, `22-COMMENT-CENSUS-POST.md`, `22-COMMENT-DIFF.md`.

---

## Inventory

| # | form | file | section/anchor | verbatim text | preservation-verified |
|---|------|------|----------------|---------------|-----------------------|
| 1 | Author note | ctl_instruction.md | multi-stage-data-stratification-by-difficulty-revised-to-handle-the-issue-that-virial-ratio-is-not-preserved-for-quasi-random-ic-sampling | "> **Author note:** I have a suggestion: how about we give the entire IC files a scan > using some algorithms and analyze the gathered data from there, to first > get an insight on what the data looks like, and then we can decide on > the criteria for each stage? This will be a good starting point > considering that simply designing the criteria based on theoretical > values might not be the best way to go espesically since my IC sampling > method is complicated -- virial ratio is not preserved for quasi-random > IC sampling." | ✓ |
| 2 | Author Comment | ctl_instruction.md | phase-1-data-preparation-and-stratification | "Author Comment: I believe this is another case for broken syntax or stale code from conversion. Also, this not estatement itself is outdated since all the code in the code folder is already outdated and unusuable." | ✓ |
| 3 | Author Comment | ctl_instruction.md | 2-5-global-scaling | "Author Comment: so far all the inline math notations that have this format `xxxx` are rendered as literal text strings in the preview and are not readable. Consider changing this syntax in a way that is machine-reading friendly and also renders correctly and nicely for human reader reading in preview." | ✓ |
| 4 | Author Comment | ctl_instruction.md | outputs-of-this-step | "Author Comment: this section is a syntax disaster. ALl the raw latex syntax are broken in rendered preview, and they show up as literal text strings. The other syntax are also incorrect for proper markdown file. Carefully look into this and think about how to fix it. Maintaining the exact, identifical math equation and expressions is of the utmost importance here. The following sections after this and below this should also be carefully examined." | ✓ |
| 5 | Author note | ctl_instruction.md | outputs-of-this-step | "> **Author note:** We need the code snippets here for this." | ✓ |
| 6 | Author note | ctl_instruction.md | outputs-of-this-step | "> **Author note:** The two paragraphs below are suspicious. We need to carefully > examine them." | ✓ |
| 7 | Author note + Historical author note | ctl_instruction.md | scope | "> **Historical author note (pre-Phase 17; retained as a non-normative > question):** Confirm that all components in the IC vector are in the > range $[-1,1]$ and that it is the final form that will be fed to the > PINN." | ✓ |
| 8 | Author note + Historical author note | ctl_instruction.md | scope | "> **Historical author note (pre-Phase 17; retained as a non-normative > question):** Confirm on this mathematcial guarantees' arguments and the > numerical implementation's purpose and validity. If confirmed, how > should we integrate and implement this into the existing workflow? > Also, we have to add the time t into this vector to achieve the > final 14-dimensional input vector ready to be fed to the PINN." | ✓ |
| 9 | Author Comment | ctl_instruction.md | network-input-contract | "Author Comment: again the syntax issues here above in the `` format are all broken and need fixing." | ✓ |
| 10 | Author note + Historical author note | ctl_instruction.md | phase-2-the-definitive-ctl-pinn-training-loop | "> **Historical author note (pre-Phase 17; retained as a non-normative > question):** My biggest question now for this training loop is that: how are we > feeding the exact input vector and brutus simulation data into the > network? … what is the network ultimately doing? … is the ouptut file going to > be something similar to a brutus output file, sort of acting as a > replacement for the brutus algorithm?" | ✓ |
| 11 | Author note | ctl_instruction.md | stage-transition-criteria | "> **Author note:** Now, for this, we will need to look at how the first stage goes > when the actual process starts. … Based on this, how should we handle the stage transition criteria > depending on the actual situations that might happen? Should we first > test train stage 0 and see how it goes and then go from there?" | ✓ |
| 12 | Author note | ctl_instruction.md | evaluation-metrics-and-validation | "> **Author note:** Should we also use the same definition here for the Lyapunov time from section 2.3 'Necessary Calculations of Invariants'?" | ✓ |
| 13 | Author Comment | ctl_instruction.md | reproducibility-note-ignore-now-and-come-back-later | "- `stage.yaml` -- curriculum definition and data-set indices\\ (Author Comment: why is there a \"\\\" sign here and in the next line?)" | ✓ |
| 14 | Author Comment | pinn_architecture.md | 1-foundational-architectural-principles-a-co-designed-approach-for-chaotic-systems | "Author Comment: Again, all the superscript instances are rendered as raw literal strings in the preview. Fix this carefully." | ✓ |
| 15 | Author Comment | pinn_architecture.md | 2-2-a-principled-initialization-scheme-for-siren-layers | "Author Comment: All of these fields with `\\text{xxx}` are not rnedered correctly and show up in the preview as raw literal text strings. The examples are the hidden omega 0, and first omega, etc." | ✓ |
| 16 | Author Comment | pinn_architecture.md | 2-4-finalized-architectural-hyperparameters | "Author Comment: I'm not sure why this section is formatted like this. It looks like broken syntax to me and it displays in the preview simply as a paragraph. Look into this." | ✓ |
| 17 | Author Comment | pinn_architecture.md | 3-the-multi-component-physics-constrained-loss-function | "Author Comment: the above formula is not written in the correct syntax. We need to fix it so that it will be rendered correctly in markdown preview in Cursor." | ✓ |
| 18 | Author Comment | pinn_architecture.md | 3-the-multi-component-physics-constrained-loss-function | "Author Comment: the above canonical text form is also rendered in raw text strings in preview." | ✓ |
| 19 | Author Comment | pinn_architecture.md | 3-1-data-fidelity-term-mathcalltextdata-anchoring-to-ground-truth | "Author Comment: again, the syntax is broken" | ✓ |
| 20 | Author Comment (bold-bracketed form) | pinn_architecture.md | 3-1-data-fidelity-term-mathcalltextdata-anchoring-to-ground-truth | "**[Author Comment: This above batch construction is not consistent with the CTL instruction plan. Look into this.]**" | ✓ |
| 21 | Author Comment ⚠ D-05 wrapper repair | pinn_architecture.md | 3-4-soft-energy-conservation-regularizer-le-enforcing-a-global-conservation-law | "$\\epsilon_{train} = 10^{-5}$. (Author Comment: I am not sure why there is a duplicate 10^-5 here)Persist both $S_H$ and $\\epsilon_H$ in training metadata. …" — comment clause byte-identical; surrounding prose normalized: `` `10^-5` ``→`$10^{-5}$`, `epsilon_H`→`$\\epsilon_H$`, `<=`→`$\\leq$` | ✓ (comment clause preserved; wrapper repaired under D-05) |
| 22 | Author Comment ⚠ D-05 wrapper repair | pinn_architecture.md | 3-4-soft-energy-conservation-regularizer-le-enforcing-a-global-conservation-law | "- **Softening Parameter:** The same value $\\epsilon_{train} = 10^{-5}$ (author comment: again duplicate number) is used consistently in both the physics residual and energy calculations to prevent numerical instabilities during close encounters." — comment clause byte-identical; surrounding prose `` `10^-5` `` → `$10^{-5}$` | ✓ (comment clause preserved; wrapper repaired under D-05) |
| 23 | Author Comment ⚠ D-05 wrapper repair | pinn_architecture.md | 4-2-optional-alm-ablation-p2 | "- **Constraints:** $c_E = \\mathrm{RMS}_n(\\Delta H_n)$ (energy drift), $c_{L,\\alpha} = \\mathrm{RMS}_n((L'_{\\theta,\\alpha}(u_n) - L'_{0,\\alpha}) / L_{scale})$ (angular momentum drift per component). (Author Comment: this syntax is not ideal since it invovles math equations/formula; it should properly use correct markdown render-friendly syntax)" — comment clause byte-identical; surrounding prose raw-subscript math → LaTeX | ✓ (comment clause preserved; wrapper repaired under D-05) |
| 24 | Author Comment | pinn_architecture.md | si-pinn-002-author-comments-preserved-in-converted-body | "### SI-PINN-002: Author comments preserved in converted body" (meta-doc heading; see negative-control note below) | ✓ |
| 25 | Author Comment + \\authcomment | pinn_architecture.md | si-pinn-002-author-comments-preserved-in-converted-body | "- **Description:** 3 author comments from the LaTeX source (`\\authcomment{}`) are preserved in the converted body as bold bracketed text (`**[...]**`). These are editorial notes from the original authors, not content discrepancies: 1. \"Need more detail on this dynamic scheduling for omega_0\" (Section 2) 2. \"Need confirmation on this hidden layer's detail\" (Section 2) 3. \"Comment: This above batch construction is not consistent with the CTL instruction plan\" (Section 3)" | ✓ |
| 26 | Author Comment | pinn_architecture.md | si-pinn-003-batch-construction-inconsistency-with-ctl-instruction-plan | "- **Description:** The author comment \"This above batch construction is not consistent with the CTL instruction plan\" flags a methodological inconsistency between the data sampling strategy described here and the CTL curriculum training plan. This should be investigated and resolved during training implementation." | ✓ |

---

## Negative-control note

**SI-PINN-002 meta-doc** (rows 24 and 25 above): The `### SI-PINN-002: Author comments preserved in converted body` heading and its Description bullet are enumerated in this inventory because they carry author-marker text (`Author Comment`, `\authcomment{}`), but they are **meta-documents**: they describe the preservation of other author comments rather than flagging a new issue. They are enumerated here for census completeness (the detector flags them as marker-bearing) and are **excluded from defect findings**. FUT-05 may wish to treat them as a special category during adjudication — Phase 22 takes no position.

**`sampling_method.md`**: 0 author comments found (negative control confirmed).

---

## Reconciliation

- **Committed PRE census:** `22-COMMENT-CENSUS-PRE.md` (26 entries, source_ref faa73d0)
- **Committed POST census:** `22-COMMENT-CENSUS-POST.md` (26 entries, source_ref 7fe572e)
- **Committed DIFF:** `22-COMMENT-DIFF.md` (26 ↔ 26 by stable-id; 23 hash-identical + 3 D-05 wrapper repairs)
- **Live census:** `node tools/spec-render-check/detect.mjs --census` re-derived on 2026-06-09 returns 26 (13 ctl + 13 pinn + 0 sampling).

**All three sources agree: 26 comments, 0 lost, 0 semantically changed.**

---

## FUT-05 ownership

FUT-05 consumes this handoff for per-comment adjudication under the design §6 disposition engine:
per-comment basis classification (GROUNDED-STALE / SURFACE / KEEP), git temporal grounding where
needed, and any deletion/revision/resurfacing verdict. Phase 22 deliberately expresses **no
position** on any of these. The ✓ column in this document means "verbatim-preserving confirmed by
Phase 22" — it does **not** mean "resolved" or "approved for retention".

**Boundary respected (GAP-22-01 resolved → Defer):** no basis class, no disposition, no
keep/remove verdict appears on any row.
