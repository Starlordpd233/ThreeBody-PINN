import torch

def test_force_energy():
    masses = torch.tensor([1.0, 1.0, 1.0], dtype=torch.float64)
    
    # Random pos and vel
    pos = torch.randn(3, 3, dtype=torch.float64)
    vel = torch.randn(3, 3, dtype=torch.float64)
    
    # Plummer softening
    eps_soft = 0.01
    
    # Compute potential energy U
    U = 0.0
    forces = torch.zeros_like(pos)
    for i in range(3):
        for j in range(i+1, 3):
            r_ij = pos[i] - pos[j]
            dist_sq = torch.sum(r_ij**2)
            soft_dist = torch.sqrt(dist_sq + eps_soft**2)
            
            U -= (masses[i] * masses[j]) / soft_dist
            
            f_mag = (masses[i] * masses[j]) / (soft_dist**3)
            force_ij = f_mag * r_ij
            forces[i] -= force_ij
            forces[j] += force_ij
            
    # Calculate force from U using autograd
    pos_var = pos.clone().detach().requires_grad_(True)
    U_var = 0.0
    for i in range(3):
        for j in range(i+1, 3):
            r_ij = pos_var[i] - pos_var[j]
            dist_sq = torch.sum(r_ij**2)
            soft_dist = torch.sqrt(dist_sq + eps_soft**2)
            U_var -= (masses[i] * masses[j]) / soft_dist
            
    # dU/dx = -F
    dU = torch.autograd.grad(U_var, pos_var)[0]
    expected_forces = -dU
    
    relative_error = torch.norm(expected_forces - forces).item() / torch.norm(forces).item()
    assert relative_error < 1e-5, f"Force-Energy consistency failed: {relative_error}"
    print(f"Force-Energy Consistency check passed! relative_error: {relative_error:.2e}")

if __name__ == "__main__":
    test_force_energy()
