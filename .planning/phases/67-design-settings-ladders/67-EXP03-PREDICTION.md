# EXP-03 learning-rate ladder — Prediction

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
    "equal_updates": "every arm runs the same common update count N from the shared cost-only budget (D-08)"
  },
  "control_arm": "lr1e-4",
  "controls": {
    "lr1e-3": "lr1e-4",
    "lr1e-4": "lr1e-4",
    "lr1e-5": "lr1e-4",
    "lr3e-4": "lr1e-4",
    "lr3e-5": "lr1e-4"
  },
  "experiment": "exp03",
  "hypothesis": {
    "name": "rate",
    "prediction": "learning-rate sensitivity: the fit's E changes across the rate ladder against the lr1e-4 control on the registered cases",
    "statement": "the locked 1e-4 constant Adam rate is mis-set for this task; a different constant rate fits the same locked network better"
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
    "lr1e-3": {
      "flat": "no effect against the control inside the registered rule; the hypothesis is not supported on this arm",
      "hypothesis": "under the hypothesis, learning-rate sensitivity improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule",
      "mechanical": "this arm's evidence is mechanically unusable; it reads nothing about the hypothesis",
      "opposite": "this arm fits worse than the control; the hypothesis is contradicted on this arm",
      "unsettled": "the endpoint is still improving when its budget ends; the no-continuation policy records it and extends nothing"
    },
    "lr1e-4": {
      "flat": "no effect against the control inside the registered rule",
      "hypothesis": "the control arm 'lr1e-4' defines the contrast reference; the hypothesis predicts learning-rate sensitivity against it",
      "mechanical": "the run's evidence is mechanically unusable",
      "opposite": "the control fits at least as well as every arm",
      "unsettled": "the endpoint is still improving when its budget ends"
    },
    "lr1e-5": {
      "flat": "no effect against the control inside the registered rule; the hypothesis is not supported on this arm",
      "hypothesis": "under the hypothesis, learning-rate sensitivity improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule",
      "mechanical": "this arm's evidence is mechanically unusable; it reads nothing about the hypothesis",
      "opposite": "this arm fits worse than the control; the hypothesis is contradicted on this arm",
      "unsettled": "the endpoint is still improving when its budget ends; the no-continuation policy records it and extends nothing"
    },
    "lr3e-4": {
      "flat": "no effect against the control inside the registered rule; the hypothesis is not supported on this arm",
      "hypothesis": "under the hypothesis, learning-rate sensitivity improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule",
      "mechanical": "this arm's evidence is mechanically unusable; it reads nothing about the hypothesis",
      "opposite": "this arm fits worse than the control; the hypothesis is contradicted on this arm",
      "unsettled": "the endpoint is still improving when its budget ends; the no-continuation policy records it and extends nothing"
    },
    "lr3e-5": {
      "flat": "no effect against the control inside the registered rule; the hypothesis is not supported on this arm",
      "hypothesis": "under the hypothesis, learning-rate sensitivity improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule",
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
  "title": "EXP-03 learning-rate ladder",
  "variants": [
    {
      "arm": "lr1e-3",
      "declarations": {
        "hierarchical/gold/1632": {
          "depth": 12,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.001,
          "name": "exp03-d12-w256-lr1e-3",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        },
        "hierarchical/gold/851": {
          "depth": 12,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.001,
          "name": "exp03-d12-w256-lr1e-3",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        }
      }
    },
    {
      "arm": "lr3e-4",
      "declarations": {
        "hierarchical/gold/1632": {
          "depth": 12,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0003,
          "name": "exp03-d12-w256-lr3e-4",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        },
        "hierarchical/gold/851": {
          "depth": 12,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0003,
          "name": "exp03-d12-w256-lr3e-4",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        }
      }
    },
    {
      "arm": "lr1e-4",
      "declarations": {
        "hierarchical/gold/1632": {
          "depth": 12,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp03-d12-w256-lr1e-4",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        },
        "hierarchical/gold/851": {
          "depth": 12,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp03-d12-w256-lr1e-4",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        }
      }
    },
    {
      "arm": "lr3e-5",
      "declarations": {
        "hierarchical/gold/1632": {
          "depth": 12,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 3e-05,
          "name": "exp03-d12-w256-lr3e-5",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        },
        "hierarchical/gold/851": {
          "depth": 12,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 3e-05,
          "name": "exp03-d12-w256-lr3e-5",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        }
      }
    },
    {
      "arm": "lr1e-5",
      "declarations": {
        "hierarchical/gold/1632": {
          "depth": 12,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 1e-05,
          "name": "exp03-d12-w256-lr1e-5",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        },
        "hierarchical/gold/851": {
          "depth": 12,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 1e-05,
          "name": "exp03-d12-w256-lr1e-5",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        }
      }
    }
  ]
}
```

```json phase67-budget
{
  "common_optimizer_steps": 155100,
  "experiment": "exp03",
  "experiment_projected_seconds": {
    "exp03": 39055.08603667113
  },
  "inputs": {
    "cap_seconds": 3540.0,
    "min_steps": 300,
    "rate_margin": 0.25,
    "rows": {
      "exp03|lr1e-3|hierarchical/gold/1632|41|10.0": {
        "predicted_byte_bound": 3646090,
        "published_bytes": 3631444,
        "residual_seconds": 4.951147882267833,
        "seconds_per_step": 0.013342685419949703,
        "warmup_seconds": 2.6936651989235543
      },
      "exp03|lr1e-3|hierarchical/gold/1632|42|10.0": {
        "predicted_byte_bound": 3646072,
        "published_bytes": 3631426,
        "residual_seconds": 4.411409249762073,
        "seconds_per_step": 0.013277421673818025,
        "warmup_seconds": 2.714852493547369
      },
      "exp03|lr1e-3|hierarchical/gold/851|42|10.0": {
        "predicted_byte_bound": 3646081,
        "published_bytes": 3631435,
        "residual_seconds": 3.7661358021432534,
        "seconds_per_step": 0.013345859206106979,
        "warmup_seconds": 2.6860381996957585
      },
      "exp03|lr1e-4|hierarchical/gold/1632|41|10.0": {
        "predicted_byte_bound": 3645828,
        "published_bytes": 3631182,
        "residual_seconds": 4.6303320155711845,
        "seconds_per_step": 0.013467594028217717,
        "warmup_seconds": 2.696695873164572
      },
      "exp03|lr1e-4|hierarchical/gold/1632|42|10.0": {
        "predicted_byte_bound": 3645828,
        "published_bytes": 3631182,
        "residual_seconds": 3.502570828422904,
        "seconds_per_step": 0.01355755709967343,
        "warmup_seconds": 2.7076941138366237
      },
      "exp03|lr1e-4|hierarchical/gold/851|42|10.0": {
        "predicted_byte_bound": 3645814,
        "published_bytes": 3631168,
        "residual_seconds": 5.019913930387702,
        "seconds_per_step": 0.013334910443634726,
        "warmup_seconds": 2.6876010851119645
      },
      "exp03|lr1e-5|hierarchical/gold/1632|41|10.0": {
        "predicted_byte_bound": 3646055,
        "published_bytes": 3631409,
        "residual_seconds": 4.018753694079351,
        "seconds_per_step": 0.013370521478296723,
        "warmup_seconds": 2.693291327683255
      },
      "exp03|lr1e-5|hierarchical/gold/1632|42|10.0": {
        "predicted_byte_bound": 3646046,
        "published_bytes": 3631400,
        "residual_seconds": 4.618348092073575,
        "seconds_per_step": 0.013642324828426354,
        "warmup_seconds": 2.718501497351099
      },
      "exp03|lr1e-5|hierarchical/gold/851|42|10.0": {
        "predicted_byte_bound": 3646018,
        "published_bytes": 3631372,
        "residual_seconds": 4.9634916769573465,
        "seconds_per_step": 0.013249733653618022,
        "warmup_seconds": 2.6840975863160565
      },
      "exp03|lr3e-4|hierarchical/gold/1632|41|10.0": {
        "predicted_byte_bound": 3645937,
        "published_bytes": 3631291,
        "residual_seconds": 3.4834079917054623,
        "seconds_per_step": 0.013661160601768642,
        "warmup_seconds": 2.6858245735638775
      },
      "exp03|lr3e-4|hierarchical/gold/1632|42|10.0": {
        "predicted_byte_bound": 3645923,
        "published_bytes": 3631277,
        "residual_seconds": 4.661358858749736,
        "seconds_per_step": 0.013453796681773383,
        "warmup_seconds": 2.685843418643344
      },
      "exp03|lr3e-4|hierarchical/gold/851|42|10.0": {
        "predicted_byte_bound": 3645941,
        "published_bytes": 3631295,
        "residual_seconds": 4.041761639120523,
        "seconds_per_step": 0.01328605115483515,
        "warmup_seconds": 2.700032623077277
      },
      "exp03|lr3e-5|hierarchical/gold/1632|41|10.0": {
        "predicted_byte_bound": 3646087,
        "published_bytes": 3631441,
        "residual_seconds": 4.645484532578848,
        "seconds_per_step": 0.013389539721189067,
        "warmup_seconds": 2.7173349942313507
      },
      "exp03|lr3e-5|hierarchical/gold/1632|42|10.0": {
        "predicted_byte_bound": 3646080,
        "published_bytes": 3631434,
        "residual_seconds": 4.037958717206493,
        "seconds_per_step": 0.013343219822680111,
        "warmup_seconds": 2.7032059200573713
      },
      "exp03|lr3e-5|hierarchical/gold/851|42|10.0": {
        "predicted_byte_bound": 3646104,
        "published_bytes": 3631458,
        "residual_seconds": 4.134043795755133,
        "seconds_per_step": 0.013213173619296867,
        "warmup_seconds": 2.689209500909783
      }
    },
    "size_ceiling_bytes": 9437184,
    "step_quantum": 100,
    "target_seconds": 2655.0,
    "time_fraction": 0.75
  },
  "loss_trace_stride": 156,
  "measured_steps": 154900,
  "per_row_projection_seconds": {
    "exp03|lr1e-3|hierarchical/gold/1632|41|10.0": 2593.850885231721,
    "exp03|lr1e-3|hierarchical/gold/1632|42|10.0": 2582.317958494936,
    "exp03|lr1e-3|hierarchical/gold/851|42|10.0": 2593.382320407748,
    "exp03|lr1e-4|hierarchical/gold/1632|41|10.0": 2618.0313122442913,
    "exp03|lr1e-4|hierarchical/gold/1632|42|10.0": 2634.204256756691,
    "exp03|lr1e-4|hierarchical/gold/851|42|10.0": 2592.318247310105,
    "exp03|lr1e-5|hierarchical/gold/1632|41|10.0": 2598.12274470807,
    "exp03|lr1e-5|hierarchical/gold/1632|42|10.0": 2651.531782479481,
    "exp03|lr1e-5|hierarchical/gold/851|42|10.0": 2575.6809961679405,
    "exp03|lr3e-4|hierarchical/gold/1632|41|10.0": 2654.237286167739,
    "exp03|lr3e-4|hierarchical/gold/1632|42|10.0": 2615.4444265249813,
    "exp03|lr3e-4|hierarchical/gold/851|42|10.0": 2581.9418523801755,
    "exp03|lr3e-5|hierarchical/gold/1632|41|10.0": 2603.3096954518146,
    "exp03|lr3e-5|hierarchical/gold/1632|42|10.0": 2592.83281638746,
    "exp03|lr3e-5|hierarchical/gold/851|42|10.0": 2567.87945595798
  },
  "phase_cost_ledger": {
    "cap_seconds": 3540.0,
    "experiments": [
      {
        "basis": "measured_projection",
        "declared_runs": 15,
        "experiment": "exp03",
        "note": "measured timing rows; update this ledger with the measured projections before each science launch",
        "planned_seconds": 39055.08603667113
      }
    ]
  },
  "schema": "phase67-budget/v1",
  "score_cadence": [
    77550,
    116325,
    155100
  ],
  "similarity_cadence": [
    0,
    38775,
    77550,
    116325,
    155100
  ],
  "timing_evidence": {
    "rows": [
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp03/timing/main-1632-s42/lr1e-3/record.json",
        "sha256": "196fb4abe858a40cdc4e55f876e111ab804b6dde254d34695735a6a44da466ac"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp03/timing/main-1632-s42/lr3e-4/record.json",
        "sha256": "de69e8d10ea2540fb1b3f32fa5208328c50c0968b8609e90370877bd95ac069d"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp03/timing/main-1632-s42/lr1e-4/record.json",
        "sha256": "2e2232d12e93f1f2783250f26ef973b79204bae9627315d73090e03255076a7b"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp03/timing/main-1632-s42/lr3e-5/record.json",
        "sha256": "112302b6fb97c00d1fb7834e9a1b0c2d64de64991f56435a7facfc84209b9bb0"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp03/timing/main-1632-s42/lr1e-5/record.json",
        "sha256": "8c148e19a577ee132a442e6fb72b67b75eaad873b6fa6c314b071c034c61e526"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp03/timing/repeat-851-s42/lr1e-3/record.json",
        "sha256": "ba2edc0379c11cfdcb26f04efe7ee289d43f63f36225b808210f410b7d0ac577"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp03/timing/repeat-851-s42/lr3e-4/record.json",
        "sha256": "aa8257152fe2f152649efc21ee2222615b4256cd51bd9688e9eca98cab012baf"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp03/timing/repeat-851-s42/lr1e-4/record.json",
        "sha256": "5264f3778257069ab644066392c1706993e7026a43fdc99021bef57cd00029aa"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp03/timing/repeat-851-s42/lr3e-5/record.json",
        "sha256": "f2ff0724a590ae10c5cad22abb3ea678ed8308f20edfcd30274a7ea8549b108e"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp03/timing/repeat-851-s42/lr1e-5/record.json",
        "sha256": "9583697e56dafe6dba1770aad2b12fc561afffe280255b63aa5d556426b766f2"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp03/timing/repeat-1632-s41/lr1e-3/record.json",
        "sha256": "d335bcdd02dd2c70c58d6c7b04cd04609e6553a9ef4d3a2ea9f15e60228475f3"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp03/timing/repeat-1632-s41/lr3e-4/record.json",
        "sha256": "af8e5c61b5e41f6ad9ace4d071cb8a46d2463753dda7f68354f7153c527ff11c"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp03/timing/repeat-1632-s41/lr1e-4/record.json",
        "sha256": "83ed9c6015be16a18fd15ada0e95ab3ee3d6396941fe547a7c264873ef4b3e4c"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp03/timing/repeat-1632-s41/lr3e-5/record.json",
        "sha256": "5e1f2e9e1a38809c97c050f91be2b54217ef0f40be15bcd02c325451920601e3"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp03/timing/repeat-1632-s41/lr1e-5/record.json",
        "sha256": "b92237fb503b79805ac690ab7673b486efde3068e868375853ed9161408158ba"
      }
    ]
  },
  "timing_evidence_digests": {
    "exp03|lr1e-3|hierarchical/gold/1632|41|10.0": null,
    "exp03|lr1e-3|hierarchical/gold/1632|42|10.0": null,
    "exp03|lr1e-3|hierarchical/gold/851|42|10.0": null,
    "exp03|lr1e-4|hierarchical/gold/1632|41|10.0": null,
    "exp03|lr1e-4|hierarchical/gold/1632|42|10.0": null,
    "exp03|lr1e-4|hierarchical/gold/851|42|10.0": null,
    "exp03|lr1e-5|hierarchical/gold/1632|41|10.0": null,
    "exp03|lr1e-5|hierarchical/gold/1632|42|10.0": null,
    "exp03|lr1e-5|hierarchical/gold/851|42|10.0": null,
    "exp03|lr3e-4|hierarchical/gold/1632|41|10.0": null,
    "exp03|lr3e-4|hierarchical/gold/1632|42|10.0": null,
    "exp03|lr3e-4|hierarchical/gold/851|42|10.0": null,
    "exp03|lr3e-5|hierarchical/gold/1632|41|10.0": null,
    "exp03|lr3e-5|hierarchical/gold/1632|42|10.0": null,
    "exp03|lr3e-5|hierarchical/gold/851|42|10.0": null
  },
  "warmup_steps": 200,
  "whole_run_cap_seconds": 3540.0
}
```

The science runs are frozen at 155100
common optimizer steps (200 warmup) under the
3540-second cap: the exact
case-major science matrix beside this page carries every registered
row. No rule is re-set after a result is seen.
