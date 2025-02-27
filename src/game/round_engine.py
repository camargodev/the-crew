from typing import Tuple
from src.model.player_hand import Player
from src.model.card import Card
from src.model.round_data import RoundData

class RoundEngine:
    def __init__(self, players: list[Player]):
        self.round_data = RoundData(players)

    def player_play_card(self, player: Player, card: Card) -> Player:
        """Allows a player to play a card. Raises an error if the player has already played."""
        # Check if the player has already played
        if player in self.round_data.card_by_player:
            raise ValueError(f"{player.name} has already played a card.")

        player.play_card(card)
        self.round_data.add_played_card(player, card)
        return player

    def get_round_winner(self) -> Tuple[Player, Card] | None:
        """Returns the player who played the strongest card of the round, along with the card."""
        if len(self.round_data.card_by_player) != len(self.round_data.players):
            raise ValueError("Not all players have played a card.")

        return self.round_data.get_winner()
