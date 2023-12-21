"Edax wrapper."
import subprocess
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from typing import Iterable
from pathlib import Path
from secrets import token_hex
import locale
from reversi.search import (
    ClosedInterval,
    Field,
    Position,
    Player,
    Intensity,
    SearchResult,
)
from .engine import Engine


def split(data: Iterable, max_sections: int):
    "Splits data into sections."
    data = list(data)

    elements_per_section, remainder = divmod(len(data), max_sections)
    sections = min(len(data), max_sections)
    for i in range(remainder):
        yield data[i * (elements_per_section + 1) : (i + 1) * (elements_per_section + 1)]
    for i in range(remainder, sections):
        yield data[
            i * elements_per_section + remainder : (i + 1) * elements_per_section + remainder
        ]


def flatten(data: Iterable[Iterable]) -> list:
    "Flattens data."
    return [x for xs in data for x in xs]


class UniqueTempFile:
    "Context manager that creates a temporary file and deletes it when done."

    def __init__(self, directory: Path) -> None:
        self.filename: Path = Path(directory) / f"tmp_{token_hex(16)}"

    def __enter__(self):
        return self.filename

    def __exit__(self, *_):
        self.filename.unlink()
        return False


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
        self.search_result = SearchResult(
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
                f"selectivity: {self.selectivity}%",
                f"intensity: d{self.intensity}",
                f"score: {self.score:+03}",
                f"time: {self.time}",
                f"nodes: {self.nodes:n}",
                f"speed: {self.speed:n} N/s" if self.speed else "speed: ? N/s",
                f"pv: {pv}",
                f"best_move: {self.best_move.name}",
                f"search_result: {self.search_result}",
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
        self.exe = Path(exe_path)
        self.hash_table_size = hash_table_size
        self.tasks = tasks
        self.level = level
        self.multi_instance = multi_instance

    @property
    def name(self) -> str:
        result = subprocess.run(
            [self.exe, "-v", "-h"], capture_output=True, check=True, text=True
        )
        return " ".join(result.stderr.split()[0:3])

    def solve_many_native(self, pos: Iterable[Position]) -> list[EdaxLine]:
        "Solves positions using Edax."
        with UniqueTempFile(self.exe.parent) as tmp_file:
            tmp_file.write_text("\n".join(str(p) for p in pos))

            command = [self.exe, "-solve", tmp_file]
            if self.hash_table_size is not None:
                command += ["-h", str(self.hash_table_size)]
            if self.tasks is not None:
                command += ["-n", str(self.tasks)]
            if self.level is not None:
                command += ["-l", str(self.level)]

            result = subprocess.run(
                command, cwd=self.exe.parent, capture_output=True, check=True, text=True
            )
        return [EdaxLine(l) for l in result.stdout.split("\n")[2:-4]]

    def solve_native(self, pos: Position) -> EdaxLine:
        "Solves a position using Edax."
        return self.solve_many_native([pos])[0]

    def __solve_many_search_result(self, pos: Iterable[Position]) -> list[SearchResult]:
        return [x.search_result for x in self.solve_many_native(pos)]

    # Add missing import statements
    def solve(self, pos: Position) -> SearchResult:
        return self.__solve_many_search_result([pos])[0]

    def solve_many(self, pos: Iterable[Position]) -> list[SearchResult]:
        if self.multi_instance:
            with ThreadPool() as pool:
                return flatten(
                    pool.map(
                        self.__solve_many_search_result,
                        split(pos, cpu_count()),
                    )
                )
        else:
            return self.__solve_many_search_result(pos)

    def choose_move(self, pos: Position) -> Field:
        return self.solve(pos).best_move

    def choose_moves(self, pos: Iterable[Position]) -> list[Field]:
        return [x.best_move for x in self.solve_many(pos)]
