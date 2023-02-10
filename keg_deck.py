import random
from typing import List
from community_keg.bar_error_in_your_favor import BarErrorInYourFavor
from community_keg.keg import Keg
from community_keg.spilt_beer import SpiltBeer


class KegDeck:
    def __init__(self) -> None:
        self.cards: List[Keg] = self.generate_card_deck()
        self.used_cards: List[Keg] = []

    def pick_a_card(self):
        picked_card = self.cards.pop()
        self.used_cards.append(picked_card)
        if len(self.cards) == 0:
            self.shuffle_deck()
        return picked_card

    def shuffle_deck(self):
        self.cards = self.used_cards
        self.used_cards = []
        random.shuffle(self.cards)

    def generate_card_deck(self) -> List[Keg]:
        cards = [BarErrorInYourFavor(), SpiltBeer()]
        random.shuffle(cards)
        return cards
