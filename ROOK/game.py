from deck import Deck
from card import Card, Color
from player import Player, Team
from gamestatistics import GameStatistics
import numpy as np
import random

class Game():
    USER_ID = "USER"
    def __init__(self, inputFile):
        self.deck = Deck()
        self.widdow = None
        self.numPlayers = 5
        self.players = []
        self.numRounds = int(len(self.deck.cards) / self.numPlayers)
        self.gameStats = GameStatistics()
        
        self._initPlayers(self._importUserInput(inputFile))
        
        
        
    def _initPlayers(self, hand):
        cardsPerPlayer = self.numRounds
        cardsInWiddow = len(self.deck.cards) - cardsPerPlayer * self.numPlayers
        
        while True:
            userPlayer = Player(self.deck.buildUserHand(hand), self.gameStats)
            userPlayer.id, userPlayer.team = Game.USER_ID, Team.BID_WINNER
            self.players.append(userPlayer)
            for x in range(self.numPlayers - 1):
                newPlayer = Player(self.deck.deal(cardsPerPlayer), self.gameStats)
                self.players.append(newPlayer)
                
            if not all(np.array([x.hand.pointValue() for x in self.players[1:]]) > 0):
                self.players = []
                self.deck.refresh()
                continue
            
            self.gameStats.sittingOrder = [player.id for player in self.players]
            self.gameStats.startGame()
            self.widdow = self.deck.deal(cardsInWiddow)
            break

            
    def _findPlayerByID(self, ID):
        for player in self.players:
            if player.id == ID:
                return player
    
    def _buildTeams(self):
        bidWinner = self._findPlayerByID(Game.USER_ID)
        partnerCard, self.widdow = bidWinner.declareTrumpAndPartner(self.widdow)
        self.gameStats.roundLeader = Game.USER_ID
        
        for player in self.players:
            if (partnerCard in player.hand) or (player.team == Team.BID_WINNER):
                player.team = Team.BID_WINNER
                self.gameStats.teams[Team.BID_WINNER].append(player.id)
            else:
                player.team = Team.REGULAR
                self.gameStats.teams[Team.REGULAR].append(player.id)
    
    def _playRound(self):
        timeSpent = 0
        playerIndex = self.gameStats.sittingOrder.index(self.gameStats.roundLeader)
        self._findPlayerByID(self.gameStats.sittingOrder[playerIndex]).leadRound()
        for x in range(self.numPlayers - 1):
            timeSpent += self._findPlayerByID(self.gameStats.sittingOrder[(playerIndex + 1 + x) % self.numPlayers]).playInRound()
        
        self.gameStats.endRound()
        return timeSpent
    
    def _parseValue(self, val):
        if val.isdigit():
            return int(val)
        else:
            return None
        
    def _parseSuit(self, suit):
        responce = {'b':Color.BLACK, 'r':Color.RED, 'g':Color.GREEN,
                    'y':Color.YELLOW, '$':Color.ROOK, '*':None}
        return responce[suit]
    
    def _importUserInput(self, filename):
        text = ""
        with open(filename, 'r') as outfile:
            text = outfile.read()
        tokens = text.split()
        cards = [(self._parseValue(tokens[x]), self._parseSuit(tokens[x+1])) for x in range(0, len(tokens)-1, 2)]
        if len(cards) != self.numRounds:
            raise ValueError("Incorrect number of input cards")
        return cards

    def estimateBid(self):
        timeSpent = 0
        self._buildTeams()
        for x in range(self.numRounds):
            timeSpent += self._playRound()
        pointsWon = sum([self.gameStats.cardsWon[ID].pointValue()  for ID in self.gameStats.teams[Team.BID_WINNER]])
        return [pointsWon, timeSpent]
        
import time
tic = time.time()
points = []
timeSpent = []
for x in range(1000):
    if x % 100 == 0:
        print(x)
    g = Game('input.txt')
    blah = g.estimateBid()
    points.append(blah[0])
    timeSpent.append(blah[1])

toc = time.time()

import matplotlib.pyplot as plt

plt.figure(1)
plt.hist(points, bins = 10)
plt.show()

print(np.mean(points))
#print(sum(timeSpent) / (toc - tic))






    
