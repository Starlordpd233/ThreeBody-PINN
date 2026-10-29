"""Read-only probe: does the time input survive through the network's depth?

Compares the locked network at initialization with the committed Rung-1
weights of arm r1-1632 (Adam and polish states), on that arm's own training
orbit, in CPU float64. Writes nothing; prints a table.
"""
import sys
from pathlib import Path

import torch
import torch.nn.functional as F

REPO = Path("<home>/Desktop/3_body_problem/.worktrees/trainex")
sys.path.insert(0, str(REPO))

from pinn.architecture_spec import ArchitectureSpec  # noqa: E402
from pinn.network import build_network  # noqa: E402
from pinn.verification.feasibility_scorecard import load_scorecard  # noqa: E402
from pinn.verification.learnability_arms import SEED, arm_spec  # noqa: E402
from pinn.verification.learnability_data import load_arm_data, open_real_context  # noqa: E402

torch.set_grad_enabled(True)
cpu = torch.device("cpu")
ctx = open_real_context(repo_root=REPO)
data = load_arm_data(arm_spec("r1-1632"), ctx, scorecard=load_scorecard(),
                     dtype=torch.float64, device=cpu)
X = data.data_points.tau_ic13.clone()
M = data.data_points.masses
Y = data.data_points.targets
tau = X[:, 0]
print(f"points {X.shape[0]}, tau range [{tau.min():.3f}, {tau.max():.3f}], "
      f"IC13 constant across rows: {bool((X[:, 1:] == X[0, 1:]).all())}")


def layer_stats(a):
    centered = a - a.mean(dim=0, keepdim=True)
    # share of the representation that changes with time
    moving = centered.pow(2).mean().sqrt() / a.pow(2).mean().sqrt()
    # how alike the representation is at neighbouring times (0.01 apart)
    adj = F.cosine_similarity(centered[:-1], centered[1:], dim=1).mean()
    # how much of the vector's energy sits in its single largest feature
    spike = (a.pow(2).max(dim=1).values / a.pow(2).sum(dim=1)).median()
    return moving.item(), adj.item(), spike.item()


def probe(model, label):
    print(f"\n== {label}")
    w_tau = model.input_layer.weight[:, 0].detach().abs() * model.input_layer.omega_0
    cycles = w_tau * 2.0 / (2 * torch.pi)  # cycles across tau in [-1, 1]
    print(f"first-layer time frequency: median {cycles.median():.2f}, max {cycles.max():.2f} "
          f"cycles per window")
    print(f"{'layer':<6}{'skip/siren':>11}{'moving':>9}{'adj-cos':>9}{'spike':>8}")
    with torch.no_grad():
        x = model.input_layer(X)
        m, adj, sp = layer_stats(x)
        print(f"{'in':<6}{'':>11}{m:>9.4f}{adj:>9.4f}{sp:>8.4f}")
        for i, layer in enumerate(model.hidden_layers, 1):
            if hasattr(layer, "siren"):
                s = layer.siren(x)
                k = layer.layernorm(x) ** layer.power_p
                ratio = (k.norm(dim=1) / s.norm(dim=1)).median().item()
                x = s + k
                tag = f"{ratio:.1f}"
            else:
                x = layer(x)
                tag = ""
            m, adj, sp = layer_stats(x)
            print(f"{'h' + str(i):<6}{tag:>11}{m:>9.4f}{adj:>9.4f}{sp:>8.4f}")
    Xg = X.clone().requires_grad_(True)
    out = model(Xg, M)
    tvr = ((out - out.mean(0)).norm() / (Y - Y.mean(0)).norm()).item()
    d_out = torch.stack([torch.autograd.grad(out[:, j].sum(), Xg, retain_graph=True)[0][:, 0]
                         for j in range(out.shape[1])], dim=1)
    d_true = torch.gradient(Y, spacing=(tau,), dim=0)[0]
    rough = (d_out.pow(2).mean().sqrt() / d_true.pow(2).mean().sqrt()).item()
    print(f"output: time-variation ratio {tvr:.4f}; rms d/dtau ratio (net/true) {rough:.3g}")


init = build_network(ArchitectureSpec(seed=SEED), dtype=torch.float64, device=cpu)
probe(init, "locked network at initialization (seed 42)")
arm = REPO / ".planning/phases/60-single-system-learnability/evidence/arms/r1-1632"
for state in ("adam", "polish"):
    net = build_network(ArchitectureSpec(seed=SEED), dtype=torch.float64, device=cpu)
    sd = torch.load(arm / f"{state}.weights", weights_only=True, map_location=cpu)
    net.load_state_dict({k: v.to(torch.float64) for k, v in sd.items()})
    probe(net, f"trained r1-1632, {state} state")
