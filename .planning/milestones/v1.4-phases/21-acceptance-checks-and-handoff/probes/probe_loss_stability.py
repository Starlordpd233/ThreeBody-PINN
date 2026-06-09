import torch
import torch.nn as nn

class SineLayer(nn.Module):
    def __init__(self, in_features, out_features, omega_0=1.0, is_first=False):
        super().__init__()
        self.omega_0 = omega_0
        self.linear = nn.Linear(in_features, out_features)

        with torch.no_grad():
            if is_first:
                bound = 1.0 / in_features
            else:
                bound = (6.0 / in_features) ** 0.5 / omega_0
            self.linear.weight.uniform_(-bound, bound)
            self.linear.bias.uniform_(-bound, bound)

    def forward(self, x):
        return torch.sin(self.omega_0 * self.linear(x))


class RepresentativeSQRSiren(nn.Module):
    def __init__(self, input_dim=14, width=256, hidden_layers=12, output_dim=9):
        super().__init__()
        self.first = SineLayer(input_dim, width, omega_0=30.0, is_first=True)
        self.hidden = nn.ModuleList(
            SineLayer(width, width, omega_0=1.0, is_first=False)
            for _ in range(hidden_layers - 1)
        )
        self.skip_norms = nn.ModuleList(
            nn.LayerNorm(width, eps=1e-5, elementwise_affine=False)
            for _ in range(hidden_layers - 1)
        )
        self.final = nn.Linear(width, output_dim)

    def forward(self, x):
        x = self.first(x)
        for layer_number, (layer, norm) in enumerate(
            zip(self.hidden, self.skip_norms),
            start=2,
        ):
            layer_out = layer(x)
            if layer_number % 2 == 1:
                x = layer_out + norm(x).pow(2)
            else:
                x = layer_out
        return self.final(x)


def project_com(raw_positions, masses):
    com = (masses.view(1, 3, 1) * raw_positions).sum(dim=1) / masses.sum()
    return raw_positions - com.unsqueeze(1)


def componentwise_time_derivatives(projected_positions, u):
    flat = projected_positions.reshape(projected_positions.shape[0], 9)
    velocities = []
    accelerations = []
    for k in range(9):
        velocity_k = torch.autograd.grad(
            flat[:, k].sum(),
            u,
            create_graph=True,
            retain_graph=True,
        )[0]
        acceleration_k = torch.autograd.grad(
            velocity_k.sum(),
            u,
            create_graph=True,
            retain_graph=True,
        )[0]
        velocities.append(velocity_k)
        accelerations.append(acceleration_k)
    return (
        torch.stack(velocities, dim=1).reshape(-1, 3, 3),
        torch.stack(accelerations, dim=1).reshape(-1, 3, 3),
    )


def plummer_acceleration(positions, masses, eps_train=1e-5):
    accel = torch.zeros_like(positions)
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            r_ji = positions[:, j, :] - positions[:, i, :]
            safe_dist = torch.sqrt((r_ji**2).sum(dim=1, keepdim=True) + eps_train**2)
            accel[:, i, :] += masses[j] * r_ji / safe_dist**3
    return accel


def matched_plummer_hamiltonian(positions, velocities, masses, eps_train=1e-5):
    kinetic = 0.5 * (masses.view(1, 3, 1) * velocities**2).sum(dim=(1, 2))
    potential = torch.zeros(positions.shape[0], dtype=positions.dtype)
    for i in range(3):
        for j in range(i + 1, 3):
            r_ij = positions[:, j, :] - positions[:, i, :]
            safe_dist = torch.sqrt((r_ij**2).sum(dim=1) + eps_train**2)
            potential -= masses[i] * masses[j] / safe_dist
    return kinetic + potential, kinetic, potential


def huber(x, delta=1.0):
    abs_x = torch.abs(x)
    return torch.where(abs_x <= delta, 0.5 * x**2, delta * (abs_x - 0.5 * delta))


def test_loss_stability():
    torch.manual_seed(21)
    torch.set_default_dtype(torch.float64)

    model = RepresentativeSQRSiren().to(dtype=torch.float64)
    masses = torch.tensor([1.0, 1.5, 0.75], dtype=torch.float64)
    batch_size = 4

    u = torch.linspace(0.1, 0.9, batch_size, dtype=torch.float64).requires_grad_(True)
    tau = (2.0 * u - 1.0).unsqueeze(1)
    ic13 = torch.rand(batch_size, 13, dtype=torch.float64) * 2.0 - 1.0
    inputs = torch.cat([tau, ic13], dim=1)

    raw_positions = model(inputs).reshape(batch_size, 3, 3)
    positions = project_com(raw_positions, masses)
    velocities, accelerations = componentwise_time_derivatives(positions, u)

    target_positions = torch.zeros_like(positions)
    data_loss = huber(positions - target_positions).mean()
    ic_loss = huber(positions[0]).mean() + huber(velocities[0]).mean()

    residual = accelerations - plummer_acceleration(positions, masses)
    physics_loss = (residual**2).mean()

    hamiltonian, kinetic, potential = matched_plummer_hamiltonian(
        positions,
        velocities,
        masses,
    )
    scale_h = torch.median(kinetic + potential.abs()).detach() + 1e-8
    epsilon_h = 1e-4 * scale_h
    energy_drift = (hamiltonian - hamiltonian[0]) / (hamiltonian[0].abs() + epsilon_h)
    energy_loss = huber(energy_drift).mean()

    angular_momentum = (
        masses.view(1, 3, 1) * torch.cross(positions, velocities, dim=2)
    ).sum(dim=1)
    angular_scale = torch.linalg.norm(angular_momentum[0]).detach() + 1e-8
    angular_loss = huber((angular_momentum - angular_momentum[0]) / angular_scale).mean()

    total_loss = data_loss + ic_loss + physics_loss + energy_loss + angular_loss

    assert torch.isfinite(total_loss), "Loss is NaN or Inf"
    print(
        "Loss Stability Dry Run passed! "
        f"total_loss={total_loss.item():.12e}; "
        f"data={data_loss.item():.3e}; ic={ic_loss.item():.3e}; "
        f"physics={physics_loss.item():.3e}; energy={energy_loss.item():.3e}; "
        f"angular={angular_loss.item():.3e}"
    )

if __name__ == "__main__":
    test_loss_stability()
