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
        # Weird bug no clue why it's happening
        if player.has_lost:
            return
        super().Land(gm, player)
        players = [x for x in gm.players if not x.has_lost]
        # print([(x.name, x.has_lost) for x in gm.players])
        # print([x.name for x in players])
        # print(player.name)
        player_index = players.index(player)
        waterfall_amount = self.penalty
        for i in range(0, len(players)):
            players[(player_index + i) % len(players)].Drink(waterfall_amount)
            waterfall_amount += self.penalty
        return
