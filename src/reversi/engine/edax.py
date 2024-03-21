"Edax wrapper."

import subprocess
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from typing import Iterable
from pathlib import Path
import locale
from reversi.search import (
    ClosedInterval,
    Field,
    Position,
    Player,
    Intensity,
    Result,
)
from .engine import Engine
from .helpers import split, flatten, UniqueTempFile


class EdaxLine:
    "Line of Edax' output."

    def __init__(self, string: str):
        index, rest = string.split("|")

        self.index = int(index)
        intensity = rest[:6].strip()
        self.selectivity = None
        if "@" in intensity:
            depth, selectivity = intensity.split("@")
            self.selectivity = int(selectivity[:-1])
            confidence_level = {
                73: 1.1,
                87: 1.5,
                95: 2.0,
                98: 2.6,
                99: 3.3,
            }[self.selectivity]
            self.intensity = Intensity(int(depth), confidence_level)
        else:
            self.selectivity = None
            self.intensity = Intensity(int(intensity))
        self.score = int(rest[7:12].strip())
        self.time = rest[13:27].strip()
        self.nodes = int(rest[28:41].strip())
        speed = rest[42:52].strip()
        self.speed = int(speed) if speed else None
        pv = rest[53:73].split()
        self.pv = [Field[x.upper()] for x in pv if x != ""]
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
        depth = (
            f"{self.intensity.depth}@{self.selectivity}%"
            if self.selectivity
            else f"{self.intensity.depth} "
        )
        speed = self.speed if self.speed else ""
        pv = " ".join(x.name for x in self.pv)
        return f"{self.index:3}|{depth:>6}  {self.score:+03} {self.time:>15} {self.nodes:13} {speed:10} {pv}"

    def pretty_string(self) -> str:
        locale.setlocale(locale.LC_ALL, "")
        pv = " ".join(x.name for x in self.pv)
        return "\n".join(
            [
                f"index: {self.index}",
                f"selectivity: {self.selectivity}%",
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


class Edax(Engine, Player):
    "Edax wrapper"

    def __init__(
        self,
        exe_path: Path | str,
        hash_table_size: int | None = None,
        tasks: int | None = None,
        level: int | None = None,
        multi_instance: bool = False,
    ):
        """
        exe_path: Path to Edax executable.
        hash_table_size: Hash table size in number of bits.
        tasks: Search in parallel using n tasks.
        level: Search using limited depth.
        multi_instance: Whether to use multiple instances of Edax concurrently.
        """
        self.exe = Path(exe_path).resolve()
        self.hash_table_size = hash_table_size
        self.tasks = tasks
        self.level = level
        self.multi_instance = multi_instance

    @property
    def name(self) -> str:
        result = subprocess.run([self.exe, "-v", "-h"], capture_output=True, check=True, text=True)
        return " ".join(result.stderr.split()[0:3])

    def __command(self, temp_file: Path) -> list[str]:
        command = [str(self.exe), "-solve", str(temp_file)]
        if self.hash_table_size is not None:
            command += ["-h", str(self.hash_table_size)]
        if self.tasks is not None:
            command += ["-n", str(self.tasks)]
        if self.level is not None:
            command += ["-l", str(self.level)]
        return command

    def solve_many_native(self, pos: Iterable[Position]) -> list[EdaxLine]:
        "Solves positions."
        with UniqueTempFile(self.exe.parent) as temp_file:
            temp_file.write_text("\n".join(str(p) for p in pos))
            result = subprocess.run(
                self.__command(temp_file),
                cwd=self.exe.parent,
                capture_output=True,
                check=True,
                text=True,
            )
        return [EdaxLine(l) for l in result.stdout.split("\n")[2:-4]]

    def solve_native(self, pos: Position) -> EdaxLine:
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
