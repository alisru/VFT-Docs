import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# Parameters
grid_size = 20
num_frames = 60
wave_speed = 1.0
drag_threshold = 1.5

# Initialize grid (Macro cells, 1s/s frame)
# 0 = empty space, 1 = active boundary, >1 = subdivided micro-frame density
grid = np.zeros((grid_size, grid_size, grid_size))

# Setup figure
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(0, grid_size)
ax.set_ylim(0, grid_size)
ax.set_zlim(0, grid_size)
ax.set_title("Relative Homogeneous Scope:\nOrthogonal Time Dilation & Cell Subdivision")
ax.set_xlabel("X (Space Frame)")
ax.set_ylabel("Y (Space Frame)")
ax.set_zlabel("Z (Space Frame)")

# Initial wave positions (Orthogonal 2D waves)
wave1_x = 0
wave2_y = grid_size - 1

def update(frame):
    global grid, wave1_x, wave2_y
    ax.clear()
    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_zlim(0, grid_size)
    ax.set_title(f"Timephase: {frame} | Relative Homogeneous Scope")

    # Reset macro grid slightly (cooling/dissipation)
    grid = grid * 0.9

    # Propagate waves
    if frame < grid_size / 2:
        # Wave 1 moving +x
        wave1_x = int(frame * wave_speed)
        if wave1_x < grid_size:
            grid[wave1_x, :, grid_size//2] += 1.0

        # Wave 2 moving -y
        wave2_y = int(grid_size - 1 - frame * wave_speed)
        if wave2_y >= 0:
            grid[:, wave2_y, grid_size//2] += 1.0

    # Check for subdivision (intersection)
    # Where density > drag_threshold, cell subdivides (represented by higher integer values/colors)
    subdivided = np.where(grid > drag_threshold)

    if len(subdivided[0]) > 0:
        # 0-1-2 Unit logic: 2c space applies inward opposition
        # The subdivided cells pull neighboring energy into a rotational cluster (voxel ball)
        cx, cy, cz = np.mean(subdivided[0]), np.mean(subdivided[1]), np.mean(subdivided[2])

        # Localized Temporal Drag: Convert linear to rotational density
        for x, y, z in zip(subdivided[0], subdivided[1], subdivided[2]):
            # Increase density drastically to represent the 0.1s/s micro-frame chaotic interaction
            grid[x, y, z] += 0.5

            # Simulated rotation/orbiting of micro-frames around the center of mass
            # We don't move "particles", we transfer cell energy orthogonally
            dx = x - cx
            dy = y - cy

            # Simple orthogonal transfer (curl)
            nx = int(np.clip(cx - dy, 0, grid_size-1))
            ny = int(np.clip(cy + dx, 0, grid_size-1))

            if grid[nx, ny, z] < grid[x, y, z]:
                transfer = grid[x, y, z] * 0.2
                grid[nx, ny, z] += transfer
                grid[x, y, z] -= transfer

    # Plot voxels
    x, y, z = np.where(grid > 0.2)
    colors = grid[x, y, z]

    # Colormap: low energy = blue (macro), high energy = red (micro/subdivided)
    sc = ax.scatter(x, y, z, c=colors, cmap='coolwarm', s=colors*100, alpha=0.6, marker='s')

    return sc,

# Create animation
ani = animation.FuncAnimation(fig, update, frames=num_frames, interval=100, blit=False)

# Save animation
try:
    ani.save('homogeneous_scope_subdivision.gif', writer='imagemagick')
    print("Successfully generated homogeneous_scope_subdivision.gif")
except Exception as e:
    print(f"Imagemagick failed, trying Pillow: {e}")
    try:
        ani.save('homogeneous_scope_subdivision.gif', writer='pillow')
        print("Successfully generated homogeneous_scope_subdivision.gif using Pillow")
    except Exception as e:
        print(f"Failed to generate gif: {e}")
