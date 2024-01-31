from typing import Iterable
from pathlib import Path
from secrets import token_hex


def split(data: Iterable, max_sections: int):
    "Splits data into sections."
    data = list(data)

    elements_per_section, remainder = divmod(len(data), max_sections)
    sections = min(len(data), max_sections)
    for i in range(remainder):
        yield data[
            i * (elements_per_section + 1) : (i + 1) * (elements_per_section + 1)
        ]
    for i in range(remainder, sections):
        yield data[
            i * elements_per_section
            + remainder : (i + 1) * elements_per_section
            + remainder
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
