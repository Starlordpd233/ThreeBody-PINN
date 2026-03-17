#!/usr/bin/env python3
"""
Utility functions for managing incremental prescreening.
"""

import json
import os
import glob
from typing import Dict, List
import shutil
from datetime import datetime

def load_index(index_file: str) -> Dict:
    """Load processing index."""
    if os.path.exists(index_file):
        with open(index_file, 'r') as f:
            return json.load(f)
    return None


def get_processing_stats(index_file: str):
    """Get statistics from processing index."""
    index = load_index(index_file)
    if not index:
        print("No processing index found.")
        return
    
    total_files = len(index['processed_files'])
    passed_files = sum(1 for f in index['processed_files'].values() if f['passed'])
    failed_files = total_files - passed_files
    
    print("Processing Statistics")
    print("=" * 50)
    print(f"Total files processed: {total_files}")
    print(f"Passed: {passed_files} ({passed_files/total_files*100:.1f}%)")
    print(f"Failed: {failed_files} ({failed_files/total_files*100:.1f}%)")
    
    # Processing run history
    print(f"\nProcessing runs: {len(index['processing_runs'])}")
    for i, run in enumerate(index['processing_runs'][-5:]):  # Show last 5 runs
        print(f"\nRun {i+1}:")
        print(f"  Timestamp: {run['timestamp']}")
        print(f"  Files processed: {run['files_processed']}")
        print(f"  Passed: {run['files_passed']} ({run['files_passed']/run['files_processed']*100:.1f}%)")
        print(f"  Time: {run.get('elapsed_time', 0):.2f}s")


def reset_file_status(index_file: str, filenames: List[str]):
    """Reset the status of specific files so they'll be reprocessed."""
    index = load_index(index_file)
    if not index:
        print("No processing index found.")
        return
    
    count = 0
    for filename in filenames:
        if filename in index['processed_files']:
            del index['processed_files'][filename]
            count += 1
            print(f"Reset: {filename}")
    
    if count > 0:
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)
        print(f"\nReset {count} files. They will be reprocessed on next run.")
    else:
        print("No matching files found in index.")


def find_failed_files(index_file: str) -> List[str]:
    """Get list of all failed files."""
    index = load_index(index_file)
    if not index:
        return []
    
    failed = []
    for filename, data in index['processed_files'].items():
        if not data['passed']:
            failed.append(filename)
    return failed


def analyze_failures(index_file: str):
    """Analyze failure reasons across all processed files."""
    index = load_index(index_file)
    if not index:
        print("No processing index found.")
        return
    
    failure_reasons = {}
    failed_files_by_reason = {}
    
    for filename, data in index['processed_files'].items():
        if not data['passed']:
            results = data.get('results', {})
            reason = results.get('reason', results.get('stage', 'unknown'))
            
            failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
            
            if reason not in failed_files_by_reason:
                failed_files_by_reason[reason] = []
            failed_files_by_reason[reason].append(filename)
    
    print("Failure Analysis")
    print("=" * 50)
    for reason, count in sorted(failure_reasons.items(), key=lambda x: x[1], reverse=True):
        print(f"\n{reason}: {count} files")
        # Show first 3 examples
        examples = failed_files_by_reason[reason][:3]
        for ex in examples:
            print(f"  - {ex}")
        if len(failed_files_by_reason[reason]) > 3:
            print(f"  ... and {len(failed_files_by_reason[reason]) - 3} more")


def clean_output_directory(index_file: str, output_dir: str):
    """Remove files from output directory that are no longer marked as passed."""
    index = load_index(index_file)
    if not index:
        print("No processing index found.")
        return
    
    # Get list of files that should be in output
    should_exist = set()
    for filename, data in index['processed_files'].items():
        if data['passed']:
            should_exist.add(filename)
    
    # Check what's actually in output directory
    existing_files = set()
    for filepath in glob.glob(os.path.join(output_dir, "*.txt")):
        existing_files.add(os.path.basename(filepath))
    for filepath in glob.glob(os.path.join(output_dir, "*.dat")):
        existing_files.add(os.path.basename(filepath))
    
    # Find orphaned files
    orphaned = existing_files - should_exist - {'processing_index.json', 'prescreening_results.json'}
    orphaned = [f for f in orphaned if not f.startswith('run_results_')]
    
    if orphaned:
        print(f"Found {len(orphaned)} orphaned files in output directory:")
        for f in orphaned[:10]:
            print(f"  - {f}")
        if len(orphaned) > 10:
            print(f"  ... and {len(orphaned) - 10} more")
        
        response = input("\nRemove orphaned files? (y/n): ")
        if response.lower() == 'y':
            for f in orphaned:
                os.remove(os.path.join(output_dir, f))
            print(f"Removed {len(orphaned)} files.")
    else:
        print("No orphaned files found.")


def export_passed_list(index_file: str, output_file: str):
    """Export a simple list of passed filenames."""
    index = load_index(index_file)
    if not index:
        print("No processing index found.")
        return
    
    passed_files = []
    for filename, data in index['processed_files'].items():
        if data['passed']:
            passed_files.append(filename)
    
    with open(output_file, 'w') as f:
        for filename in sorted(passed_files):
            f.write(f"{filename}\n")
    
    print(f"Exported {len(passed_files)} passed filenames to {output_file}")


def check_new_files(input_dir: str, index_file: str):
    """Check how many new files are waiting to be processed."""
    index = load_index(index_file)
    if not index:
        processed_files = set()
    else:
        processed_files = set(index['processed_files'].keys())
    
    # Find all IC files
    all_files = set()
    for filepath in glob.glob(os.path.join(input_dir, "*.txt")):
        all_files.add(os.path.basename(filepath))
    for filepath in glob.glob(os.path.join(input_dir, "*.dat")):
        all_files.add(os.path.basename(filepath))
    
    new_files = all_files - processed_files
    
    print(f"Total files in input directory: {len(all_files)}")
    print(f"Already processed: {len(processed_files)}")
    print(f"New files to process: {len(new_files)}")
    
    if new_files and len(new_files) <= 20:
        print("\nNew files:")
        for f in sorted(new_files):
            print(f"  - {f}")


def main():
    """Main utility interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Prescreening Index Utilities")
    
    # Paths
    default_output_dir = "<home>/Desktop/3_body_problem/simulation_data/Data/ic_final"
    default_index = os.path.join(default_output_dir, "processing_index.json")
    default_input_dir = "<home>/Desktop/3_body_problem/simulation_data/Data/ic_raw/ic_standard_quasi_random"
    
    parser.add_argument("--index", default=default_index, help="Path to processing index")
    
    # Commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Stats command
    subparsers.add_parser('stats', help='Show processing statistics')
    
    # Reset command
    reset_parser = subparsers.add_parser('reset', help='Reset files for reprocessing')
    reset_parser.add_argument('files', nargs='+', help='Filenames to reset')
    
    # Failed command
    subparsers.add_parser('failed', help='List failed files')
    
    # Analyze command
    subparsers.add_parser('analyze', help='Analyze failure reasons')
    
    # Clean command
    clean_parser = subparsers.add_parser('clean', help='Clean orphaned files')
    clean_parser.add_argument('--output-dir', default=default_output_dir, help='Output directory')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export passed file list')
    export_parser.add_argument('output', help='Output file path')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check for new files')
    check_parser.add_argument('--input-dir', default=default_input_dir, help='Input directory')
    
    args = parser.parse_args()
    
    if args.command == 'stats':
        get_processing_stats(args.index)
    
    elif args.command == 'reset':
        reset_file_status(args.index, args.files)
    
    elif args.command == 'failed':
        failed = find_failed_files(args.index)
        print(f"Failed files ({len(failed)}):")
        for f in failed[:20]:
            print(f"  - {f}")
        if len(failed) > 20:
            print(f"  ... and {len(failed) - 20} more")
    
    elif args.command == 'analyze':
        analyze_failures(args.index)
    
    elif args.command == 'clean':
        clean_output_directory(args.index, args.output_dir)
    
    elif args.command == 'export':
        export_passed_list(args.index, args.output)
    
    elif args.command == 'check':
        check_new_files(args.input_dir, args.index)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
