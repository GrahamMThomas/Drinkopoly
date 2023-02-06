from board.board_space import BoardSpace


class QuestionMaster(BoardSpace):
    penalty = 0.25

    def __init__(self, name: str):
        super().__init__(name)
