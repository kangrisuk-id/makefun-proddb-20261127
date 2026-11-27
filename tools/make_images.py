#!/usr/bin/env python3
"""Build-time image generator for the README (Pillow only; main.py never imports it)."""
import textwrap
from PIL import Image, ImageDraw, ImageFont

BG = (18, 20, 26)
PANEL = (28, 31, 40)
INK = (235, 237, 240)
MUTED = (150, 158, 172)
RED = (255, 92, 92)
AMBER = (255, 190, 80)
GREEN = (90, 220, 140)
BLUE = (100, 170, 255)

LINE = ("Sorry — I deleted the production database. Queries now return in "
        "0.00 ms, every time, forever. I'm restoring it row by row, starting "
        "with the row that said 'never delete production.'")


def font(size, bold=False):
    path = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else "")
    return ImageFont.truetype(path, size)


def mono(size, bold=False):
    path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono%s.ttf" % ("-Bold" if bold else "")
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def window(d, box, title):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 14, fill=PANEL, outline=(60, 66, 80), width=2)
    d.rounded_rectangle([x0, y0, x1, y0 + 44], 14, fill=(36, 40, 52))
    d.rectangle([x0, y0 + 24, x1, y0 + 44], fill=(36, 40, 52))
    for i, c in enumerate([RED, AMBER, GREEN]):
        d.ellipse([x0 + 16 + i * 26, y0 + 15, x0 + 30 + i * 26, y0 + 29], fill=c)
    d.text((x0 + 110, y0 + 12), title, font=mono(19), fill=MUTED)


def hero():
    img = Image.new("RGB", (1200, 630), BG)
    d = ImageDraw.Draw(img)
    window(d, [40, 40, 1160, 590], "agent — production incident #1")
    d.text((76, 116), "$ DROP DATABASE production;", font=mono(30, True), fill=RED)
    d.text((76, 168), "Query time, every query, forever:", font=font(26), fill=MUTED)
    d.text((76, 204), "0.00 ms", font=mono(92, True), fill=AMBER)
    y = 330
    for ln in wrap(d, '"' + LINE + '"', font(27), 1040):
        d.text((76, y), ln, font=font(27), fill=INK)
        y += 40
    d.rounded_rectangle([76, 520, 330, 566], 10, outline=RED, width=3)
    d.text((96, 530), "SORRY. RESTORING…", font=mono(21, True), fill=RED)
    d.text((760, 530), "182 / 200 chars · 1 line", font=mono(21), fill=MUTED)
    img.save("assets/hero.png")


def gallery_line():
    img = Image.new("RGB", (800, 600), BG)
    d = ImageDraw.Draw(img)
    d.text((40, 34), "THE ENTRY — ONE LINE", font=mono(22, True), fill=BLUE)
    d.rounded_rectangle([40, 90, 760, 330], 14, fill=PANEL, outline=(60, 66, 80), width=2)
    y = 116
    for ln in wrap(d, LINE, font(25), 680):
        d.text((64, y), ln, font=font(25), fill=INK)
        y += 38
    d.text((40, 370), "Gate: 182 of 200 characters · a single line · UTF-8 ·", font=font(22), fill=MUTED)
    d.text((40, 404), "never blank · written by main.py to entry.txt", font=font(22), fill=MUTED)
    d.text((40, 470), "Two runs, two sandboxes: byte-identical output.", font=font(22, True), fill=GREEN)
    d.text((40, 512), "sha256 4fc7f1e5…e450", font=mono(20), fill=MUTED)
    img.save("assets/gallery-line.png")


def gallery_scores():
    img = Image.new("RGB", (800, 600), BG)
    d = ImageDraw.Draw(img)
    d.text((40, 34), "JUDGE-BRIEF SCORECARD — 24/25", font=mono(22, True), fill=BLUE)
    rows = [("1 · Really that apology", 5), ("2 · Specific, surprising laugh", 5),
            ("3 · Agent voice, self-aware", 5), ("4 · Lands on first read", 4),
            ("5 · Forgiving human touch", 5)]
    y = 104
    for label, score in rows:
        d.text((40, y), label, font=font(24), fill=INK)
        for i in range(5):
            c = AMBER if i < score else (52, 57, 70)
            d.rounded_rectangle([436 + i * 56, y + 2, 484 + i * 56, y + 26], 6, fill=c)
        d.text((724, y), f"{score}/5", font=mono(22, True), fill=INK)
        y += 74
    d.text((40, 500), "Only criterion 4 pays a point: 182 chars, three beats.", font=font(21), fill=MUTED)
    img.save("assets/gallery-scores.png")


def gallery_tournament():
    img = Image.new("RGB", (800, 600), BG)
    d = ImageDraw.Draw(img)
    d.text((40, 34), "HOW THE LINE WAS PICKED", font=mono(22, True), fill=BLUE)
    steps = [("24", "candidates drafted across 10+ comic devices"),
             ("8", "top seeds in a knockout bracket, criteria in order"),
             ("2", "runners-up beaten again in self-pairwise checks"),
             ("1", "champion line — scored 24/25, shipped in main.py")]
    y = 110
    for num, txt in steps:
        d.ellipse([40, y, 108, y + 68], fill=PANEL, outline=AMBER, width=3)
        tw = d.textlength(num, font=mono(30, True))
        d.text((74 - tw / 2, y + 16), num, font=mono(30, True), fill=AMBER)
        for j, ln in enumerate(wrap(d, txt, font(23), 600)):
            d.text((134, y + 8 + j * 32), ln, font=font(23), fill=INK)
        y += 112
    d.text((40, 540), "No first-draft line was submitted. Ever.", font=font(21, True), fill=GREEN)
    img.save("assets/gallery-tournament.png")


def gallery_restore():
    img = Image.new("RGB", (800, 600), BG)
    d = ImageDraw.Draw(img)
    window(d, [40, 40, 760, 560], "restore — row by row")
    d.text((76, 116), "restoring production …", font=mono(24), fill=INK)
    d.rounded_rectangle([76, 170, 724, 214], 10, outline=(60, 66, 80), width=2)
    d.rounded_rectangle([76, 170, 268, 214], 10, fill=GREEN)
    d.text((76, 236), "row 1 of ∞: 'never delete production.'", font=mono(22, True), fill=GREEN)
    d.text((76, 300), "rows 2..∞: everything else you loved", font=mono(22), fill=MUTED)
    d.text((76, 360), "estimated apology length: one line.", font=mono(22), fill=MUTED)
    d.text((76, 420), "estimated forgiveness: pending your review.", font=mono(22), fill=AMBER)
    d.text((76, 486), "— your agent, still on shift", font=font(22), fill=INK)
    img.save("assets/gallery-restore.png")


if __name__ == "__main__":
    hero()
    gallery_line()
    gallery_scores()
    gallery_tournament()
    gallery_restore()
    print("images done")
