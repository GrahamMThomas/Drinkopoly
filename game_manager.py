import random
from typing import List
from board.question_master import QuestionMaster
from game_board import GameBoard
from models.player import Player
import logging


class GameManager:
    def __init__(self, players: List[Player], board: GameBoard):
        self.players = players
        self.board = board
        self.logger = logging.getLogger("Drinkopoly")

    def DoRound(self, i):
        self.logger.debug(f"\n##### Round {i} Start! #####")

        for player in self.players:
            if player.has_lost:
                self.logger.debug(f"{player.name} has lost.")
                continue

            if player.in_jail:
                self.logger.debug(f"{player.name} is in the DRUNK TANK!")
                continue

            if player.is_question_master:
                loser = random.choice(self.players)
                if loser != player:
                    self.logger.debug(f"{loser.name} answered {player.name}'s question")
                    loser.Drink(QuestionMaster.penalty)

            player.BuyHousesIfDesired()

            roll_outcome = player.Roll()
            visited_spaces = self.board.move_player(roll_outcome, player)

            for visited_space in visited_spaces:
                visited_space.Visit(self, player)

            landed_space = visited_spaces[-1]
            landed_space.Land(self, player)
            self.logger.debug("---")
