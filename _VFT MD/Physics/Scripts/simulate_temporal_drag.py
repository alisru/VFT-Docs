import numpy as np
import matplotlib.pyplot as plt

# Simulate Gravity as Temporal Drag with the 2c Breakthrough Mechanic
# A wave packet moves past a dense mass. The side closer to the mass updates slower (high drag/low D).
# However, if the vector has enough energy and the density exceeds the '2c' threshold (event horizon),
# the structural constraint breaks. The vector enters a faster, unopposed timephase (D resets to 1.0)
# and shoots through the space.

grid_size = 200
time_ticks = 400

y, x = np.ogrid[0:grid_size, 0:grid_size]

# 1. Define the Mass and the 2c Threshold
center_x, center_y = 100, 100
mass_radius = 20
distance_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)

epsilon = 1.0
density_map = 1000.0 / (distance_from_center**2 + epsilon)
# Instead of capping at 10, we let the core reach extreme densities
# We define the "2c structural limit" at density = 8.0
limit_2c = 8.0
event_horizon_mask = density_map >= limit_2c

# 2. Calculate the Temporal Drag Field (D)
k = 0.5
drag_field_D = 1.0 / (1.0 + k * density_map)

# APPLY THE BREAKTHROUGH: Inside the 2c limit, the structural frame breaks.
# The space becomes unopposed (a new timephase), so D resets to a fast state (1.0)
drag_field_D[event_horizon_mask] = 1.0

# 3. Initialize the Vector Wave Packet
packet_pos = np.array([40.0, 10.0]) # [x, y]
packet_vel = np.array([0.0, 1.0])   # Initial velocity straight down
packet_width = 4.0

trajectory_x = []
trajectory_y = []

# 4. Simulate the Grid Processing (Universal Ticks)
for t in range(time_ticks):
    trajectory_x.append(packet_pos[0])
    trajectory_y.append(packet_pos[1])

    px, py = int(np.clip(packet_pos[0], 0, grid_size-1)), int(np.clip(packet_pos[1], 0, grid_size-1))

    speed = np.linalg.norm(packet_vel)
    if speed == 0: break

    normal = np.array([-packet_vel[1], packet_vel[0]]) / speed

    side1_pos = packet_pos + normal * (packet_width / 2.0)
    side2_pos = packet_pos - normal * (packet_width / 2.0)

    s1x, s1y = int(np.clip(side1_pos[0], 0, grid_size-1)), int(np.clip(side1_pos[1], 0, grid_size-1))
    s2x, s2y = int(np.clip(side2_pos[0], 0, grid_size-1)), int(np.clip(side2_pos[1], 0, grid_size-1))

    D_side1 = drag_field_D[s1y, s1x]
    D_side2 = drag_field_D[s2y, s2x]

    # Gradient of drag across the packet width
    dD = D_side2 - D_side1

    rotation_rate = 0.6
    theta = dD * rotation_rate

    rot_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                           [np.sin(theta),  np.cos(theta)]])

    packet_vel = np.dot(rot_matrix, packet_vel)

    # Throttled movement based on local processing speed
    D_center = drag_field_D[py, px]
    packet_pos += packet_vel * D_center

# 5. Plotting Results
fig, ax = plt.subplots(figsize=(10, 8))

# Plot the Temporal Drag Field (D)
im = ax.imshow(drag_field_D, cmap='inferno', origin='upper')
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Temporal Drag $D$ (Processing Speed)')

# Plot the Mass core
circle = plt.Circle((center_x, center_y), mass_radius, color='cyan', fill=False, linestyle='--', linewidth=2, label='Gravitational Well')
ax.add_patch(circle)

# Plot the Trajectory
ax.plot(trajectory_x, trajectory_y, color='white', linewidth=2, label='Vector Trajectory')

# Highlight the breakthrough point
ax.scatter(trajectory_x[0], trajectory_y[0], color='green', s=100, label='Start', zorder=5)
ax.scatter(trajectory_x[-1], trajectory_y[-1], color='red', s=100, label='End (Breaks through 2c Core)', zorder=5)

ax.set_title("Temporal Drag and the '2c' Phase Breakthrough\nVector overpowers constraint and enters unopposed timephase")
ax.legend(loc='upper right')
ax.axis('off')

plt.tight_layout()
plt.savefig("_VFT MD/Physics/Scripts/temporal_drag_breakthrough.png", dpi=150)
print("Plot saved to _VFT MD/Physics/Scripts/temporal_drag_breakthrough.png")
