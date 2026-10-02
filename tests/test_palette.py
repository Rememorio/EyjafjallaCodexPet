"""Catch slow closed-eye holds and single-frame material color regressions."""

from pathlib import Path
import sys
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from palette import calibrate_cell, frame, sample, saturation, validate_palette, validate_reference_color
from validate import validate_idle_eyes


class PaletteTests(unittest.TestCase):
    def setUp(self):
        self.sheet = Image.open(ROOT / "pets/eyjafjalla/spritesheet.webp").convert("RGBA")

    def test_uniform_old_coral_palette_is_rejected_against_original(self):
        with self.assertRaisesRegex(AssertionError, "Original-reference hair"):
            validate_reference_color((198, 126, 116))

    def test_equal_lightness_and_saturation_do_not_hide_wrong_hue(self):
        # Same extrema as the original, but shifted toward red rather than brown.
        with self.assertRaisesRegex(AssertionError, "hue drift"):
            validate_reference_color((204, 152, 139))

    def test_single_dark_hover_frame_is_rejected_even_with_same_saturation(self):
        cell = frame(self.sheet, 4, 0)
        before = sample(cell, 4)["crown"]
        rgb = cell.copy()
        crown = cell.crop((0, 0, 192, 65)).convert("RGB").point(lambda c: round(c * .85))
        rgb.paste(crown, (0, 0))
        rgb.putalpha(cell.getchannel("A"))
        after = sample(rgb, 4)["crown"]
        self.assertLess(abs(saturation(after) - saturation(before)), .025)
        self.sheet.paste(rgb, (0, 4 * 208))
        with self.assertRaisesRegex(AssertionError, "lightness drift: 4/0"):
            validate_palette(self.sheet)

    def test_closed_eyes_cannot_return_to_long_idle_frame(self):
        cell = frame(self.sheet, 0, 3)
        left, top, right, bottom = cell.getbbox()
        cell.paste((254, 241, 228, 255), (round(left + (right - left) * .25), round(top + (bottom - top) * .30),
                                          round(left + (right - left) * .75), round(top + (bottom - top) * .53)))
        self.sheet.paste(cell, (3 * 192, 0))
        with self.assertRaisesRegex(AssertionError, "Closed or narrowed eyes"):
            validate_idle_eyes(self.sheet)

    def test_dark_working_locks_are_rejected_with_unchanged_crown(self):
        cell = frame(self.sheet, 7, 2)
        before = sample(cell, 7)["crown"]
        x0, y0, x1, y1 = cell.getbbox()
        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b, a = cell.getpixel((x, y))
                xn, yn = (x - x0) / (x1 - x0), (y - y0) / (y1 - y0)
                if a >= 250 and (xn < .28 or xn > .72) and .36 < yn < .70 and r > g + 25 and 0 < g - b < 30 and 65 < b and r < 190:
                    cell.putpixel((x, y), tuple(round(c * .94) for c in (r, g, b)) + (a,))
        self.assertEqual(before, sample(cell, 7)["crown"])
        self.sheet.paste(cell, (2 * 192, 7 * 208))
        with self.assertRaisesRegex(AssertionError, "Working hair shadow lightness drift: 7/2"):
            validate_palette(self.sheet)

    def test_brown_locks_do_not_block_calibration_as_false_irises(self):
        cell = Image.new("RGBA", (192, 208), (204, 155, 139, 255))
        brown, iris = (145, 70, 67, 255), (175, 60, 70, 255)
        cell.putpixel((45, 90), brown)
        cell.putpixel((80, 90), iris)
        changed = calibrate_cell(cell, 7, (204, 155, 139), brown[:3],
                                 (204, 155, 139), (150, 78, 75))
        self.assertNotEqual(changed.getpixel((45, 90)), brown)
        self.assertEqual(changed.getpixel((80, 90)), iris)
        self.assertEqual(cell.getchannel("A").tobytes(), changed.getchannel("A").tobytes())

    def test_color_calibration_preserves_alpha_irises_and_boots(self):
        cell = frame(self.sheet, 0, 0)
        colors = sample(cell, 0)
        changed = calibrate_cell(cell, 0, colors["crown"], colors["shadow"],
                                 tuple(c + 5 for c in colors["crown"]), colors["shadow"])
        self.assertNotEqual(cell.tobytes(), changed.tobytes())
        self.assertEqual(cell.getchannel("A").tobytes(), changed.getchannel("A").tobytes())
        self.assertEqual(cell.crop((0, 175, 192, 208)).tobytes(), changed.crop((0, 175, 192, 208)).tobytes())
        for y in range(60, 112):
            for x in range(48, 144):
                r, g, b, a = cell.getpixel((x, y))
                if a and r > 80 and r > 1.9 * max(g, b):
                    self.assertEqual(cell.getpixel((x, y)), changed.getpixel((x, y)))


if __name__ == "__main__":
    unittest.main()
