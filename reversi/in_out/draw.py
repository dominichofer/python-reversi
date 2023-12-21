from reversi.board import Position, possible_moves

class DrawEngine:
    "Draw a reversi position as a PNG image."

    def __init__(self):
        self.tile_size = 20
        self.background_color = (40, 100, 50) # forest green
        self.grid_line_width = 1
        self.grid_line_color = (0, 40, 20) # dark green
        self.grid_dot_size = 2
        self.disc_size = int(self.tile_size * 0.9)
        self.player_color = "black"
        self.opponent_color = "white"
        self.x_size = int(self.tile_size * 0.2)
        self.x_color = "red"

    def square_around_tile_center(
        self, i: int, j: int, diff: float
    ) -> tuple[float, float, float, float]:
        "Return the four corners of the square around the center of the tile at (i, j)."
        x = (i + 0.5) * self.tile_size
        y = (j + 0.5) * self.tile_size
        return (x - diff, y - diff, x + diff, y + diff)

    def draw(self, pos: Position):
        "Draw the position as a PNG image."
        image_size = self.tile_size * 8
        image = Image.new("RGB", (image_size, image_size), self.background_color)
        drawing = ImageDraw.Draw(image)

        # Draw grid
        for i in range(8):
            for j in range(8):
                drawing.rectangle(
                    self.square_around_tile_center(i, j, self.tile_size / 2),
                    fill=self.background_color,
                    outline=self.grid_line_color,
                    width=self.grid_line_width,
                )

        # Draw grid dots
        for i in [2, 6]:
            for j in [2, 6]:
                x = i * self.tile_size
                y = j * self.tile_size
                diff = self.grid_dot_size
                drawing.ellipse(
                    (x - diff, y - diff, x + diff, y + diff), self.grid_line_color
                )

        # Draw discs and Xs
        moves = possible_moves(pos)
        for i in range(8):
            for j in range(8):
                bit = uint64(1) << uint64(63 - (j * 8 + i))
                if pos.discs() & bit:
                    # Draw disc
                    if pos.player & bit:
                        color = self.player_color
                    elif pos.opponent & bit:
                        color = self.opponent_color
                    drawing.ellipse(
                        self.square_around_tile_center(i, j, self.disc_size / 2), color
                    )
                elif moves & bit:
                    # Draw X
                    x1, y1, x2, y2 = self.square_around_tile_center(
                        i, j, self.x_size / 2
                    )
                    drawing.line((x1, y1, x2, y2), self.x_color)
                    drawing.line((x1, y2, x2, y1), self.x_color)

        return image
