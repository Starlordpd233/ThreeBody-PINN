# metrics_analysis.py

"""
To run:
python <home>/Desktop/cursor/3_Body_Problem/analyze_data_generation/metrics_analysis.py hist      
python <home>/Desktop/cursor/3_Body_Problem/analyze_data_generation/metrics_analysis.py heatmap   
python <home>/Desktop/cursor/3_Body_Problem/analyze_data_generation/metrics_analysis.py scatter   
python <home>/Desktop/cursor/3_Body_Problem/analyze_data_generation/metrics_analysis.py xyz       

"""


import glob
import numpy as np
import matplotlib.pyplot as plt
from utils import load_metrics  # should return dict with 'duration', 'positions', 'energy_error', etc.
import matplotlib.colors as colors

def histogram_simulation_times(folder, show_plot=False):
    times = []
    files_processed = 0
    for f in glob.glob(f"{folder}/*.json"):
        data = load_metrics(f)
        if data and 'duration' in data:
            times.append(data['duration'])
            files_processed += 1
    
    print(f"Processed {files_processed} files, found {len(times)} valid duration values")
    
    if not times:
        print("No valid duration data found!")
        return
    
    plt.figure(figsize=(10, 6))
    plt.hist(times, bins=30, alpha=0.7)
    plt.title('Simulation Time Distribution')
    plt.xlabel('Duration')
    plt.ylabel('Count')
    
    output_path = '<home>/Desktop/cursor/3_Body_Problem/analyze_data_generation/figures/metrics_analysis/simulation_times_histogram.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Histogram saved to: {output_path}")
    
    if show_plot:
        plt.show()
    plt.close()

def heatmap_pos2_vs_duration(folder, show_plot=False):
    data = []
    files_processed = 0
    for f in glob.glob(f"{folder}/*.json"):
        d = load_metrics(f)
        files_processed += 1
        if d and 'positions' in d and 'duration' in d and len(d['positions']) > 1:
            data.append(d)
    
    print(f"Processed {files_processed} files, found {len(data)} valid data points for heatmap")
    
    if not data:
        print("No valid data found for heatmap!")
        return
    
    pos2x = [d['positions'][1][0] for d in data]
    durations = [d['duration'] for d in data]
    
    plt.figure(figsize=(10, 6))
    plt.hexbin(pos2x, durations, gridsize=30, cmap='inferno', 
               norm=colors.PowerNorm(gamma=0.5), mincnt=1)
    plt.xlabel('Particle 2 Initial X')
    plt.ylabel('Simulation Duration')
    plt.title('Position 2 vs Duration')
    plt.colorbar(label='Count')
    
    output_path = '<home>/Desktop/cursor/3_Body_Problem/analyze_data_generation/figures/metrics_analysis/pos2_vs_duration_heatmap.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Heatmap saved to: {output_path}")
    
    if show_plot:
        plt.show()
    plt.close()

def scatter_ic_vs_energy(folder, show_plot=False):
    data = []
    files_processed = 0
    for f in glob.glob(f"{folder}/*.json"):
        d = load_metrics(f)
        files_processed += 1
        if d and 'initial_param' in d and 'energy_error' in d:
            data.append(d)
    
    print(f"Processed {files_processed} files, found {len(data)} valid data points for scatter plot")
    
    if not data:
        print("No valid data found for scatter plot!")
        return
    
    ic_param = [d['initial_param'] for d in data]
    energy = [d['energy_error'] for d in data]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(ic_param, energy, alpha=0.6)
    plt.xlabel('IC Parameter')
    plt.ylabel('Max Energy Error')
    plt.title('IC vs Energy Conservation')
    
    output_path = '<home>/Desktop/cursor/3_Body_Problem/analyze_data_generation/figures/metrics_analysis/ic_vs_energy_scatter.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Scatter plot saved to: {output_path}")
    
    if show_plot:
        plt.show()
    plt.close()

if __name__ == '__main__':
    import sys
    import os
    
    
    mode = sys.argv[1] if len(sys.argv)>1 else 'hist'
    folder = sys.argv[2] if len(sys.argv)>2 else '<home>/Desktop/cursor/3_Body_Problem/sim_result_metric_hierarchical'
    show_plots = '--show' in sys.argv  # Add --show flag to display plots
    
    print(f"Running metrics analysis with mode: {mode}, folder: {folder}")
    print(f"Show plots: {show_plots}")
    
    if mode == 'hist':
        histogram_simulation_times(folder, show_plots)
    elif mode == 'heatmap':
        heatmap_pos2_vs_duration(folder, show_plots)
    else:
        scatter_ic_vs_energy(folder, show_plots)