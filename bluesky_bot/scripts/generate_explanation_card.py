import os
import sys
from PIL import Image, ImageDraw, ImageFont

def generate_card():
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bot_dir = os.path.abspath(os.path.join(script_dir, ".."))
    output_dir = os.path.join(bot_dir, "infographics")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "hypocrisy_explanation.png")

    # Dimensions: 1200 x 1150
    width = 1200
    height = 1150
    image = Image.new("RGB", (width, height), color="#0f172a") # Slate-900 background
    draw = ImageDraw.Draw(image)

    # Load system fonts
    font_path_bold = "C:\\Windows\\Fonts\\segoeuib.ttf" # Segoe UI Bold
    font_path_reg = "C:\\Windows\\Fonts\\segoeui.ttf" # Segoe UI Regular
    font_path_italic = "C:\\Windows\\Fonts\\segoeuii.ttf" # Segoe UI Italic

    if not os.path.exists(font_path_bold):
        font_path_bold = "C:\\Windows\\Fonts\\arialbd.ttf"
        font_path_reg = "C:\\Windows\\Fonts\\arial.ttf"
        font_path_italic = "C:\\Windows\\Fonts\\ariali.ttf"

    try:
        title_font = ImageFont.truetype(font_path_bold, 36)
        header_font = ImageFont.truetype(font_path_bold, 22)
        body_font = ImageFont.truetype(font_path_reg, 21)
        italic_font = ImageFont.truetype(font_path_italic, 19)
    except Exception:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        italic_font = ImageFont.load_default()

    # Draw cyan left border accent line
    draw.rectangle([0, 0, 15, height], fill="#0ea5e9")

    # Main Title
    draw.text((60, 60), "How the \"Actor Hypocrisy Leaderboard\" Works", fill="#0ea5e9", font=title_font)
    
    # Subtitle
    intro_text = (
        "The scoring is entirely automated, AI-driven, and calculated programmatically using "
        "a formal coordinate system called Vector Field Theory (specifically the 6-Attractor SON "
        "Convergence Protocol). No human operator manually adjusts the numbers."
    )
    
    def draw_wrapped_paragraph(text, font, color, x, y, max_w, spacing=30, indent=0):
        words = text.split(" ")
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            line_str = " ".join(current_line)
            w = draw.textlength(line_str, font=font)
            if w > max_w:
                current_line.pop()
                lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))

        for line in lines:
            draw.text((x + indent, y), line, fill=color, font=font)
            y += spacing
        return y

    y_cursor = 125
    y_cursor = draw_wrapped_paragraph(intro_text, body_font, "#f8fafc", 60, y_cursor, width - 120)
    y_cursor += 15

    # Horizontal divider
    draw.line([60, y_cursor, width - 60, y_cursor], fill="#1e293b", width=2)
    y_cursor += 25

    # Pipeline title
    draw.text((60, y_cursor), "Here is the step-by-step pipeline:", fill="#38bdf8", font=header_font)
    y_cursor += 45

    def draw_bullet_section(title_text, body_text, y, indent_level=0):
        start_x = 60 + (indent_level * 30)
        max_w = width - start_x - 60
        
        if title_text:
            # We measure the title width to draw the body inline right after it if they fit,
            # but wrapping is cleaner if we draw the header inline as part of the first line.
            # So let's draw the title, and then calculate where to start the body.
            draw.text((start_x, y), title_text, fill="#38bdf8", font=header_font)
            title_w = draw.textlength(title_text + " ", font=header_font)
            
            # Wrap the body starting with an offset on the first line
            words = body_text.split(" ")
            first_line_words = []
            rest_lines = []
            
            for word in words:
                first_line_words.append(word)
                test_str = " ".join(first_line_words)
                w = draw.textlength(test_str, font=body_font)
                if w > (max_w - title_w):
                    first_line_words.pop()
                    break
            
            first_line_str = " ".join(first_line_words)
            draw.text((start_x + title_w, y), first_line_str, fill="#f8fafc", font=body_font)
            y += 30
            
            remaining_text = " ".join(words[len(first_line_words):])
            if remaining_text:
                y = draw_wrapped_paragraph(remaining_text, body_font, "#f8fafc", start_x, y, max_w)
        else:
            y = draw_wrapped_paragraph(body_text, body_font, "#f8fafc", start_x, y, max_w)
            
        return y + 18

    # Step 1
    y_cursor = draw_bullet_section(
        "• Information Harvesting:",
        "The bot continuously gathers news articles and reports from multiple feeds (RSS and Bluesky).",
        y_cursor
    )

    # Step 2
    y_cursor = draw_bullet_section(
        "• AI Semantic Auditing:",
        "For each story, a Google Gemini model acting as the Master Aletheia Auditor parses the facts.",
        y_cursor
    )

    # Step 3
    y_cursor = draw_bullet_section(
        "• Calculating Stated vs. Actual Coordinates:",
        "The AI calculates two coordinate pairs on a continuous spectrum from -2.0 to +2.0 (representing the Morality u and Will ψ axes):",
        y_cursor
    )
    
    # Sub-bullets for Step 3
    y_cursor = draw_bullet_section(
        "",
        "– The Stated Claim (C_ideal / claim_u): What the actor publicly projects, promises, or claims their intent is.",
        y_cursor,
        indent_level=1
    )
    y_cursor = draw_bullet_section(
        "",
        "– The Assessed Reality (C_action / real_u): The real-world physical outcome or structural effect of the action as documented in the reports (verified using live search queries where necessary).",
        y_cursor,
        indent_level=1
    )

    # Step 4
    y_cursor = draw_bullet_section(
        "• Attractor Math:",
        "The coordinates are computed by calculating the balance of forces against six attractor points (Greater Good, Greater Evil, Lesser Good, Lesser Evil, Good Preference, and Bad Preference).",
        y_cursor
    )

    # Step 5
    y_cursor = draw_bullet_section(
        "• Calculating the Hypocrisy Gap (ΔH):",
        "",
        y_cursor
    )
    
    # Sub-bullets for Step 5
    y_cursor = draw_bullet_section(
        "",
        "– The individual hypocrisy score for a story is the gap between the actor's stated moral position and the actual moral outcome: ΔH = u_claim - u_real.",
        y_cursor,
        indent_level=1
    )
    y_cursor = draw_bullet_section(
        "",
        "– The leaderboard aggregates all stories related to a specific actor and averages this delta (avg Δu).",
        y_cursor,
        indent_level=1
    )
    y_cursor = draw_bullet_section(
        "",
        "– A higher score (rendered in red on the dashboard) indicates a wider distance between what that actor publicly projects vs. the actual outcome of their actions.",
        y_cursor,
        indent_level=1
    )

    # Footer note
    draw.text((60, height - 50), "Methodology derived from Vector Field Theory & 6-Attractor SON Convergence Protocol.", fill="#64748b", font=italic_font)

    image.save(output_path, "PNG")
    print(f"Programmatic Pillow card generated successfully at: {output_path}")

if __name__ == "__main__":
    generate_card()
