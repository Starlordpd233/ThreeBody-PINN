import numpy as np

def test_scaling_consistency():
    G = 1.0 # usually G=1 in this non-dimensional system
    T = 1.0 # say T=1 for max time
    D = (G * T**2)**(1/3)
    
    expected_D = 1.0
    relative_error = abs(D - expected_D)
    assert relative_error < 1e-10, f"Scaling relative error too high: {relative_error}"
    print(f"Scaling Consistency Pass: relative_error = {relative_error:.2e}")

if __name__ == "__main__":
    test_scaling_consistency()
