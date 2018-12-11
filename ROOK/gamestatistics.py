from player import Team
from collection import Collection
from card import Card
import time

class GameStatistics():
    
    def __init__(self):
        self.roundNum = 1
        self.roundLeader = None
        self.sittingOrder = []
        self.teams = {Team.BID_WINNER:[], Team.REGULAR:[]}
        self.cardsWon = {}
        self.cardsPlayedThisRound = {}
        self.cardsNotPlayed = {}
        
        self.playersMissingSuit = {}
        
    def startGame(self):
        self.cardsWon = {player : Collection() for player in self.sittingOrder}
        self.cardsPlayedThisRound = {player : None for player in self.sittingOrder}
        self.playersMissingSuit = {player : [] for player in self.sittingOrder}
        self.cardsNotPlayed = Collection().complement()
        
    def playCard(self, playerID, card):
        if card.suit != Card.lead:
            self.playersMissingSuit[playerID].append(Card.lead)
        self.cardsNotPlayed.remove([card])
        self.cardsPlayedThisRound[playerID] = card
            
    def endRound(self):
        winner = self.whoIsWinningRound()
        self.cardsWon[winner].add(list(self.cardsPlayedThisRound.values()))
        self.cardsPlayedThisRound = {player : None for player in self.sittingOrder}
        self.roundNum += 1
        self.roundLeader = winner
    
    def pointsToBePlayed(self):
        cardsLeftToBePlayed = list(self.cardsPlayedThisRound.values()).count(None) - 1
        averageCardValue = self.cardsNotPlayed.pointValue() / len(self.cardsNotPlayed)
        return cardsLeftToBePlayed * averageCardValue
        
        
    def oddsOfWinning(self, playerID, card):
        """ this returns the probability that you win minus the probability that the 
        opponent wins"""
        
        myTeam = Team.BID_WINNER if playerID in self.teams[Team.BID_WINNER] else Team.REGULAR
        winningPlayer = self.whoIsWinningRound()
        if winningPlayer == None:
            #TODO: startingGame
            return None
        else:    
            winningTeam = Team.BID_WINNER if winningPlayer in self.teams[Team.BID_WINNER] else Team.REGULAR
            winningCard = self.cardsPlayedThisRound[winningPlayer]
            if winningCard > card and winningTeam != myTeam:
                #TODO: add the possability that the our team will win
                return -1
            else:
                #TODO: subtract the possability that the other team will win
                return 1
            
        
    
    def whoIsWinningRound(self):
        playedCards = list(set(self.cardsPlayedThisRound.values()))
        if None in playedCards:
            playedCards.remove(None)
            
        if len(playedCards) == 0:
            return None
        
        winningCard = max(playedCards)
        return list(self.cardsPlayedThisRound.keys()) \
            [list(self.cardsPlayedThisRound.values()).index(winningCard)]
        
        