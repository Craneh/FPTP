# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 23:36:51 2016

@author: Harry
"""
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas
import urllib2
import re


browser = webdriver.Firefox()
browser.get("http://www.racingpost.com/horses/result_home.sd?race_id=665589&r_date=2016-12-16&popup=yes#results_top_tabs=re_&results_bottom_tabs=ANALYSIS")
content = browser.page_source

soup = bs(content)

horsedata =  soup.findAll('tbody')
print horsedata
odds_regex = re.compile('(\d+\/\d+).{1,2}(<\/span|<img)')
weight_regex = re.compile('<span>(\d+-\d+)')
stall_regex = re.compile('<span class="draw">(\d+)</span> </td>')
result_regex = re.compile('<h3>(\d+)\s</h3>')
Odds = odds_regex.findall(str(horsedata))
Stall = stall_regex.findall(str(horsedata))
Weight = weight_regex.findall(str(horsedata))
Results = result_regex.findall(str(horsedata))
print Stall
print Odds
print Weight
print Results