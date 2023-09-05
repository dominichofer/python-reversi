import subprocess
import multiprocessing
from collections.abc import Iterable
from pathlib import Path
from secrets import token_hex
from reversi import Field


class UniqueTempFile:    def __init__(self, directory: Path) -> None:
        self.filename: Path = Path(directory) / f"tmp_{token_hex(16)}"

    def __enter__(self):
        return self.filename

    def __exit__(self, *_):
        self.filename.unlink()
        return False


class Line:    def __init__(self, string: str):
        index, rest = string.split("|")
        depth = rest[:6].strip().split("@")

        self.index = int(index)
        self.depth = int(depth[0])
        self.selectivity = int(depth[1][:-1]) if len(depth) == 2 else None
        self.confidence_level = {
            None: float("inf"),
            73: 1.1,
            87: 1.5,
            95: 2.0,
            98: 2.6,
            99: 3.3,
        }[self.selectivity]
        self.score = int(rest[7:12].strip())
        self.time = rest[13:27].strip()
        self.nodes = int(rest[28:41].strip())
        speed = rest[42:52].strip()
        self.speed = int(speed) if speed else None
        pv_as_str = rest[53:73].split()
        self.pv = [Field[x.upper()] for x in pv_as_str if x != ""]


def split(lst: list, num_sections: int) -> list:
    s, rem = divmod(len(lst), num_sections)
    return [
        lst[i * (s + 1): (i + 1) * (s + 1)]
        if i < rem
        else lst[rem + i * s: rem + (i + 1) * s]
        for i in range(num_sections)
    ]


class Edax:    def __init__(
        self,
        exe_path,
        hash_table_size: int | None = None,
        tasks: int | None = None,
        level: int | None = None,
    ):
        self.exe: Path = Path(exe_path)
        self.hash_table_size: int | None = hash_table_size
        self.tasks: int | None = tasks
        self.level: int | None = level

    @property
    def name(self) -> str:
        result = subprocess.run([self.exe, "-v", "-h"],
                                capture_output=True, text=True)
        return " ".join(result.stderr.split()[0:3])

    def solve(self, pos) -> list[Line]:
        if isinstance(pos, str) or not isinstance(pos, Iterable):
            pos = [pos]

        with UniqueTempFile(self.exe.parent) as tmp_file:
            tmp_file.write_text("\n".join(str(p) for p in pos))

            cmd = [self.exe, "-solve", tmp_file]
            if self.hash_table_size is not None:
                cmd += ["-h", str(self.hash_table_size)]
            if self.tasks is not None:
                cmd += ["-n", str(self.tasks)]
            if self.level is not None:
                cmd += ["-l", str(self.level)]

            result = subprocess.run(
                cmd, cwd=self.exe.parent, capture_output=True, text=True
            )

        return [Line(l) for l in result.stdout.split("\n")[2:-4]]

    def choose_move(self, pos) -> list[Field]:
        result = self.solve(pos)
        return [(Field(r.pv[0]) if r.pv else Field.PS) for r in result]


class ThreadPoolEdax:    def __init__(
        self,
        exe_path,
        hash_table_size: int | None = None,
        tasks: int | None = None,
        level: int | None = None,
        chunksize: int = multiprocessing.cpu_count() * 4,
    ):
        self.edax = Edax(exe_path, hash_table_size, tasks, level)
        self.chunksize = chunksize

    @property
    def name(self) -> str:
        return self.edax.name

    def solve(self, pos) -> list[Line]:
        if isinstance(pos, str) or not isinstance(pos, Iterable):
            pos = [pos]

        pool = pool.ThreadPool()
        results = pool.map(self.edax.solve, split(pos, self.chunksize))
        pool.close()
        return [r for result in results for r in result]

    def choose_move(self, pos) -> list[int]:
        result = self.solve(pos)
        return [(r.pv[0] if r.pv else 64) for r in result]
