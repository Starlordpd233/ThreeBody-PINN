"""Physical invariants computation"""

import numpy as np
from scipy.interpolate import interp1d
from sklearn.decomposition import PCA
from scipy.signal import correlate
from scipy.stats import linregress
from typing import Optional, Tuple
from ..core.data_structures import ScaledTrajectoryData, PhysicalInvariants


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