from game_board import GameBoard
from game_manager import GameManager
from models.player import Player


def Main():
    players = [Player("Alfred"), Player("Bob"), Player("Cooper"), Player("Doofus")]
    board = GameBoard()
    for player in players:
        board.add_player_to_board(player)
    gm = GameManager(players, board)

    round_number = 1
    while True:
        gm.DoRound(round_number)
        if sum([1 for player in players if player.has_lost]) >= len(players) - 1 or round_number > 200:
            print("\n\nGame over!")
            print("Stats -------------------------")
            print(f"Rounds played: {round_number}")

            for player in players:
                print(f"{player.name}:")
                print(f"\tAlcohol Drank: {player.total_oz_drank}")
                print(f"\tArrests: {player.times_in_jail}")
                print(f"\tQuestion Master: {player.times_question_master}")
            break
        round_number += 1


if __name__ == "__main__":
    Main()
