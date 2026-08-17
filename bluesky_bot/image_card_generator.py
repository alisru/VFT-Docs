import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

def get_font(font_name, size):
    """Safely attempts to load a TrueType font, falling back to None if not found."""
    # Common Windows font paths
    paths_to_try = [
        font_name,
        os.path.join("C:\\Windows\\Fonts", font_name),
        os.path.join("C:\\Windows\\Fonts", font_name.lower()),
    ]
    for p in paths_to_try:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return None

def load_theme_fonts():
    """Loads consistent theme fonts for the visual card layout."""
    fonts = {}
    regular_names = ["segoeui.ttf", "arial.ttf"]
    bold_names = ["segoeuib.ttf", "arialbd.ttf"]
    mono_names = ["consola.ttf", "cour.ttf"]
    
    # Helper to check if font is valid FreeType font
    def is_valid_font(font):
        return font is not None and type(font).__name__ == "FreeTypeFont"

    # Regular fonts
    fonts["regular_20"] = None
    for n in regular_names:
        f = get_font(n, 20)
        if is_valid_font(f):
            fonts["regular_20"] = f
            break
    if fonts["regular_20"] is None:
        fonts["regular_20"] = ImageFont.load_default()
        
    fonts["regular_29"] = None
    for n in regular_names:
        f = get_font(n, 29)
        if is_valid_font(f):
            fonts["regular_29"] = f
            break
    if fonts["regular_29"] is None:
        fonts["regular_29"] = ImageFont.load_default()

    fonts["regular_26"] = None
    for n in regular_names:
        f = get_font(n, 26)
        if is_valid_font(f):
            fonts["regular_26"] = f
            break
    if fonts["regular_26"] is None:
        fonts["regular_26"] = ImageFont.load_default()

    fonts["regular_24"] = None
    for n in regular_names:
        f = get_font(n, 24)
        if is_valid_font(f):
            fonts["regular_24"] = f
            break
    if fonts["regular_24"] is None:
        fonts["regular_24"] = ImageFont.load_default()

    fonts["regular_22"] = None
    for n in regular_names:
        f = get_font(n, 22)
        if is_valid_font(f):
            fonts["regular_22"] = f
            break
    if fonts["regular_22"] is None:
        fonts["regular_22"] = ImageFont.load_default()

    # Bold fonts
    fonts["bold_39"] = None
    for n in bold_names:
        f = get_font(n, 39)
        if is_valid_font(f):
            fonts["bold_39"] = f
            break
    if fonts["bold_39"] is None:
        fonts["bold_39"] = ImageFont.load_default()

    fonts["bold_36"] = None
    for n in bold_names:
        f = get_font(n, 36)
        if is_valid_font(f):
            fonts["bold_36"] = f
            break
    if fonts["bold_36"] is None:
        fonts["bold_36"] = ImageFont.load_default()

    fonts["bold_32"] = None
    for n in bold_names:
        f = get_font(n, 32)
        if is_valid_font(f):
            fonts["bold_32"] = f
            break
    if fonts["bold_32"] is None:
        fonts["bold_32"] = ImageFont.load_default()

    fonts["bold_27"] = None
    for n in bold_names:
        f = get_font(n, 27)
        if is_valid_font(f):
            fonts["bold_27"] = f
            break
    if fonts["bold_27"] is None:
        fonts["bold_27"] = ImageFont.load_default()

    fonts["bold_24"] = None
    for n in bold_names:
        f = get_font(n, 24)
        if is_valid_font(f):
            fonts["bold_24"] = f
            break
    if fonts["bold_24"] is None:
        fonts["bold_24"] = ImageFont.load_default()

    fonts["bold_20"] = None
    for n in bold_names:
        f = get_font(n, 20)
        if is_valid_font(f):
            fonts["bold_20"] = f
            break
    if fonts["bold_20"] is None:
        fonts["bold_20"] = ImageFont.load_default()

    fonts["bold_16"] = None
    for n in bold_names:
        f = get_font(n, 16)
        if is_valid_font(f):
            fonts["bold_16"] = f
            break
    if fonts["bold_16"] is None:
        fonts["bold_16"] = ImageFont.load_default()

    # Monospace fonts
    fonts["mono_20"] = None
    for n in mono_names:
        f = get_font(n, 20)
        if is_valid_font(f):
            fonts["mono_20"] = f
            break
    if fonts["mono_20"] is None:
        fonts["mono_20"] = ImageFont.load_default()

    return fonts

def wrap_text(text, font, max_width, draw):
    """Wraps text helper to fit within max_width pixels using PIL textbox measuring."""
    lines = []
    paragraphs = text.split('\n')
    for p in paragraphs:
        if not p.strip():
            lines.append("")
            continue
        words = p.split(' ')
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            try:
                bbox = draw.textbbox((0, 0), test_line, font=font)
                w = bbox[2] - bbox[0]
            except Exception:
                # Safe char fallback if font is default and getbbox fails
                w = len(test_line) * 8
            if w <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
    return lines

def generate_compact_info_card(thread_config, output_path):
    """Renders posts of the thread config into a beautiful two-column dark-mode infographic card (including Claim, Reality, Verdict in single-post mode)."""
    subject = thread_config.get("subject", "Assessment Summary")
    posts = thread_config.get("posts", [])
    link = thread_config.get("link", "")
    
    if len(posts) < 13:
        raise ValueError(f"Cannot generate compact info card: posts array has length {len(posts)} (expected 13 or 14).")

    if thread_config.get("five_word") is True:
        # Load fonts, generate single 5-word terminal card
        fonts = load_theme_fonts()
        stated_u = thread_config.get("claim_u", 0.0)
        stated_psi = thread_config.get("claim_psi", 0.0)
        real_u = thread_config.get("real_u", 0.0)
        real_psi = thread_config.get("real_psi", 0.0)
        verdict_subtitle = f"Stated: ({stated_u:+.1f}, {stated_psi:+.1f}) | Actual: ({real_u:+.1f}, {real_psi:+.1f})"
        
        # Replace output_path extension to output f"{slug}_info_card_five_word.png"
        five_word_output_path = output_path.replace(".png", "_five_word.png")
        _generate_five_word_card(subject, verdict_subtitle, posts, fonts, link, five_word_output_path)
        return


    # Load standard layout configuration
    fonts = load_theme_fonts()
    
    is_multi_aspect = (len(posts) == 14)
    
    if is_multi_aspect:
        sections = [
            {
                "label": "THE HOOK",
                "text": posts[0].replace("Hook:\n", "").strip(),
                "color": "#F472B6" # Pink/Magenta
            },
            {
                "label": "THE CLAIM",
                "text": posts[1].replace("Claim:\n", "").replace("The Claim:\n", "").replace("Stated Judgement:\n", "").strip(),
                "color": "#94A3B8" # Slate
            },
            {
                "label": "THE REALITY",
                "text": posts[2].replace("Reality:\n", "").replace("The Reality:\n", "").replace("Resulting Judgement:\n", "").strip(),
                "color": "#38BDF8" # Sky Blue
            },
            {
                "label": "THE VERDICT",
                "text": posts[3].replace("Verdict:\n", "").replace("Stated Verdict:\n", "").strip(),
                "color": "#FBBF24" # Yellow/Amber
            },
            {
                "label": "SUB-AUDITS BREAKDOWN",
                "text": posts[4].replace("Sub-Audits Breakdown:\n", "").replace("Sub-Audits:\n", "").strip(),
                "color": "#A855F7"  # Deep Purple
            }
        ]

        sections.extend([
            {
                "label": "CONTEXT",
                "text": posts[5].replace("What's happening:\n", "").replace("Context:\n", "").strip(),
                "color": "#38BDF8" # Teal
            },
            {
                "label": "THE BRIGHT SIDE" if posts[6].lower().startswith("the bright side") else "THE POISON",
                "text": posts[6].replace("The Bright Side:\n", "").replace("The Poison:\n", "").strip(),
                "color": "#10B981" if posts[6].lower().startswith("the bright side") else "#EF4444" # Emerald Green or Rose Red
            },
            {
                "label": "BREAKDOWN & PLANE ERROR",
                "text": posts[7].replace("The Breakdown & Plane Error:\n", "").strip(),
                "color": "#C084FC" # Purple
            },
            {
                "label": "SOCIAL PHYSICS ANALYSIS",
                "text": posts[8].replace("Social Physics Analysis:\n", "").strip(),
                "color": "#60A5FA" # Light Blue
            },
            {
                "label": "TRAJECTORY & DESTINATION",
                "text": posts[9].replace("The Trajectory:", "").strip(),
                "color": "#F472B6" # Magenta
            },
            {
                "label": "THE UNAVOIDABLES",
                "text": posts[10].replace("The Unavoidable Truth:", "Truth:").replace("The Unavoidable Lie:", "Lie:").strip(),
                "color": "#F59E0B" # Amber/Orange
            }
        ])
        
        personas = [
            {
                "label": "ALETHEKANON",
                "text": posts[11].replace("Alethekanon:\n", "").strip(),
                "color": "#38BDF8" # Sky Blue
            },
            {
                "label": "AWWTHEKANON",
                "text": posts[12].replace("Awwthekanon:\n", "").strip(),
                "color": "#10B981" # Emerald Green
            },
            {
                "label": "BROTHEKANON",
                "text": posts[13].replace("Brothekanon:\n", "").strip(),
                "color": "#F59E0B" # Amber
            }
        ]
    else:
        sections = [
            {
                "label": "THE HOOK",
                "text": posts[0].replace("Hook:\n", "").strip(),
                "color": "#F472B6" # Pink/Magenta
            },
            {
                "label": "THE CLAIM",
                "text": posts[1].replace("Claim:\n", "").replace("The Claim:\n", "").replace("Stated Judgement:\n", "").strip(),
                "color": "#94A3B8" # Slate
            },
            {
                "label": "THE REALITY",
                "text": posts[2].replace("Reality:\n", "").replace("The Reality:\n", "").replace("Resulting Judgement:\n", "").strip(),
                "color": "#38BDF8" # Sky Blue
            },
            {
                "label": "THE VERDICT",
                "text": posts[3].replace("Verdict:\n", "").replace("Stated Verdict:\n", "").strip(),
                "color": "#FBBF24" # Yellow/Amber
            }
        ]

        sections.extend([
            {
                "label": "CONTEXT",
                "text": posts[4].replace("What's happening:\n", "").replace("Context:\n", "").strip(),
                "color": "#38BDF8" # Teal
            },
            {
                "label": "THE BRIGHT SIDE" if posts[5].lower().startswith("the bright side") else "THE POISON",
                "text": posts[5].replace("The Bright Side:\n", "").replace("The Poison:\n", "").strip(),
                "color": "#10B981" if posts[5].lower().startswith("the bright side") else "#EF4444" # Emerald Green or Rose Red
            },
            {
                "label": "BREAKDOWN & PLANE ERROR",
                "text": posts[6].replace("The Breakdown & Plane Error:\n", "").strip(),
                "color": "#C084FC" # Purple
            },
            {
                "label": "SOCIAL PHYSICS ANALYSIS",
                "text": posts[7].replace("Social Physics Analysis:\n", "").strip(),
                "color": "#60A5FA" # Light Blue
            },
            {
                "label": "TRAJECTORY & DESTINATION",
                "text": posts[8].replace("The Trajectory:", "").strip(),
                "color": "#F472B6" # Magenta
            },
            {
                "label": "THE UNAVOIDABLES",
                "text": posts[9].replace("The Unavoidable Truth:", "Truth:").replace("The Unavoidable Lie:", "Lie:").strip(),
                "color": "#F59E0B" # Amber/Orange
            }
        ])
        
        personas = [
            {
                "label": "ALETHEKANON",
                "text": posts[10].replace("Alethekanon:\n", "").strip(),
                "color": "#38BDF8" # Sky Blue
            },
            {
                "label": "AWWTHEKANON",
                "text": posts[11].replace("Awwthekanon:\n", "").strip(),
                "color": "#10B981" # Emerald Green
            },
            {
                "label": "BROTHEKANON",
                "text": posts[12].replace("Brothekanon:\n", "").strip(),
                "color": "#F59E0B" # Amber
            }
        ]


    # Generate split cards for mobile view
    verdict_path = output_path.replace(".png", "_verdict.png")
    analysis_path = output_path.replace(".png", "_analysis.png")
    
    # Extract coordinates and verdict for title integration
    real_u = thread_config.get("real_u", 0.0)
    real_psi = thread_config.get("real_psi", 0.0)
    coords_str = f"({real_u:+.1f}, {real_psi:+.1f})"
    
    # Try to find anchor and verdict from posts
    import re
    verdict_text = ""
    if len(posts) > 2:
        m = re.search(r"Resulting Judgement:\s*(.*)", posts[2])
        if m:
            verdict_text = m.group(1).strip()
    if not verdict_text:
        # Fallback based on coordinates
        anchor = "Neutral"
        if real_u > 0.3 and real_psi > 0.3:
            anchor = "Greater Good"
        elif real_u < -0.3 and real_psi > 0.3:
            anchor = "Greatest Lie"
        elif real_u > 0.3 and real_psi < -0.3:
            anchor = "Lesser Good"
        elif real_u < -0.3 and real_psi < -0.3:
            anchor = "Greater Evil"
        verdict_text = f"{coords_str} — {anchor}"
        
    v_class = ""
    if len(posts) > 3:
        m_v = re.search(r"Verdict:\s*(.*?)(?:\.|\n|$)", posts[3])
        if m_v:
            v_class = m_v.group(1).strip()
            
    if v_class:
        verdict_subtitle = f"Resulting Judgement: {verdict_text} | {v_class}"
    else:
        verdict_subtitle = f"Resulting Judgement: {verdict_text}"

    # Verdict Card: Hook, Claim, Reality, Verdict, plus Sub-Audits Breakdown if multi-aspect is active
    _generate_verdict_card(subject, verdict_subtitle, sections[:5] if is_multi_aspect else sections[:4], fonts, link, verdict_path)

    
    # Analysis & Perspectives Card: Context, Nuance, Breakdown, Social Physics, Trajectory, Unavoidables
    analysis_subtitle = f"SYSTEM ANALYSIS & PERSPECTIVES | {coords_str}"
    _generate_analysis_full_card(subject, analysis_subtitle, sections[5:] if is_multi_aspect else sections[4:], personas, fonts, link, analysis_path)


def _generate_verdict_card(subject, subtitle, sections, fonts, link, output_path):
    canvas_bg = "#0B0F19"
    card_bg = "#141D2F"
    border_color = "#25354F"
    text_color = "#E2E8F0"
    canvas_w = 1200
    x_left = 40
    x_right = canvas_w - x_left
    drawable_w = x_right - x_left
    
    temp_img = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    
    col_gap = 30
    col_w = (drawable_w - col_gap) // 2
    col_1_x_left = x_left
    col_1_x_right = col_1_x_left + col_w
    col_2_x_left = col_1_x_right + col_gap
    col_2_x_right = col_2_x_left + col_w
    
    sec_text_w = col_w - 40
    line_h = 38 # size 29 line height
    card_gap = 25
    
    current_y = 50
    title_lines = wrap_text(subject, fonts["bold_39"], drawable_w, temp_draw)
    subtitle_lines = wrap_text(subtitle, fonts["bold_27"], drawable_w, temp_draw)
    
    title_h = (len(title_lines) * 46) + 5 + (len(subtitle_lines) * 34)
    title_y_start = current_y
    current_y += title_h + 30
    
    grid_start_y = current_y
    
    left_sections = sections[0:2] # Hook, Claim
    right_sections = sections[2:4] # Reality, Verdict
    
    left_layouts = []
    left_y = grid_start_y
    for sec in left_sections:
        wrapped_body = wrap_text(sec["text"], fonts["regular_29"], sec_text_w, temp_draw)
        body_h = len(wrapped_body) * line_h
        card_h = 25 + 24 + body_h + 25
        left_layouts.append({
            "sec": sec, "x_left": col_1_x_left, "x_right": col_1_x_right, "y": left_y, "h": card_h, "lines": wrapped_body
        })
        left_y += card_h + card_gap
    left_grid_h = left_y - card_gap - grid_start_y
        
    right_layouts = []
    right_y = grid_start_y
    for sec in right_sections:
        wrapped_body = wrap_text(sec["text"], fonts["regular_29"], sec_text_w, temp_draw)
        body_h = len(wrapped_body) * line_h
        card_h = 25 + 24 + body_h + 25
        right_layouts.append({
            "sec": sec, "x_left": col_2_x_left, "x_right": col_2_x_right, "y": right_y, "h": card_h, "lines": wrapped_body
        })
        right_y += card_h + card_gap
    right_grid_h = right_y - card_gap - grid_start_y
        
    grid_h = max(left_grid_h, right_grid_h)
    
    # Horizontal card layout for Sub-Audits Breakdown if present
    sub_layout = None
    if len(sections) == 5:
        sec = sections[4]
        sec_text_w_full = drawable_w - 40
        wrapped_body = wrap_text(sec["text"], fonts["regular_29"], sec_text_w_full, temp_draw)
        body_h = len(wrapped_body) * line_h
        card_h_sub = 25 + 24 + body_h + 25
        sub_card_y = grid_start_y + grid_h + card_gap
        sub_layout = {
            "sec": sec, "x_left": x_left, "x_right": x_right, "y": sub_card_y, "h": card_h_sub, "lines": wrapped_body
        }
        grid_h += card_gap + card_h_sub

    footer_h = 160
    final_height = grid_start_y + grid_h + footer_h
    
    img = Image.new("RGB", (canvas_w, final_height), canvas_bg)
    draw = ImageDraw.Draw(img)
    
    y = title_y_start
    for line in title_lines:
        draw.text((x_left, y), line, fill="#F8FAFC", font=fonts["bold_39"])
        y += 46
    y += 5
    for line in subtitle_lines:
        draw.text((x_left, y), line, fill="#38BDF8", font=fonts["bold_27"])
        y += 34
        
    for lay in left_layouts:
        _draw_individual_card_v3(draw, lay, fonts, card_bg, border_color, text_color, line_h, "bold_27", "regular_29", 65)
    for lay in right_layouts:
        _draw_individual_card_v3(draw, lay, fonts, card_bg, border_color, text_color, line_h, "bold_27", "regular_29", 65)
        
    if sub_layout:
        _draw_individual_card_v3(draw, sub_layout, fonts, card_bg, border_color, text_color, line_h, "bold_27", "regular_29", 65)
        
    # Draw Footer with Watermark and QR code
    footer_y = grid_start_y + grid_h + 30
    draw.text((x_left, footer_y + 15), "Aletheia Bot | Uncompromising Logic & Truth", fill="#64748B", font=fonts["bold_27"])
    draw.text((x_left, footer_y + 55), "Scan QR code to read the verified source article", fill="#475569", font=fonts["regular_22"])
    
    if link:
        qr_img = _generate_qr_code(link, size=110)
        if qr_img:
            qr_x = x_right - 110
            qr_y = footer_y + 10
            draw.rounded_rectangle([qr_x - 5, qr_y - 5, qr_x + 115, qr_y + 115], radius=6, fill=card_bg, outline=border_color, width=1)
            img.paste(qr_img, (qr_x, qr_y))
            
    img.save(output_path, "PNG")
    print(f"Verdict Card generated: {output_path}")

def _generate_analysis_full_card(subject, subtitle, sections, personas, fonts, link, output_path):
    canvas_bg = "#0B0F19"
    card_bg = "#141D2F"
    border_color = "#25354F"
    text_color = "#E2E8F0"
    canvas_w = 1200
    x_left = 40
    x_right = canvas_w - x_left
    drawable_w = x_right - x_left
    
    temp_img = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    
    col_gap = 30
    col_w = (drawable_w - col_gap) // 2
    col_1_x_left = x_left
    col_1_x_right = col_1_x_left + col_w
    col_2_x_left = col_1_x_right + col_gap
    col_2_x_right = col_2_x_left + col_w
    
    sec_text_w = col_w - 40
    line_h = 32 # size 24 line height
    card_gap = 25
    
    current_y = 50
    title_wrap_w = drawable_w - 140 if link else drawable_w
    title_lines = wrap_text(subject, fonts["bold_36"], title_wrap_w, temp_draw)
    subtitle_lines = wrap_text(subtitle, fonts["bold_24"], title_wrap_w, temp_draw)
    
    title_h = (len(title_lines) * 42) + 5 + (len(subtitle_lines) * 30)
    title_y_start = current_y
    current_y += title_h + 30
    if link and current_y < 180:
        current_y = 180
    
    grid_start_y = current_y
    
    left_sections = sections[0:3] # Context, Poison/Bright Side, Breakdown
    right_sections = sections[3:6] # Social Physics, Trajectory, Unavoidables
    
    left_layouts = []
    left_y = grid_start_y
    for sec in left_sections:
        wrapped_body = wrap_text(sec["text"], fonts["regular_24"], sec_text_w, temp_draw)
        body_h = len(wrapped_body) * line_h
        card_h = 25 + 20 + body_h + 25
        left_layouts.append({
            "sec": sec, "x_left": col_1_x_left, "x_right": col_1_x_right, "y": left_y, "h": card_h, "lines": wrapped_body
        })
        left_y += card_h + card_gap
    left_grid_h = left_y - card_gap - grid_start_y
        
    right_layouts = []
    right_y = grid_start_y
    for sec in right_sections:
        wrapped_body = wrap_text(sec["text"], fonts["regular_24"], sec_text_w, temp_draw)
        body_h = len(wrapped_body) * line_h
        card_h = 25 + 20 + body_h + 25
        right_layouts.append({
            "sec": sec, "x_left": col_2_x_left, "x_right": col_2_x_right, "y": right_y, "h": card_h, "lines": wrapped_body
        })
        right_y += card_h + card_gap
    right_grid_h = right_y - card_gap - grid_start_y
        
    grid_h = max(left_grid_h, right_grid_h)
    
    perspectives_header_y = grid_start_y + grid_h + 30
    persona_start_y = perspectives_header_y + 60
    
    per_gap = 20
    per_col_w = (drawable_w - (per_gap * 2)) // 3
    per_x_positions = [
        (x_left, x_left + per_col_w),
        (x_left + per_col_w + per_gap, x_left + per_col_w + per_gap + per_col_w),
        (x_left + (per_col_w + per_gap) * 2, x_left + (per_col_w + per_gap) * 2 + per_col_w)
    ]
    per_text_w = per_col_w - 40
    
    persona_heights = []
    persona_lines = []
    for per in personas:
        wrapped_body = wrap_text(per["text"], fonts["regular_24"], per_text_w, temp_draw)
        body_h = len(wrapped_body) * line_h
        card_h = 25 + 20 + body_h + 25
        persona_heights.append(card_h)
        persona_lines.append(wrapped_body)
        
    max_per_h = max(persona_heights)
    final_height = persona_start_y + max_per_h + 50
    
    img = Image.new("RGB", (canvas_w, final_height), canvas_bg)
    draw = ImageDraw.Draw(img)
    
    # Draw QR code in top-right corner if link is present
    if link:
        qr_img = _generate_qr_code(link, size=110)
        if qr_img:
            qr_x = x_right - 110
            qr_y = 40
            draw.rounded_rectangle([qr_x - 5, qr_y - 5, qr_x + 115, qr_y + 115], radius=6, fill=card_bg, outline=border_color, width=1)
            img.paste(qr_img, (qr_x, qr_y))

    y = title_y_start
    for line in title_lines:
        draw.text((x_left, y), line, fill="#F8FAFC", font=fonts["bold_36"])
        y += 42
    y += 5
    for line in subtitle_lines:
        draw.text((x_left, y), line, fill="#38BDF8", font=fonts["bold_24"])
        y += 30
        
    for lay in left_layouts:
        _draw_individual_card_v3(draw, lay, fonts, card_bg, border_color, text_color, line_h, "bold_24", "regular_24", 60)
    for lay in right_layouts:
        _draw_individual_card_v3(draw, lay, fonts, card_bg, border_color, text_color, line_h, "bold_24", "regular_24", 60)
        
    draw.text((x_left, perspectives_header_y), "TRINARY PERSPECTIVES", font=fonts["bold_24"], fill="#F8FAFC")
    draw.line((x_left, perspectives_header_y + 35, x_right, perspectives_header_y + 35), fill=border_color, width=1)
    
    for idx, per in enumerate(personas):
        x1, x2 = per_x_positions[idx]
        lines = persona_lines[idx]
        
        draw.rounded_rectangle([x1, persona_start_y, x2, persona_start_y + max_per_h], radius=12, fill=card_bg, outline=border_color, width=1)
        draw.rounded_rectangle([x1 + 10, persona_start_y + 1, x1 + 10 + (x2 - x1 - 20), persona_start_y + 7], radius=3, fill=per["color"])
        draw.text((x1 + 20, persona_start_y + 22), per["label"], fill=per["color"], font=fonts["bold_24"])
        
        text_y = persona_start_y + 60
        for line in lines:
            draw.text((x1 + 20, text_y), line, fill=text_color, font=fonts["regular_24"])
            text_y += line_h
            
    img.save(output_path, "PNG")
    print(f"Analysis & Perspectives Card generated: {output_path}")

def _draw_individual_card_v3(draw, lay, fonts, card_bg, border_color, text_color, line_h, header_font_key, body_font_key, text_y_offset):
    sec = lay["sec"]
    x1 = lay["x_left"]
    x2 = lay["x_right"]
    card_y = lay["y"]
    card_h = lay["h"]
    lines = lay["lines"]
    
    draw.rounded_rectangle([x1, card_y, x2, card_y + card_h], radius=12, fill=card_bg, outline=border_color, width=1)
    draw.rounded_rectangle([x1 + 1, card_y + 10, x1 + 7, card_y + card_h - 10], radius=3, fill=sec["color"])
    draw.text((x1 + 20, card_y + 22), sec["label"], fill=sec["color"], font=fonts[header_font_key])
    
    text_y = card_y + text_y_offset
    for line in lines:
        draw.text((x1 + 20, text_y), line, fill=text_color, font=fonts[body_font_key])
        text_y += line_h

def _generate_five_word_card(subject, subtitle, posts, fonts, link, output_path):
    canvas_bg = "#0B0F19"
    card_bg = "#141D2F"
    border_color = "#25354F"
    text_color = "#E2E8F0"
    canvas_w = 1100
    canvas_h = 860
    x_left = 40
    x_right = canvas_w - x_left
    drawable_w = x_right - x_left
    
    img = Image.new("RGB", (canvas_w, canvas_h), canvas_bg)
    draw = ImageDraw.Draw(img)
    
    temp_img = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # Wrap title within 1020px
    title_lines = wrap_text(subject, fonts["bold_36"], drawable_w, temp_draw)
    subtitle_lines = wrap_text(subtitle, fonts["bold_24"], drawable_w, temp_draw)
    
    y = 40
    for line in title_lines:
        draw.text((x_left, y), line, fill="#F8FAFC", font=fonts["bold_36"])
        y += 42
    y += 5
    for line in subtitle_lines:
        draw.text((x_left, y), line, fill="#38BDF8", font=fonts["bold_24"])
        y += 30
        
    # Container coordinates
    container_y1 = 160
    container_y2 = 820
    
    # Draw Container Box
    draw.rounded_rectangle([x_left, container_y1, x_right, container_y2], radius=16, fill=card_bg, outline=border_color, width=1)
    
    # Draw Left-side Terminal rows
    line_configs = [
        {"label": "HOOK", "color": "#F472B6"},
        {"label": "CLAIM", "color": "#94A3B8"},
        {"label": "REALITY", "color": "#38BDF8"},
        {"label": "VERDICT", "color": "#FBBF24"},
        {"label": "CONTEXT", "color": "#60A5FA"},
        {"label": "NUANCE", "color": "#34D399"},
        {"label": "BREAKDOWN", "color": "#F87171"},
        {"label": "PHYSICS", "color": "#A78BFA"},
        {"label": "TRAJECTORY", "color": "#FB923C"},
        {"label": "LIMITS", "color": "#E879F9"},
        {"label": "ALETHEIA", "color": "#2DD4BF"},
        {"label": "AWWTHE", "color": "#F43F5E"},
        {"label": "BROTHE", "color": "#F59E0B"},
    ]
    
    row_start_y = container_y1 + 30
    row_height = 45
    
    for idx, cfg in enumerate(line_configs):
        if idx >= len(posts):
            break
        text = posts[idx].strip()
        
        # Clean clean prefixes from the generated text if the LLM outputted them
        for prefix in ["Alethekanon:\n", "Awwthekanon:\n", "Brothekanon:\n", "The Bright Side:\n", "The Poison:\n", "Social Physics Analysis:\n", "The Trajectory: "]:
            if text.startswith(prefix):
                text = text[len(prefix):].strip()
        if idx == 0 and "\n\n" in text:
            text = text.split("\n\n")[0].strip()
            
        line_y = row_start_y + idx * row_height
        
        # Draw label
        draw.text((x_left + 30, line_y), cfg["label"] + ":", fill=cfg["color"], font=fonts["bold_24"])
        
        # Draw 5-word text
        wrapped_text_lines = wrap_text(text, fonts["regular_24"], 600, temp_draw)
        text_y_offset = 0
        for w_line in wrapped_text_lines[:2]: # Max 2 lines to fit row
            draw.text((x_left + 230, line_y + text_y_offset), w_line, fill=text_color, font=fonts["regular_24"])
            text_y_offset += 24
            
    # Draw QR Code if link is present
    if link:
        qr_img = _generate_qr_code(link, size=130)
        if qr_img:
            qr_x = x_right - 170
            qr_y = container_y2 - 150
            draw.text((qr_x, qr_y - 25), "SCAN SOURCE", fill="#64748B", font=fonts["bold_16"])
            draw.rounded_rectangle([qr_x - 5, qr_y - 5, qr_x + 135, qr_y + 135], radius=8, fill=card_bg, outline=border_color, width=1)
            img.paste(qr_img, (qr_x, qr_y))

            
    img.save(output_path, "PNG")
    print(f"Five-Word Info Card generated: {output_path}")

def _generate_qr_code(url, size=150):
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=10, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="white", back_color="#141D2F")
        img = img.convert("RGB")
        return img.resize((size, size))
    except Exception as e:
        print(f"Warning: Failed to generate QR code image for url '{url}': {e}")
        return None

