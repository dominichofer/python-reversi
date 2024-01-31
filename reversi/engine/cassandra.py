"Cassandra wrapper."
import subprocess
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from typing import Iterable
from pathlib import Path
import locale
from reversi.search import (
    OpenInterval,
    ClosedInterval,
    Field,
    Position,
    Player,
    Intensity,
    Result,
)
from .engine import Engine
from .helpers import split, flatten, UniqueTempFile


def parse_int(string: str) -> int:
    "Parses an integer."
    return int(string.replace("'", ""))


class CassandraLine:
    "Line of Cassandra's output."

    def __init__(self, string: str):
        index, depth, evl, _, time, nodes, nps, pv = [
            s.strip() for s in string.split("|")
        ]

        self.index = parse_int(index)
        self.intensity = Intensity.from_string(depth)
        self.score = parse_int(evl)
        self.time = time
        self.nodes = parse_int(nodes)
        self.speed = parse_int(nps) if nps else None
        self.pv = [Field[x.upper()] for x in pv.split() if x != ""]
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
        return "\n".join(
            [
                f"index: {self.index}",
                f"intensity: d{self.intensity}",
                f"score: {self.score:+03}",
                f"time: {self.time}",
                f"nodes: {self.nodes:n}",
                f"speed: {self.speed:n} N/s" if self.speed else "speed: ? N/s",
                f"pv: {pv}",
                f"best_move: {self.best_move.name}",
                f"result: {self.result}",
            ]
        )


class Cassandra(Engine, Player):
    "Cassandra wrapper."

    def __init__(
        self,
        exe_path: Path | str,
        model_path: Path | str,
        window: OpenInterval | None = None,
        intensity: Intensity | None = None,
        hash_table_size: int | None = None,
        threads: int | None = None,
        multi_instance: bool = False,
    ):
        self.exe = Path(exe_path).resolve()
        self.model = Path(model_path).resolve()
        self.window = window
        self.threads = threads
        self.hash_table_size = hash_table_size
        self.intensity = intensity
        self.multi_instance = multi_instance

    @property
    def name(self) -> str:
        return "Cassandra"

    def __command(self, temp_file: Path) -> list[str]:
        command = [str(self.exe), "-m", str(self.model), "-solve", str(temp_file)]
        if self.window is not None:
            command += ["-w", str(self.window)]
        if self.intensity is not None:
            command += ["-d", str(self.intensity)]
        if self.hash_table_size is not None:
            command += ["-tt", str(self.hash_table_size)]
        if self.threads is not None:
            command += ["-t", str(self.threads)]
        return command

    def solve_many_native(self, pos: Iterable[Position]) -> list[CassandraLine]:
        "Solves positions."
        with UniqueTempFile(self.exe.parent) as temp_file:
            temp_file.write_text("\n".join(str(p) for p in pos))
            result = subprocess.run(
                self.__command(temp_file), capture_output=True, check=True, text=True
            )
        return [CassandraLine(l) for l in result.stdout.split("\n")[2:-4]]

    def solve_native(self, pos: Position) -> CassandraLine:
        "Solves a position."
        return self.solve_many_native([pos])[0]

    def __solve_many_result(self, pos: Iterable[Position]) -> list[Result]:
        return [x.result for x in self.solve_many_native(pos)]

    def solve(self, pos: Position) -> Result:
        return self.__solve_many_result([pos])[0]

    def solve_many(self, pos: Iterable[Position]) -> list[Result]:
        if self.multi_instance:
            with ThreadPool() as pool:
                return flatten(
                    pool.map(
                        self.__solve_many_result,
                        split(pos, cpu_count()),
                    )
                )
        else:
            return self.__solve_many_result(pos)

    def choose_move(self, pos: Position) -> Field:
        return self.solve(pos).best_move

    def choose_moves(self, pos: Iterable[Position]) -> list[Field]:
        return [x.best_move for x in self.solve_many(pos)]
