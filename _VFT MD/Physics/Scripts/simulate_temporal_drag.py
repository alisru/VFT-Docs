import numpy as np
import matplotlib.pyplot as plt

# Simulate Gravity as Temporal Drag (D)
# A wave packet moves past a dense mass. The side closer to the mass updates slower (high drag/low D).
# This asymmetric processing speed causes the vector to refract (wheel inward) toward the mass.

grid_size = 200
time_ticks = 400

# Setup Coordinate Grid
y, x = np.ogrid[0:grid_size, 0:grid_size]

# 1. Define the Mass (Fractional Density)
center_x, center_y = 100, 100
mass_radius = 20
distance_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)

# Fractional density drops off via inverse square to simulate a central mass
# We add a small epsilon to avoid division by zero
epsilon = 1.0
density_map = 1000.0 / (distance_from_center**2 + epsilon)
density_map[distance_from_center <= mass_radius] = 10.0 # Cap the core density

# 2. Calculate the Temporal Drag Field (D)
# D = 1 / (1 + k * density)
# Where D is processing speed (1.0 = vacuum speed, approaches 0 near mass)
k = 0.5
drag_field_D = 1.0 / (1.0 + k * density_map)

# 3. Initialize the Vector Wave Packet
# Starting at top left, moving straight down (y-direction) initially
packet_pos = np.array([50.0, 10.0]) # [x, y]
packet_vel = np.array([0.0, 1.0])   # Initial velocity straight down
packet_width = 4.0 # The spatial width of the wave packet

# Track trajectory for plotting
trajectory_x = []
trajectory_y = []

# 4. Simulate the Grid Processing (Universal Ticks)
for t in range(time_ticks):
    trajectory_x.append(packet_pos[0])
    trajectory_y.append(packet_pos[1])

    # Current grid indices (rounded)
    px, py = int(np.clip(packet_pos[0], 0, grid_size-1)), int(np.clip(packet_pos[1], 0, grid_size-1))

    # To calculate refraction, we sample the Drag (D) on the left and right sides of the packet
    # Since it's moving mostly in Y, the "sides" are along the X axis.
    # In a full simulation, this would use the cross product of velocity, but this is a 2D simplification.

    # Calculate normal vector (perpendicular to velocity) to find the "sides"
    speed = np.linalg.norm(packet_vel)
    if speed == 0: break

    # Normal points to the "right" of the velocity vector
    normal = np.array([-packet_vel[1], packet_vel[0]]) / speed

    side1_pos = packet_pos + normal * (packet_width / 2.0) # Right side
    side2_pos = packet_pos - normal * (packet_width / 2.0) # Left side

    s1x, s1y = int(np.clip(side1_pos[0], 0, grid_size-1)), int(np.clip(side1_pos[1], 0, grid_size-1))
    s2x, s2y = int(np.clip(side2_pos[0], 0, grid_size-1)), int(np.clip(side2_pos[1], 0, grid_size-1))

    D_side1 = drag_field_D[s1y, s1x] # Right side Drag
    D_side2 = drag_field_D[s2y, s2x] # Left side Drag

    # The gradient of Temporal Drag (del D)
    # The side with lower D processes slower. This causes the velocity vector to rotate.
    # The pivot turns toward the slower side.
    # If the right side (side1) is slower (lower D), it should turn right (positive theta).
    # Therefore, we want a positive theta when D_side1 < D_side2.
    dD = D_side2 - D_side1

    # Apply rotation based on asymmetric drag (Simulating General Relativity without curved space)
    # The angle change is proportional to the difference in processing speeds across its width
    rotation_rate = 0.5
    theta = dD * rotation_rate

    # Rotation matrix
    rot_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                           [np.sin(theta),  np.cos(theta)]])

    packet_vel = np.dot(rot_matrix, packet_vel)

    # 5. Move the packet
    # The absolute distance traveled this tick is throttled by the local Temporal Drag (D)
    D_center = drag_field_D[py, px]
    packet_pos += packet_vel * D_center

# 5. Plotting Results
fig, ax = plt.subplots(figsize=(10, 8))

# Plot the Temporal Drag Field (D)
# Darker = lower D (slower time/higher drag)
im = ax.imshow(drag_field_D, cmap='inferno', origin='upper')
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Temporal Drag $D$ (Processing Speed)')

# Plot the Mass core
circle = plt.Circle((center_x, center_y), mass_radius, color='cyan', fill=False, linestyle='--', linewidth=2, label='Mass Core (Fractional Density)')
ax.add_patch(circle)

# Plot the Trajectory
ax.plot(trajectory_x, trajectory_y, color='white', linewidth=2, label='Vector Trajectory')

# Plot start and end points
ax.scatter(trajectory_x[0], trajectory_y[0], color='green', s=100, label='Start', zorder=5)
ax.scatter(trajectory_x[-1], trajectory_y[-1], color='red', s=100, label='End', zorder=5)

ax.set_title("Gravity as Temporal Drag (Asymmetric Processing Speed)\nRefraction without Curved Spacetime")
ax.legend(loc='upper right')
ax.axis('off')

plt.tight_layout()
plt.savefig("_VFT MD/Physics/Scripts/temporal_drag_refraction.png", dpi=150)
print("Plot saved to _VFT MD/Physics/Scripts/temporal_drag_refraction.png")
