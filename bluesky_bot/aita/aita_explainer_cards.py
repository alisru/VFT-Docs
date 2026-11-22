import os
import sys
from PIL import Image, ImageDraw

_PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)

from image_card_generator import load_theme_fonts, wrap_text

CANVAS_BG = "#0B0F19"
CARD_BG = "#141D2F"
BORDER_COLOR = "#25354F"
TEXT_COLOR = "#E2E8F0"


def _draw_card(draw, x_left, x_right, y, height, title, accent, lines, fonts, line_h=28, body_font_key="regular_20"):
    draw.rounded_rectangle([x_left, y, x_right, y + height], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.rectangle([x_left, y + 12, x_left + 5, y + height - 12], fill=accent)
    draw.text((x_left + 22, y + 18), title, fill=accent, font=fonts["bold_20"])
    cy = y + 52
    for line in lines:
        if line == "":
            cy += line_h // 2
            continue
        draw.text((x_left + 22, cy), line, fill=TEXT_COLOR, font=fonts[body_font_key])
        cy += line_h


def _measure(title, text, max_w, fonts, temp_draw, line_h=28, body_font_key="regular_20"):
    lines = wrap_text(text, fonts[body_font_key], max_w - 44, temp_draw)
    body_h = sum((line_h // 2) if l == "" else line_h for l in lines)
    return {"title": title, "lines": lines, "h": 52 + body_h + 22}


def generate_7planes_explainer_card(output_path):
    """Generates a plain-English Bluesky reference card explaining the 7 Planes of Reality (Q1-Q7)."""
    fonts = load_theme_fonts()
    canvas_w = 1200
    x_left, x_right = 40, canvas_w - 40
    drawable_w = x_right - x_left
    col_gap = 24
    col_w = (drawable_w - col_gap) // 2
    col1_x, col2_x = x_left, x_left + col_w + col_gap

    temp_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    title = "FIELD GUIDE: WHAT ARE THE 7 PLANES (Q1–Q7)?"
    subtitle = "How Aletheia breaks down any dispute into 7 separate layers of reality instead of vibes"

    planes = [
        ("Q1 • WHO — METAPHYSICAL (Identity & Will)", "#38BDF8",
         "Checks who holds power, who is acting in good faith, and whether someone is putting their ego above shared reality.\nVirtue: Humility  |  Sin: Pride"),
        ("Q2 • WHAT — POSSIBLE (Alternatives & Proof)", "#10B981",
         "Checks what realistic options existed and whether claims actually hold up under a stress test.\nVirtue: Diligence  |  Sin: Sloth"),
        ("Q3 • WHERE — PHYSICAL (Body, Space & Cost)", "#F59E0B",
         "Checks who pays the real-world physical, financial, or sensory cost — and whether personal boundaries are respected.\nVirtue: Temperance  |  Sin: Gluttony"),
        ("Q4 • WHY — LYRICAL (Meaning, Framing & Motive)", "#A855F7",
         "Compares the story someone tells about why they acted against their actual motive. Spots spin, guilt-trips, and cover stories.\nVirtue: Kindness  |  Sin: Envy"),
        ("Q5 • HOW — LOGICAL (Rules & Consistency)", "#38BDF8",
         "Checks if the rule applies equally to both sides, or if a technicality is being weaponized to bully someone.\nVirtue: Patience  |  Sin: Wrath"),
        ("Q6 • CAUSE — HISTORICAL (Timeline & Precedent)", "#10B981",
         "Checks what prior agreements, patterns, or provocations led to this moment — and who is erasing history.\nVirtue: Charity  |  Sin: Greed"),
        ("Q7 • EFFECT — EMOTIVE (Impact & Consequence)", "#EF4444",
         "Checks whether people are treated as whole human beings or used as props/objects to regulate someone else's ego.\nVirtue: Chastity  |  Sin: Lust"),
    ]

    intro_text = (
        "Most internet arguments get stuck on one loud detail. The 7-Plane Scan forces every case through 7 independent lenses "
        "(Who, What, Where, Why, How, Cause, Effect) so neither a smooth talker nor a bad excuse can hide."
    )
    c_intro = _measure("WHY 7 PLANES?", intro_text, drawable_w, fonts, temp_draw, line_h=28, body_font_key="regular_20")

    measured = [_measure(t, b, col_w if i < 6 else drawable_w, fonts, temp_draw, line_h=26, body_font_key="regular_18") for i, (t, _c, b) in enumerate(planes)]

    row_gap = 18
    row1_h = max(measured[0]["h"], measured[1]["h"])
    row2_h = max(measured[2]["h"], measured[3]["h"])
    row3_h = max(measured[4]["h"], measured[5]["h"])
    row4_h = measured[6]["h"]

    header_h = 135
    footer_h = 75
    total_h = header_h + c_intro["h"] + row_gap + row1_h + row_gap + row2_h + row_gap + row3_h + row_gap + row4_h + footer_h

    img = Image.new("RGB", (canvas_w, total_h), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    draw.text((x_left, 38), title, fill="#F8FAFC", font=fonts["bold_32"])
    draw.text((x_left, 82), subtitle, fill="#38BDF8", font=fonts["bold_20"])

    cy = header_h
    _draw_card(draw, x_left, x_right, cy, c_intro["h"], c_intro["title"], "#FACC15", c_intro["lines"], fonts, line_h=28, body_font_key="regular_20")
    cy += c_intro["h"] + row_gap

    for r_idx, rh in [(0, row1_h), (2, row2_h), (4, row3_h)]:
        _draw_card(draw, col1_x, col1_x + col_w, cy, measured[r_idx]["h"], measured[r_idx]["title"], planes[r_idx][1], measured[r_idx]["lines"], fonts, line_h=26, body_font_key="regular_18")
        _draw_card(draw, col2_x, col2_x + col_w, cy, measured[r_idx + 1]["h"], measured[r_idx + 1]["title"], planes[r_idx + 1][1], measured[r_idx + 1]["lines"], fonts, line_h=26, body_font_key="regular_18")
        cy += rh + row_gap

    _draw_card(draw, x_left, x_right, cy, row4_h, measured[6]["title"], planes[6][1], measured[6]["lines"], fonts, line_h=26, body_font_key="regular_18")
    cy += row4_h + 22

    draw.text((x_left, cy), "Aletheia Field Guide  •  7 Planes of Reality (1 Who → 7 Effect)", fill="#64748B", font=fonts["bold_20"])
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"7-Planes Explainer Card generated: {output_path}")


def generate_deception_and_metrics_explainer_card(output_path):
    """Generates a single, compact Bluesky reference card explaining the 7 Planes, Deception Matrix, 0.5-Zone Traps, Silent Judgment, and Graph Metrics."""
    fonts = load_theme_fonts()
    canvas_w = 1200
    x_left, x_right = 40, canvas_w - 40
    drawable_w = x_right - x_left
    col_gap = 24
    col_w = (drawable_w - col_gap) // 2
    col1_x, col2_x = x_left, x_left + col_w + col_gap

    temp_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    title = "FIELD GUIDE: 7 PLANES, DECEPTION MATRIX & TRAPS"
    subtitle = "Plain-English key for reading Aletheia AITA audits and graphs"

    planes_text = (
        "Every dispute is checked across 7 independent layers (1 Who → 7 Effect):\n"
        "• Q1 Who (Metaphysical): Agency, ego, Pride vs. Humility.\n"
        "• Q2 What (Possible): Realistic options & proof, Sloth vs. Diligence.\n"
        "• Q3 Where (Physical): Body, space, money & boundaries, Gluttony vs. Temperance.\n"
        "• Q4 Why (Lyrical): Stated story vs. real motive, Envy vs. Kindness.\n"
        "• Q5 How (Logical): Equal rules vs. weaponized technicalities, Wrath vs. Patience.\n"
        "• Q6 Cause (Historical): Prior agreements & patterns, Greed vs. Charity.\n"
        "• Q7 Effect (Emotive): People treated as humans vs. props, Lust vs. Chastity."
    )

    dec_text = (
        "Format: [Plane . Sense . Use . Impulse] — full 1–7 key:\n"
        "• Plane: 1 Who, 2 What, 3 Where, 4 Why, 5 How, 6 Cause, 7 Effect.\n"
        "• Sense: 1 Sight, 2 Hearing, 3 Touch, 4 Smell, 5 Taste, 6 Balance, 7 Proprioception.\n"
        "• Use / Impulse: 1 Survival/Threat, 2 Domination, 3 Expression, 4 Transcendence, 5 Acquisition/Debt, 6 Gaslight, 7 Symbiosis/Hive.\n"
        "Ex: [2.3.5.5] = Treating a paid cinema ticket as ownership over someone's time/body."
    )

    traps_text = (
        "Near the center (0.5 Zone), ego flips how actions feel:\n"
        "• Service Trap (+υ +ψ): Normal boundaries feel 'selfish' (gaslit OPs).\n"
        "• Peace Trap (+υ -ψ): Staying silent to 'keep the peace' while enabling harm.\n"
        "• Ambition Trap (-υ +ψ): Controlling others feels like 'winning' or 'being right'.\n"
        "• Protection Trap (-υ -ψ): Cruelty or payback feels like 'self-defense'."
    )

    silent_text = (
        "• Mute Observer: Watch with the sound off — ignore adjectives and sob stories; list ONLY physical actions taken.\n"
        "• Deaf Observer: Ignore polite wording and measure only what the words DID to the room (e.g. hanging up to punish, yelling, recruiting relatives).\n\n"
        "THE 9 STATES OF BELIEF (What you see vs. what the group pushes):\n"
        "• You see Truth: 1 Agonizing Choice (group calls it false) · 2 Consensus Truth (both agree) · 3 Revolutionary Truth (group is outraged).\n"
        "• You see a Lie: 4 Consensus Lie (both call it false) · 5 Gaslit / Cassandra / Grifter (group buys the lie) · 6 Contrarian Cynic (group is outraged).\n"
        "• You feel Insulted: 7 Reactionary (group dismisses it) · 8 Persecuted Martyr (group accepts it) · 9 Consensus Taboo (both outraged)."
    )

    metrics_text = (
        "• υ (Morality, -2..+2): Who benefits (+2 Everyone, +1 Others, 0 No One, -1 Me, -2 Only Me).\n"
        "• ψ (Will, -2..+2): Energy direction (+2 Building, 0 Neutral, -2 Destroying/Forcing).\n"
        "• ΔH & Wisdom: Distance between OP's story and reality; Wisdom = 1 / (1 + ΔH).\n"
        "• R_net & Strain σ: Context completeness (1.0 = full, <1 = omitted context) & emotional tension."
    )

    c_planes = _measure("THE 7 PLANES OF REALITY (Q1–Q7)", planes_text, drawable_w, fonts, temp_draw, line_h=26, body_font_key="regular_18")
    c_dec = _measure("DECEPTION MATRIX [PLANE.SENSE.USE.IMPULSE]", dec_text, col_w, fonts, temp_draw, line_h=26, body_font_key="regular_18")
    c_traps = _measure("THE 0.5-ZONE PERCEPTUAL TRAPS", traps_text, col_w, fonts, temp_draw, line_h=26, body_font_key="regular_18")
    c_silent = _measure("SILENT JUDGMENT & BELIEF STATES", silent_text, col_w, fonts, temp_draw, line_h=26, body_font_key="regular_18")
    c_metrics = _measure("READING THE GRAPH & METRICS", metrics_text, col_w, fonts, temp_draw, line_h=26, body_font_key="regular_18")

    gap = 20
    left_h = c_dec["h"] + gap + c_silent["h"]
    right_h = c_traps["h"] + gap + c_metrics["h"]
    grid_h = max(left_h, right_h)

    header_h = 128
    footer_h = 68
    total_h = header_h + c_planes["h"] + gap + grid_h + footer_h

    img = Image.new("RGB", (canvas_w, total_h), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    draw.text((x_left, 38), title, fill="#F8FAFC", font=fonts["bold_32"])
    draw.text((x_left, 82), subtitle, fill="#38BDF8", font=fonts["bold_20"])

    _draw_card(draw, x_left, x_right, header_h, c_planes["h"], c_planes["title"], "#A855F7", c_planes["lines"], fonts, line_h=26, body_font_key="regular_18")
    grid_y = header_h + c_planes["h"] + gap

    _draw_card(draw, col1_x, col1_x + col_w, grid_y, c_dec["h"], c_dec["title"], "#EF4444", c_dec["lines"], fonts, line_h=26, body_font_key="regular_18")
    _draw_card(draw, col1_x, col1_x + col_w, grid_y + c_dec["h"] + gap, c_silent["h"], c_silent["title"], "#38BDF8", c_silent["lines"], fonts, line_h=26, body_font_key="regular_18")

    _draw_card(draw, col2_x, col2_x + col_w, grid_y, c_traps["h"], c_traps["title"], "#F59E0B", c_traps["lines"], fonts, line_h=26, body_font_key="regular_18")
    _draw_card(draw, col2_x, col2_x + col_w, grid_y + c_traps["h"] + gap, c_metrics["h"], c_metrics["title"], "#10B981", c_metrics["lines"], fonts, line_h=26, body_font_key="regular_18")

    draw.text((x_left, grid_y + grid_h + 20), "Aletheia Field Guide  •  7 Planes, Deception Matrix, Traps & Metrics", fill="#64748B", font=fonts["bold_20"])
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Deception & Metrics Explainer Card generated: {output_path}")


if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "cards")
    generate_deception_and_metrics_explainer_card(os.path.join(out_dir, "vft_explainer_deception_traps_card.png"))
