from typing import Dict
from models.player import Player
from board.property import Property


class GameBoard:
    def __init__(self):
        self.properties = self.get_properties()
        self.player_positions: Dict[str, int] = {}  # Player name to positional index

    def add_player_to_board(self, player: Player):
        self.player_positions[player.name] = 0

    def move_player(self, num_of_spaces: int, player: Player) -> Property:
        self.player_positions[player.name] = (
            self.player_positions[player.name] + num_of_spaces
        ) % len(self.properties)
        return self.properties[self.player_positions[player.name]]

    def get_properties(self):
        return [
            Property("Go", 0),
            Property("Mediterranean Avenue", 60),
            Property("Community Chest", 0),  # Keg theme
            Property("Baltic Avenue", 60),
            Property("Income Tax", 0),
            Property("Reading Railroad", 200),
            Property("Oriental Avenue", 100),
            Property("Chance", 0),
            Property("Vermouth Avenue", 100),
            Property("Cabernet Avenue", 120),
            Property("Drunk Tank", 0),
            Property("St. Charles Place", 140),
            Property("Electric Company", 150),
            Property("States Avenue", 140),
            Property("Virginia Avenue", 160),
            Property("Pennslyvania Railroad", 200),
            Property("St. James Place", 180),
            Property("Community Chest", 0),
            Property("Hennessy Avenue", 180),
            Property("New York Avenue", 200),
            Property("Free Parking", 0),  # Kings Cup
            Property("Kentucky Avenue", 230),
            Property("Chance", 230),
            Property("Indiana Avenue", 230),
            Property("Illinois Avenue", 230),
            Property("B. & O. Railroad", 200),
            Property("Atlantic Avenue", 260),
            Property("Ventnor Avenue", 260),
            Property("Water Works", 150),  # Water Fall
            Property("Go To Jail", 0),
            Property("Pacific Avenue", 300),
            Property("North Carolina Avenue", 300),
            Property("Community Chest", 0),
            Property("Pennsylvania Avenue", 320),
            Property("Short Line", 200),  # Short Bus
            Property("Chance", 0),
            Property("Park Place", 320),
            Property("Luxury Tax", 0),
            Property("Boardwalk", 400),
        ]
