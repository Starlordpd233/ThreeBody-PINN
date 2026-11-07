# EXP-04 time-input designs — Prediction

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
    "encoded": {
      "fan_in": "the first layer's fan-in bound is 1/internal_dim (16 for f1, 18 for f12) on both backbones",
      "frequency": "f = N_in/10 from the committed census row, with harmonics 1 or 1 and 2 on both backbones",
      "input_design_not_omega": "the encoded arms change the input design, not first_omega_0 (D-05)"
    }
  },
  "control_arm": null,
  "controls": {
    "exp01-f1": "exp01-raw",
    "exp01-f12": "exp01-raw",
    "exp01-raw": "exp01-raw",
    "locked-f1": "locked-raw",
    "locked-f12": "locked-raw",
    "locked-raw": "locked-raw"
  },
  "experiment": "exp04",
  "hypothesis": {
    "name": "input",
    "prediction": "the encoded harmonic input improves the fit: each encoded arm's E is below its own backbone's raw control's on all three registered cases",
    "statement": "the raw [tau, IC13] input under-resolves the orbit's inner motion; an input carrying the census-frequency harmonics fits better without changing the backbone"
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
    "exp01-f1": {
      "flat": "no effect against the control inside the registered rule; the hypothesis is not supported on this arm",
      "hypothesis": "under the hypothesis, encoded harmonic improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule",
      "mechanical": "this arm's evidence is mechanically unusable; it reads nothing about the hypothesis",
      "opposite": "this arm fits worse than the control; the hypothesis is contradicted on this arm",
      "unsettled": "the endpoint is still improving when its budget ends; the no-continuation policy records it and extends nothing"
    },
    "exp01-f12": {
      "flat": "no effect against the control inside the registered rule; the hypothesis is not supported on this arm",
      "hypothesis": "under the hypothesis, encoded harmonic improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule",
      "mechanical": "this arm's evidence is mechanically unusable; it reads nothing about the hypothesis",
      "opposite": "this arm fits worse than the control; the hypothesis is contradicted on this arm",
      "unsettled": "the endpoint is still improving when its budget ends; the no-continuation policy records it and extends nothing"
    },
    "exp01-raw": {
      "flat": "no effect against the control inside the registered rule",
      "hypothesis": "the control arm 'exp01-raw' defines the contrast reference; the hypothesis predicts encoded harmonic against it",
      "mechanical": "the run's evidence is mechanically unusable",
      "opposite": "the control fits at least as well as every arm",
      "unsettled": "the endpoint is still improving when its budget ends"
    },
    "locked-f1": {
      "flat": "no effect against the control inside the registered rule; the hypothesis is not supported on this arm",
      "hypothesis": "under the hypothesis, encoded harmonic improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule",
      "mechanical": "this arm's evidence is mechanically unusable; it reads nothing about the hypothesis",
      "opposite": "this arm fits worse than the control; the hypothesis is contradicted on this arm",
      "unsettled": "the endpoint is still improving when its budget ends; the no-continuation policy records it and extends nothing"
    },
    "locked-f12": {
      "flat": "no effect against the control inside the registered rule; the hypothesis is not supported on this arm",
      "hypothesis": "under the hypothesis, encoded harmonic improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule",
      "mechanical": "this arm's evidence is mechanically unusable; it reads nothing about the hypothesis",
      "opposite": "this arm fits worse than the control; the hypothesis is contradicted on this arm",
      "unsettled": "the endpoint is still improving when its budget ends; the no-continuation policy records it and extends nothing"
    },
    "locked-raw": {
      "flat": "no effect against the control inside the registered rule",
      "hypothesis": "the control arm 'locked-raw' defines the contrast reference; the hypothesis predicts encoded harmonic against it",
      "mechanical": "the run's evidence is mechanically unusable",
      "opposite": "the control fits at least as well as every arm",
      "unsettled": "the endpoint is still improving when its budget ends"
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
  "title": "EXP-04 time-input designs",
  "variants": [
    {
      "arm": "locked-raw",
      "declarations": {
        "hierarchical/gold/1632": {
          "depth": 12,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp04-locked-raw",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        },
        "hierarchical/gold/851": {
          "depth": 12,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp04-locked-raw",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        }
      }
    },
    {
      "arm": "locked-f1",
      "declarations": {
        "hierarchical/gold/1632": {
          "depth": 12,
          "feature_frequency": 1.0471994061054544,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp04-locked-f1",
          "time_features": "tau_ic13_fourier1",
          "width": 256,
          "window_length": 10.0
        },
        "hierarchical/gold/851": {
          "depth": 12,
          "feature_frequency": 1.8612048388702,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp04-locked-f1-851",
          "time_features": "tau_ic13_fourier1",
          "width": 256,
          "window_length": 10.0
        }
      }
    },
    {
      "arm": "locked-f12",
      "declarations": {
        "hierarchical/gold/1632": {
          "depth": 12,
          "feature_frequency": 1.0471994061054544,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp04-locked-f12",
          "time_features": "tau_ic13_fourier12",
          "width": 256,
          "window_length": 10.0
        },
        "hierarchical/gold/851": {
          "depth": 12,
          "feature_frequency": 1.8612048388702,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp04-locked-f12-851",
          "time_features": "tau_ic13_fourier12",
          "width": 256,
          "window_length": 10.0
        }
      }
    },
    {
      "arm": "exp01-raw",
      "declarations": {
        "hierarchical/gold/1632": {
          "depth": 1,
          "first_omega_0": 1000.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp04-exp01-raw",
          "time_features": "raw_tau_ic13",
          "width": 384,
          "window_length": 10.0
        },
        "hierarchical/gold/851": {
          "depth": 1,
          "first_omega_0": 1000.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp04-exp01-raw",
          "time_features": "raw_tau_ic13",
          "width": 384,
          "window_length": 10.0
        }
      }
    },
    {
      "arm": "exp01-f1",
      "declarations": {
        "hierarchical/gold/1632": {
          "depth": 1,
          "feature_frequency": 1.0471994061054544,
          "first_omega_0": 1000.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp04-exp01-f1",
          "time_features": "tau_ic13_fourier1",
          "width": 384,
          "window_length": 10.0
        },
        "hierarchical/gold/851": {
          "depth": 1,
          "feature_frequency": 1.8612048388702,
          "first_omega_0": 1000.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp04-exp01-f1-851",
          "time_features": "tau_ic13_fourier1",
          "width": 384,
          "window_length": 10.0
        }
      }
    },
    {
      "arm": "exp01-f12",
      "declarations": {
        "hierarchical/gold/1632": {
          "depth": 1,
          "feature_frequency": 1.0471994061054544,
          "first_omega_0": 1000.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp04-exp01-f12",
          "time_features": "tau_ic13_fourier12",
          "width": 384,
          "window_length": 10.0
        },
        "hierarchical/gold/851": {
          "depth": 1,
          "feature_frequency": 1.8612048388702,
          "first_omega_0": 1000.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp04-exp01-f12-851",
          "time_features": "tau_ic13_fourier12",
          "width": 384,
          "window_length": 10.0
        }
      }
    }
  ]
}
```

```json phase67-budget
{
  "common_optimizer_steps": 112700,
  "experiment": "exp04",
  "experiment_projected_seconds": {
    "exp04": 25880.314258506063
  },
  "inputs": {
    "cap_seconds": 3540.0,
    "min_steps": 300,
    "rate_margin": 0.25,
    "rows": {
      "exp04|exp01-f12|hierarchical/gold/1632|41|10.0": {
        "predicted_byte_bound": 1088074,
        "published_bytes": 1073326,
        "residual_seconds": 5.4995146377477795,
        "seconds_per_step": 0.005049391411594115,
        "warmup_seconds": 1.2322182425996289
      },
      "exp04|exp01-f12|hierarchical/gold/1632|42|10.0": {
        "predicted_byte_bound": 1088064,
        "published_bytes": 1073316,
        "residual_seconds": 4.805189767270349,
        "seconds_per_step": 0.004225688359467313,
        "warmup_seconds": 0.9552413730416447
      },
      "exp04|exp01-f12|hierarchical/gold/851|42|10.0": {
        "predicted_byte_bound": 1088097,
        "published_bytes": 1073349,
        "residual_seconds": 5.5425255639711395,
        "seconds_per_step": 0.004392872276017442,
        "warmup_seconds": 0.9955563672119752
      },
      "exp04|exp01-f1|hierarchical/gold/1632|41|10.0": {
        "predicted_byte_bound": 1084704,
        "published_bytes": 1069956,
        "residual_seconds": 5.878807990113273,
        "seconds_per_step": 0.005110342258471064,
        "warmup_seconds": 1.0606552074896172
      },
      "exp04|exp01-f1|hierarchical/gold/1632|42|10.0": {
        "predicted_byte_bound": 1084720,
        "published_bytes": 1069972,
        "residual_seconds": 5.062476526945829,
        "seconds_per_step": 0.00480695181293413,
        "warmup_seconds": 1.044022700865753
      },
      "exp04|exp01-f1|hierarchical/gold/851|42|10.0": {
        "predicted_byte_bound": 1084694,
        "published_bytes": 1069946,
        "residual_seconds": 4.466930895578116,
        "seconds_per_step": 0.005163391068112105,
        "warmup_seconds": 1.2224335774080828
      },
      "exp04|exp01-raw|hierarchical/gold/1632|41|10.0": {
        "predicted_byte_bound": 1078236,
        "published_bytes": 1063488,
        "residual_seconds": 5.152772036381066,
        "seconds_per_step": 0.004772175401682034,
        "warmup_seconds": 1.0210738119203597
      },
      "exp04|exp01-raw|hierarchical/gold/1632|42|10.0": {
        "predicted_byte_bound": 1078236,
        "published_bytes": 1063488,
        "residual_seconds": 4.291669143829495,
        "seconds_per_step": 0.004830433234921656,
        "warmup_seconds": 0.9097843702184036
      },
      "exp04|exp01-raw|hierarchical/gold/851|42|10.0": {
        "predicted_byte_bound": 1078264,
        "published_bytes": 1063516,
        "residual_seconds": 4.8055864934576675,
        "seconds_per_step": 0.004265002265456132,
        "warmup_seconds": 0.9890728240134194
      },
      "exp04|locked-f12|hierarchical/gold/1632|41|10.0": {
        "predicted_byte_bound": 3654054,
        "published_bytes": 3639306,
        "residual_seconds": 5.195013225311413,
        "seconds_per_step": 0.016978516700095498,
        "warmup_seconds": 3.3695976155577227
      },
      "exp04|locked-f12|hierarchical/gold/1632|42|10.0": {
        "predicted_byte_bound": 3654067,
        "published_bytes": 3639319,
        "residual_seconds": 6.286234082304873,
        "seconds_per_step": 0.01617021970951464,
        "warmup_seconds": 3.2175300809321925
      },
      "exp04|locked-f12|hierarchical/gold/851|42|10.0": {
        "predicted_byte_bound": 3654044,
        "published_bytes": 3639296,
        "residual_seconds": 5.424074928858317,
        "seconds_per_step": 0.018760958958417177,
        "warmup_seconds": 3.5545105716446415
      },
      "exp04|locked-f1|hierarchical/gold/1632|41|10.0": {
        "predicted_byte_bound": 3651739,
        "published_bytes": 3636991,
        "residual_seconds": 5.339890199014917,
        "seconds_per_step": 0.016841022647102362,
        "warmup_seconds": 2.948277363786474
      },
      "exp04|locked-f1|hierarchical/gold/1632|42|10.0": {
        "predicted_byte_bound": 3651719,
        "published_bytes": 3636971,
        "residual_seconds": 4.251886669313535,
        "seconds_per_step": 0.013994574384414591,
        "warmup_seconds": 2.86959303135518
      },
      "exp04|locked-f1|hierarchical/gold/851|42|10.0": {
        "predicted_byte_bound": 3651817,
        "published_bytes": 3637069,
        "residual_seconds": 5.034251824137755,
        "seconds_per_step": 0.014963101514033041,
        "warmup_seconds": 3.2062037858413532
      },
      "exp04|locked-raw|hierarchical/gold/1632|41|10.0": {
        "predicted_byte_bound": 3645928,
        "published_bytes": 3631180,
        "residual_seconds": 5.060410213423893,
        "seconds_per_step": 0.014227602374157869,
        "warmup_seconds": 3.202073870343156
      },
      "exp04|locked-raw|hierarchical/gold/1632|42|10.0": {
        "predicted_byte_bound": 3645927,
        "published_bytes": 3631179,
        "residual_seconds": 4.3067188480636105,
        "seconds_per_step": 0.013370133329881356,
        "warmup_seconds": 2.6951340320520103
      },
      "exp04|locked-raw|hierarchical/gold/851|42|10.0": {
        "predicted_byte_bound": 3645906,
        "published_bytes": 3631158,
        "residual_seconds": 5.022306600934826,
        "seconds_per_step": 0.014672061359975487,
        "warmup_seconds": 3.5504642070736736
      }
    },
    "size_ceiling_bytes": 9437184,
    "step_quantum": 100,
    "target_seconds": 2655.0,
    "time_fraction": 0.75
  },
  "loss_trace_stride": 113,
  "measured_steps": 112500,
  "per_row_projection_seconds": {
    "exp04|exp01-f12|hierarchical/gold/1632|41|10.0": 719.8030722289092,
    "exp04|exp01-f12|hierarchical/gold/1632|42|10.0": 602.1695238843084,
    "exp04|exp01-f12|hierarchical/gold/851|42|10.0": 626.6549240780793,
    "exp04|exp01-f1|hierarchical/gold/1632|41|10.0": 727.6433472269241,
    "exp04|exp01-f1|hierarchical/gold/1632|42|10.0": 684.7111721689007,
    "exp04|exp01-f1|hierarchical/gold/851|42|10.0": 734.2209578387883,
    "exp04|exp01-raw|hierarchical/gold/1632|41|10.0": 679.6520606939702,
    "exp04|exp01-raw|hierarchical/gold/1632|42|10.0": 686.3407530530704,
    "exp04|exp01-raw|hierarchical/gold/851|42|10.0": 607.7194675122593,
    "exp04|locked-f12|hierarchical/gold/1632|41|10.0": 2401.36128431072,
    "exp04|locked-f12|hierarchical/gold/1632|42|10.0": 2292.3049621536857,
    "exp04|locked-f12|hierarchical/gold/851|42|10.0": 2653.9377255494896,
    "exp04|locked-f1|hierarchical/gold/1632|41|10.0": 2382.325108071681,
    "exp04|locked-f1|hierarchical/gold/1632|42|10.0": 1979.0181027648111,
    "exp04|locked-f1|hierarchical/gold/851|42|10.0": 2118.4908888061873,
    "exp04|locked-raw|hierarchical/gold/1632|41|10.0": 2014.8163285527235,
    "exp04|locked-raw|hierarchical/gold/1632|42|10.0": 1891.5876710523107,
    "exp04|locked-raw|hierarchical/gold/851|42|10.0": 2077.5569085592465
  },
  "phase_cost_ledger": {
    "cap_seconds": 3540.0,
    "experiments": [
      {
        "basis": "measured_projection",
        "declared_runs": 18,
        "experiment": "exp04",
        "note": "measured timing rows; update this ledger with the measured projections before each science launch",
        "planned_seconds": 25880.314258506063
      }
    ]
  },
  "schema": "phase67-budget/v1",
  "score_cadence": [
    56350,
    84525,
    112700
  ],
  "similarity_cadence": [
    0,
    28175,
    56350,
    84525,
    112700
  ],
  "timing_evidence": {
    "rows": [
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/main-1632-s42/locked-raw/record.json",
        "sha256": "130db22477bb8bc8c9a5c000e8f8c0faf4c5af052f8f763be693921546773c86"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/main-1632-s42/locked-f1/record.json",
        "sha256": "34484eb6ac32eabc93963d191bf23cc000ff26f81784001de60efeada2cd9fb4"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/main-1632-s42/locked-f12/record.json",
        "sha256": "ae689fbb3b9c84f527d0b6a04fab5eb534c9bf33a7273ad54b779585a9a3aee8"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/main-1632-s42/exp01-raw/record.json",
        "sha256": "56e6cf67ef653c1799aebf6aef907179cbc4354236e967423e74792d3ecb7d42"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/main-1632-s42/exp01-f1/record.json",
        "sha256": "466eefdeff47781c4f812f89556cb085b5f7c70808009f37f7629ec6a9cf321d"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/main-1632-s42/exp01-f12/record.json",
        "sha256": "c65e66d19383767c2e03ab922bcc1d0f4d68c0011dbbcda8793c7556f085b549"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/repeat-851-s42/locked-raw/record.json",
        "sha256": "54151ec3cc8f7ffcc768a90d71d2a4dc4fcf0ce7f7847e3ed6d8fb1207014401"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/repeat-851-s42/locked-f1/record.json",
        "sha256": "de4107a78c39735574aaffc351d60a5da42978d131c4dc245367d290477ba927"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/repeat-851-s42/locked-f12/record.json",
        "sha256": "2393e5d176338da1cc3ff266f1cbdc5363bd34c139998121c58932a107f389c6"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/repeat-851-s42/exp01-raw/record.json",
        "sha256": "9ba4c1c3a3c692ba1a99dd7f14dd04e23515408e55723ac9f47508eeffaefeb7"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/repeat-851-s42/exp01-f1/record.json",
        "sha256": "e5e970fc3df561641d6695f0e6042163e13092666369dafcd237a631ac8d090d"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/repeat-851-s42/exp01-f12/record.json",
        "sha256": "ea8b5b84bd1481af1cdbad62679f78da76822e3c39086d8e65ec141ee6d0bc58"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/repeat-1632-s41/locked-raw/record.json",
        "sha256": "9ab033edda5869620ef70c2b6b0324fcaeab5809cc3ebf0d463fda2f837d65a2"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/repeat-1632-s41/locked-f1/record.json",
        "sha256": "f9b4df3e2949d4a03c9374dfbc85c6f9e768ceb98e3acaa28211878b02c96639"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/repeat-1632-s41/locked-f12/record.json",
        "sha256": "ea4a9539a8de7cf78f4133edf2679190923df61adf9acd6afb373a67ddf4832d"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/repeat-1632-s41/exp01-raw/record.json",
        "sha256": "2ea8157255d90dd7b1e885161b60bc7c86bb60b6a222aa70a65cac824d97fb44"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/repeat-1632-s41/exp01-f1/record.json",
        "sha256": "220110dba99007ad87009dd852886376376bff7cd78a7632662eef732edc0558"
      },
      {
        "path": ".planning/phases/67-design-settings-ladders/evidence/exp04/timing/repeat-1632-s41/exp01-f12/record.json",
        "sha256": "f68e64cae893f92b916b479351946c66239bdb4a50cad4285415880ce3e75cf6"
      }
    ]
  },
  "timing_evidence_digests": {
    "exp04|exp01-f12|hierarchical/gold/1632|41|10.0": null,
    "exp04|exp01-f12|hierarchical/gold/1632|42|10.0": null,
    "exp04|exp01-f12|hierarchical/gold/851|42|10.0": null,
    "exp04|exp01-f1|hierarchical/gold/1632|41|10.0": null,
    "exp04|exp01-f1|hierarchical/gold/1632|42|10.0": null,
    "exp04|exp01-f1|hierarchical/gold/851|42|10.0": null,
    "exp04|exp01-raw|hierarchical/gold/1632|41|10.0": null,
    "exp04|exp01-raw|hierarchical/gold/1632|42|10.0": null,
    "exp04|exp01-raw|hierarchical/gold/851|42|10.0": null,
    "exp04|locked-f12|hierarchical/gold/1632|41|10.0": null,
    "exp04|locked-f12|hierarchical/gold/1632|42|10.0": null,
    "exp04|locked-f12|hierarchical/gold/851|42|10.0": null,
    "exp04|locked-f1|hierarchical/gold/1632|41|10.0": null,
    "exp04|locked-f1|hierarchical/gold/1632|42|10.0": null,
    "exp04|locked-f1|hierarchical/gold/851|42|10.0": null,
    "exp04|locked-raw|hierarchical/gold/1632|41|10.0": null,
    "exp04|locked-raw|hierarchical/gold/1632|42|10.0": null,
    "exp04|locked-raw|hierarchical/gold/851|42|10.0": null
  },
  "warmup_steps": 200,
  "whole_run_cap_seconds": 3540.0
}
```

The science runs are frozen at 112700
common optimizer steps (200 warmup) under the
3540-second cap: the exact
case-major science matrix beside this page carries every registered
row. No rule is re-set after a result is seen.
