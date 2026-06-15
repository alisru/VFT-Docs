import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as mtransforms

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

def draw_graph(claim_u, claim_psi, real_u, real_psi, title, filename,
               macro_event="", macro_claim_u=None, macro_claim_psi=None, macro_real_u=None, macro_real_psi=None):
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='#111111')
    ax.set_facecolor('#111111')

    # Grid Bounds
    ax.set_xlim(2.5, -2.5) # Reversed X axis: Left is Positive (+2.0), Right is Negative (-2.0)
    ax.set_ylim(-2.5, 2.5) # Y axis: Top is Positive (+2.0), Bottom is Negative (-2.0)

    # Explicit Ticks & Grid Lines to ensure high precision alignment (preventing overlap/inversion confusion)
    x_ticks = [2.0, 1.0, 0.5, 0.0, -0.5, -1.0, -2.0]
    y_ticks = [2.0, 1.0, 0.0, -1.0, -2.0]
    
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    
    x_labels = [
        "Everyone\n(+2.0)",
        "Others\n(+1.0)",
        "Other\n(+0.5)",
        "No One\n(0.0)",
        "My Group\n(-0.5)",
        "Me\n(-1.0)",
        "Only Me\n(-2.0)"
    ]
    y_labels = [
        "Active-Active (+2.0)",
        "Passive-Active (+1.0)",
        "Neutral (0.0)",
        "Passive-Passive (-1.0)",
        "Active-Passive (-2.0)"
    ]
    
    ax.set_xticklabels(x_labels, fontsize=8, color='white', ha='center')
    ax.set_yticklabels(y_labels, fontsize=8, color='white', va='center')
    
    ax.grid(True, which='both', color='gray', linestyle=':', linewidth=0.5, alpha=0.3)

    # Axes lines
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)

    # Zone 1 (The Inner Horizon)
    zone1 = patches.Rectangle((1.0, -1.0), -2.0, 2.0, fill=False, edgecolor='white', linestyle='--', linewidth=1, zorder=1)
    ax.add_patch(zone1)

    # Zone 2 (The Outer Horizon)
    zone2 = patches.Rectangle((2.0, -2.0), -4.0, 4.0, fill=False, edgecolor='white', linestyle='-', linewidth=1.5, zorder=1)
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

    has_macro = macro_event and macro_event.strip()
    
    if has_macro:
        # Defaults for macro if not provided
        m_claim_u = macro_claim_u if macro_claim_u is not None else 0.0
        m_claim_psi = macro_claim_psi if macro_claim_psi is not None else 0.0
        m_real_u = macro_real_u if macro_real_u is not None else 0.0
        m_real_psi = macro_real_psi if macro_real_psi is not None else 0.0

        # 1. Plot Macro Points on Outer Grid
        macro_claim_pt, = ax.plot(m_claim_u, m_claim_psi, marker='o', color='yellow', markersize=10, 
                                  fillstyle='none', markeredgewidth=2, label="Macro Stated", zorder=3)
        macro_real_pt, = ax.plot(m_real_u, m_real_psi, marker='*', color='red', markersize=15, 
                                 label="Macro Actual", zorder=3)
        
        # Draw macro path arrow
        ax.annotate("",
                    xy=(m_real_u, m_real_psi), xycoords='data',
                    xytext=(m_claim_u, m_claim_psi), textcoords='data',
                    arrowprops=dict(arrowstyle="->", color="white", linestyle="dashed", linewidth=1.5, connectionstyle="arc3,rad=-0.2"),
                    zorder=3)

        # 2. Draw Nested Inner Box (represented as outer [-0.5, 0.5])
        inner_box = patches.Rectangle((0.5, -0.5), -1.0, 1.0, fill=True, facecolor='#161616', 
                                      edgecolor='white', linestyle='-', linewidth=1.5, zorder=2)
        ax.add_patch(inner_box)

        # Draw axes inside inner box
        ax.plot([0.5, -0.5], [0.0, 0.0], color='gray', linestyle='-', linewidth=0.5, alpha=0.5, zorder=2)
        ax.plot([0.0, 0.0], [-0.5, 0.5], color='gray', linestyle='-', linewidth=0.5, alpha=0.5, zorder=2)

        # 3. Determine Rotation (perceptual inversion if macro-event is selfish)
        is_mirrored = (m_real_u < 0)

        # 4. Write Inner Box Quadrant Labels (perceptually inverted by default inside the 0.5 square)
        inner_font = {'color': 'white', 'fontsize': 6.5, 'ha': 'center', 'va': 'center', 'zorder': 3}
        t1 = ax.text(0.25, 0.28, "Percieved Greater Evil\n(Void)", **inner_font)
        t2 = ax.text(-0.25, 0.28, "Percieved Lesser Good\n(Peace)", **inner_font)
        t3 = ax.text(0.25, -0.28, "Percieved Lesser Evil\n(Greed)", **inner_font)
        t4 = ax.text(-0.25, -0.28, "Percieved Greater Good\n(Flow)", **inner_font)

        # Write Inner Box Corner Tags
        corner_font = {'color': '#cccccc', 'fontsize': 5.5, 'va': 'center', 'ha': 'center', 'zorder': 3}
        c1 = ax.text(0.38, 0.38, "CHAOS", **corner_font)
        c2 = ax.text(-0.38, 0.38, "STAGNATION", **corner_font)
        c3 = ax.text(0.38, -0.38, "TYRANNY", **corner_font)
        c4 = ax.text(-0.38, -0.38, "JUSTICE", **corner_font)

        if is_mirrored:
            # Apply horizontal mirror transformation using Affine2D
            mirror_transform = mtransforms.Affine2D().scale(-1, 1) + ax.transData
            for t in [t1, t2, t3, t4, c1, c2, c3, c4]:
                t.set_transform(mirror_transform)

        # 5. Plot Micro Points inside the Inner Box (scaled by 0.5, and mirrored horizontally if is_mirrored)
        u_st_plot = (-claim_u if is_mirrored else claim_u) * 0.5
        psi_st_plot = claim_psi * 0.5
        u_ac_plot = (-real_u if is_mirrored else real_u) * 0.5
        psi_ac_plot = real_psi * 0.5

        micro_claim_pt, = ax.plot(u_st_plot, psi_st_plot, marker='o', color='yellow', markersize=6, 
                                  fillstyle='none', markeredgewidth=1.5, label="Micro Stated", zorder=4)
        micro_real_pt, = ax.plot(u_ac_plot, psi_ac_plot, marker='*', color='red', markersize=9, 
                                 label="Micro Actual", zorder=4)

        # Draw micro path dashed arrow
        ax.annotate("",
                    xy=(u_ac_plot, psi_ac_plot), xycoords='data',
                    xytext=(u_st_plot, psi_st_plot), textcoords='data',
                    arrowprops=dict(arrowstyle="->", color="white", linestyle="dashed", linewidth=1.0, connectionstyle="arc3,rad=-0.2"),
                    zorder=4)

        # 6. Draw Dashed Connection lines from outer points to inner box corners on the 0.5 square (straight)
        def get_corner(u, psi):
            u_c = 0.5 if u >= 0 else -0.5
            psi_c = 0.5 if psi >= 0 else -0.5
            return u_c, psi_c

        c_st_u, c_st_psi = get_corner(m_claim_u, m_claim_psi)
        ax.plot([m_claim_u, c_st_u], [m_claim_psi, c_st_psi], color='white', linestyle='--', linewidth=0.75, alpha=0.7, zorder=1)

        c_ac_u, c_ac_psi = get_corner(m_real_u, m_real_psi)
        ax.plot([m_real_u, c_ac_u], [m_real_psi, c_ac_psi], color='white', linestyle='--', linewidth=0.75, alpha=0.7, zorder=1)

        legend_handles = [macro_claim_pt, macro_real_pt, micro_claim_pt, micro_real_pt]
        path_name = get_path_name(claim_u, claim_psi, real_u, real_psi)
        title_text = (
            f"{title}\n"
            f"Projected Eventuality: {path_name}\n"
            f"Micro: Stated ({claim_u:+.1f}, {claim_psi:+.1f}) | Actual ({real_u:+.1f}, {real_psi:+.1f})\n"
            f"Macro [{macro_event}]: Stated ({m_claim_u:+.1f}, {m_claim_psi:+.1f}) | Actual ({m_real_u:+.1f}, {m_real_psi:+.1f})"
        )
    else:
        # Standard Single-Level Graph Plotting
        claim_point, = ax.plot(claim_u, claim_psi, marker='o', color='yellow', markersize=10, fillstyle='none', markeredgewidth=2, label="Stated Claim", zorder=3)
        real_point, = ax.plot(real_u, real_psi, marker='*', color='red', markersize=15, label="Actual Reality", zorder=3)

        # Draw Path
        path_name = get_path_name(claim_u, claim_psi, real_u, real_psi)

        ax.annotate("",
                    xy=(real_u, real_psi), xycoords='data',
                    xytext=(claim_u, claim_psi), textcoords='data',
                    arrowprops=dict(arrowstyle="->", color="white", linestyle="dashed", linewidth=1.5, connectionstyle="arc3,rad=-0.2"),
                    zorder=3)

        legend_handles = [claim_point, real_point]
        title_text = f"{title}\nProjected Eventuality: {path_name}\nStated: ({claim_u:+.1f}, {claim_psi:+.1f})  |  Actual: ({real_u:+.1f}, {real_psi:+.1f})"

    # Axis labels
    ax.set_xlabel("Morality (υ)", color='white')
    ax.set_ylabel("Will (ψ)", color='white')
    ax.tick_params(colors='gray')
    ax.set_title(title_text, color='white', pad=25, fontsize=10)

    # Legend
    legend = ax.legend(handles=legend_handles, loc='upper right', facecolor='#111111', edgecolor='white', labelcolor='white')

    # Watermark label
    fig.text(0.5, 0.01, 'Psychic Hegemony Graph', ha='center', va='bottom',
             color='#444444', fontsize=9, fontstyle='italic')

    plt.tight_layout()

    plt.savefig(filename, facecolor=fig.get_facecolor(), dpi=300)
    plt.close(fig)

if __name__ == "__main__":
    # Test a Path of Deception
    draw_graph(-1.0, 1.0, -1.0, -1.0, "Embargo Assessment", "embargo_graph.png")
