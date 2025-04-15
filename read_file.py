import numpy as np
import matplotlib.pyplot as plt

def read_and_plot_waypoints(track_file):
    # Load the waypoints from the .npy file
    waypoints = np.load(track_file)
    
    # Print basic information about the waypoints
    print(f"\nTrack file: {track_file}")
    print(f"Number of waypoints: {len(waypoints)}")
    print(f"Shape of waypoints array: {waypoints.shape}")
    print("\nFirst few waypoints:")
    print(waypoints[:5])
    
    # Plot the waypoints
    plt.figure(figsize=(10, 10))
    plt.plot(waypoints[:, 0], waypoints[:, 1], 'b-', label='Track')
    plt.plot(waypoints[:, 0], waypoints[:, 1], 'ro', markersize=2, label='Waypoints')
    plt.title(f'Track Visualization: {track_file}')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_ccw_track():
    # Load the counter-clockwise track
    waypoints = np.load('reInvent2019_track_ccw.npy')
    
    # Create a figure with three subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # Plot 1: Track with waypoint numbers
    ax1.plot(waypoints[:, 0], waypoints[:, 1], 'b-', label='Center Line')
    ax1.plot(waypoints[:, 2], waypoints[:, 3], 'g-', label='Inner Boundary')
    ax1.plot(waypoints[:, 4], waypoints[:, 5], 'r-', label='Outer Boundary')
    
    # Add waypoint numbers
    for i, (x, y) in enumerate(zip(waypoints[:, 0], waypoints[:, 1])):
        ax1.text(x, y, str(i), fontsize=8, ha='center', va='center')
    
    ax1.set_title('Track with Waypoint Numbers')
    ax1.set_xlabel('X coordinate')
    ax1.set_ylabel('Y coordinate')
    ax1.axis('equal')
    ax1.grid(True)
    ax1.legend()
    
    # Plot 2: Detailed waypoint information
    ax2.axis('off')
    waypoint_info = []
    for i, wp in enumerate(waypoints):
        waypoint_info.append(f"Waypoint {i}:")
        waypoint_info.append(f"  Center: ({wp[0]:.2f}, {wp[1]:.2f})")
        waypoint_info.append(f"  Inner:  ({wp[2]:.2f}, {wp[3]:.2f})")
        waypoint_info.append(f"  Outer:  ({wp[4]:.2f}, {wp[5]:.2f})")
        waypoint_info.append("")
    
    ax2.text(0.1, 0.95, "\n".join(waypoint_info), 
             fontfamily='monospace', 
             verticalalignment='top',
             fontsize=8)
    
    plt.tight_layout()
    plt.show()
    
    # Print summary information
    print(f"\nCounter-Clockwise Track Summary:")
    print(f"Total waypoints: {len(waypoints)}")
    print(f"Track length: {len(waypoints)} waypoints")
    print("\nFirst 5 waypoints details:")
    for i in range(5):
        wp = waypoints[i]
        print(f"\nWaypoint {i}:")
        print(f"  Center: ({wp[0]:.2f}, {wp[1]:.2f})")
        print(f"  Inner:  ({wp[2]:.2f}, {wp[3]:.2f})")
        print(f"  Outer:  ({wp[4]:.2f}, {wp[5]:.2f})")

# Read and plot each track file
track_files = ['reInvent2019_track.npy', 'reInvent2019_track_cw.npy', 'reInvent2019_track_ccw.npy']

for track_file in track_files:
    try:
        read_and_plot_waypoints(track_file)
    except Exception as e:
        print(f"Error reading {track_file}: {e}")

# Run the visualization
plot_ccw_track()
