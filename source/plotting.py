import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def plot_prism(ax, x, y, z, dx, dy, dz, color, opacity=0.2):
    """Plots a rectangular prism centered at (x, y, z)."""
    x_min, x_max = x - dx / 2, x + dx / 2
    y_min, y_max = y - dy / 2, y + dy / 2
    z_min, z_max = z - dz / 2, z + dz / 2
    
    vertices = [
        [x_min, y_min, z_min], [x_max, y_min, z_min], [x_max, y_max, z_min], [x_min, y_max, z_min],
        [x_min, y_min, z_max], [x_max, y_min, z_max], [x_max, y_max, z_max], [x_min, y_max, z_max]
    ]
    
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # Bottom face
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # Top face
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # Side face 1
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # Side face 2
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # Side face 3
        [vertices[4], vertices[7], vertices[3], vertices[0]]   # Side face 4
    ]
    
    ax.add_collection3d(Poly3DCollection(faces, facecolors=color, alpha=opacity, linewidths=0.5, edgecolors='k'))
        

def plot_crystal_point_map(crystal_map_1, crystal_map_2):
    xlabel="x-axis [mm]"
    ylabel="y-axis [mm]"
    zlabel="z-axis [mm]"
    label_offset=(0.1, 0.1, 0.1)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # --- plot crystal map 1 data --- #
    
    # Extract labels and coordinates
    labels = [f"({int(row[0])}, {int(row[1])})" for row in crystal_map_1]
    x, y, z = crystal_map_1[:, 2], crystal_map_1[:, 3], crystal_map_1[:, 4]
    ax.scatter(x, y, z, c='b', marker='o')
    
    # Add labels
    for label, x_pos, y_pos, z_pos in zip(labels, x, y, z):
        ax.text(x_pos + label_offset[0], 
                y_pos + label_offset[1], 
                z_pos + label_offset[2], 
                label, fontsize=10, color='black')
    
    # --- plot crystal map 2 data --- #
    
    # Extract labels and coordinates
    labels = [f"({int(row[0])}, {int(row[1])})" for row in crystal_map_2]
    x, y, z = crystal_map_2[:, 2], crystal_map_2[:, 3], crystal_map_2[:, 4]
    ax.scatter(x, y, z, c='r', marker='o')
    
    # Add labels
    for label, x_pos, y_pos, z_pos in zip(labels, x, y, z):
        ax.text(x_pos + label_offset[0], 
                y_pos + label_offset[1], 
                z_pos + label_offset[2], 
                label, fontsize=10, color='black')
    
    # Set axis labels and title
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    
    plt.show()
    
    
def plot_crystal_surface_map(crystal_map_1, crystal_map_2,
                             crystal_x_width, crystal_y_width, crystal_z_width):
    xlabel="x-axis [mm]"
    ylabel="y-axis [mm]"
    zlabel="z-axis [mm]"
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # dimensions for rectangular prisms
    dx = crystal_x_width
    dy = crystal_y_width
    dz = crystal_z_width
    
    # --- plot crystal map 1 data --- #
    x, y, z = crystal_map_1[:, 2], crystal_map_1[:, 3], crystal_map_1[:, 4]
    for x_pos, y_pos, z_pos in zip(x, y, z):
        plot_prism(ax, x_pos, y_pos, z_pos, dx, dy, dz, color='blue')
    
    # --- plot crystal map 2 data --- #
    x, y, z = crystal_map_2[:, 2], crystal_map_2[:, 3], crystal_map_2[:, 4]
    for x_pos, y_pos, z_pos in zip(x, y, z):
        plot_prism(ax, x_pos, y_pos, z_pos, dx, dy, dz, color='red')
    
    # Set axis labels and title
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    
    ax.axes.set_xlim3d(left=-150, right=150) 
    ax.axes.set_ylim3d(bottom=-150, top=150) 
    ax.axes.set_zlim3d(bottom=-150, top=150) 
    
    plt.show()
    
    
def plot_electrode_point_map(top_electrode_map, bottom_electrode_map,
                             crystal_z_width, crystal_z_pitch):
    xlabel="x-axis [mm]"
    ylabel="y-axis [mm]"
    zlabel="z-axis [mm]"
    label_offset=(0.1, 0.1, 0.1)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # --- plot top crystal electrode data --- #
    
    # Extract labels and coordinates
    labels = [f"({int(row[0])}, {int(row[1])})" for row in top_electrode_map]
    x, y, z = top_electrode_map[:, 2], top_electrode_map[:, 3], top_electrode_map[:, 4]
    z += (crystal_z_width/2 + crystal_z_pitch/2)
    ax.scatter(x, y, z, c='b', marker='o')
    
    # Add labels
    for label, x_pos, y_pos, z_pos in zip(labels, x, y, z):
        ax.text(x_pos + label_offset[0], 
                y_pos + label_offset[1], 
                z_pos + label_offset[2], 
                label, fontsize=10, color='black')
    
    # --- plot bottom crystal electrode data --- #
    
    # Extract labels and coordinates
    labels = [f"({int(row[0])}, {int(row[1])})" for row in bottom_electrode_map]
    x, y, z = bottom_electrode_map[:, 2], bottom_electrode_map[:, 3], bottom_electrode_map[:, 4]
    z -= (crystal_z_width/2 + crystal_z_pitch/2)
    ax.scatter(x, y, z, c='r', marker='o')
    
    # Add labels
    for label, x_pos, y_pos, z_pos in zip(labels, x, y, z):
        ax.text(x_pos + label_offset[0], 
                y_pos + label_offset[1], 
                z_pos + label_offset[2], 
                label, fontsize=10, color='black')
    
    # Set axis labels and title
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    
    plt.show()
    

def plot_electrode_surface_map(top_electrode_map, bottom_electrode_map,
                               crystal_x_width, crystal_y_width,
                               crystal_z_width, crystal_z_pitch,
                               anode_strip_width, cathode_strip_width):
    xlabel="x-axis [mm]"
    ylabel="y-axis [mm]"
    zlabel="z-axis [mm]"
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    dz = 0.2
    
    # --- plot top crystal electrode data --- #
    
    x, y, z = top_electrode_map[:, 2], top_electrode_map[:, 3], top_electrode_map[:, 4]
    z_display = z + (crystal_z_width/2 + crystal_z_pitch/2)
    for i, (x_pos, y_pos, z_pos) in enumerate(zip(x, y, z_display)):
        if z[i] > 0:
            dx = anode_strip_width
            dy = crystal_y_width
        else:
            dx = crystal_x_width
            dy = cathode_strip_width
        plot_prism(ax, x_pos, y_pos, z_pos, dx, dy, dz, color='blue')
    
    # --- plot bottom crystal electrode data --- #
    
    x, y, z = bottom_electrode_map[:, 2], bottom_electrode_map[:, 3], bottom_electrode_map[:, 4]
    z_display = z - (crystal_z_width/2 + crystal_z_pitch/2)
    for i, (x_pos, y_pos, z_pos) in enumerate(zip(x, y, z_display)):
        if z[i] < 0:
            dx = anode_strip_width
            dy = crystal_y_width
        else:
            dx = crystal_x_width
            dy = cathode_strip_width
        plot_prism(ax, x_pos, y_pos, z_pos, dx, dy, dz, color='red')
    
    # --- plot crystals --- #
    
    x_pos, y_pos, z_pos = 0, 0, crystal_z_width/2 + crystal_z_pitch/2
    dx, dy, dz = crystal_x_width, crystal_y_width, crystal_z_width
    plot_prism(ax, x_pos, y_pos, z_pos, dx, dy, dz, color='black', opacity=0.1)
    plot_prism(ax, x_pos, y_pos, -z_pos, dx, dy, dz, color='black', opacity=0.1)
    
    # --- axis specs --- #
    
    # Set axis labels and title
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    
    ax.axes.set_xlim3d(left=-(crystal_x_width/2) * 1.1, right=(crystal_x_width/2) * 1.1) 
    ax.axes.set_ylim3d(bottom=-(crystal_y_width/2) * 1.1, top=(crystal_y_width/2) * 1.1) 
    ax.axes.set_zlim3d(bottom=-crystal_z_width * 1.1, top=crystal_z_width * 1.1) 
    
    plt.show()
    

def plot_test_channels(test_channel_map, crystal_map_1, crystal_map_2,
                       crystal_x_width, crystal_y_width, crystal_z_width):
    
    
    xlabel="x-axis [mm]"
    ylabel="y-axis [mm]"
    zlabel="z-axis [mm]"
    label_offset=(0.1, 0.1, 0.1)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # dimensions for rectangular prisms
    dx = crystal_x_width
    dy = crystal_y_width
    dz = crystal_z_width
    
    # --- plot crystal map 1 data --- #
    x, y, z = crystal_map_1[:, 2], crystal_map_1[:, 3], crystal_map_1[:, 4]
    for x_pos, y_pos, z_pos in zip(x, y, z):
        plot_prism(ax, x_pos, y_pos, z_pos, dx, dy, dz, color='blue', opacity=0.01)
    
    # --- plot crystal map 2 data --- #
    x, y, z = crystal_map_2[:, 2], crystal_map_2[:, 3], crystal_map_2[:, 4]
    for x_pos, y_pos, z_pos in zip(x, y, z):
        plot_prism(ax, x_pos, y_pos, z_pos, dx, dy, dz, color='red', opacity=0.01)
        
    # --- plot test channels --- #
    # Extract labels and coordinates
    labels = [f"({int(row[0])}, {int(row[1])}, {int(row[2])}, {int(row[3])})" for row in test_channel_map]
    x, y, z = test_channel_map[:, 4], test_channel_map[:, 5], test_channel_map[:, 6]
    ax.scatter(x, y, z, c='k', marker='o')
    
    # Add labels
    for label, x_pos, y_pos, z_pos in zip(labels, x, y, z):
        ax.text(x_pos + label_offset[0], 
                y_pos + label_offset[1], 
                z_pos + label_offset[2], 
                label, fontsize=10, color='black')
        
    # --- axis specs --- #
    
    # Set axis labels and title
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    
    ax.axes.set_xlim3d(left=-150, right=150) 
    ax.axes.set_ylim3d(bottom=-150, top=150) 
    ax.axes.set_zlim3d(bottom=-150, top=150) 
    
    plt.show()