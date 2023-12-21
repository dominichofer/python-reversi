"Intervals"
from dataclasses import dataclass


@dataclass
class OpenInterval:
    "An open interval of integers, e.g. (0, 1)"
    lower: int
    upper: int

    def __eq__(self, o) -> bool:
        return self.lower == o.lower and self.upper == o.upper

    def __lt__(self, o) -> bool:
        if isinstance(o, OpenInterval):
            return self.upper <= o.lower
        elif isinstance(o, ClosedInterval):
            return self.upper <= o.lower
        else:
            return self.upper <= o

    def __gt__(self, o) -> bool:
        if isinstance(o, OpenInterval):
            return self.lower >= o.upper
        elif isinstance(o, ClosedInterval):
            return self.lower >= o.upper
        else:
            return self.lower >= o

    def __neg__(self) -> "OpenInterval":
        return OpenInterval(-self.upper, -self.lower)

    def __str__(self) -> str:
        return f"({self.lower:+03},{self.upper:+03})"

    def __contains__(self, value: int) -> bool:
        return self.lower < value < self.upper


@dataclass
class ClosedInterval:
    "A closed interval of integers, e.g. [0, 1]"
    lower: int
    upper: int

    def __eq__(self, o) -> bool:
        return self.lower == o.lower and self.upper == o.upper

    def __lt__(self, o) -> bool:
        if isinstance(o, OpenInterval):
            return self.upper <= o.lower
        elif isinstance(o, ClosedInterval):
            return self.upper < o.lower
        else:
            return self.upper < o

    def __gt__(self, o) -> bool:
        if isinstance(o, OpenInterval):
            return self.lower >= o.upper
        elif isinstance(o, ClosedInterval):
            return self.lower > o.upper
        else:
            return self.lower > o

    def __neg__(self) -> "ClosedInterval":
        return ClosedInterval(-self.upper, -self.lower)

    def __str__(self) -> str:
        return f"[{self.lower:+03},{self.upper:+03}]"

    def __contains__(self, value: int) -> bool:
        return self.lower <= value <= self.upper

    def overlaps(self, o: OpenInterval) -> bool:
        "Check if this interval overlaps with another open interval"
        return self.upper > o.lower and self.lower < o.upper


def intersection(l, r):
    "Find the intersection of two intervals"
    if isinstance(l, OpenInterval) and isinstance(r, OpenInterval):
        return OpenInterval(max(l.lower, r.lower), min(l.upper, r.upper))
    if isinstance(l, ClosedInterval) and isinstance(r, ClosedInterval):
        return ClosedInterval(max(l.lower, r.lower), min(l.upper, r.upper))
    raise TypeError(f"Cannot intersect {type(l)} and {type(r)}")
