from numpy import uint64
from itertools import islice
from .bit_manipulation import cleared_lsb, countr_zero
from .field import Field


class Moves(uint64):
    
    class Iterator:
        def __init__(self, b: uint64):
            self.b = b

        def __next__(self):
            if self.b == 0:
                raise StopIteration
            move = countr_zero(self.b)
            self.b = cleared_lsb(self.b)
            return Field(move)

    def __str__(self) -> str:
        return ' '.join(move.name for move in self)

    def __new__(cls, b):
        return super(Moves, cls).__new__(cls, b)

    def __iter__(self):
        return self.Iterator(self)

    def __getitem__(self, index) -> int:
        return next(islice(self, index, None))

    def __len__(self) -> int:
        return self.bit_count()

    def __contains__(self, field: Field) -> bool:
        return self & (uint64(1) << uint64(field.value)) != 0
