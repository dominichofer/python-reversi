import time
from reversi import *

fforum_1 = Position.from_string('--XXXXX--OOOXX-O-OOOXXOX-OXOXOXXOXXXOXXX--XOXOXX-XXXOOO--OOOOO-- X')

start = time.perf_counter()
for _ in range(1_000):
    possible_moves(fforum_1)
end = time.perf_counter()
print('possible_moves: {:.1f} us'.format((end - start) * 1_000))

start = time.perf_counter()
for _ in range(1_000):
    flips(fforum_1, Field.G8)
end = time.perf_counter()
print('flips: {:.1f} us'.format((end - start) * 1_000))

start = time.perf_counter()
for _ in range(1_000):
    play(fforum_1, Field.G8)
end = time.perf_counter()
print('play: {:.1f} us'.format((end - start) * 1_000))

start = time.perf_counter()
for _ in range(1_000):
    play_pass(fforum_1)
end = time.perf_counter()
print('play_pass: {:.1f} us'.format((end - start) * 1_000))

start = time.perf_counter()
for _ in range(1_000):
    end_score(fforum_1)
end = time.perf_counter()
print('end_score: {:.1f} us'.format((end - start) * 1_000))
