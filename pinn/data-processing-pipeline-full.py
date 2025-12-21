"""
CTL-PINN Data Processing Pipeline
=================================
Modular pipeline for processing three-body simulation data for the CTL-PINN framework.

Structure:
1. core/data_structures.py - Core data structures
2. core/parsing.py - File parsing utilities
3. core/scaling.py - Scaling and normalization
4. processing/invariants.py - Physical invariants computation
5. processing/stage_assignment.py - Curriculum stage assignment
6. processing/input_vector.py - PINN input vector formulation
7. scripts/preprocess_dataset.py - Main preprocessing script
8. scripts/prepare_training_data.py - Final training data preparation
"""

# ============================================================================
# FILE: core/data_structures.py
# ============================================================================
"""Core data structures for the CTL-PINN pipeline"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Tuple
import numpy as np
from pathlib import Path


@dataclass
class SimulationMetadata:
    """Metadata for a simulation"""
    trajectory_id: str
    ic_file: Path
    brutus_file: Path
    dataset_type: str  # 'hierarchical' or 'quasi-random'
    fidelity: str  # 'low' or 'high'
    dt_out: float  # 0.01, 0.08, or 0.17
    set_name: str  # '1a', '1b', '2a', '2b'
    
    @property
    def is_hierarchical(self) -> bool:
        return self.dataset_type == 'hierarchical'
    
    @property
    def is_high_fidelity(self) -> bool:
        return self.fidelity == 'high'


@dataclass
class RawTrajectoryData:
    """Raw parsed data from IC and BRUTUS files"""
    metadata: SimulationMetadata
    
    # From IC file (raw, unscaled)
    masses: np.ndarray  # (3,)
    r_initial: np.ndarray  # (3, 3)
    v_initial: np.ndarray  # (3, 3)
    
    # From BRUTUS file
    times: np.ndarray  # (T,)
    positions: np.ndarray  # (T, 3, 3)
    velocities: np.ndarray  # (T, 3, 3)
    
    # Additional BRUTUS metadata
    cpu_times: Optional[np.ndarray] = None  # (T,)
    energy_initial: Optional[float] = None
    energy_final: Optional[float] = None
    energy_error: Optional[float] = None


@dataclass
class ScaledTrajectoryData:
    """Scaled trajectory data with dimensionless units"""
    metadata: SimulationMetadata
    raw_data: RawTrajectoryData
    
    # Scaled quantities
    masses: np.ndarray  # (3,) - masses don't scale
    r_prime: np.ndarray  # (3, 3) - scaled initial positions
    v_prime: np.ndarray  # (3, 3) - scaled initial velocities
    
    # Scaled time series
    times: np.ndarray  # (T,) - same as raw
    positions_scaled: np.ndarray  # (T, 3, 3)
    velocities_scaled: np.ndarray  # (T, 3, 3)
    
    # Scaling factors used
    length_scale: float
    velocity_scale: float
    time_scale: float


@dataclass
class PhysicalInvariants:
    """Computed physical invariants for stage assignment"""
    E: float  # Total energy
    Q: float  # Virial ratio  
    s_min: float  # Minimum initial separation
    L_norm: float  # Normalized angular momentum
    I_norm: float  # Normalized moment of inertia
    tau_L: float  # Lyapunov time
    
    # Additional quantities for reference
    L_max: float
    r_char: float
    v_char: float


@dataclass
class ProcessedTrajectory:
    """Fully processed trajectory with all computed quantities"""
    metadata: SimulationMetadata
    scaled_data: ScaledTrajectoryData
    invariants: PhysicalInvariants
    stage: Optional[int] = None
    
    # 13-component IC vector (without time)
    ic_vector: Optional[np.ndarray] = None
    
    # Additional computed quantities
    canonical_ordering: Optional[np.ndarray] = None  # Permutation indices


@dataclass
class GlobalScales:
    """Global normalization scales computed across dataset"""
    T_max: float = 10.0  # Maximum simulation time
    G: float = 1.0  # Gravitational constant
    
    # Derived scales
    D: float = field(init=False)  # Length scale
    V: float = field(init=False)  # Velocity scale
    
    # Dataset-wide scales
    E_scale: Optional[float] = None
    smin_scale: Optional[float] = None
    Q_scale: float = 0.5  # Fixed
    
    # Dataset statistics (optional)
    dataset_stats: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self.D = np.cbrt(self.G * self.T_max**2)
        self.V = self.D / self.T_max


# ============================================================================
# FILE: core/parsing.py
# ============================================================================
"""File parsing utilities for IC and BRUTUS files"""

import numpy as np
from pathlib import Path
from typing import Tuple, Optional
import re
from core.data_structures import RawTrajectoryData, SimulationMetadata


def detect_simulation_metadata(ic_path: Path, brutus_path: Path) -> SimulationMetadata:
    """
    Detect simulation metadata from file paths and names.
    
    Expected patterns:
    - ic_hierarchical_XXXX.txt or ic_quasirandom_XXXX.txt
    - brutus_hierarchical_XXXX.txt or brutus_quasirandom_XXXX.txt
    """
    ic_name = ic_path.stem
    brutus_name = brutus_path.stem
    
    # Extract dataset type
    if 'hierarchical' in ic_name:
        dataset_type = 'hierarchical'
    elif 'quasirandom' in ic_name or 'quasi-random' in ic_name:
        dataset_type = 'quasi-random'
    else:
        raise ValueError(f"Cannot determine dataset type from {ic_name}")
    
    # Extract trajectory ID
    match = re.search(r'(\d+)', ic_name)
    if match:
        traj_id = match.group(1)
    else:
        traj_id = ic_name.split('_')[-1]
    
    # Determine fidelity and dt_out from brutus file
    # This is a heuristic - you may need to adjust based on your naming convention
    # or pass this information explicitly
    with open(brutus_path, 'r') as f:
        # Read first few time stamps to determine dt
        times = []
        for line in f:
            if line.strip():
                parts = line.strip().split()
                if len(parts) == 3:  # Header line
                    times.append(float(parts[0]))
                    if len(times) > 2:
                        break
    
    if len(times) >= 2:
        dt_approx = times[1] - times[0]
        if abs(dt_approx - 0.01) < 0.005:
            fidelity = 'high'
            dt_out = 0.01
        elif abs(dt_approx - 0.08) < 0.02:
            fidelity = 'low'
            dt_out = 0.08
        elif abs(dt_approx - 0.17) < 0.02:
            fidelity = 'low'  
            dt_out = 0.17
        else:
            # Default based on dataset type
            if dataset_type == 'hierarchical':
                fidelity = 'low'
                dt_out = 0.08
            else:
                fidelity = 'low'
                dt_out = 0.17
    else:
        raise ValueError(f"Cannot read timestamps from {brutus_path}")
    
    # Determine set name
    if dataset_type == 'hierarchical':
        set_name = '2a' if fidelity == 'high' else '1a'
    else:
        set_name = '2b' if fidelity == 'high' else '1b'
    
    return SimulationMetadata(
        trajectory_id=f"{dataset_type}_{traj_id}",
        ic_file=ic_path,
        brutus_file=brutus_path,
        dataset_type=dataset_type,
        fidelity=fidelity,
        dt_out=dt_out,
        set_name=set_name
    )


def parse_ic_file(filepath: Path) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Parse initial condition file.
    
    Format: Single line or 3 lines with 7 values each
    [m1, x1, y1, z1, vx1, vy1, vz1, m2, ..., m3, ...]
    
    Returns:
        masses: (3,) array
        positions: (3, 3) array
        velocities: (3, 3) array
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Handle both single-line and multi-line formats
    if len(lines) == 1:
        # Single line with 21 values
        data = np.fromstring(lines[0], sep=' ')
        if len(data) != 21:
            raise ValueError(f"Expected 21 values in IC file, got {len(data)}")
        
        masses = np.zeros(3)
        positions = np.zeros((3, 3))
        velocities = np.zeros((3, 3))
        
        for i in range(3):
            base_idx = i * 7
            masses[i] = data[base_idx]
            positions[i] = data[base_idx + 1:base_idx + 4]
            velocities[i] = data[base_idx + 4:base_idx + 7]
    
    elif len(lines) == 3:
        # Three lines, one per body
        masses = np.zeros(3)
        positions = np.zeros((3, 3))
        velocities = np.zeros((3, 3))
        
        for i, line in enumerate(lines):
            data = np.fromstring(line, sep=' ')
            if len(data) != 7:
                raise ValueError(f"Expected 7 values per body, got {len(data)} for body {i}")
            masses[i] = data[0]
            positions[i] = data[1:4]
            velocities[i] = data[4:7]
    
    else:
        raise ValueError(f"IC file should have 1 or 3 lines, got {len(lines)}")
    
    return masses, positions, velocities


def parse_brutus_file(filepath: Path, max_snapshots: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
    """
    Parse BRUTUS output file.
    
    Format: Blocks of data, each with:
    - Header: t, N, t_cpu
    - N lines of body data: m, x, y, z, vx, vy, vz
    
    Returns:
        times: (T,) array
        positions: (T, 3, 3) array
        velocities: (T, 3, 3) array
        metadata: dict with additional info
    """
    times = []
    positions = []
    velocities = []
    cpu_times = []
    masses_check = []
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Check for result line at the end
    metadata = {}
    if lines and lines[-1].startswith('Result:'):
        result_line = lines[-1]
        # Parse energy values
        match = re.search(r'E_initial=\s*([-\d.e]+)', result_line)
        if match:
            metadata['E_initial'] = float(match.group(1))
        match = re.search(r'E_final=\s*([-\d.e]+)', result_line)
        if match:
            metadata['E_final'] = float(match.group(1))
        match = re.search(r'dE/E=\s*([-\d.e]+)', result_line)
        if match:
            metadata['dE/E'] = float(match.group(1))
        # Remove result line from data
        lines = lines[:-1]
    
    i = 0
    snapshot_count = 0
    
    while i < len(lines):
        if max_snapshots and snapshot_count >= max_snapshots:
            break
            
        # Skip empty lines
        if not lines[i].strip():
            i += 1
            continue
        
        # Parse header
        header = lines[i].strip().split()
        if len(header) != 3:
            i += 1
            continue
        
        try:
            t = float(header[0])
            n_bodies = int(header[1])
            t_cpu = float(header[2])
        except (ValueError, IndexError):
            i += 1
            continue
        
        if n_bodies != 3:
            raise ValueError(f"Expected 3 bodies, got {n_bodies}")
        
        # Parse body data
        body_data = np.zeros((3, 7))
        try:
            for j in range(3):
                body_line = lines[i + 1 + j].strip().split()
                body_data[j] = [float(x) for x in body_line]
        except (IndexError, ValueError):
            i += 1
            continue
        
        times.append(t)
        cpu_times.append(t_cpu)
        positions.append(body_data[:, 1:4])  # x, y, z
        velocities.append(body_data[:, 4:7])  # vx, vy, vz
        masses_check.append(body_data[:, 0])  # masses
        
        i += 4
        snapshot_count += 1
    
    # Convert to arrays
    times = np.array(times)
    positions = np.array(positions)
    velocities = np.array(velocities)
    cpu_times = np.array(cpu_times)
    
    # Verify masses are consistent
    if masses_check:
        masses_check = np.array(masses_check)
        if not np.allclose(masses_check, masses_check[0]):
            print("Warning: Masses vary throughout simulation")
    
    metadata['cpu_times'] = cpu_times
    
    return times, positions, velocities, metadata


def parse_trajectory_pair(ic_path: Path, brutus_path: Path, 
                         detect_metadata: bool = True) -> RawTrajectoryData:
    """
    Parse a pair of IC and BRUTUS files into RawTrajectoryData.
    
    Args:
        ic_path: Path to IC file
        brutus_path: Path to BRUTUS file
        detect_metadata: Whether to auto-detect metadata from filenames
    
    Returns:
        RawTrajectoryData object
    """
    # Parse files
    masses, r_initial, v_initial = parse_ic_file(ic_path)
    times, positions, velocities, brutus_metadata = parse_brutus_file(brutus_path)
    
    # Get metadata
    if detect_metadata:
        metadata = detect_simulation_metadata(ic_path, brutus_path)
    else:
        # Create minimal metadata
        metadata = SimulationMetadata(
            trajectory_id=ic_path.stem,
            ic_file=ic_path,
            brutus_file=brutus_path,
            dataset_type='unknown',
            fidelity='unknown',
            dt_out=times[1] - times[0] if len(times) > 1 else 0.0,
            set_name='unknown'
        )
    
    return RawTrajectoryData(
        metadata=metadata,
        masses=masses,
        r_initial=r_initial,
        v_initial=v_initial,
        times=times,
        positions=positions,
        velocities=velocities,
        cpu_times=brutus_metadata.get('cpu_times'),
        energy_initial=brutus_metadata.get('E_initial'),
        energy_final=brutus_metadata.get('E_final'),
        energy_error=brutus_metadata.get('dE/E')
    )


# ============================================================================
# FILE: core/scaling.py
# ============================================================================
"""Scaling and normalization utilities"""

import numpy as np
from typing import List, Optional, Tuple
from core.data_structures import (
    RawTrajectoryData, ScaledTrajectoryData, GlobalScales, ProcessedTrajectory
)


def compute_global_scales(trajectories: List[RawTrajectoryData], 
                         verbose: bool = True) -> GlobalScales:
    """
    Compute global normalization scales across entire dataset.
    
    This must be called once on the entire dataset before processing
    individual trajectories.
    """
    scales = GlobalScales()
    
    if verbose:
        print(f"Computing global scales from {len(trajectories)} trajectories...")
        print(f"  Characteristic scales: D = {scales.D:.4f}, V = {scales.V:.4f}")
    
    all_E = []
    all_r_char = []
    
    for traj in trajectories:
        # Scale positions and velocities
        r_prime = traj.r_initial / scales.D
        v_prime = traj.v_initial / scales.V
        
        # Compute energy
        E = compute_energy(traj.masses, r_prime, v_prime)
        all_E.append(E)
        
        # Compute characteristic radius
        r_char = compute_r_char(r_prime)
        all_r_char.append(r_char)
    
    # Set global scales
    scales.E_scale = np.abs(np.median(all_E)) + 1e-8
    scales.smin_scale = np.median(all_r_char)
    
    # Store additional statistics
    scales.dataset_stats = {
        'E_mean': np.mean(all_E),
        'E_std': np.std(all_E),
        'E_min': np.min(all_E),
        'E_max': np.max(all_E),
        'r_char_mean': np.mean(all_r_char),
        'r_char_std': np.std(all_r_char),
        'n_trajectories': len(trajectories)
    }
    
    if verbose:
        print(f"  E_scale: {scales.E_scale:.6f}")
        print(f"  smin_scale: {scales.smin_scale:.6f}")
        print(f"  E range: [{scales.dataset_stats['E_min']:.3f}, {scales.dataset_stats['E_max']:.3f}]")
    
    return scales


def scale_trajectory(raw_traj: RawTrajectoryData, 
                    global_scales: GlobalScales) -> ScaledTrajectoryData:
    """
    Scale a single trajectory to dimensionless units.
    """
    # Scale initial conditions
    r_prime = raw_traj.r_initial / global_scales.D
    v_prime = raw_traj.v_initial / global_scales.V
    
    # Scale time series
    positions_scaled = raw_traj.positions / global_scales.D
    velocities_scaled = raw_traj.velocities / global_scales.V
    
    return ScaledTrajectoryData(
        metadata=raw_traj.metadata,
        raw_data=raw_traj,
        masses=raw_traj.masses.copy(),  # Masses don't scale
        r_prime=r_prime,
        v_prime=v_prime,
        times=raw_traj.times.copy(),
        positions_scaled=positions_scaled,
        velocities_scaled=velocities_scaled,
        length_scale=global_scales.D,
        velocity_scale=global_scales.V,
        time_scale=global_scales.T_max
    )


def verify_com_frame(masses: np.ndarray, positions: np.ndarray, 
                    velocities: np.ndarray, eps: float = 1e-12) -> bool:
    """
    Verify that the system is in the center-of-mass frame.
    """
    # Check COM position
    com_pos = np.sum(masses[:, np.newaxis] * positions, axis=0) / np.sum(masses)
    if np.linalg.norm(com_pos) > eps:
        print(f"Warning: COM position {com_pos} exceeds tolerance {eps}")
        return False
    
    # Check COM velocity (total momentum)
    com_vel = np.sum(masses[:, np.newaxis] * velocities, axis=0) / np.sum(masses)
    if np.linalg.norm(com_vel) > eps:
        print(f"Warning: COM velocity {com_vel} exceeds tolerance {eps}")
        return False
    
    return True


def apply_canonical_ordering(masses: np.ndarray, positions: np.ndarray, 
                           velocities: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Apply canonical ordering to ensure permutation invariance.
    
    Returns:
        Reordered (masses, positions, velocities, permutation_indices)
    """
    # Create sorting keys: primary by mass (descending), 
    # secondary by distance from origin, tertiary by speed
    keys = []
    for i in range(3):
        key = (-masses[i], 
               np.linalg.norm(positions[i]), 
               np.linalg.norm(velocities[i]))
        keys.append(key)
    
    # Get sorting indices
    idx = sorted(range(3), key=lambda i: keys[i])
    idx = np.array(idx)
    
    # Reorder all quantities
    masses_ordered = masses[idx]
    positions_ordered = positions[idx]
    velocities_ordered = velocities[idx]
    
    return masses_ordered, positions_ordered, velocities_ordered, idx


# Helper functions for computing quantities
def compute_energy(masses: np.ndarray, r_prime: np.ndarray, 
                  v_prime: np.ndarray, eps: float = 1e-10) -> float:
    """Compute total mechanical energy."""
    # Kinetic energy
    T = 0.5 * np.sum(masses * np.sum(v_prime**2, axis=1))
    
    # Potential energy with softening
    V = 0.0
    for i in range(3):
        for j in range(i+1, 3):
            r_ij = np.linalg.norm(r_prime[i] - r_prime[j]) + eps
            V -= masses[i] * masses[j] / r_ij
    
    return T + V


def compute_r_char(r_prime: np.ndarray) -> float:
    """Compute characteristic radius."""
    pairwise_dists = []
    for i in range(3):
        for j in range(i+1, 3):
            pairwise_dists.append(np.linalg.norm(r_prime[i] - r_prime[j]))
    return np.mean(pairwise_dists) if pairwise_dists else 0.0


# ============================================================================
# FILE: processing/invariants.py
# ============================================================================
"""Physical invariants computation"""

import numpy as np
from scipy.interpolate import interp1d
from sklearn.decomposition import PCA
from scipy.signal import correlate
from scipy.stats import linregress
from typing import Optional
from core.data_structures import ScaledTrajectoryData, PhysicalInvariants


def compute_basic_invariants(masses: np.ndarray, r_prime: np.ndarray, 
                           v_prime: np.ndarray, eps: float = 1e-10) -> Tuple[float, float, float]:
    """
    Compute E, Q, s_min from scaled initial conditions.
    
    CRITICAL: ε is used ONLY in potential V to avoid singularities
    s_min is computed from exact separations (no ε)
    """
    # Kinetic energy
    T = 0.5 * np.sum(masses * np.sum(v_prime**2, axis=1))
    
    # Potential energy with softening
    V = 0.0
    pairwise_dists = []
    
    for i in range(3):
        for j in range(i+1, 3):
            r_ij_exact = np.linalg.norm(r_prime[i] - r_prime[j])
            pairwise_dists.append(r_ij_exact)
            V -= masses[i] * masses[j] / (r_ij_exact + eps)
    
    E = T + V
    Q = 2 * T / np.abs(V) if np.abs(V) > eps else 0.0
    s_min = min(pairwise_dists) if pairwise_dists else 0.0
    
    return E, Q, s_min


def compute_angular_momentum_canonical(masses: np.ndarray, r_prime: np.ndarray, 
                                     v_prime: np.ndarray, E: float, 
                                     eps: float = 1e-10) -> Tuple[float, float, float, float]:
    """
    Compute L_norm using the CANONICAL formula from CTL framework.
    
    Returns: (L_max, L_norm, r_char, v_char)
    """
    # Total angular momentum
    L_vec = np.sum([masses[i] * np.cross(r_prime[i], v_prime[i]) for i in range(3)], axis=0)
    L = np.linalg.norm(L_vec)
    
    # Characteristic scales
    pairwise_dists = []
    for i in range(3):
        for j in range(i+1, 3):
            pairwise_dists.append(np.linalg.norm(r_prime[i] - r_prime[j]))
    
    r_char = np.mean(pairwise_dists) if pairwise_dists else 0.0
    M_total = np.sum(masses)
    v_char = np.sqrt(2 * np.abs(E) / M_total) if M_total > eps else 0.0
    
    L_max = M_total * r_char * v_char
    L_norm = L / (L_max + eps) if L_max > eps else 0.0
    
    return L_max, L_norm, r_char, v_char


def compute_moment_of_inertia_normalized(masses: np.ndarray, r_prime: np.ndarray,
                                       r_char: float, eps: float = 1e-10) -> float:
    """Compute normalized trace of moment of inertia tensor."""
    I_tensor = np.zeros((3, 3))
    for i in range(3):
        ri = r_prime[i]
        ri_norm_sq = np.dot(ri, ri)
        outer = np.outer(ri, ri)
        I_tensor += masses[i] * (ri_norm_sq * np.eye(3) - outer)
    
    I_trace = np.trace(I_tensor)
    M_total = np.sum(masses)
    denom = M_total * max(r_char**2, eps)
    I_norm = I_trace / denom
    
    return I_norm


def estimate_autocorrelation_time(series: np.ndarray, max_lag: Optional[int] = None) -> int:
    """Estimate autocorrelation time for Lyapunov calculation."""
    if max_lag is None:
        max_lag = len(series) // 4
    
    # Normalize series
    series = series - np.mean(series)
    c0 = np.dot(series, series) / len(series)
    
    if c0 == 0:
        return 1
    
    # Compute autocorrelation
    acf = correlate(series, series, mode='full')[len(series)-1:]
    acf = acf[:max_lag] / acf[0]
    
    # Find first zero crossing
    zero_crossings = np.where(np.diff(np.sign(acf)))[0]
    if len(zero_crossings) > 0:
        return zero_crossings[0] + 1
    
    # Otherwise find 1/e decay
    decay_idx = np.where(acf < 1/np.e)[0]
    if len(decay_idx) > 0:
        return decay_idx[0]
    
    return max_lag // 2


def rosenstein_lyapunov(series: np.ndarray, emb_dim: int = 2, 
                       tau: Optional[int] = None, theiler_window: Optional[int] = None,
                       n_neighbors: int = 5, fit_points: int = 10) -> float:
    """Rosenstein-style Lyapunov exponent estimation."""
    T = len(series)
    
    # Auto-determine tau if not provided
    if tau is None:
        tau = estimate_autocorrelation_time(series)
        tau = max(1, min(tau, T // 10))
    
    # Set Theiler window = tau if not provided
    if theiler_window is None:
        theiler_window = tau
    
    # Check if series is too short
    min_length = emb_dim * tau + fit_points + theiler_window
    if T < min_length:
        return 0.0
    
    # Delay embedding
    n_vecs = T - (emb_dim - 1) * tau
    if n_vecs < 2 * theiler_window:
        return 0.0
    
    embedded = np.zeros((n_vecs, emb_dim))
    for i in range(emb_dim):
        embedded[:, i] = series[i*tau:i*tau + n_vecs]
    
    # Compute divergence curve
    max_k = min(fit_points * 2, n_vecs // 2)
    divergence = np.zeros(max_k)
    
    for k in range(1, max_k + 1):
        log_divs = []
        
        for i in range(n_vecs - k):
            # Find neighbors with Theiler window constraint
            valid_idx = []
            for j in range(n_vecs - k):
                if abs(j - i) >= theiler_window:
                    valid_idx.append(j)
            
            if len(valid_idx) < n_neighbors:
                continue
            
            # Compute distances and find nearest neighbors
            dists = np.linalg.norm(embedded[valid_idx] - embedded[i], axis=1)
            nearest_idx = np.argsort(dists)[:n_neighbors]
            
            # Compute divergence after k steps
            for idx in nearest_idx:
                j = valid_idx[idx]
                div = np.linalg.norm(embedded[i + k] - embedded[j + k])
                if div > 0:
                    log_divs.append(np.log(div))
        
        if log_divs:
            divergence[k-1] = np.mean(log_divs)
    
    # Fit linear region
    valid_points = np.where(divergence > 0)[0][:fit_points]
    
    if len(valid_points) < 2:
        return 0.0
    
    # Linear regression
    k_values = valid_points + 1
    slope, _, _, _, _ = linregress(k_values, divergence[valid_points])
    
    return max(0.0, slope)


def estimate_lyapunov_time(scaled_traj: ScaledTrajectoryData, 
                          resample_dt: Optional[float] = None) -> float:
    """
    Estimate Lyapunov time from trajectory.
    Uses PCA(1) reduction and Rosenstein algorithm.
    """
    times = scaled_traj.times
    positions = scaled_traj.positions_scaled
    
    # Check minimum length
    if len(times) < 200:
        return float('inf')
    
    # Resample to uniform cadence if needed
    if resample_dt is not None or (len(times) > 1 and np.std(np.diff(times)) > 1e-6):
        if resample_dt is None:
            resample_dt = np.median(np.diff(times))
        
        t_uniform = np.arange(times[0], times[-1], resample_dt)
        positions_resampled = np.zeros((len(t_uniform), 3, 3))
        
        for i in range(3):
            for j in range(3):
                f = interp1d(times, positions[:, i, j], kind='linear', 
                           fill_value='extrapolate')
                positions_resampled[:, i, j] = f(t_uniform)
        
        positions = positions_resampled
    
    # Flatten positions to (T, 9)
    T = len(positions)
    flat_pos = positions.reshape(T, -1)
    
    # PCA reduction to 1 component
    pca = PCA(n_components=1)
    pca_series = pca.fit_transform(flat_pos).flatten()
    
    # Estimate Lyapunov exponent
    lambda_pca = rosenstein_lyapunov(pca_series)
    
    # Also compute for individual body x-coordinates and take median
    lambdas = [lambda_pca]
    for body in range(3):
        x_series = positions[:, body, 0]
        lambda_body = rosenstein_lyapunov(x_series)
        lambdas.append(lambda_body)
    
    # Use median for robustness
    lambda_max = np.median([l for l in lambdas if l > 0])
    
    if lambda_max <= 0:
        return float('inf')
    
    return 1.0 / lambda_max


def compute_all_invariants(scaled_traj: ScaledTrajectoryData) -> PhysicalInvariants:
    """Compute all physical invariants for a trajectory."""
    masses = scaled_traj.masses
    r_prime = scaled_traj.r_prime
    v_prime = scaled_traj.v_prime
    
    # Basic invariants
    E, Q, s_min = compute_basic_invariants(masses, r_prime, v_prime)
    
    # Angular momentum
    L_max, L_norm, r_char, v_char = compute_angular_momentum_canonical(
        masses, r_prime, v_prime, E
    )
    
    # Moment of inertia
    I_norm = compute_moment_of_inertia_normalized(masses, r_prime, r_char)
    
    # Lyapunov time
    tau_L = estimate_lyapunov_time(scaled_traj)
    
    return PhysicalInvariants(
        E=E, Q=Q, s_min=s_min,
        L_norm=L_norm, I_norm=I_norm, tau_L=tau_L,
        L_max=L_max, r_char=r_char, v_char=v_char
    )


# ============================================================================
# FILE: processing/stage_assignment.py
# ============================================================================
"""Curriculum stage assignment logic"""

import numpy as np
from typing import Dict, Optional, List
from core.data_structures import PhysicalInvariants, ProcessedTrajectory


def compute_dataset_quantiles(trajectories: List[ProcessedTrajectory]) -> Dict[str, float]:
    """
    Compute dataset quantiles for Stage 3 assignment.
    Only uses low-fidelity quasi-random data.
    """
    low_fidelity_E = []
    low_fidelity_L_norm = []
    
    for traj in trajectories:
        if not traj.metadata.is_hierarchical and traj.metadata.fidelity == 'low':
            low_fidelity_E.append(traj.invariants.E)
            low_fidelity_L_norm.append(traj.invariants.L_norm)
    
    if not low_fidelity_E:
        return {}
    
    return {
        'E_25': np.percentile(low_fidelity_E, 25),
        'L_75': np.percentile(low_fidelity_L_norm, 75)
    }


def assign_curriculum_stage(invariants: PhysicalInvariants, 
                          is_hierarchical: bool,
                          is_high_fidelity: bool,
                          dataset_quantiles: Optional[Dict] = None) -> int:
    """
    Assign curriculum stage based on invariants and data type.
    
    Stages:
    0: Easiest hierarchical (low-fidelity)
    1: Moderately stable hierarchical (low-fidelity)
    2: High-resolution hierarchical refinement
    3: Moderately chaotic low-fidelity
    4: Chaotic low-fidelity
    5: High-resolution chaotic
    6: Near-collision and extreme cases
    """
    E = invariants.E
    Q = invariants.Q
    s_min = invariants.s_min
    L_norm = invariants.L_norm
    tau_L = invariants.tau_L
    
    # Stage 6: Extreme cases (highest priority, any dataset)
    if s_min < 0.5 or abs(E) < 0.01:
        return 6
    
    # For hierarchical data
    if is_hierarchical:
        if is_high_fidelity:
            # Stage 2: High-resolution refinement of stable orbits
            # This includes all hierarchical high-fidelity data
            return 2
        else:
            # Low-fidelity hierarchical
            # Stage 0: Easiest
            if E < -0.5 and L_norm > 0.5 and 0.7 <= Q <= 1.3 and s_min > 2:
                return 0
            
            # Stage 1a: Energy relaxed
            if -0.5 <= E < -0.1 and L_norm > 0.5 and 0.7 <= Q <= 1.3 and s_min > 2:
                return 1
            
            # Stage 1b: Angular momentum relaxed
            if E < -0.5 and 0.1 <= L_norm < 0.5 and 0.7 <= Q <= 1.3 and s_min > 2:
                return 1
            
            # Other hierarchical that don't fit stages 0 or 1
            # These will be included in stage 2 during training
            return 1  # Default to stage 1 for consistency
    
    # For quasi-random data
    else:
        if is_high_fidelity:
            # Stage 5: High-resolution chaotic
            return 5
        else:
            # Low-fidelity quasi-random
            # Stage 3: Moderately chaotic (needs quantiles)
            if dataset_quantiles:
                E_25 = dataset_quantiles.get('E_25', -0.3)
                L_75 = dataset_quantiles.get('L_75', 0.3)
                
                if E <= E_25 and L_norm >= L_75 and 0.9 <= Q <= 1.1:
                    return 3
            
            # Stage 4a: Chaotic with longer predictability
            if tau_L > 5:
                return 4
            
            # Stage 4b: Highly chaotic
            if 2 < tau_L <= 5:
                return 4
            
            # Default for other chaotic cases
            return 4


def assign_stages_to_dataset(trajectories: List[ProcessedTrajectory], 
                           verbose: bool = True) -> None:
    """
    Assign curriculum stages to all trajectories in dataset.
    Modifies trajectories in-place by setting the stage attribute.
    """
    # First compute dataset quantiles
    dataset_quantiles = compute_dataset_quantiles(trajectories)
    
    if verbose and dataset_quantiles:
        print(f"Dataset quantiles for Stage 3:")
        print(f"  E_25: {dataset_quantiles['E_25']:.3f}")
        print(f"  L_75: {dataset_quantiles['L_75']:.3f}")
    
    # Assign stages
    stage_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    
    for traj in trajectories:
        stage = assign_curriculum_stage(
            traj.invariants,
            traj.metadata.is_hierarchical,
            traj.metadata.is_high_fidelity,
            dataset_quantiles
        )
        traj.stage = stage
        stage_counts[stage] += 1
    
    if verbose:
        print("\nStage assignment summary:")
        for stage in sorted(stage_counts.keys()):
            count = stage_counts[stage]
            if count > 0:
                print(f"  Stage {stage}: {count} trajectories")


# ============================================================================
# FILE: processing/input_vector.py
# ============================================================================
"""PINN input vector formulation"""

import numpy as np
from typing import Tuple, Optional
from core.data_structures import ScaledTrajectoryData, GlobalScales


def compute_shape_invariants(r_prime: np.ndarray) -> Tuple[float, float, float]:
    """
    Compute universal shape invariants I1, I2, I3.
    
    Returns:
        I1: d_short/d_long ∈ [0, 1]
        I2: d_mid/d_long ∈ [I1, 1]
        I3: (d_short + d_mid - d_long)/(d_short + d_mid + d_long) ∈ [-1, 1]
    """
    # Compute pairwise distances
    d12 = np.linalg.norm(r_prime[0] - r_prime[1])
    d13 = np.linalg.norm(r_prime[0] - r_prime[2])
    d23 = np.linalg.norm(r_prime[1] - r_prime[2])
    
    # Sort distances
    distances = sorted([d12, d13, d23])
    d_short, d_mid, d_long = distances
    
    # Compute invariants
    I1 = d_short / (d_long + 1e-10)
    I2 = d_mid / (d_long + 1e-10)
    I3 = (d_short + d_mid - d_long) / (d_short + d_mid + d_long + 1e-10)
    
    return I1, I2, I3


def compute_velocity_angles(r_prime: np.ndarray, v_prime: np.ndarray, 
                          eps: float = 1e-10) -> Tuple[float, float]:
    """
    Compute angles between position and velocity vectors.
    
    Returns:
        Two normalized angles ∈ [0, 1]
    """
    angles = []
    for i in range(2):  # Only 2 angles needed
        r_norm = np.linalg.norm(r_prime[i])
        v_norm = np.linalg.norm(v_prime[i])
        
        if r_norm < eps or v_norm < eps:
            angle = np.pi / 2  # Default perpendicular
        else:
            dot = np.dot(r_prime[i], v_prime[i])
            cross = np.cross(r_prime[i], v_prime[i])
            cross_norm = np.linalg.norm(cross)
            angle = np.arctan2(cross_norm, dot)  # Stable [0, pi]
        
        angles.append(angle / np.pi)  # Normalize to [0,1]
    
    return tuple(angles)


def normalize_ic_components(invariants, masses, shape_invariants, velocity_angles,
                          global_scales: GlobalScales) -> np.ndarray:
    """
    Normalize all IC components to [-1, 1] range.
    
    Returns:
        13-component normalized IC vector
    """
    # Extract invariants
    E = invariants.E
    Q = invariants.Q
    s_min = invariants.s_min
    L_norm = invariants.L_norm
    I_norm = invariants.I_norm
    
    # Extract shape invariants
    I1, I2, I3 = shape_invariants
    
    # Extract velocity angles
    theta1, theta2 = velocity_angles
    
    # Normalize components
    E_norm = np.tanh(E / global_scales.E_scale)
    Q_norm = np.tanh((Q - 1) / global_scales.Q_scale)
    smin_norm = np.tanh(s_min / global_scales.smin_scale)
    
    # Mass fractions
    m_total = np.sum(masses) + 1e-8
    m_norm = 2 * (masses / m_total) - 1  # Array for all 3 masses
    
    # Shape invariants normalization
    I1_norm = 2 * I1 - 1  # Map [0,1] to [-1,1]
    I2_norm = 2 * I2 - 1  # Map [0,1] to [-1,1]
    # I3 already in [-1,1]
    
    # Velocity angles normalization
    theta_norm = 2 * np.array([theta1, theta2]) - 1  # Map [0,1] to [-1,1]
    
    # Moment of inertia normalization
    I_norm_bounded = np.tanh(I_norm)  # Bound to [-1,1]
    
    # Assemble IC vector
    ic_vector = np.concatenate([
        m_norm,                    # 3 components
        [E_norm],                  # 1 component
        [L_norm],                  # 1 component (already in [0,1], map to [-1,1])
        [Q_norm],                  # 1 component
        [smin_norm],               # 1 component
        [I1_norm, I2_norm, I3],    # 3 components
        theta_norm,                # 2 components
        [I_norm_bounded]           # 1 component
    ])
    
    # L_norm adjustment (it's already in [0,1], so map to [-1,1])
    ic_vector[4] = 2 * L_norm - 1
    
    assert len(ic_vector) == 13, f"IC vector should have 13 components, got {len(ic_vector)}"
    
    return ic_vector


def formulate_ic_vector(scaled_traj: ScaledTrajectoryData, 
                       invariants: PhysicalInvariants,
                       global_scales: GlobalScales,
                       apply_ordering: bool = True) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """
    Formulate the 13-component IC vector for PINN input.
    
    Returns:
        ic_vector: 13-component normalized vector
        ordering: permutation indices if apply_ordering=True, else None
    """
    masses = scaled_traj.masses
    r_prime = scaled_traj.r_prime
    v_prime = scaled_traj.v_prime
    
    # Apply canonical ordering if requested
    if apply_ordering:
        from core.scaling import apply_canonical_ordering
        masses, r_prime, v_prime, ordering = apply_canonical_ordering(
            masses, r_prime, v_prime
        )
    else:
        ordering = None
    
    # Compute shape invariants
    shape_invariants = compute_shape_invariants(r_prime)
    
    # Compute velocity angles
    velocity_angles = compute_velocity_angles(r_prime, v_prime)
    
    # Normalize all components
    ic_vector = normalize_ic_components(
        invariants, masses, shape_invariants, velocity_angles, global_scales
    )
    
    return ic_vector, ordering


# ============================================================================
# FILE: scripts/preprocess_dataset.py
# ============================================================================
"""
Main preprocessing script that parses raw files and saves in reusable format.
This should be run once on your dataset.
"""

import numpy as np
import argparse
from pathlib import Path
import pickle
import h5py
from typing import List, Dict
import json
from tqdm import tqdm

# Import all necessary modules
from core.data_structures import *
from core.parsing import parse_trajectory_pair
from core.scaling import compute_global_scales, scale_trajectory, verify_com_frame
from processing.invariants import compute_all_invariants
from processing.stage_assignment import assign_stages_to_dataset
from processing.input_vector import formulate_ic_vector


def save_dataset_hdf5(trajectories: List[ProcessedTrajectory], 
                     global_scales: GlobalScales,
                     output_path: Path):
    """Save processed dataset in HDF5 format."""
    with h5py.File(output_path, 'w') as f:
        # Save global scales
        scales_group = f.create_group('global_scales')
        scales_group.attrs['T_max'] = global_scales.T_max
        scales_group.attrs['G'] = global_scales.G
        scales_group.attrs['D'] = global_scales.D
        scales_group.attrs['V'] = global_scales.V
        scales_group.attrs['E_scale'] = global_scales.E_scale
        scales_group.attrs['smin_scale'] = global_scales.smin_scale
        scales_group.attrs['Q_scale'] = global_scales.Q_scale
        
        # Save dataset statistics
        stats_group = f.create_group('dataset_stats')
        for key, value in global_scales.dataset_stats.items():
            stats_group.attrs[key] = value
        
        # Save trajectories
        traj_group = f.create_group('trajectories')
        
        for i, traj in enumerate(trajectories):
            traj_id = traj.metadata.trajectory_id
            g = traj_group.create_group(traj_id)
            
            # Metadata
            meta = g.create_group('metadata')
            meta.attrs['trajectory_id'] = traj_id
            meta.attrs['dataset_type'] = traj.metadata.dataset_type
            meta.attrs['fidelity'] = traj.metadata.fidelity
            meta.attrs['dt_out'] = traj.metadata.dt_out
            meta.attrs['set_name'] = traj.metadata.set_name
            meta.attrs['ic_file'] = str(traj.metadata.ic_file)
            meta.attrs['brutus_file'] = str(traj.metadata.brutus_file)
            
            # Raw data
            raw = g.create_group('raw')
            raw.create_dataset('masses', data=traj.scaled_data.raw_data.masses)
            raw.create_dataset('r_initial', data=traj.scaled_data.raw_data.r_initial)
            raw.create_dataset('v_initial', data=traj.scaled_data.raw_data.v_initial)
            raw.create_dataset('times', data=traj.scaled_data.raw_data.times)
            raw.create_dataset('positions', data=traj.scaled_data.raw_data.positions)
            raw.create_dataset('velocities', data=traj.scaled_data.raw_data.velocities)
            
            # Scaled data
            scaled = g.create_group('scaled')
            scaled.create_dataset('r_prime', data=traj.scaled_data.r_prime)
            scaled.create_dataset('v_prime', data=traj.scaled_data.v_prime)
            scaled.create_dataset('positions_scaled', data=traj.scaled_data.positions_scaled)
            scaled.create_dataset('velocities_scaled', data=traj.scaled_data.velocities_scaled)
            
            # Invariants
            inv = g.create_group('invariants')
            inv.attrs['E'] = traj.invariants.E
            inv.attrs['Q'] = traj.invariants.Q
            inv.attrs['s_min'] = traj.invariants.s_min
            inv.attrs['L_norm'] = traj.invariants.L_norm
            inv.attrs['I_norm'] = traj.invariants.I_norm
            inv.attrs['tau_L'] = traj.invariants.tau_L
            inv.attrs['L_max'] = traj.invariants.L_max
            inv.attrs['r_char'] = traj.invariants.r_char
            inv.attrs['v_char'] = traj.invariants.v_char
            
            # Stage assignment
            g.attrs['stage'] = traj.stage if traj.stage is not None else -1
            
            # IC vector
            if traj.ic_vector is not None:
                g.create_dataset('ic_vector', data=traj.ic_vector)


def main():
    parser = argparse.ArgumentParser(description='Preprocess CTL-PINN dataset')
    parser.add_argument('--ic_dir', type=Path, required=True,
                       help='Directory containing IC files')
    parser.add_argument('--brutus_dir', type=Path, required=True,
                       help='Directory containing BRUTUS files')
    parser.add_argument('--output', type=Path, required=True,
                       help='Output HDF5 file')
    parser.add_argument('--max_trajectories', type=int, default=None,
                       help='Maximum number of trajectories to process')
    parser.add_argument('--verify_com', action='store_true',
                       help='Verify center-of-mass frame')
    parser.add_argument('--compute_ic_vectors', action='store_true',
                       help='Compute IC vectors for all trajectories')
    
    args = parser.parse_args()
    
    # Find all IC files
    ic_files = sorted(args.ic_dir.glob('ic_*.txt'))
    if args.max_trajectories:
        ic_files = ic_files[:args.max_trajectories]
    
    print(f"Found {len(ic_files)} IC files")
    
    # Parse all trajectories
    print("Parsing trajectories...")
    raw_trajectories = []
    
    for ic_file in tqdm(ic_files):
        # Find corresponding BRUTUS file
        brutus_name = ic_file.name.replace('ic_', 'brutus_')
        brutus_file = args.brutus_dir / brutus_name
        
        if not brutus_file.exists():
            print(f"Warning: No BRUTUS file for {ic_file.name}")
            continue
        
        try:
            raw_traj = parse_trajectory_pair(ic_file, brutus_file)
            
            # Verify COM frame if requested
            if args.verify_com:
                is_com = verify_com_frame(
                    raw_traj.masses, 
                    raw_traj.r_initial, 
                    raw_traj.v_initial
                )
                if not is_com:
                    print(f"Warning: {ic_file.name} not in COM frame")
            
            raw_trajectories.append(raw_traj)
        
        except Exception as e:
            print(f"Error processing {ic_file.name}: {e}")
            continue
    
    print(f"Successfully parsed {len(raw_trajectories)} trajectories")
    
    # Compute global scales
    print("\nComputing global scales...")
    global_scales = compute_global_scales(raw_trajectories)
    
    # Process all trajectories
    print("\nProcessing trajectories...")
    processed_trajectories = []
    
    for raw_traj in tqdm(raw_trajectories):
        # Scale trajectory
        scaled_traj = scale_trajectory(raw_traj, global_scales)
        
        # Compute invariants
        invariants = compute_all_invariants(scaled_traj)
        
        # Create processed trajectory
        proc_traj = ProcessedTrajectory(
            metadata=raw_traj.metadata,
            scaled_data=scaled_traj,
            invariants=invariants
        )
        
        # Compute IC vector if requested
        if args.compute_ic_vectors:
            ic_vector, ordering = formulate_ic_vector(
                scaled_traj, invariants, global_scales
            )
            proc_traj.ic_vector = ic_vector
            proc_traj.canonical_ordering = ordering
        
        processed_trajectories.append(proc_traj)
    
    # Assign stages
    print("\nAssigning curriculum stages...")
    assign_stages_to_dataset(processed_trajectories)
    
    # Save dataset
    print(f"\nSaving to {args.output}...")
    save_dataset_hdf5(processed_trajectories, global_scales, args.output)
    
    print("Done!")


if __name__ == '__main__':
    main()


# ============================================================================
# FILE: scripts/prepare_training_data.py
# ============================================================================
"""
Script to prepare final training data for PINN from preprocessed HDF5 file.
This creates the actual training batches organized by curriculum stage.
"""

import numpy as np
import h5py
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import pickle
from tqdm import tqdm


def load_stage_data(hdf5_path: Path, stage: int, 
                   include_previous: bool = True) -> Dict:
    """
    Load training data for a specific curriculum stage.
    
    Args:
        hdf5_path: Path to preprocessed HDF5 file
        stage: Current curriculum stage
        include_previous: Whether to include all previous stages (replay)
    
    Returns:
        Dictionary with training data
    """
    training_data = {
        'ic_vectors': [],
        'times': [],
        'positions': [],
        'velocities': [],
        'metadata': [],
        'invariants': []
    }
    
    with h5py.File(hdf5_path, 'r') as f:
        # Get trajectories for this stage
        for traj_id in f['trajectories']:
            traj = f['trajectories'][traj_id]
            traj_stage = traj.attrs.get('stage', -1)
            
            # Include if in current stage or previous stages (if replay enabled)
            if traj_stage == stage or (include_previous and traj_stage < stage and traj_stage >= 0):
                # Load IC vector
                if 'ic_vector' in traj:
                    ic_vector = traj['ic_vector'][:]
                else:
                    continue  # Skip if no IC vector
                
                # Load trajectory data
                times = traj['raw/times'][:]
                positions = traj['scaled/positions_scaled'][:]
                velocities = traj['scaled/velocities_scaled'][:]
                
                # Store data
                training_data['ic_vectors'].append(ic_vector)
                training_data['times'].append(times)
                training_data['positions'].append(positions)
                training_data['velocities'].append(velocities)
                
                # Store metadata
                meta = {
                    'trajectory_id': traj.attrs['trajectory_id'],
                    'stage': traj_stage,
                    'dataset_type': traj['metadata'].attrs['dataset_type'],
                    'fidelity': traj['metadata'].attrs['fidelity']
                }
                training_data['metadata'].append(meta)
                
                # Store invariants
                inv = {k: v for k, v in traj['invariants'].attrs.items()}
                training_data['invariants'].append(inv)
    
    # Convert lists to arrays where appropriate
    training_data['ic_vectors'] = np.array(training_data['ic_vectors'])
    
    return training_data


def create_training_batches(training_data: Dict, 
                           batch_size: int = 256,
                           points_per_trajectory: int = 32,
                           time_sampling: str = 'mixed') -> List[Dict]:
    """
    Create training batches from stage data.
    
    Args:
        training_data: Dictionary with training data
        batch_size: Number of trajectory samples per batch
        points_per_trajectory: Number of time points per trajectory
        time_sampling: 'uniform', 'acceleration', or 'mixed'
    
    Returns:
        List of batch dictionaries
    """
    batches = []
    n_trajectories = len(training_data['ic_vectors'])
    
    # For each trajectory, create multiple samples
    all_samples = []
    
    for i in range(n_trajectories):
        ic_vector = training_data['ic_vectors'][i]
        times = training_data['times'][i]
        positions = training_data['positions'][i]
        velocities = training_data['velocities'][i]
        
        # Sample time points
        n_times = len(times)
        if n_times < points_per_trajectory:
            # Use all available points
            time_indices = np.arange(n_times)
        else:
            if time_sampling == 'uniform':
                time_indices = np.linspace(0, n_times-1, points_per_trajectory, dtype=int)
            elif time_sampling == 'acceleration':
                # Compute acceleration magnitudes
                if n_times > 1:
                    accel = np.diff(velocities, axis=0) / np.diff(times)[:, None, None]
                    accel_mag = np.sum(np.linalg.norm(accel, axis=2), axis=1)
                    # Sample proportional to acceleration
                    probs = accel_mag / (np.sum(accel_mag) + 1e-10)
                    time_indices = np.random.choice(n_times-1, size=points_per_trajectory, p=probs)
                else:
                    time_indices = np.zeros(points_per_trajectory, dtype=int)
            else:  # mixed
                # 50% uniform, 50% acceleration-weighted
                n_uniform = points_per_trajectory // 2
                n_accel = points_per_trajectory - n_uniform
                
                uniform_indices = np.linspace(0, n_times-1, n_uniform, dtype=int)
                
                if n_times > 1:
                    accel = np.diff(velocities, axis=0) / np.diff(times)[:, None, None]
                    accel_mag = np.sum(np.linalg.norm(accel, axis=2), axis=1)
                    probs = accel_mag / (np.sum(accel_mag) + 1e-10)
                    accel_indices = np.random.choice(n_times-1, size=n_accel, p=probs)
                else:
                    accel_indices = np.zeros(n_accel, dtype=int)
                
                time_indices = np.concatenate([uniform_indices, accel_indices])
        
        # Create samples for this trajectory
        for idx in time_indices:
            sample = {
                'ic_vector': ic_vector,
                't': times[idx],
                'positions': positions[idx],
                'velocities': velocities[idx],
                'trajectory_idx': i,
                'time_idx': idx
            }
            all_samples.append(sample)
    
    # Shuffle samples
    np.random.shuffle(all_samples)
    
    # Create batches
    for i in range(0, len(all_samples), batch_size):
        batch_samples = all_samples[i:i+batch_size]
        
        batch = {
            'ic_vectors': np.array([s['ic_vector'] for s in batch_samples]),
            'times': np.array([s['t'] for s in batch_samples]),
            'positions': np.array([s['positions'] for s in batch_samples]),
            'velocities': np.array([s['velocities'] for s in batch_samples]),
            'trajectory_indices': np.array([s['trajectory_idx'] for s in batch_samples]),
            'time_indices': np.array([s['time_idx'] for s in batch_samples])
        }
        
        batches.append(batch)
    
    return batches


def save_stage_training_data(stage: int, training_data: Dict, 
                           batches: List[Dict], output_dir: Path):
    """Save training data for a stage."""
    stage_dir = output_dir / f'stage_{stage}'
    stage_dir.mkdir(exist_ok=True, parents=True)
    
    # Save raw training data
    np.savez(
        stage_dir / 'training_data.npz',
        ic_vectors=training_data['ic_vectors'],
        metadata=training_data['metadata'],
        invariants=training_data['invariants']
    )
    
    # Save batches
    with open(stage_dir / 'batches.pkl', 'wb') as f:
        pickle.dump(batches, f)
    
    # Save summary
    summary = {
        'n_trajectories': len(training_data['ic_vectors']),
        'n_batches': len(batches),
        'n_samples': sum(len(b['times']) for b in batches)
    }
    
    with open(stage_dir / 'summary.json', 'w') as f:
        json.dump(summary, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description='Prepare CTL-PINN training data')
    parser.add_argument('--input', type=Path, required=True,
                       help='Input preprocessed HDF5 file')
    parser.add_argument('--output_dir', type=Path, required=True,
                       help='Output directory for training data')
    parser.add_argument('--stages', type=int, nargs='+', default=[0, 1, 2, 3, 4, 5, 6],
                       help='Stages to prepare')
    parser.add_argument('--batch_size', type=int, default=256,
                       help='Batch size')
    parser.add_argument('--points_per_trajectory', type=int, default=32,
                       help='Time points per trajectory')
    parser.add_argument('--no_replay', action='store_true',
                       help='Disable curriculum replay')
    
    args = parser.parse_args()
    
    args.output_dir.mkdir(exist_ok=True, parents=True)
    
    # Process each stage
    for stage in args.stages:
        print(f"\nPreparing Stage {stage}...")
        
        # Load data
        training_data = load_stage_data(
            args.input, stage, 
            include_previous=not args.no_replay
        )
        
        if len(training_data['ic_vectors']) == 0:
            print(f"No data for stage {stage}, skipping...")
            continue
        
        print(f"Loaded {len(training_data['ic_vectors'])} trajectories")
        
        # Create batches
        batches = create_training_batches(
            training_data,
            batch_size=args.batch_size,
            points_per_trajectory=args.points_per_trajectory,
            time_sampling='mixed'
        )
        
        print(f"Created {len(batches)} batches")
        
        # Save
        save_stage_training_data(stage, training_data, batches, args.output_dir)
    
    print("\nDone!")


if __name__ == '__main__':
    main()