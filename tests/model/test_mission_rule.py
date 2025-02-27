from src.model.card import Card, CardType
from src.model.player_hand import Player, CardHand
from src.model.round_data import RoundData
from src.model.game_data import GameData
from src.model.mission import (
    PlayerHasToWinCardRule,
    NeverWinWithNumberRule,
    WinOnceWithNumberRule,
    WinWithAllTheseCardsRule,
    PlayerShouldNeverWinRule,
)

PLAYER_1 = Player("PLAYER_1", CardHand())
PLAYER_2 = Player("PLAYER_2", CardHand())

BLUE_6 = Card(CardType.BLUE, 6)
BLUE_8 = Card(CardType.BLUE, 8)
YELLOW_9 = Card(CardType.YELLOW, 9)
YELLOW_5 = Card(CardType.YELLOW, 5)
ROCKET_1 = Card(CardType.ROCKET, 1)
ROCKET_2 = Card(CardType.ROCKET, 2)
ROCKET_3 = Card(CardType.ROCKET, 3)
ROCKET_4 = Card(CardType.ROCKET, 4)
PINK_2 = Card(CardType.PINK, 2)
GREEN_4 = Card(CardType.GREEN, 4)
PINK_1 = Card(CardType.PINK, 1)
ALL_ROCKETS = {ROCKET_1, ROCKET_2, ROCKET_3, ROCKET_4}

def test_player_has_to_win_card_rule__player_won_card():
    rounds = [create_finished_round({PLAYER_1: BLUE_8, PLAYER_2: BLUE_6})]
    game = create_test_game(num_of_rounds=8, rounds_already_played=rounds)
    
    rule = PlayerHasToWinCardRule(PLAYER_1, BLUE_8)
    assert rule.is_rule_satisfied(game) == True
    assert rule.is_rule_broken(game) == False

def test_player_has_to_win_card_rule__player_played_card_but_lost_round():
    rounds = [ create_finished_round({PLAYER_1: BLUE_6, PLAYER_2: BLUE_8})]
    game = create_test_game(num_of_rounds=8, rounds_already_played=rounds)
    
    rule = PlayerHasToWinCardRule(PLAYER_1, BLUE_6)
    assert rule.is_rule_satisfied(game) == False
    assert rule.is_rule_broken(game) == True

def test_player_has_to_win_card_rule__other_player_played_and_won_card():
    rounds = [create_finished_round({PLAYER_1: BLUE_6, PLAYER_2: BLUE_8})]
    game = create_test_game(num_of_rounds=8, rounds_already_played=rounds)
    
    rule = PlayerHasToWinCardRule(PLAYER_1, BLUE_8)
    assert rule.is_rule_satisfied(game) == False
    assert rule.is_rule_broken(game) == True

def test_player_has_to_win_card_rule__card_not_played_yet():
    rounds = [create_finished_round({PLAYER_1: BLUE_6, PLAYER_2: BLUE_8})]
    game = create_test_game(num_of_rounds=8, rounds_already_played=rounds)
    
    rule = PlayerHasToWinCardRule(PLAYER_1, PINK_2)
    assert rule.is_rule_satisfied(game) == False
    assert rule.is_rule_broken(game) == False

def test_never_win_with_number_rule__game_finished_number_didnt_win():
    rounds = [
        create_finished_round({PLAYER_1: BLUE_6, PLAYER_2: BLUE_8}),
        create_finished_round({PLAYER_1: GREEN_4, PLAYER_2: ROCKET_2}),
        create_finished_round({PLAYER_1: PINK_2, PLAYER_2: YELLOW_5})
    ]
    game = create_test_game(num_of_rounds=3, rounds_already_played=rounds)
    
    rule = NeverWinWithNumberRule(number=9)
    assert rule.is_rule_satisfied(game) == True
    assert rule.is_rule_broken(game) == False

def test_never_win_with_number_rule__game_not_finished_number_didnt_win_yet():
    rounds = [
        create_finished_round({PLAYER_1: BLUE_6, PLAYER_2: BLUE_8}),
        create_finished_round({PLAYER_1: GREEN_4, PLAYER_2: ROCKET_2}),
        create_finished_round({PLAYER_1: PINK_2, PLAYER_2: YELLOW_5})
    ]
    game = create_test_game(num_of_rounds=4, rounds_already_played=rounds)
    
    rule = NeverWinWithNumberRule(number=9)
    assert rule.is_rule_satisfied(game) == False
    assert rule.is_rule_broken(game) == False

def test_never_win_with_number_rule__game_not_finished_but_number_won():
    rounds = [create_finished_round({PLAYER_1: YELLOW_9, PLAYER_2: YELLOW_5})]
    game = create_test_game(num_of_rounds=4, rounds_already_played=rounds)
    
    rule = NeverWinWithNumberRule(number=9)
    assert rule.is_rule_satisfied(game) == False
    assert rule.is_rule_broken(game) == True

def test_win_once_with_number_rule__game_not_finished_number_won():
    rounds = [
        create_finished_round({PLAYER_1: BLUE_6, PLAYER_2: BLUE_8}),
        create_finished_round({PLAYER_1: GREEN_4, PLAYER_2: ROCKET_2}),
        create_finished_round({PLAYER_1: PINK_1, PLAYER_2: YELLOW_5})
    ]
    game = create_test_game(num_of_rounds=8, rounds_already_played=rounds)
    
    rule = WinOnceWithNumberRule(number=1)
    assert rule.is_rule_satisfied(game) == True
    assert rule.is_rule_broken(game) == False

def test_win_once_with_number_rule__game_not_finished_number_didnt_win_yet():
    rounds = [
        create_finished_round({PLAYER_1: BLUE_6, PLAYER_2: BLUE_8}),
        create_finished_round({PLAYER_1: GREEN_4, PLAYER_2: ROCKET_2}),
        create_finished_round({PLAYER_1: PINK_2, PLAYER_2: YELLOW_5})
    ]
    game = create_test_game(num_of_rounds=8, rounds_already_played=rounds)
    
    rule = WinOnceWithNumberRule(number=9)
    assert rule.is_rule_satisfied(game) == False
    assert rule.is_rule_broken(game) == False

def test_win_once_with_number_rule__game_finished_but_number_didnt_win():
    rounds = [
        create_finished_round({PLAYER_1: BLUE_6, PLAYER_2: BLUE_8}),
        create_finished_round({PLAYER_1: GREEN_4, PLAYER_2: ROCKET_2}),
        create_finished_round({PLAYER_1: PINK_2, PLAYER_2: YELLOW_5})
    ]
    game = create_test_game(num_of_rounds=3, rounds_already_played=rounds)
    
    rule = WinOnceWithNumberRule(number=1)
    assert rule.is_rule_satisfied(game) == False
    assert rule.is_rule_broken(game) == True

def test_win_with_all_these_cards__game_not_finished_but_all_cards_won():
    rounds = [
        create_finished_round({PLAYER_1: ROCKET_1, PLAYER_2: BLUE_8}),
        create_finished_round({PLAYER_1: ROCKET_2, PLAYER_2: ROCKET_2}),
        create_finished_round({PLAYER_1: ROCKET_3, PLAYER_2: YELLOW_5}),
        create_finished_round({PLAYER_1: ROCKET_4, PLAYER_2: YELLOW_5})
    ]
    game = create_test_game(num_of_rounds=8, rounds_already_played=rounds)
    
    rule = WinWithAllTheseCardsRule(cards_that_need_to_win=ALL_ROCKETS)
    assert rule.is_rule_satisfied(game) == True
    assert rule.is_rule_broken(game) == False

def test_win_with_all_these_cards__game_not_finished_but_not_all_cards_won_yet():
    rounds = [
        create_finished_round({PLAYER_1: ROCKET_1, PLAYER_2: BLUE_8}),
        create_finished_round({PLAYER_1: ROCKET_2, PLAYER_2: ROCKET_2})
    ]
    game = create_test_game(num_of_rounds=8, rounds_already_played=rounds)
    
    rule = WinWithAllTheseCardsRule(cards_that_need_to_win=ALL_ROCKETS)
    assert rule.is_rule_satisfied(game) == False
    assert rule.is_rule_broken(game) == False

def test_win_with_all_these_cards__game_finished_but_not_all_cards_won():
    rounds = [
        create_finished_round({PLAYER_1: ROCKET_1, PLAYER_2: BLUE_8}),
        create_finished_round({PLAYER_1: ROCKET_2, PLAYER_2: ROCKET_2})
    ]
    game = create_test_game(num_of_rounds=2, rounds_already_played=rounds)
    
    rule = WinWithAllTheseCardsRule(cards_that_need_to_win=ALL_ROCKETS)
    assert rule.is_rule_satisfied(game) == False
    assert rule.is_rule_broken(game) == True
    
def test_player_should_never_win__game_finished_and_player_didnt_win():
    rounds = [
        create_finished_round({PLAYER_1: ROCKET_1, PLAYER_2: BLUE_8}),
        create_finished_round({PLAYER_1: ROCKET_2, PLAYER_2: PINK_1})
    ]
    game = create_test_game(num_of_rounds=2, rounds_already_played=rounds)
    
    rule = PlayerShouldNeverWinRule(player_that_should_never_win=PLAYER_2)
    assert rule.is_rule_satisfied(game) == True
    assert rule.is_rule_broken(game) == False

def test_player_should_never_win__game_not_finished_and_player_didnt_win_yet():
    rounds = [
        create_finished_round({PLAYER_1: ROCKET_1, PLAYER_2: BLUE_8}),
        create_finished_round({PLAYER_1: ROCKET_2, PLAYER_2: PINK_1})
    ]
    game = create_test_game(num_of_rounds=8, rounds_already_played=rounds)
    
    rule = PlayerShouldNeverWinRule(player_that_should_never_win=PLAYER_2)
    assert rule.is_rule_satisfied(game) == False
    assert rule.is_rule_broken(game) == False

    
def test_player_should_never_win__game_not_finished_and_player_won():
    rounds = [
        create_finished_round({PLAYER_1: ROCKET_1, PLAYER_2: BLUE_8}),
        create_finished_round({PLAYER_1: ROCKET_2, PLAYER_2: ROCKET_4})
    ]
    game = create_test_game(num_of_rounds=8, rounds_already_played=rounds)
    
    rule = PlayerShouldNeverWinRule(player_that_should_never_win=PLAYER_2)
    assert rule.is_rule_satisfied(game) == False
    assert rule.is_rule_broken(game) == True

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

