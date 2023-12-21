import unittest
from PIL import Image, ImageChops
from reversi.board import Position
from reversi.in_out.png import png


class PngTest(unittest.TestCase):
    def test_png(self):
        reference = Image.open("tests/start_pos.png")

        image = png(Position.start())

        diff = ImageChops.difference(image, reference)
        self.assertIsNone(diff.getbbox())


if __name__ == "__main__":
    unittest.main(verbosity=2)
