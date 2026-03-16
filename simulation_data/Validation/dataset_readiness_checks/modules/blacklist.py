"""
Blacklist validation module.
"""

from pathlib import Path
from typing import List

from ..datastructures import ValidationIssue, ValidationStatus, create_issue
from ..config import config

def validate_against_blacklist(file_path: Path, variant: str, file_number: int) -> List[ValidationIssue]:
    """
    Check if a file should exist based on the blacklist.
    
    If a file exists but is blacklisted -> Error (should have been moved).
    """
    issues = []
    
    # Load blacklist
    blacklist = config.get_blacklist_ids()
    
    # Determine key for blacklist (hierarchical vs standard)
    # The blacklist json keys are 'hierarchical' and 'standard'
    # 'hierarchical_gold' likely uses 'hierarchical' blacklist? Or maybe it's separate?
    # Usually gold is a subset of standard/hierarchical runs, but might be re-run.
    # We will assume blacklist applies to the base type.
    
    blacklist_key = None
    if 'hierarchical' in variant:
        blacklist_key = 'hierarchical'
    elif 'standard' in variant:
        blacklist_key = 'standard'
        
    if blacklist_key and blacklist_key in blacklist:
        bad_ids = set(blacklist[blacklist_key])
        
        if file_number in bad_ids:
            issues.append(create_issue(
                "blacklisted_file_exists", ValidationStatus.ERROR, "blacklist",
                f"File {file_number} is in blacklist but exists in dataset", str(file_path)
            ))
            
    return issues
