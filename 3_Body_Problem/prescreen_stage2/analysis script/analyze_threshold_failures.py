#!/usr/bin/env python3
"""
Analyze the failed prescreening results to determine appropriate thresholds.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict, List
import pandas as pd
from collections import Counter

def load_all_prescreening_results(directory: str) -> Dict[str, List]:
    """
    Loads all prescreening results from JSON files in the given directory.
    Handles nested "datasets" structure if present.
    """
    all_detailed_results = []
    total_summary = Counter()
    all_failure_reasons = Counter()

    if not os.path.isdir(directory):
        print(f"Directory not found: {directory}")
        return {'detailed_results': []}

    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    if not json_files:
        print(f"No JSON files found in {directory}")
        return {'detailed_results': []}

    print(f"Processing {len(json_files)} file(s) from {directory}")

    for file_name in json_files:
        file_path = os.path.join(directory, file_name)
        try:
            results = json.load(open(file_path, 'r'))
            
            # Handle nested "datasets" structure if present
            if "datasets" in results and isinstance(results["datasets"], list):
                datasets = results["datasets"]
            else:
                # Treat as single dataset (flat structure)
                datasets = [results]
            
            for ds in datasets:
                # Process each dataset (nested or flat)
                if 'detailed_results' in ds:
                    all_detailed_results.extend(ds['detailed_results'])
                
                run_info = ds.get('run_info', {})
                total_summary['total_files'] += run_info.get('files_processed', 0)
                total_summary['passed'] += run_info.get('files_passed', 0)
                total_summary['failed'] += run_info.get('files_failed', 0)
                total_summary['elapsed_time'] += run_info.get('elapsed_time', 0)
                
                all_failure_reasons.update(ds.get('failure_reasons', {}))
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Could not process file {file_name}: {e}")

    if not all_detailed_results:
        print("No valid results found in any of the files.")
        return {'detailed_results': []}

    if total_summary['total_files'] > 0:
        total_summary['pass_rate'] = total_summary['passed'] / total_summary['total_files']
    else:
        total_summary['pass_rate'] = 0.0

    # Although the script primarily uses detailed_results, include summary for completeness
    return {
        'summary': dict(total_summary),
        'failure_reasons': dict(all_failure_reasons),
        'detailed_results': all_detailed_results,
    }

def plot_threshold_sensitivity(df: pd.DataFrame, output_dir: str):
    """
    Generates line plots showing the percentage of ICs that would pass
    as a function of changing threshold values.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Threshold Sensitivity Analysis", fontsize=16)

    # --- Virial Ratio Sensitivity ---
    q_mins = np.linspace(0, df['virial_ratio'].quantile(0.5), 50)
    q_max = 1.5 # Assume a fixed upper bound for this analysis
    pass_rates = [np.mean((df['virial_ratio'] >= qm) & (df['virial_ratio'] <= q_max)) * 100 for qm in q_mins]
    axes[0].plot(q_mins, pass_rates)
    axes[0].set_xlabel("Minimum Virial Ratio Threshold (Q_min)")
    axes[0].set_ylabel("Percent of ICs Passing (%)")
    axes[0].set_title("Impact of Q_min (with Q_max=1.5)")
    axes[0].grid(True, linestyle='--', alpha=0.6)

    # --- Angular Momentum Sensitivity ---
    l_mins = np.linspace(0, df['angular_momentum'].quantile(0.5), 50)
    pass_rates = [np.mean(df['angular_momentum'] >= lm) * 100 for lm in l_mins]
    axes[1].plot(l_mins, pass_rates)
    axes[1].set_xlabel("Minimum Angular Momentum Threshold (L_min)")
    axes[1].set_ylabel("Percent of ICs Passing (%)")
    axes[1].set_title("Impact of L_min")
    axes[1].grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    out_path = os.path.join(output_dir, "threshold_sensitivity.png")
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {out_path}")
    return fig

def plot_interactive_recommendation(df: pd.DataFrame, output_dir: str):
    """
    Creates a scatter plot of all ICs and overlays a shaded "acceptance region"
    based on percentile-based threshold recommendations.
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # --- Calculate Recommended Thresholds ---
    q_min_rec = df['virial_ratio'].quantile(0.10)  # Filter bottom 10%
    q_max_rec = df['virial_ratio'].quantile(0.99)  # Filter top 1%
    l_min_rec = df['angular_momentum'].quantile(0.10) # Filter bottom 10%

    # --- Calculate Pass Rate for these thresholds ---
    passed_region = (df['virial_ratio'] >= q_min_rec) & \
                    (df['virial_ratio'] <= q_max_rec) & \
                    (df['angular_momentum'] >= l_min_rec)
    pass_rate = np.mean(passed_region) * 100

    # --- Plot all ICs ---
    sns.scatterplot(
        data=df, x='virial_ratio', y='angular_momentum',
        alpha=0.2, ax=ax, label='All ICs'
    )

    # --- Draw the shaded "Acceptance Region" ---
    ylims = ax.get_ylim()
    ymin_frac = (l_min_rec - ylims[0]) / (ylims[1] - ylims[0])
    ymax_frac = 1.0
    ax.axvspan(q_min_rec, q_max_rec, ymin=ymin_frac, ymax=ymax_frac,
               facecolor='green', alpha=0.3, label='Recommended Pass Region')

    ax.axhline(y=l_min_rec, color='green', linestyle='--', label=f'L_min = {l_min_rec:.2f}')

    ax.set_title(f"Visual Threshold Recommendation (Passes ~{pass_rate:.0f}% of ICs)")
    ax.set_xlabel("Virial Ratio")
    ax.set_ylabel("Angular Momentum")
    ax.legend()

    plt.tight_layout()
    out_path = os.path.join(output_dir, "threshold_recommendation.png")
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {out_path}")
    return fig

def main():
    """Main analysis function."""
    results_dir = "3_Body_Problem/prescreen_stage2/prescreen_run_results"
    output_dir = "3_Body_Problem/prescreen_stage2/analysis_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load all results from all JSON files
    results = load_all_prescreening_results(results_dir)
    if not results or not results['detailed_results']:
        print("No results to analyze.")
        return

    # Convert to a DataFrame for easier analysis
    df = pd.DataFrame(results['detailed_results'])
    
    # Check if necessary columns exist
    if 'virial_ratio' not in df.columns or 'angular_momentum' not in df.columns:
        print("Required columns for threshold analysis are missing.")
        return

    print("\nGenerating threshold analysis figures...")
    
    # Generate the new plots
    fig1 = plot_threshold_sensitivity(df, output_dir)
    fig2 = plot_interactive_recommendation(df, output_dir)

    print(f"\nDisplaying 2 figure(s). Close all windows to exit.")
    plt.show()
    
    plt.close(fig1)
    plt.close(fig2)

    print("\nThreshold analysis complete. Figures saved to:", output_dir)

if __name__ == "__main__":
    main()