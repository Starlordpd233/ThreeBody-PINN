# Evidence Packet: D-03 - Processed Training-Data Format

## Header

| Field | Value |
|---|---|
| ID | `D-03` |
| Title | `Processed training-data format (HDF5 vs .npy/.npz vs txt/json)` |
| Severity | `MAJOR` |
| Current Status | `VERIFIED` |
| Current Verdict | `accept-resolution` (USER-LOCKED 2026-06-13 via the PIPE-10 mandatory gate (D-11); the user selected HDF5 canonical — the §3.6 Q-A6 candidate; NOT auto-selected) |
| Phase | `Phase 26` |
| Acceptance Check ID | `AC-PIPE-10` |
| Spec Sections Touched | `ctl_instruction.md` Step 1 item 6 (ALONE — D-03 names ctl, no architecture-side component). Replaced in P26-05 Task 3 to name HDF5 as the user-locked canonical store + round-trip acceptance clause. |
| Code Paths Touched | `Not code-applicable` (spec-only; data round-trip is FUT-01) |

## Source Positions

Side-by-side line-range citations from both primary Issue 02 sources. Both required even for an uncontested verdict (D-04 §2). The two sources do NOT disagree here — both endorse HDF5 as primary; this packet is a requirement-mandated USER format gate (PIPE-10 / D-11), not an EVID-10 source conflict.

| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` | `§3.6 Q-A6:345-382` (verdict 347-352; reasoning 354; evidence 356; confidence + flip factor 358; verification suggestion 360; proposed spec text 362-377; provenance 379) | *recommends-change*. Both HDF5 and `.npy` are spec-compliant; `txt`/`json` as a primary store is outside the recommendation (347). **Candidate recommendation:** (1) HDF5 canonical — groups `/{variant}/{fidelity}/{id}`, float64 datasets, per-group §2.6 metadata + `param_provenance` + raw-file SHA-256 + `schema_version`, chunked+compressed (349); (2) `.npy`/`.npz` acceptable as a derived cache/export, awkward as a sole store for ragged arrays + rich metadata (350); (3) JSON/text inspection-and-debugging-only, never a training input path (351); (4) methodology consequences — float64 end-to-end bitwise round-trip, auditability, determinism (352). |
| `pinn_instruction/issues/02-data-pipeline-and-validation.md` | `:27-49` (ROUTINE D-03 block; Options A/B/C at 41-44); deeper format discussion `:173-187` and `:264-275` | `[ROUTINE]` D-03, "Conflict with current SOT: No — the SOT already recommends HDF5/.npy" (31). Asks the framework owner to confirm HDF5 primary, `.npy` as acceptable alternative, and optionally add JSON export for inspection only (39). Options: A keep HDF5 primary (42); B add `.npy` acceptable alternative (43); C supplemental optional JSON export for inspection/debugging only, not training (44). Deeper discussion frames the same trade-off: HDF5 advantages vs "No HDF5 library dependency" (187), recommends keeping HDF5 for the performance-critical training store + optional JSON inspection export (275). |

Neither source is authoritative before adjudication. The substance of both converges on HDF5-primary; the open question routed to the user is the format LOCK, including any unstated operational constraint (see Verdict / flip factor).

## Spec Evidence

Current framework-spec text that defines the convention being decided:

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md` Step 1 item 6, **current lines 406-410** (re-verified verbatim at authoring time; the 26-RESEARCH "374-378" anchor is from an earlier revision and shifted after Plan 26-01 inserted Step 1 item 7): *"Save parsed objects for all simulations into an efficient format like HDF5 or NumPy (.npy) files. This avoids repeated text parsing and accelerates loading during training..."* — i.e., the current spec names **both HDF5 and `.npy` as compliant** with no lock between them and no JSON guardrail. This is the text the user's chosen format will replace in Task 3.
- `pinn_instruction/markdown_conversion/framework-specs/pinn_architecture.md`: NOT touched. D-03 names `ctl_instruction.md` ALONE (no architecture-side component; `24-ISSUE-LEDGER.md` D-03 row Spec Targets = ctl alone).
- `data_quality_assessment.md` (SCOPE-09 read-only): not applicable to the format decision.

### Dataset Evidence (§3b)

EVID-06's fourth source — `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md`. The Q-A6 block itself carries no dataset facts (`02-resolution-doc.md:357`); the evidence to PRESENT at the user gate is the dataset SCALE and the ragged-array nature that bears on format fit:

- **CLM-10** (`24-VERIFIED-FACTS.md:25`, DATA-06): per-trajectory snapshot-count distributions (integer-rounded MEDIAN authoritative per lock 2026-06-11) — `brutus_standard_quasi_random` median **61** (n=2,048; min 59 max 61); `brutus_standard_quasi_random_gold_standard` median **1003** (n=2,346); `brutus_hierarchical` median **127** (n=3,307); `brutus_hierarchical_gold_standard` median **1003** (n=4,857). Snapshot counts vary by ~17× across variants (61 → 1003), so per-trajectory arrays are **ragged** — the data model is `variant → fidelity → id → ragged arrays + per-record metadata`.
- **Dataset scale** (`24-VERIFIED-FACTS.md:35`, DATA-05 "Total compared: 15,028"): **15,028 total trajectory files** across the 4 variants (4,857 + 2,749 + 2,565 + 2,346 by fidelity/variant counts elsewhere in the annex). At this scale, a one-array-per-file format (`.npy`) implies ~15k files plus a sidecar metadata index, whereas the ragged-arrays-plus-metadata model maps directly onto HDF5 groups/datasets/attributes.

These are the verified facts the user weighs; the agent presents them and does NOT convert them into a chosen format.

## FUT-01 Hand-off Note (formerly "Code Evidence")

Live code in `pinn/` is NOT a v1.5 evidence source (user directive 2026-05-19); this section is forward-pointing only. Once the user locks a format in Task 3, FUT-01 builds the actual processed-data store + DataLoader and implements the bitwise float64 round-trip acceptance test (resolution-doc §3.6 part 5, `02-resolution-doc.md:360`). The v1.3-era `pinn/data-processing-pipeline-full.py` already emits HDF5 output (issue-doc :35) — recorded here as a forward-pointing reference for FUT-01 to reconcile against the user-locked spec text, NOT as grounding for this verdict.

## First-Principles Physics Check

Not an EVID-10 finding (the two primary sources do not disagree; `24-ISSUE-LEDGER.md` D-03 row is not flagged Sources-Disagree=YES). The one numerical fact bearing on the decision is presented for the user, not used to force a verdict: **float64 end-to-end matters** because the stored arrays feed every Q-B3 metric, and float32 storage would inject ~1e-7 relative noise — within sight of the tightest data tolerances (`02-resolution-doc.md:352`). This is a property the chosen format's round-trip clause must guarantee (bitwise float64), independent of WHICH container the user selects. It does not by itself select HDF5 over `.npy` (both can hold float64); it only rules OUT a lossy/text-coerced primary store.

## Verdict

**`accept-resolution`. USER-LOCKED 2026-06-13.**

**User-decision provenance (T-26-20 mitigation):** the format was **user-locked 2026-06-13 via the PIPE-10 mandatory gate (D-11); the user selected HDF5 canonical (the §3.6 Q-A6 candidate); it was NOT auto-selected.** PIPE-10 (`REQUIREMENTS.md:56`, verbatim: *"The training-data format decision (D-03: HDF5 vs .npy vs txt/json) is presented to the user with verified evidence; the user decides; the locked choice is recorded in the framework specs."*) mandates this as a USER gate, and D-11 forbids any execution mode (including `--auto`/yolo) from selecting the format. The Task-2 `checkpoint:decision` (gate=blocking) presented the three options (`hdf5-canonical` / `npy-npz` / `txt-json`) + the verified evidence (dataset scale, current spec text, the candidate, the unstated-operational-constraint flip factor); the user explicitly selected `hdf5-canonical`. Because the user adopted the resolution-doc §3.6 Q-A6 candidate position, the verdict enum is `accept-resolution`. No overriding operational constraint was supplied (no HDF5-dependency prohibition), so the candidate stands unmodified.

Task 3 transcribed the candidate spec text (`02-resolution-doc.md:362-377`) into `ctl_instruction.md` Step 1 item 6 (current lines 406-426): HDF5 canonical single source of truth (groups `/{variant}/{fidelity}/{id}`, float64 datasets, per-group §2.6 metadata + `param_provenance` + raw-file SHA-256 + `schema_version` + transform metadata, chunked+compressed, partial reads by group); `.npy`/`.npz` an acceptable derived cache/export preserving the identical schema; JSON/text inspection-and-debugging-only and never a training input path; plus a bitwise float64 round-trip acceptance clause (incl. times; data round-trip is FUT-01).

**Candidate recommendation (NOT a selected verdict — presented for the user to accept, modify, or reject):** the resolution-doc §3.6 Q-A6 position — HDF5 canonical (groups `/{variant}/{fidelity}/{id}`, float64 datasets, per-group §2.6 metadata + `param_provenance` + raw-file SHA-256 + `schema_version`, chunked+compressed) as the single source of truth; `.npy`/`.npz` as a derived cache/export preserving the identical schema; JSON/text inspection-and-debugging-only and never a training input path (`02-resolution-doc.md:347-352, 362-377`).

**The only verdict-flipping factor (the exact reason this is a USER call):** an *unstated operational constraint forbidding HDF5 dependencies* (`02-resolution-doc.md:358`). The resolution doc rates its own confidence High and names this single factor as the one thing that would flip the primary to `.npy` + sidecar index without touching the JSON guardrail or the float64 round-trip clause. Such a constraint (e.g., a deployment/runtime environment that cannot take an `h5py` dependency) is information only the user/framework owner can supply — the agent cannot observe it from the corpus, so the format cannot be auto-selected.

## Root-Cause Framework Ambiguity

Not applicable as an EVID-10 source conflict. The "ambiguity" is not a disagreement between the two primary sources — both endorse HDF5-primary. The decision is open solely because (a) the requirement mandates a user lock (PIPE-10) and (b) one verdict-flipping operational constraint (HDF5-dependency prohibition) lives outside the corpus, with the user. The current spec's permissive "HDF5 or NumPy (.npy)" wording (no lock, no JSON guardrail) is the spec-side gap the user's choice closes.

## Locked Convention

**LOCKED (user, 2026-06-13): HDF5 is the canonical processed-training-data store.** `ctl_instruction.md` Step 1 item 6 (lines 406-426) now reads: processed training data is stored in HDF5 (single source of truth) — groups `/{variant}/{fidelity}/{id}`, float64 datasets (`times`, `positions`, `velocities`, masses, §2.6 derived arrays), per-group attributes carrying the full §2.6 metadata (including `param_provenance`), raw-file SHA-256 hashes, a top-level `schema_version`, and the build's transform metadata (`D`, `T`, `V`, `E_scale` + scale provenance) so raw values are exactly re-derivable; chunked+compressed; partial reads by group. `.npy`/`.npz` is an ACCEPTABLE derived cache/export alternative preserving the identical schema, but the HDF5 file is the single source of truth. JSON/text exports are inspection- and debugging-only and MUST NEVER be a training input path. Round-trip acceptance clause: raw → HDF5 → arrays round-trips bit-identically in float64 against direct parsing for a sample of trajectories, including times (data round-trip is FUT-01; the spec clause is the acceptance contract).

## Which Source Was Correct / Wrong

Not applicable (no source conflict). Both primary sources converge on HDF5-primary with `.npy` acceptable and JSON inspection-only; the resolution doc adds the precision/auditability/determinism clauses (§3.6 part 4) that make the position spec-grade and corrects the issue doc's "methodology impact: zero" to "zero *iff* the float64 bitwise round-trip clause holds" (`02-resolution-doc.md:354`). The user's 2026-06-13 selection of `hdf5-canonical` adopts the resolution-doc candidate verbatim; the resolution doc's spec-grade framing (with the round-trip clause that ties storage to metric validity) is the recorded correct position. No source was wrong here — the gate existed because of the PIPE-10 user-lock requirement and the externally-held operational-constraint flip factor, not a source disagreement.

## Before / After Spec Note

**Affected section:** `ctl_instruction.md` Step 1 item 6 (current lines 406-410), ALONE — no `pinn_architecture.md` edit (D-03 names ctl alone).

**Before:** "Save parsed objects ... into an efficient format like HDF5 or NumPy (.npy) files" — both compliant, no lock between them, no JSON guardrail, no round-trip acceptance clause.

**After (applied P26-05 Task 3, user-locked 2026-06-13):** item 6 now names **HDF5 as the canonical, single-source-of-truth processed-training-data store** (groups `/{variant}/{fidelity}/{id}`, float64 datasets, per-group §2.6 metadata + `param_provenance` + raw-file SHA-256 + `schema_version` + transform metadata, chunked+compressed, partial reads by group), scopes `.npy`/`.npz` as an ACCEPTABLE derived cache/export preserving the identical schema, scopes JSON/text as inspection-only and never a training input path, and adds a bitwise-float64 round-trip acceptance clause (incl. times). The choice is attributed in-spec to the user decision ("user-locked 2026-06-13"). `pinn_architecture.md` was NOT touched (D-03 names ctl alone).

## Named Acceptance Check

**AC-PIPE-10** (spec-consistency). No new AC-ID minted (Phase 26 mints none; D-13). Reserved-name policy `AC-{REQ-ID}` → `AC-PIPE-10` (PIPE-10).

**Pass criterion (Phase 26 scope, spec-consistency probe):** after Task 3, `ctl_instruction.md` Step 1 item 6 (a) names the user-selected format (HDF5) as the locked processed-training-data store, and (b) carries a round-trip acceptance clause (bitwise float64 round-trip incl. times). The data round-trip itself (parse raw → write store → read back → bitwise `np.array_equal`) is **FUT-01**, not Phase 26 (`02-resolution-doc.md:360` is the FUT-01 design). The Phase-26 probe is a grep/parse spec-consistency check, command + output captured re-derivably below per D-15, run in Task 3.

**Exact command + captured output (re-derivable, D-15) — run 2026-06-13 post-edit:**

```
$ SPEC=pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
$ grep -nE 'stored in HDF5 \(the canonical|single source of truth|schema_version|round-trips|bit-identically|round-trip' "$SPEC"
406:6.  Processed training data is stored in HDF5 (the canonical, single
412:    `schema_version`, and the build's transform metadata (`D`, `T`, `V`,
417:    the HDF5 file is the single source of truth. JSON/text exports are
423:    Acceptance test (round-trip): raw → HDF5 → arrays round-trips
424:    bit-identically in float64 against direct parsing for a sample of
425:    trajectories, including times. (The data round-trip implementation is
$ if grep -qE 'stored in HDF5 \(the canonical' "$SPEC" && grep -qiE 'round.?trip|bit-identical' "$SPEC"; then echo PASS; else echo FAIL; fi
PASS
```

**Result: AC-PIPE-10 PASS** — Step 1 item 6 names HDF5 as the locked canonical store AND carries a bitwise-float64 round-trip acceptance clause.

**Chain regression re-checks (D-08; Step-1 region neighbors).** The item-6 expansion shifted downstream line numbers but disturbed no neighboring contract content:
- **AC-PIPE-01** (Step-1A admission gate): `## Step 1A` + `final_timestep >= 9.5` + `SCS > -5` present at 452/471/477; the rejected `>= 200` floor remains rejected (494-495), not reintroduced. **PASS, no regression.**
- **AC-PIPE-02** (`id_to_path` / `record_key`): the scan-built contract, the `^brutus_(hierarchical|standard)_(\d{4})\.txt$` regex, and the "never equal to an array index" invariant remain intact at 429-441. **PASS, no regression.**
- **AC-PIPE-06** (footer-as-metadata / `param_provenance`): the footer-metadata-only contract (359/392) and the D7 `param_provenance` home (814) are intact; the new 411 `param_provenance` hit is the §2.6 reference inside the new item-6 HDF5 attribute list, not a duplicate of the D7 contract. The dataset half (`data04_footers.py` over 15,028 files) is unchanged by a spec edit and was captured in the D7 packet; not re-run. **PASS, no regression.**

## Status Transition Log

Each entry: `date`, `commit short SHA`, `status transition`, `actor / plan reference`.

```text
2026-06-13 (uncommitted — awaiting user gate) PENDING -> IN_PROGRESS (Phase 26 P26-05 Task 1 by agent; D-03 packet authored, candidate + verified evidence presented, NO verdict selected)
2026-06-13 <26-05-SHA> IN_PROGRESS -> FIX_APPLIED (Phase 26 P26-05 Task 3; user selected hdf5-canonical at the PIPE-10 gate (D-11); ctl_instruction.md Step 1 item 6 replaced to name HDF5 canonical + round-trip acceptance clause)
2026-06-13 <26-05-SHA> FIX_APPLIED -> VERIFIED (Phase 26 P26-05 Task 3; AC-PIPE-10 PASS — item 6 names HDF5 + round-trip clause; AC-PIPE-01/02/06 regression re-checks PASS, no regression)
```

> The three transitions above share the single atomic `26-05` commit SHA (`<26-05-SHA>` to be backfilled). Per D-11/D-08 the packet + `ctl_instruction.md` Step-1-item-6 edit + ledger transition to VERIFIED + README map row all travel in that one commit. D-03 has NO synthesis (G) row to close.
