from dataclasses import dataclass


@dataclass
class Interval:
    lower: int
    upper: int
    
    def __eq__(self, o) -> bool:
        return self.lower == o.lower and self.upper == o.upper

    def __neg__(self):
        return type(self)(-self.upper, -self.lower)


class OpenInterval(Interval):
    def __str__(self) -> str:
        return f'({self.lower:+03},{self.upper:+03})'

    def __lt__(self, value: int) -> bool:
        return self.upper <= value

    def __gt__(self, value: int) -> bool:
        return self.lower >= value


class ClosedInterval(Interval):
    def __str__(self) -> str:
        return f'[{self.lower:+03},{self.upper:+03}]'

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

    def __contains__(self, value: int) -> bool:
        return self.lower <= value <= self.upper

    def overlaps(self, o: OpenInterval) -> bool:
        return self.upper > o.lower and self.lower < o.upper
