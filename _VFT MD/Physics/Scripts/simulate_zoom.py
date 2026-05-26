import numpy as np
import matplotlib.pyplot as plt

# Parameters for our 1D simulation
num_cells = 1000
time_ticks = 10000

# Constants
c_local = 1.0  # Coherence limit
base_interaction = 1.05 # Slightly above coherence limit to cause drift
noise_level = 0.5 # Random micro-storm fluctuations

# The chain array representing density/energy in each cell
chain = np.zeros((time_ticks, num_cells))

# Initialize with a "mass" knot in the middle
mass_center = num_cells // 2
mass_width = 20
chain[0, mass_center-mass_width:mass_center+mass_width] = 50.0 # High density

# Run the discrete try-catch simulation
for t in range(1, time_ticks):
    chain[t] = chain[t-1].copy() # inherit from previous tick

    # 1. Background micro-storm (noise)
    storm = np.random.normal(0, noise_level, num_cells)
    chain[t] += storm

    # 2. Try-catch evaluation across all cells
    # We look at adjacent cells and diffuse based on catch
    for i in range(1, num_cells - 1):
        interaction_energy = chain[t, i]

        # try^2{ interaction_energy <= 2*c_local }
        if interaction_energy > 2 * c_local:
            # catch{excess}
            excess = interaction_energy - 2 * c_local

            # Translate excess to adjacent cells (simple 1D drift)
            drift = excess * 0.05 # Weak drift rate

            chain[t, i] -= drift * 2
            chain[t, i-1] += drift
            chain[t, i+1] += drift

# Analyze results
# 1. Micro-scale (Snapshot of a small time window and spatial window)
micro_time_window = slice(100, 150)
micro_space_window = slice(mass_center - 10, mass_center + 10)
micro_view = chain[micro_time_window, micro_space_window]

# 2. Macro-scale (Time averaged over entire simulation)
macro_view = np.mean(chain, axis=0) # Time averaged

# Plotting
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(micro_view, aspect='auto', cmap='hot', interpolation='none')
plt.title("Micro-Homogenous Scale (Discrete Try-Catch)")
plt.xlabel("Cell Index (Space)")
plt.ylabel("Planck Ticks (Time)")
plt.colorbar(label="Energy State")

plt.subplot(1, 2, 2)
plt.plot(macro_view)
plt.title("Macro-Homogenous Scale (Time Averaged)")
plt.xlabel("Cell Index (Space)")
plt.ylabel("Averaged Density ($\\rho$)")
plt.grid(True)

plt.tight_layout()
plt.savefig("/tmp/zoom_plot.png")
print("Plot saved to /tmp/zoom_plot.png")
