from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager
    from models.player import Player
from board.board_space import BoardSpace


class LuxuryTax(BoardSpace):
    def __init__(self, name: str):
        super().__init__(name)

    def Land(self, gm: GameManager, player: Player):
        super().Land(gm, player)
        if player.drink_tokens < 0:
            return
        drink_token_to_lose = max(round(player.drink_tokens / 3), 1)
        player.YoinkDrinkTokens(drink_token_to_lose)
        return
