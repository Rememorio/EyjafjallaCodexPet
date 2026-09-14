#!/usr/bin/env python3
"""Measure and calibrate this pet's hair without changing sprite geometry."""

import argparse
from collections import Counter
import json
from pathlib import Path
from statistics import median

from PIL import Image, ImageFilter

COUNTS = (7, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8)


def frame(sheet, row, col):
    return sheet.crop((col * 192, row * 208, (col + 1) * 192, (row + 1) * 208))


def dominant(pixels):
    assert len(pixels) >= 30, "Insufficient material samples"
    bins = Counter(tuple(c // 8 for c in rgb) for rgb in pixels)
    key = bins.most_common(1)[0][0]
    selected = [rgb for rgb in pixels if tuple(c // 8 for c in rgb) == key]
    return tuple(median(rgb[i] for rgb in selected) for i in range(3))


def lightness(rgb):
    linear = [c / 255 / 12.92 if c / 255 <= .04045 else ((c / 255 + .055) / 1.055) ** 2.4 for c in rgb]
    y = sum(c * w for c, w in zip(linear, (.2126, .7152, .0722)))
    return 116 * y ** (1 / 3) - 16 if y > .008856 else 903.3 * y


def saturation(rgb):
    return (max(rgb) - min(rgb)) / max(rgb)


def sample(cell, row):
    x0, y0, x1, y1 = cell.getbbox()
    xl, xr = (.59, .81) if row == 1 else ((.19, .41) if row == 2 else (.34, .68))
    crown, shadow, skin = [], [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = cell.getpixel((x, y))
            if a < 250:
                continue
            xn, yn = (x - x0) / (x1 - x0), (y - y0) / (y1 - y0)
            hair = r > g + 25 and 0 < g - b < 30 and 65 < b and r < 235
            if hair and xl <= xn < xr and .12 <= yn < .29:
                crown.append((r, g, b))
            if hair and (xn < .28 or xn > .72) and .36 < yn < .70 and r < 190:
                shadow.append((r, g, b))
            if .25 < xn < .75 and .28 < yn < .55 and r > 225 and g > 195 and b > 160 and r - g > 5 and r - b > 15 and 2 < g - b < 35:
                skin.append((r, g, b))
    return {"crown": dominant(crown), "shadow": dominant(shadow) if row not in (1, 2) else None, "skin": dominant(skin)}


def median_color(colors):
    return tuple(median(rgb[i] for rgb in colors) for i in range(3))


def palette_report(sheet):
    rows = [[sample(frame(sheet, row, col), row) for col in range(count)] for row, count in enumerate(COUNTS)]
    reference = median_color([p["crown"] for p in rows[0][:6]])
    return {"reference": reference, "frames": [
        {"row": row, "column": col, **p,
         "lightness_delta": lightness(p["crown"]) - lightness(reference),
         "saturation_delta": saturation(p["crown"]) - saturation(reference)}
        for row, samples in enumerate(rows) for col, p in enumerate(samples)
    ]}


def validate_palette(sheet):
    report = palette_report(sheet)
    for p in report["frames"]:
        location = f"{p['row']}/{p['column']}"
        assert abs(p["lightness_delta"]) <= 2, f"Hair lightness drift: {location} ({p['lightness_delta']:+.2f} L*)"
        assert abs(p["saturation_delta"]) <= .025, f"Hair saturation drift: {location} ({p['saturation_delta']:+.3f})"
    return report


def ramp(value, low, high):
    return max(0, min(1, (value - low) / (high - low)))


def calibrate_cell(cell, row, source_crown, source_shadow, target_crown, target_shadow):
    """Blend two material anchors; keep alpha, facial features and clothing intact."""
    out = cell.copy()
    x0, y0, x1, y1 = cell.getbbox()
    # Protect saturated iris pixels and their immediate antialiasing neighbors.
    eyes = Image.new("L", cell.size)
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = cell.getpixel((x, y))
            xn, yn = (x - x0) / (x1 - x0), (y - y0) / (y1 - y0)
            if a and .25 < yn < .56 and r > 1.9 * max(g, b) and r > 80:
                eyes.putpixel((x, y), 255)
    eyes = eyes.filter(ImageFilter.MaxFilter(9))
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = cell.getpixel((x, y))
            xn, yn = (x - x0) / (x1 - x0), (y - y0) / (y1 - y0)
            if not a or eyes.getpixel((x, y)) or yn > .83 or (.60 < yn and .30 < xn < .70):
                continue
            sat = (r - min(g, b)) / max(1, r)
            weight = ramp(sat, .23, .28) * (1 - ramp(sat, .55, .65))
            weight *= ramp(r, 90, 130) * (1 - ramp(r, 230, 247))
            weight *= ramp(g - b, -3, 1) * (1 - ramp(g - b, 25, 40))
            if weight <= 0 or r <= g:
                continue
            tone = ramp(r, source_shadow[0], source_crown[0])
            delta = [(ts - ss) * (1 - tone) + (tc - sc) * tone for ts, ss, tc, sc in zip(target_shadow, source_shadow, target_crown, source_crown)]
            out.putpixel((x, y), tuple(max(0, min(255, round(c + weight * d))) for c, d in zip((r, g, b), delta)) + (a,))
    assert out.getchannel("A").tobytes() == cell.getchannel("A").tobytes()
    return out


def calibrate(sheet, reference):
    target = [sample(frame(reference, 0, col), 0) for col in range(6)]
    tc = median_color([p["crown"] for p in target])
    ts = median_color([p["shadow"] for p in target])
    out = sheet.copy()
    for row, count in enumerate(COUNTS):
        cells = [frame(sheet, row, col) for col in range(count)]
        samples = [sample(cell, row) for cell in cells]
        # Side-pose shadow exposure differs; retain its existing shadow palette.
        shadow = median_color([p["shadow"] for p in samples]) if row not in (1, 2) else ts
        for col, (cell, p) in enumerate(zip(cells, samples)):
            out.paste(calibrate_cell(cell, row, p["crown"], shadow, tc, ts), (col * 192, row * 208))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("atlas", type=Path)
    parser.add_argument("--reference", type=Path, help="Approved atlas whose idle defines the target palette")
    parser.add_argument("--output", type=Path, help="Write a calibrated atlas; requires --reference")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    sheet = Image.open(args.atlas).convert("RGBA")
    assert sheet.size == (1536, 2288), "Expected v2 atlas"
    if args.output:
        if not args.reference:
            parser.error("--output requires --reference")
        reference = Image.open(args.reference).convert("RGBA")
        assert reference.size == sheet.size, "Reference must be a v2 atlas"
        sheet = calibrate(sheet, reference)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(args.output, lossless=True, exact=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(palette_report(sheet), indent=2) + "\n")


if __name__ == "__main__":
    main()
