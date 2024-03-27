"Intensity of a search."
import struct
from dataclasses import dataclass


@dataclass
class Intensity:
    "Intensity class for representing the depth and the confidence value of a search."
    depth: int
    confidence_level: float = float("inf")

    @staticmethod
    def from_string(string: str) -> "Intensity":
        "Return an intensity from a string."
        if "@" in string:
            depth, confidence_level = string.split("@")
            if confidence_level.endswith("σ"):
                confidence_level = confidence_level[:-1]
            return Intensity(int(depth), float(confidence_level))
        else:
            return Intensity(int(string))
        
    @staticmethod
    def from_bytes(data: bytes) -> "Intensity":
        "Return an intensity from a bytes object."
        depth = int.from_bytes(data[:4], "big")
        confidence_level = struct.unpack("f", data[4:8])[0]
        return Intensity(depth, confidence_level)

    def __bytes__(self) -> bytes:
        depth = self.depth.to_bytes(4, "big")
        confidence_level = struct.pack("f", self.confidence_level)
        return depth + confidence_level

    def __str__(self) -> str:
        if self.is_exact():
            return f"{self.depth}"
        else:
            return f"{self.depth}@{self.confidence_level:3.1f}σ"

    def __eq__(self, o) -> bool:
        return self.depth == o.depth and self.confidence_level == o.confidence_level

    def __lt__(self, o) -> bool:
        return (self.depth < o.depth and self.confidence_level <= o.confidence_level) or (
            self.depth <= o.depth and self.confidence_level < o.confidence_level
        )

    def __gt__(self, o) -> bool:
        return (self.depth > o.depth and self.confidence_level >= o.confidence_level) or (
            self.depth >= o.depth and self.confidence_level > o.confidence_level
        )

    def __le__(self, o) -> bool:
        return self.depth <= o.depth and self.confidence_level <= o.confidence_level

    def __ge__(self, o) -> bool:
        return self.depth >= o.depth and self.confidence_level >= o.confidence_level

    def __add__(self, depth: int) -> "Intensity":
        return Intensity(self.depth + depth, self.confidence_level)

    def __sub__(self, depth: int) -> "Intensity":
        return Intensity(self.depth - depth, self.confidence_level)

    def is_exact(self) -> bool:
        "Return whether the intensity is exact."
        return self.confidence_level == float("inf")
