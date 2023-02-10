from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager
    from models.player import Player
from board.board_space import BoardSpace


class Jail(BoardSpace):
    def __init__(self, name: str):
        super().__init__(name)

    def Visit(self, gm: GameManager, player: Player) -> None:
        super().Visit(gm, player)
        for incarcerated_player in gm.players:
            if incarcerated_player.in_jail:
                self.logger.debug(f"{incarcerated_player.name} is no longer in Jail!")
                incarcerated_player.in_jail = False
        return
