# general
import functools
from functools import total_ordering
import random

@total_ordering
class Card:
    '''
    represent a playing card that has a value (e.g., T) and suit (e.g., C)

    Attributes
    ----------
    value : str
        value of the card (e.g., T for Ten of Clubs)
    suit : str
        suit of the card (e.g., C for Ten of Clubs)
    '''

    # constants

    # values
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "T"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"
    VALUES = [TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE]
    
    # suits
    CLUBS = "C"
    DIAMONDS = "D"
    HEARTS = "H"
    SPADES = "S"
    SUITS = [CLUBS, DIAMONDS, HEARTS, SPADES]

    # ordering
    # ace high
    # ORDERED = [f"{value}{suit}" for suit in SUITS for value in VALUES]  # idk why this doesn't work
    ORDERED = [
        '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC', 
        '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD', 
        '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH', 
        '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS'
    ]

    def __init__(self, *args):

        # parse
        if len(args) == 1:
            # e.g., 6H = 6, H
            value = args[0][0]
            suit = args[0][1]
        elif len(args) == 2:
            # e.g., 6, H = 6, H
            value = args[0]
            suit = args[1]
        
        # test

        if value not in self.VALUES:
            raise ValueError("value not supported")
        
        if suit not in self.SUITS:
            raise ValueError("suit not supported")

        self.value = value  # 1...9 = 1..9, T = 10, J = jack, Q = queen, K = king
        self.suit = suit  # C = clubs, D = diamonds, H = hearts, S = spades

    def __repr__(self):
        return f"{self.value}{self.suit}"

    def __str__(self):
        return f"{self.value}{self.suit}"

    def __add__(self, new):
        if isinstance(new, Card) or isinstance(new, Stack):
            return Stack(self, new)
        else:
            raise TypeError("unsupported add")

    def __lt__(self, other):
        return self.ORDERED.index(str(self)) < self.ORDERED.index(str(other))

    def __le__(self, other):
        return self.ORDERED.index(str(self)) <= self.ORDERED.index(str(other))

    def __gt__(self, other):
        return self.ORDERED.index(str(self)) > self.ORDERED.index(str(other))

    def __ge__(self, other):
        return self.ORDERED.index(str(self)) >= self.ORDERED.index(str(other))

    def __eq__(self, other):
        return self.ORDERED.index(str(self)) == self.ORDERED.index(str(other))

    def __ne__(self, other):
        return not self == other

class Stack:
    '''
    represent a stack of playing cards
    the end of the list is the top of the deck

    Attributes
    ----------
    cards : list
        list of cards

    Methods
    -------
    shuffle
        randomize order of cards in stack

    add_cards(cards)
        add cards to the stack
    '''

    def __init__(self, *args):
        self.cards = []
        if len(args) > 0:
            self.cards = self.stack_cards(self, *args)

    def __repr__(self):
        return f"{self.cards}"

    def __str__(self):
        return f"{self.cards}"

    def __add__(self, new):
        return Stack(self.stack_cards(self.cards, new))

    def __len__(self):
        return len(self.cards)

    def draw(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None

    def remove(self, card):
        '''
        remove a single, specific card from the deck
        '''
        if not isinstance(card, Card):
            raise TyperError("card expected")
        else:
            self.cards.remove(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def stack_cards(self, *args):
        '''
        create a stack of cards from any combination of cards, stacks, and lists of cards
        '''

        stack = []
        for item in args:
            if isinstance(item, Card):
                stack.append(item)
            elif isinstance(item, tuple) or isinstance(item, list):
                for subitem in item:
                    stack.append(subitem)
            elif isinstance(item, Stack):
                stack += item.cards
            else:
                raise TypeError("unsupported item to add")

        return stack

class StandardDeck(Stack):
    '''
    represent a standard deck of playing cards
    '''

    def __init__(self):
        self.cards = [Card(x) for x in Card.ORDERED]