from __future__ import annotations
import logging
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
        self.logger = logging.getLogger("Drinkopoly")
        self.purchase_cost = purchase_cost
        self.house_count = 0
        self.house_cost = 0.5
        self.color_code = color
        self.owner: Player = None
        self.set_property_count = 1

    def GetRentCost(self) -> int:
        # 1.75 Exponential -> Boardwalk 3 hours = 9oz
        exponent = 1.75 if self.color_code != SetColors.SINGLE else 1.25
        raw_rent_cost = (self.purchase_cost * 0.2) * (self.house_count + 1) ** exponent
        rounded_rent_cost = round(raw_rent_cost * 4) / 4
        return rounded_rent_cost

    def IsOwned(self):
        return self.owner is not None

    def Land(self, gm: GameManager, player: Player):
        super().Land(gm, player)
        if self.IsOwned() and self.owner != player:
            rentCost = self.GetRentCost()
            self.logger.debug(f"\t{self.house_count} Houses: {rentCost:.2f} oz")
            player.Drink(rentCost)
        elif self.owner == player:
            pass
        else:
            decision = player.DecideToBuy(self)
            if decision:
                player.BuyProperty(self)
        return
