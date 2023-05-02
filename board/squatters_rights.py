from __future__ import annotations
from random import randrange
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
            self.logger.debug(f"No property to squat. Teleporting instead")
            railroads = [
                gm.board.get_board_space_by_name("Whiskey Express"),
                gm.board.get_board_space_by_name("Squatter's Rights"),
                gm.board.get_board_space_by_name("D. U I. Railroad"),
                gm.board.get_board_space_by_name("Lads Lane"),
            ]
            chosen_space = railroads[randrange(0, len(railroads) - 1)]
            self.logger.debug(f"Teleporting to a random railroad: {chosen_space.name}")
            gm.board.teleport_player(chosen_space.name, player)
            chosen_space.Land(gm, player)
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
