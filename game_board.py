from typing import Dict, List
from board.board_space import BoardSpace
from board.drunken_drive import DrunkenDrive
from board.go_to_jail import GoToJail
from board.jail import Jail
from board.question_master import QuestionMaster
from board.water_fall import WaterFall
from models.player import Player
from board.property import Property
from models.setColors import SetColors


class GameBoard:
    def __init__(self):
        self.properties = self.get_properties()
        self.player_positions: Dict[str, int] = {}  # Player name to positional index

    def add_player_to_board(self, player: Player):
        self.player_positions[player.name] = 0

    def move_player(self, num_of_spaces: int, player: Player) -> List[Property]:
        visited = []
        for x in range(0, num_of_spaces):
            visited.append(self.move_by_1(player))
        return visited

    def move_by_1(self, player: Player) -> Property:
        self.player_positions[player.name] = (self.player_positions[player.name] + 1) % len(self.properties)
        return self.properties[self.player_positions[player.name]]

    def teleport_player(self, property_name: str, player: Player) -> None:
        self.player_positions[player.name] = self.get_property_location_by_name(property_name)

    def get_property_location_by_name(self, property_name):
        board_index = [i for i, v in enumerate(self.properties) if v.name == property_name]
        if len(board_index) == 0:
            raise Exception(f"Could not find property of name {property_name}")
        return board_index

    def get_properties(self):
        return [
            BoardSpace("Go"),
            Property("Mediterranean Avenue", 60, SetColors.BROWN),
            DrunkenDrive("Drunken Drive", 1),  # Keg theme
            Property("Baltic Avenue", 60, SetColors.BROWN),
            QuestionMaster("Question Master"),
            Property("Whiskey Express", 200, SetColors.BLACK),
            Property("Oriental Avenue", 100, SetColors.LIGHTBLUE),
            BoardSpace("Chance"),
            Property("Vermouth Avenue", 100, SetColors.LIGHTBLUE),
            Property("Cabernet Avenue", 120, SetColors.LIGHTBLUE),
            Jail("Drunk Tank"),
            Property("St. Charles Place", 140, SetColors.PURPLE),
            Property("Electric Company", 150, SetColors.GRAY),
            Property("States Avenue", 140, SetColors.PURPLE),
            Property("Virginia Avenue", 160, SetColors.PURPLE),
            Property("Salty Spitoon", 200, SetColors.BLACK),
            Property("Patron Place", 180, SetColors.ORANGE),
            BoardSpace("Community Chest"),
            Property("Hennessy Avenue", 180, SetColors.ORANGE),
            Property("New York Avenue", 200, SetColors.ORANGE),
            BoardSpace("Free Parking"),  # Kings Cup
            Property("Kentucky Avenue", 230, SetColors.RED),
            BoardSpace("Chance"),
            Property("Indiana Avenue", 230, SetColors.RED),
            Property("Illinois Avenue", 230, SetColors.RED),
            Property("B. & O. Railroad", 200, SetColors.BLACK),
            Property("Atlantic Avenue", 260, SetColors.YELLOW),
            Property("Ventnor Avenue", 260, SetColors.YELLOW),
            WaterFall("Water Fall", 0.25),
            GoToJail("Go To Jail"),
            Property("Pacific Avenue", 300, SetColors.GREEN),
            Property("North Carolina Avenue", 300, SetColors.GREEN),
            BoardSpace("Community Chest"),
            Property("Prosecco Avenue", 320, SetColors.GREEN),
            Property("Short Bus Booze", 200, SetColors.BLACK),
            BoardSpace("Chance"),
            Property("Park Place", 320, SetColors.BLUE),
            BoardSpace("Luxury Tax"),
            Property("Boardwalk", 400, SetColors.BLUE),
        ]
