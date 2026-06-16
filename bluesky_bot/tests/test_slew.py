import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Helper to determine trajectory path name
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

def draw_test_graph(claim_u, claim_psi, real_u, real_psi, title, filename,
                    macro_event="", macro_claim_u=None, macro_claim_psi=None, macro_real_u=None, macro_real_psi=None,
                    hide_inner_labels=False, hide_inner_corners=True, show_projection_lines=False,
                    macro_claim_desc="", macro_real_desc="", micro_claim_desc="", micro_real_desc=""):
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='#111111')
    ax.set_facecolor('#111111')

    # Grid Bounds
    ax.set_xlim(2.5, -2.5) # Reversed X axis
    ax.set_ylim(-2.5, 2.5)

    x_ticks = [2.0, 1.0, 0.5, 0.0, -0.5, -1.0, -2.0]
    y_ticks = [2.0, 1.0, 0.0, -1.0, -2.0]
    
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    
    x_labels = ["Everyone\n(+2.0)", "Others\n(+1.0)", "Other\n(+0.5)", "No One\n(0.0)", "My Group\n(-0.5)", "Me\n(-1.0)", "Only Me\n(-2.0)"]
    y_labels = ["Active-\nActive (+2.0)", "Passive-\nActive (+1.0)", "Neutral (0.0)", "Passive-\nPassive (-1.0)", "Active-\nPassive (-2.0)"]
    
    ax.set_xticklabels(x_labels, fontsize=8, color='white', ha='center')
    ax.set_yticklabels(y_labels, fontsize=8, color='white', va='center')
    
    ax.grid(True, which='both', color='gray', linestyle=':', linewidth=0.5, alpha=0.3)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)

    # Zone 1 and Zone 2
    zone1 = patches.Rectangle((1.0, -1.0), -2.0, 2.0, fill=False, edgecolor='white', linestyle='--', linewidth=1, zorder=1)
    ax.add_patch(zone1)
    zone2 = patches.Rectangle((2.0, -2.0), -4.0, 4.0, fill=False, edgecolor='white', linestyle='-', linewidth=1.5, zorder=1)
    ax.add_patch(zone2)

    font_opts = {'color': 'white', 'fontsize': 10, 'ha': 'center', 'va': 'center'}
    ax.text(1.0 + 0.1, 1.0 + 0.1, "The Greater Good\n(Flow)", **font_opts)
    ax.text(-1.0 - 0.1, 1.0 + 0.1, "The Greatest Lie\n(Greed)", **font_opts)
    ax.text(1.0 + 0.1, -1.0 - 0.1, "The Lesser Good\n(Peace)", **font_opts)
    ax.text(-1.0 - 0.1, -1.0 - 0.1, "The Greater Evil\n(Void)", **font_opts)

    # Strategic Extremes
    ax.text(1.9, 1.9, "JUSTICE", color='white', fontsize=10, ha='left', va='top')
    ax.text(-1.9, 1.9, "TYRANNY", color='white', fontsize=10, ha='right', va='top')
    ax.text(1.9, -1.9, "STAGNATION", color='white', fontsize=10, ha='left', va='bottom')
    ax.text(-1.9, -1.9, "CHAOS", color='white', fontsize=10, ha='right', va='bottom')

    has_macro = macro_event and macro_event.strip()
    
    m_claim_u = macro_claim_u if macro_claim_u is not None else 0.0
    m_claim_psi = macro_claim_psi if macro_claim_psi is not None else 0.0
    m_real_u = macro_real_u if macro_real_u is not None else 0.0
    m_real_psi = macro_real_psi if macro_real_psi is not None else 0.0
    
    coordinates_match = (
        claim_u == m_claim_u and
        claim_psi == m_claim_psi and
        real_u == m_real_u and
        real_psi == m_real_psi
    )
    
    if has_macro and not coordinates_match:
        # 1. Plot Macro Points
        macro_claim_pt, = ax.plot(m_claim_u, m_claim_psi, marker='o', color='yellow', markersize=10, 
                                  fillstyle='none', markeredgewidth=2, label="Macro Stated", zorder=3)
        macro_real_pt, = ax.plot(m_real_u, m_real_psi, marker='*', color='red', markersize=15, 
                                 label="Macro Actual", zorder=3)
        
        ax.annotate("",
                    xy=(m_real_u, m_real_psi), xycoords='data',
                    xytext=(m_claim_u, m_claim_psi), textcoords='data',
                    arrowprops=dict(arrowstyle="->", color="white", linestyle="dashed", linewidth=1.5, connectionstyle="arc3,rad=-0.2"),
                    zorder=3)

        # 2. Draw Nested Inner Box
        inner_box = patches.Rectangle((0.5, -0.5), -1.0, 1.0, fill=True, facecolor='#161616', 
                                      edgecolor='white', linestyle='-', linewidth=1.5, zorder=2)
        ax.add_patch(inner_box)
        ax.plot([0.5, -0.5], [0.0, 0.0], color='gray', linestyle='-', linewidth=0.5, alpha=0.5, zorder=2)
        ax.plot([0.0, 0.0], [-0.5, 0.5], color='gray', linestyle='-', linewidth=0.5, alpha=0.5, zorder=2)

        is_inverted = (m_real_u < 0) and (real_u > 0)

        # 3. Handle Inner Box Quadrant Labels (placed on direct 0.5 corners)
        if not hide_inner_labels:
            # We offset slightly to place labels just outside the corners of the inner box
            inner_label_opts = {'color': 'white', 'fontsize': 6, 'alpha': 0.5, 'zorder': 3}
            ax.text(0.51, 0.51, "P-LE", ha='right', va='bottom', **inner_label_opts)   # TL corner
            ax.text(-0.51, 0.51, "P-GG", ha='left', va='bottom', **inner_label_opts)  # TR corner
            ax.text(0.51, -0.51, "P-GE", ha='right', va='top', **inner_label_opts)   # BL corner
            ax.text(-0.51, -0.51, "P-LG", ha='left', va='top', **inner_label_opts)  # BR corner

        # 4. Handle Inner Corner Tags
        if not hide_inner_corners:
            corner_font_tl = {'color': '#cccccc', 'fontsize': 5.5, 'ha': 'right', 'va': 'bottom', 'zorder': 3}
            corner_font_tr = {'color': '#cccccc', 'fontsize': 5.5, 'ha': 'left', 'va': 'bottom', 'zorder': 3}
            corner_font_bl = {'color': '#cccccc', 'fontsize': 5.5, 'ha': 'right', 'va': 'top', 'zorder': 3}
            corner_font_br = {'color': '#cccccc', 'fontsize': 5.5, 'ha': 'left', 'va': 'top', 'zorder': 3}
            
            if is_inverted:
                ax.text(0.53, 0.53, "TYRANNY", **corner_font_tl)
                ax.text(-0.53, 0.53, "JUSTICE", **corner_font_tr)
                ax.text(0.53, -0.53, "CHAOS", **corner_font_bl)
                ax.text(-0.53, -0.53, "STAGNATION", **corner_font_br)
            else:
                ax.text(0.53, 0.53, "JUSTICE", **corner_font_tl)
                ax.text(-0.53, 0.53, "TYRANNY", **corner_font_tr)
                ax.text(0.53, -0.53, "STAGNATION", **corner_font_bl)
                ax.text(-0.53, -0.53, "CHAOS", **corner_font_br)

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

        ax.annotate("",
                    xy=(u_ac_plot, psi_ac_plot), xycoords='data',
                    xytext=(u_st_plot, psi_st_plot), textcoords='data',
                    arrowprops=dict(arrowstyle="->", color="white", linestyle="dashed", linewidth=1.0, connectionstyle="arc3,rad=-0.2"),
                    zorder=4)

        # 6. Optional connection lines
        if show_projection_lines:
            def get_corner(u, psi):
                u_c = 0.5 if u >= 0 else -0.5
                psi_c = 0.5 if psi >= 0 else -0.5
                return u_c, psi_c

            c_st_u, c_st_psi = get_corner(m_claim_u, m_claim_psi)
            ax.plot([m_claim_u, c_st_u], [m_claim_psi, c_st_psi], color='gray', linestyle='--', linewidth=0.5, alpha=0.3, zorder=1)
            c_ac_u, c_ac_psi = get_corner(m_real_u, m_real_psi)
            ax.plot([m_real_u, c_ac_u], [m_real_psi, c_ac_psi], color='gray', linestyle='--', linewidth=0.5, alpha=0.3, zorder=1)

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

        if macro_claim_desc:
            title_text = (
                f"{title}\n"
                f"Frame Type: {frame_desc} | Projected Eventuality: {path_name}\n"
                f"Micro Stated ({claim_u:+.1f}, {claim_psi:+.1f}): {micro_claim_desc}\n"
                f"Micro Actual ({real_u:+.1f}, {real_psi:+.1f}): {micro_real_desc}\n"
                f"Macro Stated ({m_claim_u:+.1f}, {m_claim_psi:+.1f}): {macro_claim_desc}\n"
                f"Macro Actual ({m_real_u:+.1f}, {m_real_psi:+.1f}): {macro_real_desc}"
            )
        else:
            title_text = (
                f"{title}\n"
                f"Frame Type: {frame_desc}\n"
                f"Projected Eventuality: {path_name}\n"
                f"Micro: Stated ({claim_u:+.1f}, {claim_psi:+.1f}) | Actual ({real_u:+.1f}, {real_psi:+.1f})\n"
                f"Macro: Stated ({m_claim_u:+.1f}, {m_claim_psi:+.1f}) | Actual ({m_real_u:+.1f}, {m_real_psi:+.1f})"
            )
    else:
        # Standard Single-Level Graph Plotting
        claim_point, = ax.plot(claim_u, claim_psi, marker='o', color='yellow', markersize=10, fillstyle='none', markeredgewidth=2, label="Stated Claim", zorder=3)
        real_point, = ax.plot(real_u, real_psi, marker='*', color='red', markersize=15, label="Actual Reality", zorder=3)

        path_name = get_path_name(claim_u, claim_psi, real_u, real_psi)
        ax.annotate("",
                    xy=(real_u, real_psi), xycoords='data',
                    xytext=(claim_u, claim_psi), textcoords='data',
                    arrowprops=dict(arrowstyle="->", color="white", linestyle="dashed", linewidth=1.5, connectionstyle="arc3,rad=-0.2"),
                    zorder=3)

        legend_handles = [claim_point, real_point]
        title_text = f"{title}\nProjected Eventuality: {path_name}\nStated: ({claim_u:+.1f}, {claim_psi:+.1f})  |  Actual: ({real_u:+.1f}, {real_psi:+.1f})"

    ax.set_xlabel("Morality (υ)", color='white')
    ax.set_ylabel("Will (ψ)", color='white')
    ax.tick_params(colors='gray')
    ax.set_title(title_text, color='white', pad=15, fontsize=8.5)
    
    # Place Legend at the bottom center to avoid any overlap with TR (TYRANNY) or other text
    ax.legend(handles=legend_handles, loc='upper center', bbox_to_anchor=(0.5, -0.15),
              ncol=2 if len(legend_handles)<=2 else 4, facecolor='#111111', edgecolor='white', labelcolor='white', fontsize=8)
    
    fig.text(0.5, 0.01, 'Psychic Hegemony Graph', ha='center', va='bottom', color='#444444', fontsize=9, fontstyle='italic')
    
    plt.savefig(filename, facecolor=fig.get_facecolor(), dpi=300, bbox_inches='tight')
    plt.close(fig)

# Slew Generation
def main():
    out_dir = r"E:\Vector Field Theory\VFT Docs\_AI files and chat logs\test_runs"
    os.makedirs(out_dir, exist_ok=True)
    
    # 16 cases with positive macro context (macro_real_u >= 0)
    pos_macro_cases = [
        # (claim_u, claim_psi, real_u, real_psi, m_claim_u, m_claim_psi, m_real_u, m_real_psi)
        (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),      # P1: TL -> TL micro, TL -> TL macro
        (1.0, 1.0, -1.0, -1.0, 1.5, 0.5, 1.0, 1.0),    # P2: TL -> BR micro, TL -> TL macro
        (-1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0),    # P3: TR -> BL micro, TL -> TL macro
        (1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 0.5, 0.5),    # P4: BL -> TR micro, TL -> TL macro
        (0.5, 0.5, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0),      # P5: TL -> TL micro (scaled), TL -> TL macro
        (1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0),     # P6: TL -> BL micro, TL -> TL macro
        (1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),     # P7: BL -> TL micro, TL -> TL macro
        (-1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0),   # P8: BR -> TR micro, TL -> TL macro
        (-1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0),   # P9: TR -> BR micro, TL -> TL macro
        (-1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),    # P10: BR -> TL micro, TL -> TL macro
        (1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0),     # P11: TL -> TR micro, TL -> TL macro
        (-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),     # P12: TR -> TL micro, TL -> TL macro
        (1.5, -0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0),     # P13: BL -> TL micro, TL -> TL macro
        (-0.5, -0.5, -1.5, -1.5, 1.0, 1.0, 1.0, 1.0),  # P14: BR -> BR micro, TL -> TL macro
        (1.0, 0.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0),      # P15: TL boundary micro, TL -> TL macro
        (0.0, 1.0, -1.0, 0.0, 1.0, 1.0, 1.0, 1.0),     # P16: TR boundary micro, TL -> TL macro
    ]

    # 16 cases with negative macro context (macro_real_u < 0) -> triggers horizontal flip
    neg_macro_cases = [
        # (claim_u, claim_psi, real_u, real_psi, m_claim_u, m_claim_psi, m_real_u, m_real_psi)
        (1.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0, -1.0),     # N1: TL -> TL micro, TL -> BR macro
        (1.0, 1.0, -1.0, -1.0, 1.0, 0.0, -1.0, -1.0),   # N2: TL -> BR micro, TL -> BR macro
        (-1.0, 1.0, -1.0, -1.0, 1.0, 0.0, -1.0, -1.0),   # N3: TR -> BR micro (bad stays bad), TL -> BR macro
        (1.0, -1.0, -1.0, 1.0, 1.0, 0.0, -1.0, -1.0),   # N4: BL -> TR micro, TL -> BR macro
        (0.5, 0.5, 1.5, 1.5, 1.0, 0.0, -1.0, -1.0),     # N5: TL -> TL micro (scaled), TL -> BR macro
        (1.0, 1.0, 1.0, -1.0, 1.0, 0.0, -1.0, -1.0),    # N6: TL -> BL micro, TL -> BR macro
        (1.0, -1.0, 1.0, 1.0, 1.0, 0.0, -1.0, -1.0),    # N7: BL -> TL micro, TL -> BR macro
        (-1.0, -1.0, -1.0, 1.0, 1.0, 0.0, -1.0, -1.0),  # N8: BR -> TR micro, TL -> BR macro
        (-1.0, 1.0, -1.0, -1.0, 1.0, 0.0, -1.0, -1.0),  # N9: TR -> BR micro, TL -> BR macro
        (-1.0, -1.0, 1.0, 1.0, 1.0, 0.0, -1.0, -1.0),   # N10: BR -> TL micro, TL -> BR macro
        (1.0, 1.0, -1.0, 1.0, 1.0, 0.0, -1.0, -1.0),    # N11: TL -> TR micro, TL -> BR macro
        (-1.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0, -1.0),    # N12: TR -> TL micro, TL -> BR macro
        (1.5, -0.5, 0.5, 0.5, 1.0, 0.0, -1.0, -1.0),    # N13: BL -> TL micro, TL -> BR macro
        (-0.5, -0.5, -1.5, -1.5, 1.0, 0.0, -1.0, -1.0), # N14: BR -> BR micro, TL -> BR macro
        (1.0, 0.0, 1.0, 1.0, 1.0, 0.0, -1.0, -1.0),     # N15: TL boundary micro, TL -> BR macro
        (0.0, 1.0, -1.0, 0.0, 1.0, 0.0, -1.0, -1.0),    # N16: TR boundary micro, TL -> BR macro
    ]

    pos_macro_scenarios = [
        (
            "Case P1: State Literacy Program & Reading Coaches",
            "State Literacy Program",
            "State government launches statewide literacy program to raise reading scores across all public schools",
            "Every school receives trained teachers and resources; reading scores rise district-wide",
            "Local school hires specialist reading coaches funded by the state program",
            "Reading coaches hired and embedded; measurable improvement in student outcomes"
        ),
        (
            "Case P2: City Public Park & Contractor Playground Theft",
            "City Public Park Initiative",
            "City council launches a public park initiative to build green community spaces for all residents",
            "The park opens on schedule; a vibrant, well-maintained community space is delivered",
            "A private contractor is hired to build a state-of-the-art playground inside the new park",
            "Contractor embezzles the construction funds; playground is never built, leaving a dangerous half-finished site"
        ),
        (
            "Case P3: Charity Kitchen & Price-Gouging Supplier",
            "Charity Kitchen Program",
            "City charity launches a community kitchen program to feed the homeless every day",
            "Hundreds of hot meals served daily; the program becomes a critical community lifeline",
            "A food supplier quotes above-market prices to squeeze maximum profit from the charity",
            "Supplier relents and passively donates surplus vegetables weekly instead of charging full price"
        ),
        (
            "Case P4: Zoning Reforms & Vigilante Community Garden",
            "Zoning Reforms",
            "City planners push affordable zoning housing reforms to ease the housing crisis",
            "Hundreds of affordable housing units approved and built across the city",
            "A neighborhood group passively tends a small community garden on a rezoned lot",
            "Garden group pivots and actively lobbies city council to block apartment construction on the site"
        ),
        (
            "Case P5: National Green Energy & Suburb Solar Surplus",
            "National Green Energy",
            "Federal government launches a national green energy initiative to decarbonize the grid",
            "A national wind farm network is successfully constructed and connected",
            "A suburb installs solar panels on the local town hall roof as a small contribution",
            "Surplus solar output is so large it powers the entire surrounding county, feeding back to the grid"
        ),
        (
            "Case P6: Vaccination Campaign & Pamphlet Clinic",
            "Vaccination Campaign",
            "Health department runs a mass vaccination campaign to protect the public from an outbreak",
            "The majority of the population is vaccinated; the outbreak is contained",
            "A local clinic deploys active mobile vaccination units to reach underserved areas",
            "Clinic scales back to passively distributing pamphlets only, leaving mobile coverage gaps"
        ),
        (
            "Case P7: Famine Relief & NGO Food Logistics",
            "Famine Relief",
            "UN famine relief campaign to deliver emergency food to a drought-hit region",
            "Food trucks and supply chains are established; the region receives critical food aid",
            "A local NGO passively maintains a small food inventory stockpile at a regional warehouse",
            "NGO activates, launching a large-scale logistics campaign that dramatically amplifies food delivery"
        ),
        (
            "Case P8: Open-Source Seed Coalition & Genetic Monopolist",
            "Open-Source Seed Coalition",
            "International coalition develops and releases open-source crop seeds for free public use",
            "Seeds published globally; farmers in 40 countries adopt drought-resistant varieties",
            "A biotech company lets its local heritage seed stocks decay passively, burning inventory",
            "Company actively patents and monopolizes the open-source seed genetics, blocking public access"
        ),
        (
            "Case P9: Literacy Drive & Undercutting Bookstore Chain",
            "Literacy Drive",
            "City literacy drive funds new public library branches in underserved neighborhoods",
            "Three new library branches open; reading programs are established across the city",
            "A private bookstore chain aggressively undercuts library events and price-gouges book fairs",
            "Bookstore chain goes bankrupt from overextension and closes, leaving a vacant lot near the library"
        ),
        (
            "Case P10: Research Fellowship & Student Open-Source Tool",
            "Research Fellowship",
            "University launches a free research fellowship to accelerate scientific breakthroughs",
            "Multiple peer-reviewed papers published; key breakthroughs achieved across disciplines",
            "A student project within the fellowship is disorganized and wastes significant grant funding",
            "Student team pivots and builds an open-source research tool actively adopted by thousands globally"
        ),
        (
            "Case P11: Animal Shelter Fund & Dog Breeding Pivot",
            "Animal Shelter Fund",
            "City animal shelter fund raises money to build new kennels for stray animals",
            "Modern kennel facility opens; hundreds of animals are rescued and rehomed",
            "A volunteer group promises to actively rescue and foster stray animals alongside the fund",
            "Volunteer group pivots to commercial dog breeding for profit, abandoning stray rescue work"
        ),
        (
            "Case P12: Flood Barrier Sandbags & Scab Labor Volunteer",
            "Flood Barriers",
            "City emergency services deploy flood barriers to protect homes from an incoming storm",
            "Barriers hold; all targeted homes are protected from flood damage",
            "A sandbag supplier gouges the town on emergency pricing during the crisis",
            "A volunteer trucking group arrives, builds the sandbag barrier for free, and undercuts the supplier"
        ),
        (
            "Case P13: Recycling Program & Park Restoration",
            "Public Recycling Program",
            "Council launches a public recycling program to reduce landfill waste",
            "Recycling rates increase; the program achieves its waste diversion targets",
            "A community group passively collects trash in the park only on weekends",
            "Group expands to actively clean and restore the entire local park, going beyond recycling"
        ),
        (
            "Case P14: Business Grant & Bankrupt Shop",
            "Small Business Grants",
            "Government issues small business grants to revitalize struggling local economies",
            "Grants distributed; most participating businesses report increased revenue and hiring",
            "One shop owner spends the grant slowly and keeps poor accounting records",
            "Shop owner goes bankrupt, closes the business, and defaults on remaining obligations"
        ),
        (
            "Case P15: Mars Colonization & Space Debris Cleaner",
            "Mars Colonization",
            "Space agency launches a Mars colonization program to become a multi-planetary species",
            "Ambitions scaled back; program shifts to launching practical weather and communications satellites",
            "A university team starts a space project with neutral early progress, testing orbital mechanics",
            "Team successfully deploys a functioning space debris cleaner that protects orbital corridors"
        ),
        (
            "Case P16: Wildlife Protection & Logging Expansion",
            "Wildlife Protection",
            "Conservation group launches a wildlife protection campaign to preserve national park biodiversity",
            "Protected zones established; park wildlife population stabilizes and recovers",
            "A logging firm actively starts land clearing and makes aggressive territorial access claims",
            "Logging firm transitions to commercial logging operations inside the protected park boundary"
        ),
    ]

    neg_macro_scenarios = [
        (
            "Case N1: Corporate Merger Layoffs & Dedicated Team Leader",
            "Corporate Merger",
            "A corporation claims a merger will increase efficiency and create shared prosperity",
            "Mass layoffs follow; the merged company collapses under debt within two years",
            "A team leader vows to keep the department's project running through the merger chaos",
            "Leader works overtime, delivers the project on time despite zero institutional support"
        ),
        (
            "Case N2: Corrupt Welfare Safety Net & Theft Charity",
            "Welfare Safety Net",
            "Government promises a welfare safety net program to protect the most vulnerable",
            "Officials embezzle the fund; the program goes bankrupt and collapses before helping anyone",
            "A local charity promises to distribute free food to those left behind by the welfare collapse",
            "Charity leadership steals the donations and abandons the community with nothing"
        ),
        (
            "Case N3: Clinic Takeover & Guard Bribe Scheme",
            "Clinic Takeover",
            "A private operator claims it will take over the clinic to improve and modernize healthcare",
            "Operator strips all clinic assets and closes the facility, leaving patients without care",
            "The security guard at the door actively demands bribes to allow patient entry",
            "Guard escalates — permanently locks the medicine cabinet and pockets the key for ongoing extortion"
        ),
        (
            "Case N4: Fake Anti-Corruption Purge & Neighborhood Vigilantes",
            "Anti-Corruption Drive",
            "A new government body promises a sweeping anti-corruption drive to clean up institutions",
            "The drive devolves into chaotic show trials targeting political opponents, not actual corruption",
            "A neighborhood group passively patrols streets to maintain local peace during the upheaval",
            "Group radicalizes into an active mob, hunting and harassing perceived regime dissenters"
        ),
        (
            "Case N5: Toxic Spill & Internal Sustainability Officer Whistleblower",
            "Factory Green Program",
            "A factory launches a green compliance program promising strict environmental safety",
            "Factory dumps toxic waste into the river, destroying the local ecosystem",
            "The factory's own sustainability officer runs modest quarterly compliance audits",
            "Officer documents all violations, goes public, and forces a full plant shutdown and cleanup"
        ),
        (
            "Case N6: Scam Investment & Settlement Warning Blogs",
            "Scam Investment Fund",
            "An investment fund promises high returns to create wealth for ordinary investors",
            "The fund is a scam; it goes bust and wipes out the life savings of its clients",
            "A whistleblower lawyer files active lawsuits to recover client money from the fund's operators",
            "Lawyer quietly pivots to posting passive warning blogs, abandoning the lawsuit campaign"
        ),
        (
            "Case N7: Developer Slum & Community Land Trust Housing",
            "Developer Slum Creation",
            "A real estate developer promises to deliver affordable housing for low-income families",
            "Developer cuts costs and delivers sub-standard slum housing that fails safety inspections",
            "A community land trust passively holds a small garden plot adjacent to the development",
            "Land trust activates and builds community-owned affordable housing on the garden site"
        ),
        (
            "Case N8: Oil Spill & Spill-Data Coverup Lobbyist",
            "Oil Green Transition",
            "An oil company pledges a green energy transition to reduce its environmental footprint",
            "Company causes a catastrophic offshore oil spill, destroying a coastal ecosystem",
            "A cleanup contractor passively lets its spill-cleanup equipment sit unused and degrade",
            "Contractor actively lobbies government to classify spill data as a state secret"
        ),
        (
            "Case N9: Rail Budget Cut Derailment & Supplier Parts Bankruptcy",
            "Rail Company Budget Cuts",
            "A rail company promises to upgrade trains and rail infrastructure for safer travel",
            "Company slashes maintenance budgets instead; a train derails, killing passengers",
            "A parts supplier price-gouges the rail company on critical wheel and brake components",
            "Supplier goes bankrupt mid-contract, halting all parts supply and blocking the repair program"
        ),
        (
            "Case N10: Cartel War & Rebel Neighborhood Defense",
            "Cartel Truce Promise",
            "A regional cartel promises a peace truce to end violence and allow civilian life to resume",
            "Cartel breaks the truce, triggering open gang war that displays thousands of civilians",
            "A local business owner pays the cartel protection money to survive passively",
            "Business owner rebels — organizes an active neighborhood watch that resists cartel extortion"
        ),
        (
            "Case N11: Corrupt Utility Polluter & Filter Copper Theft",
            "Utility Clean Power",
            "A utility company promises a clean power project to replace its polluting coal plants",
            "Company diverts funds and continues polluting, dumping toxic waste into nearby waterways",
            "A utility technician promises to install eco-filters to reduce the ongoing pollution",
            "Technician steals the copper wiring from inside the filters and sells it for scrap"
        ),
        (
            "Case N12: Prison Facility Abuse & Literacy Reading Lessons",
            "Rehabilitation Prison",
            "A prison system launches a rehabilitation program promising reform and inmate education",
            "Administration cuts staff budgets; facility descends into chaos, violence, and neglect",
            "A prison guard actively abuses inmates, violating the stated rehabilitation mandate",
            "A volunteer from the community enters the facility weekly to teach inmates reading lessons"
        ),
        (
            "Case N13: Predatory Loan Company & Client Debt Strike",
            "Predatory Loan Company",
            "A microfinance company promises financial inclusion loans to lift communities out of poverty",
            "The company charges predatory interest rates that bankrupt clients and trap them in debt cycles",
            "A debtor passively refuses to pay the high interest, sitting in non-payment without organizing",
            "Debtor escalates — actively organizes a coordinated client debt strike across the community"
        ),
        (
            "Case N14: Scam Charity Theft & Non-cooperating Elder",
            "Scam Charity",
            "A charity raises funds promising to build a clean water well for a drought-hit village",
            "Charity leadership steals all donation funds; no well is ever built",
            "A village elder complains vocally about the lack of visible progress on the well project",
            "Elder stops coordinating with the charity entirely, withdrawing all community cooperation"
        ),
        (
            "Case N15: Predatory Gym Chain & Trainer Refund Campaign",
            "Gym Chain Promotion",
            "A gym chain promises healthy lifestyle memberships with flexible no-commitment contracts",
            "Contracts turn predatory; members are locked in with hidden exit fees, unable to cancel",
            "A member maintains neutral training attendance, neither fighting nor accepting the contract terms",
            "A personal trainer organizes an active, public refund campaign that wins back member fees"
        ),
        (
            "Case N16: Sub-standard Housing Developer & Construction Price-Gouging",
            "Housing Development",
            "A developer promises to build standard quality housing for a growing residential area",
            "Corrupt developer substitutes cheap materials and delivers structurally unsafe slums",
            "A construction supplier aggressively hikes prices on all materials used in the development",
            "Supplier locks in price-gouging contracts for the entire remaining supply chain delivery"
        ),
    ]

    print("Generating 16 Positive Macro Context Cases...")
    for idx, case in enumerate(pos_macro_cases, 1):
        filename = os.path.join(out_dir, f"pos_macro_case_{idx}.png")
        scen_title, macro_evt, m_cl, m_rl, mi_cl, mi_rl = pos_macro_scenarios[idx - 1]
        draw_test_graph(
            claim_u=case[0], claim_psi=case[1], real_u=case[2], real_psi=case[3],
            title=scen_title, filename=filename,
            macro_event=macro_evt,
            macro_claim_u=case[4], macro_claim_psi=case[5],
            macro_real_u=case[6], macro_real_psi=case[7],
            macro_claim_desc=m_cl, macro_real_desc=m_rl,
            micro_claim_desc=mi_cl, micro_real_desc=mi_rl
        )
        print(f"Generated case {idx}: {filename}")

    print("\nGenerating 16 Negative Macro Context Cases (Inverted)...")
    for idx, case in enumerate(neg_macro_cases, 1):
        filename = os.path.join(out_dir, f"neg_macro_case_{idx}.png")
        scen_title, macro_evt, m_cl, m_rl, mi_cl, mi_rl = neg_macro_scenarios[idx - 1]
        draw_test_graph(
            claim_u=case[0], claim_psi=case[1], real_u=case[2], real_psi=case[3],
            title=scen_title, filename=filename,
            macro_event=macro_evt,
            macro_claim_u=case[4], macro_claim_psi=case[5],
            macro_real_u=case[6], macro_real_psi=case[7],
            macro_claim_desc=m_cl, macro_real_desc=m_rl,
            micro_claim_desc=mi_cl, micro_real_desc=mi_rl
        )
        print(f"Generated case {idx}: {filename}")

if __name__ == "__main__":
    main()
