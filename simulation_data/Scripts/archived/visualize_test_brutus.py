import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.widgets import Slider

def parse_brutus_output(filename):
    """Parse the Brutus output file and extract positions over time."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    snapshots = []
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        if line and len(line.split()) == 3:  # Header line
            parts = line.split()
            time = float(parts[0])
            n_bodies = int(parts[1])
            
            positions = []
            velocities = []
            masses = []
            
            # Read n_bodies lines
            for j in range(n_bodies):
                i += 1
                body_data = lines[i].strip().split()
                mass = float(body_data[0])
                x, y, z = float(body_data[1]), float(body_data[2]), float(body_data[3])
                vx, vy, vz = float(body_data[4]), float(body_data[5]), float(body_data[6])
                
                masses.append(mass)
                positions.append([x, y, z])
                velocities.append([vx, vy, vz])
            
            snapshots.append({
                'time': time,
                'positions': np.array(positions),
                'velocities': np.array(velocities),
                'masses': np.array(masses)
            })
        i += 1
    
    return snapshots

def plot_trajectories_3d(snapshots, body_indices=None):
    """Create a 3D plot of the trajectories."""
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    n_bodies = len(snapshots[0]['positions'])
    if body_indices is None:
        body_indices = range(n_bodies)
    
    # Use a colormap for different bodies
    colors = plt.cm.rainbow(np.linspace(0, 1, len(body_indices)))
    
    # Plot trajectories
    for idx, body_idx in enumerate(body_indices):
        trajectory = np.array([snap['positions'][body_idx] for snap in snapshots])
        ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], 
                color=colors[idx], alpha=0.7, linewidth=1.5, 
                label=f'Body {body_idx+1}')
        
        # Mark initial position
        ax.scatter(trajectory[0, 0], trajectory[0, 1], trajectory[0, 2], 
                  color=colors[idx], s=100, marker='o', edgecolor='black', 
                  linewidth=2, alpha=1.0)
        
        # Mark final position
        ax.scatter(trajectory[-1, 0], trajectory[-1, 1], trajectory[-1, 2], 
                  color=colors[idx], s=100, marker='s', edgecolor='black', 
                  linewidth=2, alpha=1.0)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'3-body Simulation Trajectories (t=0 to t={snapshots[-1]["time"]:.1f})')
    
    # Add legend with scroll if too many bodies
    if len(body_indices) <= 8:
        ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    
    plt.tight_layout()
    return fig, ax

def plot_trajectories_2d_projections(snapshots, body_indices=None):
    """Create 2D projections of the trajectories."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    n_bodies = len(snapshots[0]['positions'])
    if body_indices is None:
        body_indices = range(n_bodies)
    
    colors = plt.cm.rainbow(np.linspace(0, 1, len(body_indices)))
    
    # XY projection
    ax = axes[0, 0]
    for idx, body_idx in enumerate(body_indices):
        trajectory = np.array([snap['positions'][body_idx] for snap in snapshots])
        ax.plot(trajectory[:, 0], trajectory[:, 1], 
                color=colors[idx], alpha=0.7, linewidth=1.5)
        ax.scatter(trajectory[0, 0], trajectory[0, 1], 
                  color=colors[idx], s=50, marker='o', edgecolor='black')
        ax.scatter(trajectory[-1, 0], trajectory[-1, 1], 
                  color=colors[idx], s=50, marker='s', edgecolor='black')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('XY Projection')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')
    
    # XZ projection
    ax = axes[0, 1]
    for idx, body_idx in enumerate(body_indices):
        trajectory = np.array([snap['positions'][body_idx] for snap in snapshots])
        ax.plot(trajectory[:, 0], trajectory[:, 2], 
                color=colors[idx], alpha=0.7, linewidth=1.5)
        ax.scatter(trajectory[0, 0], trajectory[0, 2], 
                  color=colors[idx], s=50, marker='o', edgecolor='black')
        ax.scatter(trajectory[-1, 0], trajectory[-1, 2], 
                  color=colors[idx], s=50, marker='s', edgecolor='black')
    ax.set_xlabel('X')
    ax.set_ylabel('Z')
    ax.set_title('XZ Projection')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')
    
    # YZ projection
    ax = axes[1, 0]
    for idx, body_idx in enumerate(body_indices):
        trajectory = np.array([snap['positions'][body_idx] for snap in snapshots])
        ax.plot(trajectory[:, 1], trajectory[:, 2], 
                color=colors[idx], alpha=0.7, linewidth=1.5)
        ax.scatter(trajectory[0, 1], trajectory[0, 2], 
                  color=colors[idx], s=50, marker='o', edgecolor='black')
        ax.scatter(trajectory[-1, 1], trajectory[-1, 2], 
                  color=colors[idx], s=50, marker='s', edgecolor='black')
    ax.set_xlabel('Y')
    ax.set_ylabel('Z')
    ax.set_title('YZ Projection')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')
    
    # Time evolution of distances from origin
    ax = axes[1, 1]
    times = [snap['time'] for snap in snapshots]
    for idx, body_idx in enumerate(body_indices):
        distances = []
        for snap in snapshots:
            pos = snap['positions'][body_idx]
            dist = np.sqrt(pos[0]**2 + pos[1]**2 + pos[2]**2)
            distances.append(dist)
        ax.plot(times, distances, color=colors[idx], alpha=0.7, linewidth=1.5,
                label=f'Body {body_idx+1}')
    ax.set_xlabel('Time')
    ax.set_ylabel('Distance from Origin')
    ax.set_title('Radial Distance Evolution')
    ax.grid(True, alpha=0.3)
    if len(body_indices) <= 8:
        ax.legend(loc='best', fontsize=8)
    
    plt.suptitle(f'3-Body Simulation (t=0 to t={snapshots[-1]["time"]:.1f})', 
                 fontsize=16)
    plt.tight_layout()
    
    return fig

def create_animation(snapshots, body_indices=None, interval=50):
    """Create an animation of the simulation."""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    n_bodies = len(snapshots[0]['positions'])
    if body_indices is None:
        body_indices = range(min(n_bodies, 8))  # Limit to 8 bodies for clarity
    
    colors = plt.cm.rainbow(np.linspace(0, 1, len(body_indices)))
    
    # Initialize scatter plot
    scatters = []
    for idx, color in enumerate(colors):
        scatter = ax.scatter([], [], [], c=[color], s=100, alpha=0.8)
        scatters.append(scatter)
    
    # Initialize trajectory lines
    lines = []
    for idx, color in enumerate(colors):
        line, = ax.plot([], [], [], color=color, alpha=0.3, linewidth=1)
        lines.append(line)
    
    # Set axis limits
    all_positions = np.concatenate([snap['positions'] for snap in snapshots])
    ax.set_xlim(all_positions[:, 0].min()*1.1, all_positions[:, 0].max()*1.1)
    ax.set_ylim(all_positions[:, 1].min()*1.1, all_positions[:, 1].max()*1.1)
    ax.set_zlim(all_positions[:, 2].min()*1.1, all_positions[:, 2].max()*1.1)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    time_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes)
    
    def init():
        for scatter in scatters:
            scatter._offsets3d = ([], [], [])
        for line in lines:
            line.set_data([], [])
            line.set_3d_properties([])
        time_text.set_text('')
        return scatters + lines + [time_text]
    
    def animate(frame):
        snapshot = snapshots[frame]
        time_text.set_text(f'Time: {snapshot["time"]:.3f}')
        
        for idx, body_idx in enumerate(body_indices):
            # Update scatter position
            pos = snapshot['positions'][body_idx]
            scatters[idx]._offsets3d = ([pos[0]], [pos[1]], [pos[2]])
            
            # Update trajectory trail
            trail_positions = np.array([snapshots[j]['positions'][body_idx] 
                                      for j in range(max(0, frame-20), frame+1)])
            if len(trail_positions) > 0:
                lines[idx].set_data(trail_positions[:, 0], trail_positions[:, 1])
                lines[idx].set_3d_properties(trail_positions[:, 2])
        
        ax.set_title(f'3-body Simulation Animation (showing {len(body_indices)} bodies)')
        return scatters + lines + [time_text]
    
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                 frames=len(snapshots), interval=interval,
                                 blit=True, repeat=True)
    
    return fig, anim

def plot_energy_analysis(snapshots):
    """Plot energy analysis of the system."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    times = [snap['time'] for snap in snapshots]
    kinetic_energies = []
    potential_energies = []
    
    G = 1.0  # Gravitational constant (assumed to be 1 in N-body units)
    
    for snap in snapshots:
        # Kinetic energy
        KE = 0.5 * np.sum(snap['masses'][:, np.newaxis] * 
                         np.sum(snap['velocities']**2, axis=1))
        kinetic_energies.append(KE)
        
        # Potential energy
        PE = 0
        n_bodies = len(snap['positions'])
        for i in range(n_bodies):
            for j in range(i+1, n_bodies):
                r = np.linalg.norm(snap['positions'][i] - snap['positions'][j])
                PE -= G * snap['masses'][i] * snap['masses'][j] / r
        potential_energies.append(PE)
    
    kinetic_energies = np.array(kinetic_energies)
    potential_energies = np.array(potential_energies)
    total_energies = kinetic_energies + potential_energies
    
    # Plot kinetic energy
    ax = axes[0, 0]
    ax.plot(times, kinetic_energies, 'r-', linewidth=2)
    ax.set_xlabel('Time')
    ax.set_ylabel('Kinetic Energy')
    ax.set_title('Kinetic Energy vs Time')
    ax.grid(True, alpha=0.3)
    
    # Plot potential energy
    ax = axes[0, 1]
    ax.plot(times, potential_energies, 'b-', linewidth=2)
    ax.set_xlabel('Time')
    ax.set_ylabel('Potential Energy')
    ax.set_title('Potential Energy vs Time')
    ax.grid(True, alpha=0.3)
    
    # Plot total energy
    ax = axes[1, 0]
    ax.plot(times, total_energies, 'g-', linewidth=2)
    ax.set_xlabel('Time')
    ax.set_ylabel('Total Energy')
    ax.set_title('Total Energy vs Time')
    ax.grid(True, alpha=0.3)
    
    # Plot energy conservation error
    ax = axes[1, 1]
    energy_error = (total_energies - total_energies[0]) / abs(total_energies[0]) * 100
    ax.plot(times, energy_error, 'k-', linewidth=2)
    ax.set_xlabel('Time')
    ax.set_ylabel('Energy Error (%)')
    ax.set_title('Relative Energy Conservation Error')
    ax.grid(True, alpha=0.3)
    
    plt.suptitle('Energy Analysis of 3-Body System', fontsize=16)
    plt.tight_layout()
    
    return fig

# Main execution
if __name__ == "__main__":
    # Parse the output file
    filename = '<home>/Desktop/cursor/3_Body_Problem/brutus_output/brutus_hierarchical_gold_standard/brutus_hierarchical_4951.txt'  # Change this to your output file name
    snapshots = parse_brutus_output(filename)
    
    print(f"Loaded {len(snapshots)} snapshots")
    print(f"Simulation time: {snapshots[0]['time']} to {snapshots[-1]['time']}")
    print(f"Number of bodies: {len(snapshots[0]['positions'])}")
    
    # Create visualizations
    fig1, ax1 = plot_trajectories_3d(snapshots)
    plt.savefig('brutus_Newton-main/3d_trajectories.png')
    
    # 2. 2D projections (showing all bodies)
    fig2 = plot_trajectories_2d_projections(snapshots)
    plt.savefig('brutus_Newton-main/2d_projections.png')
    
    # 3. Energy analysis
    fig3 = plot_energy_analysis(snapshots)
    plt.savefig('brutus_Newton-main/energy_analysis.png')
    # 4. Animation (optional - uncomment to create)
    # fig4, anim = create_animation(snapshots, body_indices=range(8))
    # To save animation: anim.save('brutus_animation.mp4', fps=30)   
    
    plt.show()