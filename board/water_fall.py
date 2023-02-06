from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager
    from models.player import Player
from board.board_space import BoardSpace


class WaterFall(BoardSpace):
    def __init__(self, name: str, penalty: float):
        super().__init__(name)
        self.penalty: float = penalty

    def Land(self, gm: GameManager, player: Player):
        super().Land(gm, player)
        player_index = self.players.index(player)
        waterfall_amount = self.penalty
        for i in range(0, len(self.players)):
            self.players[(player_index + i) % len(self.players)].Drink(waterfall_amount)
            waterfall_amount += self.penalty
        return
