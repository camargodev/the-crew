import pytest
from src.model.card import CardType
from src.game.round_engine import RoundEngine
from src.model.card import *
from tests.helpers.test_data_creation_helper import create_player

def test_initial_round_type():
    """Test if round_type is initially None."""
    game_round = RoundEngine([])
    assert game_round.round_data.round_type is None


def test_player_play_card():
    """Test if a player can play a card."""
    john = create_player("John", [ROCKET_2])

    # Player should be able to play the card
    game_round = RoundEngine(players = [john])
    played_player = game_round.player_play_card(john, ROCKET_2)
    assert played_player == john
    assert game_round.round_data.card_by_player[john] == ROCKET_2
    assert game_round.round_data.round_type == CardType.ROCKET


def test_player_play_card_twice():
    """Test if a player cannot play more than one card."""
    john = create_player("John", [BLUE_3, BLUE_7])

    # First card should work
    game_round = RoundEngine(players = [john])
    game_round.player_play_card(john, BLUE_3)

    # Second card should raise an error
    with pytest.raises(ValueError):
        game_round.player_play_card(john, BLUE_7)

        
def test_get_round_winner_no_cards_played():
    """Test if no winner is determined if no cards are played."""
    john = create_player("John", [BLUE_3, BLUE_7])

    game_round = RoundEngine(players = [john])

    # Impossible to determine winner, as not all players played yet
    with pytest.raises(ValueError):
        game_round.get_round_winner()

def test_get_round_winner_non_rocket():
    """Test if the winner is determined correctly for non-rocket cards."""
    john = create_player("John", [BLUE_3])
    julie = create_player("Julie", [BLUE_7])
    matthew = create_player("Matthew", [BLUE_5])

    game_round = RoundEngine(players = [john, julie, matthew])

    # Players play their cards
    game_round.player_play_card(john, BLUE_3)
    game_round.player_play_card(julie, BLUE_7)
    game_round.player_play_card(matthew, BLUE_5)

    # Winner should be the player who played the highest card
    winner, winning_card = game_round.get_round_winner()
    assert winner == julie
    assert winning_card == BLUE_7

def test_get_round_winner_rocket_wins():
    """Test if Rocket cards win over non-rocket cards."""    
    john = create_player("John", [BLUE_3])
    julie = create_player("Julie", [BLUE_7])
    matthew = create_player("Matthew", [ROCKET_2])

    game_round = RoundEngine(players = [john, julie, matthew])

    # Players play their cards
    game_round.player_play_card(john, BLUE_3)
    game_round.player_play_card(julie, BLUE_7)
    game_round.player_play_card(matthew, ROCKET_2)

    # Winner should be the player who played the highest card
    winner, winning_card = game_round.get_round_winner()
    assert winner == matthew
    assert winning_card == ROCKET_2

def test_get_round_winner_wrong_type_are_ignored():
    """Test that only cards of the correct type are considered"""    
    john = create_player("John", [BLUE_1])
    julie = create_player("Julie", [YELLOW_9])
    matthew = create_player("Matthew", [PINK_9])

    game_round = RoundEngine(players = [john, julie, matthew])

    # Players play their cards
    game_round.player_play_card(john, BLUE_1)
    game_round.player_play_card(julie, YELLOW_9)
    game_round.player_play_card(matthew, PINK_9)

    # Winner should be the player who played the highest card
    winner, winning_card = game_round.get_round_winner()
    assert winner == john
    assert winning_card == BLUE_1

def test_get_round_winner_ROCKET_highest():
    """Test if the highest Rocket card wins."""   
    john = create_player("John", [ROCKET_4])
    julie = create_player("Julie", [BLUE_1])
    matthew = create_player("Matthew", [ROCKET_1])
    anne = create_player("Anne", [YELLOW_9])
    luke = create_player("Luke", [ROCKET_2])

    game_round = RoundEngine(players = [john, julie, matthew, anne, luke])

    # Players play their cards
    game_round.player_play_card(john, ROCKET_4)
    game_round.player_play_card(julie, BLUE_1)
    game_round.player_play_card(matthew, ROCKET_1)
    game_round.player_play_card(anne, YELLOW_9)
    game_round.player_play_card(luke, ROCKET_2)

    # Winner should be the player who played the highest card
    winner, winning_card = game_round.get_round_winner()
    assert winner == john
    assert winning_card == ROCKET_4
