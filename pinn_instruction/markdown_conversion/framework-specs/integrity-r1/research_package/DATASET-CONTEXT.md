---
title: Integrity R1 Dataset Context — Verified Facts About the Frozen Training Dataset
package_for: integrity-r1 (framework integrity audit round)
role: curated dataset-facts companion — every entry carries a per-fact status label
status: active
created: 2026-06-12
self_contained: true
---

# Dataset Context — Verified Facts About the Frozen Training Dataset

This file gives you the empirical reality of the project's training dataset so you can
check every dataset assumption the framework specs make against what is actually on
disk. It is a curated transcription: every figure was either verified by direct
read-only probes against the dataset (run 2026-06-11) or is explicitly labeled as an
unverified claim. **You do not have the dataset itself** — this file is your only
dataset evidence. Where it is silent, record the gap in your open-items register; do
not estimate or invent dataset facts.

## Status-label vocabulary

Every entry below carries exactly one of these labels:

- **`verified-empirically`** — confirmed by a direct read-only probe over the full
  on-disk dataset (probe run date 2026-06-11), recorded re-derivably in the project's
  verified-facts register. Treat as fact.
- **`claimed-unverified`** — stated in project documentation but never confirmed by a
  probe. Treat as a claim; if a spec leans on it, that reliance is itself a finding.
- **`corrected-by-DATA-07`** — a figure that earlier project documents stated and that
  empirical verification *corrected*. The entry shows both the superseded claim and the
  corrected value; the corrected value is the verified fact. The "DATA-07 correction
  addendum" is the project's authoritative correction record for these.

One additional qualifier appears on a few entries: **(post-remediation)**. A validated
data remediation was executed on 2026-06-11 *after* some of the documents embedded in
`KNOWN-ISSUES-AND-IN-FLIGHT-BUNDLE.md` were written, and it changed a small number of
counts. Post-remediation values are the current disk truth; the superseded values are
listed in the "Figures that moved" table at the end so you can recognize stale citations
in the bundle documents.

## Hard frame: the dataset is frozen

The dataset is complete and will not be regenerated — this is an explicit project
decision (a Tier-1 fixed fact per `RESEARCH-CONTEXT-MASTER.md`), not a probed figure, so
it carries no empirical label. The generation pipeline (documented in
`sampling_method.md`) has finished its job; the only post-freeze change ever made was
the validated 70-file remediation described below (`verified-empirically`), which
replaced corrupted artifacts from the *existing* generation contract — it did not extend
or re-sample the dataset. Any audit finding whose only resolution is "generate different
data" is a one-way-door finding and must be flagged as such.

## Dataset identity and variants

The training data is a set of three-body trajectory files produced by the Brutus
arbitrary-precision N-body integrator, in four variant collections
(`verified-empirically`, except where noted):

| Variant collection | Files | Role |
|---|---|---|
| `brutus_hierarchical` | 4,857 | Base-resolution hierarchical-IC trajectories |
| `brutus_hierarchical_gold_standard` | 4,857 | Gold (high temporal resolution) reruns of the same hierarchical ICs |
| `brutus_standard_quasi_random` | 2,749 | Base-resolution quasi-random-IC trajectories |
| `brutus_standard_quasi_random_gold_standard` | 2,565 | Gold reruns of a subset of the standard ICs |
| **Total trajectory files** | **15,028** | |

- File naming: all four collections use the base filename prefixes
  (`brutus_hierarchical_XXXX.txt`, `brutus_standard_XXXX.txt`) where `XXXX` is a
  4-digit zero-padded numeric ID. Gold-standard status is encoded **only** by the
  folder, never the filename. `verified-empirically` — 0 of 7,422 gold files carry any
  `_gold_` infix. (An earlier package claim that gold filenames carry a `_gold_` infix
  is `corrected-by-DATA-07`.)
- IC ↔ trajectory mapping is by numeric ID within the corresponding folder pair.
- The IC files: `ic_hierarchical_XXXX.txt` / `ic_standard_XXXX.txt`. The standard IC
  folder holds 2,749 ICs; the 2,565 gold-standard ICs were a byte-identical subset
  (the separate gold IC folders have since been removed from disk; historical note,
  `verified-empirically` for the counts).

## ID structure: IDs are not indices

- **Non-contiguous IDs are intentional** (generation continuation, prescreen rejection,
  failed runs). The numeric ID is NOT an array index. `verified-empirically`:
  - Standard: n = 2,749 files, ID range 0000–3998, **1,250 gaps** in [0..max].
  - Hierarchical: n = 4,857 files, ID range 0000–4999, **143 gaps** in [0..max].
- Nominal IC counts "~4,000 standard / ~5,000 hierarchical" are consistent with the
  observed max IDs (3,998 / 4,999) at the stated `~` precision. `verified-empirically`
  (at stated precision).
- **184 standard IDs have no gold counterpart** (simulated at base resolution, never
  selected for gold re-simulation). The documented 184-ID list matches the on-disk set
  exactly: base 2,749 − gold 2,565 = 184. `verified-empirically`.

## Blacklist

- A blacklist file `problematic_ics_blacklist.json` exists with **65 IDs total
  (2 hierarchical + 63 standard)**. Count and composition: `verified-empirically`.
- **Consumption status is a separate, open question.** Verified for the data-generation
  side: the dataset's readiness-check tooling loads the JSON; the current Brutus batch
  runners do **not** load it (the dataset README calls the JSON "legacy … not used by
  current runners"). Whether anything at *training* time loads it is
  `claimed-unverified` — it was explicitly out of the verification probes' scope, and
  the project's specs are currently silent on a blacklist-consumption contract (an
  in-flight adjudication topic; see the in-flight register in the bundle file).

## Brutus run parameters per variant

`dt_out` in these files is the **output sampling interval**, not the integrator's
internal (adaptive) step size. `verified-empirically` unless noted:

**Folder-default parameters** (apply when a file has no footer):

| Variant | Default tol | Default dt_out |
|---|---|---|
| Standard quasi-random (base) | 1e-13 | 0.17 |
| Hierarchical (base) | 1e-15 | 0.08 |
| Gold standard (both) | 1e-13 | 0.01 |

**Footer reality.** Most files end with a `Result:` footer carrying the full parameter
schema (`tol`, `Lw`, `dt_out`, `t_end`, `eta`); a subset has **no footer and no
parameter fields anywhere in the file** — for those, the folder defaults above must be
assumed. (Earlier package text called these "partial"/"minimal" footers;
`corrected-by-DATA-07` — they have no footer at all.) Current per-variant footer
populations:

| Variant | With full footer | No footer at all |
|---|---|---|
| `brutus_hierarchical` | 3,377 **(post-remediation)** | 1,480 **(post-remediation)** |
| `brutus_hierarchical_gold_standard` | 4,857 | 0 |
| `brutus_standard_quasi_random` | 2,048 | 701 |
| `brutus_standard_quasi_random_gold_standard` | 2,346 | 219 |

Observed footer parameter tuples `(tol, Lw, dt_out, t_end, eta) → count`,
`verified-empirically`:

- `brutus_hierarchical`: `(1e-15, 130, 0.08, 10, 0.263027) → 3,307`, plus the 70
  validated 2026-06-11 replacement files (same run contract — tol=1e-15, Lw=130,
  dt_out=0.08, t_end=10 — all 70 carry full footers; final time 10.000000000000007,
  126 snapshots each).
- `brutus_hierarchical_gold_standard`: `(1e-13, 130, 0.01, 10.01, 0.277971) → 4,146`;
  `(1e-13, 124, 0.01, 10.01, 0.277971) → 649`; `(1e-14, 118, 0.01, 10.01, 0.270396) → 34`;
  `(1e-14, 112, 0.01, 10.01, 0.270396) → 27`; `(1e-14, 124, 0.01, 10.01, 0.270396) → 1`.
- `brutus_standard_quasi_random`: `(1e-13, 118, 0.17, 10.03, 0.277971) → 1,126`;
  `(1e-13, 130, 0.17, 10.03, 0.277971) → 922`.
- `brutus_standard_quasi_random_gold_standard`: `(1e-13, 130, 0.01, 10.01, 0.277971) → 1,754`;
  `(1e-14, 130, 0.01, 10.01, 0.270396) → 592`.

Note the in-folder heterogeneity these tuples imply: the standard-gold folder mixes
tol=1e-13 and tol=1e-14 runs; the hierarchical-gold folder mixes three word lengths and
two tolerances; `t_end` varies (10 / 10.01 / 10.03) because `dt_out` does not always
evenly divide the nominal stop time.

## Snapshot counts per trajectory

`verified-empirically`; integer-rounded **median** is the project's locked authoritative
statistic. The issue doc's "~59 / ~125 / ~1000" figures are `corrected-by-DATA-07`:

| Variant | Median | Mode | Min | Max | n (footer-bearing probe population) |
|---|---|---|---|---|---|
| Standard (base) | **61** | 61 | 59 | 61 | 2,048 |
| Hierarchical (base) | **127** | 127 | 126 | 127 | 3,307 (pre-remediation probe; the 70 replacement files have 126 snapshots, within the observed range) |
| Standard gold | **1003** | 1003 | 1002 | 1003 | 2,346 |
| Hierarchical gold | **1003** | 1003 | 1003 | 1003 | 4,857 |

The dataset README explicitly warns against hard-coding exact snapshot counts. Any spec
text that assumes a fixed per-trajectory point count should be checked against this
distribution — including what a points-per-trajectory batch rule does at 59–61
snapshots versus 1003.

## Completeness

- The documented completeness rule is **`final_timestep >= 9.5`**. Rule:
  `verified-empirically` as the documented convention.
- Prevalence: **100 % of the probe-applicable population** reaches
  `final_timestep >= 9.5` (standard base 701/701 of the no-footer subset, modal final
  time 10.03, one file at 9.86 minimum; standard gold 219/219, modal 10.01;
  hierarchical base 1,550/1,550 at the probe date, all at 10.00; hierarchical gold not
  probed — its 1,003-snapshot layout was outside the probe parser).
  `verified-empirically` for the probed populations; the hierarchical-gold prevalence
  is `claimed-unverified`.

## Mass-consistency remediation (the "DATA-05" event) — full lifecycle

This is the one place the frozen dataset changed after its freeze. All states below are
`verified-empirically`:

1. **Discovery (2026-06-11):** a full-population probe (all 15,028 IC↔trajectory pairs)
   found **70 of 4,857 `brutus_hierarchical` files** whose t=0 masses did not match
   their IC files (`np.allclose(rtol=1e-15)`; differences 0.1–1.0 in mass units — far
   too large for float64 round-trip). Affected IDs: 0005–0059 and 0061–0075. The gold
   variant of the *same* IDs matched perfectly (0/4,857), isolating the fault to stale
   base-variant artifacts, not the ICs.
2. **Decision:** current IC files are canonical; the 70 base-hierarchical outputs were
   declared invalid/stale artifacts requiring targeted rerun; quarantined from
   training and metrics in the interim. Explicitly *not* a numeric-precision /
   Decimal-parsing problem.
3. **Remediation (2026-06-11, executed and validated):** all 70 reruns from the current
   ICs under the original run contract passed validation gates (mass equality at
   float64, full t=0 state match, final time reached, schema valid); old artifacts were
   hash-manifested and archived to a forensic location outside the live dataset;
   replacements swapped in; derived metrics for the 70 IDs regenerated and validated
   (energy-conservation relative error 2.2e-16 – 5.1e-14).
4. **Current state:** post-swap re-probe shows **0 mismatches across all 15,028
   pairs**. All quarantines are lifted. The live hierarchical folder again holds 4,857
   files.

Audit relevance: (i) the *current* dataset has exact IC↔t0 mass consistency at float64
everywhere; (ii) any document in the known-issues bundle that treats the 70-file
quarantine as open, or cites a mass-drift population, predates the remediation;
(iii) the event is evidence about dataset provenance fragility that an
assumptions/risk-register review (RD-8) may legitimately weigh.

## Dataset size

- Final-stage IC datasets ~59 MB; Brutus output datasets ~4.8 GB; total ~4.86 GB.
  `claimed-unverified` (documented in the dataset README; never probe-verified; no
  audit question is expected to turn on it).

## Figures that moved after the bundle documents were written

The documents embedded in `KNOWN-ISSUES-AND-IN-FLIGHT-BUNDLE.md` were written against
earlier states of knowledge. When you see these figures there, substitute the current
value from this file:

| Stale figure (appears in bundle docs) | Current verified value | Why it moved |
|---|---|---|
| ~59 / ~125 / ~1000 snapshots per trajectory | medians 61 / 127 / 1003 | empirical correction (DATA-07) |
| 1,550 hierarchical-base files without footer | 1,480 | 70 replacement files carry footers (post-remediation) |
| 3,307 hierarchical-base files with footer | 3,377 | same remediation |
| 70-file mass-drift quarantine "open" / "pending rerun" | remediation executed, validated, swapped; 0/15,028 mismatches | remediation completed 2026-06-11 |
| "Partial"/"minimal" footers | no footer at all (folder defaults apply) | empirical correction (DATA-07) |
| Gold filenames carry `_gold_` infix | no infix; folder encodes gold status | empirical correction (DATA-07) |

## What this file is not

- It is **not** a grounding source for spec edits and carries no design positions — it
  is dataset evidence only.
- It does **not** restate the project's locked screening gate or physics conventions —
  those live in the specs and in `RESEARCH-CONTEXT-MASTER.md` (three-tier source
  treatment).
- Sources referenced here by name (dataset README, probe register, correction addendum)
  are **not attached**; this file is the curated transcription of them. Treat any other
  dataset figure you encounter in the bundle documents as a claim unless it appears
  here as `verified-empirically`.
