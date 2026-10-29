# Phase 65 Probe Prediction: the 2026-10-27 exploratory probe, on the record

**Status:** committed historical expectations, reading rule and limitations,
registered before the first original rerun (D-02). Machine expectations:
`evidence/probe/expectations.json` (this page's SHA-256 is recorded inside it).
Preserved originals and scoped output: `evidence/original/` under this phase
directory. No rerun has happened at the time of this registration; plan 65-05
performs the real seven-arm reproduction under this committed gate.

## What is on the record

The 2026-10-27 exploratory probe measured the locked 12-layer diagnostic
network at CPU float64 seed-42 initialization ("init") and the committed
Phase 60 trained states of all seven arms, on each arm's own Stage-0 training
orbit, and printed:

- the all-arm table (`toolu_01NHGWRv6pEQCJmqeAXxqonK`, 2026-10-27T14:14:01.814Z):
  14 rows — `init` plus each arm's original `better_state` choice (adam on the
  four sweep arms, r1-4658 and r1-851; polish on r1-1632) — with the
  first-layer frequency (median, `.2f`), the centred neighbour cosines after
  hidden layers 1 and 2 (`.3f`), the min/max cosine range over hidden layers
  3..12 (`.3f`), the output movement (`.4f`) and the labelled output-rate
  comparator (`.3g`);
- the single-arm r1-1632 output (`toolu_01PUFNWxrDDsVrU8DTCH4tX3`,
  2026-10-27T14:12:02.670Z): frequency median and max (`.2f`), per-boundary
  adj-cos for `in` and h1..h12 (`.4f`), output movement (`.4f`) and rate
  (`.3g`) for the init, Adam and polish states — the Adam/polish supplement is
  registered separately from the all-arm table and its individual h3 values
  (adam `0.0186`, polish `0.0177`) are never merged into the all-arm range
  token `0.018`.

The original scripts are preserved byte-exact
(`probe_time_signal.py` SHA-256 `16db5c8c…a4f`,
`probe_all_arms.py` SHA-256 `a4dea7d0…c8`), together with the complete verbatim
text of exactly those two tool outputs and a source manifest recording the
extraction source, message identifiers, timestamps, byte counts and SHA-256
values, including the recovery provenance of the lost scratchpad originals.
The scripts are never imported or executed by any check.

## Historical vs runtime distinctions (D-04)

The rerun's initialization is a **reconstruction**: CPU float64, seed 42. The
historical training ran on MPS float32; a matching seed does not establish
identical initial weights across runtimes, and this registration never
describes the reconstruction as the historical training initialization.
Recorded trained states load only after their committed record and weight
SHA-256 agree (`weights_only=True`, CPU map location). The all-arm selected
state follows each record's committed `better_state`; the single-arm Adam and
polish comparisons stay distinct from it.

## Measurement definitions (D-05)

One shared implementation, `measure_time_signal`, serves the probe and the fit
logger — never a copied reduction. Feature-wise centring across time samples;
cosine of successive centred rows at the torch default epsilon; first-layer
frequency `abs(w_time) * omega_0 / pi` cycles per normalized window; output
movement as the centred output norm over the centred gold norm; the output-rate
comparator is the RMS of the network's autograd d/dtau over the RMS of
`torch.gradient` of the gold targets in the same normalized tau coordinate —
a labelled comparator, not a physical velocity claim. Adjacent gold samples
are physically 0.01 apart; that says nothing about normalized-tau spacing.
Samples are never sorted, merged or dropped; identical centred vectors keep
the original torch-epsilon behaviour; layer identities and both time
coordinates are recorded.

## The reproduction rule (immutable after observation)

Reproduction of a registered field is **exact formatter equality**: the
measured value must render, under the field's original formatter, to the
preserved token. Formatters: all-arm frequency `.2f`, all-arm cosines and
range `.3f`, all-arm output movement `.4f`, all-arm rate `.3g`; single-arm
frequency `.2f`, adj-cos `.4f`, output `.4f`, rate `.3g`. The `.3g` formatter
omits trailing zeros (`1.9e+08` is three-significant-digit rounding); counting
visible digits would widen acceptance and is never done. Before any rerun,
every token's exact rounding cell — the first and last representable doubles
that render to the token, as float hex with boundary inclusion and the excluded
`nextafter` neighbours — is recorded in the expectations and cross-checked
against the formatter; signed zero (`-0.000` vs `0.000`), decimal-midpoint
ties (round-half-even) and exponent changes sit inside these cells. No
tolerance is widened after results.

### Reading rule

1. Every registered **available** historical numeric field reproduces or is
   marked `not_reproduced`.
2. All required fields reproduced keeps the exploratory association on record
   — verdict `retained`.
3. Any failed required comparison **withdraws the lead** — verdict
   `withdrawn` — and yields a SCOPE-49 proposal to the owner. The rule is not
   repaired by editing it; a change requires a separately named investigation.
4. A figure whose original source output is absent is a **provenance
   limitation**, separately reported — never a fabricated failure or success.
   Missing output is not a failed reproduction (D-03).
5. A field the one shared measurement cannot produce — the single-arm
   `moving`, `spike` and skip/siren columns — is preserved verbatim with its
   own formatter and reported separately (`preserved_only`); no second
   reduction is created to compare it.
6. Individual deep-layer values the original output never printed (all arms
   except r1-1632, whose init/Adam/polish per-layer values are historical)
   are recorded as `new_measurement` entries with raw values and deltas to the
   registered range — not invented historical targets.
7. Low mean neighbour cosine is a measured association only. It does not
   establish information loss, a capacity limit or the cause of failure (D-07).

## Run gates (synthetically proven in this plan)

`require_committed_registration` admits only a committed-clean registration —
git tracked/clean checks scoped to its own enumerated artifacts (page,
expectations, source manifest/scripts/stdout, arm records, code dependencies,
frozen scorer/scorecard, the pinned run protocol revalidating all 33 frozen
sources), exact byte digests, ancestor-commit proof, and arms in stable
committed-record path order — before any data resolution, weight
deserialization or attempt creation. An unrelated dirty file elsewhere in the
repository is not a refusal reason. The run claims its attempt exclusively;
concurrent or repeated output paths refuse; an interrupted attempt stays
explicitly incomplete and never replaces a result; there is no automatic
numerical retry; a complete run returns a complete evidence record even when
figures fail; `verify-result` recomputes the reading rule, checks the
registered branch, and verifies historical dependencies against the recorded
run commit rather than requiring later source bytes to remain identical. A
probe-only interlock refuses optimizer construction and steps, counts
attempted steps (zero on a complete run) and compares parameter digests around
every measurement. `check-registration` is read-only: it reports the
registration commit and hashes and makes zero corpus or weight opens.
