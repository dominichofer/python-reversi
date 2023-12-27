import wx
from .board_painter import Painter, Color


class WxPainter(Painter):
    "Draw a reversi position on a wx canvas."

    def __init__(self, canvas: wx.BufferedDC) -> None:
        self.canvas = canvas

    def line(
        self,
        p1: tuple[int, int],
        p2: tuple[int, int],
        color: Color,
        width: int,
    ):
        self.canvas.SetPen(wx.Pen(wx.Colour(*color), width))
        self.canvas.DrawLine(*p1, *p2)
        self.canvas.DrawLine(*p2, *p1)

    def rectangle(
        self,
        p1: tuple[int, int],
        p2: tuple[int, int],
        fill: Color,
    ):
        self.canvas.SetPen(wx.Pen(wx.Colour(*fill)))
        self.canvas.SetBrush(wx.Brush(wx.Colour(*fill)))
        self.canvas.DrawRectangle(*p1, *p2)

    def circle(
        self,
        center: tuple[int, int],
        radius: int,
        fill: Color,
        outline: Color,
        width: int,
    ):
        self.canvas.SetPen(wx.Pen(wx.Colour(*outline), width))
        self.canvas.SetBrush(wx.Brush(wx.Colour(*fill)))
        self.canvas.DrawCircle(*center, radius)
