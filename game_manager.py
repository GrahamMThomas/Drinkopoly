from typing import List
from board.board_space import BoardSpace
from board.property import Property
from game_board import GameBoard
from models.player import Player


class GameManager:
    def __init__(self, players: List[Player], board: GameBoard):
        self.players = players
        self.board = board

    def DoRound(self):
        print("\n##### Round Start! #####")
        for player in self.players:
            roll_outcome = player.Roll()
            landed_space = self.board.move_player(roll_outcome, player)
            self.handle_space_activation(landed_space, player)
            print("---")

    def handle_space_activation(
        self, board_space: BoardSpace, offending_player: Player
    ) -> None:
        if isinstance(board_space, Property):
            if self.is_property_owned(
                board_space
            ) and not offending_player.OwnsProperty(board_space):
                offending_player.Drink(board_space.GetRentCost())
            elif offending_player.OwnsProperty(board_space):
                pass
            else:
                decision = offending_player.DecideToBuy(board_space)
                if decision:
                    offending_player.BuyProperty(board_space)

    def is_property_owned(self, the_property: Property) -> bool:
        return any([player.OwnsProperty(the_property) for player in self.players])
