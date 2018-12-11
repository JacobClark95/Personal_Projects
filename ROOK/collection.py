from card import Card, Color
import itertools
import random

class Collection():
    
    def __init__(self):
        self.cards = []
        
    def add(self, cards):
        """cards added must be in a list"""
        self.cards = self.cards + cards
    
    def remove(self, cards):
        for card in cards:
            self.cards.remove(card)
    
    def validCards(self):
        if len(self.withSuit(Card.lead)) != 0:
            return self.withSuit(Card.lead)
        elif len(self.withSuit(Card.trump)) != 0:
            return self.withSuit(Card.trump).union(self.withSuit(Color.ROOK))
        else:
            newCol = Collection()
            newCol.add(self.cards)
            return newCol
    
    def pointValue(self):
        return sum([x.pointValue for x in self.cards])
    
    def complement(self):
        numbers = list(range(1, 15))
        colors = [Color.RED, Color.GREEN, Color.YELLOW, Color.BLACK]
        comb = itertools.product(numbers, colors)
        allCards = [Card(x[0], x[1]) for x in comb] + [Card(0, Color.ROOK)]
        newCol = Collection()
        newCol.add(list(set(allCards) - set(self.cards)))
        return newCol
    
    def withValue(self, value):
        newCol = Collection()
        
        cardsWithValue = []
        for card in self.cards:
            if card.number == value or value == None:
                cardsWithValue.append(card)
        newCol.add(cardsWithValue)
        return newCol
                    
            
    def withSuit(self, suit):
        newCol = Collection()
        cardsWithSuit= []
        for card in self.cards:
            if card.suit == suit or suit == None:
                cardsWithSuit.append(card)
        newCol.add(cardsWithSuit)
        return newCol
    
    def withPoints(self):
        newCol = Collection()
        cardsWithPointValue= []
        for card in self.cards:
            if card.pointValue > 0:
                cardsWithPointValue.append(card)
        newCol.add(cardsWithPointValue)
        return newCol
    
    def intersection(self, collection):
        newCol = Collection()
        newCol.add(list(set(self.cards).intersection(set(collection.cards))))
        return newCol
    
    def union(self, collection):
        newCol = Collection()
        newCol.add(list(set(self.cards).union(set(collection.cards))))
        return newCol
    
    def randomElement(self):
        return random.choice(self.cards)
    
    def __len__(self):
        return (len(self.cards))
    
    def __contains__(self, value):
        return value in self.cards
    
    def __str__(self):
        return str([str(x) for x in self.cards])
    
    def __sub__(self, other):
        newCol = Collection()
        newCol.add(list(set(self.cards) - set(other.cards)))
        return newCol