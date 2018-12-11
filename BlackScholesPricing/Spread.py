import Option as o
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt



# Next thing to do is to be able to evaluate spreads before expiration and graph them

class OptionType(Enum):
    LONG_CALL = 1
    SHORT_CALL = 2
    LONG_PUT = 3
    SHORT_PUT = 4
    
    
class Spread():
    def __init__(self, underlying, volatility, interestRate=3.038):
        self.So = underlying
        self.sigma = volatility 
        self.r = interestRate
        
        self.positions = set()
        self.lossLowerBound = None
        
    def addOption(self, strike, timeToExpiration, optionType, quantity):
        for x in range(quantity):
            if optionType == OptionType.LONG_CALL:
                position = o.CallLong(self.So, strike, self.sigma, self.r, timeToExpiration)
                self.positions.add(position)
        
            elif optionType == OptionType.SHORT_CALL:
                position = o.CallShort(self.So, strike, self.sigma, self.r, timeToExpiration)
                self.positions.add(position)
        
            elif optionType == OptionType.LONG_PUT:
                position = o.PutLong(self.So, strike, self.sigma, self.r, timeToExpiration)
                self.positions.add(position)
            
            else:
                position = o.PutShort(self.So, strike, self.sigma, self.r, timeToExpiration)
                self.positions.add(position)
        
        self._calcMaxLoss()
    
    def clearSpread(self):
        self.positions = set()
        self.lossLowerBound = None
        
    def addIronButterfly(self, timeToExpiration, width, quantity):
        assert width > 0
        
        self.addOption(self.So, timeToExpiration, OptionType.SHORT_CALL, quantity)
        self.addOption(self.So, timeToExpiration, OptionType.SHORT_PUT, quantity)
        self.addOption(self.So + width/2, timeToExpiration, OptionType.LONG_CALL, quantity)
        self.addOption(self.So - width/2, timeToExpiration, OptionType.LONG_PUT, quantity)
    
    def addIronCondor(self, timeToExpiration, innerWidth, insuranceLength, quantity):
        assert (innerWidth > 0 and insuranceLength > 0)
        insFromCenter = innerWidth / 2 + insuranceLength
        
        self.addOption(self.So + innerWidth/2, timeToExpiration, OptionType.SHORT_CALL, quantity)
        self.addOption(self.So - innerWidth/2, timeToExpiration, OptionType.SHORT_PUT, quantity)
        self.addOption(self.So + insFromCenter, timeToExpiration, OptionType.LONG_CALL, quantity)
        self.addOption(self.So - insFromCenter, timeToExpiration, OptionType.LONG_PUT, quantity)
    
    
    def addCallCalendar(self, timeToExpirationLong, timeToExpirationSort, strike, quantity):
        self.addOption(strike, timeToExpirationSort, OptionType.SHORT_CALL, quantity)
        self.addOption(strike, timeToExpirationLong, OptionType.LONG_CALL, quantity)
    
    
        
    def evaluateSpreadAtExpiration(self, underlyingAtExpiration):
        payout = 0
        
        for option in self.positions:
            optionReturn = option.getPayoutAtExpiration(underlyingAtExpiration)
            payout = payout + optionReturn
        
        return payout
    
    def evaluateSpread(self, underlying, volatility, timeElapsed):
        payout = 0
        
        for option in self.positions:
            optionReturn = option.getPayout(underlying, volatility, timeElapsed)
            payout = payout + optionReturn
        
        return payout
    
    def plotSpreadAtExpiration(self):
        lowestStrike, highestStrike = self._calcLowestHighestStrike()
        lowerBound = lowestStrike - self.So * 0.05
        upperBound = highestStrike + self.So * 0.05
        
        underlyingAtExpiration = np.linspace(lowerBound, upperBound, 100)
        payoutAtExpiration = []
        
        for Sn in underlyingAtExpiration:
            payoutAtExpiration.append(self.evaluateSpreadAtExpiration(Sn))
            
        payoutAtExpiration = np.array(payoutAtExpiration)
        
        plt.figure(1)
        plt.plot(underlyingAtExpiration, payoutAtExpiration, 'b-')
        plt.plot(underlyingAtExpiration, np.zeros(len(underlyingAtExpiration)), 'r--')
        plt.plot()
        
    def plotSpread(self, volatility, timeElapsed):
        lowestStrike, highestStrike = self._calcLowestHighestStrike()
        lowerBound = lowestStrike - self.So * 0.05
        upperBound = highestStrike + self.So * 0.05
        
        underlying = np.linspace(lowerBound, upperBound, 100)
        payout = []
        
        for Sn in underlying:
            payout.append(self.evaluateSpread(Sn, volatility, timeElapsed))
            
        payout = np.array(payout)
        
        plt.figure(1)
        plt.plot(underlying, payout, 'g:')
        plt.plot(underlying, np.zeros(len(underlying)), 'r--')
        plt.plot()
        
    def plotSpreadHeatMap(self, volatility, timeElapsed):
        lowestStrike, highestStrike = self._calcLowestHighestStrike()
        lowerBound = lowestStrike - self.So * 0.05
        upperBound = highestStrike + self.So * 0.05
        lowerVolatility = self.sigma * .5
        upperVolatility = self.sigma * 1.5
        
        underlying = np.linspace(lowerBound, upperBound, 64)
        volatility = np.linspace(lowerVolatility,upperVolatility,64)
 
         # Create heatmap

        heatmap = []

        for v in np.flip(volatility, 0):
            row = []
            for u in underlying:
                payout = self.evaluateSpread(u, v, 20)
                row.append(payout)
            heatmap.append(row)


        extent = [lowerBound, upperBound, lowerVolatility, upperVolatility]
 
         # Plot heatmap
        plt.figure(2)
        plt.clf()
        plt.title('Spread Payout')
        plt.ylabel('volatility')
        plt.xlabel('underlying')
        plt.imshow(heatmap, extent=extent)
        plt.colorbar()
        plt.show()
    
    def _calcMaxLoss(self):
        lowestStrike, highestStrike = self._calcLowestHighestStrike()
        if (self.evaluateSpreadAtExpiration(lowestStrike - 1) < self.evaluateSpreadAtExpiration(lowestStrike)):
            self.lossLowerBound = - float("inf")
        elif (self.evaluateSpreadAtExpiration(highestStrike) > self.evaluateSpreadAtExpiration(highestStrike + 1)):
            self.lossLowerBound = - float("inf")
        else:
            MaxLoss = float("inf")
            
            for option in self.positions:
                payoutOnStrike = self.evaluateSpreadAtExpiration(option.X)
                if MaxLoss > payoutOnStrike:
                    MaxLoss = payoutOnStrike
                    
            self.lossLowerBound = MaxLoss
        
    def _calcLowestHighestStrike(self):
        lowestStrike = self.So * 2
        highestStrike = 0
        
        if len(self.positions) == 0:
            return [None, None]
            
        for option in self.positions:
            if option.X > highestStrike:
                highestStrike = option.X
            if option.X < lowestStrike:
                lowestStrike = option.X
            
        return [lowestStrike, highestStrike]
    
    
    
    