from dataclasses import dataclass
from src.model.player_hand import Player
from src.model.card import Card

@dataclass(frozen=True)
class PlayerMission:
    player: Player
    card: Card