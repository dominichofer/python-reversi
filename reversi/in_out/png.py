"PNG image output for reversi positions."
from PIL import Image, ImageDraw
from reversi import Position
from .board_painter import ColorScheme, Sizes, Painter, Color


class PilPainter(Painter):
    "Draw a reversi position on a PIL canvas."

    def __init__(self, canvas: ImageDraw.ImageDraw) -> None:
        self.canvas = canvas

    def line(
        self,
        p1: tuple[int, int],
        p2: tuple[int, int],
        color: Color,
        width: int,
    ):
        self.canvas.line((*p1, *p2), fill=color, width=width)

    def rectangle(
        self,
        p1: tuple[int, int],
        p2: tuple[int, int],
        fill: Color,
    ):
        self.canvas.rectangle((*p1, *p2), fill=fill)

    def circle(
        self,
        center: tuple[int, int],
        radius: int,
        fill: Color,
        outline: Color,
        width: int,
    ):
        self.canvas.ellipse(
            (
                center[0] - radius,
                center[1] - radius,
                center[0] + radius,
                center[1] + radius,
            ),
            fill=fill,
            outline=outline,
            width=width,
        )


def png(
    pos: Position,
    colors: ColorScheme = ColorScheme.green(),
    sizes: Sizes = Sizes.default(19),
) -> Image.Image:
    "Draw a reversi position as a PNG image."
    image = Image.new("RGB", (sizes.total_size, sizes.total_size))
    painter = PilPainter(ImageDraw.Draw(image))
    painter.draw_position(pos, colors, sizes)
    return image
