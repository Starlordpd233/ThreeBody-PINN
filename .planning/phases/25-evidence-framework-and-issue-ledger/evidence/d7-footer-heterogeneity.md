# Evidence Packet: D7 - Footer / parameter heterogeneity

## Header

| Field | Value |
|---|---|
| ID | `D7` |
| Title | `Footer / parameter heterogeneity (footer-precedence, folder-default fallback, per-field provenance, footer-as-metadata-only)` |
| Severity | `MAJOR` |
| Current Status | `VERIFIED` |
| Current Verdict | `accept-resolution` |
| Phase | `Phase 26` (Plan 26-03) |
| Acceptance Check ID | `AC-PIPE-06` |
| Spec Sections Touched | `ctl_instruction.md` Step 1 item 3 (replacement); `ctl_instruction.md` §2.6 Assertions and stored metadata (amendment) |
| Code Paths Touched | `Not code-applicable` (data-side spec contract; FUT-01 implements) |

## Source Positions

| Source | Required Line-Range Citation | Position Summary |
|---|---|---|
| `pinn_instruction/markdown_conversion/framework-revisions/research_reports/02-data-pipeline-and-validation/02-resolution-doc.md` | `§3.5 Q-A5:294-343` (verdict 296-305; 6-clause contract 296-303; proposed spec text 315-341; confidence/OI-6 311; verification suggestion 313) | All-or-nothing footer model: present → full schema `(tol, Lw, dt_out, t_end, eta, energies)` provenance `direct`; absent → verified folder defaults provenance `inferred`, `eta` has no default → `null` provenance `absent` (fabrication prohibited); partial-schema footer = anomaly (`footer_anomalous=true`, default fallback); per-field `param_provenance` dict over `{tol, Lw, dt_out, eta}` ∈ `{direct, inferred, absent, measured}`; `dt_out` independently measured as median snapshot spacing (provenance `measured`), warn on >1% disagreement; footers are **never** a completeness signal (Q-A1) and **never** a mapping source (Q-A2). P2-1 accepted in mechanism, corrected in premise (no "minimal footers"; schema does not "vary" — presence does), generalized to per-field provenance. |
| `pinn_instruction/issues/02-data-pipeline-and-validation.md` | `:68` (D7 row), `:85` (footer-schema MAJOR row), `:291` (P2-1 `tol_confidence`), `:301` (footer handling), `:345` (mapping INFO) | D7 (`:68`): "219 standard gold files have minimal footers (no tol parameter)... use folder-level default 1e-13... add `tol_confidence` flag 'direct'/'inferred'... log count of inferred tolerances." Footer-schema row (`:85`): "prefer actual `Result:` values when present; fall back to folder defaults when absent; treat footer as metadata only — completeness gate uses final timestamp, not footer presence." `:301` "never fail on missing footer." `:345` mapping uses numeric ID, not footer paths. The issue doc's "minimal footer (no tol)" premise is factually wrong (D-07: no-footer files have NO `Result:` footer and NO parameter fields at all). |

BOTH citations are required even for uncontested verdicts (D-04 §2). Directory-qualified per the Phase-25 ID-namespace caution.

## Spec Evidence

Current framework-spec convention being changed/extended:

- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:351-360` — Step 1 item 3, the current "optional trailing `Result:` line (which may contain energies... extract these into metadata)" text. Treats the footer as an optional energies-metadata line only; no precedence/fallback/provenance contract.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:362-366` — Step 1 item 4, "`dt_out`: inferred from timestamps or defaults like 0.08/0.17" — already gestures at the timestamp-derived `dt_out` that the `measured` channel formalizes.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:395-396` — Step 1 item 7 (B-11, landed Plan 26-02): "`Result:` footer paths are never used for mapping." D7's mapping-negative defers to this existing clause.
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:423-425` — Step-1A clause 4 (B-06, landed Plan 26-01): completeness `final_timestep >= 9.5` "computed from parsed snapshot block times. Footer presence, line counts, and snapshot-count constants MUST NOT be used as completeness signals." D7's completeness-negative defers to this existing clause; the two must be consistent (they are — both state footer presence is never a completeness signal).
- `pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md:743-764` — §2.6 stored-metadata block, including `brutus_tolerance, word_length, dt_out, trustworthy_horizon` (`:763`). `trustworthy_horizon` is undefined anywhere in the package (OI-4) — kept RESERVED, not invented.

### Dataset Evidence (§3b)

EVID-06 fourth source — `.planning/phases/24-empirical-dataset-verification-and-correction-addendum/24-VERIFIED-FACTS.md`:

- `CLM-07:22` — 219 `brutus_standard_quasi_random_gold_standard` files have NO `Result:` footer at all AND NO parameter fields anywhere (D-07 characterization; **not** "partial/minimal footer"). Confirmed.
- `CLM-08:23` — 592 standard-gold files carry `tol=1e-14` in their footer. Confirmed. **OI-12 erratum (do not propagate the slip):** the CLM-08 row prose "the remaining 2,346 present-footer files carry `tol=1e-13`" is internally inconsistent with the verified tuple decomposition. The corrected, probe-confirmed decomposition is **1,754 @ `tol=1e-13` + 592 @ `tol=1e-14` = 2,346 with-footer** (`02-resolution-doc.md §Open-Items OI-12:779`; reproduced by AC-PIPE-06 below: `tol_distribution_present_footers = {1e-13: 1754, 1e-14: 592}`). The "2,346 @ 1e-13" phrasing is a transcription slip and is NOT cited in the contract.
- `CLM-09:24` — folder-default `tol`/`dt_out` per variant; observed modal values match the claim (std base `tol=1e-13 dt_out=0.17`; hier base `tol=1e-15 dt_out=0.08`; gold both `tol=1e-13 dt_out=0.01`). Confirmed.
- `CLM-05b:20` — std-gold Brutus output = 2,565 files (= 2,346 with-footer + 219 no-footer; arithmetic closes). `CLM-06:21` — hierarchical Brutus output = 4,857 files.

## FUT-01 Hand-off Note (formerly "Code Evidence")

The footer/provenance contract is a new data-side spec convention with no v1.4 predecessor. FUT-01 will implement the footer parser, the `param_provenance` dict, the `dt_out` measured-median cross-check, and the `footer_anomalous` flag in the DataLoader/parsing layer. The v1.3-era parser in `pinn/data-processing-pipeline-full.py` predates the per-field provenance model — record as a forward divergence index entry for the eventual `NN-CODE-DIVERGENCE.md`, NOT as v1.5 evidence (live code is not a grounding source, directive 2026-05-19).

## First-Principles Physics Check

Not an EVID-10 finding (the two primary sources do not conflict on the contract — both endorse footer-precedence-then-folder-default with footer-as-metadata-only; the issue doc's only error is the factual "minimal footer (no tol)" premise, which the corrected disk facts (CLM-07) overturn without producing a verdict conflict). No physical-law adjudication required. The one quantitative check performed is the footer-presence/tol-decomposition arithmetic, executed re-derivably as AC-PIPE-06 below.

## Verdict

`accept-resolution`

The resolution doc's `§3.5 Q-A5` all-or-nothing footer contract is transcribed per D-01: it is consistent with the four EVID-06 sources, with the locked v1.4/v1.5 conventions, and with the already-landed Step-1A completeness clause (B-06) and Step-1 item-7 mapping clause (B-11). The issue doc agrees in mechanism (precedence → fallback; footer-as-metadata-only) and its only divergence — the "minimal footer (no tol)" premise — is corrected by `CLM-07` (no footer and no parameter fields at all), which strengthens rather than overturns the resolution contract. No facet is source-silent: the folder defaults are `CLM-09`-confirmed, the no-footer populations are `CLM-07`-confirmed (with the OI-9 post-rerun update below), `eta=null` follows from the defaults being enumerated for `tol`/`Lw`/`dt` only, and the `measured` `dt_out` channel is grounded in current Step-1 item 4. The candidate did not fail review; no `accept-third-position` / `reject-both` / EVID-10 route is triggered.

## Root-Cause Framework Ambiguity

Not applicable (not EVID-10). For completeness: the pre-existing ambiguity was that Step 1 item 3 framed the footer as an optional energies line with no precedence/fallback/provenance rule, so a consumer could neither tell a footer-`tol` from a default-`tol` nor know that footer presence carries no completeness information. The amendment closes that gap.

## Locked Convention

Not applicable (not EVID-10). The adopted convention is stated spec-edit-ready in the Before/After note and the spec text below.

## Which Source Was Correct / Wrong

Not applicable (not EVID-10). Per-claim summary: on the **contract mechanism** (precedence → fallback, metadata-only) both sources are correct and agree. On the **factual premise** the issue doc is wrong ("219 minimal footers with no tol" / "footer schema varies, some omit eta") — CLM-07 establishes the 219 (and the 1,480 hier-base / 701 std-base) files have no footer at all, and present footers carry the full schema; the resolution doc's corrected premise is right. On **provenance granularity** the resolution doc's per-field `param_provenance` supersedes the issue doc's single `tol_confidence` flag.

## Before / After Spec Note

**Affected section 1 — `ctl_instruction.md` Step 1 item 3.**
- *Before:* "handling an optional trailing 'Result:' line (which may contain energies like E_initial, E_final, dE/E—extract these into metadata)" — footer treated as an optional energies line; no precedence, fallback, provenance, or metadata-only rule.
- *After:* full footer-handling contract — footer present → full schema parsed, each field `provenance='direct'`; footer absent (verified no-footer populations) → folder defaults, `provenance='inferred'`, `eta=null` `provenance='absent'`; partial-schema footer → `footer_anomalous=true`, default fallback; independently MEASURE `dt_out` as median snapshot spacing (`provenance='measured'`), WARN on >1% disagreement; footers MUST NOT be used as completeness signals (defer to Step-1A clause 4) or for ID mapping (defer to Step-1 item 7).

**Affected section 2 — `ctl_instruction.md` §2.6.**
- *Before:* metadata block lists `brutus_tolerance, word_length, dt_out, trustworthy_horizon`; no provenance map; `trustworthy_horizon` undefined.
- *After:* adds a `param_provenance` map over `{brutus_tolerance, word_length, dt_out, eta}` with values in `{direct, inferred, absent, measured}` per the Step-1 item-3 contract; `trustworthy_horizon` explicitly marked RESERVED (writers emit null, readers must not consume until defined; OI-4).

Edits are data-side only (D-04 perimeter); no `pinn_architecture.md` edit (D7 has no architecture-side component). The F-1 transposed stratification table (`ctl_instruction.md:26-27`) is NOT touched (no Phase 26 req ID; T-26-11 accept).

## Named Acceptance Check

**AC-PIPE-06** (reserved in `24-ISSUE-LEDGER.md:28`; no new AC-ID minted — VER-07).

- **Pass criterion:** (a) footer-presence scan over all four Brutus output variants reproduces the per-variant with-footer / no-footer partition; (b) the std-gold present-footer tol histogram reproduces the corrected decomposition `{1e-13: 1754, 1e-14: 592}` (sum 2,346 with-footer, NOT the OI-12 "2,346 @ 1e-13" slip); (c) the spec carries `param_provenance`, folder-default fallback, `eta` absent→null, the `dt_out` measured cross-check, and footer-as-metadata-only.
- **Data it runs on:** the four `simulation_data/Data/brutus_output/{variant}` folders (15,028 files) via the Phase-24 probe `data04_footers.py`, and the edited `ctl_instruction.md` (spec-consistency grep). No `pinn/` path is touched.
- **Exact command + captured output (re-derivable, D-15)** — output archived at `.planning/phases/26-dataloader-ingestion-and-selection-contracts/probes/outputs/ac-pipe-06_data04_footers.stdout.txt`:

```
$ .venv/bin/python .planning/phases/24-empirical-dataset-verification-and-correction-addendum/probes/data04_footers.py
brutus_hierarchical:                          with_footer=3377  no_footer=1480  n_files=4857  tol={1e-15: 3377}
brutus_hierarchical_gold_standard:            with_footer=4857  no_footer=0     n_files=4857  tol={1e-13: 4795, 1e-14: 62}
brutus_standard_quasi_random:                 with_footer=2048  no_footer=701   n_files=2749  tol={1e-13: 2048}
brutus_standard_quasi_random_gold_standard:   with_footer=2346  no_footer=219   n_files=2565  tol={1e-13: 1754, 1e-14: 592}
```

- **Interpretation / PASS:**
  - std base `2,048 / 701` — matches the resolution-doc part-5 target exactly. PASS.
  - std gold `2,346 / 219`, present-footer tol `{1e-13: 1754, 1e-14: 592}` — matches the target AND the OI-12 corrected decomposition (1,754 + 592 = 2,346 with-footer). PASS. The "2,346 @ 1e-13" slip is NOT reproduced (the probe puts 1,754 at 1e-13).
  - hier gold `4,857 / 0` — matches the target exactly. PASS.
  - hier base `3,377 / 1,480` — **OI-9 supersession (see caveat below).** The resolution-doc part-5 target `3,307 / 1,550` is anchored to the pre-rerun 2026-06-11 snapshot; the validated DATA-05 rerun replaced the 70 footer-less stale base-hier files with 70 footer-bearing reruns (`24-DATA05-RERUN-REMEDIATION.md:130-134`: footer-bearing 3,307→3,377, footer-less 1,550→1,480; the 1,550/3,307 figures are "stale as of this remediation"). The probe correctly reflects current disk; the 70-file delta is exactly the rerun cohort. PASS against the current (post-rerun) authoritative state.
  - Spec-consistency grep:

```
$ grep -nE 'param_provenance|inferred|folder.level default|measured|MUST NOT be used as completeness|never be used .*mapping|RESERVED' \
    pinn_instruction/markdown_conversion/framework-specs/ctl_instruction.md
```
  confirms the `param_provenance` map, folder-default fallback (`inferred`), `eta` absent→null, the `measured` `dt_out` cross-check, the metadata-only completeness/mapping deferrals, and the `trustworthy_horizon` RESERVED marker are present. PASS.

AC-PIPE-06 is a dataset probe + spec-consistency probe; it touches no `pinn/` path. Phase 29 (VER-09) builds and re-executes the full runnable acceptance suite from this AC-ID.

## Carried Caveats (D-13)

- **OI-6** (`02-resolution-doc.md §Open-Items OI-6:773`) — the no-footer populations (2,470 files: 1,480 hier-base post-rerun + 701 std-base + 219 std-gold) are not yet characterized by a footer-split snapshot-distribution probe. This is the single named factor that could overturn the model (a genuine partial-schema population would reopen the schema-variance question and force a field-by-field fallback in place of all-or-nothing). It is also why the footer contract carries NO completeness authority (Step-1A clause 4 reads parsed block times) and why the grid-consistency check (Step-1A clause 7) is held at WARN, escalation conditional on closing OI-6. Carried, not resolved.
- **OI-9** (`24-DATA05-RERUN-REMEDIATION.md`; validated 2026-06-11) — the DATA-05 70-ID base-hier rerun (IDs 0005-0059, 0061-0075) executed and validated; all 70 stale footer-less artifacts were replaced by 70 footer-bearing reruns. Consequence for D7's footer evidence: hier-base no-footer population is now **1,480** (was 1,550) and footer-bearing **3,377** (was 3,307); the resolution-doc part-5 targets 3,307/1,550 are stale for hier-base and superseded by the post-rerun probe. The Step-1A clause-2 quarantine is liftable / lifted on the validated rerun. Recorded here per D-13 because D7's footer evidence touches the rerun files.
- **OI-12 NOT propagated:** the CLM-08 "2,346 tol=1e-13" transcription slip is explicitly excluded; the corrected decomposition (1,754 @ 1e-13 + 592 @ 1e-14 = 2,346 with-footer) is cited instead (T-26-09 mitigation).

## Phase 27 boundary note

The footer evidence base is shared with Phase 27 Q-B2/Q-B3 (footer/mass-drift + precision). This packet keeps the D7 contract strictly data-side: parsing, provenance, and metadata storage. It does NOT define the precision/Decimal parsing policy (Phase 27 PIPE-07) or the mass-drift gate (Q-B2) — those consume the remediated DATA-05 state and the `param_provenance` dict but adjudicate separately. No candidate-text collision with Phase 27 footer/precision territory was found.

## Status Transition Log

```text
2026-06-13 50076e38 PENDING -> IN_PROGRESS (Phase 26 P03 by gsd-executor; D7 packet authored, accept-resolution verdict, AC-PIPE-06 defined)
2026-06-13 50076e38 IN_PROGRESS -> FIX_APPLIED (Phase 26 P03; Step 1 item 3 replacement + §2.6 param_provenance amendment transcribed into ctl_instruction.md from 02-resolution-doc.md:315-341)
2026-06-13 50076e38 FIX_APPLIED -> VERIFIED (Phase 26 P03; AC-PIPE-06 footer-presence + tol-decomposition probe PASS; OI-9 hier-base supersession recorded; AC-PIPE-01 regression re-check PASS)
```

The Plan 26-03 commit SHA travels with all three transitions, the spec edit, and the ledger edits in one commit (D-08); the substantive commit SHA is `50076e38`, backfilled here in the immediately following provenance commit (a commit cannot reference its own hash inline — pre-approved pattern, Phase 25 e05b4b1a / 26-01 fc6554b2 / 26-02 b42fbdaa).

**Dependents / regression (D-08):** D7 and B-06 both touch the footer/completeness boundary. The AC-PIPE-01 regression re-check confirms Step-1A clause 4 still states completeness is computed from parsed block times with footer presence forbidden as a completeness signal — consistent with D7's footer-as-metadata-only clause. B-06 remains VERIFIED. B-11's Step-1 item-7 mapping clause ("`Result:` footer paths are never used for mapping") is unchanged and D7 defers to it. No regression.
