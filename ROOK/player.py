import uuid
from enum import Enum
from card import Card, Color
from collection import Collection
import time


class Team(Enum):
    BID_WINNER = 1
    REGULAR = 2

class Player():
    
    def __init__(self, hand, stats):
        self.id = str(uuid.uuid4())
        self.hand = hand
        self.team = None
        self.stats = stats
        self.knowledgeOfWiddow = None
    
    def makeBid(self):
        maxBid = hash(self.id) % 180
        if self.stats.bid < maxBid:
            self.stats.bid = self.stats.bid + 5
            self.stats.bidWinner = self.id
            return True
        else:
            return False
        
    def _smartTrump(self, widdow):
        cardValue = {1:14, 14:13, 13:12, 12:11, 11:10, 10:9, 9:8, 8:7, 7:6, 
                      6:5, 5:4, 4:3, 3:2, 2:1, 0:0}
        tallies = {Color.BLACK:0, Color.YELLOW:0, Color.GREEN:0, Color.RED:0}
        
        for color in tallies:
            tallies[color] = sum([cardValue[x.number] for x in self.hand.withSuit(color).cards]) + \
            sum([cardValue[x.number] for x in widdow.withSuit(color).cards])

        return list(tallies.keys())[list(tallies.values()).index(max(tallies.values()))] 
    
    def _smartWiddow(self, widdow):
        newWiddow = Collection()
        for wCard in widdow.cards:
            weakestCard = min(self.hand.cards)
            if wCard > weakestCard:
                newWiddow.add([weakestCard])
                self.hand.remove([weakestCard])
                self.hand.add([wCard])
            else:    
                newWiddow.add([widdow])
        self.knowledgeOfWiddow = newWiddow
        return newWiddow
    
    
    def _smartPartner(self):
        return max((self.knowledgeOfWiddow.complement().withSuit(Card.trump) - self.hand.withSuit(Card.trump)).cards)       
    
    def declareTrumpAndPartner(self, widdow):
        self.team = Team.BID_WINNER

        Card.trump = self._smartTrump(widdow)
        newWiddow = self._smartWiddow(widdow)
        return self._smartPartner(), newWiddow
    
    def leadRound(self):
        selectedCard = self.hand.randomElement()
        Card.lead = selectedCard.suit
        self.hand.remove([selectedCard])
        self.stats.playCard(self.id, selectedCard)
        
    
    def playInRound(self):
        tic = time.time()
        validCards = self.hand.validCards()
        odds = []
        pointValues = []
        
        pointsOnTable = 180 - self.stats.cardsNotPlayed.pointValue()
        
        potentialPoints = self.stats.pointsToBePlayed()
        
        
        for card in validCards.cards:
            odds.append(self.stats.oddsOfWinning(self.id, card))
            pointValues.append(card.pointValue + pointsOnTable + potentialPoints)
    
        pointOdds = [odds[x] * pointValues[x] for x in range(len(odds))]
        selectedCard = self.hand.cards[pointOdds.index(max(pointOdds))]
        
            
        self.hand.remove([selectedCard])
        self.stats.playCard(self.id, selectedCard)
        toc = time.time()
        
        return toc - tic
    
    
            
    
    