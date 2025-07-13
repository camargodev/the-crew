import pytest
from unittest.mock import MagicMock
from typing import List

from src.model.level_definition import MissionType
from src.game.mission_rules import (
    NeverWinWithNumberRule,
    WinOnceWithNumberRule,
    WinWithAllTheseCardsRule,
    PlayerShouldNeverWinRule,
    PlayerHasToWinCardRule,
)
from src.model.card import (
    BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_8,
    PINK_2,
    GREEN_3
)
from tests.helpers.test_data_creation_helper import create_player
from src.game.mission_rule_factories import (
    StaticMissionRuleFactory,
    PlayerShouldNeverWinMissionRuleFactory,
    PlayerHasToWinMissionRuleListFactory,
)

class TestStaticMissionRuleFactory:
    def test_create_never_win_with_number(self):
        rule = StaticMissionRuleFactory.create(
            MissionType.NEVER_WIN_WITH_NUMBER, 
            {MissionType.NEVER_WIN_WITH_NUMBER: {"mission_number": 7}}
        )
        assert isinstance(rule, NeverWinWithNumberRule)
        assert rule.number == 7

    def test_create_win_once_with_number(self):
        rule = StaticMissionRuleFactory.create(
            MissionType.WIN_ONCE_WITH_NUMBER,
            {MissionType.WIN_ONCE_WITH_NUMBER: {"mission_number": 3}}
        )
        assert isinstance(rule, WinOnceWithNumberRule)
        assert rule.number == 3

    def test_create_win_with_all_these_cards(self):
        cards = {BLUE_1, BLUE_2}
        rule = StaticMissionRuleFactory.create(
            MissionType.WIN_WITH_ALL_THESE_CARDS,
            {MissionType.WIN_WITH_ALL_THESE_CARDS: {"cards_that_need_to_win": cards}}
        )
        assert isinstance(rule, WinWithAllTheseCardsRule)
        assert rule.cards_that_need_to_win == cards

    def test_create_unsupported_type_raises(self):
        with pytest.raises(ValueError):
            StaticMissionRuleFactory.create(MissionType.PLAYER_HAS_TO_WIN_CARD, {})

class TestPlayerShouldNeverWinMissionRuleFactory:
    def test_create_returns_rule_with_selected_player(self):
        mock_interface = MagicMock()
        players = [
            create_player("Alice"),
            create_player("Bob"),
            create_player("Carol"),
        ]
        mock_interface.select_player_that_should_not_win.return_value = players[1]

        factory = PlayerShouldNeverWinMissionRuleFactory(mock_interface)
        rule = factory.create(players)

        assert isinstance(rule, PlayerShouldNeverWinRule)
        assert rule.player_that_should_never_win == players[1]
        mock_interface.select_player_that_should_not_win.assert_called_once_with(players)

class TestPlayerHasToWinMissionRuleListFactory:
    def setup_method(self):
        self.mock_interface = MagicMock()
        self.factory = PlayerHasToWinMissionRuleListFactory(self.mock_interface)

    def test_all_players_select_cards_no_skips(self):
        player_1 = create_player("P1")
        player_2 = create_player("P2`")
        player_3 = create_player("P3")

        mission_cards = [BLUE_8, PINK_2, BLUE_1, GREEN_3]

        selection_sequence = [BLUE_8, GREEN_3, PINK_2, BLUE_1]
        interface_args = self.mock_selected_cards_and_return_args(selection_sequence)

        players = [player_1, player_2, player_3]
        rules = self.factory.create(players, mission_cards)

        expected_mision_rules = set([
            PlayerHasToWinCardRule(player_1, BLUE_8),
            PlayerHasToWinCardRule(player_1, BLUE_1),
            PlayerHasToWinCardRule(player_2, GREEN_3),
            PlayerHasToWinCardRule(player_3, PINK_2),
        ])

        assert set(rules) == expected_mision_rules

        expected_calls = [
            (player_1.id, [BLUE_8, PINK_2, BLUE_1, GREEN_3], False),
            (player_2.id, [PINK_2, BLUE_1, GREEN_3], False),
            (player_3.id, [PINK_2, BLUE_1], False),
            (player_1.id, [BLUE_1], True),
        ]
        self.verify_interface_calls(interface_args, expected_calls)

    def test_first_player_select_card_others_dont_need_to(self):
        player_1 = create_player("P1")
        player_2 = create_player("P2`")
        player_3 = create_player("P3")

        mission_cards = [BLUE_8]

        selection_sequence = [BLUE_8]
        interface_args = self.mock_selected_cards_and_return_args(selection_sequence)

        players = [player_1, player_2, player_3]
        rules = self.factory.create(players, mission_cards)

        expected_mision_rules = set([
            PlayerHasToWinCardRule(player_1, BLUE_8),
        ])

        assert set(rules) == expected_mision_rules

        expected_calls = [
            (player_1.id, [BLUE_8], True)
        ]
        self.verify_interface_calls(interface_args, expected_calls)

    def test_first_player_skips_other_have_to_select(self):
        player_1 = create_player("P1")
        player_2 = create_player("P2`")
        player_3 = create_player("P3")

        mission_cards = [BLUE_8, PINK_2]

        selection_sequence = [None, BLUE_8, PINK_2]
        interface_args = self.mock_selected_cards_and_return_args(selection_sequence)

        players = [player_1, player_2, player_3]
        rules = self.factory.create(players, mission_cards)

        expected_mision_rules = set([
            PlayerHasToWinCardRule(player_2, BLUE_8),
            PlayerHasToWinCardRule(player_3, PINK_2),
        ])

        assert set(rules) == expected_mision_rules

        expected_calls = [
            (player_1.id, [BLUE_8, PINK_2], True),
            (player_2.id, [BLUE_8, PINK_2], False),
            (player_3.id, [PINK_2], False)
        ]
        self.verify_interface_calls(interface_args, expected_calls)

        
    def test_player_in_the_middle_skips_others_have_to_select(self):
        player_1 = create_player("P1")
        player_2 = create_player("P2`")
        player_3 = create_player("P3")

        mission_cards = [BLUE_8, PINK_2]

        selection_sequence = [BLUE_8, None, PINK_2]
        interface_args = self.mock_selected_cards_and_return_args(selection_sequence)

        players = [player_1, player_2, player_3]
        rules = self.factory.create(players, mission_cards)

        expected_mision_rules = set([
            PlayerHasToWinCardRule(player_1, BLUE_8),
            PlayerHasToWinCardRule(player_3, PINK_2),
        ])

        assert set(rules) == expected_mision_rules

        expected_calls = [
            (player_1.id, [BLUE_8, PINK_2], True),
            (player_2.id, [PINK_2], True),
            (player_3.id, [PINK_2], False)
        ]
        self.verify_interface_calls(interface_args, expected_calls)

    def test_all_players_but_last_skip(self):
        player_1 = create_player("P1")
        player_2 = create_player("P2`")
        player_3 = create_player("P3")

        mission_cards = [BLUE_8]

        selection_sequence = [None, None, BLUE_8]
        interface_args = self.mock_selected_cards_and_return_args(selection_sequence)

        players = [player_1, player_2, player_3]
        rules = self.factory.create(players, mission_cards)

        expected_mision_rules = set([
            PlayerHasToWinCardRule(player_3, BLUE_8)
        ])

        assert set(rules) == expected_mision_rules

        expected_calls = [
            (player_1.id, [BLUE_8], True),
            (player_2.id, [BLUE_8], True),
            (player_3.id, [BLUE_8], False)
        ]
        self.verify_interface_calls(interface_args, expected_calls)

    def test_players_skip_on_the_second_round_of_selection(self):
        player_1 = create_player("P1")
        player_2 = create_player("P2`")
        player_3 = create_player("P3")

        mission_cards = [BLUE_8, PINK_2, BLUE_1, GREEN_3]

        selection_sequence = [BLUE_8, GREEN_3, PINK_2, None, None, BLUE_1]
        interface_args = self.mock_selected_cards_and_return_args(selection_sequence)

        players = [player_1, player_2, player_3]
        rules = self.factory.create(players, mission_cards)

        expected_mision_rules = set([
            PlayerHasToWinCardRule(player_1, BLUE_8),
            PlayerHasToWinCardRule(player_2, GREEN_3),
            PlayerHasToWinCardRule(player_3, PINK_2),
            PlayerHasToWinCardRule(player_3, BLUE_1)
        ])

        assert set(rules) == expected_mision_rules

        expected_calls = [
            (player_1.id, [BLUE_8, PINK_2, BLUE_1, GREEN_3], False),
            (player_2.id, [PINK_2, BLUE_1, GREEN_3], False),
            (player_3.id, [PINK_2, BLUE_1], False),
            (player_1.id, [BLUE_1], True),
            (player_2.id, [BLUE_1], True),
            (player_3.id, [BLUE_1], False)
        ]
        self.verify_interface_calls(interface_args, expected_calls)

    def mock_selected_cards_and_return_args(self, selection_sequence):
        call_args = []
        def select_mission(player_id, available_cards, can_skip):
            call_args.append((player_id, list(available_cards), can_skip))
            return selection_sequence[len(call_args) - 1]

        self.mock_interface.select_mission.side_effect = select_mission
        return call_args
    
    def verify_interface_calls(self, interface_args, expected_calls):
        for i, (player_id, available_cards, can_skip) in enumerate(interface_args):
            exp_player_id, exp_available_cards, exp_can_skip = expected_calls[i]
            assert player_id == exp_player_id
            assert available_cards == exp_available_cards
            assert can_skip == exp_can_skip
