from __future__ import annotations
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager
    from models.player import Player
from board.board_space import BoardSpace


class DrunkenDrive(BoardSpace):
    def __init__(self, name: str, penalty: float):
        super().__init__(name)
        self.penalty: float = penalty

    def Land(self, gm: GameManager, player: Player):
        super().Land(gm, player)
        loser = random.choice(gm.players)
        loser.Drink(self.penalty)
        return
