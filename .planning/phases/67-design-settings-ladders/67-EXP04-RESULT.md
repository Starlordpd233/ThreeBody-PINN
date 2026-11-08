# Phase 67 Experiment Result — EXP-04

The review's complete reading: every endpoint's frozen values, the
matched contrasts, the prediction and roadmap comparison, and the
SCOPE-49 disposition. GAP-59-08 stays explicit: E is the frozen
scorecard's position-error score; no energy bar is adjudicated here.

```json phase67-review
{
  "budget_steps": 112700,
  "confirmation": {
    "confirmed": [],
    "contrasts": {
      "exp01-f1": {
        "arm": "exp01-f1",
        "cases": {
          "main": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.07822251056763327,
                "tier": 1
              },
              "control": {
                "E": 0.011069594072166582,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 6.066429903181018,
            "tier_direction": "unchanged"
          },
          "repeat-seed": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.04697019298545217,
                "tier": 1
              },
              "control": {
                "E": 0.01763443846274973,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 1.6635491163878053,
            "tier_direction": "unchanged"
          },
          "repeat-system": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.14185020924126024,
                "tier": 0
              },
              "control": {
                "E": 0.07864043014323893,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.8037822146049863,
            "tier_direction": "worsened"
          }
        },
        "confirmation": "unsettled",
        "control": "exp01-raw",
        "descriptive": {
          "adjacent_time_similarity": {
            "main": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.1195310577750206,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": -0.032717905938625336,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.11926710605621338,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": -0.017003744840621948,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.11903133243322372,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.027665192261338234,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.11896966397762299,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.06638682633638382,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.11889597773551941,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.09405852854251862,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 112700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9964733123779297,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9904256463050842,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9965022206306458,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.990788459777832,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9964118599891663,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9914138317108154,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.996241569519043,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9909675121307373,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9961069822311401,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9911242723464966,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 112700
                }
              ]
            },
            "repeat-seed": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.09319976717233658,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": -0.0356006845831871,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.09227855503559113,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": -0.021171363070607185,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.09207441657781601,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.02127128466963768,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.09205398708581924,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.05872716009616852,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.09201330691576004,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.08604976534843445,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 112700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9965821504592896,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9906841516494751,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9966053366661072,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9907867312431335,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9963721632957458,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9910871386528015,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9963014125823975,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9909143447875977,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9959641098976135,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9904946684837341,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 112700
                }
              ]
            },
            "repeat-system": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.031433455646038055,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.012948038056492805,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.03546716645359993,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.029868151992559433,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.03510734438896179,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.0667312741279602,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.034987758845090866,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.09867553412914276,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.032454416155815125,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.0630800649523735,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 112700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9964644908905029,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9903100728988647,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9964809417724609,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9908298850059509,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.996369481086731,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9914312958717346,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.996112585067749,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9907151460647583,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9958916902542114,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9904041886329651,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 112700
                }
              ]
            }
          },
          "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
          "loss": "context only",
          "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
        },
        "experiment": "exp04",
        "reasons": [
          "the main/control endpoint is unsettled",
          "the repeat-system/arm endpoint is unsettled",
          "the repeat-seed/arm endpoint is unsettled"
        ],
        "scope_disposition": {
          "dependent_launch_allowed": true,
          "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
          "scope49_disposition": "none"
        }
      },
      "exp01-f12": {
        "arm": "exp01-f12",
        "cases": {
          "main": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.04955849067979028,
                "tier": 1
              },
              "control": {
                "E": 0.011069594072166582,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 3.476992594010316,
            "tier_direction": "unchanged"
          },
          "repeat-seed": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.09316469672181629,
                "tier": 1
              },
              "control": {
                "E": 0.01763443846274973,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 4.283111051061456,
            "tier_direction": "unchanged"
          },
          "repeat-system": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.15456749202685538,
                "tier": 0
              },
              "control": {
                "E": 0.07864043014323893,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.9654965231665157,
            "tier_direction": "worsened"
          }
        },
        "confirmation": "unsettled",
        "control": "exp01-raw",
        "descriptive": {
          "adjacent_time_similarity": {
            "main": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.004805039148777723,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": -0.0008353182347491384,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.0019609369337558746,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.01864665560424328,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.0016600999515503645,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.05870116129517555,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.0014038097579032183,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.09292600303888321,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.0012766947038471699,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.11794627457857132,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 112700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9964733123779297,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9904256463050842,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9965022206306458,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.990788459777832,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9964118599891663,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9914138317108154,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.996241569519043,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9909675121307373,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9961069822311401,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9911242723464966,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 112700
                }
              ]
            },
            "repeat-seed": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.01308339461684227,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": -0.01043841801583767,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.00669738557189703,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.008830025792121887,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.0062128701247274876,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.0476517416536808,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.0058412146754562855,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.08261475712060928,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": -0.005723872222006321,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.10846047848463058,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 112700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9965821504592896,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9906841516494751,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9966053366661072,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9907867312431335,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9963721632957458,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9910871386528015,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9963014125823975,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9909143447875977,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9959641098976135,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9904946684837341,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 112700
                }
              ]
            },
            "repeat-system": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.0048432922922074795,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.0027399512473493814,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.0019532537553459406,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.017434952780604362,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.0019375999690964818,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.057734906673431396,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.00526540819555521,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.029350150376558304,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.0059949313290417194,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.08801896125078201,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 112700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9964644908905029,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9903100728988647,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9964809417724609,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9908298850059509,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.996369481086731,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9914312958717346,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.996112585067749,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9907151460647583,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9958916902542114,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9904041886329651,
                      "name": "h1",
                      "order": 1
                    }
                  ],
                  "step": 112700
                }
              ]
            }
          },
          "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
          "loss": "context only",
          "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
        },
        "experiment": "exp04",
        "reasons": [
          "the main/arm endpoint is unsettled",
          "the main/control endpoint is unsettled",
          "the repeat-seed/arm endpoint is unsettled"
        ],
        "scope_disposition": {
          "dependent_launch_allowed": true,
          "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
          "scope49_disposition": "none"
        }
      },
      "locked-f1": {
        "arm": "locked-f1",
        "cases": {
          "main": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.04615102941421912,
                "tier": 1
              },
              "control": {
                "E": 0.0344080542047465,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.3412856518882347,
            "tier_direction": "unchanged"
          },
          "repeat-seed": {
            "direction": "improvement",
            "endpoint_status": {
              "arm": "settled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.023682017735151037,
                "tier": 1
              },
              "control": {
                "E": 0.0412830122941967,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.42634957046290684,
            "tier_direction": "unchanged"
          },
          "repeat-system": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.0710851362747344,
                "tier": 1
              },
              "control": {
                "E": 0.04919948294071304,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.4448350272378731,
            "tier_direction": "unchanged"
          }
        },
        "confirmation": "unsettled",
        "control": "locked-raw",
        "descriptive": {
          "adjacent_time_similarity": {
            "main": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9966707825660706,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9920898675918579,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9835746884346008,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9614005088806152,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9215267300605774,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.824569582939148,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.6738126277923584,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.4383074939250946,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.2501904368400574,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.10665538161993027,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.04715743288397789,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.02035294845700264,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.007930945605039597,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9966904520988464,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9924165606498718,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9819537401199341,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9559968113899231,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9117640256881714,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.8043308854103088,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.6705237030982971,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.4614342451095581,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.32837390899658203,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.25986436009407043,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.2544116675853729,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.3187520205974579,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.43171408772468567,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9967541694641113,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9926725625991821,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9827526807785034,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9581771492958069,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9159895181655884,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.8188791871070862,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.7028253078460693,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.5263011455535889,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.4186973571777344,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.37381190061569214,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.4037807583808899,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.45312535762786865,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.6341452598571777,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9967648983001709,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9925332069396973,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9828145503997803,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9583020210266113,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9170644879341125,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.822171151638031,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.7211024165153503,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.5568162202835083,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.46974191069602966,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.41403719782829285,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.4868323504924774,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.5096824765205383,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.6714473962783813,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9968438744544983,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9927179217338562,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9830482006072998,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9585105180740356,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9209081530570984,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.8324716687202454,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.7379913330078125,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.5822348594665527,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.5172905325889587,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.4637739360332489,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.5578884482383728,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.5581449866294861,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.6767210960388184,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 112700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999837279319763,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999697208404541,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999352097511292,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998775124549866,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999712347984314,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999390184879303,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985547661781311,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9969659447669983,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9927595257759094,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9844540953636169,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9629203677177429,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9224951267242432,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999841451644897,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999608397483826,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999178647994995,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998276233673096,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996066689491272,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991987943649292,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.99812251329422,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9962421655654907,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.991174578666687,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9839316010475159,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9641760587692261,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9422818422317505,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999825358390808,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999604225158691,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999110698699951,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998188614845276,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995752573013306,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991735816001892,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981133341789246,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964744448661804,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9917871952056885,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9857177734375,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9687786102294922,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9519308805465698,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999820590019226,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999958872795105,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999905526638031,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999799907207489,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995323419570923,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991028308868408,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9979533553123474,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9962454438209534,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9916363954544067,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9859731197357178,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9701394438743591,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9608948826789856,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999818801879883,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999598264694214,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999110102653503,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998094439506531,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995533227920532,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991236329078674,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9979623556137085,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9961771368980408,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.991576075553894,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9859146475791931,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9697723984718323,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9595596194267273,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 112700
                }
              ]
            },
            "repeat-seed": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.996708869934082,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9921917915344238,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9838249087333679,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9622093439102173,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9227829575538635,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.828664243221283,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.6854045391082764,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.4445897340774536,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.2522827088832855,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.10424134880304337,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.04277215152978897,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.01777574047446251,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.006403487175703049,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9965741634368896,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9920174479484558,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9821437001228333,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9565058946609497,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9110372066497803,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.8023985624313354,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.6586048007011414,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.42942291498184204,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.2822277247905731,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.18980367481708527,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.18434511125087738,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.2364448755979538,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.31238603591918945,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9966338872909546,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9921594262123108,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9814533591270447,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9549652338027954,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.91105717420578,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.8085794448852539,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.6834492087364197,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.5008667707443237,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.3927289545536041,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.35454127192497253,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.3778610825538635,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.43487223982810974,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.6098452210426331,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9966120719909668,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9924116134643555,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9820225834846497,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.956578254699707,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9151694774627686,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.8186303973197937,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.7066662311553955,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.5353250503540039,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.45404478907585144,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.40334102511405945,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.46876317262649536,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.49875274300575256,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.65851891040802,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.996562123298645,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9921054244041443,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9816699028015137,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9560009837150574,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9140320420265198,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.8175833225250244,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.7168225049972534,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.5572716593742371,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.49134334921836853,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.43823525309562683,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.5324790477752686,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.5378143191337585,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.6542691588401794,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 112700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999827742576599,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999688863754272,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999354481697083,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999873161315918,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999718189239502,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993919730186462,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985952973365784,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.997002363204956,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9928239583969116,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9847432971000671,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9634863138198853,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.925688624382019,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999833703041077,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999625086784363,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999166131019592,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998229742050171,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995944499969482,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992048740386963,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981563687324524,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964001178741455,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9916437864303589,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9845506548881531,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9650442004203796,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9426186680793762,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999880194664001,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999825358390808,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999536275863647,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998936653137207,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997814297676086,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994892477989197,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989191889762878,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9974373579025269,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9951664805412292,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9891615509986877,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9811629056930542,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9586803913116455,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9403875470161438,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999828934669495,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999566674232483,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999033212661743,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998025298118591,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999534547328949,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999093770980835,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978678226470947,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9961755275726318,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9914381504058838,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.985751748085022,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.969436764717102,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9586381316184998,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999809861183167,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.99996018409729,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999132752418518,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998128414154053,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995751976966858,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991310238838196,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9980255365371704,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9965376853942871,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9923426508903503,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9874482750892639,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9733120203018188,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9656933546066284,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 112700
                }
              ]
            },
            "repeat-system": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9893693327903748,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9747711420059204,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9491488933563232,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.8853276968002319,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.7820672392845154,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.5794097781181335,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.3627089858055115,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.1652025431394577,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.0749540627002716,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.029926463961601257,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.010080614127218723,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.0011815219186246395,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.0016937174368649721,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9891822338104248,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9755899310112,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9431524872779846,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.8702897429466248,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.7551528215408325,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.5484001040458679,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.3767133057117462,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.2402121126651764,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.18729059398174286,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.2021113783121109,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.21801172196865082,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.28418347239494324,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.3539729714393616,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.989568293094635,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9756695628166199,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9431278705596924,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.8711649775505066,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.7625555992126465,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.5680919289588928,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.4125223755836487,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.29638317227363586,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.2576044201850891,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.28053703904151917,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.3144840598106384,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.38057762384414673,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.5493876934051514,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9894107580184937,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9753567576408386,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9421719312667847,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.8689127564430237,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.7620391845703125,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.566577672958374,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.42361459136009216,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.3180650770664215,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.29670092463493347,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.31771180033683777,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.38091161847114563,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.4376797080039978,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.6293333768844604,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9892618060112,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9748639464378357,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9402034878730774,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.864090085029602,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.7571356296539307,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.5713180303573608,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.44282829761505127,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.3422194719314575,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.3374705910682678,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.35265815258026123,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.4321959316730499,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.47666019201278687,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.6615689992904663,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 112700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999836683273315,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999704957008362,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999396800994873,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998784065246582,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997159242630005,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994155764579773,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986107349395752,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9970688223838806,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9929354786872864,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.985227108001709,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9650446772575378,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.926563024520874,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999880194664001,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999836087226868,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999628663063049,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999921441078186,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998414516448975,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999629557132721,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992631673812866,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9983028769493103,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9968282580375671,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9927104711532593,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9866904020309448,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.970236599445343,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9527369141578674,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999815821647644,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999589920043945,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999069571495056,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997972846031189,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995140433311462,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990220665931702,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976761341094971,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9958189725875854,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9903712868690491,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9833876490592957,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9633936882019043,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9457546472549438,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999821186065674,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999570250511169,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999034404754639,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999807596206665,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995778203010559,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991448521614075,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9979879856109619,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.996306300163269,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9916086196899414,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9861067533493042,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9698157906532288,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9578278660774231,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987781047821,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999815821647644,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999589920043945,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999058246612549,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998112916946411,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995810389518738,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991647005081177,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.998124897480011,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9965490698814392,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.992338240146637,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9875491857528687,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9735011458396912,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9643779397010803,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 112700
                }
              ]
            }
          },
          "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
          "loss": "context only",
          "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
        },
        "experiment": "exp04",
        "reasons": [
          "the main/arm endpoint is unsettled",
          "the main/control endpoint is unsettled"
        ],
        "scope_disposition": {
          "dependent_launch_allowed": true,
          "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
          "scope49_disposition": "none"
        }
      },
      "locked-f12": {
        "arm": "locked-f12",
        "cases": {
          "main": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "unsettled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.06013616119727379,
                "tier": 1
              },
              "control": {
                "E": 0.0344080542047465,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.747735016907122,
            "tier_direction": "unchanged"
          },
          "repeat-seed": {
            "direction": "improvement",
            "endpoint_status": {
              "arm": "unsettled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.03895762366412014,
                "tier": 1
              },
              "control": {
                "E": 0.0412830122941967,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": false,
            "reasons": [
              "the effect is below the registered twenty-percent line with no matching tier change"
            ],
            "relative_E_effect": 0.05632797852794896,
            "tier_direction": "unchanged"
          },
          "repeat-system": {
            "direction": "worsening",
            "endpoint_status": {
              "arm": "settled",
              "control": "settled"
            },
            "observed_fit": {
              "arm": {
                "E": 0.061705123279830354,
                "tier": 1
              },
              "control": {
                "E": 0.04919948294071304,
                "tier": 1
              }
            },
            "percentage_applicable": true,
            "qualifies_effect": true,
            "reasons": [],
            "relative_E_effect": 0.2541823529769005,
            "tier_direction": "unchanged"
          }
        },
        "confirmation": "unsettled",
        "control": "locked-raw",
        "descriptive": {
          "adjacent_time_similarity": {
            "main": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9876847267150879,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.96944260597229,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9357204437255859,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.8526566624641418,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.7239997982978821,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.49281764030456543,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.2849941551685333,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.12395106256008148,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.052989374846220016,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.02013605460524559,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.007529287599027157,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.0033469991758465767,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": -0.0011606552870944142,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9871696829795837,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9684449434280396,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9287761449813843,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.8353697061538696,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.6893578171730042,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.4415742754936218,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.24586370587348938,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.09931378066539764,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.042618755251169205,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.014744516462087631,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.004835011437535286,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.001994783990085125,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": -0.0033917922992259264,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9859890341758728,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9647995829582214,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9215041399002075,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.8182504773139954,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.659761369228363,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.4044906497001648,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.21746589243412018,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.08726835995912552,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.038364510983228683,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.023537060245871544,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.0263957716524601,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.043164532631635666,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.07676658034324646,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9855214357376099,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9642558693885803,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.918163537979126,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.8119564056396484,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.6479254961013794,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.391568124294281,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.20833154022693634,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.08477374166250229,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.04563579708337784,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.03733444958925247,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.05842522159218788,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.09972462803125381,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.16749756038188934,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9847329258918762,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9618474245071411,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9169881343841553,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.8078361749649048,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.6506189107894897,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.4019777774810791,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.2352926880121231,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.1320856213569641,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.10396428406238556,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.09983690828084946,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.158980593085289,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.20346343517303467,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.26821374893188477,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 112700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999837279319763,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999697208404541,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999352097511292,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998775124549866,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999712347984314,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999390184879303,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985547661781311,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9969659447669983,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9927595257759094,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9844540953636169,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9629203677177429,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9224951267242432,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999841451644897,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999608397483826,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999178647994995,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998276233673096,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9996066689491272,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991987943649292,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.99812251329422,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9962421655654907,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.991174578666687,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9839316010475159,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9641760587692261,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9422818422317505,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999825358390808,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999604225158691,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999110698699951,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998188614845276,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995752573013306,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991735816001892,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981133341789246,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964744448661804,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9917871952056885,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9857177734375,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9687786102294922,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9519308805465698,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999820590019226,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.999958872795105,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999905526638031,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999799907207489,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995323419570923,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991028308868408,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9979533553123474,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9962454438209534,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9916363954544067,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9859731197357178,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9701394438743591,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9608948826789856,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999818801879883,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999598264694214,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999110102653503,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998094439506531,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995533227920532,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991236329078674,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9979623556137085,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9961771368980408,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.991576075553894,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9859146475791931,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9697723984718323,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9595596194267273,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 112700
                }
              ]
            },
            "repeat-seed": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9876596927642822,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9688193798065186,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9338690638542175,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.8520930409431458,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.7242307066917419,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.4984109699726105,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.29016900062561035,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.12524740397930145,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.05150873214006424,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.02151443436741829,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.007847487926483154,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.0013329308712854981,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.00041031313594430685,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9863818287849426,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9665213823318481,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9240191578865051,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.8233514428138733,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.6723672747612,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.4233142137527466,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.23988817632198334,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.09305302798748016,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.040660612285137177,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.020399875938892365,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.024115201085805893,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.047252144664525986,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.09350267052650452,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9850890040397644,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9629500508308411,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.916533350944519,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.8091667294502258,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.6452609300613403,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.3916861414909363,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.20427973568439484,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.08489010483026505,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.038830310106277466,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.02669476717710495,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.03620820865035057,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.060873180627822876,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.11450578272342682,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9836836457252502,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9593127369880676,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9097181558609009,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.7937976121902466,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.623374879360199,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.36762407422065735,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.19632767140865326,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.07633822411298752,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.03850514814257622,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.02104945108294487,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.025054926052689552,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.039429280906915665,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.06090700253844261,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9827489256858826,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9568927884101868,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9041284322738647,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.7802560925483704,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.6086540818214417,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.3501494824886322,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.1800297200679779,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.066393181681633,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.027829743921756744,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.01780833676457405,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.023381076753139496,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.0463426299393177,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.09024476259946823,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 112700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999827742576599,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999688863754272,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999354481697083,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999873161315918,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999718189239502,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9993919730186462,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9985952973365784,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.997002363204956,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9928239583969116,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9847432971000671,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9634863138198853,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.925688624382019,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999884963035583,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999833703041077,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999625086784363,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999166131019592,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998229742050171,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995944499969482,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992048740386963,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9981563687324524,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9964001178741455,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9916437864303589,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9845506548881531,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9650442004203796,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9426186680793762,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999880194664001,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999825358390808,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999536275863647,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9998936653137207,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997814297676086,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9994892477989197,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9989191889762878,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9974373579025269,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9951664805412292,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9891615509986877,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9811629056930542,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9586803913116455,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9403875470161438,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999828934669495,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999566674232483,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999033212661743,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998025298118591,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999534547328949,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.999093770980835,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9978678226470947,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9961755275726318,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9914381504058838,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.985751748085022,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.969436764717102,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9586381316184998,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999809861183167,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.99996018409729,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999132752418518,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998128414154053,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995751976966858,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991310238838196,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9980255365371704,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9965376853942871,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9923426508903503,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9874482750892639,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9733120203018188,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9656933546066284,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 112700
                }
              ]
            },
            "repeat-system": {
              "arm": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9615857005119324,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.90608811378479,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.8126748204231262,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.6251658797264099,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.4132542014122009,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.19344350695610046,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.07935895025730133,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.03134886920452118,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.01115353126078844,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.0019414183916524053,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": -0.001311177504248917,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": -0.001955225830897689,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": -0.0024598941672593355,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9598480463027954,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9016213417053223,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.7970263957977295,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.5955512523651123,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.379767507314682,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.17416341602802277,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.07694987207651138,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.02868107333779335,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.014398090541362762,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.012204616330564022,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.021154817193746567,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.04613606259226799,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.08217640221118927,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9540629982948303,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.8894875645637512,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.7702212333679199,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.5521804094314575,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.33434605598449707,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.13895274698734283,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.05539887398481369,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.02165393903851509,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.008751432411372662,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": -0.0006982552004046738,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": -0.0003194652672391385,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": -0.002234750660136342,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.00015464812167920172,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9510906934738159,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.8818121552467346,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.748634934425354,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.5181584358215332,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.29521217942237854,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.12512540817260742,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.046495530754327774,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.01596970111131668,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.005382606294006109,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.002998949959874153,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.007910823449492455,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.03056042268872261,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.06334389001131058,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.949860692024231,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.8797006607055664,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.7510967254638672,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.5155072808265686,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.2965089678764343,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.1236242800951004,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.05230078101158142,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.025258639827370644,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.026974089443683624,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.03322690725326538,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.07609127461910248,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.087810218334198,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.18883301317691803,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 112700
                }
              ],
              "control": [
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999883770942688,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999836683273315,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999704957008362,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999396800994873,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998784065246582,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9997159242630005,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9994155764579773,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9986107349395752,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9970688223838806,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9929354786872864,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.985227108001709,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9650446772575378,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.926563024520874,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 0
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999880194664001,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999836087226868,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999628663063049,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.999921441078186,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998414516448975,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.999629557132721,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9992631673812866,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9983028769493103,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9968282580375671,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9927104711532593,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9866904020309448,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.970236599445343,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9527369141578674,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 28175
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999882578849792,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999815821647644,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999589920043945,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999069571495056,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9997972846031189,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995140433311462,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9990220665931702,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9976761341094971,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9958189725875854,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9903712868690491,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9833876490592957,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9633936882019043,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9457546472549438,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 56350
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.9999881386756897,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999821186065674,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999570250511169,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999034404754639,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.999807596206665,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995778203010559,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991448521614075,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.9979879856109619,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.996306300163269,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.9916086196899414,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9861067533493042,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9698157906532288,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9578278660774231,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 84525
                },
                {
                  "layers": [
                    {
                      "adjacent_cosine_mean": 0.999987781047821,
                      "name": "input",
                      "order": 0
                    },
                    {
                      "adjacent_cosine_mean": 0.9999815821647644,
                      "name": "h1",
                      "order": 1
                    },
                    {
                      "adjacent_cosine_mean": 0.9999589920043945,
                      "name": "h2",
                      "order": 2
                    },
                    {
                      "adjacent_cosine_mean": 0.9999058246612549,
                      "name": "h3",
                      "order": 3
                    },
                    {
                      "adjacent_cosine_mean": 0.9998112916946411,
                      "name": "h4",
                      "order": 4
                    },
                    {
                      "adjacent_cosine_mean": 0.9995810389518738,
                      "name": "h5",
                      "order": 5
                    },
                    {
                      "adjacent_cosine_mean": 0.9991647005081177,
                      "name": "h6",
                      "order": 6
                    },
                    {
                      "adjacent_cosine_mean": 0.998124897480011,
                      "name": "h7",
                      "order": 7
                    },
                    {
                      "adjacent_cosine_mean": 0.9965490698814392,
                      "name": "h8",
                      "order": 8
                    },
                    {
                      "adjacent_cosine_mean": 0.992338240146637,
                      "name": "h9",
                      "order": 9
                    },
                    {
                      "adjacent_cosine_mean": 0.9875491857528687,
                      "name": "h10",
                      "order": 10
                    },
                    {
                      "adjacent_cosine_mean": 0.9735011458396912,
                      "name": "h11",
                      "order": 11
                    },
                    {
                      "adjacent_cosine_mean": 0.9643779397010803,
                      "name": "h12",
                      "order": 12
                    }
                  ],
                  "step": 112700
                }
              ]
            }
          },
          "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
          "loss": "context only",
          "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
        },
        "experiment": "exp04",
        "reasons": [
          "the main/control endpoint is unsettled",
          "the repeat-seed/arm endpoint is unsettled"
        ],
        "scope_disposition": {
          "dependent_launch_allowed": true,
          "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
          "scope49_disposition": "none"
        }
      }
    },
    "descriptive": {
      "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
      "loss": "context only",
      "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
    },
    "experiment": "exp04",
    "unconfirmed": [
      {
        "arm": "exp01-f1",
        "confirmation": "unsettled",
        "reasons": [
          "the main/control endpoint is unsettled",
          "the repeat-system/arm endpoint is unsettled",
          "the repeat-seed/arm endpoint is unsettled"
        ]
      },
      {
        "arm": "exp01-f12",
        "confirmation": "unsettled",
        "reasons": [
          "the main/arm endpoint is unsettled",
          "the main/control endpoint is unsettled",
          "the repeat-seed/arm endpoint is unsettled"
        ]
      },
      {
        "arm": "locked-f1",
        "confirmation": "unsettled",
        "reasons": [
          "the main/arm endpoint is unsettled",
          "the main/control endpoint is unsettled"
        ]
      },
      {
        "arm": "locked-f12",
        "confirmation": "unsettled",
        "reasons": [
          "the main/control endpoint is unsettled",
          "the repeat-seed/arm endpoint is unsettled"
        ]
      }
    ]
  },
  "contrasts": {
    "exp01-f1": {
      "arm": "exp01-f1",
      "cases": {
        "main": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.07822251056763327,
              "tier": 1
            },
            "control": {
              "E": 0.011069594072166582,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 6.066429903181018,
          "tier_direction": "unchanged"
        },
        "repeat-seed": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.04697019298545217,
              "tier": 1
            },
            "control": {
              "E": 0.01763443846274973,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 1.6635491163878053,
          "tier_direction": "unchanged"
        },
        "repeat-system": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.14185020924126024,
              "tier": 0
            },
            "control": {
              "E": 0.07864043014323893,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.8037822146049863,
          "tier_direction": "worsened"
        }
      },
      "confirmation": "unsettled",
      "control": "exp01-raw",
      "descriptive": {
        "adjacent_time_similarity": {
          "main": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.1195310577750206,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": -0.032717905938625336,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.11926710605621338,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": -0.017003744840621948,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.11903133243322372,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.027665192261338234,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.11896966397762299,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.06638682633638382,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.11889597773551941,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.09405852854251862,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 112700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9964733123779297,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9904256463050842,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9965022206306458,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.990788459777832,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9964118599891663,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9914138317108154,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.996241569519043,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9909675121307373,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9961069822311401,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9911242723464966,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 112700
              }
            ]
          },
          "repeat-seed": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.09319976717233658,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": -0.0356006845831871,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.09227855503559113,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": -0.021171363070607185,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.09207441657781601,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.02127128466963768,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.09205398708581924,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.05872716009616852,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.09201330691576004,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.08604976534843445,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 112700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9965821504592896,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9906841516494751,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9966053366661072,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9907867312431335,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9963721632957458,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9910871386528015,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9963014125823975,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9909143447875977,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9959641098976135,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9904946684837341,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 112700
              }
            ]
          },
          "repeat-system": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.031433455646038055,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.012948038056492805,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.03546716645359993,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.029868151992559433,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.03510734438896179,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.0667312741279602,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.034987758845090866,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.09867553412914276,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.032454416155815125,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.0630800649523735,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 112700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9964644908905029,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9903100728988647,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9964809417724609,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9908298850059509,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.996369481086731,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9914312958717346,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.996112585067749,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9907151460647583,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9958916902542114,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9904041886329651,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 112700
              }
            ]
          }
        },
        "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
        "loss": "context only",
        "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
      },
      "experiment": "exp04",
      "reasons": [
        "the main/control endpoint is unsettled",
        "the repeat-system/arm endpoint is unsettled",
        "the repeat-seed/arm endpoint is unsettled"
      ],
      "scope_disposition": {
        "dependent_launch_allowed": true,
        "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
        "scope49_disposition": "none"
      }
    },
    "exp01-f12": {
      "arm": "exp01-f12",
      "cases": {
        "main": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.04955849067979028,
              "tier": 1
            },
            "control": {
              "E": 0.011069594072166582,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 3.476992594010316,
          "tier_direction": "unchanged"
        },
        "repeat-seed": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.09316469672181629,
              "tier": 1
            },
            "control": {
              "E": 0.01763443846274973,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 4.283111051061456,
          "tier_direction": "unchanged"
        },
        "repeat-system": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.15456749202685538,
              "tier": 0
            },
            "control": {
              "E": 0.07864043014323893,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.9654965231665157,
          "tier_direction": "worsened"
        }
      },
      "confirmation": "unsettled",
      "control": "exp01-raw",
      "descriptive": {
        "adjacent_time_similarity": {
          "main": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.004805039148777723,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": -0.0008353182347491384,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.0019609369337558746,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.01864665560424328,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.0016600999515503645,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.05870116129517555,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.0014038097579032183,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.09292600303888321,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.0012766947038471699,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.11794627457857132,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 112700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9964733123779297,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9904256463050842,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9965022206306458,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.990788459777832,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9964118599891663,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9914138317108154,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.996241569519043,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9909675121307373,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9961069822311401,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9911242723464966,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 112700
              }
            ]
          },
          "repeat-seed": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.01308339461684227,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": -0.01043841801583767,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.00669738557189703,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.008830025792121887,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.0062128701247274876,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.0476517416536808,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.0058412146754562855,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.08261475712060928,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": -0.005723872222006321,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.10846047848463058,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 112700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9965821504592896,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9906841516494751,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9966053366661072,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9907867312431335,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9963721632957458,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9910871386528015,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9963014125823975,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9909143447875977,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9959641098976135,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9904946684837341,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 112700
              }
            ]
          },
          "repeat-system": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.0048432922922074795,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.0027399512473493814,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.0019532537553459406,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.017434952780604362,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.0019375999690964818,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.057734906673431396,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.00526540819555521,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.029350150376558304,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.0059949313290417194,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.08801896125078201,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 112700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9964644908905029,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9903100728988647,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9964809417724609,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9908298850059509,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.996369481086731,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9914312958717346,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.996112585067749,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9907151460647583,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9958916902542114,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9904041886329651,
                    "name": "h1",
                    "order": 1
                  }
                ],
                "step": 112700
              }
            ]
          }
        },
        "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
        "loss": "context only",
        "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
      },
      "experiment": "exp04",
      "reasons": [
        "the main/arm endpoint is unsettled",
        "the main/control endpoint is unsettled",
        "the repeat-seed/arm endpoint is unsettled"
      ],
      "scope_disposition": {
        "dependent_launch_allowed": true,
        "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
        "scope49_disposition": "none"
      }
    },
    "locked-f1": {
      "arm": "locked-f1",
      "cases": {
        "main": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.04615102941421912,
              "tier": 1
            },
            "control": {
              "E": 0.0344080542047465,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.3412856518882347,
          "tier_direction": "unchanged"
        },
        "repeat-seed": {
          "direction": "improvement",
          "endpoint_status": {
            "arm": "settled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.023682017735151037,
              "tier": 1
            },
            "control": {
              "E": 0.0412830122941967,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.42634957046290684,
          "tier_direction": "unchanged"
        },
        "repeat-system": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.0710851362747344,
              "tier": 1
            },
            "control": {
              "E": 0.04919948294071304,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.4448350272378731,
          "tier_direction": "unchanged"
        }
      },
      "confirmation": "unsettled",
      "control": "locked-raw",
      "descriptive": {
        "adjacent_time_similarity": {
          "main": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9966707825660706,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9920898675918579,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9835746884346008,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9614005088806152,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9215267300605774,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.824569582939148,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.6738126277923584,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.4383074939250946,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.2501904368400574,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.10665538161993027,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.04715743288397789,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.02035294845700264,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.007930945605039597,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9966904520988464,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9924165606498718,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9819537401199341,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9559968113899231,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9117640256881714,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.8043308854103088,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.6705237030982971,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.4614342451095581,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.32837390899658203,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.25986436009407043,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.2544116675853729,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.3187520205974579,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.43171408772468567,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9967541694641113,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9926725625991821,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9827526807785034,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9581771492958069,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9159895181655884,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.8188791871070862,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.7028253078460693,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.5263011455535889,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.4186973571777344,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.37381190061569214,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.4037807583808899,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.45312535762786865,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.6341452598571777,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9967648983001709,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9925332069396973,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9828145503997803,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9583020210266113,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9170644879341125,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.822171151638031,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.7211024165153503,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.5568162202835083,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.46974191069602966,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.41403719782829285,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.4868323504924774,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.5096824765205383,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.6714473962783813,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9968438744544983,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9927179217338562,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9830482006072998,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9585105180740356,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9209081530570984,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.8324716687202454,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.7379913330078125,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.5822348594665527,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.5172905325889587,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.4637739360332489,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.5578884482383728,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.5581449866294861,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.6767210960388184,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 112700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999837279319763,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999697208404541,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999352097511292,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998775124549866,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999712347984314,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999390184879303,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985547661781311,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9969659447669983,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9927595257759094,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9844540953636169,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9629203677177429,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9224951267242432,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999841451644897,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999608397483826,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999178647994995,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998276233673096,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996066689491272,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991987943649292,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.99812251329422,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9962421655654907,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.991174578666687,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9839316010475159,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9641760587692261,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9422818422317505,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999825358390808,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999604225158691,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999110698699951,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998188614845276,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995752573013306,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991735816001892,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981133341789246,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964744448661804,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9917871952056885,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9857177734375,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9687786102294922,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9519308805465698,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999820590019226,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999958872795105,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999905526638031,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999799907207489,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995323419570923,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991028308868408,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9979533553123474,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9962454438209534,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9916363954544067,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9859731197357178,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9701394438743591,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9608948826789856,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999818801879883,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999598264694214,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999110102653503,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998094439506531,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995533227920532,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991236329078674,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9979623556137085,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9961771368980408,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.991576075553894,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9859146475791931,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9697723984718323,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9595596194267273,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 112700
              }
            ]
          },
          "repeat-seed": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.996708869934082,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9921917915344238,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9838249087333679,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9622093439102173,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9227829575538635,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.828664243221283,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.6854045391082764,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.4445897340774536,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.2522827088832855,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.10424134880304337,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.04277215152978897,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.01777574047446251,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.006403487175703049,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9965741634368896,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9920174479484558,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9821437001228333,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9565058946609497,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9110372066497803,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.8023985624313354,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.6586048007011414,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.42942291498184204,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.2822277247905731,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.18980367481708527,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.18434511125087738,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.2364448755979538,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.31238603591918945,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9966338872909546,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9921594262123108,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9814533591270447,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9549652338027954,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.91105717420578,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.8085794448852539,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.6834492087364197,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.5008667707443237,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.3927289545536041,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.35454127192497253,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.3778610825538635,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.43487223982810974,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.6098452210426331,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9966120719909668,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9924116134643555,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9820225834846497,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.956578254699707,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9151694774627686,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.8186303973197937,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.7066662311553955,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.5353250503540039,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.45404478907585144,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.40334102511405945,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.46876317262649536,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.49875274300575256,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.65851891040802,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.996562123298645,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9921054244041443,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9816699028015137,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9560009837150574,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9140320420265198,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.8175833225250244,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.7168225049972534,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.5572716593742371,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.49134334921836853,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.43823525309562683,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.5324790477752686,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.5378143191337585,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.6542691588401794,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 112700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999827742576599,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999688863754272,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999354481697083,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999873161315918,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999718189239502,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993919730186462,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985952973365784,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.997002363204956,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9928239583969116,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9847432971000671,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9634863138198853,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.925688624382019,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999833703041077,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999625086784363,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999166131019592,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998229742050171,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995944499969482,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992048740386963,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981563687324524,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964001178741455,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9916437864303589,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9845506548881531,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9650442004203796,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9426186680793762,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999880194664001,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999825358390808,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999536275863647,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998936653137207,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997814297676086,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994892477989197,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989191889762878,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9974373579025269,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9951664805412292,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9891615509986877,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9811629056930542,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9586803913116455,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9403875470161438,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999828934669495,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999566674232483,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999033212661743,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998025298118591,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999534547328949,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999093770980835,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978678226470947,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9961755275726318,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9914381504058838,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.985751748085022,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.969436764717102,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9586381316184998,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999809861183167,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.99996018409729,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999132752418518,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998128414154053,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995751976966858,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991310238838196,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9980255365371704,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9965376853942871,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9923426508903503,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9874482750892639,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9733120203018188,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9656933546066284,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 112700
              }
            ]
          },
          "repeat-system": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9893693327903748,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9747711420059204,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9491488933563232,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.8853276968002319,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.7820672392845154,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.5794097781181335,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.3627089858055115,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.1652025431394577,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.0749540627002716,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.029926463961601257,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.010080614127218723,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.0011815219186246395,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.0016937174368649721,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9891822338104248,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9755899310112,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9431524872779846,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.8702897429466248,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.7551528215408325,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.5484001040458679,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.3767133057117462,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.2402121126651764,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.18729059398174286,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.2021113783121109,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.21801172196865082,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.28418347239494324,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.3539729714393616,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.989568293094635,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9756695628166199,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9431278705596924,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.8711649775505066,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.7625555992126465,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.5680919289588928,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.4125223755836487,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.29638317227363586,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.2576044201850891,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.28053703904151917,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.3144840598106384,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.38057762384414673,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.5493876934051514,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9894107580184937,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9753567576408386,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9421719312667847,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.8689127564430237,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.7620391845703125,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.566577672958374,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.42361459136009216,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.3180650770664215,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.29670092463493347,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.31771180033683777,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.38091161847114563,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.4376797080039978,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.6293333768844604,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9892618060112,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9748639464378357,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9402034878730774,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.864090085029602,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.7571356296539307,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.5713180303573608,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.44282829761505127,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.3422194719314575,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.3374705910682678,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.35265815258026123,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.4321959316730499,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.47666019201278687,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.6615689992904663,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 112700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999836683273315,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999704957008362,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999396800994873,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998784065246582,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997159242630005,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994155764579773,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986107349395752,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9970688223838806,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9929354786872864,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.985227108001709,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9650446772575378,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.926563024520874,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999880194664001,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999836087226868,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999628663063049,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999921441078186,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998414516448975,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999629557132721,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992631673812866,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9983028769493103,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9968282580375671,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9927104711532593,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9866904020309448,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.970236599445343,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9527369141578674,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999815821647644,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999589920043945,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999069571495056,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997972846031189,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995140433311462,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990220665931702,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976761341094971,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9958189725875854,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9903712868690491,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9833876490592957,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9633936882019043,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9457546472549438,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999821186065674,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999570250511169,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999034404754639,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999807596206665,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995778203010559,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991448521614075,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9979879856109619,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.996306300163269,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9916086196899414,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9861067533493042,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9698157906532288,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9578278660774231,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987781047821,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999815821647644,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999589920043945,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999058246612549,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998112916946411,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995810389518738,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991647005081177,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.998124897480011,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9965490698814392,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.992338240146637,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9875491857528687,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9735011458396912,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9643779397010803,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 112700
              }
            ]
          }
        },
        "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
        "loss": "context only",
        "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
      },
      "experiment": "exp04",
      "reasons": [
        "the main/arm endpoint is unsettled",
        "the main/control endpoint is unsettled"
      ],
      "scope_disposition": {
        "dependent_launch_allowed": true,
        "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
        "scope49_disposition": "none"
      }
    },
    "locked-f12": {
      "arm": "locked-f12",
      "cases": {
        "main": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "unsettled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.06013616119727379,
              "tier": 1
            },
            "control": {
              "E": 0.0344080542047465,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.747735016907122,
          "tier_direction": "unchanged"
        },
        "repeat-seed": {
          "direction": "improvement",
          "endpoint_status": {
            "arm": "unsettled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.03895762366412014,
              "tier": 1
            },
            "control": {
              "E": 0.0412830122941967,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": false,
          "reasons": [
            "the effect is below the registered twenty-percent line with no matching tier change"
          ],
          "relative_E_effect": 0.05632797852794896,
          "tier_direction": "unchanged"
        },
        "repeat-system": {
          "direction": "worsening",
          "endpoint_status": {
            "arm": "settled",
            "control": "settled"
          },
          "observed_fit": {
            "arm": {
              "E": 0.061705123279830354,
              "tier": 1
            },
            "control": {
              "E": 0.04919948294071304,
              "tier": 1
            }
          },
          "percentage_applicable": true,
          "qualifies_effect": true,
          "reasons": [],
          "relative_E_effect": 0.2541823529769005,
          "tier_direction": "unchanged"
        }
      },
      "confirmation": "unsettled",
      "control": "locked-raw",
      "descriptive": {
        "adjacent_time_similarity": {
          "main": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9876847267150879,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.96944260597229,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9357204437255859,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.8526566624641418,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.7239997982978821,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.49281764030456543,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.2849941551685333,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.12395106256008148,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.052989374846220016,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.02013605460524559,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.007529287599027157,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.0033469991758465767,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": -0.0011606552870944142,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9871696829795837,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9684449434280396,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9287761449813843,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.8353697061538696,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.6893578171730042,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.4415742754936218,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.24586370587348938,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.09931378066539764,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.042618755251169205,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.014744516462087631,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.004835011437535286,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.001994783990085125,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": -0.0033917922992259264,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9859890341758728,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9647995829582214,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9215041399002075,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.8182504773139954,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.659761369228363,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.4044906497001648,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.21746589243412018,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.08726835995912552,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.038364510983228683,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.023537060245871544,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.0263957716524601,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.043164532631635666,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.07676658034324646,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9855214357376099,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9642558693885803,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.918163537979126,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.8119564056396484,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.6479254961013794,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.391568124294281,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.20833154022693634,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.08477374166250229,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.04563579708337784,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.03733444958925247,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.05842522159218788,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.09972462803125381,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.16749756038188934,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9847329258918762,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9618474245071411,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9169881343841553,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.8078361749649048,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.6506189107894897,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.4019777774810791,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.2352926880121231,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.1320856213569641,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.10396428406238556,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.09983690828084946,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.158980593085289,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.20346343517303467,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.26821374893188477,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 112700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999837279319763,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999697208404541,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999352097511292,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998775124549866,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999712347984314,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999390184879303,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985547661781311,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9969659447669983,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9927595257759094,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9844540953636169,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9629203677177429,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9224951267242432,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999841451644897,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999608397483826,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999178647994995,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998276233673096,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9996066689491272,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991987943649292,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.99812251329422,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9962421655654907,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.991174578666687,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9839316010475159,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9641760587692261,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9422818422317505,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999825358390808,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999604225158691,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999110698699951,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998188614845276,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995752573013306,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991735816001892,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981133341789246,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964744448661804,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9917871952056885,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9857177734375,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9687786102294922,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9519308805465698,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999820590019226,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.999958872795105,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999905526638031,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999799907207489,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995323419570923,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991028308868408,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9979533553123474,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9962454438209534,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9916363954544067,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9859731197357178,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9701394438743591,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9608948826789856,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999818801879883,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999598264694214,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999110102653503,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998094439506531,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995533227920532,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991236329078674,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9979623556137085,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9961771368980408,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.991576075553894,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9859146475791931,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9697723984718323,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9595596194267273,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 112700
              }
            ]
          },
          "repeat-seed": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9876596927642822,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9688193798065186,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9338690638542175,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.8520930409431458,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.7242307066917419,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.4984109699726105,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.29016900062561035,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.12524740397930145,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.05150873214006424,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.02151443436741829,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.007847487926483154,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.0013329308712854981,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.00041031313594430685,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9863818287849426,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9665213823318481,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9240191578865051,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.8233514428138733,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.6723672747612,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.4233142137527466,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.23988817632198334,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.09305302798748016,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.040660612285137177,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.020399875938892365,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.024115201085805893,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.047252144664525986,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.09350267052650452,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9850890040397644,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9629500508308411,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.916533350944519,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.8091667294502258,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.6452609300613403,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.3916861414909363,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.20427973568439484,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.08489010483026505,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.038830310106277466,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.02669476717710495,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.03620820865035057,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.060873180627822876,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.11450578272342682,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9836836457252502,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9593127369880676,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9097181558609009,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.7937976121902466,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.623374879360199,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.36762407422065735,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.19632767140865326,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.07633822411298752,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.03850514814257622,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.02104945108294487,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.025054926052689552,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.039429280906915665,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.06090700253844261,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9827489256858826,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9568927884101868,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9041284322738647,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.7802560925483704,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.6086540818214417,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.3501494824886322,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.1800297200679779,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.066393181681633,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.027829743921756744,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.01780833676457405,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.023381076753139496,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.0463426299393177,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.09024476259946823,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 112700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999827742576599,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999688863754272,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999354481697083,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999873161315918,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999718189239502,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9993919730186462,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9985952973365784,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.997002363204956,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9928239583969116,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9847432971000671,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9634863138198853,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.925688624382019,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999884963035583,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999833703041077,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999625086784363,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999166131019592,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998229742050171,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995944499969482,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992048740386963,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9981563687324524,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9964001178741455,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9916437864303589,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9845506548881531,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9650442004203796,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9426186680793762,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999880194664001,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999825358390808,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999536275863647,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9998936653137207,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997814297676086,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9994892477989197,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9989191889762878,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9974373579025269,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9951664805412292,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9891615509986877,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9811629056930542,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9586803913116455,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9403875470161438,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999828934669495,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999566674232483,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999033212661743,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998025298118591,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999534547328949,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.999093770980835,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9978678226470947,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9961755275726318,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9914381504058838,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.985751748085022,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.969436764717102,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9586381316184998,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999809861183167,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.99996018409729,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999132752418518,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998128414154053,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995751976966858,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991310238838196,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9980255365371704,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9965376853942871,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9923426508903503,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9874482750892639,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9733120203018188,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9656933546066284,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 112700
              }
            ]
          },
          "repeat-system": {
            "arm": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9615857005119324,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.90608811378479,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.8126748204231262,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.6251658797264099,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.4132542014122009,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.19344350695610046,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.07935895025730133,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.03134886920452118,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.01115353126078844,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.0019414183916524053,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": -0.001311177504248917,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": -0.001955225830897689,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": -0.0024598941672593355,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9598480463027954,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9016213417053223,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.7970263957977295,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.5955512523651123,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.379767507314682,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.17416341602802277,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.07694987207651138,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.02868107333779335,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.014398090541362762,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.012204616330564022,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.021154817193746567,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.04613606259226799,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.08217640221118927,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9540629982948303,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.8894875645637512,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.7702212333679199,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.5521804094314575,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.33434605598449707,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.13895274698734283,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.05539887398481369,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.02165393903851509,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.008751432411372662,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": -0.0006982552004046738,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": -0.0003194652672391385,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": -0.002234750660136342,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.00015464812167920172,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9510906934738159,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.8818121552467346,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.748634934425354,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.5181584358215332,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.29521217942237854,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.12512540817260742,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.046495530754327774,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.01596970111131668,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.005382606294006109,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.002998949959874153,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.007910823449492455,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.03056042268872261,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.06334389001131058,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.949860692024231,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.8797006607055664,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.7510967254638672,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.5155072808265686,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.2965089678764343,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.1236242800951004,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.05230078101158142,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.025258639827370644,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.026974089443683624,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.03322690725326538,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.07609127461910248,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.087810218334198,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.18883301317691803,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 112700
              }
            ],
            "control": [
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999883770942688,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999836683273315,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999704957008362,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999396800994873,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998784065246582,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9997159242630005,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9994155764579773,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9986107349395752,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9970688223838806,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9929354786872864,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.985227108001709,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9650446772575378,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.926563024520874,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 0
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999880194664001,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999836087226868,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999628663063049,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.999921441078186,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998414516448975,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.999629557132721,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9992631673812866,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9983028769493103,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9968282580375671,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9927104711532593,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9866904020309448,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.970236599445343,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9527369141578674,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 28175
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999882578849792,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999815821647644,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999589920043945,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999069571495056,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9997972846031189,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995140433311462,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9990220665931702,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9976761341094971,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9958189725875854,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9903712868690491,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9833876490592957,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9633936882019043,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9457546472549438,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 56350
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.9999881386756897,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999821186065674,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999570250511169,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999034404754639,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.999807596206665,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995778203010559,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991448521614075,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.9979879856109619,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.996306300163269,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.9916086196899414,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9861067533493042,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9698157906532288,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9578278660774231,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 84525
              },
              {
                "layers": [
                  {
                    "adjacent_cosine_mean": 0.999987781047821,
                    "name": "input",
                    "order": 0
                  },
                  {
                    "adjacent_cosine_mean": 0.9999815821647644,
                    "name": "h1",
                    "order": 1
                  },
                  {
                    "adjacent_cosine_mean": 0.9999589920043945,
                    "name": "h2",
                    "order": 2
                  },
                  {
                    "adjacent_cosine_mean": 0.9999058246612549,
                    "name": "h3",
                    "order": 3
                  },
                  {
                    "adjacent_cosine_mean": 0.9998112916946411,
                    "name": "h4",
                    "order": 4
                  },
                  {
                    "adjacent_cosine_mean": 0.9995810389518738,
                    "name": "h5",
                    "order": 5
                  },
                  {
                    "adjacent_cosine_mean": 0.9991647005081177,
                    "name": "h6",
                    "order": 6
                  },
                  {
                    "adjacent_cosine_mean": 0.998124897480011,
                    "name": "h7",
                    "order": 7
                  },
                  {
                    "adjacent_cosine_mean": 0.9965490698814392,
                    "name": "h8",
                    "order": 8
                  },
                  {
                    "adjacent_cosine_mean": 0.992338240146637,
                    "name": "h9",
                    "order": 9
                  },
                  {
                    "adjacent_cosine_mean": 0.9875491857528687,
                    "name": "h10",
                    "order": 10
                  },
                  {
                    "adjacent_cosine_mean": 0.9735011458396912,
                    "name": "h11",
                    "order": 11
                  },
                  {
                    "adjacent_cosine_mean": 0.9643779397010803,
                    "name": "h12",
                    "order": 12
                  }
                ],
                "step": 112700
              }
            ]
          }
        },
        "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
        "loss": "context only",
        "note": "adjacent-time hidden-state similarity is associated evidence only; no cosine threshold and no causal claim"
      },
      "experiment": "exp04",
      "reasons": [
        "the main/control endpoint is unsettled",
        "the repeat-seed/arm endpoint is unsettled"
      ],
      "scope_disposition": {
        "dependent_launch_allowed": true,
        "reason": "the unsettled branch is registered and equally recorded; no continuation runs (the no-continuation policy) and no scope change is proposed",
        "scope49_disposition": "none"
      }
    }
  },
  "dependent_launch_allowed": true,
  "experiment": "exp04",
  "gap_59_08": "GAP-59-08: E is the frozen scorecard's position-error score; no energy bar or scorer definition is adjudicated here",
  "predictions_comparison": {
    "exp01-f1": {
      "case_directions": {
        "main": "worsening",
        "repeat-seed": "worsening",
        "repeat-system": "worsening"
      },
      "observed_confirmation": "unsettled",
      "observed_disposition": "none",
      "registered_hypothesis": "under the hypothesis, encoded harmonic improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule"
    },
    "exp01-f12": {
      "case_directions": {
        "main": "worsening",
        "repeat-seed": "worsening",
        "repeat-system": "worsening"
      },
      "observed_confirmation": "unsettled",
      "observed_disposition": "none",
      "registered_hypothesis": "under the hypothesis, encoded harmonic improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule"
    },
    "locked-f1": {
      "case_directions": {
        "main": "worsening",
        "repeat-seed": "improvement",
        "repeat-system": "worsening"
      },
      "observed_confirmation": "unsettled",
      "observed_disposition": "none",
      "registered_hypothesis": "under the hypothesis, encoded harmonic improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule"
    },
    "locked-f12": {
      "case_directions": {
        "main": "worsening",
        "repeat-seed": "improvement",
        "repeat-system": "worsening"
      },
      "observed_confirmation": "unsettled",
      "observed_disposition": "none",
      "registered_hypothesis": "under the hypothesis, encoded harmonic improves the fit: this arm's E is below the control's on all three registered cases under the registered effect rule"
    }
  },
  "proposed_change": null,
  "roadmap_comparison": "each contrast's confirmation label is read against the committed prediction table; the roadmap's next experiment proceeds only when this review allows the dependent launch",
  "schema": "phase67-review/v1",
  "scope49_disposition": "none"
}
```
