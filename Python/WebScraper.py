# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 21:10:48 2016

@author: Harry
"""

from bs4 import BeautifulSoup 
from selenium import webdriver
import json
import pandas
from pandas.io.json import json_normalize
import numpy as np
import sys, os
import re
pandas.set_option('display.max_colwidth',10000000)
pandas.set_option('display.max_rows', 1000000)
pandas.set_option('display.max_columns', 10000000)
import time
import csv

Italy_Serie_A = ["https://www.whoscored.com/Regions/108/Tournaments/5/Seasons/5970/Stages/12770/Fixtures/Italy-Serie-A-2015-2016", "https://www.whoscored.com/Teams/", "ItalySerieA"]
English_Premier_League = ["https://www.whoscored.com/Regions/252/Tournaments/2/England-Premier-League"]
Spain_La_Liga = ["https://www.whoscored.com/Regions/206/Tournaments/4/Spain-La-Liga", "https://www.whoscored.com/Teams/", "SpanishLaLiga"]
Germany_Bundesliga = "https://www.whoscored.com/Regions/81/Tournaments/3/Germany-Bundesliga"
columns = ['EventName', 'EventNumber', 'Value', 'EventID', 'MatchID']
index = np.arange(10000)
leagues = ['https://www.whoscored.com/Regions/206/Tournaments/4/Spain-La-Liga', 'https://www.whoscored.com/Regions/252/Tournaments/2/England-Premier-League', 'https://www.whoscored.com/Regions/108/Tournaments/5/Italy-Serie-A', 'https://www.whoscored.com/Regions/81/Tournaments/3/Germany-Bundesliga', 'https://www.whoscored.com/Regions/74/Tournaments/22/France-Ligue-1' ]

def team_getter(competition):
    print "Getting teams for" +str(competition)
    browser = webdriver.Firefox()
    browser.get(competition[0])
    content = browser.page_source
    browser.close()
    full_html = str(BeautifulSoup(content, 'lxml'))
    team_name_regex = re.compile('\[\d+\,\d+\,\'\w+\,\s\w+\s\d+\s\d{4}\'\,\'\d+\:\d+\'\,\d+\,\'[a-zA-Z0-9_ ]*\'\,\d+\,(\d+)')
    team_list = set(team_name_regex.findall(full_html))
    return team_list
    
def match_id_getter(leagues):
    gottenids = open('D:/gottenids', 'rb+')
    reader = csv.reader(gottenids)
    list1 = reader.next()
    match_ids = []
    for item in leagues:      
        browser = webdriver.Firefox()
        browser.get(item)
        content = browser.page_source 
        browser.close()
        full_html = unicode(str(BeautifulSoup(content, 'lxml')), errors='ignore')
        match_id_regex = re.compile('"\w\s\w"\sid="(\d+)"')
        match_id_set = (set(match_id_regex.findall(full_html)))
        for match_id in match_id_set:
            if match_id not in list1:
                match_ids.append(match_id)   
    gottenids.close()
    return match_ids


def match_getter(competition, team):
    print "Getting match_ids for" + str(team)
    browser = webdriver.Firefox()
    browser.get(competition[1]+team+'/Fixtures')
    content = browser.page_source 
    browser.close()
    full_html = unicode(str(BeautifulSoup(content, 'lxml')), errors='ignore')
    match_id_regex = re.compile('\[(\d+)\,\d+\,\'\d+\-\d+\-\d+\'\,\'\d+\:\d+\'')
    match_ids = set(match_id_regex.findall(full_html))
    time.sleep(5)
    return match_ids

def data_filter(data):
    split_data = data.split('var matchCentreData = ')[1]
    split_data_2 = str(split_data.split('var matchCentreEventTypeJson =')[0])
    jsondata = split_data_2[:-10]
    return jsondata
    
def scrape_match_data(matchlist):
    #gottenids = open('D:/gottenids', 'rb+')
    browser = webdriver.Firefox()
    for match_id in matchlist:
        try:
            target_url = "https://www.whoscored.com/Matches/" + str(match_id) + "/Live"
            #print "Scraping" + str(target_url)
            browser.get(target_url)
            content = browser.page_source
            full_html = BeautifulSoup(content, 'lxml')
            match_data_html = full_html.find_all("script", {"type": "text/javascript"})
            match_name_html = full_html.find("title")
            match_name = str.strip(str(match_name_html.text))
            
            metamatch = re.compile('\/Regions\/\d+\/Tournaments\/\d+\/Seasons\/\d+')
            extract = re.compile('>(\w+\s\w+\s\-\s\d+\/\d+)<')
            extract2 = re.compile('>(\w+\s-\s\d+\/\d+)<')
            extract3 = re.compile('>(\w+\s\d+\s\-\s\d+\/\d+)<')
            matchmetadata = str(full_html.find(attrs={"href" : metamatch}))
            folderpath = extract.search(matchmetadata)
            
            if folderpath is None:
                folderpath = extract2.search(matchmetadata)
            if folderpath is None:
                folderpath = extract3.search(matchmetadata)
                
            countrycode = (matchmetadata.split('Regions/')[1]).split('/Tournaments')[0]
            foldernamedata = str(folderpath.group(1))

            leaguename = str.strip(foldernamedata.split('-')[0])
            year = str.strip(foldernamedata.split('-')[1])[:4]
            
            match_data = str(match_data_html)
            json_data = data_filter(match_data)
            match_data = json.loads(unicode(json_data, "ISO-8859-1"))
            normalized_data = json_normalize(match_data['events'])
            normalized_data.insert(0, 'MatchID', match_id)
            num_events = normalized_data['qualifiers'].count()-2
            qualifiers = pandas.DataFrame(columns=columns, index=index)
            
            writenum = -1
            for num in range(num_events):
                numDicts =  len(normalized_data['qualifiers'][num])
                for num2 in range(numDicts):
                    writenum = writenum + 1
                    tempdataframe = pandas.DataFrame(normalized_data['qualifiers'][num][num2], columns=['type','value']) 
                    qualifiers['EventName'][writenum] = tempdataframe['type'][0]
                    qualifiers['EventNumber'][writenum] = tempdataframe['type'][1]
                    qualifiers['Value'][writenum] = tempdataframe['value'][0]
                    qualifiers['EventID'][writenum] = num
                    qualifiers['MatchID'][writenum] = match_id
            data_path = os.path.dirname("D:/FootballData/" + countrycode + "/" + leaguename + "/" + str(year) + "/")
            qualifiers_path = data_path + "/qualifiers"
            if not os.path.exists(data_path):
                os.makedirs(data_path)
            if not os.path.exists(qualifiers_path):
                os.makedirs(qualifiers_path)
            qualifiers = qualifiers[qualifiers.EventID >= 0]
            playerData = pandas.DataFrame.from_dict(normalized_data)
            playerData = playerData.drop('qualifiers', 1)
            playerData.to_csv(data_path + "/" + match_name,encoding = "ISO-8859-1")
            qualifiers.to_csv(qualifiers_path +  "/" + match_name , encoding = "ISO-8859-1")
            #gottenids.write(str(match_id)+',')
            print "Done!"
            time.sleep(5)
        except Exception as inst:
           print(type(inst))    # the exception instance
           print(inst.args)     # arguments stored in .args
           print(inst)  
           exc_type, exc_obj, exc_tb = sys.exc_info()
           fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
           print(exc_type, fname, exc_tb.tb_lineno)
           pass
        except TypeError:
           print Exception
           pass
    browser.close()

def season_scraper(competition):
    teams = team_getter(competition)
    wanted_ids = []
    for team in teams:
        ids = match_getter(competition, team)
        wanted_ids.append(ids)
    with open(str(competition[2])+".csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerow(wanted_ids)

#temp = 
#matches_to_get =  match_id_getter(English_Premier_League) 
with open('D:/laliga201617') as temp:
    scrape_match_data(temp)
    