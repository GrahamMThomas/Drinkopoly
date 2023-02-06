from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager
    from models.player import Player


class BoardSpace:
    def __init__(self, name: str):
        self.name = name

    def Land(self, gm: GameManager, player: Player) -> None:
        print(f"{player.name} landed on {self.name}")
        pass

    def Visit(self, gm: GameManager, player: Player) -> None:
        pass
