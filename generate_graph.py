import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_graph(u_val, psi_val, title, filename):
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='#111111')
    ax.set_facecolor('#111111')

    # Grid Bounds
    ax.set_xlim(2.5, -2.5) # Reversed X axis: Left is Positive (+2.0), Right is Negative (-2.0)
    ax.set_ylim(-2.5, 2.5) # Y axis: Top is Positive (+2.0), Bottom is Negative (-2.0)

    # Axes
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)

    # Zone 1 (The Inner Horizon)
    zone1 = patches.Rectangle((1.0, -1.0), -2.0, 2.0, fill=False, edgecolor='white', linestyle='--', linewidth=1)
    ax.add_patch(zone1)

    # Zone 2 (The Outer Horizon)
    zone2 = patches.Rectangle((2.0, -2.0), -4.0, 4.0, fill=False, edgecolor='white', linestyle='-', linewidth=1.5)
    ax.add_patch(zone2)

    font_opts = {'color': 'white', 'fontsize': 10, 'ha': 'center', 'va': 'center'}

    # The Objective Boundary (Zone 1 Corners)
    # Note on placement: u is reversed, so +1.0 is Left.
    ax.text(1.0 + 0.1, 1.0 + 0.1, "The Greater Good\n(Flow)", **font_opts) # TL: u=+1, psi=+1
    ax.text(-1.0 - 0.1, 1.0 + 0.1, "The Greatest Lie\n(Greed)", **font_opts) # TR: u=-1, psi=+1
    ax.text(1.0 + 0.1, -1.0 - 0.1, "The Lesser Good\n(Peace)", **font_opts) # BL: u=+1, psi=-1
    ax.text(-1.0 - 0.1, -1.0 - 0.1, "The Greater Evil\n(Void)", **font_opts) # BR: u=-1, psi=-1

    # The Inner Traps (The 0.5 Ring)
    ax.text(0.5, 0.5 + 0.1, "P-LE", **font_opts) # Inner TL
    ax.text(-0.5, 0.5 + 0.1, "P-GG", **font_opts) # Inner TR
    ax.text(0.5, -0.5 - 0.1, "P-GE", **font_opts) # Inner BL
    ax.text(-0.5, -0.5 - 0.1, "P-LE", **font_opts) # Inner BR

    # The Strategic Extremes (Zone 2 Corners)
    # u=+2 is Left
    ax.text(1.9, 1.9, "JUSTICE", color='white', fontsize=10, ha='left', va='top') # Outer TL
    ax.text(-1.9, 1.9, "TYRANNY", color='white', fontsize=10, ha='right', va='top') # Outer TR
    ax.text(1.9, -1.9, "STAGNATION", color='white', fontsize=10, ha='left', va='bottom') # Outer BL
    ax.text(-1.9, -1.9, "CHAOS", color='white', fontsize=10, ha='right', va='bottom') # Outer BR

    # The Emotional Coordinates (The Vectors)
    ax.plot(0.8, 0.8, marker='o', color='white', markersize=3)
    ax.text(0.8, 0.8 + 0.05, "Joy", **font_opts)

    ax.plot(-0.8, 0.8, marker='o', color='white', markersize=3)
    ax.text(-0.8, 0.8 + 0.05, "Anger", **font_opts)

    ax.plot(0.8, -0.8, marker='o', color='white', markersize=3)
    ax.text(0.8, -0.8 - 0.05, "Peace", **font_opts)

    ax.plot(-0.8, -0.8, marker='o', color='white', markersize=3)
    ax.text(-0.8, -0.8 - 0.05, "Depression", **font_opts)

    # The Judgment Point
    ax.plot(u_val, psi_val, marker='*', color='red', markersize=15)
    ax.text(u_val, psi_val + 0.15, "Target Point", color='red', fontsize=12, ha='center', va='center')

    # Axis labels
    ax.set_xlabel("Morality (υ): Left + (Universal), Right - (Self)", color='white')
    ax.set_ylabel("Will (ψ): Top + (Create), Bottom - (Destroy)", color='white')
    ax.tick_params(colors='gray')
    ax.set_title("Psochic Hegemony", color='white', pad=20)

    plt.tight_layout()
    plt.savefig(filename, facecolor=fig.get_facecolor(), dpi=300)

draw_graph(-1.5, -1.2, "Embargo Assessment", "embargo_graph.png")
