import numpy as np
import matplotlib.pyplot as plt

# Simulate the [F3] ∝ [F2] ∝ [F1] Cascade where a Macro Field compression
# shrinks the interaction distance (1 limit) of the Micro fields,
# resulting in an explosion of catch{excess} events.

time_ticks = 1000

# F1 (Macro), F2 (Intermediate), F3 (Micro)
# Base capacities (interaction distance limits) based on 3-6-9 ratio
base_limit_f1 = 9.0
base_limit_f2 = 6.0
base_limit_f3 = 3.0

# 1. Simulate the Macro Field (F1) compressing over time
# n_1 (density) starts low and increases towards limit_1
n_1 = np.linspace(1.0, 8.5, time_ticks)

# Arrays to store the dynamically shrinking limits and resulting event counts
limit_f2 = np.zeros(time_ticks)
limit_f3 = np.zeros(time_ticks)
catch_events_f3 = np.zeros(time_ticks)

# Base interaction energy entering the micro field at 1s/s
base_micro_interaction = 2.5

for t in range(time_ticks):
    # F1 compresses, meaning its available space shrinks.
    # This available space dictates the absolute limit (1) of the child F2
    # Limit_child = Base_child * (Available_parent / Limit_parent)
    available_f1 = base_limit_f1 - n_1[t]
    ratio_f1 = available_f1 / base_limit_f1

    # Dynamic Limit of F2 shrinks
    limit_f2[t] = base_limit_f2 * (ratio_f1 + 0.1) # Add 0.1 to avoid strict 0

    # Assume F2 is operating at a constant density n_2 relative to its base,
    # but as its limit shrinks, it gets squeezed.
    # Let's say F2 has a constant baseline energy of 3.0
    n_2 = 3.0
    available_f2 = max(0.1, limit_f2[t] - n_2) # Squeeze!
    ratio_f2 = available_f2 / limit_f2[t]

    # Dynamic Limit of F3 shrinks
    limit_f3[t] = base_limit_f3 * ratio_f2

    # Now simulate the micro-storm in F3.
    # If the base interaction energy > F3's shrinking limit, it triggers a catch{excess}
    # We'll add some noise to simulate the 1s/s micro-storm
    storm_noise = np.random.normal(0, 0.5, 100) # 100 cells at this tick

    # How many cells breach the shrinking coherence limit?
    breaches = np.sum((base_micro_interaction + storm_noise) > limit_f3[t])
    catch_events_f3[t] = breaches

# Plotting
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

# Plot F1 Compression
ax1.plot(n_1, color='blue', label='F1 Density ($n_1$)')
ax1.axhline(y=base_limit_f1, color='r', linestyle='--', label='F1 Capacity Limit ($1_1$)')
ax1.set_title("1. Macro-Field ($F_1$) Compression")
ax1.set_ylabel("Density / Capacity")
ax1.legend(loc="upper left")

# Plot Shrinking Limits
ax2.plot(limit_f2, color='orange', label='F2 Dynamic Limit ($1_2$)')
ax2.plot(limit_f3, color='green', label='F3 Dynamic Limit ($1_3$)')
ax2.set_title("2. Cascading Interaction Distance Squeeze")
ax2.set_ylabel("Capacity Limit ($1_{child}$)")
ax2.legend(loc="upper left")

# Plot Micro-Storm Explosion
ax3.plot(catch_events_f3, color='purple', alpha=0.7)
ax3.set_title("3. Micro-Field ($F_3$) `catch{excess}` Event Explosion")
ax3.set_ylabel("Catch Events (Frequency)")
ax3.set_xlabel("Time (Ticks)")

plt.tight_layout()
plt.savefig("_VFT MD/Physics/Scripts/simulate_cascade_compression.png")
print("Plot saved to _VFT MD/Physics/Scripts/simulate_cascade_compression.png")
