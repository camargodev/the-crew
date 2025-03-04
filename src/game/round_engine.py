from src.model.player_hand import Player
from src.model.round_data import RoundData
from src.game.interface.player_interface import PlayerInterface

class RoundEngine:
    """
    Class responsible for managing a round of the game.
    This engine handles the logic for playing a round,]
    including card selection and round data tracking.
    """

    def __init__(self, player_interface: PlayerInterface):
        self.player_interface = player_interface

    def play_round(self, players: list[Player], starter_player: Player) -> RoundData:
        """
        Executes a round of the game, allowing players to play cards in turn order, 
        and returns the round data (played cards, player actions, etc.).

        Args:
            players (list[Player]): List of players participating in the round.
            starter_player (Player): The player who starts the round.

        Returns:
            RoundData: The data of the played round, including played cards.
        """
        round_data = RoundData(players)
        cards_played_count = 0
        while cards_played_count < len(players):
            current_player = self.__define_player__(players, starter_player, cards_played_count)
            card = self.player_interface.select_card(current_player)
            current_player.play_card(card)
            round_data.add_played_card(current_player, card)
            cards_played_count += 1
        return round_data

    def __define_player__(
            self,
            players: list[Player],
            starter_player: Player,
            cards_count: int) -> Player:
        starter_index = players.index(starter_player)
        return players[(starter_index + cards_count) % len(players)]
