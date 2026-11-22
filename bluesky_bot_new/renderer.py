import os
import sys
import textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['font.sans-serif'] = [
    'DejaVu Sans', 'Segoe UI Emoji', 'Arial', 'MS Gothic', 'Yu Gothic', 'SimHei', 'sans-serif'
]
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image, ImageDraw, ImageFont

# ==============================================================================
# 1. CANONICAL TRAJECTORY GEODESIC CALCULATOR
# ==============================================================================

def get_path_name(claim_u, claim_psi, real_u, real_psi):
    """
    Computes the exact canonical geodesic path name from Stated -> Resulting coordinates.
    Adheres strictly to the Aletheia Evaluator & Trajectory Invariants.
    """
    # Origin deadband: pure stasis / neutral material ground truth
    if abs(claim_u) <= 0.15 and abs(claim_psi) <= 0.15 and abs(real_u) <= 0.15 and abs(real_psi) <= 0.15:
        return "Stasis / Neutral"

    # Determine origin zone
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

    # Determine destination zone
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

    # Same-zone transitions
    if origin == dest:
        if origin == "GG":
            dist = ((claim_u - real_u)**2 + (claim_psi - real_psi)**2)**0.5
            if real_u < claim_u or real_psi < claim_psi:
                return "Small Fall from Grace" if dist <= 0.8 else "Fall from Grace"
            return "Grace"
        zone_stasis = {"GL": "Deception", "LG": "Compromise", "GE": "Destruction", "Neutral": "Stasis / Neutral"}
        return zone_stasis.get(dest, "Stasis")

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


# ==============================================================================
# 2. FULL PSOCHIC HEGEMONY GRAPH GENERATOR
# ==============================================================================

def draw_graph(claim_u, claim_psi, real_u, real_psi, title, filename):
    """
    Draws the full Psochic Hegemony Assessment Graph:
    - Background Morality gradient field
    - 6 Fixed Attractors
    - Background Static Greater Cross (25% opacity)
    - Dynamic Rotating Needle Cross (50% opacity, pointing along Resulting Judgement)
    - Yellow Circle (Stated Claim) -> Red Star (Actual Reality)
    - Complete explanatory footer description block
    """
    fig, ax = plt.subplots(figsize=(8, 8), facecolor='#111111')
    try:
        ax.set_facecolor('#111111')

        # Grid Bounds
        ax.set_xlim(2.5, -2.5)  # Reversed X axis: Left is Positive (+2.0), Right is Negative (-2.0)
        ax.set_ylim(-2.5, 2.5)  # Y axis: Top is Positive (+2.0), Bottom is Negative (-2.0)

        # Ticks and Labels
        ticks = [2.0, 1.0, 0.0, -1.0, -2.0]
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)

        x_labels = [
            "Everyone\n(+2.0)\nEgalitarian",
            "Others\n(+1.0)\nAltruism",
            "No One\n(0.0)\nNeutral",
            "My Group\n(-1.0)\nTribal",
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

        # The Six Attractors of the Hegemony
        green_attractors = [(1.0, 1.0, '#00FF00', 32), (1.0, 0.0, '#98FB98', 22), (1.0, -1.0, '#98FB98', 16)]
        red_attractors = [(-1.0, -1.0, '#FF0000', 32), (-1.0, 0.0, '#FF9999', 22), (-1.0, 1.0, '#FF9999', 16)]

        # Morality Gradient Field
        grid_res = 256
        gx = np.linspace(2.0, -2.0, grid_res)
        gy = np.linspace(2.0, -2.0, grid_res)
        U, PSI = np.meshgrid(gx, gy)

        field_sigma = 1.3
        max_size = 32.0

        judgement_points = [(claim_u, claim_psi), (real_u, real_psi)]
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
        ax.imshow(rgba, extent=[2.0, -2.0, -2.0, 2.0], aspect='auto', zorder=0.05)

        # Zone 1 (The Inner Horizon)
        zone1 = patches.Rectangle((1.0, -1.0), -2.0, 2.0, fill=False, edgecolor='white', linestyle='--', linewidth=1, zorder=1)
        ax.add_patch(zone1)

        # Zone 2 (The Outer Horizon)
        zone2 = patches.Rectangle((2.0, -2.0), -4.0, 4.0, fill=False, edgecolor='white', linestyle='-', linewidth=1.5, zorder=1)
        ax.add_patch(zone2)

        # Attractor markers
        attractor_opts = dict(markeredgewidth=0, alpha=0.75, zorder=2)
        for au, apsi, color, size in green_attractors + red_attractors:
            ax.plot(au, apsi, marker='o', color=color, markersize=size, **attractor_opts)

        # Alchemical elements
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

        # Helper to draw the exact Hegemony Cross (pivoted at 0,0)
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

        # 1. Background Greater Cross (25% opacity, static upright)
        draw_hegemony_cross(ax, scale=1.0, rotation_deg=0.0, alpha=0.25, color='#CCCCCC', zorder=0.8)

        # 2. Dynamic Needle Cross (50% opacity, rotated along Resulting Judgement)
        mag = np.hypot(real_u, real_psi)
        if mag > 0.05:
            target_angle = np.degrees(np.arctan2(real_psi, real_u))
            rot_angle = target_angle - 45.0
            draw_hegemony_cross(ax, scale=0.55, rotation_deg=rot_angle, alpha=0.50, color='white', zorder=0.9)

        # 3. Plot Points
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
        safe_title = str(title).replace('$', r'\$')
        title_text = f"{safe_title}\nProjected Eventuality: {path_name}\nStated: ({claim_u:+.1f}, {claim_psi:+.1f})  |  Actual: ({real_u:+.1f}, {real_psi:+.1f})"

        ax.set_xlabel("Morality (υ)", color='white')
        ax.set_ylabel("Will (ψ)", color='white')
        ax.tick_params(colors='gray')
        ax.set_title(title_text, color='white', pad=25, fontsize=10)

        legend = ax.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(-0.165, -0.055),
                           ncol=1, facecolor='#111111', edgecolor='white', labelcolor='white', fontsize=8)

        plt.tight_layout(rect=[0, 0.14, 1, 1])

        description_lines = (
            textwrap.wrap('This graph asks and answers the question "Who does this idea benefit?" measuring Relative Morality.', 112)
            + textwrap.wrap("Benefit is a vector where each unit is 'Scope of Potential'[Group direction, magnitude] cross spectrum of will [active activity to active passivity, magnitude]", 112)
            + textwrap.wrap("The Greater Cross points the way to Good and Joy, its smaller paths lead nowhere. The smaller cross points to the consequences of your choices and actions, the smaller paths what you could but didn't do.", 112)
            + textwrap.wrap("Your responsibility is whether you'll choose to align with or against Good", 112)
        )
        fig.text(0.50, 0.082, '\n'.join(description_lines),
                 ha='center', va='center', color='#999999', fontsize=8.8, linespacing=1.3)

        fig.text(0.5, 0.012, 'Psochic Hegemony Graph: The map of Good and Evil', ha='center', va='bottom',
                 color='#444444', fontsize=9, fontstyle='italic')

        plt.savefig(filename, facecolor=fig.get_facecolor(), dpi=300, bbox_inches='tight')
    finally:
        plt.close(fig)


# ==============================================================================
# 3. DEEP-DIVE ANALYSIS CARD GENERATOR (FOR POSTS 5+)
# ==============================================================================

def get_font(name, size):
    paths = [name, os.path.join("C:\\Windows\\Fonts", name), os.path.join("C:\\Windows\\Fonts", name.lower())]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    lines = []
    paragraphs = text.split("\n")
    for para in paragraphs:
        if not para.strip():
            lines.append("")
            continue
        words = para.split(" ")
        curr = ""
        for w in words:
            test = (curr + " " + w).strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                curr = test
            else:
                if curr:
                    lines.append(curr)
                curr = w
        if curr:
            lines.append(curr)
    return lines

def draw_card(cfg, filename):
    """
    Renders the deep-dive analysis card for Bluesky thread Part 4:
    Context, Nuance, Plane Error Breakdown, Social Physics, and Personas.
    """
    width, height = 1200, 1600
    img = Image.new("RGB", (width, height), "#0b0f19")
    draw = ImageDraw.Draw(img)

    f_title = get_font("segoeui.ttf", 24)
    f_body = get_font("segoeui.ttf", 16)
    f_bold = get_font("segoeuib.ttf", 18)
    f_mono = get_font("consola.ttf", 14)

    # Frame
    draw.rounded_rectangle([20, 20, width - 20, height - 20], radius=12, outline="#1e293b", width=2)
    draw.rounded_rectangle([20, 20, width - 20, 28], radius=4, fill="#38bdf8")

    # Header
    draw.text((45, 45), "ALETHEIA DEEP-DIVE AUDIT CARD", fill="#38bdf8", font=f_bold)
    sid = str(cfg.get("id", "AUDIT")).upper()
    draw.text((width - 450, 45), f"RECORD #{sid[:24]}", fill="#94a3b8", font=f_mono)

    # Subject
    subj = cfg.get("subject") or cfg.get("title") or "Audited Subject"
    draw.rounded_rectangle([45, 85, width - 45, 175], radius=8, fill="#111827", outline="#1e293b", width=1)
    s_lines = wrap_text(subj, f_bold, width - 120, draw)
    sy = 100
    for l in s_lines[:2]:
        draw.text((65, sy), l, fill="#f8fafc", font=f_bold)
        sy += 26

    # Sections from card_sections or posts
    sections = cfg.get("card_sections") or cfg.get("sections") or {}
    context_text = sections.get("context") or sections.get("Context") or ""
    nuance_text = sections.get("nuance") or sections.get("Nuance") or sections.get("Empirical Evidence") or ""
    breakdown_text = sections.get("breakdown") or sections.get("Breakdown") or sections.get("Plane Analysis") or ""
    social_text = sections.get("social_physics") or sections.get("Social Physics") or ""
    personas = sections.get("personas") or cfg.get("personas") or {}

    # If sections not structured, extract from 15-post thread sequence
    posts = cfg.get("posts", [])
    if not context_text and len(posts) > 5:
        context_text = posts[5]
    if not nuance_text and len(posts) > 6:
        nuance_text = posts[6]
    if not breakdown_text and len(posts) > 7:
        breakdown_text = posts[7]
    if not social_text and len(posts) > 8:
        social_text = posts[8]

    cur_y = 195
    def render_block(title, text, color="#f8fafc", bg="#111827"):
        nonlocal cur_y
        if not text:
            return
        lines = wrap_text(text, f_body, width - 130, draw)[:5]
        block_h = 45 + len(lines) * 22
        draw.rounded_rectangle([45, cur_y, width - 45, cur_y + block_h], radius=8, fill=bg, outline="#1e293b", width=1)
        draw.text((65, cur_y + 12), title, fill="#38bdf8", font=f_bold)
        ty = cur_y + 36
        for l in lines:
            draw.text((65, ty), l, fill=color, font=f_body)
            ty += 22
        cur_y += block_h + 15

    render_block("1. EVENT CONTEXT & PHYSICAL IMPACT", context_text)
    render_block("2. NUANCE (THE BRIGHT SIDE / POISON)", nuance_text)
    render_block("3. FORENSIC BREAKDOWN & PLANE ERROR", breakdown_text)
    render_block("4. SOCIAL PHYSICS ANALYSIS", social_text)

    # Personas Panel
    if personas or any("Alethekanon:" in p for p in posts):
        draw.rounded_rectangle([45, cur_y, width - 45, height - 50], radius=8, fill="#0f172a", outline="#1e293b", width=1)
        draw.text((65, cur_y + 12), "5. TRINARY & PERSONA PERSPECTIVES", fill="#fbbf24", font=f_bold)
        py = cur_y + 40

        p_items = list(personas.items()) if personas else []
        if not p_items:
            for p in posts[11:]:
                if ":" in p:
                    name, text = p.split(":", 1)
                    p_items.append((name.strip(), text.strip()))

        for name, p_text in p_items[:4]:
            draw.text((65, py), f"• {name}:", fill="#38bdf8", font=f_bold)
            p_lines = wrap_text(p_text, f_body, width - 150, draw)[:3]
            py += 22
            for pl in p_lines:
                draw.text((80, py), pl, fill="#cbd5e1", font=f_body)
                py += 20
            py += 8

    img.save(filename, format="PNG", optimize=True)
