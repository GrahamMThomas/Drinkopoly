from __future__ import annotations
from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    # from game_manager import GameManager
    from models.player import Player


class KingsCup:
    def __init__(self) -> None:
        self.alcohol_amount = 0  # oz
        self.logger = logging.getLogger("Drinkopoly")

    def Pour(self, player: Player, pour_amount: float):
        self.logger.debug(f"{player.name} poured {pour_amount:.2f} into Kings Cup")
        self.alcohol_amount += pour_amount
        player.alcohol_remaining -= min(pour_amount, player.alcohol_remaining)
        player.CheckIfLost()

    def Empty(self, player: Player):
        self.logger.debug(
            f"{player.name} drank the Kings Cup ({self.alcohol_amount} oz)!"
        )
        player.total_oz_drank += self.alcohol_amount
        player.CheckIfLost()
        self.alcohol_amount = 0
