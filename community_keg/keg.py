from __future__ import annotations
from typing import TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from game_manager import GameManager
    from models.player import Player


class Keg:
    def __init__(self, name: str, msg: str):
        self.name = name
        self.msg = msg
        self.logger = logging.getLogger("Drinkopoly")

    def Draw(self, gm: GameManager, player: Player) -> None:
        self.logger.debug(f"{player.name} Drew Keg: {self.name}")
        self.logger.debug(f'"{self.msg}"')
        return
