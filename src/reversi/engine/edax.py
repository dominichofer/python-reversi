from typing import Iterable
import locale
import edax  # type: ignore
from reversi.search import (
    ClosedInterval,
    Field,
    Position,
    Player,
    Intensity,
    Result,
)
from .engine import Engine


class EdaxLine:
    "Line of Edax' output."

    def __init__(self, line: edax.Line):
        self.index = line.index
        confidence_level = {
            73: 1.1,
            87: 1.5,
            95: 2.0,
            98: 2.6,
            99: 3.3,
            None: float("inf"),
        }[line.selectivity]
        self.intensity = Intensity(line.depth, confidence_level)
        self.score = line.score
        self.time = line.time
        self.nodes = line.nodes
        self.nodes_per_second = line.nodes_per_second
        self.pv = [Field[x.upper()] for x in line.pv]
        self.best_move = self.pv[0] if self.pv else Field.PS

    @property
    def result(self) -> Result:
        "Returns the search result."
        return Result(
            ClosedInterval(self.score, self.score),
            self.intensity,
            self.best_move,
        )

    def __str__(self) -> str:
        locale.setlocale(locale.LC_ALL, "")
        pv = " ".join(x.name for x in self.pv)
        if self.nodes_per_second is not None:
            nodes_per_second = f"{self.nodes_per_second:n} N/s"
        else:
            nodes_per_second = "? N/s"
        return "\n".join(
            [
                f"index: {self.index}",
                f"intensity: d{self.intensity}",
                f"score: {self.score:+03}",
                f"time: {self.time}",
                f"nodes: {self.nodes:n}",
                f"nodes_per_second: {nodes_per_second:n}",
                f"pv: {pv}",
                f"best_move: {self.best_move.name}",
                f"result: {self.result}",
            ]
        )


class Edax(Engine, Player):
    "Edax wrapper"

    def __init__(
        self,
        hash_table_size: int | None = None,
        tasks: int | None = None,
        level: int | None = None,
        multiprocess: bool = False,
    ):
        """
        hash_table_size: Hash table size in number of bits.
        tasks: Search in parallel using n tasks.
        level: Search using limited depth.
        multiprocess: Whether to use multiple instances of Edax concurrently.
        """
        self.multiprocess = multiprocess
        if multiprocess:
            self.edax = edax.MultiprocessEdax(hash_table_size, tasks, level)
        else:
            self.edax = edax.Edax(hash_table_size, tasks, level)

    def name(self) -> str:
        return edax.Edax.name()

    def solve_native(self, pos: Position | Iterable[Position]) -> list[EdaxLine]:
        if isinstance(pos, Position):
            pos = [pos]
        results = self.edax.solve(pos)
        if not self.multiprocess:
            results = results.lines
        return [EdaxLine(x) for x in results]

    def solve(self, pos: Position) -> Result:
        return self.solve_native(pos)[0].result

    def solve_many(self, pos: Iterable[Position]) -> list[Result]:
        return [x.result for x in self.solve_native(pos)]

    def choose_move(self, pos: Position) -> Field:
        return self.solve(pos).best_move

    def choose_moves(self, pos: Iterable[Position]) -> list[Field]:
        return [x.best_move for x in self.solve_many(pos)]
