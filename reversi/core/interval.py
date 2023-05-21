from dataclasses import dataclass

    
@dataclass
class OpenInterval:
    lower: int
    upper: int

    def __str__(self) -> str:
        return f'({self.lower:+03},{self.upper:+03})'

    def __eq__(self, o) -> bool:
        return self.lower == o.lower and self.upper == o.upper

    def __lt__(self, value: int) -> bool:
        return self.upper <= value

    def __gt__(self, value: int) -> bool:
        return self.lower >= value

    def __neg__(self):
        return OpenInterval(-self.upper, -self.lower)

    
@dataclass
class ClosedInterval:
    lower: int
    upper: int

    def __str__(self) -> str:
        return f'[{self.lower:+03},{self.upper:+03}]'

    def __eq__(self, o) -> bool:
        return self.lower == o.lower and self.upper == o.upper

    def __lt__(self, o) -> bool:
        if isinstance(o, int):
            return self.upper < o
        if isinstance(o, OpenInterval):
            return self.upper <= o.lower
        if isinstance(o, ClosedInterval):
            return self.upper < o.lower

    def __gt__(self, o) -> bool:
        if isinstance(o, int):
            return self.lower > o
        if isinstance(o, OpenInterval):
            return self.lower >= o.upper
        if isinstance(o, ClosedInterval):
            return self.lower > o.upper

    def __neg__(self):
        return ClosedInterval(-self.upper, -self.lower)

    def __contains__(self, value: int) -> bool:
        return self.lower <= value <= self.upper

    def overlaps(self, o: OpenInterval) -> bool:
        return self.upper >= o.lower and self.lower <= o.upper
