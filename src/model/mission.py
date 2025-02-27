from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.model.player_hand import Player
from src.model.card import Card
from src.model.game_data import GameData

class MissionRule(ABC):
    @abstractmethod
    def is_rule_satisfied(self, game_data: GameData) -> bool:
        pass # pragma: no cover

    @abstractmethod
    def is_rule_broken(self, game_data: GameData) -> bool:
        pass # pragma: no cover

@dataclass(frozen=True)
class PlayerHasToWinCardRule(MissionRule):
    player: Player
    card: Card

    def is_rule_satisfied(self, game_data: GameData) -> bool:
        round = game_data.get_last_round()
        if self.card not in round.get_played_cards():
            return False
        winner, _ = round.get_winner()
        return winner == self.player
        
    def is_rule_broken(self, game_data: GameData) -> bool:
        round = game_data.get_last_round()
        if self.card not in round.get_played_cards():
            return False
        winner, _ = round.get_winner()
        return winner != self.player


@dataclass(frozen=True)
class NeverWinWithNumberRule(MissionRule):
    number: int

    def is_rule_satisfied(self, game_data: GameData) -> bool:
        if not game_data.is_finished():
            return False
        winning_card_numbers = {card.number for _, card in (round_data.get_winner() for round_data in game_data.rounds)}
        return self.number not in winning_card_numbers
        
    def is_rule_broken(self, game_data: GameData) -> bool:
        round = game_data.get_last_round()
        _, winning_card = round.get_winner()
        return winning_card.number == self.number

@dataclass(frozen=True)
class WinOnceWithNumberRule(MissionRule):
    number: int

    def is_rule_satisfied(self, game_data: GameData) -> bool:
        round = game_data.get_last_round()
        _, winning_card = round.get_winner()
        return winning_card.number == self.number
        
    def is_rule_broken(self, game_data: GameData) -> bool:
        if not game_data.is_finished():
            return False
        winning_card_numbers = {card.number for _, card in (round_data.get_winner() for round_data in game_data.rounds)}
        return self.number not in winning_card_numbers

@dataclass(frozen=True)
class WinWithAllTheseCardsRule(MissionRule):
    cards_that_need_to_win: set[Card]

    def is_rule_satisfied(self, game_data: GameData) -> bool:
        return self.__won_with_all_cards__(game_data)
        
    def is_rule_broken(self, game_data: GameData) -> bool:
        if not game_data.is_finished():
            return False
        return not self.__won_with_all_cards__(game_data)
    
    def __won_with_all_cards__(self, game_data: GameData) -> bool:
        winning_cards = {card for _, card in (round_data.get_winner() for round_data in game_data.rounds)}
        return self.cards_that_need_to_win.issubset(winning_cards)
    

@dataclass(frozen=True)
class PlayerShouldNeverWinRule(MissionRule):
    player_that_should_never_win: Player

    def is_rule_satisfied(self, game_data: GameData) -> bool:
        return game_data.is_finished() and not self.__did_player_win__(game_data)
        
    def is_rule_broken(self, game_data: GameData) -> bool:
        return self.__did_player_win__(game_data)
    
    def __did_player_win__(self, game_data: GameData) -> bool:
        all_winners = {winner for winner, _ in (round_data.get_winner() for round_data in game_data.rounds)}
        return self.player_that_should_never_win in all_winners