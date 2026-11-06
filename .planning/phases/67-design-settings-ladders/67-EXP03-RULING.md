{
  "schema": "phase67-owner-ruling",
  "title": "EXP-03 SCOPE-49 owner ruling",
  "experiment": "exp03",
  "ruling_recorded_at": "2026-11-05",
  "checkpoint": {
    "plan": "67-11",
    "task": "67-11-03",
    "type": "checkpoint:decision",
    "gate": "blocking-human",
    "condition": "The committed review has dependent_launch_allowed=false because a SCOPE-47/49 or resource decision is reserved to the owner.",
    "condition_met_because": "lr1e-3 is confirmed-worsening at confirmation grade (the registered rate-sensitivity-improves hypothesis is refuted; worsening in all three cases with matching tier change and >=20% relative E effect in each, all paired endpoints settled) and nothing is confirmed-improving, so the committed review reads scope49_disposition=proposal-pending and dependent_launch_allowed=false."
  },
  "owner_words_verbatim": "proceed with option 1",
  "option_selected": "authorize-recorded-proposal",
  "disposition": "authorized",
  "ruling_context": [
    "The checkpoint presented the three registered options (authorize-recorded-proposal / direct-different-change / hold) to the owner with the agent's recommendation to authorize, after a plain-language explanation of the options.",
    "An earlier message (\"then option 2 let's go\") was ambiguous; it was superseded by an explicit clarification exchange, and the owner's final operative instruction is the verbatim string recorded in owner_words_verbatim, selecting authorize-recorded-proposal."
  ],
  "proposal": "a refuted lead or an out-of-rule result was observed; the owner decides under SCOPE-49 whether the remaining experiments run, change or stop",
  "proposal_sha256": "e949fffb415051c49cba071170f880c1bdf610259c404cbd5c7768e85216be66",
  "review_sha256": "ccd236ef2d4299133b53972fa06ab44ec5df2315d0b3ac6c293f104a4930466c",
  "result_page_sha256": "63d9148bd25acc701d05cac033025c968a61ed11a72d34893f9dc3476869abb8",
  "reviewed_artifacts": {
    "review": {
      "path": ".planning/phases/67-design-settings-ladders/evidence/exp03/review.json",
      "sha256": "ccd236ef2d4299133b53972fa06ab44ec5df2315d0b3ac6c293f104a4930466c",
      "introducing_commit": "bfd85916",
      "changed_by_ruling": false
    },
    "result_page": {
      "path": ".planning/phases/67-design-settings-ladders/67-EXP03-RESULT.md",
      "sha256": "63d9148bd25acc701d05cac033025c968a61ed11a72d34893f9dc3476869abb8",
      "introducing_commit": "bfd85916",
      "changed_by_ruling": false
    }
  },
  "allowed_dependent_work": [
    "EXP-04, the time-input ladder (plan 67-12), proceeds under its existing committed registration as the dependent launch gated by this exp03 review (check-review --experiment exp03).",
    "No plan amendment, scope change, pass-bar change or registration change is authorized by this ruling; later Phase 67 experiment plans remain governed by their own prospective reviews and conditional gates."
  ]
}
