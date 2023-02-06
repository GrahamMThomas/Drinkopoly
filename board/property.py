from board.board_space import BoardSpace
from models.setColors import SetColors


class Property(BoardSpace):
    def __init__(self, name: str, purchase_cost: int, color: SetColors):
        super().__init__(name)
        self.purchase_cost = purchase_cost
        self.house_count = 0
        self.color_code = color

    def GetRentCost(self) -> int:
        return self.purchase_cost
