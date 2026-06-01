import matplotlib.pyplot as plt
import matplotlib.patches as patches

def get_path_name(claim_u, claim_psi, real_u, real_psi):
    # Determine starting and ending quadrants
    # TL: (+u, +psi) - Greater Good / Good Preference
    # BL: (+u, -psi) - Lesser Good / Good Preference
    # TR: (-u, +psi) - Greatest Lie / Bad Preference
    # BR: (-u, -psi) - Greater Evil / Bad Preference
    
    start = "TL" if claim_u > 0 else "TR"
    if claim_psi < 0:
        start = "BL" if claim_u > 0 else "BR"
        
    end = "TL" if real_u > 0 else "TR"
    if real_psi < 0:
        end = "BL" if real_u > 0 else "BR"

    # 1. Canonical 4-Stage Gnostic Moral Cycle
    if start == "BL" and end == "TL":
        return "The Path of Grace"
    elif start == "TL" and end == "TR":
        return "The Path of The Fall"
    elif start == "TR" and end == "BR":
        return "The Path of Delusion"
    elif start == "BR" and end == "BL":
        return "The Path of Redemption"
        
    # 2. Structural Deviations & Diagonals
    elif start == "TL" and end == "BL":
        return "The Path of Empty Mass (The Fall)"
    elif start == "TL" and end == "BR":
        return "The Path of Deception"
    elif start == "BL" and end == "TR":
        return "The Path of The Fall"
    elif start == "TR" and end == "BL":
        return "The Path of Redemption"

    return "Projected Trajectory"

def draw_graph(claim_u, claim_psi, real_u, real_psi, title, filename):
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

    # The Strategic Extremes (Zone 2 Corners)
    # u=+2 is Left
    ax.text(1.9, 1.9, "JUSTICE", color='white', fontsize=10, ha='left', va='top') # Outer TL
    ax.text(-1.9, 1.9, "TYRANNY", color='white', fontsize=10, ha='right', va='top') # Outer TR
    ax.text(1.9, -1.9, "STAGNATION", color='white', fontsize=10, ha='left', va='bottom') # Outer BL
    ax.text(-1.9, -1.9, "CHAOS", color='white', fontsize=10, ha='right', va='bottom') # Outer BR

    # Coordinate Definitions
    ax.text(1.0 + 0.1, 0.0 + 0.1, "Good Preference\n(+1.0, 0.0)", **font_opts)
    ax.text(-1.0 - 0.1, 0.0 + 0.1, "Bad Preference\n(-1.0, 0.0)", **font_opts)

    # The Judgment Points & Path

    # Stated Claim (Origin)
    claim_point, = ax.plot(claim_u, claim_psi, marker='o', color='yellow', markersize=10, fillstyle='none', markeredgewidth=2, label="Stated Claim")

    # Actual Reality (Destination)
    real_point, = ax.plot(real_u, real_psi, marker='*', color='red', markersize=15, label="Actual Reality")

    # Draw Path
    path_name = get_path_name(claim_u, claim_psi, real_u, real_psi)

    ax.annotate("",
                xy=(real_u, real_psi), xycoords='data',
                xytext=(claim_u, claim_psi), textcoords='data',
                arrowprops=dict(arrowstyle="->", color="white", linestyle="dashed", linewidth=1.5, connectionstyle="arc3,rad=-0.2"))

    # Calculate midpoint for label
    mid_u = (claim_u + real_u) / 2
    mid_psi = (claim_psi + real_psi) / 2
    ax.text(mid_u, mid_psi, path_name, color='cyan', fontsize=10, ha='center', va='center', bbox=dict(facecolor='#111111', edgecolor='none', pad=1))


    # Axis labels
    ax.set_xlabel("Morality (υ): Left + (Universal), Right - (Self)", color='white')
    ax.set_ylabel("Will (ψ): Top + (Create), Bottom - (Destroy)", color='white')
    ax.tick_params(colors='gray')
    ax.set_title(f"{title}\nProjected Eventuality: {path_name}", color='white', pad=20)

    # Legend
    legend = ax.legend(handles=[claim_point, real_point], loc='upper right', facecolor='#111111', edgecolor='white', labelcolor='white')

    # Watermark label
    fig.text(0.5, 0.01, 'Psochic Hegemony Graph', ha='center', va='bottom',
             color='#444444', fontsize=9, fontstyle='italic')

    plt.tight_layout()


    plt.savefig(filename, facecolor=fig.get_facecolor(), dpi=300)

if __name__ == "__main__":
    # Test a Path of Deception
    draw_graph(-1.0, 1.0, -1.0, -1.0, "Embargo Assessment", "embargo_graph.png")
