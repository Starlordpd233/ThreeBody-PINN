'''
Updated SQR-SkipResNet-SIREN Architecture for N-body PINN
Based on the definitive implementation blueprint

This implementation follows DeepXDE patterns for neural network modules,
with a base NN class that provides transform capabilities and a specialized
SQR-SkipResNet-SIREN architecture for solving the N-body problem.
'''

import torch
import torch.nn as nn
import numpy as np

class SineLayer(nn.Module):
    """
    SIREN layer with sine activation function.
    Implements: φ(x) = sin(ω₀(Wx + b))
    """
    def __init__(self, in_features, out_features, omega_0=30.0, is_first=False):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.omega_0 = omega_0
        self.is_first = is_first
        
        self.linear = nn.Linear(in_features, out_features)
        self.init_weights()
    
    def init_weights(self):
        with torch.no_grad():
            if self.is_first:
                # First layer initialization: U[-1/n_in, 1/n_in]
                bound = 1 / self.in_features
                self.linear.weight.uniform_(-bound, bound)
            else:
                # Hidden layers initialization: U[-√(6/n_in) / ω₀, √(6/n_in) / ω₀]
                bound = np.sqrt(6 / self.in_features) / self.omega_0
                self.linear.weight.uniform_(-bound, bound)
    
    def forward(self, x):
        return torch.sin(self.omega_0 * self.linear(x))


class NN(nn.Module):
    """Base class for all neural network modules, following DeepXDE patterns."""

    def __init__(self):
        super().__init__()
        self.regularizer = None
        self._auxiliary_vars = None
        self._input_transform = None
        self._output_transform = None

    @property
    def auxiliary_vars(self):
        """Tensors: Any additional variables needed."""
        return self._auxiliary_vars

    @auxiliary_vars.setter
    def auxiliary_vars(self, value):
        self._auxiliary_vars = value

    def apply_feature_transform(self, transform):
        """Compute the features by applying a transform to the network inputs, i.e.,
        features = transform(inputs). Then, outputs = network(features).
        """
        self._input_transform = transform

    def apply_output_transform(self, transform):
        """Apply a transform to the network outputs, i.e.,
        outputs = transform(inputs, outputs).
        """
        self._output_transform = transform

    def num_trainable_parameters(self):
        """Evaluate the number of trainable parameters for the NN."""
        return sum(v.numel() for v in self.parameters() if v.requires_grad)


class SQRSkipResNetSIREN(NN):
    """
    SQR-SkipResNet with SIREN layers for N-body PINN.
    
    This is a specialized ResNet variant that combines:
    - SIREN (Sinusoidal Representation Networks) activation functions
    - SQR-SkipResNet architecture with power-enhanced skip connections
    - LayerNorm stabilization for handling chaotic dynamics
    
    Architecture specifications from the document:
    - 12 hidden layers (6 SQR-SkipResNet blocks)
    - 256 neurons per layer
    - Alternating pattern: odd layers have skip connections with power term, even layers are plain
    - Power term p=2 (element-wise square)
    - LayerNorm applied to skip path before power term (critical for stability)
    - SIREN activation throughout with specialized initialization
    """
    def __init__(self, 
                 input_dim=14,  # [t, IC] where IC is 13-dimensional
                 output_dim=9,  # 3D positions for 3 bodies
                 hidden_dim=256,
                 num_layers=12,
                 first_omega_0=30.0,
                 hidden_omega_0=1.0,
                 skip_power=2,
                 regularization=None):
        super().__init__()
        
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.skip_power = skip_power
        self.regularizer = regularization
        
        # Build network layers
        self._build_network(first_omega_0, hidden_omega_0)
        
    def _build_network(self, first_omega_0, hidden_omega_0):
        """Build the network architecture."""
        # First layer with special initialization
        self.first_layer = SineLayer(self.input_dim, self.hidden_dim, 
                                     omega_0=first_omega_0, 
                                     is_first=True)
        
        # Hidden layers following SQR-SkipResNet pattern
        self.hidden_layers = nn.ModuleList()
        for i in range(self.num_layers):
            layer = SineLayer(self.hidden_dim, self.hidden_dim, 
                             omega_0=hidden_omega_0, 
                             is_first=False)
            self.hidden_layers.append(layer)
        
        # LayerNorm for stabilizing skip connections (applied only to odd layers)
        # Critical: elementwise_affine=True, eps=1e-5 as specified
        self.layer_norms = nn.ModuleList()
        for i in range(self.num_layers):
            if (i + 1) % 2 == 1:  # Odd layers (1-indexed)
                layer_norm = nn.LayerNorm(self.hidden_dim, 
                                         elementwise_affine=True, 
                                         eps=1e-5)
                self.layer_norms.append(layer_norm)
            else:
                self.layer_norms.append(None)  # Even layers don't use LayerNorm
        
        # Final linear layer (no activation) for position outputs
        self.final_layer = nn.Linear(self.hidden_dim, self.output_dim)
        
        # Initialize final layer with small weights for stability
        with torch.no_grad():
            self.final_layer.weight.uniform_(-0.01, 0.01)
    
    def forward(self, inputs):
        """
        Forward pass implementing SQR-SkipResNet pattern with LayerNorm stabilization.
        
        Args:
            inputs: Tensor [batch_size, 14] containing [t, IC]
                   where IC = (m1, m2, m3, E, L/L_max, Q, s_min, α, 
                              cos(M_in), sin(M_in), cos(ω_in), sin(ω_in), cos(i_mut))
        
        Returns:
            outputs: Tensor [batch_size, 9] containing [r1, r2, r3] (3D positions of 3 bodies)
        """
        # Apply input transform if specified
        x = inputs
        if self._input_transform is not None:
            x = self._input_transform(x)
        
        # First layer transformation
        x = self.first_layer(x)
        
        # Apply hidden layers with SQR-SkipResNet pattern
        for i, (layer, layer_norm) in enumerate(zip(self.hidden_layers, self.layer_norms)):
            layer_num = i + 1  # 1-indexed for consistency with paper
            
            if layer_num % 2 == 1:  # Odd layers: skip connection with power term
                # Critical: Apply LayerNorm to x before the power term
                # x^(l) = f_sr^(l)(x^(l-1)) + (LayerNorm(x^(l-1)))^p
                identity = layer_norm(x) ** self.skip_power  # LayerNorm then power
                x = layer(x) + identity
            else:  # Even layers: plain transformation
                # x^(l) = f_pn^(l)(x^(l-1))
                x = layer(x)
        
        # Final linear layer to get position outputs
        outputs = self.final_layer(x)
        
        # Apply output transform if specified
        if self._output_transform is not None:
            outputs = self._output_transform(inputs, outputs)
            
        return outputs

    def compute_derivatives(self, inputs):
        """
        Compute positions and their time derivatives (velocity, acceleration).
        
        This is a convenience method for physics-informed neural networks where
        we need to compute derivatives with respect to time for the physics loss.
        
        Args:
            inputs: Tensor [batch_size, 14] containing [t, IC]
        
        Returns:
            positions: Tensor [batch_size, 9] - predicted positions
            velocities: Tensor [batch_size, 9] - first time derivative
            accelerations: Tensor [batch_size, 9] - second time derivative
        """
        # Split time and initial conditions
        t = inputs[:, 0:1].requires_grad_(True)
        ic = inputs[:, 1:]
        
        # Reconstruct input with tracked time
        tracked_input = torch.cat([t, ic], dim=1)
        
        # Forward pass
        positions = self.forward(tracked_input)
        
        # Compute velocity: v = dr/dt
        velocities = torch.autograd.grad(
            positions, t,
            grad_outputs=torch.ones_like(positions),
            create_graph=True,
            retain_graph=True
        )[0]
        
        # Compute acceleration: a = d²r/dt²
        accelerations = torch.autograd.grad(
            velocities, t,
            grad_outputs=torch.ones_like(velocities),
            create_graph=True,
            retain_graph=True
        )[0]
        
        return positions, velocities, accelerations


# Example usage and verification
if __name__ == "__main__":
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Create model with exact specifications from the document
    model = SQRSkipResNetSIREN(
        input_dim=14,
        output_dim=9,
        hidden_dim=256,
        num_layers=12,
        first_omega_0=30.0,
        hidden_omega_0=1.0,
        skip_power=2,
        regularization=None
    ).to(device)
    
    # Print model architecture summary
    print("SQR-SkipResNet-SIREN Architecture:")
    print(f"Input dimension: {model.input_dim}")
    print(f"Output dimension: {model.output_dim}")
    print(f"Hidden dimension: {model.hidden_dim}")
    print(f"Number of hidden layers: {model.num_layers}")
    print(f"Skip power term: {model.skip_power}")
    print(f"Total parameters: {model.num_trainable_parameters()}")
    
    # Test forward pass
    batch_size = 32
    
    # Create test inputs with proper structure
    t = torch.rand(batch_size, 1, device=device, requires_grad=True)
    # Initial conditions: masses, physical invariants, orientation angles
    ic = torch.rand(batch_size, 13, device=device)
    
    # Test basic forward pass
    input_vector = torch.cat([t, ic], dim=1)
    positions = model(input_vector)
    print(f"\nForward pass successful!")
    print(f"Input shape: {input_vector.shape}")
    print(f"Output shape: {positions.shape}")
    
    # Test automatic differentiation for physics using the convenience method
    print("\nTesting automatic differentiation with compute_derivatives method...")
    r, v, a = model.compute_derivatives(input_vector)
    print(f"Positions shape: {r.shape}")
    print(f"Velocities shape: {v.shape}")
    print(f"Accelerations shape: {a.shape}")
    
    # Example of using DeepXDE-style transforms
    print("\nTesting DeepXDE-style transforms...")
    
    # Example input transform (e.g., normalization)
    def example_input_transform(x):
        # Normalize time to [-1, 1]
        x_transformed = x.clone()
        x_transformed[:, 0] = 2 * x_transformed[:, 0] - 1
        return x_transformed
    
    # Example output transform (e.g., enforcing initial conditions)
    def example_output_transform(inputs, outputs):
        # This is just an example - actual transform would enforce IC
        return outputs
    
    model.apply_feature_transform(example_input_transform)
    model.apply_output_transform(example_output_transform)
    
    # Test with transforms
    positions_transformed = model(input_vector)
    print(f"Output with transforms shape: {positions_transformed.shape}")
    
    print("\nModel architecture is ready for PINN training!")