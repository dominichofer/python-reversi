import unittest
from PIL import Image, ImageChops
from reversi.board import Position
from reversi.in_out import png, Sizes, ColorScheme


class PngTest(unittest.TestCase):
    def test_start_pos_default(self):
        reference = Image.open("tests/reversi/start_pos.png")

        image = png(Position.start())

        diff = ImageChops.difference(image, reference)
        self.assertIsNone(diff.getbbox())

    def test_start_pos_size_11(self):
        reference = Image.open("tests/reversi/start_pos_size_11.png")

        image = png(Position.start(), sizes=Sizes.default(11))

        diff = ImageChops.difference(image, reference)
        self.assertIsNone(diff.getbbox())

    def test_start_pos_size_51(self):
        reference = Image.open("tests/reversi/start_pos_size_51.png")

        image = png(Position.start(), sizes=Sizes(51, 3, 7, 24, 8))

        diff = ImageChops.difference(image, reference)
        self.assertIsNone(diff.getbbox())

    def test_top_left_pos(self):
        reference = Image.open("tests/reversi/top_left_pos.png")

        image = png(Position(0x8000000000000000, 0x4000000000000000))

        diff = ImageChops.difference(image, reference)
        self.assertIsNone(diff.getbbox())

    def test_start_pos_black_and_white(self):
        reference = Image.open("tests/reversi/start_pos_black_and_white.png")

        image = png(Position.start(), colors=ColorScheme.black_and_white())

        diff = ImageChops.difference(image, reference)
        self.assertIsNone(diff.getbbox())

    def test_start_pos_rainbow(self):
        reference = Image.open("tests/reversi/start_pos_rainbow.png")
        rainbow = ColorScheme(
            background=(255, 0, 0),  # Red
            grid_line=(255, 165, 0),  # Orange
            player_fill=(255, 255, 0),  # Yellow
            player_border=(0, 128, 0),  # Green
            opponent_fill=(0, 0, 255),  # Blue
            opponent_border=(75, 0, 130),  # Indigo
            cross=(148, 0, 211),  # Violet
        )
        image = png(Position.start(), colors=rainbow)

        diff = ImageChops.difference(image, reference)
        self.assertIsNone(diff.getbbox())
