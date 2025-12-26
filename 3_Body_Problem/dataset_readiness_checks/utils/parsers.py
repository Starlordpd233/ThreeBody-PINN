#!/usr/bin/env python3
"""
File parsing utilities for the Three-Body Problem database validation system.
"""

import re
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
import numpy as np


from ..datastructures import Snapshot, ResultFooter


def parse_ic_file(ic_path: Path) -> List[Tuple[float, ...]]:
    """
    Parse an IC (Initial Condition) file.

    Format: 3 lines, each with 7 values: m x y z vx vy vz
    Returns: List of 3 tuples, each containing (m, x, y, z, vx, vy, vz)
    """
    particles = []

    try:
        with open(ic_path, 'r') as f:
            lines = f.readlines()

        if len(lines) != 3:
            raise ValueError(f"Expected 3 lines, found {len(lines)}")

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                raise ValueError(f"Empty line {i+1}")

            parts = line.split()
            if len(parts) != 7:
                raise ValueError(f"Line {i+1}: Expected 7 values, found {len(parts)}")

            try:
                # Parse values as floats
                values = tuple(float(v) for v in parts)
                particles.append(values)

            except ValueError as e:
                raise ValueError(f"Line {i+1}: Invalid numeric value: {e}")

        return particles

    except Exception as e:
        raise ValueError(f"Failed to parse IC file {ic_path}: {e}")


def parse_brutus_file(brutus_path: Path) -> Tuple[List[Snapshot], Optional[ResultFooter]]:
    """
    Parse a Brutus output file.

    Returns: (list_of_snapshots, optional_result_footer)
    """
    snapshots = []
    result_footer = None

    try:
        with open(brutus_path, 'r') as f:
            lines = f.readlines()

        # Pattern for timestep header: [time] [N] [cpu_time]
        timestep_pattern = re.compile(r'^(\d+\.?\d*)\s+(\d+)\s+(\d+\.?\d*)')

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Skip empty lines
            if not line:
                i += 1
                continue

            # Check if it's a timestep header
            match = timestep_pattern.match(line)
            if match:
                time = float(match.group(1))
                n_bodies = int(match.group(2))
                t_cpu = float(match.group(3))

                # Next 3 lines should be particle data
                particles = []
                for j in range(1, 4):
                    if i + j >= len(lines):
                        # This might happen if the file is truncated right after header
                        break

                    particle_line = lines[i + j].strip()
                    parts = particle_line.split()

                    if len(parts) < 7:
                         # Likely truncated or malformed
                         break

                    try:
                        # Parse as floats
                        particle_data = tuple(float(v) for v in parts[:7])
                        particles.append(particle_data)

                    except ValueError:
                        break
                
                if len(particles) == 3:
                    snapshot = Snapshot(
                        time=time,
                        n_bodies=n_bodies,
                        t_cpu=t_cpu,
                        particles=particles
                    )
                    snapshots.append(snapshot)
                    i += 4
                else:
                    # Malformed snapshot, skip header and continue
                    i += 1

            # Check for Result footer
            elif line.startswith('Result:'):
                result_footer = parse_result_footer(line, i + 1)
                i += 1

            else:
                # Unknown line format, skip it
                i += 1

        return snapshots, result_footer

    except Exception as e:
        raise ValueError(f"Failed to parse Brutus file {brutus_path}: {e}")


def parse_result_footer(line: str, line_number: int) -> Optional[ResultFooter]:
    """
    Parse a Result: footer line from Brutus output.

    Format: Result: filename=... N=... t_begin=... t_end=... dt=... eta=... tol=... Lw=... t_cpu=... E_initial=... E_final=... dE/E=...
    """
    if not line.startswith('Result:'):
        return None

    try:
        # Extract key-value pairs
        # Remove "Result: " prefix
        content = line[8:]  # Skip "Result: "

        # FIX: Regex updated to include '/' in keys (for dE/E) and handle varied values
        # Matches key=value where key is [\w/]+ and value is [^\s]+
        pairs = re.findall(r'([\w/]+)=([^\s]+)', content)

        # Convert to dictionary
        data = {}
        for key, value in pairs:
            try:
                if value.isdigit():
                    data[key] = int(value)
                else:
                    # Try float (handles scientific notation too)
                    data[key] = float(value)
            except ValueError:
                data[key] = value

        # Create ResultFooter object
        footer = ResultFooter(
            filename=data.get('filename'),
            n=data.get('N'),
            t_begin=data.get('t_begin'),
            t_end=data.get('t_end'),
            dt=data.get('dt'),
            eta=data.get('eta'),
            tol=str(data.get('tol')) if data.get('tol') is not None else None,
            lw=data.get('Lw'),
            t_cpu=data.get('t_cpu'),
            e_initial=data.get('E_initial'),
            e_final=data.get('E_final'),
            de_e=data.get('dE/E'),
            line_number=line_number
        )

        return footer

    except Exception:
        return None


def calculate_energy(particles: List[Tuple[float, ...]]) -> float:
    """
    Calculate total energy from particle data.
    """
    kinetic = 0.0
    potential = 0.0

    # Kinetic energy
    for m, x, y, z, vx, vy, vz in particles:
        kinetic += 0.5 * m * (vx**2 + vy**2 + vz**2)

    # Potential energy
    n = len(particles)
    for i in range(n):
        for j in range(i + 1, n):
            m_i, x_i, y_i, z_i, _, _, _ = particles[i]
            m_j, x_j, y_j, z_j, _, _, _ = particles[j]

            dx = x_j - x_i
            dy = y_j - y_i
            dz = z_j - z_i
            distance = np.sqrt(dx**2 + dy**2 + dz**2)

            if distance > 0:
                potential -= m_i * m_j / distance

    return kinetic + potential


def calculate_center_of_mass(masses: List[float], positions: List[Tuple[float, float, float]]) -> Tuple[float, float, float]:
    """
    Calculate center of mass.
    """
    total_mass = sum(masses)
    if total_mass == 0:
        return 0.0, 0.0, 0.0
        
    com_x = sum(m * x for m, (x, y, z) in zip(masses, positions)) / total_mass
    com_y = sum(m * y for m, (x, y, z) in zip(masses, positions)) / total_mass
    com_z = sum(m * z for m, (x, y, z) in zip(masses, positions)) / total_mass
    return com_x, com_y, com_z


def calculate_total_momentum(masses: List[float], velocities: List[Tuple[float, float, float]]) -> Tuple[float, float, float]:
    """
    Calculate total momentum.
    """
    p_x = sum(m * vx for m, (vx, vy, vz) in zip(masses, velocities))
    p_y = sum(m * vy for m, (vx, vy, vz) in zip(masses, velocities))
    p_z = sum(m * vz for m, (vx, vy, vz) in zip(masses, velocities))
    return p_x, p_y, p_z


def calculate_angular_momentum(masses: List[float],
                              positions: List[Tuple[float, float, float]],
                              velocities: List[Tuple[float, float, float]]) -> Tuple[float, float, float]:
    """
    Calculate angular momentum.
    """
    L_x, L_y, L_z = 0.0, 0.0, 0.0

    for i, (m, (x, y, z), (vx, vy, vz)) in enumerate(zip(masses, positions, velocities)):
        # L = r × p = r × (mv))
        L_x += m * (y * vz - z * vy)
        L_y += m * (z * vx - x * vz)
        L_z += m * (x * vy - y * vx)

    return L_x, L_y, L_z
