import numpy as np
from scipy.stats import norm


class BlackScholes():
    def __init__(self, underlying, strike, volatility, interestRate, timeToExpiration):
        self.So = underlying
        self.X = strike
        self.sigma = volatility / (100 * np.sqrt(252))
        self.r = interestRate / 100
        self.t = timeToExpiration
        self.d1 = 0
        self.d2 = 0
        
        self.callPrice = 0
        self.putPrice = 0
        
        self.deltaCall = 0
        self.deltaPut = 0
        self.vega = 0
        
        self._calcD1()
        self._calcD2()
        self._calcPrices()
        self._calcGreeks()
        
        
    def _calcD1(self):
        self.d1 = (np.log(self.So/self.X) + self.t * (self.r / 365 + (self.sigma ** 2) / 2)) / (self.sigma * np.sqrt(self.t))
        
    def _calcD2(self):
        self.d2 = self.d1 - self.sigma * np.sqrt(self.t)
    
    def _calcPrices(self):
        self.callPrice = self.So * norm.cdf(self.d1) - self.X * np.exp(-self.r * self.t / 365) * norm.cdf(self.d2)
        self.putPrice =  - self.So * norm.cdf( - self.d1) + self.X * np.exp(-self.r * self.t / 365) * norm.cdf(- self.d2)
       
    def _calcGreeks(self):
        self.deltaCall = norm.cdf(self.d1)
        self.deltaPut = (norm.cdf(self.d1) - 1) 
        self.vega = (1/100)  * np.sqrt(self.t) * (1 / (2 * np.pi)) * np.exp(((-self.d1) ** 2) / 2)
   











     