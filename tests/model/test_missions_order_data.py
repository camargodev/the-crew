import pytest
from src.game.mission_rules import PlayerHasToWinCardRule
from src.model.missions_order_data import MissionsOrderData
from src.model.card import BLUE_2, BLUE_6, BLUE_8
from tests.helpers.test_data_creation_helper import create_player

@pytest.fixture
def sample_missions():
    return PlayerHasToWinCardRule(create_player("P1"), BLUE_2), PlayerHasToWinCardRule(create_player("P2"), BLUE_6), PlayerHasToWinCardRule(create_player("P3"), BLUE_8)


def test_order_constraint_respected(sample_missions):
    a, b, _ = sample_missions
    order_data = (
        MissionsOrderData.builder()
        .add_order_constraint(a, b)
        .build()
    )

    assert not order_data.is_order_respected([], b)
    assert order_data.is_order_respected([a], b)


def test_fixed_position_respected(sample_missions):
    a, b, _ = sample_missions
    order_data = (
        MissionsOrderData.builder()
        .set_fixed_position(b, 1)
        .build()
    )

    assert not order_data.is_order_respected([], b)  # position 0, should be 1
    assert order_data.is_order_respected([a], b)  # position 1 is ok


def test_both_constraints_respected(sample_missions):
    a, b, c = sample_missions
    order_data = (
        MissionsOrderData.builder()
        .add_order_constraint(a, b)
        .set_fixed_position(b, 2)
        .build()
    )

    satisfied = [a, c]
    assert order_data.is_order_respected(satisfied, b)  # a was done, position 2 ok


def test_both_constraints_violated(sample_missions):
    a, b, c = sample_missions
    order_data = (
        MissionsOrderData.builder()
        .add_order_constraint(a, b)
        .set_fixed_position(b, 2)
        .build()
    )

    assert not order_data.is_order_respected([], b)  # a not done and wrong position
    assert not order_data.is_order_respected([c], b)  # wrong position
    assert not order_data.is_order_respected([a], b)  # right dependency, wrong position
