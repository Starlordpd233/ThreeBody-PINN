#!/usr/bin/env python3
"""
Filename pattern handling utilities for the Three-Body Problem database validation system.

Handles naming inconsistencies between directory names and actual filenames.
"""

import re
import glob
from pathlib import Path
from typing import Set, Optional, Dict, Any, List
import os

from ..config import config


def extract_file_numbers(directory: Path, variant: str, file_type: str = 'both') -> Set[int]:
    """
    Extract numeric IDs from filenames in a directory.

    Args:
        directory: Directory to scan
        variant: Dataset variant name (e.g., 'hierarchical', 'hierarchical_gold')
        file_type: 'ic', 'brutus', or 'both' (determines which pattern to use)

    Returns:
        Set of extracted numeric IDs
    """
    numbers = set()

    if file_type in ['ic', 'both']:
        pattern = config.get_ic_pattern(variant)
        prefix = pattern.split('{')[0]  # Get part before placeholder
        suffix = pattern.split('}')[-1] if '}' in pattern else ''
        
        # FIX: Ensure we don't accidentally double-underscore if prefix ends in _
        # If prefix ends with _, we don't need to add another _ in the glob
        # But actually, simpler is to just append * to the prefix directly.
        # Original bug: f"{prefix}_*{suffix}" -> "ic_hierarchical__*.txt"
        # Correct: f"{prefix}*{suffix}" -> "ic_hierarchical_*.txt"
        
        glob_pattern = f"{prefix}*{suffix}"
        full_pattern = directory / glob_pattern

        for filepath in glob.glob(str(full_pattern)):
            filename = Path(filepath).name
            # Extract number using regex
            match = re.search(r'_(\d+)\.txt$', filename)
            if match:
                try:
                    numbers.add(int(match.group(1)))
                except ValueError:
                    pass  # Skip invalid numbers

    if file_type in ['brutus', 'both']:
        pattern = config.get_brutus_pattern(variant)
        prefix = pattern.split('{')[0]
        suffix = pattern.split('}')[-1] if '}' in pattern else ''

        glob_pattern = f"{prefix}*{suffix}"
        full_pattern = directory / glob_pattern

        for filepath in glob.glob(str(full_pattern)):
            filename = Path(filepath).name
            match = re.search(r'_(\d+)\.txt$', filename)
            if match:
                try:
                    numbers.add(int(match.group(1)))
                except ValueError:
                    pass

    return numbers


def get_filename_pattern(variant: str, file_type: str) -> str:
    """
    Get the filename pattern for a given variant and file type.

    Returns:
        Filename pattern string
    """
    if file_type == 'ic':
        return config.get_ic_pattern(variant)
    elif file_type == 'brutus':
        return config.get_brutus_pattern(variant)
    else:
        raise ValueError(f"Invalid file_type: {file_type}")


def generate_filename(variant: str, file_type: str, file_number: int) -> str:
    """
    Generate a filename for a given variant, file type, and file number.

    Args:
        variant: Dataset variant name
        file_type: 'ic' or 'brutus'
        file_number: Numeric ID

    Returns:
        Generated filename
    """
    pattern = get_filename_pattern(variant, file_type)
    return pattern.format(num=file_number)


def validate_filename_pattern(variant: str, file_type: str, filename: str) -> Optional[int]:
    """
    Validate a filename against the expected pattern for a variant and file type.

    Args:
        variant: Dataset variant name
        file_type: 'ic' or 'brutus'
        filename: Filename to validate

    Returns:
        Extracted file number if valid, None otherwise
    """
    pattern = get_filename_pattern(variant, file_type)
    prefix = pattern.split('{')[0]

    # Check if filename starts with expected prefix
    if not filename.startswith(prefix):
        return None

    # Extract number using regex
    match = re.search(r'_(\d+)\.txt$', filename)
    if not match:
        return None

    try:
        return int(match.group(1))
    except ValueError:
        return None


def list_matching_files(directory: Path, variant: str, file_type: str) -> List[Path]:
    """
    List all files matching the expected pattern for a variant and file type.

    Args:
        directory: Directory to scan
        variant: Dataset variant name
        file_type: 'ic' or 'brutus'

    Returns:
        List of matching file paths
    """
    pattern = get_filename_pattern(variant, file_type)
    prefix = pattern.split('{')[0]
    suffix = pattern.split('}')[-1] if '}' in pattern else ''

    glob_pattern = f"{prefix}*{suffix}"
    full_pattern = directory / glob_pattern

    matching_files = []
    for filepath in glob.glob(str(full_pattern)):
        path = Path(filepath)
        # Double-check that it matches the pattern
        if path.name.startswith(prefix) and path.name.endswith(suffix):
            matching_files.append(path)

    return matching_files


def map_directory_to_variant(directory_name: str) -> Optional[str]:
    """
    Map a directory name to a standardized variant name.
    """
    # Map directory names to variant names
    directory_mapping = {
        'ic_hierarchical': 'hierarchical',
        'ic_hierarchical_for_gold_standard': 'hierarchical_gold',
        'ic_standard_quasi_random': 'standard',
        'ic_standard_quasi_random_for_gold_standard': 'standard_gold',
        'brutus_hierarchical': 'hierarchical',
        'brutus_hierarchical_gold_standard': 'hierarchical_gold',
        'brutus_standard_quasi_random': 'standard',
        'brutus_standard_quasi_random_gold_standard': 'standard_gold'
    }

    return directory_mapping.get(directory_name)
