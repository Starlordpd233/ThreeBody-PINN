import numpy as np
from scipy.interpolate import CubicSpline
from scipy.spatial import KDTree
from scipy.stats import linregress
from sklearn.decomposition import PCA
from scipy.signal import correlate

def compute_lyapunov_time(times, positions, 
                         method='full_state',  # 'full_state' or 'pca_reduced'
                         embedding_dim=5,
                         theiler_factor=1,
                         min_neighbors=5,
                         dt=None,
                         scaled=True,  # whether positions are already scaled
                         eps=1e-10):
    """
    Enhanced Lyapunov time estimation aligned with CTL framework.
    
    Parameters:
    -----------
    times : array-like
        Time points from BRUTUS output
    positions : np.ndarray (T, 3, 3)
        Positions of 3 bodies (already scaled if scaled=True)
    method : str
        'full_state': Use all 9D (original implementation)
        'pca_reduced': Use PCA reduction as mentioned in CTL doc
    embedding_dim : int
        Embedding dimension for delay coordinates (if using embedding)
    scaled : bool
        Whether positions are already in scaled units
    
    Returns:
    --------
    tau_L : float
        Lyapunov time (returns np.inf for regular orbits)
    lambda_max : float
        Maximum Lyapunov exponent
    diagnostics : dict
        Additional diagnostic information
    """
    
    T = len(times)
    if T < 50:  # Too short for reliable estimation
        return np.inf, 0.0, {'reason': 'trajectory_too_short'}
    
    # Flatten positions based on method
    if method == 'full_state':
        R = positions.reshape(T, 9)
    elif method == 'pca_reduced':
        # Apply PCA reduction as mentioned in CTL
        R_flat = positions.reshape(T, 9)
        pca = PCA(n_components=1)
        R = pca.fit_transform(R_flat).reshape(-1, 1)
    else:
        raise ValueError(f"Unknown method: {method}")
    
    # Determine uniform timestep
    if dt is None:
        dt = np.median(np.diff(times))
    
    # Resample to uniform timestep
    t_uniform = np.arange(times[0], times[-1] + dt, dt)
    
    # Handle both 1D and multi-D interpolation
    if R.shape[1] == 1:
        cs = CubicSpline(times, R.ravel())
        R_uniform = cs(t_uniform).reshape(-1, 1)
    else:
        cs = CubicSpline(times, R)
        R_uniform = cs(t_uniform)
    
    T_u = len(t_uniform)
    
    if T_u < 50:
        return np.inf, 0.0, {'reason': 'uniform_trajectory_too_short'}
    
    # Compute optimal embedding delay using autocorrelation
    if method == 'pca_reduced' and embedding_dim > 1:
        delay = estimate_embedding_delay(R_uniform[:, 0])
        R_embedded = embed_trajectory(R_uniform[:, 0], embedding_dim, delay)
    else:
        R_embedded = R_uniform
        delay = 1
    
    # Adaptive reference state selection based on trajectory length
    n_refstates = min(T_u // 10, 100)  # More adaptive
    refstates = np.linspace(0, len(R_embedded) - 50, n_refstates, dtype=int)
    
    # Build KDTree
    tree = KDTree(R_embedded)
    
    # Theiler window (adaptive based on autocorrelation time)
    theiler = max(theiler_factor * delay, 1)
    
    # Find nearest neighbors and collect pairs
    pairs = []
    for i in refstates:
        dists, idxs = tree.query(R_embedded[i], k=min(T_u, 50))
        # Find first valid neighbor outside Theiler window
        for d, j in zip(dists[1:], idxs[1:]):
            if abs(i - j) > theiler and d > eps:
                pairs.append((i, j))
                break
    
    if len(pairs) < min_neighbors:
        return np.inf, 0.0, {'reason': 'insufficient_neighbors', 'n_pairs': len(pairs)}
    
    # Compute divergence curve
    max_k = min(50, (len(R_embedded) - max(i for i, _ in pairs)) // 2)
    ks = np.arange(1, max_k + 1)
    E = np.zeros(len(ks))
    counts = np.zeros(len(ks))
    
    for i, j in pairs:
        for m, k in enumerate(ks):
            if i + k < len(R_embedded) and j + k < len(R_embedded):
                d_k = np.linalg.norm(R_embedded[i + k] - R_embedded[j + k])
                if d_k > 0:
                    E[m] += np.log(d_k)
                    counts[m] += 1
    
    # Average
    mask = counts > len(pairs) // 2  # Require at least half the pairs
    E = E[mask] / counts[mask]
    ks_fit = ks[mask]
    
    if len(ks_fit) < 5:
        return np.inf, 0.0, {'reason': 'insufficient_divergence_points'}
    
    # Find linear region using more sophisticated method
    lambda_max, linear_range = find_linear_region(ks_fit * dt, E)
    
    if lambda_max <= 0:
        return np.inf, 0.0, {'reason': 'non_positive_exponent', 'lambda': lambda_max}
    
    tau_L = 1.0 / lambda_max
    
    diagnostics = {
        'lambda_max': lambda_max,
        'n_pairs': len(pairs),
        'linear_range': linear_range,
        'dt_used': dt,
        'embedding_delay': delay if method == 'pca_reduced' else None
    }
    
    return tau_L, lambda_max, diagnostics


def estimate_embedding_delay(x, max_lag=50):
    """Estimate embedding delay using autocorrelation first minimum."""
    x = x - np.mean(x)
    autocorr = correlate(x, x, mode='full')[len(x)-1:]
    autocorr = autocorr / autocorr[0]
    
    # Find first minimum
    for i in range(1, min(max_lag, len(autocorr)-1)):
        if autocorr[i] > autocorr[i-1] and autocorr[i-1] < autocorr[i+1]:
            return i
    return 10  # Default if no minimum found


def embed_trajectory(x, dim, delay):
    """Create delay embedding of 1D trajectory."""
    N = len(x) - (dim - 1) * delay
    embedded = np.zeros((N, dim))
    for i in range(dim):
        embedded[:, i] = x[i*delay:i*delay + N]
    return embedded


def find_linear_region(t, E, min_points=5):
    """
    Find optimal linear region in log divergence curve.
    Uses sliding window to find region with best R²
    """
    best_r2 = -np.inf
    best_slope = 0
    best_range = (0, len(t))
    
    for start in range(len(t) - min_points):
        for end in range(start + min_points, len(t)):
            if end - start < min_points:
                continue
            
            # Fit linear regression
            slope, intercept, r_value, _, _ = linregress(t[start:end], E[start:end])
            r2 = r_value**2
            
            # Prefer positive slopes with good fit
            if slope > 0 and r2 > best_r2:
                best_r2 = r2
                best_slope = slope
                best_range = (start, end)
    
    return best_slope, best_range


# Integration function for your pipeline
def add_lyapunov_time_to_invariants(trajectory_data, global_scales, 
                                   use_pca_method=False):
    """
    Compute Lyapunov time and add to invariants tuple.
    
    This integrates with your existing Step 3 workflow.
    """
    times = trajectory_data.times
    positions = trajectory_data.positions  # Should be (T, 3, 3)
    
    # Ensure we're working with scaled data
    if not trajectory_data.is_scaled:
        # Apply scaling if needed
        D = global_scales.D
        positions = positions / D
    
    method = 'pca_reduced' if use_pca_method else 'full_state'
    
    tau_L, lambda_max, diagnostics = compute_lyapunov_time(
        times, positions, method=method, dt=trajectory_data.dt_out
    )
    
    # Could log diagnostics for quality control
    if diagnostics.get('reason'):
        print(f"Warning: Lyapunov time estimation issue: {diagnostics['reason']}")
    
    return tau_L