# Preamble Parity Verification Report

**Generated:** 2026-03-21 13:29:02
**Structures verified:** 5

## Summary

| Structure | Packages | Commands | Config Blocks | Status |
|-----------|----------|----------|---------------|--------|
| Data-quality-assessment | 11/11 | 2/2 | 1/1 | PASS |
| ctl-instruction | 15/15 | 4/4 | 4/4 | PASS |
| pinn-architecture | 15/15 | 1/1 | 3/3 | PASS |
| review_of_framework | 14/14 | 0/0 | 8/8 | PASS |
| stage_strat_revision | 13/13 | 1/1 | 8/8 | PASS |

## Detailed Results

### Data-quality-assessment

**Documentclass:** `\documentclass[11pt, a4paper]{article}` -- MATCH

#### Packages (PREAMB-01)

**Matched (11):** amsmath, amssymb, babel, booktabs, enumitem, fontenc, geometry, hyperref, inputenc, lmodern, xcolor
**Missing (0):** none
**Extra (0):** none
**Option mismatches (0):** none

#### Commands & Environments (PREAMB-02)

**Matched (2):** newcommand:\norm, newcommand:\vect
**Missing (0):** none
**Extra (0):** none
**Body mismatches (0):** none

#### Configuration Blocks (PREAMB-03)

**Matched (1):** hypersetup
**Missing (0):** none
**Extra (0):** none
**Content mismatches (0):** none

### ctl-instruction

**Documentclass:** `\documentclass{article}` -- MATCH

#### Packages (PREAMB-01)

**Matched (15):** algorithm, algpseudocode, amsmath, amssymb, booktabs, comment, float, geometry, hyperref, inputenc, listings, makecell, tikz, url, xcolor
**Missing (0):** none
**Extra (0):** none
**Option mismatches (0):** none

#### Commands & Environments (PREAMB-02)

**Matched (4):** DeclareMathOperator:\median, newcommand:\authcomment, newenvironment:authcommentenv, renewcommand:\theadfont
**Missing (0):** none
**Extra (0):** none
**Body mismatches (0):** none

#### Configuration Blocks (PREAMB-03)

**Matched (4):** geometry, hypersetup, lstset, usetikzlibrary
**Missing (0):** none
**Extra (0):** none
**Content mismatches (0):** none

### pinn-architecture

**Documentclass:** `\documentclass{article}` -- MATCH

#### Packages (PREAMB-01)

**Matched (15):** amsmath, amssymb, booktabs, comment, enumitem, float, geometry, hyperref, inputenc, listings, longtable, natbib, placeins, tabularx, xcolor
**Missing (0):** none
**Extra (0):** none
**Option mismatches (0):** none

#### Commands & Environments (PREAMB-02)

**Matched (1):** newcommand:\authcomment
**Missing (0):** none
**Extra (0):** none
**Body mismatches (0):** none

#### Configuration Blocks (PREAMB-03)

**Matched (3):** geometry, lstset, setcitestyle
**Missing (0):** none
**Extra (0):** none
**Content mismatches (0):** none

### review_of_framework

**Documentclass:** `\documentclass[11pt, a4paper]{article}` -- MATCH

#### Packages (PREAMB-01)

**Matched (14):** amsfonts, amsmath, amssymb, booktabs, caption, enumitem, float, geometry, graphicx, hyperref, inputenc, listings, longtable, xcolor
**Missing (0):** none
**Extra (0):** none
**Option mismatches (0):** none

#### Commands & Environments (PREAMB-02)

**Matched (0):** none
**Missing (0):** none
**Extra (0):** none
**Body mismatches (0):** none

#### Configuration Blocks (PREAMB-03)

**Matched (8):** definecolor(backcolour), definecolor(codegray), definecolor(codegreen), definecolor(codepurple), geometry, hypersetup, lstdefinestyle(mystyle), lstset
**Missing (0):** none
**Extra (0):** none
**Content mismatches (0):** none

### stage_strat_revision

**Documentclass:** `\documentclass[11pt, letterpaper]{article}` -- MATCH

#### Packages (PREAMB-01)

**Matched (13):** amsfonts, amsmath, amssymb, booktabs, caption, float, geometry, graphicx, hyperref, inputenc, listings, longtable, xcolor
**Missing (0):** none
**Extra (0):** none
**Option mismatches (0):** none

#### Commands & Environments (PREAMB-02)

**Matched (1):** newcommand:\authcomment
**Missing (0):** none
**Extra (0):** none
**Body mismatches (0):** none

#### Configuration Blocks (PREAMB-03)

**Matched (8):** definecolor(backcolour), definecolor(codegray), definecolor(codegreen), definecolor(codepurple), geometry, hypersetup, lstdefinestyle(pythonstyle), lstset
**Missing (0):** none
**Extra (0):** none
**Content mismatches (0):** none
