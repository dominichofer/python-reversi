from typing import Iterable


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
