from PIL import Image, ImageDraw
from reversi import Position

class DrawEngine:
    def __init__(self, tile_size: int = 20):
        self.tile_size = tile_size
        self.background_color = (40, 100, 50)
        self.grid_line_width = 1
        self.grid_line_color = (0, 40, 20)
        self.grid_dot_size = 2
        self.disc_size = int(tile_size * 0.9)
        self.player_color = 'black'
        self.opponent_color = 'white'
        self.cross_size = int(tile_size * 0.2)
        self.cross_color = 'red'

    def __around_tile_center(self, i, j, diff) -> tuple:
        x = (i+0.5) * self.tile_size
        y = (j+0.5) * self.tile_size
        return (x - diff, y - diff, x + diff, y + diff)

    def __draw_disc(self, x, y, player: bool) -> None:
        fill = self.player_color if player else self.opponent_color
        self.drawing.ellipse(self.__around_tile_center(x, y, self.disc_size/2), fill)

    def __draw_cross(self, x, y) -> None:
        x1, y1, x2, y2 = self.__around_tile_center(x, y, self.cross_size/2)
        self.drawing.line((x1, y1, x2, y2), self.cross_color)
        self.drawing.line((x1, y2, x2, y1), self.cross_color)

    def draw(self, pos: Position):
        image_size = self.tile_size * 8
        self.image = Image.new('RGB', (image_size, image_size))
        self.drawing = ImageDraw.Draw(self.image)
        
        # Draw grid
        for i in range(8):
            for j in range(8):
                self.drawing.rectangle(
                    self.__around_tile_center(i, j, self.tile_size/2),
                    fill = self.background_color,
                    outline = self.grid_line_color,
                    width = self.grid_line_width
                    )

        # Draw grid dots
        for i in [2, 6]:
            for j in [2, 6]:
                x = i * self.tile_size
                y = j * self.tile_size
                diff = self.grid_dot_size
                self.drawing.ellipse((x - diff, y - diff, x + diff, y + diff), self.grid_line_color)

        # Draw discs and crosses
        for i in range(8):
            for j in range(8):
                char = pos.character(j * 8 + i)
                if char in ['X', 'O']:
                    self.__draw_disc(i, j, char == 'X')
                elif char == '+':
                    self.__draw_cross(i, j)


def draw_position(pos: Position, tile_size: int = 20):
    engine = DrawEngine(tile_size)
    engine.draw(pos)
    return engine.image
