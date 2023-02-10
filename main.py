import sys
from game_board import GameBoard
from game_manager import GameManager
from models.player import Player
from collections import defaultdict
import statistics
import logging


def Main():
    logger = logging.getLogger("Drinkopoly")
    format = logging.Formatter("%(message)s")
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(format)
    logger.addHandler(ch)

    round_numbers = []
    player_drink_amounts = defaultdict(lambda: [])
    player_question_masters = defaultdict(lambda: [])
    player_jails = defaultdict(lambda: [])
    player_win_counts = defaultdict(lambda: 0)

    game_count = 500
    if game_count == 1:
        logger.setLevel(logging.DEBUG)

    for i in range(game_count):
        players = [
            Player("Pansy", 12, True),
            Player("SmallBoi", 18, True),
            Player("Larry", 24, False),
            Player("Anthony", 36, False),
        ]
        board = GameBoard()

        for player in players:
            board.add_player_to_board(player)
        gm = GameManager(players, board)

        round_number = 1
        while True:
            gm.DoRound(round_number)
            if (
                sum([1 for player in players if player.has_lost]) >= len(players) - 1
                or round_number > 200
            ):
                if game_count != 1:
                    break
                print("\n\nGame over!")
                print("Stats -------------------------")
                print(f"Rounds played: {round_number}")
                print(
                    f"Time Spent: {round_number*2//60} Hours and {round_number*2 % 60} Minutes"
                )

                for player in players:
                    print(f"{player.name}:")
                    print(f"\tAlcohol Drank: {player.total_oz_drank:.2f}")
                    print(f"\tArrests: {player.times_in_jail}")
                    print(f"\tQuestion Master: {player.times_question_master}")
                break
            round_number += 1
        round_numbers.append(round_number)
        for player in players:
            player_drink_amounts[player.name].append(player.total_oz_drank)
            player_question_masters[player.name].append(player.times_question_master)
            player_jails[player.name].append(player.times_in_jail)
            if not player.has_lost:
                player_win_counts[player.name] += 1

    if game_count == 1:
        return

    print(f"After {game_count} games:")
    print(f"Round Count Avg: {statistics.mean(round_numbers):.2f}")
    print(f"Round Count Std: {statistics.stdev(round_numbers):.2f}")
    for player in players:
        print(f"\n{player.name}")
        print(f"Avg Drank: {statistics.mean(player_drink_amounts[player.name]):.2f}")
        print(f"Std Drank: {statistics.stdev(player_drink_amounts[player.name]):.2f}")
        print(f"Avg QMs: {statistics.mean(player_question_masters[player.name]):.2f}")
        print(f"Avg Jails: {statistics.mean(player_jails[player.name]):.2f}")
        print(f"Wins: {player_win_counts[player.name]}")


if __name__ == "__main__":
    Main()
