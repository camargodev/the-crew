import pytest
import punq
from unittest.mock import MagicMock
from src.model.card import *
from src.game.interface.player_interface import PlayerInterface
from src.game.round_engine import RoundEngine
from tests.helpers.test_data_creation_helper import create_player

pytest_plugins = ["pytest_mock"]

@pytest.fixture
def container(mocker):
    container = punq.Container()
    mock_interface = mocker.MagicMock()
    container.register(PlayerInterface, instance=mock_interface)
    container.register(RoundEngine)
    return container

def test_play_round(container):
    player_interface = container.resolve(PlayerInterface)
    engine = container.resolve(RoundEngine)

    player_1 = create_player("player1", [BLUE_9])
    player_2 = create_player("player2", [BLUE_3])
    player_3 = create_player("player3", [BLUE_1])
    player_4 = create_player("player4", [BLUE_5])

    players = [player_1, player_2, player_3, player_4]

    given_players_play(player_interface, {
        player_1: BLUE_9,
        player_2: BLUE_3,
        player_3: BLUE_1,
        player_4: BLUE_5
    })

    round_data = engine.play_round(players, starter_player = player_1)

    assert round_data.get_played_cards() == {BLUE_9, BLUE_3, BLUE_1, BLUE_5}

    for player in players:
        player_interface.select_card.assert_any_call(player)
        assert len(player.card_hand.cards) == 0

def given_players_play(mock_interface, mapping):
    def select_card_side_effect(player):
        return mapping.get(player)
    mock_interface.select_card.side_effect = select_card_side_effect