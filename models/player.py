from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board.board_space import BoardSpace
    from board.property import Property
    from game_board import GameBoard

import board
import random
from typing import List
from models.lostReasons import LostReasons
from models.setColors import SetColors
from rollers.roller2d6 import Roller2d6
import logging


class Player:
    DRINK_TOKEN_CONVERSION_RATE = 2  # oz
    DRINK_TOKENS_PER_BEER = 4
    DRINK_TOKEN_MAX = 8

    def __init__(self, name: str, drinking_capacity: int, converts_drink_tokens: bool) -> None:
        self.logger = logging.getLogger("Drinkopoly")
        self.name = name
        self.roller = Roller2d6()
        self.owned_properties: List[Property] = []
        self.total_oz_drank = 0
        self.in_jail = False
        self.is_question_master = False
        self.times_in_jail = 0
        self.turns_in_jail = 0
        self.total_turns_in_jail = 0
        self.times_question_master = 0
        self.converts_drink_tokens = converts_drink_tokens
        self.drink_tokens = 0
        self.alcohol_remaining = 12
        self.drinking_capacity = drinking_capacity  # oz
        self.has_lost = False
        self.lost_round = 0
        self.lost_reason: LostReasons = None
        self.safety_net_amount = 2.5

    def Roll(self) -> int:
        roll_outcome = self.roller.Roll()
        self.logger.debug(f"{self.name} rolled a {roll_outcome}")
        return roll_outcome

    def Drink(self, ounces: float) -> None:
        self.logger.debug(f"{self.name} drank {ounces:.2f} oz")

        while (
            self.converts_drink_tokens
            and ounces >= self.DRINK_TOKEN_CONVERSION_RATE * 0.70
            and self.drink_tokens > 0
        ):
            self.logger.debug(f"{self.name} redeemed a drink token (Preventative)")
            ounces -= min(self.DRINK_TOKEN_CONVERSION_RATE, ounces)
            self.drink_tokens -= 1

        if (
            self.alcohol_remaining < ounces
            and self.drink_tokens >= self.DRINK_TOKENS_PER_BEER
            and (self.drinking_capacity - self.total_oz_drank) >= 8
        ):
            self.GrabABeer()

        while (
            self.alcohol_remaining < ounces
            or (
                self.total_oz_drank + ounces >= self.drinking_capacity
                and self.total_oz_drank < self.drinking_capacity
            )
        ) and self.drink_tokens > 0:
            self.logger.debug(f"{self.name} redeemed a drink token (Forced)")
            ounces -= min(self.DRINK_TOKEN_CONVERSION_RATE, ounces)
            self.drink_tokens -= 1

        self.total_oz_drank = min(self.total_oz_drank + ounces, self.drinking_capacity)
        self.alcohol_remaining = max(self.alcohol_remaining - ounces, 0)

        self.CheckIfLost()

    def CheckIfLost(self):
        if self.total_oz_drank >= self.drinking_capacity and self.drink_tokens == 0:
            self.Lose(LostReasons.TappedOut)
        elif self.alcohol_remaining <= 0 and self.drink_tokens == 0:
            self.Lose(LostReasons.OutOfBeer)

    def Lose(self, lost_reason: LostReasons):
        self.logger.debug(f"{self.name} has Lost and is out of the game!")
        for property in self.owned_properties:
            property.ReleaseOwnership()

        self.owned_properties = []
        self.has_lost = True
        self.lost_reason = lost_reason

    def EarnDrinkTokens(self, drink_token_amount_to_add: int):
        if drink_token_amount_to_add + self.drink_tokens > self.DRINK_TOKEN_MAX:
            f"{self.name} has the maximum number of allowed drink tokens. Truncating..."
            drink_token_amount_to_add = self.DRINK_TOKEN_MAX - self.drink_tokens

        self.logger.debug(f"{self.name} gained {drink_token_amount_to_add} drink token(s)")
        self.drink_tokens += drink_token_amount_to_add

    def YoinkDrinkTokens(self, drink_token_amount_to_remove: int):
        self.logger.debug(f"{self.name} lost {drink_token_amount_to_remove} drink token(s)")
        self.drink_tokens -= drink_token_amount_to_remove

    def GrabABeer(self) -> bool:
        self.logger.debug(f"{self.name} grabs a beer")
        if self.drink_tokens < self.DRINK_TOKENS_PER_BEER:
            return False
        self.drink_tokens -= self.DRINK_TOKENS_PER_BEER
        self.alcohol_remaining += 12

    def get_buying_power(self) -> float:
        return self.alcohol_remaining + (self.drink_tokens * self.DRINK_TOKEN_CONVERSION_RATE)

    def DecideToBuy(self, the_property: Property, log=True, extra_padding=0.0) -> bool:
        # Purchase if you have safety_net_amount of backup alcohol
        buying_power = self.get_buying_power()
        if buying_power - the_property.purchase_cost - extra_padding > self.safety_net_amount:
            return True
        if log:
            self.logger.debug(f"{self.name} is too broke!")
        return False

    def DecideWhereToWarp(self, game_board: GameBoard) -> BoardSpace:
        for owned_prop in self.owned_properties:
            if self.OwnsPropertySet(owned_prop):
                continue
            else:
                other_props = game_board.get_properties_set_color(owned_prop.color_code)
                for other_prop in other_props:
                    if not self.OwnsProperty(other_prop) and self.DecideToBuy(other_prop):
                        return other_prop

        badSpaceTypes = [
            board.go_space.GoSpace,
            board.jail.Jail,
            board.free_parking.FreeParking,
            board.go_to_jail.GoToJail,
            board.luxury_tax.LuxuryTax,
        ]
        leftoverSpaces = [x for x in game_board.board_spaces if type(x) not in badSpaceTypes]

        return game_board.get_board_space_by_name(random.choice(leftoverSpaces).name)

    def DecideWhichPropToSquat(self, game_board: GameBoard) -> Property:
        for owned_prop in self.owned_properties:
            if self.OwnsPropertySet(owned_prop):
                continue
            else:
                other_props = game_board.get_properties_set_color(owned_prop.color_code)
                owned_prop_count = sum([1 for x in other_props if self.OwnsProperty(x)])
                if owned_prop_count + 1 == len(other_props):
                    squatter_target_prop = [x for x in other_props if not self.OwnsProperty(x)][0]
                    if squatter_target_prop.IsOwned():
                        return squatter_target_prop
        return None

    def BuyHousesIfDesired(self) -> bool:
        buying_power = self.get_buying_power()

        for the_property in self.owned_properties:
            if not self.OwnsPropertySet(the_property):
                continue

            purchase_count = the_property.MAX_HOUSE_COUNT - the_property.house_count

            while (
                buying_power - (the_property.house_cost * purchase_count) < self.safety_net_amount
                and purchase_count > 0
            ):
                purchase_count -= 1

            if purchase_count == 0:
                continue

            self.logger.debug(f"{self.name} purchased {purchase_count} houses on {the_property.name}")
            self.Drink(the_property.house_cost * purchase_count)
            the_property.house_count += purchase_count
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
            [1 for x in self.owned_properties if x.color_code == the_property.color_code]
        )

    def SetFree(self):
        self.logger.debug(f"{self.name} is no longer in Jail!")
        self.in_jail = False
        self.turns_in_jail = 0
