import random

class Card:
    """Represents a standard playing card.
    
    Attributes:
      suit: integer 0-3
      rank: integer 1-13
    """

    # Class-level attributes for suit and rank names
    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7", 
              "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit=0, rank=2):
        # Initialize card with given suit and rank
        self.suit = suit
        self.rank = rank

    def __str__(self):
        # Human-readable string of the card's rank and suit
        return '%s of %s' % (Card.rank_names[self.rank],
                             Card.suit_names[self.suit])

    def __eq__(self, other):
        # Check if two cards are equal (same rank and suit)
        return self.suit == other.suit and self.rank == other.rank

    def __lt__(self, other):
        # Compare two cards by suit and rank
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return t1 < t2


class Deck:
    def __init__(self):
        # Create a deck with 52 cards
        self.cards = []
        for suit in range(4):
            for rank in range(1,14):
                card = Card(suit, rank)
                self.cards.append(card)

    def __str__(self):
        # String representation of the deck
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)
    
    def __len__(self):
        # Return the number of cards in the deck
        return len(self.cards)
    
    def __getitem__(self, position):
        # Allow indexing into the deck
        return self.cards[position]
    
    def __setitem__(self, key, value):
        # Allow setting cards at a specific position
        self.cards[key] = value
    
    def shuffle(self):
        # Shuffle the deck
        random.shuffle(self.cards)
        
    def pop_card(self):
        # Remove and return the last card in the deck
        return self.cards.pop()
    
    def add_card(self, card):
        # Add a card to the deck
        self.cards.append(card)
    
    def sort(self):
        # Sort the deck by suit and rank
        self.cards.sort()
        
    def move_cards(self, hand, num):
        # Move 'num' cards from the deck to a hand
        for i in range(num):
            hand.add_card(self.pop_card())


class Hand(Deck):
    """Represents a hand of playing cards."""
    
    def __init__(self, label=''):
        # Initialize an empty hand with a label
        self.cards = []
        self.label = label


def find_defining_class(obj, method_name):
    # Find the class that defines a method for a given object
    for ty in type(obj).mro():
        if method_name in ty.__dict__:
            return ty
    return None

class PokerHand(Hand):
    """Represents a poker hand."""
    
    # Rank of hands from highest to lowest
    all_labels = ['straightflush', 'fourkind', 'fullhouse', 'flush',
                  'straight', 'threekind', 'twopair', 'pair', 'highcard']

    def suit_hist(self):
        # Builds a count of suits in the hand and stores it in self.suits
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1

    def has_flush(self):
        # Returns True if the hand contains 5 or more cards of the same suit
        self.suit_hist()
        for val in self.suits.values():
            if val >= 5:
                return True
        return False
# make a deck
deck = Deck()
deck.shuffle()

# deal the cards and classify the hands
for i in range(2):
    hand = PokerHand()
    deck.move_cards(hand, 7)
    hand.sort()
    print(hand)
    print(hand.has_flush())
    print('')

# This code chunk creates a hand, 
# adds seven cards to it, 5 of which are diamonds
# it checks to see if a flush exists and returns True
hand = PokerHand()
hand.add_card(Card(1,1))
hand.add_card(Card(1,3))
hand.add_card(Card(1,13))
hand.add_card(Card(1,12))
hand.add_card(Card(1,6))
hand.add_card(Card(2,3))
hand.add_card(Card(0,7))
hand.sort()
print(hand)
print(hand.has_flush())

class PokerHand(Hand):
    """Represents a poker hand."""

    # all_labels is a list of all the labels in order from highest rank
    # to lowest rank
    all_labels = ['straightflush', 'fourkind', 'fullhouse', 'flush',
                  'straight', 'threekind', 'twopair', 'pair', 'highcard']
    
    def suit_hist(self):
        """Builds a histogram of the suits that appear in the hand.
        Stores the result in attribute suits.
        """
        self.suits = {}
        for card in self.cards:
            self.suits[card.suit] = self.suits.get(card.suit, 0) + 1

    def rank_hist(self):
        """This custom helper function creates a histogram of the ranks 
        present in the hand and stores the result in the 'ranks' attribute."""
        self.ranks = {}
        for card in self.cards:
            self.ranks[card.rank] = self.ranks.get(card.rank, 0) + 1
    
    def has_flush(self):
        """Returns True if the hand has a flush, False otherwise.
        Note that this works correctly for hands with more than 5 cards.
        """
        self.suit_hist()
        for val in self.suits.values():
            if val >= 5:
                return True
        return False

    def has_straightflush(self):
        suits = {}
        for card in self.cards:
            if card.suit in suits:
                suits[card.suit].append(card.rank)
            else:
                suits[card.suit] = [card.rank]
        for suit in suits.keys():
            for rank in suits[suit]:
                if set([rank, rank+1, rank+2, rank+3, rank+4]) & set(suits[suit]) == set([rank, rank+1, rank+2, rank+3, rank+4]):
                    return True
            if set([1, 10, 11, 12, 13]) & set(suits[suit]) == set([1, 10, 11, 12, 13]):
                return True
        return False

    def has_fourkind(self):
        self.rank_hist()
        for val in self.ranks.values():
            if val == 4:
                return True
        return False
    
    def has_fullhouse(self):
        pair_counter = 0
        triplet_counter = 0
        self.rank_hist()
        for val in self.ranks.values():
            if val >= 3:
                triplet_counter += 1
            elif val >= 2:
                pair_counter += 1
        if (pair_counter >= 1 and triplet_counter >= 1) or triplet_counter >= 2:
            return True
        return False
    
    def has_straight(self):
        self.rank_hist()
        for key in self.ranks.keys():
            if set([key, key+1, key+2, key+3, key+4]) & set(self.ranks.keys()) == set([key, key+1, key+2, key+3, key+4]):
                return True
        if set([1, 10, 11, 12, 13]) & set(self.ranks.keys()) == set([1, 10, 11, 12, 13]):
            return True
        return False
    
    def has_threekind(self):
        self.rank_hist()
        for val in self.ranks.values():
            if val >= 3:
                return True
        return False     
    
    def has_twopair(self):
        pair_counter = 0
        self.rank_hist()
        for val in self.ranks.values():
            if val >= 2:
                pair_counter += 1
        if pair_counter >= 2:
            return True
        return False
    
    def has_pair(self):
        self.rank_hist()
        for val in self.ranks.values():
            if val >= 2:
                return True
        return False

    def classify(self):
        if self.has_straightflush():
            self.label = self.all_labels[0]
        elif self.has_fourkind():
            self.label = self.all_labels[1]
        elif self.has_fullhouse():
            self.label = self.all_labels[2]
        elif self.has_flush():
            self.label = self.all_labels[3]
        elif self.has_straight():
            self.label = self.all_labels[4]
        elif self.has_threekind():
            self.label = self.all_labels[5]
        elif self.has_twopair():
            self.label = self.all_labels[6]
        elif self.has_pair():
            self.label = self.all_labels[7]
        else:
            self.label = self.all_labels[8]


# TEST CASES

## Full House 
hand = PokerHand()
hand.add_card(Card(0,1)) 
hand.add_card(Card(1,1)) 
hand.add_card(Card(2,1)) 
hand.add_card(Card(0,11))
hand.add_card(Card(1,11))
hand.add_card(Card(2,11))
hand.add_card(Card(0,3))
hand.classify()
print(hand)
print(hand.label) 
hand.has_pair()

## Straight Flush
hand = PokerHand()
hand.add_card(Card(0,1))
hand.add_card(Card(0,2))
hand.add_card(Card(0,3))
hand.add_card(Card(0,4))
hand.add_card(Card(0,5))
hand.add_card(Card(1,5))
hand.add_card(Card(2,5))
hand.classify()
print(hand)
print(hand.label)

## Straight Flush
hand = PokerHand()
hand.add_card(Card(0,1))
hand.add_card(Card(0,13))
hand.add_card(Card(0,12))
hand.add_card(Card(0,11))
hand.add_card(Card(0,10))
hand.add_card(Card(1,11))
hand.add_card(Card(2,12))
hand.classify()
print(hand)
print(hand.label) 

## Straight
hand = PokerHand()
hand.add_card(Card(0,2))
hand.add_card(Card(0,3))
hand.add_card(Card(1,4))
hand.add_card(Card(2,5))
hand.add_card(Card(1,2))
hand.add_card(Card(3,6))
hand.add_card(Card(2,6))
hand.classify()
print(hand)
print(hand.label)

## Straight
hand = PokerHand()
hand.add_card(Card(0,2))
hand.add_card(Card(0,3))
hand.add_card(Card(2,5))
hand.add_card(Card(0,10))
hand.add_card(Card(1,10))
hand.add_card(Card(1,4))
hand.add_card(Card(0,6))
hand.classify()
print(hand)
print(hand.label)

## Flush (contains a straight and a flush, but is not straight flush)
hand = PokerHand()
hand.add_card(Card(0,2))
hand.add_card(Card(0,3))
hand.add_card(Card(0,4))
hand.add_card(Card(0,5))
hand.add_card(Card(1,6))
hand.add_card(Card(1,7))
hand.add_card(Card(0,8))
hand.classify()
print(hand)
print(hand.label)

## Two Pair
hand = PokerHand()
hand.add_card(Card(0,2))
hand.add_card(Card(1,2))
hand.add_card(Card(0,4))
hand.add_card(Card(1,4))
hand.add_card(Card(0,5))
hand.add_card(Card(1,5))
hand.add_card(Card(0,6))
hand.classify()
print(hand)
print(hand.label)

## Estimating the probabilites of these hands
class PokerDeck(Deck):
    """Represents a deck of cards that can deal poker hands."""

    def deal_hands(self, num_cards=7, num_hands=7):
        """Deals hands from the deck and returns Hands. The hands are classified before they are returned.
        num_cards: cards per hand
        num_hands: number of hands

        returns: list of Hands
        """
        hands = []
        for i in range(num_hands):        
            hand = PokerHand()
            self.move_cards(hand, num_cards)
            hand.classify()
            hands.append(hand)
        return hands
    
class Hist(dict):
    """A map from each item (x) to its frequency."""

    def __init__(self, seq=[]):
        "Creates a new histogram starting with the items in seq."
        for x in seq:
            self.count(x)

    def count(self, x, f=1):
        "Increments (or decrements) the counter associated with item x."
        self[x] = self.get(x, 0) + f
        if self[x] == 0:
            del self[x]

## Test Cases for the probabilites
def main():
    # the label histogram: map from label to number of occurances
    labelhist = Hist()

    # loop n times, dealing 5 hands per iteration, 7 cards each
    n = 20000
    for i in range(n):
        if i % 1000 == 0:
            print(i)
            
        deck = PokerDeck()
        deck.shuffle()

        hands = deck.deal_hands(7, 5)
        for hand in hands:
            labelhist.count(hand.label)
            
    # print the results
    total = 5.0 * n
    print(total, 'hands dealt:')

    for label in PokerHand.all_labels:
        freq = labelhist.get(label, 0)
        p = 100 * freq / total
        if freq == 0: 
            odds = float('inf')
        else:
            odds = (total - freq) / freq
        print('{:} happens with probability {:.3f}%; odds against: {:.2f} : 1'.format(label, p, odds))


# Testing the simulator
main()