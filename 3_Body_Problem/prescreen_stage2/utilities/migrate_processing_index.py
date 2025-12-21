#!/usr/bin/env python3
"""
Migration script to split the existing processing_index.json into separate indices
for hierarchical and standard datasets.
"""

import json
import os
from datetime import datetime

def migrate_processing_index():
    """Migrate from single to dual processing indices."""
    
    # Load existing index
    existing_index_path = "<home>/Desktop/cursor/3_Body_Problem/prescreen_stage2/processing_index.json"
    
    if not os.path.exists(existing_index_path):
        print("No existing processing_index.json found. Migration not needed.")
        return
    
    print("Loading existing processing index...")
    with open(existing_index_path, 'r') as f:
        existing_data = json.load(f)
    
    # Create separate indices
    hierarchical_index = {
        'processed_files': {},
        'processing_runs': []
    }
    
    standard_index = {
        'processed_files': {},
        'processing_runs': []
    }
    
    # Analyze files to determine which dataset they belong to
    print("Analyzing processed files...")
    
    # Check recent runs to see which dataset was being processed
    last_dataset = None
    if existing_data.get('processing_runs'):
        # Look for the most recent runs to infer the dataset
        for run in reversed(existing_data['processing_runs']):
            # Check if run has dataset info (won't exist in old format)
            if 'dataset' in run:
                last_dataset = run['dataset']
                break
    
    # Since we can't determine which files belong to which dataset from the old format,
    # we'll check the actual files in the output directories
    hierarchical_output = "<home>/Desktop/cursor/3_Body_Problem/final_stage_ic_datasets/ic_hierarchical"
    standard_output = "<home>/Desktop/cursor/3_Body_Problem/final_stage_ic_datasets/ic_standard_quasi_random"
    
    hierarchical_files = set()
    standard_files = set()
    
    if os.path.exists(hierarchical_output):
        hierarchical_files = set(os.listdir(hierarchical_output))
    
    if os.path.exists(standard_output):
        standard_files = set(os.listdir(standard_output))
    
    # Distribute processed files based on which output directory they're in
    for filename, file_data in existing_data['processed_files'].items():
        if filename in hierarchical_files:
            hierarchical_index['processed_files'][filename] = file_data
        elif filename in standard_files:
            standard_index['processed_files'][filename] = file_data
        else:
            # If file is not in either output, check if it passed
            # If it didn't pass, we can't determine which dataset it's from
            # so we'll skip it (it will be reprocessed if needed)
            if file_data.get('passed', False):
                print(f"Warning: Could not determine dataset for passed file {filename}")
    
    # Copy processing runs (they'll be shared history)
    # Add a migration note
    migration_run = {
        'run_id': 'migration_' + datetime.now().isoformat(),
        'timestamp': datetime.now().isoformat(),
        'note': 'Migrated from single processing_index.json to separate indices',
        'original_runs': len(existing_data.get('processing_runs', []))
    }
    
    hierarchical_index['processing_runs'] = existing_data.get('processing_runs', []).copy()
    hierarchical_index['processing_runs'].append(migration_run)
    
    standard_index['processing_runs'] = existing_data.get('processing_runs', []).copy()
    standard_index['processing_runs'].append(migration_run)
    
    # Save new indices
    hierarchical_path = "<home>/Desktop/cursor/3_Body_Problem/prescreen_stage2/processing_index_ic_hierarchical.json"
    standard_path = "<home>/Desktop/cursor/3_Body_Problem/prescreen_stage2/processing_index_ic_standard_quasi_random.json"
    
    print(f"Saving hierarchical index with {len(hierarchical_index['processed_files'])} files...")
    with open(hierarchical_path, 'w') as f:
        json.dump(hierarchical_index, f, indent=2)
    
    print(f"Saving standard index with {len(standard_index['processed_files'])} files...")
    with open(standard_path, 'w') as f:
        json.dump(standard_index, f, indent=2)
    
    # Rename old index as backup
    backup_path = existing_index_path + '.backup_' + datetime.now().strftime('%Y%m%d_%H%M%S')
    os.rename(existing_index_path, backup_path)
    print(f"Original index backed up to: {backup_path}")
    
    print("\nMigration complete!")
    print(f"Hierarchical files: {len(hierarchical_index['processed_files'])}")
    print(f"Standard files: {len(standard_index['processed_files'])}")
    print(f"Total processing runs migrated: {len(existing_data.get('processing_runs', []))}")


if __name__ == "__main__":
    migrate_processing_index()
