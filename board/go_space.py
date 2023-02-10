from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager
    from models.player import Player
from board.board_space import BoardSpace


class GoSpace(BoardSpace):
    def __init__(self, name: str):
        super().__init__(name)

    def Visit(self, gm: GameManager, player: Player) -> None:
        super().Visit(gm, player)
        self.logger.debug(f"{player.name} passed Go!")
        player.EarnDrinkTokens(1)
        if player.is_question_master:
            self.logger.debug(f"{player.name} is no longer Question Master.")
            player.is_question_master = False
        return

    def Land(self, gm: GameManager, player: Player) -> None:
        super().Land(gm, player)
        player.EarnDrinkTokens(2)
        return
