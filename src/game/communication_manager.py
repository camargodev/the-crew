from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Set, List
from src.model.player_hand import Player
from src.game.interface.player_interface import PlayerInterface

from src.model.level_definition import LevelDefinition, CommunicationType

class CommunicationResult(Enum):
    ENABLED = auto()
    DISABLED = auto()
    LIMITED = auto()

class CommunicationManager(ABC):
    @abstractmethod
    def can_communicate(self, player: Player, round_number: int) -> CommunicationResult:
        """
        Returns whether the given player can communicate in the current round.

        Args:
            player (Player): The player to check.
            round_number (int): The current round number (1-based).

        Returns:
            CommunicationResult: ENABLED, DISABLED or LIMITED.
        """
        pass


class EnabledCommunicationManager(CommunicationManager):
    def can_communicate(self, player: Player, round_number: int) -> CommunicationResult:
        return CommunicationResult.ENABLED


class LimitedCommunicationManager(CommunicationManager):
    def can_communicate(self, player: Player, round_number: int) -> CommunicationResult:
        return CommunicationResult.LIMITED


class BlockedForNumberOfPlayerManager(CommunicationManager):
    def __init__(self, blocked_player_ids: Set[int]):
        self.blocked_player_ids = blocked_player_ids

    def can_communicate(self, player: Player, round_number: int) -> CommunicationResult:
        if player.id in self.blocked_player_ids:
            return CommunicationResult.DISABLED
        return CommunicationResult.ENABLED


class BlockedUntilRoundManager(CommunicationManager):
    def __init__(self, starting_round: int):
        self.starting_round = starting_round

    def can_communicate(self, player: Player, round_number: int) -> CommunicationResult:
        if round_number < self.starting_round:
            return CommunicationResult.DISABLED
        return CommunicationResult.ENABLED
    
class CommunicationManagerFactory:
    def __init__(self, player_interface: PlayerInterface):
        self.player_interface = player_interface

    def create(self, players: List[Player], level_definition: LevelDefinition) -> CommunicationManager:
        comm_type = level_definition.communication_type
        metadata = level_definition.communication_metadata

        if comm_type == CommunicationType.REGULAR:
            return EnabledCommunicationManager()

        elif comm_type == CommunicationType.DEAD_ZONE:
            return LimitedCommunicationManager()

        elif comm_type == CommunicationType.BLOCKED_FOR_NUMBER_OF_PLAYER:
            count = metadata["number_of_player"]
            blocked_players = self.player_interface.select_blocked_players(players, count)
            blocked_ids = {player.id for player in blocked_players}
            return BlockedForNumberOfPlayerManager(blocked_ids)

        elif comm_type == CommunicationType.BLOCKED_UNTIL_ROUND:
            round_num = metadata["starting_round"]
            return BlockedUntilRoundManager(round_num)

        raise ValueError(f"Unsupported CommunicationType: {comm_type}")