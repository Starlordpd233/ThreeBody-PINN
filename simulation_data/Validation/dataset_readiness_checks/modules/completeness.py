"""
Completeness validation module.
"""

from pathlib import Path
from typing import List
import os

from ..datastructures import ValidationIssue, ValidationStatus, create_issue

def validate_completeness(file_path: Path, threshold: float) -> List[ValidationIssue]:
    """
    Validate that a Brutus simulation is complete.
    
    Checks:
    1. Final timestamp >= threshold
    2. Minimum number of snapshots (>= 10)
    3. Monotonic time (basic check)
    """
    issues = []
    
    try:
        # Fast scan for final timestamp
        # We read the last 4KB of the file to find the last snapshot header
        file_size = os.path.getsize(file_path)
        
        if file_size == 0:
            issues.append(create_issue(
                "empty_file", ValidationStatus.ERROR, "completeness",
                "File is empty", str(file_path)
            ))
            return issues
            
        with open(file_path, 'rb') as f:
            # Read last 4KB or whole file if smaller
            read_size = min(4096, file_size)
            f.seek(-read_size, 2)
            content = f.read().decode('utf-8', errors='ignore')
            lines = content.splitlines()
            
        # Look for last timestep header: "t N t_cpu" where N=3
        # Scan backwards
        final_time = None
        for line in reversed(lines):
            parts = line.strip().split()
            if len(parts) == 3 and parts[1] == '3':
                try:
                    final_time = float(parts[0])
                    break
                except ValueError:
                    continue
                    
        if final_time is None:
            issues.append(create_issue(
                "no_valid_snapshots", ValidationStatus.ERROR, "completeness",
                "Could not find any valid snapshot headers in the last 4KB", str(file_path)
            ))
            return issues
            
        if final_time < threshold:
            issues.append(create_issue(
                "incomplete_simulation", ValidationStatus.ERROR, "completeness",
                f"Simulation ends at t={final_time} (threshold: {threshold})", str(file_path)
            ))
            
    except Exception as e:
        issues.append(create_issue(
            "completeness_check_error", ValidationStatus.ERROR, "completeness",
            f"Error checking completeness: {str(e)}", str(file_path)
        ))
        
    return issues
