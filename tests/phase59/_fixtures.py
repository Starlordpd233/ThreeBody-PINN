"""Closed-form orbits for the Phase 59 scorer. Numpy only.

``dual_frame`` reuses the Phase 46 Lagrange dual-frame wrapper. This module
does not import ``pinn.verification``: the vis-viva expectation added in
task 2 stays independent of the scorer's Hamiltonian.
"""

from __future__ import annotations

import numpy as np

from tests.phase46._fixtures import make_dual_frame_trajectory


def _equilateral_offsets(masses, side: float) -> tuple[np.ndarray, float]:
    """Equilateral vertices of side ``side`` with the mass-weighted COM at 0.

    Returns the body offsets ``(3, 3)`` and ``omega`` where
    ``omega**2 = M / side**3`` (G = 1).
    """
    masses = np.asarray(masses, dtype=np.float64)
    total_mass = float(masses.sum())
    omega = float(np.sqrt(total_mass / float(side) ** 3))
    circumradius = float(side) / np.sqrt(3.0)
    phi = np.array([0.0, 2.0 * np.pi / 3.0, 4.0 * np.pi / 3.0], dtype=np.float64)
    vertices = np.stack(
        [circumradius * np.cos(phi), circumradius * np.sin(phi), np.zeros(3)],
        axis=-1,
    )
    com = (masses.reshape(3, 1) * vertices).sum(axis=0) / total_mass
    return vertices - com, omega


def lagrange_rotation(times, masses=(1.0, 0.8, 0.6), side=1.0):
    """Rigid equilateral rotation at arbitrary ``times``.

    Returns ``(positions, velocities, omega)``. The centre of mass stays at
    the origin. ``omega**2 = M / side**3``.
    """
    offsets, omega = _equilateral_offsets(masses, side)
    time_array = np.asarray(times, dtype=np.float64).reshape(-1)
    theta = omega * time_array
    cosine = np.cos(theta)
    sine = np.sin(theta)
    positions = np.empty((time_array.shape[0], 3, 3), dtype=np.float64)
    velocities = np.empty((time_array.shape[0], 3, 3), dtype=np.float64)
    for index in range(time_array.shape[0]):
        rotation = np.array(
            [
                [cosine[index], -sine[index], 0.0],
                [sine[index], cosine[index], 0.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=np.float64,
        )
        positions[index] = offsets @ rotation.T
        velocities[index, :, 0] = -omega * positions[index, :, 1]
        velocities[index, :, 1] = omega * positions[index, :, 0]
        velocities[index, :, 2] = 0.0
    return positions, velocities, omega


def hierarchical_circular(times, masses=(1.0, 0.8, 0.6), a_in=0.1, a_out=1.0):
    """Circular inner pair (bodies 0 and 1) plus a circular outer body.

    ``omega_in = sqrt((m0 + m1) / a_in**3)`` and
    ``omega_out = sqrt(M / a_out**3)``. Body 2 orbits the inner centre of
    mass at separation ``a_out``. The system centre of mass is the origin.
    Returns ``(positions, velocities)``. The inner pair is ``(0, 1)``.
    """
    masses = np.asarray(masses, dtype=np.float64)
    time_array = np.asarray(times, dtype=np.float64).reshape(-1)
    m0, m1, m2 = (float(masses[0]), float(masses[1]), float(masses[2]))
    total = m0 + m1 + m2
    inner = m0 + m1
    omega_in = float(np.sqrt(inner / float(a_in) ** 3))
    omega_out = float(np.sqrt(total / float(a_out) ** 3))
    theta_in = omega_in * time_array
    theta_out = omega_out * time_array
    zeros = np.zeros_like(time_array)
    separation = float(a_in) * np.stack(
        [np.cos(theta_in), np.sin(theta_in), zeros], axis=-1
    )
    outer = float(a_out) * np.stack(
        [np.cos(theta_out), np.sin(theta_out), zeros], axis=-1
    )
    separation_dot = omega_in * float(a_in) * np.stack(
        [-np.sin(theta_in), np.cos(theta_in), zeros], axis=-1
    )
    outer_dot = omega_out * float(a_out) * np.stack(
        [-np.sin(theta_out), np.cos(theta_out), zeros], axis=-1
    )
    inner_com = -(m2 / total) * outer
    inner_com_dot = -(m2 / total) * outer_dot
    r0 = inner_com - (m1 / inner) * separation
    r1 = inner_com + (m0 / inner) * separation
    r2 = inner_com + outer
    v0 = inner_com_dot - (m1 / inner) * separation_dot
    v1 = inner_com_dot + (m0 / inner) * separation_dot
    v2 = inner_com_dot + outer_dot
    positions = np.stack([r0, r1, r2], axis=1)
    velocities = np.stack([v0, v1, v2], axis=1)
    return positions, velocities


def dual_frame(**kw):
    """One Lagrange trajectory in the raw frame and the locked scaled frame."""
    return make_dual_frame_trajectory(**kw)


def eccentric_homographic(
    masses=(1.0, 0.8, 0.6),
    e=0.5,
    side=1.0,
    a=1.0,
    n_samples=1001,
    n_periods=1.5,
):
    """Exact Lagrange homographic solution with one eccentric scale factor.

    Equilateral vertices ``c_i`` have side ``side`` and centre of mass 0.
    The complex scale ``z`` is the Keplerian orbit of parameter
    ``mu_eff = M / side**3``. Exact because the equilateral net force on
    body i is ``-M r_i / L**3``.

    Returns times, positions, velocities, masses, vis-viva kinetic energy
    ``K(t)``, and ``H0 = K(0) + V(0)``.
    """
    masses = np.asarray(masses, dtype=np.float64)
    total_mass = float(masses.sum())
    mu_eff = total_mass / float(side) ** 3
    mean_motion = float(np.sqrt(mu_eff / float(a) ** 3))
    anomaly = np.linspace(
        0.0, 2.0 * np.pi * float(n_periods), int(n_samples), dtype=np.float64
    )
    eccentricity = float(e)
    times = (anomaly - eccentricity * np.sin(anomaly)) / mean_motion
    z_real = float(a) * (np.cos(anomaly) - eccentricity)
    z_imag = float(a) * np.sqrt(1.0 - eccentricity**2) * np.sin(anomaly)
    denom = 1.0 - eccentricity * np.cos(anomaly)
    zdot_real = (-float(a) * np.sin(anomaly)) * mean_motion / denom
    zdot_imag = (
        float(a) * np.sqrt(1.0 - eccentricity**2) * np.cos(anomaly) * mean_motion / denom
    )
    offsets, _omega = _equilateral_offsets(masses, side)
    centre_x = offsets[:, 0]
    centre_y = offsets[:, 1]
    positions = np.empty((times.shape[0], 3, 3), dtype=np.float64)
    velocities = np.empty_like(positions)
    positions[:, :, 0] = z_real[:, None] * centre_x - z_imag[:, None] * centre_y
    positions[:, :, 1] = z_real[:, None] * centre_y + z_imag[:, None] * centre_x
    positions[:, :, 2] = 0.0
    velocities[:, :, 0] = zdot_real[:, None] * centre_x - zdot_imag[:, None] * centre_y
    velocities[:, :, 1] = zdot_real[:, None] * centre_y + zdot_imag[:, None] * centre_x
    velocities[:, :, 2] = 0.0
    centre_norm_sq = np.sum(offsets[:, :2] ** 2, axis=-1)
    z_abs = np.sqrt(z_real**2 + z_imag**2)
    kinetic = (
        0.5
        * float(np.sum(masses * centre_norm_sq))
        * mu_eff
        * (2.0 / z_abs - 1.0 / float(a))
    )
    pair_mass = (
        masses[0] * masses[1] + masses[0] * masses[2] + masses[1] * masses[2]
    )
    potential0 = -float(pair_mass) / (float(side) * float(z_abs[0]))
    h0 = float(kinetic[0] + potential0)
    return times, positions, velocities, masses, kinetic, h0


def expected_eps_h_velocity_scaling(kinetic, h0, kappa):
    """Vis-viva ``eps_H`` for velocities scaled by ``kappa``. Independent of the scorer."""
    kinetic = np.asarray(kinetic, dtype=np.float64)
    factor = float(kappa) ** 2 - 1.0
    numerator = abs(factor) * float(np.max(np.abs(kinetic - kinetic[0])))
    denominator = abs(factor * float(kinetic[0]) + float(h0))
    return numerator / denominator


def rotate_inner_pair(positions, masses, inner_pair, phi):
    """Rotate the inner separation by ``phi`` about z, keeping its centre of mass."""
    predicted = np.array(positions, dtype=np.float64, copy=True)
    masses = np.asarray(masses, dtype=np.float64)
    a, b = (int(inner_pair[0]), int(inner_pair[1]))
    ra = predicted[:, a, :]
    rb = predicted[:, b, :]
    inner_mass = float(masses[a] + masses[b])
    centre = (float(masses[a]) * ra + float(masses[b]) * rb) / inner_mass
    separation = rb - ra
    cosine = float(np.cos(phi))
    sine = float(np.sin(phi))
    rotated = np.empty_like(separation)
    rotated[:, 0] = cosine * separation[:, 0] - sine * separation[:, 1]
    rotated[:, 1] = sine * separation[:, 0] + cosine * separation[:, 1]
    rotated[:, 2] = separation[:, 2]
    predicted[:, a, :] = centre - (float(masses[b]) / inner_mass) * rotated
    predicted[:, b, :] = centre + (float(masses[a]) / inner_mass) * rotated
    return predicted
