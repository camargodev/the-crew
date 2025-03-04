from typing import Dict, Tuple, Set
from src.model.player_hand import Player
from src.model.card import Card, CardType

class RoundData:
    """
    Represents a round of the game, tracking which cards are
      played by which players and determining the winner.

    Attributes:
        players (list[Player]): A list of players participating in the round.
        card_by_player (Dict[Player, Card]): 
            A dictionary that maps each player to the card they played.
        round_type (CardType | None):
            The type of card played in the round (None if no card has been played yet).
    """
    def __init__(self, players: list[Player]):
        """
        Initializes the round data for a given list of players.

        Args:
            players (list[Player]): The players participating in the round.
        """
        self.players = players
        self.card_by_player: Dict[Player, Card] = {}
        self.round_type: CardType | None = None

    def add_played_card(self, player: Player, card: Card):
        """
        Adds a card played by a player to the round data.
        Ensures the card hasn't been played already.

        Args:
            player (Player): The player who played the card.
            card (Card): The card that was played.

        Raises:
            ValueError: If the card has already been played in the round.
        """
        if card in set(self.card_by_player.values()):
            raise ValueError("Card already played")

        self.card_by_player[player] = card

        if self.round_type is None:
            self.round_type = card.type

    def get_played_cards(self) -> Set[Card]:
        """
        Retrieves all cards that have been played during the round.

        Returns:
            Set[Card]: A set of cards that have been played in the round.
        """
        return set(self.card_by_player.values())

    def get_winner(self) -> Tuple[Player, Card]:
        """
        Determines the winner of the round based on the cards played.
        The winner is the player with the highest 
        number of the winning card type, or the round's type if no rocket cards were played.

        Returns:
            Tuple[Player, Card]: The winner player and their winning card.

        Raises:
            ValueError: If no cards have been played in the round.
        """
        played_types: Set[CardType] = {card.type for card in self.get_played_cards()}
        winning_type = CardType.ROCKET if CardType.ROCKET in played_types else self.round_type

        right_type_card_by_player = {
            player: card
            for player, card in self.card_by_player.items() if card.type == winning_type
        }

        winner = max(right_type_card_by_player,
                     key=lambda player: right_type_card_by_player[player].number)
        winning_card = right_type_card_by_player[winner]
        return winner, winning_card
