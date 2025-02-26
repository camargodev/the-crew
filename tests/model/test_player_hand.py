import pytest
from src.model.player_hand import Player, CardHand
from src.model.card import Card, CardType

def test_not_captain():
    player = Player("John", CardHand([]))

    player.deal_card(Card(CardType.BLUE, 3))
    assert player.is_captain() == False

def test_captain():
    player = Player("John", CardHand([]))

    player.deal_card(Card(CardType.ROCKET, 4))
    assert player.is_captain() == True

def test_play_card_not_in_hand():
    player = Player("John", CardHand([]))

    with pytest.raises(ValueError):
        player.play_card(Card(CardType.YELLOW, 5))

def test_deal_and_play_cards():
    player = Player("John", CardHand([]))

    player.deal_card(Card(CardType.ROCKET, 4))
    player.deal_card(Card(CardType.YELLOW, 5))
    player.deal_card(Card(CardType.ROCKET, 1))
    assert player.card_hand == CardHand([Card(CardType.ROCKET, 4), Card(CardType.YELLOW, 5), Card(CardType.ROCKET, 1)])

    player.play_card(Card(CardType.ROCKET, 1))
    assert player.card_hand == CardHand([Card(CardType.ROCKET, 4), Card(CardType.YELLOW, 5)])
