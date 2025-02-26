from typing import Dict, Tuple, Set
from src.model.player_hand import Player
from src.model.card import Card, CardType

class RoundData:
    def __init__(self, players: list[Player]):
        self.players = players
        self.card_by_player: Dict[Player, Card] = {}  # Dictionary to track which player has played which card
        self.round_type: CardType | None = None  # Variable to store the type of the card in the round

    def add_played_card(self, player: Player, card: Card):
        self.card_by_player[player] = card

        # If it's the first card played in the round, store its type
        if self.round_type is None:
            self.round_type = card.type

    def get_played_cards(self) -> Set[Card]:
        return {card for card in self.card_by_player.values()}

    def get_winner(self) -> Tuple[Player, Card]:
        played_types: Set[CardType] = {card.type for card in self.get_played_cards()}
        winning_type = CardType.ROCKET if CardType.ROCKET in played_types else self.round_type

        right_type_card_by_player = {
            player: card for player, card in self.card_by_player.items() if card.type == winning_type
        }
        winner = max(right_type_card_by_player, key=lambda player: right_type_card_by_player[player].number)
        winning_card = right_type_card_by_player[winner]
        return winner, winning_card

class GameRound:
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
