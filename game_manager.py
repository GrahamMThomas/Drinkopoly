import random
from typing import List
from board.board_space import BoardSpace
from board.drunken_drive import DrunkenDrive
from board.go_to_jail import GoToJail
from board.jail import Jail
from board.property import Property
from board.question_master import QuestionMaster
from board.water_fall import WaterFall
from game_board import GameBoard
from models.player import Player


class GameManager:
    def __init__(self, players: List[Player], board: GameBoard):
        self.players = players
        self.board = board

    def DoRound(self):
        print("\n##### Round Start! #####")
        for player in self.players:
            if player.in_jail:
                print(f"{player.name} is in the DRUNK TANK!")
                continue
                # TODO: Figure out a way to get them out.
            if player.is_question_master:
                loser = random.choice(self.players)
                if loser != player:
                    print(f"{loser.name} answered {player.name}'s question")
                    loser.Drink(QuestionMaster.penalty)
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
            return

        elif isinstance(board_space, Jail):
            return

        elif isinstance(board_space, GoToJail):
            self.board.teleport_player("Go To Jail", offending_player)
            return

        elif isinstance(board_space, WaterFall):
            player_index = self.players.index(offending_player)
            waterfall_amount = board_space.penalty
            for i in range(0, len(self.players)):
                self.players[(player_index + i) % len(self.players)].Drink(
                    waterfall_amount
                )
                waterfall_amount += board_space.penalty
            return

        elif isinstance(board_space, DrunkenDrive):
            loser = random.choice(self.players)
            loser.Drink(board_space.penalty)
            return

        elif isinstance(board_space, QuestionMaster):
            offending_player.is_question_master = True
            return

        else:
            print(f"Unhandled space {board_space.name}")
            # raise Exception(f"Unhandled space {board_space.name}")

    def is_property_owned(self, the_property: Property) -> bool:
        return any([player.OwnsProperty(the_property) for player in self.players])
