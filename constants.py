"""
Global constants defined here
Do not define constants specific to a strategy here
"""

CARD_FACE_VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}

CARD_COUNT_VALUES = {
    "2": 1,
    "3": 1,
    "4": 1,
    "5": 1,
    "6": 1,
    "7": 0,
    "8": 0,
    "9": 0,
    "10": -1,
    "J": -1,
    "Q": -1,
    "K": -1,
    "A": -1
}

NUM_SIMULATIONS = 500
NUM_DECKS = 6
DEALER_UP_CARD_FEATURE = []
PLAYER_HAND_FEATURE = []
PLAYER_ACE_FEATURE = []
PLAYER_RESULT_FEATURE = []
PLAYER_CURRENT_TOTAL = []
PLAYER_CURRENT_ACTION = []
