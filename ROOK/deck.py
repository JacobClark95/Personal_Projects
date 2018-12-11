from card import Color, Card
from collection import Collection
import itertools
from random import shuffle

class Deck:
    
    def __init__(self):
        self.cards = self._buildDeck()
    
    def _buildDeck(self):
        numbers = list(range(1, 15))
        colors = [Color.RED, Color.GREEN, Color.YELLOW, Color.BLACK]
        comb = itertools.product(numbers, colors)
        deck = [Card(x[0], x[1]) for x in comb] + [Card(0, Color.ROOK)]
        shuffle(deck)
        return deck
    
    def deal(self, num = 1):
        deal = self.cards[:num]
        del self.cards[:num]
        col = Collection()
        col.add(deal)
        return col
    
    def _pick(self, num, suit):
        col = Collection()
        col.add(self.cards)
        pickedCard = col.withValue(num).intersection(col.withSuit(suit)).randomElement()
        self.cards.remove(pickedCard)
        return pickedCard
        
    
    def buildUserHand(self, hand):
        userHand = []
        for cardTuple in hand:
            userHand.append(self._pick(cardTuple[0], cardTuple[1]))
        col = Collection()
        col.add(userHand)
        return col
    
    def refresh(self):
        self.cards = self._buildDeck()
    
    def __len__(self):
        return len(self.cards)