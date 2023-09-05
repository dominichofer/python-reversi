import time
from reversi import *

empty_key = Position()
ht = SpecialKey_1Hash_HashTable([(empty_key, None) for _ in range(1_000_000)], empty_key)
tt = Updating_HashTable(ht)
sorter = mobility_and_tt_sorter(tt)
cutters = [
    tt_cutter(tt),
    edax_cutter(r'G:\edax-ms-windows\edax-4.4', max_depth=64),
    ]

fforum = read_file(r'C:\Users\Dominic\source\repos\python-reversi\data\fforum-60-79.pos')
for ff in fforum:
    start = time.perf_counter()
    score = PrincipalVariation(tt, sorter, cutters).eval(ff.pos).score
    end = time.perf_counter()
    diff = (end - start)
    print(f'{score=} {ff.score} {diff:.1f} s')