from board.board_space import BoardSpace


class WaterFall(BoardSpace):
    def __init__(self, name: str, penalty: float):
        super().__init__(name)
        self.penalty: float = penalty
