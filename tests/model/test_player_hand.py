import pytest
from src.model.player_hand import Player, CardHand
from src.model.card import Card, CardType
from src.model.card import *

def test_not_captain():
    player = Player("John", CardHand([]))

    player.deal_card(BLUE_3)
    assert player.is_captain() == False

def test_captain():
    player = Player("John", CardHand([]))

    player.deal_card(ROCKET_4)
    assert player.is_captain() == True

def test_play_card_not_in_hand():
    player = Player("John", CardHand([]))

    with pytest.raises(ValueError):
        player.play_card(YELLOW_4)

def test_deal_and_play_cards():
    player = Player("John", CardHand([]))

    player.deal_card(ROCKET_4)
    player.deal_card(YELLOW_4)
    player.deal_card(ROCKET_1)
    assert player.card_hand == CardHand([ROCKET_4, YELLOW_4, ROCKET_1])

    player.play_card(ROCKET_1)
    assert player.card_hand == CardHand([ROCKET_4, YELLOW_4])
