import pytest
from src.game.card_dealer import CardDealer
from src.model.card import ALL_CARDS
from tests.helpers.test_data_creation_helper import create_player

@pytest.fixture
def dealer_and_players(): #  -> tuple[CardDealer, list[Player]]
    """Fixture to set up a new CardDealer instance and four players."""
    dealer = CardDealer()
    players = [create_player(f"Player {i+1}") for i in range(4)]
    return dealer, players

def test_deal_cards(dealer_and_players):
    """Tests that all cards are distributed, no duplicates exist, and the captain is correct."""
    dealer, players = dealer_and_players
    players, captain = dealer.deal_cards(players)

    # Collect all dealt cards into a single list
    all_cards = [card for player in players for card in player.card_hand.cards]
    for player in players:
        print(player.name, player.is_captain(), len(player.card_hand.cards), player.card_hand)

    # Assert all cards in the deck were distributed
    assert set(all_cards) == set(ALL_CARDS)

    # Assert there are no duplicate cards
    assert len(all_cards) == len(set(all_cards))

    # Assert the captain is correctly identified
    assert captain is not None
    assert captain.is_captain()
