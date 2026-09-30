#!/usr/bin/env python3
"""Validate the distributable v2 pet and its checksum manifest."""

import hashlib
import json
from pathlib import Path
from PIL import Image
from palette import validate_palette

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "pets" / "eyjafjalla"
CELL = (192, 208)
COUNTS = (7, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8)


def validate_idle_eyes(sheet):
    """Long ambient frames must retain the character's open red irises."""
    counts = []
    for col in range(6):
        cell = sheet.crop((col * 192, 0, (col + 1) * 192, 208))
        left, top, right, bottom = cell.getbbox()
        face = cell.crop((round(left + (right - left) * .25), round(top + (bottom - top) * .30),
                          round(left + (right - left) * .75), round(top + (bottom - top) * .53)))
        counts.append(sum(a > 250 and r > 80 and r > 1.9 * max(g, b) for r, g, b, a in face.getdata()))
    assert min(counts) >= max(20, counts[0] * .65), f"Closed or narrowed eyes in slow idle frames: {counts}"


def validate_neutral_transitions(sheet):
    """Front-facing actions must enter and leave through the shared idle pose."""
    neutral = sheet.crop((0, 0, *CELL)).tobytes()
    for row, columns in [(0, (5, 6))] + [
        (row, (0, COUNTS[row] - 1)) for row in range(3, 9)
    ]:
        for col in columns:
            tile = sheet.crop((col * 192, row * 208, (col + 1) * 192, (row + 1) * 208))
            assert tile.tobytes() == neutral, f"Neutral transition mismatch: {row}/{col}"


def validate_gaze_geometry(sheet):
    """Looking changes the head, never the standing body or character scale."""
    neutral = sheet.crop((6 * 192, 0, 7 * 192, 208))
    body_box = (0, 112, 192, 208)
    body = neutral.crop(body_box).tobytes()

    def head_metrics(tile):
        # Exclude the neck blend and long hair. Opaque geometry avoids counting
        # faint antialiasing pixels as a change in size.
        mask = tile.getchannel("A").crop((0, 0, 192, 96)).point(lambda a: 255 if a >= 128 else 0)
        bounds = mask.getbbox()
        assert bounds, "Missing gaze head"
        left, top, right, _ = bounds
        return right - left, top, (left + right) / 2, sum(mask.histogram()[1:])

    width, top, center, area = head_metrics(neutral)
    for row in (9, 10):
        for col in range(8):
            tile = sheet.crop((col * 192, row * 208, (col + 1) * 192, (row + 1) * 208))
            location = f"{row}/{col}"
            assert tile.crop(body_box).tobytes() == body, f"Gaze body mismatch: {location}"
            w, t, c, a = head_metrics(tile)
            assert abs(w / width - 1) <= .05, f"Gaze head width drift: {location}"
            assert abs(a / area - 1) <= .05, f"Gaze head area drift: {location}"
            assert abs(t - top) <= 2 and abs(c - center) <= 4, f"Gaze head anchor drift: {location}"


def validate():
    metadata = json.loads((BUNDLE / "pet.json").read_text())
    assert metadata["id"] == "eyjafjalla", "Unexpected pet ID"
    assert metadata["spriteVersionNumber"] == 2, "Expected v2"
    assert metadata["spritesheetPath"] == "spritesheet.webp", "Unexpected sprite path"
    assert metadata["displayName"] and metadata["description"], "Missing display metadata"
    manifest = dict(
        (name, digest)
        for digest, name in (
            line.split() for line in (BUNDLE / "checksums.sha256").read_text().splitlines()
        )
    )
    assert set(manifest) == {"pet.json", "spritesheet.webp"}, "Unexpected manifest files"
    for name, expected in manifest.items():
        actual = hashlib.sha256((BUNDLE / name).read_bytes()).hexdigest()
        assert actual == expected, f"Checksum mismatch: {name}"
    with Image.open(BUNDLE / "spritesheet.webp") as sheet:
        assert sheet.format == "WEBP", "Expected WebP"
        assert sheet.mode == "RGBA", "Expected RGBA transparency"
        assert sheet.size == (1536, 2288), "Expected 8 × 11 cells"
        alpha = sheet.getchannel("A")
        for row, count in enumerate(COUNTS):
            for col in range(8):
                box = (col * CELL[0], row * CELL[1], (col + 1) * CELL[0], (row + 1) * CELL[1])
                bounds = alpha.crop(box).getbbox()
                assert bool(bounds) == (col < count), f"Unexpected content at row {row}, column {col}"
                if bounds:
                    assert 0 < bounds[0] < bounds[2] < CELL[0], f"Horizontal clipping: {row}/{col}"
                    assert 0 < bounds[1] < bounds[3] < CELL[1], f"Vertical clipping: {row}/{col}"
        assert alpha.getextrema() == (0, 255), "Expected transparent and opaque pixels"
        rgba = sheet.tobytes()
        assert all(
            rgba[i + 3] or not any(rgba[i:i + 3])
            for i in range(0, len(rgba), 4)
        ), "Nonzero RGB under transparent pixels; export lossless WebP with exact=True"
        # Per-frame material lightness catches darkening that saturation alone
        # misses; row averages would also hide a single flashing frame.
        validate_palette(sheet)
        validate_idle_eyes(sheet)
        validate_neutral_transitions(sheet)
        validate_gaze_geometry(sheet)
    print("PASS: metadata, SHA-256, v2 atlas, 74 occupied cells, alpha hygiene, per-frame palette, open-eye idle, shared neutral transitions and stable gaze geometry")


if __name__ == "__main__":
    validate()
