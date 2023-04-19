from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_manager import GameManager
    from models.player import Player
from board.board_space import BoardSpace


class SquattersRights(BoardSpace):
    def __init__(self, name: str):
        super().__init__(name)

    def Land(self, gm: GameManager, player: Player):
        super().Land(gm, player)
        prop_to_squat = player.DecideWhichPropToSquat(gm.board)
        if prop_to_squat is None:
            self.logger.debug(f"No property to squat.")
            return

        if (
            player.DecideToBuy(prop_to_squat, True, player.DRINK_TOKEN_CONVERSION_RATE)
            and player.drink_tokens > 0
        ):
            self.logger.debug(f"{prop_to_squat.name} is getting squated from {prop_to_squat.owner.name}")
            player.YoinkDrinkTokens(1)
            prop_to_squat.owner.EarnDrinkTokens(1)
            prop_to_squat.ReleaseOwnership()
            player.BuyProperty(prop_to_squat)
        else:
            self.logger.debug("Too broke to squat")
        return
