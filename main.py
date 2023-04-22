import sys
from game_board import GameBoard
from game_manager import GameManager
from models.lostReasons import LostReasons
from models.player import Player
from collections import defaultdict
import statistics
import logging
from matplotlib import pyplot as plt


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
    player_turns_in_jail = defaultdict(lambda: [])
    player_win_counts = defaultdict(lambda: 0)
    player_loss_reasons = defaultdict(lambda: [])
    player_loss_round_counts = defaultdict(lambda: [])

    game_count = 2000
    # game_count = 1
    if game_count == 1:
        logger.setLevel(logging.DEBUG)

    for i in range(game_count):
        players = [
            Player("Pansy", 12, True),
            Player("SmallBoi", 24, True),
            Player("Larry", 36, False),
            Player("Larry2", 36, False),
            Player("Larry3", 36, False),
            Player("Anthony", 60, False),
        ]
        players[0].EarnDrinkTokens(3)
        players[1].EarnDrinkTokens(1)
        board = GameBoard()
        if i == 0:
            board.rent_roll_call()

        for player in players:
            board.add_player_to_board(player)
        gm = GameManager(players, board)

        round_number = 1
        while True:
            gm.DoRound(round_number)
            if sum([1 for player in players if player.has_lost]) >= len(players) - 1 or round_number > 200:
                for player in players:
                    if player.has_lost and player.lost_round == 0:
                        player.lost_round = round_number

                should_print_stats = False  # round_number > 50

                if game_count != 1 and not should_print_stats:
                    break
                print("\n\nGame over!")
                print("Stats -------------------------")
                print(f"Rounds played: {round_number}")
                print(f"Time Spent: {round_number*2//60} Hours and {round_number*2 % 60} Minutes")

                for player in players:
                    print(f"{player.name}:")
                    print(f"\tAlcohol Drank: {player.total_oz_drank:.2f}")
                    print(f"\tArrests: {player.times_in_jail}")
                    print(f"\tQuestion Master: {player.times_question_master}")
                    print(f"\tTurns in Jail: {player.total_turns_in_jail}")
                    if player.has_lost:
                        print(f"\tLoss Turn: {player.lost_round}")
                # exit(0)
                break
            round_number += 1
        round_numbers.append(round_number)
        for player in players:
            player_drink_amounts[player.name].append(player.total_oz_drank)
            player_question_masters[player.name].append(player.times_question_master)
            player_jails[player.name].append(player.times_in_jail)
            player_turns_in_jail[player.name].append(player.total_turns_in_jail)
            if not player.has_lost:
                player_win_counts[player.name] += 1
            else:
                player_loss_reasons[player.name].append(player.lost_reason)
                player_loss_round_counts[player.name].append(player.lost_round)

    if game_count == 1:
        return

    print(f"After {game_count} games:")
    print(f"Round Count Avg: {statistics.mean(round_numbers):.2f}")
    print(f"Round Count Std: {statistics.stdev(round_numbers):.2f}")

    plt.hist(round_numbers, 25)
    plt.show()
    for player in players:
        print(f"\n{player.name}")
        print(f"Avg Drank: {statistics.mean(player_drink_amounts[player.name]):.2f}")
        print(f"Std Drank: {statistics.stdev(player_drink_amounts[player.name]):.2f}")
        print(f"Avg QMs: {statistics.mean(player_question_masters[player.name]):.2f}")
        print(f"Avg Jails: {statistics.mean(player_jails[player.name]):.2f}")
        print(f"Avg Turns in Jail: {statistics.mean(player_turns_in_jail[player.name]):.2f}")
        print(f"Win %: {(player_win_counts[player.name]/game_count)*100:.1f} %")
        print("Losses: ")
        print(
            f"\tTapped Out: {sum([1 for x in player_loss_reasons[player.name] if x == LostReasons.TappedOut])}"
        )
        print(
            f"\tOut Of Beer: {sum([1 for x in player_loss_reasons[player.name] if x == LostReasons.OutOfBeer])}"
        )
        print(f"Avg Loss Round: {statistics.mean(player_loss_round_counts[player.name]):.2f}")


if __name__ == "__main__":
    Main()
