#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 meme: a GTA "WASTED" screen for a sleep schedule
killed by GTA 6 launch week, with make.fun's ghost mascot holding its magenta
star coin and the make.fun wordmark worked into the scene.

Everything here is drawn from scratch with Pillow primitives (no photos, no
downloaded assets): the ghost is my own drawing of make.fun's mascot as the
bounty describes it -- a white ghost with a thick black outline, two black
four-pointed sparkle eyes and a round little hand, holding a magenta coin
with a white star.

Usage: python3 scripts/make_meme.py  (writes meme.png next to the repo root)
Canvas is 1200x1200: the judge sees a square picture shrunk to 480x480, so
every letter is kept large and the layout is uncluttered.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "meme.png")

W, H = 1200, 1200
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WASTED_GREY = (201, 201, 201)
MID_GREY = (158, 158, 158)
FAINT_GREY = (181, 181, 181)
MAGENTA = (236, 0, 140)  # make.fun's magenta, for the coin and the dot

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def text_center(draw, y, s, f, fill):
    """Draw s centred horizontally with its top at y; return its height."""
    box = draw.textbbox((0, 0), s, font=f)
    w = box[2] - box[0]
    draw.text(((W - w) / 2 - box[0], y), s, font=f, fill=fill)
    return box[3] - box[1]


def sparkle(draw, cx, cy, v_len, h_len, pinch, fill):
    """A four-pointed sparkle star centred on (cx, cy)."""
    pts = [
        (cx, cy - v_len), (cx + pinch, cy - pinch),
        (cx + h_len, cy), (cx + pinch, cy + pinch),
        (cx, cy + v_len), (cx - pinch, cy + pinch),
        (cx - h_len, cy), (cx - pinch, cy - pinch),
    ]
    draw.polygon(pts, fill=fill)


def star5(draw, cx, cy, r_out, r_in, fill):
    """A five-pointed star centred on (cx, cy)."""
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def ghost_body_mask(size, outline):
    """A ghost silhouette (dome top, straight sides, three-bump hem) as a mask.

    outline expands the silhouette by that many pixels on every side, so
    drawing the mask in black underneath the white one leaves a thick black
    outline around the ghost.
    """
    w, h = size
    mask = Image.new("L", (w + 2 * outline, h + 2 * outline), 0)
    d = ImageDraw.Draw(mask)
    o = outline
    dome_top = o
    side_left, side_right = o + 18, o + w - 18
    hem_top = o + h - 78
    # Dome: top half of an ellipse; its flat edge is the body's shoulder line.
    d.pieslice([side_left, dome_top, side_right, dome_top + 300],
               start=180, end=360, fill=255)
    # Straight body from the dome's flat edge down to the hem.
    d.rectangle([side_left, dome_top + 150, side_right, hem_top], fill=255)
    # Three rounded bumps along the hem.
    bump_w = (side_right - side_left) / 3
    for i in range(3):
        x0 = side_left + i * bump_w
        d.ellipse([x0, hem_top - 40, x0 + bump_w, hem_top + 38], fill=255)
    return mask


def draw_ghost(img, box):
    """Draw make.fun's ghost into box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # Black outline silhouette, then the white body on top of it.
    outline_mask = ghost_body_mask((w, h), 9)
    img.paste(Image.new("RGB", outline_mask.size, BLACK),
              (x0 - 9, y0 - 9), outline_mask)
    body_mask = ghost_body_mask((w, h), 0)
    img.paste(Image.new("RGB", body_mask.size, WHITE),
              (x0, y0), body_mask)
    d = ImageDraw.Draw(img)
    # Two black four-pointed sparkle eyes.
    eye_y = y0 + int(h * 0.45)
    sparkle(d, x0 + int(w * 0.36), eye_y, 30, 17, 7, BLACK)
    sparkle(d, x0 + int(w * 0.64), eye_y, 30, 17, 7, BLACK)
    # Magenta coin with a white star, held up at the ghost's right side.
    coin_cx, coin_cy, coin_r = x0 + w - 62, y0 + int(h * 0.70), 42
    d.ellipse([coin_cx - coin_r, coin_cy - coin_r,
               coin_cx + coin_r, coin_cy + coin_r], fill=MAGENTA)
    d.ellipse([coin_cx - coin_r, coin_cy - coin_r,
               coin_cx + coin_r, coin_cy + coin_r], outline=BLACK, width=4)
    star5(d, coin_cx, coin_cy, 26, 11, WHITE)
    # Round little hand overlapping the coin's lower edge, as if holding it.
    hand_cx, hand_cy, hand_r = coin_cx - 8, coin_cy + 34, 24
    d.ellipse([hand_cx - hand_r, hand_cy - hand_r,
               hand_cx + hand_r, hand_cy + hand_r], fill=WHITE)
    d.ellipse([hand_cx - hand_r, hand_cy - hand_r,
               hand_cx + hand_r, hand_cy + hand_r], outline=BLACK, width=5)


def main():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)

    # The GTA death screen, huge and grey, with a soft shadow. Shrink the
    # font until the word fits the canvas with room on both sides.
    wasted = "WASTED"
    f_size = 258
    while True:
        f_wasted = font(f_size)
        box = d.textbbox((0, 0), wasted, font=f_wasted)
        if box[2] - box[0] <= 1060 or f_size <= 100:
            break
        f_size -= 8
    ww = box[2] - box[0]
    d.text(((W - ww) / 2 - box[0] + 7, 178 + 8), wasted,
           font=f_wasted, fill=(38, 38, 38))
    d.text(((W - ww) / 2 - box[0], 178), wasted,
           font=f_wasted, fill=WASTED_GREY)

    # What died.
    text_center(d, 486, "MY SLEEP SCHEDULE", font(64), WHITE)
    # Cause of death.
    text_center(d, 578, "cause of death: GTA 6 launch week",
                font(44), MID_GREY)

    # make.fun's ghost, bottom right, holding its coin.
    draw_ghost(img, (780, 650, 1130, 1100))

    # make.fun wordmark, bottom left: white name, magenta dot.
    wx, wy = 78, 1008
    f_mark = font(82)
    d.text((wx, wy), "make", font=f_mark, fill=WHITE)
    w_make = d.textbbox((0, 0), "make", font=f_mark)[2]
    d.text((wx + w_make, wy), ".", font=f_mark, fill=MAGENTA)
    w_dot = d.textbbox((0, 0), ".", font=f_mark)[2]
    d.text((wx + w_make + w_dot, wy), "fun", font=f_mark, fill=WHITE)

    # One-line pitch under the wordmark, in the meme's own voice.
    d.text((80, 1112), "my AI agent got paid to make this",
           font=font(34), fill=FAINT_GREY)

    img.save(OUT, "PNG")
    print(f"wrote {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
