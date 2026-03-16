#!/usr/bin/env python3
import os
import glob
from datetime import datetime

def check_last_line(filepath):
    """Check if the last non-empty line of a file starts with 'Result: filename='"""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            
        # Find the last non-empty line
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i].strip()
            if line:  # Found a non-empty line
                return line.startswith('Result: filename=')
        
        # File is empty or has only empty lines
        return False
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

def main():
    folders = [
        'brutus_hierarchical',
        'brutus_hierarchical_gold_standard', 
        'brutus_standard_quasi_random',
        'brutus_standard_quasi_random_gold_standard'
    ]
    
    # Create report file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"missing_results_report_{timestamp}.txt"
    
    with open(report_filename, 'w') as report:
        report.write("BRUTUS OUTPUT FILES MISSING 'Result: filename...' LINE\n")
        report.write(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write("="*80 + "\n\n")
        
        summary_data = []
        
        for folder in folders:
            print(f"\nChecking folder: {folder}")
            pattern = os.path.join(folder, '*.txt')
            txt_files = glob.glob(pattern)
            txt_files.sort()
            
            missing_in_folder = []
            
            for filepath in txt_files:
                if not check_last_line(filepath):
                    missing_in_folder.append(os.path.basename(filepath))
            
            # Write to report
            report.write(f"\nFOLDER: {folder}\n")
            report.write(f"Total files: {len(txt_files)}\n")
            report.write(f"Missing 'Result:' line: {len(missing_in_folder)}\n")
            report.write("-"*50 + "\n")
            
            if missing_in_folder:
                for filename in sorted(missing_in_folder):
                    report.write(f"  {filename}\n")
            else:
                report.write("  All files have 'Result:' line ✓\n")
            
            report.write("\n")
            
            # Store summary data
            summary_data.append({
                'folder': folder,
                'total': len(txt_files),
                'missing': len(missing_in_folder),
                'percentage': (len(missing_in_folder) / len(txt_files) * 100) if len(txt_files) > 0 else 0
            })
            
            print(f"  Total files: {len(txt_files)}")
            print(f"  Missing 'Result:' line: {len(missing_in_folder)}")
            print(f"  Percentage missing: {summary_data[-1]['percentage']:.1f}%")
        
        # Write summary at the end
        report.write("\n" + "="*80 + "\n")
        report.write("SUMMARY\n")
        report.write("="*80 + "\n\n")
        
        for data in summary_data:
            report.write(f"{data['folder']:<50} {data['missing']:>5}/{data['total']:<5} ({data['percentage']:>5.1f}% missing)\n")
    
    print(f"\nDetailed report saved to: {report_filename}")
    
    # Also create a simple CSV for easy processing
    csv_filename = f"missing_results_{timestamp}.csv"
    with open(csv_filename, 'w') as csv_file:
        csv_file.write("folder,filename\n")
        for folder in folders:
            pattern = os.path.join(folder, '*.txt')
            txt_files = glob.glob(pattern)
            for filepath in txt_files:
                if not check_last_line(filepath):
                    csv_file.write(f"{folder},{os.path.basename(filepath)}\n")
    
    print(f"CSV file saved to: {csv_filename}")

if __name__ == "__main__":
    main() 