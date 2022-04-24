"""
Counting cards strategy logic goes here
Create a separate function for this strategy if you feel the need
"""

from constants import NUM_DECKS
from strategies.basic import soft_totals_strategy, hard_totals_strategy


def take_action(player_hand, dealer_up_card):
    player_total = player_hand.get_hand_total()

    if player_hand.is_soft_total():
        action = soft_totals_strategy(player_total, dealer_up_card)
    else:
        action = hard_totals_strategy(player_total, dealer_up_card)

    return action


def get_bet_value(running_count, cards_left):
    num_decks_left = cards_left / 52
    true_count = int(running_count / num_decks_left)
    bet_value = 1
    if true_count <= 1:
        return bet_value
    elif true_count < 4:
        return bet_value * 1.5
    else:
        return bet_value * 3

