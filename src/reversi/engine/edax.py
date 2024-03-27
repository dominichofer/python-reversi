from typing import Iterable
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

    @staticmethod
    def from_bytes(data: bytes) -> "EdaxLine":
        "Return an EdaxLine from a bytes object."
        index = int.from_bytes(data[:4], "big")
        data = data[4:]

        intensity = Intensity.from_bytes(data[:8])
        data = data[8:]

        score = int.from_bytes(data[:4], "big")
        data = data[4:]

        time_length = int.from_bytes(data[:4], "big")
        time = data[4 : 4 + time_length].decode()
        data = data[4 + time_length :]

        nodes = int.from_bytes(data[:4], "big")
        data = data[4:]

        nodes_per_second = int.from_bytes(data[:4], "big")
        data = data[4:]

        pv_length = int.from_bytes(data[:4], "big")
        pv = [Field(x) for x in data[4 : 4 + pv_length]]
        data = data[4 + pv_length :]

        best_move = Field(data[0])

        return EdaxLine(
            index,
            intensity,
            score,
            time,
            nodes,
            nodes_per_second,
            pv,
            best_move,
        )

    def __bytes__(self) -> bytes:
        index = self.index.to_bytes(4, "big")
        Intensity = bytes(self.intensity)
        score = self.score.to_bytes(4, "big")
        time = self.time.encode()
        time = len(time).to_bytes(4, "big") + time
        nodes = self.nodes.to_bytes(4, "big")
        nps = self.nodes_per_second.to_bytes(4, "big")
        pv = b"".join(Field[x.name].value.to_bytes(1, "big") for x in self.pv)
        pv = len(pv).to_bytes(4, "big") + pv
        best_move = self.best_move.value.to_bytes(1, "big")
        return index + Intensity + score + time + nodes + nps + pv + best_move

    def __str__(self) -> str:
        pv = " ".join(x.name for x in self.pv)
        if self.nodes_per_second is not None:
            nodes_per_second = f"{self.nodes_per_second:_} N/s".replace("_", "'")
        else:
            nodes_per_second = "? N/s"
        return "\n".join(
            [
                f"index: {self.index}",
                f"intensity: d{self.intensity}",
                f"score: {self.score:+03}",
                f"time: {self.time}",
                f"nodes: {self.nodes:_}".replace("_", "'"),
                f"nodes_per_second: {nodes_per_second}",
                f"pv: {pv}",
                f"best_move: {self.best_move.name}",
                f"result: {self.result}",
            ]
        )

    @property
    def result(self) -> Result:
        "Returns the search result."
        return Result(
            ClosedInterval(self.score, self.score),
            self.intensity,
            self.best_move,
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
        results = self.edax.solve([str(p) for p in pos])
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
