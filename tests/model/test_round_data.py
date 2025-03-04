      
import pytest
from src.model.card import *
from src.model.round_data import RoundData
from tests.helpers.test_data_creation_helper import create_player

def test_play_duplicated_card():
    """Test if no winner is determined if no cards are played."""
    john = create_player("John", [BLUE_3, BLUE_7])

    round_data = RoundData(players = [john])

    # Impossible to determine winner, as not all players played yet
    round_data.add_played_card(john, BLUE_3)
    with pytest.raises(ValueError):
        round_data.add_played_card(john, BLUE_3)

def test_get_winner_no_cards_played():
    """Test if no winner is determined if no cards are played."""
    john = create_player("John", [BLUE_3, BLUE_7])

    round_data = RoundData(players = [john])

    # Impossible to determine winner, as not all players played yet
    with pytest.raises(ValueError):
        round_data.get_winner()

def test_get_winner_non_rocket():
    """Test if the winner is determined correctly for non-rocket cards."""
    john = create_player("John", [BLUE_3])
    julie = create_player("Julie", [BLUE_7])
    matthew = create_player("Matthew", [BLUE_5])

    round_data = RoundData(players = [john, julie, matthew])

    # Players play their cards
    round_data.add_played_card(john, BLUE_3)
    round_data.add_played_card(julie, BLUE_7)
    round_data.add_played_card(matthew, BLUE_5)

    # Winner should be the player who played the highest card
    winner, winning_card = round_data.get_winner()
    assert winner == julie
    assert winning_card == BLUE_7

def test_get_winner_rocket_wins():
    """Test if Rocket cards win over non-rocket cards."""    
    john = create_player("John", [BLUE_3])
    julie = create_player("Julie", [BLUE_7])
    matthew = create_player("Matthew", [ROCKET_2])

    round_data = RoundData(players = [john, julie, matthew])

    # Players play their cards
    round_data.add_played_card(john, BLUE_3)
    round_data.add_played_card(julie, BLUE_7)
    round_data.add_played_card(matthew, ROCKET_2)

    # Winner should be the player who played the highest card
    winner, winning_card = round_data.get_winner()
    assert winner == matthew
    assert winning_card == ROCKET_2

def test_get_winner_wrong_type_are_ignored():
    """Test that only cards of the correct type are considered"""    
    john = create_player("John", [BLUE_1])
    julie = create_player("Julie", [YELLOW_9])
    matthew = create_player("Matthew", [PINK_9])

    round_data = RoundData(players = [john, julie, matthew])

    # Players play their cards
    round_data.add_played_card(john, BLUE_1)
    round_data.add_played_card(julie, YELLOW_9)
    round_data.add_played_card(matthew, PINK_9)

    # Winner should be the player who played the highest card
    winner, winning_card = round_data.get_winner()
    assert winner == john
    assert winning_card == BLUE_1

def test_get_winner_ROCKET_highest():
    """Test if the highest Rocket card wins."""   
    john = create_player("John", [ROCKET_4])
    julie = create_player("Julie", [BLUE_1])
    matthew = create_player("Matthew", [ROCKET_1])
    anne = create_player("Anne", [YELLOW_9])
    luke = create_player("Luke", [ROCKET_2])

    round_data = RoundData(players = [john, julie, matthew, anne, luke])

    # Players play their cards
    round_data.add_played_card(john, ROCKET_4)
    round_data.add_played_card(julie, BLUE_1)
    round_data.add_played_card(matthew, ROCKET_1)
    round_data.add_played_card(anne, YELLOW_9)
    round_data.add_played_card(luke, ROCKET_2)

    # Winner should be the player who played the highest card
    winner, winning_card = round_data.get_winner()
    assert winner == john
    assert winning_card == ROCKET_4
