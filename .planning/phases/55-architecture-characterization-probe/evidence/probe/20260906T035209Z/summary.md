# Architecture characterization probe

## Provenance

- command: `python -m pinn.verification.architecture_characterization_probe`
- git_sha: `2b1a4fd1490bba817639485063888b49a365b90d` (available=True)
- git_worktree_dirty: `True` (available=True)
- timestamp: `2026-09-06T03:52:09.405712+00:00`
- precision/device: `float64` / `cpu`
- n_col: `16`
- median_convention: numpy.median: arithmetic mean of the two central order statistics (explicitly not torch.median's lower-of-two)
- ic13_rng_scheme: zero: zero-vector; random_tanh: numpy.random.default_rng(seed + IC13_RNG_OFFSET) standard-normal then elementwise tanh

## Cases

| seed / IC | ‖r′‖ | ‖v′‖ | ‖a′‖ = ‖d²r′/du²‖ | ‖F_grav‖ | min pairwise sep | `R̄` median | `front_idx` |
|---|---|---|---|---|---|---|---|
| 41 (seed=41, m=(1.0, 1.0, 1.0), IC13=zero) | 1.085 | 251.8 | 1.975e+05 | 3.131 | 0.784 | 1.301e+10 | 0 |
| 42 (seed=42, m=(1.0, 1.0, 1.0), IC13=zero) | 1.009 | 313.5 | 2.411e+05 | 4.41 | 0.6072 | 1.938e+10 | 0 |
| 43 (seed=43, m=(1.0, 1.0, 1.0), IC13=zero) | 0.8298 | 297.9 | 2.078e+05 | 5.913 | 0.5815 | 1.440e+10 | 0 |
| 0 (seed=0, m=(1.0, 1.0, 1.0), IC13=zero) | 0.9759 | 301.8 | 2.040e+05 | 5.803 | 0.5542 | 1.387e+10 | 0 |
| 7 (seed=7, m=(1.0, 1.0, 1.0), IC13=zero) | 1.083 | 239.4 | 2.027e+05 | 3.616 | 0.6767 | 1.370e+10 | 0 |
| 41-variable-mass (seed=41, m=(1.0, 0.8, 0.6), IC13=random_tanh) | 1.124 | 327.4 | 1.917e+05 | 2.807 | 0.7188 | 1.224e+10 | 0 |
