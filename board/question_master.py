from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager
    from models.player import Player
from board.board_space import BoardSpace


class QuestionMaster(BoardSpace):
    penalty = 0.25

    def __init__(self, name: str):
        super().__init__(name)

    def Land(self, gm: GameManager, player: Player):
        super().Land(gm, player)
        player.is_question_master = True
        player.times_question_master += 1
        return
