"""Gaze must preserve body pixels and head scale, even with a stable outer box."""

from pathlib import Path
import sys
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from palette import frame
from validate import validate_gaze_geometry


class GazeTests(unittest.TestCase):
    def setUp(self):
        self.sheet = Image.open(ROOT / "pets/eyjafjalla/spritesheet.webp").convert("RGBA")

    def replace(self, tile):
        self.sheet.paste(tile, (0, 9 * 208))

    def test_all_directions_share_body_and_neutral_scale(self):
        validate_gaze_geometry(self.sheet)

    def test_body_change_inside_unchanged_silhouette_is_rejected(self):
        tile = frame(self.sheet, 9, 0)
        bounds = tile.getchannel("A").getbbox()
        r, g, b, a = tile.getpixel((96, 140))
        self.assertGreater(a, 0)
        tile.putpixel((96, 140), (max(0, r - 12), g, b, a))
        self.assertEqual(bounds, tile.getchannel("A").getbbox())
        self.replace(tile)
        with self.assertRaisesRegex(AssertionError, "Gaze body mismatch: 9/0"):
            validate_gaze_geometry(self.sheet)

    def test_narrower_head_with_same_total_height_is_rejected(self):
        tile = frame(self.sheet, 9, 0)
        bounds = tile.getchannel("A").getbbox()
        head = tile.crop((0, 0, 192, 96)).resize((164, 96), Image.Resampling.LANCZOS)
        tile.paste((0, 0, 0, 0), (0, 0, 192, 96))
        tile.paste(head, (14, 0))
        self.assertEqual(bounds[1:], tile.getchannel("A").getbbox()[1:])
        self.replace(tile)
        with self.assertRaisesRegex(AssertionError, "Gaze head width drift: 9/0"):
            validate_gaze_geometry(self.sheet)

    def test_head_area_change_inside_unchanged_box_is_rejected(self):
        tile = frame(self.sheet, 9, 0)
        bounds = tile.getchannel("A").getbbox()
        tile.paste((0, 0, 0, 0), (80, 70, 115, 90))
        self.assertEqual(bounds, tile.getchannel("A").getbbox())
        self.replace(tile)
        with self.assertRaisesRegex(AssertionError, "Gaze head area drift: 9/0"):
            validate_gaze_geometry(self.sheet)

    def test_head_vertical_shift_is_rejected(self):
        tile = frame(self.sheet, 9, 0)
        head = tile.crop((0, 0, 192, 96))
        tile.paste((0, 0, 0, 0), (0, 0, 192, 96))
        tile.paste(head.crop((0, 3, 192, 96)), (0, 0))
        self.replace(tile)
        with self.assertRaisesRegex(AssertionError, "Gaze head anchor drift: 9/0"):
            validate_gaze_geometry(self.sheet)


if __name__ == "__main__":
    unittest.main()
