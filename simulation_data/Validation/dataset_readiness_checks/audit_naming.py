#!/usr/bin/env python3
"""
Script to audit codebase for outdated filename patterns.
"""

from pathlib import Path
import re
import glob

def audit_naming_patterns(base_dir: Path):
    """
    Scan python files for strings that look like outdated filename patterns.
    """
    suspicious_patterns = [
        r"brutus_hierarchical_\d+",
        r"metrics_hierarchical_\d+",
        r"metrics_standard_\d+",
        r"ic_hierarchical_gold_standard", # Directory name confusion?
        r"brutus_standard_quasi_random_\d+"
    ]
    
    print("Auditing python scripts for potential naming issues...")
    
    python_files = glob.glob(str(base_dir / "**/*.py"), recursive=True)
    
    for py_file in python_files:
        if "dataset_readiness_checks" in py_file:
            continue
            
        try:
            with open(py_file, 'r') as f:
                content = f.read()
                
            found = []
            for pat in suspicious_patterns:
                if re.search(pat, content):
                    found.append(pat)
                    
            if found:
                print(f"Warning: {Path(py_file).relative_to(base_dir)}")
                for pat in found:
                    print(f"  - Contains pattern: {pat}")
                    
        except Exception:
            pass

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent.parent
    audit_naming_patterns(base_dir)
