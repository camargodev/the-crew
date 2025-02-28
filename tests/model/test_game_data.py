import pytest
from src.model.round_data import RoundData
from src.model.game_data import GameData
from src.model.player_hand import Player, CardHand
from src.model.card import Card
from src.model.card import *

PLAYER_1 = Player("PLAYER_1", CardHand())

def test_game_finished():
    round = create_finished_round(dict())
    game = create_test_game(num_of_rounds=1, rounds_already_played=[round])
    assert game.is_finished() == True

def test_game_not_finished():
    round = create_finished_round(dict())
    game = create_test_game(num_of_rounds=8, rounds_already_played=[round])
    assert game.is_finished() == False

def test_get_last_round():
    round_1 = create_finished_round({PLAYER_1: BLUE_8})
    round_2 = create_finished_round({PLAYER_1: BLUE_6})
    game = create_test_game(num_of_rounds=8, rounds_already_played=[round_1, round_2])
    assert game.get_last_round() == round_2

def test_get_last_round():
    game = create_test_game(num_of_rounds=8, rounds_already_played=[])
    with pytest.raises(ValueError):
        game.get_last_round()

def create_finished_round(card_by_player: dict[Player, Card]) -> GameData:
    players = card_by_player.keys
    round = RoundData(players)
    for player, card in card_by_player.items():
        round.add_played_card(player, card)
    return round

def create_test_game(num_of_rounds, rounds_already_played: list[RoundData]) -> GameData:
    game =  GameData(num_of_rounds)
    for round in rounds_already_played:
        game.add_round(round)
    return game
