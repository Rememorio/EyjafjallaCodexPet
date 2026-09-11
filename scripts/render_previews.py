#!/usr/bin/env python3
"""Export lossless RGBA previews from the exact installable atlas frames."""

import argparse
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


def transition_frames(sheet, name):
    """Show state entry, three desktop cycles, then return to ambient idle."""
    row, durations = ANIMATIONS[name]
    idle_row, idle_durations = ANIMATIONS["idle"]
    idle_frames = [cell(sheet, idle_row, col) for col in range(len(idle_durations))]
    state_frames = [cell(sheet, row, col) for col in range(len(durations))]
    return (
        idle_frames + state_frames * 3 + idle_frames,
        idle_durations + durations * 3 + idle_durations,
    )


def render(transition_dir=None):
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
        if transition_dir is not None:
            transition_dir.mkdir(parents=True, exist_ok=True)
            for name in ANIMATIONS:
                if name != "idle":
                    frames, durations = transition_frames(sheet, name)
                    export_animation(frames, durations, transition_dir / f"idle-{name}-idle.png")
    print("Rendered 10 lossless APNG previews at the original 192 × 208 resolution")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transition-dir", type=Path, help="Also export state transitions for visual review")
    render(parser.parse_args().transition_dir)
