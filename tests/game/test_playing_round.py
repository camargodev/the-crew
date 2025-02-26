import pytest
from src.model.player_hand import Player, CardHand
from src.model.card import Card, CardType
from src.game.playing_round import GameRound


def test_initial_round_type():
    """Test if round_type is initially None."""
    game_round = GameRound([])
    assert game_round.round_type is None


def test_player_play_card():
    """Test if a player can play a card."""
    rocket_2 = Card(CardType.ROCKET, 2)
    john = Player("John", CardHand([rocket_2]))

    # Player should be able to play the card
    game_round = GameRound(players = [john])
    played_player = game_round.player_play_card(john, rocket_2)
    assert played_player == john
    assert game_round.played_cards[john] == rocket_2
    assert game_round.round_type == CardType.ROCKET


def test_player_play_card_twice():
    """Test if a player cannot play more than one card."""
    blue_3 = Card(CardType.BLUE, 3)
    blue_7 = Card(CardType.BLUE, 7)
    john = Player("John", CardHand([blue_3, blue_7]))

    # First card should work
    game_round = GameRound(players = [john])
    game_round.player_play_card(john, blue_3)

    # Second card should raise an error
    with pytest.raises(ValueError):
        game_round.player_play_card(john, blue_7)

        
def test_get_round_winner_no_cards_played():
    """Test if no winner is determined if no cards are played."""
    john = Player("John", CardHand([Card(CardType.BLUE, 3), Card(CardType.BLUE, 7)]))

    game_round = GameRound(players = [john])

    # Impossible to determine winner, as not all players played yet
    with pytest.raises(ValueError):
        game_round.get_round_winner()

def test_get_round_winner_non_rocket():
    """Test if the winner is determined correctly for non-rocket cards."""
    blue_3 = Card(CardType.BLUE, 3)
    blue_7 = Card(CardType.BLUE, 7)
    blue_5 = Card(CardType.BLUE, 5)

    john = Player("John", CardHand([blue_3]))
    julie = Player("Julie", CardHand([blue_7]))
    matthew = Player("Matthew", CardHand([blue_5]))

    game_round = GameRound(players = [john, julie, matthew])

    # Players play their cards
    game_round.player_play_card(john, blue_3)
    game_round.player_play_card(julie, blue_7)
    game_round.player_play_card(matthew, blue_5)

    # Winner should be the player who played the highest card
    winner, winning_card = game_round.get_round_winner()
    assert winner == julie
    assert winning_card == blue_7

def test_get_round_winner_rocket_wins():
    """Test if Rocket cards win over non-rocket cards."""
    blue_3 = Card(CardType.BLUE, 3)
    blue_7 = Card(CardType.BLUE, 7)
    rocket_2 = Card(CardType.ROCKET, 2)
    
    john = Player("John", CardHand([blue_3]))
    julie = Player("Julie", CardHand([blue_7]))
    matthew = Player("Matthew", CardHand([rocket_2]))

    game_round = GameRound(players = [john, julie, matthew])

    # Players play their cards
    game_round.player_play_card(john, blue_3)
    game_round.player_play_card(julie, blue_7)
    game_round.player_play_card(matthew, rocket_2)

    # Winner should be the player who played the highest card
    winner, winning_card = game_round.get_round_winner()
    assert winner == matthew
    assert winning_card == rocket_2

def test_get_round_winner_wrong_type_are_ignored():
    """Test that only cards of the correct type are considered"""
    blue_1 = Card(CardType.BLUE, 1)
    yellow_9 = Card(CardType.YELLOW, 9)
    pink_9 = Card(CardType.PINK, 9)
    
    john = Player("John", CardHand([blue_1]))
    julie = Player("Julie", CardHand([yellow_9]))
    matthew = Player("Matthew", CardHand([pink_9]))

    game_round = GameRound(players = [john, julie, matthew])

    # Players play their cards
    game_round.player_play_card(john, blue_1)
    game_round.player_play_card(julie, yellow_9)
    game_round.player_play_card(matthew, pink_9)

    # Winner should be the player who played the highest card
    winner, winning_card = game_round.get_round_winner()
    assert winner == john
    assert winning_card == blue_1

def test_get_round_winner_rocket_highest():
    """Test if the highest Rocket card wins."""
    rocket_4 = Card(CardType.ROCKET, 4)
    blue_1 = Card(CardType.BLUE, 1)
    rocket_1 = Card(CardType.ROCKET, 1)
    yellow_9 = Card(CardType.YELLOW, 9)
    rocket_2 = Card(CardType.ROCKET, 2)
    
    john = Player("John", CardHand([rocket_4]))
    julie = Player("Julie", CardHand([blue_1]))
    matthew = Player("Matthew", CardHand([rocket_1]))
    anne = Player("Anne", CardHand([yellow_9]))
    luke = Player("Luke", CardHand([rocket_2]))

    game_round = GameRound(players = [john, julie, matthew, anne, luke])

    # Players play their cards
    game_round.player_play_card(john, rocket_4)
    game_round.player_play_card(julie, blue_1)
    game_round.player_play_card(matthew, rocket_1)
    game_round.player_play_card(anne, yellow_9)
    game_round.player_play_card(luke, rocket_2)

    # Winner should be the player who played the highest card
    winner, winning_card = game_round.get_round_winner()
    assert winner == john
    assert winning_card == rocket_4
