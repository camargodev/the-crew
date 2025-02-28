from enum import Enum
from dataclasses import dataclass
from typing import ClassVar

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

    _instances: ClassVar[list["Card"]] = []
    _locked = False

    def __post_init__(self):
        if Card._locked:
            raise RuntimeError("Cannot create new Card instances")
        Card._instances.append(self)

    @classmethod
    def lock(cls):
        cls._locked = True

# Defining all possible cards
ALL_CARDS = (
    [Card(type, number) for type in (CardType.BLUE, CardType.YELLOW, CardType.PINK, CardType.GREEN) for number in range(1, 10)] +
    [Card(CardType.ROCKET, number) for number in range(1, 5)]
)

# Lock class to prevent further instances
Card.lock()

# Exporting constants
(BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5, BLUE_6, BLUE_7, BLUE_8, BLUE_9,
 YELLOW_1, YELLOW_2, YELLOW_3, YELLOW_4, YELLOW_5, YELLOW_6, YELLOW_7, YELLOW_8, YELLOW_9,
 PINK_1, PINK_2, PINK_3, PINK_4, PINK_5, PINK_6, PINK_7, PINK_8, PINK_9,
 GREEN_1, GREEN_2, GREEN_3, GREEN_4, GREEN_5, GREEN_6, GREEN_7, GREEN_8, GREEN_9,
 ROCKET_1, ROCKET_2, ROCKET_3, ROCKET_4) = ALL_CARDS

__all__ = [
    "BLUE_1", "BLUE_2", "BLUE_3", "BLUE_4", "BLUE_5", "BLUE_6", "BLUE_7", "BLUE_8", "BLUE_9",
    "YELLOW_1", "YELLOW_2", "YELLOW_3", "YELLOW_4", "YELLOW_5", "YELLOW_6", "YELLOW_7", "YELLOW_8", "YELLOW_9",
    "PINK_1", "PINK_2", "PINK_3", "PINK_4", "PINK_5", "PINK_6", "PINK_7", "PINK_8", "PINK_9",
    "GREEN_1", "GREEN_2", "GREEN_3", "GREEN_4", "GREEN_5", "GREEN_6", "GREEN_7", "GREEN_8", "GREEN_9",
    "ROCKET_1", "ROCKET_2", "ROCKET_3", "ROCKET_4"
]

def get_cards_by_number(number: int) -> set[Card]:
    return {card for card in ALL_CARDS if card.number == number and card.type != CardType.ROCKET.value}

def get_cards_by_type(card_type: str) -> set[Card]:
    return {card for card in ALL_CARDS if card.type == card_type}
