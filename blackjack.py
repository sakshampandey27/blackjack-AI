"""
Blackjack documentation
"""

from constants import NUM_SIMULATIONS
from card_deck import Card, Deck

'''
Hand class refers to a hand for a participant of the game
'''
class Hand:

    def __init__(self):
        self.hand_cards = []
        self.total = []
        # self.soft_total = 0

    # Method to get hand total
    def get_hand_total(self):
        total = 0
        for card in self.hand_cards:
            total += card.num_value
        self.total = total
        return self.total

'''
Defining a sample strategy for reference
'''
def sample_strategy():
    player_hand = Hand()
    dealer_hand = Hand()
    deck = Deck()

    for i in range(3):
        player_hand.hand_cards.append(deck.deal())

    for i in range(3):
        dealer_hand.hand_cards.append(deck.deal())

    player_total = player_hand.get_hand_total()
    dealer_total = dealer_hand.get_hand_total()

    if player_total > dealer_total:
        return True
    return False


'''
Running simulations 
'''
def play():
    player_wins = 0

    for sim in range(NUM_SIMULATIONS):
        # print("Simulation #{0}".format(sim))
        if sample_strategy():
            player_wins += 1

    win_sample_strategy = (player_wins / NUM_SIMULATIONS) * 100
    print("Win percentage for player with sample strategy = {0:.2f}%".format(win_sample_strategy))


if __name__ == '__main__':
    play()
