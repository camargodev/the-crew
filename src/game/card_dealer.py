import random
from src.model.player_hand import Player
from src.model.card import ALL_CARDS


class CardDealer:
    """
    Class responsible for dealing cards to players in a round-robin manner.
    It shuffles a copy of the deck and assigns cards to each player, then
    determines the captain of the round based on the presence of the 'ROCKET 4' card.
    """

    def deal_cards(self, players: list[Player]):
        """Deals cards to players in a round-robin fashion without modifying self.deck.
        Returns the players and the player who is the captain.
        """
        shuffled_deck = ALL_CARDS[:]  # Create a copy of the deck
        random.shuffle(shuffled_deck)  # Shuffle the copy

        player_count = len(players)
        index = 0

        while shuffled_deck:
            card = shuffled_deck.pop()  # Pick a random card from the shuffled copy
            players[index % player_count].deal_card(card)
            index += 1  # Move to the next player

        # Find the captain (the player with ROCKET 4)
        captain = next((player for player in players if player.is_captain()), None)

        return players, captain
