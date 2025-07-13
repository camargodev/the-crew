import pytest
from typing import List
from unittest.mock import Mock

from src.game.communication_manager import (
    CommunicationResult,
    EnabledCommunicationManager,
    LimitedCommunicationManager,
    BlockedForNumberOfPlayerManager,
    BlockedUntilRoundManager,
    CommunicationManagerFactory
)

from src.model.level_definition import LevelDefinition, CommunicationType
from src.model.player_hand import Player
from src.game.interface.player_interface import PlayerInterface
from tests.helpers.test_data_creation_helper import create_player


def test_enabled_communication_manager_allows_all():
    manager = EnabledCommunicationManager()
    assert manager.can_communicate([], 1) == CommunicationResult.ENABLED


def test_limited_communication_manager_returns_limited():
    manager = LimitedCommunicationManager()
    assert manager.can_communicate([], 2) == CommunicationResult.LIMITED


def test_blocked_for_number_of_player_blocks_correct_ids():
    player_1, player_2, player_3 = create_player("1"), create_player("2"), create_player("3")
    manager = BlockedForNumberOfPlayerManager(blocked_player_ids={player_1.id, player_3.id})
    round_number = 1 # Rouund does not matter here
    assert manager.can_communicate(player_1, round_number) == CommunicationResult.DISABLED
    assert manager.can_communicate(player_2, round_number) == CommunicationResult.ENABLED
    assert manager.can_communicate(player_3, round_number) == CommunicationResult.DISABLED


def test_blocked_until_round_blocks_before_threshold():
    manager = BlockedUntilRoundManager(starting_round=3)
    player = create_player("1")
    assert manager.can_communicate(player, 1) == CommunicationResult.DISABLED
    assert manager.can_communicate(player, 3) == CommunicationResult.ENABLED
    assert manager.can_communicate(player, 4) == CommunicationResult.ENABLED

def test_factory_enabled():
    level_def = make_level_definition(CommunicationType.REGULAR, {})
    player_interface = Mock(spec=PlayerInterface)
    factory = CommunicationManagerFactory(player_interface)

    manager = factory.create([create_player("1")], level_def)
    assert isinstance(manager, EnabledCommunicationManager)


def test_factory_limited():
    level_def = make_level_definition(CommunicationType.DEAD_ZONE, {})
    player_interface = Mock(spec=PlayerInterface)
    factory = CommunicationManagerFactory(player_interface)

    manager = factory.create([create_player("1")], level_def)
    assert isinstance(manager, LimitedCommunicationManager)


def test_factory_blocked_for_number_of_players():
    player_1, player_2, player_3 = create_player("1"), create_player("2"), create_player("3")
    level_def = make_level_definition(
        CommunicationType.BLOCKED_FOR_NUMBER_OF_PLAYER,
        { "number_of_player": 2}
    )

    player_interface = Mock(spec=PlayerInterface)
    player_interface.select_blocked_players.return_value = [player_1, player_2]

    factory = CommunicationManagerFactory(player_interface)
    manager = factory.create([player_1, player_2, player_3], level_def)

    assert isinstance(manager, BlockedForNumberOfPlayerManager)
    round_number = 1 # Rouund does not matter here
    assert manager.can_communicate(player_1, round_number) == CommunicationResult.DISABLED
    assert manager.can_communicate(player_2, round_number) == CommunicationResult.DISABLED
    assert manager.can_communicate(player_3, round_number) == CommunicationResult.ENABLED


def test_factory_blocked_until_round():
    player_1 = create_player("1")
    level_def = make_level_definition(
        CommunicationType.BLOCKED_UNTIL_ROUND,
        { "starting_round": 3}
    )

    player_interface = Mock(spec=PlayerInterface)
    factory = CommunicationManagerFactory(player_interface)

    manager = factory.create(player_1, level_def)
    assert isinstance(manager, BlockedUntilRoundManager)
    assert manager.can_communicate(player_1, round_number=1) == CommunicationResult.DISABLED
    assert manager.can_communicate(player_1, round_number=2) == CommunicationResult.DISABLED
    assert manager.can_communicate(player_1, round_number=3) == CommunicationResult.ENABLED

def make_level_definition(comm_type: CommunicationType, metadata: dict) -> LevelDefinition:
    return LevelDefinition(
        order_tokens=[],
        mission_types=[],
        communication_type=comm_type,
        communication_metadata=metadata
    )
