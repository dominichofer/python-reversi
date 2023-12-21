"Benchmarking the functions in reversi.py"
import time
from reversi import Position, Field, possible_moves, play, play_pass, end_score, perft


def benchmark(name: str, fkt) -> None:
    "Benchmark the function `fkt` with the name `name`."
    fforum_1 = Position.from_string(
        "--XXXXX--OOOXX-O-OOOXXOX-OXOXOXXOXXXOXXX--XOXOXX-XXXOOO--OOOOO-- X"
    )

    start = time.perf_counter()
    for _ in range(1_000):
        fkt(fforum_1)
    end = time.perf_counter()
    diff = (end - start) * 1_000
    print(f"{name}: {diff:.1f} us")


if __name__ == "__main__":
    benchmark("possible_moves", possible_moves)
    benchmark("play", lambda pos: play(pos, Field.G8))
    benchmark("play_pass", play_pass)
    benchmark("end_score", end_score)

    for i in range(8):
        start = time.perf_counter()
        value = perft(i)
        end = time.perf_counter()
        diff = end - start
        print(f"perft({i}): {diff:.1f} s")
