"""
Basic strategy logic goes here (refer to chart)
Create a separate function for this strategy if you feel the need
"""


def hard_totals_strategy(total, dealer_up_card):
    dealer_up_card_val = dealer_up_card.get_value()

    if total < 12:
        action = "hit"
    elif total == 12:
        if dealer_up_card_val in [4, 5, 6]:
            action = "stand"
        else:
            action = "hit"
    elif total < 17:
        if dealer_up_card_val in [7, 8, 9, 10] or dealer_up_card.get_face() == 'A':
            action = "stand"
        else:
            action = "hit"
    else:
        action = "stand"

    return action


def soft_totals_strategy(total, dealer_up_card):
    dealer_up_card_val = dealer_up_card.get_value()

    if total <= 17:
        action = "hit"
    elif total == 18:
        if dealer_up_card_val in [9,10] or dealer_up_card.get_face() == 'A':
            action = "hit"
        else:
            action = "stand"
    else:
        action = "stand"

    return action


def deviations(player_hand, dealer_up_card, true_count):
    pass


def take_action(player_hand, dealer_up_card):
    player_total = player_hand.get_hand_total()

    if player_hand.is_soft_total():
        action = soft_totals_strategy(player_total, dealer_up_card)
    else:
        action = hard_totals_strategy(player_total, dealer_up_card)

    return action

