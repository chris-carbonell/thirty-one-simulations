# general
import copy
from itertools import combinations, cycle
import pandas as pd
from tabulate import tabulate

# game
import cards

# Constants

HAND_SCORES = pd.read_csv("assets/hand_scores.csv")

# Funcs

def calc_potential_scores(hand):
    '''
    calculate the average potential score of a hand if each card in the hand were replaced
    i.e., replace the first card with every other available card, calculate the scores for each
    of those combinations, and take the average of those scores. Then, repeat for the other two
    cards in the hand as well.
    '''
        
    # calculate scores
    scores = {}
    for remove_card in hand.cards:
               
        # get other cards
        other_cards = hand.cards.copy()
        other_cards.remove(remove_card)
                
        # filter permutations to potential hands
        # assuming we replaced only the removed card
        potential_hands = HAND_SCORES.loc[
            (HAND_SCORES['card_one'] == str(other_cards[0])) &
            (HAND_SCORES['card_two'] == str(other_cards[1])) &
            (HAND_SCORES['card_three'] != str(remove_card))
        ]  # i.e., card_three varies (just can't be the card we already have)
        
        scores[str(remove_card)] = round(potential_hands['score'].sum() / len(potential_hands.index), 3)
    
    return scores

def get_better_hand(hand_one, hand_two):
    '''
    identify better hand based on score
    '''
    if hand_one.score >= hand_two.score:
        return hand_one
    else:
        return hand_two

# Classes

class Hand(cards.Stack):
    '''
    represent a hand of cards
    
    A legal hand must contain three cards. Therefore, while we're dealing cards, technically,
    the first card of a hand goes into a Stack, the second and third carsd get added to that Stack,
    then that Stack is converted into a Hand.
    '''

    def __init__(self, *args):
        if len(args) > 0:
            self.cards = cards.Stack.stack_cards(self, *args)
        if len(self.cards) != 3:
            raise ValueError("unsupported number of cards in hand")

    def __repr__(self):
        return f"{sorted(self.cards)}"

    def __str__(self):
        return f"{sorted(self.cards)}"

    def swap(self, old, new):
        '''
        replace old card with new card
        '''
        for idx, card in enumerate(self.cards):
            if card == old:
                self.cards[idx] = new

    @property
    def score(self):
        '''
        score the hand
        '''

        # if hand not complete, then error out
        if len(self.cards) != 3:
            raise ValueError("unexpected number of cards in hand")
        
        else:
            
            # define score values for each card value
            VALUES = {
                cards.Card.TWO: 2,
                cards.Card.THREE: 3,
                cards.Card.FOUR: 4,
                cards.Card.FIVE: 5,
                cards.Card.SIX: 6,
                cards.Card.SEVEN: 7,
                cards.Card.EIGHT: 8,
                cards.Card.NINE: 9,
                cards.Card.TEN: 10,
                cards.Card.JACK: 10,
                cards.Card.QUEEN: 10,
                cards.Card.KING: 10,
                cards.Card.ACE: 11
            }

            # if all same value, then 30
            if self.cards[0].value == self.cards[1].value == self.cards[2].value:
                return 30.5

            # otherwise, tally score per suit and take max
            
            # calculate score for each suit in hand
            scores = {}
            for card in self.cards:
                if card.suit not in scores:
                    suit = card.suit
                    scores[suit] = sum([VALUES[card.value] if card.suit == suit else 0 for card in self.cards])

            # get max score
            max_score = None
            for suit, score in scores.items():
                if max_score is None:
                    max_score = score
                else:
                    max_score = max(max_score, score)

            return max_score
    
    @property
    def potential_scores(self):
        '''
        calculate the average potential scores of the hand if each card in the hand were replaced
        '''
        return calc_potential_scores(self)

    @property
    def worst_card(self):
        '''
        identify the worst card (by potential score)
        i.e., this is the card we should most likely replace
        '''
        worst_card_score = max(list(self.potential_scores.values()))
        for k, v in self.potential_scores.items():
            if v == worst_card_score:
                return cards.Card(k)  # even if there's a tie, just return the first one we find

class ThirtyOne():

    def __init__(self, num_players=2, num_chips=3):
        
        # get players and chips
        self.players = list(range(num_players))
        self.chips = [num_chips for i in self.players]  # give each player chips

        # get deck
        self.deck = cards.StandardDeck()
        self.deck.shuffle()

        # deal cards to players
        stacks = [cards.Stack() for i in self.players]  # holding spot for cards until they can be added to hands
        # in 3 rounds, deal one card to each player for a total of 3 cards for each player
        for i in range(3):
            for player in self.players:
                stacks[player] += self.deck.draw()

        # convert to hands
        hands = []
        for stack in stacks:
            hands.append(Hand(stack))
        self.hands = hands

        # counters
        self.turns = 0  # count turns
        self.round = 0  # count rounds
        self._turn_cycle = cycle(self.players)  # current turn's player i.e., 0, 1, ... , n, 0, 1, ... , n, ...
        self.current_player = 0

        # discard pile
        self.discard = cards.Stack(self.deck.draw())  # initiate with first card

        # key players
        self.knocker = None  # who knocked?
    
    def __repr__(self):
        return self.print()

    def __str__(self):
        return self.print()

    def advance_counters(self):

        # update current player
        if self.turns == 0:
            # current player initialized to zero
            # so need to advance twice: first time to 0 then to 1
            next_player = next(self._turn_cycle)  # 0
            next_player = next(self._turn_cycle)  # 1
        else:
            next_player = next(self._turn_cycle)
        self.current_player = next_player

        # update counters
        self.turns += 1
        if self.current_player == self.players[-1]:
            # if last player, after we advance, it'll be the start of a new round
            self.round += 1

    def print(self):

        game_info = [
            "1. Game Info:",
            f"num_players: {len(self.players)}",
            f"deck (unsorted) ({len(self.deck)}): {self.deck.cards}",
            f"deck (sorted) ({len(self.deck)}): {sorted(self.deck.cards)}",
            f"discard ({len(self.discard)}): {self.discard}",
            f"round: {self.round}",
            f"turns: {self.turns}",
            f"knocker: {self.knocker}",
            f"knocker_survived: {self.knocker_survived}"
        ]
        
        # get status codes for eaach player
        player_codes = []
        for player in self.players:

            code = ""

            # current
            if player == self.current_player:
                code += "*"

            # knocker
            if player == self.knocker:
                code += "k"

            # bottom
            if player in self.bottom_players:
                code += "b"

            # wrap
            if len(code) > 0:
                code = f"{player}({code})"
            else:
                code = player

            player_codes.append(code)

        table = {
            'player': player_codes,
            'chips': self.chips,
            'hand': self.hands,
            'score': self.scores
        }
        
        table_tabulated = tabulate(
            table, 
            headers='keys',
            tablefmt='github',
            colalign=("center",) * len(table.keys())
        )

        return "\n".join(game_info) + "\n\n2. Player Info:\n" + table_tabulated

    @property
    def scores(self):
        return [hand.score for hand in self.hands]

    @property
    def bottom_score(self):
        return min(self.scores)

    @property
    def bottom_players(self):
        bottom_players = []
        for player in self.players:
            if self.scores[player] == self.bottom_score:
                bottom_players.append(player)
        return bottom_players

    @property
    def knocker_survived(self):
        '''
        did the knocker not have the lowest hand?
        '''
        if self.knocker is not None:
            if self.knocker in self.bottom_players:
                if len(self.bottom_players) > 1:
                    return True  # knocker is safe if there's a tie
                else:
                    return False
            else:
                return True
        else:
            return None

    def play_hand(self):
        '''
        play through current player's turn
        '''

        # get player hand
        player_hand = self.hands[self.current_player]

        # if score is 31, game over
        if player_hand.score == 31:
            self.end_game(winner=self.current_player)

        # if discard card improves hand's score potential, take it
        potential_hand = copy.deepcopy(player_hand)
        discard_card = self.discard.cards[-1]  # don't draw it, just look at it
        potential_hand.swap(
            potential_hand.worst_card,
            discard_card
        )
        if get_better_hand(player_hand, potential_hand) == potential_hand:
            remove_card = player_hand.worst_card
            player_hand.swap(
                remove_card,
                self.discard.draw()
            )
            self.discard += remove_card  # put replaced card in discard pile

        else:
            
            # if deck has cards
            if len(self.deck) > 0:
            
                # otherwise, draw the top card
                drawn_card = self.deck.draw()
                
                # if the top card improves hand's score potential, take it
                potential_hand = copy.deepcopy(player_hand)
                potential_hand.swap(
                    potential_hand.worst_card,
                    drawn_card
                )
                if get_better_hand(player_hand, potential_hand) == potential_hand:
                    remove_card = player_hand.worst_card
                    player_hand.swap(
                        remove_card,
                        drawn_card
                    )
                    self.discard += remove_card
                
                else:
                    # otherwise, put top card on top of discard pile
                    self.discard += drawn_card
            
            # deck has no cards so end
            else:
                self.end_game()

        # if score is 31, game over
        if player_hand.score == 31:
            self.end_game(winner=self.current_player)

        # update counters
        self.advance_counters()

    def end_game(self, knocker=None, winner=None):
        
        # game won via 31
        if winner:
            # everyone but winner loses a life
            for player, chips in enumerate(self.chips):
                if player != winner:
                    self.chips[player] = max(0, self.chips[player] - 1)

        # game won via knocking
        if knocker:
            # find lowest score
            min_score = min(self.scores)
            for player, chips in enumerate(self.chips):
                    if self.scores[player] == min_score and player != knocker:
                        # if tie, knocker is safe
                        self.chips[player] = max(0, self.chips[player] - 1)

    def play(self, knocker=None):
        '''
        play through, at most, two full rounds:
        1. in the first round, the knocker will knock without picking up any cards
        2. after the kocker knocks, everyone else gets another turn
        '''

        # track knocker
        self.knocker = knocker

        # for every player before knocker,
        # play hand
        for player in range(knocker):
            self.play_hand()

        # knocker knocks ie skips their turn
        self.advance_counters()

        # everyone else gets one more play
        while self.current_player != knocker:
            self.play_hand()