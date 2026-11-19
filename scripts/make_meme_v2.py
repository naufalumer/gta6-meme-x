#!/usr/bin/env python3
"""GTA 6 meme v2 for make.fun gta6-meme-x-01.

Rebuild after the user rejected v1 ("gada unsur gta nya"): v1 was a text-only
WASTED image with a drawn ghost. v2 is built on REAL GTA VI art: the 9
round-3 cover-art panels (Vice City sunset art in the official cover style),
arranged as a busy 3x3 grid like the official GTA VI cover, with an original
caption in Pricedown (GTA's own font) and the official make.fun ghost mark
from the press kit in the bottom-right cell (the R* logo spot on the real cover).

Layout (1024x1024, square so the judge sees it at 480x480):
  top band    0-96    black, Pricedown caption
  grid        96-928  3x3 cells 338x274, 5px gutters
  bottom band 928-1024 black, Pricedown caption
Grid: heli | couple | bike / car | city | gunman / gator | boat | ghost cell.
Landscape panels are cover-cropped; portrait panels (heli, bike) are
contain-fitted on black so no art is cut. Ghost cell: official mark-1024.png
badge + "make.fun" in Pricedown underneath.

Run: python3 make_meme_v2.py  -> writes meme.png next to this script's dir
(parent local/) and a 480x480 judge-view preview to /tmp/meme-v2-480.png.
Stdlib + Pillow only. No network, no wall clock.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.dirname(HERE)  # local/ (repo mirror)
PANELS = "/home/hatch/workspace/make-fun/gta6-cover-art-01/app/panels"
FONT = "/home/hatch/workspace/make-fun/gta6-cover-art-01/app/fonts/Pricedown.otf"
GHOST = "/tmp/mark-1024.png"

W = H = 1024
TOP_H, BOT_H = 96, 96
GRID_Y0, GRID_Y1 = TOP_H, H - BOT_H
CELL_W, CELL_H, GUT = 338, 274, 5
TOP_TEXT = "ME: JUST 30 MINUTES OF GTA VI"
BOT_TEXT = "ME AT 4AM: STILL IN VICE CITY"

GRID = [
    ["heli", "couple", "bike"],
    ["car", "city", "gunman"],
    ["gator", "boat", None],  # None = ghost cell
]


def fit_font(draw, text, start, max_w):
    size = start
    while size > 20:
        f = ImageFont.truetype(FONT, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(FONT, 20)


def cover(im, w, h):
    """Center-crop image to w x h (cover)."""
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    im = im.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def contain(im, w, h):
    """Scale image to fit inside w x h, centred on black."""
    sw, sh = im.size
    scale = min(w / sw, h / sh)
    im = im.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    canvas = Image.new("RGB", (w, h), (0, 0, 0))
    canvas.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return canvas


def ghost_cell(w, h):
    cell = Image.new("RGB", (w, h), (0, 0, 0))
    mark = Image.open(GHOST).convert("RGBA")
    badge = 168
    mark = mark.resize((badge, badge), Image.LANCZOS)
    cell.paste(mark, ((w - badge) // 2, 12), mark)
    d = ImageDraw.Draw(cell)
    f = fit_font(d, "make.fun", 56, w - 16)
    tw = d.textlength("make.fun", font=f)
    d.text(((w - tw) / 2, 12 + badge + 6), "make.fun", font=f,
           fill=(255, 255, 255),
           stroke_width=3, stroke_fill=(0, 0, 0))
    return cell


def main():
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    for r, row in enumerate(GRID):
        for c, name in enumerate(row):
            x = c * (CELL_W + GUT)
            y = GRID_Y0 + r * (CELL_H + GUT)
            if name is None:
                cell = ghost_cell(CELL_W, CELL_H)
            else:
                im = Image.open(os.path.join(PANELS, name + ".png")).convert("RGB")
                if im.width >= im.height:
                    cell = cover(im, CELL_W, CELL_H)
                else:
                    cell = contain(im, CELL_W, CELL_H)
            canvas.paste(cell, (x, y))

    d = ImageDraw.Draw(canvas)
    f_top = fit_font(d, TOP_TEXT, 76, W - 44)
    tw = d.textlength(TOP_TEXT, font=f_top)
    d.text(((W - tw) / 2, 14), TOP_TEXT, font=f_top, fill=(255, 255, 255),
           stroke_width=4, stroke_fill=(0, 0, 0))
    f_bot = fit_font(d, BOT_TEXT, 76, W - 44)
    tw = d.textlength(BOT_TEXT, font=f_bot)
    d.text(((W - tw) / 2, H - BOT_H + 14), BOT_TEXT, font=f_bot,
           fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))

    out = os.path.join(BUILD, "meme.png")
    canvas.save(out, "PNG")
    print("wrote", out, canvas.size, os.path.getsize(out), "bytes")
    preview = canvas.resize((480, 480), Image.LANCZOS)
    preview.save("/tmp/meme-v2-480.png", "PNG")
    print("judge preview /tmp/meme-v2-480.png")


if __name__ == "__main__":
    main()
