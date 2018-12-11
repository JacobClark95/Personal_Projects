import BlackScholes as bs
from interface import implements, Interface

class Option(Interface):
    
    def getOptionCost(self):
        pass
    
    def getPayoutAtExpiration(self, underlyingAtExpiration):
        pass
    
    def getPayout(self, underlying, volatility, timeElapsed):
        pass
 
    

class CallLong(implements(Option)):
    def __init__(self, underlying, strike, volatility, interestRate, timeToExpiration):
        self.So = underlying
        self.X = strike
        self.sigma = volatility 
        self.r = interestRate
        self.t = timeToExpiration 
        
        self.option = bs.BlackScholes(self.So, self.X, self.sigma, self.r, self.t)
        self.debit = - self.option.callPrice
        
    def getOptionCost(self):
        return self.debit
            
    def getPayoutAtExpiration(self, underlyingAtExpiration):
        if underlyingAtExpiration <= self.X:
            return self.debit
        else:
            return self.debit + (underlyingAtExpiration - self.X)
        
    def getPayout(self, underlying, volatility, timeElapsed):
        assert timeElapsed >= 0;
        if (timeElapsed >= self.t):
            return self.getPayoutAtExpiration(underlying)
        else:
            newOption = bs.BlackScholes(underlying, self.X, volatility, self.r, (self.t - timeElapsed))
            return self.debit + newOption.callPrice


class CallShort(implements(Option)):
    def __init__(self, underlying, strike, volatility, interestRate, timeToExpiration):
        self.So = underlying
        self.X = strike
        self.sigma = volatility 
        self.r = interestRate
        self.t = timeToExpiration 
        
        self.option = bs.BlackScholes(self.So, self.X, self.sigma, self.r, self.t)
        self.credit = self.option.callPrice
        
    def getOptionCost(self):
        return self.credit
            
    def getPayoutAtExpiration(self, underlyingAtExpiration):
        if underlyingAtExpiration <= self.X:
            return self.credit
        else:
            return self.credit - (underlyingAtExpiration - self.X)
        
    def getPayout(self, underlying, volatility, timeElapsed):
        assert timeElapsed >= 0;
        if (timeElapsed >= self.t):
            return self.getPayoutAtExpiration(underlying)
        else:
            newOption = bs.BlackScholes(underlying, self.X, volatility, self.r, (self.t - timeElapsed))
            return self.credit - newOption.callPrice


class PutLong(implements(Option)):
    def __init__(self, underlying, strike, volatility, interestRate, timeToExpiration):
        self.So = underlying
        self.X = strike
        self.sigma = volatility 
        self.r = interestRate
        self.t = timeToExpiration 
        
        self.option = bs.BlackScholes(self.So, self.X, self.sigma, self.r, self.t)
        self.debit = - self.option.putPrice
        
    def getOptionCost(self):
        return self.debit
            
    def getPayoutAtExpiration(self, underlyingAtExpiration):
        if underlyingAtExpiration >= self.X:
            return self.debit
        else:
            return self.debit + (self.X - underlyingAtExpiration)
        
    def getPayout(self, underlying, volatility, timeElapsed):
        assert timeElapsed >= 0;
        if (timeElapsed >= self.t):
            return self.getPayoutAtExpiration(underlying)
        else:
            newOption = bs.BlackScholes(underlying, self.X, volatility, self.r, (self.t - timeElapsed))
            return self.debit + newOption.putPrice



class PutShort(implements(Option)):
    def __init__(self, underlying, strike, volatility, interestRate, timeToExpiration):
        self.So = underlying
        self.X = strike
        self.sigma = volatility 
        self.r = interestRate
        self.t = timeToExpiration 
        
        self.option = bs.BlackScholes(self.So, self.X, self.sigma, self.r, self.t)
        self.credit = self.option.putPrice
        
    def getOptionCost(self):
        return self.credit
            
    def getPayoutAtExpiration(self, underlyingAtExpiration):
        if underlyingAtExpiration >= self.X:
            return self.credit
        else:
            return self.credit - (self.X - underlyingAtExpiration )
        
    def getPayout(self, underlying, volatility, timeElapsed):
        assert timeElapsed >= 0;
        if (timeElapsed >= self.t):
            return self.getPayoutAtExpiration(underlying)
        else:
            newOption = bs.BlackScholes(underlying, self.X, volatility, self.r, (self.t - timeElapsed))
            return self.credit - newOption.putPrice

    
