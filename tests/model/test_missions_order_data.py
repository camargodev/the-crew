import pytest
from src.game.mission_rules import PlayerHasToWinCardRule
from src.model.missions_order_data import MissionsOrderData
from src.model.card import BLUE_2, BLUE_6, BLUE_8
from tests.helpers.test_data_creation_helper import create_player

@pytest.fixture
def sample_missions():
    return (
        PlayerHasToWinCardRule(create_player("P1"), BLUE_2),
        PlayerHasToWinCardRule(create_player("P2"), BLUE_6),
        PlayerHasToWinCardRule(create_player("P3"), BLUE_8)
    )

def test_without_constraints(sample_missions):
    first, second, _ = sample_missions
    order_data = MissionsOrderData.empty()

    assert order_data.is_order_respected([], first)
    assert order_data.is_order_respected([], second)
    assert order_data.is_order_respected([first], second)
    assert order_data.is_order_respected([second], first)

def test_fixed_position_respected(sample_missions):
    first, other, _ = sample_missions
    order_data = (
        MissionsOrderData.builder()
        .set_fixed_position(first, 1)
        .build()
    )

    assert order_data.is_order_respected([], first)  # true because mission is the first
    assert not order_data.is_order_respected([other], first)  # false, other mission was done first


def test_order_constraint_respected(sample_missions):
    first, second, _ = sample_missions
    order_data = (
        MissionsOrderData.builder()
        .add_order_constraint(first, second)
        .build()
    )

    assert not order_data.is_order_respected([], second)
    assert order_data.is_order_respected([first], second)

def test_with_unrelated_mission(sample_missions):
    first, second, unrelated = sample_missions
    order_data = (
        MissionsOrderData.builder()
        .add_order_constraint(first, second)
        .build()
    )

    assert order_data.is_order_respected([unrelated], first)
    assert order_data.is_order_respected([first], second)
    assert order_data.is_order_respected([first, unrelated], second)


def test_both_constraints_respected(sample_missions):
    first, second, third = sample_missions
    order_data = (
        MissionsOrderData.builder()
        .add_order_constraint(first, second)
        .set_fixed_position(third, 3)
        .build()
    )

    assert order_data.is_order_respected([], first)
    assert order_data.is_order_respected([first], second)
    assert order_data.is_order_respected([first, second], third)


def test_both_constraints_violated(sample_missions):
    first, second, third = sample_missions
    order_data = (
        MissionsOrderData.builder()
        .add_order_constraint(first, second)
        .set_fixed_position(third, 3)
        .build()
    )

    # 'first' was not done yet, should fail
    assert not order_data.is_order_respected([], second)
    # no dependency, but wrong position, should fail
    assert not order_data.is_order_respected([], third)
