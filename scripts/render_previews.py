#!/usr/bin/env python3
"""Export lossless RGBA previews from the exact installable atlas frames."""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

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


def export_contact_sheets(sheet):
    """Keep the static atlas and cursor-direction documentation current too."""
    counts = (7, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8)
    names = [*ANIMATIONS, "look 000-157.5", "look 180-337.5"]
    overview = Image.new("RGB", (768, 1386), "#111111")
    draw = ImageDraw.Draw(overview)
    for row, (name, count) in enumerate(zip(names, counts)):
        top = row * 126
        draw.text((6, top + 5), f"row {row}: {name}", fill="white")
        for col in range(8):
            x, y = col * 96, top + 22
            for sy in range(0, 104, 16):
                for sx in range(0, 96, 16):
                    color = "#e7e7e7" if (sx // 16 + sy // 16) % 2 else "#fafafa"
                    draw.rectangle((x + sx, y + sy, x + min(sx + 15, 95), y + min(sy + 15, 103)), fill=color)
            sprite = cell(sheet, row, col).resize((96, 104), Image.Resampling.LANCZOS)
            overview.paste(sprite, (x, y), sprite)
            draw.rectangle((x, y, x + 95, y + 103), outline="#59a879" if col < count else "#bd5663")
            draw.text((x + 3, y + 3), str(col), fill="black")
    overview.save(ROOT / "docs/spritesheet-preview.png")

    directions = Image.new("RGB", (1536, 702), "white")
    draw = ImageDraw.Draw(directions)
    poses = [(0, 6, 0, 0, "neutral")]
    poses += [(9 + i // 8, i % 8, i % 8, 1 + i // 8, f"{i * 22.5:g} degrees") for i in range(16)]
    for row, col, x, y, label in poses:
        x, y = x * 192, y * 234
        draw.text((x + 6, y + 7), label, fill="black")
        draw.rectangle((x, y + 26, x + 191, y + 233), fill="#f1f1f1")
        sprite = cell(sheet, row, col)
        directions.paste(sprite, (x, y + 26), sprite)
    directions.save(ROOT / "docs/look-directions.png")


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
        export_contact_sheets(sheet)
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
