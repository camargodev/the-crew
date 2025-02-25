from src.model.player_hand import Player
from src.game.card_dealer import CardDealer

# Create players
players = [Player("Alice"), Player("Bob"), Player("Charlie")]

# Create a dealer and deal cards
dealer = CardDealer()
dealer.deal_cards(players)

# Print results
for player in players:
    print(player)