import pytest
from src.model.player_hand import Player, CardHand
from src.model.card import BLUE_6, BLUE_8
from tests.helpers.test_data_creation_helper import create_finished_round, create_test_game

PLAYER_1 = Player("PLAYER_1", CardHand())

def test_game_finished():
    game_round = create_finished_round({})
    game = create_test_game(num_of_rounds=1, rounds_already_played=[game_round])
    assert game.is_finished() is True

def test_game_not_finished():
    game_round = create_finished_round({})
    game = create_test_game(num_of_rounds=8, rounds_already_played=[game_round])
    assert game.is_finished() is False

def test_get_last_round():
    round_1 = create_finished_round({PLAYER_1: BLUE_8})
    round_2 = create_finished_round({PLAYER_1: BLUE_6})
    game = create_test_game(num_of_rounds=8, rounds_already_played=[round_1, round_2])
    assert game.get_last_round() == round_2

def test_get_last_round_raises_error_when_there_are_no_rounds():
    game = create_test_game(num_of_rounds=8, rounds_already_played=[])
    with pytest.raises(ValueError):
        game.get_last_round()
