from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager
    from models.player import Player

from community_keg.keg import Keg


class BarErrorInYourFavor(Keg):
    amount_of_drink_tokens_to_give = 1

    def __init__(self):
        name = "Bar Error In Your Favor"
        msg = f"There was a bar error in your favor, collect {self.amount_of_drink_tokens_to_give} drink token"
        super().__init__(name, msg)

    def Draw(self, gm: GameManager, player: Player) -> None:
        super().Draw(gm, player)
        player.EarnDrinkTokens(self.amount_of_drink_tokens_to_give)
        return
