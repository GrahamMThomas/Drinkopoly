from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager
    from models.player import Player

from community_keg.keg import Keg


class SpiltBeer(Keg):
    pour_amount = 1.5

    def __init__(self):
        name = "Spilt Beer"
        message = f"Ohhh noooo! You spilt {self.pour_amount:.2f} oz of beer into the kings cup."
        super().__init__(name, message)

    def Draw(self, gm: GameManager, player: Player) -> None:
        super().Draw(gm, player)
        gm.kings_cup.Pour(player, self.pour_amount)
        return
