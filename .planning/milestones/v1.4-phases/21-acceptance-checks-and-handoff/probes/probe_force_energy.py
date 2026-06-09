import torch

def test_force_energy():
    masses = torch.tensor([1.0, 1.5, 0.75], dtype=torch.float64)
    pos = torch.tensor(
        [
            [-0.75, 0.15, 0.20],
            [0.45, -0.35, -0.10],
            [0.10, 0.80, -0.25],
        ],
        dtype=torch.float64,
    )
    vel = torch.tensor(
        [
            [0.05, -0.03, 0.02],
            [-0.02, 0.04, -0.01],
            [0.01, -0.02, 0.03],
        ],
        dtype=torch.float64,
    )
    eps_train = 1e-5

    manual_accel = torch.zeros_like(pos)
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            r_ji = pos[j] - pos[i]
            safe_dist = torch.sqrt(torch.sum(r_ji**2) + eps_train**2)
            manual_accel[i] += masses[j] * r_ji / safe_dist**3

    pos_var = pos.clone().detach().requires_grad_(True)
    potential = torch.zeros((), dtype=torch.float64)
    for i in range(3):
        for j in range(i + 1, 3):
            r_ij = pos_var[j] - pos_var[i]
            safe_dist = torch.sqrt(torch.sum(r_ij**2) + eps_train**2)
            potential -= masses[i] * masses[j] / safe_dist

    dV_dpos = torch.autograd.grad(potential, pos_var)[0]
    accel_from_hamiltonian = -dV_dpos / masses.unsqueeze(1)

    kinetic = 0.5 * torch.sum(masses.unsqueeze(1) * vel**2)
    hamiltonian = kinetic + potential.detach()
    relative_error = (
        torch.norm(accel_from_hamiltonian - manual_accel)
        / torch.norm(manual_accel)
    ).item()

    assert torch.isfinite(hamiltonian), "Matched-Plummer Hamiltonian is not finite"
    assert relative_error < 1e-5, f"Force-energy consistency failed: {relative_error}"
    print(
        "Force-Energy Consistency check passed! "
        f"relative_error: {relative_error:.2e}; "
        f"H_epsilon: {hamiltonian.item():.12e}; eps_train: {eps_train:.1e}"
    )

if __name__ == "__main__":
    test_force_energy()
