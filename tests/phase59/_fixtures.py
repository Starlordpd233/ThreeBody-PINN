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
