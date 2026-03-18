#!/usr/bin/env python3
"""
Correspondence validation module for the Three-Body Problem database.

Checks 1:1 correspondence between IC files and Brutus output files.
"""

from pathlib import Path
from typing import List, Dict, Set, Tuple, Any
import logging

from ..datastructures import ValidationIssue, ValidationStatus, create_issue
from ..utils.naming import extract_file_numbers, list_matching_files
from ..config import config


def validate_correspondence(variant: str) -> List[ValidationIssue]:
    """
    Validate 1:1 correspondence between IC and Brutus files for a dataset variant.

    Args:
        variant: Dataset variant name (e.g., 'hierarchical', 'hierarchical_gold')

    Returns:
        List of validation issues
    """
    issues = []

    try:
        # Get directories for this variant
        ic_dir = config.get_ic_dir(variant)
        brutus_dir = config.get_brutus_dir(variant)

        # Check if directories exist
        if not ic_dir.exists():
            issues.append(create_issue(
                issue_id="ic_dir_missing",
                severity=ValidationStatus.ERROR,
                module="correspondence",
                message=f"IC directory does not exist: {ic_dir}",
                file_path=str(ic_dir)
            ))
            return issues

        if not brutus_dir.exists():
            issues.append(create_issue(
                issue_id="brutus_dir_missing",
                severity=ValidationStatus.ERROR,
                module="correspondence",
                message=f"Brutus directory does not exist: {brutus_dir}",
                file_path=str(brutus_dir)
            ))
            return issues

        # Extract file numbers from both directories
        ic_numbers = extract_file_numbers(ic_dir, variant, 'ic')
        brutus_numbers = extract_file_numbers(brutus_dir, variant, 'brutus')

        # Check for missing Brutus outputs (ICs without corresponding Brutus)
        missing_brutus = ic_numbers - brutus_numbers
        for num in sorted(missing_brutus):
            # Check if this IC is blacklisted (should not have Brutus output)
            if is_blacklisted(num, variant):
                issues.append(create_issue(
                    issue_id="blacklisted_ic_missing_brutus",
                    severity=ValidationStatus.PASS,
                    module="correspondence",
                    message=f"Blacklisted IC {num} correctly has no Brutus output",
                    file_path=str(ic_dir / config.get_ic_pattern(variant).format(num=num))
                ))
            else:
                issues.append(create_issue(
                    issue_id="missing_brutus",
                    severity=ValidationStatus.FAIL,
                    module="correspondence",
                    message=f"IC file {num} has no corresponding Brutus output",
                    file_path=str(ic_dir / config.get_ic_pattern(variant).format(num=num))
                ))

        # Check for missing ICs (Brutus outputs without corresponding ICs)
        missing_ic = brutus_numbers - ic_numbers
        for num in sorted(missing_ic):
            issues.append(create_issue(
                issue_id="missing_ic",
                severity=ValidationStatus.WARNING,
                module="correspondence",
                message=f"Brutus output {num} has no corresponding IC file",
                file_path=str(brutus_dir / config.get_brutus_pattern(variant).format(num=num))
            ))

        # Check for duplicate files (should not happen with numeric IDs)
        duplicate_issues = check_for_duplicates(ic_dir, variant, 'ic')
        issues.extend(duplicate_issues)

        duplicate_issues = check_for_duplicates(brutus_dir, variant, 'brutus')
        issues.extend(duplicate_issues)

        # Log summary statistics
        log_summary(variant, ic_numbers, brutus_numbers, missing_brutus, missing_ic)

    except Exception as e:
        issues.append(create_issue(
            issue_id="correspondence_error",
            severity=ValidationStatus.ERROR,
            module="correspondence",
            message=f"Error during correspondence validation: {str(e)}"
        ))
        logging.error(f"Error in validate_correspondence for {variant}: {e}", exc_info=True)

    return issues


def is_blacklisted(file_number: int, variant: str) -> bool:
    """
    Check if a file number is in the blacklist for its variant.

    Args:
        file_number: Numeric ID to check
        variant: Dataset variant name

    Returns:
        True if blacklisted, False otherwise
    """
    # Check standard_gold exclusions first (184 IDs not selected for gold-standard re-simulation)
    if variant == 'standard_gold':
        excluded_ids = load_standard_gold_exclusions()
        if file_number in excluded_ids:
            return True

    blacklist = config.get_blacklist_ids()

    # Map variant names to blacklist keys
    variant_to_key = {
        'hierarchical': 'hierarchical',
        'hierarchical_gold': 'hierarchical',
        'standard': 'standard',
        'standard_gold': 'standard'
    }

    key = variant_to_key.get(variant)
    if key and key in blacklist:
        return file_number in blacklist[key]

    return False


def load_standard_gold_exclusions() -> Set[int]:
    """
    Load 184 excluded IDs from standard_quasi_random_ids_not_in_gold.md.

    These are ICs that exist in ic_standard_quasi_random/ but were never
    selected for gold-standard re-simulation (dt_out=0.01).

    Returns:
        Set of excluded numeric IDs
    """
    excluded: Set[int] = set()
    md_path = Path(__file__).parent.parent.parent.parent / "Documentation" / "standard_quasi_random_ids_not_in_gold.md"
    if not md_path.exists():
        logging.warning(f"Exclusion list not found: {md_path}")
        return excluded

    with open(md_path) as f:
        in_list = False
        for line in f:
            line = line.strip()
            if line.startswith('```') and line.endswith('```'):
                in_list = not in_list
                continue
            if in_list:
                for token in line.split():
                    if token.isdigit():
                        excluded.add(int(token))

    if len(excluded) != 184:
        logging.warning(f"Expected 184 excluded IDs, found {len(excluded)}. Exclusion list may be outdated.")

    return excluded


def check_for_duplicates(directory: Path, variant: str, file_type: str) -> List[ValidationIssue]:
    """
    Check for duplicate files with the same numeric ID.

    Args:
        directory: Directory to check
        variant: Dataset variant name
        file_type: 'ic' or 'brutus'

    Returns:
        List of validation issues for duplicates
    """
    issues = []

    # List all files matching the pattern
    matching_files = list_matching_files(directory, variant, file_type)

    # Count occurrences of each file number
    number_counts = {}
    for filepath in matching_files:
        from ..utils.naming import validate_filename_pattern
        num = validate_filename_pattern(variant, file_type, filepath.name)
        if num is not None:
            number_counts[num] = number_counts.get(num, 0) + 1

    # Report duplicates
    for num, count in number_counts.items():
        if count > 1:
            issues.append(create_issue(
                issue_id=f"duplicate_{file_type}",
                severity=ValidationStatus.ERROR,
                module="correspondence",
                message=f"Found {count} files with number {num} ({file_type})",
                file_path=str(directory)
            ))

    return issues


def log_summary(variant: str, ic_numbers: Set[int], brutus_numbers: Set[int],
                missing_brutus: Set[int], missing_ic: Set[int]):
    """
    Log summary statistics for correspondence validation.

    Args:
        variant: Dataset variant name
        ic_numbers: Set of IC file numbers
        brutus_numbers: Set of Brutus file numbers
        missing_brutus: Set of IC numbers without Brutus output
        missing_ic: Set of Brutus numbers without IC file
    """
    logger = logging.getLogger("three_body_validator")

    # Count blacklisted ICs that are correctly missing Brutus outputs
    blacklisted_missing = sum(1 for num in missing_brutus if is_blacklisted(num, variant))
    actual_missing = len(missing_brutus) - blacklisted_missing

    logger.info(f"Correspondence validation for {variant}:")
    logger.info(f"  IC files: {len(ic_numbers)}")
    logger.info(f"  Brutus outputs: {len(brutus_numbers)}")
    logger.info(f"  Missing Brutus outputs: {actual_missing} (excluding {blacklisted_missing} blacklisted)")
    logger.info(f"  Missing IC files: {len(missing_ic)}")
    if len(ic_numbers) > 0:
        logger.info(f"  Completion: {len(brutus_numbers)}/{len(ic_numbers)} ({len(brutus_numbers)/len(ic_numbers)*100:.1f}%)")
    else:
        logger.info(f"  Completion: N/A (no IC files found)")

    # Report standard_gold exclusion list (184 IDs not selected for gold-standard re-simulation)
    if variant == 'standard_gold':
        excluded_ids = load_standard_gold_exclusions()
        logger.info(f"  {len(excluded_ids)} IDs excluded per standard_quasi_random_ids_not_in_gold.md (expected subset gap)")

    if actual_missing == 0 and len(missing_ic) == 0:
        logger.info(f"  ✅ Perfect 1:1 correspondence!")
    elif actual_missing > 0:
        logger.warning(f"  ⚠️  Incomplete: {actual_missing} ICs missing Brutus outputs")
    else:
        logger.info(f"  ✓ All existing ICs have corresponding Brutus outputs")


def get_correspondence_status(variant: str) -> Dict[str, Any]:
    """
    Get detailed correspondence status for a dataset variant.

    Args:
        variant: Dataset variant name

    Returns:
        Dictionary with correspondence statistics
    """
    try:
        ic_dir = config.get_ic_dir(variant)
        brutus_dir = config.get_brutus_dir(variant)

        if not ic_dir.exists() or not brutus_dir.exists():
            return {"error": "Directories not found"}

        ic_numbers = extract_file_numbers(ic_dir, variant, 'ic')
        brutus_numbers = extract_file_numbers(brutus_dir, variant, 'brutus')

        missing_brutus = ic_numbers - brutus_numbers
        missing_ic = brutus_numbers - ic_numbers

        # Filter out blacklisted ICs
        blacklisted_missing = [num for num in missing_brutus if is_blacklisted(num, variant)]
        actual_missing = list(missing_brutus - set(blacklisted_missing))

        return {
            "variant": variant,
            "ic_count": len(ic_numbers),
            "brutus_count": len(brutus_numbers),
            "missing_brutus": sorted(actual_missing),
            "missing_ic": sorted(missing_ic),
            "blacklisted_missing": sorted(blacklisted_missing),
            "completion_percentage": len(brutus_numbers) / len(ic_numbers) * 100 if ic_numbers else 0,
            "perfect_correspondence": len(actual_missing) == 0 and len(missing_ic) == 0
        }

    except Exception as e:
        return {"error": str(e)}