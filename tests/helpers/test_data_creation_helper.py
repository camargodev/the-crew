from src.model.round_data import RoundData
from src.model.game_data import GameData
from src.model.player_hand import Player, Card, CardHand

def create_player(name: str, hand_cards: list[Card] = []) -> Player:
    card_hand = CardHand(hand_cards) if len(hand_cards) > 0 else CardHand([])
    return Player(name, card_hand)

def create_finished_round(card_by_player: dict[Player, Card]) -> RoundData:
    players = card_by_player.keys()
    round = RoundData(players)
    for player, card in card_by_player.items():
        round.add_played_card(player, card)
    return round

def create_test_game(num_of_rounds, rounds_already_played: list[RoundData]) -> GameData:
    game = GameData(num_of_rounds)
    for round in rounds_already_played:
        game.add_round(round)
    return game
