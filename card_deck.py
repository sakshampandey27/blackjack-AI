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

    def get_value(self):
        return self.num_value

    def get_face(self):
        return self.value


'''
Deck class holds the properties of a standard deck of cards
'''


class Deck:

    def __init__(self, num_decks=1):
        self.cards = []
        self.open_cards = []
        self.suits = ["C", "S", "D", "H"]
        self.values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.shuffle(num_decks)

    # Method to shuffle the deck
    def shuffle(self, num_decks):
        self.cards = []
        self.open_cards = []
        for _ in range(num_decks):
            for suit in self.suits:
                for fvalue in self.values:
                    self.cards.append(Card(suit, fvalue))

        random.shuffle(self.cards)

    # Method for total number of cards in deck
    def total_cards(self):
        return len(self.cards)

    def deal(self):
        card = random.choice(self.cards)
        self.cards.remove(card)
        self.open_cards.append(card)
        return card


'''
Hand class refers to a hand for a participant of the game
'''


class Hand:

    def __init__(self):
        self.hand_cards = []
        self.total = []
        # self.soft_total = 0

    # Method to get hand total
    def get_hand_total(self):
        total = 0
        for card in self.hand_cards:
            total += card.num_value
        self.total = self.get_final_total(total)
        return self.total

    def is_soft_total(self):
        if 'A' in [card.get_face() for card in self.hand_cards]:
            return True
        return False

    def get_final_total(self, total):
        if total <= 21:
            return total
        high_ace = False
        for card in self.hand_cards:
            if card.get_face() == 'A':
                high_ace = True
                card.num_value = 1
                break
        if high_ace:
            return total - 10
        return total

    def get_initial_hand_total(self):
        initial_sum = 0
        for card in self.hand_cards[0:2]:
            initial_sum += card.get_value()
        return initial_sum
