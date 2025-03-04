from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.model.player_hand import Player
from src.model.card import Card, CardsOperation
from src.model.game_data import GameData

class MissionRule(ABC):
    """
    Abstract base class for defining mission rules in the game.
    Each rule must define how it is satisfied and how it is broken.
    """

    @abstractmethod
    def is_rule_satisfied(self, game_data: GameData) -> bool:
        """
        Check if the mission rule is satisfied based on the current game data.

        Args:
            game_data: The current state of the game.

        Returns:
            True if the rule is satisfied, False otherwise.
        """

    @abstractmethod
    def is_rule_broken(self, game_data: GameData) -> bool:
        """
        Check if the mission rule is broken based on the current game data.

        Args:
            game_data: The current state of the game.

        Returns:
            True if the rule is broken, False otherwise.
        """

@dataclass(frozen=True)
class PlayerHasToWinCardRule(MissionRule):
    """
    Rule that specifies a player must win with a specific card.
    """
    player: Player
    card: Card

    def is_rule_satisfied(self, game_data: GameData) -> bool:
        last_round = game_data.get_last_round()
        if self.card not in last_round.get_played_cards():
            return False
        winner, _ = last_round.get_winner()
        return winner == self.player

    def is_rule_broken(self, game_data: GameData) -> bool:
        last_round = game_data.get_last_round()
        if self.card not in last_round.get_played_cards():
            return False
        winner, _ = last_round.get_winner()
        return winner != self.player

@dataclass(frozen=True)
class NeverWinWithNumberRule(MissionRule):
    """
    Rule that specifies a player must never win with a specific card number.
    """
    number: int

    def is_rule_satisfied(self, game_data: GameData) -> bool:
        all_cards_of_number = CardsOperation.get_cards_by_number(self.number)
        all_cards_played = game_data.get_all_cards_played()
        all_number_cards_played =  all_cards_of_number.issubset(all_cards_played)
        if not game_data.is_finished() and not all_number_cards_played:
            return False
        winning_card_numbers = {
            card.number for _, card in (round_data.get_winner() for round_data in game_data.rounds)
        }
        return self.number not in winning_card_numbers

    def is_rule_broken(self, game_data: GameData) -> bool:
        last_round = game_data.get_last_round()
        _, winning_card = last_round.get_winner()
        return winning_card.number == self.number

@dataclass(frozen=True)
class WinOnceWithNumberRule(MissionRule):
    """
    Rule that specifies a player must win at least once with a specific card number.
    """
    number: int

    def is_rule_satisfied(self, game_data: GameData) -> bool:
        last_round = game_data.get_last_round()
        _, winning_card = last_round.get_winner()
        return winning_card.number == self.number

    def is_rule_broken(self, game_data: GameData) -> bool:
        if not game_data.is_finished():
            return False
        winning_card_numbers = {
            card.number for _, card in (round_data.get_winner() for round_data in game_data.rounds)
        }
        return self.number not in winning_card_numbers

@dataclass(frozen=True)
class WinWithAllTheseCardsRule(MissionRule):
    """
    Rule that specifies a player must win with all of the given cards.
    """
    cards_that_need_to_win: set[Card]

    def is_rule_satisfied(self, game_data: GameData) -> bool:
        return self.__won_with_all_cards__(game_data)

    def is_rule_broken(self, game_data: GameData) -> bool:
        if not game_data.is_finished():
            return False
        return not self.__won_with_all_cards__(game_data)

    def __won_with_all_cards__(self, game_data: GameData) -> bool:
        winning_cards = {
            card for _, card in (round_data.get_winner() for round_data in game_data.rounds)
        }
        return self.cards_that_need_to_win.issubset(winning_cards)

@dataclass(frozen=True)
class PlayerShouldNeverWinRule(MissionRule):
    """
    Rule that specifies a player should never win.
    """
    player_that_should_never_win: Player

    def is_rule_satisfied(self, game_data: GameData) -> bool:
        return game_data.is_finished() and not self.__did_player_win__(game_data)

    def is_rule_broken(self, game_data: GameData) -> bool:
        return self.__did_player_win__(game_data)

    def __did_player_win__(self, game_data: GameData) -> bool:
        all_winners = {
            winner for winner, _ in (round_data.get_winner() for round_data in game_data.rounds)
        }
        return self.player_that_should_never_win in all_winners
