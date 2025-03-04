import pytest
from src.model.player_hand import CardHand
from src.model.card import BLUE_3, ROCKET_4, YELLOW_4, ROCKET_1
from tests.helpers.test_data_creation_helper import create_player

def test_not_captain():
    player = create_player("John")

    player.deal_card(BLUE_3)
    assert player.is_captain() is False

def test_captain():
    player = create_player("John")

    player.deal_card(ROCKET_4)
    assert player.is_captain() is True

def test_play_card_not_in_hand():
    player = create_player("John")

    with pytest.raises(ValueError):
        player.play_card(YELLOW_4)

def test_deal_and_play_cards():
    player = create_player("John")

    player.deal_card(ROCKET_4)
    player.deal_card(YELLOW_4)
    player.deal_card(ROCKET_1)
    assert player.card_hand == CardHand([ROCKET_4, YELLOW_4, ROCKET_1])

    player.play_card(ROCKET_1)
    assert player.card_hand == CardHand([ROCKET_4, YELLOW_4])
