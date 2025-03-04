from abc import ABC, abstractmethod

from src.model.player_hand import Player
from src.model.card import Card

class PlayerInterface(ABC):
    @abstractmethod
    def select_card(player: Player) -> Card:
        pass # pragma: no cover