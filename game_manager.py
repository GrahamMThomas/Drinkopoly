import random
from typing import List
from board.question_master import QuestionMaster
from game_board import GameBoard
from models.player import Player


class GameManager:
    def __init__(self, players: List[Player], board: GameBoard):
        self.players = players
        self.board = board

    def DoRound(self, i):
        print(f"\n##### Round {i} Start! #####")

        for player in self.players:
            if player.has_lost:
                print(f"{player.name} has lost.")
                continue

            if player.in_jail:
                print(f"{player.name} is in the DRUNK TANK!")
                continue

            if player.is_question_master:
                loser = random.choice(self.players)
                if loser != player:
                    print(f"{loser.name} answered {player.name}'s question")
                    loser.Drink(QuestionMaster.penalty)

            roll_outcome = player.Roll()
            visited_spaces = self.board.move_player(roll_outcome, player)

            for visited_space in visited_spaces:
                visited_space.Visit(self, player)

            landed_space = visited_spaces[-1]
            landed_space.Land(self, player)
            print("---")
