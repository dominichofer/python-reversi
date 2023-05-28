import time
from reversi import *

def benchmark(name: str, fkt) -> None:
    fforum_1 = Position.from_string('--XXXXX--OOOXX-O-OOOXXOX-OXOXOXXOXXXOXXX--XOXOXX-XXXOOO--OOOOO-- X')

    start = time.perf_counter()
    for _ in range(1_000):
        fkt(fforum_1)
    end = time.perf_counter()
    diff = (end - start) * 1_000
    print(f'{name}: {diff:.1f} us')

    
benchmark('flips', lambda pos: flips(pos, Field.G8))
benchmark('play', lambda pos: play(pos, Field.G8))
benchmark('play_pass', play_pass)
benchmark('end_score', end_score)


tt = SpecialKey_1Hash_HashTable([b'00000000']*8, b'0000')
start = time.perf_counter()
for _ in range(1_000):
    tt.insert(b'0001', b'0001')
    tt.look_up(b'0001')
    tt.look_up(b'0002')
end = time.perf_counter()
diff = (end - start) * 1_000
print(f'Hashtable: {diff:.1f} us')
