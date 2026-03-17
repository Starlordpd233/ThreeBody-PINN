#!/usr/bin/env python3
"""
Audit and backfill Brutus Result: footers.

This script scans all Brutus output files to:
1. Identify missing Result: footers
2. Identify partial Result: footers (missing energy fields)
3. Validate existing energy values against trajectory data
4. Backfill missing/partial footers (with --apply flag)

Usage:
    python audit_and_backfill_brutus_result_footers.py              # Audit only (dry-run)
    python audit_and_backfill_brutus_result_footers.py --validate   # Audit + validate energy
    python audit_and_backfill_brutus_result_footers.py --apply      # Apply backfill
"""

import argparse
import glob
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class Snapshot:
    """Represents a single snapshot in a Brutus output file."""
    time: float
    n_bodies: int
    t_cpu: float
    particles: List[Tuple[float, ...]]  # List of (m, x, y, z, vx, vy, vz) tuples


@dataclass
class ResultFooter:
    """Represents a Result: footer line from Brutus output."""
    filename: Optional[str] = None
    n: Optional[int] = None
    t_begin: Optional[float] = None
    t_end: Optional[float] = None
    dt: Optional[float] = None
    eta: Optional[float] = None
    tol: Optional[str] = None
    lw: Optional[int] = None
    t_cpu: Optional[float] = None
    e_initial: Optional[float] = None
    e_final: Optional[float] = None
    de_e: Optional[float] = None
    line_number: Optional[int] = None

    def is_complete(self) -> bool:
        """Check if footer has all expected fields."""
        return all([
            self.filename is not None,
            self.n is not None,
            self.t_begin is not None,
            self.t_end is not None,
            self.dt is not None,
            self.e_initial is not None,
            self.e_final is not None,
            self.de_e is not None
        ])

    def missing_fields(self) -> List[str]:
        """Return list of missing field names."""
        missing = []
        if self.filename is None: missing.append('filename')
        if self.n is None: missing.append('N')
        if self.t_begin is None: missing.append('t_begin')
        if self.t_end is None: missing.append('t_end')
        if self.dt is None: missing.append('dt')
        if self.e_initial is None: missing.append('E_initial')
        if self.e_final is None: missing.append('E_final')
        if self.de_e is None: missing.append('dE/E')
        return missing


def calculate_energy(particles: List[Tuple[float, ...]]) -> float:
    """
    Calculate total energy from particle data.

    Each particle is (m, x, y, z, vx, vy, vz).
    Energy = Kinetic + Potential
    K = 0.5 * sum(m_i * v_i^2)
    U = -sum_{i<j} (m_i * m_j / r_ij)
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
            mi, xi, yi, zi = particles[i][:4]
            mj, xj, yj, zj = particles[j][:4]
            dx = xi - xj
            dy = yi - yj
            dz = zi - zj
            r = (dx**2 + dy**2 + dz**2)**0.5
            if r > 0:
                potential -= mi * mj / r

    return kinetic + potential


def parse_snapshot(lines: List[str], start_idx: int) -> Optional[Tuple[Snapshot, int]]:
    """
    Parse a single snapshot starting at start_idx.

    Returns (Snapshot, next_line_idx) or None if parsing fails.
    """
    if start_idx >= len(lines):
        return None

    # Parse header: time N t_cpu
    header_parts = lines[start_idx].strip().split()
    if len(header_parts) < 3:
        return None

    try:
        time = float(header_parts[0])
        n_bodies = int(header_parts[1])
        t_cpu = float(header_parts[2])
    except (ValueError, IndexError):
        return None

    # Parse particle lines
    particles = []
    current_idx = start_idx + 1
    for _ in range(n_bodies):
        if current_idx >= len(lines):
            return None

        parts = lines[current_idx].strip().split()
        if len(parts) < 7:
            return None

        try:
            particle = tuple(float(x) for x in parts[:7])
            particles.append(particle)
        except ValueError:
            return None

        current_idx += 1

    snapshot = Snapshot(time=time, n_bodies=n_bodies, t_cpu=t_cpu, particles=particles)

    # Skip empty line after snapshot (if present)
    if current_idx < len(lines) and lines[current_idx].strip() == '':
        current_idx += 1

    return snapshot, current_idx


def parse_result_footer(line: str, line_number: int) -> ResultFooter:
    """Parse a Result: footer line into a ResultFooter object."""
    footer = ResultFooter(line_number=line_number)

    # Extract fields using regex
    patterns = {
        'filename': r'filename=\s*(\S+)',
        'n': r'N=\s*(\d+)',
        't_begin': r't_begin=\s*([\d.e+-]+)',
        't_end': r't_end=\s*([\d.e+-]+)',
        'dt': r'dt=\s*([\d.e+-]+)',
        'eta': r'eta=\s*([\d.e+-]+)',
        'tol': r'tol=\s*(\S+)',
        'lw': r'Lw=\s*(\d+)',
        't_cpu': r't_cpu=\s*([\d.e+-]+)',
        'e_initial': r'E_initial=\s*([-\d.e+-]+)',
        'e_final': r'E_final=\s*([-\d.e+-]+)',
        'de_e': r'dE/E=\s*([-\d.e+-]+)',
    }

    for field, pattern in patterns.items():
        match = re.search(pattern, line)
        if match:
            value = match.group(1)
            if field == 'filename':
                footer.filename = value
            elif field == 'tol':
                footer.tol = value
            elif field in ['n', 'lw']:
                setattr(footer, field, int(value))
            else:
                setattr(footer, field, float(value))

    return footer


def read_brutus_file(filepath: str) -> Tuple[List[Snapshot], Optional[ResultFooter], List[str]]:
    """
    Read a Brutus output file and extract snapshots and Result footer.

    Returns:
        (snapshots, result_footer, all_lines)
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()

    snapshots = []
    result_footer = None

    # Check for Result: footer at the end
    for i in range(len(lines) - 1, max(len(lines) - 10, -1), -1):
        if lines[i].startswith('Result:'):
            result_footer = parse_result_footer(lines[i], i + 1)  # 1-indexed
            break

    # Parse snapshots
    idx = 0
    while idx < len(lines):
        # Skip Result: line and anything after
        if lines[idx].startswith('Result:'):
            break

        # Skip empty lines
        if not lines[idx].strip():
            idx += 1
            continue

        # Try to parse snapshot
        result = parse_snapshot(lines, idx)
        if result:
            snapshot, next_idx = result
            snapshots.append(snapshot)
            idx = next_idx
        else:
            idx += 1

    return snapshots, result_footer, lines


def infer_ic_path(output_filepath: str, folder_type: str) -> Optional[str]:
    """
    Infer the IC file path based on the output file path and folder type.

    folder_type: 'hierarchical', 'hierarchical_gold', 'standard', 'standard_gold'
    """
    base_dir = Path('<home>/Desktop/3_body_problem/simulation_data/Data/ic_final')

    # Extract file number from brutus output filename
    basename = os.path.basename(output_filepath)
    match = re.search(r'_(hierarchical|standard)_(\d+)\.txt$', basename)
    if not match:
        return None

    file_num = match.group(2)

    # Map folder type to IC directory
    ic_dir_map = {
        'hierarchical': 'ic_hierarchical',
        'hierarchical_gold': 'ic_hierarchical_for_gold_standard',
        'standard': 'ic_standard_quasi_random',
        'standard_gold': 'ic_standard_quasi_random'  # Try both standard and standard_gold
    }

    ic_dir = base_dir / ic_dir_map[folder_type]
    ic_filename = f"ic_{match.group(1)}_{file_num}.txt"
    ic_path = ic_dir / ic_filename

    if ic_path.exists():
        return str(ic_path)

    # For standard_gold, also try the gold-standard specific directory
    if folder_type == 'standard_gold':
        ic_dir_gold = base_dir / 'ic_standard_quasi_random_for_gold_standard'
        ic_path_gold = ic_dir_gold / ic_filename
        if ic_path_gold.exists():
            return str(ic_path_gold)

    return None


def get_folder_type(filepath: str) -> Optional[str]:
    """Determine folder type from filepath."""
    if 'brutus_hierarchical_gold_standard' in filepath:
        return 'hierarchical_gold'
    elif 'brutus_hierarchical' in filepath:
        return 'hierarchical'
    elif 'brutus_standard_quasi_random_gold_standard' in filepath:
        return 'standard_gold'
    elif 'brutus_standard_quasi_random' in filepath:
        return 'standard'
    return None


def get_folder_defaults(folder_type: str) -> Dict[str, any]:
    """
    Get default parameters for each folder type.

    Returns dict with 'tol', 'lw', 'dt', 'eta' keys.
    Note: eta is derived from tol in Brutus code, but we include known values.
    """
    defaults = {
        'hierarchical': {
            'tol': '1e-15',
            'lw': 130,
            'dt': 0.08,
            'eta': None  # Will be computed if needed
        },
        'hierarchical_gold': {
            'tol': '1e-13',
            'lw': 130,
            'dt': 0.01,
            'eta': None
        },
        'standard': {
            'tol': '1e-13',
            'lw': 118,
            'dt': 0.17,
            'eta': None
        },
        'standard_gold': {
            # Special case: omit tol and eta for missing footers
            'tol': None,
            'lw': 130,
            'dt': 0.01,
            'eta': None
        }
    }

    return defaults.get(folder_type, {})


def format_footer_line(footer_data: Dict[str, any], folder_type: str) -> str:
    """
    Format a Result: footer line from footer_data dict.

    Omits tol/eta for standard_gold missing footers as specified.
    """
    parts = ["Result:"]

    # Always include these if available
    if 'filename' in footer_data and footer_data['filename']:
        parts.append(f"filename= {footer_data['filename']}")
    if 'n' in footer_data:
        parts.append(f"N= {footer_data['n']}")
    if 't_begin' in footer_data:
        parts.append(f"t_begin= {footer_data['t_begin']}")
    if 't_end' in footer_data:
        parts.append(f"t_end= {footer_data['t_end']}")
    if 'dt' in footer_data:
        parts.append(f"dt= {footer_data['dt']}")

    # Include eta/tol/Lw only if not standard_gold with missing footer
    # (The plan says to omit tol/eta for the 219 standard_gold missing-footers)
    if folder_type != 'standard_gold' or footer_data.get('_existing_footer', False):
        if 'eta' in footer_data and footer_data['eta'] is not None:
            parts.append(f"eta= {footer_data['eta']}")
        if 'tol' in footer_data and footer_data['tol'] is not None:
            parts.append(f"tol= {footer_data['tol']}")

    if 'lw' in footer_data and footer_data['lw'] is not None:
        parts.append(f"Lw= {footer_data['lw']}")
    if 't_cpu' in footer_data:
        parts.append(f"t_cpu= {footer_data['t_cpu']}")

    # Energy fields (always include if available)
    if 'e_initial' in footer_data:
        parts.append(f"E_initial= {footer_data['e_initial']}")
    if 'e_final' in footer_data:
        parts.append(f"E_final= {footer_data['e_final']}")
    if 'de_e' in footer_data:
        parts.append(f"dE/E= {footer_data['de_e']}")

    return ' '.join(parts)


def audit_file(filepath: str, validate: bool = False) -> Dict[str, any]:
    """
    Audit a single Brutus output file.

    Returns dict with audit results:
        - has_footer: bool
        - footer_complete: bool (if has_footer)
        - missing_fields: list of field names (if incomplete)
        - energy_valid: bool or None (if validate=True)
        - energy_mismatch: dict or None (if validation failed)
        - snapshots_count: int
        - first_snapshot: Snapshot or None
        - last_snapshot: Snapshot or None
        - footer: ResultFooter or None
        - lines: list of all lines
    """
    try:
        snapshots, footer, lines = read_brutus_file(filepath)
    except Exception as e:
        return {
            'error': str(e),
            'has_footer': False,
            'footer_complete': False,
            'snapshots_count': 0
        }

    result = {
        'has_footer': footer is not None,
        'footer_complete': footer.is_complete() if footer else False,
        'missing_fields': footer.missing_fields() if footer else [],
        'snapshots_count': len(snapshots),
        'first_snapshot': snapshots[0] if snapshots else None,
        'last_snapshot': snapshots[-1] if snapshots else None,
        'footer': footer,
        'lines': lines,
        'energy_valid': None,
        'energy_mismatch': None
    }

    # Validate energy if requested and footer has energy fields
    if validate and footer and footer.e_initial is not None and footer.e_final is not None:
        if snapshots:
            first_energy = calculate_energy(snapshots[0].particles)
            last_energy = calculate_energy(snapshots[-1].particles)

            # Compare with footer values (allow small tolerance for floating point)
            e_init_match = abs(first_energy - footer.e_initial) / abs(footer.e_initial) < 1e-6
            e_final_match = abs(last_energy - footer.e_final) / abs(footer.e_final) < 1e-6

            result['energy_valid'] = e_init_match and e_final_match

            if not result['energy_valid']:
                result['energy_mismatch'] = {
                    'footer_e_initial': footer.e_initial,
                    'computed_e_initial': first_energy,
                    'footer_e_final': footer.e_final,
                    'computed_e_final': last_energy
                }

    return result


def generate_audit_report(audit_results: Dict[str, Dict[str, any]], output_path: str):
    """Generate a markdown audit report."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    with open(output_path, 'w') as f:
        f.write(f"# Brutus Result Footer Audit Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Summary by folder
        folders = {}
        for filepath, result in audit_results.items():
            folder = os.path.basename(os.path.dirname(filepath))
            if folder not in folders:
                folders[folder] = {
                    'total': 0,
                    'missing': 0,
                    'partial': 0,
                    'complete': 0,
                    'energy_invalid': 0
                }

            folders[folder]['total'] += 1

            if not result['has_footer']:
                folders[folder]['missing'] += 1
            elif not result['footer_complete']:
                folders[folder]['partial'] += 1
            else:
                folders[folder]['complete'] += 1

            if result.get('energy_valid') == False:
                folders[folder]['energy_invalid'] += 1

        f.write("## Summary by Folder\n\n")
        f.write("| Folder | Total | Missing Footer | Partial Footer | Complete | Energy Invalid |\n")
        f.write("|--------|-------|----------------|----------------|----------|----------------|\n")

        for folder, stats in sorted(folders.items()):
            if folder == 'check missing results line':
                continue
            f.write(f"| {folder} | {stats['total']} | {stats['missing']} | {stats['partial']} | {stats['complete']} | {stats['energy_invalid']} |\n")

        # Detailed listings
        f.write("\n## Detailed Findings\n\n")

        for folder in sorted(folders.keys()):
            if folder == 'check missing results line':
                continue

            f.write(f"### {folder}\n\n")

            # Missing footers
            missing_files = [fp for fp, res in audit_results.items()
                           if os.path.basename(os.path.dirname(fp)) == folder and not res['has_footer']]

            if missing_files:
                f.write(f"**Missing Result footer ({len(missing_files)} files):**\n\n")
                for fp in sorted(missing_files)[:50]:  # Limit to first 50
                    basename = os.path.basename(fp)
                    f.write(f"- `@{basename}` (missing Result footer)\n")
                if len(missing_files) > 50:
                    f.write(f"- ... and {len(missing_files) - 50} more\n")
                f.write("\n")

            # Partial footers
            partial_files = [(fp, res) for fp, res in audit_results.items()
                           if os.path.basename(os.path.dirname(fp)) == folder
                           and res['has_footer'] and not res['footer_complete']]

            if partial_files:
                f.write(f"**Partial Result footer ({len(partial_files)} files):**\n\n")
                for fp, res in sorted(partial_files, key=lambda x: x[0])[:20]:
                    basename = os.path.basename(fp)
                    missing = ', '.join(res['missing_fields'])
                    line_num = res['footer'].line_number if res['footer'] else '?'
                    f.write(f"- `@{basename}` (line {line_num}, missing: {missing})\n")
                if len(partial_files) > 20:
                    f.write(f"- ... and {len(partial_files) - 20} more\n")
                f.write("\n")

            # Energy validation failures
            energy_invalid = [(fp, res) for fp, res in audit_results.items()
                            if os.path.basename(os.path.dirname(fp)) == folder
                            and res.get('energy_valid') == False]

            if energy_invalid:
                f.write(f"**Energy validation failed ({len(energy_invalid)} files):**\n\n")
                for fp, res in sorted(energy_invalid, key=lambda x: x[0])[:10]:
                    basename = os.path.basename(fp)
                    mismatch = res['energy_mismatch']
                    f.write(f"- `@{basename}`:\n")
                    f.write(f"  - E_initial: footer={mismatch['footer_e_initial']:.6g}, computed={mismatch['computed_e_initial']:.6g}\n")
                    f.write(f"  - E_final: footer={mismatch['footer_e_final']:.6g}, computed={mismatch['computed_e_final']:.6g}\n")
                if len(energy_invalid) > 10:
                    f.write(f"- ... and {len(energy_invalid) - 10} more\n")
                f.write("\n")

    print(f"Audit report written to: {output_path}")


def backfill_file(filepath: str, audit_result: Dict[str, any], apply: bool = False) -> bool:
    """
    Backfill missing or partial Result footer in a file.

    Returns True if backfill was performed (or would be performed if apply=True).
    """
    if audit_result.get('error'):
        return False

    # Skip if footer is already complete
    if audit_result['has_footer'] and audit_result['footer_complete']:
        return False

    snapshots = []
    if audit_result['first_snapshot']:
        snapshots.append(audit_result['first_snapshot'])
    if audit_result['last_snapshot'] and audit_result['last_snapshot'] != audit_result['first_snapshot']:
        snapshots.append(audit_result['last_snapshot'])

    if not snapshots:
        print(f"Warning: No snapshots found in {filepath}, skipping backfill")
        return False

    first_snap = audit_result['first_snapshot']
    last_snap = audit_result['last_snapshot']

    # Calculate energies
    e_initial = calculate_energy(first_snap.particles)
    e_final = calculate_energy(last_snap.particles)
    de_e = abs((e_final - e_initial) / e_initial) if e_initial != 0 else 0.0

    # Determine folder type and defaults
    folder_type = get_folder_type(filepath)
    defaults = get_folder_defaults(folder_type) if folder_type else {}

    # Build footer data
    footer_data = {}

    # If partial footer exists, preserve existing fields
    if audit_result['has_footer']:
        footer = audit_result['footer']
        footer_data['_existing_footer'] = True
        if footer.filename: footer_data['filename'] = footer.filename
        if footer.n: footer_data['n'] = footer.n
        if footer.t_begin is not None: footer_data['t_begin'] = footer.t_begin
        if footer.t_end is not None: footer_data['t_end'] = footer.t_end
        if footer.dt is not None: footer_data['dt'] = footer.dt
        if footer.eta is not None: footer_data['eta'] = footer.eta
        if footer.tol: footer_data['tol'] = footer.tol
        if footer.lw: footer_data['lw'] = footer.lw
        if footer.t_cpu is not None: footer_data['t_cpu'] = footer.t_cpu
    else:
        # No footer exists, infer fields
        footer_data['_existing_footer'] = False
        footer_data['n'] = first_snap.n_bodies
        footer_data['t_begin'] = first_snap.time
        footer_data['t_end'] = last_snap.time
        footer_data['t_cpu'] = last_snap.t_cpu

        # Try to infer IC path
        ic_path = infer_ic_path(filepath, folder_type)
        if ic_path:
            footer_data['filename'] = ic_path

        # Add defaults (respecting standard_gold special case)
        if folder_type and defaults:
            if defaults.get('tol') and folder_type != 'standard_gold':
                footer_data['tol'] = defaults['tol']
            if defaults.get('lw'):
                footer_data['lw'] = defaults['lw']
            if defaults.get('dt'):
                footer_data['dt'] = defaults['dt']
            if defaults.get('eta'):
                footer_data['eta'] = defaults['eta']

    # Always add/update energy fields
    footer_data['e_initial'] = e_initial
    footer_data['e_final'] = e_final
    footer_data['de_e'] = de_e

    # Format the footer line
    new_footer_line = format_footer_line(footer_data, folder_type)

    if not apply:
        print(f"Would backfill: {os.path.basename(filepath)}")
        print(f"  New footer: {new_footer_line}")
        return True

    # Apply the backfill
    lines = audit_result['lines']

    if audit_result['has_footer']:
        # Replace existing partial footer
        footer_line_idx = audit_result['footer'].line_number - 1  # Convert to 0-indexed
        lines[footer_line_idx] = new_footer_line + '\n'
        action = "replaced partial"
    else:
        # Append new footer
        # Make sure file ends with newline before footer
        if lines and not lines[-1].endswith('\n'):
            lines[-1] += '\n'
        lines.append(new_footer_line + '\n')
        action = "added missing"

    # Write back to file
    with open(filepath, 'w') as f:
        f.writelines(lines)

    print(f"Backfilled ({action}): {os.path.basename(filepath)}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Audit and backfill Brutus Result: footers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--validate', action='store_true',
                       help='Validate existing energy values against trajectory data')
    parser.add_argument('--apply', action='store_true',
                       help='Apply backfill (modify files in-place)')
    parser.add_argument('--output-dir', default=None,
                       help='Output directory for reports (default: brutus_output/check missing results line/)')

    args = parser.parse_args()

    # Find all Brutus output files
    base_dir = '<home>/Desktop/3_body_problem/simulation_data/Data/brutus_output'
    patterns = [
        f'{base_dir}/brutus_hierarchical/brutus_*.txt',
        f'{base_dir}/brutus_hierarchical_gold_standard/brutus_*.txt',
        f'{base_dir}/brutus_standard_quasi_random/brutus_*.txt',
        f'{base_dir}/brutus_standard_quasi_random_gold_standard/brutus_*.txt',
    ]

    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern))

    print(f"Found {len(files)} Brutus output files")
    sys.stdout.flush()

    # Audit all files
    print("\nAuditing files...")
    sys.stdout.flush()
    audit_results = {}
    for i, filepath in enumerate(files, 1):
        if i % 500 == 0:
            print(f"  Progress: {i}/{len(files)} ({100*i/len(files):.1f}%)")
            sys.stdout.flush()
        audit_results[filepath] = audit_file(filepath, validate=args.validate)

    print(f"  Completed: {len(files)}/{len(files)} (100.0%)")
    sys.stdout.flush()

    # Generate report
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path(base_dir) / 'check missing results line'

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = output_dir / f'footer_audit_{timestamp}.md'

    generate_audit_report(audit_results, str(report_path))

    # Backfill if requested
    if args.apply or not args.apply:  # Always show what would be backfilled
        print("\n" + ("Backfilling files..." if args.apply else "Dry-run (use --apply to modify files):"))
        backfill_count = 0

        for filepath, result in audit_results.items():
            if backfill_file(filepath, result, apply=args.apply):
                backfill_count += 1

        print(f"\n{'Backfilled' if args.apply else 'Would backfill'}: {backfill_count} files")

        if args.apply:
            print("\nRe-running audit to verify backfill...")
            # Re-audit
            audit_results_post = {}
            for filepath in files:
                audit_results_post[filepath] = audit_file(filepath, validate=False)

            report_path_post = output_dir / f'footer_audit_post_backfill_{timestamp}.md'
            generate_audit_report(audit_results_post, str(report_path_post))
            print(f"\nPost-backfill audit report: {report_path_post}")


if __name__ == '__main__':
    main()
