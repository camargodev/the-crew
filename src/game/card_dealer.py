import random
from src.model.card import Card, CardType

class CardDealer:
    def __init__(self):
        self.deck = self.__create_deck__()  # Deck remains unchanged

    def deal_cards(self, players):
        """Deals cards to players in a round-robin fashion without modifying self.deck.
        Returns the players and the player who is the captain.
        """
        shuffled_deck = self.deck[:]  # Create a copy of the deck
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


    
    def __create_deck__(self):
        """Creates a full deck of cards based on the rules."""
        deck = []
        
        # Add BLUE, YELLOW, PINK, GREEN (1-9)
        for card_type in [CardType.BLUE, CardType.YELLOW, CardType.PINK, CardType.GREEN]:
            for number in range(1, 10):
                deck.append(Card(card_type, number))
        
        # Add ROCKET (1-4)
        for number in range(1, 5):
            deck.append(Card(CardType.ROCKET, number))
        
        return deck
