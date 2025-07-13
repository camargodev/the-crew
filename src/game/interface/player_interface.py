from abc import ABC, abstractmethod
from typing import List

from src.model.player_hand import Player
from src.model.card import Card

class PlayerInterface(ABC):
    @abstractmethod
    def select_card(player: Player) -> Card:
        pass # pragma: no cover

    @abstractmethod
    def select_mission(player: Player, missions: List[Card], can_skip: bool) -> Card:
        pass # pragma: no cover
    
    @abstractmethod
    def select_blocked_players(player: List[Player], number_of_player: int) ->  List[Player]:
        pass # pragma: no cover