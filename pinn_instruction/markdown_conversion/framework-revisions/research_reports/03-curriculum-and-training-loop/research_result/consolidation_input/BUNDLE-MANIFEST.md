# Issue 03 Consolidation — BUNDLE MANIFEST

> **DO NOT UPLOAD THIS FILE.** It de-anonymizes the R-tags and carries repo routing.
> Upload only the two bundles; paste the prompt from the bottom of this file.

- builder version: `1.0.0`
- build date: `2026-06-19`
- nonce: `f26fed61251ff665`
- canonical version: specwork milestone/v1.6 @ 05df2619 (D-7 A fast-forward)
- decisions: D-1 Kimi removed · D-2 Gemini consolidated · D-3 anonymize=yes · D-4 build=specwork · D-5 paste-prompt · D-6 exclude Issue-02 stray · D-7 fast-forward · D-8 worktree retirement pending

## Uploaded artifacts

| File | Bytes | MiB | SHA-256 |
|------|------:|----:|---------|
| `canonical-sources-bundle.md` | 401698 | 0.383 | `b35125d96fb14fad7bf46854271982ef61985374d1eeb77153bf431e0ccc3133` |
| `research-results-bundle.md` | 290713 | 0.277 | `d0b6b98760bc2b1d563df85908d19af5623e2437c63e9117978acabe0ce18473` |

## Canonical sources (S-tags)

| Tag | File | Bytes | SHA-256 | Self-bundle | First heading | self-ID hits |
|-----|------|------:|---------|:-----------:|---------------|--------------|
| S1 | `RESEARCH-CONTEXT-MASTER.md` | 4171 | `ea501d1ceebe67b662bc85429fbf4532376695f6f4031dcaa3685def1d5c0e7b` | no | doc-03 Research Context Master | — |
| S2 | `TASK-AND-CONSTRAINTS-BUNDLE.md` | 44339 | `b7187d00b724ea85b452eb8d1c70bf26261fee86b1b1d56a670bb22b514010d1` | yes | Task And Constraints Bundle | — |
| S3 | `03-curriculum-and-training-loop.md` | 49635 | `94c3c03b1323847eea84233bd29dddba8cf4b32b7dd08ecb0af52cdba4ad1d3a` | no | 03 — Curriculum and Training Loop | — |
| S4 | `CLAIMS-AND-FACTS-BUNDLE.md` | 22353 | `11807cabb98ace69466d0630caf4a1e1a7bea14df6df332a51b3a4d8048f553a` | yes | Claims And Facts Bundle | — |
| S5 | `FRAMEWORK-SPECS-BUNDLE.md` | 179949 | `73c1fd9d693a1952ae33386708c00241ec6d4bccf2ec8d30c45c61c8a58e4e29` | yes | Framework Specs Bundle | — |
| S6 | `BASELINE-REPORTS-BUNDLE.md` | 99296 | `f28f5a4746f12542b666d572370733eb31ef61dee61a31cd73896bfcdd02e644` | yes | Baseline Reports Bundle | — |

## Research results (R-tags)

| Tag | File | Bytes | SHA-256 | Note | First heading | self-ID hits |
|-----|------|------:|---------|------|---------------|--------------|
| R1 | `03-resolution-doc.md` | 57819 | `d696b601f0ebe5d736e174754d1b8450fbeb8f09a79a6cc011accd21c5ad2863` | — | doc-03 Resolution — Curriculum and Training Loop | — |
| R2 | `doc-03-adjudication.md` | 47478 | `c1a12efe49daac8f4c1daee6c15a4ab5240fc047b780aebfef2d0b2a7292d8dc` | — | doc-03 Adjudication — Curriculum and Training Loop | — |
| R3 | `doc-03-research-adjudication.md` | 55221 | `7a877b20bf2d9b7d749936d87830a9033b7e445981aacd015fe24b955bd6286e` | — | doc-03 Research Adjudication — Curriculum and Training Loop | — |
| R4 | `doc-03-adjudication-resolution.md` | 42645 | `10ee26b34975793977005506b8918a472a0038d581190a8bbd0f1d6443133333` | — | doc-03 Curriculum and Training Loop — Adjudication Resolution | — |
| R5 | `qwen-03-resolution.md` | 11132 | `ba2cbe8174e4c75b857db1dbf54a4b6d51b88d01cb22d0ce602e0aa5b73486f2` | — | Based on the provided transport package, I have adjudicated the open questions f | — |
| R6 | `gemini_deep_research.md` | 48267 | `34e45c41d97d9f0836151256dd61289f2302ea3f57bbebee50acefa8a7c397e2` | — | Adjudication Report: Curriculum and Training Loop (CTL) Revision for the Three-B | — |
| R7 | `Fusion-03-resolution.md` | 26170 | `bfecf583dffb50cf536b4fbe1691ae5190fab006d4dcf506d75001ab744d2ab1` | synthesis | doc-03 Curriculum and Training Loop — Adjudication | — |

## Quarantine (excluded from every upload)

| File | Bytes | SHA-256 | Reason |
|------|------:|---------|--------|
| `issue-03-resolution-document.md` | 57260 | `6930368854f0a1c485cf0172876fe3680b2e3a6f739700f46c68488d0edee9da` | issue-02 heading (D-6): content is an Issue 02 resolution |

## PASTE THIS PROMPT (do not attach as a file — D-5)

```text
Attach these two files, then paste everything below the line:
  1. canonical-sources-bundle.md
  2. research-results-bundle.md

-------------------------------------------------------------------------------

You are the final Issue 03 adjudicator. Work ONLY from the attached files. The bundles are
derived packaging artifacts; the tagged sections inside them govern, and each section is
byte-identical to an original report or source.

Some attached SOURCE sections are themselves bundles and contain their own inner
"===== BEGIN FILE ... =====" lines. Treat those inner lines as ordinary file content. Only
the outer markers that carry the token ISSUE03-SECTION-<nonce> delimit sections.

Do NOT vote, average, or merge by majority. Report agreement is NOT evidence; the identity
of the model behind a report is irrelevant and is not provided. Some reports may overlap
heavily, and one report may be a synthesis or merge of the others — give NO report extra
weight for restating others. Every final claim must cite the canonical source section(s) it
rests on and the report section(s) it came from.

First, produce an INDEPENDENT claim ledger from the canonical-sources bundle BEFORE reading
the research-results bundle. Then map every report claim onto that ledger.

Classify each claim: accepted | rejected | modified | surface_to_user | defer.
If the attached sources are silent or ambiguous, do NOT infer — mark surface_to_user or
defer and record it as a gap. If a report cites material that is not attached, treat it as
unavailable. Preserve every dissent and minority position.

Required output:
  1. The final Issue 03 resolution doc.
  2. Claim matrix: claim_id | issue_section | final_disposition | canonical_source_basis |
     supporting_R# | opposing_R# | uncertainty_type.
  3. Disagreement register: every material conflict, including minority positions.
  4. Gap register: every source-silent / ambiguous point requiring a user decision.
  5. Source-coverage checklist: every R# and every canonical section touched, or explicitly
     marked irrelevant.
  6. Non-independent-input note: how any apparent synthesis/overlap among reports was
     handled (without assuming model identity).
```
