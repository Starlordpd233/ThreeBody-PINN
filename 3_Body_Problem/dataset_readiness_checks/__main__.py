"""
Entry point for dataset readiness checks.
"""

import sys
import argparse
from pathlib import Path
from .validator import run_validation
from .config import config
from .reports.markdown import generate_markdown_report
from .reports.json_report import generate_json_report

def main():
    parser = argparse.ArgumentParser(description='Dataset Readiness Checks for PINN Training')
    
    parser.add_argument('--variants', nargs='+', 
                        default=['hierarchical', 'standard', 'hierarchical_gold', 'standard_gold'],
                        help='Dataset variants to validate')
    
    parser.add_argument('--threshold', type=float, default=9.5,
                        help='Completeness threshold for Brutus simulations (default: 9.5)')
    
    parser.add_argument('--output-dir', type=Path, default=None,
                        help='Directory for output reports')
    
    parser.add_argument('--modules', nargs='+', default=None,
                        help='Specific validation modules to run')

    parser.add_argument('--strict', action='store_true',
                        help='Fail with exit code 1 if ANY warning is found')

    args = parser.parse_args()
    
    # Configure output directory
    output_dir = args.output_dir or config.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Update config with CLI args
    config.completeness_threshold = args.threshold
    if args.modules:
        config.enabled_modules = args.modules
        
    print(f"Running dataset readiness checks for: {', '.join(args.variants)}")
    print(f"Output directory: {output_dir}")
    
    # Run validation
    report = run_validation(variants=args.variants, output_dir=output_dir, threshold=args.threshold, modules=config.enabled_modules if args.modules else None)
    
    # Generate reports
    print("Generating reports...")
    
    # JSON Report
    json_path = output_dir / "readiness_report.json"
    generate_json_report(report, json_path)
    print(f"  - JSON: {json_path}")
    
    # Markdown Report
    md_path = output_dir / "READINESS_REPORT.md"
    generate_markdown_report(report, md_path)
    print(f"  - Markdown: {md_path}")
    
    # Determine exit code
    stats = report.get_summary()
    error_count = stats.get('total_errors', 0)
    warning_count = stats.get('total_warnings', 0)
    
    if error_count > 0:
        print(f"\nFAILURE: Found {error_count} errors.")
        sys.exit(2)
    elif warning_count > 0 and args.strict:
        print(f"\nFAILURE: Found {warning_count} warnings (strict mode).")
        sys.exit(1)
    elif warning_count > 0:
        print(f"\nSUCCESS (with warnings): Found {warning_count} warnings.")
        sys.exit(0)
    else:
        print("\nSUCCESS: All checks passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
