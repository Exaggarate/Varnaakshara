#!/usr/bin/env python3
"""Generate DMG background image — drag Varnaakshara to Applications arrow."""

from PIL import Image, ImageDraw, ImageFont
import os

def create_dmg_background(output_path='dmg_background.png', width=660, height=400):
    """Create a professional DMG background with drag-to-Applications arrow."""
    
    # Deep purple gradient background matching app theme
    img = Image.new('RGBA', (width, height), (26, 14, 40, 255))
    draw = ImageDraw.Draw(img)
    
    # Gradient overlay
    for y in range(height):
        alpha = int(255 * (1 - y / height * 0.3))
        r = int(26 + (32 - 26) * y / height)
        g = int(14 + (16 - 14) * y / height)
        b = int(40 + (48 - 40) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    
    # Subtle mandala-like decorative circle in center
    cx, cy = width // 2, height // 2
    for r in range(120, 40, -10):
        opacity = int(20 + (120 - r) * 0.3)
        draw.ellipse(
            [cx - r, cy - r - 20, cx + r, cy + r - 20],
            outline=(201, 151, 62, opacity),
            width=1
        )
    
    # Arrow from left (app icon area) to right (Applications area)
    arrow_y = height // 2 + 20
    arrow_start = width // 2 - 60
    arrow_end = width // 2 + 60
    
    # Arrow shaft
    draw.line(
        [(arrow_start, arrow_y), (arrow_end - 15, arrow_y)],
        fill=(201, 151, 62, 200),
        width=3
    )
    
    # Arrowhead
    draw.polygon(
        [(arrow_end, arrow_y), (arrow_end - 18, arrow_y - 10), (arrow_end - 18, arrow_y + 10)],
        fill=(201, 151, 62, 200)
    )
    
    # Title text at top
    try:
        title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
        sub_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    except (IOError, OSError):
        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
    
    # Title
    title = "Varnaakshara"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, 30), title, fill=(232, 200, 98, 255), font=title_font)
    
    # Subtitle
    sub = "Drag to Applications to install"
    bbox2 = draw.textbbox((0, 0), sub, font=sub_font)
    sw = bbox2[2] - bbox2[0]
    draw.text(((width - sw) // 2, height - 40), sub, fill=(184, 168, 138, 220), font=sub_font)
    
    # Convert to RGB for PNG
    rgb_img = Image.new('RGB', (width, height), (26, 14, 40))
    rgb_img.paste(img, mask=img.split()[3])
    rgb_img.save(output_path, 'PNG')
    print(f'DMG background saved: {output_path} ({width}x{height})')
    return output_path


if __name__ == '__main__':
    create_dmg_background()
