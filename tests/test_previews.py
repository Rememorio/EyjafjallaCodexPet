"""Previews must show the installed pixels and actual state timing."""

from pathlib import Path
import sys
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from render_previews import ANIMATIONS, cell


class PreviewTests(unittest.TestCase):
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
                self.assertEqual(preview.convert("RGBA").tobytes(), cell(sheet, 9 + index // 8, index % 8).tobytes())


if __name__ == "__main__":
    unittest.main()
