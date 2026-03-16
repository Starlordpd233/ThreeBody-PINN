#!/usr/bin/env python3
"""
Metrics Analysis Tool for Brutus Simulations
Analyzes the JSON metrics files to generate summary statistics and plots

Usage:
python3 <home>/Desktop/cursor/3_Body_Problem/analyze_metrics.py
"""

import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Paths
BASE_DIR = Path("<home>/Desktop/cursor/3_Body_Problem")
METRICS_DIRS = {
    "hierarchical": BASE_DIR / "sim_result_metric_hierarchical",
    "standard": BASE_DIR / "sim_result_metric_standard"
}

def load_metrics(metrics_dir):
    """Load all metrics files from a directory."""
    metrics_list = []
    
    for json_file in sorted(metrics_dir.glob("*.json")):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                data['filename'] = json_file.name
                data['sim_number'] = int(json_file.stem.split('_')[-1])
                metrics_list.append(data)
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
    
    return metrics_list

def analyze_conservation(metrics_list, sim_type):
    """Analyze conservation properties."""
    if not metrics_list:
        print(f"No metrics found for {sim_type}")
        return
    
    # Extract conservation errors
    energy_errors = []
    momentum_errors = []
    angular_momentum_errors = []
    wall_times = []
    cpu_times = []
    
    for m in metrics_list:
        if 'error' not in m:
            energy_errors.append(m['energy']['relative_error'])
            momentum_errors.append(m['linear_momentum']['relative_error'])
            angular_momentum_errors.append(m['angular_momentum']['relative_error'])
            wall_times.append(m['wall_time_seconds'])
            cpu_times.append(m['cpu_time_seconds'])
    
    if not energy_errors:
        print(f"No valid simulations for {sim_type}")
        return
    
    # Print statistics
    print(f"\n{sim_type.upper()} SIMULATIONS ANALYSIS")
    print("=" * 50)
    print(f"Total simulations: {len(metrics_list)}")
    print(f"Successful simulations: {len(energy_errors)}")
    print(f"Failed simulations: {len(metrics_list) - len(energy_errors)}")
    
    print(f"\nENERGY CONSERVATION:")
    print(f"  Mean relative error: {np.mean(energy_errors):.2e}")
    print(f"  Median relative error: {np.median(energy_errors):.2e}")
    print(f"  Max relative error: {np.max(energy_errors):.2e}")
    print(f"  Min relative error: {np.min(energy_errors):.2e}")
    
    print(f"\nLINEAR MOMENTUM CONSERVATION:")
    print(f"  Mean relative error: {np.mean(momentum_errors):.2e}")
    print(f"  Median relative error: {np.median(momentum_errors):.2e}")
    print(f"  Max relative error: {np.max(momentum_errors):.2e}")
    
    print(f"\nANGULAR MOMENTUM CONSERVATION:")
    print(f"  Mean relative error: {np.mean(angular_momentum_errors):.2e}")
    print(f"  Median relative error: {np.median(angular_momentum_errors):.2e}")
    print(f"  Max relative error: {np.max(angular_momentum_errors):.2e}")
    
    print(f"\nCOMPUTATIONAL EFFICIENCY:")
    print(f"  Mean wall time: {np.mean(wall_times):.1f}s")
    print(f"  Total wall time: {np.sum(wall_times):.1f}s")
    print(f"  Mean CPU time: {np.mean(cpu_times):.1f}s")
    print(f"  CPU utilization: {np.mean(cpu_times) / np.mean(wall_times):.2%}")
    
    return {
        'energy_errors': energy_errors,
        'momentum_errors': momentum_errors,
        'angular_momentum_errors': angular_momentum_errors,
        'wall_times': wall_times,
        'cpu_times': cpu_times
    }

def create_plots(hier_data, std_data):
    """Create comparison plots."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Energy conservation comparison
    ax = axes[0, 0]
    if hier_data and 'energy_errors' in hier_data:
        ax.hist(np.log10(hier_data['energy_errors']), bins=20, alpha=0.5, label='Hierarchical', color='blue')
    if std_data and 'energy_errors' in std_data:
        ax.hist(np.log10(std_data['energy_errors']), bins=20, alpha=0.5, label='Quasi-Random', color='red')
    ax.set_xlabel('log10(Energy Relative Error)')
    ax.set_ylabel('Count')
    ax.set_title('Energy Conservation')
    ax.legend()
    
    # Momentum conservation comparison
    ax = axes[0, 1]
    if hier_data and 'momentum_errors' in hier_data:
        ax.hist(np.log10(hier_data['momentum_errors']), bins=20, alpha=0.5, label='Hierarchical', color='blue')
    if std_data and 'momentum_errors' in std_data:
        ax.hist(np.log10(std_data['momentum_errors']), bins=20, alpha=0.5, label='Quasi-Random', color='red')
    ax.set_xlabel('log10(Momentum Relative Error)')
    ax.set_ylabel('Count')
    ax.set_title('Linear Momentum Conservation')
    ax.legend()
    
    # Wall time distribution
    ax = axes[1, 0]
    if hier_data and 'wall_times' in hier_data:
        ax.hist(hier_data['wall_times'], bins=20, alpha=0.5, label='Hierarchical', color='blue')
    if std_data and 'wall_times' in std_data:
        ax.hist(std_data['wall_times'], bins=20, alpha=0.5, label='Quasi-Random', color='red')
    ax.set_xlabel('Wall Time (seconds)')
    ax.set_ylabel('Count')
    ax.set_title('Computational Time Distribution')
    ax.legend()
    
    # CPU utilization
    ax = axes[1, 1]
    if hier_data and 'cpu_times' in hier_data and 'wall_times' in hier_data:
        cpu_util_hier = [c/w for c, w in zip(hier_data['cpu_times'], hier_data['wall_times'])]
        ax.hist(cpu_util_hier, bins=20, alpha=0.5, label='Hierarchical', color='blue')
    if std_data and 'cpu_times' in std_data and 'wall_times' in std_data:
        cpu_util_std = [c/w for c, w in zip(std_data['cpu_times'], std_data['wall_times'])]
        ax.hist(cpu_util_std, bins=20, alpha=0.5, label='Quasi-Random', color='red')
    ax.set_xlabel('CPU Utilization')
    ax.set_ylabel('Count')
    ax.set_title('CPU Utilization Distribution')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(BASE_DIR / 'metrics_analysis.png', dpi=150)
    print(f"\nPlots saved to: {BASE_DIR / 'metrics_analysis.png'}")

def save_summary_csv(hier_metrics, std_metrics):
    """Save summary data to CSV for further analysis."""
    summary_data = []
    
    # Process hierarchical metrics
    for m in hier_metrics:
        if 'error' not in m:
            summary_data.append({
                'type': 'hierarchical',
                'sim_number': m['sim_number'],
                'energy_error': m['energy']['relative_error'],
                'momentum_error': m['linear_momentum']['relative_error'],
                'angular_momentum_error': m['angular_momentum']['relative_error'],
                'wall_time': m['wall_time_seconds'],
                'cpu_time': m['cpu_time_seconds'],
                'cpu_utilization': m['efficiency']['cpu_utilization']
            })
    
    # Process standard metrics
    for m in std_metrics:
        if 'error' not in m:
            summary_data.append({
                'type': 'standard',
                'sim_number': m['sim_number'],
                'energy_error': m['energy']['relative_error'],
                'momentum_error': m['linear_momentum']['relative_error'],
                'angular_momentum_error': m['angular_momentum']['relative_error'],
                'wall_time': m['wall_time_seconds'],
                'cpu_time': m['cpu_time_seconds'],
                'cpu_utilization': m['efficiency']['cpu_utilization']
            })
    
    if summary_data:
        df = pd.DataFrame(summary_data)
        csv_path = BASE_DIR / 'metrics_summary.csv'
        df.to_csv(csv_path, index=False)
        print(f"\nSummary CSV saved to: {csv_path}")
    print(f"\nSimulation parameters used:")
    print(f"  Tolerance: 1e-15")
    print(f"  Word length: 130 bits")
    print(f"  Time interval: 0.08")
    print(f"  Expected snapshots: ~126 (t=0 to t=10 with dt=0.08)")

def main():
    print("Brutus Simulation Metrics Analysis")
    print("=" * 50)
    print(f"Analysis started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load metrics
    hier_metrics = load_metrics(METRICS_DIRS["hierarchical"])
    std_metrics = load_metrics(METRICS_DIRS["standard"])
    
    # Analyze conservation properties
    hier_data = analyze_conservation(hier_metrics, "hierarchical")
    std_data = analyze_conservation(std_metrics, "standard")
    
    # Create plots
    if hier_data or std_data:
        create_plots(hier_data, std_data)
    
    # Save summary CSV
    save_summary_csv(hier_metrics, std_metrics)
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()
