import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve

# Simulate a 2D Macro Frame with multiple adjacent Homogeneous Zones (F2),
# each containing Micro-Homogeneous cells (F3) that interact.

# Grid Size (Macro Frame F1)
grid_size = 100
time_ticks = 100

# Base capacities (interaction distance limits)
base_limit_f2 = 6.0
base_limit_f3 = 3.0

# 1. Define distinct F2 Homogeneous Zones within the F1 Macro-Grid
# We'll create 4 distinct quadrants with different density states (n_2)
f2_density_map = np.zeros((grid_size, grid_size))
f2_density_map[0:50, 0:50] = 5.0    # High density zone (squished micro limits)
f2_density_map[50:100, 0:50] = 1.0  # Low density zone (relaxed micro limits)
f2_density_map[0:50, 50:100] = 3.0  # Medium density zone
f2_density_map[50:100, 50:100] = 4.5 # High-Med density zone

# Smooth the boundaries slightly to simulate natural field transition
kernel = np.ones((5,5)) / 25
f2_density_map = convolve(f2_density_map, kernel, mode='reflect')

# 2. Calculate the dynamic bounds (1_3) for the Micro-cells (F3)
# S = {0, n, 1}. Limit_child = f(Limit_parent - n_parent)
# Limit F3 = Base F3 * ( (Limit F2 - n2) / Limit F2 )
available_f2 = np.maximum(0.1, base_limit_f2 - f2_density_map)
ratio_f2 = available_f2 / base_limit_f2
limit_f3_map = base_limit_f3 * ratio_f2

# Initialize F3 Energy Grid (starts at baseline 1.5 everywhere)
f3_energy_grid = np.full((grid_size, grid_size), 1.5)

# Array to store cumulative catch events for plotting
cumulative_catch_events = np.zeros((grid_size, grid_size))

# Diffusion kernel for translating catch{excess} energy to neighbors
diffusion_kernel = np.array([[0.05, 0.1, 0.05],
                             [0.1,  0.4, 0.1 ],
                             [0.05, 0.1, 0.05]])

# 3. Run the Simulation
for t in range(time_ticks):
    # Add random background micro-storm noise at 1s/s
    storm_noise = np.random.normal(0, 0.6, (grid_size, grid_size))
    f3_energy_grid += storm_noise

    # Evaluate try^2{interaction <= limit}
    # Cells where energy exceeds their specific dynamic limit trigger catch{excess}
    breach_mask = f3_energy_grid > limit_f3_map
    cumulative_catch_events += breach_mask

    # Calculate the excess energy to translate
    excess_energy = np.zeros_like(f3_energy_grid)
    excess_energy[breach_mask] = f3_energy_grid[breach_mask] - limit_f3_map[breach_mask]

    # Remove the excess from the breaching cells
    f3_energy_grid[breach_mask] = limit_f3_map[breach_mask]

    # Translate (diffuse) the excess energy across boundaries
    # This allows micro-zones to bleed energy into neighboring homogenous zones
    translated_energy = convolve(excess_energy, diffusion_kernel, mode='constant', cval=0.0)

    # Add the translated energy back to the grid
    f3_energy_grid += translated_energy


# 4. Plotting Results
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

# Plot 1: F2 Density Map
im1 = ax1.imshow(f2_density_map, cmap='viridis', interpolation='nearest')
ax1.set_title("1. F2 Homogenous Zones Density ($n_2$)")
fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

# Plot 2: F3 Dynamic Limits Map
im2 = ax2.imshow(limit_f3_map, cmap='magma', interpolation='nearest')
ax2.set_title("2. F3 Dynamic Micro-Limits ($1_3$)\n(Squeezed by F2 Density)")
fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

# Plot 3: Cumulative Catch Events (The resulting thermodynamic drift)
im3 = ax3.imshow(cumulative_catch_events, cmap='hot', interpolation='nearest')
ax3.set_title("3. Micro `catch{excess}` Event Freq.\n(Energy Bleed Across Zones)")
fig.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)

plt.tight_layout()
plt.savefig("_VFT MD/Physics/Scripts/2d_nested_homogeny_plot.png")
print("Plot saved to _VFT MD/Physics/Scripts/2d_nested_homogeny_plot.png")
