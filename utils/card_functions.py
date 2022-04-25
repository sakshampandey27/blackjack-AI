from constants import CARD_FACE_VALUES


def get_card_num_value(value):
    if value is None:
        return None
    return CARD_FACE_VALUES[value]
