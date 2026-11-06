# EXP-04 time-input designs — Timing Prediction

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

## 2. Predictions and their alternatives

Every arm's hypothesis prediction and the flat, opposite, unsettled
and mechanical alternatives are recorded equally in the design block
above; the review reads the observed branch against this table.

- `locked-raw` — the control arm 'locked-raw' defines the contrast reference; the hypothesis predicts encoded harmonic against it
- `locked-f1` — under the hypothesis, encoded harmonic improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule
- `locked-f12` — under the hypothesis, encoded harmonic improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule
- `exp01-raw` — the control arm 'exp01-raw' defines the contrast reference; the hypothesis predicts encoded harmonic against it
- `exp01-f1` — under the hypothesis, encoded harmonic improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule
- `exp01-f12` — under the hypothesis, encoded harmonic improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule

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
