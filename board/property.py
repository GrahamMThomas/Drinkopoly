from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager
    from models.player import Player
from board.board_space import BoardSpace
from models.setColors import SetColors


class Property(BoardSpace):
    MAX_HOUSE_COUNT: int = 3

    def __init__(self, name: str, purchase_cost: int, color: SetColors):
        super().__init__(name)
        self.purchase_cost = purchase_cost
        self.house_count = 0
        self.house_cost = 0.5
        self.color_code = color
        self.owner: Player = None

    def GetRentCost(self) -> int:
        return self.purchase_cost

    def IsOwned(self):
        return self.owner is not None

    def Land(self, gm: GameManager, player: Player):
        super().Land(gm, player)
        if self.IsOwned() and self.owner != player:
            player.Drink(self.GetRentCost())
        elif self.owner == player:
            pass
        else:
            decision = player.DecideToBuy(self)
            if decision:
                player.BuyProperty(self)
        return

    def BuyHouse(self) -> bool:
        if self.house_count >= self.MAX_HOUSE_COUNT:
            return False
        self.owner.Drink(self.house_cost)
        self.house_count += 1
        return True
