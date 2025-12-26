"""
Metadata validation module.
"""

from pathlib import Path
from typing import List
import os

from ..datastructures import ValidationIssue, ValidationStatus, create_issue
from ..utils.parsers import parse_result_footer

def validate_metadata(file_path: Path, variant: str) -> List[ValidationIssue]:
    """
    Validate metadata in Brutus output files (Result footer).
    """
    issues = []
    
    try:
        # We need to find the Result line. It's usually at the end.
        # Fast scan again.
        file_size = os.path.getsize(file_path)
        if file_size == 0:
             return [] # Handled by completeness
             
        with open(file_path, 'rb') as f:
            read_size = min(4096, file_size)
            f.seek(-read_size, 2)
            content = f.read().decode('utf-8', errors='ignore')
            lines = content.splitlines()
            
        footer_line = None
        for line in reversed(lines):
            if line.startswith('Result:'):
                footer_line = line
                break
                
        if footer_line:
            footer = parse_result_footer(footer_line, 0)
            if footer:
                # Check consistency
                if footer.n != 3:
                    issues.append(create_issue(
                        "metadata_n_mismatch", ValidationStatus.ERROR, "metadata",
                        f"Result footer says N={footer.n}, expected 3", str(file_path)
                    ))
                
                # Check if energy is populated
                if footer.e_initial is None or footer.e_final is None:
                     issues.append(create_issue(
                        "metadata_missing_energy", ValidationStatus.WARNING, "metadata",
                        "Result footer missing energy values", str(file_path)
                    ))
            else:
                 issues.append(create_issue(
                    "metadata_parse_error", ValidationStatus.WARNING, "metadata",
                    "Found 'Result:' line but failed to parse it", str(file_path)
                ))
        else:
            # Missing footer is a known issue for some files, strictly it's a warning/error depending on strictness
            # We'll mark as warning.
            issues.append(create_issue(
                "missing_result_footer", ValidationStatus.WARNING, "metadata",
                "No 'Result:' footer line found", str(file_path)
            ))
            
    except Exception as e:
        issues.append(create_issue(
            "metadata_check_error", ValidationStatus.ERROR, "metadata",
            f"Error checking metadata: {str(e)}", str(file_path)
        ))
        
    return issues
