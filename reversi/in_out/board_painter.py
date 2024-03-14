from abc import ABC, abstractmethod
from dataclasses import dataclass
from reversi.board import Field, Position, possible_moves

Color = tuple[int, int, int]


@dataclass
class ColorScheme:
    "Colors for drawing a reversi position."
    background: Color
    grid_line: Color
    player_fill: Color
    player_border: Color
    opponent_fill: Color
    opponent_border: Color
    cross: Color

    @staticmethod
    def green() -> "ColorScheme":
        "Return a green color scheme."
        return ColorScheme(
            background=(40, 100, 50),  # forest green
            grid_line=(0, 40, 20),  # dark green
            player_fill=(0, 0, 0),
            player_border=(0, 0, 0),
            opponent_fill=(255, 255, 255),
            opponent_border=(255, 255, 255),
            cross=(255, 0, 0),
        )

    @staticmethod
    def black_and_white() -> "ColorScheme":
        "Return a black and white color scheme."
        return ColorScheme(
            background=(255, 255, 255),
            grid_line=(0, 0, 0),
            player_fill=(0, 0, 0),
            player_border=(0, 0, 0),
            opponent_fill=(255, 255, 255),
            opponent_border=(0, 0, 0),
            cross=(0, 0, 0),
        )


class Sizes:
    "Sizes for drawing a reversi position."

    def __init__(
        self, field: int, line: int, grid_dot: int, disc: int, cross: int
    ) -> None:
        assert field > 0 and field % 2 == 1
        assert line > 0 and line % 2 == 1
        assert grid_dot > 0
        assert disc > 0
        assert cross > 0
        self.field = field
        self.line = line
        self.grid_dot = grid_dot
        self.disc = disc
        self.cross = cross

    @staticmethod
    def default(field: int, line: int = 1) -> "Sizes":
        "Return a default size scheme."
        return Sizes(
            field=field,
            line=line,
            grid_dot=line * 2,
            disc=field // 2,
            cross=field // 8,
        )

    @property
    def total_size(self) -> int:
        "Return the total size of the board."
        return self.field * 8 + self.line * 7

    def line_center(self, index: int) -> int:
        "Return the center of a line."
        return (index + 1) * self.field + index * self.line + self.line // 2

    def field_center(self, index: int) -> int:
        "Return the center of a field."
        return index * (self.field + self.line) + self.field // 2


class Painter(ABC):
    "A painter for drawing on a canvas."

    @abstractmethod
    def line(
        self,
        p1: tuple[int, int],
        p2: tuple[int, int],
        color: Color,
        width: int,
    ):
        "Draw a line."

    @abstractmethod
    def rectangle(
        self,
        p1: tuple[int, int],
        p2: tuple[int, int],
        fill: Color,
    ):
        "Draw a rectangle."

    @abstractmethod
    def circle(
        self,
        center: tuple[int, int],
        radius: int,
        fill: Color,
        outline: Color,
        width: int,
    ):
        "Draw a circle."

    def draw_position(self, pos: Position, colors: ColorScheme, sizes: Sizes):
        "Draw the position on the canvas."
        # Fill background
        self.rectangle(
            (0, 0),
            (sizes.total_size, sizes.total_size),
            fill=colors.background,
        )

        # Draw grid lines
        for i in range(7):
            self.line(
                (0, sizes.line_center(i)),
                (sizes.total_size, sizes.line_center(i)),
                color=colors.grid_line,
                width=sizes.line,
            )
            self.line(
                (sizes.line_center(i), 0),
                (sizes.line_center(i), sizes.total_size),
                color=colors.grid_line,
                width=sizes.line,
            )

        # Draw grid dots
        for i in [1, 5]:
            for j in [1, 5]:
                self.circle(
                    (sizes.line_center(i), sizes.line_center(j)),
                    sizes.grid_dot,
                    fill=colors.grid_line,
                    outline=colors.grid_line,
                    width=sizes.line,
                )

        # Draw discs
        for i in range(8):
            for j in range(8):
                field = Field(63 - (j * 8 + i))
                if pos.player_at(field) or pos.opponent_at(field):
                    if pos.player_at(field):
                        fill = colors.player_fill
                        outline = colors.player_border
                    else:
                        fill = colors.opponent_fill
                        outline = colors.opponent_border
                    self.circle(
                        (sizes.field_center(i), sizes.field_center(j)),
                        sizes.disc,
                        fill=fill,
                        outline=outline,
                        width=sizes.line,
                    )

        # Draw Xs
        moves = possible_moves(pos)
        for i in range(8):
            for j in range(8):
                field = Field(63 - (j * 8 + i))
                if field in moves:
                    self.line(
                        (
                            sizes.field_center(i) - sizes.cross,
                            sizes.field_center(j) - sizes.cross,
                        ),
                        (
                            sizes.field_center(i) + sizes.cross,
                            sizes.field_center(j) + sizes.cross,
                        ),
                        color=colors.cross,
                        width=sizes.line,
                    )
                    self.line(
                        (
                            sizes.field_center(i) - sizes.cross,
                            sizes.field_center(j) + sizes.cross,
                        ),
                        (
                            sizes.field_center(i) + sizes.cross,
                            sizes.field_center(j) - sizes.cross,
                        ),
                        color=colors.cross,
                        width=sizes.line,
                    )
