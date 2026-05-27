import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve

# Simulate a 2D Macro Frame with explicitly nested topological regions
# (things within things) to match the "Greater Homogeny -> Homogeny ->
# Micro-Homogeny -> Sub-Micro-Homogeny" visual model.

grid_size = 300
time_ticks = 150

# Set up coordinate grid
y, x = np.ogrid[0:grid_size, 0:grid_size]

def create_circle_mask(cx, cy, r):
    return (x - cx)**2 + (y - cy)**2 <= r**2

# 1. Define Distinct Nested Homogeneous Zones (Topological Nesting)
# Background: Greater Homogeny (Low density n=1.0)
density_map = np.full((grid_size, grid_size), 1.0)

# Level 1: Homogeny (Inner circle, Medium density n=2.5)
mask_homogeny = create_circle_mask(150, 150, 120)
density_map[mask_homogeny] = 2.5

# Level 2: Micro-homogeny (Three smaller circles inside the main one, High density n=5.0)
mask_micro1 = create_circle_mask(110, 110, 30)
mask_micro2 = create_circle_mask(200, 130, 25)
mask_micro3 = create_circle_mask(150, 220, 25)
density_map[mask_micro1] = 5.0
density_map[mask_micro2] = 5.0
density_map[mask_micro3] = 5.0

# Level 3: Sub-micro-homogeny (Tiny hyper-dense core inside micro1, Extreme density n=8.0)
mask_sub_micro = create_circle_mask(110, 110, 12)
density_map[mask_sub_micro] = 8.0

# Add slight Gaussian blur to boundaries for field transition smoothness
kernel = np.ones((3,3)) / 9
density_map = convolve(density_map, kernel, mode='reflect')

# 2. Calculate the dynamic bounds (Limits) based on nested density
# S = {0, n, 1}. The denser the parent, the tighter the limit for the child.
base_limit = 10.0
available_space = np.maximum(0.1, base_limit - density_map)
# Calculate dynamic interaction capacity (Limit shrinks as we go deeper into nested circles)
limit_map = 4.0 * (available_space / base_limit)

# 3. Setup Energy Grid and Diffusion
# Start with uniform background energy
energy_grid = np.full((grid_size, grid_size), 1.5)
cumulative_catch_events = np.zeros((grid_size, grid_size))

# Diffusion kernel to spread excess energy radially outward
diffusion_kernel = np.array([[0.05, 0.1, 0.05],
                             [0.1,  0.4, 0.1 ],
                             [0.05, 0.1, 0.05]])

# Base micro-storm interaction energy at 1s/s
base_interaction = 0.5

# 4. Run the Simulation
for t in range(time_ticks):
    # Apply background noise (the micro-storm)
    storm_noise = np.random.normal(0, 0.5, (grid_size, grid_size))
    energy_grid += base_interaction + storm_noise

    # Check for Limit Breaches (try^2 mechanics)
    breach_mask = energy_grid > limit_map
    cumulative_catch_events += breach_mask

    # Calculate excess
    excess_energy = np.zeros_like(energy_grid)
    excess_energy[breach_mask] = energy_grid[breach_mask] - limit_map[breach_mask]

    # Cap breached cells back to their limit
    energy_grid[breach_mask] = limit_map[breach_mask]

    # Catch: Translate (diffuse) the excess energy radially outward
    translated_energy = convolve(excess_energy, diffusion_kernel, mode='constant', cval=0.0)

    # Add translated energy back
    energy_grid += translated_energy


# 5. Plotting Results
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

# Plot 1: Nested Density Map
im1 = ax1.imshow(density_map, cmap='viridis')
ax1.set_title("1. Topological Nesting\n(Density $n$)")
ax1.axis('off')
fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

# Plot 2: Shrinking Limits
im2 = ax2.imshow(limit_map, cmap='magma_r') # reversed so tighter limits are darker
ax2.set_title("2. Dynamic Interaction Limits\n(Squeezed Inward)")
ax2.axis('off')
fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

# Plot 3: Cumulative Catch Events (Radial Energy Bleed)
im3 = ax3.imshow(cumulative_catch_events, cmap='hot')
ax3.set_title("3. Outward Energy Bleed\n(`catch{excess}` events)")
ax3.axis('off')
fig.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)

plt.tight_layout()
plt.savefig("_VFT MD/Physics/Scripts/2d_nested_circles_plot.png")
print("Plot saved to _VFT MD/Physics/Scripts/2d_nested_circles_plot.png")
