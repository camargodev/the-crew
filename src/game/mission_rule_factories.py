from typing import Any, Dict, List
from src.model.level_definition import MissionType
from src.game.mission_rules import (
    NeverWinWithNumberRule,
    WinOnceWithNumberRule,
    WinWithAllTheseCardsRule,
    PlayerShouldNeverWinRule,
    MissionRule,
)
from src.model.card import Card
from src.model.player_hand import Player
from src.game.interface.player_interface import PlayerInterface
from src.game.mission_rules import PlayerHasToWinCardRule

class StaticMissionRuleFactory:
    @staticmethod
    def create(mission_type: MissionType, metadata: Dict[MissionType, Any]) -> MissionRule:
        """
        Create a static MissionRule instance based on mission_type and provided data.

        Args:
            mission_type (MissionType): The type of mission rule to create.
            data (dict): Required data to instantiate the mission rule.

        Returns:
            MissionRule: The created mission rule instance.
        """

        metadata_for_mission = metadata.get(mission_type, dict())

        if mission_type == MissionType.NEVER_WIN_WITH_NUMBER:
            return NeverWinWithNumberRule(number=metadata_for_mission['mission_number'])

        if mission_type == MissionType.WIN_ONCE_WITH_NUMBER:
            return WinOnceWithNumberRule(number=metadata_for_mission['mission_number'])

        if mission_type == MissionType.WIN_WITH_ALL_THESE_CARDS:
            return WinWithAllTheseCardsRule(cards_that_need_to_win=metadata_for_mission['cards_that_need_to_win'])

        raise ValueError(f"Unsupported mission type: {mission_type}")
    
class PlayerShouldNeverWinMissionRuleFactory:
    def __init__(self, player_interface: PlayerInterface):
        self.player_interface = player_interface

    def create(self, players: List[Player]) -> PlayerShouldNeverWinRule:
        """
        Selects the player who should never win using PlayerInterface,
        and returns the corresponding mission rule.
        """
        selected_player = self.player_interface.select_player_that_should_not_win(players)
        return PlayerShouldNeverWinRule(player_that_should_never_win=selected_player)

class PlayerHasToWinMissionRuleListFactory:
    def __init__(self, player_interface: PlayerInterface):
        self.player_interface = player_interface

    def create(
        self,
        players: List[Player],
        mission_cards: List[Card],
    ) -> List[PlayerHasToWinCardRule]:
        """
        Distributes PLAYER_HAS_TO_WIN_CARD missions among players according to the game rules.

        Each player can receive at most one more mission than any other player.
        Players can skip a mission only if the remaining missions can still be
        fairly distributed among the other players.

        Args:
            players (List[Player]): List of players participating in the game.
            mission_cards (List[Card]): List of cards to be assigned as missions.

        Returns:
            List[PlayerHasToWinCardRule]: The list of assigned mission rules.
        """
        player_count = len(players)
        assigned_rules: List[PlayerHasToWinCardRule] = []
        player_index = 0
        remaining_cards = mission_cards.copy()

        while remaining_cards:
            player = players[player_index]
            can_skip = self.__can_player_skip(remaining_cards, player_count, player_index)

            selected_card = self.player_interface.select_mission(
                player.id, remaining_cards, can_skip=can_skip
            )

            if selected_card:
                assigned_rules.append(
                    PlayerHasToWinCardRule(player=player, card=selected_card)
                )
                remaining_cards.remove(selected_card)

            player_index = (player_index + 1) % player_count

        return assigned_rules

    def __can_player_skip(
        self,
        remaining_cards: List[Card],
        number_of_players: int,
        current_player_index: int,
    ) -> bool:
        number_of_remaining_players = number_of_players - (current_player_index + 1)
        result = number_of_remaining_players >= len(remaining_cards)
        return result
