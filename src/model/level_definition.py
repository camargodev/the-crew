from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Any

class OrderToken(Enum):
    FIRST_ABSOLUTE = auto()
    SECOND_ABSOLUTE = auto()
    THIRD_ABSOLUTE = auto()
    FOURTH_ABSOLUTE = auto()
    FIFTH_ABSOLUTE = auto()
    LAST_ABSOLUTE = auto()
    FIRST_RELATIVE = auto()
    SECOND_RELATIVE = auto()
    THIRD_RELATIVE = auto()
    FOURTH_RELATIVE = auto()

class MissionType(Enum):
    PLAYER_HAS_TO_WIN_CARD = auto()
    NEVER_WIN_WITH_NUMBER = auto()
    WIN_ONCE_WITH_NUMBER = auto()
    WIN_WITH_ALL_THESE_CARDS = auto()
    PLAYER_SHOULD_NEVER_WIN = auto()

class CommunicationType(Enum):
    REGULAR = auto()
    DEAD_ZONE = auto()
    BLOCKED_FOR_NUMBER_OF_PLAYER = auto()
    BLOCKED_UNTIL_ROUND = auto()

@dataclass
class LevelDefinition:
    order_tokens: List[OrderToken]
    mission_types: Dict[MissionType, int]
    communication_type: CommunicationType
    communication_metadata: Dict[str, Any] = field(default_factory=dict)
    missions_metadata: Dict[str, Any] = field(default_factory=dict)


LEVEL_1 = LevelDefinition(
    order_tokens=[],
    mission_types={MissionType.PLAYER_HAS_TO_WIN_CARD: 1},
    communication_type=CommunicationType.REGULAR
)

LEVEL_2 = LevelDefinition(
    order_tokens=[],
    mission_types={MissionType.PLAYER_HAS_TO_WIN_CARD: 2},
    communication_type=CommunicationType.REGULAR
)

LEVEL_3 = LevelDefinition(
    order_tokens=[OrderToken.FIRST_ABSOLUTE, OrderToken.SECOND_ABSOLUTE],
    mission_types={MissionType.PLAYER_HAS_TO_WIN_CARD: 2},
    communication_type=CommunicationType.REGULAR
)

LEVEL_4 = LevelDefinition(
    order_tokens=[],
    mission_types={MissionType.PLAYER_HAS_TO_WIN_CARD: 3},
    communication_type=CommunicationType.REGULAR
)

LEVEL_5 = LevelDefinition(
    order_tokens=[],
    mission_types={MissionType.PLAYER_SHOULD_NEVER_WIN: 1},
    communication_type=CommunicationType.REGULAR
)