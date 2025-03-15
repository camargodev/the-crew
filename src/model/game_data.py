from dataclasses import dataclass, field
from src.model.round_data import RoundData
from src.model.card import Card

@dataclass(frozen=True)
class GameData:
    """
    Represents the data for the game, including the number of rounds and the rounds themselves.

    Attributes:
        number_of_rounds (int): The total number of rounds in the game.
        rounds (list[RoundData]): A list of RoundData objects representing the rounds played.
    """
    number_of_rounds: int
    rounds: list[RoundData] = field(default_factory=list)


    def add_round(self, round_data: RoundData):
        """
        Adds a new round to the game.

        Args:
            round_data (RoundData): The round data to be added.
        """
        return self.rounds.append(round_data)

    def is_finished(self) -> bool:
        """
        Checks if the game is finished.

        Returns:
            bool: True if the game is finished (i.e., the number of 
              rounds played equals the total rounds), False otherwise.
        """
        return len(self.rounds) == self.number_of_rounds

    def get_last_round(self) -> RoundData:
        """
        Gets the last round played in the game.

        Raises:
            ValueError: If no rounds have been played yet.

        Returns:
            RoundData: The last round played.
        """
        if len(self.rounds) == 0:
            raise ValueError("No rounds played.")
        return self.rounds[-1]

    def get_all_cards_played(self) -> set[Card]:
        """
        Retrieves all cards played in the game.

        Returns:
            set[Card]: A set of all cards that have been played across all rounds.
        """
        return set().union(*(round_data.get_played_cards() for round_data in self.rounds))
