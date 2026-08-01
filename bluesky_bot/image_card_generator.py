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
        
    fonts["regular_24"] = None
    for n in regular_names:
        f = get_font(n, 24)
        if is_valid_font(f):
            fonts["regular_24"] = f
            break
    if fonts["regular_24"] is None:
        fonts["regular_24"] = ImageFont.load_default()

    # Bold fonts
    fonts["bold_32"] = None
    for n in bold_names:
        f = get_font(n, 32)
        if is_valid_font(f):
            fonts["bold_32"] = f
            break
    if fonts["bold_32"] is None:
        fonts["bold_32"] = ImageFont.load_default()

    fonts["bold_24"] = None
    for n in bold_names:
        f = get_font(n, 24)
        if is_valid_font(f):
            fonts["bold_24"] = f
            break
    if fonts["bold_24"] is None:
        fonts["bold_24"] = ImageFont.load_default()

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
    """Renders posts 4-12 of the thread config into a beautiful dark-mode infographic card."""
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
    
    # Define sections with clean titles, content (strip prefixes), and custom colors
    sections = [
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
    ]
    
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

    # 1. LAYOUT PASS: Compute dynamic heights
    x_left = 40
    x_right = 960
    card_w = x_right - x_left # 920px
    text_w = card_w - 60 # 860px (30px card padding left/right)
    
    line_h = 28 # Height per text line including spacing
    gap = 25 # Gap between cards
    
    current_y = 50 # Start padding

    # Title layout
    title_lines = wrap_text(subject, fonts["bold_32"], card_w, temp_draw)
    title_h = len(title_lines) * 38
    title_y_start = current_y
    current_y += title_h + 30 # Title margin

    # Calculate height for each section card
    section_layouts = []
    for sec in sections:
        wrapped_body = wrap_text(sec["text"], fonts["regular_20"], text_w, temp_draw)
        body_h = len(wrapped_body) * line_h
        card_h = 25 + 15 + body_h + 25 # Label height (25) + label margin (15) + body (body_h) + bottom padding (25)
        
        section_layouts.append({
            "sec": sec,
            "y": current_y,
            "h": card_h,
            "lines": wrapped_body
        })
        current_y += card_h + gap

    # Header for Perspectives Panel
    perspectives_header_y = current_y
    current_y += 35 + 15 # Label (35) + gap (15)

    # Calculate height for each persona block
    persona_layouts = []
    for per in personas:
        wrapped_body = wrap_text(per["text"], fonts["regular_20"], text_w, temp_draw)
        body_h = len(wrapped_body) * line_h
        card_h = 25 + 15 + body_h + 25 # Label height (25) + label margin (15) + body (body_h) + bottom padding (25)
        
        persona_layouts.append({
            "per": per,
            "y": current_y,
            "h": card_h,
            "lines": wrapped_body
        })
        current_y += card_h + 20 # Symmetrical spacing between persona cards

    # Add watermark/footer height
    current_y += 40 # Footer margin
    footer_y = current_y
    current_y += 30 + 50 # Bottom padding (50)

    final_height = current_y

    # 2. DRAWING PASS
    img = Image.new("RGB", (1000, final_height), canvas_bg)
    draw = ImageDraw.Draw(img)

    # Draw Title
    y = title_y_start
    for line in title_lines:
        draw.text((x_left, y), line, font=fonts["bold_32"], fill="#FFFFFF")
        y += 38

    # Draw Sections
    for layout in section_layouts:
        sec = layout["sec"]
        card_top = layout["y"]
        card_h = layout["h"]
        card_bottom = card_top + card_h
        
        # Draw card card panel background
        draw.rounded_rectangle(
            (x_left, card_top, x_right, card_bottom),
            radius=12, fill=card_bg, outline=border_color, width=1
        )
        
        # Draw accent strip on left border
        draw.rounded_rectangle(
            (x_left + 1, card_top + 10, x_left + 7, card_bottom - 10),
            radius=3, fill=sec["color"]
        )
        
        # Draw card label header
        draw.text(
            (x_left + 30, card_top + 22),
            sec["label"], font=fonts["bold_16"], fill=sec["color"]
        )
        
        # Draw card body text
        text_y = card_top + 55
        for line in layout["lines"]:
            draw.text(
                (x_left + 30, text_y),
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

    # Draw Persona blocks
    for layout in persona_layouts:
        per = layout["per"]
        card_top = layout["y"]
        card_h = layout["h"]
        card_bottom = card_top + card_h
        
        # Draw card card panel background
        draw.rounded_rectangle(
            (x_left, card_top, x_right, card_bottom),
            radius=12, fill=card_bg, outline=border_color, width=1
        )
        
        # Draw accent strip on left border
        draw.rounded_rectangle(
            (x_left + 1, card_top + 10, x_left + 7, card_bottom - 10),
            radius=3, fill=per["color"]
        )
        
        # Draw card label header
        draw.text(
            (x_left + 30, card_top + 22),
            per["label"], font=fonts["bold_16"], fill=per["color"]
        )
        
        # Draw card body text
        text_y = card_top + 55
        for line in layout["lines"]:
            draw.text(
                (x_left + 30, text_y),
                line, font=fonts["regular_20"], fill=text_color
            )
            text_y += line_h

    # Draw Footer
    draw.text(
        (x_left, footer_y),
        "Alethekanon | Uncompromising Logic & Truth", font=fonts["mono_20"], fill="#475569"
    )

    # Save to disk
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Info Card generated and saved successfully: {output_path}")
