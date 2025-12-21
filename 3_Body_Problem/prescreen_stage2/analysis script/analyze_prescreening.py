#!/usr/bin/env python3
"""
Analyze and visualize the results from Stage 2 pre-screening.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import os
from typing import Dict, List
from collections import Counter

def load_prescreening_results(results_file: str) -> Dict:
    """Load the prescreening results JSON file."""
    with open(results_file, 'r') as f:
        return json.load(f)

def load_all_prescreening_results(results_dir: str, files_to_process: List[str] = None) -> Dict:
    """Load and combine all prescreening results from a directory."""
    all_detailed_results = []
    total_summary = Counter()
    all_failure_reasons = Counter()

    if not os.path.isdir(results_dir):
        print(f"Directory not found: {results_dir}")
        return None

    if files_to_process:
        json_files = files_to_process
    else:
        json_files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
        
    if not json_files:
        print(f"No JSON files found in {results_dir}")
        return None

    print(f"Processing {len(json_files)} result file(s) in {results_dir}")

    for file_name in json_files:
        file_path = os.path.join(results_dir, file_name)
        try:
            results = load_prescreening_results(file_path)
            
            all_detailed_results.extend(results['detailed_results'])
            
            # Extract summary info and map keys from 'run_info'
            run_info = results.get('run_info', {})
            summary_data = {
                'total_files': run_info.get('files_processed', 0),
                'passed': run_info.get('files_passed', 0),
                'failed': run_info.get('files_failed', 0),
                'elapsed_time': run_info.get('elapsed_time', 0)
            }
            total_summary.update(summary_data)
            
            all_failure_reasons.update(results.get('failure_reasons', {}))
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Could not process file {file_name}: {e}")

    if not all_detailed_results:
        print("No valid results found in any of the files.")
        return None

    # Recalculate pass rate
    if total_summary['total_files'] > 0:
        total_summary['pass_rate'] = total_summary['passed'] / total_summary['total_files']
    else:
        total_summary['pass_rate'] = 0
        
    return {
        'summary': dict(total_summary),
        'failure_reasons': dict(all_failure_reasons),
        'detailed_results': all_detailed_results,
    }

def analyze_passed_ics(results: Dict) -> None:
    """Analyze the properties of ICs that passed prescreening."""
    passed_ics = [r for r in results['detailed_results'] if r['passed']]
    
    if not passed_ics:
        print("No ICs passed prescreening!")
        return
    
    # Extract properties
    virial_ratios = [ic['virial_ratio'] for ic in passed_ics]
    angular_momenta = [ic['angular_momentum'] for ic in passed_ics]
    min_separations = [ic['min_separation'] for ic in passed_ics]
    max_energy_errors = [ic['max_energy_error'] for ic in passed_ics]
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Properties of Pre-screened Initial Conditions', fontsize=16)
    
    # Virial ratio distribution
    ax = axes[0, 0]
    ax.hist(virial_ratios, bins=30, alpha=0.7, color='blue', edgecolor='black')
    ax.axvline(x=1.0, color='red', linestyle='--', label='Virial equilibrium')
    ax.set_xlabel('Virial Ratio (Q = 2T/|U|)')
    ax.set_ylabel('Count')
    ax.set_title('Virial Ratio Distribution')
    ax.legend()
    
    # Angular momentum distribution
    ax = axes[0, 1]
    ax.hist(angular_momenta, bins=30, alpha=0.7, color='green', edgecolor='black')
    ax.set_xlabel('Angular Momentum Magnitude')
    ax.set_ylabel('Count')
    ax.set_title('Angular Momentum Distribution')
    ax.set_yscale('log')
    
    # Minimum separation distribution
    ax = axes[1, 0]
    ax.hist(min_separations, bins=30, alpha=0.7, color='orange', edgecolor='black')
    ax.axvline(x=0.01, color='red', linestyle='--', label='Rejection threshold')
    ax.set_xlabel('Minimum Separation During Integration')
    ax.set_ylabel('Count')
    ax.set_title('Minimum Separation Distribution')
    ax.legend()
    
    # Energy conservation
    ax = axes[1, 1]
    ax.hist(np.array(max_energy_errors) * 100, bins=30, alpha=0.7, color='purple', edgecolor='black')
    ax.axvline(x=1.0, color='red', linestyle='--', label='1% threshold')
    ax.set_xlabel('Maximum Energy Error (%)')
    ax.set_ylabel('Count')
    ax.set_title('Energy Conservation Performance')
    ax.legend()
    
    plt.tight_layout()
    return fig

def create_correlation_plot(results: Dict) -> None:
    """Create correlation plots between different properties."""
    passed_ics = [r for r in results['detailed_results'] if r['passed']]
    
    if len(passed_ics) < 2:
        print("Not enough passed ICs for correlation analysis!")
        return
    
    # Extract properties
    virial_ratios = np.array([ic['virial_ratio'] for ic in passed_ics])
    angular_momenta = np.array([ic['angular_momentum'] for ic in passed_ics])
    min_separations = np.array([ic['min_separation'] for ic in passed_ics])
    
    # Create scatter plot matrix
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Property Correlations for Passed ICs', fontsize=16)
    
    # Virial vs Angular Momentum
    ax = axes[0, 0]
    scatter = ax.scatter(virial_ratios, angular_momenta, alpha=0.6, c=min_separations, cmap='viridis')
    ax.set_xlabel('Virial Ratio')
    ax.set_ylabel('Angular Momentum')
    ax.set_title('Virial Ratio vs Angular Momentum')
    plt.colorbar(scatter, ax=ax, label='Min Separation')
    
    # Virial vs Min Separation
    ax = axes[0, 1]
    ax.scatter(virial_ratios, min_separations, alpha=0.6)
    ax.set_xlabel('Virial Ratio')
    ax.set_ylabel('Minimum Separation')
    ax.set_title('Virial Ratio vs Minimum Separation')
    
    # Angular Momentum vs Min Separation
    ax = axes[1, 0]
    ax.scatter(angular_momenta, min_separations, alpha=0.6)
    ax.set_xlabel('Angular Momentum')
    ax.set_ylabel('Minimum Separation')
    ax.set_title('Angular Momentum vs Minimum Separation')
    
    # Energy distribution (T vs U)
    ax = axes[1, 1]
    T = np.array([ic['kinetic_energy'] for ic in passed_ics])
    U = np.array([ic['potential_energy'] for ic in passed_ics])
    E = T + U
    ax.scatter(T, -U, alpha=0.6, c=E, cmap='RdBu')
    ax.plot([0, max(T)], [0, max(T)], 'k--', alpha=0.5, label='Virial equilibrium')
    ax.set_xlabel('Kinetic Energy')
    ax.set_ylabel('-Potential Energy')
    ax.set_title('Energy Distribution')
    ax.legend()
    
    plt.tight_layout()
    return fig

def print_summary_statistics(results: Dict) -> None:
    """Print detailed summary statistics."""
    summary = results['summary']
    
    print("=" * 60)
    print("STAGE 2 PRE-SCREENING SUMMARY")
    print("=" * 60)
    print(f"Total ICs processed: {summary['total_files']}")
    print(f"Passed: {summary['passed']} ({summary['pass_rate']*100:.1f}%)")
    print(f"Failed: {summary['failed']} ({(1-summary['pass_rate'])*100:.1f}%)")
    print(f"Processing time: {summary['elapsed_time']:.2f} seconds")
    print(f"Average time per IC: {summary['elapsed_time']/summary['total_files']:.3f} seconds")
    print()
    
    print("Failure Breakdown:")
    for reason, count in results['failure_reasons'].items():
        percentage = (count / summary['failed']) * 100 if summary['failed'] > 0 else 0
        print(f"  - {reason}: {count} ({percentage:.1f}% of failures)")
    print()
    
    # Statistics for passed ICs
    passed_ics = [r for r in results['detailed_results'] if r['passed']]
    if passed_ics:
        print("Statistics for Passed ICs:")
        
        virial_ratios = [ic['virial_ratio'] for ic in passed_ics]
        print(f"  Virial Ratio: {np.mean(virial_ratios):.3f} ± {np.std(virial_ratios):.3f}")
        print(f"    Range: [{np.min(virial_ratios):.3f}, {np.max(virial_ratios):.3f}]")
        
        angular_momenta = [ic['angular_momentum'] for ic in passed_ics]
        print(f"  Angular Momentum: {np.mean(angular_momenta):.3f} ± {np.std(angular_momenta):.3f}")
        print(f"    Range: [{np.min(angular_momenta):.3f}, {np.max(angular_momenta):.3f}]")
        
        min_seps = [ic['min_separation'] for ic in passed_ics]
        print(f"  Min Separation: {np.mean(min_seps):.3f} ± {np.std(min_seps):.3f}")
        print(f"    Range: [{np.min(min_seps):.3f}, {np.max(min_seps):.3f}]")
        
        energy_errors = [ic['max_energy_error'] for ic in passed_ics]
        print(f"  Max Energy Error: {np.mean(energy_errors)*100:.4f}% ± {np.std(energy_errors)*100:.4f}%")
        print(f"    Range: [{np.min(energy_errors)*100:.4f}%, {np.max(energy_errors)*100:.4f}%]")

def main():
    """Main analysis function."""
    # Path to results directory
    results_dir = "3_Body_Problem/prescreen_stage2/prescreen_run_results"
    output_dir = "3_Body_Problem/prescreen_stage2/analysis_output"

    os.makedirs(output_dir, exist_ok=True)
    
    # For debugging, process only the first JSON file found.
    # To process all files, set 'files_to_process' to None.
    all_json_files = sorted([f for f in os.listdir(results_dir) if f.endswith('.json')])
    if not all_json_files:
        print(f"No JSON files found in {results_dir}")
        return

    files_to_process = all_json_files
    print("--- Running in single-file debug mode ---")
    print(f"Processing: {files_to_process[0]}")

    # Load and combine all results from the directory
    results = load_all_prescreening_results(results_dir, files_to_process=files_to_process)
    
    if not results:
        print("No results to analyze.")
        return

    # Print summary
    print_summary_statistics(results)
    
    # Create visualizations
    print("\nGenerating visualizations...")
    
    # Property distributions
    fig1 = analyze_passed_ics(results)
    if fig1:
        output_path = os.path.join(output_dir, 'property_distributions.png')
        fig1.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {output_path}")

    # Correlation plots
    fig2 = create_correlation_plot(results)
    if fig2:
        output_path = os.path.join(output_dir, 'property_correlations.png')
        fig2.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Saved: {output_path}")
    
    plt.show()

if __name__ == "__main__":
    main()
