import os
import sys
import json
import textwrap
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = [
    'DejaVu Sans', 'Segoe UI Emoji', 'Arial', 'MS Gothic', 'Yu Gothic', 'SimHei', 'sans-serif'
]
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


def get_path_name(claim_u, claim_psi, real_u, real_psi):
    if abs(claim_u) <= 0.15 and abs(claim_psi) <= 0.15 and abs(real_u) <= 0.15 and abs(real_psi) <= 0.15:
        return "Stasis / Neutral"
    if abs(claim_u) <= 0.15 and abs(claim_psi) <= 0.15:
        origin = "Neutral"
    elif claim_u > 0 and claim_psi > 0:
        origin = "GG"
    elif claim_u <= 0 and claim_psi > 0:
        origin = "GL"
    elif claim_u > 0 and claim_psi <= 0:
        origin = "LG"
    else:
        origin = "GE"

    if abs(real_u) <= 0.15 and abs(real_psi) <= 0.15:
        dest = "Neutral"
    elif real_u > 0 and real_psi > 0:
        dest = "GG"
    elif real_u <= 0 and real_psi > 0:
        dest = "GL"
    elif real_u > 0 and real_psi <= 0:
        dest = "LG"
    else:
        dest = "GE"

    if origin == dest:
        if origin == "GG":
            dist = ((claim_u - real_u) ** 2 + (claim_psi - real_psi) ** 2) ** 0.5
            if real_u < claim_u or real_psi < claim_psi:
                return "Small Fall from Grace" if dist <= 0.8 else "Fall from Grace"
            return "Grace"
        return {"GL": "Deception", "LG": "Compromise", "GE": "Destruction", "Neutral": "Stasis / Neutral"}.get(dest, "Stasis")

    geodesic_matrix = {
        ("GG", "GE"): "Fall into Destruction",
        ("GG", "GL"): "Fall into Deception",
        ("GG", "LG"): "Fall from Grace",
        ("GG", "Neutral"): "Fall into Stasis",
        ("LG", "GG"): "Awakening into Grace",
        ("LG", "GE"): "Fall into Destruction",
        ("LG", "GL"): "Fall into Deception",
        ("LG", "Neutral"): "Compromise to Stasis",
        ("GL", "GG"): "Revelation into Grace",
        ("GL", "LG"): "Revelation into Redemption",
        ("GL", "GE"): "Descent into Destruction",
        ("GL", "Neutral"): "Deception to Stasis",
        ("GE", "GG"): "Reckoning into Grace",
        ("GE", "LG"): "Reckoning into Redemption",
        ("GE", "GL"): "Descent into Deception",
        ("GE", "Neutral"): "Destruction to Stasis",
        ("Neutral", "GG"): "Emergence into Grace",
        ("Neutral", "LG"): "Emergence into Compromise",
        ("Neutral", "GL"): "Fall into Deception",
        ("Neutral", "GE"): "Fall into Destruction",
    }
    return geodesic_matrix.get((origin, dest), "Stasis")


def draw_aita_graph_exact(claim_u, claim_psi, real_u, real_psi, title, filename,
                          verdict="", other_actual=None, third_parties=None):
    """Exact copy of bluesky_bot/generate_graph.py draw_graph() with AITA actors added."""
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='#111111')
    try:
        ax.set_facecolor('#111111')

        # Grid Bounds
        ax.set_xlim(2.5, -2.5)
        ax.set_ylim(-2.5, 2.5)

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
        ax.axhline(0, color='gray', linewidth=0.5)
        ax.axvline(0, color='gray', linewidth=0.5)

        green_attractors = [(1.0, 1.0, '#00FF00', 32), (1.0, 0.0, '#98FB98', 22), (1.0, -1.0, '#98FB98', 16)]
        red_attractors = [(-1.0, -1.0, '#FF0000', 32), (-1.0, 0.0, '#FF9999', 22), (-1.0, 1.0, '#FF9999', 16)]

        grid_res = 256
        gx = np.linspace(2.0, -2.0, grid_res)
        gy = np.linspace(2.0, -2.0, grid_res)
        U, PSI = np.meshgrid(gx, gy)

        field_sigma = 1.3
        max_size = 32.0

        judgement_points = [(claim_u, claim_psi), (real_u, real_psi)]
        if other_actual is not None:
            judgement_points.append((float(other_actual[0]), float(other_actual[1])))
        green_lean = sum(max(ju, 0.0) / 2.0 for ju, _jp in judgement_points)
        red_lean = sum(max(-ju, 0.0) / 2.0 for ju, _jp in judgement_points)
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

        judgement_exaggeration = 2.0
        white_exaggeration = 3.5

        def judgement_pull():
            green_total = np.zeros_like(U)
            red_total = np.zeros_like(U)
            white_total = np.zeros_like(U)
            for ju, jpsi in judgement_points:
                cv = np.clip(ju / 2.0, -1.0, 1.0)
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
        hue_t = red_pull / (green_pull + red_pull + 1e-9)
        rgba = hegemony_cmap(hue_t)
        white_fraction = white_pull / (green_pull + red_pull + white_pull + 1e-9)
        rgba[..., 0:3] = rgba[..., 0:3] * (1.0 - white_fraction[..., None]) + 1.0 * white_fraction[..., None]
        rgba[..., 3] = 0.30
        ax.imshow(rgba, extent=[2.0, -2.0, -2.0, 2.0], aspect='equal', zorder=0.05)
        ax.set_aspect('equal', adjustable='box')

        zone1 = patches.Rectangle((1.0, -1.0), -2.0, 2.0, fill=False, edgecolor='white', linestyle='--', linewidth=1, zorder=1)
        ax.add_patch(zone1)

        zone2 = patches.Rectangle((2.0, -2.0), -4.0, 4.0, fill=False, edgecolor='white', linestyle='-', linewidth=1.5, zorder=1)
        ax.add_patch(zone2)

        attractor_opts = dict(markeredgewidth=0, alpha=0.75, zorder=2)
        for au, apsi, color, size in green_attractors + red_attractors:
            ax.plot(au, apsi, marker='o', color=color, markersize=size, **attractor_opts)

        alchemy_opts = dict(color='white', fontsize=9, fontstyle='italic', alpha=0.45, ha='center', va='center', zorder=0)
        quality_opts = dict(color='white', fontsize=8, fontstyle='italic', alpha=0.35, ha='center', va='center', zorder=0)

        ax.text(2.22, 2.22, "AIR", **alchemy_opts)
        ax.text(-2.22, 2.22, "FIRE", **alchemy_opts)
        ax.text(2.22, -2.22, "WATER", **alchemy_opts)
        ax.text(-2.22, -2.22, "EARTH", **alchemy_opts)

        ax.text(0.0, 2.15, "HOT", **quality_opts)
        ax.text(0.0, -2.15, "COLD", **quality_opts)
        ax.text(2.3, 0.0, "WET", **quality_opts)
        ax.text(-2.3, 0.0, "DRY", **quality_opts)

        font_opts = {'color': 'white', 'fontsize': 10, 'ha': 'center', 'va': 'center', 'zorder': 4}

        ax.text(1.0 + 0.1, 1.0 + 0.1, "The Greater Good\n(Flow)", **font_opts)
        ax.text(-1.0 - 0.1, 1.0 + 0.1, "The Greatest Lie\n(Greed)", **font_opts)
        ax.text(1.0 + 0.1, -1.0 - 0.1, "The Lesser Good\n(Peace)", **font_opts)
        ax.text(-1.0 - 0.1, -1.0 - 0.1, "The Greater Evil\n(Void)", **font_opts)

        ax.text(1.9, 1.9, "PRODUCTIVE\n(Joy)", color='white', fontsize=10, ha='left', va='top', zorder=4)
        ax.text(-1.9, 1.9, "REDUCTIVE\n(Anger)", color='white', fontsize=10, ha='right', va='top', zorder=4)
        ax.text(1.9, -1.9, "CONSTRUCTIVE\n(Peace)", color='white', fontsize=10, ha='left', va='bottom', zorder=4)
        ax.text(-1.9, -1.9, "REGRESSIVE\n(Depression)", color='white', fontsize=10, ha='right', va='bottom', zorder=4)

        def draw_hegemony_cross(ax, scale=1.0, rotation_deg=0.0, alpha=0.25, color='white', zorder=0.8):
            rad = np.radians(rotation_deg)
            cos_r, sin_r = np.cos(rad), np.sin(rad)

            def rot(u, psi):
                return u * cos_r - psi * sin_r, u * sin_r + psi * cos_r

            p_ge_u, p_ge_psi = rot(-1.0 * scale, -1.0 * scale)
            p_tl_u, p_tl_psi = rot(2.0 * scale, 2.0 * scale)
            p_lg_u, p_lg_psi = rot(1.0 * scale, -1.0 * scale)
            p_le_u, p_le_psi = rot(-1.0 * scale, 1.0 * scale)

            lw = 14 * scale
            cross_opts = dict(color=color, alpha=alpha, solid_capstyle='butt', zorder=zorder)
            ax.plot([p_ge_u, p_tl_u], [p_ge_psi, p_tl_psi], linewidth=lw, **cross_opts)
            ax.plot([p_lg_u, p_le_u], [p_lg_psi, p_le_psi], linewidth=lw, **cross_opts)

        draw_hegemony_cross(ax, scale=1.0, rotation_deg=0.0, alpha=0.25, color='#CCCCCC', zorder=0.8)

        mag = np.hypot(real_u, real_psi)
        if mag > 0.05:
            target_angle = np.degrees(np.arctan2(real_psi, real_u))
            rot_angle = target_angle - 45.0
            draw_hegemony_cross(ax, scale=0.55, rotation_deg=rot_angle, alpha=0.50, color='white', zorder=0.9)

        # OP Stated + OP Actual (exact generate_graph.py markers) + AITA Counterparty & Third Parties
        claim_point, = ax.plot(claim_u, claim_psi, marker='o', color='yellow', markersize=10, fillstyle='none', markeredgewidth=2, label=f"OP Stated ({claim_u:+.2f}, {claim_psi:+.2f})", zorder=3)
        real_point, = ax.plot(real_u, real_psi, marker='*', color='#38BDF8', markeredgecolor='white', markeredgewidth=0.7, markersize=15, label=f"OP Actual ({real_u:+.2f}, {real_psi:+.2f})", zorder=3)
        legend_handles = [claim_point, real_point]

        if other_actual is not None:
            oth_u, oth_psi = float(other_actual[0]), float(other_actual[1])
            other_point, = ax.plot(oth_u, oth_psi, marker='D', color='red', markeredgecolor='white', markeredgewidth=0.8, markersize=10, label=f"Counterparty ({oth_u:+.2f}, {oth_psi:+.2f})", zorder=3)
            legend_handles.append(other_point)

        tp_markers = ['^', 's', 'P', 'X']
        tp_colors = ['#A855F7', '#10B981', '#F97316', '#EC4899']
        tp_offsets = [(8, 8), (8, -14), (-52, 8), (-52, -14)]
        for idx, tp in enumerate(third_parties or []):
            tu = float(tp.get("upsilon", 0.0))
            tpsi = float(tp.get("psi", 0.0))
            tname = tp.get("actor", f"3rd Party {idx+1}").split("(")[0].strip()
            mk = tp_markers[idx % len(tp_markers)]
            col = tp_colors[idx % len(tp_colors)]
            p_tp, = ax.plot(tu, tpsi, marker=mk, color=col, markeredgecolor='white', markeredgewidth=0.7, markersize=9, label=f"{tname} ({tu:+.2f}, {tpsi:+.2f})", zorder=3)
            legend_handles.append(p_tp)
            ax.annotate(tname, (tu, tpsi), textcoords="offset points", xytext=tp_offsets[idx % len(tp_offsets)],
                        color=col, fontsize=7.5, fontweight='bold', zorder=5)

        path_name = get_path_name(claim_u, claim_psi, real_u, real_psi)

        ax.annotate("",
                    xy=(real_u, real_psi), xycoords='data',
                    xytext=(claim_u, claim_psi), textcoords='data',
                    arrowprops=dict(arrowstyle="->", color="white", linestyle="dashed", linewidth=1.5, connectionstyle="arc3,rad=-0.2"),
                    zorder=3)

        safe_title = "\n".join(textwrap.wrap(str(title).replace('$', r'\$'), 62))
        verdict_tag = f"Verdict: {verdict}  |  " if verdict else ""
        title_text = f"{safe_title}\n{verdict_tag}Projected Eventuality: {path_name}\nOP Stated: ({claim_u:+.2f}, {claim_psi:+.2f})  |  OP Actual: ({real_u:+.2f}, {real_psi:+.2f})"

        ax.set_xlabel("Morality (υ)", color='white')
        ax.set_ylabel("Will (ψ)", color='white')
        ax.tick_params(colors='gray')
        ax.set_title(title_text, color='white', pad=25, fontsize=10)

        ax.legend(handles=legend_handles, loc='upper center', bbox_to_anchor=(0.5, -0.11),
                  ncol=2, facecolor='#111111', edgecolor='white', labelcolor='white', fontsize=8.5)

        plt.tight_layout()

        description_lines = (
            textwrap.wrap('This graph asks and answers the question "Who does this idea benefit?" measuring Relative Morality.', 112)
            + textwrap.wrap("Benefit is a vector where each unit is 'Scope of Potential'[Group direction, magnitude] cross spectrum of will [active activity to active passivity, magnitude]", 112)
            + textwrap.wrap("The Greater Cross points the way to Good and Joy, its smaller paths lead nowhere. The smaller cross points to the consequences of your choices and actions, the smaller paths what you could but didn't do.", 112)
            + textwrap.wrap("Your responsibility is whether you'll choose to align with or against Good", 112)
        )
        desc_y = -0.22 if len(legend_handles) <= 4 else -0.26
        ax.text(0.50, desc_y, '\n'.join(description_lines), transform=ax.transAxes,
                ha='center', va='top', color='#999999', fontsize=8.5, linespacing=1.25)

        ax.text(0.50, desc_y - 0.145, 'Psochic Hegemony Graph: The map of Good and Evil', transform=ax.transAxes,
                ha='center', va='top', color='#444444', fontsize=9, fontstyle='italic')

        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        plt.savefig(filename, facecolor=fig.get_facecolor(), dpi=300, bbox_inches='tight')
        print(f"AITA Graph generated: {filename}")
    finally:
        plt.close(fig)


def generate_aita_graph(case_data, output_path):
    """Wrapper extracting AITA actors from evaluated JSON and calling draw_aita_graph_exact()."""
    ev = case_data.get("evaluation") or case_data.get("vft_appendix") or {}
    coords = ev.get("coordinates", {})
    op_stated = coords.get("op_stated", [case_data.get("claim_u", 0.0), case_data.get("claim_psi", 0.0)])
    op_actual = coords.get("op_actual", [case_data.get("real_u", 0.0), case_data.get("real_psi", 0.0)])
    other_actual = coords.get("other_actual")
    third_parties = list(coords.get("third_parties", []))
    actor_aspects = ev.get("actor_aspects") or []
    if not third_parties and actor_aspects:
        for a in actor_aspects:
            role = (a.get("role") or "").lower()
            if role in ("op", "primary counterparty") or (a.get("actor") or "").upper() == "OP":
                continue
            third_parties.append({
                "actor": f"{a.get('actor', 'Actor')} ({a.get('role', '')})".strip(),
                "upsilon": a.get("son_u", 0.0),
                "psi": a.get("son_psi", 0.0),
            })

    verdict = case_data.get("verdict") or ev.get("verdict", "")
    title = case_data.get("title") or case_data.get("subject") or "AITA Moral Vector Assessment"
    draw_aita_graph_exact(
        float(op_stated[0]), float(op_stated[1]),
        float(op_actual[0]), float(op_actual[1]),
        title, output_path,
        verdict=verdict,
        other_actual=other_actual,
        third_parties=third_parties,
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python aita_graph_generator.py <case_json_path> [output_png_path]")
        sys.exit(1)
    json_path = sys.argv[1]
    with open(json_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    data = raw[0] if isinstance(raw, list) else raw
    out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(json_path)[0] + "_graph.png"
    generate_aita_graph(data, out_path)
