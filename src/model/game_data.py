from dataclasses import dataclass, field
from src.model.round_data import RoundData
from src.model.card import Card

@dataclass(frozen=True)
class GameData:
    number_of_rounds: int
    rounds: list[RoundData] = field(default_factory=list)

    def add_round(self, round_data: RoundData):
        return self.rounds.append(round_data)

    def is_finished(self) -> bool:
        return len(self.rounds) == self.number_of_rounds
    
    def get_last_round(self) -> RoundData:
        if len(self.rounds) == 0:
            raise ValueError("No rounds played.")
        return self.rounds[-1]
    
    def get_all_cards_played(self) -> set[Card]:
        return set().union(*(round_data.get_played_cards() for round_data in self.rounds))
