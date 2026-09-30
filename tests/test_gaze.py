"""Gaze must preserve body pixels and head scale, even with a stable outer box."""

from pathlib import Path
import sys
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from palette import frame
from validate import validate_gaze_geometry, validate_gaze_face_continuity


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
        # Start at the neutral anchor so a three-pixel mutation cannot cancel
        # a permitted one-pixel offset in a particular illustrated direction.
        tile = frame(self.sheet, 0, 6)
        head = tile.crop((0, 0, 192, 96))
        tile.paste((0, 0, 0, 0), (0, 0, 192, 96))
        tile.paste(head.crop((0, 3, 192, 96)), (0, 0))
        self.replace(tile)
        with self.assertRaisesRegex(AssertionError, "Gaze head anchor drift: 9/0"):
            validate_gaze_geometry(self.sheet)

    def test_face_shift_inside_unchanged_head_is_rejected(self):
        tile = frame(self.sheet, 9, 0)
        alpha = tile.getchannel("A").tobytes()
        original = tile.copy()
        # Move only facial color content, preserving every silhouette pixel.
        for y in range(62, 112):
            for x in range(54, 138):
                rgb = original.getpixel((x - 12, y))[:3]
                tile.putpixel((x, y), rgb + (original.getpixel((x, y))[3],))
        self.assertEqual(alpha, tile.getchannel("A").tobytes())
        self.replace(tile)
        with self.assertRaisesRegex(AssertionError, "Gaze face anchor jump"):
            validate_gaze_face_continuity(self.sheet)

    def test_face_area_jump_inside_unchanged_head_is_rejected(self):
        # A crop is narrower than the head mask, leaving head geometry intact.
        tile = frame(self.sheet, 10, 7)
        alpha = tile.getchannel("A").tobytes()
        for y in range(62, 112):
            for x in range(76, 116):
                r, g, b, a = tile.getpixel((x, y))
                if r > 235 and g > 215 and b > 185:
                    tile.putpixel((x, y), (204, 155, 139, a))
        self.assertEqual(alpha, tile.getchannel("A").tobytes())
        self.sheet.paste(tile, (7 * 192, 10 * 208))
        with self.assertRaisesRegex(AssertionError, "Gaze face (area|anchor) jump|Missing gaze face"):
            validate_gaze_face_continuity(self.sheet)

    def test_gradual_face_drift_is_rejected_at_closing_loop_boundary(self):
        original = frame(self.sheet, 9, 0)
        for index in range(16):
            tile = original.copy()
            for y in range(62, 112):
                for x in range(54, 138):
                    rgb = original.getpixel((x - index // 2, y))[:3]
                    tile.putpixel((x, y), rgb + (original.getpixel((x, y))[3],))
            self.sheet.paste(tile, (index % 8 * 192, (9 + index // 8) * 208))
        with self.assertRaisesRegex(AssertionError, "Gaze face anchor jump: 337.5 -> 0"):
            validate_gaze_face_continuity(self.sheet)


if __name__ == "__main__":
    unittest.main()
