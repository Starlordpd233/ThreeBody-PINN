import torch
import torch.nn as nn

class DummyPINN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Linear(14, 9)
    def forward(self, x):
        return self.net(x)

def test_loss_stability():
    model = DummyPINN()
    inputs = torch.rand(10, 14) # 14D input contract
    
    # Forward pass
    preds = model(inputs)
    
    # Physics Loss (dummy)
    loss_phys = torch.mean(preds**2)
    # IC Loss
    loss_ic = torch.mean((preds - 1.0)**2)
    
    total_loss = loss_phys + loss_ic
    
    assert not torch.isnan(total_loss), "Loss is NaN"
    assert not torch.isinf(total_loss), "Loss is Inf"
    print("Loss Stability Dry Run passed! Loss is finite.")

if __name__ == "__main__":
    test_loss_stability()
