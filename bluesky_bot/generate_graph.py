import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as mtransforms
import numpy as np
import textwrap
from matplotlib.colors import LinearSegmentedColormap

def get_path_name(claim_u, claim_psi, real_u, real_psi):
    # Determine exit name and origin zone
    if claim_u > 0 and claim_psi > 0:
        exit_name = "Fall"
        origin_zone = "Greater Good"
    elif claim_u <= 0 and claim_psi > 0:
        exit_name = "Revelation"
        origin_zone = "Greatest Lie"
    elif claim_u > 0 and claim_psi <= 0:
        exit_name = "Awakening"
        origin_zone = "Lesser Good"
    else:
        exit_name = "Reckoning"
        origin_zone = "Greater Evil"

    # Determine entry name and destination zone
    if real_u > 0 and real_psi > 0:
        entry_name = "Grace"
        dest_zone = "Greater Good"
    elif real_u <= 0 and real_psi > 0:
        entry_name = "Deception"
        dest_zone = "Greatest Lie"
    elif real_u > 0 and real_psi <= 0:
        entry_name = "Redemption"
        dest_zone = "Lesser Good"
    else:
        entry_name = "Destruction"
        dest_zone = "Greater Evil"

    if origin_zone == dest_zone:
        return "Stasis"
        
    return f"{exit_name} into {entry_name}"

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
        "Everyone\n(+2.0)\nEgalitarian",
        "Others\n(+1.0)",
        "Other\n(+0.5)",
        "No One\n(0.0)",
        "My Group\n(-0.5)",
        "Me\n(-1.0)",
        "Only Me\n(-2.0)\nAnti-Egalitarian"
    ]
    y_labels = [
        "Active-\nActive (+2.0)",
        "Passive-\nActive (+1.0)",
        "Neutral (0.0)",
        "Passive-\nPassive (-1.0)",
        "Active-\nPassive (-2.0)"
    ]
    
    ax.set_xticklabels(x_labels, fontsize=8, color='white', ha='center')
    ax.set_yticklabels(y_labels, fontsize=8, color='white', va='center')
    
    ax.grid(True, which='both', color='gray', linestyle=':', linewidth=0.5, alpha=0.3)

    # Axes lines
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)

    # The Six Attractors of the Hegemony -- this list is the single source of truth. The
    # background gradient is a field computed FROM these points (each one pulls color toward
    # itself, weighted by its own size/vividness); the dots plotted afterward are drawn from the
    # same list. Move a dot or change its weight and the boundary below moves with it -- nothing
    # about the divide is a separately chosen shape.
    green_attractors = [(1.0, 1.0, '#00FF00', 32), (1.0, 0.0, '#98FB98', 22), (1.0, -1.0, '#98FB98', 16)]
    red_attractors = [(-1.0, -1.0, '#FF0000', 32), (-1.0, 0.0, '#FF9999', 22), (-1.0, 1.0, '#FF9999', 16)]

    # Morality Gradient: green (Everyone, +u) <-> red (Only Me, -u), single blended background layer.
    # At each point on the field, green's pull = sum of its three attractors' influence
    # (gaussian falloff by distance, scaled by marker size); red's pull is computed the same way.
    # Wherever one pull dominates, that color shows; wherever they're equal, white shows --
    # plain background colormap, nothing painted separately. The boundary curve is just
    # wherever green_pull == red_pull, which emerges from the attractor layout itself: green is
    # vivid at psi=+1 and only faint at psi=-1, red is the mirror image, so the boundary
    # naturally swings toward red at the top and toward green at the bottom.
    #
    # Two more emergent effects feed the same field:
    # 1. "Like" reinforcement -- the judgement coordinates (stated claim, actual reality) boost
    #    whichever color's attractors share their moral sign. A claim/reality that leans green
    #    (+u) strengthens the green attractors' pull; one that leans red (-u) strengthens red's.
    # 2. The judgement coordinates are themselves field sources, pulling color the same way the
    #    six fixed attractors do -- weighted by how far they lean (a coordinate near u=0 barely
    #    pulls at all; one near u=+/-2 pulls hard).
    grid_res = 256
    gx = np.linspace(2.0, -2.0, grid_res)   # left=+2.0 (green) -> right=-2.0 (red)
    gy = np.linspace(2.0, -2.0, grid_res)   # row 0=top(+2.0) -> last row=bottom(-2.0), matching imshow's default origin='upper'
    U, PSI = np.meshgrid(gx, gy)

    field_sigma = 1.3
    max_size = 32.0

    judgement_points = [(claim_u, claim_psi), (real_u, real_psi)]
    green_lean = sum(max(ju, 0.0) / 2.0 for ju, _jp in judgement_points)  # 0..1 per point
    red_lean = sum(max(-ju, 0.0) / 2.0 for ju, _jp in judgement_points)   # 0..1 per point
    like_boost_strength = 0.6
    green_boost = 1.0 + like_boost_strength * green_lean
    red_boost = 1.0 + like_boost_strength * red_lean

    def pull(attractors, boost=1.0):
        total = np.zeros_like(U)
        for au, apsi, _color, size in attractors:
            weight = (size / max_size) * boost
            dist_sq = (U - au) ** 2 + (PSI - apsi) ** 2
            total += weight * np.exp(-dist_sq / (2.0 * field_sigma ** 2))
        return total

    # Judgement points sit directly on the green=+1 / white=0 / red=-1 spectrum via their own u
    # (cv = u/2, clipped to [-1,1]). A point near u=+/-2 pulls almost entirely green or red; a
    # point near u=0 pulls almost entirely white -- and that white pull is exaggerated (weighted
    # harder than the green/red pull an equally-placed attractor would exert), so a judgement
    # landing near "No One" visibly bleaches the field around it rather than just going quiet.
    judgement_exaggeration = 2.0
    white_exaggeration = 3.5

    def judgement_pull():
        green_total = np.zeros_like(U)
        red_total = np.zeros_like(U)
        white_total = np.zeros_like(U)
        for ju, jpsi in judgement_points:
            cv = np.clip(ju / 2.0, -1.0, 1.0)  # +1=green, 0=white, -1=red
            dist_sq = (U - ju) ** 2 + (PSI - jpsi) ** 2
            influence = np.exp(-dist_sq / (2.0 * field_sigma ** 2))
            green_total += judgement_exaggeration * max(cv, 0.0) * influence
            red_total += judgement_exaggeration * max(-cv, 0.0) * influence
            white_total += white_exaggeration * (1.0 - abs(cv)) * influence
        return green_total, red_total, white_total

    j_green, j_red, j_white = judgement_pull()
    green_pull = pull(green_attractors, green_boost) + j_green
    red_pull = pull(red_attractors, red_boost) + j_red
    white_pull = j_white

    hegemony_cmap = LinearSegmentedColormap.from_list('hegemony_gradient', ['#00FF00', '#FFFFFF', '#FF0000'])
    hue_t = red_pull / (green_pull + red_pull + 1e-9)  # 0=green dominant, 1=red dominant, ignoring white
    rgba = hegemony_cmap(hue_t)
    white_fraction = white_pull / (green_pull + red_pull + white_pull + 1e-9)
    rgba[..., 0:3] = rgba[..., 0:3] * (1.0 - white_fraction[..., None]) + 1.0 * white_fraction[..., None]
    rgba[..., 3] = 0.30
    ax.imshow(rgba, extent=[2.0, -2.0, -2.0, 2.0], aspect='auto', zorder=0.05)

    # Zone 1 (The Inner Horizon)
    zone1 = patches.Rectangle((1.0, -1.0), -2.0, 2.0, fill=False, edgecolor='white', linestyle='--', linewidth=1, zorder=1)
    ax.add_patch(zone1)

    # Zone 2 (The Outer Horizon)
    zone2 = patches.Rectangle((2.0, -2.0), -4.0, 4.0, fill=False, edgecolor='white', linestyle='-', linewidth=1.5, zorder=1)
    ax.add_patch(zone2)

    # Plot the same six attractors used to build the field above
    attractor_opts = dict(markeredgewidth=0, alpha=0.75, zorder=2)
    for au, apsi, color, size in green_attractors + red_attractors:
        ax.plot(au, apsi, marker='o', color=color, markersize=size, **attractor_opts)

    # Alchemical Element & Quality Overlays (outside the white box, before graph arms)
    alchemy_opts = dict(color='white', fontsize=9, fontstyle='italic', alpha=0.45, ha='center', va='center', zorder=0)
    quality_opts = dict(color='white', fontsize=8, fontstyle='italic', alpha=0.35, ha='center', va='center', zorder=0)

    # Corners
    ax.text(2.22, 2.22, "AIR", **alchemy_opts)      # TL: Justice (hot + wet)
    ax.text(-2.22, 2.22, "FIRE", **alchemy_opts)    # TR: Tyranny (hot + dry)
    ax.text(2.22, -2.22, "WATER", **alchemy_opts)   # BL: Stagnation (cold + wet)
    ax.text(-2.22, -2.22, "EARTH", **alchemy_opts)  # BR: Chaos (cold + dry)

    # Axis Midpoints
    ax.text(0.0, 2.15, "HOT", **quality_opts)       # Top
    ax.text(0.0, -2.15, "COLD", **quality_opts)     # Bottom
    ax.text(2.3, 0.0, "WET", **quality_opts)        # Left
    ax.text(-2.3, 0.0, "DRY", **quality_opts)       # Right

    font_opts = {'color': 'white', 'fontsize': 10, 'ha': 'center', 'va': 'center'}

    # The Objective Boundary (Zone 1 Corners)
    # Note on placement: u is reversed, so +1.0 is Left.
    ax.text(1.0 + 0.1, 1.0 + 0.1, "The Greater Good\n(Flow)", **font_opts) # TL: u=+1, psi=+1
    ax.text(-1.0 - 0.1, 1.0 + 0.1, "The Greatest Lie\n(Greed)", **font_opts) # TR: u=-1, psi=+1
    ax.text(1.0 + 0.1, -1.0 - 0.1, "The Lesser Good\n(Peace)", **font_opts) # BL: u=+1, psi=-1
    ax.text(-1.0 - 0.1, -1.0 - 0.1, "The Greater Evil\n(Void)", **font_opts) # BR: u=-1, psi=-1

    # The Strategic Extremes (Zone 2 Corners)
    # u=+2 is Left
    ax.text(1.9, 1.9, "JUSTICE\n(Joy)", color='white', fontsize=10, ha='left', va='top') # Outer TL
    ax.text(-1.9, 1.9, "TYRANNY\n(Anger)", color='white', fontsize=10, ha='right', va='top') # Outer TR
    ax.text(1.9, -1.9, "STAGNATION\n(Peace)", color='white', fontsize=10, ha='left', va='bottom') # Outer BL
    ax.text(-1.9, -1.9, "CHAOS\n(Depression)", color='white', fontsize=10, ha='right', va='bottom') # Outer BR

    has_macro = macro_event and macro_event.strip()
    
    if has_macro:
        # Defaults for macro if not provided
        m_claim_u = macro_claim_u if macro_claim_u is not None else 0.0
        m_claim_psi = macro_claim_psi if macro_claim_psi is not None else 0.0
        m_real_u = macro_real_u if macro_real_u is not None else 0.0
        m_real_psi = macro_real_psi if macro_real_psi is not None else 0.0

        # Check if micro and macro coordinates are identical
        coordinates_match = (
            claim_u == m_claim_u and
            claim_psi == m_claim_psi and
            real_u == m_real_u and
            real_psi == m_real_psi
        )
        
        if coordinates_match:
            has_macro = False

    if has_macro:
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

        # 3. Determine Inversion (horizontal reflection/mirroring if macro-context is selfish and a positive micro event occurs)
        is_inverted = (m_real_u < 0) and (real_u > 0)

        # 4. Write Inner Box Quadrant Labels (placed on direct 0.5 corners)
        inner_label_opts = {'color': 'white', 'fontsize': 6, 'alpha': 0.5, 'zorder': 3}
        ax.text(0.51, 0.51, "P-LE", ha='right', va='bottom', **inner_label_opts)   # TL corner
        ax.text(-0.51, 0.51, "P-GG", ha='left', va='bottom', **inner_label_opts)  # TR corner
        ax.text(0.51, -0.51, "P-GE", ha='right', va='top', **inner_label_opts)   # BL corner
        ax.text(-0.51, -0.51, "P-LG", ha='left', va='top', **inner_label_opts)  # BR corner

        # 5. Plot Micro Points inside the Inner Box (scaled by 0.5)
        # Horizontally flipped if is_inverted is active
        u_st_plot = (-claim_u if is_inverted else claim_u) * 0.5
        psi_st_plot = claim_psi * 0.5
        u_ac_plot = (-real_u if is_inverted else real_u) * 0.5
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

        # 6. (Connection lines to corners disabled to declutter layout)
        pass

        legend_handles = [macro_claim_pt, macro_real_pt, micro_claim_pt, micro_real_pt]
        path_name = get_path_name(claim_u, claim_psi, real_u, real_psi)
        
        macro_good = (m_real_u >= 0)
        micro_good = (real_u >= 0)
        if macro_good and micro_good:
            frame_desc = "Standard Hegemony: Good Event in Good Macro Frame"
        elif macro_good and not micro_good:
            frame_desc = "Standard Hegemony: Bad Event in Good Macro Frame"
        elif not macro_good and micro_good:
            frame_desc = "Inverted Hegemony: Good Event in Bad Macro Frame"
        else:
            frame_desc = "Inverted Hegemony: Bad Event in Bad Macro Frame"

        title_text = (
            f"{title}\n"
            f"Frame Type: {frame_desc}\n"
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
        if macro_event and macro_event.strip():
            title_text += f"\nMacro Event: {macro_event}"

    # Axis labels
    ax.set_xlabel("Morality (υ)", color='white')
    ax.set_ylabel("Will (ψ)", color='white')
    ax.tick_params(colors='gray')
    ax.set_title(title_text, color='white', pad=25, fontsize=10)

    # Legend, still axes-attached (so it participates correctly in layout/cropping like before),
    # but pushed with a negative x-anchor past the axes' own left edge -- which sits well inboard
    # because of the y-axis label -- so it ends up flush against the actual canvas border instead.
    legend = ax.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(-0.155, -0.13),
                       ncol=1, facecolor='#111111', edgecolor='white', labelcolor='white', fontsize=8)

    # Description block, seated beside the legend on that same row (not centered across the full
    # width, not stacked in its own row) so the canvas doesn't need to grow to fit it. Centered
    # (not left-aligned/cramped) within the space between the legend's right edge and the axes,
    # at a readable font size -- wrap width and position verified against actual rendered
    # bounding boxes to stay clear of the watermark below and the xlabel above.
    description_lines = (
        textwrap.wrap('This graph asks and answers the question "Who does this idea benefit?" measuring Relative Morality.', 100)
        + textwrap.wrap("Benefit is a vector where each unit is 'Scope of Potential'[Group direction, magnitude] cross spectrum of will [active activity to active passivity, magnitude]", 100)
    )
    description_x_center = 0.626  # midpoint between the legend's right edge (~0.30) and the axes right edge (~0.95)
    fig.text(description_x_center, 0.058, '\n'.join(description_lines),
              ha='center', va='center', color='#999999', fontsize=6.5, linespacing=1.4)

    # Watermark label
    fig.text(0.5, 0.01, 'Psochic Hegemony Graph: The map of Good and Evil', ha='center', va='bottom',
             color='#444444', fontsize=9, fontstyle='italic')

    plt.tight_layout()
    plt.savefig(filename, facecolor=fig.get_facecolor(), dpi=300, bbox_inches='tight')
    plt.close(fig)

if __name__ == "__main__":
    # Test a Path of Deception
    draw_graph(-1.0, 1.0, -1.0, -1.0, "Embargo Assessment", "embargo_graph.png")
