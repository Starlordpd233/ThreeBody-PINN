'''
to navigate to the brutus folder to generate data, run the following command in terminal 
(cursor's integrated terminal or Mac's terminal):
cd ~/Desktop/cursor/brutus_Newton-main


Command for running simulation:
(after testing these are the parameters that worked)

for hierarchical:
./brutus 1e-15 130 0 10 0.15 3 <home>/Desktop/cursor/simulation_data/Data/testing_data/single_ic.txt > <home>/Desktop/cursor/simulation_data/Data/testing_data/test_output.txt

for quasi-random:
./brutus 1e-14 122 0 10 0.18 3 <home>/Desktop/cursor/simulation_data/Data/testing_data/single_ic.txt > <home>/Desktop/cursor/simulation_data/Data/testing_data/test_output.txt


./brutus 1e-11 84  0   10   0.01    3   my_IC.txt  > output.txt
         │      │  │    │     │     │       └─────── input snapshot
         │      │  │    │     │     └────────────── Number of bodies
         │      │  │    │     └──────────────────── Bulirsch-Stoer time-step (dt)
         │      │  │    └────────────────────────── end time
         │      │  └─────────────────────────────── start time
         │      └──────────────────────────────────── working precision (digits)
         └──────────────────────────────────────── tolerance ε

type the absolute path for my_IC.txt and output.txt in the terminal (copy them from cursor's tab)

input ic.txt has the following format:

mass1 x1 y1 z1 vx1 vy1 vz1
mass2 x2 y2 z2 vx2 vy2 vz2
mass3 x3 y3 z3 vx3 vy3 vz3

'''

'''
Enhanced Three-Body Initial Condition Generator
Based on Stage 1: Enhanced Quasi-Random Sampling from the unified pipeline

Key improvements:
1. Non-zero initial velocities using Sobol sampling
2. Hierarchical system generation for stable configurations  
3. Epsilon set to 0.05 based on PDF recommendation
4. 6D Sobol sequence for position + velocity sampling
5. Proper mapping of Sobol numbers to physical coordinates
'''

import numpy as np
from scipy.stats import qmc, norm
from typing import Tuple, Optional, Union, Dict
import warnings
import os

class EnhancedThreeBodySampler:
    """
    Enhanced quasi-random sampler for three-body initial conditions.
    Implements Stage 1 from the unified pipeline with velocity sampling.
    """
    
    def __init__(self, epsilon: float = 0.05, scale_range: Tuple[float, float] = (1.0, 1.0),
                 velocity_scale: float = 0.1, rotate: bool = False, 
                 dtype: np.dtype = np.float64, seed: Optional[int] = None):
        """
        Initialize the enhanced sampler.
        
        Parameters:
        -----------
        epsilon : float
            Minimum allowed distance between particles (default: 0.05 per PDF)
        scale_range : tuple of (float, float)
            Range for optional global scaling (min, max)
        velocity_scale : float
            Standard deviation for velocity component sampling
        rotate : bool
            Whether to apply random rotation (future feature)
        dtype : numpy dtype
            Data type for output arrays
        seed : int, optional
            Random seed for Sobol scrambling
        """
        self.epsilon = epsilon
        self.scale_range = scale_range
        self.velocity_scale = velocity_scale
        self.rotate = rotate
        self.dtype = dtype
        
        # Determine Sobol dimension based on features
        # 3 for position + 3 for velocity + 1 for scaling = 7 dimensions
        self.use_scaling = (scale_range[0] != scale_range[1])
        self.use_velocity = (velocity_scale > 0)
        
        # Base: 3D for position sampling
        self.sobol_dim = 3
        if self.use_scaling:
            self.sobol_dim += 1
        if self.use_velocity:
            self.sobol_dim += 3  # Add 3D for velocity sampling
        if self.rotate:
            self.sobol_dim += 3  # Future: add rotation angles
            
        # Initialize Sobol generator with scrambling (recommended in PDF)
        self.sobol = qmc.Sobol(d=self.sobol_dim, scramble=True, seed=seed)
        self.sobol_index = 0
        self.first_batch = True
        
    def _map_sobol_to_velocity(self, u_vel: np.ndarray) -> np.ndarray:
        """
        Map Sobol coordinates to velocity using inverse transform sampling.
        Uses quantile function of normal distribution as per PDF recommendation.
        """
        # Convert uniform [0,1] to standard normal using inverse CDF
        vel_components = norm.ppf(u_vel, loc=0, scale=self.velocity_scale)
        return vel_components
        
    def _process_sobol_batch(self, sobol_batch: np.ndarray, p1: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Process a batch of Sobol points into particle positions and velocities."""
        batch_size = len(sobol_batch)
        
        # Extract Sobol coordinates
        idx = 0
        u1, u2, u3 = sobol_batch[:, idx], sobol_batch[:, idx+1], sobol_batch[:, idx+2]
        idx += 3
        
        # === Position Sampling (following PDF exactly) ===
        # Direction on unit sphere
        cos_theta = 1 - 2 * u1  # Ensures uniform distribution by solid angle
        sin_theta = np.sqrt(1 - cos_theta**2)
        phi = 2 * np.pi * u2
        
        # Enforce x ≤ 0 constraint by mirroring
        needs_mirror = np.cos(phi) > 0
        phi[needs_mirror] = (phi[needs_mirror] + np.pi) % (2 * np.pi)
        
        # Direction vectors
        d = np.stack([
            sin_theta * np.cos(phi),
            sin_theta * np.sin(phi),
            cos_theta
        ], axis=-1)
        
        # Radial distances (cube root for volume uniformity)
        r = u3**(1/3)
        
        # Positions of particle 2
        p2_batch = r[:, np.newaxis] * d
        
        # Apply scaling if enabled
        if self.use_scaling:
            u_scale = sobol_batch[:, idx]
            idx += 1
            scale = self.scale_range[0] + (self.scale_range[1] - self.scale_range[0]) * u_scale
            p1_scaled = p1[np.newaxis, :] * scale[:, np.newaxis]
            p2_batch = p2_batch * scale[:, np.newaxis]
        else:
            p1_scaled = np.tile(p1, (batch_size, 1))
            scale = np.ones(batch_size)
        
        # Positions of particle 3 (center of mass constraint)
        p3_batch = -(p1_scaled + p2_batch)
        
        # === Velocity Sampling (new feature from PDF) ===
        if self.use_velocity:
            # Sample velocity for particle 2 using 3 Sobol dimensions
            u_vel = sobol_batch[:, idx:idx+3]
            v2_batch = self._map_sobol_to_velocity(u_vel)
            
            # For equal masses, maintain zero total momentum
            # v1 + v2 + v3 = 0, so we can set v1 = -v2/2, v3 = -v2/2
            # This maintains symmetry while ensuring momentum conservation
            v1_batch = -v2_batch / 2
            v3_batch = -v2_batch / 2
            
            # Scale velocities with position scaling to maintain consistent dynamics
            v1_batch = v1_batch * scale[:, np.newaxis]
            v2_batch = v2_batch * scale[:, np.newaxis]
            v3_batch = v3_batch * scale[:, np.newaxis]
        else:
            # Zero velocities
            v1_batch = np.zeros((batch_size, 3))
            v2_batch = np.zeros((batch_size, 3))
            v3_batch = np.zeros((batch_size, 3))
        
        return p1_scaled, p2_batch, p3_batch, v1_batch, v2_batch, v3_batch, sobol_batch
        
    def generate_batch(self, n_samples: int, max_rejection_factor: int = 100) -> Tuple[np.ndarray, np.ndarray, int]:
        """
        Generate a batch of initial conditions using enhanced Sobol sampling.
        
        Returns:
        --------
        positions : ndarray of shape (n_valid, 3, 3)
            Particle positions
        velocities : ndarray of shape (n_valid, 3, 3)
            Particle velocities
        final_sobol_index : int
            Last Sobol index used
        """
        # Fix particle 1
        p1 = np.array([1.0, 0.0, 0.0], dtype=self.dtype)
        
        valid_positions = []
        valid_velocities = []
        total_attempts = 0
        
        # For the first batch, use random_base2 for optimal properties
        if self.first_batch and n_samples >= 16:
            m = int(np.ceil(np.log2(n_samples * 1.5)))
            m = min(m, 20)
            
            try:
                sobol_batch = self.sobol.random_base2(m)
                self.first_batch = False
                
                # Process the batch
                p1_scaled, p2_batch, p3_batch, v1_batch, v2_batch, v3_batch, _ = self._process_sobol_batch(sobol_batch, p1)
                
                # Vectorized collision checking
                d12 = np.linalg.norm(p1_scaled - p2_batch, axis=1)
                d13 = np.linalg.norm(p1_scaled - p3_batch, axis=1)
                d23 = np.linalg.norm(p2_batch - p3_batch, axis=1)
                
                # Valid configurations
                valid_mask = (d12 > self.epsilon) & (d13 > self.epsilon) & (d23 > self.epsilon)
                valid_indices = np.where(valid_mask)[0]
                
                # Collect valid configurations
                for idx in valid_indices[:n_samples]:
                    positions = np.stack([p1_scaled[idx], p2_batch[idx], p3_batch[idx]])
                    velocities = np.stack([v1_batch[idx], v2_batch[idx], v3_batch[idx]])
                    valid_positions.append(positions)
                    valid_velocities.append(velocities)
                
                self.sobol_index += len(sobol_batch)
                total_attempts += len(sobol_batch)
                
            except Exception as e:
                warnings.warn(f"random_base2 failed: {e}. Falling back to random().")
                self.first_batch = False
        
        # Continue with regular random() for remaining samples
        while len(valid_positions) < n_samples:
            needed = n_samples - len(valid_positions)
            batch_size = min(max(needed * 2, 100), 10000)
            
            if total_attempts + batch_size > n_samples * max_rejection_factor:
                raise RuntimeError(f"Epsilon {self.epsilon} too large: exceeded {max_rejection_factor}x "
                                 f"rejection limit. Generated only {len(valid_positions)}/{n_samples} samples.")
            
            sobol_batch = self.sobol.random(batch_size)
            total_attempts += batch_size
            
            # Process the batch
            p1_scaled, p2_batch, p3_batch, v1_batch, v2_batch, v3_batch, _ = self._process_sobol_batch(sobol_batch, p1)
            
            # Vectorized collision checking
            d12 = np.linalg.norm(p1_scaled - p2_batch, axis=1)
            d13 = np.linalg.norm(p1_scaled - p3_batch, axis=1)
            d23 = np.linalg.norm(p2_batch - p3_batch, axis=1)
            
            # Valid configurations
            valid_mask = (d12 > self.epsilon) & (d13 > self.epsilon) & (d23 > self.epsilon)
            valid_indices = np.where(valid_mask)[0]
            
            # Collect valid configurations
            for idx in valid_indices:
                if len(valid_positions) < n_samples:
                    positions = np.stack([p1_scaled[idx], p2_batch[idx], p3_batch[idx]])
                    velocities = np.stack([v1_batch[idx], v2_batch[idx], v3_batch[idx]])
                    valid_positions.append(positions)
                    valid_velocities.append(velocities)
            
            self.sobol_index += batch_size
        
        # Convert to arrays
        positions_array = np.array(valid_positions[:n_samples], dtype=self.dtype)
        velocities_array = np.array(valid_velocities[:n_samples], dtype=self.dtype)
        
        return positions_array, velocities_array, self.sobol_index
    
    def save_brutus_format_single(self, position: np.ndarray, velocity: np.ndarray, 
                                  filename: str, mass: float = 1.0):
        """Save a single initial condition in BRUTUS format."""
        with open(filename, 'w') as f:
            for particle_idx in range(3):
                x, y, z = position[particle_idx]
                vx, vy, vz = velocity[particle_idx]
                f.write(f'{mass} {x} {y} {z} {vx} {vy} {vz}\n')


def generate_stable_hierarchical_systems(n_systems: int = 1000, output_dir: str = "simulation_data/Data/ic_raw/ic_hierarchical",
                                       mass_range: Tuple[float, float] = (0.5, 1.5),
                                       save_files: bool = True) -> np.ndarray:
    """
    Generate hierarchical triple systems that are more likely to be stable.
    Based on the prescreening script's hierarchical generation.
    
    Parameters:
    -----------
    n_systems : int
        Number of systems to generate
    output_dir : str
        Directory to save the IC files
    mass_range : tuple
        Range for mass ratios (min, max)
    save_files : bool
        Whether to save individual files
        
    Returns:
    --------
    ics : ndarray
        Array of initial conditions
    """
    print(f"\nGenerating {n_systems} hierarchical systems...")
    
    if save_files:
        os.makedirs(output_dir, exist_ok=True)
    
    ics = []
    saved_count = 0
    
    # Find the last file number
    start_number = 0
    try:
        all_files = os.listdir(output_dir)
        matching_files = [f for f in all_files if f.startswith('ic_hierarchical_') and f.endswith('.txt')]
        
        if matching_files:
            numbers = []
            for filename in matching_files:
                try:
                    number_part = filename[len('ic_hierarchical_'):-4]
                    number = int(number_part)
                    numbers.append(number)
                except ValueError:
                    continue
            
            if numbers:
                start_number = max(numbers) + 1
                print(f"Found {len(numbers)} existing files. Starting from {start_number:04d}")
                
    except Exception as e:
        print(f"Error reading directory: {e}. Starting from 0000.")
    
    for i in range(n_systems):
        # Mass ratios for hierarchical stability
        q_inner = np.random.uniform(0.1, 1.0)  # m2/m1
        q_outer = np.random.uniform(0.1, 2.0)  # m3/(m1+m2)
        
        # Masses (normalized so total mass ~ 3)
        m1 = np.random.uniform(*mass_range)
        m2 = q_inner * m1
        m3 = q_outer * (m1 + m2)
        total_mass = m1 + m2 + m3
        m1 /= total_mass/3
        m2 /= total_mass/3
        m3 /= total_mass/3
        
        # Hierarchical separation ratio
        # Kozai-Lidov stability requires a_out/a_in > 2.8 * ((1+q_outer)/(1+e_outer))^(2/5)
        min_ratio = 2.8 * ((1 + q_outer) / 0.5) ** 0.4  # Assume max e_outer = 0.5
        hierarchy_ratio = np.random.uniform(max(3, min_ratio), 10)
        
        # Semi-major axes
        a_inner = np.random.uniform(0.1, 0.3)
        a_outer = hierarchy_ratio * a_inner
        
        # Eccentricities (keep moderate for stability)
        e_inner = np.random.uniform(0, 0.3)
        e_outer = np.random.uniform(0, 0.3)
        
        # Initial phases
        M_inner = np.random.uniform(0, 2*np.pi)  # Mean anomaly
        M_outer = np.random.uniform(0, 2*np.pi)
        
        # Convert to Cartesian (using circular approximation for simplicity)
        # Inner binary
        r_inner = a_inner * (1 - e_inner * np.cos(M_inner))
        v_inner = np.sqrt((m1 + m2) / r_inner)
        
        # Add small inclination for variety
        inc_inner = np.random.uniform(0, 0.1)  # Small inclination
        
        # Positions relative to inner binary COM
        x1 = np.array([-m2/(m1+m2) * r_inner * np.cos(inc_inner), 0, 
                       -m2/(m1+m2) * r_inner * np.sin(inc_inner)])
        x2 = np.array([m1/(m1+m2) * r_inner * np.cos(inc_inner), 0,
                       m1/(m1+m2) * r_inner * np.sin(inc_inner)])
        v1 = np.array([0, -m2/(m1+m2) * v_inner, 0])
        v2 = np.array([0, m1/(m1+m2) * v_inner, 0])
        
        # Outer body
        m_inner = m1 + m2
        r_outer = a_outer * (1 - e_outer * np.cos(M_outer))
        v_outer = np.sqrt((m_inner + m3) / r_outer)
        
        # Position of inner binary COM
        x_inner_com = np.array([-m3/(m_inner+m3) * r_outer, 0, 0])
        v_inner_com = np.array([0, -m3/(m_inner+m3) * v_outer, 0])
        
        # Outer body position
        x3 = np.array([m_inner/(m_inner+m3) * r_outer, 0, 0])
        v3 = np.array([0, m_inner/(m_inner+m3) * v_outer, 0])
        
        # Transform to global frame
        x1 += x_inner_com
        x2 += x_inner_com
        v1 += v_inner_com
        v2 += v_inner_com
        
        # Verify and adjust COM
        com_pos = (m1*x1 + m2*x2 + m3*x3) / (m1+m2+m3)
        com_vel = (m1*v1 + m2*v2 + m3*v3) / (m1+m2+m3)
        
        x1 -= com_pos; x2 -= com_pos; x3 -= com_pos
        v1 -= com_vel; v2 -= com_vel; v3 -= com_vel
        
        # Add small random perturbation for variety
        perturbation = 0.01
        for vec in [x1, x2, x3, v1, v2, v3]:
            vec += np.random.normal(0, perturbation, 3)
        
        # Save to file if requested
        if save_files:
            file_number = start_number + i
            filename = os.path.join(output_dir, f'ic_hierarchical_{file_number:04d}.txt')
            with open(filename, 'w') as f:
                f.write(f'{m1} {x1[0]} {x1[1]} {x1[2]} {v1[0]} {v1[1]} {v1[2]}\n')
                f.write(f'{m2} {x2[0]} {x2[1]} {x2[2]} {v2[0]} {v2[1]} {v2[2]}\n')
                f.write(f'{m3} {x3[0]} {x3[1]} {x3[2]} {v3[0]} {v3[1]} {v3[2]}\n')
            saved_count += 1
        
        # Store in array format
        ic = np.concatenate([
            [m1], x1, v1,
            [m2], x2, v2,
            [m3], x3, v3
        ])
        ics.append(ic)
    
    if save_files:
        print(f"✓ Generated {saved_count} hierarchical systems in {output_dir}/")
    
    return np.array(ics)


def compute_system_invariants(positions: np.ndarray, velocities: np.ndarray, masses: np.ndarray) -> Dict[str, float]:
    """
    Compute physical invariants for stratification (Stage 1 enhancement).
    
    Parameters:
    -----------
    positions : ndarray of shape (3, 3)
        Particle positions
    velocities : ndarray of shape (3, 3)
        Particle velocities  
    masses : ndarray of shape (3,)
        Particle masses
        
    Returns:
    --------
    invariants : dict
        Dictionary containing computed invariants
    """
    # Kinetic energy
    ke = 0.5 * np.sum(masses[:, np.newaxis] * velocities**2)
    
    # Potential energy
    pe = 0.0
    min_sep = np.inf
    r12 = np.linalg.norm(positions[0] - positions[1])
    r13 = np.linalg.norm(positions[0] - positions[2])
    r23 = np.linalg.norm(positions[1] - positions[2])
    
    pe -= masses[0] * masses[1] / r12
    pe -= masses[0] * masses[2] / r13
    pe -= masses[1] * masses[2] / r23
    
    min_sep = min(r12, r13, r23)
    
    # Total energy
    total_energy = ke + pe
    
    # Angular momentum
    L_total = np.zeros(3)
    for i in range(3):
        L_total += masses[i] * np.cross(positions[i], velocities[i])
    L_mag = np.linalg.norm(L_total)
    
    # Virial ratio
    virial = 2 * ke / abs(pe) if pe != 0 else np.inf
    
    # Shape metric (optional)
    alpha = r12 / (r13 + r23)
    
    return {
        'energy': total_energy,
        'kinetic_energy': ke,
        'potential_energy': pe,
        'angular_momentum': L_mag,
        'virial_ratio': virial,
        'min_separation': min_sep,
        'shape_metric': alpha
    }


# Enhanced functional interface
def generate_enhanced_three_body_ics(
    n_samples: int,
    epsilon: float = 0.05,
    scale_range: Tuple[float, float] = (1.0, 1.0),
    velocity_scale: float = 0.1,
    rotate: bool = False,
    dtype: np.dtype = np.float64,
    seed: Optional[int] = None,
    save_directory: Optional[str] = None,
    mass: float = 1.0,
    compute_invariants: bool = False
) -> Tuple[np.ndarray, np.ndarray, int, Optional[list]]:
    """
    Enhanced functional interface with velocity sampling and invariant computation.
    """
    sampler = EnhancedThreeBodySampler(epsilon, scale_range, velocity_scale, rotate, dtype, seed)
    
    positions, velocities, final_index = sampler.generate_batch(n_samples)
    
    invariants_list = []
    
    # Save individual files and compute invariants if requested
    if save_directory:
        os.makedirs(save_directory, exist_ok=True)
        
    for i in range(n_samples):
        if save_directory:
            filename = os.path.join(save_directory, f'ic_hierarchical{i:04d}.txt')
            sampler.save_brutus_format_single(positions[i], velocities[i], filename, mass)
        
        if compute_invariants:
            masses = np.array([mass, mass, mass])
            invariants = compute_system_invariants(positions[i], velocities[i], masses)
            invariants['index'] = i
            invariants_list.append(invariants)
    
    return positions, velocities, final_index, invariants_list if compute_invariants else None


def test_enhanced_sampling():
    """Test the enhanced sampling with velocities."""
    print("Testing enhanced three-body sampling...")
    
    # Test with velocities
    sampler = EnhancedThreeBodySampler(epsilon=0.05, velocity_scale=0.1, seed=42)
    pos, vel, idx = sampler.generate_batch(10)
    
    # Check shapes
    assert pos.shape == (10, 3, 3), f"Wrong position shape: {pos.shape}"
    assert vel.shape == (10, 3, 3), f"Wrong velocity shape: {vel.shape}"
    
    # Check COM constraints
    com_pos = pos.mean(axis=1)
    com_vel = vel.mean(axis=1)  # For equal masses
    assert np.allclose(com_pos, 0, atol=1e-12), f"Position COM not at origin"
    assert np.allclose(com_vel, 0, atol=1e-12), f"Velocity COM not zero"
    
    # Check velocities are non-zero
    assert not np.allclose(vel, 0), "Velocities should be non-zero"
    
    # Check minimum separations
    for i in range(len(pos)):
        d12 = np.linalg.norm(pos[i, 0] - pos[i, 1])
        d13 = np.linalg.norm(pos[i, 0] - pos[i, 2])
        d23 = np.linalg.norm(pos[i, 1] - pos[i, 2])
        assert min(d12, d13, d23) > 0.05, f"Separation violates epsilon=0.05"
    
    print("✓ Enhanced sampling tests passed!")


def continuation_enhanced_ic_generation(
    n_samples: int,
    ic_type: str = "standard",  # "standard" or "hierarchical"
    start_from_last: bool = True,
    base_filename: str = "ic_",
    directory: str = None,
    epsilon: float = 0.05,
    scale_range: Tuple[float, float] = (1.0, 1.0),
    velocity_scale: float = 0.1,
    seed: Optional[int] = None,
    mass: float = 1.0
) -> None:
    """
    Generate enhanced initial conditions with continuous file numbering.
    Supports both standard and hierarchical ICs.
    """
    # Set directory based on IC type
    if directory is None:
        if ic_type == "hierarchical":
            directory = "<home>/Desktop/cursor/simulation_data/Data/ic_raw/ic_hierarchical"
            base_filename = "ic_hierarchical_"
        else:
            directory = "<home>/Desktop/cursor/simulation_data/Data/ic_raw/ic_standard_quasi_random"
            base_filename = "ic_standard_"
    
    os.makedirs(directory, exist_ok=True)
    
    # Find the last file number
    start_number = 0
    if start_from_last:
        try:
            all_files = os.listdir(directory)
            matching_files = [f for f in all_files if f.startswith(base_filename) and f.endswith('.txt')]
            
            if matching_files:
                numbers = []
                for filename in matching_files:
                    try:
                        number_part = filename[len(base_filename):-4]
                        number = int(number_part)
                        numbers.append(number)
                    except ValueError:
                        continue
                
                if numbers:
                    start_number = max(numbers) + 1
                    print(f"Found {len(numbers)} existing files. Starting from {start_number:04d}")
                    
        except Exception as e:
            print(f"Error reading directory: {e}. Starting from 0000.")
    
    print(f"\nGenerating {n_samples} {ic_type} ICs starting from {base_filename}{start_number:04d}.txt")
    
    if ic_type == "hierarchical":
        # Generate hierarchical systems
        generate_stable_hierarchical_systems(
            n_systems=n_samples,
            output_dir=directory,
            save_files=True
        )
    else:
        # Generate standard enhanced ICs
        sampler = EnhancedThreeBodySampler(epsilon, scale_range, velocity_scale, dtype=np.float64, seed=seed)
        
        for i in range(n_samples):
            file_number = start_number + i
            filename = os.path.join(directory, f"{base_filename}{file_number:04d}.txt")
            
            # Generate one configuration
            positions, velocities, _ = sampler.generate_batch(1)
            
            # Save with velocities
            sampler.save_brutus_format_single(positions[0], velocities[0], filename, mass)
    
    print(f"✓ Completed generating {n_samples} {ic_type} ICs")


if __name__ == "__main__":
    # Run tests
    test_enhanced_sampling()
    
    # ========== GENERATE STANDARD ENHANCED ICs ==========
    print("\n" + "="*60)
    print("Generating enhanced standard initial conditions...")
    print("="*60)
    
    continuation_enhanced_ic_generation(
        n_samples=100,
        ic_type="standard",
        start_from_last=True,
        epsilon=0.05,  # As recommended in PDF
        velocity_scale=0.1,  # Non-zero velocities
        scale_range=(0.8, 1.2),  # Some variety in scale
        seed=42,
        mass=1.0
    )
    
    # ========== GENERATE HIERARCHICAL ICs ==========
    print("\n" + "="*60)
    print("Generating hierarchical initial conditions...")
    print("="*60)
    
    continuation_enhanced_ic_generation(
        n_samples=100,
        ic_type="hierarchical",
        start_from_last=True,  # Start fresh for hierarchical
        seed=43,
        mass=1.0
    )
    
    print("\n✓ All generation completed!")
    
    # ========== STRATIFICATION CODE (COMMENTED AS REQUESTED) ==========
    """
    # This would be Stage 1 stratification, but keeping it commented as requested
    
    def stratify_initial_conditions(ic_directory: str, output_base_dir: str):
        '''Stratify ICs based on physical invariants as described in Stage 1 PDF.'''
        
        # Define bins based on Table 1 from PDF
        energy_bins = [
            (-np.inf, -0.5, "strongly_bound"),
            (-0.5, -0.1, "moderately_bound"),
            (-0.1, 0, "weakly_bound"),
            (0, np.inf, "unbound")
        ]
        
        angular_momentum_bins = [
            (0, 0.1, "low_spin"),
            (0.1, 0.5, "intermediate"),
            (0.5, np.inf, "high_spin")
        ]
        
        virial_bins = [
            (0, 0.7, "sub_virial"),
            (0.7, 1.5, "near_virial"),
            (1.5, np.inf, "super_virial")
        ]
        
        # Load and compute invariants for all ICs
        # Then sort into appropriate bins...
        pass
    """