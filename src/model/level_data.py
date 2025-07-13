from dataclasses import dataclass
from typing import List
from src.model.player_hand import Player
from src.game.mission_rules import MissionRule
from src.model.missions_order_data import MissionsOrderData
from src.game.communication_manager import CommunicationManager

@dataclass
class LevelData:
    players: List[Player]
    missions: List[MissionRule]
    mission_order_data: MissionsOrderData
    communication_manager: CommunicationManager