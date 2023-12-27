from dataclasses import dataclass
import wx
from reversi import Field, bit, Position
from .board_painter import ColorScheme, Sizes
from .wx_painter import WxPainter


@dataclass
class Model:
    "Model in a MVC pattern."
    pos: Position


class Controller:
    "Controller in a MVC pattern."

    def __init__(self, model: Model, refresh_view):
        self.model = model
        self.refresh_view = refresh_view
        self.action = self.do_nothing  # Controller state

    def set(self, pos: Position):
        "Set position."
        self.model.pos = pos
        self.refresh_view()

    def do_nothing(self, _):
        "Do nothing."

    def set_to_player(self, field: Field):
        "Set disc at field to player."
        mask = bit(field)
        self.model.pos = Position(
            self.model.pos.player | mask, self.model.pos.opponent & ~mask
        )

    def set_to_opponent(self, field: Field):
        "Set disc at field to opponent."
        mask = bit(field)
        self.model.pos = Position(
            self.model.pos.player & ~mask, self.model.pos.opponent | mask
        )

    def clear(self, field: Field):
        "Clear field."
        mask = bit(field)
        self.model.pos = Position(
            self.model.pos.player & ~mask, self.model.pos.opponent & ~mask
        )

    def on_left_down(self, field: Field):
        "Left mouse button was pressed at field."
        if self.model.pos.player_at(field):
            self.action = self.clear
        else:
            self.action = self.set_to_player
        self.action(field)
        self.refresh_view()

    def on_right_down(self, field: Field):
        "Right mouse button was pressed at field."
        if self.model.pos.opponent_at(field):
            self.action = self.clear
        else:
            self.action = self.set_to_opponent
        self.action(field)
        self.refresh_view()

    def on_up(self, _):
        "Mouse button was released."
        self.action = self.do_nothing

    def on_move(self, field: Field):
        "Mouse was moved to field."
        self.action(field)
        self.refresh_view()


# View
class BoardPanel(wx.Panel):
    """
    A panel that displays a reversi position.
    A view in a MVC pattern.
    """

    def __init__(self, parent, sizes: Sizes, model: Model, controller: Controller):
        super().__init__(parent, size=(sizes.total_size, sizes.total_size))
        self.sizes = sizes
        self.model = model
        self.controller = controller

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda _: None)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_up)
        self.Bind(wx.EVT_RIGHT_UP, self.on_up)
        self.Bind(wx.EVT_MOTION, self.on_move)

    def field(self, event):
        "Return the field closest to the mouse position."
        x, y = event.GetPosition()
        i = x // (self.sizes.field + self.sizes.line)
        j = y // (self.sizes.field + self.sizes.line)
        return Field(63 - (j * 8 + i))

    def on_paint(self, _):
        "Paint the board."
        painter = WxPainter(wx.BufferedPaintDC(self))
        painter.draw_position(self.model.pos, ColorScheme.green(), self.sizes)

    def on_left_down(self, event):
        "Left mouse button was pressed."
        self.controller.on_left_down(self.field(event))

    def on_right_down(self, event):
        "Right mouse button was pressed."
        self.controller.on_right_down(self.field(event))

    def on_up(self, event):
        "Mouse button was released."
        self.controller.on_up(self.field(event))

    def on_move(self, event):
        "Mouse was moved."
        self.controller.on_move(self.field(event))


class SetUpFrame(wx.Frame):
    "A frame for setting up a position."

    def __init__(self, pos: Position):
        super().__init__(
            None,
            title="Position setup",
            style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER & ~wx.MAXIMIZE_BOX,
        )

        self.model = Model(pos)
        self.controller = Controller(self.model, self.refresh)
        self.board = BoardPanel(
            self, Sizes(51, 3, 6, 23, 6), self.model, self.controller
        )

        self.single_line_str = wx.TextCtrl(self, size=(484, -1))
        self.player_str = wx.TextCtrl(self, size=(242, -1))
        self.opponent_str = wx.TextCtrl(self, size=(242, -1))

        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, faceName="Consolas")
        self.single_line_str.SetFont(font)
        self.player_str.SetFont(font)
        self.opponent_str.SetFont(font)

        self.Bind(wx.EVT_TEXT_ENTER, self.on_enter)

        grid = wx.GridBagSizer(0, 0)
        grid.Add(self.board, pos=(0, 0), span=(1, 2), flag=wx.ALIGN_CENTER)
        grid.Add(self.single_line_str, pos=(1, 0), span=(1, 2))
        grid.Add(self.player_str, pos=(2, 0))
        grid.Add(self.opponent_str, pos=(2, 1))

        self.SetSizer(grid)
        self.Fit()
        self.Show()

        self.refresh()

    def refresh(self):
        "Refresh the GUI."
        self.board.Refresh()
        self.single_line_str.SetValue(str(self.model.pos))
        self.player_str.SetValue(f"0x{self.model.pos.player:016x}")
        self.opponent_str.SetValue(f"0x{self.model.pos.opponent:016x}")

    def on_enter(self, event):
        "Enter was pressed in one of the text fields."
        if event.EventObject == self.single_line_str:
            pos = Position.from_string(self.single_line_str.GetValue())
            self.controller.set(pos)
        elif event.EventObject in (self.player_str, self.opponent_str):
            try:
                player = int(self.player_str.GetValue(), 16)
                opponent = int(self.opponent_str.GetValue(), 16)
                self.controller.set(Position(player, opponent))
            except ValueError:
                pass


def setup_position() -> Position:
    "Set up a reversi position."
    app = wx.App()
    frame = SetUpFrame(Position.start())
    app.MainLoop()
    return frame.model.pos
