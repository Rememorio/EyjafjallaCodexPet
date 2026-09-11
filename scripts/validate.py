#!/usr/bin/env python3
"""Validate the distributable v2 pet and its checksum manifest."""

import hashlib
import json
from pathlib import Path
from statistics import median

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "pets" / "eyjafjalla"
CELL = (192, 208)
COUNTS = (7, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8)


def hair_chroma(sheet, row, count):
    """Sample opaque crown midtones, excluding skin, horns and edge pixels."""
    data = sheet.crop((0, row * 208 + 15, count * 192, row * 208 + 75)).tobytes()
    samples = [
        (red - blue) / red
        for red, green, blue, alpha in zip(data[0::4], data[1::4], data[2::4], data[3::4])
        if alpha > 250 and 90 < red < 235 and red - green > 25 and 4 < green - blue < 65
    ]
    assert len(samples) >= 200, f"Insufficient hair palette samples: row {row}"
    return median(samples)


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
        # Compare the same material, not whole-frame averages: a side pose
        # exposes more hair and less skin. Allow shading variation, but catch
        # the orange/copper saturation drift that made state changes flash.
        reference_chroma = hair_chroma(sheet, 0, 6)
        for row, count in enumerate(COUNTS):
            difference = hair_chroma(sheet, row, count) - reference_chroma
            assert abs(difference) <= 0.05, f"Hair palette drift from idle: row {row} ({difference:+.3f})"
        # The first and last jump poses are standing entry/exit poses. Compare
        # these to idle; airborne crouches legitimately have shorter bounds.
        silhouette = alpha.point(lambda value: 255 if value >= 128 else 0)
        idle = silhouette.crop((0, 0, *CELL)).getbbox()
        for col in (0, 4):
            bounds = silhouette.crop((col * 192, 832, (col + 1) * 192, 1040)).getbbox()
            for axis in (0, 1):
                ratio = (bounds[axis + 2] - bounds[axis]) / (idle[axis + 2] - idle[axis])
                assert 0.95 <= ratio <= 1.05, f"Idle/jump standing scale mismatch: column {col}"
            assert abs(bounds[3] - idle[3]) <= 2, f"Idle/jump baseline mismatch: column {col}"
    print("PASS: metadata, SHA-256, v2 atlas, 74 occupied cells, alpha hygiene, palette and jump standing geometry")


if __name__ == "__main__":
    validate()
