"""
Markdown report generator.
"""

from pathlib import Path
from ..datastructures import ValidationReport, ValidationStatus

def generate_markdown_report(report: ValidationReport, output_path: Path):
    """
    Generate a Markdown report from validation results.
    """
    with open(output_path, 'w') as f:
        f.write(f"# Dataset Readiness Report\n\n")
        f.write(f"**Date:** {report.timestamp}\n")
        f.write(f"**Completeness Threshold:** {report.config['completeness_threshold']}\n\n")
        
        summary = report.get_summary()
        f.write("## Executive Summary\n\n")
        f.write(f"- **Total Files Scanned:** {summary['total_files']}\n")
        f.write(f"- **Total Issues:** {summary['total_issues']}\n")
        f.write(f"- **Dataset Variants:** {summary['dataset_count']}\n\n")
        
        f.write("### Status Counts\n")
        for status, count in summary['status_counts'].items():
            f.write(f"- **{status}:** {count}\n")
            
        f.write("\n## Global Issues\n\n")
        if report.global_issues:
            for issue in report.global_issues:
                f.write(f"- **[{issue.severity.value}]** {issue.message} ({issue.issue_id})\n")
        else:
            f.write("No global issues found.\n")
            
        f.write("\n## Dataset Details\n\n")
        for variant, result in report.datasets.items():
            f.write(f"### Variant: {variant}\n\n")
            
            stats = result.summary_stats
            f.write(f"- **IC Files:** {stats['ic_count']}\n")
            f.write(f"- **Brutus Files:** {stats['brutus_count']}\n")
            f.write(f"- **Missing Brutus:** {len(stats['missing_brutus'])} \n")
            f.write(f"- **Missing IC:** {len(stats['missing_ic'])} \n")
            
            # Group issues by type
            issues_by_type = {}
            for file_res in list(result.ic_results.values()) + list(result.brutus_results.values()):
                for issue in file_res.issues:
                    key = (issue.severity.value, issue.message)
                    if key not in issues_by_type:
                        issues_by_type[key] = 0
                    issues_by_type[key] += 1
                    
            if issues_by_type:
                f.write("\n#### Top Issues\n")
                # Sort by count desc
                sorted_issues = sorted(issues_by_type.items(), key=lambda x: x[1], reverse=True)
                for (severity, msg), count in sorted_issues[:10]:
                    f.write(f"- **[{severity}]** {msg}: {count} occurrences\n")
            else:
                f.write("\nNo file-level issues found.\n")
                
            f.write("\n")

