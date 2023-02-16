import random
from typing import List
from board.question_master import QuestionMaster
from game_board import GameBoard
from keg_deck import KegDeck
from mechanics.kings_cup import KingsCup
from models.player import Player
import logging


class GameManager:
    def __init__(self, players: List[Player], board: GameBoard):
        self.players = players
        self.board = board
        self.logger = logging.getLogger("Drinkopoly")
        self.kings_cup = KingsCup()
        self.keg_deck = KegDeck()

    def DoRound(self, i):
        self.logger.debug(f"\n##### Round {i} Start! #####")

        for player in self.players:
            if player.has_lost:
                # If we haven't set lost round, assume they lost last round.
                if player.lost_round == 0:
                    player.lost_round = i - 1
                continue
            self.logger.debug(f"{player.name}:")
            self.logger.debug(f"\t{player.drink_tokens} drink tokens.")
            self.logger.debug(f"\t{player.alcohol_remaining:.2f} alcohol left.")
            self.logger.debug(
                f"\t{player.total_oz_drank:.2f} of {player.drinking_capacity:.2f} drinking capacity."
            )
            self.logger.debug(f"\t{len(player.owned_properties)} properties.")
            self.logger.debug(
                f"\t{sum([x.house_count for x in player.owned_properties])} houses."
            )

            if player.in_jail:
                self.logger.debug(f"{player.name} is in the DRUNK TANK!")
                if player.turns_in_jail == 3:
                    player.SetFree()
                else:
                    player.turns_in_jail += 1
                    player.total_turns_in_jail += 1
                    self.logger.debug("---")
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
