from constants import CARD_FACE_VALUES

# Get numeric value for a card
# Face cards are valued 10.
# Ace is valued 11 by default unless total exceeds 21.

def get_card_num_value(value):
    if value is None:
        return None
    return CARD_FACE_VALUES[value]
