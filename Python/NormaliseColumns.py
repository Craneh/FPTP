# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 20:38:20 2015

@author: Hazza
"""
import pandas as pd
import os
import numpy as np
import csv
import codecs
gameweek = 2
dir = "D:/FootballData/206/La Liga/2016/GameWeek"+str(gameweek)
EventTypes = ['shotSixYardBox','shotPenaltyArea','shotOboxTotal','shotOpenPlay','shotCounter',
'shotSetPiece','shotOffTarget','shotOnPost','shotOnTarget','shotsTotal','shotBlocked','shotRightFoot',
'shotLeftFoot','shotHead','shotObp','goalSixYardBox','goalPenaltyArea','goalObox','goalOpenPlay',
'goalCounter','goalSetPiece','penaltyScored','goalOwn','goalNormal','goalRightFoot','goalLeftFoot',
'goalHead','goalObp','shortPassInaccurate','shortPassAccurate','passCorner','passCornerAccurate',
'passCornerInaccurate','passFreekick','passBack','passForward','passLeft','passRight','keyPassLong',
'keyPassShort','keyPassCross','keyPassCorner','keyPassThroughball','keyPassFreekick','keyPassThrowin',
'keyPassOther','assistCross','assistCorner','assistThroughball','assistFreekick','assistThrowin','assistOther',
'dribbleLost','dribbleWon','challengeLost','interceptionWon','clearanceHead','outfielderBlock',
'passCrossBlockedDefensive','outfielderBlockedPass','offsideGiven','offsideProvoked','foulGiven',
'foulCommitted','yellowCard','voidYellowCard','secondYellow','redCard','turnover','dispossessed',
'saveLowLeft','saveHighLeft','saveLowCentre','saveHighCentre','saveLowRight','saveHighRight',
'saveHands','saveFeet','saveObp','saveSixYardBox','savePenaltyArea','saveObox','keeperDivingSave',
'standingSave','closeMissHigh','closeMissHighLeft','closeMissHighRight','closeMissLeft','closeMissRight',
'shotOffTargetInsideBox','touches','assist','ballRecovery','clearanceEffective','clearanceTotal',
'clearanceOffTheLine','dribbleLastman','errorLeadsToGoal','errorLeadsToShot','intentionalAssist',
'interceptionAll','interceptionIntheBox','keeperClaimHighLost','keeperClaimHighWon','keeperClaimLost',
'keeperClaimWon','keeperOneToOneWon','parriedDanger','parriedSafe','collected','keeperPenaltySaved',
'keeperSaveInTheBox','keeperSaveTotal','keeperSmother','keeperSweeperLost','keeperMissed','passAccurate',
'passBackZoneInaccurate','passForwardZoneAccurate','passInaccurate','passAccuracy','cornerAwarded','passKey',
'passChipped','passCrossAccurate','passCrossInaccurate','passLongBallAccurate','passLongBallInaccurate',
'passThroughBallAccurate','passThroughBallInaccurate','passThroughBallInacurate','passFreekickAccurate',
'passFreekickInaccurate','penaltyConceded','penaltyMissed','penaltyWon','passRightFoot','passLeftFoot','passHead'
,'sixYardBlock','tackleLastMan','tackleLost','tackleWon','cleanSheetGK','cleanSheetDL','cleanSheetDC',
'cleanSheetDR','cleanSheetDML','cleanSheetDMC','cleanSheetDMR','cleanSheetML','cleanSheetMC','cleanSheetMR',
'cleanSheetAML','cleanSheetAMC','cleanSheetAMR','cleanSheetFWL','cleanSheetFW','cleanSheetFWR','cleanSheetSub',
'goalConcededByTeamGK','goalConcededByTeamDL','goalConcededByTeamDC','goalConcededByTeamDR','goalConcededByTeamDML'
,'goalConcededByTeamDMC','goalConcededByTeamDMR','goalConcededByTeamML','goalConcededByTeamMC',
'goalConcededByTeamMR','goalConcededByTeamAML','goalConcededByTeamAMC','goalConcededByTeamAMR',
'goalConcededByTeamFWL','goalConcededByTeamFW','goalConcededByTeamFWR','goalConcededByTeamSub',
'goalConcededOutsideBoxGoalkeeper','goalScoredByTeamGK','goalScoredByTeamDL','goalScoredByTeamDC',
'goalScoredByTeamDR','goalScoredByTeamDML','goalScoredByTeamDMC','goalScoredByTeamDMR','goalScoredByTeamML',
'goalScoredByTeamMC','goalScoredByTeamMR','goalScoredByTeamAML','goalScoredByTeamAMC','goalScoredByTeamAMR',
'goalScoredByTeamFWL','goalScoredByTeamFW','goalScoredByTeamFWR','goalScoredByTeamSub','aerialSuccess',
'duelAerialWon','duelAerialLost','offensiveDuel','defensiveDuel','bigChanceMissed','bigChanceScored',
'bigChanceCreated','overrun','successfulFinalThirdPasses','punches','penaltyShootoutScored',
'penaltyShootoutMissedOffTarget','penaltyShootoutSaved','penaltyShootoutSavedGK','penaltyShootoutConcededGK',
'throwIn','subOn','subOff','defensiveThird','midThird','finalThird','pos']

def directorybuilder(directory, gameweeknumber):
    return str(directory)+'/GameWeek'+str(gameweeknumber)
def NormaliseColumns(gameweekdir):
    list1 = []
    for i in os.listdir(gameweekdir):
        data = pd.read_csv(gameweekdir+'/'+i, index_col=0) 
        list1 = data.keys()
        if list1[0] != 'MatchID':
            data.insert(0, 'MatchID', np.nan)
            list1 = data.keys()
        if list1[1] != 'blockedX':
            data.insert(1, 'blockedX', np.nan)
            list1 = data.keys()
        if list1[2] != 'blockedY':
            data.insert(2, 'blockedY', np.nan)
            list1 = data.keys()
        if list1[3] != 'cardType.displayName':
            data.insert(3, 'cardType.displayName', np.nan)
            list1 = data.keys()
        if list1[4] != 'cardType.value':
            data.insert(4,'cardType.value', np.nan)
            list1 = data.keys()
        if list1[5] != 'endX':
            data.insert(5, 'endX', np.nan)
            list1 = data.keys()
        if list1[6] != 'endY':
            data.insert(6, 'endY', np.nan)
            list1 = data.keys()
        if list1[7] != 'eventId':
            data.insert(7, 'eventId', np.nan)
            list1 = data.keys()
        if list1[8] != 'expandedMinute':
            data.insert(8, 'expandedMinute', np.nan)
            list1 = data.keys()
        if list1[9] != 'goalMouthY':
            data.insert(9, 'goalMouthY', np.nan)
            list1 = data.keys()
        if list1[10] != 'goalMouthZ':
            data.insert(10, 'goalMouthZ', np.nan)
            list1 = data.keys()
        if list1[11] != 'id':
            data.insert(11, 'id', np.nan)
            list1 = data.keys()
        if list1[12] != 'isGoal':
            data.insert(12, 'isGoal', np.nan)
            list1 = data.keys()
        if list1[13] != 'isOwnGoal':
            data.insert(13, 'isOwnGoal', np.nan)
            list1 = data.keys()
        if list1[14] != 'isShot':
            data.insert(14, 'isShot', np.nan)
            list1 = data.keys()
        if list1[15] != 'isTouch':
            data.insert(15, 'isTouch', np.nan)
            list1 = data.keys()
        if list1[16] != 'minute':
            data.insert(16,'minute', np.nan)
            list1 = data.keys()
        if list1[17] != 'outcomeType.displayName':
            data.insert(17,  'outcomeType.displayName', np.nan)
            list1 = data.keys()
        if list1[18] != 'outcomeType.value':
            data.insert(18, 'outcomeType.value', np.nan)
            list1 = data.keys()
        if list1[19] != 'period.displayName':
            data.insert(19, 'period.displayName', np.nan)
            list1 = data.keys()
        if list1[20] != 'period.value':
            data.insert(20, 'period.value', np.nan)
            list1 = data.keys()
        if list1[21] != 'playerId':
            data.insert(21, 'playerId', np.nan)
            list1 = data.keys()
        if list1[22] != 'relatedEventId':
            data.insert(22, 'relatedEventId', np.nan)
            list1 = data.keys()
        if list1[23] != 'relatedPlayerId':
            data.insert(23, 'relatedPlayerId', np.nan)
            list1 = data.keys()
        if list1[24] != 'satisfiedEventsTypes':
            data.insert(24, 'satisfiedEventsTypes', np.nan)
            list1 = data.keys()
        if list1[25] != 'second':
            data.insert(25, 'second', np.nan)
            list1 = data.keys()
        if list1[26] != 'teamId':
            data.insert(26, 'teamId', np.nan)
            list1 = data.keys()
        if list1[27] != 'type.displayName':
            data.insert(27, 'type.displayName', np.nan)
            list1 = data.keys()
        if list1[28] != 'type.value':
            data.insert(28, 'type.value', np.nan)
            list1 = data.keys()
        if list1[29] != 'x':
            data.insert(29,'x', np.nan)
            list1 = data.keys()
        if list1[30] != 'y':
            data.insert(30, 'y', np.nan)
            list1 = data.keys()
        data.to_csv(gameweekdir+'/'+i)
        
def removeheaders(gameweekdir):
    read_files = os.listdir(gameweekdir)
    for i in read_files:
        if i == read_files[0]:
            pass
        else:   
           with open(gameweekdir+'/'+i, 'r') as fin:
                data = fin.read().splitlines(True)
               # headerline = data[0]
           with open(gameweekdir+'/'+i, 'w') as fout:
                fout.writelines(data[1:])  
            
def mergefiles(gameweekdir):
    read_files = os.listdir(gameweekdir)
    with codecs.open(gameweekdir+'/result.txt', "a", "utf-8") as outfile:
        for f in read_files:
            with open(gameweekdir+'/'+f, "rb") as infile:
                outfile.write(infile.read())
                
                
def addeventtypes(gameweekdir):
    data = pd.read_csv(gameweekdir+'/result.txt', index_col=0)
    list1 = data.keys()    
    n=0
    while n < len(EventTypes)-3:      
        for item in EventTypes:
            data.insert(31+n, EventTypes[n], np.nan)
            list1 = data.keys()
            print len(EventTypes)
            print list1
            print n
            n=n+1       
    data.to_csv(gameweekdir+'/result.txt')
 
def addevents(targetname, csvfile):
    target = open(targetname, 'a')
    csvdata = open(csvfile, 'r')
    reader = csv.reader(csvdata)
    for row in reader:
        if row[25] == "satisfiedEventsTypes":
            pass
        else:
            try:
                satisfiedeventtypes = row[25]
                satisfiedeventtypes = satisfiedeventtypes[1:-1]
                ids = satisfiedeventtypes.split(',')
                for item in ids:
                    if len(item) > 0:
                        row[32+int(item)] = 1                       
            except Exception,e:
                print str(e)
        del(row[25])
        target.write(str(row).replace("'", "").replace(" ", "")[1:-1]+'\n') 
    target.close()
        
def addeventtypevalues(gameweekdir, filename):   
    targetname = gameweekdir+'/'+filename
    csvfile = gameweekdir+'/result.txt'
    addevents(targetname, csvfile)

        
def main(directory, gameweeknumber, filename):
    gameweekdir = directorybuilder(directory,gameweeknumber)
    NormaliseColumns(gameweekdir)
    removeheaders(gameweekdir)
    mergefiles(gameweekdir)
    addeventtypes(gameweekdir)
    addeventtypevalues(gameweekdir, filename)
    
main("D:/FootballData/206/La Liga/2016", str(gameweek),'GameWeek'+str(gameweek) )

    
