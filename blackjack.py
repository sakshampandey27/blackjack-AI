"""
Blackjack documentation
"""
import enum

from constants import NUM_SIMULATIONS
from card_deck import Card, Deck, Hand
from strategies import basic, inexperienced


class Strategy(enum.Enum):
    random = 1
    basic = 2
    counting = 3


def play(deck, strategy):
    player_hand = Hand()
    dealer_hand = Hand()
    action = "stand"

    for i in range(2):
        player_hand.hand_cards.append(deck.deal())
    for i in range(2):
        dealer_hand.hand_cards.append(deck.deal())

    # print(player_hand)
    # print(dealer_hand)

    dealer_up_card = dealer_hand.hand_cards[0]
    player_total = player_hand.get_hand_total()

    if strategy.value == 1:
        action = inexperienced.take_action()
    elif strategy.value == 2:
        action = basic.take_action(player_hand, dealer_up_card)

    while action == "hit" and player_total < 21:
        player_hand.hand_cards.append(deck.deal())
        # print(player_hand)
        player_total = player_hand.get_hand_total()
        if strategy.value == 1:
            action = inexperienced.take_action()
        elif strategy.value == 2:
            action = basic.take_action(player_hand, dealer_up_card)

    if player_total > 21:
        return False

    if player_total == 21:
        return True

    dealer_total = dealer_hand.get_hand_total()
    while dealer_total < 17:
        dealer_hand.hand_cards.append(deck.deal())
        # print(dealer_hand)
        dealer_total = dealer_hand.get_hand_total()

    if dealer_total > 21:
        return True

    if player_total > dealer_total:
        return True
    return False


def simulate():
    player_wins = 0
    deck = Deck()

    for sim in range(NUM_SIMULATIONS):
        if deck.total_cards() <= 13:
            deck = Deck()

        # if play(deck, Strategy.basic):
        #     player_wins += 1

        if play(deck, Strategy.random):
            player_wins += 1

    win_basic_strategy = (player_wins / NUM_SIMULATIONS) * 100
    print("Win percentage for player with basic strategy = {0:.2f}%".format(win_basic_strategy))


if __name__ == '__main__':
    simulate()
