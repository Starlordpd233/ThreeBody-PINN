"""
Core physics calculations for PINN data processing.
Adapted from pinn/data-processing-pipeline-full.py.
"""

import numpy as np

def compute_basic_invariants(masses, r_prime, v_prime, eps=1e-10):
    """
    Compute E, Q, s_min from scaled initial conditions.
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

def compute_angular_momentum_canonical(masses, r_prime, v_prime, E, eps=1e-10):
    """
    Compute L_norm using the CANONICAL formula from CTL framework.
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

def compute_moment_of_inertia_normalized(masses, r_prime, r_char, eps=1e-10):
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

def compute_shape_invariants(r_prime):
    """
    Compute universal shape invariants I1, I2, I3.
    """
    d12 = np.linalg.norm(r_prime[0] - r_prime[1])
    d13 = np.linalg.norm(r_prime[0] - r_prime[2])
    d23 = np.linalg.norm(r_prime[1] - r_prime[2])
    
    distances = sorted([d12, d13, d23])
    d_short, d_mid, d_long = distances
    
    I1 = d_short / (d_long + 1e-10)
    I2 = d_mid / (d_long + 1e-10)
    I3 = (d_short + d_mid - d_long) / (d_short + d_mid + d_long + 1e-10)
    
    return I1, I2, I3

def compute_velocity_angles(r_prime, v_prime, eps=1e-10):
    """
    Compute angles between position and velocity vectors.
    """
    angles = []
    for i in range(2):
        r_norm = np.linalg.norm(r_prime[i])
        v_norm = np.linalg.norm(v_prime[i])
        
        if r_norm < eps or v_norm < eps:
            angle = np.pi / 2
        else:
            dot = np.dot(r_prime[i], v_prime[i])
            cross = np.cross(r_prime[i], v_prime[i])
            cross_norm = np.linalg.norm(cross)
            angle = np.arctan2(cross_norm, dot)
        
        angles.append(angle / np.pi)
    
    return tuple(angles)

def compute_13_component_vector(masses, r_prime, v_prime):
    """
    Compute the full 13-component IC vector.
    """
    # 1. Basic Invariants
    E, Q, s_min = compute_basic_invariants(masses, r_prime, v_prime)
    
    # 2. Angular Momentum
    _, L_norm, r_char, _ = compute_angular_momentum_canonical(masses, r_prime, v_prime, E)
    
    # 3. Shape Invariants
    I1, I2, I3 = compute_shape_invariants(r_prime)
    
    # 4. Velocity Angles
    theta1, theta2 = compute_velocity_angles(r_prime, v_prime)
    
    # 5. Moment of Inertia
    I_norm = compute_moment_of_inertia_normalized(masses, r_prime, r_char)
    
    # Normalization (hardcoded scales for now, ideally passed in)
    # Using defaults from pipeline
    E_scale = 1.0 # Placeholder
    Q_scale = 0.5
    smin_scale = 1.0 # Placeholder
    
    # Normalize components
    E_norm = np.tanh(E / E_scale)
    Q_norm = np.tanh((Q - 1) / Q_scale)
    smin_norm = np.tanh(s_min / smin_scale)
    
    m_total = np.sum(masses)
    m_norm = 2 * (masses / m_total) - 1
    
    I1_norm = 2 * I1 - 1
    I2_norm = 2 * I2 - 1
    
    theta_norm = 2 * np.array([theta1, theta2]) - 1
    I_norm_bounded = np.tanh(I_norm)
    L_norm_bounded = 2 * L_norm - 1
    
    vector = np.concatenate([
        m_norm,
        [E_norm],
        [L_norm_bounded],
        [Q_norm],
        [smin_norm],
        [I1_norm, I2_norm, I3],
        theta_norm,
        [I_norm_bounded]
    ])
    
    return vector
