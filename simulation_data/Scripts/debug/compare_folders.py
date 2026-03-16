#!/usr/bin/env python3
"""
Script to compare two folders to check if they are identical.
"""

import os
import hashlib
from pathlib import Path

def get_file_hash(filepath):
    """Calculate SHA256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def get_folder_files(folder_path):
    """Get all files in a folder with their relative paths and hashes."""
    folder_path = Path(folder_path)
    files_info = {}
    
    if not folder_path.exists():
        print(f"Folder does not exist: {folder_path}")
        return files_info
    
    for file_path in folder_path.rglob('*'):
        if file_path.is_file():
            relative_path = file_path.relative_to(folder_path)
            file_hash = get_file_hash(file_path)
            file_size = file_path.stat().st_size
            files_info[str(relative_path)] = {
                'hash': file_hash,
                'size': file_size,
                'full_path': str(file_path)
            }
    
    return files_info

def compare_folders(folder1, folder2):
    """Compare two folders for identical content."""
    print(f"Comparing folders:")
    print(f"  Folder 1: {folder1}")
    print(f"  Folder 2: {folder2}")
    print()
    
    # Get file information for both folders
    files1 = get_folder_files(folder1)
    files2 = get_folder_files(folder2)
    
    print(f"Folder 1 contains {len(files1)} files")
    print(f"Folder 2 contains {len(files2)} files")
    print()
    
    # Check if same number of files
    if len(files1) != len(files2):
        print(f"❌ DIFFERENT: Folders have different number of files!")
        print(f"   Folder 1: {len(files1)} files")
        print(f"   Folder 2: {len(files2)} files")
    
    # Find files only in folder1
    only_in_1 = set(files1.keys()) - set(files2.keys())
    if only_in_1:
        print(f"❌ Files only in folder 1 ({len(only_in_1)} files):")
        for file in sorted(only_in_1)[:10]:  # Show first 10
            print(f"   {file}")
        if len(only_in_1) > 10:
            print(f"   ... and {len(only_in_1) - 10} more")
        print()
    
    # Find files only in folder2
    only_in_2 = set(files2.keys()) - set(files1.keys())
    if only_in_2:
        print(f"❌ Files only in folder 2 ({len(only_in_2)} files):")
        for file in sorted(only_in_2)[:10]:  # Show first 10
            print(f"   {file}")
        if len(only_in_2) > 10:
            print(f"   ... and {len(only_in_2) - 10} more")
        print()
    
    # Check files that exist in both folders
    common_files = set(files1.keys()) & set(files2.keys())
    different_content = []
    different_size = []
    
    for file in common_files:
        if files1[file]['size'] != files2[file]['size']:
            different_size.append(file)
        elif files1[file]['hash'] != files2[file]['hash']:
            different_content.append(file)
    
    if different_size:
        print(f"❌ Files with different sizes ({len(different_size)} files):")
        for file in sorted(different_size)[:10]:
            print(f"   {file}: {files1[file]['size']} vs {files2[file]['size']} bytes")
        if len(different_size) > 10:
            print(f"   ... and {len(different_size) - 10} more")
        print()
    
    if different_content:
        print(f"❌ Files with different content ({len(different_content)} files):")
        for file in sorted(different_content)[:10]:
            print(f"   {file}")
        if len(different_content) > 10:
            print(f"   ... and {len(different_content) - 10} more")
        print()
    
    # Final verdict
    are_identical = (len(only_in_1) == 0 and len(only_in_2) == 0 and 
                    len(different_size) == 0 and len(different_content) == 0)
    
    print("=" * 50)
    if are_identical:
        print("✅ FOLDERS ARE IDENTICAL!")
        print("   - Same number of files")
        print("   - Same file names")
        print("   - Same file sizes")
        print("   - Same file content")
    else:
        print("❌ FOLDERS ARE DIFFERENT!")
        differences = []
        if len(only_in_1) > 0:
            differences.append(f"{len(only_in_1)} files only in folder 1")
        if len(only_in_2) > 0:
            differences.append(f"{len(only_in_2)} files only in folder 2")
        if len(different_size) > 0:
            differences.append(f"{len(different_size)} files with different sizes")
        if len(different_content) > 0:
            differences.append(f"{len(different_content)} files with different content")
        
        print("   Differences found:")
        for diff in differences:
            print(f"   - {diff}")
    
    return are_identical

def main():
    folder1 = "<home>/Desktop/cursor/simulation_data/Documentation/problematic_ics/hierarchical"
    folder2 = "<home>/Desktop/cursor/simulation_data/Documentation/problematic_ics/hierarchical_for_gold_standard"
    
    compare_folders(folder1, folder2)

if __name__ == "__main__":
    main() 