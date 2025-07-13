from typing import List
from src.model.level_definition import MissionType
from src.game.mission_rules import MissionRule
from src.model.card import Card
from src.model.player_hand import Player
from src.game.interface.player_interface import PlayerInterface
from src.game.mission_rules import PlayerHasToWinCardRule
from src.model.level_definition import LevelDefinition
from src.game.mission_rule_factories import PlayerHasToWinMissionRuleListFactory, PlayerShouldNeverWinMissionRuleFactory, StaticMissionRuleFactory

class MissionRuleListBuilder:
    """
    Builder class responsible for creating mission rules based on the level definition and players.

    Uses PlayerHasToWinMissionRuleListFactory for PLAYER_HAS_TO_WIN_CARD missions,
    PlayerInterface to select player for PLAYER_SHOULD_NEVER_WIN,
    and StaticMissionRuleFactory for other static mission types.
    """

    def __init__(self, player_interface: PlayerInterface):
        self.player_interface = player_interface
        self.player_win_factory = PlayerHasToWinMissionRuleListFactory(player_interface)
        self.player_never_win_factory = PlayerShouldNeverWinMissionRuleFactory(player_interface)

    def build(
        self,
        players: List[Player],
        level_definition: LevelDefinition,
        mission_cards: List[Card],
    ) -> List[MissionRule]:
        """
        Build a list of mission rules based on the level definition and players.

        This method handles:
        - Creating PlayerHasToWinCardRule missions once if present.
        - Selecting the player who should never win using PlayerInterface.
        - Creating other static mission rules using StaticMissionRuleFactory.

        Args:
            players (List[Player]): The list of players participating.
            level_definition (LevelDefinition): The level definition containing mission types and metadata.
            mission_cards (List[Card]): The list of cards to assign for PLAYER_HAS_TO_WIN_CARD missions.

        Returns:
            List[MissionRule]: The list of constructed mission rules.
        """
        mission_rules: List[MissionRule] = []

        if MissionType.PLAYER_HAS_TO_WIN_CARD in level_definition.mission_types:
            mission_rules += self.player_win_factory.create(players, mission_cards)

        for mission_type in level_definition.mission_types:
            if mission_type == MissionType.PLAYER_HAS_TO_WIN_CARD:
                continue

            if mission_type == MissionType.PLAYER_SHOULD_NEVER_WIN:
                mission_rules.append(self.player_never_win_factory.create(players))
                continue

            mission_rule = StaticMissionRuleFactory.create(
                mission_type, 
                level_definition.missions_metadata
            )
            mission_rules.append(mission_rule)

        return mission_rules
