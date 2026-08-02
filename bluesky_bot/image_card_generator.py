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
    
    if len(posts) < 13:
        raise ValueError(f"Cannot generate compact info card: posts array has length {len(posts)} (expected 13).")

    # Load standard layout configuration
    fonts = load_theme_fonts()
    canvas_bg = "#0B0F19"
    card_bg = "#141D2F"
    border_color = "#25354F"
    text_color = "#E2E8F0"
    
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

    # Create dummy draw interface to measure sizes
    temp_img = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)

    # 1. LAYOUT PASS: Compute grid dimensions and dynamic height
    canvas_w = 1200
    x_left = 40
    x_right = canvas_w - x_left # 1160px
    drawable_w = x_right - x_left # 1120px
    
    # 2-Column Grid dimensions for Sections
    col_gap = 30
    col_w = (drawable_w - col_gap) // 2 # 545px
    col_1_x_left = x_left
    col_1_x_right = col_1_x_left + col_w
    col_2_x_left = col_1_x_right + col_gap
    col_2_x_right = col_2_x_left + col_w
    
    # Text wrapping widths
    sec_text_w = col_w - 50 # 495px (25px padding left/right)
    
    # Sizing parameters
    line_h = 28 # Height per text line
    card_gap = 25 # Vertical space between stacked cards
    
    current_y = 50 # Start padding

    # Title layout (spans full width)
    title_lines = wrap_text(subject, fonts["bold_32"], drawable_w, temp_draw)
    title_h = len(title_lines) * 38
    title_y_start = current_y
    current_y += title_h + 30 # Title margin

    grid_start_y = current_y

    # Split sections into Left and Right Columns (5 sections each)
    left_sections = sections[:5]  # Hook, Claim, Reality, Verdict, Context
    right_sections = sections[5:] # Nuance, Breakdown, Social Physics, Trajectory, Unavoidables

    # Left Column cards layout
    left_layouts = []
    left_y = grid_start_y
    for sec in left_sections:
        wrapped_body = wrap_text(sec["text"], fonts["regular_20"], sec_text_w, temp_draw)
        body_h = len(wrapped_body) * line_h
        card_h = 25 + 15 + body_h + 25
        
        left_layouts.append({
            "sec": sec,
            "y": left_y,
            "h": card_h,
            "lines": wrapped_body
        })
        left_y += card_h + card_gap

    # Right Column cards layout
    right_layouts = []
    right_y = grid_start_y
    for sec in right_sections:
        wrapped_body = wrap_text(sec["text"], fonts["regular_20"], sec_text_w, temp_draw)
        body_h = len(wrapped_body) * line_h
        card_h = 25 + 15 + body_h + 25
        
        right_layouts.append({
            "sec": sec,
            "y": right_y,
            "h": card_h,
            "lines": wrapped_body
        })
        right_y += card_h + card_gap

    # Grid bottom is the max of both columns
    grid_end_y = max(left_y, right_y) - card_gap + 15

    # Perspectives Panel Header
    perspectives_header_y = grid_end_y
    persona_start_y = perspectives_header_y + 35 + 25 # label (35) + padding (25)

    # 3-Column Grid for perspectives
    per_gap = 20
    per_col_w = (drawable_w - (per_gap * 2)) // 3 # 360px
    
    per_x_positions = [
        (x_left, x_left + per_col_w),
        (x_left + per_col_w + per_gap, x_left + per_col_w + per_gap + per_col_w),
        (x_left + (per_col_w + per_gap) * 2, x_left + (per_col_w + per_gap) * 2 + per_col_w)
    ]
    
    per_text_w = per_col_w - 40 # 320px (20px card padding left/right)

    # Measure persona card heights
    persona_heights = []
    persona_lines = []
    for per in personas:
        wrapped_body = wrap_text(per["text"], fonts["regular_20"], per_text_w, temp_draw)
        body_h = len(wrapped_body) * line_h
        card_h = 25 + 15 + body_h + 25
        persona_heights.append(card_h)
        persona_lines.append(wrapped_body)

    # Make them all the same height (max) for perfect alignment
    max_per_h = max(persona_heights)

    # Footer position
    footer_y = persona_start_y + max_per_h + 40
    final_height = footer_y + 30 + 50 # padding/margins

    # 2. DRAWING PASS
    img = Image.new("RGB", (canvas_w, final_height), canvas_bg)
    draw = ImageDraw.Draw(img)

    # Draw Title
    y = title_y_start
    for line in title_lines:
        draw.text((x_left, y), line, font=fonts["bold_32"], fill="#FFFFFF")
        y += 38

    # Draw Left Column
    for layout in left_layouts:
        sec = layout["sec"]
        card_top = layout["y"]
        card_h = layout["h"]
        card_bottom = card_top + card_h
        
        draw.rounded_rectangle(
            (col_1_x_left, card_top, col_1_x_right, card_bottom),
            radius=12, fill=card_bg, outline=border_color, width=1
        )
        draw.rounded_rectangle(
            (col_1_x_left + 1, card_top + 10, col_1_x_left + 7, card_bottom - 10),
            radius=3, fill=sec["color"]
        )
        draw.text(
            (col_1_x_left + 25, card_top + 22),
            sec["label"], font=fonts["bold_16"], fill=sec["color"]
        )
        text_y = card_top + 55
        for line in layout["lines"]:
            draw.text(
                (col_1_x_left + 25, text_y),
                line, font=fonts["regular_20"], fill=text_color
            )
            text_y += line_h

    # Draw Right Column
    for layout in right_layouts:
        sec = layout["sec"]
        card_top = layout["y"]
        card_h = layout["h"]
        card_bottom = card_top + card_h
        
        draw.rounded_rectangle(
            (col_2_x_left, card_top, col_2_x_right, card_bottom),
            radius=12, fill=card_bg, outline=border_color, width=1
        )
        draw.rounded_rectangle(
            (col_2_x_left + 1, card_top + 10, col_2_x_left + 7, card_bottom - 10),
            radius=3, fill=sec["color"]
        )
        draw.text(
            (col_2_x_left + 25, card_top + 22),
            sec["label"], font=fonts["bold_16"], fill=sec["color"]
        )
        text_y = card_top + 55
        for line in layout["lines"]:
            draw.text(
                (col_2_x_left + 25, text_y),
                line, font=fonts["regular_20"], fill=text_color
            )
            text_y += line_h

    # Draw Perspectives Header
    draw.text(
        (x_left, perspectives_header_y),
        "TRINARY PERSPECTIVES", font=fonts["bold_24"], fill="#F8FAFC"
    )
    draw.line(
        (x_left, perspectives_header_y + 35, x_right, perspectives_header_y + 35),
        fill=border_color, width=1
    )

    # Draw 3 perspective columns
    for idx, per in enumerate(personas):
        x_start, x_end = per_x_positions[idx]
        card_top = persona_start_y
        card_bottom = card_top + max_per_h
        
        draw.rounded_rectangle(
            (x_start, card_top, x_end, card_bottom),
            radius=12, fill=card_bg, outline=border_color, width=1
        )
        draw.rounded_rectangle(
            (x_start + 1, card_top + 10, x_start + 7, card_bottom - 10),
            radius=3, fill=per["color"]
        )
        draw.text(
            (x_start + 20, card_top + 22),
            per["label"], font=fonts["bold_16"], fill=per["color"]
        )
        text_y = card_top + 55
        for line in persona_lines[idx]:
            draw.text(
                (x_start + 20, text_y),
                line, font=fonts["regular_20"], fill=text_color
            )
            text_y += line_h

    # Draw Footer
    draw.text(
        (x_left, footer_y),
        "Aletheia Bot | Uncompromising Logic & Truth", font=fonts["mono_20"], fill="#475569"
    )

    # Save to disk
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Info Card generated and saved successfully: {output_path}")

    # Generate split cards for mobile view
    core_path = output_path.replace(".png", "_core.png")
    analysis_path = output_path.replace(".png", "_analysis.png")
    perspectives_path = output_path.replace(".png", "_perspectives.png")
    
    # Core: Hook, Claim, Reality, Verdict, Context at the bottom
    _generate_split_card(subject, "PART 1: CORE VERDICT", sections[:5], fonts, core_path)
    
    # Analysis: Nuance, Breakdown, Trajectory, Unavoidables, Social Physics at the bottom
    analysis_orig = sections[5:]
    analysis_sections = [
        analysis_orig[0],  # Nuance
        analysis_orig[1],  # Breakdown
        analysis_orig[3],  # Trajectory
        analysis_orig[4],  # The Unavoidables
        analysis_orig[2]   # Social Physics Analysis
    ]
    _generate_split_card(subject, "PART 2: SYSTEM ANALYSIS", analysis_sections, fonts, analysis_path)
    _generate_perspectives_card(subject, personas, fonts, perspectives_path)

def _generate_split_card(subject, subtitle, sections, fonts, output_path):
    canvas_bg = "#0B0F19"
    card_bg = "#141D2F"
    border_color = "#25354F"
    text_color = "#E2E8F0"
    canvas_w = 1200
    x_left = 40
    x_right = canvas_w - x_left
    drawable_w = x_right - x_left
    
    # Create dummy draw interface to measure sizes
    temp_img = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    
    # 2-Column Grid dimensions
    col_gap = 30
    col_w = (drawable_w - col_gap) // 2 # 545px
    col_1_x_left = x_left
    col_1_x_right = col_1_x_left + col_w
    col_2_x_left = col_1_x_right + col_gap
    col_2_x_right = col_2_x_left + col_w
    
    sec_text_w = col_w - 40 # 505px (20px padding left/right)
    
    # Sizing parameters
    line_h = 38 # Height per text line (perfect for size 29)
    card_gap = 25
    
    current_y = 50
    # Title layouts (spans full width)
    title_lines = wrap_text(subject, fonts["bold_39"], drawable_w, temp_draw)
    subtitle_lines = wrap_text(subtitle, fonts["bold_27"], drawable_w, temp_draw)
    
    title_h = (len(title_lines) * 46) + 5 + (len(subtitle_lines) * 34)
    title_y_start = current_y
    current_y += title_h + 30
    
    grid_start_y = current_y
    
    # Splicing: left column gets first 2, right column gets next 2, bottom gets last 1
    left_sections = sections[0:2]
    right_sections = sections[2:4]
    bottom_sec = sections[4]
    
    # Measure left column (Top Left)
    left_layouts = []
    left_y = grid_start_y
    for sec in left_sections:
        wrapped_body = wrap_text(sec["text"], fonts["regular_29"], sec_text_w, temp_draw)
        body_h = len(wrapped_body) * line_h
        card_h = 25 + 24 + body_h + 25 # top pad + label + body + bottom pad
        
        left_layouts.append({
            "sec": sec,
            "x_left": col_1_x_left,
            "x_right": col_1_x_right,
            "y": left_y,
            "h": card_h,
            "lines": wrapped_body
        })
        left_y += card_h + card_gap
    left_grid_h = left_y - card_gap - grid_start_y
        
    # Measure right column (Top Right)
    right_layouts = []
    right_y = grid_start_y
    for sec in right_sections:
        wrapped_body = wrap_text(sec["text"], fonts["regular_29"], sec_text_w, temp_draw)
        body_h = len(wrapped_body) * line_h
        card_h = 25 + 24 + body_h + 25 # top pad + label + body + bottom pad
        
        right_layouts.append({
            "sec": sec,
            "x_left": col_2_x_left,
            "x_right": col_2_x_right,
            "y": right_y,
            "h": card_h,
            "lines": wrapped_body
        })
        right_y += card_h + card_gap
    right_grid_h = right_y - card_gap - grid_start_y
        
    # Symmetrical grid bottom height
    grid_h = max(left_grid_h, right_grid_h)
    
    # Measure bottom full-width block
    bottom_y = grid_start_y + grid_h + card_gap
    wrapped_bottom = wrap_text(bottom_sec["text"], fonts["regular_29"], drawable_w - 50, temp_draw)
    bottom_body_h = len(wrapped_bottom) * line_h
    bottom_card_h = 25 + 24 + bottom_body_h + 25
    
    bottom_layout = {
        "sec": bottom_sec,
        "x_left": x_left,
        "x_right": x_right,
        "y": bottom_y,
        "h": bottom_card_h,
        "lines": wrapped_bottom
    }
    
    final_height = bottom_y + bottom_card_h + 40 # padding/margins
    
    # Create canvas
    img = Image.new("RGB", (canvas_w, final_height), canvas_bg)
    draw = ImageDraw.Draw(img)
    
    # Draw Title
    y = title_y_start
    for line in title_lines:
        draw.text((x_left, y), line, fill="#F8FAFC", font=fonts["bold_39"])
        y += 46
    y += 5
    for line in subtitle_lines:
        draw.text((x_left, y), line, fill="#38BDF8", font=fonts["bold_27"])
        y += 34
        
    # Draw Left Column Card list
    for lay in left_layouts:
        _draw_individual_card(draw, lay, fonts, card_bg, border_color, text_color, line_h)
        
    # Draw Right Column Card list
    for lay in right_layouts:
        _draw_individual_card(draw, lay, fonts, card_bg, border_color, text_color, line_h)
        
    # Draw Bottom Full-Width Block
    _draw_individual_card(draw, bottom_layout, fonts, card_bg, border_color, text_color, line_h)
    
    # Save image
    img.save(output_path, "PNG")
    print(f"Split Info Card generated (Grid + Bottom Span, size 29): {output_path}")

def _draw_individual_card(draw, lay, fonts, card_bg, border_color, text_color, line_h):
    sec = lay["sec"]
    x1 = lay["x_left"]
    x2 = lay["x_right"]
    card_y = lay["y"]
    card_h = lay["h"]
    lines = lay["lines"]
    
    # Card outer box
    draw.rounded_rectangle(
        [x1, card_y, x2, card_y + card_h],
        radius=12,
        fill=card_bg,
        outline=border_color,
        width=1
    )
    
    # Indicator bar on the left side
    draw.rounded_rectangle(
        [x1 + 1, card_y + 10, x1 + 7, card_y + card_h - 10],
        radius=3,
        fill=sec["color"]
    )
    
    # Label / Header (27pt font)
    draw.text(
        (x1 + 20, card_y + 22),
        sec["label"],
        fill=sec["color"],
        font=fonts["bold_27"]
    )
    
    # Body text (29pt font)
    text_y = card_y + 65
    for line in lines:
        draw.text(
            (x1 + 20, text_y),
            line,
            fill=text_color,
            font=fonts["regular_29"]
        )
        text_y += line_h

def _generate_perspectives_card(subject, personas, fonts, output_path):
    canvas_bg = "#0B0F19"
    card_bg = "#141D2F"
    border_color = "#25354F"
    text_color = "#E2E8F0"
    canvas_w = 1200
    x_left = 40
    x_right = canvas_w - x_left
    drawable_w = x_right - x_left
    
    # Create dummy draw interface to measure sizes
    temp_img = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    
    line_h = 38 # Size 29 line height
    current_y = 50
    
    # Title layouts (spans full width)
    title_lines = wrap_text(subject, fonts["bold_39"], drawable_w, temp_draw)
    subtitle_lines = wrap_text("PART 3: PERSPECTIVE REACTIONS", fonts["bold_27"], drawable_w, temp_draw)
    
    title_h = (len(title_lines) * 46) + 5 + (len(subtitle_lines) * 34)
    title_y_start = current_y
    current_y += title_h + 30
    
    persona_start_y = current_y
    
    # 3-Column Grid for perspectives
    per_gap = 20
    per_col_w = (drawable_w - (per_gap * 2)) // 3 # 360px
    per_x_positions = [
        (x_left, x_left + per_col_w),
        (x_left + per_col_w + per_gap, x_left + per_col_w + per_gap + per_col_w),
        (x_left + (per_col_w + per_gap) * 2, x_left + (per_col_w + per_gap) * 2 + per_col_w)
    ]
    per_text_w = per_col_w - 40 # 320px (20px card padding left/right)
    
    persona_heights = []
    persona_lines = []
    for per in personas:
        wrapped_body = wrap_text(per["text"], fonts["regular_29"], per_text_w, temp_draw)
        body_h = len(wrapped_body) * line_h
        card_h = 25 + 24 + body_h + 25
        persona_heights.append(card_h)
        persona_lines.append(wrapped_body)
        
    max_per_h = max(persona_heights)
    
    final_height = persona_start_y + max_per_h + 50
    
    # Create canvas
    img = Image.new("RGB", (canvas_w, final_height), canvas_bg)
    draw = ImageDraw.Draw(img)
    
    # Draw Title
    y = title_y_start
    for line in title_lines:
        draw.text((x_left, y), line, fill="#F8FAFC", font=fonts["bold_39"])
        y += 46
    y += 5
    for line in subtitle_lines:
        draw.text((x_left, y), line, fill="#38BDF8", font=fonts["bold_27"])
        y += 34
        
    # Draw the 3 columns
    for idx, per in enumerate(personas):
        x1, x2 = per_x_positions[idx]
        lines = persona_lines[idx]
        
        # Card Background
        draw.rounded_rectangle(
            [x1, persona_start_y, x2, persona_start_y + max_per_h],
            radius=12,
            fill=card_bg,
            outline=border_color,
            width=1
        )
        
        # Indicator top bar
        draw.rounded_rectangle(
            [x1 + 10, persona_start_y + 1, x1 + 10 + (x2 - x1 - 20), persona_start_y + 7],
            radius=3,
            fill=per["color"]
        )
        
        # Label
        draw.text(
            (x1 + 20, persona_start_y + 22),
            per["label"],
            fill=per["color"],
            font=fonts["bold_27"]
        )
        
        # Body text
        text_y = persona_start_y + 65
        for line in lines:
            draw.text(
                (x1 + 20, text_y),
                line,
                fill=text_color,
                font=fonts["regular_29"]
            )
            text_y += line_h
            
    # Save image
    img.save(output_path, "PNG")
    print(f"Split Perspectives Card generated: {output_path}")
