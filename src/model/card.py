from enum import Enum
from dataclasses import dataclass

class CardType(Enum):
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    PINK = "PINK"
    GREEN = "GREEN"
    ROCKET = "ROCKET"

@dataclass(frozen=True)
class Card:
    type: str
    number: int
