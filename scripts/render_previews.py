#!/usr/bin/env python3
"""Export lossless RGBA previews from the exact installable atlas frames."""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CELL = (192, 208)
# Desktop state timings. Idle uses the slower ambient breathing cadence.
ANIMATIONS = {
    "idle": (0, [1680, 660, 660, 840, 840, 1920]),
    "running-right": (1, [120] * 7 + [220]),
    "running-left": (2, [120] * 7 + [220]),
    "waving": (3, [140] * 3 + [280]),
    "jumping": (4, [140] * 4 + [280]),
    "failed": (5, [140] * 7 + [240]),
    "waiting": (6, [150] * 5 + [260]),
    "running": (7, [120] * 5 + [220]),
    "review": (8, [150] * 5 + [280]),
}


def cell(sheet, row, column):
    x, y = column * CELL[0], row * CELL[1]
    return sheet.crop((x, y, x + CELL[0], y + CELL[1]))


def export_animation(frames, durations, path):
    frames[0].save(
        path, format="PNG", save_all=True, append_images=frames[1:],
        duration=durations, loop=0, disposal=0, blend=0,
    )


def render():
    output = ROOT / "docs" / "previews"
    output.mkdir(parents=True, exist_ok=True)
    with Image.open(ROOT / "pets" / "eyjafjalla" / "spritesheet.webp") as sheet:
        for name, (row, durations) in ANIMATIONS.items():
            export_animation(
                [cell(sheet, row, col) for col in range(len(durations))],
                durations, output / f"{name}.png",
            )
        # Cursor-controlled poses have no autoplay timing. This loop simply
        # demonstrates the sixteen directions at evenly spaced intervals.
        export_animation(
            [cell(sheet, 9 + index // 8, index % 8) for index in range(16)],
            [180] * 16, output / "look-loop.png",
        )
    print("Rendered 10 lossless APNG previews at the original 192 × 208 resolution")


if __name__ == "__main__":
    render()
