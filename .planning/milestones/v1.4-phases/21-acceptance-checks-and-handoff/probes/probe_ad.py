import torch

def test_ad():
    u = torch.tensor(0.3, requires_grad=True, dtype=torch.float64) # Arbitrary u in [0, 1]
    
    # Forward synthetic trajectory
    # r'(u) = [sin(2pi u), cos(2pi u), u^2]
    x = torch.sin(2 * torch.pi * u)
    y = torch.cos(2 * torch.pi * u)
    z = u**2
    r_prime = torch.stack([x, y, z])
    
    # Compute AD derivatives using explicit per-component loop
    derivatives = []
    for k in range(3):
        grad_k = torch.autograd.grad(r_prime[k], u, create_graph=True)[0]
        derivatives.append(grad_k)
    drdu_ad = torch.stack(derivatives)
    
    # Analytical
    drdu_analytical = torch.stack([
        2 * torch.pi * torch.cos(2 * torch.pi * u),
        -2 * torch.pi * torch.sin(2 * torch.pi * u),
        2 * u
    ])
    
    relative_error = torch.norm(drdu_ad - drdu_analytical).item() / torch.norm(drdu_analytical).item()
    assert relative_error < 1e-6, f"AD check failed: {relative_error}"
    print(f"AD check passed! relative_error: {relative_error:.2e}")

if __name__ == "__main__":
    test_ad()
