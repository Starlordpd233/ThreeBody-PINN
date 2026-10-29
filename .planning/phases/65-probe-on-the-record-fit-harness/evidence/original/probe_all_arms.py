"""Read-only: the same time-signal measures on the official state of all seven arms."""
import json
import sys
from pathlib import Path

import torch
import torch.nn.functional as F

REPO = Path("<home>/Desktop/3_body_problem/.worktrees/trainex")
sys.path.insert(0, str(REPO))

from pinn.architecture_spec import ArchitectureSpec  # noqa: E402
from pinn.network import build_network  # noqa: E402
from pinn.verification.diagnostic_architecture import build_network_with_first_omega  # noqa: E402
from pinn.verification.feasibility_scorecard import load_scorecard  # noqa: E402
from pinn.verification.learnability_arms import SEED, arm_spec  # noqa: E402
from pinn.verification.learnability_data import load_arm_data, open_real_context  # noqa: E402

cpu = torch.device("cpu")
ARMS = REPO / ".planning/phases/60-single-system-learnability/evidence/arms"
ctx = open_real_context(repo_root=REPO)


def net_for(omega):
    if omega == 30.0:
        return build_network(ArchitectureSpec(seed=SEED), dtype=torch.float64, device=cpu)
    return build_network_with_first_omega(omega, seed=SEED, dtype=torch.float64, device=cpu)


def measures(model, X, M, Y):
    adj = []
    with torch.no_grad():
        x = model.input_layer(X)
        for layer in model.hidden_layers:
            x = layer(x)
            c = x - x.mean(dim=0, keepdim=True)
            adj.append(F.cosine_similarity(c[:-1], c[1:], dim=1).mean().item())
    Xg = X.clone().requires_grad_(True)
    out = model(Xg, M)
    tvr = ((out - out.mean(0)).norm() / (Y - Y.mean(0)).norm()).item()
    d_out = torch.stack([torch.autograd.grad(out[:, j].sum(), Xg, retain_graph=True)[0][:, 0]
                         for j in range(9)], dim=1)
    d_true = torch.gradient(Y, spacing=(X[:, 0],), dim=0)[0]
    rough = (d_out.pow(2).mean().sqrt() / d_true.pow(2).mean().sqrt()).item()
    w = model.input_layer.weight[:, 0].detach().abs() * model.input_layer.omega_0 / torch.pi
    return adj, tvr, rough, w.median().item()


print(f"{'arm':<15}{'state':<8}{'1st-layer cyc':>14}{'adj h1':>8}{'adj h2':>8}"
      f"{'adj h3..h12 range':>23}{'out move':>10}{'d/dt x truth':>14}")
for rec_path in sorted(ARMS.glob("*/record.json")):
    rec = json.loads(rec_path.read_text())
    arm_id, state, omega = rec["arm_id"], rec["better_state"], float(rec["first_omega_0"])
    data = load_arm_data(arm_spec(arm_id), ctx, scorecard=load_scorecard(),
                         dtype=torch.float64, device=cpu)
    X, M, Y = data.data_points.tau_ic13, data.data_points.masses, data.data_points.targets
    for label, model in (("init", net_for(omega)), (state, None)):
        if model is None:
            model = net_for(omega)
            sd = torch.load(rec_path.parent / f"{state}.weights", weights_only=True,
                            map_location=cpu)
            model.load_state_dict({k: v.to(torch.float64) for k, v in sd.items()})
        adj, tvr, rough, cyc = measures(model, X, M, Y)
        deep = f"{min(adj[2:]):.3f} to {max(adj[2:]):.3f}"
        print(f"{arm_id:<15}{label:<8}{cyc:>14.2f}{adj[0]:>8.3f}{adj[1]:>8.3f}"
              f"{deep:>23}{tvr:>10.4f}{rough:>14.3g}")
