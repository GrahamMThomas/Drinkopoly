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

    def __init__(self, name: str, purchase_cost: float, color: SetColors):
        super().__init__(name)
        self.logger = logging.getLogger("Drinkopoly")
        self.purchase_cost = purchase_cost
        self.house_count = 0
        self.color_code = color
        self.owner: Player = None
        self.set_property_count = 1
        self.house_cost = self.DetermineHouseCost()

    def GetRentCost(self, override_house_count: int = None) -> float:
        # 1.75 Exponential -> Boardwalk 3 hours = 9oz
        exponent = 1.75 if self.color_code != SetColors.SINGLE else 1.25
        house_count_temp = self.house_count if override_house_count is None else override_house_count
        raw_rent_cost = (self.purchase_cost * 0.2) * (house_count_temp + 1) ** exponent
        rounded_rent_cost = round(raw_rent_cost * 4) / 4
        return rounded_rent_cost

    def IsOwned(self):
        return self.owner is not None

    def ReleaseOwnership(self):
        self.owner = None
        self.house_count = 0
        self.logger.debug(f"{self.name} has been Released!")

    def Land(self, gm: GameManager, player: Player):
        super().Land(gm, player)
        self.logger.debug(f"\tOwned by: {'nobody' if self.owner is None else self.owner.name}")
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

    def DetermineHouseCost(self) -> float:
        if self.color_code == SetColors.SINGLE:
            return 1
        raw_house_cost = self.purchase_cost * 0.50
        raw_house_cost = max(raw_house_cost, 1)
        return round(raw_house_cost * 4) / 4
