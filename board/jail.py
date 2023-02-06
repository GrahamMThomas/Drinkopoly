from board.board_space import BoardSpace


class Jail(BoardSpace):
    def __init__(self, name: str):
        super().__init__(name)
