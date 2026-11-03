# EXP-02 depth ladder — Timing Prediction

The frozen scientific design, committed before any real timing or
experiment run for this experiment (D-10).
No rule is re-set after a result is seen.

## 1. The frozen design

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
    "depth_parameter_counts": {
      "d12": 795657,
      "d2": 137737,
      "d4": 269321,
      "d6": 400905,
      "d8": 532489
    },
    "note": "the size change that accompanies depth is recorded, not controlled away (D-03)"
  },
  "control_arm": "d12",
  "controls": {
    "d12": "d12",
    "d2": "d12",
    "d4": "d12",
    "d6": "d12",
    "d8": "d12"
  },
  "experiment": "exp02",
  "hypothesis": {
    "name": "depth",
    "prediction": "shallower depth improves the one-orbit fit: each shallower arm's E is below the d12 control's on all three registered cases under the registered effect rule",
    "statement": "the locked 12-layer depth contributes to the time-constant failure; a shallower network at the same locked width, input, frequencies, rate and window fits the orbit better"
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
    "d12": {
      "flat": "no effect against the control inside the registered rule",
      "hypothesis": "the control arm 'd12' defines the contrast reference; the hypothesis predicts shallower depth against it",
      "mechanical": "the run's evidence is mechanically unusable",
      "opposite": "the control fits at least as well as every arm",
      "unsettled": "the endpoint is still improving when its budget ends"
    },
    "d2": {
      "flat": "no effect against the control inside the registered rule; the hypothesis is not supported on this arm",
      "hypothesis": "under the hypothesis, shallower depth improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule",
      "mechanical": "this arm's evidence is mechanically unusable; it reads nothing about the hypothesis",
      "opposite": "this arm fits worse than the control; the hypothesis is contradicted on this arm",
      "unsettled": "the endpoint is still improving when its budget ends; the no-continuation policy records it and extends nothing"
    },
    "d4": {
      "flat": "no effect against the control inside the registered rule; the hypothesis is not supported on this arm",
      "hypothesis": "under the hypothesis, shallower depth improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule",
      "mechanical": "this arm's evidence is mechanically unusable; it reads nothing about the hypothesis",
      "opposite": "this arm fits worse than the control; the hypothesis is contradicted on this arm",
      "unsettled": "the endpoint is still improving when its budget ends; the no-continuation policy records it and extends nothing"
    },
    "d6": {
      "flat": "no effect against the control inside the registered rule; the hypothesis is not supported on this arm",
      "hypothesis": "under the hypothesis, shallower depth improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule",
      "mechanical": "this arm's evidence is mechanically unusable; it reads nothing about the hypothesis",
      "opposite": "this arm fits worse than the control; the hypothesis is contradicted on this arm",
      "unsettled": "the endpoint is still improving when its budget ends; the no-continuation policy records it and extends nothing"
    },
    "d8": {
      "flat": "no effect against the control inside the registered rule; the hypothesis is not supported on this arm",
      "hypothesis": "under the hypothesis, shallower depth improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule",
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
  "title": "EXP-02 depth ladder",
  "variants": [
    {
      "arm": "d2",
      "declarations": {
        "hierarchical/gold/1632": {
          "depth": 2,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp02-d2-w256-o30",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        },
        "hierarchical/gold/851": {
          "depth": 2,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp02-d2-w256-o30",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        }
      }
    },
    {
      "arm": "d4",
      "declarations": {
        "hierarchical/gold/1632": {
          "depth": 4,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp02-d4-w256-o30",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        },
        "hierarchical/gold/851": {
          "depth": 4,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp02-d4-w256-o30",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        }
      }
    },
    {
      "arm": "d6",
      "declarations": {
        "hierarchical/gold/1632": {
          "depth": 6,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp02-d6-w256-o30",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        },
        "hierarchical/gold/851": {
          "depth": 6,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp02-d6-w256-o30",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        }
      }
    },
    {
      "arm": "d8",
      "declarations": {
        "hierarchical/gold/1632": {
          "depth": 8,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp02-d8-w256-o30",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        },
        "hierarchical/gold/851": {
          "depth": 8,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp02-d8-w256-o30",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        }
      }
    },
    {
      "arm": "d12",
      "declarations": {
        "hierarchical/gold/1632": {
          "depth": 12,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp02-d12-w256-o30",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        },
        "hierarchical/gold/851": {
          "depth": 12,
          "first_omega_0": 30.0,
          "hidden_omega_0": 1.0,
          "learning_rate": 0.0001,
          "name": "exp02-d12-w256-o30",
          "time_features": "raw_tau_ic13",
          "width": 256,
          "window_length": 10.0
        }
      }
    }
  ]
}
```

## 2. Predictions and their alternatives

Every arm's hypothesis prediction and the flat, opposite, unsettled
and mechanical alternatives are recorded equally in the design block
above; the review reads the observed branch against this table.

- `d2` — under the hypothesis, shallower depth improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule
- `d4` — under the hypothesis, shallower depth improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule
- `d6` — under the hypothesis, shallower depth improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule
- `d8` — under the hypothesis, shallower depth improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule
- `d12` — the control arm 'd12' defines the contrast reference; the hypothesis predicts shallower depth against it

## 3. The timing run

The registered timing run is 1200
steps (200 warmup,
1000 measured) at the five
normalized similarity events and three frozen-score checkpoints of
the registered schedule, under the
900-second whole-launch cap.
One row launches at a time; no retry, no batch loop.

## 4. The budget

The cost-only common-update budget (67-04) consumes only the timing
rows' measured cost fields and freezes the science update count
before any science registration exists.

## 5. Harness provenance

The committed harness freeze manifest pins every harness file at its
current bytes; every registration this page admits pins the freeze.
