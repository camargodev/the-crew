from src.model.card import Card
from src.model.card import ROCKET_4
from dataclasses import dataclass, field
from typing import List

@dataclass
class CardHand:
    cards: List[Card] = field(default_factory=list)

    def add_card(self, card: Card):
        self.cards.append(card)

    def remove_card(self, card: Card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            raise ValueError("Card not in hand")

    def has_card(self, card: Card) -> bool:
        return card in self.cards
    
    def __hash__(self):
        return hash(tuple(set(self.cards)))

@dataclass(frozen=True)
class Player:
    name: str
    card_hand: CardHand

    def deal_card(self, card: Card):
        self.card_hand.add_card(card)

    def play_card(self, card: Card):
        self.card_hand.remove_card(card)

    def is_captain(self) -> bool:
        """Returns True if the player has a ROCKET 4."""
        return self.card_hand.has_card(ROCKET_4)

