
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math

# ==========================================
# THE FAV' MAVERICK - GITHUB ANIMATED BANNER
# ==========================================

WIDTH = 1500
HEIGHT = 500
TOTAL_FRAMES = 48
DURATION = 70

PHOTO_PATH = "profile.jpg"
OUTPUT_PATH = "ambi-rajan-banner.gif"

# Neon theme
BG = (3, 8, 3)
GREEN = (167, 245, 66)
LIME = (212, 255, 0)
WHITE = (239, 255, 220)
MUTED = (150, 180, 130)

# ==========================================
# LOAD FONTS
# ==========================================

def get_font(size, bold=False):

    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold
        else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]

    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


font_small = get_font(19)
font_name = get_font(82, True)
font_brand = get_font(51, True)
font_tag = get_font(19)

# ==========================================
# LOAD ORIGINAL PHOTO
# ==========================================

if not os.path.exists(PHOTO_PATH):
    raise FileNotFoundError(
        "Please place your original photograph "
        "in this folder and name it profile.jpg"
    )

photo = Image.open(PHOTO_PATH).convert("RGB")

# Crop photo proportionally
def crop_photo(image, width, height):

    ratio = max(
        width / image.width,
        height / image.height
    )

    new_width = int(image.width * ratio)
    new_height = int(image.height * ratio)

    image = image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )

    left = (new_width - width) // 2
    top = (new_height - height) // 2

    return image.crop((
        left,
        top,
        left + width,
        top + height
    ))

photo = crop_photo(photo, 405, 440)

# ==========================================
# DRAW TEXT WITH NEON GLOW
# ==========================================

def glowing_text(image, position, text, font, color):

    x, y = position

    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    glow_draw.text(
        (x, y),
        text,
        font=font,
        fill=(*color, 150),
        stroke_width=1
    )

    glow = glow.filter(
        ImageFilter.GaussianBlur(13)
    )

    image.alpha_composite(glow)

    draw = ImageDraw.Draw(image)

    draw.text(
        (x, y),
        text,
        font=font,
        fill=color
    )

# ==========================================
# CREATE ANIMATED FRAMES
# ==========================================

frames = []

for frame_number in range(TOTAL_FRAMES):

    frame = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        BG
    )

    draw = ImageDraw.Draw(frame)

    # Background subtle digital lines
    for y in range(15, HEIGHT, 25):

        draw.line(
            (0, y, WIDTH, y),
            fill=(15, 35, 12),
            width=1
        )

    # Outer frame
    draw.rectangle(
        (10, 10, WIDTH - 10, HEIGHT - 10),
        outline=GREEN,
        width=2
    )

    # Animated light particles
    for i in range(35):

        x = (i * 73 + frame_number * 5) % WIDTH
        y = (i * 47 + frame_number * 3) % HEIGHT

        draw.ellipse(
            (x, y, x + 3, y + 3),
            fill=(80, 150, 40)
        )

    # --------------------------------------
    # LEFT SIDE BRANDING
    # --------------------------------------

    # Animated entrance
    progress = frame_number / 12

    if progress > 1:
        progress = 1

    offset = int(90 * (1 - progress))

    # Small heading
    draw.text(
        (95 - offset, 100),
        "WELCOME TO MY PROFILE",
        font=font_small,
        fill=GREEN
    )

    # First name
    glowing_text(
        frame,
        (90 - offset, 150),
        "AMBI RAJAN",
        font_name,
        WHITE
    )

    # Second name
    glowing_text(
        frame,
        (95 - offset, 270),
        "THE FAV' MAVERICK",
        font_brand,
        LIME
    )

    # Animated connecting line
    line_width = int(430 * progress)

    draw.rounded_rectangle(
        (95, 345, 95 + line_width, 349),
        radius=2,
        fill=GREEN
    )

    # Tagline
    draw.text(
        (95, 380),
        "DATA ANALYTICS  |  DIGITAL CREATOR",
        font=font_tag,
        fill=MUTED
    )

    # --------------------------------------
    # RIGHT SIDE ORIGINAL PHOTO
    # --------------------------------------

    px = 1010
    py = 30

    # Neon photo frame
    draw.rectangle(
        (px - 5, py - 5, px + 410, py + 450),
        outline=GREEN,
        width=3
    )

    # Paste original photo unchanged in content
    frame.paste(photo, (px, py))

    # Photo corner accents
    draw.line(
        (px, py, px + 35, py),
        fill=LIME,
        width=4
    )

    draw.line(
        (px, py, px, py + 35),
        fill=LIME,
        width=4
    )

    draw.line(
        (px + 410, py + 450, px + 375, py + 450),
        fill=LIME,
        width=4
    )

    # --------------------------------------
    # ANIMATED SCANLINE
    # --------------------------------------

    scan_y = (frame_number * 11) % HEIGHT

    scan = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0)
    )

    scan_draw = ImageDraw.Draw(scan)

    scan_draw.rectangle(
        (0, scan_y, WIDTH, scan_y + 2),
        fill=(167, 245, 66, 35)
    )

    frame.alpha_composite(scan)

    frames.append(frame.convert("RGB"))

# ==========================================
# EXPORT ANIMATED GIF
# ==========================================

frames[0].save(
    OUTPUT_PATH,
    save_all=True,
    append_images=frames[1:],
    duration=DURATION,
    loop=0,
    optimize=True
)

print("====================================")
print("GITHUB BANNER CREATED SUCCESSFULLY!")
print("File:", OUTPUT_PATH)
print("Dimensions: 1500 x 500")
print("====================================")
