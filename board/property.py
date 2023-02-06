from board.board_space import BoardSpace


class Property(BoardSpace):
    def __init__(self, name: str, purchase_cost: int):
        super().__init__(name, "#FFFFFF")
        self.purchase_cost = purchase_cost
        self.house_count = 0

    def GetRentCost(self) -> int:
        return self.purchase_cost
