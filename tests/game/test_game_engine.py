import pytest
import punq
from src.model.card import *
from src.game.interface.player_interface import PlayerInterface
from src.game.round_engine import RoundEngine
from src.game.game_engine import GameEngine
from src.game.card_dealer import CardDealer
from src.model.game_missions_data import GameMissionsData
from src.model.game_data import GameData
from src.model.round_data import RoundData
from src.model.player_hand import Player
from src.game.mission_engine import MissionRule, PlayerHasToWinCardRule
from src.model.card import Card
from tests.helpers.test_data_creation_helper import create_player
from typing import Dict, List, Tuple

pytest_plugins = ["pytest_mock"]

# Typing for the container fixture
@pytest.fixture
def container(mocker) -> punq.Container:
    container = punq.Container()
    mock_interface = mocker.MagicMock()
    mock_round_engine = mocker.MagicMock()
    mock_card_dealer = mocker.MagicMock()
    container.register(PlayerInterface, instance=mock_interface)
    container.register(RoundEngine, instance=mock_round_engine)
    container.register(CardDealer, instance=mock_card_dealer)
    container.register(GameEngine)
    return container

def test_play_game_should_return_result_as_soon_as_all_missions_are_complete(container: punq.Container):
    engine: GameEngine = container.resolve(GameEngine)
    round_engine: RoundEngine = container.resolve(RoundEngine)
    card_dealer: CardDealer = container.resolve(CardDealer)

    players = given_players_are_dealt_cards(
        card_dealer,
        captain_name="player_1",
        cards_dealt_by_player={
            "player_1": [YELLOW_2, GREEN_5, PINK_1, BLUE_1, ROCKET_4,
                         PINK_4, GREEN_4, YELLOW_9, BLUE_4, PINK_9],
            "player_2": [BLUE_7, YELLOW_4, ROCKET_1, GREEN_3, PINK_8,
                         GREEN_2, PINK_6, YELLOW_5, BLUE_3, GREEN_8],
            "player_3": [GREEN_9, BLUE_2, BLUE_5, YELLOW_1, ROCKET_3,
                         GREEN_6, PINK_3, YELLOW_6, BLUE_6, YELLOW_7],
            "player_4": [ROCKET_2, GREEN_7, YELLOW_3, BLUE_8, PINK_2,
                         YELLOW_8, PINK_5, PINK_7, GREEN_1, BLUE_9],
        }
    )

    player_1, player_2, player_3, player_4 = players

    given_played_round(
        round_engine,
        rounds_data = [make_round_data({
            player_1: YELLOW_9,
            player_2: YELLOW_4,
            player_3: YELLOW_6,
            player_4: YELLOW_3
        })]
    )

    mission = PlayerHasToWinCardRule(player_1, YELLOW_9)

    game_data, missions_data = engine.play_game(players, [mission])

    assert len(game_data.rounds) == 1
    assert game_data.number_of_rounds == 10
    assert missions_data.all_missions == {mission}
    assert missions_data.sucessfull_missions == {mission}
    assert missions_data.missing_missions == set()
    assert missions_data.failed_missions == set()
    assert missions_data.are_missions_complete() is True
    assert missions_data.has_any_failed_mission() is False

def test_play_game_should_return_result_as_soon_as_any_mission_fail(container: punq.Container):
    engine: GameEngine = container.resolve(GameEngine)
    round_engine: RoundEngine = container.resolve(RoundEngine)
    card_dealer: CardDealer = container.resolve(CardDealer)

    players = given_players_are_dealt_cards(
        card_dealer,
        captain_name="player_1",
        cards_dealt_by_player={
            "player_1": [YELLOW_2, GREEN_5, PINK_1, BLUE_1, ROCKET_4,
                         PINK_4, GREEN_4, YELLOW_9, BLUE_4, PINK_9],
            "player_2": [BLUE_7, YELLOW_4, ROCKET_1, GREEN_3, PINK_8,
                         GREEN_2, PINK_6, YELLOW_5, BLUE_3, GREEN_8],
            "player_3": [GREEN_9, BLUE_2, BLUE_5, YELLOW_1, ROCKET_3,
                         GREEN_6, PINK_3, YELLOW_6, BLUE_6, YELLOW_7],
            "player_4": [ROCKET_2, GREEN_7, YELLOW_3, BLUE_8, PINK_2,
                         YELLOW_8, PINK_5, PINK_7, GREEN_1, BLUE_9],
        }
    )

    player_1, player_2, player_3, player_4 = players

    given_played_round(
        round_engine,
        rounds_data = [make_round_data({
            player_1: YELLOW_9,
            player_2: YELLOW_4,
            player_3: YELLOW_6,
            player_4: YELLOW_3
        })]
    )

    mission = PlayerHasToWinCardRule(player_3, YELLOW_9)

    game_data, missions_data = engine.play_game(players, [mission])

    assert len(game_data.rounds) == 1
    assert game_data.number_of_rounds == 10
    assert missions_data.all_missions == {mission}
    assert missions_data.sucessfull_missions == set()
    assert missions_data.missing_missions == set()
    assert missions_data.failed_missions == {mission}
    assert missions_data.are_missions_complete() is False
    assert missions_data.has_any_failed_mission() is True

def test_play_game_should_play_all_rounds_but_without_completing_mission(container: punq.Container):
    engine: GameEngine = container.resolve(GameEngine)
    round_engine: RoundEngine = container.resolve(RoundEngine)
    card_dealer: CardDealer = container.resolve(CardDealer)

    # Setup players and cards dealt
    players = given_players_are_dealt_cards(
        card_dealer,
        captain_name="player_1",
        cards_dealt_by_player={
            "player_1": [YELLOW_2, GREEN_5, PINK_1, BLUE_1, ROCKET_4,
                         PINK_4, GREEN_4, YELLOW_9, BLUE_4, PINK_9],
            "player_2": [BLUE_7, YELLOW_4, ROCKET_1, GREEN_3, PINK_8,
                         GREEN_2, PINK_6, YELLOW_5, BLUE_3, GREEN_8],
            "player_3": [GREEN_9, BLUE_2, BLUE_5, YELLOW_1, ROCKET_3,
                         GREEN_6, PINK_3, YELLOW_6, BLUE_6, YELLOW_7],
            "player_4": [ROCKET_2, GREEN_7, YELLOW_3, BLUE_8, PINK_2,
                         YELLOW_8, PINK_5, PINK_7, GREEN_1, BLUE_9],
        }
    )

    player_1, player_2, player_3, player_4 = players

    # Generate 10 rounds with different cards for each player
    rounds_data = [
        make_round_data({
            player_1: YELLOW_2,
            player_2: BLUE_7,
            player_3: GREEN_9,
            player_4: ROCKET_2
        }),
        make_round_data({
            player_1: GREEN_5,
            player_2: YELLOW_4,
            player_3: BLUE_2,
            player_4: GREEN_7
        }),
        make_round_data({
            player_1: PINK_1,
            player_2: ROCKET_1,
            player_3: BLUE_5,
            player_4: YELLOW_3
        }),
        make_round_data({
            player_1: BLUE_1,
            player_2: GREEN_3,
            player_3: YELLOW_1,
            player_4: BLUE_8
        }),
        make_round_data({
            player_1: ROCKET_4,
            player_2: PINK_8,
            player_3: ROCKET_3,
            player_4: PINK_2
        }),
        make_round_data({
            player_1: PINK_9,
            player_2: GREEN_2,
            player_3: GREEN_6,
            player_4: YELLOW_8
        }),
        make_round_data({
            player_1: GREEN_4,
            player_2: PINK_6,
            player_3: PINK_3,
            player_4: BLUE_9
        }),
        make_round_data({
            player_1: YELLOW_9,
            player_2: YELLOW_5,
            player_3: YELLOW_6,
            player_4: YELLOW_7
        }),
        make_round_data({
            player_1: BLUE_4,
            player_2: BLUE_3,
            player_3: BLUE_6,
            player_4: YELLOW_6
        }),
        make_round_data({
            player_1: PINK_4,
            player_2: GREEN_8,
            player_3: YELLOW_9,
            player_4: PINK_5 
        })
    ]

    given_played_round(round_engine, rounds_data)

    # Player 1 loses this on the last round
    mission = PlayerHasToWinCardRule(player_1, PINK_4)

    game_data, missions_data = engine.play_game(players, [mission])

    # Assert that 10 rounds have been played
    assert len(game_data.rounds) == 10
    assert game_data.number_of_rounds == 10

    # Check mission status
    assert missions_data.all_missions == {mission}
    assert missions_data.sucessfull_missions == set()
    assert missions_data.missing_missions == set()
    assert missions_data.failed_missions == {mission}
    assert missions_data.are_missions_complete() is False
    assert missions_data.has_any_failed_mission() is True


def given_players_are_dealt_cards(
    card_dealer: CardDealer,
    captain_name: str,
    cards_dealt_by_player: Dict[str, List[Card]]
) -> List[Player]:
    players = []
    captain = None
    for player_name, cards in cards_dealt_by_player.items():
        player = create_player(player_name, cards)
        players.append(player)
        if player_name == captain_name:
            captain = player
    card_dealer.deal_cards.return_value = (players, captain)
    return players

def make_round_data(
    card_by_player: Dict[Player, Card]
) -> RoundData:
    round_data = RoundData(list(card_by_player.keys()))
    for player, card in card_by_player.items():
        round_data.add_played_card(player, card)
    return round_data

def given_played_round(
    round_engine: RoundEngine,
    rounds_data: List[RoundData]
):
    round_engine.play_round.side_effect = rounds_data
