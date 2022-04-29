"""
Blackjack documentation
"""
import copy
import enum
import sys
import time

import numpy as np

import stats

from card_deck import Deck, Hand
from constants import DEALER_UP_CARD_FEATURE, PLAYER_HAND_FEATURE, PLAYER_RESULT_FEATURE, \
    PLAYER_CURRENT_TOTAL, PLAYER_CURRENT_ACTION
from constants import NUM_SIMULATIONS, CARD_COUNT_VALUES, NUM_DECKS
from strategies import basic, simple, inexperienced, counting, learning

# To run tensorflow on GPU
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


PLAYER_MONEY = copy.deepcopy(NUM_SIMULATIONS)
RUNNING_COUNT = 0


# Strategy enum class
class Strategy(enum.Enum):
    random = 1
    simple = 2
    basic = 3
    counting = 4
    ml = 5


# Result enum class
class GameResult(enum.Enum):
    win = 1
    loss = -1
    tie = 0


# Determining strategy to be used
def find_strategy(game_strategy):
    if game_strategy == "random":
        strategy = Strategy.random
    elif game_strategy == "simple":
        strategy = Strategy.simple
    elif game_strategy == "basic":
        strategy = Strategy.basic
    elif game_strategy == "counting":
        strategy = Strategy.counting
    elif game_strategy == "ml":
        strategy = Strategy.ml
    else:
        strategy = None

    return strategy


def get_enum_value(result):
    if result == "win":
        game_result = GameResult.win
    elif result == "loss":
        game_result = GameResult.loss
    else:
        game_result = GameResult.tie

    return game_result.value


# Getting the desired action for a particular strategy
def action_strategy(strategy, player_hand, dealer_up_card, deck, ml_model=None):
    action = "stand"
    bet_value = 1
    global RUNNING_COUNT

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
    elif strategy.value == 5:
        player_total = player_hand.get_hand_total()
        dealer_card_val = dealer_up_card.get_value()
        player_hand_ace = player_hand.is_soft_total()
        action = learning.take_action(ml_model, player_total, dealer_card_val, player_hand_ace)

    return action, bet_value


# Initial steps of a game involve dealing 2 hands each to the player and the dealer
def initial_deal(deck):
    player_hand = Hand()
    dealer_hand = Hand()
    global RUNNING_COUNT

    for i in range(2):
        card = deck.deal()
        player_hand.hand_cards.append(card)
        RUNNING_COUNT += CARD_COUNT_VALUES[card.get_face()]

    for i in range(2):
        card = deck.deal()
        dealer_hand.hand_cards.append(card)
        RUNNING_COUNT += CARD_COUNT_VALUES[card.get_face()]

    return player_hand, dealer_hand


# Logic function to check if player or dealer have busted
def is_bust(total):
    if total > 21:
        return True
    return False


# Logic function to check if player has a blackjack
def is_blackjack(total, num_cards):
    if total == 21 and num_cards == 2:
        return True
    return False


# Logic function to check if player has a better total than the dealer
def player_wins(p_total, d_total):
    if p_total > d_total:
        return True
    return False


# Logic function to check if player has tied with the dealer
def game_tied(p_total, d_total):
    if p_total == d_total:
        return True
    return False


def play(deck, strategy, ml_model=None):
    global RUNNING_COUNT, PLAYER_MONEY
    curr_totals = []

    player_hand, dealer_hand = initial_deal(deck)
    dealer_up_card = dealer_hand.hand_cards[0]
    player_total = player_hand.get_hand_total()
    curr_totals.append(player_total)

    # Main logic goes here
    # Strategy decides an appropriate action based on certain parameters
    # Play continues until the player busts or chooses to stand
    action, bet_value = action_strategy(strategy, player_hand, dealer_up_card, deck, ml_model)
    while action == "hit" and player_total < 21:
        card = deck.deal()
        player_hand.hand_cards.append(card)
        player_total = player_hand.get_hand_total()
        curr_totals.append(player_total)
        RUNNING_COUNT += CARD_COUNT_VALUES[card.get_face()]
        action, bet_value = action_strategy(strategy, player_hand, dealer_up_card, deck, ml_model)

    PLAYER_MONEY -= bet_value

    # Play continues until the dealer's total goes past 17. Dealer doesn't choose to stand
    dealer_total = dealer_hand.get_hand_total()
    while dealer_total < 17:
        card = deck.deal()
        dealer_hand.hand_cards.append(card)
        dealer_total = dealer_hand.get_hand_total()
        RUNNING_COUNT += CARD_COUNT_VALUES[card.get_face()]

    DEALER_UP_CARD_FEATURE.append(dealer_up_card.get_value())
    PLAYER_HAND_FEATURE.append(player_hand)

    # Determining the winner of a round
    if is_bust(player_total):
        result = "loss"
        return_amount = -1 * bet_value
    elif is_blackjack(player_total, len(player_hand.hand_cards)):
        result = "win"
        return_amount = 2.5 * bet_value
    elif is_bust(dealer_total):
        result = "win"
        return_amount = 2 * bet_value
    elif player_wins(player_total, dealer_total):
        result = "win"
        return_amount = 2 * bet_value
    elif game_tied(player_total, dealer_total):
        result = "tie"
        return_amount = bet_value
    else:
        result = "loss"
        return_amount = -1 * bet_value

    curr_result = np.array([get_enum_value(result)])
    PLAYER_RESULT_FEATURE.append(curr_result)
    PLAYER_CURRENT_TOTAL.append(curr_totals)
    if action == "hit":
        action_tag = 1
    else:
        action_tag = 0
    PLAYER_CURRENT_ACTION.append(action_tag)
    return result, return_amount


# Function to simulate the game `NUM_SIMULATIONS` times
def simulate(strategy):
    wins = 0
    deck = Deck()
    plot_wins = []
    win_rate = 0
    ml_model = None

    global RUNNING_COUNT, PLAYER_MONEY

    # In case desired strategy is learning strategy, we first run the basic strategy to generate training data
    if strategy.name == "ml":
        for sim in range(NUM_SIMULATIONS):
            if deck.total_cards() <= NUM_DECKS * 13:
                deck = Deck(NUM_DECKS)
            result, return_amount = play(deck, strategy.basic)

        # Generate a model and train that model using the training data from basic strategy
        ml_model_df = stats.generate_model()
        ml_model = learning.neural_net(ml_model_df)

    # Run simulations for the strategy
    PLAYER_MONEY = copy.deepcopy(NUM_SIMULATIONS)
    for sim in range(NUM_SIMULATIONS):
        if deck.total_cards() <= NUM_DECKS * 13:
            deck = Deck(NUM_DECKS)

        result, return_amount = play(deck, strategy, ml_model)

        # Calculate win rate
        if result == "win":
            wins += 1
            PLAYER_MONEY += return_amount

        win_rate = (wins / (sim + 1)) * 100
        plot_wins.append(win_rate)

    print("Win percentage for player with {0} strategy = {1:.2f}%".format(strategy.name, win_rate))
    print("Amount after {0} rounds = {1:.2f}".format(NUM_SIMULATIONS, PLAYER_MONEY))

    stats.generate_stats(strategy.name)
    stats.plot_chart(plot_wins, os.path.join("stats", strategy.name))


if __name__ == '__main__':
    # start_time = time.time()
    input_strategy = sys.argv[1]

    input_strategy = find_strategy(input_strategy)
    if input_strategy is None:
        print("Invalid strategy")
        exit(0)
    simulate(input_strategy)
    # end_time = time.time()
    # print("{0:.2f}".format(end_time - start_time))
