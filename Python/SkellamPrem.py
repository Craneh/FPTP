# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 19:30:15 2016

@author: Harry
"""

import pandas as pd
from scipy.stats import skellam
from scipy.stats import poisson
from itertools import chain
import numpy as np

shotdata = pd.read_csv('C:/Users/Harry/Documents/premierleagueratings.csv', index_col="Team", names = ["Team", "OTD","GF","GA"])

fixturedata = pd.read_csv('C:/Users/Harry/Documents/premfixutes.csv')
fixturedata.columns=["MatchID","Gameweek","Home_Team","Away_Team"]

scores = []

for number in range(5):
    for number2 in range(5):
        scores.append(str(number2)+"-"+str(number))
print scores

Gwf = fixturedata[fixturedata['Gameweek']==8]
Odds =  pd.DataFrame(columns=('Home','HomeWin','Draw','AwayWin','Away'))
Goals =  pd.DataFrame(columns=('Home','HomeWin','Draw','AwayWin','Away'))
n=0
for Home, Away in zip(Gwf['Home_Team'], Gwf['Away_Team']):

    HomeFor = float(shotdata.ix[Home, 'GF'])
    HomeAg = float(shotdata.ix[Home, 'GA'])
    AwayFor = float(shotdata.ix[Away, 'GF'])
    AwayAg = float(shotdata.ix[Away, 'GA'])
    list1 = []
    array1 = np.zeros((5,5))
    Homexg = ((HomeFor/1.22)*(AwayAg/1.22)*1.35)
    Awayxg = ((AwayFor/1.22)*(HomeAg/1.22)*1.09)
    Draw = 1/skellam.pmf(0,Homexg, Awayxg)
    AwayWin = 1/skellam.cdf(-1,Homexg, Awayxg)
    HomeWin = 1/skellam.cdf(-1,Awayxg,Homexg)
    list1.append(Home)
    list1.append(HomeWin)
    list1.append(Draw)
    list1.append(AwayWin)
    list1.append(Away)
    Odds.loc[n] = (list1)
    n=n+1
    for n2 in range(5):
        for i in range(5):
            array1[n2][i] = poisson.pmf(n2,Homexg) * poisson.pmf(i,Awayxg)
    l = chain.from_iterable(zip(*array1))
    y = 0
    for item in l:
        print str(1/item) + " " + str(Home) + " " + scores[y] + " " + str(Away)
        y = y + 1
        if y == 25:
            y = 0
        

print Odds

