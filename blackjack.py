"""
Blackjack documentation
"""
import copy
import enum
import sys
import matplotlib.pyplot as plt
import random

from card_deck import Deck, Hand
from constants import NUM_SIMULATIONS, CARD_COUNT_VALUES, NUM_DECKS
from strategies import basic, simple, inexperienced, counting

PLAYER_MONEY = copy.deepcopy(NUM_SIMULATIONS)
RUNNING_COUNT = 0


class Strategy(enum.Enum):
    random = 1
    simple = 2
    basic = 3
    counting = 4


def play(deck, strategy):
    player_hand = Hand()
    dealer_hand = Hand()
    action = "stand"
    bet_value = 1

    global RUNNING_COUNT, PLAYER_MONEY

    for i in range(2):
        card = deck.deal()
        player_hand.hand_cards.append(card)
        RUNNING_COUNT += CARD_COUNT_VALUES[card.get_face()]

    for i in range(2):
        card = deck.deal()
        dealer_hand.hand_cards.append(card)
        RUNNING_COUNT += CARD_COUNT_VALUES[card.get_face()]

    dealer_up_card = dealer_hand.hand_cards[0]
    player_total = player_hand.get_hand_total()

    if strategy.value == 1:
        action = inexperienced.take_action()
    elif strategy.value == 2:
        action = simple.take_action(player_hand)
    elif strategy.value == 3:
        action = basic.take_action(player_hand, dealer_up_card)
    elif strategy.value == 4:
        action = counting.take_action(player_hand, dealer_up_card)
        if action == "hit":
            bet_value = counting.get_bet_value(RUNNING_COUNT, deck.total_cards())

    while action == "hit" and player_total < 21:
        card = deck.deal()
        player_hand.hand_cards.append(card)
        player_total = player_hand.get_hand_total()

        RUNNING_COUNT += CARD_COUNT_VALUES[card.get_face()]

        if strategy.value == 1:
            action = inexperienced.take_action()
        elif strategy.value == 2:
            action = simple.take_action(player_hand)
        elif strategy.value == 3:
            action = basic.take_action(player_hand, dealer_up_card)
        elif strategy.value == 4:
            action = counting.take_action(player_hand, dealer_up_card)
            if action == "hit":
                bet_value = counting.get_bet_value(RUNNING_COUNT, deck.total_cards())

    PLAYER_MONEY -= bet_value
    if player_total > 21:
        return "loss", -1*bet_value

    if player_total == 21 and len(player_hand.hand_cards) == 2:
        return "win", 2.5*bet_value

    dealer_total = dealer_hand.get_hand_total()
    while dealer_total < 17:
        card = deck.deal()
        dealer_hand.hand_cards.append(card)
        dealer_total = dealer_hand.get_hand_total()
        RUNNING_COUNT += CARD_COUNT_VALUES[card.get_face()]

    if dealer_total > 21:
        return "win", 2*bet_value

    if player_total > dealer_total:
        return "win", 2*bet_value

    return "loss", -1*bet_value


def simulate(strategy):
    player_wins = 0
    deck = Deck()
    global RUNNING_COUNT, PLAYER_MONEY

    for sim in range(NUM_SIMULATIONS):
        if deck.total_cards() <= NUM_DECKS * 13:
            deck = Deck(NUM_DECKS)

        result, return_amount = play(deck, strategy)
        if result == "win":
            player_wins += 1
            PLAYER_MONEY += return_amount

    win_rate = (player_wins / NUM_SIMULATIONS) * 100
    print("Win percentage for player with {0} strategy = {1:.2f}%".format(strategy.name, win_rate))
    print("Amount after {0} rounds = {1:.2f}".format(NUM_SIMULATIONS, PLAYER_MONEY))


def find_strategy(game_strategy):
    if game_strategy == "random":
        strategy = Strategy.random
    elif game_strategy == "simple":
        strategy = Strategy.simple
    elif game_strategy == "basic":
        strategy = Strategy.basic
    elif game_strategy == "counting":
        strategy = Strategy.counting
    else:
        strategy = None

    return strategy


def plot_chart():
    pass

if __name__ == '__main__':
    input_strategy = sys.argv[1]
    input_strategy = find_strategy(input_strategy)
    if input_strategy is None:
        print("Invalid strategy")
        exit(0)
    simulate(input_strategy)
