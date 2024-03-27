import unittest
import edax
from reversi import Field, Position, Intensity  # type: ignore
from reversi.engine.edax import EdaxLine, Edax  # type: ignore


class EdaxOutputTest(unittest.TestCase):
    def test_exact_depth(self):
        line = edax.Line(
            "  7|   24   -08        0:00.234      63133975  269803312 b3 C1 b1 A3 b2 H3 a5"
        )
        line = EdaxLine.from_edax_line(line)
        self.assertEqual(line.index, 7)
        self.assertEqual(line.intensity, Intensity(24))
        self.assertEqual(line.score, -8)
        self.assertEqual(line.time, "0:00.234")
        self.assertEqual(line.nodes, 63133975)
        self.assertEqual(line.nodes_per_second, 269803312)
        self.assertEqual(
            line.pv,
            [Field.B3, Field.C1, Field.B1, Field.A3, Field.B2, Field.H3, Field.A5],
        )
        self.assertEqual(line.best_move, Field.B3)
        self.assertEqual(
            str(line),
            "\n".join(
                [
                    "index: 7",
                    "intensity: d24",
                    "score: -08",
                    "time: 0:00.234",
                    "nodes: 63'133'975",
                    "nodes_per_second: 269'803'312 N/s",
                    "pv: B3 C1 B1 A3 B2 H3 A5",
                    "best_move: B3",
                    "result: [-08,-08] d24 B3",
                ]
            ),
        )
        new_line = EdaxLine.from_bytes(bytes(line))
        self.assertEqual(new_line, line)

    def test_depth_selectivity(self):
        line = edax.Line(
            "  8|25@98%  +03        0:00.094       9940593  105750989 G2 b8 B7 a2 A5 b2 G3"
        )
        line = EdaxLine.from_edax_line(line)
        self.assertEqual(line.index, 8)
        self.assertEqual(line.intensity, Intensity(25, 2.6))
        self.assertEqual(line.score, +3)
        self.assertEqual(line.time, "0:00.094")
        self.assertEqual(line.nodes, 9940593)
        self.assertEqual(line.nodes_per_second, 105750989)
        self.assertEqual(
            line.pv,
            [Field.G2, Field.B8, Field.B7, Field.A2, Field.A5, Field.B2, Field.G3],
        )
        self.assertEqual(line.best_move, Field.G2)
        self.assertEqual(
            str(line),
            "\n".join(
                [
                    "index: 8",
                    "intensity: d25@2.6σ",
                    "score: +03",
                    "time: 0:00.094",
                    "nodes: 9'940'593",
                    "nodes_per_second: 105'750'989 N/s",
                    "pv: G2 B8 B7 A2 A5 B2 G3",
                    "best_move: G2",
                    "result: [+03,+03] d25@2.6σ G2",
                ]
            ),
        )
        new_line = EdaxLine.from_bytes(bytes(line))
        self.assertEqual(new_line, line)

    def test_no_nodes_per_second(self):
        line = edax.Line(
            "  1|   14   +18        0:00.000         95959            g8 H7 a8 A6 a4 A7 b6"
        )
        line = EdaxLine.from_edax_line(line)
        self.assertEqual(line.index, 1)
        self.assertEqual(line.intensity, Intensity(14))
        self.assertEqual(line.score, +18)
        self.assertEqual(line.time, "0:00.000")
        self.assertEqual(line.nodes, 95959)
        self.assertEqual(line.nodes_per_second, None)
        self.assertEqual(
            line.pv,
            [Field.G8, Field.H7, Field.A8, Field.A6, Field.A4, Field.A7, Field.B6],
        )
        self.assertEqual(line.best_move, Field.G8)
        self.assertEqual(
            str(line),
            "\n".join(
                [
                    "index: 1",
                    "intensity: d14",
                    "score: +18",
                    "time: 0:00.000",
                    "nodes: 95'959",
                    "nodes_per_second: ? N/s",
                    "pv: G8 H7 A8 A6 A4 A7 B6",
                    "best_move: G8",
                    "result: [+18,+18] d14 G8",
                ]
            ),
        )
        new_line = EdaxLine.from_bytes(bytes(line))
        self.assertEqual(new_line, line)

    def test_pass(self):
        line = edax.Line("  7|   24   -08        0:00.234      63133975  269803312 ps")
        line = EdaxLine.from_edax_line(line)
        self.assertEqual(line.index, 7)
        self.assertEqual(line.intensity, Intensity(24))
        self.assertEqual(line.score, -8)
        self.assertEqual(line.time, "0:00.234")
        self.assertEqual(line.nodes, 63133975)
        self.assertEqual(line.nodes_per_second, 269803312)
        self.assertEqual(line.pv, [Field.PS])
        self.assertEqual(line.best_move, Field.PS)
        self.assertEqual(
            str(line),
            "\n".join(
                [
                    "index: 7",
                    "intensity: d24",
                    "score: -08",
                    "time: 0:00.234",
                    "nodes: 63'133'975",
                    "nodes_per_second: 269'803'312 N/s",
                    "pv: PS",
                    "best_move: PS",
                    "result: [-08,-08] d24 PS",
                ]
            ),
        )
        new_line = EdaxLine.from_bytes(bytes(line))
        self.assertEqual(new_line, line)


class EdaxTest(unittest.TestCase):
    def setUp(self) -> None:
        self.pos = Position.from_string(
            "--XXXXX--OOOXX-O-OOOXXOX-OXOXOXXOXXXOXXX--XOXOXX-XXXOOO--OOOOO-- X"
        )
        self.multi_pos = [
            "--XXXXX--OOOXX-O-OOOXXOX-OXOXOXXOXXXOXXX--XOXOXX-XXXOOO--OOOOO-- X",
            "-XXXXXX---XOOOO--XOXXOOX-OOOOOOOOOOOXXOOOOOXXOOX--XXOO----XXXXX- X",
            "----OX----OOXX---OOOXX-XOOXXOOOOOXXOXXOOOXXXOOOOOXXXXOXO--OOOOOX X",
        ]
        self.score = +18
        self.multi_score = [+18, +10, +2]

    def test_solve_native_single_process_single_pos(self):
        engine = Edax()
        result = engine.solve_native(self.pos)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].score, self.score)

    def test_solve_native_single_process_multi_pos(self):
        engine = Edax()
        result = engine.solve_native(self.multi_pos)
        self.assertEqual(len(result), 3)
        self.assertEqual([x.score for x in result], self.multi_score)

    def test_solve_native_multi_process_single_pos(self):
        engine = Edax(multiprocess=True)
        result = engine.solve_native(self.pos)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].score, self.score)

    def test_solve_native_multi_process_multi_pos(self):
        engine = Edax(multiprocess=True)
        result = engine.solve_native(self.multi_pos)
        self.assertEqual(len(result), 3)
        self.assertEqual([x.score for x in result], self.multi_score)
