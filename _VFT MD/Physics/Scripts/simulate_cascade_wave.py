import numpy as np
import matplotlib.pyplot as plt

# Simulate the [F3] ∝ [F2] ∝ [F1] Cascade where a Macro Field acts as an oscillating wave
# (density goes up and down cyclically), to show that the micro field
# perfectly pulses in sync with the macro constraints.

time_ticks = 1000

base_limit_f1 = 9.0
base_limit_f2 = 6.0
base_limit_f3 = 3.0

# 1. Simulate the Macro Field (F1) as an oscillating wave
# We use a sine wave to represent a continuous density wave passing through
x = np.linspace(0, 4 * np.pi, time_ticks)
n_1 = 4.5 + 3.5 * np.sin(x) # Oscillates between 1.0 and 8.0

limit_f2 = np.zeros(time_ticks)
limit_f3 = np.zeros(time_ticks)
catch_events_f3 = np.zeros(time_ticks)

base_micro_interaction = 2.5

for t in range(time_ticks):
    available_f1 = base_limit_f1 - n_1[t]
    ratio_f1 = available_f1 / base_limit_f1

    limit_f2[t] = base_limit_f2 * (ratio_f1 + 0.1)

    n_2 = 3.0
    available_f2 = max(0.1, limit_f2[t] - n_2)
    ratio_f2 = available_f2 / limit_f2[t]

    limit_f3[t] = base_limit_f3 * ratio_f2

    storm_noise = np.random.normal(0, 0.5, 100)

    breaches = np.sum((base_micro_interaction + storm_noise) > limit_f3[t])
    catch_events_f3[t] = breaches

# Plotting
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

# Plot F1 Wave
ax1.plot(n_1, color='blue', label='F1 Density ($n_1$) Wave')
ax1.axhline(y=base_limit_f1, color='r', linestyle='--', label='F1 Capacity Limit ($1_1$)')
ax1.set_title("1. Macro-Field ($F_1$) Density Wave")
ax1.set_ylabel("Density / Capacity")
ax1.legend(loc="upper right")

# Plot Pulsing Limits
ax2.plot(limit_f2, color='orange', label='F2 Dynamic Limit ($1_2$)')
ax2.plot(limit_f3, color='green', label='F3 Dynamic Limit ($1_3$)')
ax2.set_title("2. Cascading Interaction Distance Pulses")
ax2.set_ylabel("Capacity Limit ($1_{child}$)")
ax2.legend(loc="upper right")

# Plot Micro-Storm Pulses
ax3.plot(catch_events_f3, color='purple', alpha=0.7)
ax3.set_title("3. Micro-Field ($F_3$) `catch{excess}` Event Pulses")
ax3.set_ylabel("Catch Events (Frequency)")
ax3.set_xlabel("Time (Ticks)")

plt.tight_layout()
plt.savefig("_VFT MD/Physics/Scripts/simulate_cascade_wave.png")
print("Plot saved to _VFT MD/Physics/Scripts/simulate_cascade_wave.png")
