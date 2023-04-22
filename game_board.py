import random
from typing import Dict, List
from board.blacked_out import BlackedOut
from board.board_space import BoardSpace
from board.community_keg_space import CommunityKegSpace
from board.drunken_drive import DrunkenDrive
from board.free_parking import FreeParking
from board.go_space import GoSpace
from board.go_to_jail import GoToJail
from board.jail import Jail
from board.luxury_tax import LuxuryTax
from board.question_master import QuestionMaster
from board.squatters_rights import SquattersRights
from board.water_fall import WaterFall
from models.player import Player
from board.property import Property
from models.setColors import SetColors


class GameBoard:
    def __init__(self):
        self.board_spaces = self.get_properties()
        self.player_positions: Dict[str, int] = {}  # Player name to positional index

    def add_player_to_board(self, player: Player):
        self.player_positions[player.name] = 0

    def move_player(self, num_of_spaces: int, player: Player) -> List[Property]:
        visited = []
        for x in range(0, num_of_spaces):
            visited.append(self.move_by_1(player))
        return visited

    def move_by_1(self, player: Player) -> Property:
        self.player_positions[player.name] = (self.player_positions[player.name] + 1) % len(self.board_spaces)
        return self.board_spaces[self.player_positions[player.name]]

    def teleport_player(self, board_space_name: str, player: Player) -> None:
        self.player_positions[player.name] = self.get_board_space_index_by_name(board_space_name)

    def get_board_space_index_by_name(self, board_space_name):
        board_index = [i for i, v in enumerate(self.board_spaces) if v.name == board_space_name]
        if len(board_index) == 0:
            raise Exception(f"Could not find property of name {board_space_name}")
        return board_index[0]

    def get_board_space_by_name(self, board_space_name):
        board_spaces = [x for x in self.board_spaces if x.name == board_space_name]
        if len(board_spaces) == 0:
            raise Exception(f"Could not find property of name {board_space_name}")
        return board_spaces[0]

    def get_properties_set_color(self, color: SetColors):
        return [x for x in self.board_spaces if isinstance(x, Property) and x.color_code == color]

    def get_properties(self) -> List[BoardSpace]:
        properties = [
            GoSpace("Go"),
            Property("Aperol Avenue", 1, SetColors.BROWN),
            DrunkenDrive("Drunken Drive", 1),
            Property("Bacardi Boulevard", 1.25, SetColors.BROWN),
            CommunityKegSpace("Community Keg 1"),
            Property("Whiskey Express", 2.50, SetColors.SINGLE),
            Property("Vermouth Avenue", 1.5, SetColors.LIGHTBLUE),
            QuestionMaster("Question Master"),
            Property("Rose Roundabout", 1.75, SetColors.LIGHTBLUE),
            Jail("Drunk Tank"),
            Property("Watering Hole", 2.5, SetColors.SINGLE),
            Property("Curacao Circle", 2, SetColors.PURPLE),
            SquattersRights("Squatter's Rights"),
            Property("Vodka Alley", 2.25, SetColors.PURPLE),
            Property("Salty Spitoon", 2.5, SetColors.SINGLE),
            Property("Patron Place", 2.5, SetColors.ORANGE),
            CommunityKegSpace("Community Keg 2"),
            Property("Hennessy Avenue", 2.5, SetColors.ORANGE),
            FreeParking("Paid Parking"),
            Property("Sake Street", 2.75, SetColors.RED),
            Property("Liquor Land", 3, SetColors.RED),
            Property("D. U I. Railroad", 2.5, SetColors.SINGLE),
            BlackedOut("Blacked Out"),
            Property("Booze Bodega", 3.25, SetColors.YELLOW),
            Property("Marvin Beer Gardens", 3.25, SetColors.YELLOW),
            WaterFall("Water Fall", 0.25),  # Potentially take out
            GoToJail("Go To Jail"),
            Property("Pacifico Avenue", 3.5, SetColors.GREEN),
            Property("North Carolina Avenue", 3.5, SetColors.GREEN),
            CommunityKegSpace("Community Keg 3"),
            Property("Prosecco Avenue", 3.5, SetColors.GREEN),
            Property("Lads Lane", 2.5, SetColors.SINGLE),
            Property("Prohibition Place", 3.75, SetColors.BLUE),
            LuxuryTax("Shot O'Clock"),
            Property("Boardwalk", 4, SetColors.BLUE),
        ]

        for the_property in properties:
            if isinstance(the_property, Property):
                the_property.set_property_count = sum(
                    [
                        1
                        for x in properties
                        if isinstance(x, Property) and x.color_code == the_property.color_code
                    ]
                )
        return properties

    def rent_roll_call(self) -> None:
        for space in self.board_spaces:
            if not isinstance(space, Property):
                continue

            # iterate 0 to Max House and get rent costs and print
            print(f"\n{space.name} - {space.color_code.name}")
            print(f"\tHouse Cost - {space.house_cost} oz")
            print(f"\tRents:")
            for i in range(0, space.MAX_HOUSE_COUNT + 1):
                rent_cost = space.GetRentCost(i)
                print(f"\t\t{i} Houses: {rent_cost} oz")
