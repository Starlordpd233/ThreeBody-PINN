# EXP-05 signed-lap window ladder — Prediction

The complete pre-registered prediction: the frozen design, the
measured budget and the exact science registrations. This page is
written once by the budget step and frozen before science; the
review reads every result against it.

```json phase67-design
{
  "alternative_branches": [
    "flat",
    "opposite",
    "unsettled",
    "mechanical"
  ],
  "budget_rule": {
    "cap_seconds": 3540.0,
    "loss_entry_bytes": 32,
    "loss_trace_entries_max": 1000,
    "min_steps": 300,
    "rate_margin": 0.25,
    "residual_tolerance": 1e-09,
    "score_events": 3,
    "similarity_events": 5,
    "size_fraction": 0.9,
    "size_limit_bytes": 10485760,
    "step_quantum": 100,
    "time_fraction": 0.75,
    "timing_cap_seconds": 900.0,
    "timing_measured": 1000,
    "timing_steps": 1200,
    "timing_warmup": 200,
    "warmup_steps": 200
  },
  "cases": [
    {
      "case": "main-1632-s42",
      "orbit_key": "hierarchical/gold/1632",
      "seed": 42
    },
    {
      "case": "repeat-851-s42",
      "orbit_key": "hierarchical/gold/851",
      "seed": 42
    },
    {
      "case": "repeat-1632-s41",
      "orbit_key": "hierarchical/gold/1632",
      "seed": 41
    }
  ],
  "confounds": {
    "window_only": "the window changes and nothing else: locked depth, width, frequencies, rate and global tau normalization"
  },
  "control_arm": "lap10",
  "controls": {
    "lap1": "lap10",
    "lap10": "lap10",
    "lap2": "lap10",
    "lap5": "lap10"
  },
  "experiment": "exp05",
  "hypothesis": {
    "name": "window",
    "prediction": "a shorter window improves the fit: each shorter prefix arm's E is below the lap10 control's on all three registered cases",
    "statement": "the full [0, 10] window is harder than the orbit's early motion; a shorter exact signed-lap prefix fits better at the locked settings"
  },
  "metadata_algorithm": {
    "baselines": "same_window_expectations (67-03) per window: the window-mean constant and the two-Kepler comparison, independently cross-checked",
    "byte_bound": 9437184,
    "cap_seconds": 900.0,
    "frequency": "N_in from the committed Phase 59 panels row; f = N_in/10 cycles per physical time unit on both backbones",
    "harmonic_phase_increment": "max adjacent 2*pi*k*f*dt per harmonic k; strictly below pi or EXP-04 timing refuses without retuning",
    "harmonics": {
      "f1": [
        1
      ],
      "f12": [
        1,
        2
      ]
    },
    "normalizer": "the retained Phase 59 recorded normalizer; never refit",
    "reader": "pinn.verification.diagnostic_data.Stage0TrainingReader"
  },
  "no_continuation": "no branch extends, retries or re-sizes any run after its score is read; an unsettled endpoint is recorded as unsettled",
  "positive_control_note": "Phase 66 (EXP-01) remains a multi-setting positive control (D-02): its confirmed Tier-1 fit refutes only 'too small' and identifies no single enabling setting",
  "prediction_table": {
    "lap1": {
      "flat": "no effect against the control inside the registered rule; the hypothesis is not supported on this arm",
      "hypothesis": "under the hypothesis, shorter window improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule",
      "mechanical": "this arm's evidence is mechanically unusable; it reads nothing about the hypothesis",
      "opposite": "this arm fits worse than the control; the hypothesis is contradicted on this arm",
      "unsettled": "the endpoint is still improving when its budget ends; the no-continuation policy records it and extends nothing"
    },
    "lap10": {
      "flat": "no effect against the control inside the registered rule",
      "hypothesis": "the control arm 'lap10' defines the contrast reference; the hypothesis predicts shorter window against it",
      "mechanical": "the run's evidence is mechanically unusable",
      "opposite": "the control fits at least as well as every arm",
      "unsettled": "the endpoint is still improving when its budget ends"
    },
    "lap2": {
      "flat": "no effect against the control inside the registered rule; the hypothesis is not supported on this arm",
      "hypothesis": "under the hypothesis, shorter window improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule",
      "mechanical": "this arm's evidence is mechanically unusable; it reads nothing about the hypothesis",
      "opposite": "this arm fits worse than the control; the hypothesis is contradicted on this arm",
      "unsettled": "the endpoint is still improving when its budget ends; the no-continuation policy records it and extends nothing"
    },
    "lap5": {
      "flat": "no effect against the control inside the registered rule; the hypothesis is not supported on this arm",
      "hypothesis": "under the hypothesis, shorter window improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule",
      "mechanical": "this arm's evidence is mechanically unusable; it reads nothing about the hypothesis",
      "opposite": "this arm fits worse than the control; the hypothesis is contradicted on this arm",
      "unsettled": "the endpoint is still improving when its budget ends; the no-continuation policy records it and extends nothing"
    }
  },
  "reading_rule": {
    "confirmation": "all three registered cases qualifying in one direction with settled, clean endpoints",
    "confirmation_labels": [
      "confirmed-improvement",
      "confirmed-worsening",
      "ambiguous",
      "unsettled",
      "inconclusive-mechanical"
    ],
    "descriptive": {
      "adjacent_time_similarity": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim",
      "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
      "loss": "context only"
    },
    "effect": "a case qualifies through a matching tier change or a relative E effect of at least twenty percent",
    "improvement": "(E_at_3N/4 - E_at_N)/E_at_3N/4 strictly greater than five percent leaves the endpoint unsettled"
  },
  "schedule": {
    "science": {
      "cap_seconds": 3540.0,
      "formula": "phase67_cadence/phase67_score_cadence/phase67_loss_trace_stride at the budget's N",
      "optimizer_steps": "the phase67_budget common N, frozen at budget time before any science run"
    },
    "timing": {
      "cap_seconds": 900.0,
      "loss_trace_stride": 2,
      "measured_steps": 1000,
      "optimizer_steps": 1200,
      "score_cadence": [
        600,
        900,
        1200
      ],
      "similarity_cadence": [
        0,
        300,
        600,
        900,
        1200
      ],
      "warmup_steps": 200
    }
  },
  "schema": "phase67-design/v1",
  "scope_branches": {
    "ambiguous": {
      "dependent_launch_allowed": true,
      "reason": "the ambiguous branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
      "scope49_disposition": "none"
    },
    "confirmed-improvement": {
      "dependent_launch_allowed": true,
      "reason": "the hypothesis-supported branch is a registered technical ruling; continue under D-01",
      "scope49_disposition": "none"
    },
    "confirmed-worsening": {
      "dependent_launch_allowed": false,
      "reason": "a refuted lead: the registered hypothesis is contradicted on all three cases, so a concrete owner proposal under SCOPE-49 is recorded before dependent work continues",
      "scope49_disposition": "proposal-pending"
    },
    "inconclusive-mechanical": {
      "dependent_launch_allowed": false,
      "reason": "an out-of-rule result routes to the owner under SCOPE-47; dependent work waits for the ruling",
      "scope49_disposition": "proposal-pending"
    },
    "unsettled": {
      "dependent_launch_allowed": true,
      "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
      "scope49_disposition": "none"
    }
  },
  "title": "EXP-05 signed-lap window ladder",
  "variants": [
    {
      "arm": "lap1",
      "lap_count": 1,
      "selection": "first_lap_prefixes",
      "window_source": "the committed metadata capture's exact first-crossing endpoint"
    },
    {
      "arm": "lap2",
      "lap_count": 2,
      "selection": "first_lap_prefixes",
      "window_source": "the committed metadata capture's exact first-crossing endpoint"
    },
    {
      "arm": "lap5",
      "lap_count": 5,
      "selection": "first_lap_prefixes",
      "window_source": "the committed metadata capture's exact first-crossing endpoint"
    },
    {
      "arm": "lap10",
      "lap_count": 10,
      "selection": "first_lap_prefixes",
      "window_source": "the committed metadata capture's exact first-crossing endpoint"
    }
  ],
  "window_selection": {
    "algorithm": "first_lap_prefixes",
    "lap_counts": [
      1,
      2,
      5,
      10
    ],
    "note": "the exact first-crossing gold sample is the endpoint; no interpolation and no tau rescaling (D-06)"
  }
}
```

```json phase67-budget
{
  "common_optimizer_steps": 148700,
  "experiment": "exp05",
  "experiment_projected_seconds": {
    "exp05": 30305.529825570553
  },
  "inputs": {
    "cap_seconds": 3540.0,
    "min_steps": 300,
    "rate_margin": 0.25,
    "rows": {
      "exp05|lap10|hierarchical/gold/1632|41|9.509999999999842": {
        "predicted_byte_bound": 3627037,
        "published_bytes": 3612289,
        "residual_seconds": 4.733894592849538,
        "seconds_per_step": 0.01423962545953691,
        "warmup_seconds": 2.851341405767016
      },
      "exp05|lap10|hierarchical/gold/1632|42|9.509999999999842": {
        "predicted_byte_bound": 3627168,
        "published_bytes": 3612420,
        "residual_seconds": 4.382319472148083,
        "seconds_per_step": 0.013982053701998665,
        "warmup_seconds": 2.891633241903037
      },
      "exp05|lap10|hierarchical/gold/851|42|5.36999999999993": {
        "predicted_byte_bound": 3465840,
        "published_bytes": 3451092,
        "residual_seconds": 4.371860653394833,
        "seconds_per_step": 0.01353036704857368,
        "warmup_seconds": 2.8271653380943462
      },
      "exp05|lap1|hierarchical/gold/1632|41|0.9500000000000006": {
        "predicted_byte_bound": 3289583,
        "published_bytes": 3274835,
        "residual_seconds": 4.740526863373816,
        "seconds_per_step": 0.013144119987962768,
        "warmup_seconds": 2.708933772868477
      },
      "exp05|lap1|hierarchical/gold/1632|42|0.9500000000000006": {
        "predicted_byte_bound": 3289452,
        "published_bytes": 3274704,
        "residual_seconds": 4.871480809175409,
        "seconds_per_step": 0.013364078238722868,
        "warmup_seconds": 2.803521370049566
      },
      "exp05|lap1|hierarchical/gold/851|42|0.5400000000000003": {
        "predicted_byte_bound": 3273332,
        "published_bytes": 3258584,
        "residual_seconds": 4.673884937190451,
        "seconds_per_step": 0.012997238275711425,
        "warmup_seconds": 2.7478075351100415
      },
      "exp05|lap2|hierarchical/gold/1632|41|1.8900000000000015": {
        "predicted_byte_bound": 3326921,
        "published_bytes": 3312173,
        "residual_seconds": 4.121718380018137,
        "seconds_per_step": 0.013366644837660716,
        "warmup_seconds": 2.711998950340785
      },
      "exp05|lap2|hierarchical/gold/1632|42|1.8900000000000015": {
        "predicted_byte_bound": 3326947,
        "published_bytes": 3312199,
        "residual_seconds": 4.633509021019563,
        "seconds_per_step": 0.013327648517908528,
        "warmup_seconds": 2.792817752342671
      },
      "exp05|lap2|hierarchical/gold/851|42|1.0800000000000007": {
        "predicted_byte_bound": 3294606,
        "published_bytes": 3279858,
        "residual_seconds": 5.051306832814589,
        "seconds_per_step": 0.01335675887716934,
        "warmup_seconds": 2.81034974695649
      },
      "exp05|lap5|hierarchical/gold/1632|41|4.759999999999943": {
        "predicted_byte_bound": 3441493,
        "published_bytes": 3426745,
        "residual_seconds": 4.967259941273369,
        "seconds_per_step": 0.013773683987092228,
        "warmup_seconds": 2.7745611536083743
      },
      "exp05|lap5|hierarchical/gold/1632|42|4.759999999999943": {
        "predicted_byte_bound": 3441439,
        "published_bytes": 3426691,
        "residual_seconds": 4.370441124192439,
        "seconds_per_step": 0.013769331928458996,
        "warmup_seconds": 2.850522030261345
      },
      "exp05|lap5|hierarchical/gold/851|42|2.679999999999987": {
        "predicted_byte_bound": 3358199,
        "published_bytes": 3343451,
        "residual_seconds": 3.8934422520687804,
        "seconds_per_step": 0.01373532808839809,
        "warmup_seconds": 2.824865867383778
      }
    },
    "size_ceiling_bytes": 9437184,
    "step_quantum": 100,
    "target_seconds": 2655.0,
    "time_fraction": 0.75
  },
  "loss_trace_stride": 149,
  "measured_steps": 148500,
  "per_row_projection_seconds": {
    "exp05|lap10|hierarchical/gold/1632|41|9.509999999999842": 2654.0048012963243,
    "exp05|lap10|hierarchical/gold/1632|42|9.509999999999842": 2607.985317232382,
    "exp05|lap10|hierarchical/gold/851|42|5.36999999999993": 2523.1684410968437,
    "exp05|lap1|hierarchical/gold/1632|41|0.9500000000000006": 2448.155918957134,
    "exp05|lap1|hierarchical/gold/1632|42|0.9500000000000006": 2491.471399849021,
    "exp05|lap1|hierarchical/gold/851|42|0.5400000000000003": 2421.8934022841377,
    "exp05|lap2|hierarchical/gold/1632|41|1.8900000000000015": 2489.4581665281407,
    "exp05|lap2|hierarchical/gold/1632|42|1.8900000000000015": 2484.561839821793,
    "exp05|lap2|hierarchical/gold/851|42|1.0800000000000007": 2489.4556754086343,
    "exp05|lap5|hierarchical/gold/1632|41|4.759999999999943": 2567.1914979711587,
    "exp05|lap5|hierarchical/gold/1632|42|4.759999999999943": 2567.9721005258266,
    "exp05|lap5|hierarchical/gold/851|42|2.679999999999987": 2560.211264599161
  },
  "phase_cost_ledger": {
    "cap_seconds": 3540.0,
    "experiments": [
      {
        "basis": "measured_projection",
        "declared_runs": 12,
        "experiment": "exp05",
        "note": "measured timing rows; update this ledger with the measured projections before each science launch",
        "planned_seconds": 30305.529825570553
      }
    ]
  },
  "schema": "phase67-budget/v1",
  "score_cadence": [
    74350,
    111525,
    148700
  ],
  "similarity_cadence": [
    0,
    37175,
    74350,
    111525,
    148700
  ],
  "timing_evidence": {
    "rows": [
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp05/timing/main-1632-s42/lap1/record.json",
        "sha256": "6be9bbd1a9ce56956205fdf23b750a2c63156683904577ad7413a20745e2801f"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp05/timing/main-1632-s42/lap2/record.json",
        "sha256": "7f8a8d0d3e56ea2064d89def27f51a9014ce437f9be3544bd79d167ee00f4519"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp05/timing/main-1632-s42/lap5/record.json",
        "sha256": "102592d7833da818b8438639df391b685d07c34d442bcad9bb7e216a7345355f"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp05/timing/main-1632-s42/lap10/record.json",
        "sha256": "5ee4fa3e02f2a750c8a1617954e06eb52604ba7cac3f2fae082da0f7835dccb4"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp05/timing/repeat-851-s42/lap1/record.json",
        "sha256": "c35e0bec2e6d11ae6da364783273230875b4b4f28352864b62c0d95d35713e1c"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp05/timing/repeat-851-s42/lap2/record.json",
        "sha256": "b4e78cde6c392374d20f797adab7d780359866f7fedf9c45af7dea23d818903f"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp05/timing/repeat-851-s42/lap5/record.json",
        "sha256": "2c477478786111f3c18d01bd23fb61b09fa48e99e83d2d52dad19953598d12e1"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp05/timing/repeat-851-s42/lap10/record.json",
        "sha256": "7618d2b422a3945d7a26ea89e94ab333368a98f24a765f922465648f31065f72"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp05/timing/repeat-1632-s41/lap1/record.json",
        "sha256": "154cf2495286d0dc44e751aa3336732790121080d3ac15e5aa586d09b5a0ce1c"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp05/timing/repeat-1632-s41/lap2/record.json",
        "sha256": "dd2f630593bbc50721323c6fe4068dc2ac2d165a13c2e6d0f6fd33fd8abe2366"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp05/timing/repeat-1632-s41/lap5/record.json",
        "sha256": "fc9542d94029e88d6e89e8584e40b8aca906eec4a37384880192823f0440298b"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp05/timing/repeat-1632-s41/lap10/record.json",
        "sha256": "b6c8e949ca7277ea47c21ff951065cf6b20ff64d3f37cdc1fa071f87ffc4dddb"
      }
    ]
  },
  "timing_evidence_digests": {
    "exp05|lap10|hierarchical/gold/1632|41|9.509999999999842": null,
    "exp05|lap10|hierarchical/gold/1632|42|9.509999999999842": null,
    "exp05|lap10|hierarchical/gold/851|42|5.36999999999993": null,
    "exp05|lap1|hierarchical/gold/1632|41|0.9500000000000006": null,
    "exp05|lap1|hierarchical/gold/1632|42|0.9500000000000006": null,
    "exp05|lap1|hierarchical/gold/851|42|0.5400000000000003": null,
    "exp05|lap2|hierarchical/gold/1632|41|1.8900000000000015": null,
    "exp05|lap2|hierarchical/gold/1632|42|1.8900000000000015": null,
    "exp05|lap2|hierarchical/gold/851|42|1.0800000000000007": null,
    "exp05|lap5|hierarchical/gold/1632|41|4.759999999999943": null,
    "exp05|lap5|hierarchical/gold/1632|42|4.759999999999943": null,
    "exp05|lap5|hierarchical/gold/851|42|2.679999999999987": null
  },
  "warmup_steps": 200,
  "whole_run_cap_seconds": 3540.0
}
```

The science runs are frozen at 148700
common optimizer steps (200 warmup) under the
3540-second cap: the exact
case-major science matrix beside this page carries every registered
row. No rule is re-set after a result is seen.
