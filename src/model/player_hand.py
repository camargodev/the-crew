from src.model.card import Card, CardType

class CardHand:
    def __init__(self, cards):
        self.cards = cards

    def add_card(self, card: Card):
        self.cards.append(card)

    def remove_card(self, card: Card):
        if card in self.cards:
            self.cards.remove(card)
        else:
            raise ValueError("Card not in hand")

    def has_card(self, card: Card) -> bool:
        return card in self.cards

    def __repr__(self):
        return f"CardHand({self.cards})"
    
    def __eq__(self, other):
        if not isinstance(other, CardHand):
            return False
        return set(self.cards) == set(other.cards)
    
    def __hash__(self):
        return hash(tuple(set(self.cards))) 


class Player:
    def __init__(self, name: str):
        self.name = name
        self.card_hand = CardHand([])

    def deal_card(self, card: Card):
        self.card_hand.add_card(card)

    def play_card(self, card: Card):
        self.card_hand.remove_card(card)

    def is_captain(self) -> bool:
        """Returns True if the player has a ROCKET 4."""
        return self.card_hand.has_card(Card(CardType.ROCKET, 4))

    def __repr__(self):
        return f"Player(name={self.name}, hand={self.card_hand})"
    
    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        return self.name == other.name and self.card_hand == other.card_hand
    
    def __hash__(self):
        # Hash based on the player's name and their hand of cards
        return hash((self.name, self.card_hand))

