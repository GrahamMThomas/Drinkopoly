from __future__ import annotations
from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from game_manager import GameManager
    from models.player import Player


class BoardSpace:
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger("Drinkopoly")

    def Land(self, gm: GameManager, player: Player) -> None:
        self.logger.debug(f"{player.name} landed on {self.name}")
        pass

    def Visit(self, gm: GameManager, player: Player) -> None:
        pass
