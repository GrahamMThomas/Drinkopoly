import random
from typing import List
from board.property import Property
from models.lostReasons import LostReasons
from models.setColors import SetColors
from rollers.roller2d6 import Roller2d6
import logging


class Player:
    DRINK_TOKEN_CONVERSION_RATE = 2  # oz
    DRINK_TOKENS_PER_BEER = 4

    def __init__(
        self, name: str, drinking_capacity: int, converts_drink_tokens: bool
    ) -> None:
        self.logger = logging.getLogger("Drinkopoly")
        self.name = name
        self.roller = Roller2d6()
        self.owned_properties: List[Property] = []
        self.total_oz_drank = 0
        self.in_jail = False
        self.is_question_master = False
        self.times_in_jail = 0
        self.times_question_master = 0
        self.converts_drink_tokens = converts_drink_tokens
        self.drink_tokens = 0
        self.alcohol_remaining = 12
        self.drinking_capacity = drinking_capacity  # oz
        self.has_lost = False
        self.lost_reason: LostReasons = None

    def Roll(self) -> int:
        roll_outcome = self.roller.Roll()
        self.logger.debug(f"{self.name} rolled a {roll_outcome}")
        return roll_outcome

    def Drink(self, ounces: float) -> None:
        self.logger.debug(f"{self.name} drank {ounces:.2f} oz")

        while (
            self.converts_drink_tokens
            and ounces > self.DRINK_TOKEN_CONVERSION_RATE
            and self.drink_tokens > 0
        ):
            self.logger.debug(f"{self.name} redeemed a drink token (Preventative)")
            ounces -= self.DRINK_TOKEN_CONVERSION_RATE
            self.drink_tokens -= 1

        while (
            not self.converts_drink_tokens
            and self.alcohol_remaining < ounces
            and self.drink_tokens > 0
            and self.drink_tokens < self.DRINK_TOKENS_PER_BEER
        ):
            self.logger.debug(f"{self.name} redeemed a drink token (Forced)")
            ounces -= self.DRINK_TOKEN_CONVERSION_RATE
            self.drink_tokens -= 1

        if (
            self.alcohol_remaining < ounces
            and self.drink_tokens >= self.DRINK_TOKENS_PER_BEER
        ):
            self.GrabABeer()

        self.total_oz_drank += ounces
        self.alcohol_remaining -= ounces

        if self.total_oz_drank > self.drinking_capacity:
            self.Lose(LostReasons.TappedOut)
        elif self.alcohol_remaining < 0:
            self.Lose(LostReasons.OutOfBeer)

    def Lose(self, lost_reason: LostReasons):
        self.logger.debug(f"{self.name} has Lost and is out of the game!")
        self.has_lost = True
        self.lost_reason = lost_reason

    def EarnDrinkTokens(self, drink_token_amount_to_add):
        self.logger.debug(
            f"{self.name} gained {drink_token_amount_to_add} drink token(s)"
        )
        self.drink_tokens += drink_token_amount_to_add

    def GrabABeer(self) -> bool:
        if self.drink_tokens < self.DRINK_TOKENS_PER_BEER:
            return False
        self.drink_tokens -= self.DRINK_TOKENS_PER_BEER
        self.alcohol_remaining += 12

    def DecideToBuy(self, the_property: Property) -> bool:
        # Purchase if you have 4 oz of backup alcohol
        buying_power = self.alcohol_remaining + (
            self.drink_tokens * self.DRINK_TOKEN_CONVERSION_RATE
        )
        if buying_power - the_property.purchase_cost > 4:
            return True
        self.logger.debug(f"{self.name} is too broke! ({buying_power})")
        return False

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
