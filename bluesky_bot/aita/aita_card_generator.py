import os
import sys
import json
from PIL import Image, ImageDraw

# Allow importing shared font/QR helpers from parent bluesky_bot directory
_PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)

from image_card_generator import load_theme_fonts, wrap_text, _generate_qr_code
from aita_graph_generator import generate_aita_graph

CANVAS_BG = "#0B0F19"
CARD_BG = "#141D2F"
BORDER_COLOR = "#25354F"
TEXT_COLOR = "#E2E8F0"
MUTED_TEXT = "#94A3B8"

VERDICT_COLORS = {
    "NTA": "#10B981",
    "YWNBTA": "#10B981",
    "YTA": "#EF4444",
    "YWBTA": "#EF4444",
    "ESH": "#F59E0B",
    "NAH": "#38BDF8",
    "INFO": "#A855F7",
}


def _draw_section_card(draw, x_left, x_right, y, height, title, accent_color, lines, fonts, line_h=30, body_font_key="regular_22"):
    draw.rounded_rectangle([x_left, y, x_right, y + height], radius=12, fill=CARD_BG, outline=BORDER_COLOR, width=2)
    draw.rectangle([x_left, y + 12, x_left + 5, y + height - 12], fill=accent_color)
    draw.text((x_left + 22, y + 18), title, fill=accent_color, font=fonts["bold_20"])
    cur_y = y + 52
    for line in lines:
        if line == "":
            cur_y += line_h // 2
            continue
        draw.text((x_left + 22, cur_y), line, fill=TEXT_COLOR, font=fonts[body_font_key])
        cur_y += line_h


def _measure_card(title, text, max_w, fonts, temp_draw, line_h=30, body_font_key="regular_22"):
    lines = wrap_text(text, fonts[body_font_key], max_w - 44, temp_draw)
    body_h = 0
    for line in lines:
        body_h += (line_h // 2) if line == "" else line_h
    card_h = 52 + body_h + 22
    return {"title": title, "lines": lines, "h": card_h}


def _draw_header(draw, canvas_w, x_left, x_right, title, subtitle, verdict, metrics_text, fonts, temp_draw):
    verdict_color = VERDICT_COLORS.get(verdict.upper(), "#38BDF8")
    drawable_w = x_right - x_left
    title_max_w = drawable_w - 170

    title_lines = wrap_text(title, fonts["bold_32"], title_max_w, temp_draw)
    sub_lines = wrap_text(subtitle, fonts["bold_20"], drawable_w, temp_draw)
    metric_lines = wrap_text(metrics_text, fonts["mono_16"], drawable_w - 28, temp_draw)

    y = 40
    # Verdict badge on top-right
    badge_w = 145
    badge_h = 54
    badge_x = x_right - badge_w
    draw.rounded_rectangle([badge_x, y, x_right, y + badge_h], radius=10, fill=verdict_color)
    bbox = draw.textbbox((0, 0), verdict, font=fonts["bold_28"])
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((badge_x + (badge_w - tw) // 2, y + (badge_h - th) // 2 - 4), verdict, fill="#0B0F19", font=fonts["bold_28"])

    cur_y = y
    for line in title_lines:
        draw.text((x_left, cur_y), line, fill="#F8FAFC", font=fonts["bold_32"])
        cur_y += 40
    cur_y = max(cur_y, y + badge_h + 6)
    for line in sub_lines:
        draw.text((x_left, cur_y), line, fill="#38BDF8", font=fonts["bold_20"])
        cur_y += 28

    cur_y += 8
    strip_h = 16 + len(metric_lines) * 22 + 8
    draw.rounded_rectangle([x_left, cur_y, x_right, cur_y + strip_h], radius=8, fill="#111827", outline=BORDER_COLOR, width=1)
    my = cur_y + 10
    for mline in metric_lines:
        draw.text((x_left + 14, my), mline, fill="#CBD5E1", font=fonts["mono_16"])
        my += 22
    return cur_y + strip_h + 24


def generate_aita_story_card(case_data, output_path):
    """Generates the Story & Verdict Info Card for an evaluated AITA case."""
    fonts = load_theme_fonts()
    canvas_w = 1200
    x_left = 40
    x_right = canvas_w - 40
    drawable_w = x_right - x_left
    col_gap = 26
    col_w = (drawable_w - col_gap) // 2
    col1_x = x_left
    col2_x = x_left + col_w + col_gap

    ev = case_data.get("evaluation") or case_data.get("vft_appendix") or {}
    coords = ev.get("coordinates", {})
    res = ev.get("resolution", {})
    verdict = case_data.get("verdict") or ev.get("verdict", "INFO")
    verdict_label = ev.get("verdict_label", "")
    title = case_data.get("title") or case_data.get("subject") or "AITA Assessment"
    subreddit = case_data.get("subreddit", "AmItheAsshole")
    author = case_data.get("author", "anonymous")
    mode = "Hypothetical (WIBTA)" if (case_data.get("is_hypothetical") or "wibta" in title.lower()) else "Past / Completed (AITA)"
    subtitle = f"r/{subreddit}  •  {mode}  •  u/{author}"

    op_s = coords.get("op_stated", [case_data.get("claim_u", 0.0), case_data.get("claim_psi", 0.0)])
    op_a = coords.get("op_actual", [case_data.get("real_u", 0.0), case_data.get("real_psi", 0.0)])
    oth_a = coords.get("other_actual", [0.0, 0.0])
    wisdom_val = coords.get("wisdom_score", coords.get("C_act", 0.0))
    metrics_text = (
        f"OP Stated: ({op_s[0]:+.2f}, {op_s[1]:+.2f})  |  "
        f"OP Actual: ({op_a[0]:+.2f}, {op_a[1]:+.2f})  |  "
        f"Other: ({oth_a[0]:+.2f}, {oth_a[1]:+.2f})  |  "
        f"ΔH: {coords.get('delta_H', 0):.2f}  |  "
        f"Integrity: {round(float(wisdom_val) * 100)}%  |  "
        f"R_net: {coords.get('R_net', 1):.2f}"
    )

    temp_img = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)

    # Compute header height by dry-running layout metrics
    title_lines = wrap_text(title, fonts["bold_32"], drawable_w - 170, temp_draw)
    sub_lines = wrap_text(subtitle, fonts["bold_20"], drawable_w, temp_draw)
    metric_lines = wrap_text(metrics_text, fonts["mono_16"], drawable_w - 28, temp_draw)
    header_end_y = max(40 + len(title_lines) * 40, 40 + 54 + 6) + len(sub_lines) * 28 + 8 + (16 + len(metric_lines) * 22 + 8) + 24

    # Prepare cards (full-width Story -> 2-col Verdict & Resolution -> full-width Actors)
    story_text = (case_data.get("selftext") or "").strip().replace("\\*", "*").replace("\\_", "_")
    if not story_text:
        posts_arr = case_data.get("posts") or []
        story_text = posts_arr[1] if len(posts_arr) > 1 else title
    actors_lines = [
        f"• OP Stated: ({op_s[0]:+.2f}, {op_s[1]:+.2f})   |   OP Actual: ({op_a[0]:+.2f}, {op_a[1]:+.2f})   |   Counterparty Actual: ({oth_a[0]:+.2f}, {oth_a[1]:+.2f})",
    ]
    for tp in coords.get("third_parties", []):
        actors_lines.append(f"• {tp.get('actor', 'Third Party')} ({tp.get('upsilon', 0):+.2f}, {tp.get('psi', 0):+.2f}): {tp.get('role', '')}")
    for a in ev.get("actor_aspects", []):
        actors_lines.append(f"• {a.get('actor', 'Actor')} [{a.get('role', '')}] ({float(a.get('son_u', 0)):+.2f}, {float(a.get('son_psi', 0)):+.2f}) — {a.get('aspect_verdict', '')}")
    actors_text = "\n".join(actors_lines)

    why_body = (ev.get("why_verdict") or "").strip()
    if not why_body:
        posts_arr = case_data.get("posts") or []
        why_body = posts_arr[4] if len(posts_arr) > 4 else ""
    why_text = f"{verdict} — {verdict_label}\n\n{why_body}".strip() if verdict_label else f"{verdict}\n\n{why_body}".strip()

    trap_txt = res.get("trap_to_step_out_of") or res.get("trap_to_exit") or ""
    script_txt = res.get("verbatim_script") or res.get("script") or ""
    patch_txt = res.get("structural_patch") or res.get("serenity_boundary") or ""
    flip_txt = res.get("counterfactual_flip_thresholds") or res.get("counterfactual_flip") or ""
    res_parts = []
    if trap_txt:
        res_parts.append(f"Trap to Step Out Of:\n{trap_txt}")
    if script_txt:
        res_parts.append(f"Verbatim Script:\n\"{script_txt}\"")
    if patch_txt:
        res_parts.append(f"Boundary / Patch:\n{patch_txt}")
    if flip_txt:
        res_parts.append(f"Counterfactual Flip:\n{flip_txt}")
    res_text = "\n\n".join(res_parts) if res_parts else "See thread Resolution post."

    c_story = _measure_card("THE STORY (OP'S ACCOUNT)", story_text, drawable_w, fonts, temp_draw, line_h=28, body_font_key="regular_20")
    c_why = _measure_card("VERDICT & PLAIN-ENGLISH WHY", why_text, col_w, fonts, temp_draw, line_h=28, body_font_key="regular_20")
    c_res = _measure_card("RESOLUTION & VERBATIM SCRIPT", res_text, col_w, fonts, temp_draw, line_h=28, body_font_key="regular_20")
    c_actors = _measure_card("ACTORS & MORAL COORDINATES", actors_text, drawable_w, fonts, temp_draw, line_h=28, body_font_key="regular_20")

    card_gap = 22
    mid_h = max(c_why["h"], c_res["h"])
    footer_h = 130
    total_h = header_end_y + c_story["h"] + card_gap + mid_h + card_gap + c_actors["h"] + footer_h

    img = Image.new("RGB", (canvas_w, total_h), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    y_cur = _draw_header(draw, canvas_w, x_left, x_right, title, subtitle, verdict, metrics_text, fonts, temp_draw)

    _draw_section_card(draw, x_left, x_right, y_cur, c_story["h"], c_story["title"], "#38BDF8", c_story["lines"], fonts, line_h=28, body_font_key="regular_20")
    y_cur += c_story["h"] + card_gap

    verdict_accent = VERDICT_COLORS.get(verdict.upper(), "#10B981")
    _draw_section_card(draw, col1_x, col1_x + col_w, y_cur, mid_h, c_why["title"], verdict_accent, c_why["lines"], fonts, line_h=28, body_font_key="regular_20")
    _draw_section_card(draw, col2_x, col2_x + col_w, y_cur, mid_h, c_res["title"], "#10B981", c_res["lines"], fonts, line_h=28, body_font_key="regular_20")
    y_cur += mid_h + card_gap

    _draw_section_card(draw, x_left, x_right, y_cur, c_actors["h"], c_actors["title"], "#A855F7", c_actors["lines"], fonts, line_h=28, body_font_key="regular_20")
    y_cur += c_actors["h"]

    footer_y = y_cur + 24
    draw.text((x_left, footer_y + 10), "Aletheia AITA Engine | Story & Verdict Card", fill="#64748B", font=fonts["bold_22"])
    draw.text((x_left, footer_y + 44), f"Case ID: {case_data.get('id', 'unknown')}", fill="#475569", font=fonts["regular_18"])

    url = case_data.get("url", "")
    if isinstance(url, str) and url.strip():
        qr_img = _generate_qr_code(url.strip(), size=92)
        if qr_img:
            qr_x = x_right - 92
            qr_y = footer_y
            draw.rounded_rectangle([qr_x - 4, qr_y - 4, qr_x + 96, qr_y + 96], radius=6, fill=CARD_BG, outline=BORDER_COLOR, width=1)
            img.paste(qr_img, (qr_x, qr_y))

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"AITA Story Card generated: {output_path}")


def generate_aita_appendix_card(case_data, output_path):
    """Generates the Appendix & VFT Audit Context Card containing all 7-plane, deception, UCF, trap, and Oberon details."""
    fonts = load_theme_fonts()
    canvas_w = 1200
    x_left = 40
    x_right = canvas_w - 40
    drawable_w = x_right - x_left
    col_gap = 26
    col_w = (drawable_w - col_gap) // 2
    col1_x = x_left
    col2_x = x_left + col_w + col_gap

    ev = case_data.get("evaluation") or case_data.get("vft_appendix") or {}
    coords = ev.get("coordinates", {})
    ucf = coords.get("ucf_tuning", {})
    trace = ev.get("vft_audit_trace", {})
    verdict = case_data.get("verdict") or ev.get("verdict", "INFO")
    raw_title = case_data.get("title") or case_data.get("subject") or "AITA Case"
    title = f"APPENDIX & AUDIT CONTEXT — {raw_title}"
    subtitle = f"r/{case_data.get('subreddit', 'AmItheAsshole')}  •  Full VFT Protocol Trace"

    if ucf:
        ucf_text = (
            f"UCF v6.11: LHS={ucf.get('LHS', 0)}  |  RHS_Stated={ucf.get('RHS_Stated', 0)}  |  "
            f"RHS_Obs={ucf.get('RHS_Observed', 0)}  |  Tuned={ucf.get('Tuned_Score', 0)}  |  "
            f"State: {ucf.get('state', 'N/A')}"
        )
    else:
        wisdom_val = coords.get("wisdom_score", coords.get("C_act", 0.0))
        ucf_text = (
            f"Say-Do Gap ΔH: {coords.get('delta_H', 0):.2f}  |  "
            f"Integrity: {round(float(wisdom_val) * 100)}%  |  "
            f"R_net: {coords.get('R_net', 1):.2f}  |  "
            f"OP Anchor: {coords.get('op_eca_anchor', 'N/A')}  |  "
            f"Other Anchor: {coords.get('other_eca_anchor', 'N/A')}"
        )

    temp_img = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)

    title_lines = wrap_text(title, fonts["bold_32"], drawable_w - 170, temp_draw)
    sub_lines = wrap_text(subtitle, fonts["bold_20"], drawable_w, temp_draw)
    metric_lines = wrap_text(ucf_text, fonts["mono_16"], drawable_w - 28, temp_draw)
    header_end_y = max(40 + len(title_lines) * 40, 40 + 54 + 6) + len(sub_lines) * 28 + 8 + (16 + len(metric_lines) * 22 + 8) + 24

    unsaid_text = (trace.get("unsaid_horizon_and_multi_actor_graph") or trace.get("unsaid_horizon") or "").strip()
    silent_text = (trace.get("silent_judgment") or "").strip()

    seven = trace.get("seven_plane_scan")
    if isinstance(seven, dict) and seven:
        seven_lines = [f"{k.replace('_', ' ')}: {seven[k]}" for k in ["Q1_Who", "Q2_What", "Q3_Where", "Q4_Why", "Q5_How", "Q6_Cause", "Q7_Effect"] if k in seven]
        seven_text = "\n\n".join(seven_lines)
    else:
        seven_text = (trace.get("seven_planes") or "").strip()
    if ev.get("reasoning_summary"):
        seven_text = f"{seven_text}\n\nReasoning:\n{ev['reasoning_summary']}".strip()

    dec_codes = coords.get("deception_codes", [])
    _planes = {"1": "Who", "2": "Why", "3": "Cause", "4": "What", "5": "Where", "6": "How", "7": "Effect"}
    _senses = {"1": "Sight", "2": "Hearing", "3": "Touch", "4": "Smell", "5": "Taste", "6": "Balance", "7": "Proprioception"}
    _uses = {"1": "Survival/Threat", "2": "Domination", "3": "Expression", "4": "Transcendence", "5": "Acquisition/Debt", "6": "Gaslight", "7": "Symbiosis/Hive"}
    fmt_codes = []
    for c in dec_codes:
        cs = str(c).strip()
        if cs.startswith("[") and "]" in cs:
            bracket_end = cs.index("]")
            code_part = cs[1:bracket_end]
            rest = cs[bracket_end + 1:].strip()
            parts = code_part.split(".")
            if len(parts) == 4 and all(p in _planes for p in parts):
                decoded = f"{_planes[parts[0]]}.{_senses[parts[1]]}.{_uses[parts[2]]}.{_uses[parts[3]]}"
                if not rest:
                    cs = f"[{code_part}] {decoded}"
                elif "Plane.Sense.Use.Impulse" in rest:
                    cs = f"[{code_part}] {rest.replace('Plane.Sense.Use.Impulse', decoded)}"
        fmt_codes.append(f"• {cs}")
    dec_text = "\n".join(fmt_codes) if fmt_codes else "None detected."

    if trace.get("traps_and_belief_state"):
        traps_belief_text = trace["traps_and_belief_state"].strip()
    else:
        t_part = (trace.get("zero_point_five_zone_traps") or "").strip()
        b_part = (trace.get("nine_states_of_belief") or "").strip()
        traps_belief_text = "\n\n".join([x for x in [f"0.5-Zone Traps:\n{t_part}" if t_part else "", f"9 States of Belief:\n{b_part}" if b_part else ""] if x])

    oberon_part = (trace.get("oberon_and_sins_virtues") or "").strip()
    fallacy_part = (trace.get("cognitive_fallacy_check") or "").strip()
    oberon_fallacy_text = "\n\n".join([x for x in [f"Oberon Laws & 7 Sins/Virtues:\n{oberon_part}" if oberon_part else "", f"Cognitive Fallacy Check:\n{fallacy_part}" if fallacy_part else ""] if x])
    if not oberon_fallacy_text:
        persp_lines = []
        for k, label in [("alethekanon", "Alethekanon"), ("awwthekanon", "Awwthekanon"), ("brothekanon", "Brothekanon")]:
            if ev.get(k):
                persp_lines.append(f"{label}: {ev[k]}")
        oberon_fallacy_text = "\n\n".join(persp_lines)

    c_unsaid = _measure_card("UNSAID HORIZON", unsaid_text, drawable_w, fonts, temp_draw, line_h=28, body_font_key="regular_20") if unsaid_text else None
    c_silent = _measure_card("SILENT JUDGMENT (MUTE / DEAF OBSERVER)", silent_text, drawable_w, fonts, temp_draw, line_h=28, body_font_key="regular_20") if silent_text else None
    c_seven = _measure_card("7-PLANE SCAN (Q1 WHO – Q7 EFFECT)", seven_text or "See Story Card.", col_w, fonts, temp_draw, line_h=26, body_font_key="regular_18")
    c_dec = _measure_card("DECEPTION MATRIX CODES [P.S.U.I]", dec_text, col_w, fonts, temp_draw, line_h=26, body_font_key="regular_18")
    c_traps = _measure_card("0.5-ZONE TRAPS & 9 STATES OF BELIEF", traps_belief_text, col_w, fonts, temp_draw, line_h=26, body_font_key="regular_18") if traps_belief_text else None
    c_oberon = _measure_card("PERSPECTIVES & AUDIT NOTES" if not oberon_part else "OBERON LAWS, SINS/VIRTUES & FALLACY CHECK", oberon_fallacy_text, drawable_w, fonts, temp_draw, line_h=28, body_font_key="regular_20") if oberon_fallacy_text else None

    gap = 20
    mid_right_h = c_dec["h"] + ((gap + c_traps["h"]) if c_traps else 0)
    mid_h = max(c_seven["h"], mid_right_h)
    footer_h = 130
    total_h = header_end_y + ((c_unsaid["h"] + gap) if c_unsaid else 0) + ((c_silent["h"] + gap) if c_silent else 0) + mid_h + gap + ((c_oberon["h"] + gap) if c_oberon else 0) + footer_h

    img = Image.new("RGB", (canvas_w, total_h), CANVAS_BG)
    draw = ImageDraw.Draw(img)

    cur_y = _draw_header(draw, canvas_w, x_left, x_right, title, subtitle, verdict, ucf_text, fonts, temp_draw)

    if c_unsaid:
        _draw_section_card(draw, x_left, x_right, cur_y, c_unsaid["h"], c_unsaid["title"], "#F59E0B", c_unsaid["lines"], fonts, line_h=28, body_font_key="regular_20")
        cur_y += c_unsaid["h"] + gap

    if c_silent:
        _draw_section_card(draw, x_left, x_right, cur_y, c_silent["h"], c_silent["title"], "#38BDF8", c_silent["lines"], fonts, line_h=28, body_font_key="regular_20")
        cur_y += c_silent["h"] + gap

    _draw_section_card(draw, col1_x, col1_x + col_w, cur_y, c_seven["h"], c_seven["title"], "#10B981", c_seven["lines"], fonts, line_h=26, body_font_key="regular_18")
    _draw_section_card(draw, col2_x, col2_x + col_w, cur_y, c_dec["h"], c_dec["title"], "#EF4444", c_dec["lines"], fonts, line_h=26, body_font_key="regular_18")
    if c_traps:
        _draw_section_card(draw, col2_x, col2_x + col_w, cur_y + c_dec["h"] + gap, c_traps["h"], c_traps["title"], "#A855F7", c_traps["lines"], fonts, line_h=26, body_font_key="regular_18")
    cur_y += mid_h + gap

    if c_oberon:
        _draw_section_card(draw, x_left, x_right, cur_y, c_oberon["h"], c_oberon["title"], "#38BDF8", c_oberon["lines"], fonts, line_h=28, body_font_key="regular_20")
        cur_y += c_oberon["h"] + 24

    draw.text((x_left, cur_y + 10), "Aletheia AITA Engine | Appendix & 7-Plane Audit Context", fill="#64748B", font=fonts["bold_22"])
    draw.text((x_left, cur_y + 44), "Scan QR code for the original Reddit post", fill="#475569", font=fonts["regular_18"])

    url = case_data.get("url", "")
    if isinstance(url, str) and url.strip():
        qr_img = _generate_qr_code(url.strip(), size=92)
        if qr_img:
            qr_x = x_right - 92
            qr_y = cur_y
            draw.rounded_rectangle([qr_x - 4, qr_y - 4, qr_x + 96, qr_y + 96], radius=6, fill=CARD_BG, outline=BORDER_COLOR, width=1)
            img.paste(qr_img, (qr_x, qr_y))

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"AITA Appendix Card generated: {output_path}")


def generate_all_aita_assets(case_json_path, output_dir=None):
    """Generates Story Card, Appendix Card, and Multi-Actor Psochic Hegemony Graph for an AITA JSON."""
    with open(case_json_path, "r", encoding="utf-8") as f:
        case_data = json.load(f)
    base_name = os.path.splitext(os.path.basename(case_json_path))[0]
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(case_json_path)), "cards")
    os.makedirs(output_dir, exist_ok=True)

    story_png = os.path.join(output_dir, f"{base_name}_story_card.png")
    appendix_png = os.path.join(output_dir, f"{base_name}_appendix_card.png")
    graph_png = os.path.join(output_dir, f"{base_name}_graph.png")

    generate_aita_story_card(case_data, story_png)
    generate_aita_appendix_card(case_data, appendix_png)
    generate_aita_graph(case_data, graph_png)
    return story_png, appendix_png, graph_png


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python aita_card_generator.py <case_json_path> [output_dir]")
        sys.exit(1)
    json_path = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None
    generate_all_aita_assets(json_path, out_dir)
