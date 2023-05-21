from pathlib import Path
from reversi import read_file

endgame = read_file(Path(__file__) / '..' / '..' / 'data' / 'endgame.pos')
