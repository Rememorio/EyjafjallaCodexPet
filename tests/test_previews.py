"""Previews must show the installed pixels and actual state timing."""

from pathlib import Path
import sys
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from render_previews import ANIMATIONS, LOOK_DURATION, LOOK_DEMO_ORIGIN, LOOK_DEMO_SIZE, cell, transition_frames


class PreviewTests(unittest.TestCase):
    def test_jump_transition_returns_to_idle_after_three_cycles(self):
        with Image.open(ROOT / "pets/eyjafjalla/spritesheet.webp") as sheet:
            frames, durations = transition_frames(sheet, "jumping")
            expected = [(0, col) for col in range(6)] + [(4, col) for col in range(5)] * 3 + [(0, col) for col in range(6)]
            self.assertEqual(len(frames), 27)
            self.assertEqual(durations, ANIMATIONS["idle"][1] + [140, 140, 140, 140, 280] * 3 + ANIMATIONS["idle"][1])
            for frame, (row, col) in zip(frames, expected):
                self.assertEqual(frame.tobytes(), cell(sheet, row, col).tobytes())

    def test_previews_preserve_rgba_and_state_timing(self):
        with Image.open(ROOT / "pets/eyjafjalla/spritesheet.webp") as sheet:
            for name, (row, durations) in ANIMATIONS.items():
                with self.subTest(name=name), Image.open(ROOT / f"docs/previews/{name}.png") as preview:
                    self.assertEqual(preview.size, (192, 208))
                    self.assertEqual(preview.n_frames, len(durations))
                    for index, duration in enumerate(durations):
                        preview.seek(index)
                        self.assertEqual(preview.info["duration"], duration)
                        self.assertEqual(preview.convert("RGBA").tobytes(), cell(sheet, row, index).tobytes())

    def test_look_demo_keeps_all_sixteen_source_poses(self):
        with Image.open(ROOT / "pets/eyjafjalla/spritesheet.webp") as sheet, Image.open(ROOT / "docs/previews/look-loop.png") as preview:
            self.assertEqual(preview.n_frames, 16)
            for index in range(16):
                preview.seek(index)
                self.assertEqual(preview.info["duration"], LOOK_DURATION)
                self.assertEqual(preview.convert("RGBA").tobytes(), cell(sheet, 9 + index // 8, index % 8).tobytes())

    def test_direction_marker_never_overlaps_or_changes_the_pet(self):
        x, y = LOOK_DEMO_ORIGIN
        with Image.open(ROOT / "pets/eyjafjalla/spritesheet.webp") as sheet, Image.open(ROOT / "docs/previews/look-demo.png") as preview:
            self.assertEqual(preview.size, LOOK_DEMO_SIZE)
            self.assertEqual(preview.n_frames, 16)
            for index in range(16):
                preview.seek(index)
                self.assertEqual(preview.info["duration"], LOOK_DURATION)
                source = cell(sheet, 9 + index // 8, index % 8).convert("RGBA")
                shown = preview.convert("RGBA").crop((x, y, x + 192, y + 208))
                self.assertEqual(shown.tobytes(), source.tobytes())


if __name__ == "__main__":
    unittest.main()
