from src.model.player_hand import Player
from src.game.mission_rules import MissionRule
from src.game.round_engine import RoundEngine
from src.game.card_dealer import CardDealer
from src.model.card import ALL_CARDS
from src.model.game_data import GameData
from src.model.game_missions_data import GameMissionsData
from src.model.missions_order_data import  MissionsOrderData

class GameEngine:
    """
    Represents the data for mission on the game

    Attributes:
        round_engine (RoundEngine): manages rounds
        card_dealer (CardDealer): deals cards to players
    """

    def __init__(
            self,
            round_engine: RoundEngine,
            card_dealer: CardDealer):
        self.round_engine = round_engine
        self.card_dealer = card_dealer

    def play_game(
            self,
            players: list[Player],
            missions: list[MissionRule],
            mission_order_data: MissionsOrderData
        ):
        """
        Play a game, with all its rounds

        Args:
            players (list[Player]): players on the game
            missions (list[MissionRule]): the missions that need to be completed
            mission_order_data (MissionsOrderData): the missions order data

        Returns:
            game_data, missions_data
        """
        players, captain = self.card_dealer.deal_cards(players)
        number_of_rounds = self.__define_number_of_rounds__(players)

        game_data = GameData(number_of_rounds)
        missions_data = GameMissionsData.make(set(missions))

        starter_player = captain

        for _ in range(number_of_rounds):
            round_data = self.round_engine.play_round(players, starter_player)
            game_data.add_round(round_data)

            missions_data, is_game_over = self.__validate_missions__(
                missions_data,
                game_data,
                mission_order_data
            )
            if is_game_over:
                break

        return game_data, missions_data

    def __validate_missions__(
            self,
            missions_data: GameMissionsData,
            game_data: GameData,
            mission_order_data: MissionsOrderData
        ):
        # Check if any mission rule was broken before checking ordering
        for mission_rule in missions_data.missing_missions:
            if mission_rule.is_rule_broken(game_data):
                missions_data.add_failed_mission(mission_rule)
                return missions_data, True

        # First, check all successul missions on this round
        # This is to cover the scenario where two ordered missions
        #   are completed at once (which is okay)
        previously_successful_missions = missions_data.successful_missions
        succesful_missions_on_this_round = set()
        for mission_rule in missions_data.missing_missions:
            if mission_rule.is_rule_satisfied(game_data):
                succesful_missions_on_this_round.add(mission_rule)

        # For every successful mission, check if they dependencies
        #   were already satisfied (including current round)
        all_sucessful_missions = previously_successful_missions|succesful_missions_on_this_round
        for mission_rule in succesful_missions_on_this_round:
            if mission_order_data.is_order_respected(all_sucessful_missions, mission_rule):
                missions_data.add_sucessfull_mission(mission_rule)
            else:
                missions_data.add_failed_mission(mission_rule)

            if missions_data.are_missions_complete() or missions_data.has_any_failed_mission():
                return missions_data, True

        return missions_data, False


    def __define_number_of_rounds__(self, players: list[Player]) -> int:
        number_of_players = len(players)
        number_of_cards = len(ALL_CARDS)
        return int(number_of_cards//number_of_players)
