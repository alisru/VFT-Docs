import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys
sys.path.insert(0, 'bluesky_bot')

def draw_graph_alchemy_test(claim_u, claim_psi, real_u, real_psi, title, filename):
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='#111111')
    ax.set_facecolor('#111111')

    ax.set_xlim(2.5, -2.5)
    ax.set_ylim(-2.5, 2.5)

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
        "Active-\nActive (+2.0)",
        "Passive-\nActive (+1.0)",
        "Neutral (0.0)",
        "Passive-\nPassive (-1.0)",
        "Active-\nPassive (-2.0)"
    ]

    ax.set_xticklabels(x_labels, fontsize=8, color='white', ha='center')
    ax.set_yticklabels(y_labels, fontsize=8, color='white', va='center')
    ax.grid(True, which='both', color='gray', linestyle=':', linewidth=0.5, alpha=0.3)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)

    # Zone boxes
    zone1 = patches.Rectangle((1.0, -1.0), -2.0, 2.0, fill=False, edgecolor='white', linestyle='--', linewidth=1, zorder=1)
    ax.add_patch(zone1)
    zone2 = patches.Rectangle((2.0, -2.0), -4.0, 4.0, fill=False, edgecolor='white', linestyle='-', linewidth=1.5, zorder=1)
    ax.add_patch(zone2)

    # ── ALCHEMY LABELS: outside zone2 box, inside the axis arms ──────────────
    # These sit in the band between zone2 edge (±2.0) and the axes limit (±2.5)
    # Opacity 0.45, italic, smaller font — background flavour only

    alchemy_opts = dict(color='white', fontsize=9, fontstyle='italic', alpha=0.45, ha='center', va='center', zorder=0)
    quality_opts = dict(color='white', fontsize=8, fontstyle='italic', alpha=0.35, ha='center', va='center', zorder=0)

    # Four corner elements (between zone2 and axis limit, so at ±2.22 approx)
    ax.text( 2.22,  2.22, "AIR",   **alchemy_opts)   # TL: Justice (hot+wet)
    ax.text(-2.22,  2.22, "FIRE",  **alchemy_opts)   # TR: Tyranny (hot+dry)
    ax.text( 2.22, -2.22, "WATER", **alchemy_opts)   # BL: Stagnation (cold+wet)
    ax.text(-2.22, -2.22, "EARTH", **alchemy_opts)   # BR: Chaos (cold+dry)

    # Axis quality labels — midpoint of each arm (between zone2 edge and plot limit)
    ax.text( 0.0,  2.3, "HOT",  **quality_opts)   # Top
    ax.text( 0.0, -2.3, "COLD", **quality_opts)   # Bottom
    ax.text( 2.3,  0.0, "WET",  **quality_opts)   # Left (+υ)
    ax.text(-2.3,  0.0, "DRY",  **quality_opts)   # Right (-υ)

    # ── Inner zone labels ─────────────────────────────────────────────────────
    font_opts = {'color': 'white', 'fontsize': 10, 'ha': 'center', 'va': 'center'}
    ax.text( 1.0+0.1,  1.0+0.1, "The Greater Good\n(Flow)",   **font_opts)
    ax.text(-1.0-0.1,  1.0+0.1, "The Greatest Lie\n(Greed)",  **font_opts)
    ax.text( 1.0+0.1, -1.0-0.1, "The Lesser Good\n(Peace)",   **font_opts)
    ax.text(-1.0-0.1, -1.0-0.1, "The Greater Evil\n(Void)",   **font_opts)

    # Outer corner labels
    ax.text( 1.9,  1.9, "JUSTICE",    color='white', fontsize=10, ha='left',  va='top')
    ax.text(-1.9,  1.9, "TYRANNY",    color='white', fontsize=10, ha='right', va='top')
    ax.text( 1.9, -1.9, "STAGNATION", color='white', fontsize=10, ha='left',  va='bottom')
    ax.text(-1.9, -1.9, "CHAOS",      color='white', fontsize=10, ha='right', va='bottom')

    # ── Plot points ───────────────────────────────────────────────────────────
    claim_pt, = ax.plot(claim_u, claim_psi, marker='o', color='yellow', markersize=10,
                        fillstyle='none', markeredgewidth=2, label="Stated Claim", zorder=3)
    real_pt,  = ax.plot(real_u,  real_psi,  marker='*', color='red',    markersize=15,
                        label="Actual Reality", zorder=3)

    ax.annotate("",
                xy=(real_u, real_psi), xycoords='data',
                xytext=(claim_u, claim_psi), textcoords='data',
                arrowprops=dict(arrowstyle="->", color="white", linestyle="dashed",
                                linewidth=1.5, connectionstyle="arc3,rad=-0.2"),
                zorder=3)

    ax.set_xlabel("Morality (υ)", color='white')
    ax.set_ylabel("Will (ψ)", color='white')
    ax.tick_params(colors='gray')
    title_text = f"{title}\nStated: ({claim_u:+.1f}, {claim_psi:+.1f})  |  Actual: ({real_u:+.1f}, {real_psi:+.1f})"
    ax.set_title(title_text, color='white', pad=25, fontsize=10)

    legend = ax.legend(handles=[claim_pt, real_pt], loc='upper center',
                       bbox_to_anchor=(0.5, -0.15), ncol=2,
                       facecolor='#111111', edgecolor='white', labelcolor='white', fontsize=8)

    fig.text(0.5, 0.01, 'Psychic Hegemony Graph', ha='center', va='bottom',
             color='#444444', fontsize=9, fontstyle='italic')

    plt.tight_layout()
    plt.savefig(filename, facecolor=fig.get_facecolor(), dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {filename}")

draw_graph_alchemy_test(
    0.5, 0.5, -0.8, -0.5,
    "Scott Morrison joins India-based visa firm",
    "bluesky_bot/graph_png/morrison_bls_visa_alchemy_test.png"
)
