import pytest
from unittest.mock import MagicMock
from src.model.card import BLUE_1, BLUE_2, BLUE_3, BLUE_4
from src.model.level_definition import MissionType, LevelDefinition, CommunicationType
from src.model.player_hand import Player
from src.game.mission_rule_builder import MissionRuleListBuilder
from src.game.mission_rule_factories import (
    StaticMissionRuleFactory,
    PlayerShouldNeverWinMissionRuleFactory,
    PlayerHasToWinMissionRuleListFactory,
)
from src.game.mission_rules import (
    PlayerHasToWinCardRule,
    PlayerShouldNeverWinRule,
    NeverWinWithNumberRule,
    WinOnceWithNumberRule,
    WinWithAllTheseCardsRule,
)
from tests.helpers.test_data_creation_helper import create_player

class TestMissionRuleListBuilder:
    def setup_method(self):
        self.mock_interface = MagicMock()
        self.builder = MissionRuleListBuilder(self.mock_interface)
        self.players = [create_player("Alice"), create_player("Bob")]

    def test_static_mission_types(self):
        metadata = {
            MissionType.NEVER_WIN_WITH_NUMBER: {"mission_number": 4},
            MissionType.WIN_ONCE_WITH_NUMBER: {"mission_number": 5},
            MissionType.WIN_WITH_ALL_THESE_CARDS: {"cards_that_need_to_win": {BLUE_1, BLUE_2}},
        }
        definition = LevelDefinition(
            order_tokens=[],
            mission_types=[
                MissionType.NEVER_WIN_WITH_NUMBER,
                MissionType.WIN_ONCE_WITH_NUMBER,
                MissionType.WIN_WITH_ALL_THESE_CARDS,
            ],
            communication_type=CommunicationType.REGULAR,
            communication_metadata={},
            missions_metadata=metadata,
        )

        rules = self.builder.build(self.players, definition, [])

        assert any(isinstance(r, NeverWinWithNumberRule) for r in rules)
        assert any(isinstance(r, WinOnceWithNumberRule) for r in rules)
        assert any(isinstance(r, WinWithAllTheseCardsRule) for r in rules)

    def test_player_should_never_win_rule(self):
        self.mock_interface.select_player_that_should_not_win.return_value = self.players[1]

        definition = LevelDefinition(
            order_tokens=[],
            mission_types=[MissionType.PLAYER_SHOULD_NEVER_WIN],
            communication_type=CommunicationType.REGULAR,
            communication_metadata={},
            missions_metadata={},
        )

        rules = self.builder.build(self.players, definition, [])

        assert len(rules) == 1
        rule = rules[0]
        assert isinstance(rule, PlayerShouldNeverWinRule)
        assert rule.player_that_should_never_win == self.players[1]
        self.mock_interface.select_player_that_should_not_win.assert_called_once_with(self.players)

    def test_player_has_to_win_card_rules(self):
        self.mock_interface.select_mission.side_effect = [BLUE_1, BLUE_2]

        definition = LevelDefinition(
            order_tokens=[],
            mission_types=[MissionType.PLAYER_HAS_TO_WIN_CARD] * 2,
            communication_type=CommunicationType.REGULAR,
            communication_metadata={},
            missions_metadata={},
        )

        rules = self.builder.build(self.players, definition, [BLUE_1, BLUE_2])

        assert len(rules) == 2
        assert all(isinstance(r, PlayerHasToWinCardRule) for r in rules)
        assigned_cards = [r.card for r in rules]
        assert BLUE_1 in assigned_cards
        assert BLUE_2 in assigned_cards
        self.mock_interface.select_mission.assert_called()

    def test_ignores_player_has_to_win_card_if_no_card(self):
        definition = LevelDefinition(
            order_tokens=[],
            mission_types=[MissionType.PLAYER_HAS_TO_WIN_CARD],
            communication_type=CommunicationType.REGULAR,
            communication_metadata={},
            missions_metadata={},
        )

        rules = self.builder.build(self.players, definition, [])
        assert rules == []
