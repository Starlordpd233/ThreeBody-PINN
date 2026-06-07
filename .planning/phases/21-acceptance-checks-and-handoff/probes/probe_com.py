import torch

def test_com():
    # M_i are the actual masses, we use arbitrary positive values
    masses = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float64)
    total_mass = masses.sum()
    
    # Raw network outputs for positions: shape (3, 3) representing 3 bodies in 3D
    raw_pos = torch.randn(3, 3, dtype=torch.float64)
    
    # Projection head logic from pinn_architecture.md
    # x'_i = x_i - sum_j(M_j x_j)/total_mass
    raw_com = (masses.unsqueeze(1) * raw_pos).sum(dim=0) / total_mass
    projected_pos = raw_pos - raw_com
    
    # Check COM invariance of projected pos
    final_com = (masses.unsqueeze(1) * projected_pos).sum(dim=0) / total_mass
    com_magnitude = torch.norm(final_com).item()
    
    assert com_magnitude < 1e-10, f"COM invariance failed: {com_magnitude}"
    print(f"COM Invariance check passed! COM magnitude: {com_magnitude:.2e}")

if __name__ == "__main__":
    test_com()
