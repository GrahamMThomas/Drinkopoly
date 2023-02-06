from game_board import GameBoard
from game_manager import GameManager
from models.player import Player


def Main():
    players = [Player("Alfred"), Player("Bob"), Player("Cooper"), Player("Doofus")]
    board = GameBoard()
    for player in players:
        board.add_player_to_board(player)
    gm = GameManager(players, board)
    gm.DoRound()


if __name__ == "__main__":
    Main()
