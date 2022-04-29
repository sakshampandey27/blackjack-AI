"""
Simple strategy functionality
"""

# Decides action - hit or stand
def take_action(player_hand):
    player_total = player_hand.get_hand_total()

    if player_total < 17:
        action = "hit"
    else:
        action = "stand"
    return action
