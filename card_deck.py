"""
Classes related to playing cards have been defined here
"""

import random
from utils.card_functions import get_card_num_value

'''
Card class holds the properties of a single playing card
'''


class Card:

    def __init__(self, suit=None, value=None):
        self.suit = suit
        self.value = value
        self.num_value = get_card_num_value(value)

    def set(self, suit, value):
        self.suit = suit
        self.value = value
        self.num_value = get_card_num_value(value)

    def get(self):
        return self.suit, self.value


'''
Deck class holds the properties of a standard deck of cards
'''


class Deck:

    def __init__(self):
        self.cards = []
        self.open_cards = []
        self.suits = ["C", "S", "D", "H"]
        self.values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.shuffle()

    # Method to shuffle the deck
    def shuffle(self):
        self.cards = []
        self.open_cards = []
        for suit in self.suits:
            for fvalue in self.values:
                self.cards.append(Card(suit, fvalue))

        random.shuffle(self.cards)

    # Method for total number of cards in deck
    def total_cards(self):
        return len(self.cards)

    # TODO: Why do we need this?
    # Method for the open cards
    def negation(self):
        final = []
        # pad the final list
        for i in range(52):
            final.append(0)
        # now fill in the proper order
        for card in self.open_cards:
            value = int(card.split('-')[0])
            # find the right place in the list
            # the first index for any value is 4 * (value-1)
            index = 4 * (value - 1)

            # is this the first, second, third or fourth instance of this card?
            if final[index] is 0:
                final[index] = 1
            elif final[index + 1] is 0:
                final[index + 1] = 1
            elif final[index + 2] is 0:
                final[index + 2] = 1
            else:
                final[index + 3] = 1
        return final

    # Method to deal a card from the deck
    def deal(self):
        card = random.choice(self.cards)
        self.cards.remove(card)
        self.open_cards.append(card)
        return card
