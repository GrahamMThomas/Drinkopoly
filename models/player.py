from typing import List
from board.property import Property
from rollers.roller2d6 import Roller2d6


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.roller = Roller2d6()
        self.owned_properties: List[Property] = []
        self.total_oz_drank = 0
        self.in_jail = False
        self.is_question_master = False

    def Roll(self) -> int:
        roll_outcome = self.roller.Roll()
        print(f"{self.name} rolled a {roll_outcome}")
        return roll_outcome

    def Drink(self, ounces: float) -> None:
        print(f"{self.name} drank {ounces} oz")
        self.total_oz_drank += ounces

    def DecideToBuy(self, the_property: Property) -> bool:
        return True

    def BuyProperty(self, the_property: Property) -> None:
        print(f"{self.name} buys {the_property.name}")
        self.Drink(the_property.GetRentCost())

    def OwnsProperty(self, the_property: Property) -> bool:
        return the_property in self.owned_properties
