import random
from typing import List, TYPE_CHECKING

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from game_board import GameBoard, BoardSpace, Property


def main():
    board = GameBoard()
    board_spaces: List[BoardSpace] = board.get_properties()
    properties = [x for x in board_spaces if isinstance(x, Property)]
    chosen = random.choice(properties)
    print(chosen.name)


if __name__ == "__main__":
    main()
