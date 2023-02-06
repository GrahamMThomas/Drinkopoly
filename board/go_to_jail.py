from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager
    from models.player import Player
from board.board_space import BoardSpace


class GoToJail(BoardSpace):
    def __init__(self, name: str):
        super().__init__(name)

    def Land(self, gm: GameManager, player: Player):
        super().Land(gm, player)
        gm.board.teleport_player("Go To Jail", player)
        player.times_in_jail += 1
        return
