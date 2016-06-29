# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 18:46:23 2016

@author: djunh
"""

import re
import os

import pandas as pd
from bs4 import BeautifulSoup
import urllib


def get_soup(url):
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r)
    return soup


def get_next_urlSuffix(soup):
    urlReturn =''
    pattern = re.compile('Next')
    for a in soup.find_all('a', text=pattern):
        urlReturn = a['href']
        break
    return urlReturn
    #Returns none if empty
    
    
def extract_data(url , df):
    soup = get_soup(url)
    
    #Get post_id data, input into a dataframe
    pattern = re.compile('[0-9]')
    post_id_details = soup.find_all('a',{"name":True})
    for idx, value in enumerate(post_id_details):
        if re.match(pattern, value['name']):        
            df.ix[idx]['post_id'] = value['name']
            
    #Get name of post, input into dataframe
    name_details = soup.find_all('span', {"class": 'name'})
    for idx,value in enumerate(name_details):
        df.ix[idx+1]['name'] = value.find('b').getText()
    
    #Get Date of post
    for idx, value in enumerate(soup(text=re.compile('Posted:'))):
        df.ix[idx+1]['date'] = value.parent.getText()[7:][:26]
     
    #Get Body of Post
    body_details = soup.find_all('span', {"class": 'postbody'})
    for idx,value in enumerate(body_details) if value.getText() != '':
        print value.getText()
        
    return df

if __name__ == "__main__":
    path = str(os.path.dirname(os.path.realpath(__file__)))+'/data/'
    
    fields = ['post_id', 'name', 'date', 'body']
    df = pd.DataFrame(columns = fields, index = range(1,16))
    
    urlPrefix = 'http://www.oldclassiccar.co.uk/forum/phpbb/phpBB2/'
    urlSuffix = 'viewtopic.php?t=12591'
    url = urlPrefix+urlSuffix
    
    dfNew = extract_data(url,df)
    
    
    
    
    soup = get_soup(url)
    newUrl = get_next_urlSuffix(soup)
    
    