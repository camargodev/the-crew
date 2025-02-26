from typing import Dict, Tuple
from src.model.player_hand import Player
from src.model.card import Card, CardType

class GameRound:
    def __init__(self, players: list[Player]):
        self.players = players
        self.played_cards: Dict[Player, Card] = {}  # Dictionary to track which player has played which card
        self.round_type: CardType | None = None  # Variable to store the type of the card in the round

    def player_play_card(self, player: Player, card: Card) -> Player:
        """Allows a player to play a card. Raises an error if the player has already played."""
        # Check if the player has already played
        if player in self.played_cards:
            raise ValueError(f"{player.name} has already played a card.")

        # If it's the first card played in the round, store its type
        if self.round_type is None:
            self.round_type = card.type

        player.play_card(card)
        self.played_cards[player] = card
        return player

    def get_round_winner(self) -> Tuple[Player, Card] | None:
        """Returns the player who played the strongest card of the round, along with the card."""
        if len(self.played_cards) != len(self.players):
            raise ValueError("Not all players have played a card.")

        # Separate the played cards into rockets and non-rockets
        rocket_cards = {
            player: card for player, card in self.played_cards.items() if card.type == CardType.ROCKET
        }
        # Only cards of the valid type (first card) should be considered
        non_rocket_cards = {
            player: card for player, card in self.played_cards.items() if card.type == self.round_type
        }

        # If there are Rocket cards, find the one with the highest number
        # Otherwise, find the winner among non-Rocket cards
        if rocket_cards:
            winner = max(rocket_cards, key=lambda player: rocket_cards[player].number)
            winning_card = rocket_cards[winner]
        else:
            winner = max(non_rocket_cards, key=lambda player: non_rocket_cards[player].number)
            winning_card = non_rocket_cards[winner]

        return winner, winning_card
