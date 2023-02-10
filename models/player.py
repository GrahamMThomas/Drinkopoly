import random
from typing import List
from board.property import Property
from models.setColors import SetColors
from rollers.roller2d6 import Roller2d6
import logging


class Player:
    def __init__(self, name: str) -> None:
        self.logger = logging.getLogger("Drinkopoly")
        self.name = name
        self.roller = Roller2d6()
        self.owned_properties: List[Property] = []
        self.total_oz_drank = 0
        self.in_jail = False
        self.is_question_master = False
        self.times_in_jail = 0
        self.times_question_master = 0
        self.drinking_capacity = 48  # oz
        self.has_lost = False

    def Roll(self) -> int:
        roll_outcome = self.roller.Roll()
        self.logger.debug(f"{self.name} rolled a {roll_outcome}")
        return roll_outcome

    def Drink(self, ounces: float) -> None:
        self.logger.debug(f"{self.name} drank {ounces:.2f} oz")
        self.total_oz_drank += ounces
        if self.total_oz_drank > self.drinking_capacity:
            self.Lose()

    def Lose(self):
        self.logger.debug(f"{self.name} has Lost and is out of the game!")
        self.has_lost = True

    def DecideToBuy(self, the_property: Property) -> bool:
        return True

    def BuyHousesIfDesired(self) -> bool:
        for the_property in self.owned_properties:
            if not self.OwnsPropertySet(the_property):
                continue
            if random.randint(0, 2) == 0:
                if the_property.house_count + 1 > the_property.MAX_HOUSE_COUNT:
                    return False
                self.logger.debug(
                    f"{self.name} purchased {1} houses on {the_property.name}"
                )
                self.Drink(the_property.house_cost * 1)
                the_property.house_count += 1
                return True

    def BuyProperty(self, the_property: Property) -> None:
        self.logger.debug(f"{self.name} buys {the_property.name}")
        self.Drink(the_property.purchase_cost)
        self.owned_properties.append(the_property)
        the_property.owner = self

    def OwnsProperty(self, the_property: Property) -> bool:
        return the_property in self.owned_properties

    def OwnsPropertySet(self, the_property: Property):
        if the_property.color_code == SetColors.SINGLE:
            return True
        return the_property.set_property_count == sum(
            [
                1
                for x in self.owned_properties
                if x.color_code == the_property.color_code
            ]
        )
