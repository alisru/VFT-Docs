import numpy as np
import matplotlib.pyplot as plt

# Simulate Quantum Pair Production via "Constructive Grid Jamming"
# A high energy wave intersects an existing particle's Compton ring.
# The local grid capacity is overwhelmed, forcing an orthogonal time dilation lock
# that spins off a new stable particle shell (pair production).

grid_size = 200
y, x = np.ogrid[0:grid_size, 0:grid_size]

# Initialize grid capacities (Maximum vectors a cell can process per tick)
grid_capacity = np.full((grid_size, grid_size), 5.0)

# 1. Define the Pre-existing Stable Particle (Compton Frequency Ring)
particle_center = (100, 70)
particle_radius = 25
# A stable ring of energy representing the particle shell
distance_to_ring = np.abs(np.sqrt((x - particle_center[0])**2 + (y - particle_center[1])**2) - particle_radius)
existing_particle_energy = np.exp(-distance_to_ring**2 / 10.0) * 4.0 # Base energy just below capacity

# 2. Inject High-Energy Incoming Wave Vector
# A dense wave hitting the particle from the left
wave_x_pos = 75
wave_width = 5
incoming_wave_energy = np.zeros((grid_size, grid_size))
incoming_wave_energy[:, wave_x_pos-wave_width:wave_x_pos+wave_width] = 4.0

# 3. Calculate Collision and Grid Overload
total_energy = existing_particle_energy + incoming_wave_energy

# Where does the energy exceed the grid's processing capacity? (The Overload Threshold)
overload_mask = total_energy > grid_capacity

# 4. Trigger Orthogonal Split (Pair Production)
# The grid cannot process the excess linearly, so it forces an orthogonal 90-degree projection
# This generates a new localized feedback loop (a new electron/positron)
new_particle_energy = np.zeros((grid_size, grid_size))

# Find the center of the collision overload to act as the new "Ionizing Anchor"
if np.any(overload_mask):
    overload_y, overload_x = np.where(overload_mask)
    new_center = (int(np.mean(overload_x)), int(np.mean(overload_y)))

    # Generate the new Compton ring orthogonal (offset) to the collision
    # Shifted slightly right to represent the momentum of the incoming wave carrying it forward
    new_center = (new_center[0] + 30, new_center[1] + 30)
    new_radius = 20
    dist_to_new_ring = np.abs(np.sqrt((x - new_center[0])**2 + (y - new_center[1])**2) - new_radius)
    new_particle_energy = np.exp(-dist_to_new_ring**2 / 8.0) * 4.5

# 5. Plotting Results
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# Plot 1: Pre-collision State
im1 = axs[0].imshow(existing_particle_energy + incoming_wave_energy, cmap='Blues')
axs[0].set_title("1. Incoming Wave Approaches\nStable Particle (Compton Ring)")
axs[0].axis('off')

# Plot 2: Grid Jamming (Overload)
# Show the base energy plus the highlighted overload zones
jamming_viz = existing_particle_energy + incoming_wave_energy
jamming_viz[overload_mask] = 10.0 # Spike the visual for the bottleneck
im2 = axs[1].imshow(jamming_viz, cmap='hot')
axs[1].set_title("2. Constructive Grid Jamming\n(Capacity Overload at Intersection)")
axs[1].axis('off')

# Plot 3: The Orthogonal Split (New Matter Generation)
# Combine the original particle, the dispersed wave, and the newly generated particle
final_state = existing_particle_energy + (incoming_wave_energy * 0.3) + new_particle_energy
im3 = axs[2].imshow(final_state, cmap='magma')
axs[2].set_title("3. Orthogonal Split (Pair Production)\nGrid generates new stable 3D shell")
axs[2].axis('off')

plt.tight_layout()
plt.savefig("_VFT MD/Physics/Scripts/pair_production_jamming.png", dpi=150)
print("Plot saved to _VFT MD/Physics/Scripts/pair_production_jamming.png")
