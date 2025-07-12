from dataclasses import dataclass, field
from typing import List
from src.model.card import Card, CardType
from src.model.card import ROCKET_4

@dataclass(frozen=True)
class CardHand:
    """
    Represents a player's hand of cards.

    Attributes:
        cards (List[Card]): A list of cards held by the player.
    """
    cards: List[Card] = field(default_factory=list)

    def add_card(self, card: Card):
        """
        Adds a card to the hand.

        Args:
            card (Card): The card to be added to the hand.
        """
        self.cards.append(card)

    def remove_card(self, card: Card):
        """
        Removes a card from the hand. Raises an error if the card is not present.

        Args:
            card (Card): The card to be removed from the hand.

        Raises:
            ValueError: If the card is not found in the hand.
        """
        if card in self.cards:
            self.cards.remove(card)
        else:
            raise ValueError("Card not in hand")

    def has_card(self, card: Card) -> bool:
        """
        Checks if the hand contains a specific card.

        Args:
            card (Card): The card to check for.

        Returns:
            bool: True if the card is in the hand, False otherwise.
        """
        return card in self.cards

    def get_playable_cards(self, card_type: CardType) -> List[Card]:
        """
        Returns the playable cards based on the given card type.

        If the hand contains cards of the specified type, only those are returned.
        Otherwise, all cards in the hand are returned.

        Args:
            card_type (CardType): The type of card to filter by.

        Returns:
            List[Card]: A list of playable cards.
        """
        filtered = [card for card in self.cards if card.type == card_type]
        return filtered if filtered else self.cards

    def __hash__(self):
        """
        Returns a hash value for the CardHand object. The hash is based on the set of cards in hand.

        Returns:
            int: The hash value for the CardHand.
        """
        return hash(tuple(set(self.cards)))


@dataclass(frozen=True)
class Player:
    """
    Represents a player in the game, including their name and card hand.

    Attributes:
        name (str): The name of the player.
        card_hand (CardHand): The cards currently held by the player.
    """
    name: str
    card_hand: CardHand

    def deal_card(self, card: Card):
        """
        Deals a card to the player by adding it to their hand.

        Args:
            card (Card): The card to be dealt to the player.
        """
        self.card_hand.add_card(card)

    def play_card(self, card: Card):
        """
        Makes the player play a card by removing it from their hand.

        Args:
            card (Card): The card to be played.
        """
        self.card_hand.remove_card(card)

    def is_captain(self) -> bool:
        """
        Checks if the player is the captain by determining if they have a ROCKET 4 card.

        Returns:
            bool: True if the player has the ROCKET 4 card, False otherwise.
        """
        return self.card_hand.has_card(ROCKET_4)
