from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLACK = 4
    ROOK = 5
    
    def __str__(self):
        nameMap = {Color.RED : "RED", Color.BLACK : "BLACK", \
                   Color.YELLOW : "YELLOW", Color.GREEN : "GREEN",\
                   Color.ROOK : "ROOK"}
        return nameMap[self]


class Card:
    trump = None
    lead = None
    _cardValue = {1:14, 14:13, 13:12, 12:11, 11:10, 10:9, 9:8, 8:7, 7:6, 6:5, 5:4, 4:3, 3:2, 2:1, 0:0}
    _suitValue = {Color.RED:1, Color.GREEN:2, Color.YELLOW:3, Color.BLACK:4}
    
    def __init__(self, number, suit):
        self.suit = suit
        self.number = number
        self.pointValue = self._getPoint()   
        
    def _getPoint(self):
        if self.number in [10, 14]:
            return 10
        elif self.number in [5]:
            return 5
        elif self.number in [1]:
            return 15
        elif self.suit == Color.ROOK:
            return 20
        else:
            return 0
    
    def __lt__(self, other):
        if self == other:
            return False
        
        if Card.trump != None:
            if (self.suit in [Card.trump, Color.ROOK] and other.suit in [Card.trump, Color.ROOK]):
                return Card._cardValue[self.number] < Card._cardValue[other.number]
            elif self.suit not in [Card.trump, Color.ROOK] and other.suit in [Card.trump, Color.ROOK]:
                return True
            elif self.suit in [Card.trump, Color.ROOK] and other.suit not in [Card.trump, Color.ROOK]:
                return False
        
        if Card.lead != None:    
            if self.suit == Card.lead and other.suit == Card.lead:
                return Card._cardValue[self.number] < Card._cardValue[other.number]
            elif self.suit != Card.lead and other.suit == Card.lead:
                return True
            elif self.suit == Card.lead and other.suit != Card.lead:
                return False
        
        if Card._cardValue[self.number] != Card._cardValue[other.number]:
            return Card._cardValue[self.number] < Card._cardValue[other.number]
        
        return Card._suitValue[self.suit] < Card._suitValue[other.suit]
        
        
    def __gt__(self, other):
        if self == other:
            return False
        else:
            return not self < other
    
    def __eq__(self, other):
        if other == None:
            return False
        elif self.number == other.number and self.suit == other.suit:
            return True
        else:
            return False
    
    def __str__(self):
        return str(self.number) + " " + str(self.suit)

    def __hash__(self):
        return hash(str(self))