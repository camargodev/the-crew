from enum import Enum
from dataclasses import dataclass

class CardType(Enum):
    """
    Enum representing the different types of cards in the game.
    Types include BLUE, YELLOW, PINK, GREEN, and ROCKET.
    """
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    PINK = "PINK"
    GREEN = "GREEN"
    ROCKET = "ROCKET"

@dataclass(frozen=True)
class Card:
    """
    Represents a card in the game with a specific type and number.

    Attributes:
        type (str): The type of the card (e.g., BLUE, YELLOW).
        number (int): The number of the card (1-9 for most types, 1-4 for ROCKET).
    """
    type: str
    number: int

    _locked = False

    def __post_init__(self):
        if Card._locked:
            raise RuntimeError("Cannot create new Card instances")

    @classmethod
    def lock(cls):
        """
        Locks the Card class, preventing the creation of new Card instances.
        """
        cls._locked = True

class CardsOperation:
    """
    A class that provides operations for retrieving cards based on their attributes.
    """

    @classmethod
    def get_cards_by_number(cls, number: int) -> set[Card]:
        """
        Retrieves all cards of a specific number, excluding ROCKET cards.

        Args:
            number (int): The number of the cards to retrieve.

        Returns:
            set[Card]: A set of cards with the specified number (excluding ROCKET cards).
        """
        return {
            card
            for card in ALL_CARDS
            if card.number == number and card.type != CardType.ROCKET.value
        }

    @classmethod
    def get_cards_by_type(cls, card_type: CardType) -> set[Card]:
        """
        Retrieves all cards of a specific type.

        Args:
            card_type (CardType): The type of cards to retrieve.

        Returns:
            set[Card]: A set of cards of the specified type.
        """
        return {card for card in ALL_CARDS if card.type == card_type}

## Global Cards definitions

ALL_CARDS = (
    [Card(type, number)
     for type in (CardType.BLUE, CardType.YELLOW, CardType.PINK, CardType.GREEN)
     for number in range(1, 10)] +
    [Card(CardType.ROCKET, number)
     for number in range(1, 5)]
)

(BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5, BLUE_6, BLUE_7, BLUE_8, BLUE_9,
 YELLOW_1, YELLOW_2, YELLOW_3, YELLOW_4, YELLOW_5, YELLOW_6, YELLOW_7, YELLOW_8, YELLOW_9,
 PINK_1, PINK_2, PINK_3, PINK_4, PINK_5, PINK_6, PINK_7, PINK_8, PINK_9,
 GREEN_1, GREEN_2, GREEN_3, GREEN_4, GREEN_5, GREEN_6, GREEN_7, GREEN_8, GREEN_9,
 ROCKET_1, ROCKET_2, ROCKET_3, ROCKET_4) = ALL_CARDS

ALL_ROCKETS = CardsOperation.get_cards_by_type(CardType.ROCKET)

# Lock class to prevent further instances
Card.lock()
