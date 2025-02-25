from enum import Enum

class CardType(Enum):
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    PINK = "PINK"
    GREEN = "GREEN"
    ROCKET = "ROCKET"

class Card:
    def __init__(self, type: CardType, number: int):
        self.type = type
        self.number = number

    def __repr__(self):
        return f"Card(type={self.type.value}, number={self.number})"
    
    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.type == other.type and self.number == other.number

    def __hash__(self):
        return hash((self.type, self.number))
