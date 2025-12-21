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