from typing import Tuple
from src.model.player_hand import Player
from src.model.card import Card
from src.model.round_data import RoundData
from src.game.interface.player_interface import PlayerInterface

class RoundEngine:
    def __init__(self, player_interface: PlayerInterface):
        self.player_interface = player_interface

    def play_round(self, players: list[Player], starter_player: Player) -> RoundData:
        round_data = RoundData(players)
        cards_played_count = 0
        while cards_played_count < len(players):
            current_player = self.__define_player__(players, starter_player, cards_played_count)
            card = self.player_interface.select_card(current_player)
            current_player.play_card(card)
            round_data.add_played_card(current_player, card)
            cards_played_count += 1
        return round_data

    def __define_player__(self, players: list[Player], starter_player: Player, cards_count: int) -> Player:
        starter_index = players.index(starter_player)
        return players[(starter_index + cards_count) % len(players)]

    # def player_play_card(self, player: Player, card: Card) -> Player:
    #     """Allows a player to play a card. Raises an error if the player has already played."""
    #     if player in self.round_data.card_by_player:
    #         raise ValueError(f"{player.name} has already played a card.")

    #     player.play_card(card)
    #     self.round_data.add_played_card(player, card)
    #     return player

