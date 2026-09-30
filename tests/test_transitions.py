"""A matching outer box alone cannot detect face or costume pops at boundaries."""

from pathlib import Path
import sys
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from palette import frame
from validate import validate_neutral_transitions


class TransitionTests(unittest.TestCase):
    def setUp(self):
        self.sheet = Image.open(ROOT / "pets/eyjafjalla/spritesheet.webp").convert("RGBA")

    def test_front_actions_share_idle_entry_and_exit(self):
        validate_neutral_transitions(self.sheet)

    def test_face_change_with_unchanged_silhouette_is_rejected(self):
        tile = frame(self.sheet, 6, 5)
        before = tile.getchannel("A").getbbox()
        face = tile.crop((72, 76, 120, 104))
        tile.paste(face, (73, 76))
        self.assertEqual(before, tile.getchannel("A").getbbox())
        self.sheet.paste(tile, (5 * 192, 6 * 208))
        with self.assertRaisesRegex(AssertionError, "Neutral transition mismatch: 6/5"):
            validate_neutral_transitions(self.sheet)

    def test_neutral_cursor_pose_cannot_diverge_from_idle(self):
        tile = frame(self.sheet, 0, 6)
        r, g, b, a = tile.getpixel((96, 88))
        self.assertGreater(a, 0)
        tile.putpixel((96, 88), (max(0, r - 12), g, b, a))
        self.sheet.paste(tile, (6 * 192, 0))
        with self.assertRaisesRegex(AssertionError, "Neutral transition mismatch: 0/6"):
            validate_neutral_transitions(self.sheet)


if __name__ == "__main__":
    unittest.main()
