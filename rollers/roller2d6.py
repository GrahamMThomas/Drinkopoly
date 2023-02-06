import random
from rollers.roller import Roller


class Roller2d6(Roller):
    def Roll(self) -> int:
        return random.randint(1, 6) + random.randint(1, 6)
